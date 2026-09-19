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
| An angle | degrees **clockwise from the horizontal, in the `0..1` coordinates**; `y` runs *down*, so `90` is downward. Passes *run* along the angle and a stack *steps* across it. On a canvas that is not square the screen angle is flatter than the number: `direction=-23` lays passes at `-12°` on a 2:1 canvas and `-18°` on 4:3, and `45` runs at `37°` on 4:3. An angle read off the picture does not have to be converted: hand `direction=` the two points instead — `direction=((0.33, 0.01), (0.58, 0.29))` — and it does the `atan2` for you |
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
| `sketch(reference, level=, pressure=, areas=)` — it lays pencil, and is an assisted mode the log records; `areas=` lays some of the numbered masses rather than all of them | |

`s.stroke_count` is the tally, `s.spent` and `s.remaining` are it against a
`Session(budget=...)`, and `s.budget_line()` prints both. The first five marks whose
`note` contains `signature` are free; every one after that is charged. Inside a
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
| `pencil(points)` | graphite under the paint | 0 |
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
`load=1.0, load_falloff=0.0` already, because that pair is the burying recipe.

---

## The arguments that mean something particular

| Argument | Default | What it does |
|---|---|---|
| `density` | `1.0` | how close the passes run: `size × (1 − 0.45 × density)` apart. **Spacing, not coverage** |
| `solid` (`block_in`, `stroke`, `sweep`, `scumble`) | `False` | `load=1.0, load_falloff=0.0`, so no pass runs dry along its length. A solid mass still lands a little short of its mixture on any brush but a round one, and an oriented tip under four pixels wide lands the ground and says so: *What a solid mass actually lands at* in `CALIBRATION.md` |
| `overhang` (`block_in`) | `0.35` box, `0` shape | how far each pass runs **past the ends of the pass**, in brush widths. It moves the ends only, never the sides, and which two edges are the ends turns with `direction`. A shape defaults to `0` because its outline is the drawing; a rectangle stopping short of its corners reads as cropped |
| `overhang` (`scumble`) | `0.35` | the same measure as `block_in`'s, but flat — `scumble` does not vary its default between a box and a shape |
| `overhang` (`cover`) | `1.0` | one full brush width, so a repair's ends sit outside the mistake it is covering rather than stopping at its edge |
| `edge` | `"ragged"` | `"clean"` insets the fill half a brush and draws the contour along the inset outline — along its **own edges**, not a spline through its corners, which bowed 65px off a four-cornered tower. The contour does not wander: the line is the drawing. On a mass whose shorter extent is under four brushes it says so, and so does `preview`. `"hard"` masks every dab to the outline instead — no inset, no contour pass, no extra stroke, and no paint outside the shape: the one setting that ends a pass on a line rather than on its own tip. `overhang` defaults to a full brush there, since nothing can cross the outline. `cover()` takes both, and `scumble()` takes `"hard"` — a passage has no contour to draw, and a band crossed at an angle is the place a mass lands furthest outside itself |
| `direction` | left off: `"horizontal"` | `"horizontal"`, `"vertical"`, `"diagonal"`, `"cross"`, `"axis"` (the place's own), degrees clockwise from horizontal, a **line of two points** to run along, or a sequence of any of those. A pair of points is a line; a pair of numbers is two angles. **A sequence lays a full stack per angle and is priced as the sum**; `"cross"` is two angles and the affordable way to break a comb. On `scumble`, also `"inward"`. Left off on a shape, `block_in` and `cost` say so when horizontal passes cost over 2.5× `"axis"`; given a sequence, when it costs over 2.5× its own dearest angle. **Where the stack starts** is below |
| `pressure` | `"taper"` | see *Pressure* below |
| `opacity` | the brush's | per-dab strength. Dabs overlap, so a low one accumulates back toward full colour |
| `load` | the brush's | how much paint the brush carries. It spends itself along the stroke |
| `load_falloff` | the brush's | how fast it spends. `0` never runs dry |
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
| `round_soft` | round | `0.06` | `0.75` | `0.20` | `1.0` | `0.35` | blending and soft edges; above `size≈0.05` it airbrushes |
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
r.point(u, v)  r.inset(a)  r.scaled(f)  r.shifted(dx, dy)  r.split_h(n)  r.split_v(n)
```

## Shapes

```python
polygon(points, name="")               # an outline you already have
ellipse(place, rx=None, ry=None, rotate=0, steps=48, aspect=None, name="")
blob(place, radius=None, ry=None, wobble=0.22, points=15, seed=0, rotate=0,
     aspect=None, name="")
hull(places, name="")                  # the mass around some points
ribbon(places, width, end_width=None, smooth=True, name="")   # a mass along a line
union(a, b, ..., resolution=1024, name="")     # one silhouette round overlapping shapes
s.circle(place, r, wobble=0, points=15, seed=0, rotate=0, steps=48, name="")
                                       # round in *pixels* on any canvas
shape.inset(a)  shape.smooth(2)  shape.scaled(f)  shape.shifted(dx, dy)
shape.box  shape.area  shape.axis  shape.center  shape.closed
shape.contains(x, y)                   # is this mark inside the mass?
shape.inside(xs, ys)                   # ...and the same question for many at once
```

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
p.value_of(c)               # what look(values=True) will show
p.chroma_of(c)              # how coloured: 0 for a grey, 0.20 for cadmium_red
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
       path=)                                   # the last three are on unless turned off
s.preview(plan, reference=, region=, grid=, values=, scale=, path=)   # where a mark goes
s.rehearse(plan, reference=, region=, grid=, values=, scale=, path=)  # what it looks like
s.cost(plan, share=0.25)   s.cost_line(plan)    # what it charges, and why; share= is
                                                # how much of what is left it may eat
s.paint(plan, note="")                          # the same plan, now paid for
s.compare("ref.jpg", region=, threshold=0.10, near=0.01, path=)
                                                # per-cell value of both, and the miss
s.compare({place: value, ...})                  # ...against your own value plan, and
                                                # the pairs it puts within 0.10: do they touch?
s.sample(place=None, rendered=False)            # the colour already there, to paint with
s.report(since=None, subject_share=None)        # the post-pass check, read off the log
s.notices(since=None)   s.explain(code)         # what the calls themselves said, and why
s.prepare("ref.jpg", level="coarse", min_share=0.004, path=)
                                                # 7 masses; "medium" 20, "fine" 40
s.log(last=10)                                  # last=10_000 for the whole record
s.export("painting.png", impasto=True, sketch=True)
s.timelapse_gif("p.gif", fps=8.0, every=1, scale=None, from_log=False)
                                                # from_log rebuilds the frames by
                                                # replaying, at any size
s.contact_sheet("sheet.png", columns=6)
```

A **plan** is one object all four planning verbs read: a list whose entries are a path,
a dict of `stroke` arguments, a dict with `shape=` and any `block_in` argument, or a
dict with `edge=` and any `sweep` argument. A bare place or shape is a mass.

Looks are written to `out_dir` and numbered `look_001.png`, `preview_001.png`,
`compare_001.png`, `rehearse_001.png` upward — each kind counting on its own, and each
taking the next free name **in the directory** rather than the next number in the
session. So two sessions sharing an `out_dir` do not write over each other, and a
painting reopened between `easel run` calls carries on where the directory left off.
Pass `path=` to name a file yourself.

`report()` is the check `easel run` prints beside the budget line after every pass:
seven rules read off the log — one brush at one size for a whole pass of two or more
calls; twelve or more long marks within six degrees of one angle, from two or more
calls, **said once and again only when the picture has picked up a long mark 30 degrees
off the bars it was said about** (`--check`, which is asked for rather than printed at
you, says it whenever it is true); **a graded passage laid too narrow**, five or more long parallel marks at three
or more colours, in one run with no gap wider than four brushes, their colours turning
at most once, stepped further apart than half the narrowest brush laying them (a brush
that lays no colour of its own is not counted);
a bristle under `size=0.025` **at a load over `0.6`**, because below that the
comb's gaps are the mark; eight or more marks under `size=0.02` inside the
painting's first sixty; a pressure list on a short chisel mark; and three or more small
round-tip marks at `tip_wobble=0`, each short enough to be the tip's silhouette rather
than a line. Under those, two standing measurements: the subject's share of the marks so
far, wherever a mark is noted `subject`, against `subject_share` if given, and what
share of the canvas is **still bare ground**, which says so under `0.5%`. Both count the
painting behind a rehearsal copy, not the copy's own log.
`since=` is the log index the pass began at (`len(s.history.records)` before it);
left off, the whole painting. Two more need the shape and fire at the call: a shaped
`block_in` with `direction` left off costing over 2.5× its axis (or a sequence costing
over 2.5× its own dearest angle), and a round tip blocking in a **feature** — a shape under a
tenth of the canvas across — that is less than four of its brushes wide. Over that
width the same brush is a mass with a soft silhouette, which is what a round tip is
for.

---

## What the tool will tell you

Everything the engine says at a call carries a **code**, and `easel explain <code>` —
`s.explain(code)` from Python, `explain` through the MCP server — prints the passage
that measured it. That is where a rule's reason lives once it is no longer in the
reading path: not deleted, handed over at the one moment it applies.

`easel run` prints them above the post-pass check, in one block, said once each
however many calls tripped them, and **facts first**. A *fact* is a number about what
this call is going to do — the mark lands nothing, the mass costs 3.9× its own axis,
the value that comes back measures neither mass. A *habit* is a rule of thumb about
the picture that a painter can be right to break, and one painting broke the comb
floor twenty-eight times and was right every time.

| Code | Kind | What it says | Measured under |
|---|---|---|---|
| `budget-share` | fact | a plan would eat more than its share of what is left of the budget | `CALIBRATION.md`, *Budget* |
| `budget-spent` | fact | a plan was priced against a budget that is already spent | `CALIBRATION.md`, *Budget* |
| `chisel-blank` | fact | an oriented tip under four pixels wide lays no paint, and is charged for it | `CALIBRATION.md`, *What a solid mass actually lands at* |
| `chisel-pressure` | fact | a pressure list on a chisel tip changes the paint, not the width | `CALIBRATION.md`, *Pressure* |
| `clean-small` | fact | a clean edge whose brush is a large share of the shape: the inset takes the mass rather than a rim off it | `CALIBRATION.md`, *A clean edge on a narrow mass* |
| `count-only` | fact | a counted copy was asked something counting cannot answer | `PAINTING.md`, *Try the mark before you spend it* |
| `solid-comb` | fact | a mass laid solid with a bristle: `solid=` closes the gaps along a pass and not the ones the comb leaves across it | `CALIBRATION.md`, *The holes a solid comb leaves* |
| `cover-comb` | fact | `cover()` with a bristle does not bury: the comb leaves the old paint showing between the streaks at any opacity | `CALIBRATION.md`, *The bristle comb* |
| `direction-default` | fact | a shaped `block_in` with `direction` left off, costing far more than its own axis | `CALIBRATION.md`, *A shaped mass with `direction` left off* |
| `direction-sequence` | fact | a sequence of directions is one whole pass per angle, and is charged the sum | `CALIBRATION.md`, *`direction` given a sequence* |
| `foreign-out-dir` | fact | a loaded session file writes its looks somewhere that is neither the working directory nor beside the file | `REFERENCE.md`, *The session, and the shell* |
| `glaze-nothing` | fact | a film aimed at a value the paint under it already reads solves to no opacity, and still costs a stroke | `CALIBRATION.md`, *Aiming a film at a value* |
| `inward-flat` | fact | an inward scumble's brush wider than about three ring steps: the last rings bury the first and the middle comes back flat | `CALIBRATION.md`, *`scumble`* |
| `jitter-beads` | fact | `jitter=` a multiple of its default, which comes out as width: a chain of beads rather than a line | `PAINTING.md`, *Per-stroke overrides* |
| `round-fringe` | fact | a round tip blocking in a feature lays about half again the shape's area, and the fringe is the silhouette | `CALIBRATION.md`, *A clean edge on a narrow mass* |
| `sample-split` | fact | `sample()` averaged two masses, so the value it returns is a measurement of neither | `PAINTING.md`, *Colour* |
| `scumble-bars` | fact | a banded scumble whose passes do not overlap: bars with the ground showing between them | `CALIBRATION.md`, *The band, and the brush that closes its joins* |
| `scumble-dabs` | fact | a scumble whose every pass is shorter than the brush laying it: dabs, and the paint blooms past the outline | `CALIBRATION.md`, *The band across a wedge* |
| `scumble-wedge` | fact | a scumble across a shape whose width varies: no one brush is right for both ends, and the narrow end blooms | `CALIBRATION.md`, *The band across a wedge* |
| `clean-comb` | habit | a clean edge drawn with a bristle, whose comb covers about three-quarters of its width | `CALIBRATION.md`, *The contour of a clean edge* |
| `inward-comb` | habit | an inward scumble laid with a bristle under the comb floor: four streaks with gaps rather than a brush | `CALIBRATION.md`, *The bristle comb* |
| `smudge-wide` | habit | a smudge past `0.02`, where one pass stops softening a join and starts dragging a lobe | `CALIBRATION.md`, *`smudge`* |

A pass prints the code and the sentence; the measurement stays where it was
measured. So `chisel-blank` after a pass means a mark was charged and landed nothing,
and `easel explain chisel-blank` is the table of what a solid mass lands at, at four
pixels and either side of it.

`s.notices(since=None)` is the list itself, oldest first, and it is saved in the
`.easel` file, so a painting worked from the shell keeps what it was told. Notices
live **beside** `history.records` and never in it: a mark's texture is seeded from its
place in the log, so anything new that took an index would repaint every painting made
before it.

---

## The session, and the shell

```python
Session(width=1024, height=768, texture="linen", ground="white", seed=0,
        timelapse=True, out_dir="out", texture_strength=1.0, budget=None)
                   # timelapse=<px> is the frame's long side; the default is 360
s.size   s.aspect   s.ground   s.stroke_count   s.spent   s.remaining   s.budget_line()
s.marks  s.mark(name, x, y)   s.pt(name)   s.unmark(name)
s.guides s.guide(points, note="")        s.unguide(note=None)
s.scratch(count_only=False)   # a throwaway copy: the painter's scrap of canvas,
s.undo(n)          # counting on log entries, not marks you paid for; puts the
                   # stream back too. count_only skips the pixel work
s.replay(upto=None, frames=None)   # frames=<px> records a time-lapse as it rebuilds,
                   # which is what timelapse_gif(from_log=True) is made of: the film
                   # at any size, from a painting that recorded no frames at all
s.save(path)       Session.load(path)
```

```bash
easel new p.easel --size 1024x768 --texture linen --ground toned_grey --seed 7 --budget 300 [--frame-px 720]
easel run p.easel pass.py [p3.py p4.py ...] [--rehearse] [--count] [--prelude other.py] [--no-prelude] [--check]
easel look p.easel [--grid] [--fine] [--values] [--region D4] [--reference ref.jpg] [--diff]
easel mark p.easel top_l 0.335 0.315
easel compare p.easel ref.jpg [--region D4]
easel prepare p.easel ref.jpg [--level coarse]
easel undo p.easel 3
easel export p.easel painting.png
easel timelapse p.easel p.gif [--fps 8] [--every 3] [--scale 240] [--from-log]
easel log p.easel [-n 20] [--check]
easel brushes
easel guide [--full | --painting | --recipes | --reference | --calibration] [--path]
easel explain [code]
```

A script run by `easel run` gets the session as `s`, with the whole public API already
in scope and no imports needed. A `prelude.py` beside the session file runs first in the
same scope, so helpers, mixtures and landmarks survive between passes.

Several scripts run in the order given, each in its own scope with the prelude in front
of it — the same painting as running them one at a time, and with `--rehearse` they go
on **one** copy, so a pass that lands on top of another pass is judged on it.

After every pass, rehearsed or committed, `run` prints the budget line and then the
post-pass check over that pass; `--check` runs it over the whole painting instead, and
`easel log --check` does the same without painting anything.

`--count` is `--rehearse` with the pixel work skipped: the pass is worked out stroke for
stroke and none of it is laid, so a helper that calls a dozen verbs has a price and a
check in about a thirtieth of the time and there is no look to write.
`s.scratch(count_only=True)` is the same thing from Python and `run(count=True)` through
the MCP server. Rehearse when the question is what it looks like.

---

## Or through the MCP server

If your client speaks MCP, the same verbs are there as tools, and the difference worth
having is that **the looking tools hand you the picture**: `look`, `preview`,
`rehearse`, `compare` and `prepare` return their PNG beside the path they wrote it to,
so looking every five to fifteen strokes costs one call instead of a call and a file
read. Marks are still made by `run`, which takes the script as text — the same Python
the guide teaches, with `s` and the whole API already in scope. `preview`, `rehearse`
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

A **plan** is a list of those three kinds of thing, or one on its own: a mass is an
object with `shape` and any `block_in` argument, a sweep one with `edge` and any
`sweep` argument, a mark a list of points or an object with `points`.

```json
{"shape": {"blob": "D5", "radius": 0.12, "seed": 3},
 "brush": "bristle", "color": "dark", "size": 0.05, "direction": "axis"}
```

The server is `easel-mcp`, or `python -m easel.mcp_server` when the scripts directory
is not on `PATH`. It needs one extra: `pip install easel-paint[mcp]`. The `guide` tool
returns any of the five documents, so a client with no repository to read still has the
method.
