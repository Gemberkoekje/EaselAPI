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
changes. Next: the owner pastes the questions into the painting session; then step 2.**

This plan is written the way its own documentation item asks: the rule or the finding
first, then the number, then the history if it is needed.

---

## 1. What this round is

**One painter, painting against 0.8.0 the day it shipped.** `claude-opus-5-5`, at max
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
| 2 | **Edges are hard or ragged, never soft.** `feather=` breaks an edge but doesn't soften it; losing one costs a smudge per tenth of the canvas, so `edge="hard"` is the easy path. 59% crisp edges; *cut paper* | M | **Confirmed.** 43 of 44 masses are held, all but the wall, every one at the default feather `0.002`; 81 of 181 hand-laid marks are clipped. `edges:` read 70% under 2.5 px after the wall and 59% at the end. Two edges were lost, one smudge each, in the last pass. `RECIPES.md` says a smudge loses a stretch under a tenth of the canvas, and past that, paint across. **History:** 0.7.0 benched a 2-px Gaussian feather on every hold (64% → 9% hard), which read as blur, not paint, and its painter chose the broken edge from four candidates, blind. 0.8.0 measured `feather=` wider than the default as fur. **What is new:** a softness chosen per call, for the edges a painter means to lose, not a default | **4B** |
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

### For the painter, batch 2, after step 2

The soft edge's candidates, blind, on its own picture; the disc rule's candidates on the
corpus's crops where they disagree; and anything step 2 finds that turns on the eye.

---

## 7. Order of work

| Step | What | Leaves |
|---|---|---|
| 1 | **The record.** The painting filed, the verdict checked, the round opened, the questions written | this PR, `NOTES-step1.md` |
| 2 | **Measure.** `scripts/probe_uktarl_session.py`: the rebuild, and a flag per workstream: `--clip-out`, `--soft` (sheets), `--rules` (the corpus replayed with each candidate), `--direction`, `--key`, `--shares`, `--reading` (the documents' inventory). The corpus replay cached as 0.8.0's was, and copied out before a later flag writes over it | `NOTES-step2.md`, `CALIBRATION.md`'s round, batch 2 |
| 3 | **A and D.** `clip_out=`, `intersection()`, `difference()`; the record refused by 0.8.0; the rehearsal look's flags | `NOTES-step3.md` |
| 4 | **B.** The soft hold, as the painter chooses | `NOTES-step4.md` |
| 5 | **C.** The three rules narrowed as the corpus allows; `habits=` | `NOTES-step5.md` |
| 6 | **E and F.** `.rotated()`, the frame; `shares=` and its line | `NOTES-step6.md` |
| 7 | **G and H.** The direction notices as measured; the low key said, and the line without one | `NOTES-step7.md` |
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
