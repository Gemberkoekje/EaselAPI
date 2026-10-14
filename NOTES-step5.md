# Step 5 of `PLAN-0.9.0.md`: the check

**To understand this, start by reading the plan's section 4C, and section 6's P3 and
*Answered after the bench* (4C disc, bars and graded, C5), then the painter's own words,
[`answers.md`](paintings/Claude/uktarl_krannoc/answers.md) C and
[`answers-step2.md`](paintings/Claude/uktarl_krannoc/answers-step2.md) 3b, 4a, 7 and 8,
then `CALIBRATION.md`'s *The check, as built*, then
[`tests/test_habits.py`](tests/test_habits.py).**

Branch: `ccr-41356652-bm55is`, off `main` at `a7cf3d4` (#106, step 4, merged).

---

## What landed

| | |
|---|---|
| **`src/easel/plan.py`** | `HABIT_WORDS = ("disc",)`; `Habit` (a habit, a place, the reason); `Plan.habits` and `habit_places()`; `declared_habits()` and `build(habits=)`; saved under the plan's `"habits"`, a habit this build cannot name dropped on load |
| **`src/easel/session.py`** | `plan(habits=)`, its places checked against the canvas as a value plan's are; `_declared_discs` and `_declared_line`, and the disc rule leaving out the signature and the declared places over a pass as over a painting; `_habit_line` in `report()` and `checklist()`; `_standing_said` and `_standing`, the reading each report keeps, inherited by a rehearsal copy and saved in the file (`"standing"`) |
| **`src/easel/cli.py`**, **`src/easel/mcp_server.py`** | `easel plan --habit HABIT PLACE REASON`, the server's `plan(habits=)`; a pass that raised puts back the reading the painter last saw |
| **`src/easel/history.py`** | `is_signature`'s docstring: the disc rule leaves a signature out over a pass too |
| **`PAINTER.md`** | `habits=` in the plan's sentence; the shell's paragraph says the check prints findings first and only the standing lines that changed. Paid for in the same file: 6,699 words, 10 more than before, inside 6,700 |
| **`REFERENCE.md`** | the on-change rule, rule first, under `report()`; the disc row; a `discs declared:` row; a `habits=` row under *What the plan changes*. 11,793 words, 126 more: two history clauses cut |
| **`scripts/probe_uktarl_session.py`** | `--check-built`, the painting rebuilt as built and with its places declared, against 0.8.0's saved reports; `--check-corpus`, the corpus replayed through the built check |
| **`tests/test_habits.py`**, **`tests/test_mcp.py`** | the new behaviour; the server's `plan` declaring and clearing a habit |
| **`CALIBRATION.md`**, **`SUGGESTIONS.md`**, **`PLAN-0.9.0.md`** | the round's *The check, as built*; the row for the three rules; the status line and step 5's row |
| **`LESSONS.md`** | *Warning is not method*: a line that repeats costs the lines beside it |
| **`README.md`** | the check's row says findings first, then what changed; the plan's row carries `habits=` |

## Decisions and gotchas

- **As the painter chose**: the three rules as they are (3b, 4a), the disc habit declared
  per place (C), the signature left out of the pass rule (8), findings first and a
  standing line only when it changes, against the painting as committed, the rest named
  on one line (7a, 7b). No bars habit: `bands="subject"` is that (C). The canvas test for
  bars and graded stays a later candidate, already in `SUGGESTIONS.md`.
- **The form of `habits=` is mine, and is a reading to confirm**:
  `habits={"disc": {place: reason}}`, the habit and then its places as a value plan writes
  them, each with its reason; `{}` clears. The painter chose *per place* and *with a
  reason* but wrote no call. The other readings were a list of `(habit, place, reason)`
  triples, or one reason for several places. A face per key repeats a reason three times
  for three faces, which is the cost of this one.
- **A mark is in a place by the middle of its path**, the point the closing audit
  already groups discs by, so a mark is in one place and never half in two; the first
  declared place that holds it has it. A face's outline from the prelude (`uk_head_poly`)
  holds its features: on the rebuild, of the face marks the 0.8.0 audit named, all lie
  inside the head they belong to but two, the doppelganger's ear light (laid in its
  ear) and the left bandit's neck shade, and each is left under the rule's three.
- **The count is not a finding.** *discs declared: ...* prints under the findings and is
  not counted among them: a pass that laid only declared discs says *nothing to report*,
  as `subject:` is printed and not counted. `bands="subject"`'s line stays a finding, as
  it was: it asks a question, what crosses the bars; this one only counts.
- **The checklist names every declared place**, a place nothing fell in included (`0 in
  the cards`), so every reason is quoted back once at the end, as `why` is. A pass names
  only the places it laid a disc in. `--check` is the audit, and says it as the
  checklist does.
- **What a standing line is compared against.** Every `report()` keeps what it measured,
  each line by its label, at the record it read it at; a rehearsal copy starts from the
  painting's reading and never writes it back. A pass prints a line when its text
  differs from that reading's, word for word. **The reading counts only when it was taken
  at the record the pass opened at** -- the painting's own numbering, a copy's base
  included -- so after an undo, or a pass nobody reported, every line prints. A pass that
  raised prints no check, so the shell and the server put back the reading the painter
  last saw. `since=None` and the checklist print every line.
- **`landed nothing:` and `discs declared:` are about the pass**, and print whenever they
  have something to say: neither is a standing line, so neither is ever *unchanged*.
- **The file**: the reading is saved under `"standing"`, `{"at", "lines"}`, beside the
  log, read with `.get`; a file without it opens with none and its next pass prints
  every line. 0.8.0 never sees it. The plan's `"habits"` is also read with `.get`: 0.8.0
  opens the plan without it, and its disc rule warns where 0.9.0 counts. A line, never
  a mark, so nothing to refuse.
- **`reports.txt`'s committed report of two scripts**, `p01_draw.py, p02_wall.py`, is one
  report for both; the probe gives it to the last script of the painting's order in it,
  so 0.8.0's standing lines match the built check's measurement on every pass, which the
  probe asserts. A saved report prints the notices said at the calls above its check in
  the same `- ` form as a finding; the probe counts only under `check over`.

## Next

Step 6 (E and F: `.rotated()`, `s.frame()` with `.arc()`, rotation in pixels; `shares=`
and its line) starts from the plan's sections 4E and 4F and P4, P5 and Q5's answers.
Step 7 (G1, G2 (a), H1 and H2) and step 8 can go in any order after it.
