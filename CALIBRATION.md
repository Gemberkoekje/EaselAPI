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
| `burnt_umber` | 0.23 |
| `ultramarine` | 0.26 |
| `alizarin` | 0.30 |
| `burnt_sienna` | 0.33 |
| `viridian` | 0.39 |
| `cerulean` | 0.42 |
| `cadmium_red` | 0.48 |
| `yellow_ochre` | 0.58 |
| `cadmium_yellow` | 0.79 |
| `lemon_yellow` | 0.88 |
| `titanium_white` | 0.96 |

**The floor is about `0.23`, and it is the pigments, not the mixing.** Mixing in
this engine never takes a channel below the darker of its two ingredients, so no
mixture is darker than the darkest thing in the box. `ultramarine` + `burnt_umber`
at 50/50 reads `0.226` — a hair under umber alone. Eight dried passes of the darkest
mix measure `0.231`, four rounds of glazing `0.234`, all five darks mixed together
`0.228` (`rehearsal3/probe_value_floor.py`). The pigment swatches are simply lighter
than real tube masstones; real ultramarine and burnt umber mixed go close to black,
and these do not. That is an engine limit, and phase M6b in `painting-api-brief.md` darkens
the pigments to fix it. Until it lands, `compare()` marks cells below reach with
`~` and leaves them out of `fixable`.

### If you want to map a reference's range onto the palette's

Not a rule — one way to plan the three values when the reference runs darker than
the box does. Read the reference's lightest and darkest cell off `compare()` on the
empty canvas, decide what they become on your canvas, and place the rest
proportionally:

```python
lo, hi = 0.23, 0.94              # what the palette reaches
ref_lo, ref_hi = 0.06, 0.59      # what the reference runs, from compare()
def mine(v):                     # where a reference value lands on your canvas
    return lo + (hi - lo) * (v - ref_lo) / (ref_hi - ref_lo)
```

Relationships are what read; absolute values are not.

### Tinting and mixing

- White is a weaker lightener than you expect. For a really pale colour use a
  white ratio of about `0.7`, not `0.4`.
- A yellow and a blue make green even when you were after a grey, and tinting does
  not undo it: `tint(mix("yellow_ochre", "cerulean", 0.3), 0.5)` is `#98ae69`, a
  pale green. Neutral greys come from complements or from earth and white:
  `tint(mix("ultramarine", "burnt_sienna", 0.5), 0.7)` is a cool grey (`#9c8d8d`),
  `mix("burnt_umber", "titanium_white", 0.6)` a warm one (`#8b725b`), and
  `desaturate(c, 0.5)` pulls any mixture toward grey at the same value.
- The mixing model is a Kubelka-Munk power mean (`src/easel/color.py`); the
  optional Mixbox backend is better and is opt-in for licence reasons.

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
  `"axis"` (the place's own long axis), a number of degrees clockwise from
  horizontal, or a sequence of any of those for one pass each.

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

- **A shaped mass costs what its box costs.** The passes are counted across the
  extent of the mass along the sweep's normal, not over its area, so a shape and its
  box come out within a pass of each other. Budget for a shape exactly as before.
- **Coverage at `density=1.0` is 99% of the shape**, at every brush size tried
  (`0.06` to `0.20`).
- **Paint stops within three-quarters of a brush width past the silhouette.** The
  pass *centres* stop at the boundary — that is what `overhang=0` means — and the
  brush spreads half its width beyond, plus the pass wander. There is no second edge
  out there: it is the same ragged spill a block-in has always had at its ends.
- **One sweep leaves the boundary stringy**, because a bristle brush covers about
  three-quarters of its width. `direction=("axis", 90)` crosses it and closes it up,
  at twice the passes (7 → 17 on the blob above).
- **`"axis"`** resolves to the long axis of the outline, weighted by edge length:
  `-35.5°` for a ribbon from `(0.15, 0.8)` to `(0.85, 0.3)`, `0°` for a wide
  ellipse, `90°` for a tall rectangle.

Five masses of a 900×675 painting, sized `0.06`–`0.17`, come to 46 passes; the same
composition laid as the boxes around those masses came to 53, and looked like boxes.
Its axis-aligned edge share went from 31.4% as boxes to 25.2% as shapes — a real
move, and a smaller one than the pictures look, because much of what that probe
counts is the bristle comb's own streaks along each pass rather than the boundaries
of the masses. The pair is `m8/boxes.png` and `m8/shapes.png`; regenerate with
`python m8/paint_two_ways.py`.

Passes swept *along* a boundary and stepped inward, rather than straight across the
mass, describe a form differently again and are still open: phase M6c in
`painting-api-brief.md` (`s.sweep()`).

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
