# Painting with Easel

You are about to paint. Not draw, not render — paint. This guide assumes you have
never seen the engine's source and do not need to.

Read the whole thing once before your first stroke. It is short, and the workflow
section matters more than the API section.

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
s.block_in("lower-half", brush="bristle", color="dark", density=0.7, size=0.2)
```

Resist detail here. If you can already name what you are painting, you have gone
too far too early.

### 2. Paint from back to front

**Lay the furthest thing first and let each nearer thing be painted over it.** Sky
before headland, headland before water, water before the post standing in it. Wall
before table, table before mug, mug before the spoon in it. Background, middle
distance, foreground, in that order, every time.

This is not tidiness. It is the only cheap way to get an edge:

```python
s.palette["sky"] = s.palette.tint("cerulean", 0.55)
s.palette["water"] = s.palette.desaturate(s.palette["sky"], 0.4)

s.block_in("upper-half", "flat", "sky", size=0.18)          # furthest
s.block_in(span("A4", "H6"), "flat", "water", size=0.16)    # nearer
s.stroke([(0.3, 0.42), (0.3, 0.78)], "bristle", "dark", size=0.03)   # the post
```

The post's edges are now real edges — the place where the post's paint stops and
the water's paint is still showing — and you drew none of them. Paint the post
first and the only way to get the same edges is to cut the water carefully around
it, which is painting *up to* a line, which is the one thing this guide will tell
you four more times not to do.

Three things follow from it, and they are where the order earns its keep:

- **Draw after the background is down, not before.** An underdrawing laid on the
  ground and then blocked over is gone — paint buries graphite in proportion to
  how much lands, and a full-strength block-in lands all of it. Lay the far masses,
  *then* draw the near things on top of them, then paint those.
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
reports exactly the value the greyscale view will show, so you can check a mixture
before spending a stroke on it:

```python
p = s.palette
p["dark"] = p.mix("ultramarine", "burnt_umber", 0.55)
p["mid"]  = p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.35), 0.40)
p["lit"]  = p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.40), 0.74)
for name in ("dark", "mid", "lit"):
    print(name, p.hex(p[name]), round(p.value_of(p[name]), 2))
```

Two mixtures that sound different can be the same value, and that is the commonest
way a first pass turns into mush. If two of your three are within about `0.10` of
each other, they will not read as separate masses no matter how different their
colours are.

**Know the range you actually have. It is about `0.23` to `0.96`, not 0 to 1.**
There is no black on this palette, and no combination of pigments gets below
roughly `0.23` — ultramarine and burnt umber, shaded and desaturated as far as they
go, all land there. Piling on more passes does not help and neither does glazing:
eight dried coats of the darkest mix measure within a hundredth of one. So you
cannot make a near-black shadow, and trying is a waste of strokes. **You build
contrast by pushing the lights up, not the darks down.** If a dark mass is not
reading as dark, the fix is almost always that everything around it is too dark,
not that it is too light.

**So do not match a photograph's values. Compress them.** A lamp-lit photograph
runs from about `0.04` to `0.90`; you have `0.23` to `0.96`. Matching the numbers
one for one is impossible at the bottom and it flattens everything above it,
because you spend the range you *do* have trying to reach a floor you cannot. Map
the reference's range onto yours instead — decide what its darkest passage will be
on your canvas, decide what its lightest will be, and place everything else
proportionally between them:

```python
lo, hi = 0.23, 0.94                                  # what you can actually reach
ref_lo, ref_hi = 0.06, 0.59                          # what the reference runs
def mine(v):                                         # where a reference value goes
    return lo + (hi - lo) * (v - ref_lo) / (ref_hi - ref_lo)
```

Take `ref_lo` and `ref_hi` from `compare()` on the empty canvas — see *Put a number
on it*, which also tells you which cells are out of reach so you can stop spending
strokes on them. Relationships are what read; absolute values are not.

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
between a likeness and a set of coloured rectangles. Do not skip it and start
placing strokes from your impression of the picture — that impression is wrong
about position in exactly the way you are worst at.

**Put the same grid on both, and never take a coordinate out of your head.**

```python
s.look(reference="ref.jpg", grid=True)     # the same A-H / 1-8 cells on each
```

Both panels carry the same labelled cells, so a place you can *see* on the
reference has a name you can *paint* into. That is the whole trick. Work like this:

1. **Name the big masses by cell, out loud, before painting anything.** "The dark
   coat fills E5 to H8. The head is D3 to F3. The lit wall is G1 to H2. The bright
   shape bottom-left is B7 to C8." Four or five of those sentences is a drawing.
2. **Paint the masses into those cells** and look again with the grid on. Compare
   cell against cell, not impression against impression: *my* face is D3–D4 but on
   the reference it runs D3–D5, so it is half a cell too high and too short.
3. **Correct by cell too.** Errors of placement are the ones you cannot see by
   looking at your own painting alone, because it looks internally consistent. They
   only show up against the grid.

A mass is rarely one cell. `span("E5", "H8")` is the rectangle from one cell to
another, both included, so what you said out loud is what you block in — and it is
the right size of crop for inspecting a passage:

```python
s.block_in(span("E5", "H8"), "bristle", "dark", density=1.0, size=0.14)
s.look(region=span("D2", "E4"))                # the head, close up
```

### The drawing, before the masses

A cell is a large place. On a 1200-wide canvas one cell is 150 pixels, and an eye,
a knuckle, the lip of a cup, the gap between two fingers are all *smaller than
that*. Named by cell alone they land somewhere in the right neighbourhood, which is
how a painting comes out a recognisable scene made of unrecognisable things.

So before the masses: six or seven points, each one verified. That is a drawing,
and everything else hangs on it.

```python
s.mark("rim_l", 0.335, 0.315)          # a named point, shown on every look after
s.mark("rim_r", 0.630, 0.315)
s.mark("foot",  0.480, 0.715)
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
s.mark("eye_l", *cell("D4").point(0.35, 0.55))     # read off the fine grid
```

Then draw, with the pencil, through the points:

```python
s.pencil([s.pt("rim_l"), (0.36, 0.68), s.pt("foot"), (0.60, 0.68), s.pt("rim_r")])
s.look(reference="ref.jpg")             # is the drawing right, before any paint?
```

`pencil()` puts graphite into the canvas — no paint, no wetness, and **it does not
count as a stroke**, so the drawing is free. Paint covers it in proportion to how
much actually lands, so it survives thin paint and disappears under solid paint.
Making it disappear is the painting.

**Thin means `opacity`, not `density`.** One pass over a line leaves 79% of the
graphite at `opacity=0.04`, 55% at `0.10`, 34% at `0.18` and 19% at `0.30`. A
`block_in` at `density=0.3` is *not* thin paint — density only spaces the passes out;
each one still lands at full strength, and a seven-stroke scumble at `density=0.3`
takes the drawing off completely. If you want to work over a drawing and keep it,
drop the opacity.

This is the other reason for painting back to front: draw *after* the far masses are
down, and nothing has to be scumbled over the drawing at all.

Four things about drawing that are easy to get wrong:

- **Draw through the shapes, not around them.** A line you painted *up to* is an
  outline filled in, and that is the clearest possible sign nobody was looking at
  masses. Paint across your own lines.
- **Erase rather than argue.** If a line is wrong, `s.erase(region)` and redraw.
  Arguing with a wrong line while painting costs strokes and loses every time.
- **Hair drawn along a line still has to go every which way.** The drawing says
  where the mass is. It does not say what the marks inside it do.
- **Fix the drawing before you paint it.** A look at the pencil alone is the
  cheapest correction available to you — it costs nothing and no paint has been
  spent yet.

`s.sketch_lines()` gives every line back as points, so a stroke can be swept along
one, aimed at one, or ignore it:

```python
for line in s.sketch_lines():
    s.stroke(line, "bristle", "dark", size=0.05)
```

### Try the mark before you spend it

Two tools sit between deciding on a mark and paying for it. Neither touches the
canvas and neither writes to the log.

```python
plan = [{"points": [s.pt("rim_l"), (0.40, 0.62)], "brush": "liner",
         "size": 0.006, "color": "light", "label": "rim"}]

s.preview(plan,  reference="ref.jpg", region=span("C3", "F6"), grid="fine")
s.rehearse(plan, reference="ref.jpg", region=span("C3", "F6"))
```

`preview` draws your intended points and the brush's *width* over both panels —
where the mark will go, checked against the photograph. `rehearse` paints it on a
copy of the canvas and shows you the result — what it will look like, with its
tooth and its edge and how it mixes with what is already there. A feature the size
of an eye can be tried three ways and judged before a stroke is spent.

The plan is a list of the same arguments `s.stroke()` takes, so what you checked is
what you paint, without rewriting it:

```python
for spec in plan:
    s.stroke(**{k: v for k, v in spec.items() if k != "label"})
```

The rehearsal is seeded as if these were the next strokes of the real painting, so
what you rehearsed is what lands. This is what the scrap of canvas beside a real
easel is for, and it is the last reason to reach for `undo`.

**Compare values, not colours, at least as often.**

```python
s.look(reference="ref.jpg", values=True)   # both panels greyscale, same scale
```

Both sides are converted the same way, so the greys are directly comparable. This
is the fastest way to find the error that will otherwise sink the painting: a
background that is far lighter than the reference's, a light mass that is not
actually the lightest thing, two masses that are separate in colour and identical
in value.

**Get the value map right before you care about the drawing.** A copy with the
right values and a clumsy drawing still reads as the scene. A copy with an exact
drawing and flat values reads as nothing. If your greyscale comparison shows the
reference has a dark corner where you have a bright one, fix that before you touch
a feature.

### Put a number on it

Squinting says something is off. It does not say which mass or by how much, and by
the last twenty strokes that is the only question left.

```python
print(s.compare("ref.jpg"))
```

**Run it once before your first stroke.** On the empty canvas the difference column
is meaningless but the reference column is the photograph's entire value map, free,
in numbers, before you have committed anything — the lightest cell, the darkest
cell, and where every mass sits between them. That is what you need to plan the
three values and to set `ref_lo` and `ref_hi` for the compression above. Your eye
will guess the range of a dim photograph two stops too light; this will not.

Per cell: the reference's mean value, yours, and the difference, as a table and as
a heat map beside the two greyscales. **The number that matters is `0.10`** — two
masses closer than a tenth of the value range read as one, so a cell further out
than that is a separation your painting has lost.

```
       A      B      C      D      E      F      G      H
  1  +0.04  +0.04  +0.04  +0.04  +0.03  +0.04  +0.04  +0.04
  4  +0.04  +0.04  -0.06 -0.34* -0.32* -0.12*  +0.04  +0.04
6 of 64 cells more than 0.10 out (* above); largest 0.34.
    D4 ref 0.87 canvas 0.53 -0.34 (#E2DED6 vs #8C8880)
```

Negative means your canvas is *darker* than the reference there. The mean colour is
in the table too, coarse on purpose: it is there to catch "that whole passage is too
warm", not to be sampled and matched. Matching sampled colour cell by cell is
tracing, and it produces a painting nobody would look at twice.

Inside a region, `compare` measures its tenths and labels them the way
`grid="fine"` does, so a cell that is out names the place to fix:

```python
print(s.compare("ref.jpg", region=cell("D4")))     # the tenths of one cell
```

**Some cells are out because you were wrong, and some because no paint in the box
goes that dark.** A cell whose *reference* is below about `0.13` cannot be brought
within `0.10` of it by any stroke — the palette floors at `0.23`. Those are marked
`~` instead of `*` and listed separately, and they are not work:

```
17 of those (~) ask for a value below the palette's 0.23 floor and cannot be
painted. 43 are worth strokes.
```

```python
for c in s.compare("ref.jpg").fixable:      # off, minus what cannot be painted
    print(c.label, c.delta)
```

Work down `fixable`, largest first, and stop when it is empty. Chasing a `~` cell
is the most expensive mistake this table can lead you into: the mark lands, the
number does not move, and you do it again.

### When to stop measuring

Measuring is not painting, and every tool in this section can be used to avoid
making a mark. Stop when:

- **no cell is more than `0.10` out** — the value structure is right, and value is
  what carries a copy;
- **the landmarks are verified** — six or seven, checked at feature scale. A dozen
  is not twice as good; it is a session spent on arithmetic;
- **you can see the subject in your own painting with the reference covered up.**

Past that point, more measuring makes the painting worse, not better: it turns
marks into corrections and corrections into mud. The grid gets the masses into the
right cells and the landmarks get the features into the right places. Neither will
draw a face for you, and chasing small features cell by cell is how you spend three
hundred strokes and arrive at a diagram.

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

**The map is not the truth.** It joins hair to a wall of the same brown and cuts a
coat along its folds, because it knows about colours and a painting is made of
things. `merge` and `split` are how you say so. The useful sentence is "area 5 is
the hair, less the strip that is really wall" — not "the computer says eleven".

`s.sketch()` lays those outlines as pencil in one call. **That is an assisted mode.**
The drawing is meant to be yours: sketch, look, adjust, then paint. A painting that
starts from the machine's outlines is measuring the segmenter and not you, and any
write-up has to say it was used. Prefer `prepare` for *reading* the reference and
your own `pencil()` for drawing it.

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

**Finding an edge is the same mistake in disguise.** When a profile or a silhouette
is not crisp enough, the reflex is to run a thin dark stroke along it. That stroke
is an outline, and it reads as one the moment you look — a drawn line around a
painted shape. Sharpen an edge by painting the mass on the *other side* of it: a
brush at least `0.03` wide, running along the boundary with its centre outside the
shape, laying the background's own colour up to where the shape stops. The edge is
then where two masses meet, which is the only kind of edge a painting has.

**A region is a rectangle. Almost nothing you want to paint is.** `block_in` fills
a box, which is right for a wall, a band of ground, a field of sky — and wrong for
anything with a silhouette. If you block in a figure as a box you get a box, and no
amount of later work removes that. For a mass with a shape, drive the strokes
yourself: walk across it and let each stroke start where the *edge actually is*.

```python
def edge(knots):                       # a boundary given as (x, y) corners
    def at(x):
        for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return knots[-1][1]
    return at

top = edge([(0.33, 1.02), (0.46, 0.66), (0.58, 0.43), (0.74, 0.50), (1.02, 0.68)])
for k in range(9):                                  # passes, not columns
    off = 0.035 * k                                 # step down into the mass
    xs = [0.345 + 0.65 * i / 8 for i in range(9)]
    band = [(x, min(top(x) + off, 1.02)) for x in xs]
    s.stroke(band if k % 2 == 0 else band[::-1], "bristle", "dark",
             size=0.13, load=0.9, pressure="even")
```

**Each pass follows the edge; it does not hang off it.** The obvious way to write
this is a column at every x — walk across, drop a vertical stroke from the boundary
to the bottom — and it is wrong for the reason the section above gives: nine passes
that run *along* the silhouette describe the form, and thirty columns that run
*down* from it comb the mass into vertical strands and print the canvas's axis over
the whole thing. Same silhouette, half the strokes, and it looks like a hill instead
of a fence.

That is nine or ten strokes and it gives you a real silhouette, which is what you
wanted from the block-in and could not have got. One sweep leaves the boundary
stringy — a bristle brush covers about three-quarters of its width. Cross it with a
second set of passes at an angle to the first and the mass closes up. Some
raggedness left over is a good thing on the outside of a mass and a bad thing in the
middle of one.

If the mass is close enough to a box that this feels like overkill, `block_in` at
the angle the mass runs at is the cheaper version of the same idea.

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

Two things about the mixing that will surprise you:

- **Blue and yellow make green**, red and blue make violet, and complements make
  lively greys. This is subtractive pigment mixing, not RGB averaging.
- **White is a weaker lightener than you expect.** If you want a really pale colour,
  use a higher white ratio than feels right — `0.7`, not `0.4`.
- **A yellow and a blue make green even when you were after a grey**, and tinting
  does not undo it: `tint(mix("yellow_ochre", "cerulean", 0.3), 0.5)` is `#98ae69`,
  a pale green that sits in a warm painting like a traffic light. Neutral greys
  come from complements or from earth and white: `tint(mix("ultramarine",
  "burnt_sienna", 0.5), 0.7)` is a cool grey (`#9c8d8d`), `mix("burnt_umber",
  "titanium_white", 0.6)` a warm one (`#8b725b`), and `desaturate(c, 0.5)` pulls
  any mixture toward grey at the same value. Print `hex()` of a mixture before you
  paint a field of it.

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

Wetness also fades on its own as strokes accumulate, so you do not have to manage it
constantly. **Rule of thumb: if you want the new colour to read as itself, `dry()`
first.**

**Wet is a matter of a few strokes, not a whole pass.** Paint lands at roughly `0.7`
wetness and loses about six percent of what is left with every mark you make
anywhere on the canvas — half of it gone after about eleven strokes. That number
matters more than it sounds, because **one `block_in` is not one stroke**: a mass
laid with a medium brush is ten to thirty of them. So by the time you have blocked
in a second mass, the first is already most of the way dry, and paint you lay across
them both will blend into one and not the other. If you actually want two colours to
mix on the canvas, put the second one down within a few strokes of the first.

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
| `bristle` | **The workhorse** for any mark with a direction. Broken, streaky, alive — and never solid: one pass covers about three-quarters of its width. |
| `flat` | Block-in, chisel edges, flat planes. Turns to follow the stroke. |
| `round_hard` | Deliberate marks, accents, small shapes, final highlights. |
| `liner` | Fine lines at the scale of a feature: a lid, a brow, the lip of a cup, a mast. `round_hard` at `size=0.005` with no jitter at all, and it holds its load. |
| `round_soft` | Blending and soft edges. The least painterly — use it sparingly, and never for a mass: above about `size=0.05` it airbrushes. |
| `knife` | Thick slabs with a hard edge. Drags what it crosses. Use rarely, for punctuation. |
| `smudge` | Carries no paint; moves what is already there. For losing edges. |

The `knife` needs one more warning than "use rarely". Its marks are hard-edged
slabs, and against a mass of a different value they do not read as paint at all —
they read as something stuck to the surface. If you want a knife mark to belong,
keep it close in value to what it lands on and let a later stroke or a `smudge`
break one of its ends. Three knife marks two values lighter than the mass under
them will each look like a strip of tape.

A `bristle` stroke is never solid. Fully loaded it covers about three-quarters of
its own width, in a comb of parallel streaks. That comb is what makes it alive on
a mark whose direction you mean — hair, a fold, the sweep of an edge — and it is
what makes corduroy of a big quiet mass laid with single passes: above about
`size=0.12` the streaks print wider than anything in the picture, and every stroke
prints the same ones. Lay large quiet masses — a wall, a sky, a tabletop, a coat —
with `flat`, or with two `bristle` passes crossed, and keep single bristle
strokes for marks that have a direction.

Size is a fraction of the canvas's long side. `0.2` is a big brush, `0.02` is a small
one. **Use a bigger brush than feels comfortable**, especially early.

### The angle of the mark

**Do not let the canvas choose your stroke direction.** This is the loudest tell in
every painting made with this engine so far, and it is the easiest to fix. Left
alone, everything here runs horizontally or vertically: `block_in`'s named
directions are horizontal, vertical and a 45° diagonal; every named region is an
axis-aligned rectangle; and an oriented tip is held square to its travel, so a
horizontal stroke necessarily ends on a vertical edge. Paint a hillside with
horizontal passes and you get a stack of bars with flat ends, which is what a
hillside is not.

**Sweep a mass along its own axis.** `block_in` takes a number of degrees, clockwise
from horizontal, as well as the four names:

```python
s.block_in(span("A4", "F7"), "flat", "shadow", direction=28, size=0.12)
s.block_in(span("A4", "F7"), "flat", "shadow", direction=(28, 118), size=0.12)  # crossed
```

Measured on the same hillside: laid with the canvas's own axes it is 35% axis-aligned
edges, swept at its own angle 20% — and it took twenty *fewer* strokes, because
passes that run along the form cover it instead of stepping down it.

**Turn the blade.** Any oriented tip can be pinned instead of following its travel,
which is what turning a knife to cut a slope does:

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
the brush to change to — not `round_soft`, which airbrushes above `size=0.05`.

Anything about a brush can be overridden per stroke:

```python
s.stroke(path, "bristle", "shadow", size=0.14, opacity=0.5)
s.stroke(path, "flat", "light", hardness=0.9, jitter=0.05, load=0.4)
s.stroke(path, "bristle", "shadow", size=0.12, load_falloff=0.25)   # runs dry slower
```

`load` is how much paint the brush carries, and dropping it is how you get dry
brush — a broken, scratchy mark — with no special function to call. It is one of the
best tools you have for making a surface look worked.

**Load is not only a dry-brush control, and low is not the interesting default.**
Brushes start loaded (`bristle` at `0.9`, the rest at `1.0`), and anything that has
to read as a *solid mass* — a face, a block of local colour, a correction painted
over something wrong — wants to stay up there. Pass `load=1.0` explicitly when you
are covering. The numbers below are the window for deliberately *broken* marks; a
pass laid at `0.5` because it sounded painterly leaves a speckled film that
everything you paint afterwards has to sit on top of.

**The useful window is roughly `load=0.4` to `0.6`.** Below about `0.35` a bristle
brush is genuinely almost empty and leaves almost nothing, which is what an almost
empty brush does; if you wanted a mark there, you wanted a higher load. Brushes
differ — `flat` and `knife` keep marking further down than `bristle`, which is the
most texture-sensitive of them. Look after a dry-brush pass rather than assuming, and
if a stroke seems to have vanished, `s.log()` will tell you how much paint it laid.

The canvas decides what the breakup looks like: `rough` skips in chunky islands,
`linen` speckles at the scale of the weave, `smooth` leaves broader open gaps.

**A loaded brush runs dry along a stroke, and a long stroke shows it.** A bristle
stroke the full width of the canvas at `size=0.12` is about three-quarters solid
where it starts and, on `rough`, under half by its last quarter; on `linen` and
`smooth` it loses about a fifth. Where a long stroke ends is where its texture is
loudest, and if every stroke in a field runs the same way, one side of the field
speckles. `load_falloff` sets how fast the brush empties: the default is right for
marks a brush-length or three long, `load_falloff=0.25` keeps a canvas-wide stroke
even from end to end, and `0.0` never runs dry. For a big even field either pass
it, or run the next stroke the other way so the two dry ends do not coincide.

**Do not lay one broken pass across the whole canvas.** A single load, one brush,
edge to edge, prints the surface's own texture as an even field over everything —
the most mechanical mark available to you, and it stays visible under every later
stroke. If you want to knock a whole picture down, do it in three or four
overlapping passes at different loads and sizes, leave places untouched, and paint
back into it solidly afterwards.

### Pressure

`pressure` shapes the stroke along its length:

- `"taper"` — lands light, presses, lifts off. **The default, and usually right.**
- `"press_in"` — starts light, ends heavy.
- `"lift_off"` — starts heavy, trails away.
- `"even"` — constant. Use it deliberately; it is the flattest-looking option.
- `"swell"` — thin, thick in the middle, thin.
- `"dab"` — heavy at the start, gone quickly.

Or pass a number, or a list interpolated along the stroke: `pressure=[0.2, 1.0, 0.3]`.

**Pressure changes how heavily paint lands, not how wide the mark is.** A stroke at
`pressure=0.2` covers the same width as one at `1.0`; it just lays less paint. Two
consequences worth knowing before you go looking for a bug:

- On a long stroke with dabs overlapping, the profile is easy to miss — the marks
  pile up and saturate, so `taper` and `even` can come out looking much the same.
  You see the profiles most clearly on shortish strokes, and on a colour that is not
  already at full strength against its background.
- **Varying the width of your marks is your job, not the pressure profile's.** Pass
  a different `size` — that is the single most effective thing you can do to stop a
  painting looking mechanical, and no pressure setting will do it for you.

**At the scale of a feature.** A `round_hard` line keeps its width down to about
three pixels of the long side (`size=0.003` on a 1200-wide canvas), at full
strength, so the brushes go as small as anything you will paint. What changes at
that scale is not the brush. A single dab lands at about a third of its colour's
strength, so a highlight the size of a catchlight is two or three dabs on the same
spot, not one. A fine line runs dry over the same *distance* as a fat one, which
is far more brush-lengths, so it lasts. And pressure does not thin a line at its
ends, so a mark that tapers is two strokes of different sizes. Anything the size
of a cell or smaller is three marks at most — the dark, the light, and the edge
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

A `region=` crop is at full resolution, and a small one — a single cell — is
enlarged to at least 800 px, which shows a cell at five times or more. That is
the scale at which a feature can actually be judged. `region=span("D2", "E4")` is
the usual size for inspecting a passage, and a single cell is the size for a
feature. Regions can be written as strings anywhere: `region="D4"`,
`region="C3:F6"`, `region="upper-band"`.

With a reference, a `region=` crop crops **both** panels to the same place, so
you are always comparing like with like. `grid="fine"` then labels the tenths of
that crop on both — see *The drawing, before the masses* above, which is where
this view earns its keep.

Each look writes a numbered PNG under `out/` — `out/look_001.png`, `out/look_002.png`
and so on — and returns the path. Print it and open that file. The numbering belongs
to the session, so a second session started in the same directory begins again at
`look_001.png` and writes over the first one's; copy anything you want to keep.

With a reference, `grid=True` labels **both** panels with the same cells and
`values=True` converts **both** to greyscale on the same scale, so either one is a
like-for-like comparison. See *Working from a reference* above — that is the section
that matters if you were given a photograph.

Use `values=True` far more often than feels necessary. Use `diff=True` after a pass
to confirm you changed what you meant to change and nothing else.

When a mark seems to have gone missing, `s.log()` says how much paint each one
actually laid, and prints `NO PAINT LANDED` for a mark that changed nothing at all —
usually an opacity of zero, or a glaze into paint that is still soaking wet.

```
#014 stroke bristle #3a4a6b 212 dabs 8.4k paint
#015 stroke bristle #3a4a6b 212 dabs NO PAINT LANDED
```

---

## The rest of the API

```python
s.stroke(points, brush, color, pressure="taper", size=None, opacity=None, note="")
s.dab(x, y, brush, color, size=...)                # one mark
s.block_in(region, brush, color, direction=, density=)   # a mass, as strokes
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
`"cross"`, **a number of degrees**, or a sequence of any of those for one pass each.
**Vary it between passes, and prefer the angle the subject runs at** — see *The angle
of the mark*. Two passes of parallel strokes look like hatching; crossed passes look
like paint. Successive passes already run in opposite directions on their own, so a
mass does not fade towards the side the brush ran out on.

One `block_in` is not one stroke: it lays a pass for every brush-width of the
region, so a big region with a small brush can be twenty or thirty of them. Check
`s.stroke_count` if you are keeping a budget — a whole painting is usually a few
hundred marks, not a few thousand.

**`block_in` paints past its region.** Each pass runs about a third of a brush
beyond the region's ends (`overhang=0.35`), and the first and last rows sit a
quarter of a brush outside it, so a region blocked in at `size=0.1` comes out
roughly `0.05` wider than you asked on the sides and `0.025` taller. That is fine
for a wall and wrong for anything that meets something else: a shirt blocked in
beside a face lands on the face, a band of water blocked in under a headland buries
its foot. Painting back to front is the real answer — the far mass spilling into
where the near one is going does no harm, because the near one goes on over it next.
When two masses are at the *same* depth, pass `overhang=0` to keep the ends within a
fifth of a brush, or inset the region by half the brush size.

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

Under `easel run` all of these are already in scope. In a plain Python script,
import them: `from easel import Session, Region, region, cell, span, horizon,
below, above, left_of, right_of, between`.

---

## Seven small exercises

Run these before painting anything real. They take a minute each and will teach you
the engine's feel faster than reading will.

**1. A value scale.** Nine steps from dark to light. This calibrates your sense of
what the palette can actually reach.

```python
from easel import Session, Region

s = Session(900, 200, ground="toned_grey", seed=1)
for i in range(9):
    v = i / 8.0
    band = Region(i / 9.0, 0.15, (i + 1) / 9.0, 0.85)
    s.block_in(band, "flat", s.palette.mix("burnt_umber", "titanium_white", v),
               density=1.0, size=0.06)
s.look(values=True)     # do the steps look evenly spaced in greyscale?
```

**2. One stroke, six pressures.** See what the profiles actually do. Note the
`opacity=0.35` and `load_falloff=0.0`: at full strength the overlapping dabs
saturate and every profile looks identical, and paint running out along the stroke
hides the profile behind its own fade. Both have to be out of the way before you
can see what pressure alone is doing.

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
dry. This is the lesson that will otherwise cost you a painting.

Each band is laid with a *single* stroke, not a `block_in`. A block-in is ten to
thirty strokes, and wetness fades with every one of them — do this with block-ins
and the "wet" half has already dried by the time the yellow arrives, and the
exercise quietly teaches you the opposite of the truth.

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
- If you had a reference, does `s.compare("ref.jpg")` leave anything in
  `fixable`? Those are the last strokes worth spending. The `~` cells are not.
- Is every mass laid along its own axis, or are the big shapes stacks of horizontal
  and vertical bars? Turn the picture on its side if you cannot tell.
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
easel mark painting.easel rim_l 0.335 0.315    # and `easel mark p.easel` to list
easel compare painting.easel ref.jpg           # per-cell value numbers
easel prepare painting.easel ref.jpg --level coarse --merge 3,7
easel undo painting.easel 3
easel export painting.easel painting.png
easel timelapse painting.easel painting.gif
easel brushes                          # the full reference, printed
```

A script given to `easel run` has `s`, `palette`, and the whole API already in
scope. It needs no imports.
