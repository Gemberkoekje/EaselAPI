# Suggestions for the engine and the guide, from one painting session

These come from one session: a still life painted from `PAINTER.md` alone, with no
reference photograph, through the shell path (`easel new` / `easel run`), in 224 strokes.
The painting and its scripts are in `paintings/windowsill_pears/`. Nothing else in the
repository was read before painting, so this is the guide judged on its own, which is
what it asks for.

Before writing this I ran a few probes to check the claims that depend on the engine
rather than on taste. Each claim below says whether it was measured or is an opinion.
Where I could not settle something, it is written as a question.

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
2. **`paint(plan)`.** `cost`, `preview` and `rehearse` all take a plan of masses, sweeps
   and marks, and the guide promises "what you checked is what you paint, without
   rewriting it". That is true only for marks: a mass or a sweep in a plan has to be
   dispatched by hand to `block_in` or `sweep`, so I wrote my own runner. One method that
   paints any plan closes the gap and removes the drift the guide warns about.
3. **A budget on the session.** `Session(budget=300)`, with `easel run` printing spent and
   remaining, and `cost` flagging a call that would take more than some share. The guide
   asks the painter to write the split down; the engine could hold it.
4. **A soft-passage verb.** The guide is honest that there is no gradient tool, and its
   own remedy (steps, then a scumble of overlapping strokes at closely spaced values) is
   the one thing every painter needs and gets wrong first. `scumble(band, color_a,
   color_b, n)` that lays exactly that, charged as `n` strokes, would replace the loop the
   guide prints. My sun in the pane cost 27 strokes over two attempts; the first attempt
   was four hard bars, the loudest tell in the finished picture.
5. **A `cover()` verb for corrections.** The burying recipe needs a solid tip, `load=1.0`,
   `opacity=1.0`, `pressure="even"`, ends outside the area, and, as I found, also
   `load_falloff=0.0`: a full-width correction stroke with `load=1.0` still ran dry and
   left speckle at its far end. A verb with those defaults would make the commonest
   repair the one that needs no thought.
6. **Square-unit helpers.** `circle(center, r)` that is round on any canvas, or
   `ellipse(..., square=True)`, or a session-level unit option. I had to bake the aspect
   ratio into my own shape builder to get round pear lobes.
7. **Shape operations.** `union(a, b)` and `shape.smooth()` would have let the pears be
   two circles and a waist without a custom generator, and a smoothed polygon would have
   had a cleaner silhouette than the scalloped one a round tip leaves.
8. **A clean-edge option for shaped block-ins.** What finally gave the pears a smooth
   contour was: inset the shape by half the brush, block it in, then one `sweep` pass
   along the true outline in the same colour. Measured, that pass lays nothing outside
   the outline. `block_in(..., edge="clean")` doing those three steps would save the
   discovery.
9. **Two-way `palette.at_value(base, target)`.** The guide's helper only adds white and
   raises below the base. I needed to hit a value from either side on every mixture, and
   wrote one that mixes in the blue-umber dark to go down. It belongs in the palette.
10. **`compare()` against a plan, not only a photograph.** With no reference, the planned
    values existed only in my head and in `value_of` printouts; nothing checked the
    canvas against them. `compare({place: target_value, ...})` would give a painter
    without a reference the same table and heat map.
11. **A prelude for shell mode.** Helpers had to be loaded with `exec(open(...).read())`
    at the top of every pass. `easel run --prelude helpers.py`, or auto-loading a
    `prelude.py` in the session's directory, would do.
12. **Smaller time-lapses.** 235 marks made a 2.6 MB GIF. `every=` or `scale=` on
    `timelapse_gif`, alongside the `fps` it already has.

## The guide

1. **A one-page reference beside the essay.** The essay is good and its voice is what
   made the rules stick, but the operational facts are hard to find inside it: what
   counts against the budget, the defaults, what `overhang`, `density`, `opacity` and
   `load` do exactly, what pressure does on each kind of tip, which unit each argument
   is in. A table, either at the top or as a separate file, would have saved me guesses.
   The `overhang` line should be corrected with the numbers above.
2. **Make the exercises a gate, with the cost of skipping them.** I skipped all eight and
   went straight to the picture. The stripy curtain and the sun bars were both lessons
   the exercises teach, and together they cost more strokes than the exercises would
   have. Say that.
3. **Rehearse masses, not just features.** The guide teaches rehearsal for a feature
   smaller than a cell. The expensive mistakes are block-ins of big masses, which are
   cheap to repaint only until something stands on them. A rule such as "rehearse any
   block-in you will not want to repaint" belongs next to the two-`compare()` rhythm.
4. **A positive recipe for a soft patch, with its cost.** The scumble recipe is written
   for a join between two bands. There is no recipe for a glow, a sky, a lit patch on a
   surface. My second attempt (one region with a diagonal edge, inset, laid at 0.6
   opacity) was better than the first and still shows its pass ends. I do not know the
   right recipe; a calibrated one is worth a section.
5. **A recipe for a cast shadow.** My first shadows were capsule-shaped slugs at the
   palette's darkest value; the second were still heavy. Two sentences would have saved
   eight strokes: a shadow on a lit surface is a step or two below the surface, not the
   palette's dark; lay it as a tapering stroke and lose its far end.
6. **Small shaped masses with a round tip.** The guide's inset rule is under "Masses that
   are not rectangles" and the pears are exactly where I forgot it. Add the dotted-fringe
   symptom to "The shape each tool leaves behind", with the inset and the single-pass
   outline sweep as the remedy.
7. **The unit mismatch belongs under coordinates.** One sentence there, with the ellipse
   example, and a formula: a round radius `r` in x is `r * width / height` in y.
8. **Document `log(last=)`, `contact_sheet`, and `timelapse_gif(fps=)`.**
9. **Add `load_falloff=0.0` to the burying recipe.** Every other clause is there.
10. **A short path through the guide.** At 1600 lines it is a long read before a first
    stroke, and several rules appear three times in different words (painting up to a
    line, the box that should have been a shape, back to front). A "first hour" version
    of about a fifth the length, pointing into the full text, would get a painter to the
    exercises sooner without losing anything.
11. **Warn about recipes repeated over similar objects.** One shading recipe painted all
    three of my pears, and they read as three copies. The guide warns about mechanical
    marks; it could warn about mechanical objects too: vary one thing per object on
    purpose.
12. **A page for painting without a reference.** Half the precision tooling assumes a
    photograph. For a painter working from a subject in their head: print `value_of` for
    every mixture and for the ground, write the value plan down as numbers, check
    `look(values=True)` against it after every mass, and, if `compare()` learns to take a
    plan, use that.

## What I would not change

The look loop, the region crops, `rehearse`, `cost` on the preview, named mixtures that
persist, `value_of` for planning, back to front, the inside-of-a-hollow-thing rule, and
the closing checklist. Those carried the painting from an empty ground to a readable
picture without a reference, and the guide's warnings predicted most of my failures
before I made them.
