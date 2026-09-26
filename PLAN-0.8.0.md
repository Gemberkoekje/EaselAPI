# Plan: act on the bell-warden's verdict on 0.7.0, and cut 0.8.0

_To understand this, start by reading: this file; then [`LESSONS.md`](LESSONS.md), whose
rules for how the engine and the guide may change bind every row below; then the
painter's own [`verdict.md`](paintings/Claude/bell_warden/verdict.md) and the painting's
[`NOTES.md`](paintings/Claude/bell_warden/NOTES.md), filed in step 1; then the
places in the engine most of this lands -- `_draw_guides` in `src/easel/look.py` (the ink a
guide is drawn in), `Session.guide` and `Session.pencil` in `src/easel/session.py`,
`Session._one_call` there and `_cmd_run` in `src/easel/cli.py` (what a pass says it cost),
`Planned.mean_value` in `src/easel/plan.py` and `values_line` in `src/easel/checklist.py`
(what the plan's lines read), and the wet blend in `Canvas.stamp` beside
`_check_glaze_far` in `session.py`. Then the newest `NOTES-step<N>.md`.
[`PLAN-0.7.0.md`](https://github.com/Gemberkoekje/EaselAPI/blob/v0.7.0/PLAN-0.7.0.md), as
tagged, is the round before this one and the shape most of the conventions here come
from._

**Status: step 2 (measure) is built on branch `measure-bell-round`, 2026-09-26, off `main`
at `a180395`** -- step 1 merged as [#88](https://github.com/Gemberkoekje/EaselAPI/pull/88) and
[#89](https://github.com/Gemberkoekje/EaselAPI/pull/89). Nothing under `src/` has changed.
[`scripts/probe_bell_session.py`](scripts/probe_bell_session.py) rebuilds both paintings to
the pixel and benches every candidate of section 4 on them and on the corpus; its numbers are
in [`CALIBRATION.md`](CALIBRATION.md), *The bell-warden's round*, and what it decided is
marked *Step 2* under each workstream and gathered in [`NOTES-step2.md`](NOTES-step2.md). In
short: A1's cased line and A2 as written; A3 as written, its default size and signature the
painter's (question 4); A4's recipe with `union(...).smooth()` and no `ribbon(width=[...])`;
B as written, the join measured as the turn; C as decided; **D narrowed** -- a round dab that
lands nothing, told its size, meets all four conditions, and the general *lands short* meets
none of the last three; E1 with its clusters unjudged, E2's median, E4's 95th percentile; the
floor's black not proposed, on the painter's own darks; H2 narrowed to rebinds that change a
name the prelude assigned; **H4's decline stands**; I2's rings at every count. Questions 4, 9
and 10, and a follow-up to 5, went to the first painter as a blind package,
[`questions-step2/`](paintings/Claude/bell_warden/questions-step2/README.md).

*Step 1 (record) was built on branch `record-bell-warden`, 2026-09-26, off `main`
at `2ee54d3` -- 0.7.0's claim ([#87](https://github.com/Gemberkoekje/EaselAPI/pull/87))
merged.* O1 is answered from the painting session's metadata, and the owner answered O2 and
O3 (section 6): the painting is filed with the pack's details left out, the report is
`verdict.md` and nothing is posted, and the painter's questions go through the owner. The
painting session's transcript turned out to be evidence this plan had not counted on: it
answers questions 1 and 3 by measurement and all of 2 but a follow-up, holds every version
the painter threw away -- each recovered and re-run to the report it printed -- and
corrects rows 8 and 9 and adds to row 12 (marked where they stand). Question 2's
follow-up and questions 5 to 8 went to the painter as
[`questions-step1.md`](paintings/Claude/bell_warden/questions-step1.md), and **its answers
came back the same day** ([`answers.md`](paintings/Claude/bell_warden/answers.md), filed and
re-measured): they decide C, E1, E2 and F1, withdraw D's `into-wet` as written -- D is
rewritten -- and find two more things, the ember that did not land and twelve paid
strokes that laid nothing. 4, 9 and 10 wait for step 2's sheets. **And a second painting
arrived the same morning** -- *Wenna Brask*, by a second session that began from the first
painter's notes -- with its own verdict; the owner filed it the same way and folded its
verdict into this round (section 3b, and every row marked *added 2026-09-26*), in a PR on
top of step 1's -- and **its answers came back the same day too**
([`answers.md`](paintings/Claude/wenna_brask/answers.md), re-measured): they decide A5, H1,
I1 and E4's form, withdraw three of its sentences, and find the flour its why names never
landed. See [`NOTES-step1.md`](NOTES-step1.md). Nothing under `src/` has
changed. Every number in section 3 was measured on this machine on the 0.7.0 engine, from
the painter's own session file (`bell.easel`, 292 records, 27 pass reports), its prelude
and its seven pass scripts; three of the painter's claims changed shape under that
checking and are marked where they stand. Row 13 and E3 answer the owner's follow-up,
whether it is time for a black.

---

## 1. What this round is

**One painter, painting against 0.7.0 from the package, on a brief it was handed.** A
Claude session -- `claude-opus-5-5` at max effort, by its own metadata (O1) -- installed
`easel-paint` 0.7.0, did the nine exercises, read about 20,000 words of the guide by its
own count (about 21,000 of the documents, measured), and painted *the Bell-Warden* -- a
stone gargoyle crouched on a plinth in a dark undercroft, lit warm from the upper left,
which *has to pass for a statue* -- as sample art for a content pack in another of the
owner's projects: **280 of 300 marks in seven passes, after nineteen rehearsals**,
eighteen of which the file records (the nineteenth raised). The subject was set by that
pack rather than chosen, which is the lighthouse-greenhouse brief's case in
`PAINTINGS.md`: the rule satisfied because nobody picked it after reading. Then it wrote a
verdict on the tool, the documentation and its picture, ranked eight suggestions most
useful first, and asked whether to write it all up in the painting's folder or as issues
here.

**Its headline is a step the engine does not help with yet**: *drawing a complex shape as
coordinates*. Its creature is one 42-point polygon typed by hand and its wing another of
16, and its three failures on the way were drawing failures that paint showed up -- a
silhouette whose two symmetric peaks read as ears, lit planes laid as islands that read as
a piebald, and a lit band wrapped round the body that read as an arch. A rehearsal caught
each, and each was fixed at the drawing, as the card's *if a passage has failed twice, the
fault is upstream of the brush* told it to; the painter credits that rule with saving the
picture.

**It is the next run 0.7.0 asked for** (`SUGGESTIONS.md`, *What the round left open*), and
it answers two of the three things that section said to look for first:

- **The broken edge.** 0.7.0 breaks every held edge against the tooth by default, a choice
  made blind from sheets. This painter held every zone of its creature to a polygon and
  names the result *a vinyl toy ... the engine looks least painted exactly where I held
  everything to a polygon*; it never found `feather=` as a softening tool -- though it
  had read what one does (row 9) -- and supposed it might have softened its boundaries
  between light and shadow. Benched on its own pass, it would not have
  (row 9): a feather breaks an edge, it does not soften one. The `edges:` line read 51% to
  61% of edges under 2.5 px on the subject's passes and changed nothing, which is
  `LESSONS.md`'s *nor is a measurement* arriving a second time. The round's other engine
  answer, the dry brush that drags, it names among what looks painted without being asked:
  *the dry brush on the plinth*.
- **The way in.** Told by the card where to start, it read about 20,000 words before the
  first stroke -- fewer than the lighthouse handover's 194 KB, far more than the card and
  its exercises -- and calls the corpus long, and **it is the first painter to say which
  of the text it would move** (commentary on the documents themselves, and anecdotes) **and
  which of it worked** (*What you are bad at*, the upstream rule, the recipes' *Goes wrong
  as* blocks, the units table and the table of where a stack of passes starts).
- ~~Whether it reached for `--alternatives` unasked is not in the file: a rehearsal of
  versions saves as `rehearsed` like any other. Question 1.~~ *Answered from the
  painting session's transcript: it did not. It never ran `--alternatives`, `--count`,
  `cost()`, `cost_line()`, `explain` or `diagnose`, and rehearsed one version at a time.*

**What it says the method did.** Its checklist's `boxes:` line reads **0 of 17**, and it
credits the card -- *I painted no boxes, because it warned me* -- where the card still says
*every painter so far has painted boxes*. It spent **280 of its 300 marks**, where the
lighthouse handover stopped at 57% and five of the cohort's six budgeted painters stopped
under half, and gave its subject 61% of them against the 45% it planned. The plan object,
the notices and rehearsal worked as designed: `plan-pairs` named a pair on the empty
canvas, `inward-comb` gave it the ring count, `glaze-far` sent it to `to_value=`, and it
rehearsed about twenty times to commit seven passes.

**Scope.** Fix what the verdict measured, where the measurement stands; say so where it
did not; and record the rest. Four items are the engine's help for drawing (guides that
read on any ground, a shape handed to `guide()` and `pencil()`, a flat thumbnail of the
masses, and a helper for the edge where a form turns), two are the check's (what a pass's
calls cost, one by one; a light laid into wet paint, on evidence), three are about values
(a declared key; what a place reads; the palette's floor, said as it is -- and a black,
kept as a question with a measurement), and four are the documentation's (two recipes and an
exercise, `PAINTER.md` made lighter by moving what is not method, a paragraph turned into
tables, and the claims that stopped being true). The release is **0.8.0**: new verbs and
declarations, and one instrument changes what it prints. **Nothing in it changes what a
rebuild lays**, so `notices.REBUILDS` gains no row and no saved painting moves.

---

## 2. The rules this plan works under

From `LESSONS.md` and the last two rounds, restated because every row below is held to
them.

1. **Measure the condition before writing the rule** -- and re-measure a painter's number
   from the painter's own file before anything is built on it. Three of this verdict's
   claims changed shape when that was done (section 3, rows 4, 9 and 13).
2. **Ask what a rule says to a painter doing the right thing.** Every guide block runs
   notice-clean in CI and every demo fails exactly as it says, and both stay true through
   this round -- which is a real constraint on workstream D, since exercise 4 lays a light
   into wet paint on purpose.
3. **A default is worth more than a warning, and a procedure more than a louder line** --
   *warning is not method*. Only one of the painter's eight suggestions is a warning, and
   it is the one this plan builds last, and only on evidence (4D).
4. **A declaration, not a switch.** What the painter knows and the engine cannot, the
   painter declares up front and is then held to -- `bands=` and `ground=`, and here
   `key=` -- and the line a declaration replaces says something measurable instead of
   falling silent.
5. **One home per rule, and a finding never adds a paragraph to `PAINTER.md`.** Every line
   this round adds to the card is paid for in the same commit by text moved out of it, and
   the budget in `tests/test_guide.py` enforces it.
6. **A worked example is an instruction, and the guide names no subject.** Two new recipes
   are written under that discipline, and this painting's nouns join the grep list the
   day it is filed.
7. **Nothing new may touch the log index or the random stream.** A thumbnail, a tally of
   calls, a key and a reading all live beside the log.
8. **The check reads marks and measures the canvas; it does not judge an arrangement.** The
   painting's anatomy and the size of its give-aways stay outside the line (4G).
9. **Each landed step leaves a `NOTES-step<N>.md`**, and the next step starts by reading
   the newest.
10. **The decisions are the painter's** -- the owner's ruling since 0.7.0, because the tool
    is for painters -- **except where the bench or the corpus can decide**, and those go
    to the bench first.

---

## 3. The verdict, checked

*Kind* is the project's own distinction -- **M** measured by the painter, **O** observed,
**R** reasoned -- assigned here. Every *what checking found* was measured on 2026-09-25 on
the 0.7.0 engine, from `bell.easel` and the painter's scripts, with scratch probes that
step 2 turns into `scripts/probe_bell_session.py`.

| # | What the painter said | Kind | What checking found | Goes to |
|---|---|---|---|---|
| 1 | **Guide lines vanish on a dark canvas**; it judged its drawings on a separate throwaway canvas with a light ground | O | **Confirmed, and measured.** A guide is drawn one pixel wide in a fixed graphite, `(58, 58, 64)` -- value `0.23` -- at 75% alpha, and its note in the same ink. Over the painter's 17 guides: on the bare ground the line steps the value by a median `0.147`, and no pixel of it by under `0.05`; over the finished canvas by a median ~~`0.045`~~ *`0.042`*, and **~~69%~~ *65%* of its pixels by under `0.05`** -- gone. *Re-measured by step 2's probe, and over the room -- where the second drawing went -- a median `0.026`, 96% under `0.05`.* Its drawing look after the plinth shows it; its three drawing checks are the throwaway canvas. | **4A1** |
| 2 | **`pencil()` smooths its path by default**: in its drawing check a box came out as a rounded pot; shapes built from polygons should keep their corners | O | **Confirmed.** `smooth=True`, the default, fits a Catmull-Rom spline through the points (`stroke.catmull_rom`), which passes through every corner and bows every side of a closed outline outward: the painter's first drawing check is the plinth as a pot, its second the same with `smooth=False`. **A shape cannot be handed over at all**: `pencil(shape)` and `guide(shape)` raise `TypeError` for a `Polygon` or a `Region`, so the painter passed `shape.closed` -- and `RECIPES.md`'s own straight-edge recipe writes `s.pencil(shape.closed, ..., smooth=False)`. | **4A2** |
| 3 | **Cost is hard to predict**: the subject pass rehearsed at 85 to 113 strokes, and the report didn't say which call ate them -- *partly my fault, since I didn't use `cost()` before each mass* | M, O | **Confirmed.** The file's saved reports read the subject pass at 85, 98, 113, 101 and 101 marks over five rehearsals, and `easel run --rehearse` heads each with one total. **The log already knows the answer**: grouped by the call that laid them -- every record of one mass call carries that call's `via` and the stream state it began at -- the committed pass is 102 marks in 12 calls, **four `block_in`s laying 23, 22, 20 and 14: the shade copy, the mid copy, the whole body and the wing, 79 of the 102**. The details pass is 68 marks in 26 calls, two `block_in`s laying 24 and 17. `cost()` takes a plan, and a pass written as functions is not one. | **4C** |
| 4 | **Nothing warned about highlights mixing into wet paint**: *they landed at 0.52 instead of 0.64 until I added `dry()`*; the engine knows how wet the canvas is under a mark, so this could be a warning like `glaze-far` | M | **The mechanism is real; the number did not reproduce, and `0.52` is something else.** A brush dragged through wet paint takes `0.15 x wetness` of what it meets at every dab and refreshes a quarter toward its own colour, and lands at `1 - 0.55 x wetness` of its alpha (`stroke.py`, `Canvas.stamp`): a light mark drawn through wet dark paint carries about a third of the dark in its own paint, and 0.6.0 measured a mark laid across wet films dragging what it met by up to `0.40` in value. But **the committed details pass lands the same with and without its two `dry()` calls** -- the head's top plane at a median `0.607` against `0.606`, the two ridge lights at `0.53` and `0.62` either way -- because the paint under them had already dried by stroke count: wetness `0.001` under the head's top when it was laid, so the `dry()` before it had nothing to dry. And **`0.52` is exactly what the plan's line reads for that plane with the eye inside it** (row 5b): the saved reports read it at `0.51` to `0.52` in every version of the details pass, dried or not. Two rehearsals of the subject pass read it at `0.56` and `0.54`, which suggests those versions laid a light on the head in the same pass as the body under it -- the one place in the painting a light could have met wet paint -- ~~and their scripts are gone~~. **Changed shape**; ~~asked of the painter (question 2)~~. *Settled from the painter's own session when the painting was filed: the details pass's second rehearsal read the plane at `0.52`, the painter added the two `dry()` calls, and the third read `0.52` again -- at which point its own reasoning put the reading down to the eye. Both are recovered in `versions/`, as are the two subject-pass versions that read `0.56` and `0.54`, each re-run to the report it printed.* | **4D** |
| 5a | **"No clear light" can't be switched off for a dark picture**: a buried ground can be declared in the plan, a low-key picture can't | O | **Confirmed**: the `values:` line said *no clear light -- nothing above* `0.30` to `0.38` on **25 of the file's 27 saved reports** -- every one after the first mark -- of a picture its own notes call low-key *by design, not a fault*. It is the stack-of-bars line's history again: right, unanswerable, and printed until it is skimmed. `plan()` has `bands=` and `ground=` for exactly that, and nothing for a key. | **4E1** |
| 5b | **The "lightest" check averages the whole place**, so the dark eye inside the head's top pulled it down | M, R | **Confirmed.** The head's top plane, planned at `0.66`, reads **`0.524` by mean**, `0.606` by median, `0.622` at the 75th percentile and `0.626` at the 90th; **14% of its 1,592 pixels are under `0.35`**, the eye's socket first among them. `lightest:` still named it, at `0.52`; `plan:` called it a miss -- *6 of 7 places inside 0.10; head top -0.14* -- where by median it is `-0.05` and all seven are inside. **The one other painting with a plan keeps every verdict**: the lighthouse handover, rebuilt, names the same lightest place after each of its twelve painted passes under the mean, the median and the 75th and 90th percentiles, and its closing `plan:` line is 7 of 7 by mean and by median. `compare(s.plan())` reads a place the same way (`measure.compare_plan`, a mean). | **4E2** |
| 6 | **It's long**: about 20,000 words read before the first stroke; a good share is commentary on the docs themselves and painter anecdotes; *a few anecdotes persuade, dozens cost context* | M | ~~**The count is plausible and not yet placed**: `PAINTER.md` is 6,655 words, so the painter read two or three other files as well (question 1).~~ *Placed from its session: about 22,300 words printed before the first mark, 21,262 of them the documents' -- the README's first 400 lines of 417, `PAINTER.md` to line 700 of 754, `REFERENCE.md` to line 520 of 723, and twelve of `RECIPES.md`'s twenty-one entries; `PAINTING.md`, `CALIBRATION.md` and `DIAGNOSIS.md` unopened.* The two sentences it quotes are `PAINTER.md`'s own -- *every rule in these five files is stated once* and *this file has stopped calling them a gate* -- and the card and the body carry at least five anecdotes (*one painter chose the underside of a pier*, *one painting lost eighty strokes to four near-parallel fingers*, *one painter redrew an arrangement three times*, *one painter finished a whole picture without opening any of the other four*, *one painting spent about eighty strokes on four treatments*) and four *every painter so far*. The file is **45 words under its 6,700-word budget**, so nothing this round adds to it can go in without something coming out. | **4F1** |
| 7 | **Some passages are hard to parse**: the post-pass check's paragraph lists ten rules with their thresholds in one block; a table would read far faster | O | **Confirmed**: `REFERENCE.md`, *Looking, planning, measuring* -- **one paragraph of 678 words** naming ten rules, five standing lines and a dozen thresholds. The same page already has tables where they work: *What the plan changes*, and the notices. | **4F2** |
| 8 | **The hardest part of the session has the least guidance**: getting a creature's silhouette to read; neither the recipes nor the exercises cover it; a recipe for any complex organic silhouette would be subject-neutral | O | **Confirmed.** No recipe builds a silhouette and no exercise judges one. The pieces exist and are nearly undocumented: `union()` -- *one silhouette round overlapping shapes* -- is named by `REFERENCE.md`'s list of shapes and by no other guide file, and `PAINTING.md`'s *Masses that are not rectangles* offers five ways to make a mass without it. ~~So the painter typed its silhouettes as coordinates.~~ *Corrected from its session: the painter found it. Its first drawing's creature was a `union()` of eight ellipses and ribbons, which read as a spiky blob beside a plinth nearly as wide, and after that one look it typed polygons instead -- 32 points, the cat; then 42. A union of parts was its first reach, and failed as a drawing.* | **4A3, 4A4** |
| 9 | **It never found `feather=` as a softening tool**, which *might have softened my hard boundaries between light and shadow*; the *form that turns* recipe only mentions join strokes | R | **It would not have -- and the join would have.** The painter's subject pass, re-laid on the canvas it opened on, with its two shifted copies (a) as painted, (b) at `feather=0.012`, (c) at `feather=0.03`, (d) with their own edge left ragged inside `clip=body`, (e) as painted plus a half-value join stroke along each terminator, and (f) as painted plus a smudge along each. Looked at: **(b) and (c) read as a speckled band** along every held edge -- a feather breaks an edge against the tooth, it does not soften it -- **and they break the silhouette as well**, because one `feather=` applies to every hold of a call; (d) shows a flat brush's pass ends as a staircase down the terminator; **(e) turns the form, for two strokes** (102 to 104), and the tool says nothing; (f) softens it and is told `smudge-across` and `smudge-long`. The recipe the painter read had the right answer, for a column; what was missing was that answer for any silhouette. **Changed shape.** *And it had read what a feather does: `REFERENCE.md`'s paragraph on holds and its arguments table were both in what it printed before the first mark.* | **4B** |
| 10 | **The painting is a vinyl toy, not weathered stone**: flat grey fills with a hard, even rim of light; *I held every zone with a hard edge* | O | The bench's (a) against (e) is the difference: the terminators are steps, and the fills are flat because nothing broke them -- its own notes say *the dry brush and three carving seams only begin on it*. Both are what 4B's recipe is for. | **4B** |
| 11 | **The anatomy is stiff**: the head reads as a goat's more than a gargoyle's, the legs are sticks, the profile rigid -- *more cute than eerie* | O | A verdict on the drawing, outside the check's line. The instruments are the drawing's: 4A's thumbnail and its silhouette recipe and exercise. | **4A, 4G** |
| 12 | **The give-aways are too small for a projector**: the eye glint and the claws are a few pixels across; *the reason the picture exists is in it, but only on close inspection* | O | Measured: the ember is a `0.0068` dab and the spark `0.0028` -- seven pixels and three at 1024 -- and the claws are 8 to 10 pixels wide. The closing checklist asked *is that reason still in the picture?*, and this row is the painter's answer: the question worked, and it carries no size. *Found when it was filed: the spark did not land. It changed two pixels, by at most 21 levels; `easel log` lists it as NO PAINT LANDED, and nothing at the call said so -- `chisel-blank` is for an oriented tip, and a round tip is said to have no such cliff. Step 2 measures where a round dab stops landing.* *And the painter's answers found that the ember did not land either: `1.62` units over five pixels, reading a dull `0.22` against its own `0.62`. The glint is the glaze laid over both (re-measured; D, as rewritten).* | **4F3, 4G, 4D** |
| 13 | **The box bottoms out near 0.14**: *0.13 is below what this mix can reach ... setting the cast shadow to 0.14 from the darkest mix* -- and the owner's question on it, whether it is time for a black | M | **Changed shape: 0.13 was in the box, and the documents said otherwise.** Burnt umber alone reads **`0.128`**, the box's real floor, and `shade()` reaches it; what stopped the painter is `at_value`'s default dark, the blue-umber mix at `0.137`, whose error named nothing else -- mixing that mix *toward itself*, *only gets to 0.137* -- and never the umber or the one route below the box, a supplied colour, which lands as written (`#0d0c10` reads `0.049`, and mixed with umber lays `0.07` to `0.11`). The documents state the floor three ways: `CALIBRATION.md`'s table puts umber at `0.13` and two paragraphs later calls the `0.14` mix *darker than any single pigment*; `PAINTER.md` calls that mix *the bottom of the range at 0.14*; `PAINTING.md` *the palette's floor of 0.14*. **On a black: the corpus has never asked for one** -- parsed, no `at_value` target, planned value or supplied colour under `0.14` in any of the 22 committed paintings' scripts -- **but four low-key pictures sit on the floor**: the GLM terminal window's darkest twentieth at `0.140` with 17% of its canvas under `0.15`, and the darkest 1% of Gemini's forest, BigPickle's sunset and the night pool at `0.137` to `0.143`. | **4E3** |
| -- | **The headline**: *the engine is more capable than my painting shows; its weakest point is the one step it can't help much with yet, drawing a complex shape as coordinates* | R | Rows 1, 2 and 8 are that step's missing pieces -- a drawing that cannot be seen over paint, a pencil that rounds what was drawn, and no way to judge a silhouette flat and small nor recipe for building one -- and 4A is the answer to all three. | **4A** |

**Found while checking, not by the painter.** The log carries two `erase all` records, at
index 0 and at 96: the drawing pass was run again after the plinth's. A record takes an
index, and a stroke's texture is seeded from its index, so **the pass scripts rebuild the
painting only in the order the saved reports record** -- the drawing, the room, the plinth,
the drawing again, then the rest -- and not in their numbered order, which moves every mark
from the subject's pass on. The painter's *the log replays to the stroke* is right; the
filing says the rest, as `PAINTINGS.md`'s own note on drawing passes run twice predicts.

**What the painter defended, unprompted, and this plan does not touch:** rehearsal (*all
four failed versions of the creature cost nothing*); warnings that come with a measurement
and a fix -- `plan-pairs` on the empty canvas, `inward-comb`'s ring count, `glaze-far`
pointing at `to_value=`; `at_value()`, which hit every target of the value-scale exercise
to two decimals; the paint, wherever it is let be paint -- the wall's strokes, the dry brush
on the plinth, the beam of lit air; shapes and holds composing, since `shifted()`, `clip=`
and `edge="hard"` made its final lighting; and in the documentation, `PAINTER.md` as a
method rather than an API tour, *What you are bad at*, the upstream rule, the recipes with
their failures shown first, and the units table and the table of where a stack of passes
starts.

### 3b. The second verdict, checked

*Added 2026-09-26.* **A second painter, the next morning.** Asked by the owner to choose
the pack's pictures, a second `claude-opus-5-5` session at max effort wrote a list of them,
painted the first -- *Wenna Brask*, a woman by a lantern at dusk, 768×1024, **262 of 300
marks in eleven passes after 25 rehearsals** -- and gave its verdict when asked; the owner
chose to file it with the pack's details left out (`paintings/Claude/wenna_brask/`) and to
fold its verdict into this round. **It is not independent of the first.** It began from the
first painter's memory note -- which carried the Bell-Warden's lighting and the wet-paint
lesson that painter has since withdrawn -- and read the Bell-Warden's notes and six of its
passes before painting. So where it repeats the first verdict (rows W1, W2, W4, W11) it is
one painter's lesson and a second painter's experience of it; where it contradicts the
first (W13) it is the only kind of evidence a lesson carried over can give. Checked as the
first was, from its own session file and its transcript, which holds every version: all 31
of the file's saved reports come back word for word.

| # | What the painter said | Kind | What checking found | Goes to |
|---|---|---|---|---|
| W1 | **Drawing precise shapes in `0..1` coordinates on a canvas that is not square** -- *the most useful code I wrote was my own: a pixel helper `P()` and a `T()` that scaled the first drawing up by 1.3*; asks for a drawing unit and a way to move or scale a group of shapes | O | Confirmed. Its prelude draws in pixels through `P()` and scales the first head `1.3` times about a point with `T()`. The units table states the trap and `aspect=` answers it for one shape; nothing moves or scales several shapes about one point. The first verdict's headline, again. | **4A5** |
| W2 | **Cost only as a total**: the figure pass at 135, then 101, then 99 | O | Confirmed; the first verdict's row 3 on a second painting. | **4C** |
| W3 | **A finding that cannot be traced to its marks**: *4 small marks … around (0.55, 0.37)* | O | Confirmed: the closing checklist names a place and a count, no index, note or line; the pass's own report named no place at all. | **4H1** |
| W4 | **A low-key picture with a small light is misread**: *no clear light, nothing above 0.42*; *lantern reads 0.49 averages in the iron straps* | M | Confirmed, and **the median does not rescue it**: the lantern reads `0.491` by its mean, `0.506` by its median, `0.58` at its 90th percentile and `0.71` at its brightest, against `0.76` -- its iron is most of its place, the median's own failure the first painter named. The picture's top twentieth is `0.42`, with `1.4%` of the canvas above `0.60`.  *Its answers: the face is the lightest mass by every reading (median `0.584`, `0.620` at the 95th), which its plan never named, and the lantern's `0.76` was a mixture's value -- its panes' middle third reads `0.58`.* | **4E1, 4E2, 4E4** |
| W5 | **No lettering**: the pack's next pictures need text | O | Confirmed: no verb lays a letter; a stroke along a hand-typed path is the only way. | **4I1** |
| W6 | **`easel timelapse --scale` takes only whole numbers** | M | Confirmed, and it is the name: `--scale` is *the long side in pixels*, an integer, on `timelapse` and `look` alike, and reads as a factor. | **4H3** |
| W7 | **A pass can silently overwrite a prelude's name**: its `H` replaced the canvas height, and `P()` divided by a dict | M | Confirmed: two rehearsals raised on it, and nothing is said when a pass rebinds a name the prelude bound. | **4H2** |
| W8 | **Turn *failed twice, go back to the drawing* into a notice** -- ~~*I broke that rule on the fist with the rule in front of me*~~ *withdrawn by the painter in its answers: it went back upstream at the second failure each time, and its first redraw kept the view* | R | Its fist was laid over by five passes before a different drawing worked. **0.7.0's round considered a repainted-passage count and dropped it**: the log cannot tell a passage failing from a subject being built. A second painter asking, with a case -- and its answers measure one: four passes laid paint on the fist and four on the face, so passes cannot tell them apart, while masses laid over the painter's own earlier marks can (two on the fist, none elsewhere), and would have spoken exactly when the rule did. | **4H4**; section 5, row 6 |
| W9 | **A glow verb for lamps and windows** | O | The lamp's light on the wall took seven rehearsals -- fourteen rings of an inward scumble showed as rings, eighteen tripped `inward-comb` and left a dark rim, films wide enough to spread spread too thin and `to_value` refused -- before three soft round-tip strokes of paint made the pool. The Bell-Warden's glow showed its rings too. | **4I2** |
| W10 | **Volume**: *over 2,000 lines before the first stroke*, and links to chase mid-task | M | `PAINTER.md` and `RECIPES.md` whole, `REFERENCE.md` to line 500: about 20,500 words. The first verdict's row 6 again. | **4F1** |
| W11 | **`paintings/` isn't in the pip package** though the guide sends painters there | O | Confirmed: `PAINTER.md` line 23 and `RECIPES.md` line 965 link to it, and the wheel ships six documents and no painting. | **4F5** |
| W12 | ~~**`rehearse_each` and `cost_line` appear only in `REFERENCE.md`**~~ | O | **Half right**: `rehearse_each` and `--alternatives` are in `REFERENCE.md` and `PAINTING.md`, not the card; `cost()` and `cost_line()` are in the card at line 58, as the price of a plan. | **4F6** |
| W13 | **The Bell-Warden's lighting does not paint a face** -- three stacked profiles and a striped kerchief; *A mass built of planes* with the terminator as the shared edge did -- and **where the terminator goes**: a head turned toward a lamp lights more than half its visible face | O | Confirmed from its versions: the figure's first rehearsal is the shifted copies on a face, and its second the terminator run beside the profile, a strip. Its prelude's fix is a `terminator` path shared by the lit plane and the half-tone -- B2's helper, written by hand. **This contradicts B1 as written, for any surface turned toward the light.** | **4B1, 4B4** |
| W14 | **The gaps**: a light's glow on a wall; a hand, *four-finger failure twice but never a fix*; lettering; units for `ribbon` width and `blob` radius | O | In part: no recipe for a light's pool, a hand holding something, or writing; no units row for a ribbon's width or a blob's radii. ~~Never a fix~~: the four-finger failure is told about seven times and its fix once, as a principle, with no recipe. | **4F7, 4F8, 4I** |
| W15 | **A one-page quickstart of the 20 calls a painting uses** | R | The first painter's answers found the same gap: the card names none of the six calls its scripts leaned on most. | **4F1** |
| W16 | **The docs' example budget of 300**, ~~taken for a portrait that wanted 450~~ *(the 450 withdrawn by the painter: the budget never bound, 38 unspent)* | R | The card's example session is `Session(1024, 768, ..., budget=300)`, and its shell section says `300` too. | **4F9** |
| W17 | *From its answers, measured*: **the flour never landed** -- 11 of 262 charged strokes laid no paint, the eight flour strokes among them, laid with a small bristle at loads of `0.12` to `0.25` | M | Confirmed: records 173, 193, 219, 220, 237, 240, 258-262, `4.2%` of the strokes; the flour's finger stroke laid again lays nothing at `0.22`, a trace at `0.35`, paint from `0.5` up. The first painter's ninth engine item, a second time, with a second cause the engine can name. | **4D** (rewritten) |
| W18 | *From its answers*: **the log names a colour by hex where the palette names it** (`#9e6c57` for `lip`) | R | Confirmed: the record keeps the colour, not the slot. | **4H1** |
| W19 | *From its answers*: **an edge shared with an outline, typed by hand** -- `T()`'s outputs worked out and typed where `polygon(face.closed[i:j] + terminator)` would take the edge from the face | R | 38 distinct decimal pairs in its prelude invert through `T()` to whole pixels (its count, 32). The recipes slice `.closed` for a smudge and never for a plane. | **4B4** |

**Found while filing it**: its drawing ran only on a scratch canvas, never on the painting
(the guides-vanish workaround, carried from the first painter's memory), so its drawing
pass is left out of the rebuild. ~~And its fist and face show the upstream rule failing
*with the rule in front of me* -- the first painter credited that rule with saving its
picture, and the second broke it knowingly.~~ *Corrected by its answers: it followed the
rule at the second failure each time, and the move did not go far enough -- the redraw
kept the view.* **Its answers found two more things** (W17, W18): the flour its why names
never landed, and its log names a colour by hex where the palette names it.

---

## 4. Workstreams

Each says what is there, what is proposed, **how it answers the painter's point**, what
step 2 measures before it is built, and -- where it does -- what earlier work it changes,
which section 5 gathers in one place. The painter's eight suggestions, in its own order,
land here:

| # | The painter's suggestion | Answered by | In short |
|---|---|---|---|
| 1 | A free silhouette and value thumbnail at drawing time -- a notan | **4A3** | `s.thumbnail({place: value})`: the masses flat, small and free, before a mark |
| 2 | Guides visible on any ground; `guide()` and `pencil()` taking a shape and drawing its exact outline | **4A1, 4A2** | a two-tone line; a shape drawn as its outline, corners kept |
| 3 | A per-call cost breakdown in the rehearsal report | **4C** | a `dearest:` line naming each costly call by its script line |
| 4 | A warning when a light mark lands in wet paint, with `dry()` as the fix | **4D** | `into-wet`, measured on the damage -- built only on evidence, since the painter's own number was the plan's reading |
| 5 | Declaring a low- or high-key picture; *lightest* by the brightest part of a place | **4E1, 4E2** | `plan(key=)`; a place read by its median, or the reading the painter picks |
| 6 | A recipe or helper for lighting a silhouette from one side, and a note on `feather=` | **4B** | the recipe with its missing join; the terminator as a path; `feather=` said to break, not soften |
| 7 | A silhouette-readability exercise, and a recipe for complex organic silhouettes | **4A4** | *A silhouette built from parts*, and exercise 10 |
| 8 | A leaner `PAINTER.md` with a self-sufficient first page, anecdotes and commentary moved out, dense paragraphs as tables | **4F1, 4F2** | moved, not cut; the budget lowered behind it; `report()` as two tables |

And its closing question -- a report in the painting's folder, or issues here -- is O3.

*Added 2026-09-26.* **The second painter's suggestions** land here too; its questions are
W-Q1 to W-Q7 in section 6.

| # | The second painter's suggestion | Answered by | In short |
|---|---|---|---|
| 1 | A drawing unit (`s.px()` or `Session(units="px")`), and a way to scale or move a group of shapes together | **4A5** | `s.px(x, y)` beside the fractions, and a group moved or scaled about one point |
| 2 | A per-call cost table in each rehearsal report | **4C** | the dearest line, as the first painter decided it |
| 3 | Every finding names its marks: the log index, the `note`, or the script line | **4H1** | a finding names the calls behind it, by script line where `_one_call` knows it |
| 4 | Plan declarations for a low-key picture and for a small light source | **4E1, 4E4** | `key=`; and the light the plan names read where it is, not by the canvas's top twentieth |
| 5 | Turn *failed twice, go back to the drawing* into a notice | **4H4** | measured first: a count of passes laid over one place, over the corpus |
| 6 | A lettering verb, and a glow verb for lamps and windows | **4I1, 4I2** | a recipe first for each, and a verb only if the recipe is too dear |
| 7 | A warning when a pass overwrites a name the prelude defined | **4H2** | a fact at the call, from `run_scripts` |
| docs | A one-page quickstart; `paintings/` shipped or linked; `rehearse_each` and `cost` in the loop; recipes for a light pool on a surface, a head turned toward a light, a hand holding something, and lettering | **4F1, 4F5-4F9, 4B4, 4I** | the card's vocabulary line; working links; one clause in the loop; three recipes, and a fourth if lettering is built |

### A. Drawing a complex shape

The painter's headline, and rows 1, 2, 8 and 11. The drawing is free, and it is the one
thing *failed twice* sends a painter back to -- and for a complex shape three things stand
between the painter and seeing what it drew.

**A1. Guides that read on any ground.** `_draw_guides` draws every guide as a two-tone
line -- a light casing about three pixels wide under the one-pixel graphite core -- and
puts its note in a box, as a landmark's name already is. Whatever the paint under it, one
of the two tones differs from it by a wide margin, which is why maps draw roads that way;
both are neutral, so nothing on screen carries hue in a values view. Only the view
changes: not the canvas, not the log, not an export, and not `look(sketch=False)`, which
still hides the drawing with the pencil.

- *How it answers the painter*: the drawing is judged where it is -- over the paint, on the
  real canvas -- and the throwaway light canvas is not needed. The near masses drawn again
  after the far ones are down, which is the guide's own order, become visible for the
  first time on a dark picture.
- *Step 2*: the value step at every guide pixel, for the candidates side by side -- the
  casing; an ink chosen per pixel against what is under it; today's -- over the corpus's
  darkest and lightest finished canvases and the bare grounds, the target being no guide
  pixel under a step of about `0.25` in one of its tones; and looked at on a mid-grey
  canvas, where a double line could hide what it is drawn over.
- *Changes*: 0.5.0 drew the overlay *the way a pencil line reads rather than the way a
  landmark does -- thin, dark*. It still reads as a line; it stops disappearing.
- *Step 2 (2026-09-26): built as written.* Over 35 grounds -- every ground preset bare, a
  flat mid-grey, both paintings, and every committed picture -- today's line leaves a median
  88% of its pixels under a step of `0.25`, and over the room the painter's second drawing
  went on, 96% under `0.05`; **the cased line leaves none under `0.25` on any of them**,
  opaque or with its casing at 150 of 255. An ink chosen per pixel fails where the paint
  sits at its switch (100% on `burnt_sienna`). Looked at, the translucent casing gives way
  to the paint most; which of the two is the painter's (question 4b).

**A2. A shape handed to `guide()` or `pencil()` is drawn as its outline, corners kept.**
`s.guide(plinth, note="plinth")` and `s.pencil(plinth)` take a shape -- a `Polygon`, a
`Region`, or anything `as_place` reads -- and draw its closed outline exactly. A pencil
record then carries the outline's points and `smooth=False`, so it replays as drawn, and
`sketch_lines()` and `erase(place)` treat it as any other line. A list of points is drawn
as it is today, splined by default, and the docstrings and `REFERENCE.md` say in one
clause what the spline does to a corner. Through the server, the `guide` and `pencil`
tools take a place where they take points; `RECIPES.md`'s straight-edge recipe loses its
`.closed, ..., smooth=False`.

- *How it answers the painter*: the call that feels natural for a polygon is the shape
  itself, and it keeps the polygon's corners -- the plinth is a box in the drawing check, as
  it is in the prelude -- while every script that relies on the spline, a curve drawn
  through six points, is left alone.
- *Not proposed*: moving `smooth`'s default. A pencil line is graphite in the canvas and
  shows in the export wherever paint leaves it, and a curve drawn through a few points
  *wants* the spline. The fault was that a shape could not be handed over at all, and
  both calls raise on one today, so nothing that worked changes.
- *Step 2 (2026-09-26): built as written.* Both calls raise `TypeError` on a `Polygon` and
  on a `Region`, and the spline through a closed outline puts 99% of the plinth's drawn
  path outside the plinth, as far as 21.6 px (30.7 on its front plane).

**A3. A thumbnail of the masses, flat, at drawing time -- the painter's first
suggestion.** `s.thumbnail({place: value, ...}, size=None, path=None)`: each place filled
flat at its value -- or at a colour's value, a slot like `"stone_mid"` read through
`value_of` -- in the order given, later over earlier, on the ground's own value, rendered
small in greyscale and written as a PNG. With no argument it draws the plan's own places.
Free, as a preview is: nothing painted, logged or charged, the stream untouched, and a test
in the *planning verbs leave nothing behind* pattern. The same through the server, as a
`thumbnail` tool whose places are read as `plan`'s are.

- *How it answers the painter*: it is the notan -- the arrangement as three or four values
  at the size of a postage stamp, before a mark -- which is where a silhouette reads or
  does not. The ears, the piebald's islands and the arch are all plain in a flat, small
  render of the shapes that made them, and each cost this painter a rehearsal of 85 to 113
  marks to see. `preview()` does not answer it: it draws a mass in a translucent hue over
  the canvas at full size, which says *where* the mass goes, not whether the arrangement
  reads.
- *Step 2*: the painter's own masses -- the final set, and the cat and piebald versions if
  the painter sends them (question 3), or rebuilt from its first drawing look -- at 96,
  128, 192 and 256 px on the long side, shown blind for the default size (question 4).
- The card's step 1, *Draw it first*, gains one clause naming it, paid for in 4F.
- *Step 2 (2026-09-26): built as written; its default size and signature go to the painter
  (question 4).* The prototype draws each of the painter's seven arrangements in 14 to 36 ms.
  Looked at, at their own sizes: the cat's ears read from 128 px, the piebald's islands at
  every size, the arch's band only from 192. **With no argument it draws the plan's own
  places, and this painting's plan names no mass of its creature** -- the thumbnail of the
  plan is a room and a plinth -- so the build asks the painter whether no argument should
  draw the masses laid so far too. The drawing over a thumbnail buries it.

**A4. A recipe for a silhouette built from parts, and an exercise that judges one.** A new
recipe, *A silhouette built from parts*, under *Before the first stroke*: the largest mass
as an `ellipse` or a `blob` along its own axis; a second at a third to a half of its size,
overlapping it rather than set beside it; the members as `ribbon`s that narrow, set on at
an angle; `union()` for one outline, and `roughen()` for anything nobody ruled; then
`thumbnail({shape: dark})` against the ground, and the arrangement turned until it reads.
Its rules carry ratios, not subjects -- members of one width, narrower than about a sixth
of the largest mass, read as sticks; two matching peaks either side of an upright axis
read as facing the viewer, so one is moved or overlapped; parts that all meet at right
angles, or all leave one point, read as made rather than grown -- and its *Goes wrong as*
is the painter's three failures in the abstract, with a demo. And **exercise 10, *Three
silhouettes***: one set of parts laid three ways -- symmetric, turned with one part
overlapping another, and with its members swelling and narrowing -- each thumbnailed, the
painter writing down what it expects each to read as before it looks. `PAINTING.md`'s list
of ways to make a mass gains `union()` as its sixth.

- *How it answers the painter*: the hardest part of its session gets a procedure, and a
  silhouette stops being forty-two coordinates typed in a row: its parts are few, named and
  movable, which is what makes redrawing a failed drawing cheap.
- *Step 2*: whether the parts need anything the shapes cannot give today. The candidate is
  a width per point on `ribbon()` (`width=[...]`, beside `width` and `end_width`), so a
  member swells and narrows along its length; it is built only if a `union` of ellipses
  along a ribbon cannot do the same cleanly -- *add capability beside the old path*.
  *Added when the painting was filed:* the painter's own first drawing was a `union()` of
  eight ellipses and ribbons, and read as a spiky blob (`evidence/drawing_first.png`,
  redrawn to the pixel from `versions/prelude_union.py` and `p01_v1_union.py`). It is the
  recipe's real failure case, not a reconstructed one: step 2 thumbnails it beside the typed
  polygons that replaced it, and the recipe has to say what the typed polygon did that
  the union did not.
- *Guard*: written under the no-nouns discipline -- the recipe says what a shape of paint
  does and never what it is of -- and grepped for this painting's nouns as well as the
  references'.
- *Step 2 (2026-09-26): the recipe as written, and `ribbon(width=[...])` not built.* A
  member swelling from `0.03` to `0.06` and narrowing to `0.016`, drawn as a `union()` of
  round lobes along its path, swells as a width per point would and leaves 51 sharp notches
  in its outline -- a string of beads; `.smooth()` takes it to 3, the same as a chain of
  ribbons' joints. So the recipe's members are lobes, unioned and smoothed. And in the
  thumbnail the first drawing's union reads as the painter said, a small spiky blob beside
  the plinth; the typed polygons that replaced it read as a creature.

**A5. Drawing in pixels, and a group moved as one** -- *added 2026-09-26*, row W1. **`s.px(x,
y)`** returns the place of a pixel as the fractions every call takes -- `(x / width, y /
height)` -- and `s.px(r)` a length in pixels as a fraction of the long side, the unit a
`size` is in; a helper beside the fractions, so no script changes and nothing touches the
log. **A group**: `group(a, b, ...)` holding shapes, with `.shifted(dx, dy)` and
`.scaled(f, about=)` moving every shape in it about one point, and `.shapes` giving them
back -- what the painter's `T()` did to a head's worth of polygons by hand. Not proposed:
`Session(units="px")`, a switch that would change what every coordinate in a script means
and make every recipe's numbers wrong for the painter who set it.
- *How it answers the painter*: the pixel helper it wrote first is in the engine, named for
  what it is, and the scaling it did by hand is one call on the group.
- *Step 2*: the corpus's own helpers of this kind -- how many preludes define a
  pixel-to-fraction function or scale a set of shapes by hand -- and W-Q1 and W-Q2 for the
  painter.
- *Decided by the second painter (W-Q1, W-Q2, 2026-09-26)*: **the helper, yes** -- it
  would have replaced its `P()` everywhere -- **but not `s.px(r)` as a bare length**: a
  fraction of the long side is a size's unit, and `ellipse` and `blob` take a radius per
  axis in coordinate units, so `blob(p, s.px(25), s.px(25))` is an oval on a canvas that
  is not square. So the length says it is a size (`s.px_size(r)`), and the round shapes
  take pixels themselves (`s.circle(p, px=25)`, `ellipse(..., px=True)`). **The group,
  yes**, and its whole use in this painting was one scale by `1.3` about a point.
- *Step 2 (2026-09-26): built as decided.* Parsed, the corpus: one painting of 24 wrote a
  pixel helper (this one), two moved or scaled points about a centre by hand (this one and
  the heron's second attempt), one drew in metres through a projection; `.shifted()` is in
  eight paintings, `aspect=` in seven, `s.circle` in eight. And **a ribbon's width is not a
  size**: `ribbon(..., 0.05)` is 38 px across a level ribbon on a 1024x768 canvas, 52
  across an upright one and 45 at 45 degrees -- a fraction of the height or the width across
  its line -- which F7's row has to say, and which a `px` form of a width would end.

### B. Light on a form: the terminator, not the feather

Rows 9 and 10, and the painter's sixth suggestion. What the painter found -- copies of the
silhouette shifted away from the light, each held to the silhouette, so the lit rim follows
every edge that faces the light and nothing is drawn by hand -- is the right structure, and
no recipe has it. What the recipes do have is its last step, for a column only: *A form
that turns* joins its two shapes with one half-strength stroke, and says *that step is the
whole difference between a cylinder and two stripes*.

**B1. A recipe, *A silhouette lit from one side*.** The whole silhouette laid in the
light; a copy shifted away from the light laid at the mid value and held to the silhouette
(`clip=`); a second, further off, at the shade; then **a half-value join along each
terminator** -- the part of each copy's outline that lies inside the silhouette; and then
the fills broken, as *A mass built of planes* breaks its planes. The shift is the width of
the lit rim where an edge faces the light, and step 2 puts a number on it. *Goes wrong as*:
islands of light (planes laid as patches), a lit band wrapped round the form, and every
zone held with nothing joined -- the cut-out.

**B2. The terminator as a path.** A helper in `regions.py`, beside `roughen()`: the run of
one outline that lies inside another shape, a margin off its edge. The bench's dozen lines
are its specification, as the handover painter's fifteen were `roughen()`'s. It makes the
join one stroke per zone, on any silhouette.

**B3. `feather=` said for what it is.** One clause where the painter looked -- the new
recipe, and `REFERENCE.md`'s `feather` row -- and one in *A form that turns* pointing at
B1 for a silhouette that is not a column: **a feather breaks a held edge against the
tooth; it does not soften one**, and it breaks every hold of its call, the silhouette's
included. No engine change: 0.7.0's default of `0.002` stays, and a feather per hold is
not built, because at any width a wider feather is speckle (row 9).

- *How B answers the painter*: the technique it found becomes a recipe with its missing
  step -- which on its own pass took the terminators from steps to a turn for two strokes
  -- and its question about `feather=` gets the answer the bench gave, in the place it
  would have looked.
- *Step 2*: row 9's six candidates, plus a zone laid with a soft brush, at 1024x768 and
  1440x960, on the painter's pass and on the recipe's abstract demo; shown to the painter
  blind (question 9). The rim's width, and the join's width and value, as numbers for the
  recipe.
- *Step 2 (2026-09-26): B1, B2 and B3 as written; the painter reads the candidates blind
  (question 9).* Measured as the step across each terminator, 10 to 90%, in pixels: as
  painted `0.5` and `1.0`, a step; **with a half-value join along each terminator, `9.0` and
  `10.5`, the silhouette still `0.5`** -- nine strokes, one a run of B2's helper as benched
  (the runs of a copy's outline inside the body, 4 px off its edge, runs under `0.02` left
  out). At `feather=0.012` one terminator stays a step and the other becomes a speckled
  band ten pixels wide; at `0.03` both do, and the silhouette breaks with them (`1.5`); the
  ragged copies are a staircase; a smudge smears and is told so; soft copies held hard are
  hard. On the recipe's abstract form, the join's size is the turn's width -- `0.006` about
  4 px, `0.010` about 9, `0.016` about 15 -- and past `opacity=0.6` barely matters; a shift
  of `0.016` of the long side, the painter's own, leaves a rim the join can turn. A join run
  ending against the silhouette leaves a blot: the recipe tapers its ends.

*Added 2026-09-26, row W13.* **B1 is scoped, and B gains a fourth recipe.** The second
painter carried B1's structure to a face turned toward the lamp and got three profiles
stacked inside it, like cut paper, and a striped kerchief. Shifted copies light the edges
that face the light, which is the whole of a form seen side-on to it -- a gargoyle in
profile, a column -- and **none of a surface that faces the light**, where the lit part is
a plane inside the silhouette and its terminator runs across the form rather than along
the outline. So **B1 says where it applies**: when the light comes from beside the form, not
from in front of it; and its *Goes wrong as* shows the stacked profiles.
**B4. A recipe, *A head turned toward a light*** -- the painter's own fix, under *A mass
built of planes*: the shadow mass first; then a half-tone band and a lit plane drawn as
polygons **sharing one edge, the terminator**, which is B2's path; and the rule its second
failure taught, with a ratio and no subject -- **a form turned toward the light lights its
whole front plane, more than half of what the viewer sees of it in a three-quarter view**,
so the terminator runs well back from the leading edge, not beside it. *Goes wrong as*: the
strip ([`face_strip.png`](paintings/Claude/wenna_brask/evidence/face_strip.png)), and form
marks laid too strong -- at `0.45` to `0.65` opacity a cast shadow and a hollow read as a
smear and a bruise, at about `0.22` as form.
- *How it answers the second painter*: the technique it was handed says where it stops,
  and the one that worked for it is a recipe with its number.
- *Step 2*: both structures laid on the second painter's own face at its size -- the
  versions in `versions/` are the failures -- and the terminator's place as a share of the
  visible form, for the ratio.
- *From the second painter's answers (W19)*: the recipe takes the shared edge **from the
  outline itself** -- `polygon(form.closed[i:j] + terminator)` -- as *A smudge* already
  slices `.closed`; its painter typed that edge's points by hand, dozens of them, for want
  of the one sentence.
- *Step 2 (2026-09-26): B4 as written, with its ratio.* On the second painter's own face,
  the share of it reading lighter than halfway between its lit and shadow mixtures: the
  shifted copies 35%, the terminator beside the profile 24%, **the planes sharing the
  terminator as painted 74% -- 81% of a row, at the median**. The recipe's rule is a
  number: a form turned toward the light lights about three quarters of what is seen.

### C. What a pass costs, call by call

Row 3, and the painter's third suggestion. `easel run` heads every pass -- rehearsed,
counted or committed -- with one total. **Under it, a line naming the dearest calls**, each
with its strokes, its verb and the script line it was called from, and their share of the
pass. On the painter's own subject pass it would have read:

```
Rehearsed p04_gargoyle.py: 102 strokes of the 210 left. Nothing committed.
  dearest: 23 block_in at p04_gargoyle.py:40 (lay_body), 22 at :38, 20 at :36, 14 at :18 -- 79 of the 102
```

Said only when a call cost more than one stroke -- a mark laid by hand is one, and is never
listed. On `--count` too, which prices a pass in seconds and lays no paint; per version
under `--alternatives`; in the answer of the server's `run`; and in the saved report's
text. The tally is transient: `_one_call` already brackets every mass call, and it notes
the call's verb, its first record, its count, and its site -- the first frame of the stack
outside the package, which is the painter's own line. Beside the log and never in it, and
saved only as the report's text.

- *How it answers the painter*: the rehearsal that came back at 113 would have said which of
  four `block_in`s had grown, and so which one to widen, or to price with `cost_line`. That
  is the question the painter could not put to a script, because `cost()` takes a plan and a
  pass is functions.
- *Step 2*: the line over every pass of the corpus -- how long it runs, whether three calls
  or four is the right count, and whether the line or the function's name is what reads
  (question 8).
- *Decided by the painter (question 8, 2026-09-26)*: **after every pass** -- rehearsed,
  counted and committed, because the committed report is the one kept and a painter who
  does not rehearse sees only that one; **the function named once per run of calls from
  it, and every call's line** -- its three dearest subject calls are all `lay_body`, all
  noted `subject`, and told apart only by line; **up to four calls, stopping once three
  quarters of the pass is named** -- a fixed three stops its room at 71% and its subject at
  64%; and **per call, the strokes that landed nothing**: *24 block_in at
  p05_details.py:12 (lay_core_shadow), 6 landing nothing* would have told it to fit that
  shape before paying for it (D, and the ninth engine row in `SUGGESTIONS.md`).
- *Step 2 (2026-09-26): built as decided.* Over the 331 corpus passes that lay paint, the
  line prints on 143 (43%) -- the rest have no call dearer than a stroke -- names one call on
  53 of them, two on 41, three on 29 and four on 20, and **names a median 76% of its pass**
  (a fixed three, 74%; four calls fall short of three quarters on 10 passes); it runs a
  median of 67 characters, 163 at the longest. A call made inside a prelude's helper is
  named at the helper's line in `prelude.py`, with the helper's name. The subject's pass
  would have read *dearest: 23 block_in at p04_gargoyle.py:40 (lay_body, 2 landing
  nothing), 22 at :38, 20 at :36, 14 at :18 (lay_wing) -- 79 of the 102*.

### D. ~~A light laid into wet paint -- built only on evidence~~ A mark that lands short, and strokes that land nothing

*Rewritten 2026-09-26, after the painter's answers.* **The painter withdrew `into-wet` as
written.** The one light in its painting that met wet paint, on the claws, loses `0.01` to
`0.05` to the wet and `0.27` to `0.31` to its own size -- a `0.0032` to `0.0035` round tip
lays too little paint to reach its value -- so a notice gated on a light landing short on
wet paint *would fire on these two and send me to `dry()`, which recovers `0.05` of `0.31`.
That is the engine making my own misattribution for me.* If one is ever built, it measures
the mark laid wet against the same mark laid dry, not against the mark's own value.
**What it asked for instead** is a fact at the call for any mark laid by hand that lands
far short of its own value, whatever the cause, saying the cause the engine can see -- the
mark's size in pixels, the wetness under it, the clip that took it. On this painting it
names the spark, the ember and the claw lights, which are the eye and the claws its
why-sentence names. And, on C's line, per call, the strokes that landed nothing: twelve of
its 280 were passes of clipped masses, paid for and laying nothing. The four conditions
below hold for the new candidate as for the old: a real case (the eye and the claws), about
one corpus pass in twenty or fewer, a threshold in a gap, and no guide block but a failure
on purpose. Step 2's `--wet` becomes `--short`: every hand-laid mark's landed shortfall over
the corpus, and the cause the engine could name. **Whether a stroke that lands nothing is
charged** is step 2's too, and narrow: dropping it from the log would renumber every later
record, which rule 7 forbids, so the candidates are saying so, and keeping its place in the
log while it stops counting against the budget. **A second painting gives it a second case
and a second cause** (W17): the flour its why names never landed -- eight strokes of a small
bristle at loads of `0.12` to `0.25`, where it lays nothing under about `0.5` -- with the
nostril, the catchlight and the flame's core, `4.2%` of its strokes. The fact names the
cause the engine can see: here the load, for the brush's size. *The text below is the
candidate as it was first written.*

*Step 2 (2026-09-26): narrowed to a round dab that lands nothing, which meets all four
conditions; the general fact meets none of the last three.* Over the corpus's 3,096 marks
laid by hand, 2,047 meant to stand `0.10` off what they met, **how far a mark gets toward
its own value has no gap** -- a continuum from nought up, the marks that laid nothing the
only cluster -- and a fact below any share of the way would speak on 14% to 39% of the
corpus's passes, because most marks that land short do it on purpose: a starved bristle is
the dry brush, a translucent stroke a film laid as paint. On the guide's blocks it fires on
2 to 4 of 72. **A round dab that lays under one unit of paint is another matter**: where a
round tip stops landing is a cliff in pixels, not in the size's fraction -- `press=1` from
6.5 px, `press=2` from 5.6, `press=3` from 2 to 3, at 1024 and at 1440 alike -- and of the
corpus's 196 round dabs laid by hand, 56 of the 57 that landed nothing were under their
cliff. It falls on 11 passes of 341 (3.2%), in eight paintings, every one a mark that laid
nothing, and on no guide block: the spark (2.9 px at `press=1`), the catchlight, and the
misty forest's forty-two two-touch dabs of 5 px. The cause is geometric, so it can be said
at the call: *this dab laid no paint: a round tip at press=1 lays none under about 6.5 px
-- press=3, or size over 0.0065*. **A starved bristle that lays nothing** -- the flour -- is
on 33 passes (9.7%), a continuum of paint, and past the budget as a notice; it stays on C's
line when a call is dearer than a stroke, and is question D for the painter below: whether
the post-pass check should name the marks that laid nothing, as H1 names a finding's
marks. Such a line would name one guide block's mark: *A mass built of planes*'s dry-brush
stroke, a bristle at `load=0.35` that lays nothing on the check's 400x300 canvas -- the
recipe's to fix in F, as rule 2 says of a rule that fires on a recipe. **And the wet has no
case left**: the two subject-pass versions that laid the head's plane in the pass with the
body read it at `0.595` and `0.567` laid wet and `0.591` and `0.563` dried first, with
`0.014` and `0.005` of wetness under it. A dab that lands but
short -- the ember, `1.6` units at `press=2`, reading a tenth of its way -- is a light touch
by design, as `dab()` says: a two-touch dab reads a fifth of the way at any size to 12 px.

Row 4, and the painter's fourth suggestion. **The candidate is a fact at the call, measured
after the mark as `glaze-far` is** -- the damage rather than the wetness: a mark laid by
hand, meant to stand off what it lands on by more than `0.10`, that lands short of its own
value by more than a threshold over its footprint, on paint that was wet under it. Working
name `into-wet`: *this mark was mixed at 0.64 and reads 0.52 where it landed: the paint
under it was wet (0.83), and a brush dragged through wet paint carries it. `s.dry()` first
-- or `dry(region=...)` to keep the rest wet.*

**It is built only if** (a) it fires on a pass that really did lay a light into wet paint
-- ~~the painter's own, rebuilt if it can be (question 2), since its committed passes did
not~~ *the painter's own case is not one: its session shows the head's top reading `0.52`
before and after the `dry()` calls (row 4). The candidates left are the two subject-pass
versions that read the plane at `0.56` and `0.54`, recovered in `versions/`, and any
other case the painter can name (question 2's follow-up)*;
(b) it fires on no more than about one corpus pass in twenty; (c) its threshold sits in a
gap of the corpus's distribution rather than in its tail; and (d) it fires on no guide
block that is not a failure on purpose. Exercise 4 lays yellow into wet blue to show
exactly this, so it would say so -- the one place where its saying so is the point -- and
`check_guide_blocks.py` has to be told, the way a *Goes wrong as* block is.

- *How it answers the painter*: where the engine can know that a light landed dull because
  of wet paint, it says so at the mark, with the number and the fix, the way `glaze-far`
  sent this painter to `to_value=`.
- *Changes*: it reopens 0.6.0's decline of `wet-under` (section 5, row 1). If the evidence
  does not come, the decline stands, and the round records its new data point: this
  painter's own number, checked against its file, was the plan's reading and not the paint.
  *Settled 2026-09-26: the evidence did not come, and the decline stands; section 5, row
  1.*

### E. The plan: a declared key, and what a place reads

**E1. `s.plan(key="low")` -- and `"high"`.** A declaration in `bands=` and `ground=`'s
pattern -- `KEY_WORDS = ("", "low", "high")`, saved with the rest of the plan and read
back with `.get` -- which **replaces the `values:` line's judgement against the box's middle with the
key's own question**. Under `"low"` the line does not say *no clear light*. It says the
picture is low-key as the plan says -- or, if its top twentieth has risen past the box's
middle, that it has left its key and by how much -- and then goes on to the question it
never reaches for a dark picture today: whether its clusters are a light, a mid and a dark
*inside* the key, or two of them read as one. `"high"` is the same the other way. `easel
plan --key low`, `key` on the server's `plan`, the `easel new` prelude, and a row in
`REFERENCE.md`'s *What the plan changes*.

- *How it answers the painter*: a low-key picture can say so where the check can hold it to
  it, as a buried ground can, and twenty-five reports of *no clear light* become one line
  that measures something the painter could still get wrong. Its own picture would have
  been told that its bottom two clusters are `0.07` apart.
- *Not a switch*: under either key the line keeps a number and a threshold, and a picture
  that drifts out of its key is told so.
- *Decided by the painter (question 6, 2026-09-26)*: **(1), the top twentieth under the
  box's middle.** On its picture it would never have spoken -- its top twentieth ran from
  `0.28` to `0.38` over all 25 reports, never within `0.16` of `0.54` -- which is the shape
  a declaration should have: silent while kept, speaking when left. (2) asks for a number a
  painter does not have, and (3) is a switch. **Under a key, print the clusters and do not
  yet judge their gaps**: at today's fixed `0.10`, its bottom two clusters, `0.03` to
  `0.09` apart, would have fired on all 25 reports -- the next *no clear light*. A low key
  compresses the range, so the gap is measured on the corpus's dark pictures (step 2's
  `--key`) before the line judges one. Its picture's own fault, the creature's chest
  against the glow inside one cluster, is one no gap between clusters can see; a planned
  pair could have.
- *Step 2 (2026-09-26): built as decided, the clusters printed and not judged.* Over the
  corpus's 349 passes with paint, *no clear light* is said on 78, and seven pictures finish
  low-key: the pier, the hands, this one, Wenna Brask, the terminal window, the harbour and
  Kimi's lighthouse. Declared low-key, **they would have heard nothing on 72 of their 74
  passes**, and on the other two the pier would have been told its top twentieth had risen
  to `0.73`, past its key. Their closest two clusters sit a median `0.078` apart against
  `0.141` on every other pass, so a fixed `0.10` would judge 61 of the 74 as one mass, and a
  gap scaled to the picture's range (about `0.027`) judges none: no threshold yet.

**E2. A place reads what most of it reads.** One reading for every planned place --
`plan:`, `lightest:`, and `compare(s.plan())` or any `{place: value}` handed to
`compare()` -- taken as **the median of the place rather than its mean**, so that a detail
inside a planned plane does not move what the plane reads. `compare()` against a
photograph keeps its cells and their means: that is a different question.

- *How it answers the painter*: the head's top reads `0.61` -- the lightest of the places,
  and inside its plan -- where it read `0.52` and a miss, and the plan's lines stop
  reporting the eye as the plane.
- *Candidates, and why the median*: the painter asked for *the brightest part of a place*.
  The 90th percentile answers `lightest:`, but it would read every planned mass by its
  lights on the `plan:` line; the median serves both lines with one number and holds the
  painter's case (`0.606` against `0.626`). Step 2 decides between the median and the 75th
  and 90th percentiles, on both plans pass by pass and on synthetic places with a detail
  inside them over the corpus's canvases (question 5), and whether a place split between
  two values should say so -- *head top reads 0.61, 14% of it under 0.35* -- in
  `sample-split`'s manner.
- *Changes*: 0.6.0's instrument (section 5, row 2).
- *Decided by the painter (question 5, 2026-09-26)*: **the median, one number for both
  lines.** By the 90th percentile the floor misses by `0.12` from the plinth's pass on,
  because the lamp's pool lies in it, so the 90th cannot read `plan:`; and a brightest part
  for `lightest:` alone would leave `plan:` printing the mean's miss beside a `lightest:`
  reading `0.63` -- the reading that sent it wrong. **A split place says so, on a line that
  already names it, measured from its own median**: *head top reads 0.61; 24% of it darker
  by more than 0.15*. A tenth of a place or more, more than `0.15` from its own median,
  marks exactly two places over the whole painting, both for a reason -- the plinth's top,
  where the creature's feet stand (15%, then 18%), and the head's top, the eye (24%) --
  and nothing else passes 7% (re-measured, `CALIBRATION.md`). A fixed `0.35` was chosen
  knowing where the eye was. The same clause shows the median's own failure: a detail
  covering more than half its place.
- *Step 2 (2026-09-26): built as decided.* The three plans pass by pass: this painting's
  `plan:` line 7 of 7 by the median from the details pass on (6 by the mean, 6 by the 90th);
  the handover's 7 of 7 under every reading -- **and on its tower's pass the mean named
  another place the lightest where the median names the lantern**; Wenna Brask's 4 of 5
  under every reading. A detail `0.30` off its place's median, put into 595 places over
  every finished corpus canvas: **the median moves under `0.02` to 30% of the place, `0.05`
  at 45%, and flips past half**, either way; the mean moves `0.03` a tenth; the 90th gives
  way to a light detail at 10% and the 75th at 30%. The split marks 4 of the 19 planned
  places, each with something inside it, and 31% of places drawn at random -- which straddle
  two masses as often as not, what the clause is for.

**E3. The floor, said as it is -- and a black, as a question with a measurement.** Row 13,
and the owner's follow-up on it.

- **`at_value` tells the truth at the bottom.** When a target is under the default dark,
  the error names what the box does reach and how -- `dark="burnt_umber"` lays `0.128`,
  warm, and seven parts umber to three of ultramarine the most neutral near-black at
  `0.132` -- and the one way below it, a supplied colour, with its value. It does not
  switch darks by itself: a colour handed back in a hue nobody asked for is the silent
  failure `at_value` raises to prevent. `shade()` is left as it is; it already reaches the
  floor.
- **One floor in every document**: `0.128`, burnt umber alone, with the blue-umber mix
  holding `0.13` to `0.15` as it swings from cool to warm -- in `PAINTER.md`,
  `PAINTING.md`, `CALIBRATION.md` and `palette.py`'s own docstrings, which say *about
  0.13* in one place and *0.14-0.96* in another. Written in F3.
- **A black is not proposed this round.** The one ask was a hundredth, and inside the box;
  the corpus never asked; and a supplied colour already lays any dark as written.
  **Step 2 measures the real question instead** -- whether a low-key picture wants more
  room below `0.128`, which is where the floor costs most, since a picture that lives
  between `0.13` and `0.35` has two steps of `0.10` to separate its masses with. The darks
  of the four pictures that sit on the floor, and of this one, re-laid with a supplied
  near-black between `0.05` and `0.09`, and looked at; and the painter asked (question
  10). If that says yes, the candidate is **a dark with a hue** -- a deeper masstone of
  one of the darks the box has -- rather than a neutral tube black, and it comes with what
  it moves: `darkest_value`, and with it every `values:` line's box and the middle E1's key
  is judged against, and `compare()`'s unreachable split. The reason for the hue is the one
  `PAINTING.md` opens its colour section with -- *mixed darks are alive, tube black is dead*
  -- and `LESSONS.md`'s trap 14: whatever the box offers, a painter reaches for, and a
  pigment named black gets reached for first, for shadows.
- *Step 2 (2026-09-26): no black; the painter sees its painting both ways (question 10).*
  Six low-key pictures rebuilt with every colour under `0.20` taken further down, the floor
  to `0.07`: their darkest hundredth falls from `0.137`-`0.157` to `0.086`-`0.122`, and the
  share of the canvas under `0.15` from 1%-18% to 18%-62%. **But the darks move down
  together**: this painting's planned darks, the wall and the floor, both planned at `0.17`,
  stay `0.01` apart (`0.17`-`0.18`, then `0.15`-`0.16`); what a darker dark separates is
  only what was already apart -- its room's mixtures, `0.15` to `0.21`, would have run `0.11`
  to `0.21`. The room lacked a plan with its darks apart, not a pigment.

**E4. The light a plan names, read where it is** -- *added 2026-09-26*, row W4. The second
painting's lamp is the case E1 and E2 do not reach. Its place is mostly iron, so the
median reads it at `0.51` against `0.76` and no reading of the whole place finds the lit
panes; and the `values:` line reads the canvas's top twentieth, `0.42`, where `1.4%` of
the canvas lies above `0.60` -- a lamp is too small for a percentile of a twentieth. The
painter asked for *a declaration for a small light source*, and **the plan already has
one**: `lightest=` names the place. What is proposed is to read it as a light: **the
`lightest:` line reads the named place by its brightest part** -- its 90th percentile, or
step 2's number -- while `plan:` keeps E2's median for every place, the lightest
included, so the two lines say two different things about it and each says what it
measures (*lantern: its lightest tenth `0.58`, the place as a whole `0.51`* -- and a place
whose lit part is smaller than a tenth still needs its panes planned as a place of their
own, which the recipe for a light says); and **under a key,
the `values:` line asks whether the named light stands clear of the rest**, which is the
question a low-key picture with a small light is really asking. This reopens the
Bell-Warden painter's reason against the 90th for `lightest:` -- two lines disagreeing
about one place -- and answers it by saying what each line measures.
- *How it answers the second painter*: its lamp is read as a lamp, and the line that
  missed it by `0.27` says how bright its brightest part is.
- *Step 2*: the lightest place of every corpus painting with a plan, read by its median
  and its 90th and 95th percentiles, pass by pass; how often a named light is under a
  twentieth of the canvas; and question W-Q5 for the second painter and a follow-up for
  the first, since this revisits its answer.
- *Decided by the second painter (W-Q5, 2026-09-26)*: **if it is built, the 95th
  percentile inside the named place, not its brightest pixel** -- a stray highlight is one
  pixel, and on its canvas that pixel was the face's -- **printed beside the whole**:
  *lantern 0.49 as a place, 0.59 at its brightest twentieth*. **But its own case was a
  wrong plan, not a wrong reading**: the face is the lightest thing in the picture by every
  reading, it should be, and the plan never named it; the lantern's `0.76` was a mixture's
  value, where its panes read `0.58`. So the documentation's half of E4 is the rule the
  why already implies: **plan the place the why names, and plan a light at the value its
  place will read, not the value its mixture was mixed at**.
- *Step 2 (2026-09-26): built as decided.* Every plan's named light is under a fiftieth of
  its canvas -- the head's top 0.20%, the handover's lantern 0.08%, Wenna Brask's 1.13% --
  and every one stands clear of the canvas's top twentieth, which the `values:` line reads,
  by `0.17` to `0.28` at its 95th percentile. Read at its 95th, no plan's `lightest:`
  verdict changes; the number printed does (Wenna Brask's lantern `0.51` by its median,
  `0.59` at its 95th). The first painter's follow-up is question 5f.

### F. The documentation

**F1. `PAINTER.md`, lighter by moving what is not method -- the painter's eighth
suggestion.** Out of the card and the body, and into the files that already hold such
things: **commentary on the documents themselves** -- *every rule in these five files is
stated once*, *this file has stopped calling them a gate*, *this file is sufficient to
finish a painting, which is a trap*, *the card above is the whole of it* -- to
`LESSONS.md`, where the documents' own history lives; and **the anecdotes**, to
`CALIBRATION.md`'s *From the sessions*, labelled as reports, keeping beside each rule the
one sentence of evidence the painter says persuaded (question 7). What stays is what it
said worked: the order of work, *What you are bad at* with its fixes, the upstream rule,
the exercises, the checklist, and the card as a first page someone could start painting
from alone. **Then `FRONT_PAGE_WORDS` comes down to the new size and a little room**, so
the file cannot grow back to its ceiling. At 6,655 of 6,700 today, the budget is what makes
this round's own lines -- A3's clause, exercise 10, F3's clause -- impossible without the
move. Every signpost that states the card's or the file's size -- the README, `llms.txt`,
the CLI's help, the server's `guide` tool -- moves with it, which is 0.7.0's step 9 lesson.

- *How it answers the painter*: the first page reads as a method and nothing else, the
  context a painter spends on the documents' account of themselves goes to painting, and
  the persuasion that worked is kept.
- *Changes*: 0.7.0's ruling on the weight (section 5, row 4).
- *Decided by the painter (question 7, 2026-09-26)*: **keep, beside their rules**, *eighty
  strokes on four treatments* -- once, where the painter finds it told in five places with
  three morals -- *the picture finished without opening the other four*, and *the pier*,
  the one story about a failure no line catches. **Drop** *the four near-parallel fingers*
  and *the arrangement redrawn three times*, whose rules carry their own instruments, and
  the framing *every painter so far* (lines 109, 373 and 407), whose work was done by *and
  the checklist counts them*. **And the card lacks one line**: that a mass can be held to a
  shape with `clip=` and `edge="hard"`, with `at_value` beside `mix`. The card (lines 1 to
  143) names none of the six calls its scripts lean on most -- `at_value` 29 times, `edge=`
  14, `s.dry` 10, `clip=` 8, `.shifted` 4, `.inset` 3 -- and **`clip=` appears nowhere in
  `PAINTER.md`**, where half its lighting came from. For the method the card carried it;
  for the vocabulary it did not.
- *And the second painter's twenty (W-Q7, 2026-09-26)*, counted from its scripts --
  `opacity=` 97 uses, `pressure=` 86, `s.stroke` 84, `p.at_value` 54, `note=` 51, `clip=`
  41 -- of which the card names none of `at_value`, `clip=`, `pressure`, `opacity`,
  `sample`, `mix_many` or `note=`, and **`clip=`, `sample` and `mix_many` appear nowhere in
  `PAINTER.md`**. Its list for a first page: `s.stroke`; `s.block_in` with `solid=`,
  `direction=` and `edge="hard"`; `clip=`; `s.glaze`; `s.dab`, and that a round dab under
  about `0.007` lands next to nothing; `s.dry`; `pressure=`; `opacity=`; `load=`, and that a
  small bristle under about `0.5` lays nothing; `tip_wobble=`; `note=`; `p.at_value`;
  `p.mix` and `p.mix_many`; `p.value_of`; `polygon`, `blob` and `roughen`, with slices of
  `.closed`; `s.look` with `values=` and `region=`; `s.sample`; `s.plan`; `easel run
  --rehearse`; and `easel log`, for what landed nothing, with `easel check`. F1's line for
  the card is chosen from it and from the first painter's six.

**F2. Tables where a paragraph is a list.** `REFERENCE.md`'s `report()` paragraph becomes
two tables -- the ten rules, each with when it fires, the number it uses and what it says;
and the five standing lines, each with what it measures and when it speaks -- and the prose
around them keeps only what is not a row. The same pass looks for any other paragraph that
is a list in disguise and names what it turns; `PAINTER.md`'s account of the checklist's
lines is the likeliest.

**F3. What is no longer true, and one question with a size in it.** *Every painter so far
has painted boxes* and *each has been made by every painter so far* stopped being true with
this painting (0 of 17), and are said as what they are. The palette's floor is said one way
everywhere -- `0.128`, burnt umber alone -- where it is `0.13`, `0.14` and *darker than any
single pigment* today (E3). `LESSONS.md`'s count of re-measured claims -- left stale by
0.7.0 -- is counted again with this round's three in it.
And the closing checklist's third question gains the size the picture will be seen at --
*is that reason still in the picture, looked at small?*, with `s.look(scale=256)` beside it
-- which is row 12's answer, in the one place the tool already asks about the reason.

**F4. The record.** `SUGGESTIONS.md` opens the round; `LESSONS.md`'s protocol gains its
data points -- what the second painter against the card and body read, a `boxes:` line at
nought against the card's *every painter so far*, a broken edge that did not stop a
cut-out where every zone was held, and a painter's number that turned out to be the
plan's reading; a section
in `CALIBRATION.md`, *The bell-warden's round*; and a section in `PAINTINGS.md`, with the
order its passes rebuild in.

*Added 2026-09-26, for the second verdict.*

**F5. Links that work from the package** (W11). `PAINTER.md` and `RECIPES.md` send a painter
to `paintings/`, which the wheel does not ship: the links become the repository's own
address, so they work from `easel guide` as they do on GitHub, and `llms.txt` and the
README already point there. Shipping the paintings in the wheel is not proposed: they are
megabytes of pictures, and the decide-then-read rule wants them one step away, not in the
package a painter reads first.

**F6. Versions and prices in the loop** (W12). One clause in the card's *rehearse* step
naming `--alternatives` for versions of a pass and `--count` for a price in seconds -- paid
for by F1's move -- where today a painter meets them only in `REFERENCE.md` and
`PAINTING.md`.

**F7. The units table, finished** (W14). Rows for a `ribbon`'s width and end width and a
`blob`'s radii -- the long side, or the width and height -- measured from the code, not
reasoned, and the sentence under the table saying which shapes are round in pixels.
*Step 2 (2026-09-26), measured off the masks*: a ribbon's width is the canvas's coordinate
across its line -- `ribbon(..., 0.05)` is 38 px across a level ribbon at 1024x768, 52 across
an upright one, 45 at 45 degrees -- so it changes as the ribbon turns; `ellipse(p, 0.05)`
and `blob(p, 0.05)` are 102 x 76 px, a fraction of the width across and the height down, and
round in pixels only with `aspect=` (102 x 102); a brush's `size=0.05` is 51 px on either
canvas.

**F8. Two more recipes** (W14), under the no-nouns discipline: ***A light's pool on a
surface*** -- the second painter's fix, three soft round-tip strokes of paint, each smaller
and lighter, centred where the light falls, with the inward scumble's rings and the wide
film too thin to reach its value as its *Goes wrong as* -- and ***A hand closed on
something*** -- the first painter's rule for a row of like things, turned into a procedure:
draw the view, not the object; the fingers as one mass coming toward the viewer, an edge
of what is held crossing them. The hand is the one of the two that is a subject rather
than a shape, so it is written as *a small cluster of like parts gripping an edge*, and
grepped.

**F9. The example's budget, said to be the example's** (W16). The card's example session
keeps `budget=300`, and one clause beside it says a budget is the painter's to set from
the picture -- a figure at the size of the canvas wants more than a landscape of big masses
-- because a worked example is an instruction. *Its painter's answer (W-Q7)*: it typed
`300` without a thought, from the card, its shell section and its memory of the first
painting; the budget never bound (38 unspent), so the clause would have changed the number
and not the painting -- and is still worth its line, for the painter who runs out.

### H. What the check says, and where -- *added 2026-09-26*

The second verdict's points about the tool's own messages.

**H1. A finding names its marks** (W3, W18). Every post-pass finding that counts marks names
them: the calls they came from, by script line where `_one_call` knew it -- the same site
C records -- and the log indexes. *4 small marks … around (0.55, 0.37)* becomes *4 small
marks at `p05_face.py:58`, `:62`, `:64` and `:72` (records 174, 176, 177 and 179), around
(0.55, 0.37)* -- the mouth's four soft marks, found here by hand from the file. Output
only; beside the log. *Decided by the second painter (W-Q3)*: **the script line with its
function** -- `p05_face.py:58 (lay_mouth)` -- the name it thinks in; the note cannot tell
them apart (184 of its 262 marks say `subject`). And **the log line names a colour by its
palette slot** where it has one -- *`lip`*, not *`#9e6c57`* -- which means the record
keeps the slot's name beside the colour: a new key on the record, read with `.get`,
beside the log and not in the index, so nothing rebuilds differently.

**H2. A pass that rebinds a prelude's name is told** (W7). `run_scripts` notes the names
the prelude binds; after the pass it says, once, which of them the pass bound again --
*this pass rebinds `H`, which the prelude defined: the prelude's value is gone for the rest
of this pass*. A fact at the call, not a refusal: rebinding on purpose is a painter's
right. *Step 2 (2026-09-26): narrowed, then built.* Parsed, 20 of the corpus's 284 committed
passes run after a prelude bind a name it bound -- 17 to the same thing (the pier's
`p = s.palette` in twelve passes, a re-import) and 3 to a variable the prelude's own loop
left bound. Said only when the name was the prelude's by assignment, definition or import,
and the pass bound it to something else, it would speak on none of them -- and on the
second painter's `H`, which was in rehearsals that raised on it and are not filed.

**H3. `--scale` said for what it is** (W6). The option stays the long side in pixels,
because a pixel count is what a look is sized by; its help and `REFERENCE.md` say so in
the option's first words, and a value under `1` is read as a factor of the canvas's long
side, which is what the painter meant and what no pixel count can be.

**H4. A place laid over and over: measured, not built** (W8). The second painter asked for
the upstream rule as a notice; 0.7.0's round considered a repainted-passage count and
dropped it, because the log cannot tell a passage failing from a subject being built.
Step 2 counts, over the corpus, the passes that lay marks over one place -- the fist's
five, the Bell-Warden's head, the handover's headland -- against the subjects built in as
many; **it is built only if a count separates them**, and then as a fact with the number,
not a rule. Otherwise the decline stands with a second painter's case beside it (section
5, row 6). *Decided by the second painter (W-Q6)*: **count masses laid over the painter's
own earlier marks in one place, rehearsals included, and speak at the second** -- passes
cannot tell its fist (four) from its face (four); masses over earlier marks can (two, and
none elsewhere). On its painting that count would have spoken at the redraw, when the rule
already had, so it adds a number, not a decision, and **is built only if the corpus
separates**. *Step 2 (2026-09-26): it does not separate, and the decline stands* (section 5,
row 6). Over the corpus's committed passes, counting the painter's `subject` marks -- which
17 of 24 paintings note -- a place is laid over in two runs in two paintings: the fist, and
the night pool's water, laid again in a pass the painter called `p6_redeck`. Counting every
mark, every painting but two has such a place. With the filed rehearsals, the count speaks
on this painting's creature at the details pass's second rehearsal -- a subject being built
-- and never sees the head's failures, laid on a canvas with no subject on it yet; counting a
rehearsal's own marks as earlier, it sees them at the arch, the third version, after the
upstream rule had already sent the painter back twice, and speaks on the second painter's
figure at the pass it committed. It finds the fist, and speaks on a subject being built as
readily.

### I. Lettering, and a lamp's light -- *added 2026-09-26*

**I1. Lettering** (W5). The pack's next pictures need text, and nothing lays a letter. A
recipe first: letters as strokes along a stroke font's paths -- one path a letter, laid by
`s.stroke` like any mark -- with the size a letter reads at, from the units. A verb,
`s.write(text, place, ...)`, only if step 2 shows the recipe's cost or its look is not
good enough, and then laying strokes through the same calls, so it touches nothing a
rebuild lays. Question W-Q4 asks what the painter needs written.
*Decided by the second painter (W-Q4, 2026-09-26)*: **a helper that returns paths, not a
verb that lays paint** -- `letter_paths(text, place, cap=, slant=, seed=)`, a
single-stroke font shipped as data, its paths placed, slanted and varied, laid with
`s.stroke` or `s.pencil` as any path is, the way `ribbon` returns a shape. It found the
font is the part a painter gets wrong: its own `G` came out a `∂`, the arc run the wrong
way round. Its measurements: capitals 32 px tall read at the size the pack's app shows a
handout; a letter costs about 1.5 strokes, so a fifty-letter note is about 75 strokes, a
quarter of a 300 budget; and letters laid along even paths read as type -- a hand wants a
slant, a baseline that drifts, pressure through each stroke, and no two letters alike,
which is what `seed=` is for.

**I2. A lamp's light on a wall** (W9). A recipe (F8's *A light's pool on a surface*), not a
verb: the painter's own fix worked, and a verb for one kind of light would be the first
verb named for a subject. **The inward scumble's rings are the finding**: both paintings
of this round laid a glow as an inward scumble and both showed its rings. Step 2 measures
the ring count at which an inward scumble reads as a target on a dark ground, and
*A passage light in the middle* says where it stops. *Step 2 (2026-09-26): there is no such
count.* Laid on a flat dark field, the Bell-Warden's glow and the second painter's first
pool read as rings at every count from 4 to 20: more rings are finer and fainter, never
gone, and `inward-comb` speaks only at the last. So *A passage light in the middle* says an
inward scumble on a dark ground shows its rings, and the recipe for a light's pool is F8's
three soft strokes of paint.

### G. Recorded and not built

- **The picture's anatomy, and the size of its give-aways** (rows 11 and 12). Arrangement
  and purpose, outside the check's line by `LESSONS.md`'s own restatement. The instruments
  are the painter's sentence, which was quoted back and answered honestly, the thumbnail,
  and the checklist's question with a size in it (F3).
- **A notice for a zone held hard inside its own silhouette.** Considered, because it is
  what made the cut-out. Not proposed: the painter held its zones hard knowingly, named the
  result itself and asked for a recipe, which is the procedure *warning is not method*
  prefers; and the `edges:` line already printed 51% to 61% at it.
- **A feather per hold.** The bench says a wider feather is speckle at any width (row 9),
  so there is nothing for it to carry.
- **Moving `pencil()`'s `smooth` default.** A2 says why.
- **A look of the drawing alone on a plain ground**, full size -- the painter's throwaway
  canvas as a flag. Not proposed until A1 has been seen; asked in question 4.
- **The rest of what 0.7.0 left open** stays where it is written: the smudge as a plan
  entry (no painter has asked), the three things left alone, and the stacked masses the
  graded rule still tells.

---

## 5. What this round undoes, and why

Five things built or decided in earlier rounds change, and a sixth is reopened as a
question by the second painter. Each is listed with the reason the change is warranted and
the guard on it. **None of them changes what a saved painting rebuilds to**, and none of
them is a moved default.

| # | What changes | Built or decided in | What it becomes | Why it is warranted | Guard |
|---|---|---|---|---|---|
| 1 | **`wet-under`'s decline** | 0.6.0, ruled 2026-09-21: as a habit rule gated on wetness it fired on 22% of the corpus's passes and 8 guide blocks, and the fact line left of it rested on a reconstruction of a take its painter overwrote | reopened as a question, and built as `into-wet` only on the four conditions in 4D | **A different gate, and -- if it comes -- new evidence.** Wetness was no gate because the corpus lays opaque paint into wet on purpose (a median wetness of `0.09` under a mark, a tenth over `0.41`); the landed shortfall of a light meant to stand off its field is what a deliberate wet blend of close colours never reaches. And a painter has now reported the damage with numbers. | built only if it fires on a real case, on about one corpus pass in twenty or fewer, and on no guide block but a failure on purpose; otherwise the decline stands, with this round's data point beside it. *Settled 2026-09-26: **the decline stands.** The painter withdrew its suggestion as written: the one light in its painting that met wet paint lost `0.01` to `0.05` to it and five times that to its size. What replaces it, a mark that lands short whatever the cause, is 4D as rewritten, and reopens nothing. Step 2 found no case left: the two versions of the subject's pass that laid the head's plane in the pass with the body under it read it within `0.004` of the same versions laid on a dried canvas.* |
| 2 | **What a planned place reads**: its mean, in `plan:`, `lightest:` and `compare()` against a value plan | 0.6.0's plan object, and `compare()` against a value plan, whose reading the plan's lines share | its median, or whichever reading step 2 and the painter choose. *The painter chose the median (question 5).* | the mean made a detail inside the plan's own lightest plane into a false miss (`-0.14`) on the one line a painter relies on most, and the only other painting with a plan keeps every verdict under the change | every number those lines print moves a little, so it is named in `CHANGELOG.md`; output only, nothing rebuilds differently; replayed over both plans pass by pass before it lands |
| 3 | **The `values:` line judging every picture against the box's middle** | 0.6.0 -- the standing lines | judged against the key a plan declares, where it declares one | *no clear light* printed twenty-five times at a picture declared low-key on purpose -- the stack-of-bars history, which 0.6.0 answered for bars with `bands=` | a declaration, not a switch: the line still measures and says when the picture leaves its key; with no key declared, nothing changes |
| 4 | **The weight of `PAINTER.md` -- *watch*, and nothing cut on one painter's word** | 0.7.0's G5, the handover painter's own ruling; and before it the tenth round's *one home per rule* | anecdotes and commentary on the documents moved to `LESSONS.md` and `CALIBRATION.md`; the budget lowered to the new size | the seventh painter to call the corpus long, and **the first to say which text** -- none of it a rule -- **and which text worked**; the tenth round had already found *the stories were most of the words, and they did not do what the corpus believed*; and 45 words under its budget, the file cannot take this round's exercise and clauses without it | a move, not a cut: every sentence lands in a file that keeps it; the painter says which anecdotes persuaded, and those stay; `check_guide_overlap.py` and the budget test hold the result; and it is a hypothesis until the next fresh session paints against it |
| 5 | **How a guide looks** | 0.5.0 -- `guide()`, drawn *thin, dark, the way a pencil line reads* | a graphite core on a light casing, its note in a box | over a dark picture the overlay is invisible -- ~~69%~~ *65%* of its pixels step under `0.05` over the finished canvas, *96% over the room the second drawing went on* -- which defeats the one thing it exists for, a drawing that paint cannot bury | the view only; `sketch=False` still hides it; the test that a guide survives the paint and stays out of the picture still holds. *And the second painter never drew on its painting at all, working round it from the first painter's memory -- the workaround the overlay made necessary, carried to a second picture.* |
| 6 | **A repainted-passage count, declined** | 0.7.0's round, *What the check cannot see*: the headland took four passes and so did the tower, and the log cannot tell a passage failing from a subject being built | reopened as a question (4H4): measured over the corpus, and built as a fact with its number only if a count separates a failing passage from a subject built in as many passes | a second painter asks for it by name, with a case -- its fist was laid over by five passes -- and says it broke the rule it would enforce *with the rule in front of me*, which is `LESSONS.md`'s *warning is not method* seen from the painter's side | the count must separate the corpus's failing passages -- the fist, the Bell-Warden's head, the handover's headland -- from its subjects; if it does not, the decline stands, with this case beside it. *Settled by step 2, 2026-09-26: **the decline stands.** Counted over the corpus and both paintings' filed rehearsals, masses laid over the painter's own earlier marks find the fist and the night pool's water, and speak on the Bell-Warden's creature and the second painter's figure as they were being built; the Bell-Warden's head they see only after the rule had already sent the painter back twice, and the handover's headland not at all (4H4).* |

**What stays as it was, on purpose**, because each would be the obvious thing to undo:
0.7.0's default feather of `0.002`, since a wider one is speckle; one `feather=` for every
hold of a call, since a feather per hold would carry nothing; `pencil()`'s spline for a
list of points (A2); `edge="hard"` and `clip=` as they compose, which the painter called
what made its lighting possible; and the palette's *no black*, which the corpus has never
once asked past (E3).

---

## 6. Questions

**For the painter**, by the owner's ruling. Each goes with its evidence; the ones that
compare candidates go as the last round's did -- under letters, blind, and the key after.

| # | Question | Evidence and cost | What the answer changes |
|---|---|---|---|
| 1 | ~~What did you read before the first stroke -- which files, whole or in part? Did you use `--count`, `cost()` or `cost_line()`, `--alternatives`, `explain` or `diagnose`?~~ **Answered from the painting session's transcript, not asked.** | `PAINTER.md` is 6,655 of the 20,000 words; the file cannot tell a rehearsal of versions from a rehearsal of a pass. *Measured: the README's first 400 lines, `PAINTER.md` to line 700 of 754, `REFERENCE.md` to line 520 of 723, twelve of `RECIPES.md`'s twenty-one entries -- 21,262 words of the documents; none of the tools named.* | the record, and F1's target: what a painter who starts at the card actually reads |
| 2 | ~~The highlights at `0.52` instead of `0.64`: which marks, measured how, and in which version of which pass? Can you rebuild that version, as the handover painter rebuilt its misfires?~~ **Answered from the transcript**; what still goes is its follow-up: *is there any other place where you saw a light land dull in wet paint?* | committed, the details pass lands the same with and without its `dry()` calls, and `0.52` is the plan line's mean for the head's top with the eye in it; two rehearsals of the subject pass read it at `0.56` and `0.54`. *The session: the details pass's second rehearsal read `0.52`, the two `dry()`s went in, the third read `0.52`, and the painter put it down to the eye.* | whether D has a case to be built on |
| 3 | ~~Can you send, or rebuild, the prelude and passes of the cat and the piebald versions?~~ **Answered from the transcript**: every version is recovered in `versions/`, each re-run to the report it printed. | they are the real test cases for the thumbnail and for both recipes; ~~without them step 2 reconstructs from the first drawing look~~ | A3's default size; the demos |
| 4 | The thumbnail: masses as `{place: value or colour}` in the order they would be painted, and the plan's own places with no argument -- right? Which size reads, shown blind at four? With the guides drawn over it, or without? And with guides that read on any ground, would you still have wanted a look of the drawing alone on a plain ground, full size? | A3 | A3's signature and default; whether 4G's drawing-only look is built |
| 5 | What should a place read: its median, one number for `plan:` and `lightest:`; or its brightest part for `lightest:` alone, with the mean kept for `plan:`? And should a place split between two values say so? | row 5b; the handover's verdicts do not move under any of them | E2 |
| 6 | What should `key="low"` hold you to: the top twentieth of the picture staying under the box's middle; a top you name, `key=("low", 0.40)`; or only the clusters inside the key? | row 5a | E1's line |
| 7 | Which anecdotes persuaded you -- which should stay beside their rule -- and did the card alone carry what you needed to start? | row 6 | F1's list of what stays |
| 8 | The dearest-calls line: after every pass, or only rehearsed and counted ones? By script line, by function, or both? Three calls or four? | row 3 | C's format |
| 9 | After step 2, blind: the terminator candidates side by side -- which reads as a form turning in stone? | row 9 | B1's recipe and B3's sentence |
| 10 | Your cast shadow wanted `0.13`, which burnt umber alone reaches (`0.128`). Had the box held a darker dark, would you have used it -- and would the room's darks, planned between `0.15` and `0.21`, have spread further apart? After step 2, blind: this picture's darks re-laid with a near-black under the floor, beside the painting. | row 13 | whether E3's black is ever built |

**Answered by the painter, 2026-09-26**, in
[`answers.md`](paintings/Claude/bell_warden/answers.md), measured on its own file and
re-measured here: question 2's follow-up -- no other case; the only light that met wet
paint lost a sixth of its shortfall to it, and **it withdraws `into-wet` as written** (4D,
rewritten); 5 -- **the median**, and a split place said from its own median (E2); 6 --
**(1)**, and under a key the clusters printed but not yet judged (E1); 7 -- **keep three
anecdotes, drop two and *every painter so far*, and give the card `clip=` and `at_value`**
(F1); 8 -- **after every pass, function and line, up to four calls until three quarters,
and the strokes that landed nothing** (C). It also found, measuring, that the ember did
not land either and that twelve paid strokes landed nothing (row 12; D). *Questions 4, 9
and 10 went to it after step 2, 2026-09-26, as a blind package with step 2's sheets,
[`questions-step2/`](paintings/Claude/bell_warden/questions-step2/README.md) -- 4 split in
four (the size, blind; the guide candidates, blind; the signature; the drawing over the
thumbnail and the drawing alone), 9 and 10 in two each -- with the follow-up below as 5f,
and one question the bench raised, D: whether the post-pass check should name the marks
a pass laid that landed nothing.* *One follow-up goes to it with the second batch*: E4
revisits its answer to question 5 for a light whose lit part is under a tenth of its place
-- would it keep the median for `lightest:` there too?

**For the second painter** -- *added 2026-09-26*, by the same ruling, through the owner,
as [`questions-step1.md`](paintings/Claude/wenna_brask/questions-step1.md) beside its
painting.

| # | Question | Evidence | What the answer changes |
|---|---|---|---|
| W-Q1 | A pixel helper, `s.px(x, y)` beside the fractions, or `Session(units="px")` for a whole script -- which would you have used, and would the helper have replaced your `P()`? | W1 | A5's form |
| W-Q2 | Your `T()` scaled the first head by `1.3` about a point: would a group of shapes, moved and scaled about a point you name, have done it -- and what else did you need to move together? | W1 | A5's group |
| W-Q3 | When a finding names its marks, what reads: the script line, the `note`, or the log index -- and would the line have found the mouth's four marks for you? | W3 | H1's form |
| W-Q4 | Lettering: what do the pictures you listed need written -- a word, a line, a page -- at what size on the canvas, and in a hand or in type? | W5 | whether I1 is a recipe or a verb |
| W-Q5 | Your lantern read `0.49` against `0.76` because its iron is most of its place. Should `lightest:` read a named light by its brightest part while `plan:` reads the place as a whole -- or would you rather have planned the panes as a place of their own? | W4 | E4 |
| W-Q6 | A notice for a place laid over again and again: counted in passes or in marks, after how many -- and would it have stopped you at the fist? | W8 | whether H4 is ever built |
| W-Q7 | Would one clause saying the example's budget of `300` is the example's, not a rule, have changed yours? And which calls did your painting actually lean on -- your *twenty*? | W15, W16 | F9, and F1's line for the card |

**Answered by the second painter, 2026-09-26**, in
[`answers.md`](paintings/Claude/wenna_brask/answers.md), measured with the three scripts
in its `probes/` and re-measured here: **W-Q1** -- the helper, which would have replaced
its `P()` in all of about 360 places, but **`s.px(r)` as a fraction of the long side is a
size's unit, not a shape's radius**: `blob(p, s.px(25), s.px(25))` comes out an oval on a
canvas that is not square, so the helper says so in its name, or shapes take pixels
themselves (`s.circle(p, px=25)`) (A5); **W-Q2** -- yes, its `T()` is exactly one scale by
`1.3` about a point, and the time went elsewhere: an edge shared with the face typed by
hand, where a slice of `.closed` would have taken it (A5, B4); **W-Q3** -- **the script
line with its function**, and the log's colour named by its palette slot (H1); **W-Q4** --
two pictures need writing, a note of about fifty letters in a hand and a sketch map's
labels; capitals 32 px tall read at the size the pack's app shows a handout, at about 1.5
strokes a letter; the probe's letters read as type, and **the recipe needs its font as
data** -- a helper that returns a single-stroke font's paths placed, slanted and varied,
`letter_paths(text, place, cap=, slant=, seed=)`, laid by `s.stroke` or `s.pencil` (I1);
**W-Q5** -- **neither reading would have helped, because its plan was wrong**: the face is
the lightest thing in the picture by every reading and should be, and it would rather have
planned the panes at the value it painted them and planned the face; if `lightest:` reads a
light by its brightest part, **the 95th percentile inside the place, printed beside the
whole** (E4); **W-Q6** -- count masses laid over the painter's own earlier marks,
rehearsals included, and speak at the second; on its painting that singles out the fist,
but it would have spoken exactly when the rule did, so **build it only if the corpus
separates** (H4); **W-Q7** -- the clause is still worth its line, though its budget never
bound, and **its twenty calls**, counted from its scripts (F1, F9). Its answers also found
the flour that never landed (W17) and withdrew three of its own sentences: the rule broken
on the fist, the fist too large, and *450 would have suited it*.

**For the owner**, on the second painting -- **answered 2026-09-26, all four the
recommended option**: O4, filed as the first was, with the pack's details left out -- the
painter's paragraph placing her in the pack's list and its story, the sentence naming the
pack beside the signature, the catalogue entry, two lines of the verdict that name the
pack's other pictures, and one phrase of the prelude's docstring; O5, its verdict folded
into this round rather than planned as the next; O6, the first painter's answers into step
1's PR and this painting in a second PR on top of it; O7, `verdict.md` only, nothing
posted.

**For the owner.**

| # | Question | Why it is the owner's |
|---|---|---|
| O1 | Which model painted it, and at what effort? | the handover's was read off its session's metadata, and every section of `PAINTINGS.md` says it. **Answered from the metadata: `claude-opus-5-5` at max effort, on every turn.** |
| O2 | Is the painting filed here -- scripts, looks, and the notes' account of the pack it was made for -- or filed with the pack's details left out, or not at all? | it was made for another of your projects; step 1 waits on it. **Answered 2026-09-26: filed, with the pack's details left out** -- the notes' paragraph naming the pack and where its copy goes, its catalogue entry, and the WebP copy. |
| O3 | The painter asked whether to write its report up in the painting's folder or as issues here, posted under your account. This plan files it as `verdict.md` in the painting's folder, as every round's has been, and posts nothing. | posting in public is yours to decide. **Answered 2026-09-26: `verdict.md` only; nothing is posted.** And the painter's questions go through the owner, who pastes them into the painting session: questions 5 to 8 with step 1 ([`questions-step1.md`](paintings/Claude/bell_warden/questions-step1.md)), 4, 9 and 10 after step 2, as a blind package. |

---

## 7. Order of work

One round, cut as 0.8.0, in PRs that each stand alone: *record*, then *measure*, then *act
and cut*.

1. **Record** (after O2). `paintings/Claude/bell_warden/`: the prelude and the seven
   passes, the notes, `verdict.md` verbatim, the painting and its film, and `evidence/` --
   the drawing look with its guides lost, the drawing check as a pot and again with its
   corners, the cat, the piebald and the arch -- under names `.gitignore` does not exclude.
   A section in `PAINTINGS.md`, with the order its passes rebuild in; an entry in
   `probe_cohort_session.py`'s corpus, laid in that order; this plan; the round open in
   `SUGGESTIONS.md`, M/O/R per row, with rows 4, 9 and 13 struck where they changed shape; a
   stub of *The bell-warden's round* in `CALIBRATION.md`; this painting's nouns in the
   guide's grep list. Then the questions go to the painter. *As built: also
   `reports.txt` (the session file is not committed, so its 27 saved reports are written
   out), `ex/exercises.py`, `versions/` (the first drawing, the five subject-pass versions
   and three details-pass versions, recovered from the transcript and re-run to their
   reports), and `paintings/**/looks/` in `.gitignore`, where the passes write their looks.
   The guide's grep list does not exist -- `LESSONS.md` describes the grep as a check run
   by hand -- so the nouns are recorded in the painting's notes, and the grep was run: one
   old sentence, where `RECIPES.md` calls a crescent's two points its horns.* *Then, the
   same day: the first painter's answers filed and re-measured in the same PR; and the
   second painting, `paintings/Claude/wenna_brask/`, filed the same way in a PR of its own
   on top of it, with its verdict folded into this plan (3b, and the rows marked added).*
2. **Measure.** `scripts/probe_bell_session.py`, in the pattern of the probes beside it:
   section 3 again from the rebuild, and where a round dab stops landing paint -- the
   spark's `0.0028` landed two pixels (`--claims`); the guide candidates' contrast over the
   corpus (`--guides`); the thumbnails (`--thumbnail`); the terminator candidates at two
   sizes (`--terminator`); the place readings over both plans and over synthetic places
   (`--place`); the `values:` line under each key over the corpus's own low- and high-key
   pictures (`--key`); the landed shortfall of every hand-laid mark over the corpus, and
   ~~the painter's rebuilt pass if it comes~~ *the two recovered subject-pass versions
   that read the head's top at `0.56` and `0.54`* (~~`--wet`~~ *`--short`, after D was
   rewritten: every hand-laid mark's shortfall and the cause the engine could name, and how
   many corpus strokes are charged and land nothing*); the dearest line over every corpus
   pass (`--cost`); and the darks of the low-key pictures that sit on the floor, re-laid
   with a supplied near-black and set beside themselves (`--floor`). *For the second
   verdict: the lightest place of every plan read by its median and upper percentiles, and
   how often a named light is under a twentieth of the canvas (`--lamp`, E4); the passes
   that lay marks over one place, failing passages against subjects (`--repaint`, H4); the
   prelude names the corpus's passes rebind (`--rebind`, H2); B1's and B4's structures on
   the second painter's face (`--terminator`, widened); the inward scumble's ring count on
   a dark ground (`--rings`, I2); and the corpus's own pixel helpers and hand-scaled groups
   (`--units`, A5).* Numbers into `CALIBRATION.md`, sheets under `out/bell/`. **Its output
   decides which rows of A to E, H and I are built as written.** *As built: every flag
   above, and a corpus replay shared by `--cost`, `--short`, `--key`, `--place`, `--lamp`
   and `--repaint` -- the corpus probe's harness with each call's site, what each hand-laid
   mark landed at and a footprint of what each call painted, kept in `out/bell/corpus.pkl`
   (half an hour, once). `--thumbnail` also answers A4's width-per-point question and
   `--units` F7's, off the masks; `--short` also measures where marks stop landing and runs
   the candidate over the guide's blocks. The painter's questions 4, 9 and 10 went with the
   sheets as [`questions-step2/`](paintings/Claude/bell_warden/questions-step2/README.md),
   whose `make_package.py` lays the sheets out under their letters. See
   [`NOTES-step2.md`](NOTES-step2.md).*
3. **A1 and A2**: guides that read on any ground; a shape handed to `guide()` and
   `pencil()`. Small, certain, one PR. *With A5 -- `s.px()` and a group -- after W-Q1 and
   W-Q2.*
4. **C**: the dearest calls. *With H1, which names a finding's marks from the same record
   of each call's site, and H2 and H3, which are small.*
5. **E**: the key and the place reading, after questions 5 and 6, and `at_value`'s error at
   the floor. *And E4, after W-Q5 and the first painter's follow-up.*
6. **A3**: the thumbnail, after question 4, with its server tool.
7. **A4 and B**: the two recipes with their demos, the terminator helper, exercise 10,
   `union()` in `PAINTING.md`, and `feather=` said for what it is -- with `ribbon()`'s
   widths only if the recipe's bench needs them. *And B1 scoped, B4's recipe for a form
   turned toward the light, F8's two recipes, and I1 and I2 as recipes -- a lettering
   verb only if step 2 and W-Q4 say the recipe will not do.*
8. **D**: ~~`into-wet`, on its four conditions -- or the decline recorded with its new data
   point~~ *as rewritten: a mark that lands short, and the strokes that land nothing, on the
   same four conditions. And H4, only if step 2's count separates a failing passage from a
   subject built in as many passes.*
9. **F**: `PAINTER.md` moved and its budget lowered, `REFERENCE.md`'s tables, the claims
   that stopped being true, the checklist's size, *F5 to F9,* and the record -- last, because it moves
   text that every earlier step touched. `check_guide_blocks.py` green,
   `check_guide_overlap.py` clean, the no-nouns grep run, and every new example read end to
   end.
10. **Cut 0.8.0**: the version in `pyproject.toml`, `src/easel/__init__.py` and both
    entries of `server.json`; `CHANGELOG.md`'s entry without the claim; the tag on the
    owner's word; then the claim, which takes this file and the step notes out of the
    repository and leaves what survives of them in `SUGGESTIONS.md`.

---

## 8. Risks

| Risk | Guard |
|---|---|
| The haloed guide shouts over the picture in every look. | Benched on a mid-grey canvas as well as the dark and light ones, and looked at; `sketch=False` takes it off, as today. |
| The thumbnail is a verb nobody reaches for, as `diagnose` has been. | One clause at the card's step 1, the exercise that uses it, and the silhouette recipe that ends in it -- and the next fresh session is asked whether it was used. |
| The median hides a place that straddles two masses. | Step 2 builds such places on purpose, and the split clause is the candidate answer. |
| `key=` becomes the switch `LESSONS.md` warns about. | The line under a key still measures, and says when the key is left: declaring one buys a question, not silence. |
| `into-wet` is `wet-under` again -- noisy, and firing on the guide's own wet-into-wet. | Measured on the damage, not the wetness; the four conditions; the corpus and the guide blocks decide. |
| The lighter `PAINTER.md` loses what persuaded. | The painter says what persuaded; one sentence of evidence stays with each rule; nothing is deleted; and it is a hypothesis with its test named. |
| A recipe leaks a subject -- this painting's or a reference's. | The no-nouns grep with this painting's nouns added, and every example read end to end. |
| The silhouette recipe's code is copied as the silhouette. | Its example is abstract parts, not an animal, and its *Goes wrong as* shows a copied arrangement failing. |
| The dearest line is noise on a pass of hand-laid marks. | Said only when a call cost more than one stroke. |
| The decisions are one painter's. | Where an answer meets the corpus -- the guide blocks, the other plan, the goldens -- the corpus wins; where the painter has no evidence, the bench decides. |
| The second painter's agreement is counted as a second opinion, when it is the first painter's lesson. | Every row of 3b says where it repeats the first verdict; only its contradiction (W13) and its own measurements weigh on their own. |
| The round grows with every picture the pack still wants. | *Proposed, and the owner's to confirm*: this round takes the two verdicts it has; a third painting against 0.7.0 is filed and recorded, and planned on after 0.8.0 is cut. |
| A lettering verb pulls the engine toward drawing type. | A recipe first, laying letters as strokes through the calls a painter already has; a verb only if the recipe is too dear, and then through the same calls. |

---

## 9. File map: what will change

| File | Change |
|---|---|
| `src/easel/look.py` | the guide's casing and boxed note; the thumbnail's render |
| `src/easel/session.py` | `thumbnail()`; `guide()` and `pencil()` taking a shape; the call tally in `_one_call`; the place reading; `into-wet`, if built |
| `src/easel/plan.py`, `checklist.py`, `measure.py` | `key=`; the median reading; `values_line` under a key; `compare_plan` reading a place as the plan does |
| `src/easel/palette.py` | `at_value`'s error at the floor; the floor said one way in its docstrings |
| `src/easel/regions.py` | the terminator helper; `ribbon()`'s widths, if needed |
| `src/easel/cli.py`, `mcp_server.py` | the dearest line; `easel plan --key`; the prelude scaffold; `key`, `thumbnail`, and places for `guide` and `pencil` through the server |
| `src/easel/notices.py`, `docs.py` | `into-wet`'s code and passage, if built; `FRONT_PAGE_WORDS` lowered |
| `scripts/probe_bell_session.py` (new), `probe_cohort_session.py`, `check_guide_blocks.py` | the benches; the corpus entry, in its rebuild order (a `Painting.order` field, since a pass runs twice); exercise 4 marked as saying `into-wet`, if built |
| `tests/test_requests.py`, `test_reference.py`, `test_guide.py`, `test_notices.py`, `test_mcp.py` | one test per row, named for the finding; the budget; the reference rows |
| `paintings/Claude/bell_warden/` | filed in step 1, with `reports.txt`, `versions/` and `evidence/`; its answers filed beside it as they come; `questions-step2/`, step 2's blind package and its builder |
| `paintings/Claude/wenna_brask/` | filed the same way, in a PR on top of step 1's; its answers filed beside it as they come |
| `src/easel/regions.py`, `session.py`, `cli.py`, `checklist.py` | *for the second verdict*: `s.px()` and a group (A5); a finding's marks (H1); the prelude-name fact (H2); `--scale` read as a factor under `1` (H3); `lightest:` read by the named light's brightest part (E4) |
| `.gitignore` | `paintings/**/looks/`, where this painting's passes write their looks (step 1) |
| `PAINTER.md`, `RECIPES.md`, `PAINTING.md`, `REFERENCE.md` | F1 to F3; the two recipes and exercise 10; `union()`; `feather=` said for what it is; the tables |
| `CALIBRATION.md`, `LESSONS.md`, `SUGGESTIONS.md`, `PAINTINGS.md`, `CHANGELOG.md`, `README.md`, `llms.txt` | the round's numbers, the moved text, the record, and the cut |
