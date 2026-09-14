# The tenth round: one home per rule

*To understand this, start by reading [`PAINTER.md`](PAINTER.md) — it is 6,300 words
now and its first section is the card — then the new entry at the top of
[`RECIPES.md`](RECIPES.md), *A scene with straight edges*, then the two new sections
in [`CALIBRATION.md`](CALIBRATION.md): the index at the top and *From the sessions*
at the end. [`LESSONS.md`](LESSONS.md) → *One home per rule* has the reasoning and the
hypothesis.*

The documentation was restructured after the tenth painting session, by the painter,
at the owner's request. No engine behaviour or default moved. The three source edits
are docstrings and help strings describing the files.

## What was wrong, measured

Six rules were each stated in full in four to six of the five files. `PAINTER.md` held
itself three times — a first-hour summary, a body, and a checklist restating the body.
Every rule carried its anecdote, and the anecdotes were most of the words. The
photograph material sat in the middle of the reasons file where a painter without a
photograph had to read around it. And the corpus had nothing on constructing a scene of
straight edges, which three painters had each built for themselves.

## What changed

| File | Before | After | What moved |
|---|---|---|---|
| `PAINTER.md` | 9,973 words | 6,441 | a card (*The first hour*, 894 words) and a body; the drawing is step 1 of seven; stories out; each step states its rule once with its number and links to the situation and the measurement |
| `RECIPES.md` | 5,000 | 5,605 | same entries, trimmed to the calls, the failure and the number; one new entry, *A scene with straight edges*; subject nouns removed from the composition entries |
| `PAINTING.md` | 11,500 | 6,923 | the engine's behaviour only; the photograph material is a skippable last chapter; the MCP section moved to `REFERENCE.md`; *Painting without a reference* and *Rehearse everything* went to the method, which was their home |
| `REFERENCE.md` | 3,300 | 3,724 | essay-length argument rows cut to facts; the MCP section added |
| `CALIBRATION.md` | 12,000 | 14,000 | an index mapping each rule to its measurement; *From the sessions* holding the painters' own reported counts, labelled as reports; no measurement touched |
| `DIAGNOSIS.md` | 128 lines | 129 | pointers follow the renumbered steps; one row for the new recipe |

Also: `scripts/check_guide_overlap.py` reports any twelve-word run of prose stated in
more than one of the four guide files (the calibration file on request, since its claim
lines restate the guide on purpose). It reports zero. `README.md`, `llms.txt`,
`CHANGELOG.md`, the CLI help and the MCP tool docstring describe the new shape.

## Decisions

- **The drawing is step 1, and the order is seven steps.** The owner asked whether
  "make a sketch first" should be explicit; it was a paragraph inside the block-in
  step. In the tenth session the two thrown-away drawings found the composition fault
  for free and the two passages never drawn came out weakest, so it earned a step.
  The diagnosis pointers were renumbered with it.
- **Stories moved, not deleted.** Every count a painter reported that the guide used
  to quote is in *From the sessions*, labelled as a report rather than a measurement,
  which is the calibration file's own rule applied the other way round.
- **No new file.** The build ships exactly the five documents `guide.DOCUMENTS` names
  and a test holds that equality, so the photograph material became a last chapter
  rather than a sixth file.
- **Headings the diagnosis index points at were kept verbatim** where the content
  stayed, so the pointer test needed only the renumbering and one repoint.
- **The reasons file stays above 5,000 words** because a test says a stub there
  would mean the front page's budget had become a deletion.

## Gotchas

- `guide.front_page()` cuts at the next `## ` heading, so the card may use `###`
  headings but not `##`, and it must contain the sentence *Look every 5 to 15
  strokes* verbatim.
- `scripts/check_guide_blocks.py` runs every Python block with a preamble that
  defines `dark`, `light`, `shadow`, `mid`, `pale`, `cool`, `surface`, `path`, three
  landmarks, `plan`, `mass`, `patch` and `bent`; a block that names anything else has
  to define it. Blocks containing `...` are skipped as pseudo-code.
- The reference test pins the brush table's column order and the backticked
  `field default` list; edit the prose around them, not them.
- The no-nouns discipline is manual. The grep in this round found `pear`, `tower`,
  `bird` and `lamp` still in the four guide files; the ones in prose I rewrote were
  replaced, the one in an exercise's palette name and the two in the reference file's
  examples were left.

## Filed afterwards

The painting's own findings went into `SUGGESTIONS.md` as *Open: the winter
greenhouse* — seven engine items, labelled measured, observed or reasoned, and the
documentation items as done. While this session ran, another session painted
`paintings/fogged_glass/`, moved `greenhouse_winter/` into `paintings/`, and filed its
own open round; three of its documentation items were closed by the rewrite and are
marked so on its rows, and its open `direction=` question was measured on a box: the
angle is in normalised units, which is now in the reference's units table.

## Verified

`python scripts/check_guide_blocks.py` — 77 blocks ok, 0 failed, 10 skipped.
`python -m pytest -q` — the suite passes. `python scripts/check_guide_overlap.py` —
0 passages.

## Deliberately not done

- Wiring the overlap script into the test suite. It is a script for now; whether it
  should block a commit is the owner's call, because the first round that adds a
  legitimate cross-reference will be the one that decides its window.
- Rewriting `CALIBRATION.md`'s prose. Its measurements are the evidence and were not
  re-measured here; only the index and the sessions section were added.
- Testing the hypothesis. The corpus's own protocol — a fresh session painting against
  the shorter guide and then being read — is the measurement, and this round is one
  data point in favour, not the test.
