# Plan: act on the 0.5.0 cohort's verdicts, and cut 0.6.0

_To understand this, start by reading: this file; then [`LESSONS.md`](LESSONS.md), because
this plan is written under its rules for how the engine and the guide may change; then
the seven verdicts under `paintings/{GPT,GLM,Deepseek,Gemini,Grok,Kimi,BigPickle_blind}/*/verdict.md`
with the `NOTES.md` beside each; then `src/easel/session.py` at `report()` (line 3214),
`_pass_findings` and the `_check_*` family, which is where every notice the tool gives
today lives -- all of them through `Session._notify` and `src/easel/notices.py` since
step 3._

**Status: steps 1 to 5, 7 and 8 are done, steps 6 and 9 are part-done, and step 10 is
still a plan; of workstreams A to G, A, B, C, E and F are built, D1 and D2 are, and G
is started.**
Step 1 filed the round
in `SUGGESTIONS.md` with its evidence. Step 2 is `scripts/probe_cohort_session.py`: it
rebuilds the corpus, re-measures every claim in 2a and 2d, and counts what every
candidate in D, E and F would cost. Its numbers are in `CALIBRATION.md` under *The 0.5.0
cohort's round*, and **what they decide is under section 6 below**. Step 3 is the notice
channel (A, all five rows): `src/easel/notices.py`, `Session._notify` with all 21 sites
converted, delivery through `easel run` and the MCP `run` / `cost` / `preview` /
`rehearse` results, `easel explain`, and `REFERENCE.md`'s *What the tool will tell you*
held against the registry by `tests/test_notices.py`. **Every check D adds from here
lands on that channel rather than beside it.** Step 4 is workstream B, every row of it
except B8, which was held back to the default moves (F5) because it repaints 55
committed calls. Step 5 is the plan object (C): `src/easel/plan.py`, `Session.plan()`,
its five effects on the check, `easel plan` and an MCP `plan` tool, and the finding-11
contradiction resolved in both the engine and the recipe. **Step 6 is part-done**: both
D1 checks the probe left standing are built -- `chisel-staircase`, and `spill`, whose
multiple is predicted off the passes a call is about to lay and which settled B17's
open question (the auto brush is not capped) -- and so is D2: `smudge-across`,
`smudge-long` and `glaze-far`, with an engine bug found on the way (a smudge started
loaded with white, which was half of finding 3's thumbprint) fixed, and D3 is not
started; `NOTES-step6.md` has the gotchas of `spill` and of D2. Step 7 is
workstream E and `s.checklist()` (G4): `src/easel/checklist.py`, the `values:` /
`edges:` / `holes:` / `pencil:` / `boxes:` / `unspent:` lines, `easel check` and the MCP
`check` tool; `NOTES-step7.md` has its gotchas, including one published `edges:` number
withdrawn. Step 8 is the two default moves the step-2 probe left standing -- a banded
`scumble` laid solid (F3) and two brushes of overhang under `edge="hard"` (F5) -- with
F1, F2 and F4 declined on the corpus's own evidence and written into `CHANGELOG.md` so
they are not re-argued; `NOTES-step8.md` has its gotchas. **Step 9 is part-done**, in
two parts so far. Part one is G5: `src/easel/diagnosis.py`, `easel diagnose`, a
`diagnose` MCP tool, and `DIAGNOSIS.md` as the sixth shipped document. Part two is
**G7 and G9** -- the fixes to what is there, and the one small fact of five that was
genuinely open (vision is required). Two of G7's rows had already been closed by steps 5
and 6, and two faults it did not know about were found by running every guide block past
the checks: **every runnable block in the guide is now notice-clean**, and
`scripts/check_guide_blocks.py` fails if that stops being true. G4 landed with step 7,
so what is left of G is G2, G3, G6, G8, G10 and G11; `NOTES-step9.md` has the gotchas
for both parts. The three rulings the step notes left for the owner -- the standing
lines, the inward `load`, the code-to-symptom link -- were settled on 2026-09-21 and are
the last three rows of the decisions table below. Written 2026-09-18 against
`main` at `8192736`, engine 0.5.0 (released: `v0.5.0` is tagged at `54c2a0b`). Working
file: delete it, or fold what survives into `SUGGESTIONS.md` / `CHANGELOG.md`, when the
round is cut.

---

## 1. What this round is

Seven painters that are not Claude -- GPT, GLM, DeepSeek, Gemini, Grok, Kimi and
BigPickle (blind) -- each painted a picture with `easel-paint` 0.5.0 from the installed
package. **They were told to install it and paint, nothing about what to read.** Each
left a `verdict.md` on the tool, the documentation and its own picture. None of it is
filed in `SUGGESTIONS.md` yet.

Two more verdicts are untracked in the worktree (`paintings/Claude/fogged_glass/`,
`paintings/Claude/greenhouse_winter/`). Those paintings predate 0.4.0 and their engine
items were closed there, so they are **corroboration only** -- chiefly for the sentence
both of them lead with: *reading the warning did not stop me; the rehearsal image and
the post-pass check did.*

**The owner's goal for the round:** wherever the tool can know a thing, the warning
comes out of the tool and leaves the documentation; and the bugs the verdicts report get
fixed. That is `LESSONS.md`'s own growth rule (*each rule that becomes a check can leave
the guide*), asked for at scale.

### Decisions already taken (owner, 2026-09-18; the last three 2026-09-21)

| Question | Decision |
|---|---|
| How far may defaults move? | **Measure, then move.** Only where a probe shows the default sits outside its usable window; every move listed under *defaults moved* in `CHANGELOG.md`. |
| How does the tool learn that a standing warning is the subject's own truth? | **Declared in a plan**, up front: `s.plan(...)`, saved in the `.easel` file. Not an after-the-fact `accept()`. |
| Where does the check's line sit? | **Marks, plus canvas *measurements*.** Numbers like the existing `ground:` line. No composition judgement. |
| What shape are the docs after this? | **Card + tool.** Rules that become checks leave as one line; the closing checklist becomes tool output; `DIAGNOSIS.md` becomes a command; recipes gain runnable good-vs-failure demos. No separate quick-start file. |
| What were the sessions told to read? | **Nothing -- "install and paint".** So the ~2,600 lines they read before the first stroke is the docs' own instruction being followed, and the entry path is in scope. |
| Painters that cannot see images? | **Out of scope: vision is required**, and the README should say so. BigPickle's verdict is weighted accordingly. |
| Release shape | **One 0.6.0 round**, as several PRs. |
| Where the plan lives | This file. Filing the open round in `SUGGESTIONS.md` is step 1 below. |
| `import easel_paint` | **It just works**: ship a small `easel_paint` package that re-exports `easel` (B10). |
| Validation | **The owner's, and not a step of this plan.** The plan only makes sure a run can be read afterwards (notices saved in the `.easel` file, A2). |
| A painter who never calls `s.plan()` | **Said where it costs**: no message at the first stroke; the card's example and the `easel new` scaffold show it, and the closing check lists what it could not answer (C). |
| `solid=True` with a comb | **Say so, with prices**: no default move; the call names the bare share to expect and each remedy with its stroke price (B2). |
| GLM's rings | The owner supplied GLM's working folder; what its frames show is in B18. |
| The four standing lines after every pass, against *fewer than three lines on a median pass* (`NOTES-step7.md`) | **Kept on every pass.** The target counts findings and call-time notices, which is what the probe has always counted: `ground:` printed after every pass of 0.5.0 while the probe reported a median of `0`. A standing measurement is not a finding. Whether the longer block gets skimmed is the next run's to show. |
| The inward `scumble`'s `load` (`NOTES-step8.md`, gotcha 3) | **Kept, as intended**: the brush's own `0.9`, where a band has laid `1.0` since F3. `0.005%` of a patch bare against `0.012%` is inside any window, so under *measure, then move* it stays. `REFERENCE.md`'s `solid` and `load` rows now say *a banded `scumble`*, which is all they were ever true of. |
| Linking notice codes to `DIAGNOSIS.md` rows (`NOTES-step9.md`) | **Not this round.** Sixteen of the twenty-five codes already resolve to the passage a row points at, so `explain` and `diagnose` print the same text and only the name is missing. Revisit once a run shows whether a painter calls either. |

---

## 2. What the verdicts say

*Who* counts only the 0.5.0 cohort unless marked. *Kind* is the project's own
distinction: **M** measured by the painter, **O** observed, **R** reasoned.

### 2a. Failures the documentation already names, that the tool did not catch

| # | Finding | Who | Kind | Today |
|---|---|---|---|---|
| 1 | **Chisel staircase** down a sloped boundary. Kimi's rock faces are the `RECIPES.md` *mass built of planes* call **character for character** (`pass4_lighthouse.py:16`) -- a ragged `flat` on sloped polygons. *A worked example is an instruction.* | Kimi; winter greenhouse x4, Opus (earlier) | O | prose + table row in `PAINTING.md`; no check |
| 2 | **Holes inside a `solid=True` mass.** GPT closed three by hand (`paint.py:630 solid_joins`), Grok one (`pass6_repair.py`). *The holes are real; the reported cause -- passes wandering apart -- did not survive checking: see B2 and B8.* | GPT, Grok | O | nothing |
| 3 | **Smudge drags a bright thumbprint** out of the light mass. | GPT, Grok; laundromat 4 of 5, car wash x2 (earlier) | O | prose; warns only on `size > 0.03` |
| 4 | **A glaze far from its ground**: green blooms over blue water, a searchlight on a flat sheet. | GPT, Grok; Opus, Fable, pool, heron (earlier) | O | prose + table; `to_value=` exists, nothing fires |
| 5 | **Paint laid over a still-wet film**: six crossing glazes, then a block-in, printed concentric rings and cost the session's one `undo`. *Real -- but the painter's own frames show the glazes did not print them: B18.* | GLM; Opus x2, laundromat (earlier) | O | prose (*dry() first*); nothing fires |
| 6 | **Strokes radiating from one point**: a wagon wheel. | Gemini; fogged glass x2, Fable, car wash (earlier) | O | prose in three places |
| 7 | **One loop's signature**: a column of same-length marks for a reflection on water -- *floating rectangles*, *small bricks*, *a ziggurat*, *spoon-shaped islands*. **Four of seven failed the same passage the same way first, and `RECIPES.md` has no entry for it.** | DeepSeek, Gemini, Kimi, GPT | O | one table row (*any loop you write*) |
| 8 | **`scumble` / `cover` land well outside the place they were given**: a water scumble covered part of the sky; a `cover()` repair laid a flat patch in front of the tower. *Checked, and larger than claimed: a band at 60 degrees paints 3.5x its own area and no warning can fire for a rectangle (B17).* | GPT, Kimi, Grok | O | wedge warning only, and only on a `Polygon`; `cover(edge="hard")` exists and the card does not name it |
| 9 | A late pass **buries what stands in front of it** (weathering over a nearer cottage; a rope repainted after the wall). `LESSONS.md` lists the depth-order paragraph as failed in three runs and still open. | GPT, Kimi; fogged glass, heron 1, pool (earlier) | O / M | prose + checklist line |

### 2b. Warnings the tool gives, that were noise

| # | Finding | Who |
|---|---|---|
| 10 | **Stack of bars** on a subject that is horizontal: accepted by hand in the notes. BigPickle's was a true positive. | DeepSeek, Kimi, Gemini (392 of 583), GLM |
| 11 | **`ground: 0.0x% ... the checklist asks for some`**: accepted by hand. Three painters give the same cause in nearly the same words -- *the `density=0.8` breather was buried by the graded fields*. **The graded-field recipe (solid scumbles over most of the canvas) and the ground line contradict each other.** | DeepSeek, Grok, Kimi, GPT (0.06%), Gemini (0.38%) |
| 12 | Small-bristle (265 marks) and round-disc (176 marks) rules fired on a whole painting and were argued with rather than acted on. | Gemini |
| -- | *"Useful heuristics, but they're philosophy, not errors, and it doesn't know which."* There is no way to tell the tool anything (inventory: no acknowledge/suppress mechanism exists). | DeepSeek |

### 2c. What the check cannot see

| # | Finding | Who |
|---|---|---|
| 13 | `report()` said *nothing to report* over flat cut-out shapes, uniform edge handling and a banded sky. | GPT; pier (earlier) |
| 14 | *No linter catches a stripe instead of a catch-light* -- a recipe followed exactly and expressively wrong. | DeepSeek |
| 15 | Safe, frontal, centred compositions. Five of seven stopped under 45% of budget (68/300, 126/300, 132/300, 170/420, 50/120), each saying more marks made it worse. | GLM, DeepSeek, Grok, Kimi, BigPickle |

### 2d. Bugs and API gaps

Eighteen items, in workstream B, each with what checking it against the code found.
Four reported mechanisms did not survive, one bug is larger than reported, and one
turned up a second silent bug beside it.

### 2e. The documentation

| # | Finding | Who |
|---|---|---|
| 16 | **Too long before the first stroke**: ~2,600 / ~2,500 lines, 10,000+ words, *2000+ lines of docstrings*. Wants a quick start or cheat-sheet. | DeepSeek, GLM, BigPickle, Kimi |
| 17 | **Too prescriptive**: stroke allocations, bare-ground percentages and marks-per-object read as universal; *supervised by a very earnest painting instructor*. | GPT, Kimi |
| 18 | **The voice hides the call**; *runtime warnings are clearer in the moment than the prose*; rules fight each other until each has been failed once. | Grok |
| 19 | Wants **small runnable visual comparisons**: the recommended call, what it looks like, the common failure, the smallest fix. *The documentation sometimes compensates for difficult tool behaviour with additional rules.* | GPT |
| 20 | The two things that cost real work (the ring interaction, the hard-edge bites) were not in it. *Written for a painter who already knows painting; the first steps are assumed.* | GLM, DeepSeek |
| 21 | *Reading it did not stop me making the mistakes it describes ... move more prose into `report()`.* The sixth and seventh painters to say so. | Claude x2 (pre-0.4.0) |

**What every one of them defended**, unprompted, and this plan does not touch: rehearsal
seeded as the next real strokes; `at_value` and errors that teach; `cost_line` naming
the lever; one plan object for `cost`/`preview`/`rehearse`/`paint`; determinism.

---

## 3. The rules this plan works under

Taken from `LESSONS.md`, because a plan that ignores them will be re-litigated in review.

1. **Measure the condition before writing the rule.** Thirty painter claims have been
   re-measured and eight did not survive; expect some of section 2 to die the same way.
   A check earns its line by firing on a real pass of a real painting.
2. **Ask what the rule says to a painter doing the right thing.** A rule that fires on
   the remedy it names, or on a recipe's own code block, is worse than no rule.
3. **A default is worth more than a warning** -- measure the curve, move the default,
   warn about the far end.
4. **Warning is not method.** Where a warning keeps failing, replace it with a procedure
   or with the method's next question.
5. **One engine change per paragraph, the paragraph leaving in the same commit.**
   `PAINTER.md` never grows.
6. **A guide change is a hypothesis** until a fresh session paints against it.
7. **A warning that fires on almost every pass is a warning nobody reads.** The bars
   rule already taught two painters to skim. Every new rule is budgeted for noise
   (workstream C).
8. **Nothing new may touch the log index or the random stream.** A mark's texture is
   seeded from its place in the log; notices and the plan live *beside*
   `history.records`, never in it, or every painting after an upgrade moves.

---

## 4. Workstreams

### A. Delivery: one notice channel -- the prerequisite

**Built, step 3.** All five rows, as written, with two additions the inventory below
missed: `_say_uncounted` and the foreign-`out_dir` warning are codes too (`count-only`,
`foreign-out-dir`), which makes the registry the whole of what the engine says rather
than most of it, and lets `tests/test_notices.py` assert that no bare `warnings.warn`
is left in `src/easel/`. 21 codes; 3 of them habits. Two things worth carrying forward:
`rehearse` and the price walk both work on a throwaway copy, so what they say has to be
carried back to the session (`Session._adopt_notices`) or it is lost -- which is
precisely what an MCP painter was losing; and a notice must not touch the log, which the
*planning verbs leave nothing behind* test proved by catching a first attempt that did.

**Today** (inventory, `session.py`): every call-time warning is a bare
`warnings.warn(str)` from one of twelve `_check_*` functions, two methods and three
inline sites. No class, no code, no collection. `cli.py` and `mcp_server.py` never touch
`warnings`: under `easel run` they go to stderr, unformatted and apart from the check;
**through the MCP server they reach nobody** (`_tool`, `mcp_server.py:376`, converts
exceptions only). So for an MCP painter "the tool warns" is currently false for
everything except `report()`.

| Step | What |
|---|---|
| A1 | `src/easel/notices.py`: `EaselWarning(UserWarning)` carrying a stable `code` (`"chisel-staircase"`), a `kind` (**fact** -- *this lands nothing, this paints 3x the area* -- or **habit** -- *a stack of bars unless the subject runs that way*), the text, and a `where` (the doc heading that holds the reason). Subclassing `UserWarning` keeps every existing `pytest.warns(UserWarning, match=...)` green. |
| A2 | `Session._notify(code, text, stacklevel)`: append to `self._notices` (beside the log, carried into `scratch()` copies the way `_uncounted` is, saved under a new `"notices"` key in the `.easel` meta -- `load()` reads meta with `.get`, so 0.5.0 still opens the file), then `warnings.warn`. Convert the 17 existing sites; no message text changes in this step. |
| A3 | `run_scripts` (`cli.py:610`) and the MCP `run` / `cost` / `preview` / `rehearse` results print the pass's notices **in one block with the check**: *at the call* first, *over the pass* second, facts before habits, identical codes collapsed with a count. Under `easel run` the stderr copy of an `EaselWarning` is filtered so it is said once, in order, on stdout. |
| A4 | A registry `NOTICES = {code: spec}`. Tests, in the pattern of `tests/test_reference.py`: every `_notify` code is registered; every registered code is a row of a new *What the tool will tell you* table in `REFERENCE.md`; every doc sentence of the form *the call says so* / *`report()` counts it* names a code that exists. **That last test is what stops prose and tool drifting apart again.** |
| A5 | `easel explain <code>` / `s.explain(code)`: print the `CALIBRATION.md` / `PAINTING.md` passage `where` points at. This is where the *reason* goes when its paragraph leaves the reading path: not deleted, delivered at the moment it applies. |

### B. Bugs and API consistency

**Every row below was checked against `src/` on 2026-09-18** -- by reading the code and,
where it was cheap, by painting the case on a scratch canvas -- before it was allowed
into this plan. That is `LESSONS.md`'s *check the painters' numbers*, and it did what it
usually does: **four reported mechanisms did not survive** (B2, B7, B12, and B18 -- whose
cause neither the painter nor the first check got right), one bug turned out larger than
reported (B17), and one turned up a second, silent bug beside it (B5).
Step 2 of section 6 turns these spot checks into a runnable probe.

| # | Reported | Who | What the check found | Fix |
|---|---|---|---|---|
| B1 | `scumble(clip=)` raises `TypeError`. | GPT | **Confirmed.** `clip` is a named parameter of `stroke()` only (`session.py:305`). `dab`, `smudge` and `glaze` reach it through `**kw`; `block_in`, `sweep`, `cover` and `scumble` cannot. The error is the generic *`clip=` is not a brush field*: `_NOT_BRUSH_FIELDS` (`3845`) has rows for `solid`, `glaze`, `edge`, `density`, `overhang`, `pressure` and none for `clip`, so it never names `stroke(clip=)` or `edge="hard"`. | `clip=` on every verb that lays paint, and `edge="hard"` on `scumble` as its mass form; one shared path, the clip riding in the log as it does for `stroke`. A verb x (`clip`, `edge`, overrides) matrix in `REFERENCE.md`, held by `test_reference.py`. The `_NOT_BRUSH_FIELDS` row is the five-minute version and lands first. |
| B2 | Holes inside a `solid=True` mass: *shaped block-in paths wander apart*. | GPT, Grok | **The holes are real and the mechanism is not the one reported.** A `flat` left **0.0000%** bare at every size, direction and density tried. A **`bristle`** -- `block_in`'s default brush -- leaves them: `size=0.06, direction=37, density=1.0, solid=True` on 1440x960 gives 22 bare blobs, the largest 187 px (25x51); 0.41% at `density=0.9`. It is the comb covering about three-quarters of its width, which `solid=` cannot close: it sets `load` and `load_falloff` and nothing else (`821`). GPT's own three holes were laid with a `flat` and sit at x = 0.552 / 0.694 / 0.904 -- the joins between neighbouring hard-edged walls -- so they are most likely **B8**, not this. | **Decided: say so, with prices.** `solid=True` with a comb says at the call what share will stay bare and what each remedy costs in strokes -- a `flat`; a tighter `density` (passes sit `size x (1 - 0.45 x density)` apart, so 1.3 is a third more passes and 1.5 two-thirds more; the probe finds the density that actually closes a comb); crossed passes. No default moves and `cost()` is unchanged. The `holes:` line (E). Re-measure GPT's three joins from its own script in step 2. |
| B3 | `timelapse_gif()` fails on a rehearsal copy. | DeepSeek | **Confirmed.** `_trial_session` sets `timelapse = False` (`2555`), so the copy has no frames and `save_gif` raises a clean `ValueError` -- whose first remedy is wrong here: *create the session with `timelapse=True`*. The painting had it; the copy switched it off. | Say what happened: *this is a rehearsal copy and rehearsals record no frames -- run the pass for real, or `easel timelapse` on the painting.* |
| B4 | Time-lapse frames are 360 px beside a 1440 px painting. | GPT | **Confirmed.** `add_frame(max_side=360)` and `thumbnail_srgb8(max_side=360)` (`history.py:179`, `canvas.py:534`) are called with no argument (`session.py:400`), so the size is unreachable from `Session` or the CLI; `scale=` only shrinks (`history.py:242`). Frames are stored in the `.easel` file at that size. `replay(upto=)` rebuilds a full-size session, so frames at any size are available in principle; nothing wires it. | `timelapse_gif(from_log=True, scale=)` built on `replay`, so resolution is chosen afterwards and nothing larger is stored. `Session(timelapse=<px>)` is the simpler second choice. |
| B5 | `cost_line` failed on a `scumble`. | GLM | **Confirmed, and there is a worse one beside it.** `_plan_specs` (`2617`) knows three kinds -- mass, sweep, stroke -- so `scumble`, `cover`, `glaze` and `smudge` cannot be planned, priced, previewed or rehearsed. And a scumble-shaped dict carrying `shape=` **prices silently as a block-in** (6 strokes where the scumble costs 8) and only raises when `paint()` reaches the extra keys. The MCP server already refuses unknown keys before pricing (`_ACCEPTS` / `_check`, `mcp_server.py:104, 297`: *a quote for a plan that cannot be painted is worse than no quote*); the library does not. | Lift the server's `_check` into `_plan_specs` first. Then plan entries for `scumble` and `cover`, through the one dispatch. |
| B6 | `replay(upto=)`, `undo(n)`, `log(last=)`: records or strokes? | GLM | **Partly.** All three count log **records**, free ones included. `replay`'s docstring says so and `REFERENCE.md` says so for `undo`; `undo`'s own docstring says *scrape back `n` strokes* (`1980`), and `log(last=)` says nothing. | One word in `undo`'s docstring, a clause for `log`. |
| B7 | The Windows cp1252 console chokes on the docs' unicode. | GLM | **Not reproduced for the tool.** `docs.write()` writes UTF-8 bytes past the codec on purpose (`docs.py:120`); `easel guide` and `--calibration` exit 0 under cp1252, byte-identical to the files; and no string in `src/easel/` contains a non-ASCII character, so no notice or `report()` line can do it. What does die is a painter's own `print(easel.docs.read(...))`: four characters in the five shipped files are outside cp1252 -- an arrow, a true minus, *approximately* and *less-or-equal* -- 35 occurrences, 31 of them in `CALIBRATION.md`. | Replace those four with ASCII in the shipped documents and hold it with a test: *every shipped document encodes as cp1252*. Reading a doc from Python is the most natural thing a painter does with `easel.docs`. |
| B8 | `edge="hard"` leaves pass-end bites at the outline. | GLM | **Confirmed, and the mechanism is isolated.** `hard` cuts the bites three- to four-fold against `ragged`, but on a slanted outline it still leaves **1.9%** (`flat`) to **4.9%** (`round_hard`) of the 3 px strip inside the line unpainted. `_mass_overhang` gives `hard` one brush of overhang (`5236`) and the default `pressure="taper"` reaches zero one brush out, so every pass arrives at the outline at part pressure -- and a round tip at part *width*. At `overhang=2.0` it is **0.016%** (`flat`) and **0.000%** (`round_hard`, even). `solid=` moves nothing (13.63% -> 13.56%), so it is pressure and not load. | `_mass_overhang` returns 2.0 under `hard`: nothing can cross the mask, so the cost is a few dabs. It moves what existing `edge="hard"` scripts paint, so it goes with the default moves (F), goldens looked at. |
| B9 | Subject share counts free signature marks (172/411, not 172/408). | GPT | **Confirmed and reproduced**: five subject marks, three signature marks and one pencil line give `spent = 5` and *subject: 5 of 8 marks so far (62%)*. `session.py:3329` builds `paid` without the exemption `History.stroke_count` applies (`history.py:105`). | Reuse that exemption. |
| B10 | `import easel_paint` fails. | DeepSeek; the install session (earlier) | **Partly.** `llms.txt` and the package docstring put `from easel import` straight after the install line. `README.md` does not: its install section has no import at all, and its only one is 76 lines above. **And PyPI carries an unrelated distribution named `easel`** (0.0.1 and 0.0.2; `pip index versions easel`, 2026-09-18 -- not downloaded, so what it installs is unverified), which is what a painter who guesses `pip install easel` from the import name would get. | **Decided: it just works.** A small `easel_paint` package in the wheel that re-exports `easel` (`packages` in `pyproject.toml`; a test that the two expose the same names), so the one import name that is certainly this project's is a real one. Docs keep teaching `easel`. Plus the two lines under README's install block, and a sentence there that the distribution is `easel-paint`, never `easel`. |
| B11 | A ground name used as a colour; three namespaces. | Gemini | **Partly.** `Palette.__getitem__` lists every valid pigment and slot but does not notice that the name it was given is a valid *ground*; `canvas.py:243` is blind the other way round. Nothing exposes a ground as a colour (`ground_name`, `ground_spec` and `bare()` only). | Each handler checks the other namespace first and says so; expose the ground as a palette-ready colour, since `s.sample()` of bare canvas is today's only route. |
| B12 | `region("bottom")` is the bottom third, not a foreground band. | GLM | **It is smaller than reported: a ninth.** `_NAMED` (`regions.py:191`) makes `top`, `bottom`, `left`, `right` and `center` cells of a 3x3, so `bottom` is x 1/3-2/3, y 2/3-1. The full-width places are `lower-band` and `lower-half`. `REFERENCE.md` lists the names and none of their extents; the repr does print the box. | An extents table in `REFERENCE.md` and in `region()`'s docstring. |
| B13 | A 0-255 integer list clamps to white in silence (`PAINTING.md` documents it as a trap). | the docs | Not re-checked; documented behaviour. | **Raise**, naming both fixes. A documented trap the engine can detect is a bug. |
| B14 | `solid=True` is refused on `stroke` and `scumble`, with a good teaching error. | Gemini; laundromat (earlier) | Not re-checked; the error text is in the inventory (`session.py:3845`). | Accept it wherever it has a meaning -- `stroke`, `scumble`, `sweep`. It is `load=1.0, load_falloff=0.0` everywhere, and it is the clause painters type by hand most often. |
| B15 | 30-45 s for 500-800 marks. | Gemini | **Confirmed as fixed cost per stroke; nothing is quadratic.** Every stroke snapshots rgb, wetness, thickness and sketch for `undo` -- about 33 MB and 6.4 ms at 1440x960, and with `MAX_SNAPSHOTS = 24` roughly **800 MB resident**. With `timelapse=True`, the default, every stroke also builds its 360 px frame from a full-canvas composite: 25.6 ms. About 32 ms of bookkeeping per mark before a dab lands, ~26 s over 800 marks. The per-dab loop dominates wide marks (1.3-1.8 s for a full-width `bristle` pass). | In scope after all, as two cheap cuts: a frame every Nth stroke or from a small buffer, and a smaller or dirty-rectangle snapshot. The dab loop stays open in `LESSONS.md`. |
| B16 | Easier calibration of size, load and pressure before committing. | GPT | A feature, not a bug. | `s.rehearse(plan, vary={"size": [...], "load": [...]})`: one labelled sheet of the same mark, in place, on a copy. Free, like any rehearsal. |
| B17 | A wide angled `scumble` lands far outside its band (finding 8). | GPT, Kimi, Grok | **Confirmed, and larger than claimed.** The auto brush is `3 x step`, and `step` is the band's *bounding box* projected on the pass normal (`_normal_extent`, `4583`), so an oblique angle on a wide, low band inflates it. A band 0.20 tall at `n=8` paints **1.43x** its own area at `"axis"`, 2.84x at 30 degrees and **3.53x at 60** -- a brush 1.65x the band's own height, covering 0.83 of the canvas height. **Nothing fires**: the narrow-brush check looks the other way, and `_check_scumble_ends` returns at once for a `Region` (`4546`), so the guide's own `span(...)` bands can never trip *passes shorter than the brush*. | Run `_check_scumble_ends` on rectangles too; the `spill` notice (D1) with the predicted ratio; `clip=` / `edge="hard"` on `scumble` (B1) as the remedy it names. Probe whether the auto brush should be capped by the band's own shorter extent. |
| B18 | Glazes crossed wet, then a block-in: concentric rings (finding 5). | GLM | **The rings are real; both accounts of their cause are wrong, and GLM's own folder shows it** (`C:\Users\arie_\Documents\Default Project1\painting-GLM-5.3-Flash\out`, 69 looks and rehearsals in time order). (1) *Not the six crossing glazes:* `look_005` and `look_006`, taken after them and before pass 2, show faint straight bands and a clean wall. (2) *Not a wet film at full wetness:* wetness is `alpha x brush.wetness` and alpha carries the opacity (`stroke.py:410`, `canvas.py:354`), so a film at `opacity=0.15` leaves about 0.13, not 0.90, and it had twenty-odd strokes at 6% a stroke to fade. (3) The rings first appear in **`rehearse_012`**, the last rehearsal of pass 2's first take, and land identically in `look_007` -- **so the rehearsal showed them, and *what you rehearse is what lands* held.** (4) They are wobbly closed loops concentric with a blob-shaped patch, lying *over* the bezel's right edge and out onto the wall, one band as dark as the bezel: ring passes laid after the bezel, around a patch that overshoots the glass -- an inward `scumble`'s own contour rings, the failure `RECIPES.md` already names (*visible concentric rings*) and the pool painting called *a contour map*, possibly darkened by picking up the wet bezel. GLM's cure fits: a far lower-contrast inward scumble (`0.20 -> 0.235`, `n=10`), and `dry()` before the bezel. `noimp.png` rules out the relief; `bisect30.png` is GLM bisecting with `replay(upto=30)`. The first takes of `pass1b.py` and `pass2.py` were overwritten and the marks undone, so the calls themselves are gone. | Reconstruct pass 2's first take in the probe **against those frames** -- it is right when it reproduces `look_007`'s dark band. Then, by what it shows: a `ring-steps` notice (D1) for an inward scumble whose value step per ring is wide enough to read as contours; `wet-under` (D2) only if the wet bezel turns out to matter; `dry_first=` on `block_in` either way (default `False`). Copy the seven frames that carry the evidence into the repository with the open round (step 1), under names `.gitignore` does not exclude. |

**One thing about the workshop, met while checking these.** On this machine `import easel`
resolves to the 0.5.0 wheel in `site-packages`, not to the checkout -- the trap
`CHANGELOG.md` records under *The workshop*, live again. The two are byte-identical
today, so nothing above is affected, but a local `pytest` would be testing the wheel.
`pip install -e ".[dev]"` before step 2.

### C. The plan object, and noise control

**`s.plan(...)`** holds what the guide tells a painter to *write down* and nothing in the
engine currently holds. `Session(budget=)` was the first of these; this is the rest.

```python
s.plan(why="under a pier the light arrives from below, so every form is lit backwards",
       values={sky: 0.70, water: 0.39, quay: 0.22},   # the dict compare() already takes
       lightest=lamp,                                  # the place meant to be lightest
       subject_share=0.40,
       bands="subject",      # I counted them; the subject runs this way
       ground="buried")      # or "showing", the default expectation
```

Stored beside the log, saved under `"plan"` in the `.easel` meta, settable from
`prelude.py`, `easel plan p.easel ...` and an MCP `plan` tool. What it changes:

| Declared | Effect on the check |
|---|---|
| `values` | At registration, on the empty canvas, the touching-pairs table is printed -- the run three rounds of painters skipped. After every pass, one line: *plan: 5 of 6 places inside 0.10; `halo` +0.14*. |
| `lightest` | *lightest: `horizon` reads 0.61; the plan says `lamp`.* |
| `subject_share` | The `subject:` line always carries *against N% planned*. Today that needs `report(subject_share=)` by hand, and neither `easel run` (`cli.py:593`) nor the MCP `run` tool (`mcp_server.py:565`) passes it -- so a shell or MCP painter has never seen the comparison. |
| `bands="subject"` | The bars **warning** is replaced by the method's next **question**, as a number: *bands declared as the subject: 3 long marks cross them at 30 degrees or more* -- or *nothing crosses them yet*. `_crossing_marks` already computes it. |
| `ground="buried"` | The ground line prints the number and drops *the checklist asks for some*. |
| `why` | Quoted back by `s.checklist()` (workstream G): *you wrote "..." -- is that still in the picture?* |
| nothing registered | **Decided: said where it costs.** No message at the first stroke. The card's first code block carries `s.plan(...)` (*a worked example is an instruction*), `easel new` scaffolds a `prelude.py` with the stub to fill in, and `s.checklist()` lists exactly which lines it could not answer because no plan was registered. |

This also answers finding 17: the guide's stroke splits and ground percentages stop
being the guide's numbers and become the painter's declared plan.

**Noise budget.** `scripts/probe_cohort_session.py` (section 6) replays every painting
pass by pass and prints, per rule, how often it fires and on what share of passes. A
*habit* rule that fires on more than about one pass in six across the corpus is narrowed,
made said-once in the bars rule's pattern (state in the `.easel` file), or demoted to a
measurement line. The probe's table goes into `CALIBRATION.md` so the next round can see
whether it moved.

**Resolve the contradiction in finding 11** before anything else touches the ground
line: either *a graded field that is most of the picture* says how to leave the ground
breathing, or the checklist line becomes conditional on the plan. Five of seven cannot
all be wrong.

### D. New checks

Each row is a **candidate until step 2 measures it**. *Leaves* is the prose that goes in
the same commit, replaced by one line naming the code.

**D1. At the call, from geometry alone** (cheap, exact, no canvas read)

| Code | Fires when | Evidence | Leaves |
|---|---|---|---|
| `chisel-staircase` | `block_in(shape, flat/knife, edge="ragged")` and a measurable share of the outline is neither parallel nor square to the passes. Names `edge="hard"`, or `direction=` as the boundary's two points. | 1 | the staircase paragraph in `PAINTING.md` (the table row stays); **and the two recipe blocks that produce it are fixed** |
| `spill` | a ragged chisel/comb mass whose brush is over a fifth of the shorter extent: says how far it lands outside. For `scumble`: the predicted share of paint outside the band, from the auto brush, `overhang` and angle -- the ratio B17 measured at 1.43x to 3.53x. Names `clip=` / `edge="hard"` (B1). | 8, B17; pier, fogged glass (earlier) | *the paint lands outside the shape...* in `PAINTING.md`, down to the three remedies |
| `ring-steps` | `scumble(direction="inward")` whose value step per ring is wide enough to read as contour lines: says the step, and the `n` or the closer pair of colours that brings it under. Palette arithmetic only. | B18 (GLM's frames); pool (*a contour map*), earlier | *visible concentric rings, which is too few rings for the patch* in `RECIPES.md` |
| `inset-lost` | `inset()` keeps under about 70% of the area, or drops a lobe: says what it kept. | earlier (62.7% kept) | *on a shape that is not convex...* |
| `cross-small`, `mass-is-a-stroke`, `shallow-box`, `scumble-few` (`n < 5`), `round-soft-mass` | the four geometric rows of *the shape each tool leaves behind* and two one-line rules. Tier 2: build only those the probe shows a real painting tripping. | table rows | their sentences |

**D2. At the call, reading the canvas under the footprint** (new: the tool can *see* what
the mark lands on; sample along the path, do not rasterise)

| Code | Fires when | Evidence | Leaves |
|---|---|---|---|
| `smudge-across` | the value changes more *along* the smudge path than across it: the path crosses a boundary instead of following one. States the step it crosses. | 3 | two of the *three things about `smudge`* in `PAINTER.md` step 6 |
| `smudge-again` | the path lies within a brush of an earlier smudge for most of its length: *a second pass undoes most of the first (0.214 -> 0.280); lay paint across it*. Log only. | four painters in one run (earlier); Grok's list | the *one pass, not three* paragraph |
| `smudge-long` | path longer than about a tenth of the canvas: *a smudge loses a stretch; over this length it leaves a mid-value strip, two edges where there was one*. | winter greenhouse | the *stretch, not a boundary* paragraph in `RECIPES.md` |
| `glaze-far` | the film's predicted shift over its own footprint reaches the 0.08-0.10 that makes a new mass, or its hue is far from what is under it. Names `to_value=` and *mix it closer*. | 4 | most of the glaze table's prose in `PAINTING.md` (table stays in `CALIBRATION.md`) |
| `ring-rim` | `scumble(direction="inward")` whose first colour differs in value from what the canvas reads along the patch's own boundary: *the first ring lands on the boundary and is 0.06 off what it meets -- that draws a rim*. Offers the sampled colour. | GLM (*the halo's oval edge is faintly detectable as a shape* -- visible in its `painting.png`); the recipe's own *goes wrong as* | *give the first ring the value the patch meets its surroundings at*, in `PAINTER.md` step 5 and `RECIPES.md` |
| `wet-under` | **Only if the probe shows the wet bezel mattered in B18.** An opaque mark or mass lands on paint still wet **and** far from it in colour. Says how wet, names `dry()`. Must stay silent on deliberate wet-into-wet (close colours) -- the probe decides the gate. | 5 | *if you want the new colour to read as itself...* ; plus the missing clause in *a volume of lit air*: dry again **after** the films |

**D3. After the pass, off the log** (new rows in `_pass_findings`, in its pattern)

| Code | Fires when | Evidence | Leaves |
|---|---|---|---|
| `radiating` | four or more hand-laid marks or films start within a small radius and fan out. | 6 | the daisy sentence in `PAINTER.md` step 5, in `RECIPES.md` x2, and in `scumble`'s docstring |
| `one-loop` | six or more hand-laid marks of one brush and colour family, one length (or a strict ramp of sizes), evenly spaced on a line. *A loop's signature: one length, one spacing, no clumps and no holes.* | 7 | the *any loop or generator* row's prose; the checklist's *a row of identical marks* |
| `buried` | the pixels this pass changed cover a large share of earlier **small** marks or marks noted `subject`: *this pass covered 41% of 9 earlier small marks -- a film is a mass at a depth*. Needs the canvas as it stood when the pass began: `run` already knows that moment (`before`, `cli.py:593`), so it takes one snapshot there. `look(diff=True)` is no use for this -- it diffs against the last *look*, not the start of the pass. | 9 | **closes the open depth-order item in `LESSONS.md` with a check instead of a fourth rewrite**; the checklist's *did a correction bury something* |
| `boxes` | share of the masses laid so far whose place is a rectangle. A measurement line rather than a finding. | fogged glass, pier (earlier) | the checklist's *is any mass a rectangle* |

Considered and **folded or dropped**: a *short chisel marks are bricks* rule -- it would
fire on *a small container*'s own recipe, where the rectangle is on purpose, so the
repeated case is left to `one-loop`. A *repainted twice* rule -- 0.5.0 already weighed it
and a region is not a passage. A *thin dark line along a silhouette* rule -- plausible
from the log, no cohort evidence; tier 3.

### E. Canvas measurements

Standing lines under the findings, like `ground:` -- a number, its scale, and where a
threshold is a judgement it says so. Thresholds are calibrated on the 21 finished PNGs
and their own notes, which say which pictures have which fault.

| Line | What it prints | Evidence |
|---|---|---|
| `values:` | the 5th-95th percentile of the values view, the three clusters and how far apart they sit: *0.15-0.35 of a box that reaches 0.14-0.96; no clear light*. | pier, heron 1 (no light until stroke 217), fogged glass (two largest areas 0.008 apart) |
| `edges:` | how the picture's edge length divides between hard and soft, by rise width on the values view: *94% of edges are under 2 px wide*. | 13 (GPT: *equally crisp boundaries*); `DIAGNOSIS.md`'s clip-art row |
| `holes:` | after a `solid=True` mass: unpainted share inside the shape, and where. | 2 |
| `pencil:` | graphite still showing, as a share. | checklist line |
| `unspent:` | in `checklist()` only: *232 of 300 unspent -- name the weakest passage*. | 15 |

`LESSONS.md` and `report()`'s docstring both say *the check cannot see a composition*.
That boundary is **kept and restated**: the check reads marks and measures the canvas;
it still does not judge an arrangement. Findings 14 and 15 stay with the painter, and the
`why` line is the instrument for them.

### F. Default moves -- each behind a probe

**Built, step 8, and two of the five survived the probe.** F3 (a banded `scumble` laid
`load=1.0, load_falloff=0.0`) and F5 (`_mass_overhang` returning `2.0` under `"hard"`),
each its own commit with a before-and-after rendered and looked at. **F1, F2 and F4
were declined** on the numbers under *What step 2 measured* below, and the declines are
written into `CHANGELOG.md` so they are not re-argued. Two things the build found that
the table did not: the inward `scumble`'s `load` is **not** already `1.0` -- the reason
column says it is -- and was measured (`0.005%` of a patch against `0.012%`) and left
alone; and `scumble` never called `_mass_overhang`, so F5 does not reach it, which it
does not need, because its passes are `pressure="even"` already and it has no pass-end
bites at any overhang. `NOTES-step8.md` has the rest.

| Candidate | Reason | Probe question |
|---|---|---|
| `cover()` -> `edge="hard"` | The plain recipe paints **3.07x** the area it is handed (measured in 0.4.0); Kimi and the fogged glass both buried `cover`'s own output. 0.4.0 declined to warn because the overrun is the recipe working -- so move the default instead. | Does a hard-edged repair read as a cut-out patch on a worked passage? |
| round-tip `block_in` / `sweep` -> `pressure="even"` | The docs already say *give it `pressure="even"` or it will show its passes at their ends*. | Any committed painting that relies on the taper? |
| banded `scumble` -> `load=1.0, load_falloff=0.0` | The inward form already defaults this way. The recipe calls it *the one that gets left off*: 0.9% bare against 0.0%, ripple 0.0021 -> 0.0008. All four cohort painters who laid a graded field typed the clause by hand. | What does a deliberately broken band lose, and is `load=` enough to get it back? |
| `scumble` with a `flat` -> halved `jitter` / `size_jitter` | Measured earlier at 0.112 peak to peak against 0.032; Kimi's scalloped horizon, GPT's banded sky. | Ripple with the halved pair on cohort bands. |
| `edge="hard"` -> two brushes of overhang | B8, measured: 1.9%-4.9% of the strip inside a slanted outline left bare at one brush, 0.016% / 0.000% at two. Nothing can cross the mask, so the only cost is dabs. | Does any committed `edge="hard"` mass change visibly? |

Not proposed, so they are not re-argued: `tip_wobble`'s default and `direction`'s default
(both weighed and declined in 0.2.0 / 0.4.0); ragged -> hard for chisel masses (wait for
what `chisel-staircase` does once painters have met it); and a tighter `density` under
`solid=True` with a comb (decided against: it says so with prices instead, B2).

Every move follows `LESSONS.md` trap 2: open both goldens, look, then regenerate.

### G. Documentation

**G1. The migration map** is section 5. Rule: a paragraph leaves only in the commit
that lands its check, and leaves behind one line carrying the code.

**G2. The entry path.** Painters told only to *install and paint* read ~2,600 lines
first, because the card says *read `PAINTING.md` once* and the file table says when to
read the rest. New path, as a hypothesis: the card -> `easel demo mistakes` (one sheet,
the six mistakes as pictures) -> the nine exercises (every session defends them) -> paint.
`PAINTING.md` becomes *the reasons, delivered by `easel explain` when a notice fires*.
The known risk is the pier's finding -- a card so sufficient the recipes went unread --
which notices that name the recipe at the moment of need are meant to cover. **That is
the first thing to look for in whatever run follows the release.**

**G3. `easel demo <recipe>`** renders *recommended call / common failure / smallest fix*
side by side from code blocks in `RECIPES.md` (finding 19). Each *Goes wrong as* gains
the failing block beside the prose. `scripts/check_guide_blocks.py` already runs all 80
blocks; extend it with the invariant that makes the docs and the tool one system:
**every recommended block runs notice-clean, and every failure block trips exactly the
code it names.** Finding 1 -- a recipe that produces the defect the guide warns about --
becomes impossible to ship.

**G4. `s.checklist()` / `easel check`**: the closing checklist as output. Measured lines
answered with their number (values, edges, ground, discs, bars or their crossings, boxes,
lightest, buried, pencil, subject share, unspent); the three judgement lines printed as
questions, with `why` quoted. `PAINTER.md`'s checklist shrinks to those three and the
call.

**G5. `easel diagnose <words>`**: ship `DIAGNOSIS.md` in the wheel (a sixth document:
`docs.DOCUMENTS`, the `force-include` list, `test_guide.py`), match rows, and print the
**target passage**, not the pointer. The only session that had the index followed zero
pointers; this makes following one free. Package-only painters have never had it at all.

**G6. One new recipe, collected not composed**: light broken down a surface toward the
viewer (noun-free heading per `LESSONS.md`), from the four cohort paintings' *accepted*
versions -- GPT's one connected mass with a broken lower edge, Kimi's five bent starved
strokes at the sides, Gemini's scattered broken flashes, DeepSeek's flashes shorter and
fainter toward the viewer. Its failure block is the `one-loop` demo.

**G7. Fixes to what is there. Built, step 9 part two**, and two of the five rows were
already closed by the steps that carried them. *A mass built of planes* and *a form that
turns* (finding 1) were **fixed in step 6**, in the commit that landed
`chisel-staircase`, because a worked example is an instruction and all three offending
recipes moved with the check. The ground contradiction (finding 11) went in **step 5**,
in the engine and the recipe together. What was left, and what it turned out to be:

- *A volume of lit air*: **dry after the films**, which was the missing clause. Measured
  rather than asserted, because B18 debunked the full-wetness story: the three films
  leave `0.14` at the core, and an opaque mark laid across the beam afterwards drags
  what it lands on by up to `0.30` in value where a mass crosses it and `0.40` where a
  stroke does.
- The card's `undo` row: F1 was declined and `spill` is not built, so the row **names
  `edge="hard"` itself** -- `2.32x` the area handed at `ragged` against `1.01x`. Finding
  8 said the card did not mention it; nor did `PAINTER.md`'s *What you are bad at*, and
  now both do.
- *Do not lay one broken pass across the whole canvas* against the graded field's
  *crossers*: **the rule gives**, scoped to what it was earned on -- a broken pass laid
  *under* work that sits on it -- with the crossers named as the deliberate exception.
  The rule was prose with no measurement behind it; the recipe came out of paintings.
- **And two the plan did not know about**, both found by running every guide block past
  the checks rather than by reading: the three answers under *Masses that are not
  rectangles* demonstrated `edge="clean"` at `size=0.09`, which is 34% of that mass's
  narrowest extent and trips `clean-small` -- a block contradicting the paragraph
  directly under it -- and the graded field drew its own top boundary inside the canvas,
  which cut the passes reaching it into stubs of `0.210` against a brush of `0.252` and
  tripped `scumble-wedge`. **Every runnable block in the guide is now notice-clean**,
  and `scripts/check_guide_blocks.py` fails if that stops being true, which is the first
  half of G3's invariant landing early because G7's fixes needed something to hold
  them.

**G8. Voice** (findings 17, 18). Every rule marked as **measured** (its number, its
`CALIBRATION.md` heading) or as a **habit** (*most painters so far...*). Numbers that
belong to a plan -- the stroke split, the ground share, three marks per small thing --
reworded as defaults `s.plan()` overrides. The call first, the sentence after. The
thirteen *you will...* in `PAINTER.md` go wherever a check now says it.

**G9. Small facts. Built, step 9 part two -- and four of the five were already there**,
closed by the steps that had reason to touch them: the install line carries both import
names and the *never `pip install easel`* warning; `REFERENCE.md` has the named-region
extents as a full table with the ninths called out in prose; what `upto=`, `n` and
`last=` count is on the `log(last=)` line (*log records, as `undo(n)` and `replay(upto=)`
count: a dry or a pencil line is one and is free*); and the verb x (`clip`, `edge`,
`solid`) matrix landed with #58. **Only one was genuinely open.**

**Vision is required** -- and none of the three places said so. All three *described* it
(*built for an agent that can see what it just did*; *for agents that can look at their
own work*), which is a design note and not a requirement, and the blind painter of the
cohort installed it, painted, and wrote *I can't see it ... so I'm trusting the tool*.
README, `llms.txt` and the package docstring now say it is a requirement and why: every
pass ends by looking, so a painter without image input can drive the whole API without
ever learning whether a mark landed.

**G10. Budgets, enforced.** `PAINTER.md` is 6,522 words against a 10,000 ceiling that no
longer binds. After the migration lower `FRONT_PAGE_WORDS` to what the file then is
(target about 5,000), and add a cap on the card (1,183 words today) -- *a rule nothing
enforces is a preference*.

**G11. The record.** `SUGGESTIONS.md` (step 1), `PAINTINGS.md` (link the two Claude
verdicts), `LESSONS.md` (the restated boundary; a multi-model cohort in the protocol;
the depth-order item closed), `README.md` / `llms.txt` (counts, the check's new shape),
`CHANGELOG.md` (no *released* claim until the tag exists).

### H. Validation -- the owner's, and not planned here

A guide change is a hypothesis until a fresh session paints against it, and this round
makes many; the owner runs that and it is not a step below. Two things in this plan exist
so that such a run can be *read* afterwards: notices are saved in the `.easel` file (A2),
so which codes fired on which pass is data rather than recollection; and section 5 is
the map back, if a cut turns out to have gone too far.

---

## 5. Migration map: prose that leaves, and what carries it

| Where it is today | What it says | Carried by | What stays |
|---|---|---|---|
| `PAINTER.md` card, *six things*, row 5 | the tool's own shape; staircase | `chisel-staircase`, and the existing round-disc rule | the row, shorter |
| `PAINTER.md` card, row 4; *you will reach for `undo`* | `cover` overruns; bury by hand | **neither carrier arrived** -- F1 was declined in step 8, and `spill`, built in step 6, is silent inside `cover()` by design. **Settled in step 9: nothing leaves.** The row and the paragraph keep the rule and now name `edge="hard"`, which the tool has had all along and the card never mentioned (finding 8) | the row, and the prose, with the keyword in them |
| `PAINTER.md` step 3, *a veil of light is a mass at a depth* | depth order of films | `buried` | the rule, one sentence |
| `PAINTER.md` step 4, *put the plan through `compare()`* | pairs that touch | `s.plan(values=)` | one line |
| `PAINTER.md` step 5, daisy sentence | radiating strokes | `radiating` | -- |
| `PAINTER.md` step 6, three things about `smudge` | size, along not across, once | existing size warning, `smudge-across`, `smudge-again` -- **two arrived in step 6 (D2)**: the three rules are one paragraph naming `smudge-across`, `smudge-long` and `smudge-wide`. `smudge-again` is tier 3, so *one pass, not three* stays | *lose one edge completely*; *one pass, not three* |
| `PAINTER.md` checklist, 13 lines | faults to look for | `s.checklist()` | the three judgement lines |
| `PAINTING.md`, *Wet paint*: dry first; glaze distance | | `wet-under`, `glaze-far` -- **`glaze-far` arrived in step 6 (D2)**: the glaze table is one line naming it, and the example stopped glazing raw alizarin. `wet-under` was dropped in step 2, so *`dry()` first* stays | the mechanism, short; *`dry()` first* |
| `PAINTING.md`, *The shape each tool leaves behind* | ten rows + three paragraphs | `chisel-staircase`, `cross-small`, `mass-is-a-stroke`, `shallow-box`, `one-loop`, and the existing small-bristle and round-disc rules (which get codes in A2) | the table as an index of codes |
| `PAINTING.md`, *Masses that are not rectangles*: spill, `inset` | | `spill`, `inset-lost` -- **`spill` arrived in step 6**, and the spill paragraph is one line naming it; the `inset` paragraph waits for `inset-lost`, which is tier 3 | the three remedies |
| `PAINTING.md`, 0-255 list clamps to white | | B13 raises | -- |
| `RECIPES.md`, every *Goes wrong as* | failure described in words | the failure block under `easel demo`, and the code it trips | one line |
| `RECIPES.md`, graded field: *the clause that gets left off* | | F (default) | -- |
| `RECIPES.md`, quiet gradient: a `flat` scallops; under five passes | | **neither carrier arrived** -- F4 was declined on the numbers (the halved pair moves the ripple `0.0053` to `0.0059`), and `scumble-few` is not built. **Settled in step 9: nothing leaves**, and the paragraph is unchanged | the whole paragraph |
| `RECIPES.md`, lost edge: stretch not boundary | | `smudge-long` -- **arrived in step 6 (D2)**: the paragraph is a line naming it, and the block above it, which smudged half the canvas, smudges a stretch | the paint-across recipe |
| `DIAGNOSIS.md` | symptom -> pointer | `easel diagnose` | the file, now shipped |

---

## 6. Order of work

One round, cut as 0.6.0, in PRs that each stand alone. The repository's rhythm is
*record the round as open*, then *act on it and cut*.

1. **Record the cohort as an open round.** A `SUGGESTIONS.md` section in the register's
   table format (what was wrong / what was done, left blank), seven painters, each
   finding labelled M/O/R; commit the two Claude verdicts and link them from
   `PAINTINGS.md`; copy the seven frames of GLM's that carry B18's evidence in beside its
   painting. No engine change.
2. **Measure.** `scripts/probe_cohort_session.py`, in the pattern of the six probes
   beside it: rebuild all 21 paintings from their committed pass scripts; re-measure
   every painter claim in 2a and 2d; for every candidate in D, E and F print how often
   it would fire, on which passes, and whether it fires on any block of the guide. **The
   output decides which rows of this plan survive.** Numbers into `CALIBRATION.md`.
3. **The notice channel** (A), including delivery to the CLI and MCP results.
4. **Bugs and API consistency** (B).
5. **`s.plan()`**, its effect on the bars, ground, subject and values lines, and the
   noise budget (C).
6. **Checks**, in three PRs -- D1, D2, D3 -- each with its paragraphs leaving (section 5)
   and tests in `tests/test_requests.py` in that file's pattern: one assertion that it
   fires with the exact substring, at least one that it is silent on the neighbouring
   right-thing case.
7. **Measurements** (E) and **`s.checklist()`** (G4).
8. **Default moves** (F), each its own commit with the goldens looked at.
9. **Docs**: `demo`, `diagnose`, `explain`, the new recipe, the fixes, the voice pass,
   the entry path, the budgets (G).
10. **Cut 0.6.0**: `CHANGELOG.md` without the claim, tag, then the claim.

### What step 2 measured, and what it decides

`scripts/probe_cohort_session.py` rebuilt all 21 paintings — **343 passes, 5,422 strokes**
— re-measured every claim in 2a and 2d, and ran each candidate in D, E and F against the
corpus and against the guide's own 70 runnable code blocks. The numbers are in
`CALIBRATION.md`; what they do to the rows above:

**Dropped, or not built as written.**

| Row | Why |
|---|---|
| `mass-is-a-stroke` (D1) | fires on **18%** of passes and on **9** of the guide's blocks, including `PAINTER.md`'s first `block_in`. Rule 2: wrong, not noisy |
| `shallow-box` (D1) | fires on **18%** of passes — the graded sky and sea bands that are the right thing |
| `wet-under` (D2) | fires on **22%** of passes and **8** guide blocks. Wetness is no gate: a fifth of every mark in the corpus lands on paint over `0.15` wet. B18 still shows the wet bezel moving pixels by `0.13`, so what is left is a *fact* line at the call, not a habit rule |
| `ring-steps`, `ring-rim` (D1, D2) | fire on **nothing** in the corpus and on one guide block each. Every committed inward `scumble` steps `0.014`-`0.021` a ring, well under any contour threshold. Their only evidence is GLM's lost take |
| `round-soft-mass` (D1) | never fires |
| F4, halved `jitter` on a `flat` scumble | the halved pair moves the ripple from `0.0053` to `0.0059`: nothing this measures |
| F1, `cover()` to `edge="hard"` | **no committed pass script calls `cover()`**, so the move is free and unevidenced. Do it with the `spill` notice or not at all. **`spill` is built (step 6) and says nothing inside `cover()`**, whose canonical call overruns about three times its cell by design -- so the move is the owner's to rule on, and nothing in the engine waits for it |
| F2, a round tip to `pressure="even"` | **0 committed calls** would move |

**Survive, with the threshold the corpus gives.**

| Row | Number |
|---|---|
| `chisel-staircase` (D1) | 6% of passes, 5 guide blocks — three more than the two recipe blocks the plan already fixes. Name them in the same commit. **Built, and not as written:** the prototype's window of angles measured how irregular a shape is, and was silent on the lit band `CALIBRATION.md` measures the staircase on. The rule is the mechanism instead — a pass end lands every `step × cot(theta)` down a side, so it is *nearest parallel* that a chisel steps worst — and comes in at **2% of passes and 3 guide blocks, all recipes, all fixed here** |
| `spill` (D1) | 4% of passes, 5 guide blocks. B17 is confirmed to the second decimal: **1.42x / 2.99x / 3.62x** at axis / 30 / 60 degrees. **Built in step 6, predicted rather than measured:** the engine's `spill` fires on 18 calls in 13 of the 325 painted passes -- **4%**, the prototype's own share -- and on none of the guide's blocks once the three that were painting their neighbours moved; where it spoke, the paint measured a median of `1.71x` (p90 `2.42x`) |
| `glaze-far` (D2) | 4% of passes, 1 guide block, and `0.08` **is the corpus's own p90**. **Built in step 6, measured once the film lands, on two lines**: the value shift at `0.08`, and how far the film was *mixed* from what it lands on at `0.07` in Oklab -- the case the reports were about, which moves the value too little for the first line to see (the harbour's searchlight moved it `0.020`). 38 of 222 films in 17 passes, **5%**; no guide block once `PAINTING.md`'s own example stopped glazing raw alizarin |
| `smudge-across` (D2) | 5% of passes, **0** guide blocks. **Built in step 6, and not as the prototype was**: its test fired on both heron necks and missed a hull dragged into the water. The engine finds each crossing on the path the stroke will be stamped down -- 11 of 37 smudges in 9 passes, **3%**, no guide block. And half of what finding 3 reported was an engine bug, fixed here: a smudge started loaded with white |
| `radiating` (D3) | 7% of passes, **0** guide blocks |
| `buried` (D3) | 17% of passes, 0 guide blocks — over the ceiling, so it needs a narrower gate than *four marks at half covered* before it is built |
| `smudge-long` (D2) | 6% of passes but **3** guide blocks, and the corpus median smudge is `0.168` long. The `0.10` threshold is far too low. **Built in step 6 on the length a path runs *along a boundary***, not its length: 14 of 37 smudges in 11 passes, **3%**, no guide block. The `0.10` stayed -- a strip along a hard step reads as a drawn line from `0.10` -- and the guide blocks that smudged a third and half of the canvas were the guide's own examples, now a stretch |
| `holes:` (E) | fires after 8% of passes. **A hole is a contrast, not a gap**: the same comb leaves `0.16%` on `toned_grey` and **`3.16%` on a dark ground** |
| F3, a banded `scumble` to `load=1.0, load_falloff=0.0` | **40 of 60** committed banded scumbles type the clause by hand; bare `5.17%` to `0.01%` |
| F5, `edge="hard"` to two brushes of overhang | **55 committed calls, none naming an overhang**: every one moves, so the goldens are the cost |

**Tier 3, on the evidence.** `one-loop`, `cross-small`, `scumble-few`, `smudge-again` and
`inset-lost` fire on one or two passes each. `one-loop` is the one to keep on the list
anyway: four of the seven painters reported the fault and the committed scripts hold it
twice, because they **rewrote the passage before delivering the painting**. The corpus
cannot see a fault that was repaired before it was committed, which is a limit of this
instrument.

**Two of section 2's own findings changed shape.**

- **Finding 15 is the cohort's and not the engine's.** Five of the six budgeted cohort
  paintings stopped under 45% of budget, median 42% spent; **none of the thirteen
  budgeted paintings before them did**, median 86%.
- **Finding 11 is older than this round.** Half the corpus finishes under the bare-ground
  floor, cohort or not. Resolving the contradiction (C) is still the right move; blaming
  the graded-field recipe for the cohort is not.

**And the rebuild found two things of its own**, neither of which belongs to this round:
`car_wash` and `pears` claim a rebuild and come back five marks over (`car_wash`
re-checked with only the nineteen passes its notes name, so it is not the pass list), and
two committed passes -- `pears/p9_rehearse_pear.py` and `heron1/pass1_draw.py` -- do not
run at all from a clean session, because each uses a name the passes before it never
define. Both want an issue against `PAINTINGS.md`'s reproducibility claims rather than a
row above.

---

## 7. Risks

| Risk | Guard |
|---|---|
| More warnings, read less. The project has watched this happen twice. | Noise budget from the corpus replay; facts before habits; said-once with state in the file; `s.plan()` declarations; **fewer than three findings and call-time notices on a median pass** as a target the probe reports. The standing measurement lines under a pass are not counted, as `ground:` never was (ruled 2026-09-21). |
| A check that fires on the right thing. | Rule 2: every block of the guide runs notice-clean in CI. |
| Canvas-reading checks slow a pass (already ~200 ms a stroke). | Sample along the path; one canvas pass per `report()`; skip all of it on `count_only` copies; time it in the probe. |
| Notices or the plan shift every later mark's texture. | Rule 8: stored beside `history.records`; asserted by the existing *planning verbs leave nothing behind* test, extended. |
| 0.5.0 cannot open a 0.6.0 file. | New keys only, read with `.get`; a round-trip test against a 0.5.0-format file. |
| Default moves repaint committed paintings. | Saved logs replay unchanged (arguments are in the log); only scripts that leave the argument off move; each is listed, and byte-for-byte claims in `PAINTINGS.md` are re-verified. |
| The doc cuts go too far. | Nothing is deleted without a check landing in the same commit; section 5 is the map back. *Too far* looks like boxes in backgrounds or skipped exercises rising in the next run. |
| **The remedies push toward cut-outs.** GPT and Grok laid every form as a hard-edged polygon and both name *flat cut-out shapes* as their picture's main fault; `chisel-staircase` and `spill` both point at `edge="hard"` / `clip=`. | The notices name the remedies in `PAINTING.md`'s own order, cheapest first -- passes *along* the sloped boundary, then a comb with a solid core, then `clean`, then `hard` -- and the `edges:` line (E) is the counterweight: a picture whose edges are all under 2 px wide says so whatever produced them. Watch this one in the next run. |
| Some of section 2 is wrong. | **It already was.** Checking workstream B while planning overturned four reported mechanisms (the holes are the comb or the hard-edge bites, not wandering passes; cp1252 does not break the tool; `region("bottom")` is a ninth, not a third; GLM's rings are an inward scumble's contours, not crossing glazes -- and the first *check* of that one was wrong too, until the painter's own frames were opened) -- every one of them reported as *observed*, which is the shape `LESSONS.md` predicts. Step 2 comes before everything else for the same reason, and the candidates in D, E and F have had no such check yet. |

---

## 8. Still open

Small, and none of it blocks step 1.

- What exactly printed the *dark* band in GLM's rings -- a ring in a dark colour, or a
  ring that picked up the wet bezel. The probe's reconstruction answers it (B18), and
  the answer decides whether `wet-under` is built at all.
- ~~Whether a banded `scumble`'s auto brush should be capped by the band's own shorter
  extent (B17), or only clipped and warned about.~~ **Settled in step 6: warned about,
  and not capped.** A cap at the band's depth still leaves `2.22x` at 30 degrees and
  `2.04x` at 60; a cap at half the depth brings the bars back (`3.2%` and `15.8%` of
  the band bare). `spill` names `edge="hard"` first (`CALIBRATION.md`, *Paint that
  lands outside the place*).
- Whether `easel_paint` should one day become the canonical import, given the unrelated
  `easel` on PyPI (B10). Not this round: the shim keeps the option open.
- **A fix that changes how a saved stroke replays.** The smudge fixed in step 6 (D2) no
  longer lays white where it starts, and that moves the first brush-width of every
  smudge -- including one already saved in an `.easel` file, which `CHANGELOG.md`'s
  preamble promises *always replays as it was painted*. The entry says so plainly.
  Whether the promise gains an exception for a stroke the engine got wrong, or a file
  saved before 0.6.0 should replay its smudges the old way, is the owner's.
- **Finding 13's spread, re-measured.** The `12%-44%, median 27%` in `CALIBRATION.md` came
  from the `edges:` prototype that step 7 withdrew, and *The measurement lines, on the
  finished canvases* says the corpus wants replaying with the shipped line before 0.6.0
  states a number. No step owns it. `scripts/probe_cohort_session.py` still carries the
  prototype as its own `edges_line(session)`, so the replay starts by pointing that at
  `easel.checklist.edges_line`.

---

## 9. File map: what will change

| File | Change |
|---|---|
| `src/easel/notices.py` (new) | `EaselWarning`, `Notice`, the `NOTICES` registry |
| `src/easel/plan.py` (new) | `Plan`, `Planned`, the `plan:` and `lightest:` lines, and the pairs. Not in this map when it was written: `plan()` was to be a method of `session.py` alone, and the value object plus its serialisation is a module's worth of anything. The `bands` and `ground` effects stay in `session.py`, where the rules they change already are |
| `src/easel/session.py` | `_notify`; the 17 existing sites; `plan()`; new `_check_*` functions; new rows in `_pass_findings`; measurement lines in `report()`; `checklist()`; `explain()`; `clip=` / `edge=` / `solid=` across verbs; B2, B3, B8, B9 |
| `src/easel/canvas.py`, `measure.py` | value clusters, edge widths, holes, graphite share |
| `src/easel/history.py` | signature exemption shared with `report()`; frame capture and the rehearsal-copy message (B3, B4, B15) |
| `src/easel/palette.py`, `regions.py` | B11, B13; `inset-lost`; region reprs |
| `src/easel/cli.py`, `mcp_server.py` | notices in results; `plan`, `check`, `explain`, `diagnose`, `demo`; stdout encoding; time-lapse from the log |
| `src/easel/docs.py`, `pyproject.toml` | the sixth document; lowered word ceilings; the `easel_paint` package |
| `src/easel_paint/__init__.py` (new) | re-exports `easel` (B10) |
| `scripts/probe_cohort_session.py` (new), `scripts/check_guide_blocks.py` | the measurements; the notice-clean invariant |
| `tests/test_requests.py`, `test_reference.py`, `test_guide.py`, `test_mcp.py`, `test_diagnosis.py` | one test per item, named for the request; the registry and doc-link checks; MCP delivery |
| `PAINTER.md`, `PAINTING.md`, `RECIPES.md`, `REFERENCE.md`, `CALIBRATION.md`, `DIAGNOSIS.md` | section 5 and G |
| `SUGGESTIONS.md`, `PAINTINGS.md`, `LESSONS.md`, `README.md`, `llms.txt`, `CHANGELOG.md` | G11 |
