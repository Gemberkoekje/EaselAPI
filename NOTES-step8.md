# Step 8 of `PLAN-0.8.0.md`: what landed nothing, said as it lands and after the pass

**To understand this, start by reading the plan's D with its *Step 2* and *Decided by the
painter* notes, and the painter's answer to D in
[`answers-step2.md`](paintings/Claude/bell_warden/answers-step2.md); then
`_check_dab_blank`, `_nothing_cause` and `Session._landed_nothing_line` in
`src/easel/session.py`, and `CALIBRATION.md`'s *Where a mark stops landing* -- and read
`NOTES-step2.md`'s D row first if you have not, because the cliff and the corpus's counts
are that bench's.**

Branch: `marks-that-landed-nothing`, off `main` at `e1dafa3` (step 7, #96).

---

## What this step was for

Both paintings of the round paid for marks that laid no paint and never heard about it.
The Bell-Warden's spark -- the one mark its reason needed from the eye -- was a round dab
of 2.9 px that moved two pixels; twelve passes of its shifted copies fell outside the body
they were held to; Wenna Brask's flour, which its why names, was eight strokes of a starved
bristle. `easel log` said *NO PAINT LANDED* for every one, and neither painter ran it while
painting. The painter decided D (2026-09-27): **name them after the pass**, hand marks by
the line that laid them and a mass call's by count, with the cause the engine can see --
and step 2 had already found the one cause that meets the four conditions for a fact at
the call, a round dab under a cliff in pixels.

## What landed

| | |
|---|---|
| **`dab-blank`** | a fact, said once the dab has landed (`_check_dab_blank`): a round dab laid by hand, at the default `taper`, that carried under one unit of paint and is under the size its tip lands from at its press (`_DAB_CLIFF_PX`). Names the dab's pixels, the cliff, and the fix -- three touches where they land at that size, and the `size` that is the cliff's pixels on this canvas. Registered in `notices.py`, a row in `REFERENCE.md`'s table, its passage `CALIBRATION.md`'s *Where a mark stops landing* |
| **`landed nothing:`** | the first of the check's standing lines, only when a mark of the pass carried under a unit (`Session._landed_nothing_line`): hand marks by line, a loop's run together, a mass call's by its passes, each with the cause its record shows (`_nothing_cause`) -- half its path outside its clip, a round dab under its cliff, an oriented tip under four pixels, a bristle loaded under `0.5`. In `report()` and `checklist()` alike; records in another process; never on a counted copy |
| **`dab()`'s touches** | a tenth, a fifth and about four fifths for a light on a dark passage; white on a mid ground a fifth, two fifths and nine tenths; and the cliff in pixels |
| **Said** | `REFERENCE.md` (the code's row, the standing line, a sentence under the budget: a mark that laid nothing is charged); `CALIBRATION.md` (*At the scale of a feature*'s touches measured again, *Where a mark stops landing*'s finer grid and what was built, *The marks that did not land*); `PAINTING.md`'s sentence on a mark gone missing; `DIAGNOSIS.md`'s *a small mark that did not register at all*, pointing at the cliff's passage too; `_check_tip_pixels`'s docstring, which said a round tip has no cliff; the README and `llms.txt`, thirty-two notices |
| **The bench** | `probe_bell_session.py --landed`: the cliff a quarter of a pixel apart and the touches; both paintings rebuilt as `easel run` says each pass; the guide's blocks; the corpus replayed with the engine as built, against what step 2's replay counted |
| **Tests** | `test_requests.py` *0.8.0 D* (6) |

## Measured as built

`probe_bell_session.py --landed`, on this branch's engine:

- **Both paintings, rebuilt as `easel run` says each pass**: the Bell-Warden's line on 3 of
  its 8 passes -- *landed nothing: 2 passes of the block_in at p04_gargoyle.py:40 (outside
  its clip)*; *6 passes of the block_in at p05_details.py:12 (outside its clip); 4 passes
  of the block_in at :14 (outside its clip)*; and *the dab at p06_finish.py:39 (a round tip
  under its cliff at press=1)*, the painter's own example word for word, the spark told at
  the call as well. Wenna Brask's on 5 of its 11, all eleven of its marks: the flour's eight
  as starved bristles with their loads, the nostril's dab *outside its clip*, and the
  catchlight and the flame's core under their cliffs, both told at the call. The passes
  step 2 counted, each of them.
- **The corpus, replayed**: the line names **the same 142 marks step 2's replay counted**,
  on the same 50 passes, each with the same count -- 14.7% of the 341 passes step 2
  counted painted, in 15 of the 24 paintings: 65 starved bristles, 56 round dabs under
  their cliff, 13 marks outside their clip (the Bell-Warden's twelve passes and the
  nostril), and 8 whose records show none of the four, named without a cause. A median
  81 characters, 128 at the ninetieth percentile, 334 at the longest: the first heron
  painting's last pass, seven starved strokes from its prelude's helpers.
- **`dab-blank` is said 56 times**, on 10 passes of 8 paintings (2.9%): every round dab
  under its cliff that laid nothing. The 57th round dab that laid nothing, a two-touch dab
  of 6.1 px centred outside the clip it was held to, is the line's, *outside its clip*.
- **The guide's 79 blocks**: `dab-blank` on none; the line on two, item 6's recipes.
- **The cliff's table in the engine is the measurement**, row for row.

## Decisions and gotchas

**1. The cliff, measured again, a quarter of a pixel apart.** Step 2's grid stepped by
`0.0005` of the long side -- half a pixel at 1024, and it started at 2 px. The finer one
puts every dab landing from **6.5 px at one touch and 5.5 at two** for a `round_hard`,
**7.5 and 5.75** for a `round_soft`, and **2.5 at three** for both: **the same pixels on
all four canvases, 400 to 1440 wide, and on all three surfaces**. `liner` lands a quarter
of a pixel sooner, so the tip's figure covers it. Step 2's `DAB_CLIFF` -- 6.5, 5.6 and
2.5 for every round tip -- was the same cliff read coarser, but for a `round_soft`'s one
touch, 7.5 and not 6.5.

**A wobble moves one figure, and it was the spark's.** A `round_hard` pressed three times
lands at every size with its tip left round, and every time only from 2.5 px at
`tip_wobble=0.7` -- the wobble the spark was laid at, so a fix quoted as *press=3 lands at
every size* would have been wrong for the one mark the fact was built for. Caught reading
the grid back before the corpus was replayed; each figure in `_DAB_CLIFF_PX` is the largest
over every canvas, surface and wobble measured.

**2. It holds for the default `taper` only.** `pressure="even"` or `"dab"` lands every time
from 2.5 px at one touch, `pressure=0.5` from 4.25 -- the taper's first stamp is its
lightest. So the fact speaks only at the taper; a dab given a pressure of its own that laid
nothing is named after the pass, with no cause.

**3. Measured on the mark, not predicted from its size.** Under the cliff some dabs land --
at 6.25 px, some of eight -- and *this dab laid no paint* said of one that did would be
false. The fact reads the record's own paint, as `glaze-far` reads the canvas after the
film.

**4. A standing line, not a finding.** A finding is a rule a painter can be right to break;
no painter lays a mark meaning it to land nothing, and the line is a count off the log, as
`subject:` is. It is printed first under the findings -- the painter's own form, *landed
nothing: ...*, is a standing line's. **And the demo check counts findings**: *A silhouette
lit from one side*'s own demo lays two passes of its far copy wholly outside the body, so
as a finding the line would have been a fault of a demo whose failure is the cut-out.
Those passes are real, and are item 6.

**5. The charge stays.** The plan left open whether a stroke that lands nothing is
charged; dropping it from the log would renumber every later record (rule 7), and keeping
it while it stops counting would make a stroke that laid nothing free -- which hides it,
where the painter asked for it to be named. It is charged, and `REFERENCE.md` says so.

**6. Two recipes lay a mark that lands nothing** -- F's, as rule 2 says of a rule that fires
on a recipe. *A mass built of planes*'s dry-brush stroke, a `bristle` 12 px wide at
`load=0.35` on the guide check's canvas (step 2 found it), and **step 7's *A silhouette lit
from one side***: three passes of its far copy fall outside the body it is held to (two in
its demo's panels). The line names both; neither is a notice, so the guide check stays
green.

**7. The causes are asked in order**, the first that fits: the clip, then the dab's cliff,
then the chisel, then the load. A pass half outside what held it is the clip's whatever
its brush; a dab under its cliff and outside its clip is the clip's. `_nothing_cause` reads
the record alone, so a painting checked in another process gets the same causes.

**8. `dab()`'s touches.** *About a quarter of the way* was *At the scale of a feature*'s
table, white at `size=0.06` on three grounds. Measured again at the median of the pixels a
dab moved: a light on a dark field reaches `0.09`, `0.19` and `0.78` from 12 px up, white
on `toned_grey` `0.23`, `0.40` and `0.89` -- the fraction turns on what the dab lands on,
not on its size. The docstring gives the accent's figures, and the mid ground's beside
them.

**9. H4, the plan's other row for this step**, was settled by step 2: the repainted-passage
count does not separate a failing passage from a subject being built, and the decline
stands. Nothing built.

**10. Where a warning points.** `_check_dab_blank` is reached from `dab()`, from
`stroke()` with one point, and from `paint(plan)`; `_to_painter()` walks out to the first
frame outside the engine, as `_painter_site` does, so the warning names the painter's line
whichever way the dab came.

**11. Count the corpus's passes by name.** A painting written as one script is cut into
passes by its numbered sections, and the corpus harness closes a section again each time
the script comes back into it -- nine of the corpus's sections closed more than once, the
misty forest's second among them, and a first count read *53 passes* for the line, *13* for
the fact and *41 marks against 8* for that section, where by name there are 50, 10 and the
same 142 marks. The bench counts by name, as step 2 did, and keeps the replay in
`out/bell/landed.pkl`.

**12. On this machine.** As before: `PYTHONPATH=src`, and a bash heredoc holding Python with
nested quotes dies with *unexpected EOF* -- the tests went in with the editor.

## What step 8 did *not* touch

What any mark lays: no golden, sampler or rebuild moves, and `notices.REBUILDS` gains no
row. The two recipes of item 6, and F3's other claims -- step 9. `dab()`'s default `press`
stays one: a light touch is what a one-touch dab is for, and the call now says when it laid
nothing.

## File map

| File | What changed |
|---|---|
| `src/easel/session.py` | `_check_dab_blank`, `_dab_cliff`, `_size_for_px`, `_to_painter`; `_DAB_CLIFF_PX`, `_STARVED_LOAD`; `Session._landed_nothing_line`, `_nothing_cause`, `_nothing_causes_said`; the line in `report()` and `checklist()`; `dab()`'s and `_check_tip_pixels`'s docstrings |
| `src/easel/notices.py` | `dab-blank` |
| `scripts/probe_bell_session.py` | `--landed`: `landing_grid`, `cliff_of`, `probe_cliffs`, `probe_touches`, `LandedWatcher`, `replay_landed`, `probe_landed_corpus`, `probe_landed_blocks`, `probe_landed`; a rebuild keeps each pass's notices |
| `tests/test_requests.py` | the tests above |
| `REFERENCE.md`, `CALIBRATION.md`, `PAINTING.md`, `DIAGNOSIS.md`, `README.md`, `llms.txt`, `CHANGELOG.md`, `SUGGESTIONS.md`, `PLAN-0.8.0.md` | as above |
| `NOTES-step8.md` | this file |

## Next

- **Step 9 (F)**: the two recipes that lay a mark that lands nothing (item 6); F7's units
  rows; line 407's boxes claim; the card's clause for the thumbnail; whether the lettering
  pass's two findings are the rule's to change; F1's move and budget, F2's tables, F3's
  claims, F5, F6 and F9.
