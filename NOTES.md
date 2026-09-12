# Phase notes: the documentation round

*To understand this, start by reading [`SUGGESTIONS.md`](SUGGESTIONS.md) — now a
register of what was wrong and what was done rather than a request list — then the new
[`PAINTER.md`](PAINTER.md) preamble and its file table, then
[`LESSONS.md`](LESSONS.md)'s new section **The essay is finished at its size. Split by
function; never cut**, which is where the rules governing all of this now live.*

Every open documentation item from three painting sessions, the synthesis across them
and the owner's two questions is done. No engine behaviour changed. The only Python
touched was the plumbing that ships and checks the documents.

## The shape of it

**The guide was split into five files by function, moving rather than cutting.** Three
sessions each said the same two things — the guide is long, and the essay in it is what
made the rules stick — and three attempts to shrink it by editing had failed. Nothing
was deleted: the 17,625-word `PAINTER.md` became a 9,463-word `PAINTER.md` plus a
10,354-word `PAINTING.md`, and the ~2,200-word difference is new material the sessions
asked for.

| File | What it is | Words |
|---|---|---|
| `PAINTER.md` | the method: the order of work, *What you are bad at*, the exercises, the checklist | 9,463 |
| `PAINTING.md` | **new** — the reasons: colour, wet paint, the brushes, working from a reference, *Masses that are not rectangles*, the rest of the API | 10,354 |
| `RECIPES.md` | **new** — fourteen procedures collected out of the paintings' own pass scripts | 3,121 |
| `REFERENCE.md` | the facts, unchanged in role | 2,577 |
| `CALIBRATION.md` | the numbers | 7,699 |

`PAINTER.md` is now held to a **10,000-word budget asserted by
`tests/test_guide.py`**, because the no-growth rule in `LESSONS.md` was a preference and
the guide doubled under it. `easel.guide.FRONT_PAGE_WORDS` is the one number;
`scripts/check_guide_blocks.py` prints it and CI enforces it through the test.

## Decisions worth knowing

**The 5,000–6,000 word target was not met, on purpose, and the reason is in three
files.** The synthesis asked for that figure *and* listed the contents the file should
keep. Those contents are about 8,500 words on their own, so the target was only
reachable by cutting them — which items 1, 2 and 4 of the same list explicitly forbid.
The budget is 10,000 and the honest claim is halving, not fifthing. Written down in
`guide.py`'s docstring for `FRONT_PAGE_WORDS`, in `LESSONS.md`, and in `SUGGESTIONS.md`,
so the next session can overrule it knowing why.

**"Read it in two goes" became a file boundary.** That instruction was tried and the
third session read straight past it. A boundary cannot be read past.

**The worked-example trade was resolved rather than maintained.** `paintings/` was
pointed at from `README.md` and deliberately not from the guide, so the cost of hiding
it was paid silently by the painter who would most have benefited. The
decide-then-read protocol dissolves it: a painter who chose a subject before opening the
repository cannot be steered by a noun. All three of `PAINTER.md`, `PAINTINGS.md` and
`README.md` now point there with the same condition attached, in the same words.

**Everything factual here was checked against the engine before it was written down**,
rather than copied out of the session reports — which is `LESSONS.md`'s *check the
painters' numbers*, applied to a documentation round. All of it held, and two of the
results are numbers the documentation did not previously have. The probes were scratch
scripts and are not kept; each is a dozen lines and the conditions are stated in
`CALIBRATION.md`, which is the point of the new rule there.

| Claim | Result |
|---|---|
| Where a pass stack starts | Confirmed. `0`/`"horizontal"`/`"axis"` → top; `90`/`"vertical"` → right; `45` → upper right |
| `solid=True`'s pass structure is ~`0.03` at any opacity/pressure | Confirmed: sd `0.009`, row peak-to-peak `0.025`–`0.033` across four combinations |
| The inward scumble's fall-off | Reproduced, **on a stated patch radius this time** — that was the whole point of the item |
| A glaze is strong in proportion to its distance in hue | **New measurement.** At `opacity=0.14` a distant glaze moves the value `+0.087`; at `0.05` the underlying hue is already neutral |
| The recipes' code | All 74 python blocks across the three guide files execute |

**`CALIBRATION.md` gained a standing rule at the top**: every number states the brush,
the size and the canvas it was measured on, and a claim with no test behind it says so.
That rule was bought — a fall-off table measured on an unstated patch was read as a
fall-off for a year, applied to a larger patch, and cost three rehearsals.

## Pitfalls hit

- **The split had to conserve every word, and that was checked arithmetically** rather
  than by reading: the slice script printed 8,209 + 8,137 + 1,279 = 17,625, the original
  total. Do the same if this is ever re-split; a section silently dropped in a move is
  invisible in review.
- **`check_guide_blocks.py` needed `textwrap.dedent`.** A fenced block nested under a
  list item carries the list's indentation — valid markdown, `IndentationError` to
  `exec`. The new checklist block is the first one in the guide to be nested.
- **The subject-noun grep caught two leaks in material I had just written**, exactly as
  `LESSONS.md` predicts it will: a multi-script example using two of a painting's pass
  filenames, and `RECIPES.md`'s own paragraph about not naming subjects naming one as a
  counter-example. Run the grep over `PAINTER.md`, `PAINTING.md`, `RECIPES.md` and
  `REFERENCE.md` — never over `README.md` or `PAINTINGS.md`, which name subjects on
  purpose.
- **`PAINTINGS.md` claimed all three paintings were made having read only the guide.**
  Two had read three and five other files, and both said so in their own reports. Fixed
  per painting, because the difference is what makes their agreement worth anything.

## What changed, by file

**New:** `PAINTING.md`, `RECIPES.md`.

**Documentation:** `PAINTER.md` (split, plus the four-mistakes table, the *rehearse
everything* rule, two checklist lines, the `solid=True` note, the boxes bridge, the file
table and the paintings pointer) · `REFERENCE.md` (where a stack starts; the new
documents and flags) · `CALIBRATION.md` (the measured-on rule; a `glaze` section; the
solid pass-structure table; the scumble tables restated with their patch) ·
`LESSONS.md` (the split and its rules; the warnings-file answer; the worked-example
resolution; the unprompted-stage note; current test and check counts) · `README.md`
(three paintings; the five-file table; the third engine round; the decide-first
condition) · `PAINTINGS.md` (what each session actually read; the decide-first framing) ·
`llms.txt` (the map) · `SUGGESTIONS.md` (rewritten as a register: 81 KB → 26 KB).

**Code, plumbing only:** `src/easel/guide.py` (`DOCUMENTS` gains two entries;
`FRONT_PAGE_WORDS`) · `src/easel/cli.py` (`easel guide --painting` / `--recipes`) ·
`src/easel/mcp_server.py` (the `guide` tool's document list) · `pyproject.toml` (the
wheel force-include) · `tests/test_guide.py` (the word budget, and that the essay is
where the length went) · `scripts/check_guide_blocks.py` (all three guide files;
dedent; the budget line).

## State

`508 passed, 79 skipped` (was `498 passed, 79 skipped`); `tests/test_mcp.py` `76
passed` with the extra installed; `ruff check src tests scripts examples mcpb` clean;
`check_guide_blocks.py` `74 ok, 0 failed, 12 skipped` and `PAINTER.md` 537 words inside
budget; the wheel builds and carries all five documents at `easel/docs/`.

## Deliberately not done

- **The pass linter** — `Session.report()` or `easel run --check`, the thing that should
  exist instead of a warnings file. It is an engine change, it is specified in
  `LESSONS.md` with its candidate rules and a way to prototype it against a finished
  painting's log, and every rule that becomes a check can then leave the guide.
- **The rules card for a compacted session.** No session has been compacted, so there is
  nothing to judge it against.
- **The split's own measurement.** Two fresh sessions under the protocol, one given only
  the method, the recipes and the reference. The prediction is written down in
  `LESSONS.md` so it can be wrong.
- **The depth-order rewrite**, which has failed three runs and is still the oldest open
  item in `LESSONS.md`. It needs a design with a measurement attached, not an edit.
