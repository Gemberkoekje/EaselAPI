# Step 1 of `PLAN-0.9.0.md`: the record

**To understand this, start by reading the plan's status line and section 3, then
[`paintings/Claude/uktarl_krannoc/NOTES.md`](paintings/Claude/uktarl_krannoc/NOTES.md) and its
[`versions/README.md`](paintings/Claude/uktarl_krannoc/versions/README.md), then
[`SUGGESTIONS.md`](SUGGESTIONS.md)'s *Uktarl's Room* and
[`CALIBRATION.md`](CALIBRATION.md)'s *Uktarl's Room's round*.**

Branch: `record-uktarls-room`, off `main` at `dcdfc94` (0.8.0's claim, #100, merged).

---

## What this step was for

*Record, then measure, then act.* The painting was in the owner's art folder and its
verdict only in the owner's paste. This step files both, checks every claim of the verdict
against the checkout, opens the round in the register, writes the plan, and writes the
painter's first questions.

## What the owner decided

Nothing was asked this time. The three questions 0.8.0's step 1 put to the owner have
answers on record, and this filing follows them; the plan's section 6 lists them so the
owner can overrule:

- **O1**, as 0.8.0's O2: filed with the campaign's details left out (the dossier's and the
  map's paths, the catalogue entry it drafted, the WebP copy), each cut marked.
- **O2**, as 0.8.0's O3: `verdict.md` only; nothing posted.
- **O3**: the painter's questions go through the owner, batch 1 now.

## What landed

| | |
|---|---|
| **`paintings/Claude/uktarl_krannoc/`** | the prelude and seventeen passes; the thumbnail, swatch and seven look scripts the notes name; `painting.png` and `painting.gif`; `verdict.md`, the painter's message from its session; `NOTES.md`, the painter's notes with the campaign's paths cut and marked, and the filer's account; `reports.txt`, all 46 saved reports; `exercises/exercises.py`; `evidence/`, five pictures; `versions/`, three recovered versions and a README; `questions-step1.md` |
| **`PLAN-0.9.0.md`** | the plan: section 3 checked, workstreams A to J, the painter's questions P1 to P9 |
| **`PAINTINGS.md`** | the painting's section; the subject and reading paragraphs; the unfinished list; *seven of the twenty-five* |
| **`scripts/probe_cohort_session.py`** | the `uktarl` entry. It replays in 47 s: 410 spent, 429 records identical to the painter's, 0 pixels off |
| **`SUGGESTIONS.md`** | the round open at the top: 8 engine items, 4 documentation items, the right-hand column blank, three struck where they changed shape; its opening counts, source table and reading list |
| **`CALIBRATION.md`** | *Uktarl's Room's round*: the rebuild, the versions, the discs, the key, the direction prices, what it read |
| **`README.md`, `llms.txt`** | *twenty-five* paintings, *twenty-four* painters, the open round |

## What filing found

**The painting session's transcript is the evidence again** (`C--git-DnD`, session
`85b72c8b`, 12:05 to 13:22 UTC on 2026-10-01; `claude-opus-5-5`, effort `max` on every
turn). From it:

- **What it read**, word for word: 33,596 words of the documents before its first
  exercise, including the 0.8.0 changelog entry read from this repository's checkout,
  which the wheel does not ship. Plus its memory note and the two earlier painters' notes.
- **How it read the check**: from the body's second rehearsal on, 29 of its 30 `easel run`s
  filtered the output down to the lines it named. That is its *I stopped reading them*,
  measured.
- **The versions**: the mountain's first pass, the body's first, and the backlight's
  second were recovered from the transcript's heredocs and edits. Each prints its saved
  report on the canvas it was rehearsed on.
- **What it never ran**: `cost()`, `--count`, `--alternatives`, `--thumbnail`, `explain`,
  `diagnose`, `preview()`, `compare()`, `undo`.

**And four things the verdict did not say:**

- **`key="low"` is the fix it asked for.** Replayed with the key set, the `values:` line asks
  the painter's own question and answers it, `0.19 over`, from the head's pass on. The
  picture is low-key by the check's test, and no document states the test.
- **The mountain's 129 strokes were a direction**: 88 across the facets' length, 31 along
  it. The concave cost it described is the collar's, and is measured in `CALIBRATION.md`
  already (*Shaped masses (M8)*), with `s.cost()` as the remedy it never ran.
- **One of its "21 face marks" is a ridge on the relief** that the disc rule's grouping
  joined to the left bandit's eye from eight passes earlier.
- **A landmark outlived its drawing**: `sun`, marked by the first `p01_draw.py`, kept by
  `unguide()`, and drawn on the face in every look after.

## Decisions and gotchas

- **The verdict is the painter's markdown from the transcript.** Its words match the
  owner's paste; the paste lost the headings and bold.
- **The note the owner sent with the verdict** is quoted in the plan as the owner's
  framing, and not filed beside the painting: it is not the painter's.
- **The passes rebuild in their numbering.** The drawing ran three times, but a drawing of
  guides lays no record, so unlike the Bell-Warden no `order=` is needed.
- **Eight of the painter's files had CRLF line endings** (written by Python on Windows);
  filed as LF, as `.gitattributes` would make them anyway. Nothing moves: line numbers in
  the reports are unchanged.
- **A recovered version keeps the painter's line numbers** by putting the prelude's old
  shape on the script's one blank line, as one long line. The backlight's version therefore
  draws a `prelude-rebind` fact the painter's report does not have, and its README says so.
- **`easel log --reports` prints the last 20** unless given `-n`; `reports.txt` is `-n 46`.
- **`import easel` now resolves to an installed 0.8.0 wheel**: the painter upgraded the
  machine's global install from 0.7.0. Its code equals this checkout's `src/`, but put
  `C:\git\EaselAPI\src` first anyway (`PYTHONPATH=src`), as before.
- **A Bash `cd` persists** in this environment and moves the working directory: start
  every command from the repository root.

## Next

The owner pastes `paintings/Claude/uktarl_krannoc/questions-step1.md` into the painting
session; its answers come back as `answers.md`, filed verbatim and re-measured here. Step 2
is `scripts/probe_uktarl_session.py`, which needs P2 (the edges to soften) and P5 (the
split) for two of its benches, and nothing else from the answers to start.
