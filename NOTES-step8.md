# Step 8 of `PLAN-0.9.0.md`: the recipes and sentences, the pixel paragraph, and a painter's lines

**To understand this, start by reading the plan's section 4I and the rows it answers in
section 3 (9 to 12) and 3b (15 and 20), section 6's P8, P9 and Q6, then the painter's own
words — [`verdict.md`](paintings/Claude/uktarl_krannoc/verdict.md)'s *The documentation*
and [`answers.md`](paintings/Claude/uktarl_krannoc/answers.md) H and I — and The Curator's
[`answers.md`](paintings/Claude/the_curator/answers.md), Question 6; then
`CALIBRATION.md`'s *The recipes and sentences, as built*.**

Branch: `ccr-23576cbd-k50d3x`, off `main` at `c8ed624` (#110, step 7, merged).

---

## What landed

| | |
|---|---|
| **`RECIPES.md`** | four recipes: *A thing drawn in its own frame* (I3, built on `s.frame()`), *Several figures in one picture* and *A light behind a silhouette* (I4), *Straight members seen flat-on* (Q6, in pixels, two blocks); a sentence each for *A hollow thing* seen low and *A form turned toward the light* lit from below (I4); the join on skin in that recipe (P9), and its half-tone band mixed at the halfway value; *An edge that is actually lost* points at the terminator as a stretch; the index table |
| **`PAINTER.md`** | *What you are bad at* opens with the painter's sentence, *absolute placement is what fails, not pixels*, and its remedy (I3); the card's *say a place; do not compute a coordinate* is gone. 6,699 words of 6,700, the card 1,370 |
| **`CHANGELOG.md`** | the preamble says each release opens with what a painter will meet, in ten lines or fewer; 0.8.0's entry has its ten (I5) |
| **`README.md`** | *Determinism*: to the pixel on one machine, within one level on another (row 15) |
| **`LESSONS.md`** | *One home per rule* ends with the order: the rule, then the number, then the history (I2) |
| **`scripts/probe_uktarl_session.py`** | `--recipes-built`: the join on the three faces, the form recipe at 400×300 and 1024×768, each head's lit share, a lit side on a dark bar; `mean_profile()` beside `step_widths()` |
| **`tests/test_guide.py`** | the pixel advice says one thing; every release from 0.8.0 on opens with its painter's lines, at most ten, one line of the file each |
| **`CALIBRATION.md`**, **`SUGGESTIONS.md`**, **`PLAN-0.9.0.md`**, **`DIAGNOSIS.md`**, **`llms.txt`** | the round's *as built* and an index row; the four documentation rows, The Curator's geometric-subjects row and its determinism note, a found row; the status line and step 8's row; three rows pointing at the new recipes, on the lines already there; the recipe list and `RECIPES.md`'s size |

## Decisions and gotchas

- **The join on skin, benched before it was written** (P9, after 4B). On the painter's
  three faces a join twice as wide lifted the shade beside the terminator and left the
  light as it was; the lit plane's terminator lost over 8 px, as a stretch, carried the
  ramp into the light and kept the lit outline; the whole lit plane soft did the same and
  ringed the face in shade, darkening a quarter to a third of the plane. The recipe gives
  the stretch first and the whole plane as the painter's other form (answer 2b), with its
  cost. Uktarl's terminator lies under the wig and barely moves, as step 2 found.
- **Found while building: the form recipe's half-tone band did not read.** Mixed half and
  half it is `0.29` between the guide's `0.14` and `0.76`; at 1024×768 it read `0.25` over
  a shadow of `0.16`. Mixed at the halfway value it reads `0.36`. **Changed in the recipe's
  block**, which the plan did not name: it is the join's value, which is P9's, and the
  painter's own join error. And a lost terminator beside a kept band leaves a trough of the
  shadow mass at the line, so the recipe says to leave the band out when the terminator is
  lost. **A reading to confirm.**
- **The `edges:`-style step under-reads a ramp laid by a flat brush**: the steepest gradient
  is the brush's grain, so twenty pixels read two or three. A 10-to-90% rise was tried and
  read the band and the hair as part of the turn; the probe prints the value across the
  terminator at fixed offsets, averaged along it, and the recipe quotes those.
- **At the guide check's 400×300 a narrow brush is under its landing width**: the band's
  4.8 px brush lands almost nothing, so the guide's own run cannot show what the band does
  at a painting's size. The recipe's numbers are from 1024×768. Workstream M's case; not
  changed here.
- **Every new block was run under the guide's preamble before it went in**, and two were
  changed by what the check said: a ledge's top edge laid with a 3 px `flat` said
  `chisel-blank`, and stones laid each at a tilt said `direction-given`. A lit side under
  about 3 px lands nothing on a dark (a 1.5 px liner raised a bar `0.06`) — The Curator's
  lost lights — so the recipe lays them at 3.5. The light behind a silhouette is run along
  the shape's own edge, half held out; run beside it, it left the dark ring the recipe
  warns of.
- ***Several figures in one picture* opens its own `Session`**, since `shares=` needs a
  budget and the preamble has none: the first recipe block to do so. Its heading is the
  plan's name, and *figure* is the one subject word in a recipe heading. **A reading to
  confirm**; *A subject that is one thing against a ground* is the nearest precedent.
- **`PAINTER.md` paid for the pixel paragraph inside itself**, by four things the page
  said twice: exercise 7's *the drawing did not count* (the card says drawing is free),
  *Be honest about these*, the workflow's sentence describing itself (the kind 0.8.0 moved
  to `LESSONS.md`), and the paragraph's own two-line grid block, folded into its prose.
  The card's sentence went as P8's fourth cut, since it was the same contradiction.
- **The rows steps 3 to 7 wrote already open with their rule** (I2's audit): nothing in
  them was rewritten.
- **0.9.0's own painter's lines are written at the cut** (step 10): `[Unreleased]` stays
  *Nothing yet.*, as every round has kept it, and the test will refuse the cut without
  them.
- **One home per rule**: the recipe for a frame first restated the pixel sentence, and
  `check_guide_overlap.py` caught it; it points at `PAINTER.md` instead.
- **`DIAGNOSIS.md` is at its 130 lines**, so the new recipes are pointers on rows already
  there; the backlight's dark ring has no row.

## Not done here

Q8's lines in `Session`'s, `block_in`'s and `stroke`'s docstrings and the flags on
`easel --help` go with the card's table, in step 9. M's table of how a mark deposits and
L's sentence on white under `at_value` are their workstreams', after the second painter's
batch 2. The Curator's line for long edges laid with under half a pixel of wander is a
candidate, not benched. None of the new recipes has a demo.

## Next

Step 9 (I1: the one-page card and the measured cuts, the reading path counted, Q8's
five-file table atop what `easel guide` prints) starts from the plan's section 4I and P8;
the reading path it starts from is 32,182 words, 2,291 longer than before this step.
**G2 waits for the painter's answer to `questions-step7/`.** **4N's `cut=` and 4K's
`alpha=` wait for the second painter's batch 2**, which is not written yet.
