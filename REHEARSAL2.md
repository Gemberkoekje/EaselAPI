# M5, second rehearsal — the fresh session

**To understand this, start by reading `REHEARSAL.md` (the first rehearsal and its
verdict), then this file, then the diff to `PAINTER.md` (the deliverable), then
`rehearsal2/c1_masses.py` through `c7_speck.py` (the copy, one script per pass).**

`REHEARSAL.md` ends by saying the first rehearsal could not measure the thing the
brief asks about, because it was run by someone who had read the source, and that
the honest next step was to hand the revised guide and the same reference to a
session that had never seen the repo. This is that session. It read
`painting-api-brief.md`, `PAINTER.md`, `README.md`, `NOTES.md` and `REHEARSAL.md`,
and the output of `easel brushes`. It did not open `src/`, `REVIEW.md`, or the first
rehearsal's pass scripts until both paintings were exported. The two probe-and-fix
notes in `NOTES.md` that leak engine facts (wetness decay, the tooth gate) are also
in the guide, so they did not give it anything a fresh reader would not have.

Same reference: the photograph of a man in profile in a dim interior, gesturing.
Canvas 1200 by 800, linen, `umber_wash` ground, seed 11.

---

## The verdict first

**The copy reaches the bar the first one did not.** At 253 strokes it is a
recognisable copy of the scene: a man in profile facing left, with an eye, a nose,
a beard and a mass of hair; a raised gloved hand with spread fingers; the juice
carton with its white cap; two glasses; the lit wall; the figure in red at the
right. A viewer given both pictures would say they are the same scene and the same
pose. It is not a portrait likeness — the face is a crude profile and the hair is
a mass with streaks — and the brief asks for a *recognisable copy*, which this is.
`rehearsal2/copies_compared.png` puts the reference, the first copy and this one
side by side; the first copy is an arrangement of blobs with no face in it.

**The unprompted painting** is a dawn estuary — a mauve layered sky, a headland in
fog, a dark spit with its reflection, a path of light on the water, posts, wet
mud — 133 strokes. It has a light, a mid and a dark, lost edges and found ones, and
the ground shows through the mud. Its weakest passage is the headland, which was
first laid with a big `round_soft` and never quite stopped looking airbrushed.

Both paintings, their time-lapses and every look are in `rehearsal2/`.

## What the revised guide got right

The first rehearsal's biggest finding — that the grid has to be on both panels —
is what made this copy work. Reading the reference out loud by cell before
painting ("the coat fills D5 to H8, the shoulder is at G4, the hair fills D1 to F3,
the face is the front of D2 to D4, the hand is B4 to C6") put every mass in the
right place at the first pass, and every later correction was made by cell. The
value-planning step also did its job: the three planned values (0.23, 0.43, 0.71)
were printed before a stroke was laid and the greyscale view had three separated
masses from pass 1 on. The `edge()` sweep from the guide gave the coat a real
silhouette in nineteen strokes. Nothing in the reference workflow needed changing.

## What the rehearsal cost, in order of when it bit

| # | What happened | Fixed in |
|---|---|---|
| 1 | Every large mass came out as corduroy: the bristle comb at `size=0.18` printed the same wavy streaks across the whole background, then the hair | `PAINTER.md`, brushes |
| 2 | The red shirt spread half a cell past its region; later the water buried the spit's foot: `block_in` paints about half a brush past its region | `PAINTER.md`, measured; `overhang=` was there all along and undocumented |
| 3 | Mixed a doorway grey from ochre and cerulean and painted a bright green rectangle | `PAINTER.md`, colour, with grey recipes |
| 4 | Carved the profile with a thin dark stroke along it and got a drawn outline, the thing the guide says not to do, by a route it did not name | `PAINTER.md`, "finding an edge" |
| 5 | Wrote a `cells("E5", "H8")` helper because there was no way to name a span of cells, which is the whole vocabulary of copying; and nothing said what to import in a plain Python script | engine — `span()`; `PAINTER.md`, places |
| 6 | `look(region=cell("D2"))` returned a 150 by 100 crop, too small to check anything in | engine — small crops are enlarged |
| 7 | Long strokes ran dry at their far end and one side of the sky speckled; `load_falloff` appeared only inside two exercises | `PAINTER.md`, measured |
| 8 | Laid the far headland with a big `round_soft` and got an airbrushed blob | `PAINTER.md`, brushes table |
| 9 | A mass that made sense beside the reference (the beard, as a hook under the chin) did not make sense without it | `PAINTER.md`, checklist |

Items not charged to the guide: hair lights laid at 0.54 against a face at 0.61
turned the head to mush (the guide's value rule already covers it); a dark mouth
mark 0.02 inside the profile read as an eye; a table-edge highlight went on as a
white bar. Those were the painter's errors, and the guide had said so beforehand.

## Measurements behind the fixes

All through the public API and exported PNGs, in `rehearsal2/probe_*.py`.

- **`block_in` overshoot** (`probe_overshoot_runout.py`, `probe_overhang_wet.py`):
  a region of 0.3–0.7 blocked in at `size=0.10` is painted from 0.247 to 0.749 in
  the stroke direction and 0.281 to 0.725 across it — half a brush on the ends, a
  quarter across. `round_hard` overshoots 0.86 of a brush. `overhang=0` brings the
  ends to a fifth of a brush with coverage inside the region unchanged (0.997).
- **Run-out** (`probe_runout_strict.py`): a canvas-wide bristle stroke at
  `size=0.12` on a toned ground is 0.75 solid in its first quarter and 0.58 in its
  last on smooth, 0.60 on linen, 0.47 on rough. `load_falloff=0.25` holds it at
  0.72–0.76 throughout. A `flat` stroke stays at 0.99–1.00 on every texture. The
  block-in itself does not speckle (`probe_blockin_speckle.py`): the speckle in the
  sky came from the single long strokes laid over it.
- **Bristle solidity**: the same probe shows a fully loaded bristle stroke never
  exceeds about three-quarters coverage of its own width. That is the comb, and it
  is why a single bristle pass cannot make a solid mass.

## What changed outside `rehearsal2/`

- `PAINTER.md` — fourteen edits, listed in the table above. The largest are the
  bristle-comb paragraph, the run-out paragraph, the grey recipes, the
  "finding an edge" paragraph, the `block_in` overshoot paragraph and `span()`.
- `src/easel/regions.py` — `span(first, last)`, the rectangle covering a run of
  cells, either order, both included. Exported from `easel`, so it is in scope
  under `easel run`.
- `src/easel/look.py` — a `region=` crop whose long side is under `MIN_CROP_SIZE`
  (480 px) is enlarged to it; larger crops are untouched.
- `tests/test_engine.py` — three tests (92 total).
- `rehearsal/check_guide_blocks.py` — its preamble now imports `span` and creates
  the session with `timelapse=True`, so the guide's final block (export plus
  time-lapse) executes instead of failing on the checker's own settings.

## Gotchas for the next session

1. **Read the reference by cell before the first stroke, and correct by cell.**
   This is the whole difference between the two copies. Nothing else in the
   workflow mattered as much.
2. **`block_in` is not a fill.** It overshoots, its passes taper, and a bristle
   pass is three-quarters solid. Block in the big thing first and let the small
   thing be painted over it, or pass `overhang=0`.
3. **A thin stroke along an edge is an outline, however good the intention.** Paint
   the mass on the other side of the edge instead.
4. **Windows heredocs, again.** A 7 KB Python patch would not pass through the
   shell here; `NOTES.md` gotcha 7 still holds. Write anything large with the
   file-writing tool and run it.
5. **The checker's session settings are part of the test.** `timelapse=False` in
   the preamble failed a guide block that is fine in real use.

## Still open

- **The bristle comb is identical from stroke to stroke.** Every wide bristle mark
  prints the same set of streaks, which is why masses go to corduroy. Varying the
  comb per stroke (spacing, phase, a few missing bristles) would help every
  painting and is the one engine change this rehearsal would ask for. Not done
  here: it changes every stroke, and belongs at the start of a milestone with the
  sampler and a real painting as the evidence.
- The `flat` brush's edge scallops at large sizes (the sky bands show it). Mild,
  and possibly a feature.
- Pressure does not modulate width; golden-image tests do not exist; M6 is
  untouched. All as before.

## File map

```
rehearsal2/
  exercises/ex1.py … ex6.py    the guide's six exercises, run first, verbatim
  values_plan.py               the copy's palette, planned as numbers before painting
  c0_look.py                   the first gridded and greyscale looks at the reference
  c1_masses.py … c7_speck.py   the copy, one script per pass (79, 144, 192, 226,
                               242, 251, 253 strokes)
  copy_final.png               the copy, 253 strokes
  copy_timelapse.gif
  copies_compared.png          reference | first rehearsal's copy | this one
  own_values.py                the unprompted painting's palette, checked first
  own1.py … own4.py            the unprompted painting, one script per pass
  own_final.png                133 strokes
  own_timelapse.gif
  probe_*.py                   the measurements above
  out/                         every look, numbered, in the order they were taken
```
