# The three engine changes wanted before M9

`ENGINE_CHANGES.md` is the request; this is what happened. All three items are done.

**To understand this, start by reading `ENGINE_CHANGES.md`, then this file, then
`src/easel/regions.py` (`_centre_and_radii`, `Polygon.inset`) and
`src/easel/session.py` (`_trial_session`, `_plan_specs`, `rehearse`).**

```
probe_blob_radii.py     item 1, both rules measured and painted. Writes blob_radii.png
probe_rehearsed_mass.py item 2, the rehearsal against the painting. Writes rehearsed_mass.png
probe_inset.py          item 3, the concave defect and the 2.7x that is not one.
                        Writes inset_shapes.png
```

`pytest` is **279 passed, 3 skipped** (273 + 6 new). **No golden moved and none was
regenerated.** `ruff check` is clean. Everything the repo judges a change on is byte
for byte what this source tree produced before it — compared against a worktree at
`HEAD` rather than against the committed PNGs, which differ from *both* by one level on
0.1% of pixels because of the numpy/Pillow on this machine:

| | |
|---|---|
| the seven golden images | identical, none regenerated |
| `samples/brushes.png` (1802×2708) | byte for byte identical |
| `samples/shapes.png` | byte for byte identical |
| `m8/boxes.png`, `m8/shapes.png` | byte for byte identical |
| `m7/repaint.py` — the 295-stroke copy | byte for byte identical |
| `rehearsal/check_guide_blocks.py` | 37 ok, 0 failed |
| `examples/exercises.py` | runs clean |

```bash
python m7/repaint.py out.png            # and again from a worktree at HEAD
python scripts/make_shape_sampler.py    # then compare samples/shapes.png
```

---

## 1. `blob(region, radius)` — took option (a)

**One radius means a circle wherever the shape is put.** `_centre_and_radii` had two
branches that disagreed, and now has one rule: a radius given on its own sets both, a
radius left out falls back to the other, and neither given takes the place's own
half-extents. `ry` alone now works too — it used to leave the width at the region's
half-width or, on a point, at the hard-coded `0.15`.

Three reasons for (a) over (b):

* **The docstring already promised it.** `ellipse` said "`ry` defaults to `rx`, which
  makes a circle on a square canvas" while the region branch did something else. This
  is a code-versus-doc disagreement, not a design choice anyone made.
* **(b) needs guide edits and (a) does not.** Guide changes are explicitly not this
  task's, and (b) would have required two of them.
* **Look at `blob_radii.png`.** The old behaviour did not return an odd ellipse, it
  returned *a flat horizontal bar four cells wide and one cell tall* — the exact
  artefact this repo has been fighting since `rehearsal3/unprompted/`. The shape
  helper a painter reaches for to escape horizontal bands was manufacturing one.

**Nothing in the corpus passed one radius to a region**, so the change moved no test,
no golden and no sample sheet. The only call anywhere that did is
`rehearsal5/unprompted/p1/probe.py`, a rehearsal probe, and it was probing this defect.

### Where the guide is now wrong about the engine

Guide changes are not mine; these are for whoever picks them up.

* **`PAINTER.md:543`** — `blob(cell("D5"), 0.22, wobble=0.3, seed=2)` is commented *"an
  irregular mass filling a cell"*. **It still is not, under either rule**, and this is
  the part `ENGINE_CHANGES.md` did not spot: `0.22` is a *radius*, so the mass is 0.44
  across against a cell's 0.125 — 3.9 cells wide, and it was 3.9 cells wide before the
  fix too. Option (a) makes it round; it cannot make it small. The call that fills a
  cell is `blob(cell("D5"), wobble=0.3, seed=2)` with no radius at all, which is what
  the same guide says correctly at line 1041. If a radius is wanted in the example it
  should be about `0.06`.
* **`PAINTER.md:61`** — `blob(cell("D5"), 0.26, ...)` in the workflow section is now a
  round mass about 4.6 cells across. Nothing there claims it fills a cell, and a large
  first mass is the point of that passage, so it reads better than it did; worth a look
  rather than an edit.
* **`PAINTER.md:1032`** — the signature line says `blob(place, radius, wobble=0.25,
  seed=0)`. The default is `wobble=0.22`.

## 2. `rehearse()` and a mass — the gap was half the size the request thought

`ENGINE_CHANGES.md` says `block_in()` and `sweep()` are both un-rehearsable. **M8
already added `block_in`**: `rehearse([{"shape": ..., "brush": ..., "direction": ...}])`
has worked since commit `0b43c95`, and `_plan_specs` was written for exactly that. Two
real gaps remained, and the second one is why the first was not enough.

**`sweep` could not be described at all.** It raised *"A stroke spec needs 'points'"*.
It now takes the same shape as a block-in mass, with the boundary under `edge=`:

```python
s.rehearse({"edge": edge, "into": "down", "depth": 0.30, "cross": 25,
            "brush": "bristle", "color": "dark", "size": 0.12})
```

`preview()` takes it too, and draws the *ground the sweep would cover* — the band from
the edge to `depth`, on the side the mass is on — rather than the edge, which would
answer the wrong question. `_sweep_cover` builds that outline from the same helpers
the sweep itself uses.

**What was rehearsed was not what landed.** This is the one that mattered. A
block-in's and a sweep's pass wander comes from the session's running generator, and
`_trial_session` deliberately gave the trial a *different* stream, on the grounds that
a rehearsal must not consume the real one. So the rehearsal showed the right masses in
the right places with a different hand — `NOTES.md` note 23 recorded that and told you
not to write a test for equality.

The fix is one line of intent: the trial gets its own generator *object* holding a
**copy of the real session's stream state**. A copy draws exactly what the real call
would draw next, and spending it costs the real session nothing, which is what the
separate stream was protecting in the first place.

```
  mass: 11 strokes,  pixels that differ 0,  max delta 0
 sweep: 19 strokes,  pixels that differ 0,  max delta 0

after two rehearsals, the painting that follows is identical: True
the rehearsals cost 0 marks and 0 log records
```

Both promises hold: **a rehearsed mass is now pixel-identical to the painted one**, and
rehearsing still writes nothing and changes nothing after it. `rehearsed_mass.png` is
the four panels; the test is
`test_rehearsing_a_mass_shows_the_paint_without_spending_it`, whose overlap assertion
is now an equality assertion.

The alternative fix — seeding the pass wander per stroke index, the way `stroke()` is
seeded — is the more thorough one and would also stop a mass depending on how much
randomness earlier calls happened to consume. It moves every golden that contains a
`block_in`, for no visible gain, so it is not what landed. It is the right change if
that fragility ever bites for its own sake.

**`NOTES.md` note 23 is now false and has been rewritten.** `ENGINE_CHANGES.md` says
the note is in `CALIBRATION.md`; it is not, and `CALIBRATION.md` never claimed this.
What `CALIBRATION.md` *does* say about masses — that passes step
`size × (1 − 0.45 × density)` apart — is still true and now lives in one function,
`_pass_step`, instead of being written out three times.

## 3. `inset()` shrinking by 2.7× — reproduced, and it is two different things

**The 2.7× is real and it is not a defect.** It reproduces on a five-pointed star:
`inset(0.045)` takes 0.24 off the width, 2.66× the 0.09 asked for. A mitre offset moves
every *edge* in by the amount, so a *tip* must move in by `amount / sin(half-angle)` for
that to be true — which is the morphological erosion, and exactly where a brush of that
reach has to stop. That is what `inset` is for (`PAINTER.md` teaches it as "inset the
shape by half the brush size"), so **the arithmetic is untouched**. The docstring now
says a tip retreats up to about three times the amount and points at `scaled()`, which
is the call for taking a fixed fraction off a mass. A painter who hit this on a lobed
blob experienced a documentation defect.

**The concave case was a real defect, and a different one.** The fold check asked
whether the offset shape's *centre* was still inside the original. A horseshoe does not
contain its own centroid — the centroid sits in the gap — so the check failed for a
reason with nothing to do with the offset, threw away a perfectly good mitre, and fell
back to scaling about a point outside the mass:

```
shape       centroid  old area  out   new area  out   width taken off
square            in    0.0961    0     0.0961    0      0.090 = 1.00x asked
lobed             in    0.2199    0     0.2199    0      0.107 = 1.18x asked
star              in    0.0105    0     0.0105    0      0.239 = 2.66x asked
horseshoe    OUTSIDE    0.1712    4     0.0846    0      0.090 = 1.00x asked
```

`out` is how many of the inset shape's own points ended up **outside the shape it had
been asked to shrink**. Four of eight. In `inset_shapes.png` the old outline seals the
mouth of the horseshoe: it covers ground the original never did.

The check now tests containment of the *points* — a shrunk shape lies inside the
original, a grown one contains it — which is the invariant that was actually wanted and
does not care whether a shape contains its own centroid. Over a corpus of 452
shape/amount pairs (convex, concave, star, lobed blob at five point-counts and four
wobbles, ribbons, a thin sliver) the only results that change are the shapes whose
centroid is outside them, and the only remaining non-containment is a tapered ribbon
inset by twice its narrow end, which is the documented "shrunk past its own width
collapses to a sliver" case.

**This was not changed on the strength of the report.** The report is about the star,
which is correct behaviour; this is a separate thing found while looking for the shape
the report guessed at, and it is reproducible in four lines.

---

## Files touched

```
src/easel/regions.py    _centre_and_radii rewritten to one rule; ellipse/blob
                        docstrings; Polygon.inset's fold check and docstring
src/easel/session.py    _trial_session copies the stream state (and _REHEARSAL_STREAM
                        is gone with it); _pass_step and _sweep_cover added and used
                        by block_in/sweep/preview; _plan_specs takes an `edge=` entry;
                        _preview_entry/_preview_sweep; rehearse lays a sweep;
                        preview/rehearse docstrings
tests/test_shapes.py    six new tests: the radii rule both ways, the no-radius case,
                        a rehearsed sweep, a previewed sweep, the horseshoe inset, and
                        the star's tip retreat. The rehearsed-mass overlap assertion
                        is now equality.
engine_changes/         this write-up and the three probes
NOTES.md                note 23 rewritten; file map and phase table
```
