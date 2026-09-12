# Painting with Easel

You are about to paint. Not draw, not render — paint. This guide assumes you have
never seen the engine's source and do not need to.

**This file is the whole method and it is meant to stay in your head.** The order of
work, the mistakes you are going to make, the exercises and the checklist. Read it,
paint the eight exercises at the end, then read [`PAINTING.md`](PAINTING.md) once — the
same rules with their reasons, the failures behind them and the numbers — and start.
Come back here while you paint; you are not expected to come back to that one.

That is the whole shape of the documentation, and it is a file boundary rather than an
instruction because an instruction to read something in two goes was tried and a
painter read straight through it.

| File | What it is | When |
|---|---|---|
| **`PAINTER.md`** — this one | the method: the order, the mistakes, the exercises, the checklist | now, and open beside you while you paint |
| [`PAINTING.md`](PAINTING.md) | the reasons: colour, wet paint, the brushes, working from a reference, the rest of the API | once, after the exercises |
| [`RECIPES.md`](RECIPES.md) | the procedures: how a thing that is made of planes gets painted, what a glow is laid as | when you are about to paint one of them |
| [`REFERENCE.md`](REFERENCE.md) | every fact on one page: units, defaults, what each argument does | when you want to look something up |
| [`CALIBRATION.md`](CALIBRATION.md) | the measured numbers behind the rules | **when a rehearsal is about to be spent finding a number that is already in there.** The rules below cite it by section where one exists |

Only this file and the exercises are required. Everything else is there for when you
want it, and **nothing has been cut to make this file short** — it was moved.

**One thing to settle before you read any further: have you decided what to paint?**
If you have, [`paintings/`](paintings) is open to you — three finished pictures, each
with the numbered pass scripts that built it, the prelude of mixtures and masses beside
them, and the painter's own notes on what went wrong. They are the end-to-end worked
example this guide cannot be, because the one thing nobody can teach abstractly is
which call to make *first*. **If you have not decided, do not open them.** They name
their subjects, and a named subject chooses for you: six of six fresh sessions once
painted a noun this guide had merely listed in passing. Decide first, then look.

---

## The first hour

One page, then go and paint the exercises. Every arrow points at where the reason for
the line is written out — a section further down this file, or one in
[`PAINTING.md`](PAINTING.md), marked *(reasons)*.

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
→ *The one habit*, and *Looking* *(reasons)*

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
  nobody made you draw. → *Masses that are not rectangles* *(reasons)*
- **You will lay parallel marks.** One direction for every pass is hatching, and a
  surface's grain repeated thirty times is a stack of bands with a different name.
  Vary the direction; three marks that describe a texture beat thirty that repeat it.
  → *The angle of the mark* *(reasons)*
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
painting it.

**Rehearse everything. It costs a look.** Not "rehearse what you would not want to
repaint" — that was the rule, and it asks you to predict which passes will go wrong,
which is the thing you are bad at. `easel run pass.py --rehearse` runs the whole pass
against a copy and commits nothing. Two painters rehearsed 27 and 18 passes; **every
one of the eighteen changed something, and not one of them was charged.** The painter
who rehearsed nothing spent about 60 of its 224 strokes repainting masses it had laid
once and disliked. → *Try the mark before you spend it* *(reasons)*

**Now go and paint the eight exercises**, at the end of this file. Then read
[`PAINTING.md`](PAINTING.md) once, and start.

| When you want | Read |
|---|---|
| the order of work, in full | *The workflow*, steps 1–6 |
| to stop making the same five mistakes | *What you are bad at, and what to do instead* |
| to stop | *A checklist before you call it finished* |
| to work from a photograph, or from nothing but your own head | *Working from a reference* / *Painting without a reference*, in [`PAINTING.md`](PAINTING.md) |
| a colour, a mixture, a value | *Colour*, in [`PAINTING.md`](PAINTING.md) |
| to know what a brush will actually leave | *The brushes* and *The shape each tool leaves behind*, in [`PAINTING.md`](PAINTING.md) |
| to check a mark before paying for it | *Try the mark before you spend it*, in [`PAINTING.md`](PAINTING.md) |
| how a particular kind of thing gets painted | [`RECIPES.md`](RECIPES.md) |
| a fact: a unit, a default, an argument | [`REFERENCE.md`](REFERENCE.md) |
| a number behind a rule | [`CALIBRATION.md`](CALIBRATION.md) |

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

**`solid=True` is as even as this engine gets, and it is not perfectly even.** A solid
`flat` block-in still shows its pass structure at about `0.03` of value — enough to
read as faint striping on a large flat plane, invisible on anything with a form. That
number does not move with `opacity` or with `pressure`; a painter believed its planes
came out striped at `0.85` and clean at `1.0`, measured it, and found what had actually
changed was the brush. (`CALIBRATION.md`, *`block_in`*, has it at every opacity and pressure.) **So hide the
passes with a bigger brush or a broken one, never with an argument** — or leave them, because a plane with no incident in it at all is
the flatter-looking mistake.

A place can be a rectangle — `cell("D5")`, `span("E5", "H8")`, `region("lower-half")`
— or a **shape**: `blob`, `ellipse`, `hull`, `ribbon`, `polygon`. `block_in` fills
either, and a shape's passes stop at its own silhouette. Most masses are shapes; see
*Masses that are not rectangles* in [`PAINTING.md`](PAINTING.md).

**Draw the arrangement before you commit paint to it, even with nothing to copy.**
`s.pencil()` is free — it costs no strokes and paint buries it — and `preview()` is
not a substitute, because the two answer different questions: `preview` checks a mark
against a plan, and the pencil checks *the plan*. A painter who worked from typed
coordinates through `preview` alone never saw its composition as a composition until
the picture was finished, and by then the fault was the picture. Put the big shapes
down in graphite, look, and move them while moving them is free.

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
  decisions actually get made, under *Put a number on it* in
  [`PAINTING.md`](PAINTING.md).

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
supply one and it lands exactly as written, black included (*Colour* in
[`PAINTING.md`](PAINTING.md) has the
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
s.smudge([(0.42, 0.50), (0.46, 0.62)])              # walk each join once, while wet
```

Three or four steps read as a gradient once the joins are softened; two read as two
slabs. Do it while the paint is wet — that is what step 5 and *Wet paint* in
[`PAINTING.md`](PAINTING.md) are for — and if you leave a plane as one flat value with marks laid on top,
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

**Leave `size` off here.** The rings step `depth / n` apart — `depth` being half the
patch's shorter extent — and each is laid over the ones before it, so the brush and
the step are one mechanism and not two settings. A brush much wider than about three
steps buries the first rings under the last, and the middle comes back one flat colour
with a rim of ramp round it: a sun, not a glow. A preset's own default is five steps
wide on a patch this size, which is why the verb now picks its brush from the step
when you do not, and says so when the one you gave it will fill.

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
s.smudge([(0.3, 0.4), (0.45, 0.44)])                # soften an edge
s.stroke([(0.6, 0.3), (0.62, 0.5)], "round_hard", "dark", size=0.02)  # sharpen one
```

**`smudge` is far stronger than "move paint around" suggests**, and it walks a
light/dark boundary into the dark side rather than blurring it evenly. Leave `size`
off. Measured, what it buys stops at about `0.02` — the default — and what it costs
does not: at `0.07` one pass drags the light mass `4.4%` of the canvas height into the
dark, against `1.3%` at the default, for a join no softer than one pass ever gets. Past
`0.03` the call says so. The table is in `CALIBRATION.md` under `smudge`.

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
s.smudge([(0.30, 0.40), (0.38, 0.41)])             # a straight edge is two points
s.smudge([(0.30, 0.40), (0.45, 0.45), (0.60, 0.53),
          (0.73, 0.63)])                            # a curved one is the curve
s.smudge(mass)                                     # a shape is already that curve
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
fraction of the canvas, not the mass's; see *The brushes* in
[`PAINTING.md`](PAINTING.md), and *Pressure* in the same file for more on painting at
that scale.

---

## What you are bad at, and what to do instead

Be honest about these. They are specific to what you are.

**Four of them have been made by every painter so far, each one after reading the
warning about it.** So each is written here with its repair on the same line, because a
warning you are going to violate anyway is only worth anything if the fix is next to
it. If you read nothing else in this section, read these four.

| The mistake | What it looks like | Do this instead |
|---|---|---|
| **Floating discs** | several small marks from a round tip: one silhouette, printed over and over | give the mark a *length* — a short smear, not a dot — or `tip_wobble=0.7`, which redraws the outline per mark |
| **A capsule shadow** | a cast shadow laid as a filled shape at the palette's darkest: a slab with two hard ends | one tapering stroke a step or two below the *surface*, losing its far end. → *step 3* |
| **A stack of bars** | a wide soft passage laid as three or four hard bands | `s.scumble(band, a, b, 8)`, or `direction="inward"` for a passage light in the middle. → *step 4* |
| **All flat and round** | the whole picture in two brushes, every pass horizontal | before each pass, name the brush and the angle out loud. `direction="axis"`, and the `bristle` and `knife` exist. → *The angle of the mark* *(reasons)* |

The pattern under all four is one thing: **the tool has a shape of its own, and if you
do not choose the shape, it chooses.** [`RECIPES.md`](RECIPES.md) is the positive half —
what to lay instead, as calls in order, for the things that have caught a painter out.

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

**You will paint boxes.** Almost nothing you want to paint is a box, and you will be
tempted to paint one anyway, because a rectangle is the easiest place to name. If you
block in a shaped mass as a box you get a box, and no amount of later work removes
that. `blob`, `ellipse`, `hull`, `ribbon`, `polygon`, `union` and `s.circle()` build a
mass with a silhouette; `block_in` fills one as readily as a rectangle, and its passes
stop at the outline. Three things about them are worth knowing before you spend twenty
passes — the paint lands *outside* the shape by up to three-quarters of a brush, a
curved mass is priced on the box its curve sweeps out rather than on its own width, and
`inset()` on a concave shape eats the thin parts first — and all three, with what they
cost, are *Masses that are not rectangles* in [`PAINTING.md`](PAINTING.md). The rule
here is the short one: **build the shape, preview it, and check the background hardest.**

**The mass that needed no drawing is the one that will give you away.** You will reach
for a shape on your subject, because its silhouette was a problem you had to solve,
and then lay everything behind it in boxes because nothing back there asked anything of
you. That is backwards. A viewer expects construction on the subject and forgives it;
a background of square patches, every edge parallel to the canvas, reads instantly as
made by a machine. **Give the masses that needed no drawing the same treatment as the
ones that did** — see *The angle of the mark* in [`PAINTING.md`](PAINTING.md), which is
the same rule and the loudest tell in this engine.

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

## Eight small exercises

Run these before painting anything real. They take a minute each and will teach you
the engine's feel faster than reading will.

**They are a gate, and here is what going round it costs.** A painter who skipped all
eight met two of the lessons inside the picture instead: a wide soft passage laid as
four hard bars — exercise 5 and *step 4* — and a surface whose grain came out as a row
of parallel stripes, which is *The angle of the mark* in
[`PAINTING.md`](PAINTING.md). Between them they cost more
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
is on every `preview`; see *Try the mark before you spend it* in
[`PAINTING.md`](PAINTING.md). Then look at the ends of the
passes on the shaped one: they stop at the boundary, and the brush breaks past it by
about half its width, which is the ragged edge you want and did not have to make.

---

## A checklist before you call it finished

**Passing this list means the painting is not *wrong*. It does not mean it is
finished.** Two painters read it as a permit to stop and put down the brush with about
a third of the budget in hand; one of them had already named its own weakest passage in
its notes and gave it four more strokes. Every line above the last two is a fault to
look for. **The last two are the only ones that ask whether you are done**, and they
are the ones to answer slowly.

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
- **And are the bands in the marks, or in the subject you chose?** A frontal elevation
  is a layer cake before a brush is picked, and no amount of angled brushwork gets it
  back. Count the horizontal bands in the arrangement *before the first mass*: more
  than three, and find something that crosses them — or a viewpoint that is not square
  on. One painter spent fifteen strokes fighting a problem it had chosen in the first
  thirty seconds.
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
- **What share of your strokes went on the subject? Write the number down, against the
  share you planned.** Not "did you spend enough on it" — a question you will answer
  yes to. A number. Three painters read the warning about underspending on the subject,
  quoted it in their own notes, and underspent anyway: 59% of strokes before the
  subject began, 24% on it against a planned 32%, and one that named its weakest
  passage and stopped with 115 strokes in hand. The log will count it for you if you
  say which marks they are as you make them:

  ```python
  s.stroke([(0.30, 0.40), (0.45, 0.44)], "round_hard", "light",
           size=0.02, note="subject")               # as you paint it
  paid = [r for r in s.history.records
          if r.kind not in ("dry", "look", "pencil", "erase")]
  on_it = [r for r in paid if "subject" in r.note]
  print(f"{len(on_it)} of {len(paid)} marks — {len(on_it) / max(len(paid), 1):.0%}")
  ```

  **Measure it at the moment the subject is finished, not at the end**, and if it is
  under what you planned then, you are not finished. After that the number is *meant*
  to fall: the last third goes on the surroundings, which is the rule two lines down,
  and a subject at 45% when it was done and 41% after two surroundings passes has
  obeyed both. `note=` costs nothing and is the only way the engine can hold this for
  you.
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

**Rehearse the pass, not just the mark — and rehearse every pass.** `easel run
--rehearse` runs the whole script against a copy of the session: it writes the look,
says what the pass would cost, and leaves the session file untouched. The strokes are
seeded as if they were the next marks of the real painting, so what you rehearse is
what lands when you run the same file again without the flag. Working this way, a mass
you dislike costs a look instead of a repaint. **The habit is to run every pass with
the flag first, look, and only then run it without** — eighteen rehearsals in one
painting all changed something and none of them was charged, so there is no pass cheap
enough to be worth deciding about.

Name several scripts and they run in the order you gave them, and with `--rehearse`
they go on **one** copy: `easel run p.easel p2_far.py p3_near.py --rehearse`. A pass
that goes on top of another pass has to be judged on it, not on bare ground.

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
