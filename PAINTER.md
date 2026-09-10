# Painting with Easel

You are about to paint. Not draw, not render — paint. This guide assumes you have
never seen the engine's source and do not need to.

Read the whole thing once before your first stroke. The workflow section matters
more than the API section. The measured numbers behind the rules here live in
`CALIBRATION.md`; you do not need them to paint.

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
  It stops being cheap the moment something is standing in front of it.

The exception is the ground itself, which is behind everything and goes on first by
definition. Everything after that is in depth order.

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

**The box has no black, and it does not need one.** `mix("ultramarine",
"burnt_umber", 0.5)` reads about `0.14` in the greyscale view — a near-black with a
colour in it, which is what a dark in a painting should be. Vary the ratio and it
stays that dark while swinging from cool to warm: more blue for a shadow in
daylight, more umber for one by a lamp. That mixture, not any single pigment, is
the bottom of your range.

The floor is around `0.13`, and it is the **box's**. Mixing never takes a channel
below the darker of its two ingredients, so the darkest thing you can reach is set by
the swatches and nothing else — and piling on passes or glazes will not go lower. If a
mass is not dark enough, mix it darker rather than painting it again.

That is a fact about the paint you have, not about the engine. A colour you supply
yourself lands exactly as written, black included. The box has no black because mixed
darks are alive and a tube black is dead, which is a reason to keep mixing, not a wall
you are being held behind.

### 4. Refine the mid-tones

Now the middle values, with a medium brush (`size≈0.08–0.12`). Work across the
whole canvas rather than finishing one corner — a painting should come up all at
once, like a photograph developing. Look every ten strokes or so.

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

An image where every edge is equally sharp looks like clip-art. That is the single
most common way this goes wrong.

### 6. Highlights last, smallest brush, fewest strokes

The lightest lights and the sharpest accents go on at the end, and there should be
very few of them. Ten deliberate marks, not a hundred. Every highlight you add makes
the others count for less.

```python
s.dab(0.62, 0.35, "round_hard", "titanium_white", size=0.015)
```

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
enlarged so a single cell fills the panel. **Read the two digits off the label; do
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

Two tools sit between deciding on a mark and paying for it. Neither touches the
canvas and neither writes to the log.

```python
plan = [{"points": [s.pt("top_l"), (0.40, 0.62)], "brush": "liner",
         "size": 0.006, "color": "light", "label": "edge"}]

s.preview(plan,  reference="ref.jpg", region=span("C3", "F6"), grid="fine")
s.rehearse(plan, reference="ref.jpg", region=span("C3", "F6"))
```

`preview` draws your intended points and the brush's *width* over both panels —
where the mark will go, checked against the photograph. `rehearse` paints it on a
copy of the canvas and shows you the result — what it will look like, with its
tooth and its edge and how it mixes with what is already there. A feature smaller
than a cell can be tried three ways and judged before a stroke is spent.

The plan is a list of the same arguments `s.stroke()` takes, so what you checked is
what you paint, without rewriting it:

```python
for spec in plan:
    s.stroke(**{k: v for k, v in spec.items() if k != "label"})
```

The rehearsal is seeded as if these were the next strokes of the real painting, so
what you rehearsed is what lands. This is what the scrap of canvas beside a real
easel is for, and it is the last reason to reach for `undo`.

### Compare values, not colours

```python
s.look(reference="ref.jpg", values=True)   # both panels greyscale, same scale
```

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
the two greyscales. Negative means your canvas is *darker* there. **The number that
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

The mean colour is in the table too, coarse on purpose: it is there to catch "that
whole passage is too warm", not to be sampled and matched. **Matching cell by cell
is tracing**, and it produces a painting nobody would look at twice. If you find
yourself working down the table one cell at a time, you have stopped painting.

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
mass, not over its area. They stop at the boundary rather than a third of a brush
past it, and a mass with a bite out of it keeps the bite — one pass across a concave
shape comes back as the two pieces that are really inside it.

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
  Take it: one sweep on its own comes out stringy, because a bristle brush covers
  about three-quarters of its width, and the crossing is what closes the mass up.
  Twenty to thirty degrees is usually enough. A shaped `block_in` has the same
  problem and the same answer — `direction=("axis", 90)`.
- `depth=` is how far into the mass to go, and the brush decides how many passes
  that takes unless you say `passes=`.

**Which one?** Fill a shape when you can see the whole silhouette and want it
covered; sweep when one edge is the thing you care about, or when the passes
following the form is the point. And if the mass is close enough to a box that
either feels like overkill, `block_in` at the angle the mass runs at is the cheaper
version of the same idea.

**The shape is a place, not a line.** Nothing draws that outline, and you must not
either: the silhouette is where this mass's paint stops and the mass behind it still
shows, which is why the far masses go down first.


**When something is wrong, paint over it.** Your instinct will be to reach for
`undo`. Resist it. Real repairs happen with paint: let the area dry, then work over
it opaquely.

```python
s.dry()                                                     # so new paint covers
s.block_in(cell("C4"), "bristle", "corrected_colour", density=1.0)
```

`undo(n)` exists and is documented below, but treat it as scraping the canvas —
something you do occasionally and reluctantly, not a free rewind. Painting over
leaves a history in the surface that is part of why paintings look alive.

**You will under-vary your marks.** Real brushwork varies in width, pressure,
direction and opacity constantly. If every stroke uses the same brush at the same
size with the same pressure, the result will look mechanical no matter how good the
drawing is. Change `size`, change `pressure`, change direction between passes.

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

**A `bristle` stroke is never solid.** It lays a comb of parallel streaks, which is
what makes it alive on a mark whose direction you mean. A bristle has a width of its
own, about a two-hundredth of the canvas, so a bigger brush prints *more* streaks
rather than fatter ones, and the brush picks up a slightly different comb each
stroke — spacing, phase, and which bristles are missing. What still makes ribbing of
a big quiet mass is laying it in single parallel passes: cross them, or lay large
quiet masses with `flat`, and keep
single bristle strokes for marks that have a direction.

Size is a fraction of the canvas's long side. `0.2` is a big brush, `0.02` is a small
one. **Use a bigger brush than feels comfortable**, especially early.

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

Anything about a brush can be overridden per stroke:

```python
s.stroke(path, "bristle", "shadow", size=0.14, opacity=0.5)
s.stroke(path, "flat", "light", hardness=0.9, jitter=0.05, load=0.4)
s.stroke(path, "bristle", "shadow", size=0.12, load_falloff=0.25)   # runs dry slower
```

**`load` is how much paint the brush carries.** Brushes start full, and anything
that has to read as a *solid mass* — a block of local colour, a correction painted
over something wrong — wants to stay there: pass `load=1.0` explicitly when you are
covering. Dropping it is how you get dry brush — a broken, scratchy mark — and it is
one of the best tools you have for making a surface look worked. The useful window
is about `0.4` to `0.6`; below that a bristle brush is genuinely nearly empty and
leaves almost nothing. Look after a dry-brush pass rather than assuming, and if a
stroke seems to have vanished, `s.log()` will tell you how much paint it laid.

**A loaded brush runs dry along a stroke, and a long stroke shows it.** Where a long
stroke ends is where its texture is loudest, and if every stroke in a field runs
the same way, one side of the field speckles. `load_falloff` sets how fast the brush
empties; for a big even field either lower it, or run the next stroke the other way
so the two dry ends do not coincide. **Do not lay one broken pass across the whole
canvas**: a single load, one brush, edge to edge, prints the surface's own texture
as an even field over everything, and it stays visible under every later stroke.

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
spot, the middle one at full pressure, and **one** stroke against your budget.
Anything the size of a cell or smaller is three marks at most — the dark, the
light, and the edge
between them — laid dark first and looked at through a `region=` crop before the
light goes on.

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
and so on — and returns the path. Print it and open that file. The numbering belongs
to the session, so a second session started in the same directory begins again at
`look_001.png` and writes over the first one's; copy anything you want to keep.

Use `values=True` far more often than feels necessary. Use `diff=True` after a pass
to confirm you changed what you meant to change and nothing else.

When a mark seems to have gone missing, `s.log()` says how much paint each one
actually laid, and prints `NO PAINT LANDED` for a mark that changed nothing at all —
usually an opacity of zero, or a glaze into paint that is still soaking wet.

---

## The rest of the API

```python
s.stroke(points, brush, color, pressure="taper", size=None, opacity=None, note="")
s.dab(x, y, brush, color, size=..., press=1)       # one mark; press stamps it again
s.block_in(place, brush, color, direction=, density=, overhang=)    # a mass, as strokes
s.sweep(edge, brush, color, into=, depth=, cross=, passes=)         # a mass with a shape
s.smudge(points, size=)                            # move paint around
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
s.compare(reference, region=None)                  # per-cell value numbers
s.prepare(reference, level="coarse")               # the reference, cut up
s.look_areas()                                     # the map again, after merging
s.export("painting.png")
s.timelapse_gif("painting.gif")
s.log()                                            # what you have done so far
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

**`block_in` paints past a rectangle** by a fraction of a brush on every side. That
is fine for a band and wrong for a mass that meets another at the *same* depth,
where it lands on its neighbour. Painting back to front is the real answer — the
far mass spilling into where the near one is going does no harm, because the near
one goes on over it next. For two masses at the same depth, pass `overhang=0` or
inset the place by half the brush size. A **shape** already does this: its passes
stop at the silhouette, and only the brush's own width breaks past it — about
three-quarters of a brush at the widest.

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
hull([p1, p2, p3])                         # the mass around three or four points
ribbon(points, width, end_width=None)      # a mass running along a line
polygon(points)                            # an outline you already have
shape.inset(0.03)  shape.scaled(0.9)  shape.shifted(0.02, 0)   # ... as a region does
shape.axis   shape.area   shape.center   shape.contains(x, y)   shape.closed
```

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

def at_value(target):                # the ratio of white that reads `target`
    a, b = 0.0, 1.0
    for _ in range(20):
        mid = (a + b) / 2
        a, b = (mid, b) if p.value_of(p.mix(dark, "titanium_white", mid)) < target else (a, mid)
    return (a + b) / 2

for i in range(9):
    r = at_value(lo + (hi - lo) * i / 8)
    band = Region(i / 9.0, 0.15, (i + 1) / 9.0, 0.85)
    s.block_in(band, "flat", p.mix(dark, "titanium_white", r), density=1.0, size=0.06)
    print(f"value {lo + (hi - lo) * i / 8:.2f}  white {r:.2f}")
s.look(values=True)     # nine even steps, 0.14 to 0.96
```

Look at the printed ratios, not just the picture. A third of white gets you the
first step; it takes nine tenths to reach the eighth. That curve is why a mixture
that "should" be halfway comes out too dark, and why the fix is always to add more
white than feels right.

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

Same brush, same direction, same number of passes — the passes are counted across
the mass, not over its area, so a shape costs what its box costs. One of them is a
rectangle and will still be a rectangle at the end of the painting; the other has a
silhouette, and a silhouette is what a mass *is*. Then look at the ends of the
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
- If you had a reference, look at the painting once *without* it beside you. A
  shape that only makes sense with the photograph next to it is not painted yet.
- Is every mass laid along its own axis, or are the big shapes stacks of horizontal
  and vertical bars? Turn the picture on its side if you cannot tell.
- Is any mass a rectangle that should have been a shape? A box is a decision, and
  it is the wrong one everywhere except a band or a flat plane.
- Was it painted back to front? An edge you had to cut carefully around something
  is a mass that went on in the wrong order.
- Is there pencil still showing where you did not mean it to? `s.erase()` takes
  it out; `s.export(path, sketch=False)` hides all of it at once, but a drawing
  showing through thin paint is a good thing and worth keeping.

If you have a reference, look at them side by side one last time:

```python
s.look(reference="ref.jpg")
s.look(reference="ref.jpg", values=True)   # compare value structure, not colour
```

Then:

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
easel look painting.easel --grid
easel look painting.easel --values
easel look painting.easel --region D4 --fine --reference ref.jpg
easel mark painting.easel top_l 0.335 0.315    # and `easel mark p.easel` to list
easel compare painting.easel ref.jpg           # per-cell value numbers
easel prepare painting.easel ref.jpg --level coarse --merge 3,7
easel undo painting.easel 3
easel export painting.easel painting.png
easel timelapse painting.easel painting.gif
easel brushes                          # the full reference, printed
```

A script given to `easel run` has `s`, `palette`, and the whole API already in
scope. It needs no imports.
