# Step 2 of `PLAN-0.9.0.md`: measure

**To understand this, start by reading the plan's status line and section 6's *Answered*
and *After the bench* tables, then [`CALIBRATION.md`](CALIBRATION.md)'s *Uktarl's Room's
round*, *Step 2*, then
[`scripts/probe_uktarl_session.py`](scripts/probe_uktarl_session.py)'s docstring.**

Branch: `measure-uktarls-room`, off `main` at `f416bcf` (step 1, #101, merged).

---

## What landed

| | |
|---|---|
| **`paintings/Claude/uktarl_krannoc/answers.md`** | the painter's answers to `questions-step1.md`, verbatim, written 2026-10-10 in the painting's own session |
| **`paintings/Claude/uktarl_krannoc/evidence/`** | `edges_2x.png`, `heads_1to1.png` and `heads_4x.png`, as the answers cite them under `out/` |
| **`paintings/Claude/uktarl_krannoc/questions-step2/`** | batch 2: `README.md`, `QUESTIONS.md`, `KEY.md`, `answers-template.md`, and `make_package.py`, which lays the probe's sheets out as a zip |
| **`scripts/probe_uktarl_session.py`** | every flag of the plan's step 2: `--claims`, `--clip-out`, `--answers`, `--soft`, `--join`, `--shares`, `--rules`, `--direction`, `--key`, `--reading`, `--corpus` |
| **`CALIBRATION.md`** | the round's *Step 2* |
| **`PLAN-0.9.0.md`** | the status line; section 6's *Answered* and *After the bench* tables |

## What it measured, in one line each

The numbers are in `CALIBRATION.md`; what each decides is in the plan's section 6.

- **The rebuild**: exact, 429 records, 410 spent, 0 px.
- **4A**: the exclusion cut on the line closes the seam and lays nothing wholly on him; the
  hold's default feather, breaking into the light, *is* the seam.
- **4B**: a soft hold per call works as a mask and costs no time, but widens the step less
  than asked wherever a later mark crosses the edge, and softens its whole outline. Blind
  sheets for batch 2.
- **P9**: the steps across the three terminators are 2.1, 1.7 and 1.4 px; a sixth of a face
  is 7 to 8.
- **4C**: near-copies keeps 8 of the disc rule's 30 passes; touching keeps 27 of the bars
  rule's 53; a mass as one keeps 3 of the graded rule's 8. Each drops corpus passes the
  rule was right on, by the bench's eye; batch 2 asks the painter's.
- **C5**: 40% of the corpus's standing lines repeat the pass before.
- **4F**: the shares line names the starved near bandit (22 of 45, 40 in hand).
- **4G**: G1 fires once in the corpus and on all ten facets; G2 on 27 masses and the V; G3
  is 12 strokes over the corpus.
- **4H**: H2 speaks on exactly the three paintings that name a light, and from the pass
  that paints it.
- **4I**: the inventory, section by section, with the share the engine also says.

## Decisions and gotchas

- **The corpus replay is this probe's own**, a `PASS_HOOKS` entry on the cohort harness,
  kept in `out/uktarl/corpus.pkl` (about 25 minutes). It keeps every pass's records,
  report and light, and prices every shaped mass by patching the two direction checks,
  which are handed the resolved brush; the walk runs on a trial copy, as theirs does.
- **The rules are asked pass by pass without the bars rule's decay**; the engine's own
  counts, with it, are printed beside them.
- **A 10-to-90% rise misreads a terminator**: on a face 44 px across the terminator is 9 px
  from the face's edge, and a ±12 px profile reads the wig. The step is measured as the
  `edges:` line measures it, over the asked width.
- **A soft ramp must reach zero at the line on both sides**: the first prototype left the
  outline's antialiased rim outside at full coverage, a dotted ring round a faded edge.
- **Pass names were matched by a label carrying the mark count**, which made every pass a
  candidate named differently look dropped. Fixed; the table is by name.
- **The pears painting's `p9_rehearse_pear.py` fails to replay**, as in 0.8.0's corpus.
- **`Session.marks`** holds landmarks; a per-pass spent total sums to 414 with the four free
  signature marks; a bare `cat > file` in Bash blocks until its timeout.
- **G2's candidate (b)**, the shape priced cut at its deepest notch, is not built: the
  bench measured (a) only, and the V's two flaps, 3 + 4, are what (b) would have to reach.

## Next

The owner sends batch 2: run `python scripts/probe_uktarl_session.py --soft --rules`, then
`python paintings/Claude/uktarl_krannoc/questions-step2/make_package.py`, and send
`out/painter-questions-uktarl-step2.zip`. Steps 3 (A and D) and 6 (E and F) need nothing
from it and can start now.

---

## Closed, 2026-10-11: batch 2 answered

On branch `file-uktarl-answers-step2`, off `main` at `bfd0107` (#102 merged).
[`answers-step2.md`](paintings/Claude/uktarl_krannoc/answers-step2.md) is filed verbatim;
`--answers2` re-measures its claims; the plan's section 6 has *Answered after the bench*,
`CALIBRATION.md` the re-measurement, `SUGGESTIONS.md` the canvas test as a later
candidate, and `questions-step2/README.md` a line saying when it was sent and what in
`KEY.md` was wrong.

- **The painter's blind picks matched the key** letter for letter: B1 the edge meant, B3 a
  blur, B2 damage. It read Part 2's text first and says so; Part 2 names no letters.
- **Every question of the round is answered.** What changed from the bench's reading:
  near-copies withdrawn (the rule stays, with C4); bars and graded unchanged; G3 not built
  (a change of the step-1 answer); a softness **per stretch** as well as per hold.
- **The bench was wrong once**: *Uktarl's sheet barely changes* measured along his
  terminator, under the wig. Measured over the lit plane, B1 darkens 24% of it, median 0.14.
- **New from the answers**: the pass check's disc rule counts the signature; step 5 leaves
  it out, as the closing audit does.

**Next: steps 3 to 9.** Step 3 (`clip_out=` at `feather=0`, `difference()` for read places,
the rehearsal look's flags) starts from `PLAN-0.9.0.md` section 4A and 4D and this file.

