# Suggestions for the engine and the guide, from the painting sessions

These come from one session: a still life painted from `PAINTER.md` alone, with no
reference photograph, through the shell path (`easel new` / `easel run`), in 224 strokes.
The painting and its scripts are in `paintings/windowsill_pears/`. Nothing else in the
repository was read before painting, so this is the guide judged on its own, which is
what it asks for.

Before writing this I ran a few probes to check the claims that depend on the engine
rather than on taste. Each claim below says whether it was measured or is an opinion.
Where I could not settle something, it is written as a question.

> **Status.** All twelve engine items are done; what each became is noted under it in
> **bold**. Of the twelve guide items, the ones that were corrections to something the
> engine does — the `overhang` line in 1, then 6, 7, 8 and 9 — are applied, along with
> 3 and 12, which the new verbs made writable. What is still open is editorial and
> stands on its own: items 2, 5, 10 and 11, plus the halves of 1 and 4 that were not
> corrections — the one-page reference, and a calibrated recipe for a soft patch.
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

   **Half done.** The `overhang` line is corrected, with the measurement repeated
   and the table in `CALIBRATION.md`. The one-page reference is still open.
2. **Make the exercises a gate, with the cost of skipping them.** I skipped all eight and
   went straight to the picture. The stripy curtain and the sun bars were both lessons
   the exercises teach, and together they cost more strokes than the exercises would
   have. Say that.

   **Open.**
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

   **Half done.** `scumble()` is the verb, with its cost, and the guide's soft-passage
   section is written round it. The calibrated recipe for a glow or a lit patch is a
   measurement job and is still open.
5. **A recipe for a cast shadow.** My first shadows were capsule-shaped slugs at the
   palette's darkest value; the second were still heavy. Two sentences would have saved
   eight strokes: a shadow on a lit surface is a step or two below the surface, not the
   palette's dark; lay it as a tapering stroke and lose its far end.

   **Open.**
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

    **Open.**
11. **Warn about recipes repeated over similar objects.** One shading recipe painted all
    three of my pears, and they read as three copies. The guide warns about mechanical
    marks; it could warn about mechanical objects too: vary one thing per object on
    purpose.

    **Open.**
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
painted from `PAINTER.md` with no reference photograph, through the shell path, in 185
strokes of a 300 budget. The painting and its scripts are in `paintings/car_wash/`.

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
2. **`block_in` should lay a solid mass when asked for one.** Either `density=1.0`
   implies `load=1.0, load_falloff=0.0`, or there is a `solid=True`. Measured above:
   fourteen times more even at no extra cost. I laid the entire near frame speckled and
   only found out by cropping into it; it reads as ash rather than moulded plastic.
3. **A small irregular mark.** The probe says the box has exactly one tip that does not
   repeat itself and it is a comb. Either give the round tips a per-mark silhouette
   wobble — `block_in` already has per-pass wander, and the reasoning in *Design notes*
   about why the bristle comb is redrawn per stroke applies here word for word — or add
   a verb for a clot. I wanted a small irregular bright mark about fifteen times, laid
   dabs twice, got a row of discs twice, and ended up inventing "a short fat stroke from
   a starved bristle". The probe says that was the only answer in the box.
4. **Do not inset a clean edge across the canvas boundary.** Clamp the inset where the
   outline leaves the canvas. Measured above; it cost me a repair pass and two strokes,
   and the repair then left a chisel end I had to fix as well.
5. **Number a rehearsal's looks in their own sequence.** `rehearse_NNN.png` would do
   it — `.gitignore` already expects that name. Six rehearsals of one pass and I could
   never put two of them side by side, which is what a scrap of canvas beside an easel
   is for.
6. **Let `cost()` say *why* a number is large.** It already warns at a share of the
   remaining budget. Three of my calls came in at four to twelve times the estimate a
   painter would make by hand, all from the same cause. "74 passes: crossed, stepping
   across 1.10 of width" would let the painter fix the call; the bare number sends you
   to redesign the shape.
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
2. **`load` belongs beside `density`, not only in the repair recipe.** One clause where
   masses are laid. Measured above.
3. **A checklist line for the tool's own shape at small scale.** *"Is any small mark a
   disc, a capsule or a rectangle — the tool's shape rather than the thing's?"* The
   warning exists in prose and in the *shape each tool leaves behind* table, I read
   both, and laid a row of discs twice anyway. The probe gives the number to put behind
   it.
4. **A checklist line about stopping.** The closing checklist has fourteen lines and
   none of them is about finishing. The guide warns at length about spending too much on
   detail and about reaching the subject too late; it says nothing about stopping early.
   I finished with **115 of 300 strokes unspent**, having already named the weakest
   passage in my own notes and then given it four more strokes. Proposed: *"You have
   named the weakest passage. How many strokes are left? Spend them there."*
5. **The lightest mass is a composition question that `compare()` answers by accident.**
   `compare()` told me the bloom was `0.12` below plan. What it was really reporting was
   that a different mass had become the brightest thing in the picture and the eye went
   to it — a composition fault, found by a value tool. The guide's *"is the thing you
   measured most carefully still the thing the picture is about?"* is the right
   question and it is one line, late, in a long section. In value terms it is cheap and
   checkable: *is the lightest mass in the picture the one you planned to be lightest?*
   `compare()` already holds the numbers.
6. **Does the pencil apply with no reference? The section does not say.** *Painting
   without a reference* says you are the reference and lists three things to do, all of
   them value work. It never mentions drawing. I did not draw, and told myself the
   previewed shapes were the drawing. Drawing is free and does not count against the
   budget, and a drawing would probably have caught my frame proportions before six
   rehearsals — **but I am not sure that is a recommendation rather than hindsight**,
   because a painter with no reference has nothing to check a drawing against, which is
   half of what the pencil is for with one. A question, not a request.
7. **A question about worked examples, which I think has no clean answer.** The guide
   has eight abstract exercises and no single small picture laid out in order, and
   sequencing was the thing I was least sure of at the start — not which call to make
   but which to make first. `LESSONS.md` is right that an example is read as an
   instruction and that a named subject leaks, and an end-to-end example would leak its
   subject harder than any fragment can. The paintings in `paintings/` already are that
   example and already carry that risk, unread. So: is `paintings/` meant to serve this,
   with the guide pointing at it — or is the sequencing meant to be worked out fresh
   every time, and the exercises deliberately abstract to keep it that way?

## What I would not change

The plan object shared by `cost`, `preview`, `rehearse` and `paint`. It is the best
thing in the engine: twenty-seven rehearsals, none of them charged, and a painting that
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
