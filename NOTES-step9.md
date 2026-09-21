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
Until then the invariant holds only for whoever runs the script.

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
