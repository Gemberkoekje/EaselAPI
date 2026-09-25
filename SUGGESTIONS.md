# What the painters asked for, and what was done

Twenty-one sessions painted a picture from the guide and then wrote down what the engine
and the documentation had cost them — twenty-two paintings, because the ninth painted its
subject twice — a synthesis pass gathered the points more than one of them raised, and
the repository's owner put two further questions to the third painter. The winter
greenhouse was painted before the fogged glass and filed after it, in its own section
below, so [`paintings/`](paintings) and this register count the same pictures again.
This file is the register: **what was wrong, and what was done about it.**

**No round is open.** The newest, at the top, is the lighthouse handover — one painter
against 0.6.0, **6 engine items and 4 documentation items** — and every item in it is
done, in 0.7.0, folded in where it was filed rather than moved, as every open round
before it was. Below it is the 0.5.0 cohort — seven painters that
are not Claude, one picture each, **32 engine items and 6 documentation items** — and
every item in it is done, in 0.6.0. Everything below it is done too: 72 engine
items and 90 documentation items, all of them — the eighth session's eight and the
ninth's fourteen in 0.3.0, the tenth and the greenhouse's fifteen engine items and three
left-over documentation items in 0.4.0 with the install session's three, the pier
session's ten in 0.5.0 plus the one that was neither, and the hands session's six in
0.5.0 as well — that release was cut for the pier round, never tagged, and the round
filed after it went into it rather than into one of its own. The long arguments that
produced each one have been cut, because a request list is worth keeping only while
somebody still has to act on it. What
survives is the finding, because a finding is still true after the fix, and the handful
of places where the answer differed from the request. Three of the sessions painted one
shared subject; their lists were deduplicated into one round, and every number any of
them took was re-measured before anything was built on it.

**Done is not the same as right, and eight times now it has meant *measured and there
was nothing to fix* — the eighth by declining to build at all.** An engine item has a
test behind it. A documentation item is a
hypothesis until a fresh session paints against it, which is the rule
[`LESSONS.md`](LESSONS.md) opens with and the reason every line below says what was
changed rather than that it worked.

| Where the items came from | Engine | Docs |
|---|---|---|
| First session — a still life, 224 strokes, `paintings/Claude/windowsill_pears/` | 12 | 12 |
| Second session — an interior, 206 strokes of 300, `paintings/Claude/car_wash/` | 7 | 8 |
| Third session — a landscape at dusk, 184 strokes of 300, `paintings/Claude/lighthouse_dusk/` | 6 | 9 |
| The synthesis across all three, and two questions from the owner | — | 8 |
| Fourth session — a night street, 286 strokes of 300, `laundromat_night/` | 6 | 5 |
| Fifth–seventh — one subject, three painters, `lighthouse_greenhouse/{sonnet,opus,fable}/` | 11 | 8 |
| Eighth session — a pool at night, 221 strokes of 300, `paintings/Claude/pool_night/` | 3 | 5 |
| Ninth session — a heron in a flooded lot at dawn, 293 of 320, `paintings/Claude/heron_lot/1/` | 3 | 6 |
| …and its second attempt at the same subject, 253 of 320, `paintings/Claude/heron_lot/2/` | 1 | 4 |
| Tenth — a fogged greenhouse wall from outside, 311 of 320, `paintings/Claude/fogged_glass/` | 8 | 6 |
| The winter greenhouse — an interior at a low sun, 297 of 300, `paintings/Claude/greenhouse_winter/`; painted before the tenth, filed after it | 7 | 8, done as the documentation round |
| An install session — no painting; `pip install easel-paint`, and the reach for the guide | 1 | 2 |
| …and that session painting, 257 of 300, `paintings/Claude/pier_underside/`, in an empty folder | 5 | 5, and one that is neither |
| Twelfth — hands sorting dried beans, 329 of 420, `paintings/Claude/hands_beans/`, from the 0.4.0 wheel in an empty folder | 2 | 4, and one found while filing |
| The 0.5.0 cohort — seven painters that are not Claude, one picture each, told to install the package and paint and nothing about what to read: `paintings/{GPT,GLM,Deepseek,Gemini,Grok,Kimi,BigPickle_blind}/` | 32 | 6 |
| The lighthouse handover — a lighthouse at dusk, 171 of 300, `paintings/Claude/lighthouse_handover/`, the first painting against 0.6.0, from the package in a sandbox | 6 | 4 |

**How much each painter had read is the first thing to check before trusting any
agreement between them.** Only the first session is a clean measurement of the guide on
its own; the second read three other files first and the third read five. Where sessions
agree, that is painters finding the same thing with increasing context; where they
disagree, it may be the context talking.

- **The fourth** read four — the front page and exercises, then `PAINTING.md`,
  `RECIPES.md`, `REFERENCE.md` — and never opened `CALIBRATION.md`, so where a
  calibrated figure would have settled one of its findings it measured the thing again
  itself. The most-read session, not the widest-read one; discount its agreement with the
  third accordingly.
- **The eighth** read three — front page and exercises, `RECIPES.md`, `REFERENCE.md` —
  and nothing else. The split test's restricted arm, and the only session here whose
  items were raised without the essay or the numbers to check them against.
- **The ninth** read the eighth's three plus `DIAGNOSIS.md`, which no earlier session
  had: the restricted arm with the symptom index added, and the **only data point on
  whether that index works**. Told it could follow a `DIAGNOSIS.md` pointer into a
  withheld file and read the area named, it never once did — its own first finding.
- **The twelfth** read four, all through `python -m easel guide`, and nothing in this
  repository until its picture was finished, exported and reviewed. The first **blind**
  run of the package-only arm; the pier session before it had spent that morning inside
  the checkout, and its reading of the guide was discounted for it.
- **The 0.5.0 cohort were told nothing about what to read at all** — *install it and
  paint* — so for the first time what a painter read is the documentation's own choice
  rather than the owner's, and the entry path is a finding rather than a control. They
  read a great deal: ~2,600 lines, ~2,500 lines and *2000+ lines of docstrings* are the
  three counts they took themselves, and one of them read all five files. That is the
  round's largest documentation item and it is measured by the people who did it.
- **The lighthouse handover** read five of the six documents the package ships, all
  through `easel guide`, before its first mark — 194 KB, everything but
  `CALIBRATION.md` — though the card's first paragraph says to start after *The first
  hour*. It is the second painter in two rounds to read everything anyway, and the
  first to do it against the card and body 0.6.0 split them into, so its reading is
  the owner's own test of that split rather than a control.

---

## The lighthouse handover: one painter against 0.6.0

**Every item in this section is done, in 0.7.0** — six engine items and four
documentation items, from one painter — `claude-opus-5-5`, at max effort — which
installed `easel-paint` 0.6.0 from the package in a sandbox on Linux and painted a
lighthouse at dusk, *two warm lights handing over*, **171 of 300 strokes**. A row's
right-hand column was filled in when its PR landed, and not before. The candidate
answers, the decisions taken on them and the measurements that decided which survived
are in [`PLAN-0.7.0.md`](PLAN-0.7.0.md); what the round left open is at the end of this
section.

**It is the first fresh session to paint against 0.6.0**, so it is also the first run of
that release's hypotheses — the card and the body, the notices at the call, the plan
object, the demos — which 0.6.0 left to the owner's own run, and it answers the three
things the cohort's round said the next run should look for (*What the cohort's round
asked the next run*, below).

**It checked its own claims before making them**, with small tests it delivered with the
painting ([`verify/verify.py`](paintings/Claude/lighthouse_handover/verify/verify.py)),
and dropped two that did not survive — the labelling [`LESSONS.md`](LESSONS.md) asks
every round for, done unasked. **Kind** is assigned here all the same, as for every
round on this page — **M** measured by the painter, **O** observed, **R** reasoned —
because the painter labelled its tests rather than its claims. Every *what checking
found* below was measured on the checkout at `v0.6.0` on 2026-09-23, with the painter's
own scripts. **Two claims changed shape under that checking and are struck through where
they stand**: the side-by-side sheet that *does* take a glaze, and the seam the painter
had already withdrawn. Both were reasoned rather than measured, which is the shape
`LESSONS.md` predicts.

**The decisions are the painter's.** The plan's nine questions were put to the owner,
whose ruling is that the tool is for painters and any answer of his would be by someone
who would never use it directly — so they were forwarded to the painter, and its answers,
filed verbatim as [`answers.md`](paintings/Claude/lighthouse_handover/answers.md), are the
decisions this round runs under. Where it said it had no evidence — which edge reads as
paint, whether a parallel sheet pays — the bench measured, and the five questions the
bench left went back to it with the candidates under letters, to be read blind; its
answers are [`answers-step2.md`](paintings/Claude/lighthouse_handover/answers-step2.md).

### The engine

| What was wrong | Kind | What was done |
|---|---|---|
| **Hard edges are all-or-nothing**: `0.59` to `0.28` in one pixel at the tower, `0.36` to `0.17` at the waterline — *they read as vector graphics; the least paint-like thing in the engine, and I relied on it*. Confirmed to the hundredth on the rebuilt painting — `0.30` in one pixel on the tower's left side, `0.28` on its right, `0.19` at the waterline, `0.44` where the headland meets the sky — and the mask a clip is cut with (`Polygon.coverage` at two samples a pixel) leaves exactly one fractional pixel per side. **The `edges:` line printed between 54% and 65% under 2.5 px after every pass from the sea's on — eleven times — and nothing changed**: that is 0.6.0's own risk table — its remedies push toward `edge="hard"` and `clip=`, with the line as the counterweight — arriving, and a measurement printed nine times not holding. The painter's own count is the design constraint: of its 33 hard or clipped calls, 9 draw an edge and **24 only keep paint inside a shape**, which a feather reaching outward would break. And it was never the jaggies, which do not show at 1024×768: *the vector-clean edge was*. | M | **0.7.0: every hold breaks its edge inward, against the canvas's own tooth** — `feather=`, `0.002` of the long side left off, on `clip=` as well as `edge="hard"` and `cover()`: the painter's blind first choice, and its answer that the clips were the edges its verdict was about. Nothing lands on or past the drawn line, a side on the canvas frame is not an edge, and a shape narrower than four feathers breaks over a quarter of its width, where a clip two pixels wide had kept 37% of its paint. `feather=0` cuts the edge on the line, which is the horizon's answer. A saved mark replays at the feather it was laid with, so no saved painting moves; a script that leaves it off lays the broken edge. The unit was benched at 1440, where the painter found the bench's copy chewed: built, the edge there bites at the export's own pixels as 1024's does. **And for rock, `roughen()`** — the painter's own fifteen lines — walks an outline off its line, calmed where something stands on it. The `edges:` line cannot see either, by construction: the answer went into the engine, not the line. Two masses held to one line on bare ground both break back from it and leave the ground between them; no committed painting does that, so it is a number in `CALIBRATION.md` and not a check. |
| **Dry-brush speckle reads as dirt** more often than texture — flecks in the sky, the first swells, blue specks in the first surf. Measured on the sky's own crosser (`bristle`, `size=0.065`, `opacity=0.40`): at `load=0.45` it lands **509 pieces with a median of 4 px**, 58% of them under 4 px, at a median contrast of `0.009`. The tooth gate is per pixel at the weave's scale, so a starved brush leaves confetti where a real one leaves streaks — and the painter was using the loads the guide recommends for a broken mark, 0.35 to 0.6. Its workaround, films for the swells, dropped the texture it wanted. | O | **0.7.0: a brush running dry drags.** Under `0.9` of its load, and wholly by `0.7`, the tooth a brush is gated against is read along the stroke's own travel -- a thread of linen long, and given back the tooth's own values rank for rank -- and a `bristle` comb's bristles run dry one by one, each keeping its own share of the canvas and the comb between them the stroke's: B1+B2, the painter's pick, tuned so each load lays what it laid. The crosser at `load=0.45`: 571 pieces with a median of 4 px become 125 with a median of 12, nearly three times as long along the travel as across, and the specks under 4 px carry 1% of its paint where they carried 8%; the painter's first surf becomes strokes of foam. Summed over 24 strokes, a starving `bristle` on linen lays `0.99` to `1.02` of what it laid from `0.30` to `0.8`, and a loaded brush, or a dab of any tip but `bristle`, lays exactly what it did. Looked at side by side as the painter asked, B2 alone is dots again once it lays today's paint and B1+B2 is dragged rather than combed, so the kernel is the same on a comb. **A fix that changes what a rebuild lays**: named under 0.7.0, and a file saved before it says as it opens how many of its marks ran dry -- every mark whose load fell under `0.9` somewhere, a preset's run-down tail included, not only the ones laid starved: 65 of this painting's 173, and 2,788 of the corpus's 5,628. The fact at the call the plan held back is not built: the flecks it would have described are gone. |
| **One check misfired, twice**: *graded passage laid too narrow* on marks that were not one. **Not reproducible from the scripts** — the line fires on none of the thirteen committed passes — because both fires were printed by rehearsals of passes rewritten before they were committed, and nothing saves what a pass's check said. **Then reproduced**: the painter rebuilt both passes from its transcript, and each prints its original line exactly ([`misfires/`](paintings/Claude/lighthouse_handover/misfires)). In both, the brush the line names is a `0.006` accent — a crevice along the join of two rock faces laid at `0.03` and `0.07`, a ripple among glints — and the rule judges a stack's step against its *narrowest* brush. Over the corpus it fires on 9 of 325 passes, never on a guide block. | O, then M | **0.7.0: what the check said is saved.** Every `easel run` and MCP `run` keeps the block it printed after a pass in the session file — **rehearsed and counted passes included**, each saying which, with the log index it began at — read back with `s.reports()`, `easel log --reports` and `log` with `reports`. So a fire on a rehearsal is in the file after the pass is rewritten, which is the painter's rider on the question: *only worth having if rehearsals are in it*. Writing the file after a rehearsal meant closing a leak first: the copy shared the painting's palette, landmarks and guides, so a mixture tried on the scrap of canvas stayed on the painting, and the painter's own harness, trying variants one after another on `scratch()`, started each on the last one's mixtures (its variants re-mixed every slot they used, so no picture of its changed). **And 0.7.0 narrows the rule to a passage laid one stroke over the next**: its run breaks between two neighbours whose reaches along the stack share under 30% of the shorter one's — the painter's pick, made reading the corpus's crops blind. The water misfire's glints and ripple fall apart into marks and are told nothing; the recipe's failure block still fires. Over the corpus it fires on 7 of 337 painted passes where it fired on 9, keeping the three stacks the painter read as passages coming back as bars and going quiet on three of the six it read as separate things. It still tells separate masses stacked edge to edge, which overlap along the stack as a passage does — the headland misfire among them; the clause tried against that kind, judging the run by its median brush, silences every passage among the fires, so it was not built. One of the three it keeps, the pier's water, it tells for the wrong brush: a reflection laid across the field rather than the field's own. |
| **About 15 seconds a variant**, in the one run timed. Confirmed, **and it is the paint**: a three-band sky variant as the painter's harness ran it takes 11.5 s here, 10.3 s of it the three 8-pass scumbles at full width, 0.15 s the look and 0.01 s the copy. The painter never used `rehearse(vary=)`: its variants were whole passes, and what it asked for is scripts rehearsed as alternatives side by side — which `easel run --rehearse a.py b.py` does not do, because it lays them in order on one copy. | M | **0.7.0: versions of a pass, side by side.** `easel run p.easel a.py b.py --alternatives` rehearses each script on a copy of its own, with its own check and its own saved report, and lays their looks in one sheet, each panel labelled with the script and the strokes it laid; `s.rehearse_each([...])` does it from Python, where a version is a plan or a function handed the copy, and the MCP `run` takes `alternatives` and hands the sheet back inline. Every copy is seeded as the next marks of the painting, so the version chosen and then run for real lands as its panel shows it — checked on the painter's own two skies, `try_sky3.py`'s B and C, which take 32.1 to 32.3 s for the two through `--alternatives`, loading and saving the file included, against 31.9 to 32.8 s through its harness. The time is the paint, as it was — about 16 s a version, the painter's own fifteen — and what changes is one sheet where there were two files and a montage. A version that raises is said and the others are still rehearsed. **The panels in parallel (D1) were not built**: 1.6 to 1.7 times one panel in four processes, against a target of 1.5. The sheet draws each copy as a rehearsal's own look does, landmarks and drawing included, where the painter's harness looked at its variants without them. If it asks, the build is the view switches `easel look` has — `--no-marks` and `--no-sketch` on `easel run`, for the rehearsal's look and every panel alike, and `marks` and `sketch` on the MCP `run` and on `rehearse_each`. |
| **`easel look` has `--no-sketch` but no `--no-marks`**, so the landmark labels covered small details; the painter wrote a helper. Confirmed: `look(marks=False)` exists and `PAINTING.md` names it, but the CLI has no flag for it and the MCP `look` tool has no argument for it. ~~And one worse: nothing at any level hides the guides — the helper's clean views still show every guide line it drew.~~ *Corrected when it was built: `sketch=False` hides the guides with the pencil, and always has — the helper passes it, and a look with a guide drawn and `sketch=False` differs from one with none in no pixel. Nothing said so.* | M | **0.7.0**: `easel look --no-marks` and `marks` on the MCP `look` tool, so the helper is `easel look p.easel --no-marks --no-sketch`; `--no-sketch`, the MCP `sketch` argument, `look()`'s docstring and `PAINTING.md` now say the guides go with it. The separate `guides=` switch planned on the struck claim was not built: nothing asked to see the pencil without the guides. |
| **Session files are large**: 16 MB after 171 marks. **55% of it is the time-lapse** — 174 frames at 360 px, stored raw, 8.83 MB — against 6.57 MB of canvas; frames left out, the painter's own file re-saves at 7.64 MB. Storing colour as float16 would save another 4 MB and move 2.6% of the export's pixels by a level, which *opens as it was painted* forbids. The painter exported its GIF once, at the end. | M | **0.7.0: the frames leave the file.** The painting rebuilt as it was painted saves at 7.37 MB where it saved at 16.43, and colour stays float32. A session loaded from a file records no frames — one recorded after a load would begin the film in the middle of the painting — and rebuilds its film from the log when asked, at its own frame size: frame for frame the film it recorded, for a full repaint (26.6 s here) where it was a read (2.4 s). A file saved before 0.7.0 that kept its frames still uses them. Every pass from the shell is cheaper for it — the thirteen take 36.5 s where they took 45.6 — so a painting that makes one film at the end spends about 15 s more in all, the trade the painter chose. And, on the painter's rider to the version, **the file says which release saved it**, and one saved by an earlier release says so as it opens when a fix since then lays some of its marks differently (`older-engine`), with how many and the release to rebuild it under. |

### The documentation

| What was wrong | Kind | What was done |
|---|---|---|
| ~~**The built-in side-by-side comparison doesn't support soft blends or glazes.**~~ **It does**: `{"points": ..., "glaze": True, "color": ..., "opacity": ...}` is a stroke entry of a plan, as is `{"points": ..., "smudge": 1.0}`, and a `vary=` sheet of three opacities of the painting's own beam rendered in 1.7 s. **No document says so** — ~~`REFERENCE.md`'s plan grammar names a stroke, a mass, a sweep, a scumble and a burial~~ *(corrected when it was built: `REFERENCE.md` named three of the five kinds — a mark, a mass and a sweep — and only the MCP server's plan help named the passage and the burial)* — and the painter's answer to the plan makes the same gap twice: *whole passes of scumbles, strokes and glazes, which as far as I could tell can't go into a plan*. They can. | R | **0.7.0**: the grammar names all five kinds, and the film as a mark **with the glaze verb's brush and opacity written out** — an entry takes a stroke's defaults, and `{"points": band, "glaze": True, "color": c}` is a bristle film at `0.88`, not a glaze — with `to_value=` staying with the verb; and one sentence says a whole pass is a plan. The same in `preview`'s and `rehearse`'s docstrings and the MCP plan help, held by `tests/test_reference.py`. **The smudge entry was not named**: written as a mark it takes the smudge brush's own `0.07`, the width the verb's `0.02` default was moved off, and says none of `smudge()`'s three notices — so naming it would hand a painter the lobe the verb exists to stop, and no painter asked for it. |
| **One sentence is backwards.** The lit-air recipe calls a glaze at pressure `[1.0 … 0.1]` *narrow-and-bright at the source and wide-and-gone at the far end*; the painter measured 80 px at the source and 32 at the far end. Confirmed against the source: a round tip's width follows pressure, so full pressure is the wide end. The recipe's code is right and its sentence is not — *the one factual error I found was in prose*. | M | **0.7.0**: the sentence says what the code does — `[1.0, ..., 0.1]` is wide and bright at the source and narrow and gone at the far end, the core and the body thinning away from the light, and the wide faint film runs the other way so the cone opens as it travels — and cites *Pressure* in `CALIBRATION.md`, where a light touch keeps about a third of the width. The block and its demo are unchanged, because they were right: laid alone, its core is 49 px across near the light and 16 where it gives out, and the wide faint film 90 px and then 159, the one that opens the cone. |
| **A caveat far from its rule.** `RECIPES.md` says a pressure list fades a soft blend to nothing at one end; measured, a scumble at `pressure=[1.0, 0.75, 0.25, 0.0]` went from `0.86` to `0.41` over a `0.14` field at opacity 0.9. **Both are right, about different things**: the painter read the last *third*, where the profile ~~still averages a quarter pressure~~ *(corrected when it was written: averages `0.135` of full pressure — the passes run from frame to frame)*, and ~~over the last 4% of the width it reads `0.20` — it does reach nothing, at the very end~~ *(corrected by the painter after step 2: over the last 4% it reads `0.183`, `0.034` above the field — close, and not arrived)*. What the recipe does not say is how fast the fade arrives, and the reason — dabs overlap and accumulate, ~~so a quarter pressure lays a quarter of a step~~ *(corrected when it was written: a quarter pressure lays two-thirds of the step on this band)* — lives in `PAINTING.md`, not beside it. | M | **0.7.0**: *A passage brightening toward one side* says **the fade arrives late**, with the number beside the rule — at the recipe's own `opacity=0.5` a quarter pressure moves the value over half as far as full pressure does and a tenth still a quarter as far, and the painter's band reads `0.41` over its last third and still `0.19` over its last twentieth, where its list runs out — and names the reason where it lives, *`opacity` does not thin a long stroke* in `PAINTING.md`. The measurement is a table under *Pressure* in `CALIBRATION.md`: the share of the change a pass makes at one pressure, on the recipe's six strokes and on the painter's band, at two opacities. The sentence the plan had drafted for it, *a quarter pressure still lays a quarter of the step*, was reasoned rather than measured, and did not survive the measurement. |
| **Too much text**: about 340 KB across six documents and 180 KB read before the first mark; *essay-like, dense cross-references, key facts buried in paragraphs*. The sizes are right — 341 KB for the six, 194 for the five it read. The reading was its own choice: the card says to start after *The first hour*. Asked, its answer is *watch* — and *if you ever cut, start with what the notices already say at the call*. | M | **Watched, as the painter ruled, and nothing cut** on one painter's word. `LESSONS.md` records the data points under its protocol: told by the card where to start, the painter read everything; it never ran `explain` or `diagnose`, because the one-line notices were enough, so the link from a notice's code to its `DIAGNOSIS.md` row stays unbuilt, on the evidence; it read three rules and broke them, and a rehearsal caught each; and its instruction for whichever round does cut, *start with what the notices already say at the call*, is written beside them. What watching saw: the five documents it read are 202 KB where they were 194, most of the difference `REFERENCE.md`'s new arguments, and `CALIBRATION.md`, the one it never opened, grew by 54 KB with this round's measurements. The two answers of this round a painter meets without reading a word are the engine's: a held edge that breaks, and a dry brush that drags. |

### Withdrawn, and recorded so it is not filed again

- ~~**A vertical seam, blamed on the sky blends.**~~ Withdrawn by the painter, which could
  not reproduce it in a minimal test and put it down to *how I layered wet paint*. Not
  reproduced here either, wet or dried: the three committed sky ramps on a fresh canvas
  show a median column jump of `0.0002`, largest at the canvas edges. The wet layering is
  real and large — drying between the bands moves a third of the canvas by more than two
  8-bit levels — and draws no seam. (O, withdrawn.)

### What the check cannot see

Not items, and recorded so they are not filed again: **the picture** — *competent,
coherent, conventional*, the headland failed twice and was patched with brushwork where
the card says to go back to the drawing, and 43% of the budget left, *partly caution*.
`unspent:` printed 129 and the painter stopped anyway, at 57% of its budget — past the
45% the cohort's finding 15 was counted under, so that count stays five of six, and well
short of the 86% median of the thirteen budgeted paintings before the cohort. The reason
it gives is the cohort's: more marks were a risk to what stood on the headland. **A
repainted-passage count** was considered for it and
dropped: the headland took four passes and so did the tower, and the log cannot tell a
passage failing from a subject being built. Both stay with the painter's own sentence,
`s.plan(why=...)`, which this painter wrote and was quoted back.

### What the cohort's round asked the next run

The cohort's round ended by naming what the next run should look for first. This is that
run, and it answered all three:

- **The way in.** The known risk was a card so sufficient that the recipes go unread.
  The opposite happened: the painter read everything, and the two passages it rates
  best — the beam and the broken reflection — came from recipes and `easel demo`. What
  steered it, by its own account, was the notices at the call, the recipes with `demo`,
  and the plan's `lightest:` line.
- **The code-to-symptom link.** It never ran `explain` or `diagnose` — *the one-line
  notices were enough* — and never opened `DIAGNOSIS.md` or `CALIBRATION.md`. One data
  point, and the one the ruling of 2026-09-21 said to wait for: **not built, on the
  evidence**, and recorded in `LESSONS.md` under *About the protocol*.
- **The cut-out risk.** It arrived, as recorded in the first engine row: over half the
  edges under 2.5 px on eleven passes running, printed and not acted on.

### What worked, recorded because a finding is still true afterwards

The painter defended these unprompted, and **nothing in this round touches them**:
rehearsal seeded as the next real strokes (*exactly what lands when you commit it*,
which caught an egg-shaped glow, a panel stuck on the headland, gold-coin reflections and
a stair-stepped tower before a mark was paid for); the notices naming the problem and the
fix — a glow too shallow for its technique, pointed at *a volume of lit air*, and the
grass's brush size; the plan held against the checklist, and the `lightest:` line
catching the lantern at `0.74` losing to the glow at `0.77`, *the one number my whole
idea depended on*; `cost_line` finding a 32-mark cliff face where 15 did the job; an
error message carrying the exact numbers; and learning the whole tool from the command
line without opening a file. **Reading the rule did not stop the mistake, again**: *I
read three rules and then broke them anyway ... Looking at rehearsals caught those, not
reading* — the eighth painter to say so.

### The painting, and what the painter owns

- **A postcard subject done the safe way**, in its own words; *ruled tower edges, flat
  fills, crisp masked outlines*, and the paint quality living mostly in the sky.
- **What it would do differently**: a later, darker dusk so the lamp dominates more;
  fewer, larger rock planes decided while it is still a drawing; a headland that
  dissolves into the water in more places; some of the warm ground left showing.

### What the round left open

Recorded here because the plan and the step notes they were written in leave the
repository once 0.7.0 is tagged. Everything else the round declined or put off is written
where it was decided: the stacked masses the graded rule still tells, and the pier's
water it tells for the wrong brush, in the finding-3 row above; the view an alternatives
sheet draws, and D1, in the finding-4 row; two masses held to one line in
`CALIBRATION.md`; the dab loop among `LESSONS.md`'s open items, as *about 200 ms per
stroke*; the code-to-symptom link under its *About the protocol*; and the rebuild claims
of `PAINTINGS.md`'s rows in [#70](https://github.com/Gemberkoekje/EaselAPI/issues/70).

- **What the next run should look for first.** The round's two engine answers are the
  ones a painter meets without reading a word — a held edge that breaks, and a dry brush
  that drags — and both were chosen blind, from sheets, by a painter that has not painted
  with either. The `edges:` line cannot see the break, by construction, so only a
  painter's eye says whether a broken edge reads as paint and a streak as texture. The
  next run is also the second against the card and body 0.6.0 split the guide into — the
  second data point on whether a painter told where to start reads everything anyway —
  and the first that can reach for `--alternatives` unasked.
- **A smudge as a plan entry, if a painter asks for one.** Not named, for the reason in
  the first documentation row above. The build is a kind named for the verb, in
  `cover`'s pattern — `{"smudge": edge, ...}`, laid through `s.smudge()` with its width
  and its notices — and the trap is that `smudge` is already a brush field and `glaze` a
  stroke keyword: the kind is told apart by its value's type, a path or a place and not a
  number or a bool, and checked after `shape`, `edge`, `band` and `cover`, so that
  `{"shape": s, "smudge": 0.3}` stays a mass with a brush override.
- **Three things left as they were.** `foreign-out-dir` is said at load and kept on the
  session, so every save writes it again, and rehearsals save now — rare, since a file's
  `out_dir` has to be neither the working directory nor beside the file. `easel timelapse
  --from-log` is ignored when the output is a `.png`: a contact sheet has no size to
  rebuild at. And the tooth a dry brush drags along is read once per canvas, a field for
  each ten degrees of travel — sixteen and 50 MB for this painting at 1024×768, about 90
  at 1440×960 — and kept in float32: float16 would halve it and move every golden again,
  for memory nobody has run short of.
- **`LESSONS.md`'s count of re-measured claims is older than the last two rounds** —
  *thirty claims have now been re-measured before anything was built on them, and eight
  did not survive*, written for the hands session's — and was left as 0.6.0 left it:
  bringing it up to date means counting both rounds' claims again, the cohort's and this
  one's.

---

## The 0.5.0 cohort: seven painters that are not Claude

**Every item in this section is done, in 0.6.0** — thirty-two engine items and six
documentation items from seven painters, GPT, GLM, DeepSeek, Gemini, Grok, Kimi and
BigPickle, each of whom installed `easel-paint` 0.5.0 from the package and painted one
picture. A row's right-hand column was filled in when its PR landed, and not before. The
candidate answers, and the measurements that decided which of them survived, are in
[`PLAN-0.6.0.md`](https://github.com/Gemberkoekje/EaselAPI/blob/v0.6.0/PLAN-0.6.0.md), as tagged; what the round left open is at the end of this
section.

**Kind** is this project's own distinction and every finding below carries it: **M**
measured by the painter, **O** observed, **R** reasoned. It is the first thing to check
before acting on a row — and the uncomfortable half of this round is that **all four of
the reported mechanisms that have already died on checking were reported as *observed***,
which is exactly the shape [`LESSONS.md`](LESSONS.md) predicts: a painter watching its own
canvas sees the symptom truly and the cause not at all. See *Four reported mechanisms
that did not survive* below.

**They were told to install it and paint, and nothing about what to read.** That is the
one thing that makes this round different from every other on this page: the ~2,600 lines
three of them counted before their first stroke is the documentation's own entry path
being followed, not a reading list somebody handed them. So the entry path is a finding
here rather than a control, and *how much each painter had read* is, for once, the
documentation's own answer rather than the owner's.

**None of them is Claude**, which is the second difference and the reason a repeated
finding here is worth more than a repeated finding above. Where seven painters that
share no architecture hit the same wall, it is the wall.

**One painter could not see its own picture.** BigPickle has no image input and painted
the whole landscape without opening a single look. The decision taken on that is that
**vision is a requirement of this tool and the documentation should say so** — one
documentation item below, and the reason the rest of BigPickle's verdict is weighted as a
reader of the documentation rather than as a painter of the picture. Its stack-of-bars
warning, alone in this round, was a true positive, which is the one thing keeping that
rule alive.

**What every one of them defended, unprompted, and this round does not touch:** rehearsal
seeded as the next real strokes, `at_value` and errors that teach, `cost_line` naming the
lever, one plan object for `cost`/`preview`/`rehearse`/`paint`, determinism. Recorded
under *What worked* below, because a finding is still true afterwards.

### What the tool did not catch, though the documentation names it

**Nine failures the guide describes in prose and the check is silent about.** This is the
round's centre and the reason it is one round: the owner's goal is that wherever the tool
can know a thing, the warning comes out of the tool and the paragraph leaves the guide,
which is [`LESSONS.md`](LESSONS.md)'s own growth rule asked for at scale.

| What was wrong | Who | Kind | What was done |
|---|---|---|---|
| **Chisel staircase down a sloped boundary.** Kimi's rock faces are `RECIPES.md`'s *mass built of planes* call character for character (`pass4_lighthouse.py:16`) — a ragged `flat` on sloped polygons — and came out stair-stepped, which its verdict names as the picture's first weakness. *A worked example is an instruction*: the recipe produces the defect the guide warns about. Today: prose and a table row in `PAINTING.md`, no check. | Kimi; winter greenhouse ×4, Opus (earlier) | O | **`chisel-staircase`, and the mechanism rather than the window of angles the plan proposed.** The step down a side is `pass step × cot(theta)`, so it is *nearest parallel* that a chisel steps worst and a side laid exactly along the passes takes no pass ends at all — the opposite of what the prototype gated on, which asked how far from square a boundary was and so measured how irregular a shape is. Measured, that prototype was **silent on the lit band `CALIBRATION.md` measures the staircase on** and silent on Kimi's rock face, while firing on an ellipse, a blob and a rectangle swept at 28 degrees — three shapes with no straight side to align to, and so no remedy to offer. The rule counts the pass ends that will land on a side the passes run nearly along and how far each steps from the last: **2% of the corpus's passes against the prototype's 6%**, with the floor at the corpus's own p90. It fires on three guide blocks, all recipes that produce the fault, and all three are fixed here — *a worked example is an instruction*. `edge="hard"` is no longer offered as a repair by anything: it is pass ends **inside** the mask and measures 22% to 20%, and `PAINTING.md` claimed it closed them until now. The staircase paragraph leaves `PAINTING.md` and the card row loses the wrong remedy; the measured repair table is in `CALIBRATION.md`, where `easel explain chisel-staircase` prints it. **And the fix was taken too far, and came back (G3).** Step 6 laid the recipe's faces with the notice's second remedy, a comb, at `0.014`–`0.02`, where a bristle is four streaks with gaps: the recipe painted the *woven surface* its own *Goes wrong as* names, and `report()` said so on 59 marks, which the notice-only block check could not see and G3's demo did. The faces are now a `flat` laid `edge="clean"`, each along a side of its own, and the notice offers the comb only at `size=0.025` and over. |
| **Holes inside a `solid=True` mass.** GPT closed three by hand (`paint.py:630 solid_joins`), Grok one (`pass6_repair.py`). The holes are real; the reported cause — shaped block-in paths wandering apart — did not survive checking. Today: nothing fires. | GPT, Grok | O | **`solid-comb` fires**, as a fact with the prices on it rather than a habit rule: the share that comes back bare (`0.16%` in 47 blobs on a mid ground, `3.16%` in 373 on a dark one), and what closes it — `density=1.2` at about a fifth more passes, a solid tip at any density, crossed passes at twice. 10 of the corpus's 198 block-ins, and **none** of the guide's 70 runnable blocks. No default moved: a comb is the right brush for anything with strands in it. See B2 below. |
| **Smudge drags a bright thumbprint** out of the light mass and into the dark one. Grok took every smudge back out of the painting because of it. Today: prose, and a warning that fires only on `size > 0.03`. | GPT, Grok; laundromat 4 of 5, car wash ×2 (earlier) | O | **Half of it was the engine's, and is fixed; the other half is `smudge-across`.** A smudge started loaded with its nominal titanium white and laid 55%, 30%, 17% of it in its first dabs — a light cap at the start of every smudge, on one colour as much as at a boundary, which is how a pier's dark piles each got a light spot in the middle. It now starts from the first colour it touches. The round's own probe had measured that cap as the crossing: light carried **4.1 brushes** into the dark by a pass that started in the dark, **0.5** once fixed. What is left is the painter's: dragged across a boundary a smudge carries the first mass about a brush into the second, either way round, and the call says so when the path crosses a step of `0.10` — 11 of the corpus's 37 smudges, 3% of passes, none of the guide's blocks. The prototype fired on both heron necks and missed a hull dragged out into the water; the engine finds each crossing on the path. `smudge-long` says what a long pass *along* a boundary leaves, and `PAINTER.md`'s three rules about `smudge` are one paragraph naming the codes. |
| **A glaze far from its ground**: green blooming over blue water; a downward glaze of afterglow reading as a searchlight on a flat sheet. Today: prose and a table; `to_value=` exists and nothing fires. | GPT, Grok; Opus, Fable, pool, heron (earlier) | O | **`glaze-far`, read once the film has landed, on two lines.** The value moved `0.08` or more — the guide's own *a stripe of a different colour* — or the film was mixed `0.07` or more from what it lands on, in hue and chroma. The second is the one these reports were about: the harbour's searchlight moved the value `0.020` and was mixed `0.085` off the water, which no value line can see, where the guide's own recipes mix their films `0.031`-`0.051` off the field. How far a film moved the hue was measured first and does not separate the two. 38 of the corpus's 222 films, 5% of passes, none of the guide's blocks once `PAINTING.md`'s own example stopped glazing raw alizarin. `to_value=` answers the value line and not the mix line. `PAINTING.md`'s glaze table is a line; the table lives in `CALIBRATION.md`. |
| **Paint laid over a still-wet film printed concentric rings** and cost the session's one `undo`. Today: prose (*`dry()` first*); nothing fires. The rings are real — the painter's own frames show the glazes did not print them, and the cause is still open. | GLM; Opus ×2, laundromat (earlier) | O | **The recipe's missing clause, in step 9; the check declined.** The rings were an inward `scumble`'s own contour rings, laid over a bezel still wet, which moved them by up to `0.13` (`CALIBRATION.md`, *GLM's rings*). *A volume of lit air* said `dry()` before the films and nothing after, so the next opaque mark landed on three wet ones. It dries after them too now — measured rather than asserted, because B18 had already killed the full-wetness story: the films leave `0.14` at the core, and a mark laid across the beam afterwards drags what it lands on by up to `0.30` in value where a mass crosses it and `0.40` where a stroke does. **`wet-under` (D2) is not in 0.6.0** (ruled 2026-09-21): as a habit rule the probe had it on 22% of passes and 8 guide blocks, and the fact line at the call that was left of it rests on a reconstruction of a take the painter overwrote. *`dry()` first* stays in `PAINTING.md`, and `CHANGELOG.md` records the decline. |
| **Strokes radiating from one point**: a wagon wheel where light was wanted. Today: prose in three places. | Gemini; fogged glass ×2, Fable, car wash (earlier) | O | **`report()` names a daisy, and not as the prototype did.** Gathering marks that start near one another fired on 22 passes; looked at one by one, one was a daisy — the fogged glass's tree, *spoke-like* in its own verdict — and the rest were pine branches, pot rims, perspective bars, fingers and a fan of sun rays. The rule is five or more marks, each a line at least twice as long as its brush is wide, leaving one point — where consecutive marks' lines meet — with no gap in their directions over 90 degrees. It names the tree and nothing else in the corpus, and none of the guide's blocks. A tree's fork leaves 120 degrees, grass and a fan of rays nearly 300, and a glow of wide films is not lines: the heron's lamp, five films crossing at it, was one film short of being called a daisy until the width clause. `PAINTER.md` step 5's daisy sentence leaves; `RECIPES.md` and `scumble`'s docstring point at the check. |
| **One loop's signature.** A column of same-length marks for a reflection on water — *floating rectangles*, *small bricks*, *a ziggurat*, *spoon-shaped islands*, four painters' own words for the same thing. **Four of seven failed the same passage the same way first, and `RECIPES.md` has no entry for it.** Today: one table row (*any loop you write*). | DeepSeek, Gemini, Kimi, GPT | O | **`report()` names a loop's signature**: six or more consecutive hand-laid marks of one brush, at one length or a strict ramp of lengths, spaced along a line within `35%` of their mean gap, and further apart than their own width. **It fires on one pass, and it is DeepSeek's fix**: its first glitter path read as floating rectangles, and the second — eight flashes its comment says shorten toward the viewer — is eight marks all `0.100` long, a ladder of bars under the sun in the finished picture. The prototype's other pass was the pier's six sparkles, placed by hand, whose lengths ramp only in the order they were typed. None of the guide's blocks. **And the passage has its recipe** (G6, step 9): *a light broken down a surface toward the viewer*, collected from the four accepted versions. What they come to, taken together: a film first; every piece a different length, bent, its tip drawn afresh; the rows further apart, wider and fainter as the light comes toward you, while the pieces keep their lengths — which is where DeepSeek's shortening went wrong; and the surface's own dark laid back across the lights. Its demo is DeepSeek's ladder, which the check names. |
| **`scumble` and `cover` land well outside the place they were given.** A water scumble covered part of the sky; a `cover()` repair laid a flat patch in front of the tower and was rejected. Checked against the code, and larger than claimed: a band at 60 degrees paints **3.5×** its own area, and no warning can fire for a rectangle. Today: a wedge warning, only on a `Polygon`; `cover(edge="hard")` exists and the card does not name it. | GPT, Kimi, Grok | O | **The API half, in step 4.** `scumble` takes `edge="hard"` and `clip=`, as `cover` and `block_in` do — a band crossed at an angle can be held inside itself — and the ends check runs on rectangles at last, so a band narrower than the brush laying it says so where before only a `Polygon` could. The `spill` notice that prints the **predicted ratio** (1.42x / 2.99x / 3.62x at axis / 30 / 60 degrees) is workstream D, and the card naming `cover(edge="hard")` is workstream G. **The card names it now** (step 9): the `undo` row and `PAINTER.md`'s *What you are bad at* both carry the keyword and the measured pair — `2.32x` the area it was handed at `ragged` against `1.01x` at `"hard"`, and the smaller the patch the worse that gets, because the overhang is a brush either way. The documentation carried it because F1, the default move that would make the keyword unnecessary, was declined in step 8 and waited for `spill`. **`spill` is built** (step 6): a ragged `block_in` whose passes will cover `1.6x` its place or more says so at the call, and a banded `scumble` at `2.0x`, because its own brush breaks past the band by design. The multiple is predicted off the passes the call is about to lay — `3.0x` for the band at 30 degrees that nothing warned about, against `2.95x` painted — and a band is told `edge="hard"` first. **The auto brush is not capped**, which B17 left open: measured, a cap at the band's depth still leaves `2.22x` and `2.04x`, and one at half the depth brings the bars back. `cover()` stays silent by design, and **its default moved instead (F1)**: `cover()` holds a burial to its place, `edge="hard"`, since the owner ruled on a bench of three passages that the corpus could not give — a repair-sized place buried with the default brush leaves `4.45x` the place visibly repainted ragged on a graded passage and `4.14x` on a worked one, the neighbours under it, against `0.47x` and `0.51x` held, whose cost is a crisp outline the size of the place (`CALIBRATION.md`, *A burial and the place it was handed*). The card's row says what the default does and no longer needs the keyword; and the bench's `clean` burial, which left `8%`–`15%` of the mistake showing in silence, made `clean-small` ask a region as it asks a shape. |
| **A late pass buries what stands in front of it** — weathering over a nearer cottage, a rope repainted after the wall. `LESSONS.md` lists the depth-order paragraph as failed in three runs and still open; this is the fourth and fifth. Today: prose and a checklist line. | GPT, Kimi; fogged glass, heron 1, pool (earlier) | O / M | **`report()` says when a film or a mass took three or more earlier details out of sight**: small or `subject` marks standing `0.05` off what is round them as the pass opened, left at under half that. The canvas as the pass opened is kept by `easel run`, the MCP `run` tool and the report before. The prototype fired on 54 passes, most of them back-to-front done right; this fires on two, both burials — a pier's pile reflections under a scumble, a pool's far lamp under the films lifting its water. **Not all of the row is caught.** GPT's cottage was a rehearsal, fixed before the pass was committed, and its weathering was strokes laid by hand over a mass, which the rule does not watch. The pool's chair, the one burial a painter wrote down, was laid too close to the deck in value to count as showing (`0.017`-`0.046`), and three glazes took it down a little at a time, never by half in one pass: a memory of each detail's contrast across `easel run` calls, and a lower floor, are open. `PAINTER.md` step 3's *veil of light* bullet is one line naming the check. |

### Warnings the tool gives, that were noise

**Painters accepted a standing warning by hand in their own notes rather than acting on
it — four for the bars, five for the ground.** *A warning that fires on almost every pass
is a warning nobody reads* is this
project's own rule, and the bars warning had already taught two earlier painters to skim.
**These four painted 0.5.0, where that rule is already said once and repeated only when a
long mark crosses it at 30 degrees or more** — so *said less often* was not the fix, and
the thing the tool still cannot know is whether the subject runs that way.

| What was wrong | Who | Kind | What was done |
|---|---|---|---|
| **Stack of bars, on a subject that is horizontal.** A horizon, a calm sea, a beam and a reflection: accepted in the notes as the subject running that way. Gemini's counted 392 of 583 long marks within six degrees of horizontal, over the whole painting, and the analysis under it in its own notes begins *standing warning accepted*. BigPickle's was a true positive — it was painting blind — which is the one thing keeping the rule alive. | DeepSeek, Kimi, Gemini, GLM | O | **The picture says so, and the line stops warning and starts counting.** `s.plan(bands="subject")` is the painter declaring what the warning's own text concedes it cannot know, and the line then reads *bands declared as the subject: 14 long marks run within 6 degrees of horizontal, and nothing crosses them yet* -- which is the method's next question rather than a rule, because a picture of nothing but parallel marks is a layer cake whether or not the subject runs that way. Declared up front and saved in the `.easel` file, not an `accept()` called after the fact. It is the noisiest rule the engine has -- **47 of the corpus's 325 painted passes, 14%**, after the decay that already cut the pier's seven firings to three -- and half of every line the engine prints. **And a `scumble` counts once (G3, ruled 2026-09-21).** The guide's own graded field, in its own colours a smooth field, came back *17 of 17 long marks ... a stack of bars*: every pass of a band laid by the verb that sizes its passes to overlap was counted as a bar. Over the corpus 10 of the 46 lines painters were shown were passes laid mostly with a scumble, and they go: the rule is on 38 of the 325 painted passes now, 12%, against 47. So does BigPickle's true positive, which reached its share only by counting the sky passes its own painter called fine. |
| **`ground: 0.0x% … the checklist asks for some`**, accepted by hand by five painters. Three give the same cause in nearly the same words: the `density=0.8` breather was buried by the graded fields. **The graded-field recipe and the ground line contradict each other**, and five of seven cannot all be wrong. | DeepSeek, Grok, Kimi, GPT (0.06%), Gemini (0.38%) | M | **The contradiction is resolved in the picture's favour, both halves in one commit.** `s.plan(ground="buried")` and the ground line prints its number and says *buried, as the plan says* instead of asking for some back; the graded-field recipe now names the declaration where it buries the ground, and the checklist line concedes the case. The floor is unchanged for a painting that has not said, because the corpus shows what it is for: an earlier painting chose a warm ground *to be seen through* and finished at `0.07%` without noticing. **And the finding is older than this round** -- the replay puts half of all 21 paintings under the floor, cohort or not, so what was wrong was never the cohort's painting. `CALIBRATION.md`, *The plan a painter declares*. |
| **The small-bristle and round-disc rules fired on a whole painting** — *265 marks with a bristle under `size=0.025`*, *that is one disc printed 176 times* — and were argued with in the notes rather than acted on: the bristle separation was the needle texture it wanted. A rule that reports a count over 726 marks is not a rule about a pass. | Gemini | O | **The closing audit reads a painting now, not a pass** (ruled 2026-09-22, and built). Counted first over the 21 finished paintings: the disc line was on 14 of their checklists and the comb line on 9, the two commonest lines the audit printed. **The small comb says nothing over a whole painting** -- what it asks for is a brush for the marks about to be laid -- and a pass that lays a habit's worth still says it; its large counts had been said by their passes already (38 of `opus`'s 40, 39 of `laundromat`'s 48), and Gemini's 265 were pine boughs whose streaks were the needles. **The discs count only where three or more sit within `0.06` of one another**, a signature left out, and the line says where they are: on 10 of the 21. The four it left were accents added up across passes -- one painting's *one disc printed 8 times* was a lamp, a moon, two notches, two edge highlights and a glint -- and the ones it kept are passages, Gemini's rows of glitter lozenges among them: the line it never answered, and the one that was right. |
| **There is no way to tell the tool anything.** *Useful heuristics, but they're philosophy, not errors, and it doesn't know which.* Inventoried and true: no acknowledge, suppress or declare mechanism exists anywhere in the API. The painter cannot say *my subject is horizontal* and the tool cannot ask. | DeepSeek | R | **`s.plan(...)`**: the four things the guide asks to be settled before the first mark, plus the two standing warnings a picture can declare its way out of -- `why`, `values`, `lightest`, `subject_share`, `bands`, `ground`. `Session(budget=)` was the first of these declarations and this is the rest of them, saved in the `.easel` file beside the log, settable from a `prelude.py`, `easel plan` or the MCP `plan` tool. Each one changes a line of the post-pass check rather than silencing it: the painter can be held to a plan and can be wrong about it, which a suppression cannot. Every one of this round's *accepted in the notes by hand* is a line the painter can now write down instead. |

### What the check cannot see

Three findings, of which **one is an item and two are being kept out of the engine on
purpose.** `LESSONS.md` and `report()`'s own docstring both say the check cannot see a
composition; this round restates that boundary rather than moving it — the check reads
marks and measures the canvas, and still does not judge an arrangement.

| What was wrong | Who | Kind | What was done |
|---|---|---|---|
| **`report()` said *nothing to report* over flat cut-out shapes, uniform edge handling and a banded sky.** The painter's own closing line: the check passed a picture whose named weaknesses were all still in it. Measurable things, none of them measured. | GPT; pier (earlier) | O | **The edges are measured now; the arrangement is not, on purpose.** The `edges:` line (step 7) prints the share of the picture's edges under `2.5` px wide after every pass and in `checklist()`. On GPT's own painting it reads `54%`, median `2.4` px — the third-hardest of the 21, where Grok's harbour, whose painter named the same fault, is the hardest at `62%` — against a corpus median of `37%` (`CALIBRATION.md`, *The `edges:` row, measured twice*). A banded passage laid by hand is the graded-band rule's (*comes back as bars*), and a stack of them the bars line's. Whether the shapes read as cut out is a judgement over what those numbers add up to, which the check still does not make: it reads marks and measures the canvas, and does not judge an arrangement. |

**Not items, and recorded so they are not filed again.** *No linter catches a stripe
instead of a catch-light* — a recipe followed exactly and expressively wrong (DeepSeek,
O). And the safe, frontal, centred compositions: **five of seven stopped under 45% of
budget** — 68/300, 126/300, 132/300, 170/420, 50/120 — with two of them saying in as many
words that further marks were making the picture worse, and a third leaving its 70
unspent strokes to the passage it had itself named as the weakest (GLM, DeepSeek, Grok,
Kimi, BigPickle; M). Both findings stay with the painter, and the instrument for them is
the painter's own written reason for the subject, not a rule.

### Bugs and API gaps

Eighteen items, **every one checked against `src/` on 2026-09-18** by reading the code
and, where it was cheap, painting the case on a scratch canvas. That check did what this
project's checks usually do: **four reported mechanisms did not survive**, one bug turned
out larger than reported, and one turned up a second, silent bug beside it. What is below
is the finding as it stands after that check, not as it was reported.

| What was wrong | Who | Kind | What was done |
|---|---|---|---|
| **`scumble(clip=)` raises `TypeError`.** Confirmed: `clip` is a named parameter of `stroke()` alone; `dab`, `smudge` and `glaze` reach it through `**kw`, and `block_in`, `sweep`, `cover` and `scumble` cannot. The error is the generic *`clip=` is not a brush field* and names neither `stroke(clip=)` nor `edge="hard"`, because the table it reads from has rows for `solid`, `glaze`, `edge`, `density`, `overhang` and `pressure` and none for `clip`. | GPT | O | **`clip=` on every verb that lays paint**, through one hold, the clip riding in the log exactly as `stroke`'s always has. `edge="hard"` *is* a clip pointed at the place the call fills, so a mass given both is held by both and the coverage masks multiply; one hold logs as one outline, as every clipped stroke has since `edge="hard"` was built, and two log as a list, which an older build refuses rather than reading as one outline and painting something else. `scumble(edge="hard")` is the mass form, and the remedy B17 names. `REFERENCE.md` grows *Which verb takes which hold*, held by a test that **makes each call** rather than reads the signature — three of these verbs take their holds through `**kw`, and a signature does not show that. |
| **Holes inside a `solid=True` mass**, reported as shaped paths wandering apart. **The holes are real and the mechanism is not the one reported.** A `flat` left 0.0000% bare at every size, direction and density tried. A `bristle` — `block_in`'s own default — leaves them: 22 bare blobs at `size=0.06, direction=37, density=1.0`, the largest 187 px. It is the comb covering about three-quarters of its width, and `solid=` cannot close it because it sets `load` and `load_falloff` and nothing else. GPT's own three holes were laid with a `flat`, at the joins between hard-edged walls, so they are most likely the hard-edge bites below. | GPT, Grok | O | **Said at the call, with the prices, and no default moved.** `solid-comb` names the share that stays bare — `0.16%` in 47 blobs on a mid ground, `3.16%` in 373 on a dark one, because a hole is a contrast and not a gap — and what closes it: `density=1.2` at about a fifth more passes, a solid tip at any density, crossed passes at twice the price. It fires on **10 of the corpus's 198 block-ins** and on **none** of the guide's 70 runnable blocks, which is rule 2. The table is `CALIBRATION.md`'s *The holes a solid comb leaves*. |
| **`timelapse_gif()` fails on a rehearsal copy.** Confirmed: the copy is created with `timelapse = False`, so it has no frames and raises a clean `ValueError` — whose first remedy is wrong here, because it says to create the session with `timelapse=True` and the painting already had it. | DeepSeek | O | It says what happened: *this is a rehearsal copy, and a rehearsal records no frames — the painting it was copied from keeps its own*, and then where to ask for them. The general message names `timelapse_gif(from_log=True)` too, which builds a film from any log. |
| **Time-lapse frames are 360 px beside a 1440 px painting.** Confirmed, and the size is unreachable: `max_side=360` is a default nothing passes, from `Session` or the CLI, and the frames are stored in the `.easel` file at that size. `scale=` only shrinks. | GPT | O | Both answers. `Session(timelapse=<px>)` — also `easel new --frame-px` and the MCP `new` — says the size up front; `timelapse_gif(from_log=True, scale=)` **rebuilds the film by replaying the painting**, at any size, storing nothing, which is the one that can help a painting already made and works on one that recorded no frames at all. Built on `replay(frames=<px>)`, so there is one rebuild and not a second beside it. |
| **`cost_line` failed on a `scumble`.** Confirmed, **and there is a worse one beside it.** The planner knows three kinds — mass, sweep, stroke — so `scumble`, `cover`, `glaze` and `smudge` cannot be planned, priced, previewed or rehearsed at all. And a scumble-shaped plan carrying `shape=` **prices silently as a block-in** (6 strokes where the scumble costs 8), raising only when `paint()` reaches the extra keys. The MCP server refuses unknown keys before pricing; the library does not. | GLM | O | Both halves. `PLAN_ACCEPTS`, read off the signatures, refuses a key the call would not take **before the entry is priced** — the check the server had and the library did not, now imported by the server rather than kept twice. And two new plan kinds through the one dispatch: `{"band": ..., "color_a": ..., "color_b": ...}` is a passage and `{"cover": ..., "color": ...}` a burial, priced by walking the same geometry the painting walks (`_scumble_paths`, beside `_block_in_paths`), so the quote is what `paint` charges. The two colours are what tell a passage from a mass filling the same place. |
| **`replay(upto=)`, `undo(n)` and `log(last=)`: records or strokes?** Partly. All three count log records, free ones included. `replay`'s docstring says so and `REFERENCE.md` says so for `undo`; `undo`'s own docstring says *scrape back `n` strokes*, and `log(last=)` says nothing. | GLM | R | One word and a clause: `undo` says **log records**, `log(last=)` says so too, and a test holds the three docstrings together — a dry, a pencil line and an erase are records, are free against the budget, and are what `undo(1)` takes back after a `dry()`. |
| **The Windows cp1252 console chokes on the docs' unicode.** **Not reproduced for the tool**: `easel guide` writes UTF-8 bytes past the codec on purpose and exits 0 under cp1252, and no string in `src/easel/` contains a non-ASCII character, so no notice or `report()` line can do it. What does die is a painter's own `print(easel.docs.read(...))` — four characters in the five shipped files are outside cp1252, 35 occurrences, 31 of them in `CALIBRATION.md`. Reading a document from Python is the most natural thing a painter does with `easel.docs`. | GLM | O | The four characters are `->`, `-`, `~` and `<=` in all five shipped documents, and `tests/test_guide.py` holds every one of them to cp1252 — so a painter's own `print(easel.docs.read(...))`, which is the most natural thing to do with `easel.docs`, prints on a Windows console. |
| **`edge="hard"` leaves pass-end bites at the outline.** Confirmed, and isolated: `hard` cuts the bites three- to four-fold against `ragged` and still leaves **1.9%** (`flat`) to **4.9%** (`round_hard`) of the 3 px strip inside a slanted outline unpainted. The cause is pressure, not load — `hard` gets one brush of overhang and the default `pressure="taper"` reaches zero one brush out, so every pass arrives at the outline at part pressure. At two brushes of overhang it is 0.016% and 0.000%. | GLM | O | **The default moved**, in workstream F with the goldens looked at rather than assumed: `edge="hard"` now carries two brushes of overhang on `block_in` and on `cover`. Re-measured on a range of slopes rather than one — a `round_hard` leaves `0.85%`–`3.26%` of the strip at one brush and `0.055%`–`0.33%` at two, a `flat` `0.00%`–`0.66%` against `0.000%` — and it is the round tip's fault more than the chisel's, which is the opposite way round from the staircase. The pass count does not move, so `cost()` quotes what it always did, and nothing can cross the mask, so neither does the outline. `scumble` keeps its own `0.35`: it is `pressure="even"` already and leaves `0.000%` of that strip bare at every overhang tried. |
| **Subject share counts free signature marks** — 172 of 411 where it should be 172 of 408. Confirmed and reproduced on a five-mark canvas: the subject line builds its total without the exemption `History.stroke_count` already applies. | GPT | M | `History.paid_marks` is that exemption in one place: `stroke_count` is its length, and `report()`'s subject line divides by it. The two numbers a line apart are now one number. |
| **`import easel_paint` fails.** Partly: `llms.txt` and the package docstring put `from easel import` straight after the install line, and `README.md` does not — its install section has no import at all and its nearest one is 76 lines above. **And PyPI carries an unrelated distribution named `easel`**, which is what a painter who guesses the install name from the import name gets. | DeepSeek; the install session (earlier) | O | **It just works.** `src/easel_paint` re-exports `easel` and ships in the wheel, so both import names are real and are the *same objects*; a test holds the two together and holds the build table to both packages. `README.md` and `llms.txt` put the import beside the install line — it was 76 lines away — and say the distribution is `easel-paint`, never `easel`, which is somebody else's. |
| **A ground name used as a colour, and three namespaces.** Partly: the palette lists every valid pigment and slot on failure but does not notice that the name it was handed is a valid *ground*, and the canvas is blind the other way round. Nothing exposes a ground as a colour, so sampling bare canvas is today's only route to the value a painter can already see. | Gemini | O | Each handler checks the other namespace and says which one the name belongs to, and the ground is a colour: `s.ground`, so `p.at_value(s.ground, 0.62)` and `p.mix(s.ground, 'ultramarine', 0.3)` both mean what they look like. Sampling an unpainted corner — which measures the tooth's shading as well as the ground — was the only route. |
| **`region("bottom")` is the bottom third, not a foreground band.** **It is smaller than reported: a ninth.** `top`, `bottom`, `left`, `right` and `center` are cells of a 3×3, so `bottom` is x 1/3–2/3, y 2/3–1. The full-width places are `lower-band` and `lower-half`. `REFERENCE.md` lists the names and none of their extents. | GLM | O | Every extent, in `REFERENCE.md`'s *Places* table and in `region()`'s own docstring, with the full-width names beside them (`lower-band`, `lower-half`, `middle-band`); `test_reference.py` holds every row of the table against `_NAMED`. |
| **A 0–255 integer list clamps to white in silence**, which `PAINTING.md` documents as a trap. Not re-checked; documented behaviour. **A documented trap the engine can detect is a bug.** | the docs | R | It **raises**, and names both fixes — the same numbers divided by 255, and the hex they spell. `PAINTING.md`'s paragraph says so instead of documenting the trap. |
| **`solid=True` is refused on `stroke` and `scumble`**, with a good teaching error that names the pair to type by hand. It is `load=1.0, load_falloff=0.0` everywhere, and it is the clause painters type most often. | Gemini; laundromat (earlier) | O | `solid=` on `stroke`, `sweep` and `scumble` as well as `block_in`, and an explicit `load=` beside it still wins, as it always did. `cover()` lays that pair already, so it is the one call whose error still explains it rather than taking it. |
| **30–45 s for 500–800 marks.** Confirmed as a fixed cost per stroke, and nothing is quadratic. Every stroke snapshots rgb, wetness, thickness and sketch for `undo` — about 33 MB and 6.4 ms at 1440×960, roughly 800 MB resident at 24 snapshots — and with `timelapse=True`, the default, every stroke also builds its 360 px frame from a full-canvas composite at 25.6 ms. About 32 ms of bookkeeping per mark before a dab lands, ~26 s over 800 marks. | Gemini | M | Two cuts, both measured. A frame is **built only if the thinning would keep it** (`History.wants_frame`), which is where the 42–60 ms a mark went: past `MAX_FRAMES` the sequence is halved anyway, so most of that work was done and thrown away. And a stroke snapshots **the box it can reach** rather than the whole canvas: at 1024×768, `15.7 MB` and `5.2 ms` become `3.5 MB` and `1.85 ms`, and 377 MB resident becomes 107. Wetness stays whole, because `tick_wetness` dries the entire canvas per stroke and no box holds that; the stack unwinds newest first; and a mark that ever landed outside its box drops the stack rather than restoring it wrongly, leaving `undo` to rebuild from the log, which is exact. |
| **No easy calibration of size, load and pressure before committing** to a passage. A feature, not a bug: one labelled sheet of the same mark at several settings, in place, on a copy — a request for more of the one thing every painter in this round defended. | GPT | R | `s.rehearse(plan, vary={"size": [...]})`: one labelled panel per setting, in place, in one image, free like any rehearsal — and each panel is its own copy seeded as the next marks of the painting, so the setting chosen lands as it was shown. At most twelve panels, because two arguments vary as their combinations. Every panel's notices come back, which is half of what the sheet is being asked. The MCP `rehearse` takes it too. |
| **A wide angled `scumble` lands far outside its band.** Confirmed, **and larger than claimed.** The auto brush is `3 × step`, and `step` is the band's *bounding box* projected on the pass normal, so an oblique angle on a wide, low band inflates it: a band 0.20 tall at `n=8` paints **1.43×** its own area along its axis, 2.84× at 30 degrees and **3.53× at 60** — a brush 1.65× the band's own height. **Nothing fires**: the narrow-brush check looks the other way, and the ends check returns immediately for a `Region`, so the guide's own `span(...)` bands can never trip it. | GPT, Kimi, Grok | O | All three. `_check_scumble_ends` runs on rectangles now — a band is not a wedge, its passes vary only at the corners, so what a rectangle is asked is whether the **whole band** is narrower than the brush laying it, measured on its longest pass. `edge="hard"` / `clip=` on `scumble` is the remedy (B1). And the `spill` notice (step 6) says the predicted multiple at the call — `3.0x` for the band at 30 degrees that nothing warned about, against `2.95x` painted — and names `edge="hard"` first; the auto brush is not capped, for the reason in the finding-8 row above. |
| **Glazes crossed wet, then a block-in, printed concentric rings.** **The rings are real; both accounts of their cause are wrong, and the painter's own folder shows it.** The seven frames are committed at [`paintings/GLM/terminal_window/rings/`](paintings/GLM/terminal_window/rings/README.md): the wall is clean after the six glazes and before the block-in; a film at `opacity=0.15` leaves about 0.13 wetness rather than 0.90, and had twenty-odd strokes at ~6% each to fade; and the rings first appear in a **rehearsal**, landing identically when the pass was paid for — so *what you rehearse is what lands* held and the painter did not see them. What they are: wobbly closed loops concentric with a blob-shaped patch that overshoots the glass — an inward scumble's own contour rings, the failure `RECIPES.md` already names. The calls are gone; the first takes were overwritten and their marks undone. | GLM | O | `dry_first=` on `block_in`, off by default: wet-into-wet is most of what makes a passage soft, and a mass laid over a dried one is a decision. The probe's reconstruction (`CALIBRATION.md`, *GLM's rings*) decided the notices, and none was built: `ring-steps` and `ring-rim` fire on nothing in the corpus, whose inward `scumble`s step `0.014`–`0.021` a ring, and `wet-under` is not in 0.6.0, for the reason in the finding-5 row above. |

### The documentation

Six items, **most of them about what a painter meets before the first stroke** — and they
arrive from painters who were told nothing about what to read, which is what makes them
evidence rather than preference.

| Gap | Who | Kind | What was done |
|---|---|---|---|
| **Too long before the first stroke.** ~2,600 lines, ~2,500 lines, *2000+ lines of docstrings*, 10,000+ words across five files — three painters counted it independently and a fourth asked for the cheat-sheet without counting. Every one of them wants a quick start. | DeepSeek, GLM, BigPickle, Kimi | M | **The entry path is the card, six failures painted, and the exercises** (G2, step 9). The card said *read `PAINTING.md` once* before starting, which is ~2,500 more words before the first mark; it now says run `easel demo mistakes` — one sheet, six failures a painter meets, each one a line the tool says — and paint the nine exercises. **`PAINTING.md` is the reasons, delivered rather than read**: every notice carries the passage its reason lives in, and `easel explain <code>` prints that passage at the call. The file table and the README say so too. The quick start they asked for is `easel guide`, the card on its own, which now has a **word ceiling of its own** (G10): 1,400 for the card, 6,700 for the file, both held by `tests/test_guide.py` where the file's ceiling used to sit 3,000 words above the text. |
| **Too prescriptive.** Stroke allocations, bare-ground percentages and marks-per-object read as universal rather than as adjustable defaults; *supervised by a very earnest painting instructor*. | GPT, Kimi | O | **The numbers that were the guide's are the painter's plan now** (C, step 5; the voice pass, G8, step 9). The three values, the place meant to be lightest, the subject's share of the budget and whether this picture's ground is meant to be buried are `s.plan(...)`, and the check answers to what was declared: the `subject:` line counts against your share, the ground line prints its number without asking, and bars declared as the subject become a count of what crosses them. What is left in the guide as a number says which kind it is — **measured**, with its `CALIBRATION.md` heading, or a **habit**, as *most painters so far*. *Three marks for a small thing* says it is a habit; the budget's split says it is yours. |
| **The voice hides the call.** *The runtime warnings are clearer in the moment than the prose*, and *a few rules fight each other in practice until you've failed each one once*. | Grok | O | **The call first, and the rule where the tool says it** (G8, step 9, with steps 3 to 8 under it). Every rule that became a check left the prose in the commit that landed the check, and what is left names the code: the smudge paragraph names `smudge-across`, `smudge-long` and `smudge-wide`; the edges step names the `edges:` line; boxes name the `boxes:` line; under-varied objects name *one disc printed* and *a loop's signature*. The rules that fought each other were the ground line against the graded field (settled in step 5, in the engine and the recipe together) and the staircase's remedies against the small-comb floor (settled in step 9). And the reason behind a line is one command away, at the moment it fires: `easel explain <code>`. |
| **Wants small runnable visual comparisons**: the recommended call, what it looks like, the common failure, the smallest fix. With the sharper half of it — *the documentation sometimes compensates for difficult tool behaviour with additional rules*, and some of that belongs in defaults and API consistency instead. | GPT | R | **`easel demo <recipe>`** (G3, step 9): nineteen of the twenty-one recipes paint beside their commonest failure and, where it is not the recipe itself, the smallest fix, with what the tool said about each panel quoted. The demo blocks sit under each *Goes wrong as*, and `scripts/check_guide_blocks.py` — in CI now — holds each to what it names. Two stay in words on purpose: *a form that turns*, whose pass on its own draws the stack-of-bars line and whose failure is a stroke too slight to show at a demo's scale, and *a scene with straight edges*, whose block is a drawing. |
| **The two things that cost real work were not in it** — the ring interaction and the hard-edge bites — and *it is written for a painter who already knows painting; the first steps are assumed*. | GLM, DeepSeek | O | **Both are in it, and one of them is a default now.** The hard-edge bites were B8: measured (`0.80%`-`3.26%` of the strip inside a sloping outline left bare at one brush), fixed by moving the default to two brushes of overhang in 0.6.0, and written up in `CALIBRATION.md`, *The bites just inside a hard edge*. The rings were B18, and the painter's own frames say what they were: an inward `scumble`'s own contour rings, laid over paint still wet, which moved them by up to `0.13` (`CALIBRATION.md`, *GLM's rings*). The call says so before they land — `inward-flat` — and *A passage light in the middle* names visible concentric rings among its failures. The first steps being assumed is G2's answer above. |
| **Nothing says that vision is required.** *I can't see it (the model doesn't support image input), so I'm trusting the tool* — a painter that followed the method exactly, could not open a single look, and had to hand the question of whether the picture works back to the owner. Every instrument this tool has for judging a picture is an image. `README.md`, `llms.txt` and the package docstring all stay silent about it. | BigPickle | O | **Said, in all three places** (step 9, G9). Each of them already *described* it — *built for an agent that can see what it just did*, *for agents that can look at their own work* — which is a design note and not a requirement, and is why this stayed invisible: the sentence looked present. All three now state it as a requirement and give the reason, which is that every pass of the method ends by looking, so a painter without image input can drive the whole API without ever learning whether a mark landed. |

### Four reported mechanisms that did not survive checking

Recorded before anything is built on them, because a retraction is as much a finding as
an item, and because **every one of these was reported as *observed*** — which is the
shape `LESSONS.md` predicts and the reason the measuring step comes before the building
one.

- **The holes are not passes wandering apart.** They are the comb covering
  three-quarters of its width, or the hard-edge bites at a join. A `flat` leaves none.
- **cp1252 does not break the tool.** It breaks a painter printing a shipped document
  from Python, which is a real bug and a different one.
- **`region("bottom")` is a ninth, not a third.**
- **GLM's rings are not the crossing glazes.** **And the first check of that was wrong
  too**, until the painter's own frames were opened — three accounts written, at least
  two of them wrong, which is why the frames are committed rather than the conclusion.

### Found while filing the round, not by a painter

**The reproducibility count had gone stale the moment the seven paintings landed**, in
the same two sentences the hands round fixed a version of. `README.md` and
`PAINTINGS.md` both said *seven of the fourteen* carry **Reproducible: not claimed**;
`paintings/` now holds twenty-one and the number that do not claim it is still seven, so
the fraction was quietly reporting half the corpus as unproven when it is a third.
Corrected in both places.

**The sentence beside it is the one to watch**: *the ones that claim the stronger one
were checked by sha256*. All seven of the cohort's paintings claim a script rebuild, and
none has been re-run here — only GPT's carries a sha256, and it is the painter's own.
Both pages now say so. **Re-running every painting from its committed pass scripts is the
first thing the round's measuring step does**, so this answered itself rather than
needing an item — and the answer is
[#70](https://github.com/Gemberkoekje/EaselAPI/issues/70), outside this round: `car_wash`
and `pears` claim a rebuild and come back five marks over, two committed passes do not
run from a clean session, and 0.6.0 changes what some committed scripts paint — two
moved defaults and the smudge fix.

### The two Claude verdicts, filed as corroboration

Two verdicts that had never been committed are committed with this round —
[`paintings/Claude/fogged_glass/verdict.md`](paintings/Claude/fogged_glass/verdict.md)
and
[`paintings/Claude/greenhouse_winter/verdict.md`](paintings/Claude/greenhouse_winter/verdict.md),
now linked from [`PAINTINGS.md`](PAINTINGS.md). **Both paintings predate 0.4.0 and their
engine items were closed there, so nothing in them is filed as an item.** They are here
for the sentence both of them lead with, which is the argument this whole round rests on:

> *Reading it did not stop me making the mistakes it describes … what stopped me was the
> post-pass check and the rehearsal image.* — the fogged glass, having painted a box in
> the background, filled an outline, got the tool's own shape four times and drawn a
> daisy, each after reading the paragraph naming it.

> *The same five warnings appear three or four times, and none of them stopped me making
> the mistakes. I painted bars too heavy and laid shadows as a fan of same-width rays
> after reading both warnings. The rehearsal stopped me, not the paragraph.* — the winter
> greenhouse.

They are the sixth and seventh painters to say it, and this round's whole shape is that
sentence taken at its word.

### What worked, recorded because a finding is still true afterwards

Every one of the seven defended these unprompted, and **nothing in this round touches
them**:

- **Rehearsal seeded as the next real strokes.** What you preview is what lands, pixel
  for pixel — and this round has the first case where that cut the other way, because
  GLM's rings were in the rehearsal and went in anyway.
- **`at_value` and errors that teach.** *Titanium white reflects at 0.958 and no mixture
  can be asked for higher* ended a pass for one painter; another calls them the best
  error messages in the Python ecosystem and quotes three back.
- **`cost_line` naming the lever**, not just the price.
- **One plan object for `cost` / `preview` / `rehearse` / `paint`** — *what you check is
  literally what lands*, which one verdict calls the design decision most tools miss.
- **Determinism**, and a reload that re-exports the same bytes: GPT reports a
  SHA-256-identical PNG from the saved session.
- **The post-pass check teaching by naming the mark**, where it fires on something real.

### The paintings, and what the painters own

- **Five of seven stopped under 45% of budget.** That is either the right stop or an
  unfinished picture, and the two that explain it say both in the same breath.
- **The compositions are safe** — near-frontal, centred, the obvious arrangement — and
  three of them say so in their own words: *dead-center and symmetric*, *the composition
  is the obvious one*, *poster-simple*. One states the consequence plainly: the fixes are
  all upstream of the brush, and a viewpoint change would move the picture further than
  any amount of texture work.
- **Flat cut-out shapes**, named by both painters who laid every form as a clipped
  polygon. It is also where two of this round's candidate remedies point, which is the
  risk this round carries into whatever run follows it.

### What the round left open

Recorded here because the working notes they were written in leave the repository once
0.6.0 is tagged. Everything else the round declined or put off is written where it was
decided: the checks it did not build in `CALIBRATION.md`, the default moves it declined
under 0.6.0's *Defaults moved* in `CHANGELOG.md`, `wet-under` in the finding-5 row above,
and `PAINTINGS.md`'s rebuild claims in
[#70](https://github.com/Gemberkoekje/EaselAPI/issues/70).

- **A notice's code, linked to the `DIAGNOSIS.md` row for the same symptom.** Not this
  round (ruled 2026-09-21): when it was ruled, sixteen of the engine's twenty-five codes
  already resolved to the passage a row points at, so `easel explain` and
  `easel diagnose` printed the same text and only the name was missing. Revisit once a
  run shows whether a painter calls either. **Revisited in 0.7.0**: the lighthouse
  handover called neither, and the link is not built.
- **Whether the card's six habits and `easel demo mistakes`' six failures should be one
  list.** They are two for now: the card's *six things you will get wrong* are habits,
  the sheet's are failures a painter meets, and the card points at the sheet. Making
  them one rewrites the card's table, the page whose word ceiling is tightest — 1,369
  words of 1,400.
- **What the next run should look for first.** The way in — the card, the sheet, the
  exercises — is a hypothesis, and its known risk is the pier's finding: a card so
  sufficient that the recipes go unread. The sheet names six recipes, which is the cover
  for it, and only a run says whether a painter opened any of them. The second is the
  cut-out risk just above, which the `edges:` line now measures.

---

## The hands session: the second painting from the package alone, and the first blind one

**Every item in this section is done, in 0.5.0** — two engine items and four
documentation items, and one more found while filing them. That release had been cut for
the pier round below and never tagged, so the two package-only rounds ship as one.

Told to `pip install easel-paint`, to make sure of **0.4.0** and not a local editable
install, and to treat that package as the only thing available, in an empty directory.
It painted from `python -m easel guide`, `--full`, `--painting`, `--reference` and
`--recipes`, all nine exercises, and nothing else: no `CALIBRATION.md`, no `LESSONS.md`,
no `DIAGNOSIS.md`, no earlier painting, and **this repository was not opened until after
the picture was exported and reviewed**. Subject chosen before any of it was read: a
pair of hands sorting dried beans, `paintings/Claude/hands_beans/`, **329 of 420 strokes**.

**It painted 0.4.0, which is the last release there has been**, and that cuts both ways.
Five of the frictions it hit are things the pier round had already fixed in an
unreleased 0.5.0 — an independent painter confirming that round aimed right, so they are
below as confirmations rather than as items. What is filed is what that round does not
touch. **And it is the blind run the pier session was not** — that one had spent the
morning inside this repository and its documentation findings were discounted for it.
This one had not, so its reading of the guide is worth full weight, and where the two
agree — the stack-of-bars warning going unread, the front page being long, the reason
for the subject going missing — that is the same fault found twice, once by a painter
who knew the numbers and once by a painter who did not.

### The folder question, answered a second time

The pier session closed this by painting in an empty directory and listing a laundromat
first and a winter greenhouse third anyway. **This one replicates it with the overlap
counted.** Asked for ten subjects before a word of the guide was read, in an empty
folder, it listed a laundromat at 2 a.m. **first**, the underside of a pier **second**,
a greenhouse in winter **third**, and an empty drained pool **eighth** — four of its ten
already hanging in `paintings/`, two of them in the same positions the pier's list put
them. Told the first three were painted, it dropped them and re-ranked the rest without
being asked how. **The subjects are not coming from the filenames, and the prior is
narrow enough that four in ten collide with a ten-painting corpus.** That is the finding
to watch next, and it is not a comfortable one: a page that says *decide before you
read* is defending against the weaker of the two effects.

**One difference from every other session here, and it should be discounted for: the
final pick was the owner's, not the painter's.** The ten were the painter's and were
written before anything was read; the hands were its named runner-up rather than its
pick. So the subject satisfies *chosen before reading* and not *chosen by the painter*.
The reason for the subject was the painter's own and written before reading, so the
finding below that turns on it stands on its own.

### The engine

| What was wrong | What was done |
|---|---|
| **A failed rehearsal says it saved, and did not.** A script that raises under `--rehearse` prints `easel: script raised, session saved with 180 strokes` — and the count is the *painting's*, because a scratch copy continues the real numbers, so it reads exactly like a commit. Nothing is committed: `cli.py` returns out of the rehearsing branch above the `if result.save: session.save(...)`. The message is built in `run_scripts`, which does not know whether it is rehearsing. The painter stopped and verified the stroke count by hand before trusting it, twice. (Observed.) | It says which it was: *nothing committed, the copy had laid N of this pass's marks*, with `N` the copy's own log rather than the painting's count carried through it. **Read off the session rather than passed in at the call site**, which is the one place the request left open and the one that matters: the flag is at two call sites, the MCP server's `run(rehearse=True)` is the second, and it had the same bug. A caller that hands over a copy and then says `rehearsing=False` would print the line this exists to stop. `exit()` on a copy says it too — it returns through its own branch, which carried the same sentence. |
| **`sample()` over a place that straddles two masses returns a confident mean of neither, and nothing says so.** Sampling the table for a found edge with `span("C3","D4")` — a span that crosses the hand — returned **0.342** where the local table is **0.258**, and the edge painted with it landed as a pale halo above the hand instead of sharpening it. The documentation does say *to measure a mass, hand it the mass*; the painter had read it, and the failure is silent, arrives as a number, and goes straight into paint. **It is the ninth session's item, at the same call, by a painter who had the sentence that round wrote** — `sample()` over a `cell()` cost that one a second probe and the conclusion that the engine was laying everything `0.14` light, and the answer then was a clause in three files. Offered with a threshold: the straddling span's own pixels have a standard deviation of **0.111**, a clear patch of the same table **0.018**, and *the two populations do not overlap*. (Measured, on `hands.easel`.) | **The warning is built and the threshold claim did not survive**, which is the interesting half. The span reproduces — `0.110` against the painter's `0.111`, and `0.011` for a clear cell of the same table — but *clear air between 0.03 and 0.06* is an artefact of four places on one canvas. Measured over **226 rectangles**, every cell and every 2×2 span of this painting and the pool rebuilt from their own passes, the two populations overlap heavily; worse, **a mass handed in whole sits at 0.093 and 0.100**, so the rule as asked for would have fired loudest on the call the remedy tells painters to make. So it is asked **of rectangles only** — the case the docstring already calls a trap — and a shape is never asked, because handing one over *is* the remedy and a mass with a turn in it is spread by design. At `sd ≥ 0.06` with a tenth of the place as the smaller part, it catches **all 35** rectangles whose mean misses their own dominant mass by more than `0.03`, fires on **23%** of the rest, and on none of the seven masses. It names what is there rather than reporting a spread: *84% of it reads about 0.276 and 16% about 0.529, so the 0.341 this returns is a measurement of neither*, split at Otsu's threshold over the place's own pixels. `compare()` is untouched, as the request asked. |

### The documentation

| Gap | What was done |
|---|---|
| **`look(marks=False)` has existed since 0.4.0 and is in none of the five documents.** `look()` takes ten parameters; `REFERENCE.md`'s signature line names eight and stops, so **`marks` and `impasto` are both missing from the page whose claim is *every fact on one page***. `PAINTING.md`'s *Looking* block shows `look(sketch=False)` and has no row for the landmarks either. This painter placed six landmarks and judged the picture through **fifty-two looks** with their labels drawn on it; one of them, `pinch`, sat on the focal point for the whole session. It found `unguide()` for the scaffolding, because that one *is* named. **This is the pier session's `unguide()` item exactly — the verb exists, the sentence naming it does not** — reproduced by a painter who had not read the first. (Observed.) | The sentence, in all three places — and then the harder answer, because this is the second of its kind and the first fix did not generalise. **`tests/test_reference.py` now reads each signature off the code**, in two checks, because the page names a parameter two ways and each misses what the other catches: every optional parameter of every call the page documents has to appear in the page's *code* (not its prose — `path`, `name` and `note` are ordinary English), and a call the page writes out in full has to be complete **on its own line**. The second is what catches `impasto`, which is named on the page, on `export`'s line, four lines from the call that was missing it — a block-wide scope reads that as documented, and it is not. What the check found on arrival: `stroke(clip=)`, `sweep(closed=)`, `cover(dry_first=)`, `sketch(areas=)`, `mix(ratio=)`, `mix_many(weights=)` and `complement_grey(ratio=)` were named nowhere on the page, and eight more calls were written out with parameters left off the end. All closed. |
| **The band count is about the scene, and the picture's worst repetition was inside one mass.** *Count the horizontal bands in the drawing; more than three, and find a viewpoint or a thing that crosses them* is asked of the arrangement, and this arrangement passed it easily: a table, a bowl, two limbs crossing on two different diagonals, no horizon anywhere. What sank the picture was four near-parallel fingers **inside a single mass** — a comb the size of a hand, which the question does not reach because the mass is one mass. (Observed.) | The clause, where the band count is asked and in step 1: **count them inside the biggest mass too, and count any row of like things** — four fingers, five pickets, a row of windows. The guide already knew this at object scale (*you will under-vary your objects*, *nine of these on one ledge want a stroke recipe*) and did not connect it to the band count, which is the instrument for it. |
| **The drawing step asks whether the arrangement is right and never asks whether the view is.** *Keep drawing until it is proportional and the way you want it* is about proportion and placement, and every tool around it — the grid, the cells, `preview`, three candidate silhouettes in one look — helps you move a mass rather than turn it. This painter redrew the whole arrangement three times, all three free, and all three were fixes to framing, limb angle and the bowl's size. **Not one of them asked whether a cupped hand seen from the front is four fingers laid out sideways or a cluster foreshortened toward the viewer.** It is the second, and the picture is the first, and that is its central failure. (Observed.) | **In step 1, which was the first of the two framings the request offered.** *What is this thing's foreshortening? Draw the view, not the object*, on the card beside the band count and again in step 1 with this painting's own loss as the example. The checklist was the other candidate and it is the wrong one: the checklist runs when the drawing is no longer free, and the whole argument for the line is that it is asked while moving a mass costs nothing. *A mass built of planes* is named beside it as what comes after — the inside of a mass once the view is settled. |
| **Nothing says when to stop repainting a passage and go back to the drawing.** The guide is firm that the drawing is free and that a mistake is cheap for as long as possible, and it has a rule for the wrong repair (*you will reach for `undo`*) and one for the wrong tool. It has none for *this is the fourth time I have repainted this passage*. About **eighty of this painting's strokes** went on four successive treatments of one failing passage — vary the brushes, break the lights, lay core darks, abandon two fingers — each a brush-level answer to a drawing-level fault, and each making the next repaint dearer because more was standing on it. (Observed; `pass06`, `pass13`, `pass24`, `pass27`.) | The stopping rule, stated as a number because a preference will not survive the moment it is needed: **if a passage has failed twice, the fault is upstream of the brush. Go back to the drawing — it is still free, and it is the only thing that is.** A sixth row in *the things you will get wrong*, which is the table a painter reads under pressure, and the paragraph beside *you will reach for `undo`*. The engine half was left alone, as the request's own weaker half: `report(since=)` can see repeated repaint of a region, and a region is not a passage. |

**Two of this round's items are the same shape, and it is the shape to watch.** The
`sample()` item and the `look(marks=)` item were each answered in an earlier round by
writing a sentence — *to measure a mass, hand it the mass* for the ninth session, and the
sentence naming `unguide()` for the pier's — and each was hit again, at the same call, by
a painter who had read what was written. **Both are closed this time with something that
fires**: a warning at the call, and a test over the page. *A rule nothing enforces is a
preference* is this page's own line, and this is the round where it came for the
sentences.

### Found while filing the round, not by the painter

**`README.md` and `PAINTINGS.md` claim every painting re-runs byte for byte, and half of
them say in their own tables that they do not.** *The scripts re-run from a fresh session
at the same seed and reproduce the export byte for byte* sits under **The worked
examples**, which is the section that sends a first-time painter to `paintings/`;
`PAINTINGS.md` makes the same claim one bullet from the end of the rules. Filed as *two
of the thirteen*, and counted while fixing it: **seven of the fourteen** carry
**Reproducible: not claimed** — drawing passes rewritten and re-run, `look` scripts run
as passes between the painting ones, preludes edited between passes, each pass edited
after its rehearsal.

The claim that is true is a different one and both pages now make it as itself: **the log
replays byte for byte**, because a stroke's randomness is drawn from `(seed, stroke
index)`, and golden-image tests hold that. Whether the committed *scripts* rebuild the
canvas is per painting, and each painting's table already says which — so the fix was to
stop the two summary pages overriding them.

**And the preamble of this page was counting one session short.** It said twelve sessions
and thirteen paintings against a `paintings/` that holds fourteen: the winter greenhouse,
painted before the fogged glass and filed after it, has a row in the table above and was
never in the sentence. Thirteen sessions, fourteen paintings.

### What the pier round had already fixed, reported by a painter who did not have it

Confirmation rather than items, because a fix aimed at the right thing is worth knowing
about from someone who hit the fault it was aimed at. All four were in an unreleased
0.5.0 while this painter was working from the 0.4.0 wheel.

- **The stack-of-bars warning fired on pass after pass on a subject that ran that way**,
  and the painter's own account says it stopped reading it. Same as the pier. The decay
  rule is aimed at exactly this.
- **`PAINTER.md` was too long to hold and the painter went back to it constantly**, which
  is what the 6,672 → 6,000 compression was for; and **the cross-references were skimmed
  past**, including two it needed, which is what 25 → 16 was for.
- **The scaffolding had to be taken off by hand before the picture could be judged.**
  `erase()` taking both drawings is half of this; the other half is the `marks=False`
  item above, which that round did not touch.
- **The one that matters: it lost half of why it chose the subject, and noticed when it
  was asked for a review afterwards.** The reason was written down first — old hands are
  warm at the knuckles and cool across the planes between, and that contrast is what
  keeps the subject out of sentimentality. The contrast is in the picture. The
  specificity is not, and nothing during the painting asked. **That is the pier's finding
  reproduced on a different subject by a painter who had never read it**, and it is the
  strongest evidence on this page that the checklist line earns its place.

### Two items that died on measurement before they were filed

The painter arrived at this repository with both and neither survived being measured,
which is recorded because a retraction is as much a finding as an item.

- **"*A form that turns* does not work at feature scale."** It does. Laid at four widths
  on a 1024×768 canvas — `0.30`, `0.16`, `0.08`, `0.05` — it keeps its transition at
  **25–40% of the form's own width** throughout and loses `0.07` of value range across
  the run. The recipe was never applied: the fingers were laid as strokes from the first
  pass, and *A form that turns* was never opened, in a `RECIPES.md` whose contents page
  the painter had read. **The mapping is the step that failed** — the painter did not
  think of a finger as a form that turns, it thought of it as a finger — which is the
  noun-free design working at the page level and failing at the point of use. 0.5.0's
  card names the situation rather than the file; this is a data point on the item the
  register flags as *most likely to still be true*, and it says the remaining risk is in
  the painter's own naming rather than in the pointer.
- **"`edge="clean"` draws a contour that reads as an outline."** It does not. Measured on
  the painting's own bowl, rim minus interior is **−0.010** for `clean`, `+0.007` for
  `ragged` and `+0.013` for `hard` — the contour is if anything the *darkest* of the
  three. What the painter had seen was a cool mass at too high a value on a warm ground,
  and it corrected the bowl by three value revisions rather than by touching `edge=`.

### What worked, recorded because a finding is still true afterwards

**Rehearsal is the part of this that works, and this session leaned on it harder than any
so far: 114 rehearsal views, none charged, against 28 committed passes.** Caught free: a
scumble that buried the fingers whole, navy-blue core shadows, four white discs clustered
at the focal point, a pink stripe where warmth was wanted, a fan-shaped scallop for the
back of a hand, and a bowl three times too light.

**`at_value` is the best primitive in the box** — nine planned values, nine exact
returns. **`glaze(to_value=)` failing is better than it succeeding**: *the paint under
this film reads 0.389, and at opacity=1.0 it reaches 0.258* is a measurement the painter
did not have, delivered at the moment it was needed, and it ended the pass. **The
post-pass check teaches by naming the mark** — *that is one disc printed seven times*, *a
comb that small is four streaks with gaps*; five of 331 marks carry a flagged fault at
the end and the early passes hold four of them.

### The painting, and what the painter owns

- **The hands do not read as hands.** The gesture is legible and the anatomy is not.
- **The view was never chosen.** Four near-parallel fingers laid out sideways, redrawn
  three times without the question being asked once.
- **Eighty strokes went on symptoms** of that, at the brush, while the fault sat in
  graphite where moving it is free.
- **It stopped at 329 of 420 with the weakest passage still the weakest** — the thing the
  checklist warns about by name — and its notes say *deliberate* and *finished* are not
  the same word, which is the honest version of the pier's own admission.

---

## The pier session: the first painting from the package alone

**Every item in this section is done, in 0.5.0** — five engine items, five documentation
items, and the one that is neither, which is the one that mattered. The install session
above, continued: told to install `easel-paint` from PyPI
and paint from whatever the package carried. `python -m easel guide`, `--full`,
`--reference` and `easel brushes`, and nothing else — the repository was not opened at
any point. Subject chosen before anything was installed: the underside of a pier at low
tide, `paintings/Claude/pier_underside/`, **257 of 300 strokes**, signed and exported. The
picture is a dark structure over water at dusk.

**It is not a blind run, and its documentation findings should be discounted for it.**
This session had spent the morning inside `SUGGESTIONS.md` and `CHANGELOG.md` doing
packaging work, so it arrived already knowing the `0.10` threshold, back-to-front, the
run-out window and the four-pixel floor — scattered numbers without the method that
holds them together. It had also *patched the engine that same day*. Its engine findings
stand, because they are about marks it laid and warnings it was shown. Its reading of the
guide is worth less, because a painter who already knows the numbers is exactly the
painter who can skip four files and still finish. **The discount is why one of its five
documentation items was answered by compressing rather than by cutting**, and the row
says so.

### The folder question is closed

Every session before this one chose its subject inside a working directory, and it had
never been possible to rule out that the directory was choosing. **This one ran in an
empty folder: no repository, no listing, nothing to read.** The subjects came anyway, and
from where they have always come — a laundromat at 2 a.m. first, a greenhouse in winter
third, a collapsing wave sixth, **and the wave was also sixth on Fable's list**. They
come from the prior, and the prior is shared across the family. The hands session above
replicates this with the overlap counted.

One thing more, and it is the most encouraging sentence in the session: asked for ten and
then for the most interesting, the painter named the laundromat its own favourite and
ruled it out unprompted — *it has been painted a thousand times*. That is the reasoning
that produced the car wash, applied by the painter to itself without being asked for it.

### The item that is neither an engine item nor a documentation one

The first on this page aimed at the picture rather than at the marks.

| What is missing | What was done |
|---|---|
| **Nothing in the method ever asks whether the reason you chose the subject is still in the picture.** The closing checklist asks whether *the thing you measured most carefully* is still attached, which is a question about a mark. It does not ask whether *the thing you wanted* survived. This session chose the pier for one reason and said so before installing anything: under a pier the light arrives from *below*, bounced up off the water, so every form is lit backwards — a thing paint can do and a camera mostly cannot. It then painted a competent dark structure over water with the light coming from the ordinary direction, passed every line of the checklist, and noticed the loss only when it was asked for an opinion afterwards. Nothing failed. The value structure is sound, the masses are shapes, the edges vary, the ground shows at `0.58%`. (Observed, and the painter's own account.) | **The two lines, as asked, and a third sentence that was not.** *Write down why this subject and not another* is on the card beside *write the three values down as numbers*, and again in step 1 with the pier's own loss as the worked example. *Read back why you chose this subject. Is that reason still in the picture?* is the last line of the checklist, and the preamble that said *every line but the last two* now says the last three, so it is read at the same speed as the two it joins. The sentence that was not asked for is the reason the line can exist at all, and it is in `report()`'s docstring rather than on the page: **the check cannot see a composition, and every rule in it is about a mark.** That is the engine row below, closed as a boundary. |

### The engine

| What was wrong | What was done |
|---|---|
| **The banding warning fired on nearly every pass until the painter stopped reading it.** *N of N long marks run within 6 degrees of horizontal — a stack of bars unless the subject runs that way.* The subject was the underside of a pier: joists, a waterline, a reflection. It **does** run that way. It fired on the masses, the joists, the water, the second water pass and the focal pass; by the fourth the painter had stopped reading the line, which means it was also unread on the pass where it was right. **This is the ninth session's twenty-eight correctly-ignored bristle-floor warnings, reproduced inside the engine rather than in a file.** (Observed; the count is from the pass output.) | It decays, by the remedy the item named. Said once, and again only when the picture has picked up a long mark **30 degrees or more** off the bars it was said about — which is the picture being asked the question the warning's own text concedes it cannot answer. Measured by replaying this painting's fifteen passes: **7 firings become 3**, and the three are the first stack, the pilings crossing it, and the stack rebuilt afterwards. The threshold is the middle of a plateau rather than a knee — every value from 20 to 60 degrees prints those same three, 15 prints four, 0 prints seven — and the pier's own angles are bimodal underneath it, 175 of 251 long marks within 10 degrees of the bars and 43 within 20 degrees of square to them. `--check` is exempt: what makes a warning skimmable is being printed at you after every pass, and an audit was asked for. |
| **The post-pass check cannot see a dead composition, and says `nothing to report` to one.** The largest mistake of the session was the first arrangement: it made the distant opening the hero and left the subject — the lit underside — an empty band across the top of the frame. It was caught by looking at a drawing, which is free, and would have cost the whole painting had it not been. Every pass the check approved was locally clean. (Observed.) | **Nothing, deliberately, and it is written down as a boundary** — which is what the item asked for and what it predicted. `report()`'s docstring now says it in the same place it lists the seven rules: the check cannot see a composition and says *nothing to report* to a dead one, because a mark is what the log holds; composition is carried by the drawing, which is free, and judged by looking at it. **The eighth item to close by measuring and finding nothing to fix**, and the only one so far that closes by declining to build. The other half of the item — that this is the argument for putting *why did you choose it* where a painter answers it — is the row above. |
| **`s.erase()` does not clear `guide()` marks, and nothing obvious does.** Redrawing an arrangement left the old scaffolding fan on the view beside the new one — two convergence points in one look, which is exactly the thing the drawing exists to judge. `s.marks` is a plain dict and `s.marks.clear()` works; it was found by poking at `dir()`. (Observed.) | All three of the item's options, because they turned out to be one fix and a naming problem. `erase()` takes both drawings, and takes them the same way: the whole of each with no region, and inside a region it cuts an overlay path exactly where it cuts a graphite line, through the same function — so a path wholly inside goes, one wholly outside stays, and one that crosses comes back as the pieces. `unguide()` already existed and had since 0.4.0; this painter never found it and reached for `s.marks.clear()`, which clears landmarks and not guides, so what was missing was not the verb but the sentence naming it. It is now in `guide()`'s own docstring, in step 1 beside the call, and in the units table. |
| **`look()` numbers its output per session, so several sessions writing into one directory overwrite each other.** Four of the nine exercises were run from one script and produced one file — `out/look_001.png`, four times. The images were gone before they could be looked at, in the one part of the method that is *only* looking. (Observed.) | The engine, not the clause — and the fix already existed one method away. Rehearsals have been numbered from **what is on disk** since 0.4.0, because a rehearsal runs on a copy and has nowhere to keep a counter; every view is numbered that way now. A directory is the one piece of state two sessions can both see. The per-session counter is gone, including out of `save()`/`load()`, where it was carried across specifically so that a reopened painting would not renumber from 1 — a workaround that is now the default. The clause was written too: the exercises say to give each `look()` a `path=`, because nine unnamed looks are still nine files to tell apart. |
| **`easel.guide` and `s.guide()` are two unrelated things under one name** — the module that reads the documents, and the method that lays scaffolding on the view. Both are reached from the same session, and the guide teaches the second without mentioning the first. (Observed.) | The module is **`easel.docs`**. `easel.guide` forwards the whole of it and is not going away — a name that has shipped does not stop working — but everything that teaches it says `docs`, including the package docstring, the README and the `dir(easel)` listing, which now carries both. Worth keeping how this one arrived: **the painter that found it patched it into the package itself, that same morning** — `guide` was bound into `__init__.py` by this session, so half the collision is its own doing. That is the taint in this round stated plainly, and it is also the argument for the blind run: the next one of these will be found the same way, by someone who did not put it there. |

### Found while acting on the round, not by the painter

**The stack-of-bars warning had been naming the wrong direction, and the fix for it was
a prerequisite for the one above.** Marks lying along the horizontal come back from the
log as a mixture of `179` and `1` degrees. The clustering reads those correctly as two
degrees apart — and then took a plain **median** of them, which is `90`. So the
commonest stack of bars there is was reported as *vertical*, and the painter was pointed
at right angles to its own fault. The pier was told *vertical* about its joists on the
pass that added the cross-bracing. The same number steers the graded-passage rule's
normal, where it measured the spread of a horizontal band *along* the band instead of
across it. Both now take a circular mean of the doubled angles, which has no seam.

It was found by trying to measure the decay rule against this painting and getting an
answer that could not be true. **That is the third time a rule's own measurement has
turned up a defect in the rule** — the argument for measuring every number before
anything is built on it, which this page has made every round since the fourth.

**A second, smaller one, about the workshop rather than the engine:** a non-editable
`easel-paint` install in `site-packages` shadows the checkout, so `pytest` in this
repository silently tests the published wheel and not the working tree. Every test run
in the first half of this round passed against 0.4.0 code. CI is unaffected — it does
`pip install -e ".[dev]"` — and the local fix is the same command. It is the install
session's stale-editable-install finding wearing the other hat, and it is recorded here
because it cost an hour twice now.

### The documentation

**Every item here has one fix, and this page has already written it down:** *a rule
nothing enforces is a preference.* The guide was restructured to stop the front page
growing. It was failing in the direction it was fixed toward.

| Gap | What was done |
|---|---|
| **The front page is so self-contained that the other four files went unread.** A whole painting was finished without opening `PAINTING.md`, `RECIPES.md` or `CALIBRATION.md` once. That is a real compliment to the card, and it is the finding: the painter hit problems those files had already solved and re-derived both badly through rehearsals. A foreground darkened with wide glazes landed as a bar with a hard lid, while *A graded field that is most of the picture* sat three keystrokes away; caustics laid as short round-tip marks came out as blobs stuck to the ceiling. (Observed.) | The second of the two candidates, the first having been dropped: the card now names the *situation* rather than the file, in the line where it sends a painter away. **Before you lay a passage you have not laid before — a form that turns, a graded field, a hollow thing, lit air — open `RECIPES.md` and find it**, with this painting's two losses as the reason and *the moment is before the pass, not after the rehearsal shows it failing*. **This is the item on the page most likely to still be true**, and it is the one to watch in the next blind round: the split is right, sufficiency is what makes it work, and this is what sufficiency costs. |
| **The pointers have become texture.** Nearly every paragraph on the card ends in a cross-reference, and this painter skimmed past all of them — including the two it needed. At that density they stop reading as navigation. (Observed.) | Counted and cut: **25 cross-references to 16**, and the seven workflow steps from **12 to 4**. Every one that survives is at the moment of a situation — the projection, the planes, the graded field, the lost edge — rather than at the end of a paragraph about something else. The five in the file table at the top are not navigation and were left; they are the map. |
| **The nine exercises are called *a gate*, and nothing gates them.** *They are a gate. A painter who skips them meets the lessons inside the picture instead.* This painter ran four of the nine, from one script, and went straight to the painting — then met exercise 8's lesson inside the picture, on a piling built as a box. (Observed.) | **The word is gone, and nothing was built to earn it back.** The item asked for a mechanism; the honest answer was that the page's own rule cuts the other way — a rule nothing enforces is a preference, and the fix for a preference dressed as a rule is to stop dressing it. What is left is the cost, stated plainly: a painter who skips them meets the same lessons inside the picture, with the rest of the painting already standing on the mass that has to be repainted. Every mechanism considered — a flag on the session, a count in `report()`, a line in the budget output — could only record what it was told, which is a preference with a `True` in it. |
| **The body restates the card at three times the length.** Steps 1–7 appear twice, once in about nine hundred words and once in about three thousand, and the short one is better. The expansion earns its place only where it adds a mechanism the card has no room for — `compare()` on a value plan, `at_value` reachable from either side, the three rules about `smudge`. (Observed.) | **Compressed rather than cut: 2,412 words to 1,540**, three times the card down to under twice it, and `PAINTER.md` from 6,672 words to about 6,000. Cut in full: the second telling of back-to-front, of what a place is, of hard edges pulling the eye, of the greyscale argument, and every code block that showed what the card had already shown. Kept, because the item named them: `compare()` on a value plan, `at_value` reaching a value from either side, the three rules about `smudge`. The section now opens by saying what it is for — *the card above is the whole of it; what follows is only the mechanism behind each step*. **Compressed and not deleted because of the discount at the top of this section**: a painter who arrived already knowing the numbers is the one most likely to find the expansion redundant, and the three-times figure is the part of the finding that is checkable. |
| **`look(path=)` is not on the card**, which is where the exercises are, which is where several sessions in one directory first collide. (Observed; the engine item above is the same fact from the other side.) | The clause is there, and the collision it was meant to prevent is gone from the engine anyway — see the row above. Both, because they answer different halves: numbering from the directory stops a file being lost, and `path=` is what makes nine looks tellable apart afterwards. |

### What worked, recorded because a finding is still true afterwards

**`--rehearse` caught four faults that would each have cost real strokes, and none of
them cost one.** A single `direction=` combing an entire mass into windswept hatching; a
ragged `block_in` at `size=0.20` breaking half a brush past its outline and eating the
slot of daylight whole; the caustic blobs; the glaze bar. The arrangement that made the
wrong thing the hero was caught in graphite, which is free. **The loop is the part of
this project that most clearly works.**

**The post-pass check teaches better than the prose does, because it names the mark.**
*A comb that small is four streaks with gaps, not a brush.* *Pressure changes a chisel's
paint, not its width, so these are rectangles with a lighter end.* *That is one disc
printed eight times.* The disc counter in particular does what no document can: the
checklist asks *is any small mark a disc*, and a painter cannot answer that about its own
silhouettes. The engine can, and did, twice.

**`at_value` refusing an unreachable value is worth more than a clamp would be.** *Value
0.125 is out of reach: mix a darker ingredient and ask again, or plan a value this box
can lay.* That is the floor of the box taught at the moment it bites, to a painter who
had read the number that morning and planned below it anyway.

### The painting, and what the painter owns

Faults the method names and the painter made regardless, which is the shape this page has
recorded every round so far:

- **The pilings are slabs.** They are cylinders, painted as rectangles with a stripe down
  one side, with no turn from lit to shadow anywhere on them. *A form that turns* is a
  recipe in a file that was never opened.
- **The range is crushed.** The box runs `0.14` to `0.96`; almost the whole picture sits
  between `0.15` and `0.35`, and the painter had been calling that atmosphere.
- **It stopped at 257 of 300 with the weakest passage still the weakest** — the thing the
  checklist warns about by name, two lines from its end.

---

## The tenth session: the fogged glass

**Every item in this section is done, in 0.4.0**, together with the winter greenhouse's
below: the two rounds raised the same two items from opposite directions — what
`direction=` names, and a check that fires on a row of separate things — and acting on
half of either would have been acting on half a fix.

It read `PAINTER.md` and its nine exercises, then `PAINTING.md`, then `RECIPES.md` where
a passage called for one — `CALIBRATION.md` and `REFERENCE.md` were grepped, not read.
Subject chosen and written down before the repository was opened: a greenhouse wall in
late winter seen from outside, the glass fogged from the inside,
`paintings/Claude/fogged_glass/`, **311 of 320 strokes**, subject share **29%** against a
planned 37%.

**It sits next to a near neighbour, and the neighbour is not the same subject.** The
painter chose *the outside of a fogged greenhouse wall* before reading anything, found
`paintings/Claude/greenhouse_winter/` in `git status`, recognised how close it was, and declined
to open it. **So this is not a held subject and not a control**, and the two are filed as
two paintings rather than as one subject with two parts. One thing in them *is* a
convergence, because it is checkable against their scripts rather than against an
impression: both painters refused a frontal elevation on the closing checklist's
layer-cake warning and both answered it with a metric perspective projection written
before any line was drawn — `P(xm, hm, dm)`, the same three arguments in the same order,
in each one's `prelude.py`, neither having read the other. Two painters reaching the same
helper off the same sentence is worth more than any similarity in the pictures.

**Three claims in this section were re-measured by the painter before it was written**,
on its own finished session file: the check bug reproduces from the CLI, the depth-order
violation is `0.089` of value on a named bar, and the buried ground is `0.07%` of the
canvas. The rest say *observed*. Every number in both rounds was re-measured again before
anything was built on it, by `scripts/probe_tenth_session.py`.

### What it found in the engine, and what was done

| What was wrong | What was done |
|---|---|
| **`direction=` is the one argument it never understood — whether passes *run* along the angle or *step* along it — and it resolved the question by rehearsing instead of by knowing.** It is the most central argument in the API and it has been ambiguous for every painting in the collection. The painter's own account: `block_in(GLASS, direction=-23)` visibly laid passes running up-right along the eave, which says *run*; `cost_line` on the same call answered *24 passes stepping across 0.80 of the canvas*, and `0.80` is not the extent perpendicular to `-23` of that mass's box by its own arithmetic. So the two instruments appear to describe different geometries, and a painter reading both cannot tell which. Four of this painting's worst rehearsals came out of it, including a glass wedge combed vertically by `("axis", 70)`. (Observed, across the session; the disagreement between the picture and `cost_line` is the reproducible half.) | The sentence was already in the units table, put there by the winter greenhouse's documentation round; the engine half turned out to be nothing. `cost_line` and the picture do not describe different geometries — passes run along the angle, the stack steps across it, and `cost_line` agrees to the hundredth. What nobody had written down is that both are in **normalised** units, so on a canvas that is not square neither is the angle on screen. **The sixth item to close by measuring and finding nothing to fix.** What was built is the thing that removes the arithmetic: `direction=` now takes a pair of points, and the worked example — one mass, three angles, the pass direction and the step direction both named — is beside the `direction=(28, 118)` line in `PAINTING.md`. |
| **The post-pass check's *detail before the masses are down* rule fires on every rehearsal for the whole life of a shell-driven painting, and it taught this painter to ignore warnings.** It claims to police *the painting's first 60* and it fired at 135, 162, 190, 243, 260 and 273 strokes spent. **Mechanism, measured and isolated:** a session reloaded by `easel run` carries `spent` but an **empty `history.records`** on the `--rehearse` path — `spent: 311, records held: 0` — so the rule's `earlier` term computes as `0` and the guard `earlier + len(marks) <= 60` is always true. On the committed path the same session holds 403 records and the rule correctly stays silent. Reproduced on the finished 311-stroke session file: rehearsing a nine-dab pass fires it, running the identical pass reports *nothing to look at*. Since the guide's standing instruction is *rehearse every pass with `--rehearse`, look, and only then run it without*, the false positive is guaranteed to reach every painter on every pass, and the correct silence only ever appears after the decision it was meant to inform. | `earlier` is taken from the painting behind the copy, not from the copy's own log. The audit found the hole a second time: **the subject's share** reads across passes too, and a rehearsed pass reported its own marks as the whole painting — a share measured where the guide says to measure it came back as 100% of nine marks. Both now read the marks charged before the pass, rehearsal copies included. The item's *confirm rather than assume* was the right instruction and it found the second one. |
| **`jitter=0.5` is accepted in silence, and it destroys a pass.** The default is `0.02`. The painter read *the default wanders about 1.2 px on a `size=0.1` flat, halving both halves the wander* as naming an operation rather than a number, passed `0.5`, and every member of the frame — eave, sill, bars, laps — came back as a chain of separate beads instead of a line. Twenty-five times the default, no warning, from a call that otherwise looked exactly like the recipe. The check warns about a pressure list on a chisel tip, which is a subtler fault than this one. (Observed; the rehearsal is in the session's notes.) | A wall at five times the default, with the number the painter needed in the line. `jitter` is the wander of each dab in tip diameters, so what it buys is width: measured on a `liner`, a stroke lands **1.2 brushes** across at the default, **1.8** at `0.1` and **3.7** at `0.5`. It fires on the override rather than on a brush's own field, the way the chisel-pixel floor only looks when `size` was asked for. |
| **`cover()` lays a rectangle larger than the area it is given, and it is offered as the answer to *you will reach for `undo`*.** Used to bury a mis-made leaf inside a worked pane, `cover(Region(0.905, 0.380, 0.985, 0.478))` put a flat pale panel across a visibly larger patch of glass, because its recipe runs the ends of each stroke *outside* the area by design. On a flat passage that is the right recipe; on a textured one the repair is louder than the mistake, and the painter buried `cover`'s own output by hand with marks shaped like the pane. (Observed.) | Both halves. `cover(..., edge="clean")` insets the fill by half the brush and draws the boundary, and `edge="hard"` masks the paint to the area outright. Measured on the painter's own patch, a `flat` at `size=0.06` on 1024x768: the plain recipe paints **3.07x** the area it was handed, clean **0.93x**, hard **1.01x**. There is deliberately no warning on the plain form — the overrun is the recipe working, the docstring's own `cover(cell("D5"))` paints about three times the cell, and a rule that fires on the canonical call is one painters learn to ignore. |
| **`inset()` erodes a boundary that lies on the canvas frame, and left a pale strip down the right edge of the finished picture.** `GLASS.inset(0.024)` pulled the glass mass `0.024` in from **every** boundary including the one at `x = 1.0`, so the right-hand frame kept its ground and the glass stopped short of the edge; the defect survived to the final inspection pass and cost a repair. `edge="clean"` is documented as dropping the inset where an outline runs off the canvas, on the stated principle that *a mass that meets the frame should run off it*. Plain `inset()` does not, and the asymmetry is invisible from the call. (Observed; the repair is `p9_repair.py`.) | Done, with `edge="clean"`'s wording, and `inset(..., frame=False)` for true erosion. Per coordinate rather than per point, so a point on the bottom frame keeps its `y` and takes the inset `x`. `edge="clean"` now calls the same method instead of carrying its own copy of the rule, which is where the asymmetry came from. |
| **There is no instrument for *is the ground still showing through*, and the painting fails the checklist line in silence.** The plan's best idea was a warm ground — `umber_wash` at `0.425` — chosen so that anything left showing through the cool condensation film would read as warmth coming through, which is the subject. Laying the glass interior at `density=1.0, load=1.0` bought a solid support for the fine marks and spent the ground to get it, and **the painter did not notice until the closing measurement**. Measured against a bare canvas of the same size, texture, ground and seed: **0.07%** of the finished canvas is within `10/255` of bare ground, `0.32%` within `16/255`. The owner's reading: *that is the pool's ground mistake in reverse, and both were caught by measuring the wrong thing late.* | `report()` prints it after every pass, off `Canvas.ground_showing()` — a diff against a bare canvas at the session's own ground, texture and seed, which is exact rather than reconstructed. Per channel rather than by value, so a cool film at the ground's own lightness counts as covering it, and graphite does not count as paint. The floor is `0.5%` and is labelled a **judgement**, placed an order of magnitude from each of the two anchors there are: a mottled `density=1.0` mass leaves `4.4%`, and this painting finished at `0.07%`. |
| **A round tip prints its own outline, and both its defaults are the bad one.** `tip_wobble` defaults to `0`, which is the disc the documentation warns about, so *several small marks with `round_hard` or `liner`* is the failure by default and the fix is opt-in. Worse in combination: `block_in` of a small `hull` with a `round_hard` at `size=0.013` — a leaf pressed on the glass, a feature about `0.05` across — printed the shape's own scalloped boundary and came back, in the painter's words, a cauliflower. It was relaid as two tapering strokes that meet plus a midrib. (Observed.) | The check, not the default: moving `tip_wobble` would repaint every script that leaves it off, and the changelog's own rule is that a default only moves where it must. Three or more small round-tip marks at `tip_wobble=0`, each short enough to be the tip's silhouette rather than a line — a `liner` drawing fine lines is the guide's own advice and does not trip it. The `block_in` half is a warning at the call, on a ragged edge, on a shape under a tenth of the canvas across — over that width a round tip is the soft silhouette the guide recommends — and at the same quarter of the shorter extent `edge="clean"` already uses: measured on that leaf, a round tip at the painter's own size lands **1.61x** the area of the shape against a chisel's **1.34x**. |
| **`scumble` over two adjacent bands is read as one stack and warned about as one graded passage.** Two overlapping ramps laid over the ground, `n=7` then `n=8`, drew *15 marks at stepping colours run parallel 0.027 apart* — the two calls summed. It may well be the right reading, since the two ramps *are* one passage and the painter did mean them to join; but the suggested remedy, `size=0.271`, is three times either band's own step and would have been wrong for both. (Observed; offered as the half most likely to be wrong, in the eighth session's sense.) | It should not span *these* calls, and the fix is the one the winter greenhouse's version of this item asked for. A passage steps one way; the rule now requires the colours across a run to turn at most once, and two ramps laid end to end turn twice. So the two bands are no longer summed and the remedy is never derived off a merged step. Three further narrowings came with it — see the winter greenhouse's row below, which is the same item measured from the other side. |

### What it asked of the documentation, and what was done

| What was wrong | What was done |
|---|---|
| **The `jitter` guidance names an operation where it should print a number.** *The default wanders about `1.2` px on a `size=0.1` `flat`, halving both halves the wander, and zero is ruled* — the painter read "halving" as a thing to say rather than a thing to compute, and passed `0.5`. The actual defaults, `jitter 0.02` and `size_jitter 0.06`, are in `REFERENCE.md` inside a run-on line listing *every other `Brush` field, with its default*, which is where nobody looks for the one they need. | Print the middle setting in *The one ruled line* as what it is: `jitter=0.01, size_jitter=0.03`. The recipe is already the right place; it is one substitution. *Done in the documentation round: the defaults, the halved setting and the `0.5` failure are all in the recipe.* The engine half came in this round: past five times the default the call says so. |
| **`direction=` needs the worked example the rest of the geometry gets.** *The angle of the mark* explains why direction matters and *Where a stack of passes starts* says which end a stack begins at, and neither says what the angle names. The engine half is in the table above; the documentation half is a diagram-in-words — one mass, three angles, the pass direction and the step direction both labelled. | Both. *The angle of the mark* now takes one band at `0`, `45` and `90` and names what each does — the passes run along the angle, the stack steps across it, and `cost_line` counts the same geometry — and the line form is beside the `direction=(28, 118)` example, with the reason for reaching for it: the angle came off the picture, and the picture is not the space the number is in. |
| **The fifth painter in a row asks for the prose to move into `report()`.** Its own account: reading the guide did not stop it making the mistakes the guide names — it painted a box in the background, filled an outline, took the tool's own shape four separate times, and drew a daisy, each after reading the paragraph naming it. What *did* stop it was the post-pass check and the rehearsal image. Its summary: about 210 KB of guidance across five files produced a working set of maybe fifteen rules plus the checks. **`PAINTING.md` already contains the finding** — *a line printed after the pass that did it is worth more than the paragraph* — and the request is that the documents take their own advice much further. The owner's reading: *the check stops mistakes; the paragraph names them afterwards.* | Three rules, and the paragraphs that held them are now one line pointing at the check: the discs on the closing checklist, the ground line beside it, and the round-tip row in *The shape each tool leaves behind*. Nothing was cut to pay for them — `PAINTER.md` is 6,672 words against its 10,000 budget — so the round's answer to *what is the prose for* is the other half of the question rather than the deletion: it is for the rules no check can hold, which is still most of them. The request stays open in the sense that every future round asks it again; what closes here is this round's three. |
| **The closing checklist asks a question the painter cannot answer.** *Is there anywhere the ground still shows through? There should be.* There is no way to tell short of building a bare canvas and diffing it, which is what this painter did — after the painting was finished, and having already lost the thing the ground was chosen for. | The checklist line says how to look and gives the number the painting lost: `report()` prints the share, and `0.07%` is what a canvas looks like when the warm ground it was planned around has gone. |
| **`cover()` is documented by its virtues.** *The whole recipe, already set* and *buries a mistake with every clause of the recipe in place*, in the row of *the five things you will get wrong* that a painter reaches for under pressure. The clause that decides whether it is usable — that its ends run outside the area — is stated two files away, under `block_in`'s `overhang` discussion, and not where `cover` is recommended. | One clause beside the recommendation: *on a worked passage it will overrun; bury it by hand instead.* *Done in the documentation round, in `PAINTER.md` where `cover` is recommended.* The engine half came in this round: `cover(..., edge="clean")` and `edge="hard"` do not overrun at all. |
| **A veil of light is a mass at a depth — read, then violated.** The painting held back-to-front throughout except in its late atmospheric passes, which is the confirmation below. The sentence exists and is correct; it sits in *Paint from back to front*, several thousand words from the glaze documentation and the glaze recipes, where a painter deciding to lay a film is actually looking. | Repeat it at `glaze`, which is the one place this round would argue for duplication over the file's one-rule-one-place discipline — or link it from there, which the file's own conventions already allow. *Done in the documentation round: one sentence at the glaze table in `PAINTING.md`, linking the rule at step 3.* |

### Confirmations, not new items

- **A depth-order violation, in a session that otherwise held back-to-front throughout,
  and it is a late atmospheric pass over near things — the second round running.** The
  ninth session's single violation was a late graded passage laid over the far trees,
  the pole and the bird's head. This one's is a late *glaze*: the warmth inside the
  greenhouse, and the cool film knocking it back, were both laid across a glazing bar
  that is **outside** the glass. Measured on the same bar, same width, clear of the
  glaze and inside it: `0.290` against `0.379`, a lift of **`0.089`** — within a
  hundredth of the `0.10` that makes a new mass — and the hue carried from `#4b494f` to
  `#63605e`. **Both violations are glazes or graded films laid late**, which is exactly
  the case *a veil of light is a mass at a depth* was written for, and both painters had
  read it. Two points is not a pattern, but it is the same shape twice, and it suggests
  the failure is not *forgetting depth order* but *not counting a film as a mass*.
- **`compare({place: value})` was run once, at stroke 115 of 311, and never on the empty
  canvas.** `PAINTER.md` step 4 asks for it twice — once before the first stroke, once
  after the block-in. This is better than the eighth and ninth sessions, which never ran
  it at all, and it is still the third round in a row where the instrument that exists
  for painting without a reference is used less than the method asks. It did its job
  when it ran: five of six planned places came back inside `0.05`.
- **The nine exercises paid for themselves inside the first pass**, twice: exercise 3's
  starved brush on rough canvas became the condensation beading and the frost, and
  exercise 8's box-against-shape was cited when the painter caught itself laying the
  yard as `Region` boxes. And **every failure in the session was caught in a rehearsal**
  — forty-four of them against 311 paid strokes, none charged. Both are *What none of
  them would change* holding for a tenth painter.

---

## The winter greenhouse: painted before the tenth, filed after it

**The documentation items in this section were done in the session itself, as the round
that rewrote the five files; the engine items are done in 0.4.0.** It was
painted *before* the fogged glass and filed *after* it, which is why the register's
count of rounds and the gallery's count of pictures briefly disagreed. Every file in the
corpus was read in full before the first stroke — `PAINTER.md` and its nine exercises,
then `PAINTING.md`, `RECIPES.md`, `REFERENCE.md`, `LESSONS.md`, the calibration file in
part, and three earlier paintings' notes and preludes. Subject chosen before the
repository was opened: a greenhouse interior in late winter, looking down the aisle at
a low sun behind the fogged end wall, `paintings/Claude/greenhouse_winter/`, **297 of 300
strokes**, seventeen rehearsals, subject share **40% at the moment the subject was
finished** against a planned 30%, and two signature marks. Two directives were added to
the run and belong with it: *keep using the pencil until everything is proportional*,
and *before redoing after a rehearsal, ask whether it is a large mistake or a happy
accident, and keep the second kind*. The first produced four drawings before paint and
the composition; the second saved rehearsal cycles and once kept a smudge strip that
should have gone.

**Three claims here were measured before they were written**, on the session's own
run output and on a fresh canvas: the cost of the first pot recipe, the check firing on
rehearsed passes, and the unit `direction=` is measured in. The rest are observed and
say so; where a mechanism is a guess, it is labelled as one.

### What it found in the engine, and what was done

| What was wrong | What was done |
|---|---|
| **The chisel staircase and the half-brush spill are one defect, and it was the most common way a mass went wrong in this painting: four times.** The end wall's gable came back as chisel ends stepping down both slopes; the bench tops, laid as strokes fanning to the vanishing point, poked chisel corners up into the wall behind them; the dark under each bench spilled half a brush above the bench's far edge onto the end wall as a sawtooth; and `edge="clean"` warned on every pot body because a pot is too narrow for the quarter-brush rule. Three workarounds were used and none is in the recipes: passes along the slope, a clean contour where the brush allowed it, and lowering the under-bench polygon by `0.12` m in world space so the overhang stayed hidden under the bench — a hack. (Observed; the mechanism is the one `CALIBRATION.md` measures under *The chisel staircase* and *`block_in`*.) | `block_in(shape, ..., edge="hard")`: every dab multiplied by the shape's own coverage, no inset, no contour pass, no extra stroke. Ragged stays the default, because a mass behind others wants the brush to break past its boundary. Settled on the two rows the item named, measured on this painting's lit face. The staircase probe's share of strong edges within ten degrees of horizontal, on a mass with no horizontal feature: `flat` at `size=0.020` **13%** ragged against **4%** hard, `knife` **16%** against **4%** — and the comb and the round tip, at **4%** and **3%** ragged, were never the ones doing it. The overhang table's *furthest paint past each edge*: **9.3px** ragged, **2.6px** clean, **under one pixel on every side** hard, that pixel being the boundary's own feathering. The three workarounds are retired, the hack included. `stroke(..., clip=place)` is the same thing by hand, and the clip rides in the log so a clipped painting replays. |
| **Nothing prices a compound recipe short of a full rehearsal, and the estimate was wrong by more than a factor of two.** The pot recipe was budgeted at about 100 strokes for thirteen pots and rehearsed at **220 against 142 left**; rebuilt from strokes it came to 108. Each rehearsal took about three minutes because the copy renders every dab. `cost()` prices one `block_in` or `sweep`; a helper that calls a dozen verbs has no price until it has been painted on a copy. (Measured, from the run output.) | `s.scratch(count_only=True)`, and `easel run --count` from the shell. The count is exact, as the item reasoned it would be: pass geometry is settled before anything is stamped, and the assertion it asked for is in `tests/test_paintings.py`, run against this painting's own scripts pass by pass — same stroke count, same paths, same dabs. Timed on the pot recipe: **1.6s rendered against 0.06s counted**, a factor of about thirty, and most of that saving turned out to be the undo snapshot rather than the dabs — three canvas-sized arrays per stroke, which a copy that lays no paint has nothing to undo to. The one thing it will not answer is a film given `to_value=`, whose search measures paint a counted run has not laid; that is skipped and said out loud, once, because an out-of-reach value raises when it is painted. |
| **The graded-passage rule fires on rows of separate things and on a `smudge`.** Three times in this painting: on the light pass — *5 marks at stepping colours run parallel 0.028 apart, and the narrowest brush laying them is 0.02* — where the `0.02` was the smudge, which lays no colour, counted with two block-in passes and two glazes; on the staging pass — *19 marks … 0.019 apart, narrowest 0.012* — the plinth's passes, its top-course stroke, the far-floor scumble and the bench boards summed across five calls; and on the pots — *30 marks at stepping colours run parallel 0.003 apart, narrowest brush 0.004, 1.2 of that step* — the vertical body strokes of ten separate pots at three terracotta values, which are ten objects and not a passage. Read against `_graded_band`: it takes the largest set of long marks within six degrees of one angle across the whole pass, requires three colours and a median step between a quarter and two brushes, and never asks whether the marks form one contiguous band or whether their colours step one way. (Observed, with the check's code read.) | All three, and a fourth. Smudge records are dropped — a brush that lays no colour of its own cannot be the narrowest brush in a passage it contributed nothing to. The offsets must form one run with no gap wider than four brushes **between neighbours**, which is what the median step could not see. The colours must step one way, turning at most once — a band that brightens and falls back is a passage, and ten pots at three terracotta values turn nine times. The fourth: a passage is now **five** marks rather than three, three being also the number of strokes a small container's body takes, which is what made ten pots into thirty marks. The ninth session's dawn band still trips it. |
| **`direction=` is measured in normalised units, and on a canvas that is not square the passes do not run at the angle you gave.** On a 1000×500 canvas, `block_in(band, direction=-23)` laid its passes at **−12° on screen** (18 passes; the reversed ones at 168°), which is exactly the screen angle of a line at −23° in the `0..1` coordinates; on 1024×768 the same call runs at −18°, and `45` runs at 37°. `cost_line`'s *stepping across N* is consistent with that same space: on a band `0.8 × 0.2`, `direction=0` stepped across `0.20`, `90` across `0.80`, `−23` across `0.50`, which is the box's extent perpendicular to −23° in normalised units to the hundredth. So the two instruments agree with each other and both disagree with the picture. This is the fogged-glass session's open item above, measured on a box: not a bug in `cost_line`, and not *run* against *step* — passes run along the angle and the stack steps across it — but a unit nobody wrote down. It also means the *passes along the sloped boundary* remedy for the staircase, which this painter used on a gable whose screen slope was 41°, laid them at 33°. (Measured.) | The sentence was done in that round. The engine form is `direction=((0.33, 0.01), (0.58, 0.29))`, a line to run along, on `block_in` and on every other verb that takes a direction. A pair of *points* is a line; a pair of *numbers* is still two angles, so `direction=(28, 118)` is untouched. `.axis` is left as it is, as the item said it could be. The measurements reproduced exactly: `-23` lays passes at **-12 degrees** on 1000x500 and `45` runs at **37** on 1024x768, and a line drawn at either angle on screen now lays them there. |
| **`compare({place: value})` asks the painter a question it could answer.** The pairs list says *do these two touch?* and the two rounds before this one answered it wrong — the ninth session's `0.00` pair met along the whole far edge. This painting's plan listed five pairs, of which two touched: the lit bench top against the right wall behind it at `0.04` apart, lightened to clear it, and the left bench against the left wall at `0.02`, darkened. Every place is a `Region` or a `Polygon`, the engine already has `contains` and `inside`, and whether two places overlap or share a boundary is one intersection test. (Reasoned; the two rounds' wrong answers are the evidence.) | Each pair is marked *(touch)* or *(apart)*, and only the touching ones go under the line that matters; the rest are named once as not a fault. Adjacent is overlapping or within `near`, which defaults to `0.01` — half of a fine brush — because a value plan carries places and values and no brushes to take half of. `Comparison.pairs` carries the answer as a fourth field. |
| **A drawing cannot survive the paint, so the method's own order costs a second drawing pass that nine of eleven paintings never made.** The guide's order is landmarks before anything, pencil after the far masses, near masses on top; in this painting the bench tops buried the first drawing and `p4_staging.py` redrew every pot and the can before the pass that painted them. Landmarks survive because a `mark()` is a point; a line is paint's to bury. (Observed.) | `s.guide(points, note="")`, with `s.unguide()` to rub it out. `mark()` extended from a point to a path, exactly as the item framed it: it touches no paint, no wetness and no graphite channel, `look()` draws it, `look(sketch=False)` leaves it out with the drawing, and `export()` never sees it. It travels with the session through save, load and replay the way the landmarks do. The measure of it is whether the next session draws once, which this round cannot answer. |
| **A smudge along a long boundary leaves a strip, not a lost edge.** One pass along each under-bench line in the finish pass, four points along a boundary about `0.4` of the canvas long, left a visible lighter band inside the dark for the whole length — the light floor carried into the dark at the calibrated reach, which on a short join is a softened edge and on a long one reads as a second edge running beside the first. It was kept under the happy-accident directive and should not have been. (Observed; the mechanism, the asymmetric pull `CALIBRATION.md` records under *`smudge`*, is a guess.) | Measured, and **the seventh item to close by measuring and finding nothing to fix**. The strip is the calibrated reach and nothing more: one pass at the default size on a hard step from `0.19` to `0.78`, the reach is **1.30%** of canvas height at join lengths `0.05`, `0.10`, `0.40` and `0.80` and `1.17%` at `0.20` — flat across a sixteen-fold range — and the strip's value comes back at `0.51`, halfway between the two masses to the hundredth. So the asymmetric pull is not doing anything extra on a long boundary, and the guess was labelled a guess. What changes is what the same band *reads* as: a softened corner over a short join, and *dark, mid, light* over `0.4` of the canvas, which is two edges where there was one. *An edge that is actually lost* now says a smudge loses a **stretch**, and that past about a tenth of the canvas the paint-across recipe is the one to start with. |

### What it asked of the documentation — done

Every item here was made in the same session, as the round recorded in `LESSONS.md`
under *One home per rule* and in `CHANGELOG.md` under *0.3.0*, in which it shipped;
each is a hypothesis until a fresh session paints against it. Three of the fogged-glass
round's open documentation items above were closed in passing and are marked there.

| Gap | What was done |
|---|---|
| **The same rule was stated in full in four to six of the five files**, and the front file held itself three times: a first-hour summary, a body, and a checklist restating the body. Counted, not felt: *paint masses, never up to a line* in six places, *vary the direction of marks* in six, *paint over, never undo* in five, the rehearsal rule and the smudge numbers in four each. | **One home per rule, linked from everywhere else.** `scripts/check_guide_overlap.py` reports any twelve-word run of prose stated in more than one of the four guide files, and reports zero; the calibration file is checked on request, because its claim lines restate the guide on purpose. **And the suite runs it since 0.6.0** (`test_one_home_per_rule`), because this claim had quietly stopped being true: the notice channel put *a mark's texture is seeded from its place in the log* into `REFERENCE.md`, where `PAINTING.md` already had it, and a script somebody has to remember to run is the preference this row is about. |
| **The stories were most of the words, and they did not prevent the mistakes they described.** This painter read every warning and still laid its glazing bars three times too heavy and its shadows as a fan of same-width rays; the rehearsal and the post-pass check caught both. The fifth painter in a row to say so, per the row above. | The anecdotes and the painters' own counts moved to `CALIBRATION.md` under *From the sessions*, labelled as reports rather than measurements, so each rule in the method could be one line with its number. `PAINTER.md` went from 9,973 words to 6,441 and is a card (*The first hour*, 894 words) and a body. `PAINTING.md` from 11,500 to 6,900, holding the engine's behaviour only. |
| **The drawing was a paragraph inside the block-in step, and the two passages this painter never drew were the two it named weakest.** The owner asked whether *make a sketch first* should be an explicit step. | **Step 1 of seven**, in its own right: draw it in graphite and keep drawing until it is proportional and the way you want it. The diagnosis index was renumbered with it. |
| **Nothing in the corpus said how to construct a scene of straight edges**, and three painters each wrote a metric projection from nothing — this one threw away two full drawings finding the eye height and the length of the room before writing it. | *A scene with straight edges* in `RECIPES.md`: the helper, the three numbers that decide the picture, why its lines cross the bands, and how it goes wrong as a diagram. |
| **The photograph material sat in the middle of the reasons file**, where a painter without a photograph had to read around it; the MCP section sat beside the brushes. | *Working from a photograph* is the last chapter of `PAINTING.md` and the reading order says to skip it; the MCP section is in `REFERENCE.md` with the rest of the facts. |
| **The eight checked rules were still paragraphs.** The check prints them after the pass that did it. | Each is one line pointing at `report()`, and the rules themselves are listed once, in `REFERENCE.md`. |
| **A row of small containers wants a stroke recipe and had a block-in one.** Thirteen pots laid with a `block_in` each, and a cross-hatched blob for what grew in them, rehearsed at 220 strokes; rebuilt as one to three chisel strokes for a body, a capsule for a rim, a dark stroke for the opening and one lit arc, at 108. | The clause in *A small container with something spilling from it*, with the cost of getting it wrong, and the rim as a hollow thing seen from above. |
| **`CALIBRATION.md` had no way in by rule**, and the reading order never reached its tables, which were the most useful pages in the corpus. | An index at its top mapping every rule the guide states to the section that measured it. |

### Confirmations, not new items

- **The *detail before the masses* rule fired on the rehearsal of every pass after the
  masses were down and never on the committed run of the same pass** — at 132 strokes
  spent (*28 marks under size=0.02 inside the painting's first 60*, the bars), at 158
  (*55 marks*, the pots), at 263 (*16 marks*, the can and the drips). The mechanism is
  the one the fogged-glass session isolated above; this is a second painting and a
  second painter meeting it on every pass, and the rewrite puts *rehearse then run* on
  the front page, so every painter will.
- **`compare({place: value})` was run four times** — on the empty canvas, after the
  glass, after the staging with the places redrawn to the new silhouettes, and at the
  finish — which is the first round since the eighth to run it as the method asks. It
  caught the two touching pairs above before either mass was laid, and it reported one
  stale place with a confident `−0.25` after a pot had been painted over it, which is
  the *re-read the places when a silhouette moves* clause doing its job.
- **Every failure was caught in a rehearsal and no committed mass was repainted** —
  seventeen rehearsals against 297 paid strokes, and not one scrape of the canvas.
- **A metric projection written before the first line**, `P(xm, hm, dm)`, the same
  helper the fogged-glass session wrote independently — a convergence then, a recipe
  now.

---

## The two long-standing items, and how they closed

**The split is a hypothesis, and the fourth session is the "given everything" arm.** The
third painter's prediction was that a session given only the method, the recipes and the
reference would paint the masses as well and improvise worse. The fourth had the essay,
and its own account of where that paid was not in laying masses — those followed the
method — but in two moments of improvisation where no recipe applied: abandoning
`scumble` for the lit field and rebuilding it as a solid block-in plus graded strokes,
and rewriting a whole edges pass as paint after the smudges failed. Both are *the smudge
softens; the paint is what removes* and *hide the passes with a bigger brush, never with
an argument* applied to situations neither sentence was written about. That is one
painter's introspection about its own reasoning and is worth what such a report is
usually worth — but it is the arm the prediction was about, and it points the same way.
**The other arm has now been run: the eighth session, below.** It did not settle the
prediction so much as re-describe what the deficit is.

**The post-pass check is built.** It was the cheapest thing on the list for two rounds:
a check over the pass just painted, printed beside the budget line, from inputs already
in the log. `Session.report()` is it, `easel run` prints it after every pass (`--check`
widens it to the painting, `easel log --check` reads it cold), and the MCP `run` tool
hands it back. Its rules are listed once, in `REFERENCE.md`, and every one of them was
met by a real pass of a real painting. The rule the fourth session proposed and this
page dropped — a solid mass whose planned and rendered values differ — is still not in
it, for the reason given then: the gap is `0.000`. The rules that need the *shape* fire
at the call instead.

**Its first outing was against a session that had never seen it** — the eighth, below,
where it fired on twelve horizontal passes in the painting's very first mass, on a
bristle under `0.025` four times and on pressure lists on a chisel tip twice, and every
one was acted on in the rehearsal it fired in. **And two rules have since left the
guide**: *you will under-vary your marks* and *you will use too many strokes on detail*,
both to `PAINTING.md` in 0.3.0, because the check names them after the pass that did
them with the numbers attached, which a paragraph read once cannot do. Neither left on
its merits — the front page's word budget left the eighth session's two items and the
ninth's three nowhere else to come from, which is the growth rule working as meant and
is now **the binding constraint on every documentation round**. Whether a rule can
safely leave is still unshown; what has changed is that it is a question a session can
answer, because there is a guide with two rules missing from it.

### The greenhouse sessions: three painters on one subject

One brief — a lighthouse mid-conversion into a greenhouse — was written down before any
of the guide was read and handed to three painters unchanged
(`paintings/Claude/lighthouse_greenhouse/{sonnet,opus,fable}/`). Their suggestion files sit
beside their paintings, and what they asked for is **done**: eleven engine items and
eight documentation items, in the two tables headed *What the greenhouse sessions
found* below, each with what was measured before it was built. Every number the three
painters took reproduced; two of the mechanisms they proposed for a real failure were
wrong, and both are said beside the fix. The one long-standing item the round closed
with them is the post-pass check.

**On the split hypothesis:** all three greenhouse painters are *given everything* arms —
they read the four guide files and at least one earlier painting — so none is the
missing *method-plus-recipes-plus-reference-only* arm. Opus and Fable each named essay
passages that did work no other file could (the glaze table, *the shape each tool leaves
behind*, *masses that are not rectangles*), the same kind of evidence the fourth session
gave, pointing the same way. **The other arm has now been run** — the eighth session,
immediately below — and the one thing left open on this page that the engine could not
close is closed.

---

## The eighth session: the arm that had not been run

Restricted to `PAINTER.md` and its nine exercises, then `RECIPES.md` and
`REFERENCE.md`. Subject chosen and written down before the repository was opened: a
municipal pool at night lit from underwater, `paintings/Claude/pool_night/`, **221 of 300 strokes**,
about forty rehearsals, subject share 39% at the moment the subject was finished against
a planned 40%, and a nine-value plan that `at_value` landed to the hundredth. It then
wrote an unprompted critique of the engine, the documentation and its own painting, and
only after that was shown the four withheld files and asked what each would have
changed. The order matters: everything in its critique was written without them.

**The prediction was that this arm paints the masses as well and improvises worse.**

The first half held and is not interesting. The masses followed the method, back to
front held throughout with no mass cut around anything, the value plan was numbers
before the first mark, and the greyscale view has its three separated values. Nothing in
the picture's structure wanted the essay.

**The second half did not hold in the form it was written**, and the reason is the
useful part. The one genuinely improvisational moment — that the water had to be mostly
the dark room reflected, with the lamps coming up through the gaps, rather than a lit
plane — came off no recipe, was arrived at by looking at a rehearsal, and is the thing
that makes the picture read at all. What the arm failed at was not improvising without a
recipe. It was **three lookups it could not make**, and only one of them is in the essay:

1. **It picked the wrong recipe and then blamed the verb.** An underwater lamp is *a
   volume of lit air* — light in a medium — and the session read it as *a passage light
   in the middle*, which is a bloom on a surface. Four rehearsals on an inward `scumble`
   that cannot lay it, converging to within a mark on the two glazes plus a core that
   `paintings/Claude/lighthouse_dusk/NOTES.md` records reaching twice. Both entries were in the
   file it had; the sentence that separates them is inside the second one. Its written
   critique called this a gap in the engine, which was wrong, and it said so once it had
   read the other painting.
2. **It could not know which numbers existed.** `PAINTER.md` points at
   `CALIBRATION.md` *"when a rehearsal is about to be spent finding a number that is
   already in there"* — an instruction that requires knowing the number is in there. It
   spent rehearsals re-deriving three: a glaze's strength being distance in **hue** as
   well as in value, `opacity` not quieting a scumble (the fix it found for a
   contour-ringed glow, and believed it had invented), and `inset()` by half a brush to
   hold a mass off its neighbour.
3. **It never ran `compare({place: value})` on the empty canvas.** This is the expensive
   one. Its worst structural fault — the coping reaching `0.50` against water at
   `0.45`–`0.55`, the frame as bright as the subject — is exactly what the pairs
   question exists to ask, and it was found at stroke 137 with `sample()` instead.

**So the essay's contribution to this arm was one section, and it is about a tool rather
than about judgement.** Of what the session could name as saveable — roughly twelve to
fifteen rehearsals and about twenty-five committed strokes — **the largest single item
is not in the essay at all.** It is in `paintings/Claude/laundromat_night/NOTES.md`: a custom
ground at `0.32`, because no preset goes below `umber_wash` at `0.425`. The eighth
session took `cool_grey` at `0.53`, knew by its third pass it was wrong, and talked
itself out of a restart that would have cost 21 strokes.

**What this arm cannot answer.** The painting is timid — six of its twenty-five passes
take something back rather than put something down, and it stopped at 221 with 79 in
hand. Whether that is the missing essay or this painter is not separable from one run,
and the run is n=1 against six of the other arm. **The honest claim is narrower than the
prediction: the deficit this arm showed was lookup, not judgement** — and two of the
three lookups were in files the split does not vary.

**One claim it made that did not survive its own reading.** Before seeing the withheld
files it wrote that the guide's repetition *seems not to have noticed its own cost*, and
`LESSONS.md` opens with the measurement that a rule correct, well placed and repeated
three times still failed every run. Fair about reading it, wrong about the cause — an
observation reasoned back to a mechanism that sounded right, which is the shape of every
re-measured claim at the foot of this page that failed. It made one of those too, and
said so in advance.

### What it asked for, and what was done

**It is the first round this page ever carried as open, and it is closed in 0.3.0** —
three engine items and five documentation items, in the two tables headed *What the
eighth session found* below. Each of its claims said whether its numbers were
*measured* or *observed*, and one was offered as an opinion with no measurement at
all; all of them were re-measured before anything was built, in
`scripts/probe_pool_session.py`. **Every number reproduced to the stroke.** One
mechanism did not, and the session had marked that one as a guess — which is what the
foot of this page predicts about guessed mechanisms, from the other arm of the same
habit.

Two of the three engine items are **instruments rather than mechanisms**, which is
what a deficit of lookup produces: the engine could answer both questions and would
not say either out loud. The third is a price the walk already knew and never quoted.

---

## The ninth session: the restricted arm, with the symptom index

`PAINTER.md` and its nine exercises, then `RECIPES.md`, `REFERENCE.md` and
`DIAGNOSIS.md`. Subject chosen and written down before the repository was opened: a grey
heron standing in sheet-flood over a parking lot at dawn, `paintings/Claude/heron_lot/1/`, **293 of 320
strokes**, about forty rehearsals, subject share **34% at the moment the subject was
finished** against a planned 32%, a thirteen-value plan `at_value` landed to the
hundredth, and two signature marks. It wrote an unprompted critique of the engine, the
documentation and its own painting, and only then read the three withheld files.

**Three things the earlier rounds predicted happened again**, and are recorded here as
confirmations rather than as new items:

- **It laid a lamp halo as an inward `scumble` and got a moon, twice**, before arriving
  at three crossing glazes — the fifth session to reach *a volume of lit air* the hard
  way, and the second to do it with `RECIPES.md` open.
- **It never ran `compare({place: value})`.** Its case is worse than the eighth's,
  because it did everything `PAINTER.md` step 3 asks: it planned thirteen values as
  numbers, printed each with `value_of`, and laid the ninth exercise's swatch strip
  before the first mass. It still shipped `sky_hi` at `0.50` and `water_mid` at `0.50` —
  planned `0.00` apart, and the two masses that meet along the entire far edge. The
  greyscale view had a dark and a mid and **no light at all until stroke 217 of 293**,
  when a look caught it; the repair is the passage the painter names as the picture's
  worst. This is the pairs question, twice in a row now, and the second painter had more
  of step 3 in hand than the first.
- **A depth-order violation, in a session that otherwise held back-to-front throughout.**
  Every mass went down far to near with nothing cut around anything. The violation was a
  late graded passage laid *over* the far trees, the pole and the bird's head — see the
  documentation table below, where the sub-case is named rather than the rule repeated. `LESSONS.md` already has this paragraph down as needing a rewrite after three
  failed runs; this is the fourth, and it is a different shape from the other three.

**What the arm did well without the essay.** The masses again followed the method. The
picture's one structural strength — the far edge lost across the whole left half, sky
meeting water at `0.07` and under the reading threshold, with the trees picking the edge
up only on the right — came out of repairing a ruled horizon and off no document. Two
passages were abandoned rather than fixed after two rehearsals each, which is the
`paintings/` habit arriving without `paintings/`.

### What it asked for, and what was done

**Closed in 0.3.0** — three engine items and six documentation items, in the two
tables headed *What the ninth session found* below, and the four its second painting
added in the two after them. Two of the three engine items are measurements taken
against an **open** item rather than new complaints, which is what this arm is for:
one of them settles the mechanism the eighth session guessed at, and it settles it
against the guess. All of it was re-measured before anything was built, in
`scripts/probe_heron_session.py`.

### The same painter, the same subject, a second time

After writing the critique above, the ninth session was shown the three withheld files
and then painted the **same subject again** with all of them in hand
(`paintings/Claude/heron_lot/2/`, 253 of 320, subject share 42% against a planned 40%). It is not a
controlled experiment — same painter, and it knew what it had got wrong — but it
separates two kinds of fault cleanly, and that is what it is recorded for.

| | first painting | second |
|---|---|---|
| strokes | 293 / 320 | 253 / 320 |
| subject share | 33% | 42% |
| stroke at which the picture had a light mass | **217** | **16** |
| depth-order violations | 1 | 0 |
| passages abandoned after two rehearsals | 2 | 1 |

**Every fault that was a lookup got fixed. The one fault that was judgement repeated
itself exactly.** `compare({place: value})` ran twice on the empty canvas and caught two
real merges before a stroke; the graded field went down in pass two with the light
already in it; every soft passage took its brush from the verb. And the body of the bird
came out a smooth mass with marks laid on it *again* — the failure *a mass built of
planes* names, which the painter had read, quoted in its own notes as its worst habit,
and then made a second time with the recipe open. That is one data point for
[`LESSONS.md`](LESSONS.md)'s standing question about what a guide change can do: the
files moved everything that was a missing number or a missing verb, and nothing that was
a missing decision.

### What the second painting added, and what was done

**Closed in the same release** — one engine item and four documentation items, in the
tables below. The engine item is the sharpest measurement the page has had from a
painter: a solid block-in does not land its own mixture, and under about four pixels
an oriented tip lands nothing at all. Its unit was wrong and its finding was right,
which the table says.


---

## The install session: the one that never painted

No strokes, no picture, and the only round on this page whose subject is the step
*before* the guide. A session was told to install the package and paint from it, and
spent its first ten minutes in `site-packages` instead: `import easel_paint` failed on
the distribution name, and the METADATA it went looking for the real one in turned out
to be a README from two releases back, whose pointer to `PAINTER.md` is a
repository-relative link. It reached the documents by following the `.pth` file to the
checkout, which is not a route anybody should need.

**The headline finding was not a bug, and that is the useful half.** The wheel ships
all five documents, `easel --help` lists `guide` last among its commands, and
`tests/test_guide.py` has guarded both since 0.3.0. What the session actually hit was
an **editable install that had gone stale**. `pip install -e .` writes `dist-info` once
and freezes it, while the `.pth` goes on serving whatever the working tree says — so
this machine had 0.1.0 metadata over 0.4.0 code, `pip show` and `easel.__version__`
three releases apart and both of them correct. The README that install serves is from
exactly the era the test file's own docstring describes, when the wheel carried none of
the method. **The fixed bug is reproducible indefinitely on any checkout old enough,
and nothing says so.**

One engine item and two documentation items, which is the whole of what survived
contact with a repository that had already fixed the thing the session came to report.

---

## The engine

*The rounds up to the ninth. Every round since the tenth carries its own tables, in its
own section above.*

### What the first session found

| What was wrong | What was done |
|---|---|
| Rehearsing a pass meant retyping it as a plan, so nobody did. About 60 of 224 strokes went on repainting masses laid once and disliked. | `easel run pass.py --rehearse` runs the script against a copy, writes the look, prints the cost, commits nothing. Seeded as the next real marks, so a rehearsed pass lands pixel for pixel. `Session.scratch()` is the same in Python. |
| `cost`, `preview` and `rehearse` took a plan; nothing *painted* one, so the plan had to be dispatched by hand — the drift the guide warns about. | `s.paint(plan)` takes exactly what the other three take and shares one dispatch with `rehearse`, so what is tried and what is committed cannot diverge. |
| The guide asks the painter to write the stroke split down. Nothing held it. | `Session(budget=300)` and `easel new --budget`. `s.spent`, `s.remaining`, `s.budget_line()`; `run` prints it after every pass; `cost` warns past a quarter of what is left. Nothing is ever refused. |
| No soft-passage verb. The guide's own remedy was a loop, and a first attempt at it came out as four hard bars — the loudest tell in that painting. | `s.scumble(band, a, b, n)` lays exactly that, charged as `n`. |
| The burying recipe was six clauses, one of which (`load_falloff=0.0`) was missing from the guide. | `s.cover(place, color)` dries the area and sets every clause. Handed a bristle it says it cannot bury. |
| `ellipse(p, 0.1, 0.1)` is an oval on a 4:3 canvas; the aspect arithmetic had to be baked into a custom shape builder. | `s.circle(place, r)` is round in *pixels* on any canvas; `ellipse(..., aspect=)` and `blob(..., aspect=)` take the ratio; `s.aspect` is the number. |
| No way to join two shapes or smooth an outline, so a lobed mass needed a custom generator and came out scalloped. | `union(a, b)` traces one silhouette and keeps the waist a `hull` would fill (and refuses shapes that do not touch); `shape.smooth()` cuts the corners off. |
| Getting a clean contour took three steps nobody would guess: inset by half the brush, fill, sweep the outline. | `block_in(..., edge="clean")` does it — **but along the *inset* outline, not the drawn one.** Measured: along the drawn line it spills further than a ragged fill (38px against 20px); along the inset line, 13px. It warns on a bristle, which leaves a stringier contour than the fill it replaced. |
| `palette.at_value` only went up, toward white. Hitting a planned value from above needed a hand-rolled mixer. | It bisects both ways — toward white to go up, toward a blue-umber dark to go down — and **raises** when the target is out of reach rather than silently handing back the nearest it managed. |
| With no photograph, the value plan existed only in the painter's head. Nothing checked the canvas against it. | `s.compare({place: value, ...})` measures each named place against what it was promised and writes the three-panel sheet. |
| Helpers had to be re-`exec`'d at the top of every pass. | A `prelude.py` beside the session file runs first, announced; `--prelude other.py` names another, `--no-prelude` turns it off. |
| 235 marks made a 2.6 MB GIF. | `timelapse_gif(path, fps=, every=, scale=)` and `easel timelapse --every --scale`. The finished painting is always the last frame. |

### What the second session found

| What was wrong | What was done |
|---|---|
| No verb for a value falling off from a *point* — a glow, a bloom. Four rehearsed attempts; the hand-rolled answer (strokes radiating from a centre) draws a daisy. | `scumble(..., direction="inward")` lays the passes *round* the place, the first on its boundary and each one further in, so nothing radiates. Charged as `n`. |
| `density=1.0` reads as a request for solid paint and is not one. Measured: interior sd `0.063` as laid against `0.007` solid, for the same 38 strokes. A whole near mass went down speckled. | `block_in(..., solid=True)` sets `load=1.0, load_falloff=0.0` as *defaults*, so an explicit `load=` still wins. Not folded into `density=1.0`, which would move every painting ever made. |
| Exactly one tip in the box does not repeat itself, and it is a comb. Five round dabs are five copies of one disc to within 7%. | `tip_wobble=0..1` draws a round tip's outline from three harmonics with a seed drawn **per stroke**, exactly as the bristle comb is. Off by default. Two dabs share 97% of their silhouette at `0` and 76% at `0.7`. `easel brushes` names it. |
| `edge="clean"` insets at the canvas frame too, so a mass drawn off the bottom left 2.4% of the bottom row unpainted. | The inset is dropped per coordinate on any side the outline reaches. Re-measured: 15.1% of the bottom row bare before, 0.3% now, against ragged's 3.6% — better than ragged, because the contour pass runs along the frame too. |
| Every rehearsal wrote `look_001.png` over the painting's and over the previous rehearsal's. Six rehearsals of one pass and no two could be compared. | Rehearsals take the next free `rehearse_NNN.png`, numbered from what is on disk rather than from a counter, because a rehearsal runs on a copy that is thrown away. |
| `cost` gave a number four to twelve times the hand estimate with no way to tell which lever moved it. | `s.cost_line(plan)` prints a line per entry — *"42 passes stepping across 0.34 of the canvas, each cut into 1.8 pieces by the outline"* — and the same sentence rides on the budget warning and the MCP echo. `s.cost_of(plan)` is it as data. The reason comes off the walk the price is counted from. |
| `sweep` took a boundary; `smudge` took only points, so following a curve meant sampling coordinates by hand — the step a painter skips. | `s.smudge(edge)` takes what it always took, and also a shape or region whose outline it walks. One mark either way. |

**One ordering note the second session made about its own list, worth keeping.** It
ranked items by strokes saved, and the smudge item saved none — both bad smudges were
caught in rehearsal. That understates it: what a smudge does wrong is not charged in
strokes but as a damaged passage, and burying a thumbprint means repainting the mass it
sits on, which buries whatever else is standing there. **This list prices a mistake by
what it costs to make, not by what it costs to live with.**

### What the third session found

| What was wrong | What was done |
|---|---|
| The inward scumble fills solid whenever the brush is wider than about twice the ring step — and a preset's default always is. Three rehearsals, and the verb was abandoned for hand-rolled strokes. | With no `size=` it now takes its brush from its own ring step, `3 × depth / n`; with one, it warns and says how many steps wide it is. `depth` is computed in one place, so the step a size is derived from and the step the rings are laid on cannot drift. |
| A pass that goes on top of another pass has to be judged on it, and `--rehearse` took one script. The wrapper written to get round it is in nobody's log. | `easel run p.easel a.py b.py [--rehearse]` runs them in order against one session or one copy. Each gets a fresh scope with the prelude re-run in front of it, asserted pixel-for-pixel identical to running them one at a time. |
| `look(diff=True)` inside a rehearsal had nothing to diff against — so the one question a rehearsal exists to answer could not be asked of it as a tint. | The trial shares the painting's last look. One assignment. |
| A `pressure` list flipped on alternate passes, so a passage meant to brighten toward one side could not be laid with the verb. Six strokes were hand-written for it. | The **paint** still alternates and the **pressure** is read in canvas order — not the `alternate=False` the item offered, which would have stacked every pass's run-out along one edge, the thing the alternation exists to prevent. Extended to `sweep`, which had the same defect. |
| Three encodings for handing a sampled colour back, one of which the documentation named and none of which the guide explained. | `s.sample(place)` returns the engine's own linear `float32` array, averaged over a shape rather than its box. It samples the paint, not the view of it: the relief shading `look` draws is light on the surface, not pigment in it. |
| *A question:* should the contour of `edge="clean"` wander? A ridge filled clean came back with a row of rounded knobs. | **Measured, and the answer is the wander — but not the lever the question proposed.** The brush's `jitter=0` moves the contour's seed-to-seed spread not at all (3.45px against 3.32px); the sweep's own wobble moves it from 3.3px to 1.1px. So `sweep` takes `wander=`, and the clean contour is laid with it off. The remaining error is the outline's own corners under a wide brush. |

### What the fourth session found

A night street: a laundromat window seen from across a wet road, 286 strokes of 300,
56 rehearsals, no repainted mass and no `undo`. Notes and pass scripts in
`laundromat_night/`. It read four documents and never opened `CALIBRATION.md`, which is
the last row of its own documentation list arriving as evidence.

**Two of its six engine items were answered by measuring them, and the answer was that
there was nothing to fix.** Both were *observed* rather than measured when they were
written, and both say so. That is `LESSONS.md`'s *check the painters' numbers* doing
what it is for — it has now overturned four claims across two rounds — and it is why
this session cost the engine less than its predecessors while being the most detailed
list yet. The measurements are in `scripts/probe_fourth_session.py` and the numbers in
`CALIBRATION.md`.

| What was wrong | What was done |
|---|---|
| **The view and the measurement disagree about value**, and only one of them is what a viewer sees: `sample()` and `compare()` report pigment, `look()` and `export()` render the impasto relief. Four masses came back as bright bars against walls they were `0.03`–`0.09` above, and `compare()` called the value plan clean throughout. | **Measured first, and they do not disagree.** Over a mass the rendered view and the sampled paint are the same to `0.000` at every load, value and ground tried; the relief is a *gradient*, so it lifts one side of every ridge of paint and drops the other by as much, and the worst single pixel anywhere is `0.038`. `look()`, `look(values=True)`, `export()` and `export(impasto=False)` all read the same mass at `0.314`. So the repair is the one the item asked for minus the premise: **`s.sample(place, rendered=True)`** samples the view, so the question is a line rather than a belief, and `compare()`'s table now names the surface it measured and the call that reports the other. The section is in `CALIBRATION.md` as *The paint and the view of it*, with what a `0.09` step actually looks like at the dark end of the range, which is the likelier account of four bright bars. |
| **`solid=True` is the argument that moves a mass furthest from its planned value** — maximum paint height, hence maximum relief, hence maximum lift in the view. The row asked for was how far a solid field moves in the rendered view. | **The row is a row of zeroes, and it is in `CALIBRATION.md` anyway**, because a number nobody has to wonder about again is worth its four lines. Laid solid, a mass reads the same in the view as in the paint to three decimal places. What `solid=True` *does* move is the paint — about `0.03` darker than the same mixture at the default load, because the passes stop running dry — and that was already documented one section up. `REFERENCE.md`'s `solid` row says both. |
| **`overhang` rotates with the pass direction, and its default differs between a box and a shape**, and both surprises cost a mass: at `0` the passes stopped dead on the window's boundary, and at `0.6` on a door — whose passes run *vertically*, because its axis does — they ran the glass over its own kick panel and onto the sidewalk. | **Said, in those words, with the measurement.** `REFERENCE.md`, `PAINTING.md` and the docstring now state that "the ends" are the ends of the *pass* and turn with `direction`, and the box/shape defaults have their own clause saying why they differ — a rectangle stopping short of its corners reads as cropped, a shape's outline *is* the drawing. Measured on a shape `0.40 × 0.30`: swept horizontally, `overhang` takes the paint from 3px to 22px past the left edge while top and bottom stay at 6px; swept vertically it moves the top and bottom instead. **The warning was not built**, because measuring its condition found nothing to warn about: laid solid, the strip inside the pass ends is `0%` bare at every setting, and at the default load the strip inside the *sides* — where `overhang` does nothing — is barer than the ends. That is the comb and the brush running dry, and its condition is `block_in`'s own defaults. |
| **`scumble` fails in both directions on the linear case**, and it already knows how to prevent one of them: at `size=0.050` on a `0.034` step the passes left gaps and the brightest mass in the painting came back a venetian blind; widened to `0.095` the centre closed. Three rehearsals, and the verb was abandoned. | **The band picks its own brush now, `3 × extent / n`** — the mechanism `direction="inward"` has used since the third session, now on both directions — and warns when handed one under two steps. Measured on a band `0.80 × 0.40` at `n=8`: the profile's one-step ripple runs `0.014` at one step and `0.015` at one and a half, which is where a preset's default lands, against `0.007` at three; under a step the band is barely painted, and past five the last passes bury the first. The painter's own two numbers — 1.5 steps bad, 2.8 steps good — reproduce exactly. **And the accumulation is the second half**: `opacity` is documented on `scumble` itself now, with the table. From `0.40` up it is the same passage to within `0.04`, because overlapping passes accumulate; to make a passage quiet, mix its two colours closer together. |
| **`smudge` at documented sizes drags a lobe instead of softening a join.** Four of five failed in one pass at `size=0.024`–`0.032`, and the sizes came from the guide's own examples. *The suspect is the default.* | **It was the default.** Measured on a steep join: below `0.014` the pass does nothing at all, the softening arrives at `0.016` and then flattens at about half the join, while the reach goes on growing in a straight line — `1.3%` of canvas height at `0.020`, `2.3%` at `0.040`, `4.4%` at `0.070`, which was the default. **So the default is `0.02`, the knee of its own curve**, and past `0.03` the call says what it will look like. The window is a table in `CALIBRATION.md` with its canvas, brush and step stated; the guide's examples, which all ran at `0.04`–`0.09`, now leave `size` off. The old *"`0.035`–`0.045` behaves"* line was measured on a canvas nobody recorded, and it measured only what a smudge buys. |
| **Three documented surfaces do not behave as the documentation's own promise implies**: `scumble(solid=True)` and `block_in(glaze=True)` raise about `Brush.__init__()`, and `shape.box` — "the rectangle a mass is priced on" — is not iterable. | All three, as asked, and it cost an afternoon. A keyword that is not a brush field now raises naming the call that takes it (`solid=` is `block_in`'s, `glaze=` is `stroke`'s, and a misspelling gets the nearest field); `Region` unpacks as `x0, y0, x1, y1`, which is what anybody does with a rectangle. **The promise itself was the problem** — *any brush field is also an override on any painting call* is true, and it means a neighbouring call's keyword lands in `**brush_overrides` and comes back as a message about a class the painter never mentioned. `REFERENCE.md` now names the owning call beside `solid`, `glaze`, `overhang`, `density` and the rest. |

**Its five documentation items are done too**, and four of them were one line each: the
checklist says at which moment the subject's share is compared against the plan (when
the subject is finished, not at the end — after which the last-third rule is *meant* to
pull it down, and the arithmetic is written out in `PAINTING.md`); a checklist line asks
whether the bands are in the marks or in the subject that was chosen, to be counted
before the first mass; step 1 says what the pencil buys that `preview` does not —
*`preview` checks a mark against a plan, and the pencil checks the plan*; and
`CALIBRATION.md` is cited from the rules that have a number in it rather than only from
the contents table, whose *when* was a curiosity rather than a moment. The fifth is the
first engine row above: what the guide has to say about a planned value and a seen value
turned out to be that they are the same number, which is a shorter thing to say than the
warning that was asked for.

### What the greenhouse sessions found

Three painters, one subject, three request lists — deduplicated into one round. Two of
the three had probed their own claims before making them and the third's were checked
here first; **every number the painters took reproduced**, to the percentage point where
one had been taken, and two of the mechanisms proposed for a real failure were wrong in
ways that changed what was built. The measurements are `scripts/probe_greenhouse_session.py`
and the numbers are in `CALIBRATION.md`.

| What was wrong | What was done |
|---|---|
| **`edge="clean"` fails on a mass narrow relative to its brush**, found by all three: a pointed arch above a tapering tower (Sonnet), a cap eaten to a mushroom, corners first (Opus), and a 65px arch standing off a four-cornered tower (Fable), who isolated it to the contour's spline bowing through sparse corners. They disagreed about the trigger — corner spacing, or the brush's share of the shorter extent. | **Both things the register asked for, and the trigger was neither number.** The contour is swept along the polygon's own edges rather than a spline through its corners: the arch goes from 65px to 4px on Fable's tower, 45px to 4px on the dusk example's own `tower()`, and 69px to 4px on a taper like Sonnet's — the ragged fill's 2–4px, so the contour now stops where the fill does. The share survives as the corners finding: measured on Opus's cap, the corners of a clean mass go past about a quarter of its shorter extent (83% of the corner pixels painted at a 22% share, 70% at 29%, 51% at 36%, 6% at 58%) while the cap as a whole stays covered, so `block_in` and `preview` say so past a quarter, in the shape the scumble warnings have. The same draw from the stream as the sweep it replaces, so nothing laid after a clean mass moves; the clean masses themselves do, in every painting that has one. |
| **A chisel tip staircases a mass whose boundary is not parallel to its passes** — 13–17% of strong edges within 10° of horizontal on a mass with no horizontal feature, against 3–4% for `bristle`/`round_hard`. One dimension over from *a shallow shape → its bounding box*, and not in that table. (Opus, measured.) | Re-measured to the percentage point — `flat` 13% and 17%, `knife` 16%, `bristle` 4% and 7%, `round_hard` 3% — and rowed in *the shape each tool leaves behind* with the repair beside it: lay the plane with a comb, put the core back with one solid stroke down the middle. The table is in `CALIBRATION.md` under *Pressure*. A documentation item with a measurement, which is what the painter asked for; the engine change it would want — breaking a chisel's pass ends — would move every mass ever laid. |
| **Oriented tips ignore a `pressure` width taper** — every pot a chisel-ended rectangle, the exact passage the painter had read, twice, in two paintings. *Warning is not method* reproduced. (Sonnet, Opus.) | **The engine says it at the call**, in the shape `smudge`'s size warning has: a hand-laid mark shorter than four brush widths given a pressure list with more than one value on a `flat`, `bristle` or `knife` says the list changes the paint and not the width, and names `round_hard` and `liner`. A list on a long pass is how *a passage brightening toward one side* is laid and is left alone, and so are the passes of a mass, where a list is the canvas-order feature. The same condition is a rule of the post-pass check. |
| **A shaped `block_in` with `direction` left off costs 3–11× its axis price** — mid plane 3.9×, lit band 11× — because the default steps down the whole height; a rehearsal charged 124 for a pass budgeted at 40. (Opus, measured.) | **The ratios reproduce exactly — 3.9×, 11.0×, and 1.0× on the one mass wider than tall — and the price walk says so at 2.5×**, from `cost` and from the call, naming the axis count and `direction="axis"`. The default does not move, for the reason the painter gave: `"axis"` would be right nearly always and moving it would move every painting ever made. `direction`'s default is now `None`, which is horizontal, so the engine can tell *left off* from *chosen*. |
| **`scumble`'s `3 × extent / n` auto-size blooms at the narrow end of a shape whose width varies ~9× along the stepping axis** — a beam wedge, abandoned after one rehearsal for a hand-built passage in five pieces. (Sonnet, observed.) | **Measured, and it is the brush being wider than the whole narrow end.** On a wedge `0.045` to `0.42` across, the auto-sized brush is `0.240` and the passes run `0.068` and `0.397` long; paint landing outside the outline is 73% of the wedge's area beside the mouth half. The verb reads the pass lengths at both ends and says so when the brush is wider than either, naming both lengths — and the sentence the painter offered as the alternative is in *a quiet gradient* beside *leave `size` off*: lay a wedge as two or three bands each sized to its own width, or hand it `size=` for the end that matters. |
| **`compare({place: value})` scores each place but never the gap *between* two places**, which is what `0.10` actually means; a sheet finished all-green with two masses planned `0.00` apart, and they merged on the canvas. (Opus, arithmetic exact.) | The table lists every pair of planned places within the threshold of each other, closest first, and asks *do these two touch?* — a question, not an error, because three of that plan's four close pairs were masses that never met. Read off the plan rather than the canvas, so it is asked on the empty canvas, which is the run the guide already tells a painter to make. `Comparison.pairs` is it as data. |
| **CLI `easel undo` is not reliably lossless** — the painting's undo detour drifted 1.06% of pixels from a clean rebuild, confined to the marks after the undo, and resisted minimisation. The mechanism was guessed as accumulated state, "the random stream or the wet paint layer". (Fable, measured.) | **Two causes, both root-caused, both fixed, both tested.** A mass draws its pass wander from the session's stream between the strokes it records, so undoing one left the stream past it; and `easel undo` rebuilds from the log, whose replay never draws the wander, so it handed back a stream sitting at the seed. Every record now carries the stream's state at the start of the call that made it — taken once, before the first draw, which is why an earlier attempt at this was left open in `LESSONS.md` — and undo restores it on both paths. The other cause was the one the toy cases could not show: the log rounded every point to five decimals, so a replay from disk laid every wobbled pass a hair off its line, invisible on hand-written coordinates. The points are exact now. A mass, a detour undone, a third mass: identical to a clean rebuild in-process for a mark, in-process for a whole mass, and through the session file. The practice note the painter asked for is therefore not written; the finding is in `CALIBRATION.md` under *The log, undo, and the stream*. |
| **Free planning verbs leave the RNG stream untouched** — the property that makes *rehearse everything* free of side effects; `pencil` is the exception and "advances the stream". (Fable, measured.) | **Asserted by a test**, verb by verb: a bristle stroke laid after `look`, `look(values=True)`, `preview`, `rehearse`, `cost` or `compare` is the stroke laid after nothing, to the pixel. The exception's mechanism was wrong and the exception was bigger: `pencil` never touches the stream — it is *logged*, and a mark's texture is seeded from its place in the log, so `dry()` and `erase()` shift every later mark the same way. One paragraph in `PAINTING.md`'s *The rest of the API*, and a table in `CALIBRATION.md`. Not changed: seeding from the count of paint marks alone would move every painting with an underdrawing. |
| **A saturated mixture reads more vivid in a very low-chroma field than `value_of` predicts**; two mixtures each needed a third desaturation pass found only at real scale. Mechanism a guess: simultaneous contrast. (Sonnet, observed twice.) | **The engine side was measured first, and it is nothing** — the fifth *nothing to fix*. A solid plane reads back at the mixture's own Oklab chroma or a little *under* it, never above (the ground pulling the first passes toward itself), and the rendered view reads the same as the paint. So what read more vivid was the eye, judging a colour against its field, which the engine cannot measure and does not add to; the instrument the painter asked for is built instead: `palette.chroma_of`, beside `value_of`, with the pigments' own numbers in `CALIBRATION.md` for scale. It is what the ninth exercise prints. Not a guide rule, as asked. |
| **A lone one-script `--rehearse` on an already-painted session reports `stroke_count`/`remaining` as `0`/full budget inside the script**, while its `compare()` sees the real canvas. Not root-caused. (Sonnet.) | Root-caused: the rehearsal copy started its own log from nothing, so its count was the pass's and its budget the whole one. The copy now carries the painting's count, so `stroke_count`, `spent`, `remaining` and `budget_line()` inside a rehearsed pass are the numbers the pass will see when run for real; what the copy itself laid is its own `history.stroke_count`, which is what the shell's *Rehearsed* line always reported and still does. |
| `cost_line()` names the mechanism (*cut into N pieces by the outline*) but not the remedy. (Sonnet.) | It names it in the same breath — *lay the straight stretches as strokes, or use a wider brush* — and *2 directions* adds *one mass rarely needs two*. |
| **The post-pass check**, open since the synthesis, with the greenhouse's two candidate rules added to it. | Built — see *Still open* above for what it is. Building it needed one thing the log did not have: a way to tell a pass of a mass from a mark laid by hand, which every record now carries as `params["via"]`. |

### What the eighth session found

A pool at night, painted against `PAINTER.md`, `RECIPES.md` and `REFERENCE.md` and
nothing else. **Every number it took reproduced to the stroke**, and one mechanism it
offered did not — it had marked that one as a guess. The measurements are
`scripts/probe_pool_session.py` and the numbers are in `CALIBRATION.md`.

| What was wrong | What was done |
|---|---|
| **A glaze's usable opacity is a function of its distance from the field, and there is no instrument for it.** `CALIBRATION.md` measures the problem — at `0.14` a film moves the value `0.087`, within a hundredth of the `0.10` that makes a new mass, and at `0.05` the underlying hue is already dead — and the guide's answer, *mix the glaze close, then choose an opacity*, leaves the second half as a two-step search run by rehearsal. Six of this painting's rehearsals went on it and one glaze was rehearsed three times and dropped. The instrument asked for: `glaze(points, color, to_value=0.62)`, solving for opacity the way `at_value` solves a mixture for a value. (Measured by the file; the cost observed here.) | **Built as asked, and it is a search rather than a formula**, for `at_value`'s reason: what a film delivers is the pigment model, the tooth and whatever is already there, and none of that is available as arithmetic. `glaze(to_value=)` lays films on trial canvases until one delivers the value, **measured over the film's own footprint** rather than a region named by hand, and then lays that one. It lands within `0.002` of the target on every case tried, costs one stroke like any other glaze, and puts the opacity it chose in the log. Because the trials come off a *copy* of the stroke stream, the film that lands is byte for byte the film that would have landed had its opacity been typed out — solving for it moves no paint, and a test holds that. A target the film cannot reach raises, naming the value under it and the value at `opacity=1.0`. |
| **The inward `scumble`'s usable `n` is bounded by the patch, and the verb warns from only one side.** The brush is `3 × depth / n` and the post-pass check's comb floor is `0.025`, so `n ≤ 120 × depth`: on a shallow patch there is no `n` giving both enough rings to avoid contour banding and a brush that is a brush. Met at `n=12` on `depth=0.075`; the resulting bristle warning was read as an unrelated complaint and two further rehearsals were spent. (Arithmetic exact; the banding observed.) | **The arithmetic is exact and the verb says it from both sides now**, in the shape its other warnings have. It names the patch's depth, the brush it derived, the floor, and the largest `n` that clears it — *more rings on a patch this shallow buy a narrower brush, not finer banding*. Where no `n` fits it names *a volume of lit air* instead, as the request asked. **One number moved**: *about `0.07`* is the wall for the recipe's eight rings, and the wall where nothing fits is `0.042`, which is five rings — the fewest the verb's own docstring says read as a fall-off. Both are in `CALIBRATION.md`. |
| **`direction=` given a sequence is priced far above any single angle in it.** Measured on one mass, same brush, same density, same call: `"axis"` **4** strokes, a single `-17°` **7**, `"cross"` **15**, a ten-angle sequence **51**. `cost()` gives the number and nothing gives the mechanism; the greenhouse round's 2.5× price walk fires on `direction` *left off*, not on a sequence. (Costs measured. The mechanism — that the stack is sized for the steepest angle in the list — is **observed and offered as a guess**, which this page's own record suggests is the half most likely to be wrong.) | **The costs reproduce to the stroke and the mechanism does not, exactly as the request predicted of itself.** A sequence is *one whole pass per angle* and the mass is charged the **sum**: on the same room mass a ten-angle list costs 85, which is `4 + 5 + 7 + 7 + 9 + 10 + 10 + 11 + 11 + 11`, and the steepest of them alone is 11. So the price walk covers a sequence at the request's own threshold — *far above any single angle in it* — and names every angle's price in the line. Two angles can never be more than twice the dearer of them, which leaves `"cross"` and the cross-at-the-mass's-own-angle idiom every painting here uses silent, and catches the list that is really a stack. The row asked for is in `CALIBRATION.md` as well. |

### What the ninth session found

A heron in a flooded lot at dawn, painted twice: once against `PAINTER.md`,
`RECIPES.md`, `REFERENCE.md` and `DIAGNOSIS.md`, and then again with the three
withheld files in hand. **Every number both paintings took reproduced**, and two of
the claims built on them did not survive in the form they were written — one of them
the *eighth* session's guess, which this session was measuring. The measurements are
`scripts/probe_heron_session.py`; the session's own probes are beside its paintings.

| What was wrong | What was done |
|---|---|
| **A hand-rolled graded passage gets none of the protection `scumble` now has, and `RECIPES.md` teaches the hand-rolled form.** *A passage brightening toward one side* is six `stroke()` calls with the sizes written out, and neither it nor step 4 says the thing the verb now knows: the brush has to be about three times the step or the passes read as bars. Measured on this painting against itself — the sky, `scumble(n=11)` with the brush left to the verb, sits at a uniform 4.0 steps and wobbles `0.037`; the dawn band, seven strokes with brushes chosen by hand, tapers 4.2 → **1.7** steps and wobbles `0.072`. Twice as rough, same canvas, same painter, same pass structure. (Measured.) | **A seventh rule of the post-pass check, as asked**, and the clause in the recipe as well rather than instead. It fires on three or more long marks at three or more colours whose step is over half the narrowest brush laying them — `scumble`'s own `2 ×` wall, applied to a stack laid by hand. The conditions are narrow on purpose, because the same session's third item is a rule it learned to ignore: **a mass is one colour however its passes are spaced**, which keeps every `block_in` out of it (at `density=1.0` its passes are `0.55` of a brush apart, and right to be), and marks further apart than four brushes are separate marks rather than a passage laid badly. Checked against the session's own dawn band, a verb-sized scumble, a narrow one, block-ins at three densities, a sweep, and three parallel trunks. |
| **`direction=` given a sequence lays a complete stack per angle, and `REFERENCE.md` says the opposite.** The eighth session filed the price and marked its mechanism — *the stack is sized for the steepest angle in the list* — as a guess. It is not that: the cost is the exact sum of what each angle costs alone, nine for nine on three shapes, and `direction=[0, 90]` logs 7 passes at `0°` plus 30 at `90°`. A treeline given sixteen angles on the guide's own advice to vary direction was quoted **515 strokes against 22 for one direction**. (Costs and pass angles both measured.) | **The measurement stands, to the stroke, and it is the second session to settle this against the first's guess.** The price walk covering a sequence landed in 0.3.0 from the eighth session's own list, so this arrives already built, and both probes fire on it. What was left was the wording, which is the half this session asked for first: `REFERENCE.md`'s `direction` row now says *a sequence lays a full stack per angle and is priced as the sum of them*, with the `[0, 90]` pass counts and the 515 beside it, and `CALIBRATION.md` has the row. One fix of its own: the warning was suggesting `direction=("axis", 180)` on a mass whose axis is `90`, which is horizontal written the long way round — normalised. |
| **The check's bristle floor fired 28 times across the painting and was correctly ignored 28 times.** *A bristle under `size=0.025`* is right for a solid plane and wrong for what this painting is mostly made of: broken glints on water, grit under a flood, feather groups on a bird — marks where the comb's gaps **are** the mark. By the second half the painter had stopped reading that line. (Observed; the count is from the log.) | **Narrowed exactly as proposed, and the repository agrees with the painter.** The rule now skips a mark whose `load` is at or under `0.6` — the top of the run-out window `CALIBRATION.md` already publishes for a deliberately broken mark, not a new number. Checked against both of this session's paintings: **every** small-bristle call site in them names an explicit `load` and **not one** uses the preset's own `0.9` — 15 of 16 at or under `0.6` in the first and 12 of 12 in the second. So the rule was firing on nothing it was written for. What still fires is a small *loaded* comb, which is a solid plane laid with the wrong tip. |
| **A solid block-in lands short of its mixture, and under about four pixels it lands whatever was underneath.** Bare ground `0.394`, every clause of *a plane that is a plane*, a mixture at `0.865`, 600×600 linen: at 2.7px a `flat` lands `0.403` — nothing — and even at 18px it is `0.04` short and a `bristle` `0.09` short, which is most of the `0.10` that separates two masses. Only a round tip holds its colour small. Four rehearsals went on a bird's head at `size=0.005` that came back a dark fuzzy ball. Asked for: a `CALIBRATION.md` row with the size column, a clause on `solid`'s `REFERENCE.md` row, and **a warning when an oriented tip is handed a `size` under about `0.008`**. (Measured; the second painting's own probe.) | **The table reproduces to the thousandth, the general statement is right, and the warning's unit is wrong.** Both halves the painter could not see from one ground are now measured: over a *lighter* ground the same mixture lands **above** itself (`0.873` over `0.957`), so it is a pull toward what is underneath in both directions. And the cliff is at four **pixels**, not at a `size`: `size` is a fraction of the canvas long side, so `0.008` is 2.4px on a 300px canvas — already dead — and 9.6px on a 1200px one, a perfectly good brush. Measured on all three canvases the knee is at the same pixel width, and one stroke of a `flat`, `bristle` or `knife` deposits **zero** paint at 1–2px against a `round_hard`'s 44–51 pixels' worth. So the warning counts pixels, fires once per call from every verb a `size=` reaches and from `cost()`, and names `round_hard`. The row and the clause are written. |

---

### What the install session found

One item, and it is about being *found* rather than about paint — the only engine item
on this page from a session that laid no strokes, and the only one with no measurement
under it, because nothing here needed measuring. It needed running `dir()`.

| What was wrong | What was done |
|---|---|
| **`easel.guide` was the one submodule `dir(easel)` did not list.** `brush`, `canvas`, `palette`, `regions`, `stroke`, `texture` and `look` are all bound by `__init__.py` as a side effect of its `from easel.X import ...` lines. `guide` is imported by nothing, so a bare `import easel` raised `AttributeError` on it. The path is narrow — `from easel import guide` has always worked, and `tests/test_guide.py` opens with it — but absence from a listing is a claim, and the claim it makes is that the engine ships no method. The exclusion looked deliberate at first, since `cli` and `mcp_server` are left out the same way, and it is not the same category: those two are process entry points nobody calls from Python, and this is an ordinary module with an ordinary API that the test suite calls on its first line. (Observed.) | **Bound in `__init__.py` and named in `__all__`**, on the grounds the module's own docstring gives: the guide is the deliverable, so it should not be the one module you cannot find by looking. Guarded by `test_the_guide_is_reachable_from_a_bare_import`, which runs the check **in a subprocess** on purpose — every other test in that file does `from easel import guide` at import time, and that binds the attribute for the rest of the process, so the same assertion made in-process passes with the fix reverted. Confirmed by reverting it. |

---

## The documentation

*The same rounds, and the same rule about where the newer ones live.*

### Rules and numbers that were wrong or missing

| What was wrong | What was done |
|---|---|
| The guide said `overhang` would hold two masses apart. It controls the ends of a pass, not its sides: measured, the sides sit half a brush past the band at `overhang` `0`, `0.35` and `1.0` alike. | Corrected in the guide, with the measurement in `CALIBRATION.md`. The half that works — inset the place by half the brush — is what it says now. |
| `log(last=)`, `contact_sheet` and `timelapse_gif` were undocumented, so a painter concluded the log was truncated. | In *The rest of the API*, with `every=` and `scale=` beside them. |
| The unit mismatch between a coordinate and a brush size was explained under brush sizes, where nobody looks for it. | Under *Getting started* where coordinates are introduced, with the formula and `s.circle()` beside it. |
| "A hex string or a **linear** RGB triple" — the triple is read as sRGB, like the hex string. A sampled colour handed back as a tuple landed near black, and the same error was in two documents. | Both corrected. The guide's *Colour* now says what a triple is, and leads with `s.sample()` for the case that actually caught someone. `REFERENCE.md` carries the same row with the measurement. |
| Nothing said which side a stack of passes starts from, so a scumble's colours landed the wrong way round and a lit face went on the wrong side. | A table in `REFERENCE.md` under `direction`: `0`/`"horizontal"`/`"axis"` starts at the top, `90`/`"vertical"` at the right, `45` upper-right. Re-measured before writing. |
| `CALIBRATION.md`'s fall-off table was measured on a patch whose size nobody wrote down, read its own flat middle as a fall-off, and a painter applied it to a larger patch and got a solid disc. | The table states the patch radius, the brush, the opacity and the canvas, and reads its own middle correctly. **And it became a standing rule at the top of the file**: every number states what it was measured on, and a claim with no test behind it says so. |
| Nothing said that `solid=True`'s remaining unevenness is the pass structure, or that it does not move with `opacity`. | A line in step 1 and a table in `CALIBRATION.md`: about `0.03` of value at every combination of opacity and pressure. Hide it with a bigger or broken brush, never with an argument. |
| The glaze line said "thin transparent film" and nothing else. A glaze far from its ground in hue is a stripe at one opacity and invisible at the next. | Measured and written up in both *Wet paint* and `CALIBRATION.md`: at `opacity=0.14` the film moves the value `+0.087`, within a hundredth of the `0.10` that separates two masses; at `0.05` the underlying hue is already dead. **Mix the glaze close, then choose an opacity.** |
| `compare()` cannot know that a place in a written value plan has changed meaning when a silhouette moves. A place that ended half one mass and half another reported a `-0.16` miss that was not one. | A paragraph under *Painting without a reference*: when a silhouette moves, the plan's places move with it — and read the sheet's outlines, not only its numbers. |

### Rules that were right and kept failing anyway

| What was wrong | What was done |
|---|---|
| The eight exercises were skippable, and the session that skipped them met two of their lessons inside the picture instead, at the worst moment. | Stated as a gate at the exercises — where the decision is made — naming the two lessons that were paid for inside a painting, and the reason an exercise is the cheap place to fail: nothing is built on top of it. |
| *Rehearse any mass you would not want to repaint* asks the painter to predict which passes will go wrong. | **Replaced with *rehearse everything; it costs a look*.** Eighteen rehearsals in one painting, every one of which changed something, none charged, and no stroke of that painting spent on repainting. |
| Three painters made the same four mistakes *after* reading the warnings about them. A warning the reader will violate anyway is only useful if the repair is beside it. | A table at the top of *What you are bad at*: floating discs, capsule shadows, the stack of bars, brushwork that is all flat and round — each with its repair on the same line, and the one cause under all four. |
| The guide warns about mechanical *marks* and not mechanical *objects*. One shading recipe painted three of a thing and they read as three copies. | The second half of *You will under-vary your marks*, stated as a procedure: vary one thing per object on purpose, and the guide names which things are cheap to vary. Repeated at the foot of `RECIPES.md`, where the temptation is strongest. |
| A shadow is the first place a painter spends the palette's darkest mixture, and it is the wrong place. | In step 3, straight after the value floor, with the measurement: on a surface at `0.60`, the darkest mixture lands at `0.16` and reads as a hole; `0.50` reads as a shadow, `0.42` as one with weight. And it is a tapering stroke, not a filled shape. |
| The `0.10` value threshold was given as a floor with no ceiling, so a mass shaded until its form read had stopped separating from its background. | Beside the threshold in step 3, as a window: shading spends value range, the range is shared with the mass's separation from what it stands against, so **shade until the form clears `0.10` and stop.** One mass behind it; worth re-measuring. |
| The closing checklist had fourteen lines and none about finishing. One painter stopped with 115 of 300 strokes unspent having already named its own weakest passage. | Two lines and a preamble. The list now opens by saying that passing it means the painting is not *wrong*, not that it is finished; it closes with *you have named the weakest passage — how many strokes are left? Spend them there.* |
| "Did you spend enough on the subject?" is a question every painter answers yes to. Three of them underspent while quoting the warning: 59% of strokes before the subject began, 24% against a planned 32%. | The checklist now asks for **a number written down**, with the four lines of `s.history.records` that count it, and `note="subject"` as the habit that makes it countable. |
| Nothing said the lightest mass could quietly stop being the one the picture is about — a composition fault that `compare()` reports as a value miss. | A checklist line under the composition question it makes checkable, with both ways to answer it. |
| The guide's only `smudge` example was two points, so a painter followed the example's shape instead of its rule and dragged two lobes of one mass into another. | The example is a curve, and names `s.smudge(shape)`. **The measurement behind it was wrong and was corrected**: on a *straight* slope two points and four are the same pass to the pixel. The effect comes from a **bend**, where it is larger than reported — `0.51%` of canvas height against `0.01%`. The rule survived its evidence and got sharper: *only a straight boundary is two points.* |
| A checklist line that only names a fault is a warning without a method. | The small-mark line names `tip_wobble` as the remedy, and the *shape each tool leaves behind* table has a row for it. |

### Structure

| What was wrong | What was done |
|---|---|
| The guide was 17,600 words, read once, before the first stroke. Every session said it was long; every session said the essay is what made the rules stick. Both are true, and three attempts to shrink it by editing had not worked. | **Split by function, moving rather than cutting.** `PAINTER.md` is the method (9,400 words); `PAINTING.md` the reasons; `RECIPES.md` the procedures; `REFERENCE.md` the facts; `CALIBRATION.md` the numbers. Not one word was deleted. The two-goes instruction is now a file boundary rather than an instruction, which is what it should have been — an instruction to read something in two goes was tried and a painter read straight through it. |
| The no-growth rule in `LESSONS.md` was a preference: the guide doubled under it, from 8,600 words to 17,000. | A **word budget asserted by `tests/test_guide.py`**, so CI holds it the way the engine holds a stroke budget. Over budget, the fix is to move a section out, not to raise the number. |
| The operational facts were hard to find inside an essay. | `REFERENCE.md`, checked against the source by `tests/test_reference.py` rather than by hand — the brush table against the presets, every default against the dataclass, every region, ground, texture, pigment, pressure profile and `prepare` level, and every `--flag` against the parser. The one thing that would make a reference worse than none is drifting from the engine, and that now fails the suite. |
| Strong on what not to do, thin on what to do. All three sessions said so independently; ten of one painting's eighteen rehearsals went on finding procedures the guide had none of. | **`RECIPES.md`**, collected out of the painters' own pass scripts rather than composed: a plane, a form that turns, a mass built of planes, a glow, a passage brightening one way, a quiet gradient, a small irregular mark, a small round thing, a tapered arc, the one ruled line, a lost edge, a mark across a boundary, a hollow thing, a repair with things standing on it. Each with what it looks like when it goes wrong, and noun-free. |
| There was no end-to-end worked example, and `paintings/` — which is one — was pointed at from `README.md` and deliberately not from the guide. | The guide points at it **with the decide-then-read condition attached**: if you chose your subject before opening the repository these are yours, and if you did not, they will choose for you. `PAINTINGS.md` and `README.md` say the same in the same words. The condition is the protocol in `LESSONS.md`, which makes it checkable rather than a matter of taste. |
| `PAINTINGS.md` said all three paintings were made having read nothing but the guide. Two of them had read three and five other files. | Corrected, per painting, with what each read and what that means for reading their agreement. |

**Four items are not rowed above because they were answered somewhere the table cannot
show.** A round tip's dotted fringe on a small shaped mass and the missing
`load_falloff` clause were both absorbed by engine changes — `edge="clean"` and
`cover()` — and their paragraphs left with them, which is the growth rule's preferred
outcome. *Painting without a reference* became a section of its own, built round
`compare({place: value})`. And one item was a question rather than a request — **does
the pencil apply with no reference?** — answered *yes, in one line*, and narrowed by the
asker's own doubt: the line does not claim a drawing can be *checked* without a
reference, only that the pencil is free and a drawing is still the cheapest place to
find out that the proportions in your head do not fit the canvas, which you can see the
moment it is down. That is the half of the pencil that survives having nothing to
compare it to.

### What the greenhouse sessions asked of the documentation

| Gap | What was done |
|---|---|
| No recipe for a **volume of lit air** — a beam, a shaft, a halo seen from outside — as opposed to *a passage light in the middle*, which is light on a surface. Reached unaided by three paintings. (Fable) | *A volume of lit air*, in `RECIPES.md`: the glaze mixed close to the field in value and hue, laid with the soft round tip along the axis, tapered by pressure so it is narrow and bright at the source and wide and gone at the far end — the painter's own three calls, rendered and looked at before they were written down. It earns the one place the guide warns off that brush, and it says so. |
| No recipe for a small **compound** object — a container plus something growing from it, in three marks or fewer; the pots read as fruit. No working calls to propose. (Sonnet) | *A small container with something spilling from it*: the other painter on the same subject had it — one chisel mark for the body, a wider lighter chisel mark for the rim, one starved stroke for what spills — and the failed version is named beside it, because a round taper for the body is the natural first attempt and reads as a bulb. Rendered side by side to check that it does. |
| *A mass built of planes* does not say **when** the tiling is decided: designed before the block-in the tower turned; invented in the pass the rock became the weakest passage. (Opus) | One clause in the recipe — *draw the planes with the silhouette* — and one line in step 1, with the failure it predicts named as the one the recipe already names, one level up. |
| *Look every 5 to 15 strokes* is written for the held Python loop; under `easel run` the atom is a pass. (Fable) | One paragraph under *The one habit*: the count is for a held session; under `easel run` the habit is *rehearse before every pass, look after it* — and now, read the check `run` prints beside the budget line. |
| An exercise calibrates value; none calibrates hue, where the mixing surprises live. (Fable) | A ninth exercise, the swatch strip: every planned mixture laid side by side before the first mass, printing value and chroma for each. In the guide and in `examples/exercises.py`. |
| `scumble`'s auto-size on a wedge: the sentence beside *leave size off*. (Sonnet) | In *a quiet gradient*, with the number, beside the warning the verb now gives — and one more finding the same painter's probe left: a `flat` scallops a wide band at `0.11` peak to peak against `0.03` for a solid block-in, measured on the committed painting. |
| The chisel staircase: a row in *the shape each tool leaves behind*, repair beside it. (Opus) | The row, the paragraph, the measurement and the repair — see the engine table. |
| Composition is the one thing painters need with no procedure. *Eventually a few `RECIPES.md` entries collected across paintings, not a `PAINTER.md` section; cannot be written from one painting.* (Opus, opinion) | Two entries, collected from four paintings' notes rather than composed: *a subject that is one thing against a ground* (the bands crossed twice, the ground cut to a wedge, the horizon found late, and *two things that both want to be the subject* folded in from the car wash) and *a picture with an empty half* (the counter-beam, and the corner left empty on purpose). Marked in the file as the least certain things in it. The third entry the painter named has one instance on record and is a sentence rather than a recipe. |

**Two lines of evidence the same painters logged as working as intended** stay where the
register put them: `cost()` catching a bent `ribbon` at 141 of 340 before a stroke was
spent, and two correct, already-written rules failing anyway — a plan's place going stale
when its silhouette moved, and the pressure list on a chisel. The second is now a
warning and a rule of the check, which is the answer both arguments were making.

---

### What the eighth session asked of the documentation

| Gap | What was done |
|---|---|
| **The two glow recipes cannot be told apart at the moment of choosing.** *A passage light in the middle* and *a volume of lit air* are the right pair, and the sentence that separates them — *an inward scumble is a bloom **on** something* — sits inside the second entry, where it is read by a painter who has already chosen correctly. Four sessions have now reached the glaze answer the hard way, and one of them had the recipe open. | The index says *on a surface* against one and *in a medium* against the other, which is the one place in that file with room for a distinction rather than a procedure, and the first entry now says it outright with the second linked from it. |
| **`compare({place: value})` is unreachable from the method file.** `PAINTER.md` step 3 teaches the plan as printed numbers; the pairs question lives in `PAINTING.md` and `REFERENCE.md` carries the signature without the reason. This session wrote a nine-value plan, checked the separations by hand, satisfied itself, and still shipped a coping that reached the subject's own value. | Two lines in step 3: put the plan itself through `compare({place: value})` on the empty canvas and read the pairs. Run on this session's own plan, before a mark, the sheet reports nine pairs inside `0.10` — the coping against the near deck among them, which is the fault it found at stroke 137 with `sample()`. |
| **No preset ground suits a low-key picture, and the guide's ground advice is silently wrong for one.** The lowest preset is `umber_wash` at `0.425`; this session took `cool_grey` at `0.53`, after which every dark mass had to be laid `solid=True` to cover it — which cost strokes, removed the ground breathing through, and left the deck repaint as the one mass it had to lay twice. The fourth session solved this and wrote the reason only in its own notes. | One sentence under *Getting started* where the presets are listed, with both numbers re-measured: `umber_wash` reads `0.425`, `cool_grey` `0.536`, and `Session(ground="#5a5045")` reads `0.320`. The mechanism was always there, since a ground takes any colour; what was missing was a rule pointing at it. |
| **A painter placing marks *inside* a shaped mass needs point-in-shape constantly, and nothing says so.** This session hand-rolled edge-intersection arithmetic about fifteen times to check that a ripple, a lamp or a glaze fell inside its pool, with `shape.contains(x, y)` listed in the file it had open. | A block in `RECIPES.md` where small marks are laid into a larger mass, with `contains` for one point and `inside(xs, ys)` for a scatter of them — and `inside` added to `REFERENCE.md`, where only `contains` was listed. A list of methods answers *what exists*; it is read once at the start rather than at the moment a mark is placed. |
| **The worked examples may prime toward one kind of picture.** Three of the four finished paintings are low-light scenes with a single light source, and most of the guide's illustrative passages are drawn from them. The named-subject priming is measured and guarded against; this is not. (**Opinion, unmeasured, and offered as one.** This session chose a low-light subject before opening anything, so it is a data point for the hypothesis and cannot test it.) | **Nothing, which is what it asked for.** The measurement it wants is a brief written for a high-key or flatly-lit subject, before anyone reads `paintings/` — the protocol the subject rule already uses — and that is a session's work rather than a release's. It is the one item on this page closed by agreeing that it cannot be acted on yet. |

**And a rule left the front page, which is the growth rule paying for itself.**
`PAINTER.md` is held to 10,000 words and the two items above did not fit; the standing
answer is that a rule the engine checks at the call can leave the guide, and none had.
*You will under-vary your marks* is the first: the post-pass check names both halves of
it after every pass, with the numbers attached, which the paragraph could not do. It is
in `PAINTING.md` now, moved rather than cut, and whether a rule can safely leave is a
question the next session can answer — which is the point of moving it.

### What the ninth session asked of the documentation

Ten items across the two paintings. Four of them are the same complaint the eighth
session made, refiled because the second instance was stronger; three are about the
*pencil*, which eight of ten paintings in this repository have never used, and the
session filed those as candidate diagnoses rather than as fixes. Two of them are
about how a **run** is configured rather than about a file, and are in `LESSONS.md`
with the protocol.

| Gap | What was done |
|---|---|
| **`compare({place: value})` is unreachable from the method file** — the eighth session's item, refiled because the second instance is stronger. Doing all of step 3 was not sufficient: thirteen values planned as numbers, `value_of` printed for each, the swatch strip laid — and the plan still had its two largest masses at `0.00` apart, meeting along the entire far edge. Step 3 teaches the `0.10` threshold as a property of *a mixture*, and the thing that fails is a property of *a pair that touches*. | The eighth session's two lines landed in 0.3.0; this adds the clause it did not ask for. Step 3 now says the threshold is about two masses that **meet**, which a column of numbers cannot show — and names both painters. The `0.00` pair is the one `Comparison.pairs` reports on the empty canvas before a stroke. |
| **`RECIPES.md` has no entry for the biggest mass in the picture.** A sky, a far field, a sheet of water at a grazing angle is not *a quiet gradient* (a band between two masses), not *a passage brightening toward one side* (a passage inside one), and not *a passage light in the middle* (a bloom). This session laid three and got one right — the one it handed to the verb. (Observed.) | *A graded field that is most of the picture*, collected from **three** paintings rather than the two the request expected: a night sky and a wet road, a dawn sky, and a flooded lot that is one graded field top to bottom. Four ingredients, and the measurement the request did not have: `load=1.0, load_falloff=0.0` is not the verb's default on a band, and without it `0.9%` of an eleven-pass field comes back within a hair of bare ground against `0.0%` with it, with the ripple dropping `0.0021` → `0.0008`. The crossers are in the recipe rather than in the composition advice, because a graded field with nothing crossing it *is* a band. |
| **Depth order failed in a new shape: a late atmospheric pass is a mass at a depth, and does not feel like one.** Back to front held for every mass in this painting. What broke it was the dawn band — laid last because it is *light*, and laid over the far trees, the pole and the bird's head. `LESSONS.md` has the depth paragraph down as needing a rewrite after three failed runs; this is a fourth and it is not the same one. (Observed.) | The sub-case named in step 2, as one more of the three things that follow from back-to-front: **a veil of light is a mass at a depth**, and asks the same question. `look(diff=True)` is named there too, which is the instrument the request said was unreachable from the method file. Not a rewrite of the depth paragraph — that is still open in `LESSONS.md` and is still a design job with a measurement attached. |
| **`sample()` over a `cell()` averages the background in with the mass, and reads like a measurement.** Checking whether the bird's dark had landed, this session sampled `F5`, read `0.449` against a planned `0.30` and the trees at `0.336` against `0.20`, concluded the engine was laying everything `0.14` light, and wrote a second probe to find out why. The cells contained water and sky. (Measured, after the fact.) | One clause in `REFERENCE.md`, one in `PAINTING.md`, and the paragraph in `sample`'s own docstring — with the mechanism reproduced on a clean canvas, where it is sharper than the session's own case: a bird planned at `0.30` standing in water at `0.50` reads **`0.501`** by its cell, `0.327` by its own shape and `0.318` by a region cut inside it. The remedy the request proposed was *a region inside the mass*; the better one is **the mass** — `sample` already averages a shape over itself, and the mass you blocked in is a shape you already have. And the rule of thumb it asked for: a number that disagrees with `at_value` by more than a hundredth is almost always the place. |
| **The guide sells the pencil on being free, and a rehearsal is free too.** *The pencil is free and does not count against the budget* is true and does not distinguish the two, so a painter who has internalised *rehearse everything* reaches for the rehearsal — which happened here, five times in sequence on one bird's head. The property that distinguishes the pencil is that it is **parallel**. (Observed, and the painter's own account of its reasoning.) | The clause, where the pencil is introduced in step 1: *a rehearsal shows you one answer; a pencil shows you six at once* — and the sentence it displaces is the one that sold it on being free, which is said again two screens later where it is load-bearing. |
| **`The drawing` is written entirely around a reference, and the painter without one is sent straight to it.** Every mechanism in that section assumes two panels; a painter with nothing to compare against finds one sentence addressed to them, and nothing that says how to draw a *feature* — which is where both of this session's paintings spent their most expensive rehearsals. | *Without a reference*, a sub-section of `The drawing`: the same loop with the points checked **against each other** rather than against a photograph, `look(region=, grid="fine")` with no `reference=`, and the parallel-pencil loop written out as three candidate silhouettes in one call with `erase(region)` taking back the two you did not want. `compare({place: value})` is named as the precedent for the whole asymmetry, which is what it is. |
| **The pass-script convention quietly makes the pencil a one-off.** `paintings/` teaches numbered pass scripts, the drawing becomes `p1_draw.py`, and once it is pass 1 it is finished — while the guide's order wants the pencil *after the far masses are down*. Both of this session's paintings put all their graphite in pass 1, on bare ground, where the first block-in buried it. (Observed across the paintings' scripts.) | Verified and stated where the convention is taught, in `PAINTINGS.md` under the rules the paintings were made under: name the second drawing pass before you need it. Counted rather than remembered — **seven of the ten paintings drew no line at all and nine placed no landmark**; `pool_night` is the only one that redrew mid-painting and the only one with landmarks in it. (The register's *six of nine* counted before the second heron became a painting of its own; the shape of it is unchanged.) |
| **Six of the nine paintings on this page used no pencil at all**, and the sub-cell precision method — `mark` → `pt` → pencil → `grid="fine"` → paint — is the guide's answer to the thing painters are worst at. *This is the largest untouched thing on the page and it needs a diagnosis before a fix; which of the three candidates is right is a question for a run, not for this table.* | **Taken at its word.** The three candidates above are each a documentation fix and each is made, because each is correct on its own terms whatever the diagnosis turns out to be. What is *not* done is picking between them, which needs a painter working from a guide that carries all three. The count is re-measured and in `scripts/probe_heron_session.py`, so the next round can say whether it moved. |
| **`DIAGNOSIS.md` worked as a recognition aid and never once as a lookup**, in 293 strokes and about forty rehearsals: five rows recognised on sight and repaired from the remembered description, **zero pointers followed** though following them was permitted. The recalled version has no measurement attached, which is the whole difference between the index and its targets. *The honest proposal is to measure the grep arm before changing the file.* (Observed, n=1, and the only n there is.) | **Not changed on n=1, as asked.** It is a question for the protocol now: `LESSONS.md` says to hand the index as a file to **grep** and not to read, and to record which it was. One sentence in the file itself, which is an instruction rather than a sixth copy of the guide: *follow the pointer; do not work from the row*, with what that cost this session. **And the arm is moot since G5**: `easel diagnose <what you can see>` matches the rows and prints the passage, so grep-and-then-open is one call, and the file ships in the wheel -- which it did not when this was filed, so a package-only painter had nothing to grep either way. What is still open is whether a painter reaches for it unprompted, which is in `LESSONS.md` with the protocol. |
| **Four of the rows most relevant to a restricted painter point into files that arm does not have** — including *two masses you planned as different that read as one*, which lands in `PAINTING.md` and is exactly this session's worst fault. A pointer into a file you were not given is worse than no row. *A property of how a run is configured rather than of the file.* (Observed.) | In `LESSONS.md` with the protocol: either ship the index only with the files it indexes, or say in the run's own instructions which files the painter has, so a row naming one they do not have reads as a prerequisite. And one clause in `DIAGNOSIS.md`: **a row naming a file you were not given is not for you**. |

**One composition note, recorded as a single instance rather than acted on.** The
guide says to count the horizontal bands and then find something that crosses them,
*or a viewpoint that is not square on*. The second painting took a stronger version —
a viewpoint steep enough that **there is no horizon in the frame at all** — and the
band problem did not arise. One painting, so it stays a note; if a second wants it, it
belongs beside *a subject that is one thing against a ground*.

**And one measurement the session tried and discarded, which did not survive being
re-measured either.** It reached for the across-band ripple from *The band, and the
brush that closes its joins*, got an answer the wrong way round, and put the
mechanism down to canvas texture on a `rough` ground. **It is not the texture.**
Measured on one solid scumble read through five windows, the number is identical on
`smooth`, `linen` and `rough` to four decimals — and on a *starved* pass `rough`
reads `0.0011` against linen's `0.0031`, lower rather than higher. What the metric is
sensitive to is the **window**: `0.0008` across the full width, `0.0016` through the
`0.13`-wide column this painter used, `0.0020` through a `0.04` one — two and a half
times the number for the same paint. The clause the session asked for is beside the
table, and it says to read both passages through the same wide window.

---

### What the install session asked of the documentation

Two items, and they are the same distance measured twice: between naming the guide and
being able to reach it.

| Gap | What was done |
|---|---|
| **The package docstring named the file and not the route.** *If you are new to the engine, read `PAINTER.md`* — a filename, with no path, no accessor and no command beside it, handed to a reader whose `import easel_paint` has just failed and who is therefore already in the mood to search a filesystem. Which is what the session did. The README's heading aimed at exactly this reader has the same shape, and sent them to a web link for a file already on their disk. (Observed, at the cost of the session's first ten minutes.) | The docstring now names the call — **`easel.guide.front_page()` here, or `python -m easel guide` from a shell** — and says *the guide* rather than the filename. `python -m easel` rather than `easel` because the console script is not on `PATH` in every install: this session's was in a `Scripts/` directory that was not, and pip had said so in a warning at install time that nobody reads.. The README's agent section now says the same thing in one line before its links, because the reader who needs it is the one who has already installed the package. |
| **A stale editable install reproduces a fixed bug forever, and nothing on this page said so.** The freeze is pip's behaviour, not this package's: `dist-info` is written once and the `.pth` serves live code for every commit after, so `pip show`, the PyPI README and `easel.__version__` can disagree by any number of releases with none of them wrong. A checkout installed before 0.3.0 serves its owner the guide-less README until somebody reinstalls. (Observed on this repository's own machine, at 0.1.0 over 0.4.0.) | Written down here, which is the whole of what was available — there is nothing to fix in the engine. What it changes is what a *report* means: **a session reporting a missing document should be asked for `easel.__version__` and `pip show easel-paint` before any file is opened**, because those two disagreeing is the signal, and this entire round would have closed in a minute by asking. |

---

## The two questions, and their answers

**On the guide's length.** Every session says it is too long and every session credits
the essay. What should be done with it?

**Stop shrinking it, and split by function instead.** The cost of length is not reading
time — one session's whole read cost a few minutes and about thirty thousand tokens,
against far more spent looking at its own rehearsals. It is that a rule read once at the
start is not in the hand at the moment it applies, and cutting cannot fix that, because
the rule cut is the one some painter needed. So: the split, a CI-held budget on the front
page, and the standing rule that a finding goes to the engine, the recipes, the reference
or the calibration file and never adds a paragraph to `PAINTER.md`. All four are done and
written into `LESSONS.md`.

**The budget landed at 10,000 words rather than the 5,000–6,000 asked for**, and that is
the one place the answer differs from the request: the figure was never costed against
the contents the same list wanted kept — the order of work, *What you are bad at*, the
checklist and the exercises come to about 8,500 words on their own. A budget nobody can
meet on the day it is written enforces nothing. The honest claim is halving.

**The split was a hypothesis and both arms have been run** — see *The eighth session*
above, where the third painter's prediction (*the restricted arm paints the masses as
well and improvises worse*) held in its first half and did not, in the form it was
written, in its second: the deficit that arm showed was lookup rather than judgement.

**On a warnings file.** Would a separate file of the warnings a painter must keep in
context help?

**No, and it is not a close call.** The third session had every warning in context for
the whole painting — the guide never left its window — and laid a glow as a solid disc,
planes as slabs and a picture in almost nothing but two brushes regardless. The front
page lists the mistakes, the checklist repeats them, and `LESSONS.md` records that a rule
correct, well placed and repeated three times failed every run. A fourth copy is the
thing that file says does not work.

**What was written down instead** is where the idea went: a check the tool runs over the
pass it just painted, printed beside the budget line, from inputs already in the log.
That is `Session.report()`, built in the greenhouse round, and in 0.3.0 the first rule
left the guide under it. The one form of the file idea with a real mechanism — a short
rules card kept where a `CLAUDE.md` is kept, which survives a context compaction where
the guide does not — is still unbuilt and still cannot be judged, because none of the
sessions has ever been compacted.

---

## What none of them would change

**Every session defended the same short list, unprompted, and none of it was touched.**
The order of work; no layers, no free undo, no black; the place vocabulary; the values
view, called *the one that tells you the truth*; back to front and the
inside-of-a-hollow-thing rule; the nine exercises, which cost two minutes and were repaid
inside the first pass; and the habit of putting a measured number behind a rule — *the
numbers changed what I did in a way the prose beside them did not*. Every row of *the
shape each tool leaves behind* has survived being measured.

**Three things are defended above the rest, by every painter that names any:**

- **Rehearsal seeded as the next real strokes.** It is where the failures happen, at a
  cost of nothing. A glow that came back a sun, foam that came back a row of discs, a
  chartreuse searchlight, three flat slabs where a cylinder should have turned, a chisel
  staircase, ten pots that were ten bricks, a staircased pool, a scumble that came back a
  contour map, a scumble that buried four fingers whole, four white discs at the focal
  point, a bowl three times too light. Counts, where a session kept them: 56, 92, about
  40, and the hands session's **114 against 28 committed passes**. No painting on this
  page has a repainted mass it rehearsed first. The tenth painter: *the single best thing
  here, and it's not close.*
- **`at_value`.** Asked for nine, nineteen and about twenty-five planned values in
  different paintings and landing every one to the hundredth, including those approached
  from above — and **raising** rather than clamping when the value is under the floor,
  which two sessions named as the right behaviour unprompted.
- **`compare({place: value})`.** It carried whole pictures with no photograph to lean on,
  and finished their places inside `0.10`.

**What individual sessions added.** `cost_line` naming the lever rather than only the
price, which turned a 130-stroke foliage pass into 38. The engine's refusals, called
*teaching errors rather than failures* — the glaze that will not be laid says how far the
paint under it can travel, and one painter says that ended the pass, the film not being
needed at all. The post-pass check, described as *a linter for painting that fires at the
moment you can still act*, and by a later session as the thing that taught it by naming
the mark: *that is one disc printed seven times*. And determinism, leaned on hard enough
to prove a finding with it: three independent clean rebuilds of one painting are
byte-identical.

**The two sessions with the least context defended the same list as the ones with the
most** — the eighth, which had three files, and the twelfth, which had the wheel and
nothing else. That is the part worth keeping: the core is not something a painter has to
read the whole corpus to arrive at.

---

## Where the arguments went

Six sessions' worth of reasoning, probe output and proposal text was cut from this file
when the work was finished. What was worth keeping outlived it:

- the measurements are in [`CALIBRATION.md`](CALIBRATION.md), each with what it was
  measured on;
- the rules are in [`PAINTER.md`](PAINTER.md), [`PAINTING.md`](PAINTING.md) and
  [`RECIPES.md`](RECIPES.md);
- the method that produced all of it, and the standing rules about how the guide may
  change, are in [`LESSONS.md`](LESSONS.md);
- the paintings, their notes and their pass scripts are in
  [`paintings/`](paintings), read from the outside in [`PAINTINGS.md`](PAINTINGS.md);
- each engine item has a test in `tests/test_requests.py`, named for the request, and
  the probes behind the third, fourth, greenhouse, eighth, ninth and tenth rounds are
  `scripts/probe_third_session.py`, `scripts/probe_fourth_session.py`,
  `scripts/probe_greenhouse_session.py`, `scripts/probe_pool_session.py`,
  `scripts/probe_heron_session.py` and `scripts/probe_tenth_session.py`, with the
  painters' own probes beside their paintings under
  `paintings/Claude/lighthouse_greenhouse/` and `paintings/Claude/heron_lot/`;
- the releases are cut by version in [`CHANGELOG.md`](CHANGELOG.md), which is where to
  look for *which defaults moved*.

**Thirty of the painters' own claims have been re-measured before anything was built on
them, and eight did not survive.** All eight are recorded above where the fix is — the
clean contour spilling further than the ragged fill it replaced, the smudge on a slope
that turned out to be a smudge on a bend, the rendered view that turned out not to lift
a solid mass at all, the bare boundary at `overhang=0` that turned out to be the comb
and the brush running dry, the direction sequence that turned out to be priced as a
sum rather than at its steepest angle, the `rough` ground that turned out not to be
what a ripple metric was reading, the `size` threshold that turned out to be a
pixel threshold, and the sampled spread whose two populations turned out to overlap.
That is `LESSONS.md`'s *check the painters' numbers* working as intended, and it is
worth noticing **what kind** of claim fails it: six of the eight were reported as
*observed* — a rehearsal showed it plainly, no number was taken, and the painter
reasoned back to a mechanism that sounded right. The nine from the greenhouse round all
held, and two held with the wrong mechanism attached — the pencil that "advances the
stream" advances the log index, and the undo that lost "the stream or the wet layer" was
losing the stream *and* the log's precision. A claim that survives is usually worth more
afterwards, because the re-measurement says what it is really about.

**The sharpest case the page has is the one the painter called on itself.** The eighth
session labelled its own mechanism *observed and offered as a guess, which this page's
own record suggests is the half most likely to be wrong*, and it was; its three costs
reproduced to the stroke, and the ninth session settled the mechanism against it. Every
round since has arrived with that labelling done, which is what makes the re-measurement
cheap: it says where to look first.

**And two of the eight were neither observed nor guessed: they were measured, and the
measurement was not general.** *A warning when an oriented tip is handed a `size` under
about `0.008`* came with a table behind it and still had to be rebuilt, because the
table was taken on one canvas and the threshold is in pixels — the same `size` is 2.4px
on a 300px canvas and 9.6px on a 1200px one. The hands session's *the two populations do
not overlap* is the same shape one round later: four places on one canvas, every number
of which reproduces, and the separation between them vanishes at 226 places on two
paintings — with a mass handed in whole, which is the remedy the warning names, landing
on the wrong side of the line. **A measurement is only as general as the conditions it
was taken under**, which is the rule at the top of `CALIBRATION.md` arriving from the
other direction: it asks every number to state what it was measured on, and this is what
happens when a number states it and the *proposal* forgets. Both were built, neither as
asked, and in both cases the thing that fixed the proposal was measuring the *same*
claim over more of the same kind of thing — which is cheap, and is now the habit.
