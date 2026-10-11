# Step 1b of `PLAN-0.9.0.md`: the second painter's record

**To understand this, start by reading the plan's status line and section 3b, then
[`paintings/Claude/the_curator/FILING.md`](paintings/Claude/the_curator/FILING.md), then
[`SUGGESTIONS.md`](SUGGESTIONS.md)'s *The Curator* and [`CALIBRATION.md`](CALIBRATION.md)'s
*The second painter: The Curator*.**

Branch: `file-the-curator`, stacked on `file-uktarl-answers-step2` (#103, open), so that the
plan's two sets of edits do not conflict.

---

## What this step was for

A second painter's verdict on 0.8.0 arrived after the first painter's questions were all
answered and before anything was built: nine pieces of interim art for the owner's game,
*The Curator*. The owner ruled on 2026-10-11 that it **joins 0.9.0's round** rather than
opening the next one. This step files it, checks its claims, and adds what it raises to
the plan.

## What the owner decided

- **Scope**: join 0.9.0, as the Bell-Warden and Wenna Brask shared 0.8.0's round.
- **Evidence**: a prompt for the cloud session that painted it, asking for its transcript
  and working files on a side branch of the game's repository. It pushed `easel-evidence`
  (`d782640`) with its scratch folder and a manifest, and **declined to copy its
  transcripts**.

## What landed

| | |
|---|---|
| **`paintings/Claude/the_curator/`** | a container with **one painting folder per piece** (`wall`, `beyond`, `desk`, `counter`, `shelf_left`, `shelf_right`, `locked_shelf`, `patron`, `candle`), each with its script as committed in the game at `76122c4e`, `painting.png`, a `painting.gif` recorded by the filer's re-run, and a `NOTES.md`; at the top, the painter's `README.md`; `set.png`, the nine on grey; `verdict.md`, as the owner pasted it, its four headings marked; `reports.txt`, the nine checklists re-run; `FILING.md`, the filer's account; `beyond/scratch/`, its drawing and swatch tests; `evidence/`, two of its crops; `questions-step1.md` |
| **`PLAN-0.9.0.md`** | the status line; section 1's first line; section 3b, the verdict checked (rows 15 to 23); workstreams K (transparency), L (a warm grey), M (deposit), N (a layer), and its other rows folded into E, H and I; its questions Q1 to Q8; steps 1b and 2b; the file map |
| **`SUGGESTIONS.md`** | *The Curator* in the open round, 6 engine items and 1 documentation item; the opening counts, the source table, the reading list |
| **`CALIBRATION.md`** | *The second painter: The Curator* |
| **`PAINTINGS.md`** | its section, and its place in the two bullets on subjects and reading |
| **`README.md`, `llms.txt`, `SUGGESTIONS.md`** | thirty-four paintings, twenty-five painters |
| **`scripts/probe_cohort_session.py`** | nine entries, and `argv=` for a driver script |

## What filing found

- **Across machines, one level.** Every piece rebuilds within one 8-bit level of its
  shipped PNG on Windows, in 12 to 2,508 pixels; to the pixel on the painter's Linux, it
  says. The engine's golden tests already allow this; no painter-facing page says it.
- **The candle's faint shading was its brush's pixel width**: 2.7 px at the sprite's own
  120×300, a mean 6 levels at opacity 0.6; at four times the canvas, 17.
- **The lavender is a narrow band**: umber with 25% ultramarine is neutral, with 35% violet;
  `at_value` makes the white irrelevant.
- **Six of nine say *no clear light*, and `key="low"` would have answered all six**; the
  plan's H2 would not, because no light stands clear. The cut-outs' checklists read the
  surround the cut removes.
- **`REFERENCE.md` already holds most of the reference it asked for**; nothing sent it there.
- **It never rehearsed**, and never saw the check after a pass.

## Decisions and gotchas

- **The verdict is the owner's paste**, with its four section labels made headings and
  nothing else changed.
- **The evidence branch could not be listed by `git ls-tree` in the game's checkout**, for a
  reason not found; its files were taken one by one with `git show` from the commit's diff.
- **The game ignores `*.log`**, so the 16 run logs the manifest lists never reached the
  branch. The scripts are seeded; `reports.txt` is the re-run.
- **Four of eight scripts draw through a pixel helper**, not every one: the widest two are
  in fractions. The first draft of row 21 said every one, and was wrong.
- **Nine paintings, not one.** `tests/test_paintings.py` holds every painting folder to a
  `painting.png`, a `painting.gif`, a `NOTES.md`, a section on the page and a corpus entry,
  and the corpus probe replays one canvas per painting. So each piece is a painting folder
  under `the_curator/`, as each painter is under `lighthouse_greenhouse/`; the counts are
  thirty-four paintings and twenty-five painters. `scripts/probe_cohort_session.py` gains
  nine `driver=` entries and an `argv` field, since these scripts read their stage (and the
  bookcase its side) from the command line; all nine replay and match their spend.
- **Model identifiers**: the game's repository keeps them out of committed files; the model
  and effort here are from the painter's own reply.

## Next

The owner pastes `paintings/Claude/the_curator/questions-step1.md` into the painting
session; its answers come back as `answers.md`, filed verbatim and re-measured. Then step 2b,
`scripts/probe_curator_session.py`. Steps 3 to 9 go on meanwhile where they do not touch K
to N; step 3's `difference()` is also 4K's arch.
