# Suggestions for the engine and the guide, from the painting sessions

Three sessions, each written by the painter who had just finished a picture. The first
is below; the second starts at *Suggestions from a second session*, and the third at
*Suggestions from a third session*. **Every item on the first two lists is done** —
nineteen for the engine, twenty for the guide — and the note under each says what it
became, including the four that came back different when they were re-measured and the
two that were questions rather than requests. **The third list is open.** After it, a
synthesis of the documentation points that more than one session raised, and then the
third session's answers to two questions about the guide's length and a warnings file,
turned into actionable items.

Done is not the same as right. An engine item has a test behind it; a guide item is a
hypothesis until a fresh session paints against it, which is the rule `LESSONS.md`
opens with and the reason this file keeps saying what was changed rather than that it
worked.

The first list comes from one session: a still life painted from `PAINTER.md` alone,
with no reference photograph, through the shell path (`easel new` / `easel run`), in
224 strokes. The painting and its scripts are in `paintings/windowsill_pears/`. Nothing
else in the repository was read before painting, so this is the guide judged on its
own, which is what it asks for.

Before writing this I ran a few probes to check the claims that depend on the engine
rather than on taste. Each claim below says whether it was measured or is an opinion.
Where I could not settle something, it is written as a question.

> **Status.** All twelve engine items and all twelve guide items are done; what each
> became is noted under it in **bold**. They landed in two rounds: the corrections to
> something the engine does went in with the verbs that made them true, and the
> editorial ones — the one-page reference, the exercises as a gate, the cast-shadow
> recipe, the short path and the warning about painting several similar objects to one
> recipe — came after, once there was nothing left to change underneath them.
> The `overhang` claim below was re-measured before it went into the guide and it
> holds; the claim under engine item 8 did not, and the note there says what was done
> instead.

## What the probes found

- **`overhang` controls the ends of passes, not their sides.** A full-width `block_in`
  into a region spanning y 0.585 to 0.775 laid solid paint from 0.549 to 0.811 with
  `overhang=0`, and from 0.548 to 0.812 without it. The sideways spill is about half a
  brush either way. The source confirms it: overhang is how far each pass runs past the
  edge, along the pass. The guide's line "for two masses at the same depth, pass
  `overhang=0` or inset the place by half the brush size" is half right: only the inset
  works for the sides.
- **A round-tip block-in does not spray.** I reported a spray of dots outside the pears'
  contours as a possible defect. Measured on the same outline and brushes, on the same
  ground, over a painted pane, dry and wet, with and without impasto in the export: no
  paint lands beyond half a brush from the outline (17 or 18 pixels in every case, none
  beyond 30). The dots are the documented half-brush overhang, which a round tip lays as
  separate discs that the linen breaks up. The remedy is the one the guide already gives,
  inset by half the brush, and I did not apply it to the pears. My mistake, and a place
  the guide could be louder.
- **`log()` takes `last=`** and defaults to ten entries; `log(last=10_000)` returns the
  whole record. The guide never says so, and I concluded the log was truncated.
- **`contact_sheet(path, columns=6)`** (the time-lapse as a grid of thumbnails) and
  **`timelapse_gif(path, fps=8.0)`** exist and are not in the guide.
- **`ellipse(place, rx, ry)` takes both radii in the same unit**, so `rx == ry` is an oval
  on a 4:3 canvas. The guide explains the unit mismatch under brush sizes, not under
  coordinates or shapes.
- What the guide says and I can confirm: `dry()` is free; the signature exemption works;
  `cost()` matched what was charged; `pencil` and `mark` are free; the palette and its
  names persist across `easel run` calls.

## The engine

In the order of how many strokes each would have saved me.

1. **Rehearse a whole pass from the shell.** Something like `easel run --rehearse
   pass.py`: run the script against a copy, write the look and print the cost, commit
   nothing. Of my 224 strokes, about 60 went on repainting masses I had laid once and
   disliked (the curtain twice, the sill twice, the cast shadows twice, the sun in the
   pane twice). Every one of those was a pass I could have rehearsed and did not, because
   rehearsing means retyping the pass as a plan. If a script can be rehearsed as written,
   the guide's best advice becomes free to follow.

   **Done.** `easel run pass.py --rehearse` runs the script against a copy of the
   session, writes the look, prints what the pass would cost against the budget, and
   leaves the session file untouched. The strokes are seeded as the next marks of the
   real painting, so a rehearsed pass lands pixel for pixel when it is run for real.
   `Session.scratch()` is the same copy in Python, and `run(rehearse=true)` on the
   server.
2. **`paint(plan)`.** `cost`, `preview` and `rehearse` all take a plan of masses, sweeps
   and marks, and the guide promises "what you checked is what you paint, without
   rewriting it". That is true only for marks: a mass or a sweep in a plan has to be
   dispatched by hand to `block_in` or `sweep`, so I wrote my own runner. One method that
   paints any plan closes the gap and removes the drift the guide warns about.

   **Done.** `s.paint(plan)` takes exactly what `cost`, `preview` and `rehearse`
   take, masses and sweeps included, and dispatches each entry itself. It shares one
   dispatch with `rehearse`, so what is tried and what is committed cannot diverge.
3. **A budget on the session.** `Session(budget=300)`, with `easel run` printing spent and
   remaining, and `cost` flagging a call that would take more than some share. The guide
   asks the painter to write the split down; the engine could hold it.

   **Done.** `Session(budget=300)` and `easel new --budget 300`. `s.spent`,
   `s.remaining` and `s.budget_line()` say where the painting is, `easel run` prints
   it after every pass, and `s.cost(plan)` warns when a plan would take more than a
   quarter of what is left. Nothing is refused: the budget goes negative and says so.
4. **A soft-passage verb.** The guide is honest that there is no gradient tool, and its
   own remedy (steps, then a scumble of overlapping strokes at closely spaced values) is
   the one thing every painter needs and gets wrong first. `scumble(band, color_a,
   color_b, n)` that lays exactly that, charged as `n` strokes, would replace the loop the
   guide prints. My sun in the pane cost 27 strokes over two attempts; the first attempt
   was four hard bars, the loudest tell in the finished picture.

   **Done.** `s.scumble(band, color_a, color_b, n=8)` lays exactly that, charged as
   `n` on a convex band, running along the band's own long axis and stepping across
   it.
5. **A `cover()` verb for corrections.** The burying recipe needs a solid tip, `load=1.0`,
   `opacity=1.0`, `pressure="even"`, ends outside the area, and, as I found, also
   `load_falloff=0.0`: a full-width correction stroke with `load=1.0` still ran dry and
   left speckle at its far end. A verb with those defaults would make the commonest
   repair the one that needs no thought.

   **Done.** `s.cover(place, color)` dries the area, then blocks it in with a solid
   tip, `load=1.0`, `load_falloff=0.0`, `opacity=1.0`, `pressure="even"` and passes
   ending a full brush outside the area. Handed a bristle it says it cannot bury.
6. **Square-unit helpers.** `circle(center, r)` that is round on any canvas, or
   `ellipse(..., square=True)`, or a session-level unit option. I had to bake the aspect
   ratio into my own shape builder to get round pear lobes.

   **Done.** `s.circle(place, r, wobble=0)` is round in *pixels* on any canvas, and
   `ellipse(..., aspect=)` and `blob(..., aspect=)` take the ratio directly.
   `s.aspect` is the number.
7. **Shape operations.** `union(a, b)` and `shape.smooth()` would have let the pears be
   two circles and a waist without a custom generator, and a smoothed polygon would have
   had a cleaner silhouette than the scalloped one a round tip leaves.

   **Done.** `union(a, b)` traces one silhouette round overlapping shapes and keeps
   the waist a `hull` fills in; it refuses shapes that do not touch rather than
   silently returning the larger. `shape.smooth()` cuts the corners off an outline.
8. **A clean-edge option for shaped block-ins.** What finally gave the pears a smooth
   contour was: inset the shape by half the brush, block it in, then one `sweep` pass
   along the true outline in the same colour. Measured, that pass lays nothing outside
   the outline. `block_in(..., edge="clean")` doing those three steps would save the
   discovery.

   **Done** — with one correction, found by measuring it. The contour pass runs along
   the *inset* outline rather than the drawn one, so the brush's outer half lands on
   the line. Laid along the drawn line it spilled **further** than the ragged fill did
   (38px against 20px on a pear-sized mass); laid on the inset line it reaches 13px.
   It also warns on a bristle, which pulls the paint in but leaves a stringier
   contour than the ragged fill it replaced.
9. **Two-way `palette.at_value(base, target)`.** The guide's helper only adds white and
   raises below the base. I needed to hit a value from either side on every mixture, and
   wrote one that mixes in the blue-umber dark to go down. It belongs in the palette.

   **Done.** `palette.at_value(base, target)` bisects toward white to go up and
   toward a blue-umber dark to go down, and returns the *colour*. It raises when the
   target is out of reach rather than handing back the nearest it managed.
10. **`compare()` against a plan, not only a photograph.** With no reference, the planned
    values existed only in my head and in `value_of` printouts; nothing checked the
    canvas against them. `compare({place: target_value, ...})` would give a painter
    without a reference the same table and heat map.

    **Done.** `s.compare({place: value, ...})` measures each named place against the
    value it was promised and writes a three-panel sheet — the plan, the canvas, and
    each place outlined with its miss. The guide has a *Painting without a reference*
    section built round it.
11. **A prelude for shell mode.** Helpers had to be loaded with `exec(open(...).read())`
    at the top of every pass. `easel run --prelude helpers.py`, or auto-loading a
    `prelude.py` in the session's directory, would do.

    **Done.** Both: `--prelude other.py`, and a `prelude.py` beside the session file
    loaded automatically and announced, with `--no-prelude` to turn it off.
12. **Smaller time-lapses.** 235 marks made a 2.6 MB GIF. `every=` or `scale=` on
    `timelapse_gif`, alongside the `fps` it already has.

    **Done.** `timelapse_gif(path, fps=, every=, scale=)` and `easel timelapse
    --every 3 --scale 240`. The finished painting is always kept as the last frame,
    whatever `every` would have landed on.

## The guide

1. **A one-page reference beside the essay.** The essay is good and its voice is what
   made the rules stick, but the operational facts are hard to find inside it: what
   counts against the budget, the defaults, what `overhang`, `density`, `opacity` and
   `load` do exactly, what pressure does on each kind of tip, which unit each argument
   is in. A table, either at the top or as a separate file, would have saved me guesses.
   The `overhang` line should be corrected with the numbers above.

   **Done.** The `overhang` line was corrected in the first round, with the
   measurement in `CALIBRATION.md`; the reference is [`REFERENCE.md`](REFERENCE.md),
   a separate file as suggested — units first, because that is where the surprises
   are, then what counts against the budget, the verbs and what each charges, every
   argument that means something particular with its default, the brush table, what
   pressure does per tip family, the places and shapes, the palette, and the shell.
   `PAINTER.md` points at it from the top and from *The rest of the API*. It is
   checked by `tests/test_reference.py` rather than by hand: the brush table against
   the presets, every default against the dataclass, every region, ground, texture,
   pigment, pressure profile and `prepare` level against the source, and every `--flag`
   against the parser — so the one thing that would make it worse than no reference,
   drifting from the engine, fails the suite instead.
2. **Make the exercises a gate, with the cost of skipping them.** I skipped all eight and
   went straight to the picture. The stripy curtain and the sun bars were both lessons
   the exercises teach, and together they cost more strokes than the exercises would
   have. Say that.

   **Done**, as the paragraph under *Eight small exercises* — which is where a painter
   is deciding whether to skip them — naming the two lessons that were paid for inside
   the picture instead, and the reason an exercise is the cheap place to fail: nothing
   is built on top of it. The guide now also opens by telling a painter to read *the
   first hour*, do the eight, and come back for the rest, so the gate is at the front
   as well as at the exercises.
3. **Rehearse masses, not just features.** The guide teaches rehearsal for a feature
   smaller than a cell. The expensive mistakes are block-ins of big masses, which are
   cheap to repaint only until something stands on them. A rule such as "rehearse any
   block-in you will not want to repaint" belongs next to the two-`compare()` rhythm.

   **Done**, and `easel run --rehearse` makes it free to follow: rehearsing a mass
   no longer means retyping the pass as a plan.
4. **A positive recipe for a soft patch, with its cost.** The scumble recipe is written
   for a join between two bands. There is no recipe for a glow, a sky, a lit patch on a
   surface. My second attempt (one region with a diagonal edge, inset, laid at 0.6
   opacity) was better than the first and still shows its pass ends. I do not know the
   right recipe; a calibrated one is worth a section.

   **Done**, in two rounds. `scumble()` was the verb for the join, with its cost, and
   the guide's soft-passage section is written round it; the glow was the half it did
   not cover, and the second session asked for that half again as its own engine item
   1. `scumble(..., direction="inward")` is it, with the measured profile in
   `CALIBRATION.md` and the recipe in the same section of the guide.
5. **A recipe for a cast shadow.** My first shadows were capsule-shaped slugs at the
   palette's darkest value; the second were still heavy. Two sentences would have saved
   eight strokes: a shadow on a lit surface is a step or two below the surface, not the
   palette's dark; lay it as a tapering stroke and lose its far end.

   **Done, and calibrated by painting it.** Both halves hold. On a surface at `0.60`,
   the palette's darkest mixture lands at `0.16` and reads as a hole punched through
   the surface; `0.50` reads as a shadow and `0.42` as a shadow with weight. And the
   same value laid as a filled shape comes back as a slab with two hard ends — an
   object lying on the surface rather than a shadow falling across it — where one
   tapering stroke that loses its far end reads as a shadow, with a short darker pass
   where the two things meet. It sits in step 3, straight after the value floor, which
   is where a painter forms the belief that a shadow is the darkest thing they have.
6. **Small shaped masses with a round tip.** The guide's inset rule is under "Masses that
   are not rectangles" and the pears are exactly where I forgot it. Add the dotted-fringe
   symptom to "The shape each tool leaves behind", with the inset and the single-pass
   outline sweep as the remedy.

   **Done**, under "Masses that are not rectangles" where the inset rule already was,
   with the dotted-fringe symptom, the measured spill, and `edge="clean"` as the
   remedy.
7. **The unit mismatch belongs under coordinates.** One sentence there, with the ellipse
   example, and a formula: a round radius `r` in x is `r * width / height` in y.

   **Done**, under *Getting started* where coordinates are introduced, with the
   formula and `s.circle()` beside it.
8. **Document `log(last=)`, `contact_sheet`, and `timelapse_gif(fps=)`.**

   **Done**, in *The rest of the API*, along with the new `every=` and `scale=`.
9. **Add `load_falloff=0.0` to the burying recipe.** Every other clause is there.

   **Done**, and the recipe now leads with `cover()`, which sets every clause itself.
10. **A short path through the guide.** At 1600 lines it is a long read before a first
    stroke, and several rules appear three times in different words (painting up to a
    line, the box that should have been a shape, back to front). A "first hour" version
    of about a fifth the length, pointing into the full text, would get a painter to the
    exercises sooner without losing anything.

    **Done**, as *The first hour* at the top of the guide: what the engine is, the
    setup, the one habit, the six steps of the workflow in one line each, the five
    things a painter will get wrong, what a mark costs and the four planning verbs —
    then a table of where to read each of them in full. The guide now opens by saying
    to read it in two goes, with the exercises between them. Nothing was cut to make
    room, which was the request: the long text is the same long text, and it is read
    second instead of not at all. It came out at **a twentieth** rather than the fifth
    you asked for, deliberately: a fifth is still 3,000 words, and the failure this is
    against is a painter who does not finish the reading. What a fifth would have held
    and this does not — colour, the value plan, wet paint, the shape each tool leaves —
    is what exercises 1, 4 and 6 teach by hand ten minutes later. The repetition you noticed is left alone on purpose
    — the depth-order rule is the one `LESSONS.md` says needs a rewrite with a
    measurement attached rather than an edit, and thinning it by eye is exactly the
    edit it warns against.
11. **Warn about recipes repeated over similar objects.** One shading recipe painted all
    three of my pears, and they read as three copies. The guide warns about mechanical
    marks; it could warn about mechanical objects too: vary one thing per object on
    purpose.

    **Done**, as the second half of *You will under-vary your marks* — the same fault
    one level up, and the same fix stated as a procedure: vary one thing per object on
    purpose, and the guide names which things are cheap to vary.
12. **A page for painting without a reference.** Half the precision tooling assumes a
    photograph. For a painter working from a subject in their head: print `value_of` for
    every mixture and for the ground, write the value plan down as numbers, check
    `look(values=True)` against it after every mass, and, if `compare()` learns to take a
    plan, use that.

    **Done.** `compare()` takes a plan, and the guide has a *Painting without a
    reference* section built round it.

## What I would not change

The look loop, the region crops, `rehearse`, `cost` on the preview, named mixtures that
persist, `value_of` for planning, back to front, the inside-of-a-hollow-thing rule, and
the closing checklist. Those carried the painting from an empty ground to a readable
picture without a reference, and the guide's warnings predicted most of my failures
before I made them.

---

# Suggestions from a second session

These come from a second session: the inside of a car wash seen from the driver's seat,
painted from `PAINTER.md` with no reference photograph, through the shell path, in 206
strokes of a 300 budget. The painting and its scripts are in `paintings/car_wash/`.
Everything below was written at 185 strokes; the painting was then resumed, and the one
finding that produced is guide item 8.

> **Status.** All seven engine items and all eight guide items are done; what each
> became is noted under it in **bold**, along with the `.gitignore` line the probes
> caught. Items 6 and 7 were questions rather than requests and are answered as
> questions: yes to the pencil with no reference, in one line and narrowed by your own
> doubt about it; and `paintings/` is the worked example, named from `README.md` and
> deliberately not from the guide.
>
> Of this list's own measured claims, one did not survive being re-measured — the
> note under guide item 1 says what was found instead — and one came back with a
> different number, under engine item 2. The rest held. Every figure in the guide and
> in `CALIBRATION.md` is the re-measured one rather than the one here, because the
> engine these were taken on is no longer this engine.

**This session is not a clean measurement of the guide, and the difference matters.**
The subject was chosen before anything was read, but `README.md`, `LESSONS.md` and
`CALIBRATION.md` were then all read before the first stroke. So where this agrees with
the first session it is a second painter finding the same thing with more context, and
where it disagrees it may be the context talking. Nothing below leans on a rule I would
only have known from `LESSONS.md`.

Before writing this I ran probes for every claim that depends on the engine rather than
on taste, in the same spirit as the first session. Each claim says whether it was
measured or is an opinion, and one of them contradicts what I believed after my own
failure. Where I could not settle something it is written as a question.

## What the probes found

- **`block_in` at `density=1.0` does not lay a solid mass, and the solid version is
  free.** A `flat` at `size=0.030`, `density=1.0`, 48 passes, a mid dark on
  `umber_wash`: with the default load the interior measures **sd 0.070** and **6.15%**
  of its pixels are still within `0.05` of bare ground. With `load=1.0,
  load_falloff=0.0` it is **sd 0.005** and **0.00%** — fourteen times more even, for
  the same 48 strokes. The guide has these clauses, under *When something is wrong,
  paint over it*, which is where a painter reads them after laying the mass.
- **`edge="clean"` does not reach the canvas edge.** A mass drawn from `y 0.70` to
  `1.05` — deliberately past the bottom — filled clean leaves the bottom-left corner at
  `0.393` against bare ground's `0.43`, and **2.4%** of the bottom row unpainted. Ragged
  leaves `0.0%`. The half-brush inset is the whole point of `edge="clean"`; running off
  the canvas is the one case where it is wrong.
- **`scumble` is a linear ramp, not a fall-off.** Nine passes `lo`→`hi` over a blob at
  the centre: **down** through the middle it reads `0.41, 0.47, 0.61, 0.71`; **across**
  the middle `0.61, 0.58, 0.61, 0.61, 0.58` — flat. It grades edge to edge, which is
  right for a band and is not a glow.
- **A smudge *can* follow a curve, and every example in the guide is two points.**
  `smudge(points, ...)` hands straight to `stroke`, so it takes a polyline of any
  length. On a boundary sloping `0.045` in y per `0.2` in x, a two-point flat pass moved
  the boundary a mean of **0.57%** of canvas height (worst `1.81%`); the same smudge
  given four points along the slope moved it **0.11%** (worst `1.25%`). Five times less.
  *This corrects what I believed after my own smudge failed: I thought the tool could
  not follow a curve. It can. I gave it two points because the examples do.*
- **The bristle is the only tip in the box that does not repeat itself.** Two
  `dab(press=3)` marks at `size=0.02` per tip, silhouettes cropped and compared:
  `liner` **98%** identical, `flat` **94%**, `round_hard` **93%**, `knife` **89%**,
  `round_soft` **85%** — and `bristle` **26%**, because its comb is redrawn per stroke.
  Fill ratios against the mark's own box: `round_hard` `0.79` and `liner` `0.77` (a
  disc is `0.79`), `flat` and `knife` `1.00` (a rectangle), `bristle` `0.96`. So *a row
  of floating discs* is not a figure of speech — five round dabs are five copies of one
  disc to within 7%.
- **A rehearsal's looks overwrite the painting's, and each other's.** `easel run
  --rehearse` restarts the look counter: a real run wrote `look_001.png`, rehearsing
  wrote `look_001.png` over it, and rehearsing a second script wrote `look_001.png`
  again. Rehearsal is the thing a painter does repeatedly to compare versions, and only
  the latest can ever be looked at.
- **Crossing a direction is where `cost` runs away, and it is one cause wearing three
  hats.** The same shape, one direction against crossed: a thin full-width band **8 →
  74**; a small concave shape **9 → 38**. And a ribbon `0.032` wide: **2** straight,
  **23** with a bend in it. All three are the passes stepping across the *bounding box*.
- **`.gitignore` names an output prefix nothing writes.** It ignores
  `paintings/**/rehearse_*.png`; the engine writes `look_`, `preview_` and `compare_`,
  and `compare_` is the one not listed. Harmless while looks live in `out/`, which is
  ignored wholesale, and wrong the moment someone points `--out-dir` at the painting.
  **Fixed from both ends**: engine item 5 makes `rehearse_` a name that is written, and
  `compare_` and `prepare_` were added to the list.
- What the guide says and I can confirm: the signature exemption is free and per-record;
  `cost()` matched what was charged every time; and rehearsal really is pixel-exact —
  re-running the fourteen pass scripts into a fresh session reproduced the export with
  a matching sha256.

## The engine

In the order of how many strokes each would have saved me.

1. **A centred fall-off.** `scumble` solved the band and there is nothing for a glow, a
   bloom, a lit patch — a value falling off from a point rather than across an edge.
   Something like `scumble(shape, a, b, n, from="center")`, or its own verb. Measured
   above. It cost me four rehearsed versions of one mass, and the second of them came
   back as a daisy: strokes radiating from a shared centre make a flower, which is the
   obvious hand-rolled answer and the wrong one. The first session asked for a
   calibrated recipe for a glow and got `scumble`; this is the half of that request the
   verb did not cover.

   **Done.** `s.scumble(patch, color_a, color_b, n, direction="inward")`. The passes go
   *round* the place instead of across it — the first along its boundary and each one
   after it a part-brush further in — so `color_a` sits on the edge and `color_b`
   arrives at the centre, and nothing radiates from a point. It is `sweep`'s geometry
   with the colour stepping as it goes in, beside that walk rather than through it, so
   a ring that folds in on itself past the middle is dropped without compressing the
   ramp. Charged as `n`, like the band. A ring is two or three times the length of a
   pass across the same patch and has no far end to run dry at, so it defaults to
   `load_falloff=0.0`; an explicit one still wins. The measurement is re-run in
   `CALIBRATION.md` under *`scumble`*.
2. **`block_in` should lay a solid mass when asked for one.** Either `density=1.0`
   implies `load=1.0, load_falloff=0.0`, or there is a `solid=True`. Measured above:
   fourteen times more even at no extra cost. I laid the entire near frame speckled and
   only found out by cropping into it; it reads as ash rather than moulded plastic.

   **Done, as `solid=True`** rather than through `density`, because `density=1.0` is
   the default and changing what it lays would move every painting ever made and every
   golden image with them. `block_in(..., solid=True)` sets `load=1.0,
   load_falloff=0.0` as a pair of *defaults*, so `load=` beside it still wins, and
   `cover()` is the same clauses for a repair. Re-measured on this engine: 38 passes of
   a `flat` at `size=0.030`, `density=1.0`, interior **sd 0.063** and **4.4%** within
   `0.05` of bare ground, against **sd 0.007** and **0.0%** solid — nine times more
   even rather than fourteen, for the same 38 strokes. The claim holds; the ratio is
   the instrument's.
3. **A small irregular mark.** The probe says the box has exactly one tip that does not
   repeat itself and it is a comb. Either give the round tips a per-mark silhouette
   wobble — `block_in` already has per-pass wander, and the reasoning in *Design notes*
   about why the bristle comb is redrawn per stroke applies here word for word — or add
   a verb for a clot. I wanted a small irregular bright mark about fifteen times, laid
   dabs twice, got a row of discs twice, and ended up inventing "a short fat stroke from
   a starved bristle". The probe says that was the only answer in the box.

   **Done, as the per-mark silhouette** rather than as a verb, since the reasoning did
   apply word for word. `tip_wobble=0..1` on a round tip draws its outline from three
   low harmonics with a seed drawn *per stroke*, exactly as the comb is, and it swells
   as far as it bites so the mark keeps the size it asked for. Off by default, so no
   existing mark moves. Two `round_hard` dabs at `size=0.05` share **97%** of their
   silhouette as they are and **76%** at `tip_wobble=0.7`. `easel brushes` names it, so
   it is findable without reading the guide first.
4. **Do not inset a clean edge across the canvas boundary.** Clamp the inset where the
   outline leaves the canvas. Measured above; it cost me a repair pass and two strokes,
   and the repair then left a chisel end I had to fix as well.

   **Done.** The inset is dropped, per coordinate, on any side the outline reaches:
   a point on the bottom frame keeps its `y` and takes the inset `x`. A `Polygon`
   clamps its points to the canvas, so "the outline is at the frame" and "the outline
   ran off it" are the same test, and it is the right one either way. Re-measured on a
   full-width mass drawn past the bottom, a `flat` at `size=0.09`: **15.1%** of the
   bottom row unpainted before, **0.3%** now, against ragged's **3.6%** — better than
   ragged, because the contour pass runs along the frame too.
5. **Number a rehearsal's looks in their own sequence.** `rehearse_NNN.png` would do
   it — `.gitignore` already expects that name. Six rehearsals of one pass and I could
   never put two of them side by side, which is what a scrap of canvas beside an easel
   is for.

   **Done**, and numbered from what is already on disk rather than from a counter,
   because there is nowhere to keep a counter: a rehearsal runs on a copy of the
   session and the copy is thrown away. Each one takes the next free
   `rehearse_NNN.png`, in the shell and from `s.scratch().look()` alike. The
   `.gitignore` line that named a prefix nothing wrote now names one that is written,
   and `compare_` and `prepare_` were added beside it.
6. **Let `cost()` say *why* a number is large.** It already warns at a share of the
   remaining budget. Three of my calls came in at four to twelve times the estimate a
   painter would make by hand, all from the same cause. "74 passes: crossed, stepping
   across 1.10 of width" would let the painter fix the call; the bare number sends you
   to redesign the shape.

   **Done.** `s.cost_line(plan)` prints the total and a line per entry — *"2
   directions, 20 passes each stepping across 1.00 of the canvas"*, *"42 passes
   stepping across 0.34 of the canvas, each cut into 1.8 pieces by the outline"* — and
   the same sentence rides on the budget warning, naming the entry that dominates, and
   on the MCP `cost` tool's echoed Python, in its own comment so the echo stays
   pasteable. `s.cost_of(plan)` is the breakdown as data. The reason comes off the same
   walk the price is counted from, so it describes the passes that were actually
   counted. It says "of the canvas" rather than "of width": a coordinate is a fraction
   of the width in x and of the height in y, and the extent mixes them.
7. **Let `smudge` take an edge, the way `sweep` does.** `sweep(edge, ...)` accepts a
   boundary — or a whole shape, and follows its own outline. `smudge(points, ...)`
   accepts only points, so following a curve means sampling coordinates off it by hand.
   That is the step a painter skips, and the guide's examples are what teach them to
   skip it. `smudge(shape, ...)` walking an outline, or an `edge=` that takes what
   `sweep` takes, would make the correct usage the default one rather than the careful
   one.

   **Strokes saved: none, and the ordering rule is wrong about this one.** My two bad
   smudges were caught in a rehearsal and never committed, so they cost nothing at all.
   That is the honest number and it understates the item, because what a smudge does
   wrong is not charged in strokes — it is charged as a damaged passage. A thumbprint
   lying across a hard edge is the expensive kind of repair: burying it means
   repainting the mass it sits on, which buries whatever else is standing there. A
   painter who does not rehearse pays that, not two strokes. Worth reading as a general
   caution about this list's ordering, which prices a mistake by what it costs to make
   and not by what it costs to live with.

   **Done.** `s.smudge(edge, ...)` takes what it always took — points, used exactly as
   given — and also a shape or a region, whose own outline it walks, resampled the way
   `sweep` resamples a boundary. One mark either way, in the log and against the
   budget. The guide's two-point example is replaced rather than supplemented, and it
   names this rather than teaching the hand-sampling it replaces.

## The guide

1. **Give `smudge` a curved example.** Measured: five times the boundary movement, and
   the tool already does the right thing. This replaces the existing two-point example
   rather than adding a paragraph. It is *a worked example is an instruction* exactly —
   I followed the example's shape and not its rule, and dragged two finger-shaped lobes
   of glass into a dark mass doing it.

   The rule as it stands is right and incomplete: *"Run it along a boundary, never
   across one... Along the boundary, in short passes, it does what it is for"*, and then
   a two-point example. Nothing says that on anything but a straight edge those two
   sentences disagree with each other. Proposed replacement for the paragraph and its
   block in step 5, keeping the existing first half:

   > **Along means along the boundary's own shape, and only a straight boundary is two
   > points.** Given a straight pass, a curved or sloping edge gets a mark that starts
   > along it and ends across it — the same thumbprint, arriving more slowly. `smudge`
   > takes as many points as you hand it, so hand it the curve; if the boundary is a
   > shape you built, its own outline is already that path.
   >
   > ```python
   > s.smudge([(0.30, 0.40), (0.38, 0.41)], size=0.04)          # a straight edge is two points
   > s.smudge([(0.30, 0.40), (0.45, 0.45), (0.60, 0.53),
   >           (0.73, 0.63)], size=0.04)                        # a curved one is the curve
   > ```

   Both passes register in the log, and the replacement above was applied to
   `PAINTER.md`, checked with `scripts/check_guide_blocks.py` — 51 ok, 0 failed,
   unchanged from baseline — and then reverted. The measurement behind it belongs in
   `CALIBRATION.md` rather than here, under *`smudge`*, as a row beside the join-sharpness
   table:

   > - **"Along" means along the boundary's *shape*.** On an edge sloping `0.045` in y
   >   per `0.2` in x, one pass at `size=0.040`: given two points it moved the boundary a
   >   mean of `0.57%` of canvas height and `1.81%` at worst; given four points sampled
   >   along the slope, `0.11%` and `1.25%` — five times less. A two-point pass on a
   >   curve begins along the boundary and ends across it.

   Two cautions on applying it. `LESSONS.md` says a guide change is a hypothesis until a
   fresh session paints against it, and I am the session that just failed this rule, so
   this is a proposal and not an edit — I have deliberately not touched `PAINTER.md`.
   And if engine item 7 is taken instead, this paragraph should name that verb rather
   than teach the hand-sampling it replaces.

   **Done, and the measurement behind it was wrong.** Engine item 7 was taken, so the
   paragraph names `s.smudge(shape)` as well as the curve. But re-measuring it first:
   on a *straight* sloping edge, two points and four along it are the same pass to the
   pixel — the spline through collinear points is the line — so the `0.57%` against
   `0.11%` cannot have come from a slope. It comes from a **bend**, and there it is
   larger than reported: on a boundary that curves, the chord between its ends moved
   the boundary a mean of `0.51%` of canvas height and `2.9%` at worst, against `0.01%`
   and `0.7%` for four points along the curve. The rule survives its evidence and is
   sharper for it: *only a straight boundary is two points*. That is what went into the
   guide, with the numbers in `CALIBRATION.md` under *`smudge`*.
2. **`load` belongs beside `density`, not only in the repair recipe.** One clause where
   masses are laid. Measured above.

   **Done**, in step 1 where the first masses are laid, as the rule with the numbers
   stripped out: *density spaces the passes; it does not fill them*, and a mass that
   has to be solid says `solid=True`. The measurement is in `CALIBRATION.md` under
   *Load and run-out*.
3. **A checklist line for the tool's own shape at small scale.** *"Is any small mark a
   disc, a capsule or a rectangle — the tool's shape rather than the thing's?"* The
   warning exists in prose and in the *shape each tool leaves behind* table, I read
   both, and laid a row of discs twice anyway. The probe gives the number to put behind
   it.

   **Done**, as that line in the closing checklist, with a row in *the shape each tool
   leaves behind* that names `tip_wobble` as the remedy — because a checklist line that
   only names the fault is the warning-without-method `LESSONS.md` is about.
4. **A checklist line about stopping.** The closing checklist has fourteen lines and
   none of them is about finishing. The guide warns at length about spending too much on
   detail and about reaching the subject too late; it says nothing about stopping early.
   I finished with **115 of 300 strokes unspent**, having already named the weakest
   passage in my own notes and then given it four more strokes. Proposed: *"You have
   named the weakest passage. How many strokes are left? Spend them there."*

   **This one was then tested rather than left as a proposal.** The painting was resumed
   and the rule followed literally: twenty-one strokes into the passage the notes had
   named, which is where item 8 came from. It is the only item in either session's list
   that has been run rather than argued, and the thing it found — that the eye and
   `compare()` each caught half of what was wrong — is not something a fourteenth
   checklist line predicts. Worth more than my confidence in it: a fresh session should
   still be the judge.

   **Done**, as the last line of the closing checklist, in your words: *you have named
   the weakest passage; how many strokes are left; spend them there* — with the reason
   the line exists, which is that nothing above it is about finishing, and the warning
   that the passage wanting them is the one you would apologise for rather than the one
   you have most recently been enjoying. Your having run it rather than argued it is
   why it went in as written.
5. **The lightest mass is a composition question that `compare()` answers by accident.**
   `compare()` told me the bloom was `0.12` below plan. What it was really reporting was
   that a different mass had become the brightest thing in the picture and the eye went
   to it — a composition fault, found by a value tool. The guide's *"is the thing you
   measured most carefully still the thing the picture is about?"* is the right
   question and it is one line, late, in a long section. In value terms it is cheap and
   checkable: *is the lightest mass in the picture the one you planned to be lightest?*
   `compare()` already holds the numbers.

   **Done**, as a checklist line directly under the composition question it makes
   checkable, in your words and with both ways of answering it: `look(values=True)`, or
   the numbers `compare()` already holds. No engine change was needed, which is what
   you said.
6. **Does the pencil apply with no reference? The section does not say.** *Painting
   without a reference* says you are the reference and lists three things to do, all of
   them value work. It never mentions drawing. I did not draw, and told myself the
   previewed shapes were the drawing. Drawing is free and does not count against the
   budget, and a drawing would probably have caught my frame proportions before six
   rehearsals — **but I am not sure that is a recommendation rather than hindsight**,
   because a painter with no reference has nothing to check a drawing against, which is
   half of what the pencil is for with one. A question, not a request.

   **Answered yes, in one line**, and your doubt narrowed it usefully. The line does not
   claim a drawing can be *checked* without a reference; it says the pencil is free and
   that a drawing is still the cheapest place to find out that the proportions in your
   head do not fit the canvas — which is a thing you can see the moment it is down,
   without anything to compare it to. That is the half of the pencil that survives
   having no reference.
7. **A question about worked examples, which I think has no clean answer.** The guide
   has eight abstract exercises and no single small picture laid out in order, and
   sequencing was the thing I was least sure of at the start — not which call to make
   but which to make first. `LESSONS.md` is right that an example is read as an
   instruction and that a named subject leaks, and an end-to-end example would leak its
   subject harder than any fragment can. The paintings in `paintings/` already are that
   example and already carry that risk, unread. So: is `paintings/` meant to serve this,
   with the guide pointing at it — or is the sequencing meant to be worked out fresh
   every time, and the exercises deliberately abstract to keep it that way?

   **Answered: `paintings/` is the worked example, and `README.md` says so while
   `PAINTER.md` does not.** Each painting is its numbered pass scripts, its prelude,
   its notes and an export that re-runs byte for byte, so the order it was made in is
   readable rather than reconstructed. A painter who goes looking finds it; one who
   reads only the guide is not handed a subject. Reading them is also what a session
   running the measurement protocol must not do, and `README.md` says that too. The
   trade is written up in `LESSONS.md` beside *a worked example is an instruction* —
   where, running the noun grep your question prompted, the guide turned out to have
   picked up one painting's subject in three examples and two of its places in a
   fourth. Those are gone.
8. **Form is bounded at both ends, and the guide gives only the lower bound.** The
   `0.10` threshold appears everywhere as the point below which two masses stop reading
   as separate, and it is right. Nothing says what happens *above* it. Measured on this
   painting's weakest mass: flat at a range of `0.09` across its width it read as a
   curtain rather than a cylinder, so form was laid until the range was `0.22` — at
   which point its shadow side sat `0.09` from the mass *behind* it and the two began to
   merge. Compressed back to about `0.15`, both separations hold. So a mass has a
   window, not a floor: **shade it until the form clears `0.10`, and stop, because past
   that the range is spent on the mass's separation from what it stands against.** One
   line, and the natural home is beside the existing threshold paragraph in step 3
   rather than as a new section.

   Worth noting how it was found, because it is the case the guide's two-`compare()`
   rhythm is not built for: the eye said the form was good, and the number said the mass
   had stopped separating from its background. Neither would have caught it alone.

   **Done**, beside the `0.10` threshold in step 3 as you suggested, and written as the
   window rather than as a second floor: shading spends value range, the range is
   shared with the mass's separation from what it stands against, so **shade until the
   form clears `0.10` and stop**. Your numbers are in it as the measurement — flat at
   `0.09`, turned at `0.22` with the background `0.09` away, both holding at about
   `0.15` — and it is one mass, so it is a rule with one measurement behind it rather
   than two. Worth re-measuring on the next painting that has a cylinder in it.

## What I would not change

The plan object shared by `cost`, `preview`, `rehearse` and `paint`. It is the best
thing in the engine: thirty-eight rehearsals, none of them charged, and a painting that
re-runs from its own pass scripts byte for byte. Everything that went wrong in this
painting went wrong on a copy of the canvas and cost nothing — a bloom that came back as
a daisy, foam that came back as a row of discs, a frame that came back as stepped
rectangles and a letterbox.

Also unchanged: `at_value`, which was asked for sixteen planned values and landed
every one of them to the second decimal;
`compare({place: value})`, which carried the whole picture with no photograph to lean
on; back to front and the inside-of-a-hollow-thing rule, which is the reason a steering
wheel reads as a ring rather than a hole; and the habit of putting a measured number
behind a rule. The numbers changed what I did in a way the prose beside them did not.
And every row of *the shape each tool leaves behind* survived being measured.

---

# Suggestions from a third session

These come from a third session: a lighthouse on a rocky headland at dusk, painted from
`PAINTER.md` with no reference photograph, through the shell path, in 184 strokes of a
300 budget. The painting and its scripts are in `paintings/lighthouse_dusk/`. Nothing
here is done yet; the items are open, and the note format the two lists above use is
left for whoever closes them.

**This session is not a clean measurement of the guide either.** The subject was chosen
before anything was read, but `README.md`, `LESSONS.md`, `CALIBRATION.md`,
`PAINTINGS.md` and both earlier paintings' notes and scripts were all read before the
first stroke. The pass-script convention, the prelude of masses as functions and the
`compare()` plan sheet were copied from `paintings/`, not worked out from the guide. So
where this agrees with the two sessions above it is a third painter with more context,
and where it disagrees it may be the context talking.

Every claim below says whether it was measured or is an opinion. The measured ones are
`scripts/probe_third_session.py`, which prints the numbers quoted here on a 512×384
canvas. Where I could not settle something it is written as a question.

## What the probes found

- **A raw `(r, g, b)` triple handed to the palette is read as sRGB, not linear.** The
  guide (*Colour*, "Supplying a colour of your own") and `REFERENCE.md` both say linear.
  Measured: a `toned_grey` ground reads `0.53`; its own mean, taken from `s.canvas.rgb`
  and assigned as a tuple, reads **`0.25`**. The same mean assigned as a `float32`
  array reads `0.53`, because `parse_color` passes an engine array through untouched,
  and so does the mean encoded to a hex string first. So there are two working ways to
  hand a sampled colour back and the guide documents a third that does not work. It
  cost me one rehearsal: the halo's outer rings, meant to be the sky's own colour,
  landed near black.
- **Where the first pass of a stack lands.** A five-pass scumble red→blue over a
  square, `flat` at `size=0.08`, full opacity: with `direction=0`, `"horizontal"` or
  `"axis"` on a wide place, colour `a` is along the **top** edge; with `90` or
  `"vertical"` it is along the **right**; with `45` it is in the upper right. A
  `polygon` behaves the same as a `Region`. So `scumble(place, a, b, direction=90)`
  puts `a` on the side away from the left, which is the opposite of what reading the
  call suggests, and nothing says so. It cost me two rehearsals and the tower's lit
  face went on the wrong side once.
- **A pressure list flips on alternate passes.** `_angled_paths` yields every odd
  path reversed, so a `pressure=[0.0, 1.0]` on a scumble or a block-in lands heavy at
  the right end of one pass and the left end of the next. Measured on four horizontal
  passes: paint at the two ends `0.35 / 0.56`, `0.52 / 0.33`, `0.35 / 0.57`,
  `0.56 / 0.34`. A passage that is meant to brighten toward one side cannot be laid
  with the verb; I laid the afterglow as six hand-written strokes instead.
- **The inward scumble fills solid when the brush is wider than about twice the ring
  step, and the default brush always is.** The rings step `depth / n` apart, where
  `depth` is half the patch's shorter extent, and each ring is laid over the ones
  before it. Measured on an ellipse `0.72 × 0.24`, `n=7`, opacity `0.5`, bristle,
  colours `0.45` at the edge and `0.75` at the centre; the second column is the share
  of the patch within `0.06` of the centre value, the profile is read from the top
  edge to the middle:

  | brush | flat at the centre value | profile, edge → centre |
  |---|---|---|
  | `0.09` | **44%** | `0.52 0.55 0.62 0.69 0.70 0.69 0.71` |
  | `0.05` | 12% | `0.49 0.49 0.59 0.61 0.64 0.69 0.65` |
  | `0.03` | 0.2% | `0.49 0.50 0.55 0.58 0.61 0.63 0.62` |
  | `0.02` | 0% | `0.50 0.53 0.53 0.57 0.54 0.55 0.61` |
  | `round_soft 0.09` | 42% | `0.50 0.56 0.60 0.66 0.71 0.72 0.72` |

  The ring step here is `0.017`. At `0.09` the brush is five steps wide and the last
  rings bury the first: nearly half the patch is one flat colour with a rim of ramp
  round it, which is the solid yellow sun I rehearsed three times. At `0.03` the
  ramp is smooth and the centre never reaches its colour, because at opacity `0.5`
  nothing lands there more than twice. `0.05`, about three steps, is the usable
  middle. The guide's example gives no `size=`, so it runs at the bristle's default
  `0.11`, which fills any patch under about half a canvas across. `CALIBRATION.md`'s
  own table shows the same thing on its patch — the inner half of the fall-off reads
  `0.86, 0.91`, flat — and reads it as a fall-off. A round patch of radius `0.10`
  with a `0.05` brush comes out right: `0.49 0.51 0.57 0.64 0.69 0.68 0.62`, 2.4% flat.
- **`solid=True` is as even as it gets, and opacity does not change it.** A `flat` at
  `size=0.03`, `density=1.0`, `solid=True` over a region: interior sd `0.009` and a
  row-mean peak-to-peak of `0.028`–`0.030` at every combination of opacity `0.85` or
  `1.0` and pressure `"taper"` or `"even"`. *This contradicts what I believed after my
  own rock planes came out striped at opacity `0.85` and clean at `1.0`: the
  measurement says the pass structure is `0.03` of value at any opacity, and what
  changed between those two rehearsals was the shapes and the brush size, not the
  opacity.* On a flat plane at feature scale `0.03` is visible; it is hidden by a
  bigger brush or a broken one, not by an argument.
- **The flat's wander has a middle setting, and it is two brush fields.** One
  horizontal `flat` stroke, `size=0.1` (51 px on this canvas), top edge measured along
  its length: default `jitter=0.02, size_jitter=0.06` wanders sd `1.2` px, peak to
  peak `6` px; `jitter=0.01, size_jitter=0.03` halves both; `jitter=0.005,
  size_jitter=0` is `1` px; zero is ruled. It scales with the brush, so at the
  `size=0.13` I used for the sky the scallops were about twice this. I rehearsed only
  the default and zero, found the default scalloped and zero ruled, and kept the
  scallops; I did not go back and lay the sky at the halved setting, so whether it
  reads better there is not measured.
- **`look(diff=True)` inside a rehearsal has nothing to diff against.**
  `_trial_session` sets the copy's `_last_look` to `None`, and the look it writes is
  the plain copy. So the one question a rehearsal exists to answer — what would this
  pass change — cannot be asked of it as a tint.
- What the guide says and I can confirm: the ten pass scripts rebuilt the export from a
  fresh session with a matching sha256; `at_value` was asked for nineteen values and
  landed every one to the hundredth; `cost()` matched what was charged; the signature
  was not charged; the rehearsal counter now runs apart from the painting's, and none
  of seventy-two rehearsal looks overwrote another.

## The engine

In the order of how many rehearsals each would have saved me, since none of my strokes
went on repainting.

1. **Derive the inward scumble's brush from its ring step.** Default `size` to about
   three times `depth / n` when `direction="inward"`, or warn when the brush given is
   wider than that, the way `cost()` warns about a share of the budget. Measured above:
   at the bristle's default size the verb lays a solid patch with a rim of gradient
   round it, on any patch a painter would call a glow. Three rehearsals, and the verb
   was abandoned for hand-rolled strokes that do less than it could.
2. **Rehearse several scripts in order from the shell.** `easel run p.easel p2.py
   p3.py --rehearse`, running them in sequence against one copy. I rehearsed the sea
   and rocks together five times, and the three finishing passes together once, by
   writing a wrapper that `exec()`s each file, because a pass that goes on top of
   another pass has to be judged on it. The wrapper is in nobody's log.
3. **Carry the last look into a rehearsal.** Copy `_last_look` into the trial session
   so that `look(diff=True)` in a rehearsed pass tints what the pass would change. It
   is one assignment, and it turns the rehearsal into the before-and-after it is for.
4. **Apply a pressure list in canvas order on `block_in` and `scumble` passes**, or
   take a keyword for it (`alternate=False`), so a passage that lands light on one
   side and heavy on the other is one call. Measured above. Six strokes of the afterglow
   are hand-written for exactly this reason, and they are the strokes in the painting
   most likely to be wanted again.
5. **A way to sample the canvas into the palette.** Something like
   `s.palette["sky_here"] = s.sample(place)` returning the engine's own array, so a
   halo ring, a moon's dark side or a repair can match what is already there without
   the painter knowing which of three encodings the palette will assume. Until then the
   working recipe is to assign the `float32` array straight from `s.canvas.rgb`.
6. **Question: should the contour pass of `edge="clean"` wander?** The headland's ridge,
   filled clean with a `flat` at `size=0.08` along an unsmoothed eleven-point outline,
   came back with a row of rounded knobs along the top edge. I did not measure whether
   that is the contour pass's wander or the outline's corners under a wide brush, and I
   painted a strip over it. If it is the wander, a contour pass with `jitter=0` would
   draw the line the painter drew.

## The guide

1. **Say what a triple is.** Under *Colour*, "a hex string or a linear RGB triple"
   should read "a hex string, or an sRGB triple `0.0–1.0` as a hex string is; a
   `float32` array from the engine itself is linear and passes through." The same row
   in `REFERENCE.md`. And, beside it, the one line a painter reaches for this section
   for: how to hand a colour sampled from the canvas back — assign the array, do not
   round-trip it through a tuple.
2. **Say where a stack starts.** In `REFERENCE.md` under `direction`: the first pass
   is at the top for `0`, at the right for `90`, and every second pass runs the other
   way, so a pressure list alternates. One row of a table.
3. **A page of recipes that worked, one line and one code block each.** The guide is
   strong on what not to do and has no recipe for the things a subject is made of; ten
   of my eighteen rehearsals were spent finding these, and each is now a pass script
   in `paintings/lighthouse_dusk/`:
   - *a cylinder*: the mass solid in the shadow colour, the lit side as a second shape
     laid on it, one half-strength stroke down the join (`p4_tower.py`). A pass ramp
     across the whole width came out flat twice.
   - *a rock*: not marks on a mass but the planes the mass is made of, as three or four
     shapes tiling it, each at one value, the block-in's dark left as the shadow
     (`p3_rocks.py`). Facets laid on the mass read as things stuck to it twice.
   - *a brightening toward one side*: strokes all run the same way with
     `pressure=[0.0, 0.55, 1.0]`, one value step apart (`p1_sky.py`).
   - *a straight horizon*: one `flat` stroke with `jitter=0, size_jitter=0`; the only
     ruled line a seascape needs (`p2_sea.py`).
   - *a crescent*: one tapered arc on the round tip, `pressure=[0.05, 0.6, 1.0, 0.6,
     0.05]` (`p6_moon_beam.py`). A disc with a disc bitten out of it leaves a ghost.
   - *a small round thing*: a `dab(press=3)` is right when the thing **is** a disc,
     and the guide's warning against discs reads as if it never is.
   Opinion, all of it; each one is a recipe that worked once.
4. **Give the inward scumble example a `size=` and a rule**, "keep the brush under
   about three ring steps, `3 * depth / n`", and have `CALIBRATION.md` state the patch's
   radius and read its own table as a rim of gradient round a flat middle. Measured
   above.
5. **"Rehearse any mass you would not want to repaint" is too weak.** Eighteen of
   eighteen rehearsals changed something, none was charged, and no stroke in the
   painting went on repainting anything. The line should say: rehearse every pass, it
   costs a look. Opinion, with that one number behind it.
6. **A line under `solid=True`**: the pass structure of a solid flat block-in is about
   `0.03` of value at any opacity and pressure, which shows on a flat plane at feature
   scale; hide it with a bigger brush or a bristle, not with `opacity`. Measured above,
   and the opposite of what I believed while painting.
7. **A line about glazes and colour.** A gold glaze at `opacity=0.14` across a violet
   sky landed as a saturated stripe; at `0.07` it landed as nothing. The knife's rule,
   "keep it close in value to what it lands on", seems to apply to a glaze's *hue* as
   well, and the glaze line says only "thin transparent film". Observed twice, not
   measured; the two rehearsals are in the notes and the beam is not in the painting.
8. **Under *Painting without a reference*: re-check the plan sheet's places after
   moving a silhouette.** My left-horizon place was written before the ridge was
   raised and made jagged; it ended half rock and reported a `-0.16` miss that was not
   one. `compare()` cannot know that a place has changed meaning; one line can.
9. **The two-goes instruction, as a data point.** I read the whole guide and the
   reference before doing the exercises, then did all eight, then painted. The
   exercises still paid: the edge study showed me the smudge's thumbprint before I
   could lay it in the picture, the load study showed the speckle a starved bristle
   leaves, and the wet-versus-dry pair is why every sea pass was laid on dry sky. So
   the gate held even when read in the wrong order. Whether the essay is finished by a
   painter who does the exercises first, I cannot say; I did not.

## What I would not change

Rehearsal, seeded as the next real strokes: eighteen runs, nothing charged, and every
one of the pictures' failures — a sun instead of a glow, a hull instead of a rock, a
dark cloud instead of a halo, a mustard stripe instead of a beam — happened on a copy.
`at_value`, which turned a value plan into nineteen mixtures without one guess.
`compare({place: value})`, which measured the picture against the plan before and after
the block-in and once at the end. The shape builders, `s.circle` doing the aspect
arithmetic, and `edge="clean"`, which is why the tower has a silhouette. The worked
examples in `paintings/`: the prelude of masses as functions and the numbered passes are
the reason the painting re-runs from its own scripts, and I would not have arrived at
that convention from the guide. And the eight exercises, which cost two minutes and
were repaid inside the first pass.

---

# Documentation suggestions, synthesised across painting sessions

Scope: documentation only. Engine findings (glow as a ramp not rings, sRGB/linear
triples, `solid=True`, bristle below 0.025, flat jitter middle setting, pass-stack
start side) are in the individual session reports and are not repeated here.

Sources: the windowsill-pears session, the car-wash session (two sittings), the
lighthouse session, and the four rehearsals before them. A point is listed only if
more than one session raised it independently.

## The three findings every session made

**1. Strong on what not to do, thin on what to do.**
Pears: "warning without procedure." Car wash: "there is no recipe for a small
irregular bright mark, and I needed one four times." Lighthouse: "no recipe for a
cylinder's form, a glow at size, or a rock mass — ten of my rehearsals were spent
discovering those. One page of recipes would have halved my rehearsal count."

Add `RECIPES.md`: one page, each recipe is the calls in order, the rehearsal count
it took to find, and one line on what it looks like when it goes wrong. The
painters have already written these in their rehearsal logs; collect, don't
compose. Starting list, all requested by name:
- a cylinder's form (lit face, terminator, reflected light)
- a glow at size (currently fails above a small patch)
- a rock mass that isn't slabs
- a plane that is a plane (opacity 1.0, even pressure — currently discovered by hand)
- a small irregular bright mark (the "short fat starved bristle smear" workaround)
- a hollow thing, in depth order (far rim, inside, near rim)
- a lost edge that is actually lost (car wash: "the two I lost are barely perceptible")
- a quiet gradient without a gradient tool
- a mark that crosses a boundary, for when a smudge isn't enough

Keep recipes noun-free in the same way the guide is: "a cylinder," not "a tower."

**2. Everyone underspends on the subject, after reading that they will.**
Pears: 59% of strokes before the subject began. Car wash: worst passage named in
its own notes, 115 strokes unspent. Lighthouse: 24% on the subject against a
planned 32%. Each painter quotes the guide's warning while doing it.

This is no longer a documentation gap; the prose has been tried three times. What
documentation can still do: make the checklist read the ledger rather than the
painter's intent. Replace "did you spend enough on the subject?" with "run
`s.log()` (or the plan sheet) and write down the subject's share of strokes
against the share you planned. If it is lower, you are not finished." A number the
painter has to write down is harder to wave through than a question.

**3. Rules known in prose are not known in the hand.**
Car wash: made the floating-disc mistake twice after reading the warning and its
measured table. Lighthouse: used only flat and round after the warning about
exactly that, and read everything instead of following the two-goes instruction.
Pears: skipped the exercises and blamed the curtain on it. Every session: "it
predicted my mistake and I made it anyway."

Consequences:
- Keep the eight exercises. The one session that skipped them regretted it in
  writing; the one that did them called them "two minutes well spent" and said the
  edge study showed it the smudge thumbprint before it could make it. They are the
  only part of the guide that teaches the hand.
- Add a short list at the top of "What you are bad at": *the four mistakes every
  painter so far has made after being warned*, each with its fix procedure on the
  same line. Floating discs, capsule shadows, the stack of bars, brushwork that is
  all flat and round. A warning the reader will violate anyway is only useful if
  the repair is next to it.
- Prefer cheap rules that are always followed over wise rules that are sometimes
  followed (see 5).

## Structure

**4. Length: 17,000 words, read once, before the first stroke.**
It was 8,600 when first reviewed, 10,800 after the subject-leak fix, and is now
17,300. Every session says it is long; every session says the essay is what made
the rules stick; both are true. "The first hour" front page is the right answer,
but it sits at the top of a file whose length still signals "read all of this."

Make the split physical. `PAINTER.md` becomes the front page, the order of work,
"What you are bad at," the checklist, and the exercises — a target of 5,000 to
6,000 words that a session can hold in its head. Everything else moves, unchanged,
to a companion: `PAINTING.md` for the essay (colour, wet paint, edges, looking,
the reasoning behind each rule), `REFERENCE.md` for facts about tools (already
exists; the brush chapter belongs there), `RECIPES.md` for procedures. The
two-goes instruction then stops being an instruction and becomes the file
boundary. A session that reads everything anyway loses nothing; a session that
reads only `PAINTER.md` gets the whole method.

Standing rule for the guide, worth writing into `LESSONS.md`: a new finding
either replaces an existing rule, becomes a checklist line, or goes to
CALIBRATION, RECIPES or LESSONS. It never adds a paragraph to `PAINTER.md`.
The file has grown by one paragraph per rehearsal; at the tenth rehearsal
nobody reads to the end.

**5. "Rehearse any mass you would not want to repaint" is too weak.**
Car wash: 27 rehearsals in the first sitting, "every bad idea cost nothing."
Lighthouse: 18 rehearsals, "changed something every time, none cost a stroke,"
and "the true rule was rehearse everything, and it never failed to pay." Change
the rule to *rehearse everything*. It is cheap, it is always followed, and the
guide's own numbers say it pays.

**6. The checklist is read as "done"; it means "may stop."**
Car wash: "the checklist passing and me taking the exit," 115 strokes unspent.
Lighthouse: stopped at 184 "partly a decision I can defend and partly wariness of
making it worse." One sentence beside the checklist: passing it means the
painting is not wrong, not that it is finished. The finished question is the
subject-share number from point 2 and the worst passage named in your own notes.

**7. Measured claims should state what they were measured on.**
Lighthouse found the glow recipe "measured on a patch of unstated size" and it
failed on a large one; the linear-triple claim was wrong in two documents. A
documentation rule, cheap to apply: every number in CALIBRATION or REFERENCE
carries the size, brush and canvas it was measured at, and a claim about the
engine's behaviour that has no test behind it is marked as such. Sessions treat
these numbers as ground truth; two of them were.

## Worked examples and leakage

**8. Point at the paintings, under the protocol.**
Car wash: "no end-to-end worked example; the pears painting is effectively that
and the guide never points at it." Lighthouse: "the worked examples in
`paintings/` gave me the whole pass-script convention, and without them I would
have invented a worse one." So they help, and `PAINTINGS.md` is right that they
leak a subject.

The decide-then-read protocol resolves this: a painter who chose the subject
before opening the repository cannot be steered by a noun in a worked example.
Say so in `PAINTINGS.md` and in the front page — "if you chose your subject
before reading, these are yours to study; if you did not, they will choose it for
you" — instead of keeping the examples unreferenced. The no-nouns discipline in
the guide itself stays; it is for the reader who did not follow the protocol.

## What not to change

Every session, unprompted, defended the same things: the order of work; no layers,
no free undo, no black; rehearsal seeded as the next real strokes; `at_value`;
the place vocabulary; the values view as "the one that tells you the truth"; the
signature rule of choose-the-mark-first-explain-after. None of these should be
touched to make room for the above.

## A note on the unprompted stage, for LESSONS.md

Four decide-then-read runs: pears (cold), car wash ("not a standard subject"),
lighthouse (cold), sunset (older guide). Cold runs produce the most-painted subjects
in the corpus; one sentence of resistance produces a memory instead. The default is
one instruction deep. If the protocol wants to test the painter rather than the
prior without naming a subject, the lever is order, not content: ask for two
subjects and paint the second, or ask it to name the obvious choice and then not
paint it. Both are nudges away from the default rather than toward anything, and
the difference should be recorded when the run is.

---

# On the guide's length, and on a warnings file: two answers as actionable items

Two questions the repository's owner put to the third session's painter after its list
was written, with the answers turned into items. Each says whether it is measured or an
opinion; the numbers are the third session's and are in
`paintings/lighthouse_dusk/NOTES.md`.

**The question on length.** Every session says `PAINTER.md` is too long, every session
says the essay is what made the rules stick, and each attempt to shrink it has not
substantially shortened it. What should be done with it?

1. **Stop shrinking the essay, and say so in `LESSONS.md`.** Reading the guide, the
   reference, the calibration, the lessons and both earlier paintings' notes cost the
   third session a few minutes and roughly thirty thousand tokens, against a session
   that spent far more looking at its own rehearsals; every session that called the
   guide long read all of it and then credited it. The cost of length is not reading
   time. It is that a rule read once at the start is not present at the moment it is
   needed, and cutting cannot fix that, because the rule cut is the one some painter
   needed. Opinion, with that one number behind it. *Action: an entry in `LESSONS.md`
   under the growth rule: the essay is finished at its size, and a finding goes to the
   engine, the reference, the recipes or the calibration file, never to the essay.*
2. **Split by function, not by length, and move rather than cut.** `PAINTER.md` keeps
   the first hour, the six steps, *What you are bad at*, the checklist and the eight
   exercises, and nothing else. The essay — colour, wet paint, the brushes, the shape
   each tool leaves behind, the angle of the mark, looking, and the reasons under every
   rule — moves whole to its own file with one instruction at its top: read it once,
   after the exercises and before the painting. Procedures go to the `RECIPES.md` the
   synthesis above asks for. Nothing is deleted. The length then stops being a
   complaint, because nobody is asked to hold the essay in their head, only to have
   read it, and the two-goes instruction stops being an instruction and becomes the
   file boundary. Opinion. *Action: the move.*
3. **Give the front page a word budget that CI holds.** The no-growth rule is already
   in `LESSONS.md` and the guide doubled under it, from 8,600 words to 17,000; the
   third session's own list above asks for four more lines in it. A stroke budget works
   because the engine holds it, so hold this one the same way: `scripts/check_guide_blocks.py`,
   which CI already runs over the guide, fails when `PAINTER.md` is over its budget —
   five to six thousand words after the split, which is the synthesis's target. Any
   addition then has to be paid for by a cut, which is the rule the file already
   states and nobody has kept, the third session included. Opinion. *Action: the
   count in the check script, and the third list's four guide additions routed to the
   essay, the reference or the recipes instead.*
4. **Move rules into the engine, and delete their paragraphs in the same commit.**
   The only shrinking that has ever worked here is the engine absorbing a rule:
   `solid=True` took the load warnings, `scumble` took the gradient-tool warning,
   `cost_line` took the arithmetic, `cover` took the burying recipe. The next three,
   all already asked for above: the inward scumble warning when the brush is wider
   than three ring steps (engine item 1 of the third list, measured); a bristle laid
   under `size=0.025` saying it is a comb; and the subject's share of strokes printed
   against the plan (item 7 below). A rule the tool states at the moment of the call
   is method; the paragraph that only warned about it can go. *Action: one engine
   change per paragraph, the paragraph leaving in the same commit.*
5. **Test the split before believing it.** Two fresh sessions under the protocol in
   `LESSONS.md`: one given only the front page, the recipes and the reference, one
   given everything. The third session's guess, written down so it can be wrong: the
   first paints the masses as well and improvises worse, because the essay is where
   the judgement came from when no recipe existed for a rock or a cylinder — masses
   not marks, back to front, the tool leaves its own shape. *Action: the run and its
   write-up. Nothing in items 1–4 depends on the result except how firmly the essay
   is recommended.*

**The question on a warnings file.** Would a separate file of the warnings a painter
must keep in context help?

6. **Not as a file read at the start.** The third session had every warning in
   context for the whole painting — the guide never left its window — and laid a glow
   as a solid egg, facets as slabs and a picture in almost nothing but flat and round
   regardless. The front page lists the five mistakes, the checklist repeats them, and
   `LESSONS.md` records that a rule correct, well placed and repeated three times still
   failed every run. A fourth copy is the thing that file says does not work. Measured
   in the sense that the failures are in the session's notes. *Action: none. Do not
   add it.*
7. **A post-pass check in `easel run` instead: the warnings said by the tool, at the
   moment they apply, computed from the log.** What caught the third session's
   mistakes was never a sentence. It was a rehearsal looked at, and the one line `run`
   prints after every pass, the budget. That line can carry the rules the log can
   check: every mark in this pass used one brush at one size; `n` passes in this pass
   ran at the same angle; `n` marks under `size=0.02` before stroke 60; a bristle under
   `0.025`; the subject's share of strokes so far against the share in the plan, which
   needs the plan sheet to say which places are the subject. A linter for a pass, in
   other words, and each rule that becomes a check can leave the guide. Opinion about
   the mechanism; every input is already in the log — brush, size, path, colour and
   load per record. *Action: a `Session.report()` over the last pass, or `--check` on
   `run`, printed beside the budget line. Prototype it against
   `paintings/lighthouse_dusk/` by replaying its log pass by pass and printing what
   each would have triggered; the painter's own prediction is that it fires on
   one-brush brushwork in passes 3 to 5 and on the subject's share from pass 6 on.*
8. **A rules card in the system prompt, only if sessions run long enough to be
   summarised.** This is the one form of the file idea with a real mechanism: a
   session whose context is compacted loses the guide first, and a card of a few
   hundred words kept where a `CLAUDE.md` is kept survives compaction where the guide
   does not. The third session was never compacted, so it cannot say whether this
   happens. *Action: check the session transcripts for compaction before writing the
   card. If none was compacted, item 6 applies to this too.*
