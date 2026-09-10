# Engine changes wanted before M9

**Read this file, then `PAINTER.md` and `CALIBRATION.md` for what the API promises,
then the source it names. You do not need to read the rehearsal write-ups.** Everything
you need from them is quoted here.

Easel is a headless painting engine for agents. Its milestones run M1–M8b (done) and
end at M9, an MCP server. The brief's rule is that **anything changing the API lands
before M9**, because the server exposes it. This file is that list. There are three
items: one confirmed defect, one API gap two independent sessions asked for unprompted,
and one unreproduced report.

Every one of these was found by a fresh session painting a picture, not by the test
suite. The suite is 276 tests and passes throughout.

## Ground rules for this work

- **`pytest -q` must stay green** — 276 passed, 3 skipped, about 100 s.
- **A golden image failing is an instruction to look, not to regenerate.** The test
  writes `tests/golden/<case>.actual.png` beside the stored one. Open both.
  `python scripts/make_golden.py <case>` only after deciding the new marks are better,
  and say so in the write-up.
- **Judge a change on a picture, not only on a hash.** `python scripts/make_brush_sampler.py`
  and `python scripts/make_shape_sampler.py` regenerate the sheets in `samples/`; look
  at them. The repo's standing lesson is that every defect worth fixing was found by
  looking and none by the suite.
- Determinism is load-bearing: same seed, same script, same PNG, and `s.replay()`
  must reproduce an export byte for byte. There are tests for this; do not weaken them.
- No nullable-heavy or defensive rewrites. Match the surrounding style.

---

## 1. `blob(region, radius)` is a horizontal sausage — confirmed defect

**Where:** `src/easel/regions.py`, `_centre_and_radii` (about line 799), reached from
`blob()` and `ellipse()`.

```python
def _centre_and_radii(place, rx, ry):
    if _looks_like_point(place):
        dx = 0.15 if rx is None else abs(float(rx))
        dy = dx if ry is None else abs(float(ry))          # one radius -> a circle
    else:
        r = as_region(place)
        dx = r.width * 0.5 if rx is None else abs(float(rx))
        dy = r.height * 0.5 if ry is None else abs(float(ry))   # <-- ry ignores rx
```

**The two branches disagree.** Given a *point* and one radius, you get a circle. Given a
*region* and one radius, the radius sets the width and the height silently stays at the
region's own half-height. Reproduction on any canvas — the shape is canvas-independent:

```python
from easel import blob, cell
for r in (0.02, 0.05, 0.10, 0.22, 0.26):
    b = blob(cell("D5"), r, wobble=0.3, seed=2)
    xs = [p[0] for p in b.points]; ys = [p[1] for p in b.points]
    print(r, round(max(xs)-min(xs), 4), round(max(ys)-min(ys), 4))
```

```
0.02  0.0444 0.1176      cell("D5") is 0.125 x 0.125
0.05  0.1109 0.1176
0.10  0.2219 0.1176
0.22  0.4881 0.1176
0.26  0.5768 0.1176      <- 4.9 : 1, and the height never moved
```

`blob(cell("D5"))` with no radius gives `0.139 x 0.118`, which fills the cell correctly.

**Why it matters beyond the arithmetic.** `PAINTER.md` shows
`blob(cell("D5"), 0.22, wobble=0.3, seed=2)` commented *"an irregular mass filling a
cell"*. It is four cells wide. Two fresh sessions hit this independently; one reported
*"the guide's own example appears to be wrong"* and both worked around it by passing
`ry` explicitly. A shape helper that silently returns a 5:1 horizontal mass is also
suspect in a repo whose loudest recurring defect is that everything comes out as
horizontal bands.

**What to decide.** Either branch is defensible and the choice is yours to argue:

- **(a)** Make the region branch match the point branch: one radius means a circle,
  `dy = dx`. Consistent, and the guide's examples become true as written. It changes
  the meaning of existing calls that pass one radius to a region, so check the goldens
  and `m8/`.
- **(b)** Keep the behaviour and document it as "rx is the x-radius; pass `ry` for the
  other". Then **fix both of the guide's `blob(cell(...), r)` examples**, which are
  wrong under this reading too.

**Do (a) or (b), not neither.** The guide's examples are wrong today either way, and
that is the part that is not optional. If you take (a), regenerate any golden it moves
only after looking at both images.

## 2. `rehearse()` cannot take a mass — the gap two sessions asked for

**Where:** `src/easel/session.py`, `rehearse()` (about line 989) and `preview()`
(about line 936).

`rehearse(strokes)` paints a plan on a copy of the canvas and shows the result, without
touching the real canvas or the log. It takes a list of stroke specs — the same
arguments `s.stroke()` takes. **`block_in()` and `sweep()` are not stroke specs.** They
are calls that expand into ten to thirty strokes, and there is no way to see what one
will look like before paying for it. `preview()` shows the silhouette a shape covers,
which answers *where* but not *what it will look like*.

Two fresh sessions, in unrelated runs, named this as the most expensive thing missing.
Their words:

> "the biggest gap: `rehearse` takes stroke specs, so masses — 10 to 30 strokes each —
> are exactly what you cannot try before you buy. **Every expensive mistake in this
> session was a mass; every cheap save was a stroke plan I could rehearse first.**"

> "the most expensive [thing I wanted the source for] being *can `rehearse()` take a
> mass, or only strokes?*, since every costly mistake in this session was a mass and
> `preview()` only shows the silhouette."

The cost is measurable. One of those sessions spent **198 of 299 strokes before its
subject existed, about 60 of them repainting its own mistakes** — a mass blocked in
with a brush that ate its own silhouette (72 strokes and the session's only `undo`), a
grain pass that saturated, a curved ribbon that staircased. Each was one call that could
not be tried.

**What is wanted:** `rehearse()` accepting a mass the same way it accepts strokes — a
`block_in` or `sweep` described rather than executed, painted on the copy, shown, and
costing nothing. The shape of the API is yours to design; the constraint is that what
you rehearse must be what lands, which is how `rehearse` already works for strokes
(it seeds the copy as if these were the next strokes of the real painting).

Watch for: `rehearse` is documented as costing nothing and writing nothing to the log,
and `CALIBRATION.md` records that a rehearsed mass is *not* pixel-identical to the
painted one (there is an existing note on this — find it and keep it true, or update it
with a measurement).

## 3. `inset()` shrinking by 2.7× — reported, not reproduced

One session reported `inset()` shrinking a mass by 2.7 times what it asked for, and
listed it among the three things that cost it most. **I could not reproduce it:**

```python
from easel import polygon
p = polygon([(0.3, 0.3), (0.7, 0.3), (0.7, 0.7), (0.3, 0.7)])   # 0.4 across
print(max(x for x, _ in p.inset(0.045).points) - min(x for x, _ in p.inset(0.045).points))
# 0.3100 — exactly 0.4 - 2*0.045, as documented
```

`Polygon.inset` is at `src/easel/regions.py` about line 483 and `Region.inset` about
line 102. On a convex square it is exact. It is plausible the report is real on a
**concave** shape or one whose points are close together — insetting a shape whose
width is small relative to the amount collapses it to a sliver at the centre by design,
and a painter who hit that on a lobed blob would experience it as "2.7× too much".

**Treat this as unconfirmed.** Either find a shape where it misbehaves and fix it, or
establish that the documented behaviour on thin and concave shapes is surprising enough
to be a documentation defect. Do not change the arithmetic on the strength of one
report.

---

## What is deliberately not in this list

- **Grading a mass from one value to another.** There is no gradient primitive, and a
  session painting a face said so: wet-into-wet dies in about eleven strokes,
  `round_soft` airbrushes above `size≈0.05`, `smudge` only moves what is there. The
  guide now says plainly that there is no gradient tool and teaches steps-with-softened-joins
  instead. Whether the engine should gain one is a real question and **should be argued
  on a picture first** — build the steps technique, look at it, and only then propose an
  API.
- Anything in `PAINTER.md` or `CALIBRATION.md`. Guide changes are handled separately and
  are not yours; if you find the guide wrong about the engine, say so in your write-up
  rather than editing it.

## When you are done

Write a short summary — what changed, what you decided and why, what moved in the
goldens and what you looked at before regenerating them, and any place the guide is now
wrong about the engine. Name the files you touched. Someone picks this up cold after
you.
