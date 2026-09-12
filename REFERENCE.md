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
| `size` (brush) | a fraction of the canvas's **long side**, whichever way the brush travels |
| `depth`, `inset()`, `overhang` distance | normalised canvas units, the same as a coordinate |
| An angle | degrees **clockwise from the horizontal**; `y` runs *down*, so `90` is downward |
| A value | `0..1`, the sRGB luminance `look(values=True)` shows and `palette.value_of` reports |
| A colour | a pigment name, a palette slot you named, `"#rrggbb"`, or an `(r, g, b)` triple |
| A place | a region name, `"D4"`, `"C3:F6"`, a `Region`, a 4-tuple `(x0, y0, x1, y1)`, or a `Polygon` |

**The first two rows are not the same unit.** On a canvas that is not square, a step of
`0.07` down is a different number of pixels from `0.07` across, while a brush at
`size=0.07` is `0.07` of the long side both ways. A radius `r` in `x` is `r * width /
height` in `y` — or use `s.circle(place, r)`, which is round in pixels, and
`ellipse(..., aspect=s.aspect)`.

---

## What counts against the budget

| Free | Charged, one per mark |
|---|---|
| `pencil`, `erase`, `mark`, `unmark` | `stroke`, `dab` |
| `dry` | `smudge`, `glaze` — marks like any other |
| `look`, `preview`, `rehearse`, `cost`, `compare`, `prepare` | `block_in`, `sweep`, `scumble`, `cover` — **once per pass**, so one call is ten to thirty |
| `undo` (it removes what was charged) | |
| `sketch(reference)` — it lays pencil, and is an assisted mode the log records | |

`s.stroke_count` is the tally, `s.spent` and `s.remaining` are it against a
`Session(budget=...)`, and `s.budget_line()` prints both. The first five marks whose
`note` contains `signature` are free; every one after that is charged.

**Before a mass, not after**: `s.cost(plan)` walks the passes without laying them and
returns the number, and `s.cost_line(plan)` says *why* it is that number.

---

## The verbs

| Call | Lays | Costs |
|---|---|---|
| `stroke(points, brush, color, ...)` | one mark along a path | 1 |
| `dab(x, y, brush, color, press=1)` | one mark at a point; `press` stamps it again | 1 |
| `smudge(edge, size=0.07)` | drags what is on the canvas, along a path **or a shape's own outline** | 1 |
| `glaze(points, color, opacity=0.18)` | a thin film that adds no height | 1 |
| `block_in(place, ...)` | a mass, as overlapping passes | one per pass |
| `sweep(edge, ..., into=, depth=)` | a mass, as passes along its boundary stepped inward | one per pass |
| `scumble(band, a, b, n=8)` | a soft passage, `n` passes stepping between two colours | `n` |
| `cover(place, color)` | a repair, with every clause of the burying recipe set | one per pass |
| `pencil(points)` | graphite under the paint | 0 |
| `erase(region=None)` | takes graphite out | 0 |
| `dry(amount=1.0, region=None)` | takes the wetness out so new paint covers rather than mixes | 0 |

---

## The arguments that mean something particular

| Argument | Default | What it does |
|---|---|---|
| `density` | `1.0` | how close the passes run: `size × (1 − 0.45 × density)` apart. **Spacing, not coverage** |
| `solid` | `False` | `load=1.0, load_falloff=0.0`, so no pass runs dry along its length. What fills a mass |
| `overhang` | `0.35` box, `0` shape | how far each pass runs **past the ends** of the place, in brush widths. Not its sides |
| `edge` | `"ragged"` | `"clean"` insets the fill half a brush and draws the contour along the inset outline. The contour does not wander: the line is the drawing |
| `direction` | `"horizontal"` | `"horizontal"`, `"vertical"`, `"diagonal"`, `"cross"`, `"axis"` (the place's own), degrees, or a sequence for one pass each. On `scumble`, also `"inward"`. **Where the stack starts** is below |
| `pressure` | `"taper"` | see *Pressure* below |
| `opacity` | the brush's | per-dab strength. Dabs overlap, so a low one accumulates back toward full colour |
| `load` | the brush's | how much paint the brush carries. It spends itself along the stroke |
| `load_falloff` | the brush's | how fast it spends. `0` never runs dry |
| `size` | the brush's | tip diameter, as a fraction of the canvas long side. On `scumble(direction="inward")`, left off, it is picked from the ring step: `3 × depth / n` |
| `wander` (sweep) | `True` | whether each pass wanders off the offset curve, so a stack is not parallel rules. A **single** pass has no parallel to break and the wander only moves it off the line drawn; off for the contour of `edge="clean"` |
| `tip_wobble` | `0.0` | a round tip's own silhouette, redrawn per mark. `0.35` a brush set down once, `0.7`+ a clot |
| `press` | `1` | for a one-point mark, how many times to stamp it. One mark either way |
| `glaze` | `False` | lay colour without building paint height |
| `smooth` | `True` | fit a spline through the points; off gives hard corners |
| `into` (sweep) | — | which side the mass is on: a compass word, degrees, or a point inside it. A closed edge needs none |
| `depth` (sweep) | `0.2` | how far into the mass to sweep, in canvas units |
| `cross` (sweep) | `None` | a second set of passes leaning this many degrees off the boundary. 20–30 is usual |
| `passes` (sweep) | `None` | pin the count instead of letting the brush decide |
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
| `round_soft` | round | `0.06` | `0.75` | `0.20` | `1.0` | `0.35` | blending and soft edges; above `size≈0.05` it airbrushes |
| `round_hard` | round | `0.045` | `0.95` | `0.85` | `1.0` | `0.50` | deliberate marks, accents, small shapes |
| `liner` | round | `0.005` | `0.95` | `1.00` | `1.0` | `0.18` | fine lines at feature scale; no jitter, holds its load |
| `smudge` | round | `0.07` | `0.60` | `0.25` | `1.0` | `0.00` | carries no paint; moves what is already there |

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
| `flat`, `bristle`, `knife` | **paint only.** The chisel keeps the width you asked for, because that width is the mass it lays |

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
r.point(u, v)  r.inset(a)  r.scaled(f)  r.shifted(dx, dy)  r.split_h(n)  r.split_v(n)
```

## Shapes

```python
polygon(points)                        # an outline you already have
ellipse(place, rx=None, ry=None, rotate=0, aspect=None)
blob(place, radius=None, wobble=0.22, points=15, seed=0, aspect=None)
hull(places)                           # the mass around some points
ribbon(places, width, end_width=None)  # a mass running along a line
union(a, b, ...)                       # one silhouette round overlapping shapes
s.circle(place, r, wobble=0)           # round in *pixels* on any canvas
shape.inset(a)  shape.smooth(2)  shape.scaled(f)  shape.shifted(dx, dy)
shape.box  shape.area  shape.axis  shape.center  shape.closed  shape.contains(x, y)
```

A shape goes anywhere a region goes. `shape.box` is the rectangle a mass is *priced*
on — worth looking at before blocking in anything long and curved.

---

## Colour

Eleven pigments and no black: `titanium_white`, `lemon_yellow`, `cadmium_yellow`,
`yellow_ochre`, `cadmium_red`, `alizarin`, `burnt_sienna`, `burnt_umber`, `ultramarine`,
`cerulean`, `viridian`. (`white`, `yellow`, `ochre`, `red`, `blue`, `umber` and `sienna`
are accepted as short names for seven of them.)

```python
p = s.palette
p["shadow"] = p.mix("ultramarine", "burnt_umber", 0.45)   # named, and it persists
p.tint(c, 0.3)   p.shade(c, 0.3)   p.desaturate(c, 0.3)
p.at_value(base, 0.62)      # that colour, moved to that value, from either side
p.value_of(c)               # what look(values=True) will show
p.darkest_value             # about 0.13: the floor of the box
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

Grounds for `Session(ground=...)`: `white`, `warm_white`, `toned_grey`,
`toned_warm_grey`, `cool_grey`, `umber_wash`, `burnt_sienna` — or any colour.
Textures: `smooth`, `linen`, `rough`.

---

## Looking, planning, measuring

```python
s.look(grid=, values=, region=, reference=, diff=, scale=, sketch=, path=)
s.preview(plan, reference=, region=, grid=)     # where a mark would go
s.rehearse(plan, reference=, region=)           # what it would look like
s.cost(plan)        s.cost_line(plan)           # what it charges, and why
s.paint(plan)                                   # the same plan, now paid for
s.compare("ref.jpg", region=, threshold=0.10)   # per-cell value of both, and the miss
s.compare({place: value, ...})                  # ...against your own value plan
s.sample(place=None)                            # the colour already there, to paint with
s.prepare("ref.jpg", level="coarse")            # 7 masses; "medium" 20, "fine" 40
s.log(last=10)                                  # last=10_000 for the whole record
s.export("painting.png", impasto=True, sketch=True)
s.timelapse_gif("p.gif", fps=8.0, every=1, scale=None)
s.contact_sheet("sheet.png", columns=6)
```

A **plan** is one object all four planning verbs read: a list whose entries are a path,
a dict of `stroke` arguments, a dict with `shape=` and any `block_in` argument, or a
dict with `edge=` and any `sweep` argument. A bare place or shape is a mass.

Looks are written to `out_dir` and numbered: `look_001.png`, `preview_002.png`,
`compare_003.png` in one run of numbers belonging to the session, and rehearsals in
their own — `rehearse_001.png` upward, each taking the next free name.

---

## The session, and the shell

```python
Session(width=1024, height=768, texture="linen", ground="white", seed=0,
        timelapse=True, out_dir="out", texture_strength=1.0, budget=None)
s.size   s.aspect   s.stroke_count   s.spent   s.remaining   s.budget_line()
s.marks  s.mark(name, x, y)   s.pt(name)   s.unmark(name)
s.scratch()        # a throwaway copy: the painter's scrap of canvas
s.undo(n)          # log entries, not marks you paid for
s.replay(upto=None)
s.save(path)       Session.load(path)
```

```bash
easel new p.easel --size 1024x768 --texture linen --ground toned_grey --seed 7 --budget 300
easel run p.easel pass.py [p3.py p4.py ...] [--rehearse] [--prelude other.py] [--no-prelude]
easel look p.easel [--grid] [--fine] [--values] [--region D4] [--reference ref.jpg] [--diff]
easel mark p.easel top_l 0.335 0.315
easel compare p.easel ref.jpg [--region D4]
easel prepare p.easel ref.jpg [--level coarse]
easel undo p.easel 3
easel export p.easel painting.png
easel timelapse p.easel p.gif [--fps 8] [--every 3] [--scale 240]
easel brushes
easel guide [--full | --painting | --recipes | --reference | --calibration] [--path]
```

A script run by `easel run` gets the session as `s`, with the whole public API already
in scope and no imports needed. A `prelude.py` beside the session file runs first in the
same scope, so helpers, mixtures and landmarks survive between passes.

Several scripts run in the order given, each in its own scope with the prelude in front
of it — the same painting as running them one at a time, and with `--rehearse` they go
on **one** copy, so a pass that lands on top of another pass is judged on it.

The same verbs are available over MCP (`easel-mcp`), where the looking tools hand back
the picture rather than a path to it. See [`README.md`](README.md).
