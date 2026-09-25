# Plan: act on the lighthouse handover's verdict on 0.6.0, and cut 0.7.0

_To understand this, start by reading: this file; then [`LESSONS.md`](LESSONS.md),
whose rules for how the engine and the guide may change bind every row below; then
[`paintings/Claude/lighthouse_handover/verdict.md`](paintings/Claude/lighthouse_handover/verdict.md),
the [`NOTES.md`](paintings/Claude/lighthouse_handover/NOTES.md) beside it, which say what
the painter found and which of its claims survived being re-measured, and
[`answers.md`](paintings/Claude/lighthouse_handover/answers.md), the painter's answers to
this plan's questions, which are the decisions this round runs under; then the three
places in the engine most of this lands -- `Session._clip_cover` in
`src/easel/session.py` (the mask a hard edge is cut with), the tooth gate in
`Canvas.stamp` in `src/easel/canvas.py` (where dry brush comes from), and
`_graded_band` in `session.py` (the rule that misfired). [`PLAN-0.6.0.md`](https://github.com/Gemberkoekje/EaselAPI/blob/v0.6.0/PLAN-0.6.0.md)
is the round before this one and the shape most of the conventions here come from._

**Status: written 2026-09-23 against `main` at `3d6fe74`, which is `v0.6.0`, and
revised the same day with the decisions taken. Steps 1 and 2 are done, and so are the
five questions step 2 left, answered by the painter the same day and recorded at the end
of section 5: A2 at `0.002` on every hard edge and every clip, inward; B1+B2, tuned to
lay today's paint; the graded rule narrowed by the overlap break alone; D1 declined.
Step 3 is built -- E and C0, `NOTES-step3.md` -- and corrected two statements of this
plan on the way, each marked where it stands: `sketch=False` has always hidden the
guides, so `guides=` was not built, and `REFERENCE.md`'s grammar named three kinds, not
five. Step 4 is built -- F, `NOTES-step4.md` -- with two things the plan did not say,
each marked in 4F: a session loaded from a file records no frames and its film is
rebuilt at its own frame size, and the notice is said at load, in the shell and through
the server alike. Step 5 is built -- A, `NOTES-step5.md` -- with three things the plan did
not say, each marked in 4A: a thin shape breaks over a quarter of its width, nothing
lands on the drawn line and the frame is not an edge, and two masses held to one line
leave the ground between them, which no committed painting does. Step 6 is built -- B,
`NOTES-step6.md` -- with three things the plan did not say, each marked in 4B: a brush
drags only as it runs dry, so a loaded mark lays exactly what it laid; the comb lays what
the stroke would stroke by stroke, not only on average; and a rebuild moves every mark
that ran dry, not the sixteen laid starved. Step 7 is built -- C2, `NOTES-step7.md` --
with two things the plan did not say, each marked in 4C: the one pass the break fires on
that the rule missed, the pier's water, is told about a reflection's brush and not the
field's; and the hands' finger, whose reading decided the gate, looks different since step
6 and was read again by the owner -- still not bars. Step 8 is built -- D0, `NOTES-step8.md`
-- with three things the plan did not say, each marked in 4D: a version that raises is said
and the others are still rehearsed; the Python form takes a function as well as a plan, and
stops one that paints the painting; and the MCP `run` answers as a list now, so that its
sheet can come back beside the text. Step 9 is written -- G, `NOTES-step9.md` -- with
three things the plan did not say, each marked in 4G: the fade's number was the plan's own
reasoning and wrong -- a quarter pressure lays two-thirds of the step, not a quarter; this
file's *graded-field recipe's measurement* is no section of `CALIBRATION.md`, so the wet
ramps went under *`scumble`*; and the signposts' sizes had gone stale -- the card is 1,369
words where six places said a thousand or under -- and say what they are. Step 10 -- the
cut -- is under way: the version is 0.7.0 and `CHANGELOG.md` has its entry without the
claim, so the tag and then the claim are what is left. This file and the step notes stay
through the tag, so `v0.7.0` carries them, and leave in the PR that adds the claim; what
survives of them and is written nowhere else is in `SUGGESTIONS.md`, under *What the
round left open*.**
Step 2 is `scripts/probe_handover_session.py` and `probe_cohort_session.py --graded`;
their numbers are in `CALIBRATION.md` under *The lighthouse handover's round*, their
sheets under `out/handover/` and `out/graded/`, and `NOTES-step2.md` says what they
decided and what surprised. The
painting is filed (`paintings/Claude/lighthouse_handover/`, a section in `PAINTINGS.md`,
an entry in the corpus probe), every number in section 3 was measured on this machine
on the checkout's own engine, and the two misfires the plan could not reproduce at first
were reconstructed by the painter, reproduced here exactly, and are filed beside the
painting. **The nine questions in section 5 were put to the owner and answered by the
painter**: the owner's ruling is that the tool is for painters and the owner is not
one, so the answers are a painter's, forwarded as the decisions. Where the painter said
it had no evidence -- which edge candidate reads as paint, whether a parallel sheet
pays -- the bench decides, as before. **Step 1 finished** with the round open at the top
of `SUGGESTIONS.md` -- six engine items and four documentation items, the right-hand
column blank -- and with 0.6.0's claim, which had waited on its tag: `CHANGELOG.md` says
it shipped, and `PLAN-0.6.0.md` and its step notes left the repository, so this round's
own `NOTES-step<N>.md` start from an empty root. Two statements here were corrected on
the way, each marked where it stands: the `edges:` line did not print 54% on every
pass (it read 54% to 65% from the sea's pass on), and finding 15's count does not move.

---

## 1. What this round is

**One painter, painting against 0.6.0 from the package.** `claude-opus-5-5`, at max
effort, installed `easel-paint` 0.6.0 in a sandbox, read every document the package
ships except `CALIBRATION.md` before its first mark -- `easel guide --full`,
`--painting`, `--recipes`, `--reference` and `--diagnosis`, 194 KB -- ran `easel demo
mistakes` and five of the nine exercises, and painted a lighthouse at dusk in 171 of
300 marks. Then it wrote a verdict on the tool, the documentation and its own picture,
and **checked its claims with small tests before making them**, dropping two that did
not survive. That is the labelling `LESSONS.md` asks every round for, done unasked, and
it is why the verdict is worth a round of its own rather than a row in the next
cohort's: most of its claims come with a number, the tests behind them came with the
delivery (`verify/verify.py`), and when the plan's first draft could not reproduce the
one claim that had none, the painter rebuilt it from its transcript and sent it
(`misfires/`).

**It is also the first fresh session to paint against 0.6.0's hypotheses**, which
`PLAN-0.6.0.md`'s workstream H left to the owner's own run. Read as that run:

- **The way in did not shorten the reading.** The card says *read the first hour, run
  `easel demo mistakes`, paint the exercises, and start*; the painter read all five
  documents first anyway, and calls the set *too heavy*. One data point, against the
  prediction in `LESSONS.md` that a shorter corpus reaches its subject earlier. What
  steered it, by its own account, was the notices at the call, the recipes with
  `demo`, and the plan's `lightest:` line; it never opened `CALIBRATION.md` or
  `DIAGNOSIS.md` and **never ran `explain` or `diagnose`** -- *the one-line notices
  were enough* -- which is the first data point on the question 0.6.0 left open about
  linking notice codes to the symptom index, and it says neither command was reached
  for.
- **The cut-out risk materialised, and the counterweight did not hold it.** The 0.6.0
  plan's risk table said the new remedies push toward `edge="hard"` and `clip=`, and
  named the `edges:` line as the counterweight. This painter laid its tower and
  headland as clipped strokes and hard masses, the `edges:` line printed between
  **54% and 65%** of edges under 2.5 px after every pass from the sea's on -- the range
  of the two cohort painters who called their own pictures *flat cut-out shapes* -- and
  the painter relied on the hard edge regardless, then named it *the least paint-like
  thing in the engine*. A measurement line printed eleven times changed nothing. That
  is *warning is not method* arriving for a number, and it is what section 4A is for.
  *(Corrected in step 1: this said 54% on every pass from the fourth; the rebuild, pass
  by pass, reads 19% after the sky, then 60, 64, 65, 63, 59, 57, 57, 57, 56, 54, 54.)*
- **The plan object, the notices and the demos worked as designed.** All of
  `s.plan(...)` was declared, `bands="subject"` turned the bars warning into the
  crossing count, the `lightest:` line caught the lantern losing to the glow at `0.74`
  against `0.77` -- *the one number my whole idea depended on* -- and the two passages
  the painter rates best came from recipes and `easel demo`. Over 13 passes the tool
  said one thing at a call and two after a pass, both in the question form the plan
  buys. The noise target holds.
- **Reading the rule did not stop the mistake, again.** *I read three rules and then
  broke them anyway: go back to the drawing after two failures, no slabs on a hull, no
  spoon-shaped islands. Looking at rehearsals caught those, not reading.* The eighth
  painter to say so; `LESSONS.md`'s first rule, from the other side.
- **The budget was left again, though not by finding 15's measure.** 129 of 300
  unspent, the `unspent:` line said so, and the painter stopped anyway -- *partly
  caution* -- at 57% of its budget, which is past the 45% the cohort's five were counted
  under. Nothing in the engine can act on that, and section 4H says so. *(Corrected in
  step 1: this said finding 15 recurred.)*
- **A rebuild is to the stroke everywhere and to the pixel on one machine.** The
  thirteen passes rebuild the log identically here and the export differs from the
  painter's by 729 pixels at one 8-bit level, from a mixture two builds of numpy round
  differently in the seventh decimal. `PAINTINGS.md`'s *byte for byte* is a claim about
  one machine; [#70](https://github.com/Gemberkoekje/EaselAPI/issues/70) gains a line.

**Scope.** Fix what the verdict measured, where the measurement stands; say so where it
did not; and record the rest. Four items are the engine's (an edge that is a step, a
starved brush that speckles, a rule that misfired, a variant that takes fifteen
seconds), three are the tool's surface (the looking flags, the plan grammar's
documentation, the session file), three are the documentation's (a backwards sentence,
a caveat far from its rule, the weight), and one is the painter's own. The release is
**0.7.0**: a default moves, the file's contents change, and one fix changes what a
rebuild lays -- and a session saved before it will be told so when it is rebuilt.

---

## 2. The rules this plan works under

From `LESSONS.md` and the last round, restated because every row below is held to them.

1. **Measure the condition before writing the rule.** Every engine candidate here has a
   bench behind it already (section 3), and each is built only on the bench rebuilt as
   a probe script, at a painting's size, looked at.
2. **Ask what the rule says to a painter doing the right thing.** Every guide block runs
   notice-clean in CI, and every demo fails exactly the way it says; both stay true
   through this round. A rule narrowed for this painter's two misfires keeps the
   corpus's true positives, or it is not narrowed.
3. **A default is worth more than a warning** -- measure the curve, move the default,
   warn about the far end. One default moves here, on the painter's own ruling.
4. **Warning is not method, and neither is a measurement.** Where a line was printed
   and did not change what the painter did, the answer is in the engine, not in a
   louder line.
5. **One engine change per paragraph, the paragraph leaving in the same commit.** The
   documentation rows are three sentences, not a rewrite; nothing is cut on one
   painter's word -- and the painter's own word is *watch*.
6. **Nothing new may touch the log index or the random stream.** A feather, a saved
   report, a gate that streaks, a version stamp -- each lives beside the log or in a
   record's own parameters, never in the sequence.
7. **A fix that changes how a saved stroke replays is named under its version**, as the
   smudge was under 0.6.0 -- and, from this round, said at load to the file it moves.
8. **Each landed step leaves a `NOTES-step<N>.md` beside it**, and the next step starts
   by reading the newest.

---

## 3. The verdict, checked

*Kind* is the project's own distinction -- **M** measured by the painter, **O**
observed, **R** reasoned -- assigned here, since the painter labelled its tests rather
than its claims. Every *what checking found* was measured on this machine on
2026-09-23, on the checkout at `v0.6.0`, with the painter's own scripts and session
file.

| # | What the painter said | Kind | What checking found | Goes to |
|---|---|---|---|---|
| 1 | **Hard edges are all-or-nothing**: `0.59` to `0.28` in one pixel at the tower, `0.36` to `0.17` at the waterline; *the least paint-like thing in the engine, and I relied on it* | M | **Confirmed to the hundredth**: `0.30` in one pixel on the tower's left side, `0.28` on its right, `0.19` at the waterline, `0.44` where the headland meets the sky. The clip mask is `Polygon.coverage(samples=2)`, which leaves **exactly one fractional pixel per side** at the tower's row. The `edges:` line said 54% to 65% on every pass from the sea's. Benched: a Gaussian feather of 2 px on the same two strokes takes the step to `0.10` and the picture's hard share from 64% to **9%**, at no cost in time -- and reads as blur, not paint. **The painter's answer sharpens it**: the jaggies are invisible at 1024x768 unless you zoom; what read as vector graphics was the clean, uniform edge. And of its 33 hard or clipped calls, 9 draw an edge and 24 only keep paint inside a shape, which a feather that reaches outward would break. | **4A** |
| 2 | **Dry-brush speckle reads as dirt** more often than texture: the flecks in the sky, the first try at the swells | O | **Measured on the sky's own crosser** (`bristle`, size 0.065, opacity 0.40): at `load=0.45` it lands **3,705 px in 509 pieces, median 4 px**, 58% of the pieces under 4 px and no body to speak of; at `0.30`, 363 pieces carrying 39% of the paint in pieces of 4 px or under; at `0.80`, 374 pieces with a median of 8 px and 1% of the paint in specks. The gate is per pixel at the weave's scale, so a starved brush leaves confetti rather than the broken streaks a comb leaves. The painter used the loads the guide recommends for broken marks, 0.35 to 0.6, and got dots; its workaround, films for the swells, dropped the texture it wanted. | **4B** |
| 3 | **One check misfired**: *graded passage laid too narrow* flagged marks that were not one, twice | O, then **M** | **Not reproducible from the scripts** -- the line fires on none of the thirteen committed passes -- because both fires were printed by rehearsals of passes rewritten before they were committed, and nothing records what a pass's check said. **Then reproduced**: the painter rebuilt both from its transcript, and re-run here each prints its original line exactly (`misfires/`). In both, the brush the line names is a thin dark accent laid among wide marks -- a `0.006` crevice along the join of two rock faces laid at `0.03` and `0.07`; a `0.006` ripple among glints -- and the rule judges a stack's step against its *narrowest* brush. In the water case the run is five glints of one colour, a foam mark and a ripple that never overlap along the stack's axis. Over the corpus the rule fires on 9 of 325 passes (3%), never on a guide block. | **4C** |
| 4 | **About 15 s per variant**, in the one run timed | M | **Confirmed, and it is the paint.** A three-band sky variant as the painter's `harness.py` ran it takes **11.5 s** here: 10.3 s the three 8-pass scumbles at full width, 0.15 s the look, 0.01 s the copy. One band is 3.1 s, 0.39 s a pass. A `rehearse(vary=)` sheet of the same band at two sizes takes 10.2 s. The bookkeeping 0.6.0 cut is gone; what is left is the dab loop. The painter never used `vary=`: its variants were whole passes, and what it wanted was scripts rehearsed as alternatives side by side, which `easel run --rehearse a.py b.py` does not do -- it stacks them on one copy. | **4D** |
| 5 | **The built-in side-by-side comparison doesn't support soft blends or glazes** | R | **It does.** `{"points": ..., "glaze": True, "color": ..., "opacity": ...}` is a stroke entry, as is `{"points": ..., "smudge": 1.0}`; a sheet of three opacities of the beam's own glaze rendered in 1.7 s and adopted `glaze-far` per panel. **No document says so** -- `REFERENCE.md`'s plan grammar names a stroke, a mass, a sweep, a scumble and a burial -- which is the whole of the gap, and the painter's answer to question 6 makes it twice: *whole passes of scumbles, strokes and glazes, which as far as I could tell can't go into a plan*. *(Corrected in step 3: `REFERENCE.md` named three of the five kinds, a mark, a mass and a sweep; only the MCP server's plan help named the passage and the burial.)* | **4E** |
| 6 | **`easel look` has `--no-sketch` but no `--no-marks`**, so landmark labels covered small details; wrote a helper | M | **Confirmed, and one worse.** `look(marks=False)` exists in the API and `PAINTING.md` names it; the CLI has no flag for it, the MCP `look` tool has no `marks` argument, and **nothing at any level hides the guides** -- `look()` has no `guides=` and `render_look` always draws them. The painter's helper still shows every guide line it drew. *(Corrected in step 3: `render_look` draws the guides only when `sketch` is on, so `sketch=False` hides them with the pencil and always has, and the helper passes it -- a look with a guide drawn and `sketch=False` differs from one with none in no pixel. What was missing was anything saying so.)* | **4E** |
| 7 | **Session files are large**: 16 MB after 171 marks | M | **16.11 MB, and 55% of it is the time-lapse.** 174 frames at 360 px, stored raw, 8.83 MB; the canvas 6.57 (float32 at 1024x768); the log 0.29; the last look 0.28. Re-saved: frames out, **7.64 MB**; colour as float16, 12.26 -- and float16 moves 20,385 export pixels (2.6%) by one level, which breaks *opens as it was painted*; frames as PNG bytes, 6.76 for 8.83, not worth a format. The painter exported its GIF once, at the end, and verified that the rebuild from the log is pixel-exact on its machine, in about 35 s. | **4F** |
| 8 | **A vertical seam** blamed on the sky blends did not reproduce; *probably how I layered wet paint* | O, withdrawn | **Not reproduced here either**, wet or dried: the three committed sky ramps laid on a fresh canvas show a median column jump of `0.0002` and their largest jumps at the canvas edges. Drying between the bands moves **34% of the canvas by more than two 8-bit levels** and 14% by more than eight, so the wet layering is real and large; it draws no seam. No row. Recorded under the graded-field recipe in `CALIBRATION.md` as a number, not a rule -- `wet-under` was declined in 0.6.0 and nothing here reopens it. | 4G, one line |
| 9 | **Too much text**: ~340 KB across six documents, ~180 KB read before the first mark; *essay-like, dense cross-references, key facts buried in paragraphs* | M | **The sizes are right**: 341 KB for the six, 194 for the five it read (`PAINTER.md` 6,654 words, `PAINTING.md` 7,390, `RECIPES.md` 7,703, `REFERENCE.md` 7,690, `DIAGNOSIS.md` 2,131). **The reading was the painter's choice**: the card's first paragraph says to start after *The first hour*, and it is the second painter in two rounds to read everything anyway. Asked, the painter's own answer is *watch* -- and *if you ever cut, start with what the notices already say at the call*. `LESSONS.md` has watched cuts fail on n=1 and forbids one here. | **4G** |
| 10 | **A caveat far from its rule**: `RECIPES.md` says a pressure list fades a soft blend to nothing at one end; measured `0.86` to `0.41` on a `0.14` field at opacity 0.9, `0.29` at 0.5 | M | **Both are right, about different things.** The painter's test is a scumble with `pressure=[1.0, 0.75, 0.25, 0.0]`, read over the right *third*, where the profile still averages a quarter pressure: 0.858 / 0.787 / 0.408 by thirds on a 0.149 field here, and **0.201 over the last 4% of the width** -- it does reach nothing, at the end. *(Corrected after step 2, by the painter: over the last 4% it reads `0.183`, still `0.034` above the field at opacity 0.9 and `0.018` at 0.5 -- close, and not arrived.)* The recipe's own passage, `pressure=[0.0, 0.55, 1.0]` on six `flat` strokes, reads 0.162 on a 0.156 field at its no-pressure end. What the recipe does not say is how fast the fade arrives: a quarter pressure still lays a quarter of a value step, because dabs overlap and accumulate -- the sentence that lives in `PAINTING.md` under *opacity does not thin a long stroke*. *(Corrected in step 9, measured: a quarter pressure lays two-thirds of the step on this band at opacity 0.9 and 0.56 of it on the recipe's own at 0.5, and the right third averages `0.135` of full pressure, not a quarter -- the passes run from frame to frame.)* | **4G** |
| 11 | **One sentence is backwards**: the lit-air recipe says `[1.0 ... 0.1]` is *narrow-and-bright at the source and wide-and-gone at the far end*; measured 80 px at the source and 32 at the far end | M | **Confirmed against the source.** A round tip's width follows pressure (`stroke.py`, `_PRESS_WIDTH_FLOOR = 0.35`; `CALIBRATION.md`'s *Pressure* table: 14 px at 0.10, 36 px at 1.00). Full pressure is the wide end. The recipe's code is right and its sentence is not -- *the one factual error I found was in prose*. | **4G** |
| 12 | **The painting**: competent, coherent, conventional; the headland failed twice and was patched with brushwork; 43% unspent, partly caution; would paint a later dusk, decide fewer larger planes while still a drawing, let the headland dissolve, let the ground show | O | The check's line is the one `LESSONS.md` restated in 0.6.0: it reads marks and measures the canvas, and does not judge an arrangement. `unspent:` printed 129; `ground:` printed `0.00%` and, as the plan said `buried`, asked for nothing. A *repainted passage* count was considered and dropped: the headland took four passes and so did the tower, and the log cannot tell a repair from a subject being developed. Recorded. | **4H** |

**What the painter defended, unprompted, and this plan does not touch:** rehearsal
seeded as the next real strokes (*exactly what lands when you commit it*), the notices
naming the problem and the fix, the plan object held against the checklist, `cost_line`
finding a 32-mark cliff face where 15 did the job, an error message carrying the exact
numbers, and learning the tool from the command line without opening a file.

---

## 4. Workstreams

### A. An edge that is not a step

**What is there.** `edge="hard"` and `clip=` multiply every dab by a coverage mask the
outline is rasterised to at two samples per axis (`Polygon.coverage`), so a boundary is
one pixel of four possible values and then a step. `cover()` has laid its patch that way
by default since 0.6.0, and `chisel-staircase`, `spill` and `clean-small` each name
`edge="hard"` or `clip=` as a remedy. The `edges:` line counts the result and cannot
change it. Before this painting one committed script uses `clip=` -- GPT's single-file
`paint.py`, thirteen times -- and eighteen literal `edge="hard"` sites in eight scripts
do, 55 calls at replay by F5's count; this painting adds 33 calls, and **the painter's
own count of them is the design constraint**: 9 draw an edge (the headland outline, two
sea stacks, the cap, the horizon, the tower, its lit side and the lantern) and **24 only
keep paint inside a shape** -- the rock planes and ledges inside the headland, the
reflection films below the horizon, the door and the warm film inside the tower.

**Two uses, and only one of them wants softening.** A feather that reaches outward
across the outline breaks containment: the planes would leave a lighter fringe around
the dark headland, which is an outline -- mistake one on the card -- and the reflection
film would leak above the horizon. So **every feather is inward**: the ramp lies inside
the outline, from full coverage at the feather's depth to nothing at the drawn line,
and nothing lands outside the place any more than it does today. `cover()`'s patch
stays inside its place by the same construction. And the horizon was a ruled line on
purpose, so `feather=0` stays available.

**The bench so far** (session scratchpad, to be rebuilt as a probe): the tower's two
clipped strokes on a flat field at 1024x768, the coverage mask blurred with a Gaussian
of sigma *f* before it is used -- a *centred* feather, which is the one thing the build
must not do; the numbers stand as the shape of the curve.

| feather | largest one-pixel step | `edges:` share under 2.5 px | median rise | the two strokes |
|---|---|---|---|---|
| 0 px (today) | `0.28` | 64% | 2.0 px | 0.20 s |
| 1 px | `0.14` | 26% | 3.0 px | 0.24 s |
| 2 px | `0.10` | 9% | 4.1 px | 0.18 s |
| 3 px | `0.12` | 14% | 4.7 px | 0.23 s |
| 5 px | `0.11` | 23% | 4.8 px | 0.22 s |

*(Step 2 rebuilt this bench inward, and the knee moved: an inward ramp over `F` pixels
rises over about `F/1.5`, so A1 at 2 px barely moves the line -- 77% to 69% -- and only
halves it at 5 px. `CALIBRATION.md`, *The lighthouse handover's round*.)* Two pixels is
the knee, it costs nothing, **and looked at it reads as blur**: the
tower's stair-stepped side becomes a smooth soft edge, which is a different wrong thing
-- and the painter says the staircase was never the problem, the uniform edge was. A
painted hard edge is neither -- it is crisp *and* broken, because the brush meets the
tooth at the boundary and the boundary itself is a hand's line, not a ruler's.

| Candidate | What it does | Standing |
|---|---|---|
| **A1 feather** | the coverage mask ramped inward over `feather` (a fraction of the long side, like `size`; `0.002` is 2 px at 1024 and 3 at 1440) | the control; benched centred, reads as blur; expected to lose |
| **A2 feather broken by the tooth** | inside the inward ramp the mask is thresholded against the canvas's own tooth field, so the boundary breaks at the weave's scale the way a loaded brush's edge does over tooth, and stays crisp where the tooth is high | the candidate for made things -- *the tower, lantern and cap wanted crisp-but-painted edges, not wandering ones* |
| **A3 the outline itself wanders** | a shape helper, `roughen(shape, amp, step, seed, calm=)`, in `regions.py` beside `blob` and `ribbon`: the painter's own correlated random walk along the outline, calmed where something stands on it -- *if A3 existed as a shape option, I'd have used it for rock* | built as the helper, not as a mask displacement; the painter's fifteen lines are its specification |

Bench A1 and A2 inward at 1024x768 and 1440x960 on the tower, on a rock silhouette
(with and without `roughen()`), on a containment clip at the same feather (the planes
inside the headland, to see whether the rim of underlayer it leaves reads as an
outline), and on `cover()`'s patch over a worked passage (F1's bench from 0.6.0) -- and
**look**; the `edges:` line and the one-pixel step are the numbers and the eye is the
verdict, which the painter cannot give because it has not seen them. Then:

- **`feather=`** on every verb that takes `clip=`, and on `block_in`, `cover` and
  `scumble` under `edge="hard"`. Rides in the log beside `clip` (`params["feather"]`),
  so a saved stroke replays as it was laid and a log without the key replays at `0`. It
  joins `_clip_cover`'s memo key, because *anything a mask is computed from has to be in
  its cache key* (`LESSONS.md`, trap 5) and a mass's passes share the memo. Built with
  PIL's own filters on the coverage image; nothing new is imported.
- **The default, decided again after step 2 (questions 10 and 11): A2 at `0.002`, on
  `edge="hard"` and on `clip=` alike, inward.** The first reading of the painter's
  answer 1 -- `edge="hard"` feathers, `clip=` keeps `0` -- was the plan's, and step 2
  showed it missed the tower, its lit side and the lantern, which are clips; the painter
  called it a mistranslation of its own answer, whose only reason for keeping clips
  hard was an outward feather. Inward, a clip cannot carry paint past its outline, and
  the containment bench shows no rim. So every hard edge and every clip moves: the
  eighteen `edge="hard"` sites, this painting's 33 calls, GPT's thirteen clips and every
  `cover()`, with goldens opened and looked at (`LESSONS.md`, trap 2); a moved default
  never reaches a saved log. The painter chose A2 blind, before it knew which letter was
  the bench's pick. A painter who wants a ruled line passes `feather=0` -- the horizon
  of this painting is that line. **One bench is left for the build**: at 1440x960 the
  painter found A2 at `0.002` *a little chewed*, and the tooth it breaks against is half
  a weave that scales with the canvas (a thread is 1/130 of the long side) and half a
  grain that does not (about 3 px at any size). Bench the feather as a share of the long
  side against a pixel count at 1440 before fixing its unit.
- **For rock, `roughen()` and the default edge on top of it**, no wider feather (the
  painter's answer to 10b): on the headland the outline moved the picture more than
  any feather did.
- The notices that name `edge="hard"` as a remedy name the feathered form, in the same
  commit; `PAINTING.md`'s *Masses that are not rectangles* gains one sentence,
  `REFERENCE.md` the argument and the helper. Nothing leaves.

*(Built in step 5, `NOTES-step5.md`, as decided -- A2 at `0.002` on every hold, inward,
`roughen()` beside it -- and with three things the plan did not say. **The unit stayed a
share of the long side**: built, the edge at 1440 bites at the export's own pixels as
1024's does (`0.94` against `0.94`), where the bench's copy the painter found chewed
measured `1.32`, and a two-pixel count is no closer. **Nothing lands on or past the drawn
line, and a side on the canvas frame is not an edge** -- the copy let the weave's peaks
through on the line and broke the frame. **A shape narrower than four feathers breaks over
a quarter of its width**: ramped over the whole feather, a clip two pixels wide kept 37%
of its paint. And **two masses held to one line on bare ground both break back from it**,
leaving a broken line of ground between them -- 14.6% of the band on the seam; over the
ten corpus paintings whose scripts hold an edge the longest run of ground the feather
uncovers is 12 px, so it is a number and not a check, and the one `RECIPES.md` passage
that laid masses that way lays its first past the line. The step-2 risk *a rim that reads
as an outline* was the seam, not the containment clip.)*

### B. Dry brush that streaks rather than speckles

**Decided: the engine.** *A notice would only have told me to avoid the mark. I'd still
have had no dry-brush mark that works.* **And after step 2 (question 12): B1+B2, tuned so
each load lays about today's paint** -- *the amount was right, the shape was wrong*. B1
keeps the tooth's whole distribution, not two moments of it, and B2's spread is set
until the painting's broken-mark loads lay what they lay now. Blind, the painter ranked
B2 alone slightly above B1+B2 on bristles (B1+B2 read *a bit combed*) and took B1+B2 for
B1's reach to flats and rounds, which B2 has none of. So after tuning, look at the
crosser at `0.45` with B2 and B1+B2 side by side, and if B1+B2 still reads combed,
shorten B1's kernel on a tip that has a comb.

**What is there.** As a brush runs out, `Canvas.stamp` gates each dab against the
canvas tooth per pixel (`need = (1 - load) x sensitivity`, a smoothstep over a band of
`0.18`), so what a starved brush leaves is exactly the pixels whose tooth clears the
threshold: the weave's peaks, at the weave's scale, wherever the mark passes. A real
dry brush leaves *streaks* -- the comb's bristles, some of them empty, dragging along
the travel -- and the engine draws that comb per stroke (`brush.bristles`) but lets the
tooth, not the comb, decide what lands when the load is low. The measured result at
`load=0.45` is 509 pieces with a median of 4 px, at a median contrast of `0.009`:
confetti at low contrast, which is what dirt looks like, at the loads the guide
recommends for a broken mark.

| Candidate | What it does | What to measure |
|---|---|---|
| **B1 the tooth read along the travel** | the tooth field the gate reads is smoothed by a short kernel *along the stroke's direction* before thresholding, so what clears it is a run of pixels, not one | piece count, median piece size, the elongation of pieces along the travel, at loads 0.3 to 0.8 |
| **B2 starvation per bristle** | the comb the stroke already draws carries the load: bristles run out individually, and an empty bristle lays nothing whatever the tooth | the same, and whether the mark keeps a body at `0.45` |
| **B3 starved paint lands thin** | inside the gated regime the dab's alpha is scaled by the load as well, so a fleck is a thin fleck | contrast only; expected not to be the fix, since the contrast is already low and the fault is isolation |

Bench on the sky's crosser, on the painter's first swells and surf (its `misfires/water`
pass has both), on `RECIPES.md`'s own dry-brush block (*a mass built of planes* lays
`load=0.35` for surface), on `PAINTER.md`'s exercise 3 (*paint running out*, the four
loads on rough canvas), and on `samples/brushes.png` -- and look, at all of them,
because the sampler *shows isolated strokes at full load* and has been fooled before
(`LESSONS.md`, trap 1). **This is a fix that changes what a rebuild lays**: every
starved stroke in every saved painting replays with the new gate -- sixteen of this
painting's own, eleven `bristle` and five `flat` *(corrected in step 6: those sixteen
were laid starved on purpose; 65 of its 173 marks run dry somewhere along their length
and move)*, which its painter accepts because its
README pins 0.6.0 -- so it is named under 0.7.0 in `CHANGELOG.md` as the smudge was
under 0.6.0, said at load by F2 below, and every golden that carries a starved stroke
is opened before it is regenerated.

Not proposed until B lands: a fact at the call (*`load=0.45` at this size lands 18% of
its paint in pieces under 4 px*). If the gate change leaves the flecks where the painter
found them, that line is cheap and the tooth histogram predicts it; if it does not, the
line would be describing a fault that is gone.

*(Built in step 6, `NOTES-step6.md`, as decided -- B1+B2, tuned so each load lays what it
laid -- and with three things the plan did not say. **A brush drags only as it runs
dry**: on linen and rough the lowest tooth lies under the gate's own band, so the gate
reads the tooth even for a full brush, and a gate read along the travel wherever it
reads anything would have moved every loaded mark on those surfaces; so the drag is
blended in as the load falls from `0.9` to `0.7`, and a loaded brush lays exactly what
it laid. **The comb is matched to the stroke stroke by stroke**, each bristle weighed by
how much of the tip it is, and a bristle running out fades rather than stopping -- matched
on average, a comb whose wet bristles fell on its weakest laid half, and cut off hard a
nearly empty stroke could lay only nothing or one bristle's worth. And **the notice counts
every mark that ran dry, not the sixteen laid starved**: a brush spends its load along
every stroke and the bristle preset starts at `0.9`, so 65 of the painting's 173 marks
move, and 2,788 of the corpus's 5,628. Built side by side as the painter asked, B2 alone is dots again once it lays today's
paint, and B1+B2 is dragged rather than combed, so B1's kernel is the same on a comb. The
fact at the call is not built: at `0.45` the specks under 4 px carry 1% of the crosser's
paint, where they carried 8%.)*

### C. The rule that misfired, and the instrument that would have caught it

**The rule** (`_graded_band`) fires on five or more long parallel marks at three or
more colours, in one run with no gap wider than four brushes, turning at most once,
stepped further apart than half the narrowest brush. It fires on nine corpus passes,
never on a guide block, and on none of this painting's committed passes.

**Both misfires are now in the repository and reproduce exactly**
(`paintings/Claude/lighthouse_handover/misfires/`): the headland pass as rehearsed at
its sixth rehearsal, 42 marks, *19 marks at stepping colours run parallel 0.020 apart,
and the narrowest brush laying them is 0.006 -- 0.3 of that step*; the water pass at
its eleventh, 19 marks, *7 marks ... 0.009 apart ... 0.006 -- 0.6 of that step*. The
mechanism is in the lines. In the headland the run is the mass's `0.07` passes, the
planes' `0.03` and `0.014`, and **one `0.006` crevice** along their join; in the water it
is five glints of one colour at `0.0075` to `0.0134`, one foam mark and **one `0.006`
ripple**, adjacent down the picture and never overlapping along the stack's axis.
Neither was a gradient; in both, the rule's *narrowest brush* is an accent.

- **C0. Save what the check said, rehearsals included.** Notices are saved in the
  `.easel` file since 0.6.0; the lines `report()` prints after a pass are not, and a
  rehearsed pass's are thrown away with its copy -- which is exactly where both fires
  were printed. Each `easel run` and MCP `run` appends the pass's report block to the
  session under a `reports` key beside `notices`, a rehearsed pass's flagged as such,
  the way `_adopt_notices` already carries a copy's notices back. Read with
  `s.reports()` and `easel log --reports`. Beside the log and never in it; a key an
  older build does not read, so 0.6.0 opens the file. **Decided**, with the painter's
  rider that it is only worth having if rehearsals are in it. *(Built in step 3, counted
  passes included, each report carrying the log index its pass began at. Writing the
  file after a rehearsal needed one more change: the copy shared the painting's palette,
  landmarks and guides, so a mixture a rehearsed pass made would have been saved with
  its report. The copy has its own of all three now.)*
- **C1. Crop the nine.** The probe replays the corpus and crops the marks each of the
  nine fires counted, in finding 12's pattern, so a human can say which are a graded
  passage laid badly. The rule's own origin -- a dawn band of seven hand-laid strokes --
  is silent on the heron's first twelve passes as committed, so the nine are elsewhere
  and only the replay finds them.
- **C2. The gate, prototyped on the four cases in hand.** Two changes, each of which
  answers one misfire and neither of which touches the recipe's own failure block:

  | | headland | water | recipe failure block (must fire) | recipe passage (must stay silent) |
  |---|---|---|---|---|
  | as it stands: narrowest brush | fires | fires | fires | silent |
  | the brush judged is the run's **median** size | silent | fires | fires | silent |
  | the run breaks where consecutive marks do not **overlap along the stack's axis** by 30% of the shorter | fires | silent | fires | silent |
  | **both** | silent | silent | fires | silent |

  A graded passage is laid with one brush and its strokes lie over one another; a
  crevice among planes fails the first and a ripple beside glints fails the second.
  Both together is the candidate, held by `check_guide_blocks.py` on the recipe's
  demo and by the corpus's true positives once C1 has named them -- **a true positive
  the gate silences is a cost, and the corpus decides**, not the two cases the gate
  was drawn on.

  **Decided after step 2 (question 13): the 30% overlap break on its own.** The corpus
  decided against *both*: read blind by the painter, and on `crop_01` by the owner, the
  median clause silences every graded passage among the nine, and the overlap break
  alone keeps all of them -- `crop_04`, the pier's water, which the rule misses today,
  among them -- while silencing the painter's water misfire and half the false
  positives, three of the six. What it still fires on: the fields of separate masses
  stacked (the painter's headland misfire, the pier's `pass2_masses.py`), a slab with
  lines ruled across it that the painter calls a real fault under another name (the
  heron's `pass11_last.py`), and the inside of a bowl that is a passage and does not
  come back as bars (the hands' `pass22_bowl3.py`). The first kind wants another clause
  if it wants one at all, and none tried here is free.

  *(Built in step 7, `NOTES-step7.md`, as decided -- the overlap break at `0.30`, the
  engine's own line firing on the same 7 of 337 passes as the bench's copy, and `0.30` the
  middle of a plateau: every share from 10% to 40% fires on the same seven -- and with two
  things the plan did not say. **The pass it adds is told about the wrong brush**: the
  pier's water was one run of fourteen under the old rule, a field's nine passes and five
  reflections whose colours turned three times; broken, its longest piece is seven of the
  field's passes and one reflection, and the brush the line names is the reflection's
  `0.02` where the field's own is `0.108`. And **the reading that decided the gate was
  read again**: the painter's pick was conditional on the hands' finger reading as
  speckle, and warned that B might turn it to stripes; under step 6's gate it is crossed
  streaks, and the owner read it, before and after side by side, as still not bars.)*

### D. Rehearsing alternatives side by side

**What the painter did, and asked for.** It never used `vary=`; its variants were whole
passes -- scumbles, strokes and glazes -- run one after another through a harness
around `s.scratch()` at fifteen seconds each, and looked at as separate files. *What
would have replaced the harness is rehearsing scripts as side-by-side alternatives.*
`easel run --rehearse a.py b.py` lays them on one copy in order, which is right for a
pass that goes on top of another and wrong for two versions of the same pass.

| Candidate | What it does | Standing |
|---|---|---|
| **D0 scripts as alternatives** | `easel run --rehearse --alternatives a.py b.py c.py`: each script on its own copy of the session, its own check block, one labelled sheet the way `rehearse(vary=)` lays one, and the same on the MCP `run`. In the API, `s.rehearse_each([plan_a, plan_b])` for plans, since a function is what a script is inside Python | **built first**; sequential, so three alternatives cost three rehearsals and a painter reads them together rather than in three files |
| **D1 panels in parallel** | the panels of a sheet, `vary=` or D0, rendered in their own processes; exact by construction, since each is seeded as the next marks | **declined** (question 14): the bench's four panels took 1.6-1.7 times one, against a target of 1.5, the cost each process's load of the session file; and the painter's variants cost the paint, which no sheet takes away |
| **D2 the dab loop** | vectorise the window blend across the dabs of one stroke where their windows do not overlap | not this round; the open item in `LESSONS.md`, and a larger project than a verdict row |

The single rehearsal and the harness loop stay as they are: a painter's own helper
laying three bands pays for three bands.

*(Built in step 8, `NOTES-step8.md`, as decided -- D0: `easel run --alternatives`, `run`
with `alternatives` through the server, and `s.rehearse_each()` -- and with three things the
plan did not say. **A version that raises does not stop the others**: scripts on one copy
stop at the first that fails because the next stands on it, and no version stands on
another, so it is said, left off the sheet and out of the reports, and the run exits with
its code. **In Python a version is a plan or a function**, the function handed the copy as
the painter's harness handed each variant its own -- and one that paints the painting
instead, through a helper that reaches `s`, is stopped with the records to undo. And **the
MCP `run` answers as a list**: declared as text, the SDK holds every answer to a text
schema and refuses a picture beside it, so the sheet could not come back otherwise, and
`run` carries no `structuredContent` now. The painter's own two skies, `try_sky3.py`'s B
and C, land as their panels show them, on both sheets. One thing is left as a question for
the painter: the sheet draws each copy as a rehearsal's own look does, landmarks and
drawing included, where its harness looked at its variants without them.)*

### E. The looking tools, and the plan grammar's documentation

Small and certain; one PR, early.

- `easel look --no-marks` and `--no-guides`; `look(guides=False)` in the API, which is
  one line into `render_look(guides=)`; `marks` and `guides` on the MCP `look` tool,
  which today has `sketch` and neither. `REFERENCE.md`'s `look` line gains the
  argument, and `tests/test_reference.py` already holds every optional parameter of
  `look` to that page, so it will fail until the row is written. The painter's
  `clean_look.py` becomes two flags. *(Built in step 3 without the guides half:
  `sketch=False` already hides them -- see section 3, row 6 -- so the two flags are
  `--no-marks --no-sketch`, and what the guides needed was the flag's help and the
  docstrings saying so.)*
- The plan grammar names a glaze and a smudge, and says in one sentence that a whole
  pass -- a scumble, a stroke, a glaze -- is a plan: `REFERENCE.md` under *Looking,
  planning, measuring* (the sentence at line 369 that lists the five kinds),
  `rehearse`'s and `preview`'s docstrings, and the MCP `rehearse` tool's, each with the
  one-line entry. A test in `test_reference.py`'s pattern: every `stroke()` keyword a
  plan entry can carry is named on the page where the grammar is. *(Built in step 3
  with two changes. The sentence listed three kinds, not five, and names all five now;
  the test holds the grammar to every kind `PLAN_ACCEPTS` lays, since
  `test_every_parameter_a_painter_can_name_is_somewhere_on_the_page` already held every
  `stroke()` keyword. And **the smudge was not named**: as a mark it takes the smudge
  brush's `0.07`, the width `smudge()`'s `0.02` default was moved off, and says none of
  the verb's three notices; the film is named with the glaze verb's brush and opacity
  written out, because an entry takes a stroke's defaults.)*

### F. The session file, and what it says about the engine that saved it

**Decided: the frames leave the file.** The numbers (the painter's own file, re-saved
with each change alone):

| | size |
|---|---|
| as saved | 16.12 MB |
| the time-lapse frames left out | **7.64 MB** |
| colour as float16 | 12.26 MB -- and 2.6% of export pixels move by one level, so *opens as it was painted* would stop being true |
| both | 3.19 MB |
| frames stored as PNG bytes | 6.76 MB against 8.83 for the frames alone; not worth a format |

- **F1.** A live session keeps its frames in memory as it does now and `timelapse_gif()`
  uses them; a session loaded from disk has none and rebuilds them from the log, which
  `timelapse_gif(from_log=True)` has done at any size since 0.6.0 -- about 35 seconds
  for this painting, which is the cost, and the painter's own use (one GIF, at the
  end) is the case for paying it once. The file format does not change: `frames` is
  already written as an empty array when there are none, so a 0.6.0 build opens a
  0.7.0 file, and a 0.7.0 build reading an older file with frames in it keeps them.
  `Session(timelapse=)` is untouched. *(Built in step 4 with two changes the plan did
  not see. A session loaded from a frameless file **records no frames** -- a frame
  recorded after a load begins the film in the middle of the painting, so a script that
  loaded, painted and asked for a GIF would have had a film of its own pass -- and
  every pass from the shell or the server is such a session, so none of them pays for a
  frame; `undo`'s rebuild builds none either. And the film is rebuilt at the session's
  **frame size**, not the canvas's own, so it is the film the painting recorded, frame
  for frame; `from_log=True` keeps its meaning, any size.)*
- **F2. The engine that saved a file, and what has moved since.** The painter's rider
  on the version: its README promises a pixel-identical rebuild that relies on the
  0.6.0 pin, and B changes what its sixteen starved strokes lay. So the meta gains
  `"engine": easel.__version__` -- a new key, read with `.get`, absent from every file
  saved so far -- and a session loaded, replayed or undone from the shell under a newer
  engine says once, as a notice, which fixes since the version that saved it change
  what a rebuild lays: the same short list `CHANGELOG.md` names under each version,
  kept in `notices.py` beside the codes so `tests/test_notices.py` can hold the two
  together. A file with no key was saved by 0.6.0 or earlier and is told so. *(Built in
  step 4 as `older-engine`, a fact, **said at load** -- every undo and replay of a file
  begins with one -- and only where a fix moves something: each fix in
  `notices.REBUILDS` carries which marks it lays differently, so the notice counts them
  and a log with none is told nothing. A file without the key is dated finer than the
  plan said, by its `notices` key -- 0.6.0 wrote one on every save, nothing before it
  did -- so a 0.6.0 file is not told about 0.6.0's own smudge fix. The list starts at
  0.6.0, the first release whose entry names its rebuild fixes in a fixed form, and the
  test holds it to that form by count. And what a file says as it opens now reaches
  both surfaces: the shell prints it on stderr, headed `at load`, and the MCP server
  puts it at the top of the tool's answer, where it had gone to the server's stderr --
  `foreign-out-dir` with it.)*

### G. The documentation: three sentences and a ruling

- **G1 the backwards sentence.** *A volume of lit air*: full pressure is the wide end
  of a round tip. The sentence is rewritten to say what the code does -- `[1.0 ... 0.1]`
  is wide and bright at the source and narrow and gone at the far end, and the wide
  faint glaze runs the other way so the cone opens as it travels. The recipe's block
  and its demo are unchanged, because they were right. `CALIBRATION.md`'s *Pressure*
  table is the measurement and is cited beside it.
- **G2 the caveat beside its rule.** *A passage brightening toward one side* says each
  pass lands at no pressure on one side; it gains the number that says how quickly the
  fade arrives (*a quarter pressure still lays a quarter of the step, because dabs
  overlap -- `0.41` on a `0.15` field over the last third of a band at opacity 0.9,
  `0.20` over its last twentieth*) and one clause naming where the reason lives, so a
  painter who reads the recipe alone knows what the end of the pass will read.
  *(Corrected in step 9: the number in brackets was reasoned, and measured it is wrong
  twice -- a quarter pressure lays two-thirds of the step on this band, and the last
  twentieth reads `0.19`. The recipe carries the measured ones.)*
- **G3 the plan grammar** -- workstream E's row, listed here because it is a document
  that was wrong by omission, twice over.
- **G4 the wet layering, as a number.** Under the graded-field recipe's measurement in
  `CALIBRATION.md`: three overlapping bands laid wet change each other by more than two
  levels over a third of the canvas against the same bands dried between. A fact for a
  painter choosing; not a rule, and not `wet-under`. *(Written in step 9 under
  *`scumble`*: `CALIBRATION.md` has no section for the graded-field recipe, whose band
  and brush are measured there.)*
- **G5 the weight: watch, decided -- and recorded.** The finding is now six painters'
  -- DeepSeek, GLM, BigPickle, Kimi, this one, and the tenth session whose answer was
  the card-and-body split -- and the answer each time has been the tool absorbing rules
  rather than the prose losing them, which is what 4A and 4B do again. What this round
  records in `LESSONS.md`'s protocol section, as the data points they are: told to
  start after the first hour, the painter read everything; it never ran `explain` or
  `diagnose`, because the one-line notices were enough, which is the answer 0.6.0 said
  to wait for before linking codes to the symptom index -- **not built, on the
  evidence**; it read three rules and broke them, and the rehearsal caught them; and
  its own instruction for whichever round does cut -- *start with what the notices
  already say at the call* -- which is 0.6.0's migration map continued, and is where
  that round's section 5 already points.

*(Written in step 9, `NOTES-step9.md`, as decided -- G1, G2 and G4 on the probe's own
numbers, re-taken on the engine the round built, and the record -- and with three things
the plan did not say. **G2's number was the plan's own reasoning, and wrong**: a quarter
pressure lays two-thirds of the step on the painter's band, and 0.56 of it on the
recipe's own at its `opacity=0.5`, where a tenth still lays a quarter; the recipe says
that beside the painter's `0.41` and `0.19`, and `CALIBRATION.md` has the table under
*Pressure*. **G4 had nowhere to go by the name the plan gave it**, and went under
*`scumble`*, beside the band's own measurements. And **the signposts' sizes had gone
stale**: the card is 1,369 words where the README, `llms.txt`, the CLI's help and the MCP
`guide` tool said a thousand or under, and `llms.txt` put `REFERENCE.md` at 3,600 words
where it is 8,800 -- so every size moved with the notices' count, to what it is.)*

### H. Recorded and not built

- **The picture's composition, and the budget left.** Outside the check's line by
  `LESSONS.md`'s own restatement; `s.plan(why=)` is the instrument and it was used.
  Finding 15's count does not move: it was counted as budgeted paintings that stopped
  under 45% of budget, and this one stopped at 57% -- well short of the 86% median of
  the thirteen before the cohort, past the line the cohort's five were under.
  *(Corrected in step 1: this said the count moved to six of seven.)*
- **A repainted-passage count**, considered and dropped: the headland took four passes
  and the tower four, and the log cannot tell a passage failing from a subject being
  built. The card's rule -- *if a passage has failed twice, the fault is upstream of the
  brush* -- stays a rule the painter reads, which this one read and did not follow.
- **The seam.** Withdrawn by the painter, not reproduced here; G4 keeps the number.
- **The pressure-list claim as reported.** Both measurements are right; G2 carries the
  sentence.
- **The rebuild across machines.** One line on #70 and one in `LESSONS.md`'s environment
  papercuts: a mixture can differ in the seventh decimal between numpy builds, so
  *byte for byte* is a claim about one machine and *to the stroke* is the one that
  travels. *(Written in step 9: the papercut, the README's own claim moved to the
  stroke, and
  [the line on #70](https://github.com/Gemberkoekje/EaselAPI/issues/70#issuecomment-5824300375),
  which names `llms.txt`'s two worked examples as well as `PAINTINGS.md`'s rows.)*

---

## 5. Decisions taken

Put to the owner on 2026-09-23 with the evidence and the cost beside each; **answered
the same day by the painter**, `claude-opus-5-5`, to whom the owner forwarded them --
*this tool is for LLMs to use; any answer I give is, by definition, by someone who
would never use the tool directly* -- and filed verbatim as
[`answers.md`](paintings/Claude/lighthouse_handover/answers.md). Where the painter said
it had no evidence, the bench decides, which is what it would have decided anyway.

| # | Question | The answer | What it changes here |
|---|---|---|---|
| 1 | Does `edge="hard"` / `clip=` gain a default feather? | **Yes for `edge="hard"`; keep `clip=` hard when it is only containing paint; feather inward or not at all; `feather=0` stays available.** Of its 33 calls, 9 drew an edge and 24 contained paint; an outward feather would fringe the headland and leak the reflection above the horizon | 4A: every feather is inward; `edge="hard"` moves, `clip=` does not. *Corrected by question 11: that column was the plan's reading, and it dropped the half of the answer that mattered -- the four clips that drew an edge. `clip=` feathers too, inward* |
| 2 | Which edge candidate? | **Cannot choose; has not seen them.** Two data points: it built a wandering outline by hand and would have used A3 for rock; the tower, lantern and cap wanted crisp-but-painted edges, which sounds like A2; A1 reading as blur fits -- *aliasing wasn't the problem, the vector-clean edge was* | 4A: A1 the control, A2 the candidate for made things, A3 built as `roughen()`; the bench and the owner's eye decide |
| 3 | Is B an engine fix or a fact line? | **The engine.** The recommended loads gave dots, not streaks; a notice would only say avoid the mark; its 16 starved marks replaying differently is fine under its 0.6.0 pin | 4B: decided; the fact line waits |
| 4 | Do the frames leave the file? | **Yes.** One GIF, at the end; the rebuild from the log is pixel-exact and took 35 s | 4F: decided |
| 5 | Save the check's lines? | **Yes -- and rehearsals' too**, or it would not have caught these: both misfires were printed by rehearsals. Rebuilt both from the transcript; each reprints its line exactly | 4C: C0 saves rehearsed reports; the misfires filed and reproduced; C2 prototyped on them |
| 6 | Parallel panels? | **No evidence** on speed, none on Windows. Never used `vary=`; its variants were whole passes, which it believed could not go into a plan; what would have replaced its harness is scripts rehearsed as side-by-side alternatives | 4D: D0 built first; D1 behind its bench; 4E documents that a pass is a plan |
| 7 | The documentation's weight? | **Watch.** Never opened `CALIBRATION.md` or `DIAGNOSIS.md`, never ran `explain` or `diagnose`; steered by the notices, the demos and `lightest:`; read three rules and broke them; *if you ever cut, start with what the notices already say at the call* | 4G: recorded in `LESSONS.md`; the code-to-symptom link stays unbuilt |
| 8 | The version? | **0.7.0**, and a notice when a pre-0.7 session is replayed or rebuilt under it, because its README's pixel-identical claim relies on the pin | 4F: F2, the engine stamp and the notice |
| 9 | The model? | **`claude-opus-5-5`, at max effort**, by the session's metadata, with the caveat that a single-turn fallback earlier would not show | `PAINTINGS.md` and the notes say so |

### Put to the painter after step 2, and answered

Step 2 answered what it could and rendered what it could not, and left five questions.
They went to the painter on 2026-09-23 as a package -- the candidates under letters,
blind, first, and the key after -- filed with its answers as
[`answers-step2.md`](paintings/Claude/lighthouse_handover/answers-step2.md) and
[`questions-step2/`](paintings/Claude/lighthouse_handover/questions-step2). The painter
answered all five, and left the one reading that decided question 13 -- whether
`crop_01` is stripes or speckle -- to the owner, who read it as speckle. The bench's
own recommendations are in the package's `KEY.md`. On four of the five the painter came
to the same answer by a different road, and on one it disagreed.

| # | Question | The answer | What it changes here |
|---|---|---|---|
| 10 | Which edge candidate reads as paint -- question 2, now with something to see | **A2 at `0.002`, chosen blind, first of four**, before it knew which letter was the bench's pick. A1 reads as blur enlarged and as today at 1:1; A2 at `0.003` reads ragged on anything made, and paint-like only on a plain rock outline. **For rock, `roughen()` with the default edge on top**, no wider feather. One reservation: at 1440x960, `0.002` reads *a little chewed* -- the feather there is 2.9 px against a grain that stays about 3 px | 4A: A2 at `0.002` is the default; the build benches the feather's unit at 1440 -- a share of the long side or a pixel count |
| 11 | Does the default reach the tower? The plan had read answer 1 as `edge="hard"` feathers, `clip=` keeps `0` | **Yes, `clip=` feathers too, inward -- and that is not a reversal but answer 1 itself, which the plan's reading mistranslated.** Four of the nine edge-drawing calls were clips; containment clips were kept hard only because of an outward feather; the 4x containment crop shows no rim. **The horizon takes `feather=0`** | 4A: both move; row 1 above is corrected where it stands |
| 12 | Which dry-brush gate | **B1+B2, tuned to lay today's paint at each load** -- *that is exactly what I meant: the amount was right, the shape was wrong*. Blind it ranked B2 alone slightly first on bristles (B1+B2 *a bit combed*) and took B1+B2 for B1's reach to flats and rounds | 4B: B1+B2, tuned; after tuning, B2 and B1+B2 side by side on the crosser at `0.45`, and B1's kernel shortened on a comb if B1+B2 still reads combed |
| 13 | Is the graded rule narrowed, and how | **The 30% overlap break on its own**, if the owner read `crop_01` as speckle -- which the owner did. Blind, the painter read three of the ten crops as graded passages (`crop_04`, `05`, `09`), six as not and one as can't tell, and differed from the bench on five. On its reading the overlap break alone keeps all three and halves the false positives; the median clause silences all three | 4C: C2 is the overlap break alone; the median clause is not built |
| 14 | Parallel panels (D1) | **Declined.** The target was missed, and the painter's variants cost the paint, which parallel panels would not take away; what it needed was D0 | 4D: D1 declined; D0 is built |

The painter also listed what the bench got wrong, and each is corrected where it stood:
the framing of question 11 (above); A2's hold at 1440, one eye against another; five
crop readings; the fade, which the round's `CALIBRATION.md` section said *does reach
the field* and which at opacity 0.9 stops `0.034` short of it; and the 35 seconds it
measured, which was its rebuild of the thirteen passes and not a GIF. And one the bench
got right against it: a glaze does go into a plan.

---

## 6. Order of work

One round, cut as 0.7.0, in PRs that each stand alone; the repository's rhythm of
*record the round as open*, then *measure*, then *act and cut*.

1. **Record.** This PR: the painting filed, the answers and the misfires beside it,
   this plan. Next: the round as an open section of `SUGGESTIONS.md` in the register's
   format -- what was wrong, what was done left blank, each finding labelled M/O/R as
   in section 3, with the two claims that changed shape struck through in place -- and
   a section in `CALIBRATION.md`, *The lighthouse handover's round*, that the probe
   below fills.
2. **Measure.** `scripts/probe_handover_session.py`, in the pattern of the probes beside
   it: the edge candidates, inward, at 1024x768 and 1440x960 on the tower, a rock with
   and without `roughen()`, a containment clip and a burial, with the `edges:` line and
   the one-pixel step for each; the fleck statistics by load, brush and gate
   candidate, with crops; the file re-saved each way; the pressure-list thirds and the
   recipe's own fade; the corpus's nine graded fires cropped (`--graded`) and the
   prototype gate's verdict on each; a `vary=` sheet timed single-process against a
   parallel prototype. **Its output decides which rows of A, B, C and D are built as
   written.** Numbers into `CALIBRATION.md`; the rendered candidates are what the
   owner looks at for question 2.
3. **E and C0**: the looking flags, the plan grammar documented, the check's lines
   saved with rehearsals in. Small, certain, one PR, with tests in
   `tests/test_requests.py`'s pattern. *Done: `NOTES-step3.md`.*
4. **F**: the frames out of the file, and the engine stamp with its notice. *Done:
   `NOTES-step4.md`.*
5. **A**: `feather=`, inward, `roughen()`, the default on `edge="hard"`, the goldens.
   *Done: `NOTES-step5.md`.*
6. **B**: the gate, the goldens, the sampler and the exercise re-rendered, the fix named
   in `CHANGELOG.md` and in F2's list. *Done: `NOTES-step6.md`.*
7. **C1, C2**: the crops, then the gate if the crops keep every true positive. *Done:
   `NOTES-step7.md`.*
8. **D0**, then **D1** if its bench meets the target. *Done: `NOTES-step8.md`; D1
   declined on the bench (question 14).*
9. **G**: the three sentences with `scripts/check_guide_blocks.py` green, the numbers
   into `CALIBRATION.md`, and the record -- `LESSONS.md` (the data points on the way
   in and on `explain`; *a measurement is not a method*; the cross-machine papercut),
   `SUGGESTIONS.md` closed, #70's line, `README.md` and `llms.txt` where a count or a
   claim moves. *Done: `NOTES-step9.md`.*
10. **Cut 0.7.0**: the version in `pyproject.toml`, `src/easel/__init__.py` and both
    entries in `server.json`; `CHANGELOG.md`'s entry **without the claim**; the tag;
    then the claim. This file and the step notes go the way `PLAN-0.6.0.md`'s did;
    what survives of them and is written nowhere else goes to `SUGGESTIONS.md`. **The
    first is done**: the version is 0.7.0 in all four copies, `[0.7.0]` is written and
    dated with no claim in it, and `SUGGESTIONS.md` says what the round left open. The
    tag goes on the commit that merges it; the claim comes after the tag, in the PR that
    deletes this file and the step notes.

---

## 7. Risks

| Risk | Guard |
|---|---|
| The feather reads as blur, and every hard edge in the corpus goes soft-focus. | A1 is the control and already reads that way; A2 is benched beside it, inward, and the owner looks before anything moves. Opt-in is the fallback and costs nothing. |
| An inward feather shows the underlayer through the edge zone of a mass, and on a containment clip leaves a rim that reads as an outline. | Both are on the bench -- a mass on bare ground with the `ground:` line read, and the planes inside the headland -- and `clip=` keeps `0` by default whatever the bench says. |
| A moved default repaints committed pictures. | A moved default never reaches a saved log; scripts that leave `feather=` off move, they are listed, and goldens are opened, not regenerated. |
| B moves every starved stroke ever saved. | Named under 0.7.0 as the amended replay promise requires, and said at load by F2; `samples/brushes.png` and exercise 3 looked at; a throwaway abstract painted after it (`LESSONS.md`, trap 1). |
| The narrowed rule silences a true positive. | C1 before C2: the nine corpus fires cropped and looked at, and the gate must keep every one a human calls a passage; the recipe's failure demo holds the floor in CI. |
| The mask memo serves a stale mask. | `feather` joins the key; a test lays the same outline at two feathers in one session and asserts the canvases differ. |
| A saved report block grows the file or the log. | Text only, beside the log; a test that `history.records` and the random stream are untouched, in the *planning verbs leave nothing behind* pattern. |
| Windows process spawn eats D1's gain. | The bench's 1.5x target, measured here; declined if missed. D0 does not depend on it. |
| A 0.6.0 build cannot open a 0.7.0 file. | `frames` written empty as today; `reports` and `engine` read with `.get`; a round-trip test against a 0.6.0-format file. |
| A documentation change on one painter's word. | Three sentences, each with a measurement behind it; the weight is ruled *watch* by the painter itself; every guide block still notice-clean in CI. |
| The decisions are one painter's. | They are, and the owner chose that on purpose; where an answer meets the corpus -- the rule's true positives, the goldens -- the corpus wins, and where the painter had no evidence the bench decides. |
| Some of section 3 is wrong. | Two of the painter's twelve claims changed shape under checking, both reasoned rather than measured, which is the shape `LESSONS.md` predicts -- and one that could not be checked was made checkable by the painter itself. Step 2 re-measures the rest before anything is built on them. |

---

## 8. File map: what will change

| File | Change |
|---|---|
| `src/easel/session.py` | `feather=` on the clipped verbs and in `_clip_cover`'s key, inward; `reports` saved and loaded beside `notices`, rehearsals included, and a rehearsal copy with its own palette, landmarks and guides; `engine` in the meta and the notice at load; the graded rule's overlap break; `rehearse_each`; the notices that name `edge="hard"` |
| `src/easel/canvas.py`, `stroke.py`, `brush.py` | the tooth gate read along the travel or per bristle (B) |
| `src/easel/regions.py` | the inward, tooth-broken coverage; `roughen()` |
| `src/easel/history.py` | frames no longer saved; `timelapse_gif` on a loaded session falls back to the log |
| `src/easel/notices.py` | the load-time notice and the per-version list of rebuild-changing fixes |
| `src/easel/look.py`, `cli.py`, `mcp_server.py` | `--no-marks`, and `marks` on the MCP `look`; `--alternatives` on `run --rehearse` and the sheet it writes; `easel log --reports`, and `reports` on the MCP `log` |
| `scripts/probe_handover_session.py` (new), `probe_cohort_session.py` | the benches as a probe; `--graded` with the prototype gate |
| `tests/test_requests.py`, `test_reference.py`, `test_golden.py`, `test_notices.py` | one test per row, named for the finding; the plan grammar and `look` rows; the misfires as two tests that the gate silences and the recipe's demo as one it must not; goldens looked at |
| `paintings/Claude/lighthouse_handover/` | filed: the passes, the helpers, `verdict.md`, `feelings.md`, `answers.md`, `verify/`, `evidence/`, `misfires/` |
| `RECIPES.md`, `PAINTING.md`, `REFERENCE.md`, `CALIBRATION.md` | G1 to G4; the `feather` argument and the helper; the round's section of numbers |
| `SUGGESTIONS.md`, `LESSONS.md`, `CHANGELOG.md`, `README.md`, `llms.txt`, `PAINTINGS.md` | the round recorded, the lessons named, the cut written without the claim |
