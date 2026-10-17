# Plan: act on Uktarl's Room's verdict on 0.8.0, and cut 0.9.0

_To understand this, start by reading this file's status line and section 3. Then read
[`LESSONS.md`](LESSONS.md), whose rules bind every row below, and
[`paintings/Claude/uktarl_krannoc/verdict.md`](paintings/Claude/uktarl_krannoc/verdict.md)
with the [`NOTES.md`](paintings/Claude/uktarl_krannoc/NOTES.md) beside it. Most of the
engine work lands in four places in `src/easel/session.py`: `Session._clip_cover` and
`_as_outlines` (the clip mask, and what a record carries of it), `_pass_findings` (the
disc, bars and graded rules), `_block_in_paths` with `_check_default_direction` (what a
mass is charged), and, in `checklist.py`, `values_line` (the key).
[`PLAN-0.8.0.md`](https://github.com/Gemberkoekje/EaselAPI/blob/v0.8.0/PLAN-0.8.0.md), as
tagged, is the round before this one._

**Status: written 2026-10-01 against `main` at `dcdfc94`, whose `src/` is `v0.8.0`'s.
Step 1 is done in this PR: the painting is filed, the verdict is checked (section 3), the
round is open at the top of `SUGGESTIONS.md`, and the first questions for the painter are
written (`paintings/Claude/uktarl_krannoc/questions-step1.md`). Nothing under `src/`
changes. 2026-10-10: the painter's answers are filed (section 6), and **step 2 is done**
on branch `measure-uktarls-room`: `scripts/probe_uktarl_session.py` benched every
candidate (`CALIBRATION.md`, the round's *Step 2*; `NOTES-step2.md`), and batch 2 is
written (`paintings/Claude/uktarl_krannoc/questions-step2/`). 2026-10-11: batch 2 is
answered (`answers-step2.md`, section 6's *Answered after the bench*), and every question
of the first painter has its answer. Later on 2026-10-11 **a second painter joined the
round**: The Curator, nine pieces of game art against 0.8.0, filed with its verdict checked
(section 3b), four workstreams added (K to N) and its questions written
(`paintings/Claude/the_curator/questions-step1.md`; `NOTES-step1b.md`). Next: its answers,
then step 2b; steps 3 to 9 go on meanwhile where they do not touch K to N. Its answers are
filed the same day (section 6), and add workstream O. **Step 2b is done** on branch
`claude/step-2b-continuation-bln1h2`: `scripts/probe_curator_session.py` benched K, L1, M,
N and O3 (`CALIBRATION.md`, the round's *Step 2b*; `NOTES-step2b.md`), and section 6 has
*After the bench (step 2b)*. **Step 3 is done** on branch `ccr-6544d06d-6o24n7`: `clip_out=`
on every verb that takes `clip=`, cut on the line, in a record 0.8.0 refuses;
`difference()` for places that are read; the rehearsal's look flags (`NOTES-step3.md`).
**Step 4 is done** on branch `ccr-65d1dbee-863bmi`: `soft=` on every verb that takes
`clip=`, B1 as the painter chose it, per hold and per stretch, in a record 0.8.0 refuses
(`NOTES-step4.md`). **Step 5 is done** on branch `ccr-41356652-bm55is`: the three rules
as they are; `habits={"disc": {place: reason}}` per place; the pass rule leaving the
signature out; a standing line printed only when it changed from the painting as
committed (`NOTES-step5.md`). **Step 6 is done** on branch `ccr-9c669476-nor0aj`:
`.rotated(deg, about=, aspect=)` on every shape and group, turned in pixels, `aspect=`
required; `s.frame()` with `.at()`, `.polygon()` and `.arc()`; `shares=` and its line, a
part named in the note. A session in pixels throughout (Q5) is not built, on the owner's
word (`NOTES-step6.md`). **Step 7 is done** on branch `ccr-52e9ee7b-rddn15`:
`direction-given`, one direction given and both prices, at the call and from `cost()`;
the low key said rule first on the card and in `REFERENCE.md`'s row; with no key, the
`values:` line naming a planned light that stands clear beside *no clear light*. The
notice for passes in pieces (G2 (a)) was built, spoke on three recipes, and is held, on
the owner's word: asked back (`questions-step7/`; `NOTES-step7.md`). 4N's `cut=` waits
for the second painter's batch 2.**

This plan is written the way its own documentation item asks: the rule or the finding
first, then the number, then the history if it is needed.

---

## 1. What this round is

**Two painters against 0.8.0; the second joined on 2026-10-11, and is in section 3b.**

**The first, painting against 0.8.0 the day it shipped.** `claude-opus-5-5`, at max
effort, in a session of the owner's own tabletop-campaign project, was asked to *look up
what the rooms of Uktarl Krannoc look like* and paint *an appropriate painting* with 0.8.0.
It painted four bandits in vampire costume at a card table, their leader standing inside
a carved sunburst, in 410 of 450 strokes, as a handout for the table. Then the owner
asked for an honest opinion on the tool, the documentation and the painting, with a fix
for every negative point. Before answering, the painter checked the installed package
for what it already did. Filed as `paintings/Claude/uktarl_krannoc/`.

**It is not a fresh painter.** It began with its own memory note from the project's
earlier paintings, and read the Bell-Warden's and Wenna Brask's notes between `PAINTER.md`
and the recipes. It read `PAINTER.md`, `RECIPES.md` and `REFERENCE.md` whole, and 0.8.0's
changelog entry from the repository's checkout: 33,596 words of the documents before its
first exercise. It ran
`easel demo mistakes` and all ten exercises.

**It is the run 0.8.0's round asked for.** *What the round left open* in `SUGGESTIONS.md`
named what the next painting should look for first. The answers, from its session:

| 0.8.0 asked | this painter |
|---|---|
| does a painter reach for the thumbnail? | yes, before any paint, as a script calling `s.thumbnail()`; never as `easel run --thumbnail`. It caught both drawing faults, and the verdict calls it the most useful addition |
| `--alternatives` and `--count`? | never run |
| does the card alone start a painting? | no: it read the three files whole |
| does `key=` stay a declaration that buys a question? | never declared, though the line it asks for is what `key="low"` says (row 8) |
| is `landed nothing:` read or skimmed? | read: it filtered every report for it from the mountain on, and its notes name the one pass it printed |
| the join on skin? | laid along all three faces' terminators; its verdict calls the faces masks, and it was not asked about the join |
| lettering? | none |

**The headline is the edge.** The verdict says the picture *reads as cut paper*: 43 of its
44 masses are held hard, 59% of its edges are under 2.5 px, and two edges are lost in the
whole picture. Holding an edge costs nothing and losing one costs a smudge per stretch. The
note the owner sent with the verdict names this the main item: *change the price and the
pictures change.* It is *Warning is not method* for the fourth painter running (the
lighthouse handover, the Bell-Warden, Wenna Brask, this one). The `edges:` line printed
59% to 70% after every pass, and the engine offers no held edge that is not hard.

**The second is the check itself.** The verdict says the habit warnings misfire *often
enough that I stopped reading them*, and its commands show it. From the body's second
rehearsal on, 29 of its 30 `easel run`s filtered the output down to the lines it named.
Of the 28 marks the closing check called *one disc printed over and over*, 20 were the
features of three faces.

**Scope.** Eight engine items, four documentation items, and the painting's own. The
release is **0.9.0**: new arguments and shape builders, three rules narrowed and a habit
that can be declared, a new standing line, and documents cut. No planned fix changes what
a rebuild lays. Any fix that does gets a row in `notices.REBUILDS` and its sentence under
the version, as `LESSONS.md` requires.

---

## 2. The rules this plan works under

From `LESSONS.md` and the last three rounds; every row below is held to them.

1. **Measure the condition before writing the rule.** Every engine candidate is built only
   on a bench rebuilt as a probe script, at a painting's size, over the corpus where it is
   a rule, and looked at.
2. **Ask what the rule says to a painter doing the right thing.** A rule narrowed for this
   painter's misfires keeps the corpus's true positives, or it is not narrowed. Every guide
   block stays notice-clean and every demo fails as it says.
3. **A default beats a warning, and neither is a method.** Where a line was printed and
   changed nothing, the answer is in the engine or a recipe, not a louder line.
4. **Decisions are the painter's.** The owner's ruling since 0.7.0: the tool is for
   painters, so where a row turns on how the tool should behave, the painter chooses,
   from evidence, through the owner.
5. **Nothing new touches the log index or the random stream**, and **a build that does not
   know a new kind of record refuses it rather than replaying it wrongly**. (0.8.0's
   `_brush_from_params` drops keys it does not know, so a new key alone would replay in
   0.8.0 as if it were absent.)
6. **A round that answers *it's long* must leave the reading path shorter, measured** —
   `LESSONS.md`, *One home per rule*, last paragraph. Adding recipes is paid for by cuts
   in the same round, counted the way this painter read.
7. **Rule first, then the number, then the history**, in every document row this round
   writes. This is the painter's second documentation item, applied from the start.
8. **Each landed step leaves a `NOTES-step<N>.md`**, and the next step starts by reading
   the newest.

---

## 3. The verdict, checked

**Kind** is assigned here: **M** measured by the painter, **O** observed, **R** reasoned.
Every *what checking found* was measured on 2026-10-01 on this machine, on the checkout at
`dcdfc94` (its engine is `v0.8.0`'s), from the painter's own session file, scripts and
transcript. The passes rebuild the painter's log exactly, in their numbering: 429 records,
410 spent, and the export to the pixel.

### The tool

| # | What the painter said | Kind | What checking found | Goes to |
|---|---|---|---|---|
| 1 | **You can't paint outside a shape.** `clip=` takes a place or the overlap of several; no exclusion, no `difference()`. To light the wall around Uktarl it typed three polygons sharing his outline, and one left a hard seam | O | **Confirmed.** `clip=` takes one place or a list, and a list multiplies the masks: an intersection. `union()` exists; nothing excludes. The three regions are 44 typed points, about 30 of them retyped from his collar, body and cape. The first pair ended at x=290 and x=812, inside the reach of a soft stroke 246 px wide, and drew a vertical seam on each side. That version is recovered as `versions/p08_v2_seam.py`; it reprints its saved report and redraws the seam (`evidence/backlight_seam.png`). **Also found:** `intersection(a, b)` as a clip exists, but not as a shape; and a new key on a record would be dropped by 0.8.0's replay, so the record needs a form an older build refuses | **4A** |
| 2 | **Edges are hard or ragged, never soft.** `feather=` breaks an edge but doesn't soften it; losing one costs a smudge per tenth of the canvas, so `edge="hard"` is the easy path. 59% crisp edges; *cut paper* | M | **Confirmed.** 43 of 44 masses are held, all but the wall, every one at the default feather `0.002`; 81 of 181 hand-laid marks are clipped. `edges:` read 70% under 2.5 px after the wall and 59% at the end. Two edges were lost, one smudge each, in the last pass. `RECIPES.md` says a smudge loses a stretch under a tenth of the canvas, and past that, paint across. **History:** 0.7.0 benched a 2-px Gaussian feather on every hold (64% to 9% hard), which read as blur, not paint, and its painter chose the broken edge from four candidates, blind. 0.8.0 measured `feather=` wider than the default as fur. **What is new:** a softness chosen per call, for the edges a painter means to lose, not a default | **4B** |
| 3a | **"One disc printed" flagged 28 marks, 21 of them the eyes, brows and mouths of three faces** | M | **Confirmed, 20 and 1.** The closing check after the light-edges pass counted 28 marks in five places, and named three. Those three are the three faces: Uktarl's 10 (eyes, the candle's catch-lights, brows, nose, mouth, fangs), the doppelganger's 6 (an ear's light, eyes, nose, mouth, a tooth), and the left bandit's 4 (a neck's shade, eyes, lips) plus one ridge stroke on the relief 56 px from her eye, from the mountain's pass. The other 7 are the candle (holder, flame, its core, a ring) and three relief marks. Every face mark is a stroke 0.8 to 3.8 widths long, mostly with a pressure list, or a dab for a catch-light. Per pass, the line fired on 7 of the 16 painted passes | **4C** |
| 3b | **"Graded passage comes back as bars" fired on a hood and the face beside it** | O | **Confirmed.** The near bandit's 10 marks are the hood's 6 passes (one colour), 3 passes of the face's profile (one colour) and a dark stroke along their edge: three masses at three values, not one passage. The rule's *three distinct colours* is met by three calls, two of them masses | **4C** |
| 3c | **"Stack of bars" fired twice, in a picture crossed by radial rays** | O | **Confirmed, and wider.** On what it read: the mountain with its seven cave mouths, and the floor's two halves with the tub. On the committed passes it also fired on the left bandit's five masses and on two laps at opposite ends of the table, 400 px apart. The rule reads angles only; it never asks whether the marks touch | **4C** |
| 4 | **Rehearsal looks can't be cropped or cleaned**: `easel run --rehearse` has none of `easel look`'s `--region`, `--no-sketch`, `--no-marks`, `--scale`; a label sat on the 48-px face | M | **Confirmed.** 13 of its 26 rehearsals carried one of seven look scripts written for this. **And the label is two labels:** the guide's note `Uktarl`, and a landmark `sun` left by the first drawing pass. The pass that replaced it no longer marks it, and its `s.unguide()` clears guides, not landmarks (`evidence/labels_on_the_face.png`). The rebuild from the final scripts has no `sun` | **4D** |
| 5 | **No rotation and no local frame**; the same helper written three times, a head in its own radii, tilted and placed | O | **Confirmed.** `Polygon` has `scaled`, `shifted`, `inset` and `smooth`, and `Group` has `shifted` and `scaled`; nothing rotates. `ellipse()` and `blob()` take `rotate=`. The prelude defines `hp()`, `dp()` and `ah()` (the same four lines with other constants) and an outline function for each. Every eye, mouth, terminator and lit plane of the three heads goes through them | **4E** |
| 6 | **The budget is planned as one number.** By the time the other three figures were begun, Uktarl had 102 marks; the last figure got 22 | M | **Confirmed.** `subject_share=` is one share, read on the marks noted `"subject"`, here Uktarl alone. He had 102 marks after his head's pass; then the doppelganger 43, the left bandit 36, the near bandit 22. The `subject:` line read 47% and 48% against 30% from his head on, and the painter saw it on six rehearsals. But that is a share of the marks laid so far, not of the budget: 102 is 23% of 450 | **4F** |
| 7 | **Concave shapes are priced by the whole strip their passes sweep.** The V collar 43 strokes, about 10 as two flaps; the first mountain pass 129 | M | **The collar is confirmed, and the mountain is something else.** The V was two calls, black and red, 22 + 21. At any single direction the black V costs 17 to 22 and the red 19 to 26. As two flaps laid along their own lengths it costs 3 + 4, and 9 with the two edge strokes. 8 of the black V's 14 passes come back in two pieces. The mechanism is measured in `CALIBRATION.md`, *Shaped masses (M8)*: a shape costs its extent across the passes times the number of times a pass crosses it. The remedy named there is `s.cost()`, which the painter never ran, nor `--count`. **The mountain's ten facets are convex.** Laid along the line from each peak to its dip, which runs across the facet's length, they cost 88, against 31 along their own axes. The 129 is mostly that. `clean-small` fired and named the brush; nothing named the direction, because `direction-default` speaks only when `direction=` is left off. Both versions are recovered and reprint their reports | **4G** |
| 8 | **"No clear light" can't be satisfied by a mostly dark picture with small lights.** It isn't low-key by the definition, so the line repeats though the declared light reads 0.69. Fix: whenever `lightest=` is declared, judge whether that light stands clear, under any key | R | **The fix exists, as `key="low"`, and the picture qualifies.** The check's test for a low key is the top twentieth under the box's middle: `0.52` against `0.54`. Replayed with the plan's key set low, the line says *low-key, as the plan says* after every pass, and from the head's pass on *Uktarl's face stands clear -- 0.69 at its brightest twentieth against 0.50 for everything else, 0.19 over*. That is the painter's request, word for word. **What is missing is the definition:** the card says only *whether this picture is low in key*, and the reference's one example reads *nothing above 0.35*. This is the third painter in two rounds to meet this line (the Bell-Warden asked for the key; Wenna's lamp gave it the light clause) | **4H** |

### The documentation

| # | What the painter said | Kind | What checking found | Goes to |
|---|---|---|---|---|
| 9 | **Volume.** The package ships about 90,000 words; it read about 30,000 before the first mark, and the rules it used would fit on two pages. The 0.8.0 changelog entry alone runs to thousands of words. Fix: a one-page card (the loop, the order of work, about 15 call signatures, the numbers that matter), and a ten-line *what's new for a painter* atop each release entry | M | **Confirmed.** The six documents are 90,369 words, 51,788 of them `CALIBRATION.md`. Before its first exercise it printed 33,596 words of the documents: `PAINTER.md` 6,680, `RECIPES.md` 10,832 and `REFERENCE.md` 11,026 (to line 820 of 841), which is 28,538, and the 0.8.0 changelog entry from the checkout, 5,058 as printed. Fourth painter in four rounds. 0.8.0 answered it *for one page and not for the corpus*: the reading path grew from 20,546 to 25,313 words, and `LESSONS.md` says so | **4I** |
| 10 | **The instruction comes last**: qualifications, measurement history and cross-references ahead of the rule | O | **Confirmed on the row this painter needed.** `REFERENCE.md`'s `key=` row opens with what the `values:` line stops saying and never says when a picture counts as low-key. The rule a painter would act on is not in it | **4I** |
| 11 | **The pixel advice contradicts itself**: *You cannot reason in pixels* while 0.8.0 adds `s.px()`; *absolute placement in an unseen picture is what fails, not pixels* | O | **Confirmed.** `PAINTER.md` line 380 says it; line 159 introduces `s.px(x, y)`. Two of the last three painters drew every shape in pixels through a helper and placed them where they meant (Wenna Brask's `P()`; this painter's `poly_px`, `ell_px` and the head frames). The Bell-Warden drew in fractions. What went wrong was placement seen whole: Wenna Brask's first head came out too small and was scaled up by 1.3, and this painter's face matched the glow behind it until the thumbnail showed it | **4I** |
| 12 | **Missing recipes**: light round a figure already painted; a scene of several figures; a hollow thing seen low; a face lit from below | O | **Confirmed, and two are a sentence each.** None of the four is in `RECIPES.md`. *A hollow thing* assumes the inside is seen; from low, the near rim hides the floor and the far inner wall fills the opening. *A form turned toward the light* places the terminator for a light near the viewer; lit from below, it sits at the brows. Light round a figure is back to front when it is planned (the light first, the figure's held edge cuts it) and needs an exclusion when it is not (row 1) | **4I** |

### The painting, and the note that came with it

| # | Claim | Kind | What checking found | Goes to |
|---|---|---|---|---|
| 13 | **The painting**: stencilled; figures that are cut-outs with masks for faces; a relief too regular, a mountain flat away from Uktarl, dwarves like pegs; a tub that reads only close up, a table that floats; dark for a projector | O | Recorded. The check reads marks and measures the canvas; it does not judge an arrangement (`LESSONS.md`). Its own faults all measure: 102 marks on the first figure; ten sliver facets, 88 strokes; six coin and card marks buried by the near bandit (records 343, 344, 357-359, 361, which the check named after that pass: *took 6 earlier details out of sight*); the table top `0.18` under its plan | **4J** |
| 14 | **The note the owner sent with the verdict**: the thumbnail *earned its place on its first outing*; the soft edge is the item that matters; *dismiss a habit once per painting* is the right size; *the low-key light check is now on its third painter*; the pixel sentence to replace a chapter; *the last three painters drew figures in pixels*; *twenty-eight thousand words it read and didn't use* | R | Its numbers hold but one. The thumbnail was suggested on 2026-09-25 and caught two faults here on 2026-10-01. Fifty-nine percent and two softened edges, yes. The light check: three painters, yes. **Two of the last three painters, not three,** drew in pixels. 28,538 words is exactly what it read of the three files | 4B, 4C, 4H, 4I |

**What the painter defended, and nothing here touches:** the thumbnail; rehearse, then
commit, with the `dearest:`, `landed nothing:` and *out of sight* lines naming each dear or
wasted call by its script line (*I never needed `undo`*); guides that stay readable over
paint; `at_value` and a swatch strip, which caught grey faces before they were painted; a
clip-held flat stroke as a stencil, thirteen rays in thirteen strokes; `RECIPES.md`, three
entries landing first time (the light's pool, the projection, the terminator join);
`REFERENCE.md`'s tables; `PAINTER.md`'s order of work.

---

## 3b. The second painter: The Curator, checked

**Nine pieces of interim art for the owner's own game**, painted against 0.8.0 on
2026-10-11 by `claude-opus-5-5` at max effort in a cloud session of the game's repository,
as stand-ins until the designer's photographed oils arrive. One script per piece, seeded,
with a stage argument; three pieces cut out afterwards by scripts the painter wrote. Filed
as `paintings/Claude/the_curator/`, with its verdict as the owner pasted it. **It joins this
round**, on the owner's ruling of 2026-10-11, as the Bell-Warden and Wenna Brask shared
0.8.0's.

**It is a different kind of painter from every other in the corpus.** It never called
`s.report()`, `cost()`, `easel run` or `easel check`: it re-ran each script and read the
stage images, and called `s.checklist()` once, at the end. It read the card and most of
`PAINTER.md`, a fifth of `RECIPES.md`, and `REFERENCE.md` for *direction* only. **Its
transcript was not handed over**, so its claims are checked against its scripts, its
manifest and its exports, and nothing is recovered from its words.

Measured on 2026-10-11 on the checkout at `8f6fa77`, whose engine is `v0.8.0`'s
([`FILING.md`](paintings/Claude/the_curator/FILING.md)):

| # | What the painter said | Kind | What checking found | Goes to |
|---|---|---|---|---|
| 15 | **Determinism**: a seeded script re-ran to a pixel-identical PNG every time | O | **On one machine, yes; across machines, to one level.** Every piece re-run here comes back within one level of its shipped PNG, in 12 to 2,508 pixels per piece. The painter's machine was Linux, this one Windows; `tests/test_golden.py` already allows a numpy build's ±1, and no painter-facing document says so | **4I** |
| 16 | **Paint deposit is hard to predict**: `density=1.0` left gaps and needed `solid=True`; shading strokes at opacity 0.6 moved the candle a few levels, so it went to 0.9, twice | O | **The candle is a canvas-size fault, not an opacity one.** The candle was painted at its sprite size, 120×300, where `size=0.009` is 2.7 px, under the 6.5 px a round tip needs to land in one touch. One wax-light stroke there moves its pixels a mean 6 levels at 0.6 and 14 at 0.9 laid twice; at four times the canvas, 17 at 0.6 once. The gaps are the comb's (`CALIBRATION.md`, *The holes a solid comb leaves*); `REFERENCE.md` says *spacing, not coverage* for `density`, which it never read. Nothing says how the three combine in one place | **4M** |
| 17 | **Colour drift**: umber and ultramarine lightened with white kept turning lavender; the stones and boards came out purple twice | O | **Confirmed, and narrow.** Burnt umber is hue 17°; with 10 to 18% ultramarine the mix is a red-brown, at 25% a neutral leaning magenta, at 35% violet (276° to 320°). The warm grey it wanted lies in a band a few points wide. `at_value` re-solves the value whatever white went in first, so the white changed nothing. Its fix, in the committed stones: yellow ochre, and 4 to 6% ultramarine | **4L** |
| 18 | **No transparency**: exports are flat RGB; the arch, the patron and the candle needed `cut_outline.py`, cutting along the outlines it had painted. *For sprites this is the biggest missing feature* | O | **Confirmed.** `export()` takes a path, `impasto` and `sketch`. The cut scripts rebuild the painter's polygons from a JSON file the painting script writes, draw them at 4×, scale down and blur 0.8 px | **4K** |
| 19 | **The checklist assumes a standalone painting**: *no clear light* on shelves kept dark to sit behind the archway; *it can't know a piece is one layer of a scene* | O | **Six of the nine say *no clear light*.** Each names a light, none declares a key. None has a light standing clear (-0.01 to +0.07), so H2 would stay silent; all six keep their top twentieth under `0.54`, so `key="low"` would have said *low-key, as the plan says* — H1's missing sentence again. **And the cut-outs are read whole**: the candle's checklist reports 67% bare ground and *detail before the masses*, on the canvas the cut throws away; the patron's, 25% | **4H**, **4N** |
| 20 | **Geometric subjects fight the method**: shelves, bars and joints are ruled lines and combs, which the guidance warns against | R | Recorded. `RECIPES.md`'s *The one ruled line* is the one recipe for it, and it read five stretches of that file, none of them this. The bookcases declared `bands="subject"`, which is that warning's answer, and their checklists count the crossings instead | **4I**, asked |
| 21 | **Polygons in 0-1 on wide canvases**: a pixel helper in every script; `s.px` exists but polygons do not take pixels | O | **Confirmed, for half of it.** Four of its eight scripts — the locked case, the wall, the patron and the candle — define `n(x, y)`, pixels to fractions, and build their shapes through it; the desk and the counter, the widest canvases, are drawn in fractions. Three of the last four painters drew in pixels through a helper (Wenna Brask's `P()`, Uktarl's `poly_px`, this `n()`) | **4E** |
| 22 | **The guide is method, not reference**: signatures read from the code — `ribbon`'s width, the pressure profiles, `press` on one point; *a one-page table of brushes, parameters and units*; *never says how opacity, density and `solid` combine* | O | **The reference exists, and nothing sent it there.** `REFERENCE.md` gives `ribbon()`'s width (line 24), the profiles (203), `density` (126), `solid` (127), `opacity` (135) and a brush table (183), and `easel guide --reference` prints it. The card names `REFERENCE.md` once, for the plan. How the three combine is not in it | **4I**, **4M** |
| 23 | **Messages**: the floor with a hex and a hue; a brush too small, with the width and the fix; `press` misused, with three alternatives | O | The engine's (`palette.py`, the landing notices, `press`'s docstring). What a script that is never rehearsed hears at the call: on this set, a chisel pressure fact, two spills and a solid comb, as warnings on every run; six pieces heard nothing | — |

**What it defended, and nothing here touches:** determinism as a pipeline; the messages;
the method's order; `at_value`.

---

## 4. Workstreams

### A. Paint held outside a shape

**Proposal.** `clip_out=` on every verb that takes `clip=`, one place or a list. The paint
lands where `clip=` allows and none of `clip_out=` reaches. Beside `union()`, two shape
builders: `intersection(a, b, ...)` and `difference(a, b, ...)`.

- **The mask.** `_clip_cover` multiplies the held masks; an exclusion multiplies by one
  minus its coverage, in the same memo, with the outline in the key. Feathered as a hold
  is: the default `0.002` breaks the exclusion's edge on the side the paint is on, so paint
  laid up to a figure meets it as a held edge meets its own outline.
- **The shapes.** Traced from the same mask `union()` traces. A result in more than one
  piece, or with a hole, is refused, and the error names `clip_out=`. The wall round a
  figure standing inside it is a hole, and an exclusion is the answer there.
- **The record.** It must replay in 0.9.0 and be refused by 0.8.0. A new key alone fails
  that: `_brush_from_params` drops it, and 0.8.0 would paint through the figure. Carry the
  exclusion inside `params["clip"]` in a form 0.8.0's `_clips_from_params` cannot read, so
  it raises. Tested against a `v0.8.0` build from `git archive`, as 0.7.0's round did.
- **Measured in step 2:** the painter's backlight laid with `clip_out=` Uktarl's parts and
  no regions: the marks, the pixels against the painted version, and the seam gone; the
  three regions' 44 typed points replaced by one argument; 0.8.0 refusing the record.
- **To the painter (P1):** both builds or one; and whether the exclusion's edge is held
  like any hold or takes B's softness.

### B. A held edge that is soft

**Proposal.** A softness on the holds of a call: the mask fades over a width the painter
names instead of cutting at the outline. This is the verdict's first answer (`edge="soft",
soft=<px>`). Its second, a verb that loses any length of an outline priced by length, is
a candidate beside it.

- **What is different from 0.7.0's decline.** 0.7.0 asked whether *every* held edge should
  blur by default, and the answer was no. This is a softness chosen per call, for the edges
  a painter means to lose, at no extra stroke: the price the note asks to change.
- **The candidates, benched in step 2:** **B1** a ramp inward from the outline over N px;
  **B2** that ramp broken against the canvas's tooth, so it reads as a dragged edge and
  not a blur (the mechanism `broken_edge` already has, over a wider depth); **B3** a ramp
  centred on the outline, which needs the passes' overhang; **B4** a `lose()` verb along
  a stretch of outline. Each is laid on the painter's own picture, on the two edges it lost
  and on the far side of every figure, at 4, 8, 16 and 32 px. The bench reports what the
  `edges:` line reads, the time it costs, and sheets at 1:1 and at 256 px.
- **Which edges.** One `soft=` applies to every hold of a call, as `feather=` does. Whether
  a softness per hold is wanted (the figure's far side soft, its near side hard) is the
  painter's question (P2), with its own picture as the case.
- **The units.** The painter wrote pixels. `feather=` and `size` are fractions of the long
  side, and `s.px_size()` converts. Which is the painter's (P2).
- **The record.** As in A: refused by 0.8.0, never misread.
- **The documents.** *An edge that is actually lost* and *Edges: lost and found* lead with
  the soft hold; the smudge stays for a stretch of an edge already painted.
- **To the painter:** the form and the edges now (P2); the look later, blind, from the
  bench's sheets (batch 2).

### C. The check: three rules narrowed, and a habit declared

**Proposal.** Narrow the three rules that misfired here, each only as far as the corpus
allows. Then let a painter declare in the plan a habit its picture means, so that the
habit's finding becomes a count.

- **C1, the disc rule.** It counts any hand-laid round mark at `tip_wobble=0` that is
  shorter than 7 of its widths. That is what eyes, brows and mouths are. Candidates:
  (a) compare what the marks landed, not their size ratio, which is the painter's form:
  two marks that differ in silhouette are not one disc printed twice; (b) leave out marks
  shaped by a pressure list or a path of three or more points; (c) neither, and rely on
  C4. Measured in step 2 over the corpus: how many disc findings are faces (this painting,
  Wenna's face, the Bell-Warden's head), how many are the true positives the rule was built
  on, and what each candidate keeps.
- **C2, the bars rule.** It reads angles over the whole pass. The candidate is the
  painter's: the stack's marks must touch, as one connected footprint. Measured: which of
  the corpus's bars findings it keeps, the pier's and the laundromat's first.
- **C3, the graded rule.** Three colours can be three masses. Candidate: a mass's passes
  count as one mark, so a graded passage needs three or more hand-laid marks at stepping
  colours. Measured: the 7 of 337 corpus passes it fires on (0.7.0's count) and this one.
- **C4, a habit declared.** By the owner's ruling of 2026-09-18, a standing warning is
  declared up front in the plan (`bands="subject"`, `ground="buried"`), not dismissed after
  the fact. The candidate: `s.plan(habits={"disc": "the features of four faces"})`. The
  finding then prints as a count with the painter's reason, and the closing checklist
  quotes the reason back as it quotes `why=`. Scope (per painting, or per place) and which
  habits may be declared are the painter's (P3).
- **The noise.** After each candidate, count the findings per committed pass over the
  corpus and over this painting, against 0.8.0's.

### D. A rehearsal's look, cropped and clean

**Proposal.** `easel run --rehearse` takes `easel look`'s `--region`, `--no-sketch`,
`--no-marks` and `--scale`, for the look it writes, and so does `--alternatives`' sheet.
The server's `run` takes the same. Nothing else about the rehearsal changes.

- **The stale landmark.** A redrawn drawing pass leaves the old one's landmarks, because
  `unguide()` is for guides and `unmark()` for landmarks. One clause in the drawing step of
  `PAINTER.md` and in `unguide`'s docstring says so; no engine change.
- **Measured:** none needed; tested at the shell and through the server.

### E. A local frame, and rotation

**Proposal.** `.rotated(degrees, about=None)` on `Polygon`, `Region` (which becomes a
`Polygon`) and `Group`, clockwise as `rotate=` is on `ellipse()`. And a frame: `s.frame(
centre, rx, ry, tilt=0)`, which maps local coordinates in its own radii to canvas places,
with `.at(u, v)` and `.polygon(points)`. That is the painter's `hp()` as a call.

- **Built against the painter's three heads:** the frame must reproduce `hp()`, `dp()` and
  `ah()` point for point, in pixels through `s.px` and in fractions.
- **The recipe** *A thing drawn in its own frame* (4I) uses it.
- **To the painter (P4):** the frame's shape, and its units.

### F. A share for each part of a picture

**Proposal.** `s.plan(shares={"uktarl": 0.15, "relief": 0.25, ...})`, keyed by the `note=`
a call carries, read against the **budget**. A standing line `shares:` prints each part's
strokes against its planned share of the budget (*uktarl 102 of 68*), and says when a part
has passed its share. `subject_share=` stays, and is a share of one.

- **Of the budget, not of the marks so far.** The `subject:` line read 47% and 48% from
  Uktarl's head on, and the painter saw it six times; it measured the marks laid so far,
  and against the budget he had 23%. A share of the budget is the number that says the last figure will be
  starved.
- **Measured in step 2:** the line on this painting with the split the painter says it
  would have planned (P5), pass by pass.

### G. What a mass is charged for its direction

**Proposal.** Say at the call what the direction costs, wherever the engine can price a
cheaper one.

- **G1, a direction given that costs far more than the shape's own axis.** The facets: 88
  along peak to dip, 31 along their axes. `direction-default` fires only when `direction=`
  is left off, and `direction-sequence` only for a list of angles. Candidate: the same
  2.5× test for a single direction given, saying both prices. Measured in step 2: how many
  of the corpus's masses with a direction given pass 2.5× their axis, and whether any is
  a direction a painter chose for the marks' look rather than in error.
- **G2, a concave shape whose passes cross it twice.** The V: 8 of 14 passes in two
  pieces, 17 to 22 strokes at any one direction, 7 as two parts. Candidates: (a) a notice
  when a third or more of a mass's passes come back in pieces, saying so and nothing more;
  (b) the same with a price for the shape cut at its deepest notch, each part along its
  own axis. Measured: how often either fires over the corpus, and how far (b)'s price is
  from the parts a painter would draw.
- **G3, passes wholly outside a clip.** This is the third painter to pay for them: 9 of
  one floor rehearsal's passes and 1 of the head's committed pass landed nothing. 0.8.0
  left it as *a default's move, for a painter to decide with the corpus beside it*,
  because skipping them renumbers every later mark of a script that lays one. Step 2
  counts the corpus's passes that would be skipped and the paintings they would move; the
  painter decides (P6).

### H. A light in a picture that is dark on purpose

**Proposal.** Say what the check counts as low-key, where `key=` is introduced. And when
no key is declared, let the `values:` line name a planned light that stands clear before
it says *no clear light*.

- **H1, the definition, rule first.** The card's plan step and `REFERENCE.md`'s `key=` row:
  *declare `key="low"` when only your light is meant to rise above the middle of the box,
  `0.54`; the check then asks whether that light stands clear of everything else.*
- **H2, the line without a key.** When the line would say *no clear light* and the plan
  names a light that stands `0.10` or more clear of everything else, it says so and names
  `key="low"`: *no clear light -- nothing above 0.52 ...; Uktarl's face stands clear of
  the rest, 0.69 against 0.50 -- plan(key="low") if the picture is dark on purpose*. The key
  stays a declaration that buys a question, which 0.8.0 ruled. Measured in step 2 over the
  corpus's plans with a named light (the handover, the Bell-Warden, Wenna Brask, this one):
  what H2 would have said on each pass.
- **H3, the painter's own form**, the light judged under any key with no declaration, is
  the third candidate. It silences *no clear light* for every plan that names a light.
- **To the painter (P7).**

### I. The documentation

**Proposal.** Make the reading path shorter for the first time, and say each rule first.

- **I1, a one-page card.** The fourth painter in four rounds says the documents are too
  long; this one read 28,538 words of the three files and says the rules it used fit on
  two pages. 0.8.0 declined a second page because the card is the first page, under a
  budget. This round writes the card as one page: the loop, the order of work, about
  fifteen call signatures, and the numbers that matter. It is held to a word budget by
  `tests/test_guide.py`, set from step 2's inventory, not guessed. `easel guide` already
  prints only the first page, about 1,400 words; this painter, like the handover's, opened
  the files in the installed package instead. So the page has to be the file's first page,
  and the files have to be shorter.
- **I1, the cuts.** The handover painter's instruction, still untried: start from what the
  notices already say at the call, and cut what they have made redundant. Step 2
  inventories every paragraph of `PAINTER.md`, `RECIPES.md` and `REFERENCE.md` against the
  notices, findings and lines that now say the same thing, and against what this painter
  says it used (P8). Each cut goes to `CALIBRATION.md` or `LESSONS.md` if it is a
  measurement or a story, and the reading path is counted before and after, as this
  painter read it. The target is set from the inventory, so that it can be met.
- **I2, rule first.** Every row this round writes, and the card. `LESSONS.md` gains the
  order (*rule, number, history*) in *One home per rule*.
- **I3, the pixel paragraph.** *You cannot reason in pixels* is replaced by the painter's
  sentence, *absolute placement in an unseen picture is what fails, not pixels*, with its
  remedy: draw in pixels or in a thing's own frame, and look at the arrangement small
  before paint (`s.thumbnail()`). A recipe, *A thing drawn in its own frame*, uses E.
- **I4, what was missing.** *Light behind a figure*: planned, it is back to front; after
  the figure, `clip_out=` (A). *Several figures*: a share each (F), several faces lit from
  one source, and figures varied by silhouette before costume. *A hollow thing* gains one
  sentence for a low view, and *A form turned toward the light* one for a light from below.
- **I5, a painter's lines atop each release entry.** Ten lines saying what a painter will
  meet, before the entry's account. From 0.9.0, and written for 0.8.0's entry too.

### K. A painting with a transparent surround

**Proposal.** `s.export(path, alpha=place)`: the alpha channel is the coverage of a place
or a list of places — the shapes the painter laid the thing in — antialiased as a hold's
mask is. `easel export --alpha` takes the plan's named places. Nothing else about the
export changes, and the canvas never holds an alpha.

- **Against the painter's own cut.** `cut_outline.py` draws the polygons at 4×, scales
  down and blurs 0.8 px. Step 2b lays both on the patron and the candle: the pixels that
  differ, the edge's width, and the sheet at 1:1 over two backgrounds.
- **The hole.** The arch is a hole in the wall: `alpha=` takes `difference()` (4A), which
  P1's answer already allows for a place that is read, not painted.
- **To the painter:** the form (Q1).

### L. A grey that stays warm

**Proposal, not yet chosen.** The trap is a narrow band: two pigments that cross neutral
into a third hue as one is added. Candidates: **L1** a fact at `mix` when the mixture lies
within a few degrees of neutral and the hue has turned more than 90° from both parents,
naming the share where it turns; **L2** a recipe, *A warm grey*, with the band measured;
**L3** a named mixture on the palette, `p.grey(value, warmth=)`. Step 2b measures L1 over
every corpus palette's mixtures: how often it would speak, and on what.

- **The white.** `at_value` re-solves the value whatever white went in, so mixing white
  first changes nothing. One sentence where `at_value` is introduced.
- **To the painter (Q2).**

### M. How a mark deposits, in one place

**Proposal.** One table, rule first, of what `opacity`, `density`, `solid`, `press` and the
brush's pixel width each do to what lands, and how they combine, in `REFERENCE.md` beside
the arguments, linked from the card. And **the canvas's size**: `size` is a share of the
long side, so a sprite painted at its own size puts every small brush under its landing
width — the candle's 2.7 px strokes. Candidates beside the sentence: **M1** paint at
two to four times and export at the size wanted, `s.export(path, size=(w, h))`; **M2** a
fact at the call when a round tip is under its one-touch landing width and laid with a
pressure list or `opacity` under 1 (today the line after the pass says what landed
nothing, which a script that is never rehearsed does not print).

- **Measured in step 2b:** the candle at 1×, 2× and 4× and exported at its size; the share
  of the corpus's hand-laid marks under their landing width, by canvas size.
- **To the painter (Q3).**

### N. A piece that is one layer of a scene

**Proposal.** Let the plan say what of the canvas ships. Under `plan(cut=place)` — the
same places `alpha=` takes (4K) — the standing lines read inside the cut only: the ground
line, `boxes:`, the values line's percentiles, and the closing audit's discs. And `key=`
said plainly where the plan is introduced (H1), since every dark layer of this set was
low-key by the check's own test.

- **Measured in step 2b:** the nine checklists with `key="low"` on the six dark pieces and
  `cut=` on the three cut-outs: what each line says then.
- **To the painter (Q4)**, and whether the scene should be declared at all: a layer that
  sits behind an archway is judged against the room it sits in, which no single canvas
  has.

### The second painter's other rows

- **Determinism across machines** (row 15): one sentence where the README promises a
  rebuild, *to the pixel on one machine, within one level on another* (4I).
- **Polygons in pixels** (row 21): E's frame takes pixels; whether `polygon()` should too
  is asked (Q5).
- **The reference** (row 22): the one-page card's *where to go next* names `easel guide
  --reference` for signatures, units and defaults (I1); M's table is the combination it
  asked for.
- **Geometric subjects** (row 20): asked (Q6) whether *The one ruled line* answers it, or a
  recipe for a ruled thing seen as paint — a shelf, a bar, a joint.
- **A painter who never rehearses** (row 23): recorded. The post-pass check reaches only
  `easel run`; a script driven from Python hears the call-time notices and the closing
  checklist. Asked (Q7) whether it knew of `s.report()`.

### O. The check where a script already stops

**Proposal, from Q7.** A painter who drives Python directly re-runs its script whole and
reads `s.look()`; it never meets the check after a pass, and the documents saying so three
times did not move it. Candidates: **O1** `s.look()` prints the check over the marks since
the last look, with `dearest:` and `landed nothing:`; **O2** `easel run` accepts a script
that builds its own `Session`; **O3** a notice for a faint mark — one that moved the canvas
by a few levels where its colour was far from what it landed on — which no path has.
Step 2b measures O3 over the corpus and on the candle, the patron's rim and the lock.

### J. Recorded and not built

- **The painting** (row 13): what the check cannot see. The stencilled look is row 2's.
- **`union()` raised twice** on parts that did not touch. It did what it says, and the
  painter's notes say so.
- **The join on skin**, 0.8.0's open question. The painter laid a join along each face's
  terminator and calls the faces masks. It is asked (P9), with its own picture.

---

## 5. What this round revisits

| Earlier decision | This round | Why it is not undone |
|---|---|---|
| 0.7.0: every held edge breaks against the tooth by default; a Gaussian soft edge declined because it reads as blur | a softness chosen per call (4B) | the default stays; the decline was about every edge, and this is for the edges a painter loses |
| 0.8.0: `feather=` breaks and does not soften; *a soft brush held hard is held hard* | the same, with a soft hold beside it | `feather=` keeps its meaning |
| 0.6.0: the default-direction notice speaks when `direction=` is left off, and is quiet on a direction chosen | a direction given says its own price when it costs over 2.5x the axis (4G, G1) | the default's notice is unchanged; a chosen direction is still the painter's to pay for, and the new line is a fact, both prices, nothing more |
| 0.6.0, the owner: standing warnings are declared in the plan, not dismissed after the fact | `habits=` in the plan (4C) | kept: the declaration is up front |
| 0.8.0: `key=` is a declaration that buys a question, not a switch that buys silence | H2 names the light and the key without a declaration | kept, unless the painter chooses H3 |
| 0.8.0: no second page; the card is the first page | a one-page card (4I) | revisited on the fourth painter's evidence; the budget test stays |
| 0.8.0: skipping a mass's passes outside its clip is a default's move | counted, and put to the painter (G3) | nothing moves without its answer |

---

## 6. Questions

### For the owner

All three have 0.8.0's precedent, so they are taken as answered that way. Say if not.

- **O1.** File with the campaign's details left out: the dossier's and map's paths, the
  catalogue entry, the WebP copy. Done, and marked where cut.
- **O2.** `verdict.md` only; nothing posted. Done.
- **O3.** The painter's questions go through the owner: batch 1 now
  (`questions-step1.md`), batch 2 after step 2 with the bench's sheets, as a blind package.

### For the painter, batch 1 (`questions-step1.md`)

| | Question | Decides |
|---|---|---|
| P1 | `clip_out=`, the two shape builders, or both; and whether an exclusion's edge is held like any hold or takes B's softness | 4A |
| P2 | the edges in this picture it would have softened if softening cost nothing, and over how many pixels; a softness per call or per hold; pixels or the long side's fraction; a soft hold or a `lose()` verb | 4B, and the bench's cases |
| P3 | a habit declared in the plan with a reason: which habits, per painting or per place; and for the disc rule, what would tell a face's marks from one disc printed | 4C |
| P4 | what it would have written instead of `hp()`, `dp()` and `ah()` | 4E |
| P5 | shares of the budget or of the marks so far; and the split it would have planned here | 4F, and the bench's case |
| P6 | whether a mass should skip passes that fall wholly outside its clip, knowing it moves later marks in scripts that lay them | G3 |
| P7 | H1, H2 or H3 | 4H |
| P8 | the rules it used, the two pages; what the one-page card must hold | 4I |
| P9 | the join along the faces' terminators: skin or facets, at 1:1 | 0.8.0's open question |

The row for G1 and G2 is not asked yet: step 2's counts come first.

**Answered 2026-10-10**, filed verbatim as
[`answers.md`](paintings/Claude/uktarl_krannoc/answers.md), with the three pictures it cites
in `evidence/`. What each answer decides, rule first; every **M** in it re-measured by
`scripts/probe_uktarl_session.py --answers` and `--clip-out`, and held:

| | The painter chose | Changes the plan |
|---|---|---|
| P1 | `clip_out=` alone for paint; `intersection()` not wanted (`clip=` with a list is one). `difference()` only for places that are read (`plan`, `sample`, `thumbnail`, `compare`), where a hole does no harm; the mass verbs keep the refusal. **The exclusion's edge is cut on the line**, or broken onto the excluded shape, never into the paint it holds | 4A: no `intersection()`; the exclusion's default is `feather=0`. Measured: the default feather breaking into the light leaves the seam the painter found, 1 to 3 px of unlit wall at 0.22 to 0.24 between light at 0.44 and him at 0.14 |
| P2 | a soft **hold**, not a `lose()` verb; **a softness per hold**, because every edge it would soften belongs to a call with a second hold that stays crisp; **in the long side's fraction**, written `soft=s.px_size(8)`; eight edges listed with widths, 2 to 12 px | 4B: B4 dropped; the bench's cases are the answer's table |
| P3 | the disc rule: **near-copies, three or more, measured on what landed**; a pair is not a print run. Declared **per place**, not per painting: the three faces and the fan of cards. No bars habit. **New:** print a standing line only when it changes, and the findings above the standing lines | 4C: C1's candidate is the painter's; a new C5 |
| P4 | `s.frame(centre, rx, ry, tilt=)` with `.at()` and `.polygon()`, and **`.arc(t0, t1, n)`**; **rotation and tilt turn in pixels** whatever unit they are handed. Measured: a square turned 30° in fractions on a 4:3 canvas comes back at 23.4°, a 104° corner | 4E |
| P5 | shares **of the budget**; the split it would have planned, by part (Uktarl 25%, the near bandit 10%, ...) | 4F; the bench's case |
| P6 | skip a pass wholly outside its clip **only if the random stream is kept**, so nothing after it moves; otherwise not. Still named under `landed nothing:`, *skipped, not charged* | G3 |
| P7 | **H1 and H2**, not H3 | 4H |
| P8 | the rules it used, in one line each; what the card holds; four cuts from *The first hour*; and one sentence: *read every line the check prints after a pass; do not filter it* | 4I |
| P9 | at 1:1 the join reads as a **facet** on all three faces; a join twice as wide at the halfway value, or the lit plane's edge held soft over about 8 px | B's first row; the recipe's join width, measured in step 2 |

### After the bench (step 2)

What each benched candidate showed against the answers above; the numbers are in
`CALIBRATION.md`, the round's *Step 2*.

| | Benched | So |
|---|---|---|
| 4A | the exclusion **cut on the line** closes the seam (0 to 1 px at the painter's rows against 1 to 3) and lays nothing wholly on him; broken into the light it is the seam exactly | as the painter chose: `clip_out=` at `feather=0` by default. Step 3 |
| 4B | a soft hold per hold costs no time; the step widens less than asked wherever a later mark crosses the edge, and a hold softens its whole outline, near side too | the look is the painter's, blind (batch 2, 1a and 1b), and the far side's crisp near side (2b) |
| 4C | near-copies keeps 8 of the disc rule's 30 passes, touching 27 of the bars rule's 53, a mass as one 3 of the graded rule's 8; each drops passes the rule was right on, by the bench's eye. The disc rule measures the silhouette, which size and value do not see | none narrowed until the painter reads the crops (batch 2, 3 and 4); the per-place declaration (C4) stands either way |
| C5 | 40% of the corpus's standing lines repeat the pass before; 61% of this painting's, rehearsals included | the form (batch 2, 7) |
| 4F | under the painter's split, the line names the near bandit at 22 of 45 with 40 in hand | as chosen. Step 6 |
| G1 | a direction given over 2.5× its axis: 1 of 197 masses in the corpus, all 10 facets | a notice is cheap in noise; batch 2, 5a |
| G2 | (a), a third of a mass's passes in pieces: 27 of 450 masses, and the V; (b) not built | batch 2, 5b |
| G3 | 12 strokes over the corpus | batch 2, 6 |
| 4H | H2 speaks on the three paintings that name a light, from the pass that paints it, and nowhere else | as chosen, H1 and H2. Step 7 |
| P9 | the steps across the terminators are 2.1, 1.7 and 1.4 px, against a sixth of a face, 7 to 8 | the join's recipe width, in step 8, after 4B's answer |

### For the painter, batch 2, after step 2

Written: [`questions-step2/`](paintings/Claude/uktarl_krannoc/questions-step2/README.md).
The soft hold blind on its own eight edges and the whole picture; the three rules'
candidates on the corpus's crops; G1, G2, G3 and the standing lines' form.

**Answered after the bench, 2026-10-11**, filed verbatim as
[`answers-step2.md`](paintings/Claude/uktarl_krannoc/answers-step2.md); its **M** claims
re-measured by `scripts/probe_uktarl_session.py --answers2`. The painter's blind picks
matched the key letter for letter; it read Part 2's text, which names no letters, before
the blind sheets, and says so.

| | The painter chose | So the round builds |
|---|---|---|
| 4B | **B1**, a smooth ramp inward, the edge meant on every sheet it could tell; B3 read as a blur, B2 as damage. **A softness per hold and per stretch**: a lit plane wants its whole outline soft; a far side wants a run of the shape's own points (`soft=[(dp_body.closed[4:8], s.px_size(9))]`), tapering back to the hold's edge at each end | step 4: B1, per hold and per stretch. Re-measured: B1 on Uktarl's lit plane darkens 24% of it by over 0.05, median 0.14, and widens the step across its outline from 1.5 to 3.1 px; the bench's *barely changes* read his terminator, under the wig, and was wrong |
| 4C, disc | **near-copies withdrawn**: of the crops it dropped, the sonnet's stairs, the fable's berries and the heron's lamp and specks are one disc printed. The rule as it is, with the per-place declaration (C4) for faces | step 5: C4 only. **New:** the pass rule counts the signature (`p17_finish.py`, records 425 to 428), which the closing audit leaves out; leave it out of the pass rule too |
| 4C, bars and graded | **the rules as they are**: touching keeps what reads as one flat colour and drops what reads as bars; a mass as one spares one false finding for four true. A test on the canvas instead -- the value alternating at the stack's spacing by over 0.03, or climbing in plateaus -- as a later candidate | nothing this round; the canvas test to `SUGGESTIONS.md` as a candidate to bench. Re-measured: across the laps' rows, the largest departure from each row's slope is 0.015 and 0.003 |
| C5 | **findings first, a standing line only when it changes**, a rehearsal compared against the painting as committed, the lines left out named on one line (*unchanged: values, edges, ground*); the closing checklist prints every line | step 5 |
| G1 | **a notice, both prices** | step 7 |
| G2 | **a notice now, with its counts**: *14 passes in 22 pieces: lay each part along its own length*; a price when one exists | step 7, (a): built, and held — at that count it spoke at the calls of three recipes. Asked back, below |
| G3 | **leave it named; do not build it** -- a change of the step-1 answer, on the bench's 12 strokes | nothing |

### Asked back after step 7 (`questions-step7/`)

Built as chosen, the pieces notice spoke on three of `RECIPES.md`'s recipes — a grip's
clean fill, a silhouette's shade, a half-tone band, at 1.33 to 1.43 pieces a pass —
against the V's 1.57, and on `PAINTING.md`'s ribbon round a bend. No count separates
them; a price for the parts (G2 (b)) does, 22 against 7 on the V. Held on the owner's word
(2026-10-17), and asked: which shapes on the sheet it would have told to lay each part
along its own length; (a) the notice held for a price of the parts, (b) a count of 1.55,
(c) its count with no remedy in the sentence, or (d) else; and, for (a), how much cheaper
the parts must be. Not answered yet.

---

### For the second painter, batch 1 (`the_curator/questions-step1.md`)

| | Question | Decides |
|---|---|---|
| Q1 | transparency: `export(alpha=place)`, a cut on the plan, or both; how the edge should fall (as a hold's, or softened as its own cut was) | 4K |
| Q2 | the warm grey: a fact at the mix, a recipe, or a named grey; and what it saw that told it the stones had gone purple | 4L |
| Q3 | deposit: which calls it fought, with what it tried; whether painting at two to four times and exporting at size would have served; and what the table must say | 4M |
| Q4 | a layer: `key="low"`, a cut on the plan, or a declared scene; which of the checklist's lines it would have wanted kept on a cut-out | 4N |
| Q5 | polygons in pixels: E's frame, a pixel form of `polygon()`, or a canvas made with pixel coordinates | 4E |
| Q6 | geometric subjects: whether *The one ruled line* would have served, and the shelf, bar and joint it would have wanted a recipe for | 4I |
| Q7 | rehearsal and the check after a pass: whether it knew of them, and why it ran the scripts whole | recorded |
| Q8 | the reference: whether it saw `easel guide --reference`, and what would have sent it there | 4I |

**Answered 2026-10-11**, filed verbatim as
[`the_curator/answers.md`](paintings/Claude/the_curator/answers.md) with the scripts behind
its measurements in `measurements/`. Its **M** claims re-measured here and held: the
patron's planned light 0.16 inside the cut against 0.54 over the cell, 10 rim pixels over
0.40; the cabinet's lock no brighter than 0.46 against 0.6 planned; the candle painted at 4×
and reduced, 0.92 at its light's brightest twentieth against 0.87, *2 of 2 places*; and
plain `easel guide` is `PAINTER.md` lines 28 to 146, which leaves out line 15's table, the
one line that says `REFERENCE.md` holds units and defaults.

| | The painter chose | Changes the plan |
|---|---|---|
| Q1 | **both, from one declaration**: `s.plan(cut=place)`, which the checklist reads inside and `s.export()` writes its alpha from, unless `alpha=` names another place. A place of its own, because it laid the masses past the outline on purpose. **The edge falls as a held edge's, 0.8 to 0.9 px**; softening is an option, in pixels (`soften=2.5`): its 0.8 px blur made a 2.5 px edge | 4K and 4N are one: `cut=` on the plan, `alpha=` on the export |
| Q2 | **`p.grey(value, warmth=)`**, with the fact at `mix()` as a backstop. The stage images showed the purple; it printed value and chroma, never hue, and its swatch is where it chose the 25% mix | 4L: L3, and L1 behind it |
| Q3 | **painting at two to four times and exporting at size** serves the small pieces, **if the export keeps the canvas's weave at the exported scale**: reduced from 4×, the linen all but disappears. The table in pixels, per brush, with the cliff drawn across it. **And a word at the call** for a mark under its cliff: nothing said one. Two more lights were lost the same way, the patron's rim and the cabinet's lock, both laid under 4 px | 4M: M1 with the weave kept, M2 built, the table in pixels |
| Q4 | **`key="low"` said plainly, and the cut in the plan; not the scene**, which the game composes in code and no canvas holds. On a cut-out, every line measured inside the cut, and one more for the cut's own edge against the picture's median. The patron's *no clear light* was reading the ground the cut throws away | 4N with Q1's `cut=`, and a cut-edge line |
| Q5 | **a canvas in pixel coordinates throughout, sizes included**: `s.frame` would not have retired `n()`, and `s.px` existed and did not; `size=2.7`, not `0.009`, would have shown the candle's fault as it was typed | 4E gains a candidate: a session in pixels. Not built in step 6, on the owner's word: Wenna Brask agreed in 0.8.0's round that it should not be, and no bench has measured it |
| Q6 | it never opened *The one ruled line*, which answers the opposite question; it read *A scene with straight edges* and did not carry it to flat-on subjects. **A recipe for a shelf, a bar and a joint as paint**, in pixels, and a line naming long edges laid with under half a pixel of wander | 4I gains the recipe; the line is a candidate to bench |
| Q7 | **it had read that rehearsal and `s.report()` exist, and did not use them. Make the tool meet the script**: `s.look()` prints the check on the marks since the last look; `easel run` takes a script that builds its own `Session`; and a notice for faint marks, which no path has | a new workstream, O: the check where a script already stops |
| Q8 | **neither seen. The five-file table atop what `easel guide` prints by default**; then a line in `Session`'s, `block_in`'s and `stroke`'s docstrings, *units and defaults: `easel guide --reference`*; then the flags on `easel --help` | 4I1: the card opens with the table |

### After the bench (step 2b)

What each benched candidate showed against the second painter's answers; the numbers are
in `CALIBRATION.md`, the round's *Step 2b*.

| | Benched | So |
|---|---|---|
| rebuild | all nine pieces to the pixel on Linux, the painter's platform, at their recorded spend; the filing's one level was Windows | row 15's sentence stands as written (4I) |
| 4K | the places' coverage as a hold's is **harder than the painter's held paint edge**: 0.3 to 0.6 px over the outline's length against 0.8 to 0.9, a visible step on the patron's diagonal at 2×2 samples; its *soften=2.5* is a Gaussian of sigma 0.8 to 0.9 px on all three | asked back (Q1 again): the held edge it chose measures 0.3 to 0.6 px as an alpha, not the 0.8 to 0.9 its paint edge does. Proposed: four samples a side, and `soften=` as the 10-90% width in pixels, solved to a sigma. Step 3, beside `difference()` for the wall's hole |
| 4M | the candle at 4× reads 0.92 at its light and *2 of 2 places*, in 11.7 s against 2.0; **the weave it loses is the marks' own texture, not the canvas's tooth** (\|r\| at most 0.05), so laying the tooth back would not restore it | asked: whether a reduced export that loses the marks' finest texture still serves, from `deposit.png`; no weave candidate is proposed. M2's reach is wide, 807 marks in 31 of 34 paintings, 22% to 75% of hand marks by canvas size |
| 4N | under `key="low"` all six dark pieces say *low-key, as the plan says*; read inside the cut, the patron's values line reads 0.08 to 0.12, its lost rim; **the ground line asks for ground on two cut-outs** painted solid to the outline (0.00% and 0.23%) | `cut=` as answered; asked: whether the ground line inside a cut keeps its floor. The audit's findings do not move. After batch 2, with 4K's `alpha=`, since Q1 makes them one declaration: not built in step 7 |
| L1 | **as worded it cannot fire on the trap**: a mixture's hue travels the arc between its parents. From the larger parent, at chroma 0.03 and 60°, it catches four of the painter's six turned mixtures and speaks in 29 of 34 paintings, mostly on umber with 30 to 55% ultramarine mixed as a dark | L3, `p.grey()`, as chosen. L1 as a backstop at every call would be the commonest fact printed; asked whether the painter still wants it, and in what form |
| O3 | at 0.15 from what it landed on and under a quarter of the way: 327 marks in 28 paintings; it fires on the patron's rim and the lock, **not on the candle's wax-light strokes** (0.32 to 0.40 of the way), which M2 catches before they land | asked: O3, M2 or both, and at which thresholds, from these tables |

**Its two offers for the game's repository** — rewording the README's *pixel for pixel*,
and repainting the patron's rim and the cabinet's lock — are the owner's to take or leave,
and touch nothing here.

---

## 7. Order of work

| Step | What | Leaves |
|---|---|---|
| 1 | **The record.** The painting filed, the verdict checked, the round opened, the questions written | this PR, `NOTES-step1.md` |
| 1b | **The second painter.** The Curator filed, its verdict checked (section 3b), workstreams K to N written, its questions | `NOTES-step1b.md` |
| 2 | **Measure.** `scripts/probe_uktarl_session.py`: the rebuild, and a flag per workstream: `--clip-out`, `--soft` (sheets), `--rules` (the corpus replayed with each candidate), `--direction`, `--key`, `--shares`, `--reading` (the documents' inventory). The corpus replay cached as 0.8.0's was, and copied out before a later flag writes over it | `NOTES-step2.md`, `CALIBRATION.md`'s round, batch 2 |
| 2b | **Measure the second painter's.** `scripts/probe_curator_session.py`: the nine pieces rebuilt; `--alpha` (K, against its cut), `--grey` (L1 over the corpus's mixtures), `--deposit` (M: the candle at 1×, 2×, 4×; the corpus's marks under their landing width), `--layer` (N: the nine checklists under `key=` and `cut=`), `--faint` (O3: faint marks over the corpus, the candle, the patron's rim and the lock) | `NOTES-step2b.md`, `CALIBRATION.md` |
| 3 | **A and D.** `clip_out=` and `difference()` (no `intersection()`, P1); the record refused by 0.8.0; the rehearsal look's flags. Done | `NOTES-step3.md` |
| 4 | **B.** The soft hold, as the painter chose: B1, per hold and per stretch (answers 2a, 2b). Done | `NOTES-step4.md` |
| 5 | **C.** The rules as they are, as the painter chose after the bench (3b, 4a); `habits=` per place; the signature left out of the pass rule; standing lines on change (C5). Done | `NOTES-step5.md` |
| 6 | **E and F.** `.rotated()` in pixels, `aspect=` required; the frame with `.arc()` (P4); `shares=` and its line, a part by the name in its note (P5). Not a session in pixels (Q5). Done | `NOTES-step6.md` |
| 7 | **G and H.** The direction notice as measured (G1); the low key said, and the line without one (H1, H2). Done. G2 (a) built and held, asked back | `NOTES-step7.md`, `questions-step7/` |
| 8 | **I2 to I5.** The recipes and sentences, the pixel paragraph, the painter's lines in the changelog | `NOTES-step8.md` |
| 9 | **I1.** The one-page card and the measured cuts; the reading path counted | `NOTES-step9.md` |
| 10 | **The cut.** 0.9.0 without the claim; then, on the owner's word, the tag; then the claim | `CHANGELOG.md` |

Steps 3 to 8 can move once their questions are answered; step 9 waits for P8 and the
inventory.

---

## 8. Risks

| Risk | Answer |
|---|---|
| A soft hold becomes the new habit, and every edge blurs | the `edges:` line will show it; the recipes say which edges to lose; the default stays hard |
| A narrowed rule loses a true positive | each candidate is replayed over the corpus, and its known true positives are the test |
| A declared habit silences what it should not | one habit per declaration, with a reason quoted back at the end; the count still prints |
| An older build replays a new record wrongly | the record is shaped so 0.8.0 refuses it, and a test runs `v0.8.0` against it |
| The cuts remove a rule some painter needed | each cut is measured against a notice that says the same thing at the call; nothing is cut on this painter's word alone |
| One painter, and not an independent one | it read two earlier painters' notes; where it repeats them, its rows say so |
| `ubuntu-latest` moves to Ubuntu 26 from 2026-10-19 | the first CI run after it may meet a `setup-python` gap; watch the cut's run |

---

## 9. File map: what will change

| File | Steps |
|---|---|
| `paintings/Claude/uktarl_krannoc/` | 1, and the painter's answers |
| `paintings/Claude/the_curator/` | 1b, and the second painter's answers |
| `scripts/probe_curator_session.py` | 2b |
| `src/easel/session.py` | 3 (`clip_out`, the record), 4 (the soft hold), 5 (rules, `habits`), 6 (`shares` line), 7 (direction notices, key line) |
| `src/easel/regions.py` | 3 (`intersection`, `difference`), 6 (`rotated`, the frame) |
| `src/easel/plan.py`, `src/easel/checklist.py` | 5 (`habits`), 6 (`shares`), 7 (the `values:` line) |
| `src/easel/cli.py`, `src/easel/mcp_server.py` | 3 (the look's flags), and every new argument |
| `src/easel/notices.py` | 7 (a direction notice's code), and `REBUILDS` if any fix moves a rebuild |
| `PAINTER.md`, `RECIPES.md`, `REFERENCE.md`, `PAINTING.md` | 8, 9 |
| `CALIBRATION.md`, `LESSONS.md`, `SUGGESTIONS.md` | every step |
| `scripts/probe_uktarl_session.py` | 2, and a flag per later step that measures the build |
| `tests/` | every engine step, and `test_guide.py`'s card budget in 9 |
| `CHANGELOG.md`, `pyproject.toml`, `src/easel/__init__.py`, `server.json` | 10 |
