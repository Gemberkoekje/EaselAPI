# Step 1 of `PLAN-0.8.0.md`: the record

**To understand this, start by reading the plan's status line and section 3, then
[`paintings/Claude/bell_warden/NOTES.md`](paintings/Claude/bell_warden/NOTES.md) and its
[`versions/README.md`](paintings/Claude/bell_warden/versions/README.md), then
[`SUGGESTIONS.md`](SUGGESTIONS.md)'s *The Bell-Warden* and
[`CALIBRATION.md`](CALIBRATION.md)'s *The bell-warden's round*.**

Branch: `record-bell-warden`, off `main` at `2ee54d3`.

---

## What this step was for

*Record, then measure, then act.* The painting was outside the repository, in the owner's
own folder, and its verdict existed only as the owner's paste; step 1 files both, opens
the round in the register, and puts the first questions to the painter. It waited on the
owner's answer to O2.

## What the owner decided

All three the recommended option, on 2026-09-26:

- **O2**: filed, **with the pack's details left out** — the painter's paragraph saying which
  pack the picture was for and where its copy goes, the pack's catalogue entry, and the
  WebP copy. The pack lives in a private repository today. The scripts name only *the
  Bell-Warden* and *a chapel's undercroft*, and were filed as they are.
- **O3**: `verdict.md` only; nothing is posted.
- **The painter's questions go through the owner**, who pastes them into the painting
  session: question 2's follow-up and 5 to 8 now
  ([`questions-step1.md`](paintings/Claude/bell_warden/questions-step1.md)), 4, 9 and 10
  after step 2 as a blind package.
- **O1** was not asked: the painting session's metadata answers it — `claude-opus-5-5` at
  max effort, on every turn.

## What landed

| | |
|---|---|
| **`paintings/Claude/bell_warden/`** | the prelude and seven passes (line endings made the repository's); `painting.png` and `painting.gif`; `verdict.md`, the painter's message as it wrote it; `NOTES.md` — the painter's own notes with the pack's paragraphs cut and marked, and the filer's account; `reports.txt`, the session file's 27 saved reports; `ex/exercises.py`; `evidence/`, seven pictures; `versions/`, thirteen recovered scripts — ten versions and checks, and the three preludes they ran with — and a README; `questions-step1.md` |
| **`PAINTINGS.md`** | the painting's section, with the order its passes rebuild in; the reading list, the brief, the convention paragraph and the unfinished list mention it; *seven of the twenty-three* |
| **`scripts/probe_cohort_session.py`** | the `bell` entry, and a `Painting.order` field for a painting whose passes were not run in their numbering — a pass run twice is listed twice, and the tables call the second run `(again)` |
| **`SUGGESTIONS.md`** | the round open at the top: 9 engine items (the ninth from the painter's answers) and 4 documentation items, M/O/R per row, three struck where they changed shape; the counts in its opening |
| **`CALIBRATION.md`** | the stub of *The bell-warden's round*: the rebuild, the versions, the spark, what it read |
| **`PLAN-0.8.0.md`** | committed; its status, section 1, rows 4, 6, 8, 9 and 12, 4A4, 4D, section 6's answers, and steps 1 and 2 corrected in place |
| **`README.md`, `llms.txt`** | *twenty-three* paintings, *twenty-two* painters, and the register's open round |
| **`.gitignore`** | `paintings/**/looks/`: this painting's passes write their looks into `looks/`, and a rebuild in place would otherwise leave them untracked |

## What filing found

**The painting session's transcript is the evidence.** The plan was written from the
painter's folder and its session file, and asked the painter to rebuild what it had
thrown away. The session's transcript, on the owner's machine (the painting ran from
14:21 to 14:58 UTC on 2026-09-25), holds every script write and edit, every report the
painter saw, and its reasoning between them:

- **Question 1, measured**: about 22,300 words printed before the first mark, 21,262 of
  them the documents' — the README's first 400 lines of 417, `PAINTER.md` to line 700 of
  754 (not *Sign it*, and the painting is unsigned), `REFERENCE.md` to line 520 of 723,
  and twelve of `RECIPES.md`'s twenty-one entries (not *A scene with straight edges*,
  the one with `smooth=False`). None of `--count`, `cost()`, `cost_line()`,
  `--alternatives`, `explain`, `diagnose`, `preview()` or `compare()` was ever run.
- **Question 2, settled**: the details pass's second rehearsal read the head's top at
  `0.52`, the painter added two `s.dry()` calls, and the third read `0.52` again; its
  reasoning then put it down to the eye. D has no case from this painting. What is left
  to ask is whether the painter saw another.
- **Question 3, recovered**: `reconstruct.py` in the session's scratchpad replays the 27
  script-changing operations in order (10 whole-file writes, 15 in-place Python edits,
  one `cat` heredoc, one `sed`). The final state is byte-identical to the painter's
  folder, and each of the 28 `easel run`s, re-run on `s.replay(upto=report.at)`, gives
  its saved report word for word. The run that raised raises again. Eight versions and
  the first drawing are filed. Each was re-run through the command lines their README
  gives, and each printed its report exactly; the two drawing checks and the first
  drawing redraw their pictures to the pixel.

**And four things nobody had asked about:**

- **The rebuild order.** The passes rebuild the log exactly (292 records, 280 spent,
  export 0 pixels off, on this machine) only as p01, p02, p03, p01, p04 to p07. In
  numbered order 12.4% of the pixels move (2,131 of them by more than 8 levels, the most
  by 87). The drawing ran three times: twice before the room — the second adding the
  `s.erase()` that is record 0 — and once after the plinth.
- **`union()` came first** (plan row 8 corrected): the first drawing's creature was a
  union of eight ellipses and ribbons that read as a spiky blob. It is the silhouette
  recipe's real failure case, filed as `versions/prelude_union.py`.
- **The spark did not land** (row 12): a `round_hard` dab at `0.0028` changed two pixels,
  by at most 21 levels; its record carries `0.19` paint, which `easel log` prints as *NO
  PAINT LANDED*, and nothing at the call said so. Step 2 measures where a round dab stops
  landing.
- **The feather was read** (row 9): `REFERENCE.md`'s hold paragraph and arguments row,
  both inside what the painter printed.

## Decisions and gotchas

- **The verdict is the painter's own markdown**, from the transcript. Its words match the
  owner's paste exactly (1,099 against 1,071 tokens, the difference all bullet markers);
  the paste had lost the headings and bold in the copy.
- **`plan()` merges.** A session made by `s.replay()` from the finished file carries the
  finished plan. So a version rehearsed before the prelude declared `ground=` reports
  *buried, as the plan says* until the plan is reset (`target._plan = Plan()`). Only the
  room's first rehearsal needs it. The command-line recipe does not meet it, because it
  builds the session from the passes.
- **The versions run from the painting's own folder** with `--prelude` where the prelude
  differs (the cat, the union). `easel run` reads the prelude beside the session file,
  never beside the script.
- **The probe replays the painting in 44 s**, 280 spent, its records the painter's. Its
  passes open at the saved reports' own `at`s: 1, 46, 96, 97, 199, 269, 286.
- **`import easel` resolves to the site-packages 0.7.0 wheel** on this machine, not the
  checkout. Every measurement here put `C:\git\EaselAPI\src` first, and `src/` is `v0.7.0`'s.
- **The guide's grep list does not exist.** `LESSONS.md` describes the no-nouns grep as a
  check run by hand. The nouns are in the painting's notes, and the grep found one
  sentence, older than the painting: *A tapered arc*'s horns.
- **A Bash `cd` persists in this environment** and moves the session's working
  directory; every command here starts from the repository root.

## The painter's answers, the same day

The owner put `questions-step1.md` to the painting session, and the painter answered in
`answers.md`, measuring its own file for every claim, and corrected its own notes. Filed
verbatim, and **re-measured here** by laying its log again record by record and each mark
in question on two copies, as painted and dried first
(`scratchpad/verify_answers.py`). Everything holds:

| its claim | re-measured |
|---|---|
| the ember did not land either: `1.6` units, 5 px, at most 22 levels; the glint is the glaze (`133` units) | `1.62` units, 5 px over `0.02`, at most 22 levels, reading `0.22`; the glaze `133.5` units, 268 px, 41 levels |
| the spark: one pixel over `0.02`, `0.2` units | `0.19` units, 1 px (2 by any level) |
| the claw lights lose `0.05` to wet paint and about five times that to size | `0.01` to `0.05` to the wet, as the moved pixels are read; dried, still `0.27` to `0.31` short of `0.60` |
| 13 strokes *NO PAINT LANDED*: the spark, and 2 + 6 + 4 passes of three clipped `block_in`s at `p04:40`, `p05:12`, `p05:14` | exactly those records (163, 164; 214, 216, 218, 220-222; 223-225, 239), eleven at `0.00` units and one at `0.11` |
| the places four ways at the finish, the floor's 90th a miss, the split at 15-18% and 24% | to the hundredth |
| the card names none of `at_value`, `edge=`, `s.dry`, `clip=`, `.shifted`, `.inset`; `clip=` is nowhere in `PAINTER.md`; its scripts use them 29, 14, 10, 8, 4 and 3 times | exactly |

What changed with them: the filed `NOTES.md` quotes the painter's corrected notes and
strikes my *the glint is the ember*; `SUGGESTIONS.md` gains a ninth engine item — marks
that land short or land nothing — and the wet-paint row the painter's withdrawal;
`CALIBRATION.md`'s stub gains *The marks that did not land* and *The places, read four
ways*; and the plan records the answers as decisions: C's format, E1's key and E2's
median with the split, F1's lists and the card's missing line, and **D rewritten** — the
painter withdrew `into-wet` as written, and asks instead for a fact at the call for any
mark that lands far short of its own value, whatever the cause, and for the strokes that
landed nothing on C's line. Section 5's first row is settled: the decline stands.

## File map

| File | Change |
|---|---|
| `paintings/Claude/bell_warden/**` | new: the painting, as above; `answers.md` added the same day |
| `PAINTINGS.md` | the section; four passages mention it; a count |
| `SUGGESTIONS.md` | the round, open; the opening's counts and state |
| `CALIBRATION.md` | *The bell-warden's round*, a stub |
| `PLAN-0.8.0.md` | new to the repository; corrected in place |
| `NOTES-step1.md` | this file |
| `scripts/probe_cohort_session.py` | `Painting.order`; the `bell` entry; `(again)` |
| `README.md`, `llms.txt` | counts |
| `.gitignore` | `paintings/**/looks/` |

## Next

- **A second painting**, *Wenna Brask*, was painted against 0.7.0 the same morning by
  another session, with the first painter's notes and scripts in hand, and gave its own
  verdict. The owner chose to file it with the pack's details out and fold its verdict
  into this round: a second PR, on top of this branch.
- **Step 2**: `scripts/probe_bell_session.py`. Its `--claims` rebuilds from these files
  and adds where a round dab stops landing. `--short` (D, rewritten) takes every
  hand-laid mark's shortfall and the two subject-pass versions that read the head at
  `0.56` and `0.54`. `--thumbnail` takes the union, the cat, the piebald and the arch from
  `versions/`.
