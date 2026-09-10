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

**The floor is about `0.13`, and it is the model's, not the pigments'.** Nothing in
this engine reflects less than `0.01` linear -- the floor in `color.py` that keeps
mixtures behaving like paint -- and `0.01` is value `0.10`. The box stops three
hundredths above it, and those three hundredths are hue: a dark that is still blue,
or still brown, cannot sit on the floor in all three channels at once.

`mix("ultramarine", "burnt_umber", 0.5)` reads `0.14` (`#21232d`) and is the bottom
of your range -- darker than any single pigment, because each channel takes the
darker side from a different ingredient. Vary the ratio and it holds that value
while swinging cool to warm: `0.3` is `#1f2434`, `0.7` is `#24231f`.

Mixing still cannot go *below* the darkest ingredient in any one channel, so piling
paint on does not help: eight dried passes of the darkest mix measure `0.129`
against one pass at `0.133`, four rounds of glazing `0.132`
(`rehearsal3/probe_value_floor.py`). If a mass is not dark enough, mix it darker.

Before M6b these swatches were colour-chart brights rather than masstones -- 
`burnt_umber` was `#4A3728` -- and the box floored at `0.23` with no mixture below
it. That is the number the older parts of this repo quote, and `REVIEW.md`
findings 21 and 33 are the history.

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
- Successive passes run in opposite directions on their own, so a mass does not
  fade toward the side the brush ran out on.
- `direction=` takes `"horizontal"`, `"vertical"`, `"diagonal"` (45°), `"cross"`,
  a number of degrees clockwise from horizontal, or a sequence of any of those for
  one pass each.

### Laying a mass along its own axis

Measured on the same sloping mass with `rehearsal3/probe_axis_alignment.py` (share
of strong edges within ten degrees of horizontal or vertical — higher is squarer):

| The same mass | Axis-aligned edges | Strokes |
|---|---|---|
| `block_in` box, canvas axes | 24.7% | 21 |
| columns dropped from the silhouette | 34.8% | 37 |
| passes swept along the slope | 20.3% | 17 |
| swept along the slope, tip pinned to it | 22.4% | 17 |

Running the passes along the form is the whole win: fourteen points squarer to
less, and twenty fewer strokes. Pinning the tip on top of that matters on short
marks and at the ends of long ones, not along their length.

---

## `sweep`

`block_in` fills a rectangle; `sweep` lays a mass that has a silhouette, as passes
along its boundary stepped into the mass one part-brush at a time. Everything below
is `scripts/probe_sweep.py` on one arbitrary five-point boundary — not a subject —
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
  a box's corners out again.
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

## Pressure

Pressure shapes how heavily paint lands along the stroke. **It does not change the
width of the mark** in the current engine: a stroke at `pressure=0.2` covers the
same width as one at `1.0` and lays less paint. Consequences:

- On a long stroke the overlapping dabs saturate, so `taper` and `even` come out
  looking much the same. The profiles show most clearly on short strokes, and on a
  colour that is not already at full strength against its background. Exercise 2
  in the guide uses `opacity=0.35` and `load_falloff=0.0` to get both out of the
  way.
- A mark that tapers in width is two strokes of different sizes.

This is scheduled to change (M7 in `painting-api-brief.md`: width following
pressure for the round tips). When it does, this section and the guide's pressure
paragraph are rewritten, not patched.

---

## At the scale of a feature

- A `round_hard` line keeps its width down to about three pixels of the long side
  (`size=0.003` on a 1200-wide canvas), at full strength.
- A single dab lands at about a third of its colour's strength. A small highlight
  is two or three dabs on the same spot.
- A fine line runs dry over the same *distance* as a fat one, which is far more
  brush-lengths, so it lasts.
- A `region=` crop is at full resolution and a small one is enlarged to at least
  800 px, so a single cell shows at five times or more. On a 1200-wide canvas one
  cell is 150 px.
- Three `knife` marks two values lighter than the mass under them read as three
  things stuck to the surface, not as paint. Keep a knife mark close in value to
  what it lands on and let a later stroke or a `smudge` break one of its ends.

---

## Budget

A whole painting is usually a few hundred marks, not a few thousand. `s.stroke_count`
keeps the tally; `pencil()`, `erase()`, `mark()`, `preview()` and `rehearse()` do not
count.
