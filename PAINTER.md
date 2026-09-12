# Painting with Easel

You are about to paint. Not draw, not render — paint. This guide assumes you have
never seen the engine's source and do not need to.

**Read it in two goes.** *The first hour*, immediately below, is the whole workflow on
one page and everything you need for the eight warm-up exercises at the end of this
file. Do those exercises — they are the cheapest strokes you will ever spend. Then read
the rest of this guide, which is the same rules with their reasons, the failures behind
them and the numbers, before you start the painting itself. The workflow section
matters more than the API section.

Two files sit beside this one and neither is needed to paint:
[`REFERENCE.md`](REFERENCE.md) is every fact on one page — units, defaults, what each
argument does — for when you want to look something up rather than read a rule, and
[`CALIBRATION.md`](CALIBRATION.md) is what was measured behind the rules here.

---

## The first hour

One page, then go and paint the exercises. Every arrow points at a section further
down, and that is where the reason for the line is.

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
→ *Getting started*

**Look every 5 to 15 strokes.** `s.look()` writes a PNG and returns the path; open it.
`s.look(values=True)` is greyscale, and it is the one that tells you the truth.
→ *The one habit*, *Looking*

**The order. It is the whole method, and it is not optional.**

1. **Big masses first, in the biggest brush you will use**, at `density` below 1 so the
   ground breathes through. Two or three of them. Not outlines — masses. → *step 1*
2. **Back to front.** The furthest thing goes down first and every nearer thing is
   painted over it. Nothing is "cut around". → *step 2*
3. **Check the values before anything else.** In greyscale, is there a clear light, a
   clear mid and a clear dark? Two masses closer than `0.10` in value read as one.
   → *step 3*
4. **Then the mid-tones**, across the whole canvas rather than finishing one corner,
   and lay each mass along *its own* axis rather than the canvas's. → *step 4*
5. **Edges last but one.** Hard edges pull the eye; soft and lost ones let it move on.
   Not every edge should be crisp. → *step 5*
6. **Highlights last, smallest brush, fewest strokes.** Ten deliberate marks, not a
   hundred. → *step 6*

```python
far  = blob(span("B2", "G4"), wobble=0.3, seed=1)
s.block_in(far, "bristle", "dark", density=0.8, size=0.18, direction="axis")
s.look(values=True)                                  # before anything goes on top
s.block_in(span("A5", "H8"), "flat", "light", size=0.14, solid=True, direction=6)
```

**The five things you will get wrong.** Painters did each of these *after* reading the
warning about it, which is why each one here comes with the thing to do instead.

- **You will draw outlines and fill them.** Don't. Paint the mass with a brush wide
  enough to cover it in a few strokes, and let the edge of the mass be the drawing.
  A silhouette that is not crisp enough is sharpened by painting the mass on the
  *other* side of it, never by running a line along it. → *What you are bad at*
- **You will paint boxes.** Almost nothing is a rectangle. `blob`, `ellipse`, `hull`,
  `ribbon`, `polygon` and `s.circle()` build a mass with a silhouette, and `block_in`
  fills one as readily as a box. **Check the background hardest** — it is the mass
  nobody made you draw. → *Masses that are not rectangles*
- **You will lay parallel marks.** One direction for every pass is hatching, and a
  surface's grain repeated thirty times is a stack of bands with a different name.
  Vary the direction; three marks that describe a texture beat thirty that repeat it.
  → *The angle of the mark*
- **You will reach for `undo`.** Repairs happen with paint: `s.cover(place, color)`
  is the whole burying recipe, already mixed. → *When something is wrong, paint over it*
- **You will spend on detail too early.** A good painting is mostly big statements. If
  you are 50 strokes in and painting tiny marks, you are in trouble.

**What a mark costs, before you make it.** `stroke`, `dab`, `smudge` and `glaze` are
one each. A `block_in` or a `sweep` is one *per pass* — ten to thirty for one call, and
the number nobody can guess. Drawing, looking, drying and all four planning verbs are
free.

```python
plan = [{"shape": blob(cell("D5"), 0.12, seed=3), "brush": "bristle",
         "color": "dark", "size": 0.09}]
s.cost(plan)                  # what it charges
print(s.cost_line(plan))      # and why that number
s.preview(plan)               # where it would go
s.rehearse(plan)              # what it would look like
s.paint(plan)                 # the same plan, now paid for
```

One plan object goes to all four, so nothing is retyped between checking it and
painting it. **Rehearse any mass you would not want to repaint.** → *Try the mark
before you spend it*

**Now go and paint the eight exercises**, at the end of this file. Then come back and
read the rest — in order, because each step assumes the one before it.

| When you want | Read |
|---|---|
| the order of work, in full | *The workflow*, steps 1–6 |
| to work from a photograph | *Working from a reference* |
| to work from nothing but your own head | *Painting without a reference* |
| to stop making the same five mistakes | *What you are bad at, and what to do instead* |
| a colour, a mixture, a value | *Colour* |
| to know what a brush will actually leave | *The brushes*, *The shape each tool leaves behind* |
| to check a mark before paying for it | *Try the mark before you spend it* |
| a fact: a unit, a default, an argument | [`REFERENCE.md`](REFERENCE.md) |
| a number behind a rule | [`CALIBRATION.md`](CALIBRATION.md) |
| to stop | *A checklist before you call it finished* |

---

## The one habit

**Look every 5 to 15 strokes. A stroke you did not look at was a guess.**

```python
s.look()                 # writes a PNG, returns the path — then open it
```

You are good at judging an image you can see and bad at predicting one you cannot.
The whole engine is built around closing that loop. If you take one thing from this
guide, take this.

---

## Getting started

```python
from easel import Session

s = Session(1024, 768, texture="linen", ground="toned_grey", seed=7)
```

Coordinates are always `0.0` to `1.0`, origin **top-left**. `(0.5, 0.5)` is the
centre, `(0.9, 0.1)` is the top right. There are no pixels anywhere in this API.

**One trap, and it is worth knowing before your first shape.** Both axes run 0–1, so
on a canvas that is not square the same number is a different distance in each: `0.1`
across a 1024×768 canvas is 102 pixels and `0.1` down it is 77. Brush sizes are a
fraction of the canvas's **long side**, so a brush is round — but `ellipse(p, 0.1,
0.1)` is an oval. A round radius `r` in x is `r * width / height` in y, and rather
than do that arithmetic, ask the session:

```python
s.circle((0.5, 0.5), 0.09)                 # round in pixels, on any canvas
s.circle(cell("D5"))                       # the biggest circle that fits the cell
s.circle((0.5, 0.5), 0.09, wobble=0.25)    # round, with a silhouette nobody drew
```

Grounds: `white`, `warm_white`, `toned_grey`, `toned_warm_grey`, `burnt_sienna`,
`umber_wash`, `cool_grey`. Textures: `smooth`, `linen`, `rough`.

**Start on a toned ground, not white.** A mid-tone ground means your first marks
already sit in a value relationship, and any ground left showing reads as a colour
you chose. On white, everything you paint looks dark and every gap looks like a
hole.

---

## The workflow

This is the part that matters. It is the order oil painters have used for centuries,
and it works for the same reason here: it keeps you making *large* decisions before
*small* ones, so a mistake is cheap for as long as possible.

### 1. Tone the ground, then find the big shapes

Two or three masses. Not outlines — **masses**. Use the biggest brush you will use
in the whole painting, something like `size=0.18`, and block in with `density`
below 1.0 so the ground still breathes through.

```python
s.palette["dark"] = s.palette.mix("ultramarine", "burnt_umber", 0.45)
s.block_in(blob(cell("D5"), 0.26, wobble=0.3, seed=2), brush="bristle", color="dark",
           density=0.7, size=0.2, direction="axis")
```

**`density` spaces the passes; it does not fill them.** Every pass runs dry along its
own length whatever the spacing, so `density=1.0` looks like a request for solid paint
and is not one — it lays a mottled mass with a twentieth of the ground still showing.
When a mass has to be solid, because it is near, or because fine marks are going to
stand on it, say so: `solid=True`, which costs nothing and no extra passes. Not for
these first masses, though — they want the ground breathing through them.

A place can be a rectangle — `cell("D5")`, `span("E5", "H8")`, `region("lower-half")`
— or a **shape**: `blob`, `ellipse`, `hull`, `ribbon`, `polygon`. `block_in` fills
either, and a shape's passes stop at its own silhouette. Most masses are shapes; see
*Masses that are not rectangles*.

Resist detail here. If you can already name what you are painting, you have gone
too far too early.

### 2. Paint from back to front

**Lay the furthest thing first and let each nearer thing be painted over it.** The
far mass, then the middle one, then the near one, then the small shape standing in
front of all of them. Background, middle distance, foreground, in that order, every
time.

This is not tidiness. It is the only cheap way to get an edge:

```python
s.palette["far"]  = s.palette.tint("cerulean", 0.55)
s.palette["near"] = s.palette.desaturate(s.palette["far"], 0.4)

s.block_in("upper-half", "flat", "far", size=0.18)          # furthest
s.block_in(span("A4", "H6"), "flat", "near", size=0.16)     # nearer
s.stroke([(0.3, 0.42), (0.3, 0.78)], "bristle", "dark", size=0.03)   # in front
```

The narrow shape's edges are now real edges — the place where its paint stops and
the mass behind it is still showing — and you drew none of them. Paint it first and
the only way to get the same edges is to cut the mass behind it carefully around
it, which is painting *up to* a line, which is the one thing this guide will tell
you several more times not to do.

Three things follow from it:

- **Draw the near things after the far masses are down.** A pencil line laid on the
  ground and then blocked over is gone — paint buries graphite in proportion to how
  much lands, and a full-strength block-in lands all of it. Landmarks go down before
  anything; the pencil goes down after the far masses; the near masses go on top.
- **Let the near mass overlap.** Run it a little into the far one. A silhouette
  that stops exactly on a boundary was measured; one that overlaps was painted.
- **A mistake in the background is cheap while the foreground is not there yet.**
  It stops being cheap the moment something is standing in front of it. Repainting a
  mass buries everything standing on it, and the correction you have just decided to
  make is exactly when you will forget that — so this rule is repeated where those
  decisions actually get made, under **Put a number on it**.

The exception is the ground itself, which is behind everything and goes on first by
definition. Everything after that is in depth order.

**Anything with an inside has its own depth order, and it is the one most often got
wrong.** A hollow thing is not one mass. It is three, at three depths, and all three
belong to the same object: **the far edge, then what is inside, then the near edge.**

```python
far  = ellipse(span("D2", "F3"))          # what stands behind the inside
near = polygon([(0.36, 0.31), (0.64, 0.31), (0.62, 0.72), (0.38, 0.72)])

s.block_in(far, "flat", "pale", size=0.04)                 # behind the inside
s.block_in(far.inset(0.015), "flat", "dark", size=0.04)    # the inside
s.block_in(near, "flat", "light", size=0.06)               # in front of the inside
```

Painted in that order, the inside's near edge is a real edge — the place where the
near mass's paint stops and the dark behind it still shows. Painted the other way
round there is nothing for the inside to stop against, so it runs out over the near
edge and no later mark puts it back: you would be cutting the near mass in around a
dark that is already outside it, which is painting up to a line.

Ask it of anything you can see into, before the first stroke: **what is behind the
inside, what is the inside, and what is in front of it?**

### 3. Check your values before you check anything else

```python
s.look(values=True)
```

This is greyscale — it is what squinting does for a painter. **Value structure is
what makes an image read.** If the greyscale version is mush, no amount of colour
will save it, and every stroke you add from here is wasted work.

A painting usually wants three clearly separated values: a light mass, a mid mass,
and a dark. If you cannot point at those three in the greyscale view, fix that
before you go on.

**Plan those three as numbers, before you mix anything.** `palette.value_of(c)`
reports exactly the value the greyscale view will show:

```python
p = s.palette
p["dark"] = p.mix("ultramarine", "burnt_umber", 0.55)
p["mid"]  = p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.35), 0.40)
p["lit"]  = p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.40), 0.74)
for name in ("dark", "mid", "lit"):
    print(name, p.hex(p[name]), round(p.value_of(p[name]), 2))
```

Two mixtures that sound different can be the same value, and that is the commonest
way a first pass turns into mush. **If two of your three are within `0.10` of each
other, they will not read as separate masses** no matter how different their
colours are.

**That threshold is a floor, and a mass also has a ceiling.** Shading a mass to give
it form spends value range, and the range is shared: past about `0.15` across one
mass, its shadow side starts closing on whatever it stands against, and you have
bought form by losing the separation that made it a mass at all. Measured on a mass
that read flat at `0.09` across its width: laid up to `0.22` it turned, and its
shadow side then sat `0.09` from the mass behind it and the two began to merge; at
about `0.15` both hold. **Shade it until the form clears `0.10`, and stop.**

**The box has no black, and it does not need one.** `mix("ultramarine",
"burnt_umber", 0.5)` is a near-black with a colour in it, which is what a dark in a
painting should be, and varying the ratio holds that value while swinging cool to
warm — more blue for a shadow in daylight, more umber for one by a lamp. That mixture,
not any single pigment, is the bottom of your range. **Piling on passes or glazes will
not go lower**: if a mass is not dark enough, mix it darker rather than painting it
again.

**The floor is a lower wall than it looks**, because a cell only has to land within
`0.10`. A reference darker than the darkest mixture is usually still reachable — you
have to *cover* the cell, at `density=1.0` and full load, with nothing lighter showing
through. Cover properly before concluding you need a colour of your own; you can
supply one and it lands exactly as written, black included (**Colour**, below, has the
syntax), but mixed darks are alive and a tube black is dead. `CALIBRATION.md` has the
arithmetic and how far it stretches.

**A cast shadow is the first place you will spend that dark, and it is the wrong
place.** A shadow lying on a lit surface is **a step or two below the surface** — not
below the palette. Measured on a surface at `0.60`: the darkest mixture lands at
`0.16` and reads as a hole punched through the surface, `0.50` reads as a shadow, and
`0.42` as a shadow with weight. And it is **a tapering stroke, not a filled shape** —
a shape comes back as a slab with two hard ends, which is an object lying on the
surface rather than a shadow falling across it. Lose the far end, and put the dark
where the thing meets the surface:

```python
dark = p.at_value("surface", p.value_of("surface") - 0.18)      # a step or two
s.stroke([(0.55, 0.30), (0.66, 0.38), (0.80, 0.46)], "flat", dark,
         size=0.085, pressure=[1.0, 0.6, 0.0])                  # and lose the far end
s.stroke([(0.55, 0.305), (0.62, 0.35)], "flat", p.at_value(dark, 0.38),
         size=0.05, pressure=[0.9, 0.0])     # darkest where the two things meet
```

Two strokes, and the second is optional. The one thing that is not optional is that
the shadow belongs to the surface it lies on, so it is mixed from that surface's value
rather than from the bottom of the box.

### 4. Refine the mid-tones

Now the middle values, with a medium brush (`size≈0.08–0.12`). Work across the
whole canvas rather than finishing one corner — a painting should come up all at
once, like a photograph developing. Look every ten strokes or so.

**There is no gradient tool, and you should stop looking for one.** Nothing here
grades a mass smoothly from one value to another: wet-into-wet blending dies after
about a dozen strokes as the paint sets, `round_soft` airbrushes above `size≈0.05`,
and `smudge` only moves paint that is already down. What a painter does instead is
paint the gradient as **steps and then lose the joins**:

```python
steps = [(cell("D4"), "dark"), (cell("D5"), "shadow"), (cell("D6"), "light")]
for place, value in steps:
    s.block_in(place, "flat", value, pressure="even", size=0.03)
s.smudge([(0.42, 0.50), (0.46, 0.62)], size=0.04)   # walk each join once, while wet
```

Three or four steps read as a gradient once the joins are softened; two read as two
slabs. Do it while the paint is wet — that is what step 5 and the **Wet paint**
section are for — and if you leave a plane as one flat value with marks laid on top,
it will read as a mask rather than as a form.

**Know what one smudge actually buys you, because it is not a lost join.** Measured
on a hard join between two values: the bare step is `0.330`, one pass at `size=0.040`
takes it to `0.184`, and **three passes take it back to `0.280`**. So a smudge removes
about **40%** of the step, once — and doing it again, which is exactly what you will
want to do, undoes most of the first pass and leaves a thumbprint besides.

**When once is not enough, stop smudging and lay paint.** Many overlapping strokes at
closely spaced values — a scumble — is what closes a join that a single smudge only
softened, and it is the one approach three separate painters arrived at independently
after the smudge recipe failed them:

```python
s.scumble(span("A4", "H6"), "shadow", "light", 8)    # close the join with paint
```

That is eight overlapping passes running along the band and stepping across it, one
value step per pass, and it costs exactly the eight strokes it says. Written out, so
you can see what it is doing and vary it:

```python
for i in range(8):                                   # the same thing, by hand
    t = i / 7
    s.stroke([(-0.05, 0.46 + t * 0.10), (1.05, 0.47 + t * 0.10)], "bristle",
             s.palette.mix("shadow", "light", t), size=0.05, opacity=0.5)
```

The overlap is the point: the brush is wider than the step between passes, which is
what closes the joins that stepping alone would leave. Below about five passes the
steps start to read as steps again.

**A passage that is light in the *middle* is the same verb turned inward.** That band
grades edge to edge, which is a band and not a glow: a lit patch, a bloom, light
falling on a surface goes dark at every edge. `direction="inward"` lays that — the
passes go round the place instead of across it, the first along its boundary and each
one after it a part-brush further in, so the colours arrive from the edge to the
centre. **Do not lay it as strokes radiating out from the centre**, which is the
obvious answer and draws a daisy: strokes that all start in one place draw the petals
of one.

```python
s.scumble(patch, "shadow", "light", 8, direction="inward")   # 8 strokes, lit in the middle
```

The first ring lands *on* the boundary, so the colour you give it is the value the
patch meets what it sits in at: the surrounding value melts the two together, and
anything darker draws a rim round your glow.

**This matters more than it looks**, because a wide soft passage is where a picture's
structure comes from. A field gradated top to bottom is a stack of horizontal bands
until its joins are gone — and a stack of bands is a composition, which your quiet
passage will announce to a viewer whether or not you meant to compose one there.

### 5. Edges: lost and found

This is the step that separates a painting from a diagram, and the one you will be
most tempted to skip.

Not every edge should be crisp. **Hard edges pull the eye; soft and lost edges let
it move on.** Decide where you want attention, make those edges hard, and lose the
others — let two masses merge with no boundary at all in places.

```python
s.smudge([(0.3, 0.4), (0.45, 0.44)], size=0.06)     # soften an edge
s.stroke([(0.6, 0.3), (0.62, 0.5)], "round_hard", "dark", size=0.02)  # sharpen one
```

**`smudge` is far stronger than "move paint around" suggests**, and it walks a
light/dark boundary into the dark side rather than blurring it evenly. Keep it small
and rehearse anything bigger; `CALIBRATION.md` has the window.

**Run it *along* a boundary, never across one.** Dragged across, it pulls a lobe of
the light mass into the dark one and what you get is a visible finger-shaped
thumbprint — the tool's own geometry, in a place you were trying to make quiet. That
failed for three separate painters in one run, on the exact usage the line above
demonstrates.

**And *along* means along the boundary's own shape — only a straight boundary is two
points.** Given two, a boundary that bends gets a pass that starts along it and ends
across it: the same thumbprint, arriving more slowly. `smudge` takes as many points
as you hand it, so hand it the curve — and if the boundary belongs to a mass you
built, hand it the mass and it walks that outline itself:

```python
s.smudge([(0.30, 0.40), (0.38, 0.41)], size=0.04)   # a straight edge is two points
s.smudge([(0.30, 0.40), (0.45, 0.45), (0.60, 0.53),
          (0.73, 0.63)], size=0.04)                 # a curved one is the curve
s.smudge(mass, size=0.04)                           # a shape is already that curve
```

And it is one pass, not three — see *what one smudge buys you* in step 4. If the
boundary is still there after that, the answer is paint, not another smudge.

An image where every edge is equally sharp looks like clip-art. That is the single
most common way this goes wrong.

### 6. Highlights last, smallest brush, fewest strokes

The lightest lights and the sharpest accents go on at the end, and there should be
very few of them. Ten deliberate marks, not a hundred. Every highlight you add makes
the others count for less.

```python
s.dab(0.62, 0.35, "round_hard", "titanium_white", size=0.015)
```

**Anything the size of a cell or smaller is three marks at most — the dark, the light,
and the edge between them** — laid dark first, and looked at through a `region=` crop
before the light goes on. This is the whole method at that scale — a knuckle, a hinge,
a fold, a catchlight: not more marks, smaller ones, in that order. `size` is the *feature's*
fraction of the canvas, not the mass's; see **The brushes**. There is more on painting
at that scale under **Pressure**.

---

## Working from a reference

If you have been given a photograph to copy, this section is the difference
between a likeness and a set of coloured rectangles. Do not start placing strokes
from your impression of the picture — that impression is wrong about position in
exactly the way you are worst at.

**Put the same grid on both, and never take a coordinate out of your head.**

```python
s.look(reference="ref.jpg", grid=True)     # the same A-H / 1-8 cells on each
```

Both panels carry the same labelled cells, so a place you can *see* on the
reference has a name you can *paint* into. That is the whole trick. Work like this:

1. **Name the big masses by cell, out loud, before painting anything.** "The dark
   mass fills E5 to H8. The light shape is D3 to F3. The lit plane is G1 to H2."
   Four or five of those sentences is a drawing.
2. **Paint the masses into those cells** and look again with the grid on. Compare
   cell against cell, not impression against impression: *my* light shape is D3–D4
   but on the reference it runs D3–D5, so it is half a cell too high and too short.
3. **Correct by cell too.** Errors of placement are the ones you cannot see by
   looking at your own painting alone, because it looks internally consistent. They
   only show up against the grid.

A mass is rarely one cell. `span("E5", "H8")` is the rectangle from one cell to
another, both included, so what you said out loud is what you block in — and it is
the right size of crop for inspecting a passage:

```python
s.block_in(span("E5", "H8"), "bristle", "dark", density=1.0, size=0.14)
s.look(region=span("D2", "E4"))                # one passage, close up
```

### The drawing

A cell is a large place, and a feature is smaller than one. Named by cell alone a
feature lands somewhere in the right neighbourhood, which is how a painting comes
out a recognisable scene made of unrecognisable things.

The order, in one sentence: **landmarks before anything, pencil after the far
masses are down, near masses on top.** Landmarks are points, and paint cannot bury
them. The pencil can be buried, so it goes on over the far masses and under the
near ones — that is what back to front buys you here.

So: six or seven points, each one verified. That is a drawing, and everything else
hangs on it.

```python
s.mark("top_l", 0.335, 0.315)          # a named point, shown on every look after
s.mark("top_r", 0.630, 0.315)
s.mark("base",  0.480, 0.715)
```

Marks are drawn on **both** panels, so one look tells you whether the point you
chose is the point you meant. Check each one at the size of the feature, not at the
size of the canvas:

```python
s.look(region=cell("D4"), reference="ref.jpg", grid="fine")
```

`grid="fine"` divides what is on screen into tenths and labels them, and the crop is
enlarged so a single cell fills the panel. **The crop is also padded out to the
panel's shape, so you are shown a little more than the span you asked for** — do not
do pixel arithmetic off its edges. Measure off the `mark()` crosses instead, which are
drawn on both panels and whose canvas coordinates you already know. **Read the two digits off the label; do
not estimate a fraction.** A label pair `(3, 6)` is `cell("D4").point(0.3, 0.6)` —
the near corner of that little square — and its middle is `point(0.35, 0.65)`.
Reading a label is something you do reliably. Estimating "about a third across" is
not, and that gap is the whole reason this view exists.

```python
s.mark("a", *cell("D4").point(0.35, 0.55))     # read off the fine grid
```

Then, once the far masses are down, draw with the pencil through the points:

```python
s.pencil([s.pt("top_l"), (0.36, 0.68), s.pt("base"), (0.60, 0.68), s.pt("top_r")])
s.look(reference="ref.jpg")             # is the drawing right, before any paint?
```

`pencil()` puts graphite into the canvas — no paint, no wetness, and **it does not
count as a stroke**, so the drawing is free. Paint covers it in proportion to how
much actually lands, so it survives thin paint and disappears under solid paint.
Making it disappear is the painting. **Thin means `opacity`, not `density`** — a
`block_in` at low density is the same full-strength paint with the passes spaced
out, and it takes a drawing off completely.

Four things about drawing that are easy to get wrong:

- **Draw through the shapes, not around them.** A line you painted *up to* is an
  outline filled in, and that is the clearest possible sign nobody was looking at
  masses. Paint across your own lines.
- **Erase rather than argue.** If a line is wrong, `s.erase(region)` and redraw.
  Arguing with a wrong line while painting costs strokes and loses every time.
- **The drawing says where the mass is. It does not say what the marks inside it
  do.** A mass drawn along a line still gets painted in every direction the form
  asks for.
- **Fix the drawing before you paint it.** A look at the pencil alone is the
  cheapest correction available to you — it costs nothing and no paint has been
  spent yet.

`s.sketch_lines()` gives every line back as points, so a stroke can be swept along
one, aimed at one, or ignore it.

### Try the mark before you spend it

Three tools sit between deciding on a mark and paying for it. They answer the three
questions you have about a mark you have not made yet — *where does it go*, *what
will it look like*, and *what does it cost*. None of them touches the canvas, none
writes to the log, and all three take the same plan.

```python
plan = [{"points": [s.pt("top_l"), (0.40, 0.62)], "brush": "liner",
         "size": 0.006, "color": "light", "label": "edge"}]

s.preview(plan,  reference="ref.jpg", region=span("C3", "F6"), grid="fine")
s.rehearse(plan, reference="ref.jpg", region=span("C3", "F6"))
s.cost(plan)                                   # 1
```

`preview` draws your intended points and the brush's *width* over both panels — at a
default width if you gave it bare points rather than a plan, which is fine for checking
placement and useless for checking an edge —
where the mark will go, checked against the photograph. `rehearse` paints it on a
copy of the canvas and shows you the result — what it will look like, with its
tooth and its edge and how it mixes with what is already there. A feature smaller
than a cell can be tried three ways and judged before a stroke is spent.

`cost` returns the number of strokes the plan would charge. For a mark that is 1 and
you did not need to ask. **For a mass it is the number you cannot work out by hand,
and getting it wrong is expensive**: a mass is priced on the extent of its box along
the direction the passes stack, *and* on how many times a pass line crosses it. Both
factors run against you on exactly the shapes worth painting.

```python
straight = ribbon([(0.20, 0.50), (0.78, 0.50)], 0.029)
s.cost({"shape": straight, "size": 0.015})                  # 4

bent = ribbon([(0.20, 0.30), (0.45, 0.62), (0.78, 0.34)], 0.029)   # same width
s.cost({"shape": bent, "size": 0.015})                      # 75 -- round a bend
s.cost({"shape": bent, "size": 0.03})                       # 38 -- a wider brush

# and the price is on the preview, beside each mass and sweep, without asking
s.preview({"shape": bent, "size": 0.015, "label": "mass"})  # reads "mass  75 strokes"
```

Nineteen times the price for the same width of paint, because the box a bend sweeps
out is ten times the band's own width, and because a pass line crosses a curve twice.
That is not a defect to route around — it is what the mass costs, and the picture it
makes is the better one. It is a number to *know* before you spend a quarter of your
budget on it. A painter who did not know it budgeted 4 and paid 21.

If the number is more than you want to pay, a wider brush or a thinner `density` is
the lever, and `cost` will tell you what either buys before you commit to it.

**And `cost_line` says *why* the number is what it is**, which is the difference
between fixing the call and redesigning the mass. There are only three answers — the
passes crossed a second direction, they stepped across a bounding box much bigger than
the mass, or a concave outline cut each one into pieces — and each names its own lever:

```python
print(s.cost_line({"shape": bent, "size": 0.015}))
# 75 strokes -- 25% of the 300 left of a 300-stroke budget
#   75  42 passes stepping across 0.34 of the canvas, each cut into 1.8 pieces by the outline
```

The same sentence rides on the budget warning, so a plan that would eat what is left
says what it is spending it on.

**And there is a fourth verb, which paints the plan you just checked.**

```python
s.paint(plan)
```

That is the whole point of the plan being one object: `cost`, `preview`, `rehearse`
and `paint` all read it, so no line of it is written twice. A plan that is checked
and then *retyped* into the call that paints it is a plan that will drift, and the
drift arrives as paint. Marks, masses and sweeps may be mixed in one list and are
painted in the order given:

```python
s.paint([{"shape": blob(cell("D5"), 0.12, seed=3), "brush": "bristle",
          "color": "dark", "size": 0.07},
         {"points": [(0.31, 0.62), (0.55, 0.58)], "brush": "liner", "size": 0.005}])
```

The rehearsal is seeded as if these were the next strokes of the real painting, so
what you rehearsed is what lands — rehearse a plan, paint that same plan with nothing
in between, and it arrives pixel for pixel as it was rehearsed. This is what the scrap
of canvas beside a real easel is for, and it is the last reason to reach for `undo`.

**Rehearse the masses, not just the features.** The tools above are written around a
mark smaller than a cell, because that is where a painter expects to need them. The
expensive mistakes are the other way up: a `block_in` of a big mass is one call and
twenty strokes, and it is cheap to repaint only until something else stands on it.
**Rehearse any block-in you will not want to repaint.**

### Compare values, not colours

```python
s.look(reference="ref.jpg", values=True)   # both panels greyscale, same scale
```

**A cool mass on a warm ground reads about two steps lighter than it measures**, so this
is also the tool for the commonest false alarm there is: a painter concluded three times
that its subject was far too light and `compare()` said it was inside `0.05` every time.
Believe the number.

Both sides are converted the same way, so the greys are directly comparable. This
is the fastest way to find the error that will otherwise sink the painting: a
background far lighter than the reference's, a light mass that is not actually the
lightest thing, two masses that are separate in colour and identical in value.

**Get the value map right before you care about the drawing.** A copy with the
right values and a clumsy drawing still reads as the scene. A copy with an exact
drawing and flat values reads as nothing.

### Put a number on it — twice

Squinting says something is off. It does not say which mass or by how much.

```python
print(s.compare("ref.jpg"))
```

Per cell: the reference's mean value, yours, the difference, and a heat map beside
the two greyscales. Negative means your canvas is *darker* there. Narrowed to one
place with `region=`, the per-cell detail lines beneath the table are `col,row` — the
transpose of the table above them, so read the header before you trust a pair. **The number that
matters is `0.10`**: a cell further out than that is a separation the painting has
lost. Every one of them is yours to fix. A cell marked `~` asks for a value below
anything the box reaches (see step 3) and is not work — on most references there
will be none, and if a photograph does hold one or two, they are its deepest
shadows and nothing else.

Run it **twice**, not continuously:

- **Once on the empty canvas**, before the first stroke. The difference column is
  meaningless but the reference column is the photograph's whole value map, in
  numbers: its lightest cell, its darkest, and where every mass sits between. That
  is what you plan the three values from. Your eye will guess the range of a dim
  photograph two stops too light; this will not.
- **Once after the block-in**, before any feature. If the three masses are within
  `0.10`, the structure is right; if a mass is out, fix the *mass* — a bigger brush,
  not a smaller one.

**Before you repaint a mass, look at what is standing on it.** This is where step 2's
rule actually bites, and a number you have just measured is the most convincing
possible reason to ignore it: a mass repainted at block-in size buries every fine mark
lying on it, and those are the expensive ones, while what you are fixing is a tenth of
a value. Cheapest first: repaint it *before* the near things go on, which is what the
two-`compare()` rhythm is for. After that it is a repair, and *When something is wrong,
paint over it* has the method. Look at the picture afterwards, not just the number:
`compare()` will happily report the cell improved while the mark you buried was the
reason the painting read.

The mean colour is in the table too, coarse on purpose: it is there to catch "that
whole passage is too warm", not to be sampled and matched. **Matching cell by cell
is tracing**, and it produces a painting nobody would look at twice. If you find
yourself working down the table one cell at a time, you have stopped painting.

### Painting without a reference

Half the tooling above assumes a photograph. If you are painting something you can
only see in your head, everything here still applies except that *you* are the
reference — so write the value plan down in numbers before a stroke, and measure
against that instead:

```python
upper, lower = span("A1", "H4"), span("A5", "H8")
s.compare({upper: 0.72, lower: 0.38})       # the same table, the same sheet
```

The keys are places and the values are what `value_of` reports, so a plan is a few
lines written before you start and checkable after every mass. The sheet shows the
plan, the canvas, and each planned place outlined with its miss written across it.
Give a place a name to see it listed under one: `blob(cell("D5"), name="near_mass")`.

The rest of the method is the same discipline without the crutch:

- **Draw first anyway.** The pencil is free and does not count against the budget, and
  with nothing to check a drawing *against* it is still the cheapest place to find out
  that the proportions in your head do not fit the canvas — which is a thing you can
  see the moment it is down. → *The drawing*
- `print(p.value_of(mix))` for every mixture as you make it, and for the ground.
- `p.at_value(base, target)` to *hit* a planned value rather than guess at it.
- `look(values=True)` after every mass, read against the numbers you wrote down.

The failure this prevents is the one a reference makes impossible: a value plan that
lives only in the painter's head drifts a step per mass, and by the fourth mass the
picture has no value structure at all — and nothing said so.

### When to stop measuring

Measuring is not painting, and every tool in this section can be used to avoid
making a mark. Stop when:

- **the three masses are within `0.10`** — value is what carries a copy;
- **the landmarks are verified** — six or seven, checked at feature scale. A dozen
  is not twice as good; it is a session spent on arithmetic;
- **you can see the subject in your own painting with the reference covered up.**

Past that point, more measuring makes the painting worse, not better: it turns
marks into corrections and corrections into mud. The grid gets the masses into the
right cells and the landmarks get the features into the right places. Neither will
paint a feature for you.

**And precision is paid for somewhere else in the picture.** Landmarks buy accuracy
exactly where you point them, out of the budget for everything you did not. The
failure: the part you measured is built, and the mass it belongs to has dissolved into
the background — silhouette, support and surroundings never got their own passes. A
small mass sitting *on* a bigger one instead of *in* it is the checklist's question at
feature scale; **it happens at picture scale too, and there it is far harder to see,
because everything you have been looking at looks right.**

So **spend the last third of your strokes on what is around the thing you measured.**
A well-built feature in an unfinished picture reads as a detail come loose; a rough one
in a picture that holds together reads as the thing itself. A viewer recognises a
subject from its mass and its placement long before they can see a feature at all.

**Decide what share of the budget the subject gets before your first stroke, and spend
everything else out of what is left.** There is arithmetic here for what a *mass*
costs — `extent / step`, below — and none at all for what a *picture* costs, and the
gap is expensive in exactly one direction. The guide warns you about spending too much
on detail; the commoner failure is quieter. A painter working to 300 spent **59% of
them before it began the subject at all**, reached the thing the picture was about with
41% left, and its own verdict was that the part it came for is the weakest passage in
the finished painting. Nothing told it that was happening, because every one of those
marks was a reasonable mark.

Write the split down. Something is the picture and everything else is what it stands
in, and the second is not entitled to half.

**This is also the rule that has to carry a busy picture.** Depth order scales to any
number of masses without changing; attention does not. Everything else here assumes one
subject against a ground, and once several things could plausibly be the subject the
checklist's question — *is the thing you measured most carefully still attached to the
picture?* — has a harder version: **is the thing you measured most carefully still the
thing the picture is about?**

**And when the two closing rules collide, this is the order.** *Spend the last third on
the surroundings* and *your last marks should be about the picture* pull against each
other on a copy that is being scored, because every near mass you lay late knocks a cell
back out of tolerance. **Finish the value work early and deliberately** — check
`compare()` comes back clean, and then stop measuring. The last third is then free for
the surroundings, and the last few marks for the picture: an accent, an incident, an
edge thrown away on purpose. A painter that has to spend its last marks on the score has
already lost the picture.

### Letting the reference be cut up for you (optional)

`s.prepare("ref.jpg")` quantises the photograph and hands back its masses,
numbered, with an overlay to look at and a table of each one's share, value,
colour, the cells it covers, and how hard its edge is against each neighbour.

```python
prep = s.prepare("ref.jpg")            # "coarse": five to eight masses
print(prep)
prep.merge(3, 7)                       # both of those are one thing
s.look_areas()                         # the corrected map, over both panels
s.look(region=prep.region(4), reference="ref.jpg", grid="fine")
```

**The map is not the truth.** It joins two things of the same colour into one area
and cuts one thing along its own shading, because it knows about colours and a
painting is made of things. `merge` and `split` are how you say so.

`s.sketch()` lays those outlines as pencil in one call, and `s.ref_shape(n)` hands
one back as a shape. **Both are assisted modes**, and so is handing
`s.ref_outline(n)` straight to `sweep()`: the boundary of a mass is a drawing, and
if the machine found it, say so. The drawing is meant to be yours, and any write-up
has to say one was used — where you went through `sketch()` or `ref_shape(n)` the
painting records it for you (`s.log()` prints it, and it is in the saved session),
and where you copied the points out by hand nothing can, so it is on you.

Prefer `prepare` for *reading* the reference: look at the area, then lay your own
outline over it — `hull` on three or four verified landmarks, a `blob` sized to the
cells the table says it covers, or an edge you read off the grid and `sweep`.


---

## What you are bad at, and what to do instead

Be honest about these. They are specific to what you are.

**You cannot reason in pixels, and you should not try.** You will misjudge absolute
positions. Use the vocabulary of place instead:

```python
s.look(grid=True)                    # labelled A–H across, 1–8 down
s.block_in(cell("D6"), ...)          # then target what you saw
s.block_in(region("upper-left"), ...)
s.stroke([below(region("center"), 0.1).point(0.5, 0.5), ...])
```

Look with `grid=True`, say to yourself "the dark mass sits around D5 to F6", then
paint into `cell("D5")`. You are reliable at *relationships* and unreliable at
*numbers*.

**You will want to draw outlines and fill them. Don't.** That is how you make
colouring books. Paint the mass directly with a brush wide enough to cover it in a
few strokes, and let the *edge of the mass* be the drawing. There is no outline in
a painting — there is a place where one mass stops.

**Finding an edge is the same mistake in disguise.** When a silhouette is not crisp
enough, the reflex is to run a thin dark stroke along it. That stroke is an
outline, and it reads as one the moment you look — a drawn line around a painted
shape. Sharpen an edge by painting the mass on the *other side* of it: a brush at
least `0.03` wide, running along the boundary with its centre outside the shape,
laying the background's own colour up to where the shape stops. The edge is then
where two masses meet, which is the only kind of edge a painting has.

**Masses that are not rectangles.** Almost nothing you want to paint is a box, and
you will be tempted to paint boxes anyway, because a rectangle is the easiest place
to name. If you block in a shaped mass as a box you get a box, and no amount of
later work removes that. There are two ways not to, and they answer different
questions.

**When you can say what shape the mass is**, build it and fill it. Five ways to make
one, none of which needs you to invent coordinates:

```python
blob(cell("D5"), 0.22, wobble=0.3, seed=2)     # an irregular mass filling a cell
ellipse(span("C3", "E5"))                      # a round mass filling a run of cells
hull([s.pt("top_l"), s.pt("top_r"), s.pt("base")])   # the mass around your landmarks
ribbon([(0.15, 0.8), (0.5, 0.55), (0.9, 0.62)], 0.18)   # a mass following a line
polygon([(0.2, 0.9), (0.35, 0.4), (0.6, 0.5), (0.7, 0.95)])   # an outline you have
```

Look at it before you spend twenty passes on it, then fill it along its own axis:

```python
shape = blob(span("D4", "F6"), wobble=0.35, seed=5)
s.preview(shape)                                    # the silhouette, painting nothing
s.block_in(shape, "bristle", "dark", direction="axis", density=0.9, size=0.12)
```

A shaped block-in costs about what its box would: the passes are counted across the
mass, not over its area. A mass with a bite out of it keeps the bite — one pass across
a concave shape comes back as the two pieces that are really inside it.

**Read "what its box would" literally, because for a long curved shape the box is the
whole story and the mass is not.** The passes step across the *bounding box*, so a
ribbon that bends pays for the box its bend sweeps out rather than for its own width. A
ribbon `0.029` wide at `size=0.015` costs **3 passes** laid straight and **19** with a
curve in it — the same ribbon, the same brush. A painter budgeted 4 for one and paid
21, which was 7% of its stroke budget on a single call and nearly cost it the strokes
for the rest of the picture. **Before you block in anything long and curved, look at
`shape.box` and cost it off that.**

**The paint still lands outside the shape, and it is the most expensive first mistake
with shapes.** A pass stops when its *centre* reaches the boundary, so the brush hangs
over — and with a brush that is a large fraction of the mass, the silhouette you built
simply disappears, taking its neighbours with it. **Keep the brush under about a fifth
of the mass's width, or `inset()` the shape by half the brush size.**

```python
mass = blob(span("D4", "F6"), wobble=0.3, seed=2)
s.block_in(mass.inset(0.045), "flat", "dark", size=0.09)   # inset by half the brush
s.block_in(mass, "flat", "dark", size=0.06)                # or keep the brush small
s.block_in(mass, "flat", "dark", size=0.09, edge="clean")  # or ask for a drawn contour
```

**`edge="clean"` is those two steps and a third.** It insets the fill by half the
brush, lays it, and then sweeps one pass along the inset outline in the same colour,
so the *outer half* of the brush lands on the line you drew. It costs one stroke more
than the same mass ragged. Reach for it when the silhouette **is** the drawing, and
especially with a round tip on a small mass, where the half-brush overhang arrives as
a fringe of separate discs around the shape rather than as a soft edge, and reads as
spray. Measured on a mass a third of the canvas across with a round
tip at `size=0.05`: paint reaches **20px** past the outline ragged and **13px** clean,
and the clean silhouette is the less ragged of the two.

**Use a solid tip for it.** A `bristle` pulls the paint in too, but one comb pass
along a contour covers about three-quarters of its width, so it leaves a *stringier*
outline than the ragged fill did — and says so when you ask for it.

Where your outline runs off the canvas the inset is dropped, because there is no drawn
line out there for the brush to land on and **a mass that meets the frame should run
off it** — so draw it past the edge and let it.

The default, `edge="ragged"`, is right for everything else: a mass sitting behind
other things wants the brush to break past its boundary, because that is what a brush
does and the mass in front will cover it.

**On a shape that is not convex, `inset()` takes far more than a rim, and it takes it
out of the thin parts first.** Erosion pulls in from every boundary at once, so a lobe
narrower than twice the inset disappears entirely while the body of the mass barely
changes. Measured on a real fifteen-point outline, `inset(0.052)` kept **62.7%** of the
shape's area: the block-in then covered 98.4% of what it was given and **76.2% of the
mass the painter meant**, with one whole limb at 15.5% — bare canvas, found twenty
strokes later by `compare()` and six strokes to fill.

**So preview the inset shape, not the shape.** `CALIBRATION.md`'s coverage figure is
measured on a blob, and a blob is convex.

```python
mass = polygon([(0.30, 0.30), (0.70, 0.30), (0.70, 0.44), (0.44, 0.44),
                (0.44, 0.62), (0.70, 0.62), (0.70, 0.78), (0.30, 0.78)])
s.preview(mass.inset(0.045))                # what you are about to fill, not what you drew
```

Worth a `preview()` every time. And **do not cross a small shaped mass** — the
crossing below is for masses several brushes across; on a small one it serrates its own
boundary.

**When what you have is one boundary** — the edge that matters, read off the grid —
give it to `sweep` and let the passes follow it:

```python
edge = [(0.06, 0.68), (0.31, 0.48), (0.56, 0.63), (0.84, 0.45)]   # read off the grid
s.sweep(edge, "bristle", "dark", into="down", depth=0.30, size=0.12, cross=25)
```

`sweep` runs its first pass along the edge and steps each one after it a part-brush
further into the mass, alternating direction the way `block_in` does. Passes that
run *along* the edge describe the form; columns that hang *down* from it comb the
mass into strands and print the canvas's axis over the whole thing.

- `into=` is which side of the edge the mass is on, and you have to say: a compass
  word or an angle steps every pass the same way, which is the hand working down a
  near-horizontal edge, and an `(x, y)` point *inside* the mass makes the passes
  follow a curved edge instead of shearing off it. A boundary that closes on itself
  needs neither — `closed=True`, and the mass is what it encloses. A shape is such a
  boundary: `s.sweep(shape, "bristle", "dark", depth=0.2)` sweeps round its own
  outline.
- `cross=` is the second set of passes, leaning that many degrees across the first.
  **Take it** — one sweep on its own comes out stringy, and the crossing is what
  closes the mass up. Twenty to thirty degrees is usually enough, and **`cross=0` is not how you decline it** — that raises. Leave the argument out. A shaped `block_in`
  has the same problem and the same answer, `direction=("axis", 90)`.
- `depth=` is how far into the mass to go, and the brush decides how many passes
  that takes unless you say `passes=`.

**Which one?** Fill a shape when you can see the whole silhouette and want it
covered; sweep when one edge is the thing you care about, or when the passes
following the form is the point. And if the mass is close enough to a box that
either feels like overkill, `block_in` at the angle the mass runs at is the cheaper
version of the same idea.

**The mass that needed no drawing is the one that will give you away.** You will reach
for a shape on your subject, because its silhouette was a problem you had to solve,
and then lay everything behind it in boxes because nothing back there asked anything of
you. That is backwards. A viewer expects construction on the subject and forgives it;
a background of square patches, every edge parallel to the canvas, reads instantly as
made by a machine. **Give the masses that needed no drawing the same treatment as the
ones that did** — see *The angle of the mark*, which is the same rule and the loudest
tell in this engine.

**And the marks inside it are not parallel lines.** This is the half that gets missed,
and missing it is worse than leaving the background alone: told to work a quiet mass, a
painter reaches for the texture of what it is — grain, weave, brick, ripple — and lays
it as a row of long strokes all running the same way, which is a stack of bands with a
different name. A measured run came out *squarer* than the one that ignored the
background entirely. If a surface has a grain, the grain **varies**: it breaks, it
crosses, it disappears for a whole passage. Three marks that describe it beat thirty
that repeat it.

**The shape is a place, not a line.** Nothing draws that outline, and you must not
either: the silhouette is where this mass's paint stops and the mass behind it still
shows, which is why the far masses go down first.

**A hole in a mass is painted the same way, and it is easy to get exactly wrong.**
The reflex is to dab the background colour into the middle of the mass, and what
that gives you is a row of floating discs — the brush's own shape, announcing
itself. **A gap is a broken sliver worked in from the silhouette with a starved
brush**, not a dot in the interior: the light comes in from the edge of the mass,
so that is where the hole opens.

```python
s.stroke([(0.42, 0.36), (0.47, 0.41)], "round_hard", "pale",
         size=0.012, load=0.3, opacity=0.7)      # in from the edge, not a dot
```


**When something is wrong, paint over it.** Your instinct will be to reach for
`undo`. Resist it. Real repairs happen with paint: let the area dry, then work over
it opaquely.

**Burying something takes a particular kind of mark, and the wrong one leaves a
worse mess than the mistake.** A `bristle` does not bury — its comb leaves the old
paint showing between the streaks, however high you push the opacity. A `flat` or
`knife` buries and leaves a rectangle with chisel ends. A `round_hard` buries and
leaves a capsule with rounded ends. What works:

```python
s.cover(cell("D5"), "corrected_colour")      # the whole recipe, already set
```

That is the repair. `cover` dries the area, then blocks it in with every clause of
the recipe in place, and what those clauses are is worth knowing because you will
sometimes want them on a stroke of your own:

```python
s.dry()                                                     # so new paint covers
s.stroke([(-0.05, 0.55), (1.05, 0.58)], "flat", "corrected_colour",
         size=0.09, load=1.0, load_falloff=0.0, opacity=1.0, pressure="even")
```

**A long stroke, a solid tip, `load=1.0`, `load_falloff=0.0`, full opacity, run along
the grain of what is already there so that its own ends fall outside the area you are
fixing.** Every clause earns its place: a solid tip because a comb does not cover,
full load because a starved brush leaves a speckled film that everything after it
sits on, `load_falloff=0.0` because a full-width stroke at `load=1.0` **still runs dry
and speckles at its far end** without it, and the ends outside because an oriented
tip's chisel end is a straight edge you did not intend wherever it stops inside the
picture.

**Repairing a mass that already has things standing on it is a different job, and it
needs a method rather than a warning.** Repainting the mass buries the fine marks on
it, which are the expensive ones. The only approach that has worked across six
sessions: **keep every mass and every near thing in its own named function, and
re-run the whole stack in depth order.** The repair then goes in at its own depth and
the near things go back on top of it, because they were never a one-off.

```python
def far_mass():  s.block_in("upper-half", "flat", "shadow", size=0.16)
def near_mass(): s.block_in(span("A4", "H6"), "flat", "mid", size=0.14)
def details():   s.stroke(path, "round_hard", "light", size=0.02)

for layer in (far_mass, near_mass, details):     # fix one, re-run all of them
    layer()
```

That is what back-to-front costs at repair time, and it is cheaper than the
alternative every time you need it twice.

`undo(n)` exists and is documented below, but treat it as scraping the canvas —
something you do occasionally and reluctantly, not a free rewind. **`n` counts log
entries, not marks you paid for**, so an `undo(3)` spanning a pencil line gives you
back two strokes. Painting over leaves a history in the surface that is part of why
paintings look alive.

**You will under-vary your marks.** Real brushwork varies in width, pressure,
direction and opacity constantly. If every stroke uses the same brush at the same
size with the same pressure, the result will look mechanical no matter how good the
drawing is. Change `size`, change `pressure`, change direction between passes.

**And you will under-vary your *objects*, which is the same fault one level up and
much harder to see.** Having worked out how to paint one of a thing, you will paint
the next one with the same recipe, and a viewer reads three copies of one object
rather than three of a kind. The fix is cheap and has to be deliberate: **vary one
thing per object on purpose** — which way its light falls, how sharp its edge is,
how much of it the mass in front takes away. One difference each is enough; the
recipe repeated exactly is what gives you away.

**You will use too many strokes on detail and too few on structure.** A good
painting is mostly big statements. Budget for it: if you are 200 strokes in and
still adjusting the big masses, that is fine. If you are 50 strokes in and painting
tiny marks, you are in trouble.

---

## Colour

You have a limited palette, and no black. This is on purpose: mixed darks are alive,
tube black is dead.

```
titanium_white
cadmium_yellow  lemon_yellow        (warm, cool)
cadmium_red     alizarin            (warm, cool)
ultramarine     cerulean            (warm, cool)
burnt_umber     yellow_ochre  burnt_sienna  viridian
```

Short aliases: `white`, `yellow`, `red`, `blue`, `umber`, `ochre`, `sienna`.

Mix on the palette, name what you mix, and reuse it. Naming your mixtures is how you
keep a painting coherent — the same three or four mixtures repeated across a canvas
is most of what "colour harmony" actually means.

```python
s.palette["shadow"] = s.palette.mix("ultramarine", "burnt_umber", 0.4)
s.palette["light"]  = s.palette.tint("yellow_ochre", 0.5)      # toward white
s.palette["muted"]  = s.palette.desaturate("cerulean", 0.3)    # keeps its value

s.stroke([...], "bristle", "shadow")     # refer to it by name later
```

| Method | What it does |
|---|---|
| `mix(a, b, ratio)` | `ratio` is how much of `b`. Mixes like paint, not like light. |
| `tint(c, amount)` | Lighter, by adding white. |
| `shade(c, amount)` | Darker, by adding umber — never black. |
| `desaturate(c, amount)` | Knocks a colour back without changing how light it reads. |
| `value_of(c)` | How light it reads, `0.0`–`1.0`. Useful for planning values. |
| `hex(c)` | The sRGB hex, for your own notes. |

**Supplying a colour of your own.** A slot takes a hex string or a linear RGB triple,
and what you supply lands exactly as written — including a black, and including
anything below the darkest mixture the box can reach:

```python
s.palette["ink"] = "#0d0c10"           # hex string
s.palette["ink"] = (0.05, 0.05, 0.07)  # linear RGB, 0.0-1.0
```

**A list of 0–255 integers is not one of the forms**, and it does not raise — it
clamps, so `[13, 12, 16]` gives you white. If you supply a colour, print
`value_of()` on it before you paint a field of it.

Reach for this when a reference genuinely goes below the palette's floor (step 3),
and not otherwise: the box has no black because mixed darks are alive, and a slot
full of tube black is the fastest way to a dead painting. Most dark references do not
need it — see the floor arithmetic in step 3.

Three things about the mixing that will surprise you:

- **Blue and yellow make green**, red and blue make violet, and complements make
  lively greys. This is subtractive pigment mixing, not RGB averaging.
- **White is a weaker lightener than you expect.** If you want a really pale colour,
  use more white than feels right.
- **A yellow and a blue make green even when you were after a grey**, and tinting
  does not undo it. Neutral greys come from complements, or from earth and white,
  or from `desaturate`. Print `hex()` of a mixture before you paint a field of it.

---

## Wet paint

Paint lands wet and stays wet for a while. Paint that lands on wet paint **mixes**
with it instead of covering it.

This is the single most common surprise. Lay yellow over still-wet blue and you get
green, not yellow. That is not a bug — it is how paint works, and used deliberately
it is how you get soft transitions for free.

```python
# Blend on purpose: work into wet paint.
s.block_in(cell("C3"), "bristle", "cerulean", density=1.0)
s.stroke([(0.3, 0.3), (0.5, 0.35)], "bristle", "titanium_white")   # blends in

# Or cover cleanly: dry first.
s.dry()                                                    # whole canvas
s.dry(0.5, region="upper-half")                            # partial, one region
s.stroke([(0.3, 0.3), (0.5, 0.35)], "bristle", "titanium_white")   # sits on top
```

**Rule of thumb: if you want the new colour to read as itself, `dry()` first.**

**Wet is a matter of a few strokes, not a whole pass.** Wetness fades with every
mark you make anywhere on the canvas, and one `block_in` is many marks — so by the
time you have blocked in a second mass, the first is already most of the way dry.
If you actually want two colours to mix on the canvas, put the second one down
within a few strokes of the first.

A `glaze` is the opposite move — a thin transparent film over dry paint that shifts
the colour underneath without hiding it:

```python
s.glaze([(0.2, 0.6), (0.8, 0.6)], "alizarin", opacity=0.15)
```

---

## The brushes

One line each. Reach for `bristle` for marks that have a direction and `flat` for
quiet masses.

| Brush | What it is for |
|---|---|
| `bristle` | **The workhorse** for any mark with a direction. Broken, streaky, alive — and never solid. |
| `flat` | Block-in, chisel edges, flat planes. Turns to follow the stroke. |
| `round_hard` | Deliberate marks, accents, small shapes, final highlights. |
| `liner` | Fine lines at the scale of a feature. `round_hard` at `size=0.005` with no jitter at all, and it holds its load. |
| `round_soft` | Blending and soft edges. The least painterly — use it sparingly, and never for a mass: above about `size=0.05` it airbrushes. |
| `knife` | Thick slabs with a hard edge. Drags what it crosses. Use rarely, for punctuation, and keep it close in value to what it lands on or it reads as something stuck to the surface. |
| `smudge` | Carries no paint; moves what is already there. For losing edges. |

**A `bristle` stroke is never solid** — it lays a comb of streaks, which is what makes
it alive on a mark whose direction you mean. Lay a big quiet mass with `flat`, or with
bristle passes that *cross*; single parallel passes rib it. Below about `size=0.02` a
bristle is four streaks with gaps, not a brush: small solid planes want `flat` at
`pressure="even"`, or `round_hard`.

**A short `flat` or `knife` stroke is a rectangle.** The oriented tips hold a chisel
square to their travel — right for a mass, wrong for an accent, and they do not taper
under a pressure list. **Small accents want `round_hard`. `flat` and `knife` want a
length.**

### The shape each tool leaves behind

That last rule is the most useful sentence in this guide, and it is one of a family.
**Every tool here has a geometry of its own, and if you do not decide the shape, the
tool decides it for you** — then you spend twenty marks fighting a structure you never
chose. What each one leaves when you are not watching:

| Reach for | and if you are not watching, you get |
|---|---|
| `flat` / `knife`, short | a rectangle with chisel ends |
| `round_hard`, short | a capsule. It needs to be about **7×** longer than it is wide before it stops reading as one |
| `round_hard` or `liner`, several small marks | **one disc, printed over and over.** A round tip draws the same silhouette every time, so five small marks are five copies — unless you give the tip an outline of its own with `tip_wobble=0.7`, which redraws it per mark |
| `bristle` below `size≈0.025` | a comb: a woven strap across a band, or a ladder of evenly spaced ticks along an edge |
| `sweep` round a closed shape | **concentric rings**, because the passes step inward from the boundary |
| several overlapping `blob`s | a dome — blobs of similar size average to a circle and the irregularities cancel |
| a shallow shape, passes along its long axis | **its bounding box** |
| any loop or generator you write | its own statistical signature: one density, one mark length, no clumps and no holes |
| repair laid on repair, always additive | horizontal strata, one visible edge per repaint |

Two of those need more than a row.

**The shallow-shape one is not covered by the brush-width rule.** An ellipse
`0.256 × 0.128` filled with a `flat` at `0.022` — a twelfth of the mass's width, well
inside the "keep the brush under about a fifth" rule below — came out a rectangle.
**The dimension that matters is the mass's extent *perpendicular to the passes*, not
its width.** Run the passes across the short way, or turn them:

```python
s.block_in(ellipse(span("D4", "F5")), "flat", "mid", direction=90, size=0.022)
```

**And a mass much longer than it is wide is a stroke, not a mass.** `block_in` will
comb a `0.022 × 0.18` band even at `density=1.0` with `direction="axis"`. A long
`stroke()` is the right tool; `block_in` is for something with two dimensions.

Size is a fraction of the canvas's long side. `0.2` is a big brush, `0.02` a small one.
**On a canvas that is not square that is not the same unit as a coordinate**: `size` is a
fraction of the long side while `y` is normalised over the short one, so a brush hangs
over a shape by a different amount vertically than horizontally. It is the reason a
mass you placed by number comes back a little taller than you drew it.
**Use a bigger brush than feels comfortable**, especially early — but that is advice
about *masses*. **Scale a mark off the thing it describes, not off the canvas**;
carrying the big brush down to something small costs a repaint. The numbers are in
`CALIBRATION.md`.

### The angle of the mark

**Do not let the canvas choose your stroke direction.** This is the loudest tell in
every painting made with this engine so far, and it is the easiest to fix. Left
alone, everything here runs horizontally or vertically: `block_in`'s named
directions are horizontal, vertical and a 45° diagonal; every named region is an
axis-aligned rectangle; and an oriented tip is held square to its travel, so a
horizontal stroke necessarily ends on a vertical edge. Paint a sloping mass with
horizontal passes and you get a stack of bars with flat ends.

**Sweep a mass along its own axis.** `block_in` takes a number of degrees, clockwise
from horizontal, as well as the four names:

```python
s.block_in(span("A4", "F7"), "flat", "shadow", direction=28, size=0.12)
s.block_in(span("A4", "F7"), "flat", "shadow", direction=(28, 118), size=0.12)  # crossed
s.block_in(ribbon([(0.2, 0.8), (0.8, 0.4)], 0.2), "flat", "shadow", direction="axis")
```

`direction="axis"` is the mass answering the question itself: it sweeps along the
long axis of the shape (or of the rectangle) you gave it, so you do not have to work
the angle out.

Passes that run along the form cover it in fewer strokes than passes that step
down it, and they come out visibly less square. Measured, if you want the numbers,
in `CALIBRATION.md`.

**Turn the blade.** Any oriented tip can be pinned instead of following its travel:

```python
s.stroke(path, "knife", "light", size=0.09, angle_follow=False, angle=45)
```

At 45° the knife lays a parallelogram; at 90° it is edge-on and draws a ribbon
instead of a slab. This matters most at the *ends* of marks and on short ones — on a
long sweep the path direction does nearly all the work, so fix the path first and
reach for the angle for a mark whose termination you can see.

**A round tip is the tip that declares no axis.** `round_hard` has no orientation at
all, so it cannot print the canvas's grain into a mass however you drive it. When a
passage keeps coming out square and you have already fixed the direction, that is
the brush to change to — not `round_soft`, which airbrushes at any size a mass needs.

### Per-stroke overrides

Anything about a brush can be overridden per stroke — and per **mass**: `block_in`
and `sweep` take the same keywords and pass them down to every stroke they emit.

```python
s.stroke(path, "bristle", "shadow", size=0.14, opacity=0.5)
s.stroke(path, "flat", "light", hardness=0.9, jitter=0.05, load=0.4)
s.stroke(path, "bristle", "shadow", size=0.12, load_falloff=0.25)   # runs dry slower
s.block_in(cell("D5"), "flat", "shadow", opacity=0.5, load=0.8)     # masses too
```

**`opacity` does not thin a long stroke, it only slows it down.** Dabs overlap, so a
low opacity accumulates back to nearly full colour. If you want a soft film, that is
what `glaze()` is for.

**`load` is how much paint the brush carries**, and dropping it is how you get dry
brush — one of the best tools you have for making a surface look worked. But pass
`load=1.0` explicitly for anything that has to read as a *solid* mass, a correction
included; a pass laid low because it sounded painterly leaves a speckled film that
everything after it sits on. On a mass, `solid=True` is that clause, together with the
`load_falloff=0.0` that keeps the far end of each pass from running dry as well.

**`tip_wobble` gives a round tip a silhouette of its own**, redrawn for every mark the
way a bristle's comb is, so a handful of small marks are not a handful of copies of one
disc. `0` is the disc; `0.35` is a brush set down once; `0.7` and up is a clot. Only
the round tips take it — a `flat` or a `knife` is a chisel, and its rectangle is the
mass it lays.

```python
s.dab(0.42, 0.36, "round_hard", "light", size=0.016, press=3, tip_wobble=0.7)
```

**A loaded brush runs dry along a stroke**, so where a long stroke ends is where its
texture is loudest — and if every stroke in a field runs the same way, one side of the
field speckles. Run the next one back the other way. **Do not lay one broken pass
across the whole canvas**: edge to edge on a single load prints the canvas's own
texture as an even field over everything, and it stays visible under every later
stroke.

Windows, falloff numbers and what each texture does are in `CALIBRATION.md`; if a
stroke seems to have vanished, `s.log()` says how much paint it laid.

### Pressure

`pressure` shapes the stroke along its length:

- `"taper"` — lands light, presses, lifts off. **The default, and usually right.**
- `"press_in"` — starts light, ends heavy.
- `"lift_off"` — starts heavy, trails away.
- `"even"` — constant. Use it deliberately; it is the flattest-looking option.
- `"swell"` — thin, thick in the middle, thin.
- `"dab"` — heavy at the start, gone quickly.

Or pass a number, or a list interpolated along the stroke: `pressure=[0.2, 1.0, 0.3]`.

**On a round tip — `round_hard`, `round_soft`, `liner` — pressure changes how wide
the mark is as well as how much paint lands.** `size` is its width at full pressure,
and it never thins below about a pixel and a half however light the touch. **On the
oriented tips — `flat`, `bristle`, `knife` — it changes only how much paint lands**,
because a flat brush's width is the mass it lays and you want that to be the width
you asked for. So:

- **A mark that tapers is one stroke.** `pressure=[1, 0]` starts at the width you
  asked for and ends at a point.
- The *paint* half of the profile shows most clearly on short strokes and on a
  colour that is not already at full strength — on a long stroke the overlapping
  dabs saturate and `taper` and `even` land much the same weight, even where they
  differ in width.
- **Varying the width of your masses is still your job**, because the brushes that
  lay masses do not vary with pressure. Pass a different `size`. That is the single
  most effective thing you can do to stop a painting looking mechanical.

**At the scale of a feature** the brushes go as small as anything you will paint.
What changes is not the brush: a single dab is a *light touch* — the start of a
`taper`, so it lands a fraction of its colour at about half the width you asked for
— and a small highlight is `s.dab(x, y, ..., press=3)`, three stamps on the same
spot, the middle one at full pressure, and **one** stroke against your budget. The
three-marks rule for anything cell-sized or smaller is in step 6, where you will be
when you need it.

**Use `press=3` for anything you actually want to land.** `CALIBRATION.md`'s numbers
for the lighter touches are measured with white on three grounds, and a dark accent on
a lit passage behaves nothing like that: a near-black accent at `press=2` did not
register at all, and cost a painter one of its last ten strokes to lay again. `press=1` and
`press=2` are whispers — reach for them when a whisper is the mark you want, not when
you are being careful.

---

## Looking

```python
s.look()                                  # plain view, downsampled
s.look(grid=True)                         # labelled grid — name places
s.look(values=True)                       # greyscale — judge value structure
s.look(region="upper-left")               # crop, full resolution — inspect closely
s.look(region=cell("D6"))
s.look(diff=True)                         # tint what changed since the last look
s.look(reference="ref.jpg")               # reference beside your painting
s.look(scale=None)                        # full resolution
s.look(region=cell("D4"), reference="ref.jpg", grid="fine")   # both panels, tenths
s.look(sketch=False)                      # hide the pencil underdrawing
```

A `region=` crop is at full resolution, and a small one is enlarged so that a single
cell fills the panel. `region=span("D2", "E4")` is the usual size for inspecting a
passage, and a single cell is the size for a feature. Regions can be written as
strings anywhere: `region="D4"`, `region="C3:F6"`, `region="upper-band"`.

With a reference, a `region=` crop crops **both** panels to the same place,
`grid=True` labels both with the same cells, and `values=True` converts both to
greyscale on the same scale — every view is a like-for-like comparison.

Each look writes a numbered PNG under `out/` — `out/look_001.png`, `out/look_002.png`
and so on — and returns the path. Print it and open that file. Rehearsals have their
own run of numbers, `rehearse_001.png` upward, and each takes the next free name: that
is what lets you rehearse a pass three ways and put the three side by side, which is
most of what rehearsing is for. The look numbering belongs to the session, so a second
session started in the same directory begins again at `look_001.png` and writes over
the first one's; copy anything you want to keep.
**This bites hardest when you paint more than one picture**: a second painting in the
same directory silently overwrites the first painting's entire record of itself, looks
and rehearsals alike. Give each painting its own directory, or copy out the frames
that matter before you start the next one.

Use `values=True` far more often than feels necessary. Use `diff=True` after a pass
to confirm you changed what you meant to change and nothing else.

When a mark seems to have gone missing, `s.log()` says how much paint each one
actually laid, and prints `NO PAINT LANDED` for a mark that changed nothing at all —
usually an opacity of zero, or a glaze into paint that is still soaking wet.

---

## The rest of the API

What each call *is*, in the order you reach for them. What each argument means, what
unit it is in and what it defaults to is one page in
[`REFERENCE.md`](REFERENCE.md) — look a fact up there rather than hunting it here.

```python
s.stroke(points, brush, color, pressure="taper", size=None, opacity=None, note="")
s.dab(x, y, brush, color, size=..., press=1)       # one mark; press stamps it again
s.block_in(place, brush, color, direction=, density=, overhang=, edge=, solid=)  # a mass
s.sweep(edge, brush, color, into=, depth=, cross=, passes=)         # a mass with a shape
s.scumble(band, color_a, color_b, n=8)             # a soft passage, as n strokes
s.scumble(patch, a, b, n, direction="inward")      # ...falling off from its middle
s.cover(place, color)                              # bury a mistake; the whole recipe
s.smudge(edge, size=)                              # move paint along a boundary:
                                                   # points, or a shape's own outline
s.glaze(points, color, opacity=)                   # thin transparent film
s.dry(amount=1.0, region=None)
s.undo(n)                                          # scraping, not free
s.look(...)

s.pencil(points, pressure=0.55)                    # graphite; not a stroke
s.erase(region=None)                               # rub the drawing out
s.sketch_lines()                                   # every line drawn, as points
s.mark(name, x, y)   s.pt(name)   s.unmark(name)   # named landmarks
s.preview(strokes, reference=, region=, grid=)     # where a mark would go
s.rehearse(strokes, reference=, region=)           # what it would look like
s.cost(strokes)                                    # what it would charge
s.cost_line(strokes)                               # ...and why it charges it
s.paint(plan)                                      # ...and now paint that same plan
s.scratch()                                        # a throwaway copy to try a pass on
s.compare(reference, region=None)                  # per-cell value numbers
s.compare({place: value, ...})                     # ...or against your own value plan
s.prepare(reference, level="coarse")               # the reference, cut up
s.look_areas()                                     # the map again, after merging
s.export("painting.png")
s.timelapse_gif("painting.gif", fps=8.0, every=1, scale=None)
s.contact_sheet("sheet.png", columns=6)            # the time-lapse as a grid
s.log(last=10)                                     # last=10_000 for the whole record
s.spent  s.remaining  s.budget_line()              # if the session carries a budget
```

`block_in` takes `direction=` of `"horizontal"`, `"vertical"`, `"diagonal"`,
`"cross"`, `"axis"` (the place's own long axis), **a number of degrees**, or a
sequence of any of those for one pass each. Two passes of parallel strokes look like
hatching; crossed passes look like paint.

Both space their passes a part-brush apart, which assumes a pass is one brush wide
all along — true of `flat`, `bristle` and `knife`, and not of a round tip under a
varying pressure. Lay masses with `flat` or `bristle`; if you want a round tip for
one, give it `pressure="even"` or it will show its passes at their ends.

One `block_in` is not one stroke: it lays a pass for every brush-width of the
region, so a big region with a small brush is twenty or thirty of them. Neither is
one `sweep` — a pass per part-brush of `depth`, and two or three times that again
if you cross it. Check `s.stroke_count` if you are keeping a budget — a whole
painting is usually a few hundred marks, not a few thousand.

**A mass can be costed before the call rather than discovered after it** —
`CALIBRATION.md` has the arithmetic, and it is the difference between planning a pass
and finding out.

**What counts against the budget:** `stroke`, `dab`, `block_in` and `sweep` per pass,
and also **`smudge` and `glaze`** — those two are marks like any other. What is free:
`pencil`, `erase`, `mark`, `look`, `preview`, `rehearse` and `compare`. Do not
discover the first list with three strokes left.

**`block_in` paints past a rectangle** by a fraction of a brush on every side, and
past a *shape* by up to three-quarters of a brush — see **Masses that are not
rectangles** for what that costs and how to inset for it. That spill is fine for a
band and wrong for a mass that meets another at the *same* depth, where it lands on
its neighbour. Painting back to front is the real answer — the far mass spilling into
where the near one is going does no harm, because the near one goes on over it next.

**`overhang` is not the remedy: it controls the ends of each pass, not its sides.**
Measured on a band at `x 0.2–0.8, y 0.585–0.775` with a `bristle` at `size=0.11`, the
passes running horizontally: `overhang=0` laid paint from `x 0.181` to `0.825`, the
default `0.35` from `0.145` to `0.854`, and `1.0` from `0.072` to `0.924` — while the
*sides* sat at `y 0.530–0.844` in all three, about half a brush past the band either
way, unmoved. **For two masses at the same depth, inset the place by half the brush
size.** That is the half of the old advice that works.

`compare(region=cell("D4"))` measures the tenths of one cell and labels them the
way `grid="fine"` does.

Places:

```python
region("top-left")   # also: top, center, upper-half, lower-half, left-half,
                     # inner, middle-band, upper-band, lower-band, all, ...
cell("D6")           # a grid cell, matching look(grid=True)
span("E5", "H8")     # the rectangle from one cell to another, both included
horizon(0.42)        # a thin band at that height
below(r, 0.15)  above(r, ...)  left_of(r, ...)  right_of(r, ...)  between(a, b)
r.point(0.5, 0.5)    # a point inside a region, in the region's own 0–1 space
r.inset(0.05)  r.scaled(0.8)  r.split_h(3)  r.split_v(2)
```

Shapes — a mass that is not a box. Every one of these is a place like the ones
above, and goes anywhere a region goes:

```python
blob(place, radius, wobble=0.25, seed=0)   # an irregular silhouette
ellipse(place, rx, ry, rotate=0)           # round, or filling the place given
s.circle(place, r, wobble=0)               # round *in pixels* — see Getting started
hull([p1, p2, p3])                         # the mass around three or four points
union(a, b)                                # one silhouette round two that overlap
ribbon(points, width, end_width=None)      # a mass running along a line
polygon(points)                            # an outline you already have
shape.inset(0.03)  shape.scaled(0.9)  shape.shifted(0.02, 0)   # ... as a region does
shape.smooth()                             # cut the corners off an outline
shape.axis   shape.area   shape.center   shape.contains(x, y)   shape.closed
```

**`hull` and `union` are not the same join.** A hull covers everything given, but
convexly: two circles come back as a lozenge with the waist between them filled in.
`union` keeps the waist, which is usually the reason there were two circles. The
shapes have to overlap, because what comes back is one silhouette:

```python
lobed = union(s.circle((0.45, 0.42), 0.05), s.circle((0.45, 0.56), 0.08)).smooth()
s.block_in(lobed, "flat", "ochre", size=0.04, edge="clean")
```

`smooth()` cuts the corners off an outline, twice by default. A shape built from a
dozen points has a dozen corners, and a round tip laid along it leaves a scalloped
edge that reads as faceting rather than as form.

`place` is a point `(x, y)` or any region — `blob(cell("D5"))` is an irregular mass
filling that cell. `shape.closed` is the outline as a path, for `s.pencil(...)` or
`s.preview(...)`; `s.sweep(shape, ...)` takes the shape itself. `shape.box` is the
rectangle around it.

Under `easel run` all of these are already in scope. In a plain Python script,
import them: `from easel import Session, Region, region, cell, span, horizon,
below, above, left_of, right_of, between, blob, ellipse, hull, ribbon, polygon`.

---

## Eight small exercises

Run these before painting anything real. They take a minute each and will teach you
the engine's feel faster than reading will.

**They are a gate, and here is what going round it costs.** A painter who skipped all
eight met two of the lessons inside the picture instead: a wide soft passage laid as
four hard bars — exercise 5 and *step 4* — and a surface whose grain came out as a row
of parallel stripes, which is *The angle of the mark*. Between them they cost more
strokes than the eight exercises would have, and they cost them at the worst moment,
with the rest of the picture already standing on the masses that had to be repainted.
That is the whole argument: an exercise is the one place in this engine where a
mistake has nothing built on top of it. **Do the eight. Then start.**

**1. A value scale.** Nine even steps from the darkest mix to white. This
calibrates your sense of what the palette reaches, and it teaches the one thing
about white you will otherwise learn the expensive way.

Mix to a *value*, not to a ratio. Equal spoonfuls of white do not give equal steps:
white is much stronger than its share of the mixture, so ask for the value you want
and let a search find the ratio.

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

`p.at_value(base, target)` is the search: it hands back the *mixture* of `base` that
reads at `target`. Do not interpolate toward it by hand. White is much stronger than
its share of the mixture — a third of white gets you the first step of nine and it
takes nine tenths to reach the eighth — and that curve is why a mixture that "should"
be halfway comes out too dark, and why the fix is always to add more white than feels
right.

**It goes both ways.** Adding white raises a colour; to lower one it mixes in a dark,
so you can hit a planned value from whichever side the mixture starts on, which is
what planning values actually asks for:

```python
s.block_in(cell("D5"), "flat", p.at_value("shadow", 0.45))   # up from the dark
s.block_in(cell("D6"), "flat", p.at_value("ochre", 0.30))    # and down from a light
```

The default dark is the blue-umber the palette is built around rather than a black it
does not have, so lowering a value keeps a colour that still has a hue in it. Ask for
a value the box cannot reach and it **raises rather than handing back the nearest it
managed** — a painter who asks for `0.30`, is silently given `0.41`, and finds out
when `compare()` says so has lost a mass, not a mixture.

**2. One stroke, six pressures.** See what the profiles actually do. On the round
brush on the left they change the *width* of the mark as well; on the `bristle` on
the right they change only how much paint lands. The low `opacity` and the flat
`load_falloff` are what make the paint half legible: at full strength the
overlapping dabs saturate and every profile lays the same weight, and paint running
out along the stroke hides the profile behind its own fade.

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

**3. Paint running out.** The same stroke at four loads, on rough canvas.

```python
from easel import Session

s = Session(900, 400, texture="rough", ground="toned_grey", seed=3)
for i, load in enumerate([1.0, 0.6, 0.35, 0.2]):
    y = 0.15 + i * 0.22
    s.stroke([(0.06, y), (0.94, y)], "bristle", "titanium_white",
             size=0.07, load=load, load_falloff=0.0, pressure="even")
s.look()
```

**4. Wet versus dry.** The same yellow over blue, once into wet paint and once onto
dry. This is the lesson that will otherwise cost you a painting. Each band is laid
with a *single* stroke, not a `block_in`, because a block-in is many strokes and
the wet half would have dried before the yellow arrived.

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

**5. An edge study.** One soft edge, one hard, one lost. Look at which one your eye
goes to.

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
s.smudge([(0.35, 0.3), (0.35, 0.7)], size=0.09)              # soft
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

**7. Draw, try, paint.** The whole precision loop on an abstract shape. Do this one
before any copy: it is four calls, and it is how a feature gets painted.

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

Three things to notice. The two rehearsals cost nothing and neither appears in
`s.log()`. The drawing did not count against `s.stroke_count`. And the graphite has
vanished exactly where the paint landed and survived everywhere else — which is what
an underdrawing is for, and why making it disappear is the painting.

**8. A box and a shape.** The same mass twice, so you can see the difference before
you have to judge it in a painting.

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

Same brush, same direction, and — for these two — much the same number of passes:
the passes are counted across the mass, not over its area. One of them is a
rectangle and will still be a rectangle at the end of the painting; the other has a
silhouette, and a silhouette is what a mass *is*.

**Do not carry "a shape costs what its box costs" any further than this pair.** It
holds while a shape is convex and a pass crosses it once. A concave or curved one is
crossed two or three times per pass and costs accordingly — a mass with a bite out
of it more than its box, a curved `ribbon` many times its own width. `s.cost(...)` is the number, and it
is on every `preview`; see *Try the mark before you spend it*. Then look at the ends of the
passes on the shaped one: they stop at the boundary, and the brush breaks past it by
about half its width, which is the ragged edge you want and did not have to make.

---

## A checklist before you call it finished

- Does the greyscale view (`look(values=True)`) have a clear light, mid and dark?
- Are the edges varied — some hard, some soft, at least one lost?
- Is there anywhere the ground still shows through? (There should be.)
- Did you vary brush size, or is everything one width?
- Are the highlights few and deliberate?
- Is anything mechanically repeated — evenly spaced marks, identical parallel
  strokes, a perfectly straight line?
- **Is any small mark a disc, a capsule or a rectangle — the tool's own shape rather
  than the thing's?** Crop into them and look. A round tip prints one silhouette
  however many times you set it down.
- If you had a reference, look at the painting once *without* it beside you. A
  shape that only makes sense with the photograph next to it is not painted yet.
- Is every mass laid along its own axis, or are the big shapes stacks of horizontal
  and vertical bars? Turn the picture on its side if you cannot tell.
- Is any mass a rectangle that should have been a shape? A box is a decision, and
  it is the wrong one everywhere except a band or a flat plane. **Check the
  background hardest** — it is the mass you never had to draw, and the one most
  likely to be a grid of square patches.
- **Is the thing you measured most carefully still attached to the picture?** Cover
  it and look at what is left: if the rest is unresolved, you spent your precision in
  one place and the painting somewhere else.
- **Is the lightest mass in the picture the one you planned to be lightest?** The same
  question in value terms, and this one is checkable: `look(values=True)`, or read it
  off the numbers `compare()` already holds. A mass that has quietly become the
  brightest thing takes the eye whatever the picture is about.
- Was it painted back to front? An edge you had to cut carefully around something
  is a mass that went on in the wrong order.
- **Anything with an inside — is its far edge under its contents, and its contents
  under its near edge?** Something that has escaped the thing containing it, or a
  small mass sitting *on* a bigger one rather than *in* it: the same mistake twice.
- **Did a correction bury something?** Every mass you repainted after the first
  block-in: look at what was standing on it before you did.
- Is there pencil still showing where you did not mean it to? `s.erase()` takes
  it out; `s.export(path, sketch=False)` hides all of it at once, but a drawing
  showing through thin paint is a good thing and worth keeping.
- **You have named the weakest passage. How many strokes are left? Spend them there.**
  Nothing above this line is about *finishing*, and a painter who stops with a third
  of the budget unspent has left the picture short on purpose without deciding to.
  The passage you would apologise for is the one that wants them — not the one you
  have most recently been enjoying.

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
the corner of something you made. Choose it yourself — nothing here says what it should
look like, and the five marks are a limit, not a target. One is enough.

Two things it is not. It is not a title, and it is not a last chance to fix something:
a signature laid across a passage you were unhappy with is a sixth correction wearing a
hat, and the budget exemption exists because the mark is *not* part of the painting.
Put it where it does the picture no harm — a corner, small, close in value to what it
sits on.

Then say in your log what you chose and why. That question is asked here, at the end,
and not before you started, because a mark chosen to be explained is not the same as a
mark chosen.

```python
s.export("painting.png")
s.timelapse_gif("painting.gif")
```

---

## Working from a shell instead

If you would rather work in increments without holding a Python process open, the
same thing is available from the command line. Session state lives in one file.

If `easel` is not found — installing puts it in a scripts directory that is often
not on `PATH`, particularly on Windows — put `python -m easel` in front of the same
arguments instead: `python -m easel look painting.easel --grid`. Both forms are the
same program. Do not spend any time fixing your `PATH`.

```bash
easel new painting.easel --size 1024x768 --texture linen --ground toned_grey --seed 7
easel run painting.easel pass1.py     # your script; `s` is already defined in it
easel run painting.easel pass1.py --rehearse   # ...against a copy, committing nothing
easel look painting.easel --grid
easel look painting.easel --values
easel look painting.easel --region D4 --fine --reference ref.jpg
easel mark painting.easel top_l 0.335 0.315    # and `easel mark p.easel` to list
easel compare painting.easel ref.jpg           # per-cell value numbers
easel prepare painting.easel ref.jpg --level coarse --merge 3,7
easel undo painting.easel 3
easel export painting.easel painting.png
easel timelapse painting.easel painting.gif --every 3 --scale 240
easel brushes                          # the full reference, printed
```

A script given to `easel run` has `s`, `palette`, and the whole API already in
scope. It needs no imports.

**Rehearse the pass, not just the mark.** `easel run --rehearse` runs the whole
script against a copy of the session: it writes the look, says what the pass would
cost, and leaves the session file untouched. The strokes are seeded as if they were
the next marks of the real painting, so what you rehearse is what lands when you run
the same file again without the flag. Working this way, a mass you dislike costs a
look instead of a repaint — which is the difference between rehearsing being the
guide's best advice and it being free to follow.

**Keep your helpers in a prelude.** A `prelude.py` sitting beside the session file is
run first, in the same scope, so mixtures, landmarks and helper functions do not have
to be redefined at the top of every pass. `--prelude other.py` names a different one
and `--no-prelude` turns it off. Auto-loading is announced, never silent.

```bash
easel new painting.easel --size 1024x768 --budget 300   # if you want it held for you
easel run painting.easel pass1.py                       # "...142 of 300 spent, 158 left"
```

**Write the split down and let the engine hold it.** With a `--budget`, every `run`
reports spent and remaining, and `s.cost(plan)` says so when one plan would eat more
than a quarter of what is left. Nothing is ever refused — the budget is your plan for
the picture, not a lock — but the number twelve strokes represents is not one a
painter can feel, and that is exactly what an engine is for.

---

## Or through the MCP server

If your client speaks MCP, the same verbs are there as tools, and the difference
worth having is that **the looking tools hand you the picture**. `look`, `preview`,
`rehearse`, `compare` and `prepare` return their PNG beside the path they wrote it
to, so looking every five to fifteen strokes costs one call instead of a call and a
file read.

Marks are still made by `run`, which takes the script as text — the same Python
this guide teaches, with `s` and the whole API already in scope. Nothing has to be
written to a file first.

Three tools have no shell equivalent, and they are the three questions about a mark
you have not made yet: `preview` (where does it go), `rehearse` (what will it look
like) and `cost` (what does it charge). They take the same plan, and each hands
back the Python that paints it — so paste that into `run` rather than retyping it.
A plan you retype between checking it and painting it is a plan that will drift.

A **place** arrives as JSON in any of six forms — a named region, a grid cell, a
span, a rectangle, an outline, or a shape builder with its own arguments:

```text
"upper-band"                                    a named region
"D4"                                            one grid cell
"C3:F6"                                         a run of cells
[0.10, 0.10, 0.45, 0.30]                        a rectangle
[[0.2, 0.2], [0.6, 0.15], [0.7, 0.5]]           an outline you have
{"blob": "D5", "radius": 0.12, "seed": 3}       and the builders: blob, ellipse,
{"ribbon": [[0.2, 0.8], [0.5, 0.5]], "width": 0.09}      hull, ribbon, polygon
```

A **plan** is a list of those three kinds of thing, or one on its own. A mass is an
object with `shape` and any `block_in` argument; a sweep is one with `edge` and any
`sweep` argument; a mark is a list of points, or an object with `points`. A place
on its own is a mass, and a bare list of points on its own is a mark.

```json
{"shape": {"blob": "D5", "radius": 0.12, "seed": 3},
 "brush": "bristle", "color": "dark", "size": 0.05, "direction": "axis"}
```

Ask `cost` what that charges before you widen the brush, not after. Then `rehearse`
it, then paste the line it gives you back into `run`.

The server is `easel-mcp`, or `python -m easel.mcp_server` when the scripts
directory is not on `PATH`. It needs one extra: `pip install easel-paint[mcp]`.
