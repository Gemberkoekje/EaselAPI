# Step 7 of `PLAN-0.7.0.md`: the graded rule, broken where marks lie side by side

**To understand this, start by reading the plan's workstream C, then `_graded_band`,
`_longest_run` and `_shared_reach` in `src/easel/session.py`, and `CALIBRATION.md`'s *The
graded rule's two misfires* -- and read `NOTES-step6.md` first if you have not, and
`NOTES-step2.md`, whose crops decided this step.**

Branch: `graded-rule-overlap-break`, off `main` at `d82caa6` (step 6, #80).

---

## What this step was for

The painter's finding 3: *graded passage laid too narrow* fired twice on marks that were
not a passage, both times on a rehearsal of a pass later rewritten, and both times the
brush the line named was a `0.006` accent laid among wider marks. Step 3 saved what a
rehearsal is told (C0); step 2 cropped every pass of the corpus the rule fires on (C1) and
put the crops to the painter blind. Decided (question 13): **the 30% overlap break on its
own** -- the run breaks where two neighbours across the stack share under 30% of the
shorter one's reach along it -- and not the median clause, which on the painter's reading
silences every passage among the corpus's fires.

## What landed

| | |
|---|---|
| **The break** | `_REPORT_BAND_OVERLAP = 0.30`; `_graded_band` measures each mark's reach along the stack beside its offset across it; `_longest_run` breaks between two neighbours that share under `0.30` of the shorter reach, as well as at a gap wider than four brushes; `_shared_reach` |
| **Words** | `report()`'s docstring and `REFERENCE.md`'s list of the check's rules gain the clause |
| **The probes** | `probe_cohort_session.py --graded`: the old rule is `0.6.0`, the built one `BUILT`, the engine's own line is held to `BUILT` on every pass, and `SWEEP` runs the share from 5% to 90%; `probe_handover_session.py --misfires` holds the engine to the built gate and prints both runs and the sweep for the four cases |
| **Tests** | `test_requests.py` *0.7.0 C2* (2) |

## Decisions and gotchas

**1. The water misfire is a test, from the painter's own files, in half a second.** The
rule reads a pass's log and the canvas's shape and nothing else, and a counted pass logs
what a painted one does (`test_paintings.py` holds that), so `_misfire` lays
`misfires/water/06_water_v1.py` on its own prelude, counted, on a fresh 1024x768 canvas --
not over the five passes the painter had laid under it. The water pass takes every point
from its own `random.Random(5)`, so its records are the rehearsal's: with the break patched
to `0`, the line is the one in the painter's `rehearse.log`, to the character, and the test
compares the two. **The headland pass cannot be laid that way**: its masses' passes draw
from the session's stream -- 37 of its 42 marks move when the seed does -- and laid on a
fresh canvas at seeds 1 to 24 it is told the line at two of them (steps `0.021` and
`0.018`), and at the painting's own seed 11 not at all. Its misfire needs the stream the
painter's three passes left, which is why `--misfires` rebuilds them under it. It is not a
test either way (see 2).

**2. The headland misfire still fires, at every share.** Its nineteen marks are the planes
of two rock faces laid along the rock's strata, and the crevice along their join: they
overlap along the stack as a passage does, from 5% to 90%. That was the price the painter
chose, and no test holds it -- a test that a false positive fires would fail the day a
clause fixes it.

**3. The share is the middle of a plateau.** Swept over the corpus, every share from 10% to
40% fires on the same seven passes. At 50% the pier's stacked masses go quiet as well -- a
false positive of the kind the break was said to leave -- but at 70% the laundromat's
street starts to fire, and at 90% the pier's water and the hands' bowl go. One pass at the
plateau's edge is not a reason to move off it, so it stays at `0.30`. On the four cases in
hand the share makes no difference at all: the water's glints share no reach even at 5%.

**4. The pass the break adds is told about the wrong brush -- found while building.** The
pier's water fires under the break and did not under 0.6.0's rule, and the painter read
its crop blind as a passage coming back as bars. Why it was silent: the pass is a
`scumble` of nine passes and five reflections laid across the field after it, lighter than
the passes they lie among, and the fourteen made one run whose colours turned three
times. The break cuts that run where the reflections lie side by side -- into 8, 4 and 2 --
and the longest piece is seven of the field's passes and one reflection at its end. So the
line reads *8 marks ... 0.025 apart, and the narrowest brush laying them is 0.02 -- 0.8 of
that step*, and the `0.02` is the reflection's: the field's own brush is `0.108`, over four
of its steps, and the size the line offers, `0.075`, is narrower than the field was laid
with. The line is right that the field shows bands and wrong about why. It does not move
the decision: counted as a miss rather than a kept passage, the break keeps both beams, as
0.6.0's rule does, and fires on three of the painter's false positives where 0.6.0's rule
fires on six. Recorded in `CALIBRATION.md` and `SUGGESTIONS.md`; the median clause, which
would have named the field's brush, was declined for silencing the beams.

**5. The reading that decided the gate was read again -- found while building.** The
painter's answer 13b chose the break *if the owner reads `crop_01` as I do* (speckle), and
added that once B landed, *starved hatching like `crop_01`'s turns from dots into streaks,
and may start to read as the stripes the bench sees* -- in which case its answer was to
leave the rule as it stands. B landed in step 6, and the corpus replay here re-crops every
pass with it: the hands' `pass08_pickmass.py` is no longer speckle but crossed streaks
dragged along the patch's two directions, most of them across the nine counted marks
rather than along them. Put to the owner on 2026-09-24 as step 2's crop and today's side by
side: **still not a passage coming back as bars**, so the break is built. The run the rule
counted there is unchanged -- 9 marks, step `0.017`, sizes `0.015` to `0.05` -- and so is every
gate's verdict. The step-2 crop was kept for the comparison before the replay overwrote it:
`out/graded/` is gitignored and rewritten by every `--graded` run, so **copy a crop out
before re-running the probe if it is evidence for a reading**.

**6. The engine and the bench's copy agree on every pass.** `--graded` holds the engine's
own line to the re-implementation of the built gate and prints a line wherever they differ;
over the 337 painted passes, and the four cases in hand, it printed none. The engine
computes each mark's reach along the stack in the copy's own arithmetic, so a pair sitting
exactly on `0.30` cannot fall on different sides in the two.

## The numbers

On this machine, the probes' (`--graded`, `--misfires`):

| | |
|---|---|
| **The corpus** | 337 painted passes; the rule fired on 9 under 0.6.0 and fires on **7** -- `car_wash/p13_form.py`, both beams, `heron2/pass11_last.py`, the pier's masses and water, the hands' bowl; quiet now on `fable/p8_base.py`, the hands' finger and GPT's hull |
| **The painter's reading** | its three passages kept (the beams, the pier's water); three of its six false positives quiet, three still told (the pier's masses, the heron's ruled slab, the hands' bowl) |
| **The four cases** | the headland misfire fires (19 marks, step `0.020`, `0.30` of a step); the water misfire is silent; the recipe's passage is silent (`4.04` of a step); its failure block fires (`0.95`) |
| **The share** | 5% -> 8 passes, 10% to 40% -> 7, 50% -> 6, 70% -> 7 (a different seven), 90% -> 4 |
| **The pier's water** | 0.6.0: one run of 14 whose colours turn 3 times, silent; built: runs of 8, 4 and 2, the longest seven field passes (`0.108`) and a reflection (`0.02`), `0.79` of a step |

## What step 7 did *not* touch

What any pass lays, the log and the stream -- the rule reads the log after the pass; every
other rule of the check; the line's wording, which the water misfire no longer reaches and
the pier's water reaches for the wrong brush; the median clause and the bench's *trimmed*
variant, both declined; the kind of false positive the break leaves, stacked masses.

## File map

| File | What changed |
|---|---|
| `src/easel/session.py` | `_REPORT_BAND_OVERLAP`; `_graded_band` measures the reach along the stack; `_longest_run` breaks on it; `_shared_reach`; `report()`'s docstring |
| `scripts/probe_cohort_session.py` | `GATES`' `0.6.0`, `BUILT`, `SWEEP`, `swept`; `graded_verdicts` sweeps; `report_graded` holds the engine to `BUILT`, prints both runs, and prints the sweep |
| `scripts/probe_handover_session.py` | `probe_misfires` holds the engine to `BUILT`, prints both runs and the sweep |
| `tests/test_requests.py` | *0.7.0 C2* |
| `REFERENCE.md` | the check's rule sentence gains the clause |
| `CALIBRATION.md` | *The graded rule's two misfires*: *Built, in step 7* |
| `CHANGELOG.md` | `[Unreleased]`: this step's section |
| `SUGGESTIONS.md` | finding 3 filled in |
| `PLAN-0.7.0.md` | status; 4C marked built, with what the build found |
| `NOTES-step7.md` | this file |

## Next

Step 8, workstream D: **D0**, scripts rehearsed as alternatives side by side -- `easel run
--rehearse --alternatives a.py b.py c.py`, each on its own copy with its own check block and
one labelled sheet, the same on the MCP `run`, and `s.rehearse_each([...])` for plans. D1 was
declined (question 14). Read the plan's 4D and `CALIBRATION.md`'s *A variant's cost, and a
sheet in four processes* first; `rehearse(vary=)` and `label_sheet` in `look.py` are the
sheet D0 lays.
