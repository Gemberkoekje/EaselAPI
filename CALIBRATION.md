# Calibration: the engine's measured numbers

`PAINTER.md` tells you how to paint with Easel. This file holds the numbers behind
its rules — what was measured, on the engine as it is now. You do not need any of
it to paint. Come here when a rule in the guide makes you want to know *how much*,
or when a mark did not do what you expected and you want to know whether that is
you or the engine.

Every figure here is a measurement of the current engine and will move when the
engine changes. Trust the picture in front of you over a number in this file.

---

## Values

`palette.value_of(c)` reports the sRGB-encoded luminance of a colour, which is the
same number `look(values=True)` shows. The greyscale view and the number agree by
construction.

**The threshold is `0.10`.** Two masses closer than a tenth of the value range read
as one mass. `compare()` uses the same number.

### What the box reaches

Each pigment, one flat pass on a toned grey ground, read off the exported PNG:

| Pigment | Value |
|---|---|
| `burnt_umber` | 0.13 |
| `alizarin` | 0.15 |
| `ultramarine` | 0.16 |
| `burnt_sienna` | 0.21 |
| `viridian` | 0.22 |
| `cerulean` | 0.30 |
| `cadmium_red` | 0.42 |
| `yellow_ochre` | 0.56 |
| `cadmium_yellow` | 0.75 |
| `lemon_yellow` | 0.83 |
| `titanium_white` | 0.95 |

**The floor is about `0.13`, and it is the pigments', not the model's.** Mixing never
takes a channel below the darker of its two ingredients, so the swatches set it: this
is the value of the darkest mixture the box can reach.

**It is a much lower wall than it looks, because of what `0.10` means.** A cell passes
within `0.10` of the reference, so **anything the reference puts at `0.03` or above is
reachable with the paint in the box** — you have to *cover* the cell to get there, at
`density=1.0` and full load, with the darkest mixture and nothing lighter showing
through. A dim reference measured in a rehearsal put 17 of its 64 cells below the
floor — a third of the picture — and every one of them landed inside tolerance, worst
at `+0.09`. The margin is real and thin: one light mark inside such a cell spends all
of it. Cover properly before concluding a supplied colour is needed.

`color.py`'s `0.01` reflectance floor is a separate thing and is not a floor on the
picture. It clips the K/S *arithmetic*, where finding 5 needs it, and comes back off
the mixture weighted by how much of each ingredient is in it, so a colour the painter
supplies below it is laid as written -- a literal `#000000` renders as `#000000`.
Before M8b it did floor the answer, and the number quoted here was `0.10` on that
basis.

`mix("ultramarine", "burnt_umber", 0.5)` reads `0.14` (`#21232d`) and is the bottom
of your range -- darker than any single pigment, because each channel takes the
darker side from a different ingredient. Vary the ratio and it holds that value
while swinging cool to warm: `0.3` is `#1f2434`, `0.7` is `#24231f`.

Mixing still cannot go *below* the darkest ingredient in any one channel, so piling
paint on does not help: eight dried passes of the darkest mix measure `0.129`
against one pass at `0.133`, four rounds of glazing `0.132`. If a mass is not dark
enough, mix it darker.

Before M6b these swatches were colour-chart brights rather than masstones --
`burnt_umber` was `#4A3728` -- and the box floored at `0.23` with no mixture below
it. That is the number any older text quotes, and `compare()`'s `unreachable` split
is what is left of the tooling built around it.

### The value scale

Nine even steps from the darkest mix to white, mixed to a value rather than to a
ratio (guide exercise 1). The white ratio each step needs:

| Step | Value | White |
|---|---|---|
| 1 | 0.14 | 0.00 |
| 2 | 0.24 | 0.33 |
| 3 | 0.34 | 0.51 |
| 4 | 0.45 | 0.63 |
| 5 | 0.55 | 0.72 |
| 6 | 0.65 | 0.80 |
| 7 | 0.75 | 0.86 |
| 8 | 0.86 | 0.93 |
| 9 | 0.96 | 1.00 |

Rendered, the nine bands measure `0.148` to `0.951` in steps of `0.100`, even to
within `0.002`. The curve in the third column is the useful part: a third of a
canvas of white buys the first step and it takes nine tenths to reach the eighth,
which is why a mixture that *should* be halfway comes out too dark, and why the fix
is always more white than feels right.

### Tinting and mixing

- White is a weaker lightener than you expect. For a really pale colour use a
  white ratio of about `0.7`, not `0.4`.
- A yellow and a blue make green even when you were after a grey, and tinting does
  not undo it: `tint(mix("yellow_ochre", "cerulean", 0.3), 0.5)` is `#a8b278`, a
  pale green. Neutral greys come from complements or from earth and white:
  `tint(mix("ultramarine", "burnt_sienna", 0.5), 0.7)` is a cool grey (`#968e90`),
  `mix("burnt_umber", "titanium_white", 0.6)` a warm one (`#776157`), and
  `desaturate(c, 0.5)` pulls any mixture toward grey at the same value.
- The mixing model is a Kubelka-Munk power mean of K/S with exponent `0.35`
  (`src/easel/color.py`); the optional Mixbox backend is better and is opt-in for
  licence reasons. The exponent is what gives white its tinting strength: it is set
  so that a 50/50 mix with white carries a colour about a quarter of the way up the
  palette's value range, and it moved from `0.5` in M6b because darkening the
  masstones widened that range. Lower it further and yellow + blue loses its green.

---

## Graphite under paint

Paint buries the pencil in proportion to how much paint actually lands. On a pencil
line at `pressure=0.8`, one pass leaves:

| Stroke `opacity` | Graphite left |
|---|---|
| 0.04 | 79% |
| 0.10 | 55% |
| 0.18 | 34% |
| 0.30 | 19% |

`density` on `block_in` does **not** thin the paint — it only spaces the passes
out, and each pass lands at full strength. A seven-stroke scumble at `density=0.3`
takes a drawing off completely. Thin means `opacity`.

A dab the canvas tooth refused leaves the drawing untouched, which is why an
underdrawing survives under a dry-brush pass and in the ground.

---

## Wetness

- Paint lands at roughly `0.7` wetness.
- Every mark made anywhere on the canvas takes about six percent off what is left,
  so half of it is gone after about eleven strokes.
- One `block_in` is ten to thirty strokes with a medium brush, so by the time a
  second mass is blocked in, the first is most of the way dry.

If two colours are meant to mix on the canvas, the second has to go down within a
few strokes of the first. `dry()` takes wetness to zero (or by `amount`, or in a
`region`).

---

## Load and run-out

- Brushes start loaded: `bristle` at `0.9`, the rest at `1.0`.
- The window for a deliberately broken mark is roughly `load=0.4` to `0.6`. Below
  about `0.35` a `bristle` brush leaves almost nothing. `flat` and `knife` keep
  marking further down; `bristle` is the most texture-sensitive.
- A pass laid at `0.5` because it sounded painterly leaves a speckled film that
  everything after it sits on. Anything meant to read as a solid mass wants
  `load=1.0`.
- **`density` spaces the passes; it does not fill them.** `density=1.0` reads as a
  request for solid paint and is not one — each pass still runs dry along its own
  length. Measured on 38 passes of a `flat` at `size=0.030` over `umber_wash`,
  sampling the interior a brush in from the edges:

  | 38 passes at `density=1.0` | interior sd | within `0.05` of bare ground |
  |---|---|---|
  | as laid | `0.063` | `4.4%` |
  | `solid=True` | `0.007` | `0.0%` |

  Nine times more even for the same 38 strokes and the same money. `solid=True` is
  `load=1.0, load_falloff=0.0` as a pair of defaults, so an explicit `load=` beside
  it still wins. The painter who found this laid a whole near mass speckled and only
  saw it by cropping into it.
- **`opacity` does not thin a long stroke, it only slows it down.** Consecutive dabs
  overlap by more than 90%, so a low opacity accumulates back to nearly full colour
  along the mark. A rehearsal run laid grain at `opacity=0.08` expecting a whisper and
  got bold stripes, which cost it a whole repaint of the mass underneath. Working
  numbers: `stroke(opacity=0.04)` is nearly invisible; a visible soft film is
  `glaze(opacity=0.10)`, which is built for it. Same accumulation as the light end of
  a taper being thin rather than faint — see *Pressure*.
- A fully loaded `bristle` stroke covers about three-quarters of its own width, in
  a comb of parallel streaks. Above about `size=0.12` those streaks print wider than
  anything in the picture, and every stroke prints the same ones.
- A `bristle` stroke the full width of the canvas at `size=0.12` is about
  three-quarters solid where it starts and, on `rough`, under half by its last
  quarter; on `linen` and `smooth` it loses about a fifth. `load_falloff=0.25`
  keeps a canvas-wide stroke even from end to end; `0.0` never runs dry; the
  default is right for marks a brush-length or three long.
- The texture decides the breakup: `rough` skips in chunky islands, `linen`
  speckles at the scale of the weave, `smooth` leaves broader open gaps.
- `s.log()` reports how much paint each mark actually laid, and prints
  `NO PAINT LANDED` for one that changed nothing.

---

## `block_in`

- It lays a pass for every brush-width of the region, so one call is ten to thirty
  strokes, and each pass runs about a third of a brush past the region's ends
  (`overhang=0.35`). The first and last rows sit a quarter of a brush outside it. A
  region blocked in at `size=0.1` comes out roughly `0.05` wider than asked on the
  sides and `0.025` taller.
- `overhang=0` keeps the ends within a fifth of a brush of the region.
- **`overhang` moves the ends of each pass and nothing else.** Measured on a band at
  `x 0.2–0.8, y 0.585–0.775`, `bristle` at `size=0.11`, passes horizontal:

  | `overhang` | paint spans (ends) | paint spans (sides) |
  |---|---|---|
  | `0` | `x 0.181–0.825` | `y 0.530–0.844` |
  | `0.35` (default) | `x 0.145–0.854` | `y 0.530–0.844` |
  | `1.0` | `x 0.072–0.924` | `y 0.529–0.850` |

  The sides do not move: they sit about half a brush past the band whatever
  `overhang` is, because that is the brush hanging over a pass whose *centre* stopped
  at the boundary. To hold a mass off its neighbour at the same depth, `inset()` the
  place by half the brush. `overhang=0` is not a substitute and never was.
- **`edge="clean"` pulls the paint back to the drawn line**, by insetting the fill
  half a brush and sweeping one pass along that inset outline, for one stroke more
  than the same mass ragged. Measured on a mass a third of the canvas across, furthest paint outside
  the outline:

  | Tip at `size=0.05` | ragged | clean |
  |---|---|---|
  | `round_hard` | 20.0px | 13.0px |
  | `round_soft` | 18.4px | 12.8px |
  | `flat` | 26.6px | 12.3px |
  | `bristle` | 29.5px | 13.3px |

  It cuts the spill on every tip, but only a *solid* tip also comes out smoother: on
  a comb the single contour pass is stringy — one bristle pass covers about
  three-quarters of its width — and the silhouette ends up rougher than the ragged
  fill's, which is why asking for a clean edge with a bristle says so.
- **The inset stops at the canvas frame.** Where an outline runs off the canvas there
  is no drawn line for the brush's outer half to land on, and holding the fill half a
  brush inside the frame leaves a strip of bare ground along it. Measured on a
  full-width mass drawn from `y 0.70` past the bottom to `1.05`, a `flat` at
  `size=0.09`, laid solid so that what is measured is where the fill stopped:

  | bottom row of the canvas | left unpainted |
  |---|---|
  | inset all the way round | `15.1%` |
  | ragged | `3.6%` |
  | inset except at the frame | `0.3%` |

  Better than ragged, because the contour pass runs along the frame too. A mass that
  meets the frame should run off it: draw it past the edge and let it.
- Successive passes run in opposite directions on their own, so a mass does not
  fade toward the side the brush ran out on.
- `direction=` takes `"horizontal"`, `"vertical"`, `"diagonal"` (45°), `"cross"`,
  `"axis"` (the place's own long axis), a number of degrees clockwise from
  horizontal, or a sequence of any of those for one pass each.
- **The part-brush step assumes a pass is one brush wide all along it, which is
  true of every tip except a round one under a varying pressure.** The step at full
  density is `0.55 * size`; a round tip at the default `taper` is `0.53 * size` at
  the ends of each pass, so there the passes stop touching and the mass shows them.
  This is why masses are laid with `flat` or `bristle`. If you want a round tip for
  one, pass `pressure="even"` and the old behaviour is back. `sweep` steps by the
  same rule and has the same caveat — its golden case shows it, deliberately.

### Laying a mass along its own axis

Measured on the same sloping mass (share of strong edges within ten degrees of
horizontal or vertical — higher is squarer; `python scripts/probe_sweep.py` computes
it):

| The same mass | Axis-aligned edges | Strokes |
|---|---|---|
| `block_in` box, canvas axes | 24.7% | 21 |
| columns dropped from the silhouette | 34.8% | 37 |
| passes swept along the slope | 20.3% | 17 |
| swept along the slope, tip pinned to it | 22.4% | 17 |

Running the passes along the form is the whole win: fourteen points squarer to
less, and twenty fewer strokes. Pinning the tip on top of that matters on short
marks and at the ends of long ones, not along their length.

### Shaped masses (M8)

`block_in` fills a shape as readily as a rectangle: `blob`, `ellipse`, `hull`,
`ribbon`, `polygon`. The passes are cut against the outline, so a mass with a
silhouette keeps it, and a concave one comes back in pieces rather than being
painted across. Measured on a blob covering `0.23` of a 900×675 canvas, against the
`0.32` box around it:

| | Shape | Its box |
|---|---|---|
| passes at `size=0.06` | 14 | 15 |
| passes at `size=0.12` | 7 | 7 |
| passes at `size=0.16` | 5 | 6 |
| default `overhang` | `0` | `0.35` |

- **A shaped mass costs its box along the passes' normal, times the number of times
  a pass line crosses it.** Both factors, not just the first. The passes are counted
  across the extent of the mass, not over its area — but each pass is then cut
  against the outline, and a pass that crosses a concave shape comes back as the two
  or three pieces really inside it, each of which is charged as a stroke.

      strokes  =  (extent along the passes' normal / part-brush)  ×  crossings

  Measured at brush `0.015`, density `1.0` (part-brush `0.00825`):

  | Shape | extent | passes | **strokes** | crossings |
  |---|---|---|---|---|
  | `ribbon`, straight, `0.029` wide | `0.029` | 4 | **4** | 1.00× |
  | `ribbon`, curved, `0.029` wide | `0.342` | 42 | **75** | 1.79× |
  | `ellipse`, convex | `0.400` | 48 | **48** | 1.00× |
  | concave, a bite out of one side | `0.400` | 48 | **78** | 1.62× |

  The first factor is the one a curved `ribbon` shows most loudly: the box a bend
  sweeps out is ten times the band's own width, so a mass `0.029` across costs what
  a mass `0.342` across costs. The second is invisible on every convex shape and is
  why the earlier version of this entry — *"a shape and its box come out within a
  pass of each other"* — was wrong on anything with a bite in it: such a shape runs
  30 strokes past its box, not one. The tell was already in the table above it, which
  recorded a curved ribbon at 19 passes beside a painter who paid **21**.

  **Neither factor is one to work out by hand: ask `s.cost(...)`**, which walks the
  passes without laying them and returns exactly what `block_in` or `sweep` will
  charge. It is on every `preview` overlay too. A painter budgeted 4 for a curved
  ribbon and paid 21, which was 7% of its stroke budget on a single call.
- **Coverage at `density=1.0` is 99% of the shape**, at every brush size tried
  (`0.06` to `0.20`) — **measured on a blob, which is convex.** It does not carry
  over to a concave shape that has been `inset()`, because erosion pulls in from
  every boundary at once and a lobe narrower than twice the inset vanishes whole.
  On a real fifteen-point outline, `inset(0.052)` kept **62.7%** of the area; the
  block-in covered 98.4% of what it was handed and **76.2% of the mass intended**,
  with one limb at 15.5%. **Preview the inset shape, not the shape.**
- **Paint stops within three-quarters of a brush width past the silhouette.** The
  pass *centres* stop at the boundary — that is what `overhang=0` means — and the
  brush spreads half its width beyond, plus the pass wander. There is no second edge
  out there: it is the same ragged spill a block-in has always had at its ends.
- **So the brush has to be small relative to the mass, or the shape inset.** A mass
  `0.32` across blocked at `size=0.12` puts paint `0.06` outside the drawing on every
  side and the silhouette is simply gone, taking its neighbours with it; the same mass
  inset `0.045` and blocked at `size=0.09` lands on the drawing. Keep the brush under
  about a fifth of the mass's width, or `inset()` by half the brush size — it works on
  `polygon`, `ellipse` and `ribbon` alike. A rehearsal run lost 72 strokes and its
  only `undo` to this, which makes it the most expensive first mistake with
  shapes on record.
- **One sweep leaves the boundary stringy**, because a bristle brush covers about
  three-quarters of its width. `direction=("axis", 90)` crosses it and closes it up,
  at twice the passes (7 → 17 on the blob above). **On a small mass, don't**: the two
  pass directions meet the outline at different angles and serrate it into a sawtooth.
  The crossing is for masses several brushes across.
- **`"axis"`** resolves to the long axis of the outline, weighted by edge length:
  `-35.5°` for a ribbon from `(0.15, 0.8)` to `(0.85, 0.3)`, `0°` for a wide
  ellipse, `90°` for a tall rectangle.

Five masses of a 900×675 painting, sized `0.06`–`0.17`, come to 46 passes; the same
composition laid as the boxes around those masses came to 53, and looked like boxes.
Measured on that pair: **17.8% of the boxed painting's paint landed outside the
masses it was meant to lay, against 10.7% of the shaped one** — and most of that
10.7% is the brush's own half-width spill past every silhouette, which is paint in
the right place. The axis-aligned edge share moved less, 27.5% to 25.0%, because
most of the strong edges in either picture are the bristle comb's streaks along the
passes rather than the boundaries of masses; read that number with the pictures, not
instead of them.

**A shape or a sweep?** They answer different questions. `block_in(shape)` fills a
mass whose *silhouette* you can name, with straight passes cut against it.
`sweep(edge)` follows one *boundary* you have read off the reference and steps
inward from it, so the passes describe the form rather than crossing it — and it
needs no closed shape. A shape's own outline can be swept: `shape.closed` is a loop,
which `sweep` detects. The numbers for that are in the next section.

---

## `sweep`

`block_in` fills a place — a rectangle, or a shape, with the passes cut against its
outline (above). `sweep` is the other way of laying a mass that has a silhouette:
passes *along* its boundary, stepped into the mass one part-brush at a time.
Everything below is `scripts/probe_sweep.py` on one arbitrary five-point boundary — not a subject —
at `depth=0.34` with a bristle brush at `0.13`, on a 520×400 canvas.

| The same mass | Strokes | Axis-aligned edges | Paint outside the shape | Value spread inside it |
|---|---|---|---|---|
| `block_in` over the bounding box | 5 | 35.9% | 19.4% | 0.047 |
| `sweep` along the boundary | 5 | 20.9% | 6.5% | 0.031 |
| `sweep`, crossed at 26° | 17 | 21.8% | 6.5% | 0.011 |

Read it as three separate claims:

- **The shape.** A box drawn round this boundary puts a fifth of its paint on the
  wrong side of it, and comes out fifteen points squarer by the axis-alignment
  metric (the one from the M6 pass, above). Both are permanent: no later work takes
  a box's corners out again. Blocking in the *shape* rather than its box fixes the
  first of those without a sweep at all; sweeping also changes what the passes
  describe.
- **The cost.** Nothing, for the shape. Both versions are five strokes, because a
  pass is a pass whether it runs along an edge or across a rectangle.
- **The crossing.** One sweep leaves the mass stringy — a bristle brush covers
  about three-quarters of its width, and the gaps show as a value spread of `0.031`
  a part-brush inside the boundary. Crossing at 26° takes that to `0.011` and lays
  the mass about a hundredth darker for twelve more strokes. It does not move the
  silhouette: the paint outside the shape is unchanged.

The two shape columns are geometry and did not notice M6b; the two value columns
are a third of a value lower under the darkened masstones than they were before it,
and the crossing still takes two thirds of the spread out.

Do not read the last column as *lower is better without limit*. A mass with no
variation left in it is a flat fill, which is the loudest tell there is; `0.011` is
still visibly brushwork, and the sheet the probe writes is there to check that by
eye.

### Spacing, depth and how many passes

- Passes step **one part-brush** apart: `size × (1 − 0.45 × density)`, the same rule
  `block_in` spaces its passes by. At `density=1.0` that is `0.55` of the brush
  width. The recipe this call replaced stepped `0.27` of a brush width, which is
  `density≈1.6`.
- `depth` and the step are in **normalised canvas units**, so on a canvas that is
  not square a sweep stepped `"down"` steps in fractions of the *height* while the
  brush is measured against the *long side*. On 520×400 a `0.0715` step down is 29
  px against a 68 px brush — tighter overlap than the same sweep run left to right.
  `block_in` has always mixed the two units the same way.
- Left alone the brush decides how many passes a depth takes: `round(depth / step)`.
  `passes=` says instead, and pins the spacing at `depth / passes`.
- A crossed sweep is roughly three times the strokes of a plain one at 26°, and more
  as the angle steepens: the second set is spaced `step / cos(angle)` apart but has
  further to run.

### Sweeping deeper than the mass

Offsetting a closed boundary inward eventually runs it past its own centre. `sweep`
drops the folded part and stops when nothing is left, so asking for too much depth
costs strokes that are never laid rather than a scribble in the middle. A boundary
of radius `0.20`, bristle at `0.13`:

| Depth asked for | Passes it works out to | Passes actually laid |
|---|---|---|
| 0.10 | 1 | 1 |
| 0.20 | 3 | 3 |
| 0.40 | 6 | 4 |
| 0.90 | 13 | 4 |

---

## `smudge`

- **It is much stronger than "moves paint around" suggests, and it is not symmetric**:
  it pulls the *lighter* mass into the darker one more than the reverse, so a smudge
  run along a light/dark boundary walks the boundary into the dark side.
- At `size=0.10` it drags finger-shaped lobes several cells long and reads as a
  thumbprint through the paint. **`0.035`–`0.045` behaves**; anything larger wants a
  `rehearse()` first. A rehearsal run lost a whole mass to seven smudges at `0.10`.
- **Inside that window it removes about 40% of a join, once, and repetition undoes it.**
  The steepest value step across a hard join, per 1% of canvas height:

  | | join sharpness |
  |---|---|
  | bare join | `0.330` |
  | smudge `0.035`, one pass | `0.214` |
  | smudge `0.040`, one pass | `0.184` |
  | **smudge `0.040`, three passes** | **`0.280`** |

  So *behaves* means *helps once*. It is not a blender and it will not finish a join.
  Four painters in one run called it the advice that cost them most, all four having
  reached for a second and third pass when the first did not close the join. When one
  pass is not enough the answer is paint — overlapping strokes at closely spaced
  values — not another smudge.
- **It works along a boundary and fails across one.** Dragged across, it pulls a lobe
  of the lighter mass into the darker and leaves a finger-shaped thumbprint; run along
  the boundary in short passes it does what it is for.
- **"Along" means along the boundary's *shape*, and only a straight boundary is two
  points.** On a straight sloping edge, two points and four along it are the same pass
  to the pixel — the spline through collinear points is the line. On a boundary that
  *bends*, they are not. One pass at `size=0.040` over a 1024×768 canvas, boundary
  position measured per column before and after:

  | one pass along a bend | boundary moved, mean | worst |
  |---|---|---|
  | its two ends (the chord) | `0.51%` of canvas height | `2.9%` |
  | four points along the curve | `0.01%` | `0.7%` |
  | eight points | `0.01%` | `0.5%` |

  A two-point pass on a curve begins along the boundary and ends across it. The
  session that found this had believed the tool could not follow a curve at all; it
  can, and had been given two points because every example in the guide had two.
  `smudge` also takes a shape or a region and walks its own outline, which is the
  sampling-by-hand step a painter skips.
- It counts against `s.stroke_count`, as `glaze` does.

---

## `scumble`

What closes a join a smudge only softened: `n` overlapping passes at closely spaced
values, charged as `n`.

**The default grades edge to edge, which is a band and not a glow.** Nine passes over
the same round patch, `bristle` at `size=0.07`, read off the values view:

| nine passes over one patch | across it | down its middle |
|---|---|---|
| `direction="axis"` (a band) | `0.90, 0.56, 0.51, 0.23, 0.17` | flat to within `0.01` |
| `direction="inward"` | `0.20, 0.41, 0.91, 0.32, 0.17` | `0.30, 0.42, 0.86, 0.91` |

So a band is one ramp and a centred passage is a fall-off from the middle in every
direction — which is what a glow, a bloom or a lit patch on a surface is, and what
the guide had no recipe for. The rings run **round** the place, stepping in a
part-brush at a time from its boundary toward its centre, in `sweep`'s geometry; the
first ring lands on the boundary, so `color_a` is the value the patch meets its
surroundings at.

A ring is two or three times the length of a pass across the same patch and has no
far end to run dry at, so a centred scumble defaults to `load_falloff=0.0`; without
it the brush starves half way round and the glow comes out bright on one side. An
explicit `load_falloff=` still wins.

---

## Pressure

Pressure shapes how heavily paint lands along the stroke, and on a **round** tip —
`round_hard`, `round_soft`, `liner` — how wide the mark is. `size` is the width at
full pressure; a light touch keeps a third of it, plus a floor of 0.75 px of radius
so a fine line thins rather than disappearing. Measured on `round_hard` at
`size=0.06` on a 600 px canvas:

| pressure | width | paint landed |
|---|---|---|
| 0.10 | 14 px | 2 080 |
| 0.25 | 18 px | 7 441 |
| 0.50 | 24 px | 23 234 |
| 0.75 | 30 px | 46 471 |
| 1.00 | 36 px | 79 538 |

The **oriented** tips — `flat`, `bristle`, `knife` — keep their chisel: 60 px at
pressure 0.2 and at 1.0 alike, because a flat brush's width is the mass it lays.

The named profiles, widest and narrowest point of one stroke, same brush:

| profile | widest | narrowest |
|---|---|---|
| `even` | 36 px | 36 px |
| `taper` | 36 px | 26 px |
| `press_in` | 36 px | 20 px |
| `lift_off` | 36 px | 20 px |
| `swell` | 36 px | 24 px |
| `dab` | 36 px | 20 px |

A hand-written profile goes further than any named one: `pressure=[1, 0]` on a
`liner` at `size=0.02` runs 12, 10, 8, 6 px along its length. A mark that tapers is
one stroke, not two of different sizes.

- On a long stroke the overlapping dabs saturate, so `taper` and `even` land much
  the same *weight* even where they differ in width. The paint half of the profile
  shows most clearly on short strokes, and on a colour that is not already at full
  strength against its background. Exercise 2 in the guide uses `opacity=0.35` and
  `load_falloff=0.0` to get both out of the way.
- The light end of a taper is *thin*, not faint: dabs overlap by more than 90%, so
  it still accumulates to nearly full colour.

---

## At the scale of a feature

- A `round_hard` line keeps its width down to about three pixels of the long side
  (`size=0.003` on a 1200-wide canvas), at full strength.
- **A single dab is a light touch.** A lone dab is the *start* of the default
  `taper`, so its pressure is 0.28: it lands about a quarter of the way to its
  colour and, since a round tip's width follows its pressure, at about half the
  width asked for. `dab(press=n)` stamps the same spot n times inside one mark, with
  the profile running across the stamps, so three of them press through full
  pressure in the middle one. White at `size=0.06`, measured on three grounds:

  | stamps | on `toned_grey` | on `umber_wash` | on `warm_white` | width |
  |---|---|---|---|---|
  | 1 | 0.17 | 0.12 | 0.26 | 12 px |
  | 2 | 0.31 | 0.24 | 0.43 | 12 px |
  | 3 | **0.84** | **0.80** | **0.87** | 24 px |
  | 5 | 0.92 | 0.90 | 0.93 | 23 px |

  Fractions of the way from the ground to the colour. A catchlight is `press=3`,
  and it costs one stroke; three *separate* dabs reach 0.45 on `toned_grey` and
  cost three.
- **Scale a mark off the thing it describes, not off the canvas.** Inside a mass
  `0.3` of the canvas across, a plane within it wants about `size≈0.015–0.025` and a
  detail within that plane `0.004–0.010`. Carrying "use a bigger brush than feels
  comfortable" — which is advice about masses — down to this scale costs a repaint;
  A rehearsal run did it three times and put the cost at about forty strokes.
- **An oriented tip does not taper under a pressure list.** On a `flat`,
  `pressure=[1.0, 0.25]` fades the paint without narrowing the mark, so a short one
  comes out as a bar with a weak end rather than a stroke that tapers. Width follows
  pressure on the round tips only (see *Pressure*), which is why a small accent wants
  `round_hard`.
- A fine line runs dry over the same *distance* as a fat one, which is far more
  brush-lengths, so it lasts.
- A `region=` crop is at full resolution and a small one is enlarged to at least
  800 px, so a single cell shows at five times or more. On a 1200-wide canvas one
  cell is 150 px.
- Three `knife` marks two values lighter than the mass under them read as three
  things stuck to the surface, not as paint. Keep a knife mark close in value to
  what it lands on and let a later stroke or a `smudge` break one of its ends.

---

## The bristle comb

A bristle has a width of its own — `BRISTLE_PITCH`, 0.005 of the canvas long side —
and the count follows the brush, so a wider brush prints more streaks rather than
fatter ones. Measured on a 900 px canvas:

| `size` | tip | bristles | comb pitch |
|---|---|---|---|
| 0.02 | 18 px | 4 | 4.5 px |
| 0.04 | 36 px | 8 | 4.5 px |
| 0.08 | 72 px | 16 | 4.5 px |
| 0.12 | 108 px | 24 | 4.5 px |
| 0.18 | 162 px | 36 | 4.5 px |

Before M7 the count was 22 at every size, so the pitch ran 3 px at `size=0.02` to
26 px at `size=0.18` — the brush's signature rather than the mark's.

The pitch being fixed in canvas units is what puts a floor under the brush: at
`size=0.02` a bristle mark is four streaks with gaps between them rather than a
covered mark. That is right for a few strands and wrong for a small solid plane,
which wants `flat` at `pressure="even"` or `round_hard` instead.

The comb — spacing, phase, and which bristles are missing — is drawn once per
stroke and held for all of that stroke's dabs, so striations stay put along a mark
and differ from the next mark's. Two strokes of one brush used to be identical to
the last bit; their combs now correlate +0.39, −0.05 and +0.33 over three pairs.

The pitch is the comb in the tip. What *reads* on a fully loaded straight stroke is
coarser, because consecutive dabs overlap by more than 90% and fill the weaker
bristles in, so only the missing ones show — two to seven streaks across a mark, at
any size. The comb shows at its own scale where the stroke is starved or the tooth
is biting. `bristle_count` still pins a comb if you want a fixed one.

**The round tips repeat themselves, and `tip_wobble` is the same idea for them.** Two
`dab(press=3)` marks at `size=0.05`, each silhouette cropped to its own box and laid
over the other, as a share of the area either covers:

| `round_hard`, two marks | silhouettes shared |
|---|---|
| as it is | `97%` |
| `tip_wobble=0.35` | `87%` |
| `tip_wobble=0.7` | `76%` |
| `tip_wobble=1.0` | `67%` |

So five small round marks are five copies of one disc unless something redraws the
outline, which is what a painter who wanted a small irregular mark fifteen times ran
into — and answered by inventing a short fat stroke from a starved bristle. The
wobble is three low harmonics round the tip, drawn per *stroke* the way the comb is,
and it swells as far as it bites so the mark keeps the size it asked for. Do not
compare tips with this instrument: a thin tip's overlap falls faster for the same
jitter, so it ranks thinness as much as repetition.

---

## Budget

A whole painting is usually a few hundred marks, not a few thousand. `s.stroke_count`
keeps the tally; `pencil()`, `erase()`, `mark()`, `look()`, `preview()`, `rehearse()`
and `compare()` do not count. **`smudge()` and `glaze()` do** — they are marks like any
other, and a rehearsal run measured that (297 → 299 for two smudges) with three
strokes of budget left.

**A mass can be costed before the call rather than discovered after it.** Passes step
`size × (1 − 0.45 × density)` apart, so a mass takes about `extent / step` of them,
times about three if crossed:

```python
step = 0.12 * (1 - 0.45 * 0.9)      # size=0.12, density=0.9  ->  0.071
passes = 0.32 / step                # a mass 0.32 across       ->  about 5
```

Or do not do the arithmetic: `s.cost(plan)` walks the same passes and returns the
number, and `s.paint(plan)` then charges exactly it — the two go through one code
path so a quote and a bill cannot drift apart.

**The session can hold the split.** `Session(budget=300)` makes `s.spent`,
`s.remaining` and `s.budget_line()` say where the painting is, `easel run` print it
after every pass, and `s.cost(plan)` warn when one plan would take more than a
quarter of what is left (`share=` moves the line, `share=0` silences it). Nothing is
refused when the budget runs out: it goes negative and says by how much. A budget is
the painter's plan for the picture, not a lock on the engine.

**`scumble(band, a, b, n)` costs exactly `n`** on a band whose silhouette is convex,
which is what makes a soft passage something that can be budgeted before it is laid.
On a concave shape a pass line is cut into the pieces really inside it, the same way
`block_in` cuts one, so it costs a little more. `direction="inward"` costs `n` too —
`n` rings stepping in from the boundary — less any that folded in on themselves past
the middle.

**Crossing a direction is where a price runs away, and it is one cause wearing three
hats.** The same shape, one direction against crossed, `bristle` at `size=0.05`: a
thin full-width band **5 → 41**; a small concave shape **12 → 32**. And a ribbon
`0.032` wide at `size=0.015`: **4** straight, **75** with a bend in it. All three are
the same thing — the passes step across the *bounding box*, once per direction, and
each pass line comes back as however many pieces of it lie inside the shape.
`s.cost_line(plan)` says which of the three a number is:

```
75 strokes -- 25% of the 300 left of a 300-stroke budget
  75  42 passes stepping across 0.34 of the canvas, each cut into 1.8 pieces by the outline
```

The same sentence rides on the budget warning, naming the entry that dominates the
plan. A painter who has the number but not the cause redesigns the mass; the levers
are a wider brush, a thinner `density`, and one direction instead of two.

**`edge="clean"` costs one stroke more than the fill it replaces** — and the fill
itself is slightly cheaper, because it is laid into the shape inset by half a brush.
`cost()` prices both halves.
