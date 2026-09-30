# Step 9 of `PLAN-0.8.0.md`: the documents -- a first page that is only method, the check's rules as tables, and what the guide says put right

**To understand this, start by reading the plan's F (F1 to F9) with its *Step 9* notes;
then `LESSONS.md`'s *One home per rule* from *The boxes half of that prediction* down,
which is where the text that left `PAINTER.md` went and what the move did not do; then
the card -- `PAINTER.md` down to *Getting started* -- and the two tables under
`report()` in `REFERENCE.md`; and `CALIBRATION.md`'s *What the documents say, measured*,
which is `probe_bell_session.py --written`.**

Branch: `lighter-card-and-tables`, off `main` at `e7e74db` (step 8, #97).

---

## What this step was for

Both painters said the documents were long. The first said which of the text it would
move -- the documents' account of themselves, and the stories -- and which paragraph it
could not parse: ten rules and their thresholds in one block. Two claims in the guide had
stopped being true, one number was said three ways, and every earlier step of the round
had left something for the documents: two recipes that pay for a mark that lays nothing,
the units table's rows, the card's clause for the thumbnail, E4's rule.

## What landed

| | |
|---|---|
| **F1, the first page** | Out of `PAINTER.md`: its four sentences about itself (quoted whole in `LESSONS.md`), the card's instances of a row of like things, the six failures' names (`easel demo mistakes` prints them), the ground line's paragraph (a table row now), the look beside a reference (`PAINTING.md`). In: `at_value` beside `mix`; `s.dry()` and a `s.stroke` with `pressure=`, `opacity=` and `note=` in the order's block; one line for `edge="hard"` and `clip=`; `key=` in the plan's signature; `union` in the row for boxes; `s.thumbnail()` at step 1 |
| **F2, the tables** | `REFERENCE.md`'s `report()` paragraph is a rules table -- *It says*, the check's own words, and *when*, every threshold a code span -- and a standing-lines table, the line, what it measures, when it is said. `PAINTER.md`'s account of the checklist's lines and `PAINTING.md`'s *After every pass* point at them |
| **F3, what was not true** | *Over half the paintings so far have boxes in them*; *where a drawing wants pixels, `s.px(x, y)`*; a place *reads what most of it reads*, and says when it is split; the floor `0.128`, burnt umber alone, in four files; the third question *looked at small -- `s.look(scale=256)`*, in `checklist()` and in the guide; `LESSONS.md`'s count, 94 claims and 21 |
| **E4's rule** | *Plan the place your `why` names, at the value the place will read* -- `PAINTER.md`'s step 4, and *A light's pool on a surface* for a light |
| **F5, links** | every link out of a shipped document goes to the repository by address: `paintings/` in `PAINTER.md` and `RECIPES.md`, `CALIBRATION.md`'s twelve, the README's two |
| **F6, F9** | `--alternatives` and `--count` in the card's loop; *the `budget=300` is this example's* |
| **F7, units** | rows for a round shape's radius, a ribbon's widths and `s.circle()`'s `r`, and the sentence saying what is round in pixels |
| **The two recipes** | *A mass built of planes* lays its dry brush at `load=0.5`; *A silhouette lit from one side* keeps its copies and says what they cost |
| **The record** | `SUGGESTIONS.md`: every row of both painters filled; `LESSONS.md`: the move, the boxes, the count, a protocol bullet; `CALIBRATION.md`: *What the documents say, measured*, *What the box reaches*, a **Boxes** paragraph in *From the sessions*; `CHANGELOG.md`; the plan |
| **The bench** | `probe_bell_session.py --written`; `probe_cohort_session.py`'s candidate gate `a mass once`; `check_guide_blocks.py` names every recommended block that pays for a mark that lays no paint |
| **Tests** | `test_guide.py` (the card's names, links that ship, the signposts' sizes); `test_reference.py` (both tables against the engine, the units rows against the masks); `test_requests.py` *0.8.0 F* (4) |

## Measured as written

`probe_bell_session.py --written`, on this branch:

- **The floor**: burnt umber alone `0.128`; the half-and-half mix `0.137`, and `0.146` to
  `0.132` as its ratio runs `0.3` to `0.7`. Laid solid on `toned_grey` at 1024x768, umber
  reads `0.153` after one pass and `0.129` after eight dried passes or four rounds of
  glazing; the mix `0.161` and `0.137`.
- **The units**: `ribbon(..., 0.05)` is 38 px across a level ribbon at 1024x768, 52 across
  an upright one, 45 at 45 degrees; `ellipse(p, 0.05)` 102 by 76, 102 by 102 with
  `aspect=s.aspect`; a brush's `size=0.05` 51 px on either canvas.
- **The guide's 79 blocks**: `dab-blank` on none; `landed nothing:` on one, the lit
  silhouette's, where it was two.
- **The calls two painters leaned on**: both painters' own counts come back exactly --
  `at_value` 29 and 54, `clip=` 8 and 41, `opacity=` 46 and 97 -- and of the 21, the card
  named 9 at 0.7.0 and names 16.
- **The boxes line over the corpus**: 13 of 24 paintings laid a mass in a rectangle, 11
  none; 41 of 349 masses; 34 of 172 in the twelve made before the guide was restructured,
  7 of 177 in the twelve since.
- **The sizes**: `PAINTER.md` 6,680 words (6,655 at 0.7.0), its card 1,369 (1,369);
  `RECIPES.md` 10,815 (7,823); `REFERENCE.md` 11,242 (8,904). Read as the second painter
  read them, **25,313 words where it was 20,546**.

And `scripts/check_guide_blocks.py`: 79 blocks ok, none told a notice, 22 of 22 demos
failing as they say; `scripts/check_guide_overlap.py` clean.

## Decisions and gotchas

**1. The budget did not come down, and the plan said it would.** F1 reads *then
`FRONT_PAGE_WORDS` comes down to the new size and a little room*. By a diff of its words,
about 490 went out of `PAINTER.md` since 0.7.0 and about 515 came in -- every one a line
this round's painters asked the page for -- so the file is 6,680 words where it was
6,655, and 6,700 already is its size and a little room. Lowering it would have meant
cutting something a painter defended, which the plan rules out (*a move, not a cut*).
`docs.py`'s comment says so. The card is 1,369 words, as it was to the word.

**2. What a painter reads before a mark is longer, and the register says so.** The move
tidied one page. Every other answer of the round is a recipe or a row of the reference --
six recipes, the facts of a dozen new calls and lines, two tables longer than their
paragraph -- and those are the files both painters read most of. *It's long* is both painters'
first documentation row, and both rows now say it is answered for the first page and not
for the corpus. `LESSONS.md` names what would answer it, the handover painter's
instruction: start from what the notices already say at the call, and cut what they have
made redundant, with a measurement behind each cut. **That is a round of its own.**

**3. *Every painter so far has painted boxes* was false the day it was written.** It went
in during 0.6.0's round (`f5a1204`, replacing *you will paint boxes*), when 8 of the 21
paintings then filed had laid none by the check's own count. Nobody had counted. The page
says what the replay says -- *over half the paintings so far* -- and the lesson is in
`LESSONS.md`: *check the painters' numbers* holds for the guide's numbers about painters.
*The step most painters so far have skipped*, of the edges, was left: 17 of the 24 laid a
smudge and the last three none, which settles nothing, since an edge is also lost with
paint.

**4. The rules table is named by what the check prints.** A first draft had a column each
for the rule, when, the number and the words, and ran to 1,321 words for a paragraph of
855. The first column is now the check's own words in italics -- what a painter has on
screen when it looks a rule up -- and the numbers are code spans in the second: 1,129 for
the section. `test_reference.py` builds each row's numbers from `easel.session`'s
constants and finds each row by the words `_pass_findings` prints, joining the adjacent
string literals in its source first; a pass laid in the test prints all ten standing
lines, and each must have a row.

**5. The planes recipe's dry brush.** A `bristle` at `size=0.03`, `load=0.35` carried
`0.2` units of paint on the guide check's 400x300 canvas and `14.1` at 1024x768; at
`load=0.5`, `12.1` and `215.8`. The recipe lays it at `0.5`.

**6. The lit silhouette keeps its far copy across the form.** A copy shifted away from
the light reaches past the silhouette, and a pass of it wholly there is charged and lays
nothing. Which pass that is turns on the wander a mass takes from the stream, so it was
laid over seeds: as written (`direction=20`), 102 strokes and a mean `3.79` lost at
400x300, `2.12` at 1024x768, never none. **Along the form (`direction=80`) it is 83
strokes and almost none lost -- and an edit to that was made and taken back**: its passes
then lie beside the join strokes, and on seed 1 over the demo's passage the check says *a
graded passage*, 17 marks, at both sizes. That is the seed the guide check lays, and rule
2 holds a recommended block to saying nothing. One seed in a single scan had looked
clean, which is why the seeds bench exists. So the recipe says what its copies cost, in
the check's own words.

**7. The graded rule was benched and left.** The one gate that would let the recipe run
along the form counts a mass's passes once (`GATES["a mass once"]` in the corpus probe,
the bench only). Over the corpus's 356 painted passes it fires on five of the engine's
seven: quiet on the pier's stacked fields, which the painter read blind as no passage,
and on the first greenhouse lighthouse's beam, a gradient laid as five flat masses, which
it read as one. A count of masses does not separate them, and the plan parks this rule
for the round (4G). Not built.

**8. The lettering pass's two findings are left to the rule.** Step 7 asked whether *one
brush at one size* and *detail before the masses* should know a stroke laid along a
glyph. No painting has laid lettering yet, and the recipe says what the check will say of
it; the next painting that writes -- the pack's note and its map, on 0.8.0 -- is the
measurement.

**9. The card's instances were a painting's subject.** *Four fingers, five pickets, a row
of windows* and *a cupped hand seen from the front* had stood on the first page since the
hands session's round, three releases. The card states the rule with no instance now;
the body keeps the one story its painter kept, which names it, and step 1's bullet.

**10. For the claim.** `CALIBRATION.md` links `PLAN-0.8.0.md` at `blob/main`; the claim
takes that file out, so the link goes to the tag then, as 0.6.0's do.

**11. On this machine.** As before: `PYTHONPATH=src`; a Bash `cd` moves the session;
`ruff` is `python -m ruff`. A Python heredoc that wrote a test turned a regex's `\n` into
a real newline; the Edit tool fixed it. A long bench piped through `tail` shows nothing
until it ends -- write it to a file with `python -u`.

## What step 9 did *not* touch

What any mark lays: no golden, sampler or rebuild moves. The engine's rules: the graded
rule (item 7) and the two the lettering trips (item 8). The length of the corpus (item
2). A mass that skips the passes falling wholly outside its clip would save the lit
recipe's lost strokes and the Bell-Warden's twelve, and would renumber every script that
lays one; it is a default's move, for a painter to decide with the corpus beside it. The
version: 0.8.0 is cut in step 10.

## File map

| File | What changed |
|---|---|
| `PAINTER.md` | the card's vocabulary and clauses; the four sentences out; step 4's places, plan rule and floor; the boxes claim; the checklist's lines and third question; exercise 7's shape; the shell's `--thumbnail` |
| `REFERENCE.md` | the two tables under `report()`; three units rows and the sentence |
| `RECIPES.md` | the planes' dry brush; what the lit silhouette's copies cost; a light planned as a place; a dab's touches; the link |
| `PAINTING.md` | the floor; `thumbnail` among what is free; *After every pass*; the look beside a reference |
| `CALIBRATION.md` | *What the documents say, measured*; *What the box reaches*; **Boxes** in *From the sessions*; twelve links |
| `DIAGNOSIS.md`, `README.md`, `llms.txt` | four rows pointing at the round's recipes; the plan's row and two links; the sizes and the recipes' list |
| `LESSONS.md` | *One home per rule*: the boxes, the move, what it did not do; the count; a claim that is the tool's own line; *record where it stopped reading*; *Verifying a change* |
| `SUGGESTIONS.md`, `CHANGELOG.md`, `PLAN-0.8.0.md` | every row filled; the step's entry; the status and the *Step 9* notes |
| `src/easel/session.py`, `palette.py`, `checklist.py`, `docs.py` | the third question's words; the floor in the docstrings; why the budget stands |
| `scripts/probe_bell_session.py`, `probe_cohort_session.py`, `check_guide_blocks.py` | `--written`; `a mass once`; the blocks that pay for nothing |
| `examples/exercises.py` | exercise 7's shape, and exercise 10 |
| `tests/test_guide.py`, `test_reference.py`, `test_requests.py` | the tests above |
| `NOTES-step9.md` | this file |

## Next

- **Step 10: cut 0.8.0** -- the version in `pyproject.toml`, `src/easel/__init__.py` and
  both entries of `server.json`; `CHANGELOG.md`'s entry without the claim; the tag on the
  owner's word; then the claim, which retargets `CALIBRATION.md`'s link to the plan (item
  10) and takes the plan and these notes out.
- **For the round after**: the corpus's length (item 2); a mass's passes outside its clip;
  the graded rule and stacked masses (item 7); a darker dark with a hue, the first
  painter's yes to question 10; and the lettering findings, once a painting has written.
