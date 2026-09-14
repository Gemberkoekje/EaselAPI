# What the painters asked for, and what was done

Eight sessions painted a picture from the guide and then wrote down what the engine and
the documentation had cost them, a synthesis pass gathered the points more than one of
them raised, and the repository's owner put two further questions to the third painter.
This file is the register: **what was wrong, and what was done about it.**

**Everything in the tables below is done — except the last two rounds, which are open
and say so** — 42 engine items and 50 documentation items closed, and 3 engine and 5
documentation items open from the eighth session, 4 engine and 10 documentation from the
ninth. The long arguments that produced each
one have been cut, because a request list is worth keeping only while somebody still has
to act on it. What survives is the
finding, because a finding is still true after the fix, and the handful of places where
the answer differed from the request. The last three sessions painted one shared
subject; their lists were deduplicated into one round, and every number they took was
re-measured before anything was built on it.

**Done is not the same as right, and five times now it has meant *measured and there was
nothing to fix*.** An engine item has a test behind it. A documentation item is a
hypothesis until a fresh session paints against it, which is the rule
[`LESSONS.md`](LESSONS.md) opens with and the reason every line below says what was
changed rather than that it worked.

| Where the items came from | Engine | Docs |
|---|---|---|
| First session — a still life, 224 strokes, `paintings/windowsill_pears/` | 12 | 12 |
| Second session — an interior, 206 strokes of 300, `paintings/car_wash/` | 7 | 8 |
| Third session — a landscape at dusk, 184 strokes of 300, `paintings/lighthouse_dusk/` | 6 | 9 |
| The synthesis across all three, and two questions from the owner | — | 8 |
| Fourth session — a night street, 286 strokes of 300, `laundromat_night/` | 6 | 5 |
| Fifth–seventh — one subject, three painters, `lighthouse_greenhouse/{sonnet,opus,fable}/` | 11 | 8 |
| Eighth session — a pool at night, 221 strokes of 300, `paintings/pool_night/` | 3 open | 5 open |
| Ninth session — a heron in a flooded lot at dawn, 293 of 320, `paintings/heron_lot/1/` | 3 open | 6 open |
| …and its second attempt at the same subject, 253 of 320, `paintings/heron_lot/2/` | 1 open | 4 open |

Only the first session is a clean measurement of the guide on its own; the second read
three other files first and the third read five. Where they agree, that is painters
finding the same thing with increasing context. Where they disagree, it may be the
context talking.

The fourth read four — `PAINTER.md`, the exercises, then `PAINTING.md`, `RECIPES.md` and
`REFERENCE.md`, in that order — and never opened `CALIBRATION.md` at all, which is worth
knowing before trusting any of its numbers: where a calibrated figure would have settled
one of its findings, it measured the thing again itself instead. It also read
`paintings/car_wash/prelude.py` and `p0_plan.py`, and nothing else under `paintings/`.
So it is the most-read session but not the widest-read one, and its agreement with the
third should be discounted accordingly.

The eighth read **three** — `PAINTER.md` with its nine exercises, then `RECIPES.md` and
`REFERENCE.md` — and nothing else: not `PAINTING.md`, not `CALIBRATION.md`, nothing
under `paintings/`. It is the split test's other arm, and the only session on this page
whose items were raised without the essay or the numbers to check them against.

The ninth read **four** — the eighth's three plus `DIAGNOSIS.md`, which did not exist
when any earlier session painted. It is therefore the restricted arm again with the
symptom index added, and the **only data point that exists on whether that index
works**. It was told it could follow a `DIAGNOSIS.md` pointer into a withheld file and
read the area named; it never once did, which is its own first finding.

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
in the log. `Session.report()` is it, `easel run` prints it after every pass
(`--check` widens it to the painting, `easel log --check` reads it cold), and the MCP
`run` tool hands it back. Six rules, every one met by a real pass of a real painting:
*one brush at one size* for a whole pass of two or more calls; *a stack of passes at one
angle*; *a bristle under `size=0.025`*; *small marks before the masses are down*; *a
pressure list on a short chisel mark*, which the greenhouse painters added; and *the
subject's share* of the marks so far, against the plan's number when it is given. The
rule the fourth session proposed and this page dropped — a solid mass whose planned
and rendered values differ — is still not in it, for the reason given then: the gap is
`0.000`. The seventh rule the greenhouse round added, a shaped mass at the default
direction costing over 2.5× its axis, needs the shape and fires at the call instead.
Every rule that becomes a check can now leave the guide, which is the growth rule
paying for itself; none has left it yet, and the check has now had its first outing
against a session that had never seen it — see the eighth session below, where it fired
on twelve horizontal passes in the painting's very first mass, on a bristle under
`0.025` four times and on pressure lists on a chisel tip twice, and every one of those
was acted on in the rehearsal it fired in. What it has not yet shown is that a
rule it holds can safely leave the guide, which needs a session painting against a guide
the rule has left.

### The greenhouse sessions: three painters on one subject

One brief — a lighthouse mid-conversion into a greenhouse — was written down before any
of the guide was read and handed to three painters unchanged
(`paintings/lighthouse_greenhouse/{sonnet,opus,fable}/`). Their suggestion files sit
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
municipal pool at night lit from underwater, `paintings/pool_night/`, **221 of 300 strokes**,
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
   `paintings/lighthouse_dusk/NOTES.md` records reaching twice. Both entries were in the
   file it had; the sentence that separates them is inside the second one. Its written
   critique called this a gap in the engine, which was wrong, and it said so once it had
   read the other painting.
2. **It could not know which numbers existed.** `PAINTER.md` points at
   `CALIBRATION.md` *"when a rehearsal is about to be spent finding a number that is
   already in there"* — an instruction that requires knowing the number is in there.
   Three it spent rehearsals on instead: a glaze's strength being distance in **hue** as
   well as in value, met as an orange sign's reflection that was a solid bar at one
   opacity and invisible at the next, which is the two-opacity failure the file already
   records; `opacity` not quieting a scumble, which is the fix it eventually found for a
   contour-ringed glow by narrowing the two colours' span, and believed it had invented;
   and `inset()` by half the brush to hold a mass off its neighbour, which it re-derived
   as a hand-shifted polygon edge on one side only.
3. **It never ran `compare({place: value})` on the empty canvas.** This is the expensive
   one. Its worst structural fault — the coping reaching `0.50` against water at
   `0.45`–`0.55`, the frame as bright as the subject — is exactly what the pairs
   question exists to ask, and it was found at stroke 137 with `sample()` instead.
   `REFERENCE.md`'s one-line entry was read and not acted on; *Painting without a
   reference*, where the reason lives, is in `PAINTING.md`.

**So the essay's contribution to this arm was one section, and it is a section about a
tool rather than about judgement.** Of what the session could name as saveable —
roughly twelve to fifteen rehearsals and about twenty-five committed strokes, the latter
almost all one repainted deck — **the largest single item is not in the essay at all.**
It is in `paintings/laundromat_night/NOTES.md`: a custom ground at `0.32`, and the
reason, *no preset goes below `umber_wash` at `0.425`, which is far too light for a
night picture*. The eighth session took `cool_grey` at `0.53`, knew by its third pass it
was wrong, and talked itself out of a restart that would have cost 21 strokes.

**What this arm cannot answer.** The painting is timid. Six of its twenty-five passes
exist to take something back rather than to put something down, four of those in the
last third; it stopped at 221 with 79 strokes in hand, and its own verdict is that the picture is illustrative rather than painterly —
that the coping is four bands generated from a normal vector and a for-loop, and that
the one passage it likes is the one where a starved bristle did something it had not
designed. Whether that is the missing essay or this painter is not separable from one
run, and the run is n=1 against six of the other arm. **The honest claim is narrower
than the prediction: the deficit this arm showed was lookup, not judgement** — and two
of the three lookups were in files the split does not vary.

**One claim this session made that did not survive its own reading.** Before being shown
the withheld files it wrote that the guide's repetition "seems not to have noticed its
own cost", and `LESSONS.md` opens with the measurement that a rule correct, well placed
and repeated three times still failed every run. Fair as a description of reading it,
wrong about the cause — which is the same shape as the four re-measured claims at the
foot of this page: an observation reasoned back to a mechanism that sounded right.

### What it asks for, and none of it is done

**This is the first round on this page that is open.** It is filed rather than held
back, because the session that raised it is the split test's other arm and these items
are worth reading beside the account above. Each says whether its numbers were
*measured* or *observed*, which the foot of this page says is what decides which claims
survive re-measurement — and one is offered as an opinion with no measurement at all,
marked so.

| The engine | What is proposed |
|---|---|
| **A glaze's usable opacity is a function of its distance from the field, and there is no instrument for it.** `CALIBRATION.md` measures the problem — at `0.14` a film moves the value `0.087`, within a hundredth of the `0.10` that makes a new mass, and at `0.05` the underlying hue is already dead — and the guide's answer is *mix the glaze close, then choose an opacity*, which is a two-step search run by rehearsal. Six of this painting's rehearsals went on it, and one glaze was rehearsed three times and dropped. (Measured by the file; the cost observed here.) | `glaze(points, color, to_value=0.62)`, solving for opacity the way `at_value` solves a mixture for a value. `at_value` is the single most defended thing on this page across seven sessions, and the same instrument does not exist for a film — which is the other place a painter aims at a value and cannot hit it. |
| **The inward `scumble`'s usable `n` is bounded by the patch, and the verb warns from only one side.** The brush is `3 × depth / n` and the post-pass check's comb floor is `0.025`, so `n ≤ 120 × depth`: on a patch shallower than about `0.07` there is no `n` giving both enough rings to avoid contour banding and a brush that is a brush. This session met it at `n=12` on `depth=0.075`, read the resulting bristle warning as an unrelated complaint, and spent two further rehearsals. (Arithmetic exact; the banding observed.) | The verb says when the brush is too *wide* for the patch and nothing when the patch cannot carry the `n` asked for. It should say so from the narrow side too — and where no `n` fits, name *a volume of lit air*, which is what lays it. |
| **`direction=` given a sequence is priced far above any single angle in it.** Measured on one mass, same brush, same density, same call: `"axis"` **4** strokes, a single `-17°` **7**, `"cross"` **15**, a ten-angle sequence **51**. `cost()` gives the number and nothing gives the mechanism; the greenhouse round's 2.5× price walk fires on `direction` *left off*, not on a sequence. (Costs measured. The mechanism — that the stack is sized for the steepest angle in the list — is **observed and offered as a guess**, which this page's own record suggests is the half most likely to be wrong.) | Either the price walk covers a sequence, or one row in `CALIBRATION.md` under `block_in`. The guide tells a painter to vary direction between passes to break a comb, so a painter following that advice reaches for the sequence first; `"cross"` at 15 was the affordable answer and nothing pointed at it. |

| The documentation | What is proposed |
|---|---|
| **The two glow recipes cannot be told apart at the moment of choosing.** *A passage light in the middle* and *a volume of lit air* are the right pair, and the sentence that separates them — *an inward scumble is a bloom **on** something* — sits inside the second entry, where it is read by a painter who has already chosen correctly. Four sessions have now reached the glaze answer the hard way, and one of them had the recipe open. | One clause in the first entry and in the index table at the head of `RECIPES.md`: on a surface, versus in a medium. The index is where a recipe is chosen, and it is the one place in that file with room for a distinction rather than a procedure. |
| **`compare({place: value})` is unreachable from the method file.** `PAINTER.md` step 3 is where the value plan is made and it teaches the plan as printed numbers; the pairs question lives in `PAINTING.md`, and `REFERENCE.md` carries the signature without the reason. This session wrote a nine-value plan, checked the separations by hand against the `0.10` rule, satisfied itself, and still shipped a coping that reached the subject's own value — the exact failure the pairs table was built for. | Two lines in step 3 beside *plan those three as numbers*: run it on the empty canvas, and read the pairs. It carried three pictures with no photograph for the greenhouse painters, and the arm without the essay never ran it once. |
| **No preset ground suits a low-key picture, and the guide's ground advice is silently wrong for one.** *Start on a toned ground, not white* is right for a mid-key picture. The lowest preset is `umber_wash` at `0.425`; this session took `cool_grey` at `0.53`, after which every dark mass had to be laid `solid=True` to cover it — which cost strokes, removed the ground-breathing-through the same page values, and left the deck repaint as the one mass this painter had to lay twice. The fourth session solved this and wrote the reason only in its own notes. | One sentence under *Getting started*, where the presets are listed: a picture whose masses sit below the presets wants a ground of its own — `Session(ground="#5a5045")` — and `value_of` it before the first mass. The mechanism is already there, since a ground takes any colour; no rule points a painter at it. |
| **A painter placing marks *inside* a shaped mass needs point-in-shape constantly, and nothing says so.** This session hand-rolled edge-intersection arithmetic about fifteen times to check that a ripple, a lamp or a glaze fell inside its pool, with `shape.contains(x, y)` listed in the file it had open. Every mark laid *in* a mass rather than *as* one wants it, and this painting is mostly such marks. | A line where `RECIPES.md` lays small marks into a larger mass. A list of methods answers *what exists*; it does not answer *what you are about to need*, and the shapes list is read once at the start rather than at the moment a mark is placed. |
| **The worked examples may prime toward one kind of picture.** Three of the four finished paintings are low-light scenes with a single light source, and most of the guide's illustrative passages are drawn from them. The named-subject priming is measured and guarded against; this is not. (**Opinion, unmeasured, and offered as one.** This session chose a low-light subject before opening anything, so it is a data point for the hypothesis and cannot test it.) | Nothing yet. If the next brief is written for a high-key or flatly-lit subject, that is the measurement — and the brief has to be written before anyone reads `paintings/`, which is the protocol the subject rule already uses. |

---

## The ninth session: the restricted arm, with the symptom index

`PAINTER.md` and its nine exercises, then `RECIPES.md`, `REFERENCE.md` and
`DIAGNOSIS.md`. Subject chosen and written down before the repository was opened: a grey
heron standing in sheet-flood over a parking lot at dawn, `paintings/heron_lot/1/`, **293 of 320
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
  documentation table below, which proposes naming the sub-case rather than repeating the
  rule. `LESSONS.md` already has this paragraph down as needing a rewrite after three
  failed runs; this is the fourth, and it is a different shape from the other three.

**What the arm did well without the essay.** The masses again followed the method. The
picture's one structural strength — the far edge lost across the whole left half, sky
meeting water at `0.07` and under the reading threshold, with the trees picking the edge
up only on the right — came out of repairing a ruled horizon and off no document. Two
passages were abandoned rather than fixed after two rehearsals each, which is the
`paintings/` habit arriving without `paintings/`.

### What it asks for, and none of it is done

Two of the three engine items below are **measurements taken against an open item rather
than new complaints**, which is what this arm is for. Probes: `paintings/heron_lot/1/probe_seq.py`,
`probe_seq2.py`, `probe_band.py`.

| The engine | What is proposed |
|---|---|
| **A hand-rolled graded passage gets none of the protection `scumble` now has, and `RECIPES.md` teaches the hand-rolled form.** *A passage brightening toward one side* is six `stroke()` calls with sizes and offsets written out, and step 4 of `PAINTER.md` writes the scumble out by hand beside the verb. Neither says the thing the verb now knows: the brush has to be about three times the step or the passes read as bars. Measured **on this painting, against itself**: the sky, laid with `scumble(n=11)` and the brush left to the verb, sits at a uniform 4.0 steps and its across-band wobble is `0.037`; the dawn band, seven strokes with brushes chosen by hand, tapers 4.2 → **1.7** steps and wobbles `0.072` — twice as rough, same canvas, same painter, same pass structure. `1.7`–`2.5` is the middle of `CALIBRATION.md`'s own measured worst zone. (Measured.) | A rule of the post-pass check, which is where `LESSONS.md` says a rule like this belongs and whose bar it meets — it fires on a real pass of a real painting: **three or more long, roughly parallel marks from one call whose offset step is under about twice the smallest brush among them.** Every input is in the log. Failing that, one clause in *a passage brightening toward one side* carrying the number the verb already uses. |
| **`direction=` given a sequence lays a complete stack per angle, and `REFERENCE.md` says the opposite.** The eighth session filed the price and marked its mechanism — *the stack is sized for the steepest angle in the list* — as a guess. **It is not that.** The cost is the **exact sum of what each angle costs alone**, on all three shapes tried (wide 37/88/137, tall 36/85/134, concave 48/100/141; sum-of-singles 37/88/137, 36/85/134, 48/100/141 — nine for nine, to the stroke). In paint: `direction=[0, 90]` logs **7 passes at 0° plus 30 at 90°**. So `REFERENCE.md`'s *"or a sequence for one pass each"* reads as *n passes for n angles* and means *n complete stacks*. This session gave a treeline sixteen angles to break its comb, on the guide's own advice to vary direction, and was quoted **515 strokes against 22 for one direction — 23×, and 1.6× the whole budget.** Caught by `cost()` before anything was spent. (Costs and pass angles both measured.) | The wording first: *a sequence lays a full stack per angle and is priced as the sum of them*, in `REFERENCE.md`'s `direction` row and in `CALIBRATION.md` under `block_in`. Then the price walk, which today fires on `direction` **left off** — the same 2.5× test on a sequence would have caught this at the call rather than at the painter's own `cost()`. `"cross"` is two angles and is the affordable answer nothing points at. |
| **The check's bristle floor fired 28 times across the painting and was correctly ignored 28 times.** *A bristle under `size=0.025`* is right for a solid plane and wrong for what this painting is mostly made of: broken glints on water, grit under a flood, feather groups on a bird — marks where the comb's gaps at `load=0.25`–`0.45` **are** the mark. By the second half the painter had stopped reading that line, which is the risk `LESSONS.md` names from the other direction when it says a warning that cannot fire is worse than none. (Observed; the count is from the log.) | Narrow the condition rather than the rule: do not fire on a mark whose `load` is inside the run-out window `CALIBRATION.md` already publishes (`0.4`–`0.6` and below), where a starved comb is the intended mark. A check a painter learns to skip costs the other five rules their credibility. |

| The documentation | What is proposed |
|---|---|
| **`DIAGNOSIS.md` worked as a recognition aid and never once as a lookup**, in 293 strokes and about forty rehearsals. Read front to back — as this session was told to — it stops being an index and becomes recall: the painter recognised *staircase*, *venetian blind*, *floating discs*, *searchlight that owns the picture* and *paper cut-out* on sight, and then **repaired each from the remembered description rather than following the pointer**. Zero pointers were followed, though following them was permitted. The recalled version has no measurement attached, which is the whole difference between the index and its targets: the one fault it fixed properly, the chisel staircase, it fixed with `edge="clean"` while `CALIBRATION.md` holds a cheaper repair (a comb, plus one solid stroke down the middle) at the other end of the same row. (Observed, n=1, and the only n there is.) | The file's own instruction — *use it the other way round*, `grep -i` — is the right one and it lost to a reading instruction. If a run hands a painter the index, hand it as a file to **grep and not to read**, and record which it was; this session cannot tell the two arms apart because it only ran one. The sharper version: an index whose rows carry the *repair* as well as the pointer stops rewarding recall, but that is the fourth copy `LESSONS.md` refuses, so the honest proposal is to measure the grep arm before changing the file. |
| **Four of the rows most relevant to a restricted painter point into files that arm does not have.** *Two masses you planned as different that read as one* → `PAINTING.md` → *Painting without a reference*, which is where `compare({place: value})` lives and is exactly this session's worst fault. Also *a mixture that should have been a grey and came out green* (met, three times, on the swatch strip), *a glaze that is a stripe at one opacity and invisible at the next* (met, and the glaze dropped), and *a form shaded until it stopped separating from its background*. A pointer into a file you were not given is worse than no row, because the answer is visibly there and out of reach. (Observed.) | Either the index ships only with the files it indexes, or each row says which file it lands in **before** the painter follows it — it does name them, but as a destination rather than as a prerequisite. This is a property of how a run is configured rather than of the file, so it belongs with the protocol in `LESSONS.md`. |
| **`compare({place: value})` is unreachable from the method file** — the eighth session's item, refiled because the second instance is stronger. Doing all of step 3 was not sufficient: numbers planned, `value_of` printed for each, swatch strip laid, and the plan still had its two largest masses at `0.00` apart. Step 3's own text is what makes this survivable-looking — it teaches the `0.10` threshold as a property of *a mixture*, and the thing that fails is a property of *a pair that touches*. | The eighth session's two lines in step 3, plus one clause it did not ask for: the threshold is about **two masses that meet**, so the pair to check is not the two closest numbers but the two closest numbers **whose masses share a boundary**. That is the question `Comparison.pairs` already asks and the reason step 3's by-hand version does not catch it. |
| **`RECIPES.md` has no entry for the biggest mass in the picture.** *A quiet gradient* is a band between two masses; *a passage brightening toward one side* is a passage inside one; *a passage light in the middle* is a bloom. A sky, a far field, a sheet of water seen at a grazing angle is none of those: it is a graded field that is a third of the canvas, that must not read as a band, and whose joins are the picture's largest surface. This session laid three of them and got one right — and the one it got right is the one it handed to the verb. (Observed.) | An entry collected the way the others were: the verb over the whole field with `size` left off, a direction a few degrees off the frame so the passes do not parallel it, and the crossers named as part of the recipe rather than as composition advice — because a graded field with nothing crossing it *is* a band, however closed its joins. Two of the four paintings on this page have one. |
| **Depth order failed in a new shape: a late atmospheric pass is a mass at a depth, and does not feel like one.** Back to front held for every mass in this painting. What broke it was the dawn band — laid last because it is *light*, and laid over the far trees, the pole and the bird's head, all of which are in front of the sky. It was repairable only because `RECIPES.md`'s *a repair under things that are standing on it* had been followed from the first pass, so the three buried things could be re-run at their own depth for twelve marks. `LESSONS.md` has the depth paragraph down as needing a rewrite after three failed runs; this is a fourth failure and it is not the same one. (Observed.) | Step 2 names masses and hollow things. The sub-case to add is one sentence: **a glaze, a graded passage or a veil of light is a mass, and the question to ask of it is the same one — what is it in front of?** And the instrument that catches it exists and is unreachable from the method file: `look(diff=True)` after a pass, which `PAINTING.md` names in one clause under *Looking* and which this painter did not use once. |
| **`sample()` over a `cell()` averages the background in with the mass, and reads like a measurement.** Checking whether the bird's dark had landed, this session sampled `F5` and read `0.449` against a planned `0.30`, plus the trees at `0.336` against `0.20` — concluded the engine was laying everything `0.14` light, and wrote a second probe to find out why. The cells contained water and sky. A tight region inside each mass read `0.324` and `0.218`, which is `at_value` doing exactly what six sessions have defended. Two probe scripts and a false belief about the engine. (Measured, after the fact.) | One clause where `REFERENCE.md` and `PAINTING.md` introduce `sample` — *it averages what is in the place, so to measure a mass, hand it a region inside the mass and not the cell the mass sits in* — or `compare()`'s own advice applied one level down: a number that disagrees with `at_value` by more than a hundredth is almost always the place, not the paint. |

### The same painter, the same subject, a second time

After writing the critique above, the ninth session was shown the three withheld files
and then painted the **same subject again** with all of them in hand
(`paintings/heron_lot/2/`, 253 of 320, subject share 42% against a planned 40%). It is not a
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

### What the second painting adds, and none of it is done

| The engine | What is proposed |
|---|---|
| **A solid block-in lands short of its mixture, and under about four pixels it lands whatever was underneath.** Bare ground `0.394`, `density=1.0, solid=True, opacity=1.0, pressure="even"` — every clause of *a plane that is a plane* — a mixture at `0.865`, 600×600 linen: <br><br>`px:` 1.8 · 2.7 · 3.6 · 4.8 · 7.2 · 12.0 · 18.0 <br>`flat:` 0.427 · **0.403** · 0.405 · 0.681 · 0.768 · 0.801 · 0.826 <br>`bristle:` 0.415 · 0.407 · 0.411 · 0.582 · 0.656 · 0.733 · 0.773 <br>`round_hard:` 0.581 · 0.669 · 0.778 · 0.834 · 0.853 · 0.852 · 0.856 <br><br>At 2.7px a chisel lands `0.403` against a ground of `0.394` — nothing. Even at 18px a `flat` is `0.04` short and a `bristle` `0.09` short, which is most of the `0.10` that separates two masses; only a round tip holds its colour small. **The evidence is already in this repo's own data**: *The paint and the view of it* records a solid mass mixed at `0.215` landing `0.241` and one at `0.50` landing `0.504` — the same pull toward what it was laid over, in four rows, unnamed, at one brush size. This cost the painting four rehearsals on a bird's head laid at `size=0.005` that came back a dark fuzzy ball, and it is the likelier account of the first painting's bill "blooming pale" as a mass. (Measured; `paintings/heron_lot/2/probe_cover.py`.) | The general statement is that **a mass lands between its mixture and what it is laid over, and how far depends on the brush**. One row in `CALIBRATION.md` under `block_in` with the size column, and one clause on `solid`'s row in `REFERENCE.md` — which currently says it is "what fills a mass" without saying it does not fill it to its colour. A warning at the call when an oriented tip is handed a `size` under about `0.008` would have saved all four rehearsals, and its condition is measurable rather than guessed. |

| The documentation | What is proposed |
|---|---|
| **Six of the nine paintings on this page used no pencil at all.** Checked, not remembered: with the pool and the two herons set aside, every `pencil` hit under `paintings/` is the word inside an `UNPAINTED_KINDS` filter list or a probe. `pool_night` is the only painting in the repository that used landmarks (3) and the only one that redrew after the far masses were down (`p4_water.py`) — which is the guide's own order. The ninth session drew 13 lines in `pass1_draw.py` in each of its two paintings, at log indices 0–15 of 316 and 273, and **zero landmarks in either**. The sub-cell precision method — `mark` → `pt` → pencil through the points → `grid="fine"` → paint — is the guide's answer to the thing painters are worst at, and eight of nine painters did not use it once. (Measured off the repository.) | This is the largest untouched thing on the page and it needs a diagnosis before a fix. The three candidates below are what one painter can offer; which of them is right is a question for a run, not for this table. |
| **The guide sells the pencil on being free, and a rehearsal is free too.** *The pencil is free and does not count against the budget* is true and does not distinguish the two, so a painter who has correctly internalised *rehearse everything* will reach for the rehearsal — which is what happened here, five sequential times on one bird's head. **The property that actually distinguishes the pencil is that it is parallel**: six candidate outlines in one call, compared in one look, against one answer per round trip from a rehearsal. Nothing in any file says this. (Observed, and it is the painter's own account of its reasoning, worth what that is usually worth.) | One clause wherever the pencil is introduced: *a rehearsal shows you one answer; a pencil shows you six at once.* That is the argument that survives `rehearse everything` being the stronger habit. |
| **`The drawing` is written entirely around a reference, and the painter without one is sent straight to it.** *Painting without a reference* says *draw first anyway* → *The drawing*, and every mechanism in that section assumes two panels: marks drawn on both, `look(region=..., reference="ref.jpg", grid="fine")`, correcting by cell against the photograph. A painter with nothing to compare against reads it and finds one sentence addressed to them — that the proportions in your head may not fit the canvas. Nothing there tells them how to draw a *feature*, which is where both of this session's paintings spent their most expensive rehearsals. | The no-reference half of the precision loop, written out: landmarks placed by eye and checked at `grid="fine"` against each other rather than against a photograph, and the pencil as the thing you iterate a silhouette with before building it as a polygon. `compare({place: value})` was built for exactly this asymmetry and is the precedent. |
| **The pass-script convention quietly makes the pencil a one-off.** `paintings/` teaches numbered pass scripts, the drawing naturally becomes `p1_draw.py` — and once it is pass 1 it is finished. The guide's actual order is *landmarks before anything, pencil **after the far masses are down**, near masses on top*, which wants the pencil between passes 2 and 3. Both of this session's paintings put all their graphite in pass 1, on bare ground, where the first block-in buried it; the only painter that redrew mid-painting did it in its fourth pass. So the worked example the guide points at fights the instruction the guide gives, and the example wins. (Observed across nine paintings' scripts.) | Name the pass. If the convention is `p1_draw.py`, the guide's order asks for a second one — and a painting in `paintings/` whose scripts show it would teach it better than the sentence does, since a worked example is an instruction whatever the prose beside it says. |

**And one composition note, offered as a single instance rather than a rule.** The guide
says to count the horizontal bands before the first mass and then find something that
crosses them, *or a viewpoint that is not square on*. The second painting took a
stronger version — a viewpoint steep enough that **there is no horizon in the frame at
all** — and the band problem did not have to be solved because it did not arise. The
water became the whole picture and the sky existed only as what it reflected. One
painting, so it is a note and not an entry; if a second one wants it, it belongs beside
*a subject that is one thing against a ground*.

**One measurement tried and discarded, recorded because the instrument is this repo's.**
The painter tried to show that a verb-picked `scumble` is smoother than a hand-laid band
using the across-band wobble from *The band, and the brush that closes its joins*, and
the number came back the wrong way round — because on a `rough` ground with heavy
flecking showing through it counts canvas texture as ripple. The table states its own
conditions (linen) and is not wrong; but a painter reaching for that metric on their own
painting will get a number that means something else. One clause beside it would prevent
the next person spending what this one spent.

---

## The engine

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

---

## The documentation

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

## The two questions, and their answers

**On the guide's length.** Every session says it is too long and every session credits
the essay. What should be done with it?

**Stop shrinking it, and split by function instead.** The cost of length is not reading
time — one session's whole read cost a few minutes and about thirty thousand tokens,
against far more spent looking at its own rehearsals. It is that a rule read once at the
start is not in the hand at the moment it applies, and cutting cannot fix that, because
the rule cut is the one some painter needed. So: the split above, a CI-held budget on the
front page, and the standing rule that a finding goes to the engine, the recipes, the
reference or the calibration file and never adds a paragraph to `PAINTER.md`. All four
are done and written into `LESSONS.md`.

**The budget landed at 10,000 words rather than the 5,000–6,000 asked for**, and that is
the one place the answer differs from the request. The figure was never costed against
the contents the same list wanted the file to keep: the order of work, *What you are bad
at*, the checklist and the exercises come to about 8,500 words on their own, so reaching
6,000 would mean cutting them — which every other item on that list forbids. A budget
nobody can meet on the day it is written enforces nothing. The honest claim is halving.

**Still open, deliberately: the split is a hypothesis.** The test is two fresh sessions,
one given only the method, the recipes and the reference, one given everything. The
third painter's prediction, written down so it can be wrong: the first paints the masses
as well and improvises worse, because the essay is where the judgement came from when no
recipe existed.

The one data point that exists on reading order is not clean, and it is in `LESSONS.md`
rather than here. The third session read everything *before* the exercises — the wrong
order — did all eight anyway, and they still paid: the edge study showed it the smudge's
thumbprint before it could lay one in the picture, the load study showed the speckle a
starved bristle leaves, and the wet-versus-dry pair is why every later pass went on dry
paint. **So the gate held even when the reading ran past it**, which argues for the
exercises and says nothing either way about the order.

**On a warnings file.** Would a separate file of the warnings a painter must keep in
context help?

**No, and it is not a close call.** The third session had every warning in context for
the whole painting — the guide never left its window — and laid a glow as a solid disc,
planes as slabs and a picture in almost nothing but two brushes regardless. The front
page lists the mistakes, the checklist repeats them, and `LESSONS.md` already records
that a rule correct, well placed and repeated three times failed every run. A fourth
copy is the thing that file says does not work.

**What was written down instead** is where the idea should go: a check the tool runs
over the pass it just painted, printed beside the budget line — one brush at one size
for a whole pass, *n* passes at the same angle, a bristle under `size=0.025`, the
subject's share of strokes against the plan. Every input is already in the log. Each
rule that becomes a check can then leave the guide, which is the growth rule paying for
itself. That is in `LESSONS.md` as the next engine step, not built. So is the one form
of the file idea with a real mechanism — a short rules card kept where a `CLAUDE.md` is
kept, which survives a context compaction where the guide does not — which cannot be
judged, because none of the three sessions was ever compacted.

---

## What none of them would change

Every session defended the same things unprompted, and none was touched:

the order of work; no layers, no free undo, no black; **rehearsal seeded as the next
real strokes**, which is where every failure in all three paintings happened — a glow
that came back a sun, foam that came back a row of discs, a mass that came back a hull,
a halo that came back a cloud — at a cost of nothing; **the one plan object** shared by
`cost`, `preview`, `rehearse` and `paint`; `at_value`, asked for nineteen planned values
in one painting and landing every one to the hundredth; `compare({place: value})`, which
carried two whole pictures with no photograph to lean on; the place vocabulary; the
values view, called "the one that tells you the truth"; back to front and the
inside-of-a-hollow-thing rule; the eight exercises, which cost two minutes and were
repaid inside the first pass; and the habit of putting a measured number behind a rule —
*"the numbers changed what I did in a way the prose beside them did not."*

Every row of *the shape each tool leaves behind* survived being measured.

**The fourth session defended the same list**, unprompted and before being asked for an
opinion, and adds two notes to it. `at_value` was asked for about twenty-five planned
values and landed every one to the hundredth, including the ones approached from above.
And the plan object plus seeded rehearsal is the reason that session has six findings
rather than six damaged passages: **every one of the failures described above was caught
in a rehearsal and cost nothing** — the venetian-blind interior, the pale-slab
reflection, the four smudge lobes, the beaded frame, the white cap on the figure's head,
the amoeba puddle and the black-domino drain were all found, rewritten and found again
without a stroke being charged for any of them. 56 rehearsals, no repainted mass, no
`undo` called once. That is the same result the first three sessions reported, from a
fourth painter who was told to expect it and still had not guessed which passes would
go wrong.

**The three greenhouse painters defended the same three things above all**, unprompted:
the seeded rehearsal (a chartreuse searchlight of a beam twice, three flat slabs where a
cylinder should have turned, a chisel staircase, ten pots that were ten bricks, a halo
twice the size of the thing it surrounded, a stair read as a hose, a fog that was green
— all caught on a copy, none charged; 92 and 20 rehearsal images between two of them);
`at_value`, which landed about twenty-five planned values each to the hundredth and
raised when asked for a value under the floor; and `compare({place: value})`, which
carried three pictures with no photograph and finished all their places inside `0.10`.
One of them leaned on determinism hard enough to prove the `undo` finding with it: three
independent clean rebuilds of its painting are byte-identical.

**The eighth session defended the same list**, in a critique written before it was shown
the files it had not been given — and its list is the more interesting one, because it
is the arm with the least context and it defended the same things anyway. The seeded
rehearsal above everything: about forty of them, none charged, and every failure in its
own account was found on a copy — a staircased pool, a combed roof, a rake of bristle
marks where reflections should have been, a scumble that came back a contour map, a
mute glaze that read as a dark post and was dropped rather than committed. `at_value`,
which landed a nine-value plan to the hundredth and **raised** when asked for `0.135`
against a floor of `0.136`, which that session named as the right behaviour unprompted.
The values view, the one plan object, and the post-pass check, whose six rules it
described as "a linter for painting that fires at the moment you can still act" and
which it acted on every time it fired.

It is also the first session in four rounds to repaint a mass, and its account says why
without being asked: it chose a ground too light for the picture and found out at pass
three, which is the one item on its open list that was already solved in a painting it
had not been allowed to read.

---

## Where the arguments went

Four sessions' worth of reasoning, probe output and proposal text was cut from this file
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
  the probes behind the third, fourth and greenhouse rounds are
  `scripts/probe_third_session.py`, `scripts/probe_fourth_session.py` and
  `scripts/probe_greenhouse_session.py`, with the painters' own probes beside their
  paintings under `paintings/lighthouse_greenhouse/`;
- the releases are cut by version in [`CHANGELOG.md`](CHANGELOG.md), which is where to
  look for *which defaults moved*.

**Sixteen of the painters' own claims have been re-measured before anything was built
on them, and four did not survive.** All four are recorded above where the fix is — the
clean contour spilling further than the ragged fill it replaced, the smudge on a slope
that turned out to be a smudge on a bend, the rendered view that turned out not to lift
a solid mass at all, and the bare boundary at `overhang=0` that turned out to be the
comb and the brush running dry. That is `LESSONS.md`'s *check the painters' numbers*
working as intended, and it is worth noticing **what kind** of claim fails it: every one
of the four was reported as *observed* — a rehearsal showed it plainly and no number was
taken — and reasoned back to a mechanism that sounded right. The nine from the
greenhouse round all held, and two of them held with the wrong mechanism attached — the
pencil that "advances the stream" advances the log index, and the undo that lost "the
stream or the wet layer" was losing the stream *and* the log's precision — which is the
other thing the check is for. A claim that survives it is usually worth more afterwards,
because the re-measurement says what it is really about.
