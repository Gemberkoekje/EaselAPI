# What the painters asked for, and what was done

Four sessions painted a picture from the guide and then wrote down what the engine and
the documentation had cost them, a fifth pass synthesised the points more than one of
them raised, and the repository's owner put two further questions to the third painter.
This file is the register: **what was wrong, and what was done about it.**

**Everything on it is done** — 31 engine items and 42 documentation items. The long
arguments that produced each one have been cut, because a request list is worth keeping
only while somebody still has to act on it. What survives is the finding, because a
finding is still true after the fix, and the handful of places where the answer differed
from the request.

**Done is not the same as right, and four times now it has meant *measured and there was
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

---

## Still open, and what the fourth session says about each

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
**The other arm has not been run.**

**The post-pass check is still not built, and it is still the cheapest thing on the
list.** `LESSONS.md` has it as the next engine step — a check over the pass just
painted, printed beside the budget line, from inputs already in the log. Scored against
the fourth session: *n passes at the same angle* catches the road's banded scumble; *one
brush at one size for a whole pass* catches the first façade attempt; *the subject's
share against the plan* catches the drift to 41% at the moment it happened rather than
at the end. The fourth rule that session proposed for it — *a mass laid solid whose
planned and rendered values differ by more than `0.10`* — **is not worth building**, and
knowing that is what measuring the gap bought: the two values agree to `0.000`, so the
check would never fire. Every rule that becomes a check can then leave the guide, which
is the growth rule paying for itself.

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
  the probes behind the third and fourth rounds are `scripts/probe_third_session.py`
  and `scripts/probe_fourth_session.py`;
- the releases are cut by version in [`CHANGELOG.md`](CHANGELOG.md), which is where to
  look for *which defaults moved*.

**Seven of the painters' own claims have been re-measured before anything was built on
them, and four did not survive.** All four are recorded above where the fix is — the
clean contour spilling further than the ragged fill it replaced, the smudge on a slope
that turned out to be a smudge on a bend, the rendered view that turned out not to lift
a solid mass at all, and the bare boundary at `overhang=0` that turned out to be the
comb and the brush running dry. That is `LESSONS.md`'s *check the painters' numbers*
working as intended, and it is worth noticing **what kind** of claim fails it: every one
of the four was reported as *observed* — a rehearsal showed it plainly and no number was
taken — and reasoned back to a mechanism that sounded right. A claim that survives the
check is usually worth more afterwards, because the re-measurement says what it is
really about.
