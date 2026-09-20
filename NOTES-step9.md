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
