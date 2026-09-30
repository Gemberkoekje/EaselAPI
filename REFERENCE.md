# Reference: every fact on one page

[`PAINTER.md`](PAINTER.md) teaches the workflow and is the file to read first. This is
the other half of it: the arguments, the units, the defaults, and what each one does —
the things you otherwise have to find inside an essay while you are holding a brush.
The reasons under the rules are in [`PAINTING.md`](PAINTING.md), the procedures in
[`RECIPES.md`](RECIPES.md), and the measured numbers behind them all in
[`CALIBRATION.md`](CALIBRATION.md); this page says what a thing *is*, not how much of it
there is.

Nothing here is a rule about painting. Every rule is in the guide, and a fact looked up
here without the rule beside it is how a painting comes out correct and dead.

---

## Units, which is where the surprises are

| Quantity | Unit |
|---|---|
| A coordinate `(x, y)` | `0..1`, origin **top-left**. `x` is a fraction of the **width**, `y` of the **height** |
| `size` (brush), `feather`, `roughen()`'s `amp` and `step`, `terminator()`'s `margin`, `step` and `least` | a fraction of the canvas's **long side**, whichever way the brush travels |
| `depth`, `inset()`, `overhang` distance | normalised canvas units, the same as a coordinate |
| A radius of `ellipse()` or `blob()` — `rx`, `ry`, `radius` | as a coordinate: a fraction of the **width** across and of the **height** down. One radius sets both, which is an oval on a canvas that is not square — `ellipse(p, 0.05)` is 102 by 76 px at 1024x768 — unless `aspect=s.aspect` is passed, which measures both by the width: 102 by 102 |
| A `ribbon()`'s `width` and `end_width` | as a coordinate, **across the ribbon's own line**: a fraction of the height where it runs level, of the width where it runs upright. `0.05` is 38 px across a level ribbon at 1024x768, 52 across an upright one and 45 at 45 degrees, so one ribbon changes width as it turns |
| `s.circle()`'s `r` | a fraction of the **width**, and the shape is round in pixels; `px=` is the radius in pixels instead |
| An angle | degrees **clockwise from the horizontal, in the `0..1` coordinates**; `y` runs *down*, so `90` is downward. Passes *run* along the angle and a stack *steps* across it. On a canvas that is not square the screen angle is flatter than the number: `direction=-23` lays passes at `-12°` on a 2:1 canvas and `-18°` on 4:3, and `45` runs at `37°` on 4:3. An angle read off the picture does not have to be converted: hand `direction=` the two points instead — `direction=((0.33, 0.01), (0.58, 0.29))` — and it does the `atan2` for you |
| A value | `0..1`, the sRGB luminance `look(values=True)` shows and `palette.value_of` reports |
| A colour | a pigment name, a palette slot you named, `"#rrggbb"`, or an `(r, g, b)` triple |
| A place | a region name, `"D4"`, `"C3:F6"`, a `Region`, a 4-tuple `(x0, y0, x1, y1)`, or a `Polygon` |

**The first two rows are not the same unit.** On a canvas that is not square, a step of
`0.07` down is a different number of pixels from `0.07` across, while a brush at
`size=0.07` is `0.07` of the long side both ways. A radius `r` in `x` is `r * width /
height` in `y`. **What is round in pixels**: a brush, always; `s.circle(place, r)`,
always; an `ellipse()` or a `blob()` given one radius and `aspect=s.aspect`, or its two
radii through `s.px(rx, ry)`. A `ribbon()` has no such form: its width is whatever its
line's direction makes it.

**To draw in pixels**, `s.px(x, y)` is a pixel's place, `(x / width, y / height)`, and
`s.px_size(r)` is a length in pixels as a size, `r` over the long side. A round shape
takes its radius in pixels itself, `s.circle(p, px=r)`; two radii are measured along
the two axes as a point is, so an oval in pixels is `ellipse(p, *s.px(rx, ry))`.

---

## What counts against the budget

| Free | Charged, one per mark |
|---|---|
| `pencil`, `erase`, `mark`, `unmark` | `stroke`, `dab` |
| `dry` | `smudge`, `glaze` — marks like any other |
| `look`, `preview`, `rehearse`, `cost`, `compare`, `prepare` | `block_in`, `sweep`, `scumble`, `cover` — **once per pass**, so one call is ten to thirty |
| `undo` (it removes what was charged) | |
| `sketch(reference, level=, pressure=, areas=)` — it lays pencil, and is an assisted mode the log records; `areas=` lays some of the numbered masses rather than all of them | |

`s.stroke_count` is the tally, `s.spent` and `s.remaining` are it against a
`Session(budget=...)`, and `s.budget_line()` prints both. The first five marks whose
`note` contains `signature` are free; every one after that is charged. A mark that laid
no paint is charged like one that did, and the check after the pass names it
(`landed nothing:`, under *Looking, planning, measuring*). Inside a
rehearsed pass — `s.scratch()`, or `easel run --rehearse` — all three **continue the
painting's own numbers**; what the copy itself laid is `s.history.stroke_count`.

**Before a mass, not after**: `s.cost(plan)` walks the passes without laying them and
returns the number, and `s.cost_line(plan)` says *why* it is that number.

---

## The verbs

| Call | Lays | Costs |
|---|---|---|
| `stroke(points, brush, color, ...)` | one mark along a path | 1 |
| `dab(x, y, brush, color, press=1)` | one mark at a point; `press` stamps it again | 1 |
| `smudge(edge, size=0.02)` | drags what is on the canvas, along a path **or a shape's own outline** | 1 |
| `glaze(points, color, opacity=0.18, to_value=None)` | a thin film that adds no height; `to_value=` solves for the opacity that lands the passage under it on a value, the way `at_value` solves a mixture | 1 |
| `block_in(place, ...)` | a mass, as overlapping passes | one per pass |
| `sweep(edge, ..., into=, depth=)` | a mass, as passes along its boundary stepped inward | one per pass |
| `scumble(band, a, b, n=8)` | a soft passage, `n` passes stepping between two colours | `n` |
| `cover(place, color)` | a repair, with every clause of the burying recipe set | one per pass |
| `pencil(points)` | graphite under the paint. A list of points is splined, which rounds every corner and bows a closed outline outward; a shape handed over whole — a `Polygon`, a `Region`, `"D4"` — is drawn as its own outline, corners kept, and so is one handed to `guide()` | 0 |
| `erase(region=None)` | takes **both** drawings out — the graphite and the `guide()` overlay | 0 |
| `dry(amount=1.0, region=None)` | takes the wetness out so new paint covers rather than mixes | 0 |

### Which verb takes which hold

Where the paint is allowed to land, and whether the brush is allowed to run dry, are
the same two questions on every verb that lays paint — so every one of them answers
both. `clip=` is a place, or a list of places, outside which none of the call's paint
may land; `solid=` is the pair `load=1.0, load_falloff=0.0`; `edge=` is what the call
does at the boundary of the place it is filling.

| Verb | `clip` | `solid` | `edge` |
|---|---|---|---|
| `stroke()` | yes | yes | — |
| `dab()` | yes | yes | — |
| `smudge()` | yes | yes | the path it drags along, positional |
| `glaze()` | yes | yes | — |
| `block_in()` | yes | yes | `ragged` `clean` `hard` |
| `sweep()` | yes | yes | the boundary it follows, positional |
| `scumble()` | yes | yes | `ragged` `hard` |
| `cover()` | yes | already solid | `ragged` `clean` `hard` |

`edge="hard"` **is** a clip, pointed at the place the call is filling; `clip=` points
one somewhere else. A call given both is held by both, and the paint lands where they
agree. A scumble has no contour to draw, so it has no `"clean"`; `cover` lays
`load=1.0, load_falloff=0.0` already, because that pair is the burying recipe, and
`scumble` lays it too — so `solid=` is still taken there and no longer moves anything.

**Every hold breaks its edge inward** (0.7.0). Over `feather=` — `0.002` of the long
side left off, two pixels at 1024 — the canvas's own tooth decides how much of the edge
takes paint, the way it does for a starving brush: crisp where the weave is high, broken
where it is low, and nothing past the drawn line. `feather=0` cuts the edge on the line,
which is what every hold was before 0.7.0 and what a line ruled on purpose wants. Every
verb that takes `clip=` takes `feather=`. On a shape narrower than four feathers the
break reaches a quarter of its width and no further, so a thin shape keeps its body. A
side lying on the canvas frame is not an edge and never breaks, and a saved mark replays
at the feather it was laid with — one saved before 0.7.0 at `0`.

---

## The arguments that mean something particular

| Argument | Default | What it does |
|---|---|---|
| `density` | `1.0` | how close the passes run: `size × (1 - 0.45 × density)` apart. **Spacing, not coverage** |
| `solid` (`block_in`, `stroke`, `sweep`, `scumble`) | `False` | `load=1.0, load_falloff=0.0`, so no pass runs dry along its length. A solid mass still lands a little short of its mixture on any brush but a round one, and an oriented tip under four pixels wide lands the ground and says so: *What a solid mass actually lands at* in `CALIBRATION.md`. **On a banded `scumble` it is already the default** and the argument is kept only because scripts type it |
| `overhang` (`block_in`) | `0.35` box, `0` shape | how far each pass runs **past the ends of the pass**, in brush widths. It moves the ends only, never the sides, and which two edges are the ends turns with `direction`. A shape defaults to `0` because its outline is the drawing; a rectangle stopping short of its corners reads as cropped |
| `overhang` (`scumble`) | `0.35` | the same measure as `block_in`'s, but flat — `scumble` does not vary its default between a box and a shape |
| `overhang` (`cover`, under `edge="ragged"`) | `1.0` | one full brush width, so a repair's ends sit outside the mistake it is covering rather than stopping at its edge. Under `cover`'s own default, `"hard"`, it is the `2.0` below, and under `"clean"` it is `0` |
| `overhang` (`block_in`, `cover`, under `edge="hard"`) | `2.0` | nothing can cross the mask, so the only thing left for an overhang to do is carry every pass end up to the outline. **Two and not one**: `pressure="taper"` reaches zero one brush out, so at one brush every pass arrived at the outline at part pressure and a round tip at part *width*, leaving `0.85%`–`3.26%` of the strip inside a sloping outline bare against `0.055%`–`0.33%` at two. It costs dabs and not strokes, so `cost()` quotes the same number. `scumble` keeps its own `0.35` under `"hard"` and needs no more: its passes are `pressure="even"` already, and it leaves `0.000%` of that strip bare at every overhang tried |
| `edge` | `"ragged"` | `"clean"` insets the fill half a brush and draws the contour along the inset outline — along its **own edges**, not a spline through its corners, which bowed 65px off a four-cornered tower. The contour does not wander: the line is the drawing. On a mass whose shorter extent is under four brushes it says so, and so does `preview`. `"hard"` masks every dab to the outline instead — no inset, no contour pass, no extra stroke, and no paint outside the shape: the one setting that ends a pass on a line rather than on its own tip. `overhang` defaults to **two** brushes there, since nothing can cross the outline and the only thing it still does is carry every pass end up to it. `cover()` takes all three and **defaults to `"hard"`** (0.6.0): a burial run a brush past its place repainted four times the place on a graded or worked passage, against half of it held — *A burial and the place it was handed* in `CALIBRATION.md`. `scumble()` takes `"hard"` — a passage has no contour to draw, and a band crossed at an angle is the place a mass lands furthest outside itself |
| `direction` | left off: `"horizontal"` | `"horizontal"`, `"vertical"`, `"diagonal"`, `"cross"`, `"axis"` (the place's own), degrees clockwise from horizontal, a **line of two points** to run along, or a sequence of any of those. A pair of points is a line; a pair of numbers is two angles. **A sequence lays a full stack per angle and is priced as the sum**; `"cross"` is two angles and the affordable way to break a comb. On `scumble`, also `"inward"`. Left off on a shape, `block_in` and `cost` say so when horizontal passes cost over 2.5× `"axis"`; given a sequence, when it costs over 2.5× its own dearest angle. **Where the stack starts** is below |
| `pressure` | `"taper"` | see *Pressure* below |
| `opacity` | the brush's | per-dab strength. Dabs overlap, so a low one accumulates back toward full colour |
| `load` | the brush's; `1.0` on a banded `scumble` and on `cover` | how much paint the brush carries. It spends itself along the stroke, and under `0.9` of it the brush drags dry: what it lays breaks into streaks along its travel, and a `bristle`'s comb runs out bristle by bristle |
| `load_falloff` | the brush's; `0.0` on `scumble` and `cover` | how fast it spends. `0` never runs dry. A passage and a repair are many wide passes laid over each other, and a brush running dry along one of them prints a stripe the passes after it do not close — so a band and a repair lay the pair themselves, and naming either beside the call still wins |
| `size` | the brush's | tip diameter, as a fraction of the canvas long side. On **either** direction of `scumble`, left off, it is picked from that verb's own step: `3 × depth / n` inward, `3 × extent / n` on a band. Named too narrow, both say so — and on a shape whose width varies along the stepping axis, so that the brush is wider than the passes at one end, the band case says so too, naming both lengths |
| `wander` (sweep) | `True` | whether each pass wanders off the offset curve, so a stack is not parallel rules. A **single** pass has no parallel to break and the wander only moves it off the line drawn; off for the contour of `edge="clean"` |
| `tip_wobble` | `0.0` | a round tip's own silhouette, redrawn per mark. `0.35` a brush set down once, `0.7`+ a clot |
| `press` | `1` | for a one-point mark, how many times to stamp it. One mark either way |
| `glaze` (`stroke`) | `False` | lay colour without building paint height. `s.glaze(points, color)` is the verb; a mass cannot be laid as one |
| `smooth` | `True` | fit a spline through the points; off gives hard corners |
| `into` (sweep) | — | which side the mass is on: a compass word, degrees, or a point inside it. A closed edge needs none |
| `depth` (sweep) | `0.2` | how far into the mass to sweep, in canvas units |
| `cross` (sweep) | `None` | a second set of passes leaning this many degrees off the boundary. 20–30 is usual |
| `passes` (sweep) | `None` | pin the count instead of letting the brush decide |
| `closed` (sweep) | inferred | treat the edge as a loop. Inferred when the last point is the first; say it when the loop is nearly closed and you meant it to be |
| `clip` (every verb that lays paint) | `None` | a place — a shape, a region, a name, a run of points — outside which none of the call's paint lands. A **list** of places holds it inside all of them at once: the paint lands where they agree. `block_in(edge="hard")` is this same clip pointed at the mass's own outline |
| `feather` (wherever `clip` or `edge="hard"` holds the paint) | `0.002` held, nothing otherwise | how far inside the outline the held edge breaks, as a fraction of the long side: two pixels at 1024, three at 1440, where it bites at the export's own pixels as it does at 1024, measured. Between the line and that depth the tooth decides; past the line nothing lands. `0` cuts it on the line. **It breaks an edge against the tooth; it does not soften one** — every hold of the call, the silhouette's included, and wider than the default the break reads as fur: to soften a terminator, lay a join along it (`terminator()`). Refused on a call that holds nothing — a ragged edge is broken by its brush — except `0`, so a helper can pass it on every mark |
| `dry_first` (`cover`) | `True` | dry the area before covering it. Free, and part of the burying recipe: wet paint mixes with what you are trying to lose |
| `share` (cost) | `0.25` | how much of the remaining budget one plan may take before it warns. `0` never warns |
| `note` | `""` | a line in the log, for your own benefit |

Any **brush field** is also an override on any painting call, per mark and per mass:
`s.block_in(place, "flat", "dark", hardness=0.9, jitter=0.05)`.

### Where a stack of passes starts

Passes stack across the place, and reading the call does not tell you from which side.
It matters whenever the passes differ from each other — a `scumble`'s two colours, a
`pressure` list, a `density` that leaves the ground showing at one end. Measured on a
wider-than-tall place, `flat` at `size=0.08`, five passes:

| `direction` | the **first** pass — where `color_a` lands |
|---|---|
| `0`, `"horizontal"`, `"axis"` on a wide place | along the **top** edge |
| `90`, `"vertical"` | along the **right** edge |
| `45` | the upper **right** corner |

So `scumble(place, a, b, direction=90)` puts `a` on the right and `b` on the left,
which is the opposite of what reading it left-to-right suggests. A `Polygon` behaves
the same as a `Region`. If a passage comes back lit on the wrong side, this is why, and
swapping the two colours is the fix.

Consecutive passes run in opposite directions (see *Pressure*), so this is the first
pass's side and not every pass's.

---

## The brushes

| Preset | Tip | `size` | `opacity` | `hardness` | `load` | falloff | For |
|---|---|---|---|---|---|---|---|
| `bristle` | bristle | `0.11` | `0.88` | `0.65` | `0.9` | `0.55` | the workhorse: broken, streaky, alive |
| `flat` | flat | `0.10` | `0.90` | `0.75` | `1.0` | `0.60` | masses, chisel edges, planes |
| `knife` | knife | `0.09` | `1.00` | `0.97` | `1.0` | `1.10` | thick slabs with a hard edge; drags what it crosses |
| `round_soft` | round | `0.06` | `0.75` | `0.20` | `1.0` | `0.35` | blending and soft edges; above `size~0.05` it airbrushes |
| `round_hard` | round | `0.045` | `0.95` | `0.85` | `1.0` | `0.50` | deliberate marks, accents, small shapes |
| `liner` | round | `0.005` | `0.95` | `1.00` | `1.0` | `0.18` | fine lines at feature scale; no jitter, holds its load |
| `smudge` | round | `0.07` | `0.60` | `0.25` | `1.0` | `0.00` | carries no paint; moves what is already there. **The `smudge()` verb passes `0.02`** unless you name a size — this row is the preset a `stroke()` would get |

Every other `Brush` field, with its default: `spacing 0.12`, `jitter 0.02`,
`size_jitter 0.06`, `angle_follow True`, `angle 0.0`, `aspect 1.0`, `wetness 0.85`,
`thickness_gain 0.5`, `smudge 0.0`, `texture_sensitivity 0.6`, `bristle_count 0`
(derive it from the size), `bristle_pitch 0.005`, `bristle_seed 0`, `tip_wobble 0.0`.
`brush("flat").with_(size=0.2)` makes a variant; `easel brushes` prints the box.

---

## Pressure

`"taper"` (the default), `"press_in"`, `"lift_off"`, `"even"`, `"swell"`, `"dab"` — or a
number, or a list interpolated along the stroke.

Consecutive passes of a mass run in **opposite** directions, so that a stack does not
stack all its run-out along one edge. The pressure profile does not go with them: a
list, or an asymmetric named profile, is read in **canvas order** on every pass, so
`pressure=[0.0, 1.0]` across a `block_in`, `scumble` or `sweep` lands light at one side
of the place and heavy at the other, once, rather than alternating.

| Tip family | What pressure changes |
|---|---|
| `round_soft`, `round_hard`, `liner` | **width and paint.** `size` is the width at full pressure; a light touch keeps about a third of it, never thinner than about a pixel and a half |
| `flat`, `bristle`, `knife` | **paint only.** The chisel keeps the width you asked for, because that width is the mass it lays — and a short hand-laid mark given a list says so, since a list on a short chisel mark can only have been asking for a taper |

---

## Places

```python
region("upper-band")     # all, canvas, center, inner,
                         # top, bottom, left, right,
                         # top-left, top-right, bottom-left, bottom-right,
                         # upper-left, upper-right, lower-left, lower-right,
                         # upper-half, lower-half, left-half, right-half,
                         # upper-band, middle-band, lower-band
cell("D4")               # the A–H by 1–8 grid look(grid=True) draws
span("C3", "F6")         # the rectangle from one cell to another, both included
horizon(0.4)             # a thin band at that height
below(r, 0.15)   above(r, 0.15)   left_of(r, 0.15)   right_of(r, 0.15)
between(a, b)            # the gap between two places
thirds()   golden()      # the x and y lines, to hang a composition on
r.point(u, v)  r.inset(a)  r.scaled(f, about=None)  r.shifted(dx, dy)  r.split_h(n)  r.split_v(n)
```

**What each name actually covers.** `top`, `bottom`, `left`, `right` and `center` are
cells of a 3x3 -- so `bottom` is a **ninth** of the canvas, not the bottom third, and a
painter who reaches for it to mean *the foreground* gets the middle of it. The
full-width places are `lower-band`, `lower-half` and `middle-band`.

| `region(...)` | x | y |
|---|---|---|
| `all` | `0.000`-`1.000` | `0.000`-`1.000` |
| `canvas` | `0.000`-`1.000` | `0.000`-`1.000` |
| `top-left` | `0.000`-`0.333` | `0.000`-`0.333` |
| `top` | `0.333`-`0.667` | `0.000`-`0.333` |
| `top-right` | `0.667`-`1.000` | `0.000`-`0.333` |
| `left` | `0.000`-`0.333` | `0.333`-`0.667` |
| `center` | `0.333`-`0.667` | `0.333`-`0.667` |
| `right` | `0.667`-`1.000` | `0.333`-`0.667` |
| `bottom-left` | `0.000`-`0.333` | `0.667`-`1.000` |
| `bottom` | `0.333`-`0.667` | `0.667`-`1.000` |
| `bottom-right` | `0.667`-`1.000` | `0.667`-`1.000` |
| `upper-half` | `0.000`-`1.000` | `0.000`-`0.500` |
| `lower-half` | `0.000`-`1.000` | `0.500`-`1.000` |
| `left-half` | `0.000`-`0.500` | `0.000`-`1.000` |
| `right-half` | `0.500`-`1.000` | `0.000`-`1.000` |
| `upper-left` | `0.000`-`0.500` | `0.000`-`0.500` |
| `upper-right` | `0.500`-`1.000` | `0.000`-`0.500` |
| `lower-left` | `0.000`-`0.500` | `0.500`-`1.000` |
| `lower-right` | `0.500`-`1.000` | `0.500`-`1.000` |
| `middle-band` | `0.000`-`1.000` | `0.333`-`0.667` |
| `upper-band` | `0.000`-`1.000` | `0.000`-`0.400` |
| `lower-band` | `0.000`-`1.000` | `0.600`-`1.000` |
| `inner` | `0.120`-`0.880` | `0.120`-`0.880` |

Any of them takes hyphens or underscores, and a `Region` prints its own box, so
`print(region("bottom"))` answers this question too.

## Shapes

```python
polygon(points, name="")               # an outline you already have
ellipse(place, rx=None, ry=None, rotate=0, steps=48, aspect=None, name="")
blob(place, radius=None, ry=None, wobble=0.22, points=15, seed=0, rotate=0,
     aspect=None, name="")
hull(places, name="")                  # the mass around some points
ribbon(places, width, end_width=None, smooth=True, name="")   # a mass along a line
roughen(shape, amp=0.006, step=0.008, seed=0, calm=None, aspect=None, name="")
                                       # an outline walked off its own line
union(a, b, ..., resolution=1024, name="")     # one silhouette round overlapping shapes
terminator(outline, inside, margin=0.004, step=0.002, least=0.02, aspect=None)
                                       # the runs of one outline inside another: paths
letter_paths(text, place, cap=0.04, slant=0, seed=None, aspect=None)
                                       # a single-stroke font's paths, placed: paths
s.circle(place, r, wobble=0, points=15, seed=0, rotate=0, steps=48, name="", px=None)
                                       # round in *pixels* on any canvas; px= is its
                                       # radius in pixels, in place of r
shape.inset(a)  shape.smooth(2)  shape.scaled(f, about=None)  shape.shifted(dx, dy)
shape.box  shape.area  shape.axis  shape.center  shape.closed
shape.contains(x, y)                   # is this mark inside the mass?
shape.inside(xs, ys)                   # ...and the same question for many at once
group(a, b, ...)                       # shapes, regions and points, moved as one
g.shifted(dx, dy)  g.scaled(f, about=None)  g.shapes  g.bounds  g.center
```

`roughen()` is for an outline nobody ruled — rock, a shore, a torn edge. It cuts every
side into steps `step` apart and walks each off its line by a wander that keeps most of
itself from one step to the next, about `amp` either side; the same `seed` is the same
outline. Nothing on the canvas frame moves. `calm=` stills the wander where something
stands on the outline — a place, a point, a list of them, or a function `calm(x, y)`
returning `0` to `1` — and `aspect=s.aspect` makes a step the same distance across as
down. Handed an open run of points rather than a shape, it roughens that stretch alone
and keeps its two ends where they were, so the stretch still meets the rest.

`terminator()` is where a lit form turns. For a silhouette laid as copies of itself
shifted away from the light and held to it, each copy's outline, where it lies inside
the silhouette and `margin` off its edge, is the line between two zones; it comes back
as runs of points, and a stroke along each at the value halfway between the zones is
the join — *A silhouette lit from one side* in [`RECIPES.md`](RECIPES.md). A run
shorter than `least` is left out. `aspect=s.aspect` makes the three distances the same
across as down.

`letter_paths()` is lettering as paths: each letter one to three strokes of a
single-stroke font, placed with its first baseline starting at `place` (a region's bottom
left, `cap` its height), `cap` a capital's height as a fraction of the canvas's
**height**, `slant` in degrees. `seed` is a hand — each letter's size, lean, points and
baseline varied, the same seed the same hand — and `None` the font as drawn. Pass
`aspect=s.aspect`. It lays nothing: `len()` of what comes back is the price in strokes,
and `LETTERS` is every character it draws.

`group()` is for a drawing made of parts, redrawn by moving the parts. `shifted()` and
`scaled()` move every part the same way — `about` is the point that stays put, a point or
a place whose middle it is, and left out it is the middle of the box round them all — and
a group unpacks into its parts, points coming back as points:
`head, jaw, eye = group(head, jaw, eye).scaled(1.3, about=s.px(300, 266))`.
`shape.scaled(f, about=)` is the same for one shape. A group is not a place: block in,
hold and draw its parts one at a time.

A shape goes anywhere a region goes. `shape.box` is the rectangle a mass is *priced*
on — worth looking at before blocking in anything long and curved. It is a `Region`,
with `.x0/.y0/.x1/.y1` and `.width/.height/.center`, and it **unpacks**:
`x0, y0, x1, y1 = shape.box`, the same four numbers as `shape.bounds`.

---

## Colour

Eleven pigments and no black: `titanium_white`, `lemon_yellow`, `cadmium_yellow`,
`yellow_ochre`, `cadmium_red`, `alizarin`, `burnt_sienna`, `burnt_umber`, `ultramarine`,
`cerulean`, `viridian`. (`white`, `yellow`, `ochre`, `red`, `blue`, `umber` and `sienna`
are accepted as short names for seven of them.)

```python
p = s.palette
p["shadow"] = p.mix("ultramarine", "burnt_umber", ratio=0.45)  # named, and it persists
p.mix_many([a, b, c], weights=[2, 1, 1])   # several at once; equal weights left off
p.complement_grey(c, b, ratio=0.5)         # a lively neutral: a colour and its complement
p.tint(c, amount=0.3)   p.shade(c, amount=0.3)   p.desaturate(c, amount=0.3)
p.at_value(base, 0.62, light="titanium_white", dark=None, steps=24)
                            # that colour, moved to that value, from either side
                            # under the default dark's 0.137, the error names burnt umber's 0.128
p.value_of(c)               # what look(values=True) will show
p.chroma_of(c)              # how coloured: 0 for a grey, 0.20 for cadmium_red
p.darkest_value             # 0.128, burnt umber alone: the floor of the box
```

A colour is a pigment name, a mixed slot's name, a `#rrggbb` string, an `(r, g, b)`
triple **read as sRGB, the same as the hex string is**, or a `float32` array the engine
made, which is linear light and passes through as itself. The triple is the trap: a
colour read off the canvas and handed back as one comes back darker — a `toned_grey`
ground reads `0.53`, its own mean as a triple reads `0.25`. To match what is already
there, ask for it and pass it straight on:

```python
p["sky_here"] = s.sample(halo_ring)     # the engine's own array, no conversion
```

**`sample` averages what is in the place it is given**, so to measure a *mass* hand it
the mass and not the cell the mass sits in: a small mass planned at `0.30` on a field
at `0.50` reads `0.501` by its cell and `0.327` by its own shape.

`sample` reads the **paint**. `sample(place, rendered=True)` reads the *view* of it —
the relief and any graphite the paint has not buried — so the two can be put side by
side in one line instead of believed. Measured, they agree over a mass to within
`0.001`: see `CALIBRATION.md`, *The paint and the view of it*. `compare()` reports the
paint too, and its table now says so.

`chroma_of` is `value_of`'s counterpart for *how coloured*: the Oklab chroma, `0` for
any grey, about `0.02` for the grounds and `burnt_umber`, `0.12` for `yellow_ochre`,
`0.20` for `cadmium_red`. A solid plane reads back at the mixture's chroma or a little
under, never above.

Grounds for `Session(ground=...)`: `white`, `warm_white`, `toned_grey`,
`toned_warm_grey`, `cool_grey`, `umber_wash`, `burnt_sienna` — or any colour.
Textures: `smooth`, `linen`, `rough`.

---

## Looking, planning, measuring

```python
s.look(grid=, values=, region=, reference=, diff=, scale=, sketch=, marks=, impasto=,
       path=)                                   # the last three are on unless turned off;
                                                # sketch=False hides the guides as well
s.thumbnail(places=None, size=192, path=)       # the arrangement, flat and small:
                                                # {place: value or colour}, a pair
                                                # (value, clip) held inside the clip; left
                                                # off, the plan's places and every mass laid
s.preview(plan, reference=, region=, grid=, values=, scale=, path=)   # where a mark goes
s.rehearse(plan, reference=, region=, grid=, values=, scale=, path=, vary=)
                                                # what it looks like -- and with
                                                # vary={"size": [0.02, 0.05, 0.08]},
                                                # one labelled panel per setting, in
                                                # place, in one image. At most twelve:
                                                # two arguments multiply
s.rehearse_each([plan, fn], reference=, region=, grid=, values=, scale=, path=,
                labels=)                        # versions of a pass, each on a copy of
                                                # its own, side by side in one sheet: a
                                                # plan, or a function handed the copy
s.cost(plan, share=0.25)   s.cost_line(plan)    # what it charges, and why; share= is
                                                # how much of what is left it may eat
s.paint(plan, note="")                          # the same plan, now paid for
s.compare("ref.jpg", region=, threshold=0.10, near=0.01, path=)
                                                # per-cell value of both, and the miss
s.compare({place: value, ...})                  # ...against your own value plan, and
                                                # the pairs it puts within 0.10: do they touch?
s.compare(s.plan())                             # ...against the plan this session holds
s.plan(why=, values=, lightest=, subject_share=, bands=, ground=, key=, clear=False)
                                                # what you decided before painting, where
                                                # the check can hold you to it
s.sample(place=None, rendered=False)            # the colour already there, to paint with
s.report(since=None, subject_share=None)        # the post-pass check, read off the log
                                                # and measured off the canvas: values,
                                                # edges, ground, pencil
s.checklist(subject_share=None)                 # the closing checklist, answered -- and
                                                # the three questions it cannot answer
s.notices(since=None)   s.explain(code)         # what the calls themselves said, and why
s.reports()                                     # what each `easel run` printed after its
                                                # pass, rehearsals included
s.prepare("ref.jpg", level="coarse", min_share=0.004, path=)
                                                # 7 masses; "medium" 20, "fine" 40
s.log(last=10)                                  # last=10_000 for the whole record.
                                                # Log records, as undo(n) and
                                                # replay(upto=) count: a dry or a
                                                # pencil line is one and is free. A
                                                # colour is named as the palette names
                                                # it -- your slot, or the pigment
s.export("painting.png", impasto=True, sketch=True)
s.timelapse_gif("p.gif", fps=8.0, every=1, scale=None, from_log=False)
                                                # from_log rebuilds the frames by
                                                # replaying, at any size
s.contact_sheet("sheet.png", columns=6)
```

A **plan** is one object all four planning verbs read: a list whose entries are a path,
a dict of `stroke` arguments, a dict with `shape=` and any `block_in` argument, a dict
with `edge=` and any `sweep` argument, a passage — `band=`, `color_a=`, `color_b=` and
any `scumble` argument — or a burial, `cover=` and any `cover` argument. A bare place or
shape is a mass. A film is a mark, with the glaze verb's brush and opacity written out
because an entry takes a stroke's, and `to_value=` stays with the verb:

```python
{"points": band, "glaze": True, "brush": "round_soft", "color": "warm", "opacity": 0.18}
                                                # lays what s.glaze(band, "warm") lays
```

So **a whole pass is a plan** — its masses, passages, marks and films in the order it
lays them — and can be priced, previewed and rehearsed, `vary=` and all, before a
stroke of it is paid for. **Versions of one pass** go side by side with
`s.rehearse_each([...])`: each is a plan, or a function that paints on the copy it is
handed, as a script would — each on a copy of its own, seeded as the next marks of the
painting, so the one chosen off the sheet lands as its panel shows it. Every panel is
labelled with its version — a function's name, a plan's place in the list, or
`labels=` — and the strokes it laid.

**`s.thumbnail()` is the arrangement before any of it is paid for** — the notan, where a
silhouette reads or does not. Each place is filled flat at its value, or at a colour's
value, in the order given, later over earlier, on the ground's own value, in greyscale,
192 pixels on its long side unless `size=` says otherwise. A pair holds a place inside a
clip, as a mass's `clip=` holds its paint — `{rim: ("lit", body)}` fills only where the
two agree — and a list of places holds it inside all of them. **Left off, it draws the
plan's places, and over them every mass the painting has laid**: each `block_in`,
`cover`, `scumble` and `sweep` at its colour's value — a passage halfway between its two
— held as it was held, in the order laid, read off the log, whose first record of every
mass call keeps the place it filled. A mark, a film and the drawing are not masses and are
not in it. A mass laid by a release before 0.8.0 kept no place and is left out, and the
shell and the server say how many. Free, as a preview is: nothing painted, logged or
charged, and the stream untouched.

```python
s.thumbnail({body: 0.12})                        # does the silhouette read?
s.thumbnail({body: "shade", rim: ("lit", body)}, size=128)
```

Looks are written to `out_dir` and numbered `look_001.png`, `preview_001.png`,
`compare_001.png`, `rehearse_001.png`, `thumbnail_001.png` upward — each kind counting
on its own, and each taking the next free name **in the directory** rather than the next
number in the session. So two sessions sharing an `out_dir` do not write over each
other, and a painting reopened between `easel run` calls carries on where the directory
left off. Pass `path=` to name a file yourself.

`report()` is the check `easel run` prints beside the budget line after every pass:
**ten rules** read off the log and the canvas, and under them the **standing lines**,
which are measurements rather than findings. A *long* mark is at least twice as long as
its brush is wide, and a mark is *laid by hand* when no mass verb laid it.

| It says | when |
|---|---|
| *one brush at one size for a whole pass reads as one tool* | every mark of a pass of `10` or more, from two or more calls, is one brush at one size |
| *a stack of bars unless the subject runs that way* | `12` or more long marks lie within `6` degrees of one angle, from two or more calls, and are most of the pass's long marks, a `scumble` counting as one. **Said once, and again only when the picture has picked up a long mark `30` degrees off the bars it was said about**; `--check`, which is asked for rather than printed at you, says it whenever it is true |
| *a graded passage comes back as bars* | `5` or more long parallel marks at `3` or more colours, in one run with no gap wider than `4` brushes and **each laid over the next rather than beside it** — two neighbours sharing under `30%` of the shorter one's reach along the stack break it, as glints do — their colours turning at most once, are stepped further apart than half the narrowest brush laying them. A brush that lays no colour of its own is not counted |
| *a comb that small is four streaks with gaps, not a brush* | `3` or more marks are laid with a `bristle` under `size=0.025` **at a load over `0.6`**, because below that the comb's gaps are the mark. A pass's rule: over a whole painting it says nothing, since what it asks for is a brush for the next marks |
| *detail before the masses are down* | `8` or more marks under `size=0.02` fall inside the painting's first `60` |
| *pressure changes a chisel's paint, not its width* | a mark laid by hand with a `flat`, a `bristle` or a `knife` is given a pressure list and is no more than `4` times as long as it is wide |
| *that is one disc printed 5 times* | `3` or more round-tip marks are laid by hand under `size=0.02` at `tip_wobble=0`, each no more than `7` times as long as it is wide: the tip's silhouette rather than a line. Over a whole painting, only where `3` or more sit within `0.06` of one another, a signature left out, with where each group is |
| *a daisy, or a wagon wheel* | `5` or more long marks laid by hand leave one point with no gap wider than `90` degrees in the circle of their directions |
| *a loop's signature* | `6` or more consecutive marks laid by hand, of one brush at one length or a strict ramp of lengths, are evenly spaced on a line and further apart than their own width |
| *this pass took 4 earlier details out of sight* | `3` or more earlier small or `subject` marks, showing as the pass opened, are left at under half their contrast by a glaze or a mass's passes. It reads the canvas as the pass opened, which `easel run` keeps, and so does the `report()` before it in a script that reports after every pass |

**A finding that counts marks names them**, on a line under it: the script lines they
were laid from, as the dearest calls are named — *laid at p05.py:58 (lay_accents), :62,
:72 (lay_edges) -- records 174, 176, 179* — or only the records, for marks laid in
another process, since which line laid a mark is known to the process that ran the
script.

| Line | Measures | Said |
|---|---|---|
| `landed nothing:` | the marks that carried under one unit of paint — *NO PAINT LANDED* in `easel log` — each by the line that laid it, a mass call's by how many of its passes, with the cause its record shows: half its path or more outside its clip, a round dab under the size its press lands from, an oriented tip under four pixels, a bristle loaded under `0.5` | only when a pass laid one: *landed nothing: the dab at p06.py:39 (a round tip under its cliff at press=1); 6 passes of the block_in at p05.py:12 (outside its clip)* |
| `plan:`, `lightest:` | the canvas against what the plan declared: *What the plan changes*, below | once a plan declares values, or a lightest place |
| `subject:` | the subject's share of the marks so far, against `subject_share` if given | wherever a mark is noted `subject` |
| `values:` | the 5th to 95th percentile of the values view against what the palette reaches, and the three clusters it splits into | after every pass; it says so when the range stays on one side of the box's middle or two clusters sit under `0.10` apart — or, under a declared `key=`, whether the picture has kept it |
| `edges:` | the share of the picture's edges under `2.5` px wide | after every pass |
| `ground:` | the share of the canvas that is **still bare ground** | after every pass; it says so under `0.5%` |
| `pencil:` | graphite still showing | left off once there is none |
| `boxes:`, `unspent:` | the masses laid in a rectangle, and what is left of the budget | in the closing checklist only |

Their thresholds are under *The measurement lines, on the finished canvases* in
`CALIBRATION.md`. All of them count the painting behind a rehearsal copy, not the copy's
own log, and everything read off the canvas is left off a counted copy, which has laid
no paint of its own.

`since=` is the log index the pass began at (`len(s.history.records)` before it); left
off, the whole painting, which is also what `s.checklist()` and `easel check` read. Two
more rules need the shape and fire at the call: a shaped `block_in` with `direction` left
off costing over 2.5× its axis (or a sequence costing over 2.5× its own dearest angle),
and a round tip blocking in a **feature** — a shape under a tenth of the canvas across —
that is less than four of its brushes wide. Over that width the same brush is a mass
with a soft silhouette, which is what a round tip is for.

### What the plan changes

`s.plan(...)` is what a painter is told to settle before the first mark, written where
the engine can see it. `Session(budget=)` was the first of these declarations; these are
the rest. Every one of them changes a line of the check, and two of them **replace a
standing warning with a number** — which is the point: a rule that concedes *unless the
subject runs that way* cannot tell whether the subject does, and the painter can.

| Declared | What the check does with it |
|---|---|
| `values={place: 0.70, ...}` | at registration, on the empty canvas, `plan-pairs` names the pairs planned within `0.10` **that meet**. After every pass: `plan: 5 of 6 places inside 0.10; halo +0.14`, the sign being the canvas minus the plan. A place reads by its **median** — what most of it reads, so an eye inside a planned plane does not move what the plane reads — and a place the line names that has a tenth of itself or more over `0.15` from that median says so: `halo +0.14 (18% of it lighter by more than 0.15)`. `compare(s.plan())` reads places the same way |
| `lightest=place` | `lightest: lamp reads 0.49 as a place, 0.59 at its brightest twentieth, the lightest of the 4 places planned` — or which place took the light instead, and by how much. A place the line names that is split says so in brackets, as on `plan:`: `lantern reads 0.51 as a place (10% of it darker by more than 0.15)`. The places are ranked by their medians; the named light is also read at its 95th percentile, because a light is often a small bright part of a place that is mostly something else. Where the two numbers are far apart, plan the lit part as a place of its own, at the value that place will read — not the value its mixture was mixed at |
| `subject_share=0.40` | the `subject:` line always carries *against 40% planned*, with no `report(subject_share=)` to remember. It is the one declaration that was reachable before and unreachable from a shell |
| `bands="subject"` | the stack-of-bars line stops warning and counts: *bands declared as the subject: 14 long marks run within 6 degrees of horizontal, and nothing crosses them yet* |
| `ground="buried"` | the ground line prints its number and says *buried, as the plan says* instead of asking for some back |
| `key="low"` or `"high"` | the `values:` line stops saying *no clear light* (or *no clear dark*) and says `low-key, as the plan says -- nothing above 0.35, under the box's middle 0.54` — or, once the top twentieth rises past the middle, by how much the picture has left its key. Its clusters are printed and not judged: a key compresses the range, and no gap has been measured for one yet. Under `"low"`, with `lightest=` named, it asks whether that light stands clear of everything else — the canvas outside its place: `lantern stands clear -- 0.59 at its brightest twentieth against 0.40 for everything else, 0.19 over`, or that it does not, under `0.10`. A high-key picture's light has no room above the rest to stand clear in, so there it is not asked |
| `why="..."` | nothing measures it. It is quoted back at the end, which is the moment it is worth reading again |
| nothing | nothing is said at the first stroke, and no line nags for a plan. What a declaration buys is the lines above; what it costs is writing it down |

Called again it **changes what it is given and keeps the rest**, so the values can be
declared in a `prelude.py` and the lightest place added from a pass; pass the empty
version of a field (`values={}`, `bands=""`) to clear it, or `clear=True` to start
again. Re-registering the same plan says nothing the second time, which is what lets a
`prelude.py` run before every pass without `plan-pairs` becoming a thing printed once a
pass. From a shell it is `easel plan p.easel --value 'A1:H3=0.70' --bands subject --key low`,
whose places are names rather than shapes, and `easel new` writes a `prelude.py`
holding the call.

The plan is saved in the `.easel` file, and lives beside `history.records` and never in
it, for the reason the notices do — see *What the tool will tell you* below. A 0.5.0 file
has no plan and opens with none.

---

## What the tool will tell you

Everything the engine says at a call carries a **code**, and `easel explain <code>` —
`s.explain(code)` from Python, `explain` through the MCP server — prints the passage
that measured it. That is where a rule's reason lives once it is no longer in the
reading path: not deleted, handed over at the one moment it applies.

`easel run` prints them above the post-pass check, in one block, said once each
however many calls tripped them, and **facts first**. What a session file says as it
opens — `foreign-out-dir`, `older-engine` — is said **at load**, before anything else:
on stderr from the shell, and at the top of the answer through the MCP server. A *fact*
is a number about what this call is going to do — the mark lands nothing, the mass
costs 3.9× its own axis, the value that comes back measures neither mass. A *habit* is
a rule of thumb about the picture that a painter can be right to break, and one
painting broke the comb floor twenty-eight times and was right every time.

| Code | Kind | What it says | Measured under |
|---|---|---|---|
| `budget-share` | fact | a plan would eat more than its share of what is left of the budget | `CALIBRATION.md`, *Budget* |
| `budget-spent` | fact | a plan was priced against a budget that is already spent | `CALIBRATION.md`, *Budget* |
| `chisel-blank` | fact | an oriented tip under four pixels wide lays no paint, and is charged for it | `CALIBRATION.md`, *What a solid mass actually lands at* |
| `chisel-pressure` | fact | a pressure list on a chisel tip changes the paint, not the width | `CALIBRATION.md`, *Pressure* |
| `chisel-staircase` | fact | a chisel filling a mass along a straight side it runs nearly along: the pass ends step down that side instead of drawing it | `CALIBRATION.md`, *The chisel staircase* |
| `spill` | fact | a mass or a band whose passes will cover well over the place they were handed: the brush hangs past every pass, over whatever is beside it | `CALIBRATION.md`, *Paint that lands outside the place* |
| `clean-small` | fact | a clean edge whose brush is a large share of the place it fills, a shape or a region: the inset takes the mass rather than a rim off it | `CALIBRATION.md`, *A clean edge on a narrow mass* |
| `count-only` | fact | a counted copy was asked something counting cannot answer | `PAINTING.md`, *Try the mark before you spend it* |
| `solid-comb` | fact | a mass laid solid with a bristle: `solid=` closes the gaps along a pass and not the ones the comb leaves across it | `CALIBRATION.md`, *The holes a solid comb leaves* |
| `holes` | fact | what a mass laid solid actually came back with: the share of its own interior still showing ground, measured, and only where that reads | `CALIBRATION.md`, *The holes a solid comb leaves* |
| `cover-comb` | fact | `cover()` with a bristle does not bury: the comb leaves the old paint showing between the streaks at any opacity | `CALIBRATION.md`, *The bristle comb* |
| `dab-blank` | fact | a round dab laid by hand under the size its press lands from, in pixels: it laid no paint, and is charged for it | `CALIBRATION.md`, *Where a mark stops landing* |
| `direction-default` | fact | a shaped `block_in` with `direction` left off, costing far more than its own axis | `CALIBRATION.md`, *A shaped mass with `direction` left off* |
| `direction-sequence` | fact | a sequence of directions is one whole pass per angle, and is charged the sum | `CALIBRATION.md`, *`direction` given a sequence* |
| `foreign-out-dir` | fact | a loaded session file writes its looks somewhere that is neither the working directory nor beside the file | `REFERENCE.md`, *The session, and the shell* |
| `glaze-far` | fact | a film that moved the passage under it past what a film is for: a new mass in value, or a colour of its own in hue | `CALIBRATION.md`, *A film far from what it lands on* |
| `glaze-nothing` | fact | a film aimed at a value the paint under it already reads solves to no opacity, and still costs a stroke | `CALIBRATION.md`, *Aiming a film at a value* |
| `inward-flat` | fact | an inward scumble's brush wider than about three ring steps: the last rings bury the first and the middle comes back flat | `CALIBRATION.md`, *`scumble`* |
| `jitter-beads` | fact | `jitter=` a multiple of its default, which comes out as width: a chain of beads rather than a line | `PAINTING.md`, *Per-stroke overrides* |
| `older-engine` | fact | a session file saved by an earlier Easel, with marks in its log that a fix since then lays differently: an undo, a replay or a film rebuilt from it will not match the canvas there | `CALIBRATION.md`, *The log, undo, and the stream* |
| `plan-pairs` | fact | two places a plan puts closer than `0.10` meet on the canvas, so one will read as the other exactly where they join | `CALIBRATION.md`, *The plan a painter declares* |
| `prelude-rebind` | fact | a pass binds again a name its prelude bound, to something else: from there to the end of the pass the prelude's value is gone | `REFERENCE.md`, *The session, and the shell* |
| `round-fringe` | fact | a round tip blocking in a feature lays about half again the shape's area, and the fringe is the silhouette | `CALIBRATION.md`, *A clean edge on a narrow mass* |
| `sample-split` | fact | `sample()` averaged two masses, so the value it returns is a measurement of neither | `PAINTING.md`, *Colour* |
| `scumble-bars` | fact | a banded scumble whose passes do not overlap: bars with the ground showing between them | `CALIBRATION.md`, *The band, and the brush that closes its joins* |
| `scumble-dabs` | fact | a scumble whose every pass is shorter than the brush laying it: dabs, and the paint blooms past the outline | `CALIBRATION.md`, *The band across a wedge* |
| `scumble-wedge` | fact | a scumble across a shape whose width varies: no one brush is right for both ends, and the narrow end blooms | `CALIBRATION.md`, *The band across a wedge* |
| `smudge-across` | fact | a smudge whose path crosses a boundary: it carries the first mass about a brush into the second, a thumbprint | `CALIBRATION.md`, *Across a boundary, and along a long one* |
| `clean-comb` | habit | a clean edge drawn with a bristle, whose comb covers about three-quarters of its width | `CALIBRATION.md`, *The contour of a clean edge* |
| `inward-comb` | habit | an inward scumble laid with a bristle under the comb floor: four streaks with gaps rather than a brush | `CALIBRATION.md`, *The bristle comb* |
| `smudge-long` | habit | a smudge run along a boundary for more than a tenth of the canvas: its strip reads as a third band, two edges where there was one | `CALIBRATION.md`, *Across a boundary, and along a long one* |
| `smudge-wide` | habit | a smudge past `0.02`, where one pass stops softening a join and starts dragging a lobe | `CALIBRATION.md`, *`smudge`* |

A pass prints the code and the sentence; the measurement stays where it was
measured. So `chisel-blank` after a pass means a mark was charged and landed nothing,
and `easel explain chisel-blank` is the table of what a solid mass lands at, at four
pixels and either side of it.

**When nothing was said and it still looks wrong**, the other end of the same
arrangement is `easel diagnose <what you can see>` — `diagnose` through the MCP server,
`easel.diagnosis.answer()` from Python. It matches your own words against
[`DIAGNOSIS.md`](DIAGNOSIS.md)'s symptom index and hands back **the passage the row
points at**, not the row: `easel diagnose concentric rings` is the `scumble`
measurement, the same text `explain` would give if there were a code for it. There is
no code for most of what can go wrong on a canvas, which is what the index is for.
`--list` is the symptoms alone, for finding the words to ask with.

**Before you lay a recipe, or after a rehearsal that looks like its failure**, `easel
demo <recipe>` paints it three ways side by side — the recipe, its commonest failure,
and the smallest fix where that is not the recipe itself — and quotes what the tool
said about each: `demo` through the MCP server, `easel.demo.answer()` from Python. Name
the recipe by the words of its heading; with none, it lists which recipes have a demo.
The blocks it paints sit under each *Goes wrong as* in [`RECIPES.md`](RECIPES.md), and
`scripts/check_guide_blocks.py` holds every one to what it says goes wrong.

`s.notices(since=None)` is the list itself, oldest first, and it is saved in the
`.easel` file, so a painting worked from the shell keeps what it was told. So is the
block `easel run` prints after each pass — `s.reports()`, `easel log --reports`, and
`log` with `reports` through the MCP server — **rehearsed and counted passes
included**, each saying which it was: a rehearsal is where a pass gets changed, so a
check that fired on one is otherwise gone with the version it fired on. Notices,
reports and the plan all live **beside** `history.records` and never in it, because
the log indexes the random stream (*Try the mark before you spend it* in
[`PAINTING.md`](PAINTING.md#try-the-mark-before-you-spend-it)): anything new that took
an index would repaint every painting made before it.

---

## The session, and the shell

```python
Session(width=1024, height=768, texture="linen", ground="white", seed=0,
        timelapse=True, out_dir="out", texture_strength=1.0, budget=None)
                   # timelapse=<px> is the frame's long side; the default is 360.
                   # The frames stay in memory: the .easel file keeps none
s.size   s.aspect   s.ground   s.stroke_count   s.spent   s.remaining   s.budget_line()
s.px(x, y)   s.px_size(r)          # a pixel as a place; a length in pixels as a size
s.marks  s.mark(name, x, y)   s.pt(name)   s.unmark(name)
s.guides s.guide(points, note="")        s.unguide(note=None)
                   # points, or a shape drawn as its outline; drawn on the view as a
                   # graphite line on a light casing, which reads over any paint
s.scratch(count_only=False)   # a throwaway copy: the painter's scrap of canvas,
s.undo(n)          # counting on log entries, not marks you paid for; puts the
                   # stream back too. count_only skips the pixel work
s.replay(upto=None, frames=None)   # frames=<px> records a time-lapse as it rebuilds,
                   # which is what timelapse_gif(from_log=True) is made of: the film
                   # at any size, from a painting that recorded no frames at all
s.save(path)       Session.load(path)
```

```bash
easel new p.easel --size 1024x768 --texture linen --ground toned_grey --seed 7 --budget 300 [--frame-px 720] [--no-prelude]
easel run p.easel pass.py [p3.py p4.py ...] [--rehearse] [--count] [--alternatives] [--thumbnail] [--prelude other.py] [--no-prelude] [--check]
easel look p.easel [--grid] [--fine] [--values] [--region D4] [--reference ref.jpg] [--diff]
                   [--no-sketch] [--no-marks] [--scale 512]
easel mark p.easel top_l 0.335 0.315
easel plan p.easel [--why "..."] [--value 'A1:H3=0.70' ...] [--lightest A1:H3]
                   [--subject-share 0.4] [--bands subject] [--ground buried] [--clear]
easel compare p.easel ref.jpg [--region D4]
easel prepare p.easel ref.jpg [--level coarse]
easel undo p.easel 3
easel export p.easel painting.png
easel timelapse p.easel p.gif [--fps 8] [--every 3] [--scale 240] [--from-log]
easel check p.easel [--subject-share 0.32]
easel log p.easel [-n 20] [--check | --reports]
easel brushes
easel guide [--full | --painting | --recipes | --reference | --calibration | --diagnosis] [--path]
easel explain [code]
easel diagnose [what you can see ...] [--list]
easel demo [recipe ...] [--out-dir out] [-o sheet.png]
```

A script run by `easel run` gets the session as `s`, with the whole public API already
in scope and no imports needed. A `prelude.py` beside the session file runs first in the
same scope, so helpers, mixtures and landmarks survive between passes — and it is where
`s.plan(...)` goes, declared once for the painting rather than once per pass. `easel new`
writes one holding the call, unless there is already one there or `--no-prelude` says not
to. **One scope means one set of names**: a pass that binds a name the prelude bound, to
something else — `H = dict(...)` over the prelude's canvas height — has replaced it for
the rest of the pass, and is told so before it runs (`prelude-rebind`), naming both lines.
Binding the same thing again, `p = s.palette` in every pass, says nothing.

Several scripts run in the order given, each in its own scope with the prelude in front
of it — the same painting as running them one at a time, and with `--rehearse` they go
on **one** copy, so a pass that lands on top of another pass is judged on it.

**With `--alternatives` they are versions of one pass instead**, and each goes on a copy
of its own: each is checked and keeps its report on its own, and their looks are laid
side by side in one sheet, `rehearse_NNN.png`, each panel labelled with the script and
the strokes it laid. Every copy is seeded as the next marks of the painting, so the
version then run for real lands as its panel shows it. A version that raises is said and
left off the sheet, and the others are still rehearsed, since none stands on another.
It implies `--rehearse`; with `--count` each is priced and no sheet is laid; a sheet
holds at most twelve. `s.rehearse_each()` is the same from Python and `run` with
`alternatives` through the MCP server.

After every pass, rehearsed, counted or committed, `run` prints the budget line and then
the post-pass check over that pass; `--check` runs it over the whole painting instead, and
`easel log --check` does the same without painting anything. **Under the budget line, the
pass's dearest calls**, whenever a call cost more than one stroke — a mark laid by hand is
one, and is never listed:

```text
Rehearsed p04.py: 102 strokes of the 210 left. Nothing committed.
  dearest: 23 block_in at p04.py:40 (lay_mass, 2 landing nothing), 22 at :38, 20 at :36, 14 at :18 (lay_side) -- 79 of the 102
```

Dearest first, up to four and none once three quarters of the pass is named; each call's
strokes, its verb and the script line it was made from, the script once per run of it and
the function once per run of calls from it; and the strokes of it that laid no paint, which
a counted pass cannot know. A call made inside a helper is named at the helper's line. It is
said per version under `--alternatives`, through the MCP server's `run`, and kept in the
pass's saved report.

`easel check` is the **closing** checklist rather than the post-pass one: the same
measured lines plus `boxes:` and `unspent:`, and then the three questions nothing can
measure, with the plan's own `why` quoted back. `s.checklist()` is the same from
Python and `check` through the MCP server. It is read-only and does not write the
session file.

`--count` is `--rehearse` with the pixel work skipped: the pass is worked out stroke for
stroke and none of it is laid, so a helper that calls a dozen verbs has a price and a
check in about a thirtieth of the time and there is no look to write.
`s.scratch(count_only=True)` is the same thing from Python and `run(count=True)` through
the MCP server. Rehearse when the question is what it looks like.

`--thumbnail` counts the pass as `--count` does and draws **the arrangement it would
leave**: `s.thumbnail()` with no argument on the copy, the pass's masses flat over the
painting's and over the plan's places, as `thumbnail_NNN.png` —

```text
Thumbnail of the plan's 7 places and 14 masses laid, 6 of them by this pass, at 192 px: out/thumbnail_004.png
```

It is the look for *does this pass's arrangement read*, taken before a mark of the pass
is rendered: `0.15` s for one painter's subject pass, whose rehearsal takes `7.9`. With
`--rehearse` the copy is painted and looked at as well; with `--alternatives` each
version is counted and the sheet is their thumbnails, side by side, each labelled under
its panel. `run(thumbnail=True)` through the MCP server; from Python, the pass laid on
`s.scratch(count_only=True)` and that copy's `thumbnail()`.

`--scale` on `look` and `timelapse` is **the long side in pixels** — `--scale 240` — and a
number under 1, which no count of pixels can be, is a share of the canvas's own long side:
`--scale 0.5` is half of it. `look --scale 0` is the canvas at its own size.

**The `.easel` file keeps everything but the time-lapse.** The frames were more than half
of a painting's file, for a film made once, at the end, so a session loaded from a file
records none and `easel timelapse` rebuilds the film from the log at the session's frame
size — the same film, frame for frame, at the price of a full repaint. A file saved
before 0.7.0 that kept its frames still uses them. **And the file says which release
saved it**: the canvas opens as it was painted under any later one, but a rebuild — an
`undo`, a `replay()`, a film made from the log — lays every mark again with the engine
installed, so a file whose log has marks a fix since then lays differently says so as
it opens, with how many (`older-engine`). Said once: the next save stamps the file with
the release that saved it.

---

## Or through the MCP server

If your client speaks MCP, the same verbs are there as tools, and the difference worth
having is that **the looking tools hand you the picture**: `look`, `preview`,
`rehearse`, `thumbnail`, `compare` and `prepare` return their PNG beside the path they
wrote it to, so looking every five to fifteen strokes costs one call instead of a call
and a file read. Marks are still made by `run`, which takes the script as text — the
same Python the guide teaches, with `s` and the whole API already in scope — and **what
it rehearses comes back inline too**: with `rehearse`, the copy's look beside the path
it was written to, and as `alternatives`, several versions of one pass, rehearsed each
on a copy of its own and handed back side by side in one sheet. `preview`, `rehearse`
and `cost` each hand back the Python that paints the plan they checked; paste that into
`run` rather than retyping it, because a plan retyped between checking and painting
drifts.

A **place** arrives as JSON in any of six forms — a named region, a grid cell, a span, a
rectangle, an outline, or a shape builder with its own arguments:

```text
"upper-band"                                    a named region
"D4"                                            one grid cell
"C3:F6"                                         a run of cells
[0.10, 0.10, 0.45, 0.30]                        a rectangle
[[0.2, 0.2], [0.6, 0.15], [0.7, 0.5]]           an outline you have
{"blob": "D5", "radius": 0.12, "seed": 3}       and the builders: blob, ellipse,
{"ribbon": [[0.2, 0.8], [0.5, 0.5]], "width": 0.09}      hull, ribbon, polygon
```

A **plan** is a list of entries, or one on its own: a mass is an object with `shape`
and any `block_in` argument, a sweep one with `edge` and any `sweep` argument, a passage
one with `band`, `color_a` and `color_b`, a burial one with `cover`, and a mark a list of
points or an object with `points` — a film among them, with `"glaze": true` and the
glaze verb's brush and opacity, as under *Looking, planning, measuring*.

```json
{"shape": {"blob": "D5", "radius": 0.12, "seed": 3},
 "brush": "bristle", "color": "dark", "size": 0.05, "direction": "axis"}
```

`thumbnail` takes its places as `plan` takes its `values` — `{"C3:F6": 0.30, "A1:H3":
"sky"}` — or as a list of `[place, value]` pairs, which is how a shape goes in, since a
JSON key is a string: `[[{"blob": "D5", "radius": 0.12}, 0.15]]`. A value is a number or
a colour, and `[value, clip]` holds a place inside a clip, as in Python.

The server is `easel-mcp`, or `python -m easel.mcp_server` when the scripts directory
is not on `PATH`. It needs one extra: `pip install easel-paint[mcp]`. The `guide` tool
returns any of the six documents, so a client with no repository to read still has the
method, and `explain` and `diagnose` hand over the passage behind a code or a symptom
without it having to fetch a file at all. `demo` hands back its sheet inline, like the
looking tools.
