# Step 9 of `PLAN-0.6.0.md`, part one: the symptom index as a command (G5)

**To understand this, start by reading [`src/easel/diagnosis.py`](src/easel/diagnosis.py)
— its module docstring is the whole argument — then `headings`, `heading_line` and
`section` in [`src/easel/docs.py`](src/easel/docs.py), which are what turn a pointer
into a passage, then the front page of [`DIAGNOSIS.md`](DIAGNOSIS.md), then
`test_every_pointer_comes_back_as_a_passage` in
[`tests/test_diagnosis.py`](tests/test_diagnosis.py).**

Branch: `f-diagnose`, off `main` at `e62f298`.

---

## What this step was for

Step 9 is workstream G, which is eight open sub-items and several PRs. This is G5, and
it was picked first because it is the only one with no dependency on anything step 6
did not build.

`DIAGNOSIS.md` had two problems, and neither was its contents.

**It was not in the wheel.** The build shipped five documents; this was a sixth file at
the repository root. So `grep -i rings DIAGNOSIS.md` — the interface the file's own
first page named — worked from a checkout and nowhere else, and a painter who ran
`pip install easel-paint` had no file to grep.

**And the one session that did have it followed none of its pointers**, in 293 strokes:
five rows recognised on sight and repaired from the remembered description, and a
recalled row has no measurement attached. It repaired the chisel staircase with
`edge="clean"` while the row's own target held a cheaper repair at the other end of the
same table. `LESSONS.md` asked that the file not be changed on n=1. It is not changed.
What changed is that following a pointer now costs nothing.

## What landed

| | |
|---|---|
| `easel diagnose <what you can see>` | matches your words against the rows and prints **the passage**, not the pointer. `--list` is the symptoms alone — what `grep` used to give |
| `diagnose` MCP tool | the same, `brief=` for the listing. A client cannot grep a file it has no filesystem for |
| `easel.diagnosis` | rows, matching, and a `Pointer` that resolves itself to its section |
| `DIAGNOSIS.md` shipped | `docs.DOCUMENTS`, the wheel force-include, `easel guide --diagnosis`, the `guide` MCP tool's sixth document |
| `docs.headings()` / `docs.heading_line()` | one scanner for what a heading is; prefix-to-heading-line resolution |
| `tests/test_diagnosis.py` | all 92 pointers resolved to real passages, plus matching and the command |

## Decisions and gotchas

**1. Shipping the index made it carry a bug the other five had already been fixed for.**
B7 — 35 characters outside cp1252 across the shipped documents, which kill
`print(easel.docs.read(...))` on a Windows console — was closed for the five. The index
was not one of them, so it still held **92 `→`**. Adding one key to `docs.DOCUMENTS` made
`test_a_shipped_document_prints_on_a_cp1252_console` fail on the spot, which is that
test doing its job on a file it had never been pointed at. All 92 are `->` now, and
`test_diagnosis.py`'s own `POINTER` regex had to move with them. **Adding a document to
`DOCUMENTS` is not a one-line change; it subjects a file to five tests it has never
faced.**

**2. `DIAGNOSIS.md` is exactly at its 130-line cap, and the preamble rewrite had to be
line-for-line.** The cap is the only thing holding the file to being an index, and its
own test says to cut rows rather than raise it. The new front page is the same length as
the old one to the line. **Anyone adding a row has to cut one**, and that now includes
this round: nothing the 0.6.0 checks added has a row here.

**3. `section()` had fence-skipping on one end of its search and not the other.** It
found a heading by scanning every line for an exact match — including lines inside
fenced code blocks — and only stepped over fences when looking for where the section
*stopped*. Both halves now go through `docs.headings()`, one scanner, because `section`
and `heading_line` disagreeing about what a heading is would show up as a passage that
ends in the wrong place and nothing in the suite could see it.

**4. A pointer is a prefix, and that is load-bearing rather than sloppy.** The rows say
`` `CALIBRATION.md` -> *`block_in`* `` where the heading is `` ## `block_in` ``. So
`heading_line` matches on the text with the markdown stripped: exact match first, then
the first in document order — which is the `##` rather than a `###` nested under it, so
a pointer that names a section gets the whole section. This is what lets the rows stay
readable prose instead of becoming anchors.

**5. *Lands on a heading* is a weaker promise than the command makes.** The old test
checked that each pointer's heading existed. That was right when a person followed the
pointer and could look around; it is not enough now that the tool hands back whatever is
under it. `test_every_pointer_comes_back_as_a_passage` does what the command does, to
all 92, and asserts more than twenty words come back. A heading that exists over an
empty section was cosmetic before and is a broken answer now.

**6. Matching is word overlap plus one plural rule, and the rows are why that is
enough** — they are written in the words a painter uses for the thing in front of them,
which was already the design. The one thing measured rather than assumed is the
**fallback to the section heading**: `gradient` appears in thirteen group headings and
in **zero** symptom rows (the rows say *graded*, *gradated*, *a stack of bands*), so
matching rows alone answers nothing to a perfectly reasonable question. The fallback
fires only when no row matches at all, so it never dilutes a precise question.

**7. `answer("")` had to fall back to the listing.** Both the no-argument CLI form and
the MCP tool's default promise *every symptom it covers*, and `match("")` returns
nothing — so without the fallback the friendliest way to call it answered *Nothing in
the index matches `''`*. Caught by writing the parser help before the code.

**8. A sixth shipped document is not a sixth guide file.** The index states no rule, so
`PAINTER.md`'s *every rule in these five files* and `README.md`'s *one file of five* are
still true and were left alone. What was stale were the counts about **shipping**:
`README.md`'s *all five documents ship inside the wheel*, `REFERENCE.md`'s *the `guide`
tool returns any of the five*, and `docs.py`'s own *there are five of them now*.

**9. `mcpb/manifest.json` said *the twelve CLI verbs* and there are sixteen.** Nothing
holds that sentence to the parser — `tests/test_server_json.py` checks the name, the
description and its length, not the body — so it went stale when `plan`, `check` and
`explain` landed in steps 3, 5 and 7. Fixed in passing because `diagnose` made it one
worse, but **the claim is still unheld**: the same shape as the changelog claims
`tests/test_version.py` now holds to tags. Worth a test, and it is not this step's.

**10. `scripts/check_guide_overlap.py` has its own hardcoded document tuple** and does not
read `docs.DOCUMENTS`, so the index did not leak into the one-home-per-rule check. That
is the right outcome — the index restates the guide on purpose, which is the one thing
that checker exists to forbid — but it is luck rather than design. If the script is ever
changed to read `DOCUMENTS`, `DIAGNOSIS.md` has to be excluded explicitly.

## Open, and for the owner to rule on

**Whether a painter reaches for `diagnose` unprompted.** This is the real question the
grep arm was groping at, and it is now in `LESSONS.md` with the protocol: the next run
should record whether the command was in the instructions and how often it was called.
The arm as originally framed — *grep or read* — is moot, because both are one call now.

**Codes and symptoms are two vocabularies with no link between them.** `easel explain
<code>` and `easel diagnose <words>` reach the same passages by different routes and
neither knows about the other. A row whose target is a notice's measurement could name
the code, which would let a painter who saw `chisel-staircase` fly and a painter who
merely *sees* a staircase land in the same place with the same words. Not built, not
costed, and it would spend lines against a cap that is already met.

**Ruled 2026-09-21: not this round.** Costed since: sixteen of the twenty-five codes
already resolve to the passage a row points at, nine of them to the same `###`, so the
two commands print the same text and only the name is missing. The cap is no obstacle
after all — it counts lines, and a code named inside a row adds none. Revisit once a run
shows whether a painter calls either command.

## What step 9 did *not* touch

**G5 is one of eight.** Still open in workstream G: **G2** the entry path, **G3**
`easel demo <recipe>` with the failure blocks and the notice-clean invariant, **G6** the
new recipe, **G7** the finding-1 fixes, **G8** the voice pass, **G9** the small facts
(vision required, the region ninths, `upto=`/`n`/`last=`), **G10** the budgets
(`FRONT_PAGE_WORDS` is still `10_000` against a `PAINTER.md` of 6,299 words), **G11** the
rest of the record. G4 landed with step 7.

Step 6 is unchanged and still part-done: `spill` (D1), D2 and D3 are not started — and
G3's invariant partly depends on them, which is why it was not taken first.

`RECIPES.md`'s *quiet gradient: a `flat` scallops* paragraph is still what step 8 left
it: the migration map's row for it names two carriers that were both dropped, so the
paragraph stays and the row is wrong. **That is G7's to settle and it is still open.**

## File map

| File | What changed |
|---|---|
| `src/easel/diagnosis.py` | **new** — `Pointer`, `Row`, `rows`, `match`, `passages`, `answer`, `listing` |
| `src/easel/docs.py` | `"diagnosis"` in `DOCUMENTS`; `headings()` and `heading_line()` new; `section()` refactored onto them; the module docstring's document count |
| `src/easel/__init__.py` | `diagnosis` bound and in `__all__`, so `dir(easel)` lists it — the documents tell a painter to call `easel.diagnosis.answer()`, and absence from that listing is a claim |
| `src/easel/cli.py` | `easel diagnose` (`words`, `--list`), `guide --diagnosis`, `_cmd_diagnose`, dispatch |
| `src/easel/mcp_server.py` | `diagnose` tool; the `guide` tool's sixth document |
| `pyproject.toml` | `DIAGNOSIS.md` in the wheel force-include |
| `DIAGNOSIS.md` | 92 `→` spelled `->`; the front page names the command instead of `grep` |
| `tests/test_diagnosis.py` | the `->` regex; the parser held against the regex; all 92 pointers resolved to passages; matching; the shell |
| `tests/test_mcp.py` | `diagnose` over the wire, brief and full |
| `REFERENCE.md` | `diagnose` in the shell block and `--diagnosis` on `guide`; a paragraph in *What the tool will tell you*; the MCP *five documents* |
| `README.md`, `llms.txt` | six documents ship; `diagnose` and `explain` in the examples |
| `CHANGELOG.md` | `### The symptom index, answered rather than grepped` under `[Unreleased]` |
| `LESSONS.md` | the grep-arm protocol item rewritten: what it settles, and what is still open |
| `SUGGESTIONS.md` | the ninth session's `DIAGNOSIS.md` row gains what G5 did |
| `mcpb/manifest.json` | *twelve CLI verbs* -> sixteen (stale since step 3); `diagnose` named in the guidance line |
| `PLAN-0.6.0.md` | status: step 9 part-done, G5 built |

---

# Step 9, part two: the fixes and the small facts (G7, G9)

**To understand this, start by reading `main()` in
[`scripts/check_guide_blocks.py`](scripts/check_guide_blocks.py) — the notice-clean
invariant is what found the two faults nobody had read — then the three answers under
*Masses that are not rectangles* in [`PAINTING.md`](PAINTING.md) and *A graded field that
is most of the picture* in [`RECIPES.md`](RECIPES.md), which are the two blocks that
moved, then the two corrected rows in section 5 of [`PLAN-0.6.0.md`](PLAN-0.6.0.md).**

Branch: `g-fixes-and-facts`, off `main` at `69254f8`.

---

## What this step was for

G7 is *fixes to what is there* and G9 is *small facts*. Both were picked because neither
depends on anything step 6 did not build. **Between them the plan listed ten items, and
four were already done** — closed in passing by the steps that had reason to touch the
same files. That is the first finding of this step, and it is a process one: a plan row
is a claim about the repository, and it goes stale exactly like any other claim.

| Plan row | Actually |
|---|---|
| G7: *a mass built of planes*, *a form that turns* (finding 1) | **done in step 6**, in the commit that landed `chisel-staircase` — it fixed all three offending recipes |
| G7: the ground contradiction (finding 11) | **done in step 5**, engine and recipe together |
| G9: `pip install easel-paint` -> `import easel` | **already there**, with the *never `pip install easel`* warning beside it |
| G9: named-region extents | **already there**: `REFERENCE.md` has the full table and calls the ninths out in prose |
| G9: what `upto=`, `n` and `last=` count | **already there**, on the `log(last=)` line |
| G9: the verb x (`clip`, `edge`, overrides) matrix | **already there**, landed with #58 |

## What landed

| | |
|---|---|
| **Every runnable guide block is notice-clean** | and `scripts/check_guide_blocks.py` fails if that stops being true, naming the block, the document and the code |
| `PAINTING.md`, *Masses that are not rectangles* | the clean-edge answer stops demonstrating a brush the paragraph under it forbids |
| `RECIPES.md`, *A graded field...* | the field runs off the top of the canvas, so no pass is a stub |
| `RECIPES.md`, *A volume of lit air* | `dry()` after the films as well as before, with the measurement |
| `PAINTER.md` | the card's `undo` row and *What you are bad at* name `cover(..., edge="hard")` |
| `PAINTING.md`, the broken-pass rule | scoped to what it was earned on, with the crossers named as the exception |
| `README.md`, `llms.txt`, the package docstring | vision is a requirement, and why |
| `PLAN-0.6.0.md` | two migration-map rows corrected; G7, G9 and the status line brought current |

## Decisions and gotchas

**1. The two real faults were found by running the guide, not by reading it.** Both
blocks sat under prose that was *correct*, which is why no review had caught them: the
paragraph under the three answers says a clean edge needs a brush under a quarter of the
shape's shorter extent, and the block beside it used 34%. Reading either one alone finds
nothing. **The only thing that finds this is executing the block and asking the engine
what it said** — which is finding 1's lesson applied to the whole file rather than to the
three recipes step 6 happened to touch.

**2. A check can be silenced without the picture improving, and that nearly happened
here.** `scumble-wedge` compares the *ratio* between the first and last pass, and on the
graded field the ratio falls under the threshold at 6° and 8° — not because the passes
get better but because **both ends become stubs**. Turning the pass angle two degrees
would have produced a green check and the same bad field. The middle pass is full width
at every angle and the ends are short at every angle, which says the shape is the fault,
not the angle. **The shape moved.** Sweeping the parameter before choosing the fix is
what showed this; the first candidate fix was the angle.

Both versions were then rendered at 640x480 and **looked at**, which `LESSONS.md` asks
for and which measurement alone would not have settled: the old recipe leaves **a patch
of bare toned ground across the top of the field**, plainly visible, where the stub
passes failed to close. The notice was not being pedantic about a ratio — it was naming
a hole.

**3. The graded field's outline contradicted its own first sentence.** The recipe opens
with *a third of the canvas or more, graded, with no outline anywhere in it* and then
handed the verb a six-vertex polygon whose top edge wobbled across about 1.2 pass steps
inside the canvas. The fix is the recipe's own sentence, which is the comfortable case:
**the prose was right and the code was wrong.** Both faults this step found are that way
round, which is worth remembering the next time a block and a paragraph disagree.

**4. Two migration-map rows had lost both their carriers**, and one of them was already
flagged in part one. A row says *this prose leaves when that check lands*; when the check
is declined and the fallback is not built, the row is a promise nothing will keep.
`PAINTER.md`'s card row 4 (carriers: F1, `spill`) and `RECIPES.md`'s quiet gradient
(carriers: F4, `scumble-few`) are both in that state — F1 and F4 were declined in step 8,
`spill` and `scumble-few` are not built. **Both now say so in the map**, and in both cases
nothing leaves. **A declined default move silently invalidates every migration row that
named it**, and step 8 did not go back through the map.

**5. Finding 8 is the case where the documentation has to carry it.** `cover(edge="hard")`
has existed all along; the card never mentioned it; F1 would have made mentioning it
unnecessary and was declined *pending `spill`*. So the keyword goes in the card and in
`PAINTER.md`'s *What you are bad at*, with the measured pair. **A deferred default is not
a closed finding** — it is the same finding with a longer wait, and the prose has to hold
it in the meantime.

**6. The cover ratio depends on the size of the patch, so the published number needed its
conditions.** Reproducing it gave `1.57x` on a large span and `2.18x` on the probe's own
small patch, against the published `2.32x` — the overhang is a brush either way, so the
smaller the place the worse the ratio, and my recomputation differs from the probe's in
where it puts the *painted* threshold. **The published figure is quoted and cited**
rather than a fresh one published beside it, and the sentence says it is a repair-sized
patch. Two numbers for one quantity in two files is how a document starts lying.

**7. `dry()` after the films is real, and the first measurement said it was not.** A
`canvas.rgb` that is float `0..1` read as though it were `0..255` turns a `0.30` move
into "0/255" — the measurement said drying changed nothing, which was the wrong scale
rather than the wrong conclusion. Corrected: up to `0.30` in value where a mass crosses
the beam, `0.40` where a stroke does. **Check the units of the array before believing a
null result**, particularly a convenient one.

**8. The rule gave, not the recipe, and that was an evidence call.** `PAINTING.md`'s *do
not lay one broken pass across the whole canvas* and the graded field's two edge-to-edge
crossers at `load=0.40`/`0.35` are a flat contradiction. The rule has no measurement
behind it anywhere in `CALIBRATION.md`; the recipe was taken out of paintings. So the
rule was scoped to the mechanism it names — *it stays visible under every later stroke*,
which is about what sits underneath — and the crossers, laid last on a passage nothing
will cover, are named as the exception.

**9. A cross-reference can break the one-home-per-rule check.** Linking the graded field
from `PAINTING.md` in the same words `PAINTER.md` already used put a 12-word run in two
files, because the checker strips markup and the anchor slug survives as one long token.
**The link text had to differ, not the rule.** Worth knowing before adding any link to a
heading that is already linked from somewhere else.

**10. The helper that applied these edits rewrote line endings, and the diff hid it.**
`.gitattributes` normalises to LF on commit, so `git diff --stat` looked clean while the
working copies had become CRLF. The only visible symptom was git's *CRLF will be replaced
by LF* warning naming exactly the files touched. Preserve a file's own endings when
rewriting it.

## Open, and for the owner to rule on

**`scripts/check_guide_blocks.py` still runs only when somebody remembers to run it.**
It is not in CI and not in the suite — and `tests/test_guide.py`'s own
`test_one_home_per_rule` exists because the overlap checker had exactly that problem and
stopped being true without anybody noticing. The block run takes **85 seconds**, against
an overlap check that is instant, and the `test` job is five matrix combinations. So this
is a cost decision rather than an oversight, and **G3 is the right place for it**: that
step is extending this script anyway, and `easel demo` will be rendering the same blocks.
Until then the invariant holds only for whoever runs the script. **Since 2026-09-21 a row
of `PLAN-0.6.0.md`'s *Loose ends*, owned by G3.**

**Whether the entry path should point at `diagnose` and `explain` before the guide.**
Untouched here, and still G2's.

## What step 9 part two did *not* touch

**Still open in workstream G: G2** the entry path, **G3** `easel demo <recipe>` with the
failure blocks and the second half of the notice invariant, **G6** the new recipe, **G8**
the voice pass, **G10** the budgets (`FRONT_PAGE_WORDS` is still `10_000` against a
`PAINTER.md` of 6,363 words — the file grew 64 words here), **G11** the rest of the
record. G4 landed with step 7 and G5 with part one.

Step 6 is unchanged and still part-done: `spill` (D1), D2 and D3 are not started. Two of
this step's decisions wait on them — the card's `undo` row and the quiet gradient
paragraph both stay until `spill` and `scumble-few` exist.

## File map

| File | What changed |
|---|---|
| `scripts/check_guide_blocks.py` | collects each block's notices, names them, and fails the run; the docstring carries why |
| `PAINTING.md` | the clean-edge answer drops to `size=0.06`; a sentence saying a clean edge does not buy back a big brush; the broken-pass rule scoped, with the crossers named |
| `RECIPES.md` | the graded field runs off the top of the canvas, and a bullet says why; *A volume of lit air* gains `s.dry()` after the films and the measurement behind it |
| `PAINTER.md` | the card's `undo` row and *What you are bad at* name `cover(..., edge="hard")`, `2.32x` against `1.01x` |
| `README.md`, `llms.txt`, `src/easel/__init__.py` | vision stated as a requirement, with the reason |
| `PLAN-0.6.0.md` | two migration-map rows corrected; G7 and G9 record what was already done; the status line |
| `SUGGESTIONS.md` | findings 5 and 8 gain what landed; the vision documentation row is closed |
| `CHANGELOG.md` | `### The guide's own examples, run past the guide's own checks` under `[Unreleased]` |

---

# Step 9, part three: the recipes' failures, painted (G3)

**To understand this, start by reading the module docstring of
[`src/easel/demo.py`](src/easel/demo.py) -- it states the block format and the invariant
-- then `_parse` and `faults` in it, then the demo block under *A mark that crosses a
boundary* in [`RECIPES.md`](RECIPES.md), which is the shape of all twelve, then
`check_demos` in [`scripts/check_guide_blocks.py`](scripts/check_guide_blocks.py).**

Branch: `g3-demo`, off `main` at `89759b4`, after a first commit recording four rulings
and the plan's *Loose ends* table.

---

## What this step was for

Finding 19: *small runnable visual comparisons -- the recommended call, what it looks
like, the common failure, the smallest fix*. And the second half of the invariant part
two began: a recommended block runs notice-clean (landed), and **a failure block trips
exactly what it names** (this). Two loose ends the plan gave G3 came with it: the
manifest's verb count, and whether the block run joins CI.

## What landed

| | |
|---|---|
| `easel demo <recipe>` | one recipe painted as the recipe, what goes wrong and the smallest fix, side by side, with what the tool said about each panel quoted; `demo` over MCP, `easel.demo.answer()` from Python. No session needed |
| twelve demo blocks | under the *Goes wrong as* of twelve of the twenty recipes with code: eight notice codes, three `report()` lines, one *nothing says so* |
| the invariant | `easel.demo.faults`, run over every demo by `scripts/check_guide_blocks.py`: **12 of 12** fail exactly the way they say |
| CI | a `guide` job runs the whole block check, which until now ran only when somebody remembered to |
| the manifest | seventeen verbs, held to the parser by `tests/test_server_json.py` |

## Decisions and gotchas

**1. One block per demo, cut by comment lines.** Three blocks per recipe (recipe,
failure, fix) would have tripled `RECIPES.md`'s code and duplicated whatever the three
share. So a demo is one block -- `# the passage:`, `# goes wrong:`, `# the smallest
fix:` -- and the first panel is the recipe's own block rather than a copy of it. The
passage is laid under every panel, so it is the one place the demo's context lives. A
demo block is the failure on purpose, and a worked example is an instruction: the
file's preamble now says not to copy one, and the `# goes wrong:` line sits directly
above the call.

**2. `report()`'s rules have no codes, so a demo names them by their own words.** D3
decided the notice channel is for what is said at the call. So a *goes wrong* line says
`report() says "a stack of bars"`, matched as a substring of a finding line. **Copy the
words; do not paraphrase them**: the first draft of the narrow-loop demo said *come back
as bars* and the line says *comes back as bars*, and the check failed it, correctly.
*nothing says so* is a claim as well, held the same way, for a failure only looking
finds.

**3. The invariant is exact on the failure and deliberate about the rest.** The
failure trips exactly its codes and its `report()` lines -- a line it does not name is a
fault. The recipe and the fix must say nothing at the call and must not trip the
failure's lines. **What `report()` says about the recipe beyond that is a note, not a
fault**, because the answer can be the rule's to change rather than the recipe's (the
graded field below is finding 10's known noise). Notes print on every run, so they
cannot be forgotten the way a script nobody runs can.

**4. The first run found two recipes the notice check could never have seen.**

- ***A mass built of planes*, as step 6 left it, paints the failure its own paragraph
  names.** Step 6 moved its faces from a ragged `flat` (the staircase, finding 1) to a
  `bristle` at `0.014`-`0.02`; `report()` now says *59 marks with a bristle under
  size=0.025 ... four streaks with gaps* and *46 of 64 long marks ... a stack of bars*,
  and the render shows hatched faces -- *a woven surface (bristle streaks used instead
  of planes)*, word for word the recipe's own *Goes wrong as*. The staircase fix traded
  one named failure for another, and only the notice half of the invariant existed to
  catch it. **Not fixed here**: it is a recipe change that wants rendering and looking,
  and `chisel-staircase`'s two remedies pull against the small-comb rule at these sizes
  (a `bristle` under `0.025` trips it; `direction=` along one side leaves the others
  stepping). `edge="clean"` on a `flat` is the candidate -- it is what the demo's own fix
  uses -- and whether `clean-small` lets the smallest face through at `0.014` is not
  measured.
- ***A graded field that is most of the picture* trips the stack-of-bars rule on 17 of
  17 long marks.** Its two crossers run within six degrees of its passes, so to the rule
  they are more bars. Angling the crossers would not clear it: the fifteen passes alone
  are over the rule's 60%. This is finding 10 again, on the guide's own recipe.

**5. A recipe presupposes a passage, and without one the demo shows it failing.** On
bare `toned_grey`, *a passage light in the middle* draws a dark rim, because its first
ring is `"shadow"` and that is only right when the patch sits in the shadow -- which is
its own third *Goes wrong as*. Its demo lays the dark first. Every passage is chosen to
fit the recipe's own coordinates, so the recipe's panel shows the recipe working: the
crossing mark crosses the join, the lost edge's smudge runs along the slope.

**6. A whole canvas of 400 px cannot show a 5 px disc.** The first sheets were full
canvases, and the five-disc failure was five dots. Each panel now keeps the box its
body changed (a channel moving more than `0.004`, the probes' own threshold), and
`focus` cuts every panel to the union of those boxes, padded, grown to the canvas's
shape, enlarged at most four times, and not cut at all when the box is over half the
canvas.

**7. Probe before writing the line.** Four of the twelve changed after the first run:
the wide inward brush was guessed as *nothing says so* and the engine already says
`inward-flat`; four bands stepping dark to light also tripped the hand-laid graded-band
rule, because to that rule a stack of stepping colours *is* a graded passage (the
bands' colours no longer step monotonically, which is also what a real stack of bands
does); the planes demo's first face, at `0.014`, also tripped *detail before the masses*
(fourteen small marks in the first sixty) and moved to the whole silhouette, where the
staircase is big enough to see; and the crossing demo's fix -- the same smudge run along
the join -- painted a pill on the boundary, which teaches nothing, so the recipe is the
fix there.

**8. The context moved into the package.** The names every block assumes -- `s`, the
palette, `mass`, `patch` -- were the check script's `PREAMBLE`. `easel demo` has to lay
the same context, or a demo that passes the check paints a different picture in the
command, so it is `easel.demo.preamble()` now. The script keeps the name
`PREAMBLE`, because `scripts/probe_cohort_session.py` imports it from there; and its
`guide_blocks()` leaves demo blocks out, because the probe runs that list past the
checks it measures and would count every failure as the guide tripping its own rule.

**9. A panel keeps no frames.** The preamble takes `timelapse=`; the check keeps
`True`, because a guide block exports a time-lapse, and a panel passes `False`.

**10. Time.** The block check went from 75 s to about 2 min 20 s here. The demos with a
full-canvas passage are the dear ones (the smudge demos about 10 s each), because the
passage is laid once per panel. That is the price of a CI job, not of a test: the
pytest half paints only the fastest demo and a few one-stroke drafts.

## Open, and for the owner to rule on

**The planes recipe** (gotcha 4): fix it -- `flat` faces with `edge="clean"`, rendered
and looked at against the woven version -- or rule the small-comb rule wrong at these
sizes. Either way the demo already shows which.

**Ruled 2026-09-21, and done: the recipe's.** Five ways of laying the faces were
painted at 400x300 and 1024x768 and read back through `report()`: the comb weaves;
finding 1's ragged flat stairs; a clean edge with every face on one axis keeps the
stack-of-bars line; each face along a side of its own with a clean edge is silent once
there is a ground under it, and reads as planes; a hard edge is silent everywhere and
reads cut out. The recipe lays the fourth. The notice that sent step 6 to the comb
offers it only at `size=0.025` and over now -- `CALIBRATION.md`'s own repair table
measured its *always works* comb at `0.022`, under the floor, which is how the advice
and the other rule came to point at each other. On a bare canvas the recipe still
draws *detail before the masses* (its faces are then the painting's first marks), so
its demo lays a ground first.

**The graded field and the bars rule** (gotcha 4): the rule's to narrow, or the recipe's
to answer. `s.plan(bands="subject")` is the engine's current answer and does not fit: a
sky's bands are not the subject.

**Ruled 2026-09-21, and done: the rule's -- a `scumble` counts once.** Two findings made
it the rule's. In its own colours the recipe paints a smooth field (the strata in the
first demo were the stand-in palette's, whose `mid` is `light`), so the line was noise
on a picture that was right; and the recipe cannot answer it, because crossers at 13
degrees are not crossings (30 is) and the fifteen passes alone are over the share.
Replayed over the corpus, the condition holds on 47 passes rather than 62 and 10 of
the 46 lines painters saw go, every one on a pass laid mostly with a scumble; the
probe's noise table, decay and all, has the rule at 38 of 325 passes, 12%, against 47. The price
was paid knowingly: BigPickle's whole-painting line, the round's one true positive,
reached its share only by counting sky passes its painter called fine, and is silent
now. The crossings that re-arm the line count a scumble once as well. The graded
field's demo lays the field in its own colours, so its recipe panel shows the recipe.

**Eight recipes are still words only**: *a scene with straight edges*, *a picture with
an empty half*, *a form that turns*, *a quiet gradient* (which has no *Goes wrong as*
paragraph at all), *a small irregular bright mark*, *a tapered arc*, *a hollow thing*
and *a repair under things that are standing on it* -- the last to wait for F1, since
its failure is `cover()`'s overrun. Most of them are *nothing says so*: compositions and
silhouettes the check cannot see, which is the boundary `LESSONS.md` keeps.

## What part three did *not* touch

**G2's `easel demo mistakes`** -- the six mistakes on one sheet -- is not built; the
module can draw any set of demos, and which six is G2's question. **G6's recipe** will
need a demo whose failure is the loop's signature, and the narrow-loop block here
already trips it. `PAINTER.md` is untouched.

## File map

| File | What changed |
|---|---|
| `src/easel/demo.py` | **new** -- `preamble`, `Recipe`, `Demo`, `recipes`, `demos`, `Panel`, `lay`, `panels`, `faults`, `notes`, `focus`, `sheet`, `draw`, `find`, `listing`, `answer` |
| `src/easel/docs.py` | `headings(name, text=None)`: a draft can be scanned |
| `src/easel/cli.py`, `src/easel/mcp_server.py` | `easel demo` and the `demo` tool; the server's stale *twelve CLI verbs* comment |
| `src/easel/__init__.py` | `demo` bound and in `__all__` |
| `scripts/check_guide_blocks.py` | the preamble from `easel.demo`; demo blocks left out of `guide_blocks()`; `check_demos()`; the docstring |
| `RECIPES.md` | twelve demo blocks; the preamble's *do not copy*; the graded field's stale strata line; three *Goes wrong as* lines name the failure their block shows; after the rulings, the planes' faces flat and clean along their own sides, a ground under the planes' demo and the graded field's own colours under its demo |
| `tests/test_demo.py` | **new** -- parsing, the rule on drafts, the sheet's focus, the command |
| `tests/test_mcp.py`, `tests/test_server_json.py` | `demo` over the wire; the manifest's verb count |
| `.github/workflows/ci.yml` | the `guide` job |
| `mcpb/manifest.json` | seventeen verbs, and `demo` |
| `REFERENCE.md`, `README.md`, `llms.txt` | `easel demo` |
| `CHANGELOG.md` | `### Recipes that show how they go wrong, and a check that they still do` |
| `SUGGESTIONS.md` | finding 19's row; findings 1 and 10 gain the two rulings |
| `PLAN-0.6.0.md` | status; G3; the migration row; *Loose ends*; the two rulings |
| `src/easel/session.py` | the rulings: `_one_per_scumble` in the stack-of-bars rule and `_crossing_marks`; `chisel-staircase` offers a comb only at `0.025` and over; both docstrings, and `report()`'s |
| `tests/test_requests.py` | a scumble counts once, as a bar and as a crossing; the staircase's comb above the floor only, and silent on a clean edge |
| `CALIBRATION.md` | the comb in the staircase's repair table is under the small-comb floor; the stack-of-bars count re-measured |

---

# Step 9, part four: the loose ends G11 owned

**To understand this, start by reading `report_noise` and `_rules_said` in
[`scripts/probe_cohort_session.py`](scripts/probe_cohort_session.py), then *The noise
budget, as 0.6.0 stands* and *The `edges:` row, measured twice* in
[`CALIBRATION.md`](CALIBRATION.md), then the preamble of [`CHANGELOG.md`](CHANGELOG.md).**

Branch: `g11-loose-ends`, off `main` at `92297fd`, after finding 12's build (#69) landed.

---

## What this part was for

`PLAN-0.6.0.md`'s *Loose ends, and who owns them* held five rows no step carried, and
four were G11's to close before 0.6.0 could quote a number or make a promise. They were
finding 13's spread, measured with a prototype that did not work; the noise table's `!`
rows, which counted notices rather than passes; the replay promise, ruled amended on
2026-09-21; and `wet-under`'s decline, ruled the same day and written down nowhere. The
fifth, `PAINTINGS.md`'s rebuild claims, is not this round and wanted an issue. Two more,
left for a ruling in step 6's notes with no row to carry them, were ruled on 2026-09-22.

## What landed

| | |
|---|---|
| **the probe** | `edges_line` is the engine's `easel.checklist.edges_line`; `report_noise` counts each rule once a pass through `_rules_said`; the notice rows carry their codes, and two labels are corrected |
| **finding 13** | `21%-62%` of edges under `2.5` px, median `37%`, the cohort no different from the fourteen before it; Grok's `62%` and GPT's `54%` first and third. In `CALIBRATION.md`'s table and its own section, `CHANGELOG.md`'s step-7 entry, `HARD_EDGE_PX`'s comment, and `SUGGESTIONS.md`'s finding-13 row |
| **the noise budget** | *as 0.6.0 stands*: 197 of 325 passes quiet (61%), the median pass `0` lines, the busiest 8; bars 38 (12%), `glaze-far` the loudest new rule at 17. The 0.5.0 table keeps its numbers and says its `!` rows count sayings |
| **the replay promise** | `CHANGELOG.md`'s preamble, `PAINTINGS.md`, and the README twice: a saved painting opens as painted, and a rebuild from its log -- `replay(upto=)`, `timelapse_gif(from_log=True)`, every shell and MCP `undo` -- lays the same strokes with the engine installed, so a fix comes back fixed and is named under its version |
| **`undo`'s other two answers** | the shell's help said *strokes*, and the MCP tool *marks, at most 24 kept*; both say log records, the tool that it rebuilds from the log; a test each |
| **`wet-under`** | the decline in `CHANGELOG.md`'s D2 entry; `SUGGESTIONS.md`'s finding-5 row says the rings' cause and the decline |
| **two rulings** | `spill` told off by its own first remedy, and four of its fires under the line: both not this round, in `CALIBRATION.md`'s *Paint that lands outside the place* and the decisions table |
| **[#70](https://github.com/Gemberkoekje/EaselAPI/issues/70)** | `PAINTINGS.md`'s rebuild claims, filed with the replay's stroke counts on 0.6.0 |

## Decisions and gotchas

**1. The noise table was one replay away from a wrong figure in print.** A call-time
notice is said at every call that trips it, and the `!` column added one per saying:
`glaze-far` read 38 where it spoke on 17 passes. `_rules_said` takes each rule once a
pass, which is also what `easel run` prints, since `notices.collapse` folds a code said
at several calls into one line with a count. **The 0.5.0 table keeps its numbers**,
labelled as ceilings on their passes: the probe reads engine internals 0.5.0 does not
have, so it cannot be re-run there, and a table rewritten from a guess would be worse
than one that says what it counted.

**2. Two of the probe's labels had been wrong since step 2.** It files a line under a
rule by a phrase only that rule prints, and two phrases were read as the wrong rule.
*Scumble on this shape* opened both the wedge's and the dabs' warnings in 0.5.0, and
opens only the wedge's now. *Wide on a band* is the brush too **narrow** for its steps
(`scumble-bars`), not too wide. The counts were right; only the names moved. Every
notice row the table prints now carries its code. **Reading `EaselWarning.code` instead
of matching a phrase would end this for good**, and was not done: the probe's
candidates match phrases too, and that is a rewrite of the harness rather than of a
table.

**3. Finding 13 does not split the cohort, unlike 11 and 15.** The seven and the
fourteen before them spread the same way (`21%`-`62%` and `23%`-`59%`, medians `37%`
and `38%`). So the line tells pictures apart, not painters, and the two pictures whose
painters named flat cut-out shapes are first and third of 21, with the winter
greenhouse between them.

**4. On 0.6.0 the bare-ground rows move, and the table keeps 0.5.0's.** Replayed now, 14
of 21 finish under the floor (was 12), median `0.17%` (was `0.38%`), because F3 and F5
lay more paint where the older scripts left those arguments off. Findings 11 and 15 are
about what the painters saw, which is the 0.5.0 replay, so those rows stand and a
paragraph under the table says what 0.6.0 does to them.

**5. The MCP `undo` claimed a limit it does not have.** *At most 24 are kept* is
`MAX_SNAPSHOTS`, and it is true only inside one session. Every MCP call loads the file,
which carries no snapshots, so every `undo` there is a rebuild from the log, as far back
as asked. The loose end named two files for the replay promise. The README said it
twice more, and a claim fixed in two places of four is still wrong in two.

**6. The replay took 49 minutes** (`--corpus --quiet`), against about twenty for
`--closing` alone. Save its output before reading it: `CALIBRATION.md` quotes it, and a
second run to check one number costs the same again.

## Open, and for the owner to rule on

Nothing new. #70 is the owner's to schedule, outside the round.

## What part four did *not* touch

The rest of G11 waits for the steps it records. That is `LESSONS.md` (the restated
boundary, a multi-model cohort in the protocol, the depth-order item narrowed rather
than closed), `SUGGESTIONS.md`'s four documentation rows, which G2 and G8 answer, and the
README's and `llms.txt`'s counts. Also untouched: **G2** (the entry path and `easel demo
mistakes`), **G6** (the new recipe), **G8** (the voice pass), **G10** (the budgets) and the
eight recipes still without a demo.

## File map

| File | What changed |
|---|---|
| `scripts/probe_cohort_session.py` | `edges_line` delegates to `easel.checklist.edges_line`; `_rules_said`; `report_noise` counts once a pass; finding 13's line reads `HARD_EDGE_PX` and survives a painting with no edges; `_RULES` labels with codes, two corrected |
| `src/easel/checklist.py` | `HARD_EDGE_PX`'s comment states the corpus spread |
| `src/easel/cli.py`, `src/easel/mcp_server.py` | `undo`'s help and the tool's description |
| `tests/test_reference.py`, `tests/test_mcp.py` | the shell's `undo` says records; the tool says records and claims no snapshots |
| `CALIBRATION.md` | the 0.5.0 noise table's caveat and labels; *The noise budget, as 0.6.0 stands*; the edges row and the 0.6.0 paragraph under the table; *The `edges:` row, measured twice*; `spill`'s two limits, ruled |
| `CHANGELOG.md` | the preamble; `wet-under` declined under D2; the step-7 entry's spread; `undo`'s other two answers |
| `PAINTINGS.md`, `README.md` | the replay promise |
| `SUGGESTIONS.md` | finding 5's and finding 13's rows |
| `PLAN-0.6.0.md` | status; two decisions rows; *Loose ends* down to #70's pointer; section 6's pointer to #70; section 8's finding-13 bullet answered |
