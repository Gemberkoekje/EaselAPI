# Recipes: one situation at a time

[`PAINTER.md`](PAINTER.md) is the order of work. This file is what to lay when you are
in a particular situation — the calls, in order, what it looks like when it goes wrong,
and the number behind it, with the measurement in [`CALIBRATION.md`](CALIBRATION.md).
Each recipe was taken out of a real painting's pass scripts, with the painter's own
note on what it replaced.

**Read a recipe when you are about to paint one of these, not before.** There is
nothing here you need in your head. **Every recipe is a recipe that worked once**, and
any of them is worth abandoning the moment the look says so — and a recipe repeated
across three similar things is the guide's mechanical-repetition fault one level up, so
vary one thing per object on purpose.

Nothing here names a subject. A recipe that says what a thing is *of* gets painted as
that thing, and the name then does the choosing. Every heading says what the paint
*does*; you decide what it is a shape of.

**Where a recipe's *Goes wrong as* has a block under it, the block is the failure on
purpose — do not copy it.** It is cut by comment lines into the passage it is laid on,
the call that goes wrong with what the tool says about it, and, where it is not the
recipe itself, the smallest fix. `easel demo <recipe>` paints them side by side.

| | |
|---|---|
| **Before the first stroke** | [a scene with straight edges](#a-scene-with-straight-edges) · [a subject that is one thing against a ground](#a-subject-that-is-one-thing-against-a-ground) · [a picture with an empty half](#a-picture-with-an-empty-half) |
| **Surfaces** | [a plane that is a plane](#a-plane-that-is-a-plane) · [a form that turns](#a-form-that-turns) · [a mass built of planes](#a-mass-built-of-planes) |
| **Light** | [a passage light in the middle](#a-passage-light-in-the-middle) — *on a surface* · [a volume of lit air](#a-volume-of-lit-air) — *in a medium* · [a light broken down a surface toward the viewer](#a-light-broken-down-a-surface-toward-the-viewer) · [a passage brightening toward one side](#a-passage-brightening-toward-one-side) · [a graded field that is most of the picture](#a-graded-field-that-is-most-of-the-picture) · [a quiet gradient](#a-quiet-gradient) |
| **Marks** | [a small irregular bright mark](#a-small-irregular-bright-mark) · [a small round thing](#a-small-round-thing) · [a small container with something spilling from it](#a-small-container-with-something-spilling-from-it) · [a tapered arc](#a-tapered-arc) · [the one ruled line](#the-one-ruled-line) |
| **Edges** | [an edge that is actually lost](#an-edge-that-is-actually-lost) · [a mark that crosses a boundary](#a-mark-that-crosses-a-boundary) |
| **Order** | [a hollow thing](#a-hollow-thing) · [a repair under things that are standing on it](#a-repair-under-things-that-are-standing-on-it) |

---

## A scene with straight edges

Anything built of straight lines seen at an angle: a floor and the walls it meets, a
shelf receding, an opening at the far end. Its lines converge, and where they land on
the canvas is exactly the kind of number you cannot guess. Three painters built their
own projection before this recipe existed; write yours before you draw a line.

```python
import math

VX, VY, F, E = 0.40, 0.42, 0.8, 1.55      # vanishing point, focal length, eye height in metres

def P(xm, hm, dm):
    """Screen point for a place xm metres right of the axis, hm above the ground,
    dm metres away. The aspect term is what keeps a metre the same height as width."""
    return (VX + xm * F / dm, VY - (hm - E) * F * s.aspect / dm)

far_plane = polygon([P(-1.4, 0.0, 6.0), P(-1.4, 2.1, 6.0), P(1.4, 2.1, 6.0), P(1.4, 0.0, 6.0)])
side = polygon([P(1.4, 0.0, 6.0), P(1.4, 2.1, 6.0), P(1.4, 2.1, 1.3), P(1.4, 0.0, 1.3)])
ledge = polygon([P(0.5, 0.85, 1.2), P(1.35, 0.85, 1.2), P(1.35, 0.85, 4.2), P(0.5, 0.85, 4.2)])
for shape in (far_plane, side, ledge):
    s.pencil(shape.closed, pressure=0.5, smooth=False)
s.look(grid=True)                               # move the eye, the length, the frame; look again
```

Place things in metres and let one function say where they land. You are reliable
about how big things are and how far apart, and unreliable about where that falls on
the canvas; the function is reliable about the second thing, and each drawing it makes
costs nothing. Three numbers decide the picture before any paint: **the eye height**
decides what stands against what — a low eye puts a near thing against what is behind
it, a high eye puts it on what it stands on; **the vanishing point** decides how much
of each side you see; **the depth of the far plane** decides how big the lit end of
the scene is. Change one, look, change another. Cut any polygon off at the frame, since
a pass laid off the canvas still costs a stroke.

**What the projection gives you for free is the thing the guide asks for by hand: the
lines cross the bands.** A frontal view of the same scene is a layer cake; the same
scene down its own length is a fan of lines converging on one point, and every band is
crossed by every one of them.

Lay a plane built this way with its passes along its own perspective lines, or with
`edge="clean"` at a brush under a quarter of its shorter extent, because its
boundaries are sloped and a chisel ending on a slope is a staircase (*The shape each
tool leaves behind* in [`PAINTING.md`](PAINTING.md#the-shape-each-tool-leaves-behind)).
Thin members along those lines — the rails, the bars, the joints — go on as strokes
after the planes, thickest near the viewer, thinnest far off, and thinned to nothing
where they cross the brightest light.

**Goes wrong as:** a diagram — every line ruled to the same weight, every plane one
flat colour, nothing lost. A scene this exact reads as a rendering with texture on it.
Vary the weight of the lines, lose a few into the light, and give the planes an
incident each; the drawing is the scaffold, not the picture.

*Built three times by three painters and written down after the third.*

---

## A subject that is one thing against a ground

Composition is the one thing painters need with no procedure. These two entries are
what four paintings' notes record having done about it, and they are the most
speculative things in this file.

An upright thing against a horizon, a small thing on a ledge, a figure in a field: a
layer cake before a brush is picked. **Count the bands, then give the subject something
that crosses them, twice** — the subject itself, upright, and one more thing on the
diagonal that does compositional work as well as saying what the picture is about: a
fall of light, a shadow, a path.

```python
field = polygon([(0.0, 0.62), (1.0, 0.55), (1.0, 0.76), (0.0, 0.76)])   # a band
near  = polygon([(0.0, 0.76), (0.55, 0.80), (1.0, 1.0), (0.0, 1.0)])    # cut to a wedge
s.block_in(field, "bristle", "mid", size=0.10, direction="axis")
s.block_in(near, "bristle", "dark", size=0.08, direction="axis")
s.stroke([(0.34, 0.62), (0.70, 0.60), (1.05, 0.58)], "flat", "pale",
         size=0.012, opacity=0.6, pressure=[0.0, 0.7, 1.0])            # a horizon found late
```

Then take the bands out of the ground itself: run one edge of a ground mass off a corner
so it is a wedge rather than a band, and let the horizon start from nothing part of the
way across, so that over the subject's third of the picture there is no horizontal at
all. **How much of the frame the subject takes is the bands' question in disguise**: a
subject that crosses every band can be a fifth of the canvas and own it; one that sits
inside a band has to be half the canvas to be seen.

**Two things that both want to be the subject** is the same fault in value: one
painting's lightest passage had quietly become something other than its subject, and
the eye went there. The fix was not to move anything — concentrate the light's core
with a second inward scumble, and lay whatever stands in front of the light *again*, so
it is in front. The closing checklist's *is the lightest mass the one you planned?* is
this, checkable.

**Goes wrong as:** a stack of bands with a subject standing in one of them; or a
horizon ruled across the whole picture, which cuts the subject at the waist.

```python
# goes wrong: report() says "a stack of bars"
for top, size, t in ((0.0, 0.10, 0.9), (0.25, 0.08, 0.2), (0.5, 0.09, 0.6), (0.75, 0.07, 0.1)):
    s.block_in(Region(0.0, top, 1.0, top + 0.25), "bristle", p.mix("dark", "light", t),
               size=size, direction="horizontal")          # four bands, and nothing across
```

---

## A picture with an empty half

The subject took one side and the other side is haze, wall, water. **The empty half is
the ground's job, and the wrong repair is to put a thing there.** What has worked twice
is a second, fainter instance of the subject's own light, laid into the empty side at a
value inside the field's own range:

```python
field = s.sample(span("E1", "H4"))
p["far_light"] = p.at_value(p.mix(field, "light", 0.4), p.value_of(field) + 0.05)
s.dry()
s.glaze([(0.69, 0.245), (0.90, 0.262), (1.08, 0.285)], "far_light", opacity=0.07,
        size=0.15, pressure=[0.4, 0.8, 1.0])
s.glaze([(0.69, 0.245), (0.88, 0.26), (1.08, 0.28)], "far_light", opacity=0.10,
        size=0.07, pressure=[1.0, 0.7, 0.35])
```

Two glazes off to the other side say the light is turning rather than fixed, and they
fill the one empty corner without competing with anything. **Rehearse it on its own, so
it can be dropped**, and mix it close enough to the field that dropping it would be a
decision rather than a rescue. The other answer is to leave the half empty on purpose,
which the checklist's last line is where you decide.

**Goes wrong as:** a second subject (the thing put there was a thing); or the busy
corner corrected again while the empty one stays empty.

```python
# the passage: a subject and its light on one side, haze on the other
p["haze"] = p.at_value(p.mix("dark", "light", 0.5), 0.50)
s.block_in(Region(0.0, 0.0, 1.0, 1.0), "flat", "haze", size=0.1, solid=True, edge="hard")
s.scumble(ellipse(span("A1", "C3")), "haze", "light", 20, direction="inward")
s.block_in(Region(0.22, 0.40, 0.28, 1.0), "flat", "dark", size=0.03, solid=True,
           direction="vertical")                                 # the subject
# goes wrong: nothing says so
s.block_in(Region(0.75, 0.52, 0.81, 1.0), "flat", "dark", size=0.03, solid=True,
           direction="vertical")                                 # a thing put there
```

---

## A plane that is a plane

A flat surface, facing one way, taking one light. The commonest mass in any picture
and the one most often laid by accident at the wrong settings.

```python
s.block_in(span("C4", "F6"), "flat", "mid", size=0.05, density=1.0,
           solid=True, opacity=1.0, pressure="even", direction="axis")
```

Four clauses and each one earns its place: `solid=True` so no pass runs dry along its
length, `opacity=1.0` so the overlapping dabs do not accumulate unevenly, `even`
pressure because a taper puts a light end on every pass, and `direction="axis"` so the
passes run the way the plane runs rather than the way the canvas does.

**Goes wrong as:** a mottled field with the ground showing through in flecks — that is
`density=1.0` without `solid=True`, which spaces the passes rather than filling them.
Or as faint striping, which is the pass structure itself at about `0.03` of value
whatever you do to `opacity`: hide it with a bigger brush or a `bristle`, never with an
argument. Neither is anything the tool can see, so look for them.

```python
# goes wrong: nothing says so
s.block_in(span("C4", "F6"), "flat", "mid", size=0.05, density=1.0,
           direction="axis")                               # no solid=True: flecks
```

---

## A form that turns

A mass that is round rather than flat — the thing a value ramp across its width does
not give you. Three marks: the mass, the lit side, and the join.

```python
form = polygon([(0.31, 0.72), (0.45, 0.72), (0.43, 0.24), (0.29, 0.24)])
lit  = polygon([(0.37, 0.72), (0.45, 0.72), (0.43, 0.24), (0.35, 0.24)])
side = [(0.31, 0.72), (0.29, 0.24)]      # the form's own side: run the passes along it

s.block_in(form, "flat", "shadow", size=0.02, density=1.0, solid=True,
           direction=side, edge="clean")                       # the whole mass, dark
s.block_in(lit, "flat", "light", size=0.016, density=1.0, solid=True,
           direction=side, opacity=1.0, pressure="even")       # the lit side, on it
s.stroke([(0.370, 0.71), (0.359, 0.46), (0.351, 0.25)], "flat",
         s.palette.mix("shadow", "light", 0.5),
         size=0.012, opacity=0.6, load=1.0, load_falloff=0.0,
         pressure="even")                                      # the join, half strength
```

The mass goes down solid in the **shadow** colour, not the mid, and the lit side is a
second *shape laid on it* rather than a value change inside it. The single
half-strength stroke down the join is what turns the form; without it the two shapes
meet at a step, and that step is the whole difference between a cylinder and two
stripes. Keep the lit shape's edge off the silhouette on the lit side by a hair. **Shade
until the form clears `0.10` and stop**: form is bounded at both ends, and past about
`0.15` across one mass its shadow side stops separating from what it stands against.

**Goes wrong as:** two flat stripes side by side (no join stroke); or as a flat field,
which is what a pass ramp across the whole width gives you — and the light on the wrong
side, because the first pass of a stack is not where reading the call suggests
(*Where a stack of passes starts* in [`REFERENCE.md`](REFERENCE.md#where-a-stack-of-passes-starts)).

---

## A mass built of planes

A big irregular solid thing with structure in it. The instinct is to lay the mass and
then put marks *on* it, which reads as things stuck to a smooth hull every time. **A
mass like this is not a mass with facets. It is the planes it is made of**, tiling it,
each one a shape at one value, with the block-in's dark left showing as the shadow
between them.

```python
whole = polygon([(0.05, 0.60), (0.22, 0.56), (0.40, 0.64), (0.52, 0.74),
                 (0.58, 0.92), (0.10, 0.92)])
faces = [(polygon([(0.06, 0.61), (0.24, 0.58), (0.38, 0.65), (0.30, 0.70),
                   (0.12, 0.66)]), "pale", 0.014,
          [(0.06, 0.61), (0.24, 0.58)]),                # the plane facing the light
         (polygon([(0.40, 0.67), (0.52, 0.76), (0.56, 0.90), (0.42, 0.86)]),
          "mid", 0.016, [(0.40, 0.67), (0.42, 0.86)]),  # the plane facing sideways
         (polygon([(0.10, 0.70), (0.34, 0.74), (0.40, 0.88), (0.14, 0.90)]),
          "cool", 0.02, [(0.10, 0.70), (0.34, 0.74)])]  # the body between them

s.block_in(whole, "flat", "dark", size=0.06, density=1.0, solid=True,
           direction="axis", edge="clean")
for face, colour, size, side in faces:                  # each along a side of its own
    s.block_in(face, "flat", colour, size=size, density=1.0, solid=True,
               direction=side, edge="clean", opacity=1.0, pressure="even")
s.stroke([(0.27, 0.66), (0.32, 0.71), (0.40, 0.77)], "round_hard", "dark",
         size=0.014, opacity=0.9, pressure="taper")            # one crevice
s.stroke([(0.14, 0.72), (0.26, 0.76)], "bristle", "pale",
         size=0.03, load=0.35, opacity=0.6)                    # dry brush, for surface
```

Three or four planes is enough; the planes carry the form and the crevices are
punctuation. Keep each plane a brush's half-width inside the silhouette so nothing
fringes past it, and give the planes different brush sizes — they are different sizes
of thing. **Run each plane's passes along a side of its own**: the grain then turns
from plane to plane, the side it runs along closes exactly, and `edge="clean"` draws
the others rather than stepping down them. A chisel ending on a
slope is a staircase, and a comb under `size=0.025` is a woven plane — at these sizes
the flat, laid clean and along a side, is the brush.

**Draw the planes with the silhouette.** A mass like this has two drawings in it, and
the second is not the finish: decide the tiling *before* the block-in, as polygons
beside the outline, the way `faces` sits beside `whole` above. Decided after the mass is
down, the planes arrive as things laid *on* a hull, which is this recipe's own failure
one level up.

**Goes wrong as:** slabs stuck on a smooth shape (planes laid as marks rather than as
tiles), or as a woven surface (bristle streaks used instead of planes). Or as a
staircase down every sloped side, which is a chisel's pass ends stacking on a slope and
is why the silhouette above is laid `edge="clean"`:

```python
# the passage: the ground it stands on, and its silhouette drawn
s.block_in(Region(0.0, 0.0, 1.0, 1.0), "flat", "surface", size=0.05, solid=True,
           edge="hard", direction="vertical")
whole = polygon([(0.05, 0.60), (0.22, 0.56), (0.40, 0.64), (0.52, 0.74),
                 (0.58, 0.92), (0.10, 0.92)])
# goes wrong: chisel-staircase
s.block_in(whole, "flat", "dark", size=0.06, density=1.0, solid=True, direction="axis")
# the smallest fix: a clean edge draws the sloped sides instead of stepping down them
s.block_in(whole, "flat", "dark", size=0.06, density=1.0, solid=True, direction="axis",
           edge="clean")
```

---

## A passage light in the middle

A glow, a bloom, light falling on a surface. It is dark at **every** edge, which is
what makes it not a gradient.

**This one is light *on* something.** If there is no surface — light in the air
itself, a beam, a halo seen from outside — it is [a volume of lit air](#a-volume-of-lit-air),
and this verb cannot lay it.

```python
s.scumble(patch, "shadow", "light", 8, direction="inward")     # 8 strokes
```

`direction="inward"` lays the passes *round* the place, the first along its boundary
and each one after it a part-brush further in, so the colour arrives from the edge to
the centre. **Leave `size` off.** The rings step `depth / n` apart and the brush has to
be under about three of those steps or the last rings bury the first; with no `size=`
the verb picks `3 × depth / n` itself and warns when you hand it a wider one. **Give
the first ring the value the patch meets its surroundings at**: the ring lands *on* the
boundary, so anything darker draws a rim round your glow and melts nothing. On a patch
too shallow for any `n` to fit, the verb says so and names the recipe below.

**Goes wrong as:** a solid disc with a thin ramp round it (brush too wide); a daisy
(strokes radiating from a shared centre, which `report()` names); a rim with nothing in
the middle (first ring darker than what it sits in); or visible concentric rings, which
is too few rings for the patch
(*`scumble`* in [`CALIBRATION.md`](CALIBRATION.md#scumble)).

```python
# the passage: the dark the patch sits in, which its first ring matches
s.block_in(Region(0.0, 0.0, 1.0, 1.0), "flat", "shadow", size=0.1, solid=True, edge="hard")
# goes wrong: inward-flat
s.scumble(patch, "shadow", "light", 8, direction="inward", size=0.2)   # a brush past the rings
```

*The single most rehearsed thing in the repository.*

---

## A volume of lit air

A beam, a shaft, a halo seen from outside: light *in* the air rather than light on a
surface. It has no surface and no edge anywhere, which is why the recipe above does not
lay it. Three glazes along the axis of the light, with the one brush the guide otherwise
warns you off masses, because this is not a mass.

```python
field = s.sample(span("A2", "H4"))                 # what the air will sit in
v = p.value_of(field)
p["air_far"]  = p.at_value(p.mix(field, "light", 0.5), v + 0.06)
p["air_body"] = p.at_value(p.mix("light", field, 0.35), v + 0.10)
p["air_core"] = p.at_value(p.mix("light", field, 0.25), v + 0.14)
source, far = (0.64, 0.24), (-0.08, 0.42)
s.dry()
s.glaze([source, (0.30, 0.335), far], "air_far", opacity=0.09, size=0.20,
        pressure=[0.4, 0.8, 1.0])                  # wide and faint: widest at the far end
s.glaze([source, (0.30, 0.33), (-0.08, 0.41)], "air_body", opacity=0.15, size=0.11,
        pressure=[1.0, 0.8, 0.4])                  # the body, thinning away from the source
s.glaze([source, (0.42, 0.295), (0.18, 0.355)], "air_core", opacity=0.17, size=0.06,
        pressure=[1.0, 0.7, 0.12])                 # the core: brightest at the source
s.dry()                                            # and again, before anything crosses it
```

**Mix the glazes close to the field, in value and in hue** — a step or two above it,
leaning toward its own colour — because a glaze far from what it lands on has no usable
opacity. Lay them with the soft round tip along the axis, and **taper by pressure**: a
round tip's width follows pressure, so `[1.0, ..., 0.1]` is narrow-and-bright at the
source and wide-and-gone at the far end, which is what a cone of lit air is. The wide
faint one runs the other way, so the cone opens as it travels. `dry()` first, so the
film sits on the field rather than mixing into it — **and again after**, which is the
clause that gets left off. The three films leave the beam wet (`0.14` at the core), and
an opaque mark laid across it afterwards drags what it lands on: up to `0.30` in value
where a mass crosses it, `0.40` where a stroke does.

**Goes wrong as:** a ribbed slab (a `bristle` block-in of the wedge); a fan of ribbons
(five `flat` rays); a searchlight that owns the picture (the glaze mixed to the light's
own colour rather than close to the field — the fix is hue, not opacity); or a beam
brightest at the *wrong* end, which is what the taper does when the list runs the other
way.

```python
# the passage: a dark field for the air to sit in
s.block_in(Region(0.0, 0.0, 1.0, 1.0), "flat", "dark", size=0.1, solid=True, edge="hard")
# goes wrong: glaze-far
s.dry()
s.glaze([(0.64, 0.24), (0.30, 0.33), (-0.08, 0.41)], "light", opacity=0.15, size=0.11,
        pressure=[1.0, 0.8, 0.4])                  # mixed as the light, not near the field
```

*Found in five rehearsals, and in two other paintings' notes.*

---

## A light broken down a surface toward the viewer

A light that lands on a surface between it and you and comes toward you in pieces. Four
of seven painters failed this passage first, and failed it alike — *floating
rectangles*, *small bricks*, *a ziggurat*, *spoon-shaped islands*, each a run of marks
of one shape. The versions they kept, taken together, come to four things.

```python
import random

rng = random.Random(5)
under = s.sample(Region(0.55, 0.55, 0.70, 0.95))          # what the light lands on
p["film"] = p.at_value(p.mix(under, "light", 0.4), p.value_of(under) + 0.06)
s.dry()
s.glaze([(0.62, 0.52), (0.625, 0.72), (0.63, 0.96)], "film", opacity=0.15, size=0.08,
        pressure=[1.0, 0.7, 0.3])                        # a film carries it down first
y, gap, spread, op = 0.53, 0.022, 0.017, 0.88
while y < 0.97:                                           # further apart, wider, fainter
    x, n = 0.62 + rng.gauss(0, spread), rng.uniform(0.018, 0.05)
    s.stroke([(x - n / 2, y + 0.002), (x, y - 0.002), (x + n / 2, y + 0.001)],
             "round_hard", "light", size=0.01, opacity=op, tip_wobble=0.6,
             pressure=[0.05, 1.0, 0.4])                  # no two the same length
    y, gap, spread, op = y + gap, gap * 1.2, spread * 1.2, op * 0.85
s.stroke([(0.58, 0.66), (0.65, 0.665)], "round_hard", "dark", size=0.006, opacity=0.8)
s.stroke([(0.61, 0.84), (0.70, 0.83)], "round_hard", "dark", size=0.006, opacity=0.8)
```

- **A film first**, carrying the light down onto the surface, mixed from what it lands
  on: the pieces then sit on a passage that is already lit rather than on the dark.
- **Every piece a different length**, with a bend in it and its ends lifted, and its
  tip's outline drawn afresh (`tip_wobble=`). A column of one length is the failure
  below, whatever else changes down it.
- **The rows, not the pieces, change as the light comes toward you**: further apart,
  spread wider, fainter. The pieces keep their lengths; the passage opens out.
- **Then the surface's own dark laid back across it**, thin and after the lights are
  down: the dark between the pieces is as much of the light as the pieces are.

**Goes wrong as:** a ladder — one mark at one length repeated down the path, which is a
loop's signature and which `report()` names; a strict ramp of lengths is the same loop
with one more number in it. Or a column of rectangles under the light, which is a chisel
at one size.

```python
# the passage: a surface, and the light above it
p["far"] = p.mix("dark", "light", 0.5)
s.block_in(Region(0.0, 0.0, 1.0, 0.5), "flat", "far", size=0.025, solid=True, edge="hard")
s.scumble(Region(0.0, 0.5, 1.0, 1.0), "far", "dark", 40)     # darkening toward you
s.dab(0.62, 0.30, "round_hard", "light", size=0.04, press=3)
# goes wrong: report() says "a loop's signature"
for i in range(8):
    y = 0.55 + 0.05 * i
    s.stroke([(0.57, y), (0.67, y)], "flat", "light", size=0.02 - 0.001 * i,
             opacity=0.8 - 0.08 * i, load=1.0, load_falloff=0.0, pressure="even")
```

*Collected from four paintings' accepted versions of the same passage.*

---

## A passage brightening toward one side

Not a glow and not a band between two masses — a whole area that simply gets lighter
toward one edge, with nothing in it having an outline.

```python
for i in range(6):
    t = i / 5
    y = 0.44 + t * 0.14
    s.stroke([(0.22 + 0.08 * t, y + 0.006), (0.60, y - 0.004), (1.06, y)],
             "flat", s.palette.mix("shadow", "light", t),
             size=0.085, opacity=0.5, load=1.0, load_falloff=0.0,
             pressure=[0.0, 0.55, 1.0])
```

Every pass runs the **same** way, one value step apart, each landing at no pressure on
one side and full pressure on the other — so the passage brightens without any pass
having a visible end. The ends run off the canvas on purpose. The same thing works as
one `block_in`, `scumble` or `sweep` call with a pressure list, which is read in canvas
order on every pass.

**Written by hand, the brush is yours to get right.** Above, the passes step `0.028`
apart and the brush is `0.085` — three steps, on purpose. **Keep the narrowest brush in
the stack over twice the step**, or hand the passage to `scumble`, which sizes its own;
the post-pass check reads this off the log and says so.

**Goes wrong as:** a stack of bars (passes too few or the brush too narrow to overlap);
or a passage that brightens in stripes, which is a pressure list on hand-written passes
that alternate direction.

```python
# goes wrong: report() says "comes back as bars"; report() says "a loop's signature"
for i in range(6):
    t = i / 5
    y = 0.44 + t * 0.14
    s.stroke([(0.22 + 0.08 * t, y + 0.006), (0.60, y - 0.004), (1.06, y)],
             "flat", s.palette.mix("shadow", "light", t),
             size=0.02, opacity=0.5, load=1.0, load_falloff=0.0,
             pressure=[0.0, 0.55, 1.0])            # a brush under one step, not three
```

---

## A graded field that is most of the picture

A sky, a far field, a sheet of water seen at a grazing angle: a third of the canvas or
more, graded, with no outline anywhere in it and no second mass to be a band
*between*. It is the biggest thing you will paint, and the recipes above are all
smaller than it.

```python
upper = polygon([(-0.06, -0.06), (1.06, -0.06),
                 (1.06, 0.59), (-0.06, 0.62)])       # where the light changes along
lower = polygon([(-0.06, 0.50), (1.06, 0.47), (1.06, 1.06), (-0.06, 1.06)])
s.scumble(upper, "light", "mid", 7, direction=4,     # the field, it is two ramps
          opacity=0.95)
s.scumble(lower, "mid", "shadow", 8, direction=3, opacity=0.95)
s.stroke([(-0.06, 0.31), (0.42, 0.37), (1.06, 0.34)], "bristle", "mid",
         size=0.075, load=0.40, opacity=0.45, pressure="swell")   # and two crossers
s.stroke([(1.06, 0.72), (0.55, 0.68), (-0.06, 0.73)], "bristle", "shadow",
         size=0.065, load=0.35, opacity=0.40, pressure="swell")
```

**Three things, and the middle one is the one that gets left off.**

- **The verb, over the whole field, with `size` left off.** It picks a brush from its
  own step; a hand-laid band is where this goes wrong. **Run the field off every edge it
  is not bounded by**, the way `upper` does above: a boundary drawn inside the canvas
  cuts the passes that reach it into stubs shorter than the brush is wide — `0.210`
  against a brush of `0.252` on this field's old outline — and the verb says so
  (`scumble-wedge`).
- **A direction a few degrees off the frame.** The passes of a field that runs exactly
  along the frame are a stack of bands parallel to the edge of the picture, which the
  eye finds and a row profile does not.
- **Two or three ramps, not one, wherever the light changes along it** — warm where it
  reflects one thing, cool where it reflects another. Overlap them; the join
  disappears into the next ramp's first pass.

**And something has to cross it.** A graded field with nothing crossing it *is* a band,
however closed its joins. Two or three starved passes at an angle, ends running off the
canvas, none of them parallel to each other.

**This buries the ground, and the closing checklist asks for some back.** Both are
right, and the picture decides which: a field over a third of the canvas at
`load=1.0, opacity=0.95` leaves nothing of the ground under it, and five painters in one
round accepted `ground: 0.0x% … the checklist asks for some` by hand for exactly this
reason. Say `s.plan(ground="buried")` and the line prints its number without asking.
Say nothing and the floor holds, which is what you want on a picture whose warm ground
was meant to be seen through.

**Goes wrong as:** horizontal strata (passes run exactly along the frame); a stack of
bands with a different name (nothing crossing it); a field that reads as two fields (two
ramps that do not overlap); or bare ground along its top, where an outline drawn inside
the canvas cut the passes into stubs:

```python
# the passage: the field's own colours, a step or two apart
p["light"] = p.mix("titanium_white", "cerulean", 0.25)
p["mid"] = p.mix("titanium_white", "cerulean", 0.45)
p["shadow"] = p.mix("ultramarine", "titanium_white", 0.55)
# goes wrong: scumble-wedge
upper = polygon([(-0.06, 0.13), (0.34, 0.19), (0.62, 0.15), (1.06, 0.10),
                 (1.06, 0.59), (-0.06, 0.62)])        # its top drawn inside the canvas
s.scumble(upper, "light", "mid", 7, direction=4, opacity=0.95)
```

---

## A quiet gradient

What closes a join between two values is many overlapping strokes at closely spaced
values.

```python
s.scumble(span("A4", "H6"), "shadow", "light", 8)      # 8 strokes, and it costs 8
```

Eight passes along the band, stepping across it, one value step per pass. The overlap
is the whole mechanism: the brush is wider than the step between passes. **Leave `size`
off** and the verb picks a brush from its own step — about three steps, the middle of
the window; between one and one and a half steps is the worst place, and it is where a
preset's own default lands on an ordinary band (*The band, and the brush that closes
its joins* in [`CALIBRATION.md`](CALIBRATION.md#the-band-and-the-brush-that-closes-its-joins)).
Below about five passes the steps read as steps again.

**That works on a band, and a band is a shape whose passes are all about one length.**
On a wedge — anything whose width changes a lot along the direction the passes step —
one brush cannot serve both ends: picked for the step, it is wider than the whole narrow
end and the paint blooms past the outline there. The verb says so, naming both pass
lengths. Lay a wedge as two or three bands each sized to its own width.

**And a `flat` scallops a wide band**: its own wander prints the passes at about `0.11`
peak to peak, against `0.03` for a solid block-in. A `bristle`'s comb reads as incident
rather than as banding; if it has to be a flat, halve `jitter` and `size_jitter`.

**Do not reach for a second smudge instead.** A smudge removes about 40% of a step
exactly once, and doing it again undoes most of the first pass (*`smudge`* in
[`CALIBRATION.md`](CALIBRATION.md#smudge)). When once is not enough the answer is
paint.

**Goes wrong as:** bars with the ground between them — a brush under the step between
passes, so nothing overlaps, which the call names; steps, under about five passes; or a
scalloped band, laid with a `flat`.

```python
# goes wrong: scumble-bars; report() says "comes back as bars"
s.scumble(span("A4", "H6"), "shadow", "light", 8, size=0.03)   # a brush under one step
```

---

## A small irregular bright mark

Something small, light and not a shape: a catch of light, a clot, a fleck of something.

```python
s.stroke([(0.19, 0.26), (0.27, 0.31), (0.34, 0.30)], "bristle", "pale",
         size=0.048, load=0.75, opacity=0.75, pressure="swell")   # a smear with a bend
s.dab(0.42, 0.36, "round_hard", "pale", size=0.016, press=3, tip_wobble=0.7)
```

Two answers, for different marks. **Give it a length and a bend** — a short smear from
a starved brush, which has a silhouette because the comb is redrawn per stroke. Or, if
it really is one small mark in one place, `tip_wobble=0.7` on a round tip, which draws
the tip's outline afresh for every mark: two `round_hard` dabs share 97% of their
silhouette at `0` and 76% at `0.7`.

**Goes wrong as:** a row of floating discs. Five small `round_hard` dabs are five copies
of one disc to within 7% — the tip printing itself. The `bristle` is the only tip that
does not repeat itself, because its comb is drawn per stroke.

```python
# the passage: a dark field
s.block_in(Region(0.0, 0.0, 1.0, 1.0), "flat", "dark", size=0.1, solid=True, edge="hard")
# goes wrong: report() says "one disc printed"
for x, y in ((0.19, 0.26), (0.23, 0.29), (0.27, 0.31), (0.31, 0.30), (0.35, 0.31)):
    s.dab(x, y, "round_hard", "pale", size=0.016, press=3)   # five of one tip: floating discs
```

**Landing one of these *inside* a mass: ask the mass.** The shape already knows:

```python
import numpy as np

x, y = 0.48, 0.52
if mass.contains(x, y):                                  # one point
    s.dab(x, y, "round_hard", "pale", size=0.012, press=3)

xs, ys = np.random.default_rng(4).random((2, 40))        # or forty at once
inside = mass.inside(xs, ys)
xs, ys = xs[inside], ys[inside]
```

---

## A small round thing

Sometimes the thing **is** a disc, and the guide's warning against discs reads as if it
never is. A light in the distance, a catchlight, a berry, a stud: lay it as a disc and
stop.

```python
s.dab(0.62, 0.35, "round_hard", "pale", size=0.012, press=3)
```

`press=3` stamps the same spot three times with the middle stamp at full pressure, and
it is **one** mark against your budget. Use it for anything you actually want to land;
`press=1` and `press=2` are whispers.

**Goes wrong as:** several of them. One disc is a thing; five discs are the brush. If
you want five, vary at least one thing per mark, or use the recipe above.

```python
# the passage: a dark field
s.block_in(Region(0.0, 0.0, 1.0, 1.0), "flat", "dark", size=0.1, solid=True, edge="hard")
# goes wrong: report() says "one disc printed"
for x, y in ((0.55, 0.33), (0.58, 0.37), (0.61, 0.32), (0.64, 0.36), (0.67, 0.33)):
    s.dab(x, y, "round_hard", "pale", size=0.012, press=3)
# the smallest fix: the tip drawn afresh for every mark
for x, y in ((0.55, 0.33), (0.58, 0.37), (0.61, 0.32), (0.64, 0.36), (0.67, 0.33)):
    s.dab(x, y, "round_hard", "pale", size=0.012, press=3, tip_wobble=0.35)
```

---

## A small container with something spilling from it

Two or three parts, each of which has to read as a different kind of thing, in three
marks or fewer — at a size where the recipes above give you a single accent.

```python
x, y, r = 0.46, 0.58, 0.02
s.stroke([(x - r * 0.8, y), (x + r * 0.8, y)], "flat", "mid", size=r * 1.55,
         opacity=1.0, load=1.0, load_falloff=0.0, pressure="even")      # the body
s.stroke([(x - r, y - r * 0.52), (x + r, y - r * 0.52)], "flat", "pale",
         size=r * 0.6, opacity=1.0, load=1.0, load_falloff=0.0,
         pressure="even")                                              # the rim, on it
s.stroke([(x - r * 0.45, y - r * 0.95), (x + r * 0.35, y - r * 2.0),
          (x + r * 0.9, y - r * 3.0)], "bristle", "cool", size=r * 0.9,
         load=0.7, opacity=0.9, pressure="swell")                      # what spills
```

The body is **one chisel mark, and a rectangle on purpose** — the one place a tool's
own geometry is allowed to stand for the thing, because a `flat`'s chisel really is
that shape. The rim is a second, narrower chisel mark, *wider* than the body and
lighter, sitting on its top edge; it is what makes a block a container. What spills is
one starved stroke going up and over: a `bristle` above `size~0.025`, and below that
`round_hard` with `pressure="lift_off"`, because a comb that small is four streaks. Then
vary one thing per container — the tilt, which side the spill falls, whether there is a
rim at all.

**Seen from above the rim, the container is a hollow thing**: the far arc of the rim
closes the silhouette, the opening inside it goes darker, and one tapered arc of light
along the near rim finishes it ([a tapered arc](#a-tapered-arc), then
[a hollow thing](#a-hollow-thing)). Nine of these on one ledge want a stroke recipe,
not a block-in each — one to three chisel strokes for a body, one capsule for a rim,
one dark stroke for the opening, one lit arc — or the row costs the budget.

**Goes wrong as:** a small round fruit (the body laid with a round tip under a pressure
taper, which reads as a bulb); a brick (the body alone); a bite or a frown (a dark arc
at the rim, which reads as damage rather than as a rim); or a fat scalloped cushion for
a rim (a round tip block-in fringing past a small ellipse).

```python
# goes wrong: round-fringe
x, y, r = 0.46, 0.58, 0.02
s.block_in(ellipse(Region(x - r, y - r * 0.8, x + r, y - r * 0.25)), "round_hard", "pale",
           size=0.012)                              # a rim laid as a mass with a round tip
```

---

## A tapered arc

A curve that thins to nothing at both ends: a rim of light along something round, a
sliver of one thing showing past another. One stroke.

```python
import math
cx, cy, r = 0.72, 0.22, 0.05
arc = [(cx + r * math.cos(math.radians(a)),
        cy + r * s.aspect * math.sin(math.radians(a)))
       for a in (-62, -20, 30, 80, 122)]
s.stroke(arc, "round_hard", "pale", size=0.011, opacity=0.95,
         load=1.0, load_falloff=0.0, pressure=[0.05, 0.6, 1.0, 0.6, 0.05])
```

The pressure list is the recipe: a round tip's width follows pressure, so the horns
thin to a point and the middle is the width you asked for. `s.aspect` in the `y` term
keeps the arc circular on a canvas that is not square.

**Goes wrong as:** a ghost. The obvious construction — a disc with a second disc in the
background's colour bitten out of it — leaves the bitten edge visible as a seam,
because the second disc is paint and not an eraser.

```python
# the passage: a dark field for the arc to lie on
s.block_in(Region(0.0, 0.0, 1.0, 1.0), "flat", "dark", size=0.1, solid=True, edge="hard")
# goes wrong: nothing says so
s.dab(0.72, 0.22, "round_hard", "pale", size=0.10, press=3)      # a disc...
s.dab(0.70, 0.20, "round_hard", "dark", size=0.095, press=3)     # ...bitten out with paint
```

---

## The one ruled line

Almost nothing in a painting should be perfectly straight, and the checklist asks you
about it. There are one or two exceptions, and when you want one you have to ask,
because every brush here wanders by default.

```python
s.stroke([(-0.05, 0.59), (1.05, 0.59)], "flat", "mid", size=0.026,
         opacity=0.9, load=1.0, load_falloff=0.0,
         jitter=0.0, size_jitter=0.0, pressure="even")
```

`jitter=0, size_jitter=0` is the ruled line. The middle setting is usually what you
actually want: the defaults are `jitter=0.02, size_jitter=0.06` and wander about `1.2`
px on a `size=0.1` `flat`; `jitter=0.01, size_jitter=0.03` halves the wander, and zero
is ruled. If a long edge is coming out scalloped, the halved setting is the one to try
before the ruled one. Larger is not an option: at `jitter=0.5` a thin member comes back
as a chain of separate beads.

**Goes wrong as:** a mechanical line in a painting that has none — which is why this
recipe carries a warning rather than a recommendation. Run the ends off the canvas so
it has no visible termination. A thin member laid as several short marks beads into a
chain of separate blocks; lay it as one stroke. So does one laid with its wander turned
up, which the call names:

```python
# goes wrong: jitter-beads
s.stroke([(-0.05, 0.59), (1.05, 0.59)], "flat", "mid", size=0.026, opacity=0.9,
         load=1.0, load_falloff=0.0, jitter=0.5, pressure="even")   # 25 times the wander
# the smallest fix: half the default wander, not twenty-five times it
s.stroke([(-0.05, 0.59), (1.05, 0.59)], "flat", "mid", size=0.026, opacity=0.9,
         load=1.0, load_falloff=0.0, jitter=0.01, size_jitter=0.03, pressure="even")
```

---

## An edge that is actually lost

A lost edge is one where two masses meet with **no boundary at all** for a stretch.
Not a soft edge; an absent one, and the thing most often done by halves.

```python
s.smudge([(0.30, 0.40), (0.34, 0.415), (0.38, 0.43)])  # the stretch you mean to lose
s.smudge(mass.closed[3:5])                             # or a stretch of the mass's outline
s.stroke([(0.42, 0.30), (0.47, 0.35), (0.45, 0.43)], "bristle", "mid",
         size=0.028, load=0.60, opacity=0.55, pressure="taper")   # then paint across it
```

Run the smudge along the boundary's own shape — only a straight boundary is two points
— and once, never twice. Then, if the boundary is still there, **lay paint across it**
in a value between the two masses, at a low opacity with a starved brush: that is what
actually loses an edge. The smudge softens; the paint is what removes.

**A smudge loses a *stretch*, not a boundary.** Past about a tenth of the canvas its
strip reads as a band of its own — *dark, mid, light* — and the call says so
(`smudge-long`); there, go to the paint-across recipe from the start.

**Goes wrong as:** two edges that are *nearly* lost and read as neither — the commonest
outcome. Lose one edge completely rather than four edges partly. Or a strip of a third
value where the edge was, which is a smudge run the length of the boundary:

```python
# the passage: a light field over a dark mass, meeting on a slope
s.block_in(Region(0.0, 0.0, 1.0, 1.0), "flat", "light", size=0.1, solid=True, edge="hard")
s.block_in(polygon([(0.0, 0.2875), (1.0, 0.6625), (1.0, 1.0), (0.0, 1.0)]), "flat", "dark",
           size=0.08, solid=True, edge="hard")
# goes wrong: smudge-long
s.smudge([(0.02, 0.295), (0.62, 0.52)])            # the whole boundary, not a stretch
```

---

## A mark that crosses a boundary

When a smudge is not the answer, which is most of the time.

```python
s.stroke([(0.15, 0.32), (0.23, 0.36), (0.29, 0.33)], "bristle", "pale",
         size=0.036, load=0.55, opacity=0.50, pressure="swell")
```

A broken mark in a value between the two masses, laid *across* where they meet, with a
starved brush at half opacity so it is a suggestion rather than a third mass. Two or
three of them, no two alike.

**Goes wrong as:** a finger-shaped lobe of the lighter mass dragged into the darker
one. That is a smudge run across a boundary instead of along it, and it is the
expensive kind of damage: burying a thumbprint means repainting the mass it sits on,
which buries everything else standing there.

```python
# the passage: two masses that meet, the first laid past the line
s.block_in(Region(0.0, 0.0, 0.24, 1.0), "flat", "dark", size=0.08, solid=True, edge="hard")
s.block_in(Region(0.22, 0.0, 1.0, 1.0), "flat", "light", size=0.08, solid=True, edge="hard")
# goes wrong: smudge-across
s.smudge([(0.34, 0.50), (0.10, 0.52)], size=0.03)  # dragged across the join, out of the light
```

---

## A hollow thing

Anything you can see into is three masses at three depths, and the order is the whole
recipe: **the far edge, then what is inside, then the near edge.** It lives in
[`PAINTER.md`](PAINTER.md#3-paint-from-back-to-front) at step 3, because it is part of
depth order rather than a procedure. What belongs here is the mark that finishes it:

```python
s.stroke([(0.165, 0.74), (0.23, 0.78), (0.31, 0.79)], "round_hard", "pale",
         size=0.0085, opacity=0.95, pressure=[0.15, 1.0, 0.35])
```

**One broken catch-light along the near edge is what makes a hollow thing read as
hollow**, and it should be the only mark on it. Partial, off-centre, and let the rest of
the near edge stay lost into whatever is behind it.

**Goes wrong as:** a ring — the catch-light carried all the way round, which outlines
the opening instead of lighting its edge; or the inside laid last, with nothing for it
to stop against.

```python
# the passage: the far wall, the inside and the near side, in that order
import math
p["wall"] = p.mix("dark", "light", 0.7)
p["body"] = p.mix("dark", "light", 0.45)
rim = [(0.30 + 0.14 * math.cos(math.radians(a)), 0.72 + 0.07 * math.sin(math.radians(a)))
       for a in range(0, 361, 15)]
s.block_in(ellipse(Region(0.16, 0.65, 0.44, 0.79)), "flat", "wall", size=0.03,
           edge="hard")                                        # the far wall
s.block_in(ellipse(Region(0.175, 0.675, 0.425, 0.80)), "flat", "dark", size=0.03,
           edge="hard")                                        # the inside, below it
s.block_in(polygon(rim[:13] + [(0.19, 0.93), (0.41, 0.93)]), "flat", "body", size=0.04,
           edge="hard")                                        # the near side
# goes wrong: nothing says so
s.stroke(rim, "round_hard", "pale", size=0.0085, opacity=0.95, pressure="even")  # an outline
```

---

## A repair under things that are standing on it

Repainting a mass buries every fine mark on it, and those are the expensive ones. The
only approach that has worked across every session is not a mark at all, it is how you
write your passes:

```python
def far_mass():  s.block_in("upper-half", "flat", "shadow", size=0.16)
def near_mass(): s.block_in(span("A4", "H6"), "flat", "mid", size=0.14)
def details():                                   # the things standing on it
    for x in (0.28, 0.46, 0.64):
        s.stroke([(x, 0.66), (x + 0.02, 0.50)], "round_hard", "light", size=0.012)

for layer in (far_mass, near_mass, details):     # fix one, re-run all of them
    layer()
```

**Keep every mass and every near thing in its own named function, in a `prelude.py`
beside the session, and re-run the whole stack in depth order.** The repair goes in at
its own depth and the near things go back on top of it, because they were never a
one-off. That is what back-to-front costs at repair time, and it is cheaper than the
alternative the second time you need it.

**Goes wrong as:** a repair that buries what stands on it — the mass repainted and the
near things never put back, which `report()` names after the pass.

```python
# the passage: the stack laid once, with things standing on the near mass
p["mid"] = p.mix("dark", "light", 0.5)
def far_mass():  s.block_in("upper-half", "flat", "shadow", size=0.16)
def near_mass(): s.block_in(span("A4", "H6"), "flat", "mid", size=0.14)
def details():
    for x in (0.28, 0.46, 0.64):
        s.stroke([(x, 0.66), (x + 0.02, 0.50)], "round_hard", "light", size=0.012)
for layer in (far_mass, near_mass, details):
    layer()
# goes wrong: report() says "earlier details out of sight"
near_mass()                                      # the repair, and nothing put back on it
```

For a repair with nothing standing on it, `s.cover(place, color)` is the whole burying
recipe already mixed — *What you are bad at* in
[`PAINTER.md`](PAINTER.md#what-you-are-bad-at-and-what-to-do-instead) has its clauses.

---

## Where these came from

Every recipe above was taken out of a pass script of a painting in
[`paintings/`](paintings), with the painter's own note on what it replaced; the two
composition entries out of the notes rather than the scripts, which is why they are the
least certain things here. Those scripts are the fuller version of this file: the calls
in the order they were actually made, with the rehearsals that failed described in the
comments above each pass.

**They name their subjects, so the decide-first rule applies to them and not to this
file.** If you chose what to paint before opening this repository, go and read them. If
you have not chosen yet, do not — a named subject chooses for you.
