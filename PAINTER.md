# Painting with Easel

You are about to paint. Not draw, not render — paint. This file is the method: the
loop, the order of work, the mistakes you will make, nine exercises, and a checklist.
Read *The first hour*, paint the exercises at the end, then read
[`PAINTING.md`](PAINTING.md) once and start. Come back here while you paint; open the
other files when a situation calls for one.

| File | What it holds | When |
|---|---|---|
| **`PAINTER.md`** — this one | the method: the loop, the order, the mistakes, the exercises, the checklist | now, and open beside you while you paint |
| [`RECIPES.md`](RECIPES.md) | one situation at a time: the calls in order, what it looks like when it goes wrong, and the number behind it | when you are about to lay one |
| [`PAINTING.md`](PAINTING.md) | how the paint, the brushes and the planning tools behave; copying a photograph, in its last chapter | once, after the exercises; the last chapter only if you have a photograph |
| [`REFERENCE.md`](REFERENCE.md) | every fact on one page: units, defaults, what each argument does | when you want to look something up |
| [`CALIBRATION.md`](CALIBRATION.md) | the measurement behind every number quoted in the other four | when a number is the question |

**Every rule in these five files is stated once, in the file it belongs to, and linked
from everywhere else.** A number quoted here is measured there. If a rule seems to be
missing from this file, it is in one of the others, on purpose.

**One thing to settle before you read further: have you decided what to paint?** If
you have, [`paintings/`](paintings) is open to you — finished pictures with the pass
scripts that built them, the prelude of mixtures and masses beside them, and the
painter's own notes. They are the end-to-end worked example this file cannot be. **If
you have not decided, do not open them.** They name their subjects, and a named subject
chooses for you. Decide first, then look.

---

## The first hour

**What this is.** Brushes carry a finite load of paint and run out. Paint lands wet and
mixes with what is already there. The canvas has tooth. There are no layers, and undo
is scraping the canvas rather than a free rewind: **when something is wrong, you paint
over it.** You work in passes and you look between them.

```python
from easel import Session, cell, span, blob, region

s = Session(1024, 768, texture="linen", ground="toned_grey", seed=7, budget=300)
s.palette["dark"]  = s.palette.mix("ultramarine", "burnt_umber", 0.45)
s.palette["light"] = s.palette.tint("yellow_ochre", 0.55)
```

Coordinates run `0..1` from the top-left. A place is `cell("D5")`, `span("C3", "F6")`,
`region("lower-half")` or a shape. Say a place; do not compute a coordinate.

**The loop.** **Look every 5 to 15 strokes.** `s.look()` writes a PNG and returns the
path; open it. `s.look(values=True)` is greyscale, and it is the one that tells you the
truth. A stroke you did not look at was a guess. **Rehearse every pass before you pay
for it.** `s.rehearse(plan)` paints the plan on a copy and shows you the result; from
the shell, `easel run pass.py --rehearse` does it for a whole script. A rehearsal costs
a look and commits nothing, and what it shows is what will land.

**What a mark costs.** `stroke`, `dab`, `smudge` and `glaze` are one each. `block_in`,
`sweep`, `scumble` and `cover` are one *per pass* — ten to thirty for one call, and the
number nobody can guess: `s.cost(plan)` says, and `s.cost_line(plan)` says why. Drawing,
looking, drying and planning are free.

```python
plan = [{"shape": blob(cell("D5"), 0.12, seed=3), "brush": "bristle",
         "color": "dark", "size": 0.09}]
s.cost(plan)                  # what it charges
s.preview(plan)               # where it would go
s.rehearse(plan)              # what it would look like
s.paint(plan)                 # the same plan, now paid for
```

**The order. It is the whole method, and it is not optional.**

1. **Draw it first, in graphite.** `s.pencil()` is free. Put the arrangement down,
   look, move it, and keep drawing until it is proportional and the way you want it.
   Nothing you paint later fixes a composition you did not draw.
2. **Big masses first, in the biggest brush you will use**, at `density` below 1 so the
   ground breathes through. Two or three of them. Not outlines — masses.
3. **Back to front.** The furthest thing goes down first and every nearer thing is
   painted over it. Nothing is cut around.
4. **Check the values before anything else.** In greyscale, a clear light, a clear mid
   and a clear dark. Two masses closer than `0.10` in value read as one.
5. **Then the mid-tones**, across the whole canvas, each mass along *its own* axis. A
   soft passage is overlapping strokes at close values, not a smudge.
6. **Edges last but one.** Hard edges pull the eye; soft and lost ones let it move on.
7. **Highlights last, smallest brush, fewest strokes.** Ten deliberate marks.

```python
far  = blob(span("B2", "G4"), wobble=0.3, seed=1)
s.block_in(far, "bristle", "dark", density=0.8, size=0.18, direction="axis")
s.look(values=True)                                  # before anything goes on top
s.block_in(span("A5", "H8"), "flat", "light", size=0.14, solid=True, direction=6)
```

**Before the first stroke.** Count the horizontal bands in the drawing; more than
three, and find a viewpoint or a thing that crosses them while it is still graphite.
Write the three values down as numbers, and the split of the budget as numbers.

**The five things you will get wrong.** Each has been made by every painter so far, so
the fix is on the same row as the mistake.

| The mistake | What it looks like | Do this instead | Where |
|---|---|---|---|
| **Outlines, filled in** | a coloured shape with a drawn edge; a thin dark line run along a silhouette to sharpen it | paint the mass with a brush wide enough to cover it in a few strokes; sharpen an edge by painting the mass on the *other* side of it | *What you are bad at*, below |
| **Boxes** | rectangles, especially in the background, which nobody made you draw | `blob`, `ellipse`, `hull`, `ribbon`, `polygon`; check the background hardest | *Masses that are not rectangles* in [`PAINTING.md`](PAINTING.md#masses-that-are-not-rectangles) |
| **Parallel marks** | hatching; a grain repeated thirty times; a soft passage laid as three hard bands | vary the direction; two directions break a comb; a soft passage is `s.scumble(...)` | *The angle of the mark* in [`PAINTING.md`](PAINTING.md#the-angle-of-the-mark); *A quiet gradient* in [`RECIPES.md`](RECIPES.md#a-quiet-gradient) |
| **Reaching for `undo`** | a scraped canvas and a stream of marks put back one at a time | `s.cover(place, colour)` buries a mistake; keep each mass in a named function and re-run the stack | *A repair under things that are standing on it* in [`RECIPES.md`](RECIPES.md#a-repair-under-things-that-are-standing-on-it) |
| **The tool's own shape** | floating discs; capsules; a rectangle with chisel ends; a staircase down a sloped boundary | give a mark a length, or `tip_wobble=0.7`; run passes along a sloped boundary, or `edge="hard"`, which masks the paint to the outline. `report()` counts the discs for you | *The shape each tool leaves behind* in [`PAINTING.md`](PAINTING.md#the-shape-each-tool-leaves-behind) |

**When you think it is finished**, the checklist is at the end of this file. Two of
its lines are about finishing rather than about faults: the last third of the budget
goes on what surrounds the subject, and the last marks are about the picture, not the
score.

**Now go and paint the nine exercises**, at the end of this file. Then read
[`PAINTING.md`](PAINTING.md) once, and start.

---

## Getting started

```python
from easel import Session

s = Session(1024, 768, texture="linen", ground="toned_grey", seed=7)
```

Coordinates are always `0.0` to `1.0`, origin **top-left**. `(0.5, 0.5)` is the
centre, `(0.9, 0.1)` the top right. There are no pixels anywhere in this API.

**Both axes run 0–1, so on a canvas that is not square the same number is a different
distance in each.** Brush sizes are a fraction of the canvas's **long side**, so a
brush is round, but `ellipse(p, 0.1, 0.1)` is an oval. Rather than do the arithmetic,
ask the session:

```python
s.circle((0.5, 0.5), 0.09)                 # round in pixels, on any canvas
s.circle(cell("D5"))                       # the biggest circle that fits the cell
s.circle((0.5, 0.5), 0.09, wobble=0.25)    # round, with a silhouette nobody drew
```

Grounds: `white`, `warm_white`, `toned_grey`, `toned_warm_grey`, `burnt_sienna`,
`umber_wash`, `cool_grey`. Textures: `smooth`, `linen`, `rough`. **Start on a toned
ground.** A mid-tone ground means your first marks already sit in a value relationship,
and any ground left showing reads as a colour you chose; on white every gap is a hole.
A picture whose masses all sit below the presets wants a ground of its own:
`Session(ground="#5a5045")` reads `0.32`, and `value_of` will tell you any other.

---

## The workflow

The order oil painters have used for centuries, for the same reason it works here: it
keeps you making *large* decisions before *small* ones, so a mistake is cheap for as
long as possible.

### 1. Draw the arrangement in graphite

`s.pencil()` puts graphite into the canvas — no paint, no wetness, and it does not count
as a stroke, so the drawing is free. **Draw the arrangement before you commit paint to
it, and keep drawing until it is proportional and the way you want it.** A rehearsal
shows you one answer; a pencil shows you six at once, and moving a mass in graphite
costs nothing where moving it in paint costs the mass and everything standing on it.
Put the big shapes down, look with the grid on, move them, look again. Try a silhouette
three ways before you build it as a shape:

```python
for wobble in (0.0, 0.18, 0.34):                     # three candidates, one look
    s.pencil(blob(span("E4", "G7"), 0.16, wobble=wobble, seed=4).closed, pressure=0.5)
s.look(region=span("E4", "G7"))                      # pick one, erase the others
s.erase(span("E4", "G7"))
```

Four things about the drawing:

- **Count the horizontal bands in it before the first mass.** More than three, and find
  a viewpoint or a thing that crosses them now, while it is graphite. A frontal
  elevation is a layer cake before a brush is picked, and no brushwork gets it back.
- **If the scene is built of straight edges that converge, write the projection before
  you draw anything.** You are reliable about sizes and distances and unreliable about
  where they land on the canvas (*A scene with straight edges* in
  [`RECIPES.md`](RECIPES.md#a-scene-with-straight-edges)).
- **Draw the planes of anything built from them with its silhouette**, not after the
  mass is down (*A mass built of planes* in
  [`RECIPES.md`](RECIPES.md#a-mass-built-of-planes)).
- **Landmarks before anything, pencil after the far masses, near masses on top.** Paint
  buries graphite in proportion to how much lands, and a full-strength block-in buries
  all of it; a `mark()` is a point and cannot be buried. So draw the whole arrangement
  now to judge it, and draw the near things *again* once the far masses are down —
  unless you draw it with `s.guide()`, which is `mark()` along a path: graphite on the
  view rather than in the canvas, so `look()` keeps showing it, `export()` never does,
  and the arrangement drawn here is still there at step 7. Use `pencil()` for the
  underdrawing that should show through thin paint, and `guide()` for the scaffolding
  that should not be in the picture at all.

The two passages you do not draw are the two that will come out weakest. Draw the small
things too — a lid, a handle, what stands in a thing — before the pass that paints them.

### 2. Tone the ground, then find the big shapes

Two or three masses. Not outlines — **masses**, in the biggest brush you will use in
the whole painting, blocked in with `density` below 1.0 so the ground breathes through.

```python
s.palette["dark"] = s.palette.mix("ultramarine", "burnt_umber", 0.45)
s.block_in(blob(cell("D5"), 0.26, wobble=0.3, seed=2), brush="bristle", color="dark",
           density=0.7, size=0.2, direction="axis")
```

**`density` spaces the passes; it does not fill them.** Every pass runs dry along its
own length whatever the spacing, so `density=1.0` lays a mottled mass with a twentieth
of the ground still showing. When a mass has to be solid — because it is near, or fine
marks will stand on it — say `solid=True`. Not for these first masses. A solid mass
still shows its pass structure at about `0.03` of value, which is faint striping on a
large flat plane and invisible on anything with a form; hide it with a bigger brush or
a broken one, never with an argument (*`block_in`* in
[`CALIBRATION.md`](CALIBRATION.md#block_in)).

A place can be a rectangle — `cell("D5")`, `span("E5", "H8")`, `region("lower-half")`
— or a shape: `blob`, `ellipse`, `hull`, `ribbon`, `polygon`. Most masses are shapes,
and a shape's passes stop at its own silhouette. What a shape costs and how far paint
lands outside it is *Masses that are not rectangles* in
[`PAINTING.md`](PAINTING.md#masses-that-are-not-rectangles).

Resist detail here. If you can already name what you are painting, you have gone too
far too early.

### 3. Paint from back to front

**Lay the furthest thing first and let each nearer thing be painted over it.**
Background, middle distance, foreground, then the small shape standing in front of all
of them.

```python
s.palette["far"]  = s.palette.tint("cerulean", 0.55)
s.palette["near"] = s.palette.desaturate(s.palette["far"], 0.4)

s.block_in("upper-half", "flat", "far", size=0.18)          # furthest
s.block_in(span("A4", "H6"), "flat", "near", size=0.16)     # nearer
s.stroke([(0.3, 0.42), (0.3, 0.78)], "bristle", "dark", size=0.03)   # in front
```

The narrow shape's edges are now real edges — the place where its paint stops and the
mass behind it still shows — and you drew none of them. Paint it first and the only way
to get the same edges is to cut the mass behind it carefully around it, which is
painting *up to* a line.

Three things follow:

- **Let the near mass overlap.** Run it a little into the far one. A silhouette that
  stops exactly on a boundary was measured; one that overlaps was painted.
- **A veil of light is a mass at a depth.** A glaze laid last because it is *light* is
  still in front of something. `look(diff=True)` shows what a pass covered.
- **A mistake in the background is cheap while the foreground is not there yet**, and
  stops being cheap the moment something stands on it. So fix a mass *before* the near
  things go on, and keep every mass in its own named function so the whole stack can be
  re-run in depth order when a repair is needed later (*A repair under things that are
  standing on it* in [`RECIPES.md`](RECIPES.md#a-repair-under-things-that-are-standing-on-it)).

**Anything with an inside has its own depth order: the far edge, then what is inside,
then the near edge.**

```python
far  = ellipse(span("D2", "F3"))          # what stands behind the inside
near = polygon([(0.36, 0.31), (0.64, 0.31), (0.62, 0.72), (0.38, 0.72)])

s.block_in(far, "flat", "pale", size=0.04)                 # behind the inside
s.block_in(far.inset(0.015), "flat", "dark", size=0.04)    # the inside
s.block_in(near, "flat", "light", size=0.06)               # in front of the inside
```

Painted the other way round there is nothing for the inside to stop against. Ask it of
anything you can see into, before the first stroke: what is behind the inside, what is
the inside, and what is in front of it? One broken catch-light along the near edge
finishes it (*A hollow thing* in [`RECIPES.md`](RECIPES.md#a-hollow-thing)).

### 4. Check your values before you check anything else

```python
s.look(values=True)
```

Greyscale is what squinting does for a painter, and **value structure is what makes an
image read.** If the greyscale is mush, no colour will save it. A painting usually
wants three clearly separated values: a light mass, a mid mass and a dark.

**Plan those three as numbers, before you mix anything.** `palette.value_of(c)` reports
exactly the value the greyscale view will show, and `palette.at_value(base, target)`
hands back the mixture of `base` that reads at `target`, from whichever side it starts:

```python
p = s.palette
p["dark"] = p.mix("ultramarine", "burnt_umber", 0.55)
p["mid"]  = p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.35), 0.40)
p["lit"]  = p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.40), 0.74)
for name in ("dark", "mid", "lit"):
    print(name, p.hex(p[name]), round(p.value_of(p[name]), 2))
```

**If two of your three are within `0.10` of each other, they will not read as separate
masses** however different their colours — but only where the two places actually
meet. Put the plan through `compare()` on the empty canvas: it lists every two places
planned within `0.10`, marks each pair `(touch)` or `(apart)`, and names the touching
ones as the ones that will read as one. Two rounds of painters were asked that
question instead of told the answer and both got it wrong.

```python
upper, lower = span("A1", "H4"), span("A5", "H8")
s.compare({upper: 0.72, lower: 0.38})       # the sheet, the outlines, and the pairs
```

The keys are places and the values are what `value_of` reports, so the plan is a few
lines written before you start and checkable after every mass. **Re-read the places
whenever you move a silhouette**: a place is a rectangle, and one that now straddles two
masses reports their average in a confident voice.

**The threshold is a floor, and a mass also has a ceiling.** Shading a mass to give it
form spends value range, and the range is shared: shade until the form clears `0.10`
and stop, because past about `0.15` across one mass its shadow side starts closing on
whatever it stands against.

**The box has no black, and does not need one.** `mix("ultramarine", "burnt_umber",
0.5)` is the bottom of the range at `0.14`, and varying the ratio holds the value while
swinging cool to warm. Piling on passes will not go lower; if a mass is not dark
enough, mix it darker. A reference darker than that is usually still reachable by
*covering* the place, at `density=1.0` and full load, with nothing lighter showing
through; a colour you supply lands as written, black included, and a mixed dark is
alive where a tube black is dead (*Colour* in [`PAINTING.md`](PAINTING.md#colour)).
`at_value` raises when a value is out of reach rather than handing back the nearest it
managed.

**A cast shadow is the first place you will spend that dark, and it is the wrong
place.** A shadow lying on a lit surface is **a step or two below the surface**, mixed
from that surface's value rather than from the bottom of the box — and it is a tapering
stroke that loses its far end, not a filled shape, which comes back as a slab with two
hard ends.

```python
dark = p.at_value("surface", p.value_of("surface") - 0.18)      # a step or two
s.stroke([(0.55, 0.30), (0.66, 0.38), (0.80, 0.46)], "flat", dark,
         size=0.085, pressure=[1.0, 0.6, 0.0])                  # and lose the far end
s.stroke([(0.55, 0.305), (0.62, 0.35)], "flat", p.at_value(dark, 0.38),
         size=0.05, pressure=[0.9, 0.0])     # darkest where the two things meet
```

**A cool mass on a warm ground reads about two steps lighter than it measures.** When
your eye says a mass is far too light and `compare()` says it is inside `0.05`, believe
the number.

### 5. Refine the mid-tones

Now the middle values, with a medium brush (`size≈0.08–0.12`), across the whole canvas
rather than finishing one corner — a painting should come up all at once. Look every
ten strokes or so.

**There is no gradient tool.** Nothing here grades a mass smoothly from one value to
another. What a painter does instead is paint the gradient as **steps and then lose the
joins**, while the paint is wet:

```python
steps = [(cell("D4"), "dark"), (cell("D5"), "shadow"), (cell("D6"), "light")]
for place, value in steps:
    s.block_in(place, "flat", value, pressure="even", size=0.03)
s.smudge([(0.42, 0.50), (0.46, 0.62)])              # walk each join once, while wet
```

**One smudge removes about 40% of a step, once, and a second pass undoes most of the
first** (*`smudge`* in [`CALIBRATION.md`](CALIBRATION.md#smudge)). When once is not
enough, stop smudging and lay paint: many overlapping strokes at closely spaced values.

```python
s.scumble(span("A4", "H6"), "shadow", "light", 8)    # close the join with paint
```

Eight passes running along the band and stepping across it, one value step per pass,
each wider than the step so the joins close. Leave `size` off: the verb picks its brush
from its own step, and a brush narrower than twice the step brings the bars back. Below
about five passes the steps read as steps again.

**A passage that is light in the *middle* is the same verb turned inward** — a lit
patch, a bloom, light falling on a surface is dark at every edge:

```python
s.scumble(patch, "shadow", "light", 8, direction="inward")   # 8 strokes, lit in the middle
```

The first ring lands on the boundary, so give it the value the patch meets its
surroundings at. Do not lay it as strokes radiating from the centre, which draws a
daisy. Light *in* the air rather than on a surface — a beam, a halo seen from outside —
is glazes, not this verb (*A volume of lit air* in
[`RECIPES.md`](RECIPES.md#a-volume-of-lit-air)).

**This matters more than it looks**, because a wide soft passage is where a picture's
structure comes from. A field gradated top to bottom is a stack of horizontal bands
until its joins are gone and something crosses it, and a stack of bands is a
composition whether or not you meant one (*A graded field that is most of the picture*
in [`RECIPES.md`](RECIPES.md#a-graded-field-that-is-most-of-the-picture)).

### 6. Edges: lost and found

The step that separates a painting from a diagram, and the one you will be most
tempted to skip. **Hard edges pull the eye; soft and lost edges let it move on.**
Decide where you want attention, make those edges hard, and lose the others — let two
masses merge with no boundary at all in places.

```python
s.smudge([(0.3, 0.4), (0.45, 0.44)])                # soften an edge
s.stroke([(0.6, 0.3), (0.62, 0.5)], "round_hard", "dark", size=0.02)  # sharpen one
```

Three things about `smudge`:

- **Leave `size` off.** What it buys stops at about `0.02`, the default; what it costs
  — how far it drags the light mass into the dark — keeps growing with the brush.
- **Run it *along* a boundary, never across one.** Dragged across, it pulls a lobe of
  the lighter mass into the darker and leaves a finger-shaped thumbprint.
- **Along means along the boundary's own shape.** Only a straight boundary is two
  points; hand a curve its points, or hand it the mass and it walks that outline.

```python
s.smudge([(0.30, 0.40), (0.38, 0.41)])             # a straight edge is two points
s.smudge([(0.30, 0.40), (0.45, 0.45), (0.60, 0.53),
          (0.73, 0.63)])                            # a curved one is the curve
s.smudge(mass)                                     # a shape is already that curve
```

One pass, not three. If the boundary is still there afterwards, the answer is paint
laid across it, not another smudge (*An edge that is actually lost* and *A mark that
crosses a boundary* in [`RECIPES.md`](RECIPES.md#an-edge-that-is-actually-lost)).

An image where every edge is equally sharp looks like clip-art. Lose one edge
completely rather than four edges partly.

### 7. Highlights last, smallest brush, fewest strokes

The lightest lights and the sharpest accents go on at the end, and there should be very
few of them. Every highlight you add makes the others count for less.

```python
s.dab(0.62, 0.35, "round_hard", "titanium_white", size=0.015)
```

**Anything the size of a cell or smaller is three marks at most — the dark, the light,
and the edge between them** — laid dark first, and looked at through a `region=` crop
before the light goes on. `size` is the *feature's* fraction of the canvas, not the
mass's. A small mark that has to land is `press=3`; a lighter touch is a whisper, and a
dark accent at `press=2` on a lit passage may not register at all (*Pressure* in
[`PAINTING.md`](PAINTING.md#pressure)).

---

## What you are bad at, and what to do instead

Be honest about these. They are specific to what you are, and every painter so far has
made each of them after reading about it. The fix is beside each.

**You cannot reason in pixels.** You will misjudge absolute positions and you are
reliable at *relationships*. Look with the grid on, say "the dark mass sits around D5
to F6", then paint into `cell("D5")`:

```python
s.look(grid=True)                    # labelled A–H across, 1–8 down
s.block_in(cell("D6"), ...)          # then target what you saw
s.block_in(region("upper-left"), ...)
s.stroke([below(region("center"), 0.1).point(0.5, 0.5), ...])
```

**You will draw outlines and fill them.** That is how you make colouring books. Paint
the mass directly with a brush wide enough to cover it in a few strokes, and let the
*edge of the mass* be the drawing. There is no outline in a painting — there is a place
where one mass stops.

**Finding an edge is the same mistake in disguise.** When a silhouette is not crisp
enough, the reflex is to run a thin dark stroke along it, and that stroke reads as a
drawn line the moment you look. Sharpen an edge by painting the mass on the *other*
side of it: a brush at least `0.03` wide, running along the boundary with its centre
outside the shape, laying the background's own colour up to where the shape stops.

**A hole in a mass is the same rule again.** Dab the background colour into the middle
and you get a floating disc. A gap is a broken sliver worked in from the silhouette
with a starved brush, because that is where the light comes in:

```python
s.stroke([(0.42, 0.36), (0.47, 0.41)], "round_hard", "pale",
         size=0.012, load=0.3, opacity=0.7)      # in from the edge, not a dot
```

**You will paint boxes.** A rectangle is the easiest place to name, and if you block in
a shaped mass as a box you get a box, and no later work removes it. Build the shape,
preview it, and **check the background hardest**: you will reach for a shape on your
subject, because its silhouette was a problem, and then lay everything behind it in
boxes because nothing back there asked anything of you. A background of square patches
reads instantly as made by a machine. Give the masses that needed no drawing the same
treatment as the ones that did — and the marks inside them are not parallel lines. If a
surface has a grain, the grain varies: it breaks, it crosses, it disappears for a whole
passage. Three marks that describe it beat thirty that repeat it.

**You will reach for `undo`.** Real repairs happen with paint. `s.cover(place, colour)`
dries the area and buries it with every clause of the recipe in place — a long solid
stroke at full load with no run-out, its ends outside the area:

```python
s.cover(cell("D5"), "corrected_colour")      # the whole recipe, already set

s.dry()                                      # or the same clauses on a stroke of your own
s.stroke([(-0.05, 0.55), (1.05, 0.58)], "flat", "corrected_colour",
         size=0.09, load=1.0, load_falloff=0.0, opacity=1.0, pressure="even")
```

A `bristle` does not bury — its comb leaves the old paint showing between the streaks.
**`cover` runs its ends a full brush outside the area**, which is right on a flat
passage and louder than the mistake on a worked one; there, bury it by hand with marks
shaped like the passage. `undo(n)` exists; treat it as scraping the canvas, and remember
that `n` counts log entries rather than marks you paid for.

**You will under-vary your objects.** Having worked out how to paint one of a thing,
you will paint the next with the same recipe, and a viewer reads three copies of one
object rather than three of a kind. Vary one thing per object on purpose: which way its
light falls, how sharp its edge is, how much of it the mass in front takes away. One
difference each is enough.

---

## Nine small exercises

**They are a gate.** A painter who skips them meets the lessons inside the picture
instead, with the rest of the painting already standing on the mass that has to be
repainted. An exercise is the one place where a mistake has nothing built on top of it.
They take a minute each. Do the nine. Then start.

**1. A value scale.** Nine even steps from the darkest mix to white. Mix to a *value*,
not to a ratio: white is much stronger than its share of the mixture, so ask for the
value and let `at_value` find the ratio.

```python
from easel import Session, Region

s = Session(900, 200, ground="toned_grey", seed=1)
p = s.palette
dark = p.mix("ultramarine", "burnt_umber", 0.5)     # the darkest thing in the box
lo, hi = p.value_of(dark), p.value_of("titanium_white")

for i in range(9):
    target = lo + (hi - lo) * i / 8
    band = Region(i / 9.0, 0.15, (i + 1) / 9.0, 0.85)
    s.block_in(band, "flat", p.at_value(dark, target), density=1.0, size=0.06)
    print(f"value {target:.2f}  reads {p.value_of(p.at_value(dark, target)):.2f}")
s.look(values=True)     # nine even steps, 0.14 to 0.96
```

A third of white gets you the first step of nine and it takes nine tenths to reach the
eighth: a mixture that "should" be halfway comes out too dark, and the fix is always
more white than feels right. It goes both ways — to lower a value it mixes in a dark,
so a planned value is reachable from either side.

**2. One stroke, six pressures.** On the round brush on the left they change the
*width* of the mark as well; on the `bristle` on the right only how much paint lands.

```python
from easel import Session

s = Session(900, 500, ground="toned_grey", seed=2)
for i, p in enumerate(["taper", "press_in", "lift_off", "even", "swell", "dab"]):
    y = 0.12 + i * 0.15
    s.stroke([(0.10, y), (0.50, y)], "round_soft", "titanium_white", pressure=p,
             size=0.05, opacity=0.35, load=1.0, load_falloff=0.0, note=p)
    s.stroke([(0.55, y), (0.92, y)], "bristle", "titanium_white", pressure=p,
             size=0.05, opacity=0.35, load=1.0, load_falloff=0.0, note=p)
s.look()      # soft brush on the left reads the profiles most clearly
```

**3. Paint running out.** The same stroke at four loads, on rough canvas. The speckle a
starved brush leaves is what everything laid after it sits on.

```python
from easel import Session

s = Session(900, 400, texture="rough", ground="toned_grey", seed=3)
for i, load in enumerate([1.0, 0.6, 0.35, 0.2]):
    y = 0.15 + i * 0.22
    s.stroke([(0.06, y), (0.94, y)], "bristle", "titanium_white",
             size=0.07, load=load, load_falloff=0.0, pressure="even")
s.look()
```

**4. Wet versus dry.** The same yellow over blue, once into wet paint and once onto dry.
Each band is a *single* stroke, because a block-in is many strokes and the wet half
would have dried before the yellow arrived.

```python
from easel import Session

s = Session(800, 400, ground="white", seed=4)
s.stroke([(0.10, 0.27), (0.90, 0.27)], "flat", "ultramarine", size=0.22, pressure="even")
s.stroke([(0.15, 0.27), (0.85, 0.27)], "flat", "cadmium_yellow", size=0.10, pressure="even")

s.stroke([(0.10, 0.73), (0.90, 0.73)], "flat", "ultramarine", size=0.22, pressure="even")
s.dry()
s.stroke([(0.15, 0.73), (0.85, 0.73)], "flat", "cadmium_yellow", size=0.10, pressure="even")
s.look()      # top band goes olive; the bottom one stays yellow
```

**5. An edge study.** One hard, one soft, one lost. Look at which one your eye goes to.

```python
from easel import Session, region

s = Session(900, 300, ground="toned_grey", seed=5)
left, mid, right = region("all").split_h(3)
for r in (left, mid, right):
    s.block_in(r, "bristle", "burnt_umber", density=1.0, size=0.1)
s.dry()
s.block_in(left,  "bristle", s.palette.tint("burnt_umber", 0.6), density=1.0, size=0.1)
s.stroke([(0.02, 0.5), (0.31, 0.5)], "round_hard",
         s.palette.tint("burnt_umber", 0.6), size=0.03)      # hard
s.smudge([(0.35, 0.3), (0.35, 0.7)])                         # soft
s.look()
```

**6. Mixing.** Prove to yourself what the pigments do together.

```python
from easel import Session

p = Session(600, 200, seed=6).palette
for a, b in [("cadmium_yellow", "ultramarine"), ("cadmium_red", "ultramarine"),
             ("cadmium_yellow", "cadmium_red"), ("cerulean", "titanium_white")]:
    print(a, "+", b, "->", p.hex(p.mix(a, b, 0.5)))
```

**7. Draw, try, paint.** The whole precision loop, on an abstract shape: this is how a
feature gets painted.

```python
from easel import Session, cell

s = Session(900, 600, ground="toned_grey", seed=7)
s.mark("a", *cell("C3").point(0.5, 0.5))       # three verified points
s.mark("b", *cell("F3").point(0.5, 0.5))
s.mark("c", *cell("D6").point(0.5, 0.5))
s.pencil([s.pt("a"), s.pt("b"), s.pt("c"), s.pt("a")], pressure=0.7)
s.look()                                        # the drawing, before any paint

plan = [{"points": [s.pt("a"), s.pt("c")], "brush": "bristle", "size": 0.09,
         "color": "titanium_white"}]
s.rehearse(plan, region="C3:F6")                # what would that mark look like?
s.rehearse([dict(plan[0], size=0.03, brush="liner")], region="C3:F6")   # or this?

s.stroke(**plan[0])                             # spend the stroke on the better one
s.look(region="C3:F6")     # the pencil is gone under the paint and still there beside it
```

The two rehearsals cost nothing and neither appears in `s.log()`. The drawing did not
count against `s.stroke_count`. The graphite has vanished exactly where the paint
landed and survived everywhere else, which is what an underdrawing is for.

**8. A box and a shape.** The same mass twice, so you can see the difference before you
have to judge it in a painting.

```python
from easel import Session, blob, cell

s = Session(900, 400, ground="toned_grey", seed=3)
s.palette["dark"] = s.palette.mix("ultramarine", "burnt_umber", 0.45)

mass = blob(cell("B4").point(0.5, 0.5), 0.16, 0.30, wobble=0.3, seed=1)
s.block_in(mass.box, "bristle", "dark", size=0.10, direction="axis")   # as a box
s.block_in(mass.shifted(0.5, 0.0), "bristle", "dark", size=0.10,
           direction="axis")                                           # as a shape
s.look()
```

Same brush, same direction, much the same number of passes. One is a rectangle and
will still be a rectangle at the end of the painting; the other has a silhouette, and
a silhouette is what a mass *is*. Look at the ends of the passes on the shaped one:
they stop at the boundary, and the brush breaks past it by about half its width, which
is the ragged edge you want and did not have to make.

**9. A swatch strip.** Exercise 1 calibrates value; this calibrates *hue*, where the
mixing surprises live. Lay every mixture you plan to use side by side and look before
the first mass: a grey that is secretly green shows here and not in its numbers.

```python
from easel import Session, Region

s = Session(900, 200, ground="toned_grey", seed=9)
p = s.palette
plan = {"haze": p.at_value(p.mix("cerulean", "titanium_white", 0.8), 0.64),
        "deep": p.at_value(p.mix("cerulean", "burnt_umber", 0.4), 0.40),
        "dark": p.at_value(p.mix("burnt_umber", "viridian", 0.3), 0.20),
        "lit":  p.at_value(p.mix("yellow_ochre", "titanium_white", 0.6), 0.78)}
for i, (name, colour) in enumerate(plan.items()):
    band = Region(0.05 + i * 0.225, 0.15, 0.25 + i * 0.225, 0.85)
    s.block_in(band, "flat", colour, size=0.08, solid=True)
    print(f"{name:5s} value {p.value_of(colour):.2f}  chroma {p.chroma_of(colour):.2f}")
s.look()            # the hues beside each other, which the numbers cannot show
```

`chroma_of` is *how coloured*, beside `value_of` for how light.

---

## A checklist before you call it finished

**Passing this list means the painting is not *wrong*. It does not mean it is
finished.** Every line but the last two is a fault to look for; the last two are the
only ones that ask whether you are done, and they are the ones to answer slowly.

- Does the greyscale view have a clear light, mid and dark?
- Are the edges varied — some hard, some soft, at least one lost?
- Is there anywhere the ground still shows through? There should be. `report()`
  prints the share — it diffs the canvas against a bare one at your own ground,
  texture and seed — and says so under `0.5%`. One painter chose a warm ground to
  be seen through, laid the passage over it at `density=1.0, load=1.0`, and
  finished at `0.07%` without noticing.
- Are the highlights few and deliberate?
- Is anything mechanically repeated — a perfectly straight line, a row of identical
  marks? **Is any small mark a disc, a capsule or a rectangle — the tool's own shape
  rather than the thing's?** `report()` counts the discs — three or more small round-tip
  marks at `tip_wobble=0` are one silhouette printed three times — and a `block_in` with
  a round tip on a feature under four brushes across says so at the call. Crop into
  what is left and look.
- Is every mass laid along its own axis, or are the big shapes stacks of bars? **And
  are the bands in the marks, or in the subject you chose?** A frontal elevation is a
  layer cake before a brush is picked.
- Is any mass a rectangle that should have been a shape? Check the background hardest.
- **Is the thing you measured most carefully still attached to the picture?** Cover
  it and look at what is left. And is the lightest mass the one you planned to be
  lightest? A mass that has quietly become the brightest thing takes the eye whatever
  the picture is about.
- Was it painted back to front — is every hollow thing's far edge under its contents
  and its contents under its near edge? Did a correction bury something standing on the
  mass you repainted?
- Is there pencil still showing where you did not mean it to? `s.erase()` takes it out,
  and `s.export(path, sketch=False)` hides all of it; a drawing showing through thin
  paint is a good thing and worth keeping.
- **What share of your strokes went on the subject? Write the number down, against the
  share you planned.** Not "did you spend enough" — a number, measured at the moment the
  subject is finished, and the log will count it if you say which marks they are:

  ```python
  s.stroke([(0.30, 0.40), (0.45, 0.44)], "round_hard", "light",
           size=0.02, note="subject")               # as you paint it
  paid = [r for r in s.history.records
          if r.kind not in ("dry", "look", "pencil", "erase")]
  on_it = [r for r in paid if "subject" in r.note]
  print(f"{len(on_it)} of {len(paid)} marks — {len(on_it) / max(len(paid), 1):.0%}")
  ```

  After that the number is *meant* to fall: **the last third of the budget goes on
  what surrounds the subject**, because a well-built feature in an unfinished picture
  reads as a detail come loose, and a rough one in a picture that holds together reads
  as the thing itself.
- **You have named the weakest passage. How many strokes are left? Spend them there.**
  A painter who stops with a third of the budget unspent has left the picture short
  without deciding to. The passage you would apologise for is the one that wants them —
  not the one you have most recently been enjoying — and the last marks are about the
  picture, never about a score.

If you have a reference, look at them side by side one last time:

```python
s.look(reference="ref.jpg")
s.look(reference="ref.jpg", values=True)   # compare value structure, not colour
```

## Sign it

When you have decided it is finished — after the last look, before you export — sign
it. **Up to five marks, and they do not come out of your stroke budget**, so long as
each one carries `note="signature"`:

```python
s.stroke([(0.86, 0.94), (0.90, 0.92)], "liner", "dark", size=0.006,
         note="signature")
```

You do not have a name, so this is not a name. It is a mark: whatever you would put in
the corner of something you made. It is not a title and it is not a last chance to fix
something. Put it where it does the picture no harm — a corner, small, close in value
to what it sits on — and say in your notes what you chose and why. That question is
asked here, at the end, because a mark chosen to be explained is not the same as a
mark chosen.

```python
s.export("painting.png")
s.timelapse_gif("painting.gif")
```

---

## Working from a shell instead

The same thing is available from the command line, without holding a Python process
open. Session state lives in one file. If `easel` is not found, put `python -m easel`
in front of the same arguments; do not spend time fixing your `PATH`.

```bash
easel new painting.easel --size 1024x768 --texture linen --ground toned_grey --seed 7 --budget 300
easel run painting.easel pass1.py                 # your script; `s` is already defined in it
easel run painting.easel pass1.py --rehearse      # ...against a copy, committing nothing
easel look painting.easel --grid
easel look painting.easel --values
easel look painting.easel --region D4 --fine
easel compare painting.easel ref.jpg              # per-cell value numbers
easel export painting.easel painting.png
```

A script given to `easel run` has `s`, `palette` and the whole API already in scope. A
`prelude.py` beside the session file runs first, in the same scope, so mixtures,
landmarks and the masses-as-functions do not have to be redefined at the top of every
pass. **The habit here is: rehearse every pass with `--rehearse`, look, and only then
run it without.** Name several scripts at once and they run in order; rehearsed
together they share one copy, so each is judged on the pass before it. After
every pass `run` prints the budget line and a check of the pass against the standing
warnings, whose rules are listed under `report()` in
[`REFERENCE.md`](REFERENCE.md#looking-planning-measuring); read it before the next
pass. The full command list is in [`REFERENCE.md`](REFERENCE.md#the-session-and-the-shell).
