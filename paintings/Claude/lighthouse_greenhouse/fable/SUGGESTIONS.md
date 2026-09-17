# A fifth session's findings

A picture painted from the split guide — `PAINTER.md`, the exercises, then `PAINTING.md`,
`RECIPES.md`, `REFERENCE.md`, and all three earlier paintings' notes and scripts, in that
order; `CALIBRATION.md` and `LESSONS.md` were read only after the painting was finished,
while writing this. The painting is `painting.png`; the notes are `NOTES.md`; the pass
scripts rebuild it byte for byte. This file is what the engine and the guide cost, in the
register [`../../../SUGGESTIONS.md`](../../../SUGGESTIONS.md) keeps: **the finding, and the
measurement behind it.**

**Each engine item has a probe in [`probes/`](probes) that reproduces it.** Run them with
`.venv/bin/python probes/<name>.py` from this directory. Two of the four findings below are
corrections to claims this same session made in chat before measuring them — that is the
`LESSONS.md` rule *check the painters' numbers* turned on its own author, and it is why
each line says what was measured rather than that it felt true.

This session read five documents and is the widest-read of the five painters, so where it
agrees with the others discount it for context; where it found something new, the probe is
the reason to believe it.

---

## The engine

### `edge="clean"` arches the contour of a mass with few corners — and it is already in a committed example

The clean-edge contour is swept along the shape's **smoothed** outline, and through two
sparse corners the spline bows outward. On a tall four-cornered tower whose top edge is at
`y=0.20`:

| fill | topmost paint above the top edge |
|---|---|
| `edge="ragged"` | **4px** — correct, half a brush |
| `edge="clean"` | **67px** — an arch standing off the top |
| `edge="clean"`, sides subdivided to 6 points each | **6px** — fixed |

It is not my geometry: the dusk example's own `tower()` polygon arches **44px** above its
top edge under `edge="clean"` on today's engine (ragged, 2px). Its committed
`painting.png` predates this and does not show it, so the regression is latent in the
repository — a rebuild of `lighthouse_dusk` today draws a bulge above its gallery that the
saved PNG does not have, which is part of the 8.8% its own notes report and attribute
elsewhere.

It cost me a full rebuild of the tower: the first pass came back with a grey dome over the
lantern that read as an arch nobody drew. The fix I used is to subdivide every side of the
tower and lit-face polygons, so the spline has collinear points to hold it straight
(`prelude.py`, `subdivide()`). **The engine fix is smaller than the workaround:** sweep the
clean contour along the polygon's actual edges, or don't smooth a contour through vertices
that are already near-collinear. `ragged` fills the same four-corner shape correctly, so
the fill's outline is fine; only the contour pass splines. Probe:
[`probes/probe_clean_contour.py`](probes/probe_clean_contour.py).

### CLI `easel undo` is not reliably lossless

Verified both directions. The painting's real detour — `run p11_last`(v1, 3 marks) → `easel
undo painting.easel 3` → `run p11_last`(v2) → `run p12` → `run p13` — produces a canvas
differing from a clean rebuild of the same final scripts by **1.06% of pixels, 0.045% by
more than 8/255, max 99**, all of it in the region painted after the undo
(`x 0.50–0.90, y 0.16–0.91`). It is not noise: rebuilding with the detour reproduces the
original working-session hash exactly, and single-shot, with-`p0_plan`, and
split-across-invocations rebuilds are all **byte-identical** to the committed PNG.

It is **not** a universal undo bug. In-process `s.undo()`, save/load with no undo, and three
separate simplified CLI-undo cases (small log, large multi-brush log, round-soft + dab like
the real v1) all restore **byte for byte**. The drift appears in the full painting and
resisted every attempt to minimize it, which points away from a simple RNG-cursor error and
toward accumulated state — the random stream or the wet-paint layer — not surviving the
CLI undo's save→undo→load boundary under conditions a real painting sets up and a toy does
not. Pinning it further needs state the engine does not expose from outside.

The mechanism is uncertain; the practice is not. **For a reproducible result, do not lean on
CLI undo mid-painting.** Edit the pass script and rebuild from the scripts, or undo
in-process where it is lossless. This is what I did — the committed `painting.png` is a clean
rebuild, not the working session. Probe:
[`probes/probe_undo_drift.py`](probes/probe_undo_drift.py) (the four-way rebuild driver;
~4 minutes, it repaints the picture four times).

### Rehearsal is genuinely side-effect-free; `pencil` is the one free verb that is not

A confirmation worth stating as a guarantee, and one small asterisk. A `bristle` stroke
laid after each free verb is byte-identical to one laid with no verb before it for
`look`, `look(values=True)`, `preview`, `rehearse`, `cost` and `compare` — so the
rehearse-everything discipline the whole engine rests on truly perturbs nothing, and that
property is worth asserting in a test rather than left implicit. The exception is
`pencil`, which advances the stream: adding or removing an underdrawing line silently
changes the texture of every stroke painted after it. Deterministic, so reproduction
holds, but a surprise for anyone who expects a buried pencil to leave no trace. Probe:
[`probes/probe_rng.py`](probes/probe_rng.py).

---

## The documentation

### "Look every 5 to 15 strokes" is written for the Python loop and does not fit `easel run`

It is the guide's one habit and its most-repeated line, and under the shell workflow the
same guide recommends for incremental work it is unfollowable: the atom there is a **pass**,
and one `block_in` or `scumble` is 10–50 strokes in a single call, looked at only when it
returns. I looked after every pass, not every 5–15 strokes, because there is no seam
between. Suggest stating the cadence in the unit the workflow actually has: **rehearse
before every pass, look after it.** The stroke-count figure is right for a held Python
session and should say so.

### There is no recipe for a volume of lit air — a beam, a shaft, a halo seen from outside

`RECIPES.md` has *a passage light in the middle* (an inward scumble, for a bloom **on a
surface**), but the green beam and the lamp's halo are a different thing: a cone of lit fog
with no surface and no edge anywhere. The only tool that renders it is the soft-round glaze
the brush table warns off masses, and I found that by rehearsing five wrong answers — a
bristle wedge (a ribbed slab), five flat rays (a fan of ribbons), lime glazes brightest at
the wrong end — to an answer the `car_wash` and `lighthouse_dusk` notes had already reached
for haze and halo. That is three sessions arriving at the same unwritten recipe. It is
worth writing: **mix the glaze close to the fog in value and hue; lay it with the soft
round tip along the axis; taper by pressure so it is narrow and bright at the source and
wide and gone at the far end.** Distinct from the inward scumble, and it earns the one place
the guide tells you not to use that brush.

### An exercise calibrates value and nothing calibrates hue

Exercise 1 is a value scale; there is no swatch exercise, and hue is where the mixing
surprises live. My first fog was green — I trusted the pigment hexes and the `at_value`
numbers without laying the mixtures next to each other, and a swatch strip I made by hand
caught it in one look. The guide says in prose that blue and yellow make green even when
you wanted grey; it has no exercise that makes you see it before the first mass. Suggest a
ninth exercise: **lay your planned mixtures as a swatch strip and look, before painting
anything.** It costs a minute and it is the hue counterpart of the value scale.

### Re-measured and did not survive: "the tower stripes are the loudest texture"

I said in chat that the pass structure striped the tower's lit face badly. Measured on the
committed painting, that face's peak-to-peak is **0.032** — exactly the `0.03` the docs
already promise for a solid `flat` block-in. The docs are right and my complaint was wrong.
What actually reads as stripes is elsewhere: the **far sea**, a `scumble` laid with `flat`
over a wide band, at **0.112** peak-to-peak — nearly four times the solid-block figure,
from the flat brush's wander scalloping a wide band. So the accurate, narrower finding is
that `scumble` with a `flat` on a wide band carries a texture cost the *quiet gradient*
recipe does not mention, and the fix is the wander controls the recipe already documents
elsewhere (`jitter`, `size_jitter`) or a bristle whose comb reads as intended incident
rather than as banding. Probe:
[`probes/probe_pass_texture.py`](probes/probe_pass_texture.py).

---

## What this session would not change

Every load-bearing thing held, and two are worth adding evidence to:

- **Rehearsal seeded as the next real strokes, and the one plan object.** Every failure in
  this painting was caught on a copy for the price of a look and cost no stroke: the beam
  five times, the halo, the lamp room, the stair read as a hose, the rock built twice, the
  fog that was green. 20 rehearsals, no repainted committed mass.
- **`at_value` and `compare({place: value})`.** About twenty-five planned values, every one
  landed to the hundredth including the ones approached from above, and the whole picture's
  value structure was carried with no photograph — all nine planned places inside `0.10` on
  the finished canvas.
- **Determinism, now that I have leaned on it hard.** Three independent clean rebuilds of
  this painting are byte-identical. That is what made the undo finding provable at all.

Also unchanged: back-to-front and the hollow-thing order; the eight exercises, repaid inside
the first pass; and the decide-then-read gate on `paintings/`, which I followed — the
subject was fixed before the repository was opened.

---

## Where the probes are, and one note on layout

- [`probes/probe_clean_contour.py`](probes/probe_clean_contour.py) — the arch, ragged vs
  clean vs subdivided, on a fresh tower and on the dusk example's own polygon.
- [`probes/probe_undo_drift.py`](probes/probe_undo_drift.py) — rebuilds this painting four
  ways and diffs each against `painting.png`.
- [`probes/probe_rng.py`](probes/probe_rng.py) — which free verbs perturb the stream.
- [`probes/probe_pass_texture.py`](probes/probe_pass_texture.py) — peak-to-peak of the pass
  structure on the tower and the sea.

**Layout note.** This painting lives in `paintings/Claude/lighthouse_greenhouse/fable/` rather than
directly under `paintings/`, at the owner's request, so `PAINTINGS.md` and `README.md` do
not index it and `p14_export.py` writes into this subfolder. If it is ever promoted to a
first-class example, that export path and the two index files are the only things to
change.
