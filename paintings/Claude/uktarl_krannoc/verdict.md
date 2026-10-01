*The painter's own review of the tool, the documentation and its picture, written after
the export when the owner asked for its honest opinion and for a fix to every negative
point, and kept here verbatim: this is the message as the painter wrote it, taken from
its session, whose words match the owner's paste of it. Before writing it, the painter
checked the installed 0.8.0 package for what it already did — `easel run --help`, the
shape functions in `regions.py`, and the six documents' word counts — "so I don't
propose fixes for things it already does". Its measured claims were re-measured when the
painting was filed; what survived and what did not is in [`NOTES.md`](NOTES.md) and in
section 3 of the plan the round is worked from. The offer it ends on is this file:
the report is filed here, and nothing was posted.*

---

The tool's planning instruments are now good, and 0.8.0's additions earned their place. What it can't do with shapes and edges is the main reason the painting looks stencilled. The docs teach the right method but are far too long, and they lack recipes for a multi-figure scene like this one. The painting does its job at the table, but it's an illustration, not a painting.

## The tool

**What worked**
- **`s.thumbnail()`** was the most useful addition. Before any paint it showed Uktarl's face disappearing into the glow behind it, and the doppelganger's ears reading as cat ears.
- **Rehearse, then commit.** The `dearest:`, `landed nothing:` and "took N details out of sight" lines named every expensive or wasted call by its script line. I never needed `undo`.
- **Guides** stayed readable over paint from start to finish.
- **`at_value` mixing and a swatch strip** made planning by value easy, and the strip caught grey faces before they were painted.
- **A clip-held flat stroke** is a superb stencil: the sunburst's rays cost 13 strokes.

**Negatives, most important first**

1. **You can't paint outside a shape.** `clip=` takes a place, or the overlap of several, but there's no exclusion and no `difference()`. To light the wall around Uktarl after painting him, I typed three polygons by hand that share his outline. One of them left a hard seam where it ended.
   - *Fix:* add `clip_out=shape`, plus `difference(a, b)` and `intersection(a, b)`, built on the same mask `union()` already makes.
2. **Edges are hard or ragged, never soft.** `feather=` breaks an edge; it doesn't soften it. Losing an edge costs a smudge per tenth of the canvas, so `edge="hard"` is the easy path. I ended with 59% crisp edges, and the picture reads as cut paper.
   - *Fix:* add `edge="soft", soft=<px>`, a held edge whose mask fades over N pixels. Or add a verb that loses any length of an outline, priced by length.
3. **The habit warnings misfire often enough that I stopped reading them.**
   - "One disc printed" flagged 28 marks, 21 of them the eyes, brows and mouths of three faces.
   - "Graded passage comes back as bars" fired on a hood and the face beside it.
   - "Stack of bars" fired twice, in a picture crossed by radial rays.
   - *Fix:* compare the shapes that actually landed, not size ratios. Require the bars rule's marks to share one mass. Let a painter dismiss a habit once per painting.
4. **Rehearsal looks can't be cropped or cleaned.** `easel run --rehearse` always shows the whole canvas with guides and labels; a label sat right on the 48-px face. I wrote a small look script for every close-up.
   - *Fix:* give `run --rehearse` the `--region`, `--no-sketch`, `--no-marks` and `--scale` flags that `easel look` already has.
5. **There's no rotation and no local frame.** I wrote the same helper three times: a head drawn in its own radii, then tilted and placed.
   - *Fix:* add `.rotated(deg, about=)` on shapes and groups, and a `frame(centre, rx, ry, tilt)` that takes local coordinates.
6. **The budget is planned as one number.** `subject_share` can't express "four figures and a wall". By the time the other three were begun, Uktarl had 102 marks; the last figure got 22 and is the weakest.
   - *Fix:* `s.plan(shares={...})` keyed by `note=`, with a running line of spent against planned for each.
7. **Concave shapes are priced by the whole strip their passes sweep.** The V-shaped collar cost 43 strokes; split into two flaps, about 10. The first mountain pass, with ten facets, cost 129.
   - *Fix:* a notice when a mass fills only a small share of what its passes cover.
8. **"No clear light" can't be satisfied by a mostly dark picture with small bright lights.** It isn't low-key by the definition, so the line repeats even when the declared light reads 0.69.
   - *Fix:* whenever `lightest=` is declared, judge whether that light stands clear of its surroundings, under any key.

## The documentation

**What worked**
- **RECIPES.md** is the most valuable file. These landed first time:
  - the light's pool, on both the relief and the table
  - the projection for a scene with straight edges
  - the terminator join on the cape lining
- **The face recipe's** structure (shadow, half-tone band, lit plane sharing one edge) was right. It only needed adapting for light from below.
- **REFERENCE.md's tables** answered every lookup, and PAINTER.md's order of work is right.

**Negatives**

1. **Volume.** The package ships about 90,000 words. I read about 30,000 before the first mark, and the rules I actually used would fit on two pages. The 0.8.0 changelog entry alone runs to thousands of words.
   - *Fix:* a one-page card (the loop, the order of work, about 15 call signatures, and the numbers that matter). Put a ten-line "what's new for a painter" at the top of each release entry.
2. **The instruction comes last.** Sentences stack qualifications, measurement history and cross-references ahead of the rule.
   - *Fix:* state the rule first, then the number, then the history if it's needed at all.
3. **The pixel advice contradicts itself.** PAINTER still says "You cannot reason in pixels", while 0.8.0 adds `s.px()`, and the last two painters drew figures in pixels without trouble. Absolute placement in an unseen picture is what fails, not pixels.
   - *Fix:* say exactly that, and add a recipe for drawing a thing in its own frame.
4. **Missing recipes for things I hit:**
   - lighting the wall around a figure that's already painted, since backlight reverses the back-to-front order
   - a multi-figure scene: a budget per figure, several faces lit from one source, varying the figures
   - a hollow thing seen low, where the near rim hides the bottom
   - a face lit from below, where the light line must sit at the brows or the eyes turn into a mask band

## The painting

It works as a table handout, not as a painting.

**What works**
- The rays meeting behind Uktarl's head read even at thumbnail size, so the reason I chose the subject comes through.
- The red collar framing the white face is a real focal point.
- The lighting is consistent: a lantern behind him and a candle in front, with matching rims and pools.
- The palette is coherent, and the card game tells the story.

**What doesn't**
- **It looks stencilled.** Nearly every mass is a hard-edged flat, and I softened two edges in the whole picture.
- **The figures are the weakest part.**
  - The bodies are cut-out silhouettes: Uktarl's is a tombstone shape, his arm a ribbon, the hands ovals.
  - The faces are masks.
  - The nearest bandit reads as the back of a bald head.
- **The relief is unconvincing.** The rays are mechanically regular, the mountain is a flat cutout away from Uktarl, and the dwarves are pegs.
- **The tub only reads close up, and the table floats.**
- **It's dark overall.** On a projector it may go muddy.

**My faults, not the tool's**
- I let the first figure eat the budget.
- I painted ten sliver facets where the recipe says three or four planes.
- I put six strokes of coins and cards where the nearest bandit then hid them.
- I left the table top near the candle 0.18 darker than planned.

If you want this filed beside the painting, like the earlier `answers.md` files, I can save it there as `verdict.md`.
