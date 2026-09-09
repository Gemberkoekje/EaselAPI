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

### 2. Check your values before you check anything else

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
go, all land there. So you cannot make a near-black shadow, and trying is a waste
of strokes. **You build contrast by pushing the lights up, not the darks down.** If
a dark mass is not reading as dark, the fix is almost always that everything around
it is too dark, not that it is too light.

### 3. Refine the mid-tones

Now the middle values, with a medium brush (`size≈0.08–0.12`). Work across the
whole canvas rather than finishing one corner — a painting should come up all at
once, like a photograph developing. Look every ten strokes or so.

### 4. Edges: lost and found

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

### 5. Highlights last, smallest brush, fewest strokes

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

**Then stop measuring and paint.** The grid gets the masses into the right cells.
It will not draw a face for you, and chasing small features cell by cell is how you
spend three hundred strokes and arrive at a diagram.

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
x = 0.345
while x < 1.0:
    s.stroke([(x, top(x)), (x, 1.02)], "bristle", "dark",
             size=0.13, load=0.9, pressure="lift_off")   # heavy where the edge is
    x += 0.033                                           # about a brush width
```

That is fifteen or twenty strokes and it gives you a real silhouette, which is what
you wanted from the block-in and could not have got. One sweep leaves the boundary
stringy — a bristle brush run *away* from an edge combs it out into threads. Cross
it with a second pass running along the edge instead of away from it, and the mass
closes up. Some raggedness left over is a good thing on the outside of a mass and a
bad thing in the middle of one.

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

One line each. Reach for `bristle` first and most.

| Brush | What it is for |
|---|---|
| `bristle` | **The workhorse.** Broken, streaky, alive. Use it for almost everything. |
| `flat` | Block-in, chisel edges, flat planes. Turns to follow the stroke. |
| `round_hard` | Deliberate marks, accents, small shapes, final highlights. |
| `round_soft` | Blending and soft edges. The least painterly — use it sparingly. |
| `knife` | Thick slabs with a hard edge. Drags what it crosses. Use rarely, for punctuation. |
| `smudge` | Carries no paint; moves what is already there. For losing edges. |

The `knife` needs one more warning than "use rarely". Its marks are hard-edged
slabs, and against a mass of a different value they do not read as paint at all —
they read as something stuck to the surface. If you want a knife mark to belong,
keep it close in value to what it lands on and let a later stroke or a `smudge`
break one of its ends. Three knife marks two values lighter than the mass under
them will each look like a strip of tape.

Size is a fraction of the canvas's long side. `0.2` is a big brush, `0.02` is a small
one. **Use a bigger brush than feels comfortable**, especially early.

Anything about a brush can be overridden per stroke:

```python
s.stroke(path, "bristle", "shadow", size=0.14, opacity=0.5)
s.stroke(path, "flat", "light", hardness=0.9, jitter=0.05, load=0.4)
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
```

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
s.export("painting.png")
s.timelapse_gif("painting.gif")
s.log()                                            # what you have done so far
```

`block_in` takes `direction=` of `"horizontal"`, `"vertical"`, `"diagonal"` or
`"cross"`. **Vary it between passes.** Two passes of parallel strokes look like
hatching; crossed passes look like paint. Successive passes already run in opposite
directions on their own, so a mass does not fade towards the side the brush ran out
on.

One `block_in` is not one stroke: it lays a pass for every brush-width of the
region, so a big region with a small brush can be twenty or thirty of them. Check
`s.stroke_count` if you are keeping a budget — a whole painting is usually a few
hundred marks, not a few thousand.

Places:

```python
region("top-left")   # also: top, center, upper-half, lower-half, left-half,
                     # inner, middle-band, upper-band, lower-band, all, ...
cell("D6")           # a grid cell, matching look(grid=True)
horizon(0.42)        # a thin band at that height
below(r, 0.15)  above(r, ...)  left_of(r, ...)  right_of(r, ...)  between(a, b)
r.point(0.5, 0.5)    # a point inside a region, in the region's own 0–1 space
r.inset(0.05)  r.scaled(0.8)  r.split_h(3)  r.split_v(2)
```

---

## Six small exercises

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

---

## A checklist before you call it finished

- Does the greyscale view (`look(values=True)`) have a clear light, mid and dark?
- Are the edges varied — some hard, some soft, at least one lost?
- Is there anywhere the ground still shows through? (There should be.)
- Did you vary brush size, or is everything one width?
- Are the highlights few and deliberate?
- Is anything mechanically repeated — evenly spaced marks, identical parallel
  strokes, a perfectly straight line?

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
easel undo painting.easel 3
easel export painting.easel painting.png
easel timelapse painting.easel painting.gif
easel brushes                          # the full reference, printed
```

A script given to `easel run` has `s`, `palette`, and the whole API already in
scope. It needs no imports.
