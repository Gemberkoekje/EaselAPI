# Step 2 of `PLAN-0.7.0.md`: the measuring probe

**To understand this, start by reading the plan's section 4 (the workstreams) and
[`scripts/probe_handover_session.py`](scripts/probe_handover_session.py)'s docstring,
then [`CALIBRATION.md`](CALIBRATION.md)'s *The lighthouse handover's round* -- and then
look at the sheets the probe writes under `out/handover/`, because two of the round's
questions are the eye's and not a number's.**

Branch: `measure-handover-round`, off `record-handover-round` (step 1).

---

## What this step was for

*Measure before building*, the plan's rule 1: every candidate of workstreams A, B, C, D,
F and G benched on the painting's own canvas before any of it is built, with the
output deciding which rows are built as written -- and the edge candidates rendered at a
painting's size, because the painter answered the plan's question 2 with *I cannot
choose; I have not seen them*.

## What landed

| | |
|---|---|
| **`scripts/probe_handover_session.py`** | new. Rebuilds the painting through the CLI's own `run_script`, keeping a rehearsal copy after each pass; re-measures section 3; benches A1 and A2 inward, B1, B2 and B3, the graded rule on the four cases in hand, a variant's cost and a sheet in four processes, the session file saved each way, the pressure-list fade and the wet bands; writes the sheets |
| **`scripts/probe_cohort_session.py --graded`** | every pass of the 22 paintings the graded rule fires on, cropped as that pass left the canvas, with six gates' verdicts; `PASS_HOOKS` on the watcher is how the crop is taken at the pass's close |
| **`CALIBRATION.md`** | *The lighthouse handover's round*: every number below, with what it was measured on |
| **`PLAN-0.7.0.md`** | the status line; section 5 gains the questions step 2 put to the owner |

## What the probe decided, row by row

| Row | Built as written? | What the probe says |
|---|---|---|
| **A1** the feather | **not as a default** | Inward, the knee is not where the plan's centred bench put it: at `0.002` the tower's one-pixel step goes `0.298` to `0.247` and the `edges:` line `77%` to `69%`, which is hard to see at the painting's size; the line only halves at `0.005`, where it is the blur the plan predicted |
| **A2** the feather broken by the tooth | **the owner's eye** (question 10) | Read here as a crisp, painted edge at `0.002` on the tower, the headland, a mass on bare ground and a burial, and ragged by `0.003` -- a reading, which is why it is a question. Invisible to both numbers by construction |
| **A3** `roughen()` | **as written** | On the headland the outline moves the picture more than any feather: the roughened and the plain silhouettes differ at a glance on `edges_headland.png`, and no feather at `0.002` does |
| the default's reach | **a question** (11) | The decided default moves 5 of the painter's 9 edge-drawing calls -- the horizon it wanted ruled among them -- and none of the four the verdict named: the tower, its lit side and the lantern are clips |
| **B1**, **B2**, **B3** | **B1+B2, tuned** (question 12) | Today's starved bristle is a halftone of dots; B1 makes dashes that run with the brush, B2 a comb's streaks with body, B1+B2 the most like a dry brush. **Both move how much a load lays** -- B1 up to a fifth either way on rough, B2 up to 3.5 times -- so the build keeps the tooth's whole distribution and tunes B2's spread. B3 is contrast only, as the plan expected |
| **C0** saved reports | **as written** | Nothing here argues against it; it is what would have made the misfires reproducible from the file |
| **C1** the crops | **done** | 9 of 337 passes, each cropped with the marks counted drawn over it |
| **C2** the gate | **not built as prototyped** (question 13) | It silences both misfires and keeps the recipe's failure block, and over the corpus it also silences three stacks read here as true positives. No variant tried is free |
| **D0** scripts as alternatives | **as written** | The variant's cost is the paint (10.2-10.6 s of 10.4-10.7), which no sheet takes away; what D0 buys is the comparison |
| **D1** parallel panels | **declined** (question 14) | 1.6-1.7 times one panel against a target of 1.5; the cost is each worker loading the session file |
| **F1** frames out | **as written** | 16.43 MB to 7.36 MB; a GIF from the log is 36 to 49 s |
| **G1-G4** | **as written** | The width (80 / 64 / 30 px), the thirds (`0.858 / 0.787 / 0.408`) and the last twentieth (`0.188`), the recipe's own no-pressure end (`0.162` on `0.150`), the wet bands (16% of the canvas past two levels of value, 34% of colour) |

## Decisions and gotchas

**1. The probe patches the engine for the length of one bench and never touches
`src/`.** Every candidate is a context manager that swaps one method -- `_clip_cover`
and `_mass_hold` for A, `Brush.mask` and `Canvas.stamp` for B -- and puts it back. The
stamp's replacement is a copy of the engine's body, line for line, except inside the
gate, so what the bench measures is the candidate and not a second engine. When B is
built, diff `_gated_stamp` against `Canvas.stamp` first: the copy was taken at `v0.6.0`.

**2. The inward ramp is exact to the outline, not to the coverage mask.**
`inside_depth` measures each pixel centre's distance to the nearest segment of the
polygon, signed by its own even-odd test. PIL's blur filters refuse a float image
(`GaussianBlur`, `BoxBlur` and `Kernel` all raise *image has wrong mode* on mode `F`);
only the rank filters -- `MinFilter`, `MaxFilter` -- take one, and they are what finds
the band of pixels near the line. The plan said *built with PIL's own filters on the
coverage image*; an erosion-count ramp would be anisotropic (a square structuring
element eats a diagonal edge faster), so if the build uses erosions, re-run the curve
against this exact one before trusting its knee.

**3. The inward knee is not the centred one.** The plan's table was a centred Gaussian,
which spreads a 2 px feather over about eight pixels; an inward smoothstep over `F`
pixels has a rise of about `F / 1.5`, so the `edges:` line reads it as hard until `F`
is past 3.75 px. That is why A1 at `0.002` is almost invisible at a painting's size and
why its curve only drops under half at `0.005`. The value the build picks is the eye's,
not the line's.

**4. A2 is invisible to both numbers on purpose.** It keeps every pixel crisp and breaks
the boundary where the tooth is low, so its one-pixel step stays at today's and the
`edges:` line cannot tell it from today. Its first construction -- thresholding the
tooth's *rank* against the ramp, with a narrow band -- read as dither at 3x and was
dropped; what is benched is the stamp's own gate (the tooth value against a need falling
with depth, over the stamp's own `0.18` band), which is what *the way a loaded brush's
edge does over tooth* means in this engine.

**5. `import easel.brush as b` gets the function**, exactly as `LESSONS.md`'s papercuts
say; the probe takes both modules from `sys.modules`.

**6. The flat fields are set, not painted.** A whole-canvas `block_in` costs about ten
seconds at 1024x768 and leaves its own passes' edges on the canvas, which the `edges:`
line then counts; `canvas.rgb[...] = colour` costs nothing and leaves the laid marks as
the only edges there are.

**7. The value view and the export's colour disagree by a factor of two.** Drying
between the three sky ramps moves 16% of the canvas by more than two 8-bit levels of
value and 34% in any colour channel; the plan quoted the second without saying so. The
probe prints both.

**8. `easel run` has to be reproduced through `run_script`, not `exec`.** The CLI runs
each pass in a fresh scope with the prelude executed in front of it, and opens a pass
(`_open_pass`) so `report(since=)` can read what it buried; the probe calls the same
`run_script` and opens the pass the same way, so the `edges:` lines it prints are the
ones the painter's shell printed.

**9. B1 keeps the tooth's mean and spread, and a load still lays a different amount.**
The line kernel makes the tooth's distribution more Gaussian, so the same `need` lets
through a different share of it: 22% more paint at `0.60` on rough, 12% less at `0.35`.
The build should match the whole distribution (a rank map is the cheap way), not two
moments.

**10. B2 as benched is heavier, not only streakier.** A bristle keeping its load keeps
all of it, so at `0.35` on rough the stroke lays 3.5 times today's paint. The spread
(`B2_REACH`) is the number to tune; the streaks are what the candidate is for.

**11. The graded crops are read, not measured.** *True positive* in the corpus table is
how each crop reads -- a passage coming back as bars, or a row of separate things -- and
it is written as a reading in `CALIBRATION.md` for that reason. The owner's reading
decides question 13, not this file's.

**12. Timings only on a quiet machine.** Two probes at once slowed the corpus replay from
about 25 minutes to about 45; the sheet and the file benches were run alone afterwards,
twice for the sheet (1.6x and 1.7x), and both numbers are quoted.

**13. A backslash in a heredoc does not survive to Python on this machine.** An edit
script fed through a quoted heredoc lost the backslash of a `\n` inside an f-string and
wrote a real newline into the probe. Make edits that carry escapes with the editor.

## Open, and for the owner to rule on

The five questions at the end of the plan's section 5, each with its evidence and a
recommendation. **The build steps wait on them**: step 3 (E and C0) and step 4 (F) do
not, and can go ahead; step 5 (A) waits on 10 and 11, step 6 (B) on 12, step 7 (C) on 13,
and step 8 (D) on 14 only as far as D1 goes.

- **10. Which edge candidate reads as paint.** Recommended: A2 at `0.002`.
- **11. Whether the default reaches a clip.** Recommended: feather `clip=` too, inward --
  which reverses a decision the painter took, so it goes back to the painter if the owner
  wants it to.
- **12. Which dry-brush gate.** Recommended: B1+B2, tuned so a load lays today's paint.
- **13. Whether the graded rule is narrowed.** Recommended: not, on this reading of the
  crops.
- **14. D1.** Recommended: declined.

To look: `python scripts/probe_handover_session.py --edges --flecks` and
`python scripts/probe_cohort_session.py --graded` write every sheet the questions cite.

## What step 2 did *not* touch

The engine. Nothing under `src/` changed; every candidate is patched in for one bench and
put back.

## File map

| File | What changed |
|---|---|
| `scripts/probe_handover_session.py` | new: the round's benches |
| `scripts/probe_cohort_session.py` | `--graded`, `GATES`, `graded_run`, `crop_graded`, `PASS_HOOKS` |
| `CALIBRATION.md` | the round's section, and its row in the index at the top |
| `PLAN-0.7.0.md` | status; the questions step 2 raised |
| `NOTES-step2.md` | this file |
