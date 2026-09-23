# Step 6 of `PLAN-0.7.0.md`: a dry brush that streaks rather than speckles

**To understand this, start by reading the plan's workstream B, then `Canvas.stamp`,
`Canvas.drag`, `Canvas.tooth_along` and `DryComb` in `src/easel/canvas.py`,
`bristle_shares` and `tip_comb` in `src/easel/brush.py`, and `drags` in
`src/easel/stroke.py` -- and read `NOTES-step5.md` first if you have not, and
`NOTES-step2.md`, whose bench this step builds.**

Branch: `dry-brush-that-streaks`, off `main` at `044c28d` (step 5, #79).

---

## What this step was for

The painter's finding 2: *dry-brush speckle reads as dirt* -- *dark flecks in the sky,
speckled first swells, and blue specks in the surf*, at the loads the guide recommends
for a broken mark. The tooth gated a starving brush a pixel at a time, so what it left
was the weave's peaks: the sky's own crosser at `load=0.45` landed 571 pieces with a
median of 4 px. Decided (question 3): the engine, not a notice. Decided after step 2
(question 12): **B1+B2, tuned so each load lays today's paint** -- *the amount was right,
the shape was wrong* -- and after tuning, B2 and B1+B2 side by side on the crosser at
`0.45`, B1's kernel shortened on a comb if B1+B2 still read combed.

## What landed

| | |
|---|---|
| **B1, the tooth read along the travel** | `Canvas.tooth_along`: the tooth averaged over `_DRAG_ALONG` (`0.0088` of the long side, 9 px at 1024, a thread of linen) along the stroke's direction, then given back the tooth's own values rank for rank; built once per surface per ten degrees and shared with every trial copy |
| **B2, the comb running dry** | `bristle_shares` (each bristle's place in the paint, from the comb, stratified), `tip_comb` (which bristle each pixel of a stamp lies under, cached with the mask), `DryComb` (each bristle's share of the canvas, the comb matched to the stroke's share, weighed by how much of the tip each bristle is) |
| **The blend** | `Canvas.drag`: `0` at `0.9` of the load and over, `1` from `0.7` down, a smoothstep between; at `0` the stamp takes 0.6.0's lines exactly |
| **The stamp** | `travel=` and `bristles=` on `Canvas.stamp`, passed by `paint_stroke`; a mark with one position has no travel |
| **The notice** | `notices.REBUILDS` gains 0.7.0's row; `RebuildChange.moves(record, canvas)`, because whether a mark drags depends on the surface it is rebuilt on; `rebuild_moves(..., canvas)`; `_drags_dry` reads a record into `stroke.drags(canvas, points, brush, smooth)` |
| **The goldens** | `marks_linen`, `marks_rough`, `marks_smooth`, `shapes`, `sweep` and the sampler's hash, each opened before it was regenerated; `samples/brushes.png` re-rendered |
| **The probe** | `probe_handover_session.py`: "today" patches `Canvas.drag` to `0`; `rebuild(cut=True)` lays the old gate too; `--dry` (the built gate beside 0.6.0's and B2 alone, the amounts over many strokes, the sheets) and `--corpus-dry` are new; step 2's copies take the stamp's new arguments and ignore them |
| **Words** | five sentences that said *speckle* or *flecks* for what a starved brush leaves (`PAINTER.md`'s exercise 3, `PAINTING.md`'s `load` paragraph, the plane recipe's failure, its `DIAGNOSIS.md` row and the graded field's), `cover()`'s docstring, the `load` row of `REFERENCE.md`, a design note in `README.md`, two lines of `CALIBRATION.md` |
| **Tests** | `test_requests.py` *0.7.0 B* (11); *0.7.0 F2*'s painting lays its mass solid, so its tests go on testing the smudge |

## Decisions and gotchas

**1. A loaded brush is 0.6.0's brush, to the bit -- which the plan did not say, and which
it needed.** On linen and rough the lowest tooth lies under the gate's own band --
`0.116` and `0.053` on a 1024 canvas, against `0.18` -- so even a full brush's gate reads
the tooth there: the deepest pits of the weave skip a loaded brush, and always have. A
gate read along the travel wherever the gate reads anything would have moved every mark
ever laid on those surfaces, loaded or not. So the drag is blended in as the brush runs
dry (`Canvas.drag`): nothing at `0.9` of its load and over, all of it from `0.7` down.
At `0` the stamp computes 0.6.0's gate line for line, and that is also how the tests and
the probe get 0.6.0's gate back: `Canvas.drag` patched to `0`, not a copy of the old
stamp. **A load of `0.9` is laid as `0.89999998`**, because a stroke's loads are float32,
so the boundary is taken to float32's rounding; without that, the bristle preset at its
own `0.9` with no falloff -- the inward scumble -- would have been counted as dragging and
laid nothing different.

**2. The amount is matched stroke by stroke, not on average.** The first build spread a
comb around a share read off a table for an even comb, and a comb of a dozen bristles
whose wet ones fell on its weakest -- the comb's gaps are 22% of its bristles -- laid half
of what the stroke should. `DryComb` weighs each bristle by how much of the tip it is
(the first stamp's mask summed per bristle) and finds, per stroke, the share around
which the weighted comb keeps the stroke's. `bristle_shares` is stratified -- one share in
each slice of `0..1`, shuffled -- so no stroke draws all its bristles wet or all dry.

**3. A bristle is not simply in or out -- found while building.** A bristle under
`_BRISTLE_EMPTY` (`0.05` of the canvas) was cut off, as the bench's B2 cut it. That made
the comb's total jump from nothing to one bristle's worth, and a stroke that keeps half a
percent of the tooth -- a bristle at `0.30` on smooth, whose need sits at the tooth's
ceiling -- could only be matched by nothing: summed over 24 strokes it laid **an eighth**
of what it had. What a bristle lays now falls away as the fourth power of how far under
`0.05` it is: the driest lay nothing, as before, and the comb's total is continuous, so
the wettest bristle carries what a nearly empty stroke keeps. The same 24 strokes lay
`1.06` of what they laid.

**4. The rank map keeps B1's amount to a percent**, which is step 2's gotcha 9 answered:
the average is narrower than the tooth it averages, and matched only in mean and spread
it let 22% more through at `0.60` on rough. Given back the tooth's own values rank for
rank, a `flat` and a `round_hard` -- which have no comb and only drag along -- lay `0.99` to
`1.01` of what they laid.

**5. Ranked against every fourth pixel, smooth came back wrong -- found while building.**
The first build took the tooth's distribution from every fourth pixel each way, the
sample `tooth_ceiling` reads. Smooth's grain is a lattice four pixels apart, so that grid
lands on its points and reads the tooth wider than the field is -- a 90th percentile of
`0.667` against the field's `0.637` -- and a gate read along the travel, ranked onto it,
let through **one and a half to two and a half times** what the raw tooth did near the
ceiling, on smooth alone: a starving bristle there laid twice its paint, summed over 24
strokes, and nine strokes in ten more. The tables are read at pixels drawn at random now, from a
generator of their own, and the three surfaces match to `0.98`-`1.03` at the ceiling. The
test that holds the rank map had been written on linen only; it holds all three now.
**`tooth_ceiling` still reads the grid**, as it has since before 0.7.0, so smooth's
ceiling is `0.692` where the field's own 95th percentile is `0.667`: a starving brush on
smooth is capped a little higher than the ceiling's docstring says. Left alone -- it is
what every painting on smooth was painted with, and moving it would move them all -- and
recorded here.

**6. Not combed, so the kernel stays.** The painter's instruction, looked at: the crosser
at `0.45` and `0.6`, 0.6.0's gate, B2 alone as built, B1+B2 as built, and B1+B2 with a
5 px kernel, side by side at twice size (`dry_crosser.png` has the first three). Tuned to
lay today's paint, **B2 alone is dots again, only in the comb's rows** -- it is the bench's
B2 at more than three times the paint that read as streaks -- and B1+B2 is chunky dashes
of every length, lens-shaped, running with the brush: dragged, not combed. The 5 px
kernel sits between the two. So B1's kernel is the same on a comb as off it.

**7. Rough is B2's.** Rough's tooth is coarse islands already -- at 1024x768, four pixels
on, it correlates `0.83` either way, where linen's correlates `0.08` -- so the read along
the travel hardly changes it (`0.89` along, `0.85` across), and on exercise 3 the streaks
come from the comb. On linen and smooth the read along does the work: linen's goes to
`0.73` along against `-0.04` across.

**8. The notice counts every mark that ran dry, not the sixteen laid starved.** The plan
said the fix moves *sixteen of this painting's own* -- the marks laid with a low load on
purpose. A brush spends its load along every stroke, and the `bristle` preset starts at
`0.9`, so most bristle marks' tails run dry and drag, and move: `--corpus-dry` counts
them for every committed painting (*The numbers*). `drags()` asks a saved mark what the stamp will: some dab under `0.9` of its load
where the tooth can gate it, and a travel or a comb. It needs the canvas the log is
rebuilt on -- the tooth's floor decides whether the gate reads anything -- so a fix's
`moves` takes the canvas now. A test lays eight kinds of mark both ways and holds
`drags()` to what moved.

**9. The fact at the call is not built.** The plan held back a line for after B
(*`load=0.45` at this size lands 18% of its paint in pieces under 4 px*), to be built if
the gate left the flecks where the painter found them. It did not: at `0.45` the specks
under 4 px carry 1% of the crosser's paint, where they carried 8%.

**10. What it costs** is timed on the painter's thirteen passes, each gate in fresh
processes (*The numbers*).

## The numbers

On this machine, the probe's (`--dry`, `--corpus-dry`):

| | |
|---|---|
| **The crosser at `0.45`** | 571 pieces, median 4 px, specks 8%, as long across as along -> 125 pieces, median 12 px, specks 1%, `2.8` times as long along the travel as across; laid `1,400` against `1,321` |
| **Exercise 3, rough** | at `0.6`, 15 islands of a median 176 px, `1.4` times as long as wide -> 25 pieces of 26 px, `2.5` times, laying `36,968` against `37,435`; at `0.35`, 54 pieces of 50 px -> 41 of 80 px, `2.0` times |
| **The painter's ledges (flat)** | 25 pieces of a median 52 px, `1.3` times as long as wide -> 26 of 11 px, `3.9` times: dashes |
| **What each load lays** | summed over 24 strokes, against 0.6.0: a `bristle` `0.99`-`1.02` on linen from `0.30` to `0.8`, `0.92`-`0.99` on rough, `0.94`-`1.06` on smooth; a `flat` and a `round_hard` `0.99`-`1.01` |
| **The corpus** | follows: `--corpus-dry` was still running when this was written |
| **What it costs** | follows, timed alone once the corpus replay is done |

## What step 6 did *not* touch

What a loaded brush lays, or a dab of any tip but `bristle`; the log and the stream; the
edge step 5 built (a held edge reads the raw tooth, `Canvas.broken_edge`); the check's
lines, which read marks and measure the canvas; any default.

## File map

| File | What changed |
|---|---|
| `src/easel/canvas.py` | the drag's constants, `_running_out`, `DryComb`; `Canvas.stamp`'s `travel=` and `bristles=`; `drag`, `_gate_tables`, `tooth_along`, `_read_along`, `_bristle_needs`; `_gating`, shared by `trial_copy`; docstrings |
| `src/easel/brush.py` | `_MASK_CACHE` holds the comb index with the mask; `_tip`, `tip_comb`, `Brush.comb_of`; `_comb` and `_bristle_index` out of `_bristle_profile`; `bristle_shares` |
| `src/easel/stroke.py` | `_dabs` and `_loads` out of `paint_stroke`; the travel and the comb handed to the stamp; `drags`; the module docstring |
| `src/easel/notices.py` | 0.7.0's `REBUILDS` row, `_drags_dry`; `moves(record, canvas)`; `rebuild_moves(..., canvas)` |
| `src/easel/session.py` | a loaded canvas's `_gating`; the canvas handed to `rebuild_moves`; `cover()`'s docstring |
| `scripts/probe_handover_session.py` | `gate()`'s "today", "built", "built B2"; `rebuild(cut=)` lays the old gate; `--dry`, `--corpus-dry`, `bench_amounts` |
| `tests/test_requests.py`, `tests/golden/`, `samples/brushes.png` | *0.7.0 B*; F2's painting solid; six goldens and the sampler |
| `PAINTER.md`, `PAINTING.md`, `RECIPES.md`, `DIAGNOSIS.md`, `REFERENCE.md`, `README.md` | the sentences in *Words* above |
| `CALIBRATION.md` | *Load and run-out*'s breakup; the round's *Built, in step 6* |
| `CHANGELOG.md` | `[Unreleased]`: this step's section, and **One fix changes what a rebuild lays** |
| `SUGGESTIONS.md` | finding 2 filled in; the counts |
| `PLAN-0.7.0.md` | status; 4B marked built, with what the build changed |
| `NOTES-step6.md` | this file |

## Next

Step 7, workstream C: C1 is step 2's crops, so what is left is C2 -- the 30% overlap break
on its own, as decided (question 13), held by the recipe's own failure block and by the
corpus's true positives. Read the plan's 4C and `CALIBRATION.md`'s *The graded rule's two
misfires* first; the two misfires are filed and reproduce exactly
(`paintings/Claude/lighthouse_handover/misfires/`).
