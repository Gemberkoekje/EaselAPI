*The painter's own review of the tool, the documentation and its picture, written after
the export when the owner asked for its honest opinions and its suggestions, and kept here
verbatim: this is the message as the painter wrote it, taken from its session, whose words
match the owner's paste of it word for word. Its measured claims were re-measured when the
painting was filed; what survived and what did not is in [`NOTES.md`](NOTES.md). The
question it ends on was answered by the owner: the report is filed here, and nothing was
posted.*

---

Overall, the engine is more capable than my painting shows. Its weakest point is the one step it can't help much with yet: drawing a complex shape as coordinates.

## The tool

**What's genuinely good:**
- **Rehearsing a pass is the best feature.** I rehearsed about twenty times and committed only seven passes. All four failed versions of the creature cost nothing, and that fits exactly how I work: try, look, revise.
- **The warnings are accurate and actionable.** Each one came with a measurement and a fix. Examples:
  - the value plan flagged "plinth side and floor 0.03 apart" before a single stroke;
  - `inward-comb` told me the exact number of rings to use;
  - `glaze-far` pointed me to `to_value=`, which fixed the plinth shading in one call.
- **Mixing to a value (`at_value()`) is exact.** The value-scale exercise hit every target to two decimals. I plan in numbers, and the palette delivers them.
- **The paint physics shows wherever you let it.** The wall's strokes, the dry brush on the plinth and the beam of lit air all look painted, and I did nothing special to get that.
- **Shapes and holds compose well.** Copies shifted with `shifted()`, held with `clip=` and `edge="hard"`, are what made the final lighting possible.

**Where it made things hard:**
- **Guide lines vanish on a dark canvas.** I had to judge my drawings on a separate throwaway canvas with a light ground.
- **`pencil()` smooths its path by default.** In my drawing check a box came out as a rounded pot. Shapes built from polygons should keep their corners.
- **Cost is hard to predict.** The subject pass rehearsed at 85 to 113 strokes, and the report didn't say which call ate them. That's partly my fault, since I didn't use `cost()` before each mass.
- **Nothing warned me about highlights mixing into wet paint.** They landed at 0.52 instead of 0.64 until I added `dry()`. The engine knows how wet the canvas is under a mark, so this could be a warning like `glaze-far`.
- **"No clear light" can't be switched off for a dark picture.** A buried ground can be declared in the plan; a low-key picture can't. The "lightest" check also averages the whole place, so the dark eye sitting inside the head's top pulled it down.

## The documentation

**Strengths:**
- **`PAINTER.md` is a real method, not an API tour.** The "what you are bad at" section describes models like me accurately. I painted no boxes (0 of 17), because it warned me.
- **The "failed twice, the fault is upstream" rule saved the painting.** After the cat and the spotted cow I went back to the drawing and the value plan, not the brush.
- **The recipes are directly usable.** The beam of lit air worked on the first try, and the "goes wrong as" examples show you the failure before you make it.
- **The reference is precise where it matters.** The units table, and the table of which side a stack of passes starts on, were both essential.

**Weaknesses:**
- **It's long.** I read roughly 20,000 words before the first stroke. A good share is commentary on the docs themselves ("every rule is stated once", "this file has stopped calling them a gate") and painter anecdotes. A few anecdotes persuade; dozens cost context.
- **Some passages are hard to parse.** The paragraph on the post-pass check lists ten rules with their thresholds in one block; a table would read far faster.
- **The hardest part of my session has the least guidance.** Most of my trouble was getting a creature's silhouette to read, and neither the recipes nor the exercises cover it. The guide deliberately avoids naming subjects, but a recipe for any complex organic silhouette would be subject-neutral.
- **I never found `feather=` as a softening tool.** It might have softened my hard boundaries between light and shadow, but the "form that turns" recipe only mentions join strokes.

## The painting

**What works:**
- **Composition:** the subject left of centre, the column on the right, and the beam as a diagonal crossing the horizontal bands.
- **Value plan:** low-key, with the glow behind the head so the lit edges read against it.
- **The plinth,** built from planes, reads as a carved block.
- **The ember eye** is the one saturated accent in the picture.

**What doesn't:**
- **The creature looks like a vinyl toy, not weathered stone.** It's flat grey fills with a hard, even rim of light. That's my doing: I held every zone with a hard edge, and the engine looks least painted exactly where I held everything to a polygon.
- **The anatomy is stiff.** The head reads as a goat more than a gargoyle, the legs are sticks, and the profile pose is rigid. It's more cute than eerie.
- **The give-aways are too small for a projector.** The eye glint and the claws are a few pixels across. The reason the picture exists is in it, but only on close inspection.

It's usable as the pack's sample art, and "painted with the project's own engine" is a nice story, but I wouldn't call it good art.

## Suggestions, most useful first

1. **A free silhouette and value thumbnail at drawing time**, say `s.thumbnail(masses, values)`. It would show the planned masses as flat values in a small image, which is the painter's classic notan. The cat ears would have been obvious before a single rehearsal.
2. **Guides visible on any ground**, for example drawn with a contrasting halo. Also let `guide()` and `pencil()` take a shape directly and draw its exact outline.
3. **A per-call cost breakdown in the rehearsal report**, naming the few most expensive calls.
4. **A warning when a light mark lands in wet paint**, with `dry()` as the fix.
5. **Declaring a low-key or high-key picture in `plan()`**, and measuring "lightest" by the brightest part of a place rather than its average.
6. **A recipe, or a helper, for lighting any silhouette from one side**, using the shifted-copy technique, plus a note on `feather=` for softening held boundaries.
7. **A silhouette-readability exercise**, and a recipe for complex organic silhouettes.
8. **A leaner `PAINTER.md`.** Keep a self-sufficient first page, move most anecdotes and commentary on the docs into `CALIBRATION.md` or `LESSONS.md`, and turn dense paragraphs into tables.

Shall I write this up as a painter's report in the painting folder, or as issues on EaselAPI? Issues would be posted publicly under your account, so I'd only do that on your go-ahead.
