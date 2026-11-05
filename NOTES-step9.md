# Step 9 of `PLAN-0.9.0.md`: the one-page card, and the cut measured before it was made

**To understand this, start by reading the plan's section 4I and section 6's P8 and Q8,
then the painters' own words — [`answers.md`](paintings/Claude/uktarl_krannoc/answers.md)
H (*the one-page card must hold*, and its four cuts) and The Curator's
[`answers.md`](paintings/Claude/the_curator/answers.md), Question 8 — then `PAINTER.md`'s
*The first hour* as it is now, and `CALIBRATION.md`'s *The card and the reading path, as
built*.**

Branch: `step-9-card`, off `main` at `058dd34` (#111, step 8, merged).

---

## What landed

| | |
|---|---|
| **`PAINTER.md`** | *The first hour* rewritten as one page (I1, P8): the five-file table first, each file with the command that prints it (Q8); *decide what to paint* moved in from above the heading, which `easel guide` never printed; the loop as the painter said it, with *read every line the check prints after a pass; do not filter it*; the seven steps one line each; seventeen calls in one runnable block; the numbers that bite as a table; where to go next. The six mistakes' table moved to the head of *What you are bad at*, whose rows it summarises; *when you think it is finished* went, the checklist's section saying it. Card 1,370 words to 985; file 6,699 to 6,349 |
| **`src/easel/docs.py`** | `CARD_WORDS` 1,400 to 1,000 and `FRONT_PAGE_WORDS` 6,700 to 6,400, each with its paragraph of why |
| **`src/easel/session.py`** | `Session`, `stroke` and `block_in` say *Units and defaults: `easel guide --reference`.* under their first line (Q8, 2) |
| **`src/easel/cli.py`** | `easel --help`'s line for `guide` names `--reference`, `--recipes`, `--painting`, `--calibration`, `--full` (Q8, 3); `easel guide --help` describes the card |
| **`tests/test_guide.py`** | the card opens with the five files and `easel guide --reference`; it carries the sentence on the check; the three docstrings; the flags on `easel --help` |
| **`scripts/probe_uktarl_session.py`** | `--reading-printed`: the three files against what a pass prints, docstrings left out, by runs of six and five words, paragraph by paragraph, and the card's size |
| **`README.md`**, **`llms.txt`**, **`src/easel/mcp_server.py`** | the card's size, *about 1,000 words*, in the five places the test holds to `CARD_WORDS`; `llms.txt`'s sizes for `PAINTER.md` (~6,400) and `REFERENCE.md` (~12,300, which had drifted to 9% off) |
| **`CALIBRATION.md`**, **`SUGGESTIONS.md`**, **`PLAN-0.9.0.md`** | the round's *as built*; Uktarl's *Volume* row and The Curator's *Method, not reference* row answered; the status line and step 9's row |

## Decisions and gotchas

- **The handover painter's cut was measured before anything was cut, and it is not
  there.** Step 2's inventory read *What the tool will tell you* at 38% *said by the engine
  too* and *Looking, planning, measuring* at 18%; it counted every string constant,
  docstrings included, and the reference is written beside the docstrings. Leaving them
  out, what a pass can print repeats 1.0% of `PAINTER.md`'s runs of six words, 0.9% of
  `RECIPES.md`'s and 7.5% of `REFERENCE.md`'s — the last its notice table, which
  `tests/test_notices.py` requires. **So the plan's target, set from the inventory, is the
  card's cut**: the path is 350 words shorter, the first round it has shrunk, against the
  2,291 step 8 added. Shingles do not see paraphrase; a reader's judgement might find more.
  **A reading to confirm.**
- **The stories were not reopened.** `PAINTER.md`'s pier and four treatments of one failing
  passage were kept on 0.8.0's painter's word (`LESSONS.md`, *One home per rule*). A sentence
  count of history and painters in the three files (445, 2,080 and 926 words) is mostly
  *Goes wrong as* lines and version tags, not stories.
- **The table moved into the card rather than being printed above it.** `front_page()`
  could have started at the top of the file instead; but the card is the section with a
  budget and tests, and *decide what to paint* — the painter's first rule of method — was in
  the same unprinted stretch. Both are in the card now; above it, the file opens with
  one short paragraph saying the card is first.
- **The card's block was run before it went in, twice changed by what came back.** Laid as a
  wall across the top half, its passes ran within six degrees of the floor's and the
  repair's, and the closing check called the three *a stack of bars*; the mass is a figure
  on the floor now, along its own height. A smudge along the figure's outline was
  `smudge-long`; it is three points. The guide check passes: 83 blocks, none trips a notice,
  22 of 22 demos fail as they say.
- **The pool's steps are on the card** because P8 listed them, though they are one recipe's
  numbers; the row names the situation, and the recipe keeps the procedure.
- **`key="low"` is not in the card's block**: its plan's lightest place is the floor at
  0.62, which no low-key picture has. The key is in the numbers table, rule first, which is
  where `tests/test_named_light.py` reads it.
- **`test_every_signpost_states_the_cards_size_as_its_ceiling` wants the card between 90%
  and 100% of `CARD_WORDS`**, so lowering the card means lowering the ceiling in the same
  change; 985 of 1,000 leaves 15 words for the next round.

## Not done here

How `opacity`, `density` and `solid` combine is still in no file (The Curator's row). A
deeper cut of the reading path — `REFERENCE.md`'s *Looking, planning, measuring* at 3,135
words, `RECIPES.md` at 13,234 — is a design decision with no measurement behind it yet, and
is not made. The faint-mark pointer The Curator suggested (*a notice that a mark is under its
cliff could end with the same pointer*) waits for M2. None of step 8's new recipes has a
demo.

## Next

Step 10, the cut: 0.9.0's ten painter's lines atop its changelog entry (the test refuses
the cut without them), then the tag on the owner's word, then the claim. **G2 waits for the
painter's answer to `questions-step7/`.** **4N's `cut=` and 4K's `alpha=` wait for the
second painter's batch 2**, which is not written yet; M's deposit table and L's sentence
wait with them.
