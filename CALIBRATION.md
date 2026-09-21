# Calibration: the engine's measured numbers

[`PAINTER.md`](PAINTER.md) tells you how to paint with Easel, and
[`PAINTING.md`](PAINTING.md) says why each of its rules is a rule. This file holds the
numbers behind them — what was measured, on the engine as it is now. You do not need
any of it to paint. Come here when a rule in the guide makes you want to know *how
much*, or when a mark did not do what you expected and you want to know whether that is
you or the engine.

Every figure here is a measurement of the current engine and will move when the
engine changes. Trust the picture in front of you over a number in this file.

**Every number here states what it was measured on: the brush, the size, and the canvas
at least, plus whatever else the number depends on.** That is a rule rather than a
habit, and it was bought. A fall-off recipe here was measured on a patch whose size
nobody wrote down; a painter applied it to a large one, got a solid disc with a rim of
gradient round it, and spent three rehearsals discovering that the number had a range
it did not carry. The table it came from had the same defect visible in its own figures
and was read as a fall-off for a year. **A number without its conditions is not a
measurement, it is a rumour**, and sessions treat this file as ground truth.

The same rule's other half: **a claim about the engine's behaviour with no test behind
it says so.** Most of what is here is re-measurable from the scripts in `scripts/`;
where a figure comes from a painter's own report and has not been re-measured, the line
says that too.

## Where each rule's number lives

The guide and the recipes quote a number beside each rule and quote it once; this is
where the rule's measurement is. The last row holds figures painters reported about
their own sessions rather than measurements of the engine.

| The rule, as the guide states it | Measured under |
|---|---|
| Two masses closer than `0.10` in value read as one | *Values* |
| The floor of the box is `0.14`, and more passes do not go lower | *What the box reaches* |
| Mix to a value, not a ratio; white is weaker than its share | *The value scale*, *Tinting and mixing* |
| The engine lays the chroma it is given, never more | *Chroma: the engine lays what it is given* |
| A mass reads the same in the view as in the paint | *The paint and the view of it* |
| Paint buries graphite by what lands; `density` does not thin | *Graphite under paint* |
| Wet is a matter of a few strokes | *Wetness* |
| `density` spaces the passes; `solid` fills them; a solid plane still stripes at `0.03` | *Load and run-out* |
| A mass never stops dead at its outline; `overhang` moves the ends only | *`block_in`* |
| A solid mass lands short of its mixture; four pixels is the cliff | *What a solid mass actually lands at* |
| Passes along the form come out less square | *Laying a mass along its own axis* |
| A shape costs its box along the passes, times the crossings | *Shaped masses (M8)* |
| A clean edge spills half what a ragged one does, and eats corners past a quarter | *The contour of a clean edge*, *A clean edge on a narrow mass* |
| A shaped mass with `direction` left off can cost many times its axis | *A shaped mass with `direction` left off* |
| A sequence of directions is priced as the sum | *`direction` given a sequence* |
| A sweep follows an edge; crossing closes it | *`sweep`* |
| A smudge buys nothing past `0.02`, removes about half a join once, and works along not across | *`smudge`* |
| A glaze far from its ground has no usable opacity | *`glaze`* |
| An inward scumble is a glow; three steps of brush is the window; `n` is bounded by the patch | *`scumble`* |
| A band's brush is three steps; a wedge needs two bands; `opacity` does not quieten a passage | *The band, and the brush that closes its joins*, *The band across a wedge*, *Opacity does not make a passage quieter* |
| A chisel does not taper; a chisel ending on a slope is a staircase | *Pressure*, *The chisel staircase* |
| A dab is a light touch; `press=3` lands; scale a mark off the thing | *At the scale of a feature* |
| A bristle under `0.025` is four streaks; round tips repeat, `tip_wobble` redraws | *The bristle comb* |
| A rehearsal is the next strokes; `pencil`, `dry` and `erase` are logged | *The log, undo, and the stream* |
| What a mass costs, before the call | *Budget* |
| Rehearsal counts, subject shares, the form window, the cast-shadow steps | *From the sessions* |
| What the 0.5.0 round measured: the corpus replay, the noise budget, the candidates | *The 0.5.0 cohort's round* |

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

### Chroma: the engine lays what it is given

A painter mixed two colours, checked each against its target `value_of`, and found both
came back far more saturated on a large plane in a very low-chroma field than the number
suggested; each needed a second and a third desaturation pass found only at real scale.
The engine side of that, measured: a mass `0.60 × 0.30` laid solid with a `flat` at
`size=0.03`, 512×384 linen on `toned_warm_grey`, the Oklab chroma of the mixture, of
the paint sampled over the mass, of the rendered view of it, and of the ground:

| mixture | mixed | paint | view | ground |
|---|---|---|---|---|
| `yellow_ochre` + `viridian` 0.3 | `0.090` | `0.086` | `0.086` | `0.026` |
| `cadmium_red` + white 0.4 | `0.164` | `0.149` | `0.149` | `0.026` |
| `cerulean` + `burnt_umber` 0.5 | `0.017` | `0.016` | `0.016` | `0.026` |
| `ultramarine` + white 0.6 | `0.084` | `0.071` | `0.071` | `0.026` |

**The paint reads at the mixture's chroma or a little under it, never above** — the
ground showing through the first passes pulls it toward the ground — and the view reads
the same as the paint. So what read as more vivid was the eye, judging a colour against
the field it sits in, which is what simultaneous contrast is; the engine cannot measure
that and does not add to it. What it can do is give the number: `palette.chroma_of`,
beside `value_of`, so a mixture's chroma can be put next to the field's before a plane
of it is laid. For scale, the pigments: `titanium_white` `0.007`, `burnt_umber`
`0.020`, `viridian` `0.055`, `alizarin` `0.057`, `burnt_sienna` `0.071`, `ultramarine`
`0.085`, `cerulean` `0.092`, `yellow_ochre` `0.123`, `cadmium_yellow` `0.170`,
`lemon_yellow` `0.175`, `cadmium_red` `0.202`; the `toned_grey` ground `0.013`.
(`scripts/probe_greenhouse_session.py`.)

## The paint and the view of it

There are two surfaces here, and it is worth knowing that they agree before spending a
rehearsal on the possibility that they do not.

- **The paint**: what `sample()` hands back, what `compare()` measures, and what
  `look(values=True)` renders. Pigment in the canvas.
- **The view**: what `look()` draws in colour and what `export()` writes. The same
  pigment with the paint's own height shaded as low relief, lit from the upper left,
  plus whatever graphite the paint has not buried.

**Over a mass the two report the same value.** Measured on 512×384 linen, a mass
`0.60 × 0.20` laid over a solid wall, `flat` at `size=0.030`, sampled over its middle
`0.56 × 0.16`:

| mixed at | at the default load | laid `solid=True` |
|---|---|---|
| `0.215` | paint `0.269`, view `0.269` | paint `0.241`, view `0.241` |
| `0.26` | paint `0.311`, view `0.311` | paint `0.284`, view `0.284` |
| `0.33` | paint `0.372`, view `0.372` | paint `0.350`, view `0.350` |
| `0.50` | paint `0.508`, view `0.508` | paint `0.504`, view `0.504` |

The gap is `0.000` to three places in every row, and the worst *single pixel* anywhere
on the canvas is `0.038`, at a step in paint height. **The relief is a gradient**: it
brightens the upper-left side of every ridge of paint and darkens the lower-right by
the same amount, so it cancels over any area bigger than a ridge and it has nothing to
work with inside a mass of even thickness. `look()` at 720px, `look()` at full
resolution, `look(values=True)`, `export()` and `export(impasto=False)` all read `0.314`
on the same mass.

**So `solid=True` costs nothing in the view.** That is the row a session asked for —
how far a solid field at a stated value moves in the rendered view against the same
value at default load — and the answer is that it does not move. What `solid=True`
*does* move is the paint: a mass reads about `0.03` darker laid solid than at the
default load, because the passes no longer run dry and let the ground show through. See
`block_in` below.

Two things really do differ between the two surfaces, and neither is large:

- **Graphite the paint has not covered.** A pencilled area under one thin pass reads
  `0.395` as paint and `0.390` as the view of it — the drawing showing through.
- **Where the average is taken.** `sample()` averages pigment in *linear* light and
  hands back a colour to mix with; `compare()` and the values view encode each pixel
  first and average the values a painter can see. On a broken passage that is worth
  `0.002` to `0.005`, the linear mean reading the darker of the two. It is why
  `value_of(s.sample(place))` and `compare({place: v})` can disagree in the third
  decimal, and they disagree in no other way.

You can ask for the second number rather than believing either:

```python
s.palette.value_of(s.sample(mass))                   # the paint
s.palette.value_of(s.sample(mass, rendered=True))    # the view of it
```

`compare()`'s own table names the surface it measured, for the same reason.

**A mass that looks lighter than the number it was mixed at is not the view lifting
it.** Look for the value it stands against instead: `0.10` separates two masses at any
point on the scale, and the same step reads far louder at the dark end — `0.17` against
`0.26` is 43 against 66 in eight-bit grey, half as bright again, where `0.63` against
`0.72` is 161 against 184. A fascia `0.09` above its wall is inside the threshold and
still the brightest thing in a dark picture.

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
- **`solid=True` is as even as this engine gets, and it is not perfectly even.** What
  is left is the pass structure itself, and it does not move with `opacity` or with
  `pressure`. A `flat` at `size=0.03`, `density=1.0`, `solid=True`, over a region on a
  512×384 `toned_grey` canvas, interior sampled a brush in from the edges:

  | | interior sd | row-mean peak to peak |
  |---|---|---|
  | `opacity=0.85`, `pressure="taper"` | `0.0092` | `0.033` |
  | `opacity=0.85`, `pressure="even"` | `0.0088` | `0.029` |
  | `opacity=1.0`, `pressure="taper"` | `0.0090` | `0.027` |
  | `opacity=1.0`, `pressure="even"` | `0.0093` | `0.025` |

  About `0.03` of value, at every combination. That is a quarter of the `0.10` that
  separates two masses, so it is invisible on anything with a form in it and visible as
  faint striping on a large flat plane at feature scale. **A bigger brush or a broken
  one hides it; an argument does not.** This one contradicts what the painter who asked
  for the measurement believed while painting — its planes came out striped at `0.85`
  and clean at `1.0`, and what had actually changed between those two rehearsals was
  the brush size and the shapes.
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
- **"The ends" turn with `direction`, and that is two masses' worth of surprise.** The
  same argument reaches past the left and right of a mass swept horizontally and past
  the top and bottom — off the foot of the mass, onto whatever it stands on — of one
  swept vertically, which is what `"axis"` picks as soon as the mass is taller than it
  is wide. Measured on a shape `0.40 × 0.30`, bristle at `size=0.030` (19px on a
  640×480 canvas), laid solid; furthest paint past each edge:

  | passes | `overhang` | left | right | top | bottom |
  |---|---|---|---|---|---|
  | horizontal | `0` | 3px | 2px | 7px | 6px |
  | horizontal | `0.35` | 9px | 9px | 7px | 6px |
  | horizontal | `1.0` | 22px | 20px | 7px | 6px |
  | vertical | `0` | 8px | 3px | 4px | 2px |
  | vertical | `0.35` | 9px | 3px | 9px | 7px |
  | vertical | `1.0` | 8px | 3px | 18px | 17px |

  Half a brush is 9px, and that is what the two edges it does not lengthen keep
  throughout. **A mass never stops dead at its own outline**, whatever this is set to.
- **`overhang=0` does not leave a boundary bare.** The half-brush strip inside the pass
  ends comes back `0.0%` unpainted on the shape above laid solid, at every setting. At
  the *default* load it comes back `8.7%` bare at `overhang=0` and `4.2%` at `1.0` —
  but the strip inside the **sides**, where `overhang` does nothing at all, is barer
  still at `14%`. What that measures is the comb's own texture and the brush running
  dry, not a boundary the passes failed to reach: `solid=True` removes all of it.
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

### What a solid mass actually lands at

**A mass lands between its mixture and what it was laid over, and how far depends on
the brush.** Every clause of *a plane that is a plane* — `density=1.0`, `solid=True`,
`opacity=1.0`, `pressure="even"` — a mixture at `0.865`, 600×600 linen, sampled well
inside the mass:

| brush width | 1.8px | 2.7px | 3.6px | 4.8px | 7.2px | 12px | 18px |
|---|---|---|---|---|---|---|---|
| `flat` | `0.427` | **`0.403`** | `0.405` | `0.681` | `0.768` | `0.801` | `0.826` |
| `bristle` | `0.415` | `0.407` | `0.411` | `0.582` | `0.656` | `0.733` | `0.773` |
| `round_hard` | `0.581` | `0.669` | `0.778` | `0.834` | `0.853` | `0.852` | `0.856` |

over a ground of `0.395`. At 2.7px a chisel lands `0.403` against that ground —
nothing at all. Even at 18px a `flat` is `0.04` short of its mixture and a `bristle`
`0.09` short, which is most of the `0.10` that separates two masses; only a round tip
holds its colour small.

**It is a pull toward the ground, not a fixed shortfall**, which is the half the
painting that found this could not see from one ground. The same mixture over a
*lighter* ground lands **above** itself: over `0.957`, `flat` reads `0.956` at 2.7px
and `0.873` at 18px; over `0.125` it reads `0.131` and `0.771`. A mixture at `0.20`
over the light ground lands `0.232`. Same direction every time — toward what was
underneath.

**The cliff is at four *pixels*, and pixels are the unit.** Not `size`, which is a
fraction of the canvas long side: the same `size=0.008` is 2.4px on a 300px canvas and
9.6px on a 1200px one. Measured on all three, a `flat` at 3.6px lands `0.405`,
`0.405` and `0.401`, and at 4.8px lands `0.674`, `0.681` and `0.600` — the knee is at
the same *pixel* width every time. One stroke tells the same story more starkly: a
`flat`, `bristle` or `knife` deposits **zero** paint at 1–2px, against a
`round_hard`'s 44–51 pixels' worth. An oriented tip handed a `size` under four pixels
now says so at the call, and `cost()` says it before a stroke is spent.

*This cost one painting four rehearsals on a bird's head laid at `size=0.005` that
came back a dark fuzzy ball. The evidence was already in this file — The paint and
the view of it records a solid mass mixed at `0.215` landing `0.241` and one at `0.50`
landing `0.504` — in four rows, at one brush size, unnamed.*

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
  at twice the passes (7 -> 17 on the blob above). **On a small mass, don't**: the two
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

### The contour of a clean edge

Three painters handed one subject hit `edge="clean"` on three shapes: a pointed arch
above a tapering tower, a cap eaten to a mushroom, and an arch standing 65px off a
four-cornered tower — which the third isolated to the contour pass being swept along a
*spline* through the polygon's corners, bowing outward wherever the corners are sparse.
The contour is swept along the polygon's own edges since 0.2.0. Pixels of paint
standing above the shape's top edge, 1024×768 linen, `flat` at `size=0.02`, laid solid
with vertical passes; the ragged fill's half-brush is about 3px:

| shape | ragged | clean, spline (until 0.2.0) | clean, along the edges |
|---|---|---|---|
| a fresh four-cornered tower, `0.10` wide | 4px | **65px** | 4px |
| `lighthouse_dusk`'s own `tower()` polygon | 3px | **45px** | 4px |
| a tower tapering from `0.20` to `0.07` | 2px | **69px** | 4px |

The dusk example's committed `painting.png` predates the regression and does not show
it; its four clean masses now rebuild where they were drawn. What the three painters
proposed as the trigger — the distance between two outline corners, or the brush's
share of the shape's shorter extent — was two views of the same spline, and neither
number was it. (`scripts/probe_greenhouse_session.py`, which prints the spline column
by putting the old contour back for one call.)

### A clean edge on a narrow mass

The other half of the same finding survives the fix and is the share. `edge="clean"`
insets the fill by half the brush all round, which is a rim on a large mass and most of
a small one. A painter's lantern cap, `0.214 × 0.036`, 1120×860 linen, `flat`, solid,
`direction="axis"`. *Share* is the brush over the cap's shorter extent in the brush's
own unit (the canvas long side); *kept* is the area the inset leaves to fill; *covered*
is the share of the cap's pixels that got paint; *corners* the same over the outer 8% of
its width at either end; *spill* the paint outside the cap as a share of its area:

| `size` | share | kept | covered ragged / clean | corners ragged / clean | spill ragged / clean |
|---|---|---|---|---|---|
| `0.004` | 14% | 86% | 92% / 92% | 87% / 91% | 7% / 5% |
| `0.006` | 22% | 80% | 99% / 99% | 97% / 83% | 16% / 8% |
| `0.008` | 29% | 74% | 100% / 99% | 96% / 70% | 23% / 11% |
| `0.010` | 36% | 68% | 100% / 98% | 97% / 51% | 30% / 15% |
| `0.012` | 43% | 62% | 100% / 97% | 92% / 29% | 31% / 18% |
| `0.016` | 58% | 51% | 99% / 96% | 85% / 6% | 42% / 21% |
| `0.020` | 72% | 40% | 99% / 94% | 79% / 0% | 45% / 25% |

The cap as a whole stays covered; **what goes is the corners**, and it goes past about
a quarter of the shorter extent — the contour pass lays the strip the inset gave up as
one chisel stroke, with the rounded ends a chisel leaves. So `block_in` and `preview`
say so past a quarter, naming the share and what the inset keeps, and the fix is a
smaller brush or the ragged edge. Clean still spills half what ragged does at every
size, which is what it is for.

### The bites just inside a hard edge (0.6.0: the default moved)

`edge="hard"` masks every dab to the outline, so nothing can land outside it — and
until 0.6.0 it still left the boundary *bitten* from the inside, in scallops between
the pass ends. The cause is pressure and not reach: the default `pressure="taper"`
arrives at zero one brush out, so at the old `overhang=1.0` every pass met the outline
at part pressure, and a round tip — which loses *width* with pressure — met it at part
width as well. Measured on the 3 px strip just inside a mass whose left and right edges
slope, `size=0.05`, `density=1.0`, `solid=True`, `direction="vertical"`, 1024×768; the
share of that strip that came back bare:

| brush | slope | `ragged` | `hard`, one brush | `hard`, two (the default now) |
|---|---|---|---|---|
| `flat` | 0° | `0.09%` | `0.000%` | `0.000%` |
| `flat` | 10° | `3.37%` | `0.657%` | `0.000%` |
| `flat` | 20° | `1.71%` | `0.000%` | `0.000%` |
| `flat` | 30° | `0.19%` | `0.000%` | `0.000%` |
| `round_hard` | 0° | `10.01%` | `3.016%` | `0.274%` |
| `round_hard` | 10° | `11.77%` | `3.260%` | `0.226%` |
| `round_hard` | 20° | `7.55%` | `1.032%` | `0.329%` |
| `round_hard` | 30° | `8.43%` | `0.854%` | `0.055%` |

**It is the round tip's fault more than the chisel's**, which is the opposite of the
staircase above. And **the cost is dabs, not strokes**: the pass count is identical at
one brush and at two — 15, 18, 22 and 25 for the four slopes — so `cost()` quotes the
same number it always did. Nothing can cross the mask, so the outline does not move
either: on a mass laid with a `round_hard` at 14°, paint outside the outline went from
225 px to 227 px, that difference being the boundary's own feathering, while bare
inside it went `0.220%` to `0.024%`.

**`scumble` keeps its own `0.35` and needs no more.** Its passes are `pressure="even"`
by default, which is the whole mechanism, and it leaves `0.000%` of the same strip bare
at `0.35`, `1.0` and `2.0` alike with either brush. `cover` does move, because it is
priced and laid as the block-in it becomes; its published area ratios are unchanged
(`1.00x` the area it was handed at `hard`, at every overhang).

### A shaped mass with `direction` left off

`direction` defaults to horizontal, and on a shape taller than it is wide the passes
step down its whole height. A painter costed two planes at 9 and 9 with `direction=90`,
wrote the calls without it, and the rehearsal charged 124 for a pass budgeted at 40.
The same masses priced three ways, `flat`, `density=1.0`, 1120×860:

| mass | `"axis"` | `90` | left off | ratio |
|---|---|---|---|---|
| the tower's mid plane, `size=0.027` | 11 | 11 | **43** | 3.9× |
| the tower's lit band, `size=0.022` | 5 | 7 | **55** | 11.0× |
| the vine mass, wider than tall, `size=0.030` | 5 | 8 | 5 | 1.0× |

The default does not move — `"axis"` would be right nearly always, and moving it would
move every painting ever made — but the price walk has both numbers, and a shaped mass
with `direction` left off says so from `cost` and from the call when the horizontal
passes cost over 2.5× the axis: it fires on the first two and not on the third.

### `direction` given a sequence

**A sequence is one whole pass per angle, and the mass is charged the sum.** Not one
stack sized for the steepest angle in it — every angle is paid for in full, and a
steep angle on a wide mass costs several times a shallow one. One painting's room
mass, `bristle` at `size=0.16`, `density=0.9`, 1024×768:

| `direction` | strokes |
|---|---|
| `"axis"` (the mass runs at 2.8°) | 4 |
| `-17` | 7 |
| `"cross"` | 15 |
| `(4, 94)` — a cross at the mass's own angle | 15 |
| a ten-angle sequence | **85** |

and those ten angles priced one at a time are `4 + 5 + 7 + 7 + 9 + 10 + 10 + 11 + 11
+ 11`, which is the 85 exactly. The steepest of them alone is 11. The painter who
found this costed a ten-angle list at **51** on the same mass — a different ten
angles, and the same arithmetic.

The guide asks a painter to vary direction between passes to break a comb, so a
painter following it reaches for the sequence first. **Two directions are what
breaks a comb and more do not break it further**, which is why the affordable answer
is the pair. A list longer than a pair says so from `cost` and from the call when it
costs over 2.5× its own dearest angle — which two angles never can, so the pair
idiom every painting here uses stays silent.

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

- Passes step **one part-brush** apart: `size × (1 - 0.45 × density)`, the same rule
  `block_in` spaces its passes by. At `density=1.0` that is `0.55` of the brush
  width. The recipe this call replaced stepped `0.27` of a brush width, which is
  `density~1.6`.
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
- **What `size` buys stops at about `0.02`; what it costs does not.** One pass along a
  step from `0.78` down to `0.17`, both masses solid, 640×480 linen, `flat` at
  `size=0.030`, the pass laid along the boundary the two masses actually met on. The
  join's sharpness is the steepest value step across it per 1% of canvas height (a bare
  join reads `1.207`); the reach is how far the pass carried the light mass into the
  dark, as a share of canvas height:

  | `size` | join sharpness | softened by | carried into the dark |
  |---|---|---|---|
  | `0.008` | `1.233` | nothing | `0.4%` |
  | `0.011` | `1.191` | nothing | `0.6%` |
  | `0.016` | `0.651` | `-46%` | `1.0%` |
  | **`0.020`** (the default) | `0.581` | `-52%` | `1.3%` |
  | `0.024` | `0.614` | `-49%` | `1.5%` |
  | `0.028` | `0.608` | `-50%` | `1.7%` |
  | `0.032` | `0.493` | `-59%` | `1.9%` |
  | `0.040` | `0.376` | `-69%` | `2.3%` |
  | `0.070` | `0.215` | `-82%` | `4.4%` |

  Three things are in that table. Below about `0.014` the tip is too small to straddle
  the join and **the pass does nothing at all** — which is worth knowing before
  concluding that a small smudge is a safe one. From `0.016` the softening arrives
  almost at once and then flattens off, while the reach goes on growing with the brush
  in a straight line. And the old default of `0.07` is off the bottom of the table: it
  takes `82%` off the join and drags the light mass `4.4%` of the canvas height into
  the dark, which is the pale finger-shaped lobe four sessions have described.
  **`0.02` is the knee and is the default since 0.2.0**; past `0.03` the call says so.
- **It removes about half of a join, once, and repetition undoes it.** The steepest
  value step across a hard join, per 1% of canvas height. *This table's canvas, brush
  and step were not recorded when it was measured*, which is what the rule at the top
  of this file exists to prevent; the row above is the one to trust for absolute
  numbers, and this one for what a second and third pass do:

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
- **Its reach does not grow with the join, so a long boundary gets a strip rather than
  a lost edge.** One pass at the default `size=0.02` along a hard step from `0.19` to
  `0.78`, 1024×768 linen, both masses laid `edge="hard"` so the step is a step, the
  pass measured across the middle of its own stretch:

  | join length | strip height | strip value |
  |---|---|---|
  | `0.05` | `1.30%` of canvas height | `0.53` |
  | `0.10` | `1.30%` | `0.51` |
  | `0.20` | `1.17%` | `0.51` |
  | `0.40` | `1.30%` | `0.51` |
  | `0.80` | `1.30%` | `0.50` |

  The height is the `1.3%` the table above already publishes for that size, flat across
  a sixteen-fold range of join lengths, and the value is halfway between the two masses
  to the hundredth. **So the mechanism is the reach and nothing else** — the asymmetric
  pull above is not doing anything extra on a long boundary, which is what the session
  that reported it guessed. What changes is what the same band *reads* as: over a short
  join a softened corner, and over `0.4` of the canvas a mid-value band running beside
  the boundary, which is *dark, mid, light* — two edges where there was one. A painter
  who smudged each under-bench line in a finish pass kept four of them.
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

## `glaze`

A thin film that adds no paint height. One mark, and the only argument that does
anything much is `opacity`.

**A glaze is strong in proportion to its distance from what it lands on — in hue as
well as in value.** Measured on a 512×384 canvas: a warm light mixture (`0.62`) glazed
over a solid cool dark mass (`0.30`), `flat` at `size=0.18`, `pressure="even"`, sampled
over the middle of the film:

| `opacity` | value under it | change | hex, before -> after |
|---|---|---|---|
| `0.05` | `0.310` -> `0.338` | `+0.028` | `#4d4c6d` -> `#5c5459` |
| `0.07` | `0.310` -> `0.351` | `+0.041` | `#4d4c6d` -> `#625754` |
| `0.10` | `0.310` -> `0.371` | `+0.061` | `#4d4c6d` -> `#6b5c4e` |
| `0.14` | `0.310` -> `0.397` | `+0.087` | `#4d4c6d` -> `#776247` |
| `0.20` | `0.310` -> `0.433` | `+0.123` | `#4d4c6d` -> `#876940` |

Read the hex column rather than the value column. By `0.05` the underlying violet is
already gone and the glaze's own warmth has not arrived — the film is a neutral grey,
which is the *complement* doing what complements do. By `0.14` the value has moved
`0.087`, within a hundredth of the `0.10` that makes two masses separate, so a film
meant to shift a passage has instead made a new one.

**There is no usable opacity for a glaze far from what it lands on**, which is the
`knife`'s rule — keep it close in value to what it sits on — arriving through hue. Mix
the glaze close first, then choose an opacity. A painter rehearsed one twice at `0.14`
and `0.07`, got a saturated stripe and then nothing, and dropped the mark.

### Aiming a film at a value

*Mix the glaze close, then choose an opacity* is two steps, and the second is a
search: the window above is a few hundredths of opacity wide and it sits somewhere
different over every passage. A later painting spent **six rehearsals** on it and
dropped a glaze it had rehearsed three times. `glaze(to_value=)` runs that search
instead — `at_value` for a film — by laying films on trial canvases until one
delivers the value asked for, measured over the film's own footprint.

The same warm film over the same cool dark, 512×384, measured over the whole
footprint rather than the middle of it (which is why the changes are a shade larger
than the table above):

| asked for | opacity found | delivered | miss |
|---|---|---|---|
| `0.34` | `0.031` | `0.338` | `-0.002` |
| `0.38` | `0.102` | `0.382` | `+0.002` |
| `0.42` | `0.164` | `0.418` | `-0.002` |
| `0.46` | `0.242` | `0.459` | `-0.001` |

It costs **one stroke**, like any other glaze: the search is spent on copies. About
eight trial films, which is nothing on a halo and about a second on a band across the
whole canvas. The trials come off a copy of the stroke stream, so **the film that
lands is byte for byte the film that would have landed had its opacity been typed
out** — solving for it moves no paint.

A target outside what the film can deliver **raises**, naming both ends of what it
can reach, for `at_value`'s reason: a film silently landing at the wrong value is
the failure the instrument exists to stop. In the row above that range is `0.319`
(the paint under it) to `0.588` (the film at `opacity=1.0`).

---

## `scumble`

What closes a join a smudge only softened: `n` overlapping passes at closely spaced
values, charged as `n`.

**The default grades edge to edge, which is a band and not a glow.** Nine passes
`0.20`->`0.90` over a **round patch of radius `0.16`** on a 512×384 canvas, `bristle`,
`opacity=0.7`, read off the values view at five points across the patch and five down
it:

| nine passes over one patch | across it | down its middle |
|---|---|---|
| `direction="axis"`, `size=0.07` (a band) | `0.79, 0.65, 0.41, 0.30, 0.24` | `0.47, 0.48, 0.41, 0.42, 0.50` — flat |
| `direction="inward"`, `size=0.07` | `0.32, 0.59, 0.89, 0.61, 0.31` | `0.48, 0.83, 0.89, 0.81, 0.53` |
| `direction="inward"`, no `size=` | `0.30, 0.57, 0.86, 0.60, 0.31` | `0.46, 0.79, 0.86, 0.81, 0.49` |

So a band is one ramp and a centred passage is a fall-off from the middle in every
direction — which is what a glow, a bloom or a lit patch on a surface is, and what
the guide had no recipe for. The rings run **round** the place, stepping in a
part-brush at a time from its boundary toward its centre, in `sweep`'s geometry; the
first ring lands on the boundary, so `color_a` is the value the patch meets its
surroundings at.

**The patch's radius is part of the measurement, which is why it is stated here now.**
The rings step `depth / n`, so on this patch they are `0.0178` apart and the `size=0.07`
above is 3.9 of them. That is already past the point where the last rings begin burying
the first; the row is legible as a fall-off because the patch is small enough to carry
it, and on a larger one the same brush lays a flat middle. The third row is what the
verb picks for itself (`3 × depth / n`, `0.0533` here) and it is the smoother of the
two. Hand it `size=0.07` today and it warns, naming the number of steps.

A ring is two or three times the length of a pass across the same patch and has no
far end to run dry at, so a centred scumble defaults to `load_falloff=0.0`; without
it the brush starves half way round and the glow comes out bright on one side. An
explicit `load_falloff=` still wins.

**Where it stops being a fall-off, measured on a patch big enough to show it.** An
ellipse `0.72 × 0.24` on a 512×384 canvas, `n=7`, `opacity=0.5`, bristle, `0.45` at the
edge to `0.75` at the centre — so the rings step `0.017` apart. The second column is the
share of the patch sitting within `0.06` of the centre value, which is the measure of
how much of it has gone flat:

| brush | flat at the centre value | profile, edge -> centre |
|---|---|---|
| `0.09` (five steps) | **44%** | `0.52 0.55 0.62 0.69 0.70 0.69 0.71` |
| `0.05` (three steps) | 12% | `0.49 0.49 0.59 0.61 0.64 0.69 0.65` |
| `0.03` | 0.2% | `0.49 0.50 0.55 0.58 0.61 0.63 0.62` |
| `0.02` | 0% | `0.50 0.53 0.53 0.57 0.54 0.55 0.61` |
| `round_soft 0.09` | 42% | `0.50 0.56 0.60 0.66 0.71 0.72 0.72` |

At five steps nearly half the patch is one flat colour with a rim of ramp round it —
a disc, not a glow — and at one step the centre never reaches its colour at all,
because at `opacity=0.5` nothing lands there more than twice. **About three steps is
the usable middle**, and that is what the verb picks when no `size=` is given. A
preset's own default is `0.11` here, five steps wide, which is why the example in the
guide carries no `size=`.

#### And the other wall: `n` is bounded by the patch

The brush is `3 × depth / n`, so **more rings on a shallow patch buy a narrower
brush, not finer banding** — and the bristle comb has a floor of `0.025`, below which
it is four streaks with gaps (*The bristle comb*, below). Putting the two together,
the derived brush is still a brush only while `n <= 120 × depth`, where `depth` is
half the patch's shorter extent:

| `depth` | most rings that fit | the brush there |
|---|---|---|
| `0.030` | 3 | `0.030` |
| `0.042` | **5** | `0.025` |
| `0.0667` | **8** | `0.025` |
| `0.075` | 9 | `0.025` |
| `0.100` | 12 | `0.025` |
| `0.200` | 24 | `0.025` |

Arithmetic, not a measurement, and exact. The two bold rows are the walls: `0.0667`
is where the recipe's eight rings stop fitting, and `0.042` is where even five — the
fewest that read as a fall-off rather than as steps — stop fitting, so **under about
`0.042` deep no `n` works at all**. A painter met this at `n=12` on a patch `0.075`
deep, read the post-pass check's bristle complaint as an unrelated one, and spent two
more rehearsals. The verb had warned from one side since the third session (a brush
too wide fills the patch flat) and said nothing from this one; it now says both, and
where no `n` fits it names *a volume of lit air* — the patch is not asking for this
verb.

### The band, and the brush that closes its joins

The same mechanism as the rings, one direction over: the passes step `extent / n` apart
whatever brush is on them, so the brush has to be wider than the step or the passes
never meet. Measured on a band `0.80 × 0.40` at `n=8` — a step of `0.050` — bristle at
`opacity=0.5`, 640×480 linen on a ground reading `0.53`, grading `0.20` to `0.70`. The
ripple is the standard deviation of the across-band profile's own one-step wobble, which
is what a stack of bars measures as; the span is what the ramp actually delivered:

| brush | in steps | ripple | delivered |
|---|---|---|---|
| `0.025` | 0.5 | `0.004` | `0.50`–`0.54` — the ground, barely painted |
| `0.038` | 0.75 | `0.009` | `0.39`–`0.54` |
| `0.050` | 1 | `0.014` | `0.31`–`0.59` |
| `0.075` | 1.5 | `0.015` | `0.27`–`0.63` |
| `0.100` | 2 | `0.008` | `0.25`–`0.62` |
| **`0.150`** | **3** | `0.007` | `0.26`–`0.63` |
| `0.200` | 4 | `0.005` | `0.28`–`0.64` |
| `0.300` | 6 | `0.006` | `0.36`–`0.63` — the last passes burying the first |

**The worst place is one to one and a half steps**, which is where a preset's own
default lands on an ordinary band, and it is the venetian blind a session abandoned the
verb over. Under a step the passes stop meeting at all and most of the band is still
ground. Past about five the ramp stops reaching its own ends. **Three steps is the
middle of the window and is what the verb picks with no `size=`** — the same figure the
inward case picks, for the same reason. Hand it under two and it says so.

**If you reach for this metric on your own painting, read both passages through
windows of the same width, and make them wide.** The ripple grows as the window
narrows, because a narrow column averages fewer pixels per row and the per-row noise
survives into the difference. Measured on one solid scumble, read through five
windows: `0.0008` across the full width, `0.0011` at `0.40` of it, `0.0016` at
`0.13`, `0.0020` at `0.04` — two and a half times the number for the same paint. A
painter compared a hand-laid band against a `scumble` this way, got an answer the
wrong way round, and put the mechanism down to canvas texture on a `rough` ground.
**It is not the texture**: the five rows above read identically on `smooth`, `linen`
and `rough` to four decimals, and on a *starved* pass `rough` reads `0.0011` against
linen's `0.0031` — lower, not higher. It is the window.

### The load a band is laid at (0.6.0: the default moved)

A ring has no far end to run dry at, so the inward case has defaulted
`load_falloff=0.0` since it was written. A band's passes *do* have ends, and until
0.6.0 they were laid on the brush's own load — which on `bristle`, the verb's own
default brush and the one preset that does not start full, is `load=0.9,
load_falloff=0.55`. Measured on a band `0.10–0.90 × 0.40–0.60`, `n=8`, burnt umber to
titanium white, 1024×768 linen on `toned_grey`, the share of the band still within
`10/255` of bare ground and the ripple down it:

| the band's load | bare | ripple |
|---|---|---|
| `load=0.9, load_falloff=0.55` — the brush's own, as 0.5.0 laid it | **`5.17%`** | `0.0110` |
| `load=1.0, load_falloff=0.0` — the default since 0.6.0 | **`0.01%`** | `0.0031` |
| `load_falloff=0.9`, named beside the call | `8.94%` | `0.0094` |

Five per cent of a passage coming back as bare ground is strata, not a ramp, and it is
the fault the graded-field recipe used to spend a bullet on: **40 of the 60 committed
banded scumbles in the corpus typed the pair by hand**, which is the corpus saying the
default was in the wrong place. The third row is the same default being overridden, and
is why this is a default and not a rule: a starved band is still one keyword away.

**`solid=` therefore moves nothing on a band any more.** It is still taken — scripts
type it — and on `direction="inward"` it still raises `load` from the brush's own to
`1.0`, which on a patch is worth `0.005%` bare against `0.012%`: nothing, and so not
moved, because nothing measured asked for it.

### The band across a wedge

The step-sized brush closes the joins on a band whose passes are all about one length.
A painter's beam — a wedge `0.045` across at the mouth and `0.42` at the far edge,
1024×768 linen on `cool_grey`, `n=8`, `direction="vertical"`, so the passes run across
the wedge and step along it — bloomed at the mouth and read as barely there at the far
end, and was abandoned after one rehearsal for a hand-built passage in five pieces. The
passes run `0.068` long at one end and `0.397` at the other. Paint landing outside the
outline, as a share of the wedge's area, by which half of the wedge it fell beside:

| brush | in steps | bloom beside the mouth half | beside the far half |
|---|---|---|---|
| `0.240` (picked from the step) | 3.0 | **73%** | 53% |
| `0.100` | 1.2 | 19% | 20% |
| `0.050` | 0.6 | 4% | 6% |

Picked for the step, the brush is wider than the whole mouth, and no one brush serves
both ends. The verb says so when the brush is wider than the passes at either end,
naming both lengths; the answer is two or three bands each sized to its own width, or a
`size=` chosen for the end that matters.

### Opacity does not make a passage quieter

The passes overlap, so a low opacity accumulates back toward full colour instead of
thinning what arrives. Eight passes from `0.30` to `0.62` over a solid `0.22` ground,
brush picked from the step, 640×480 linen:

| `opacity` | the passage's mean | span |
|---|---|---|
| `0.15` | `0.34` | `0.22`–`0.50` |
| `0.25` | `0.38` | `0.22`–`0.56` |
| `0.40` | `0.41` | `0.22`–`0.59` |
| `0.60` | `0.44` | `0.22`–`0.60` |
| `0.80` | `0.45` | `0.22`–`0.60` |
| `1.00` | `0.45` | `0.22`–`0.61` |

From `0.40` up it is the same passage — `0.04` between half opacity and full. Even at
`0.15`, a fifth of the way, it still lands within `0.12` of full colour. **To make a
passage quiet, mix `color_a` and `color_b` closer together**; that is what the two
arguments are for. This is *"`opacity` does not thin a long stroke, it only slows it
down"* arriving on the verb where a painter reaches for a low opacity to keep a passage
down, which is where one of them met it.

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
pressure 0.2 and at 1.0 alike, because a flat brush's width is the mass it lays. Two
painters read that and laid every pot as a rectangle with chisel ends under
`pressure=[1.0, 0.35]` regardless, so since 0.2.0 a hand-laid mark shorter than four
brush widths given a pressure list on one of these tips says so at the call; a list on
a long pass is how a passage brightens toward one side and is left alone.

### The chisel staircase

A chisel's pass ends stack into steps down a boundary that is not parallel to the
passes — the *shallow shape -> its bounding box* row of *the shape each tool leaves
behind*, one dimension over. A painter's lit band, `0.06 × 0.64`, its sides sloping
about three degrees off vertical, filled with vertical passes and laid solid, 1120×860
linen on `toned_warm_grey`. The mass has no horizontal feature in it, so every
horizontal edge is the tool's: the share of its strong edges (the top decile of the
Sobel magnitude) running within ten degrees of horizontal:

| tip | `size` | horizontal edges |
|---|---|---|
| `flat` | `0.020` | **13%** |
| `flat` | `0.010` | **17%** |
| `knife` | `0.020` | **16%** |
| `bristle` | `0.022` | 4% |
| `bristle` | `0.012` | 7% |
| `round_hard` | `0.020` | 3% |

Three to four times as many from a chisel, and a smaller chisel is worse, because there
are more pass ends. The repair that worked costs one stroke: lay the plane with a comb
and put the core back with a single solid stroke down its middle. Measured by the
painter who found it and re-measured here to the percentage point.

**Where the fault sits, and what each repair leaves.** The step down the side is
`pass step × cot(theta)`, where `theta` is the angle between the side and the passes —
so it is *nearest parallel* that a chisel steps worst, and a side laid exactly along
the passes takes no pass ends at all. The same band, swept at a range of angles to its
own long side:

| passes, against the side | flat `0.020` | bristle `0.022` | `round_hard` `0.020` |
|---|---|---|---|
| `0.7°` — along it | 3% | 0% | 0% |
| **`3.7°`** | **22%** | 1% | 1% |
| `6.3°` | 8% | 1% | 4% |
| `16.3°` | 5% | 1% | 1% |
| `41.3°` | 6% | 0% | 1% |
| `86.3°` — square to it | 2% | 0% | 1% |

The chisel is several times the others only in the first few degrees; past about six
the three are the same picture. That is the window `chisel-staircase` fires in, and it
is why the rule counts pass ends rather than measuring how far from square a boundary
is — the prototype that asked the second question was silent on this very band.

The repairs, on the band at `3.7°`, cheapest first:

| repair | horizontal edges | costs |
|---|---|---|
| as written — `flat`, ragged | 22% | — |
| `direction=` the side's own two points | 14%, and **nothing** where the sides run parallel | nothing |
| `edge="clean"` | 11% | one stroke |
| a comb, `bristle` | **1%** | nothing |
| a comb with one solid stroke down the core | 7% | one stroke |
| `edge="hard"` | **20%** | nothing, and it does not work |

**`edge="hard"` does not close a staircase**, and this document said it did until
0.6.0. It masks every dab to the outline, and these pass ends are *inside* the mask:
22% to 20%. Passes along the side close it exactly when the sides are parallel, and a
tapered shape has no one angle that serves both — which is why the comb, whose end is
broken into bristles rather than being a line, is the repair that always works.

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
  `0.3` of the canvas across, a plane within it wants about `size~0.015–0.025` and a
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
the last bit; their combs now correlate +0.39, -0.05 and +0.33 over three pairs.

The pitch is the comb in the tip. What *reads* on a fully loaded straight stroke is
coarser, because consecutive dabs overlap by more than 90% and fill the weaker
bristles in, so only the missing ones show — two to seven streaks across a mark, at
any size. The comb shows at its own scale where the stroke is starved or the tooth
is biting. `bristle_count` still pins a comb if you want a fixed one.

### The holes a solid comb leaves

`solid=True` sets `load=1.0` and `load_falloff=0.0` and nothing else, so it fills the
gaps a brush leaves *along* a pass as it runs dry — and leaves the ones the comb's own
missing bristles leave *across* it. A `flat` laying the same mass leaves `0.0000%` bare
at every size and density tried. Measured on a 1440×960 canvas, one shaped mass,
`solid=True`, *bare* meaning within `10/255` of the ground, which is what
`ground_showing()` means by it and what an eye means by it:

| brush | `size` | `density` | bare | blobs | largest |
|---|---|---|---|---|---|
| `flat` | 0.04 | 0.8 | `0.0000%` | 0 | — |
| `bristle` | 0.04 | 0.8 | `0.1552%` | 47 | 198 px |
| `bristle` | 0.04 | 1.2 | `0.0000%` | 0 | — |

**And a hole is a contrast, not a gap.** The same call, the same holes, on three
grounds:

| ground | bare | blobs | largest |
|---|---|---|---|
| `toned_grey` | `0.1552%` | 47 | 198 px |
| white | `0.1357%` | 41 | 176 px |
| a dark `#2e332c` | **`3.1550%`** | 373 | 2270 px |

So the comb's holes are a dark mass's problem. The passes sit `size × (1 - 0.45 ×
density)` apart, so `density=1.2` is about a fifth more passes than `1.0` and closes
them; a solid tip closes them at any density for the same money; crossed passes close
them at twice the price. `solid-comb` says this at the call, with the share and the
prices, and moves no default: a comb is the right brush for foliage, cloth and
anything with strands in it, and its holes only read where the ground is darker than
the paint. Two painters reported them as *shaped block-in paths wandering apart*,
which they are not — [`SUGGESTIONS.md`](SUGGESTIONS.md), B2.

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

## The log, undo, and the stream

**A replay from a saved log is the painting, to the pixel.** It was not: the log rounded
every point to five decimals for a tidier file, and a wobbled pass came back from disk a
hair off its line — invisible on hand-written coordinates, which are short decimals to
begin with, and the reason a painter could not minimise the drift below with toy cases.
The points are written exactly since 0.2.0, and a saved log replays byte for byte.

**`undo` puts the random stream back.** A mass draws its pass wander from the session's
stream, between the strokes it records. Undoing a plain mark was already exact; undoing
a whole mass left the stream past it, and `easel undo` — which rebuilds from the log —
handed back a stream sitting at the seed, so the next mass drew wander a clean rebuild
never had. A painter measured its working session drifting **1.06%** of its pixels from
a clean rebuild of the same scripts, confined to the marks laid after the undo. Every
mark now carries the stream's state at the start of the call that made it (taken once,
before the first draw, because per record it would already be one draw past). A mass,
then a detour, then the detour undone, then a third mass, 320×240, seed 5, against the
third mass laid straight after the first: identical in-process for a mark undone,
identical in-process for a whole mass undone, identical through the session file.

**The planning verbs leave nothing behind, and three free verbs do.** One `bristle`
stroke laid after each verb, 400×300, seed 9, hashed against the same stroke laid after
nothing:

| verb | the stroke after it |
|---|---|
| `look`, `look(values=True)`, `preview`, `rehearse`, `cost`, `compare` | identical |
| `pencil`, `dry`, `erase` | **changes** |

The first row is the property *rehearse everything* rests on, and it is asserted by a
test. The second is the log index, not the stream: a mark's texture is seeded from its
place in the log, and each of those is logged, so adding or removing one shifts every
mark after it. Deterministic, and a painting still rebuilds from its scripts.

**A rehearsal copy counts on from the painting.** Inside a lone `easel run --rehearse`,
`s.stroke_count` and `s.remaining` read `0` and the whole budget while `compare()` in
the same script saw the painted canvas; the copy started its own log from nothing. It
carries the painting's count now, so the numbers inside a rehearsed pass are the numbers
the pass will see when it is run for real, and what the copy itself laid is its own
`s.history.stroke_count` — which is what the shell's *Rehearsed* line reports.

---

## Budget

A whole painting is usually a few hundred marks, not a few thousand. `s.stroke_count`
keeps the tally; `pencil()`, `erase()`, `mark()`, `look()`, `preview()`, `rehearse()`
and `compare()` do not count. **`smudge()` and `glaze()` do** — they are marks like any
other, and a rehearsal run measured that (297 -> 299 for two smudges) with three
strokes of budget left.

**A mass can be costed before the call rather than discovered after it.** Passes step
`size × (1 - 0.45 × density)` apart, so a mass takes about `extent / step` of them,
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
thin full-width band **5 -> 41**; a small concave shape **12 -> 32**. And a ribbon
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

---

## The plan a painter declares

`Session(budget=)` above is the first of these: a number the painter writes down and
the engine then holds them to. `s.plan(...)` is the rest of them — the values, the
place meant to be lightest, the subject's share, and the two standing warnings a
picture can declare its way out of. The numbers here are why each one is worth a line
of the check.

**The pairs in a value plan.** A plan finished all-green with two of its places
planned `0.00` apart; they were the two that met on the canvas, and one dissolved into
the other exactly there. Three of that plan's four close pairs were fine, because those
masses never met. So the pairs are worth printing and *touching* is the whole of what
picks them out: `plan-pairs` says only the pairs that are both inside `0.10` and within
`0.01` of the canvas long side of each other. It is asked at registration, on the empty
canvas, because that is the one moment the answer is free — and it was asked of the
painter rather than answered for them for two rounds, both of which got it wrong, while
three rounds skipped the empty-canvas run that would have raised the question at all.

**The subject's share** is measured under *From the sessions* below, and this changes
nothing about the number — only who has it. `report(subject_share=)` has taken it since
0.4.0 and **neither `easel run` nor the MCP `run` tool ever passed it**, so a painter
working anywhere but a Python prompt had never once seen the comparison, whatever they
had written down.

**The stack of bars is the noisiest rule the engine has**, and declaring the bands is
what quietens it. Over the 325 painted passes of the corpus it fires on **47 of them,
14%** — one pass in seven, *after* the said-once decay that already cut the pier's own
seven firings to three — and it is half of all the lines the engine prints. It is also
the rule two painters learnt to skim, and one cohort painter's was the only true
positive in its round. Its own text concedes *unless the subject runs that way*: it
cannot tell whether the subject does, and the painter can. Declared, the line stops
warning and starts counting what crosses the bars, at `_REPORT_CROSSING_DEG` — 30
degrees, the middle of a plateau where every threshold from 20 to 60 prints the same
three lines on the pier. **The 14% is not re-measured here and does not need to be**: no
painting in the corpus declares a plan, because there was nothing to declare one with
until now, so a replay would print the same table. What a declaration changes is the
text of the line, not how often the condition is met — the share to watch is the one the
next round measures, over paintings that had the declaration available.

**The bare-ground floor is older than the round that reported it.** Five of seven
painters in the 0.5.0 cohort accepted `ground: 0.0x% … the checklist asks for some` by
hand, three of them naming the same cause in nearly the same words — the `density=0.8`
breather they were told to leave was buried by the graded fields they were told to lay.
But the corpus replay puts **half of all 21 paintings under the floor, cohort or not**,
so the contradiction is between the graded-field recipe and the checklist line rather
than anything the cohort did. An earlier painting shows the other half of it: it chose a
warm ground *to be seen through*, laid the passage over it at `density=1.0, load=1.0`,
and finished at `0.07%` without noticing — which is the case the floor is for, and is
not the same picture as one that buries its ground on purpose. `ground="buried"` is
which of the two the painter meant, and the floor is unchanged for a painting that has
not said.

---

## From the sessions

The guide used to quote these beside its rules. They are what painters reported about
their own paintings — counted off their logs and written in their notes — and not
measurements of the engine, so they carry the rule at the top of this file the other
way round: **every figure here is a painter's own count, re-measured where the export
allowed it and not otherwise.** They are here so that the rules they support can be
stated in one line each, and so that the next painter can put its own numbers beside
them.

**Rehearsing.** Two painters rehearsed 27 and 18 passes of one painting each; every one
of the eighteen changed something, and not one was charged. Another rehearsed and threw
away 38 marks across two sittings, at no cost. The painter who rehearsed nothing spent
about 60 of its 224 strokes repainting five masses it had laid once and disliked. A
tenth session rehearsed every one of its eleven passes and found, on the copy, a set
of thin members laid three times too heavy and a recipe for small things that would
have cost 220 strokes against 142 left.

**The subject's share.** One painter working to 300 spent 59% of them before the
subject began and reached it with 41% in hand; its own verdict was that the part it
came for was the weakest passage. Another spent 24% on the subject against a planned
32%. One stopped with 115 strokes unspent. One that measured at the moment the subject
was done stood at 45%, and at 41% after two passes on the surroundings, which obeys
both rules. The tenth stood at 40% against a plan of about 30%, and began the subject
at 44% of the budget.

**Form is bounded at both ends.** A mass that read flat at `0.09` of value across its
width was laid up to `0.22` and turned — and its shadow side then sat `0.09` from the
mass behind it and the two began to merge. At about `0.15` both held. That is the
ceiling the guide quotes beside its `0.10` floor.

**A cast shadow on a lit surface.** On a surface at `0.60`, the darkest mixture at
`0.16` read as a hole punched through it, `0.50` as a shadow, and `0.42` as a shadow
with weight.

**A cool mass on a warm ground.** A painter concluded three times that its subject was
far too light, and `compare()` said it was inside `0.05` every time — about two steps
of apparent lightness that the number does not carry.

**The drawing.** Seven of the first ten paintings drew no line at all and nine placed
no landmark. The tenth drew its arrangement four times before paint, at a cost of
nothing, and threw the first two away; the two passages it never drew were the two it
named weakest at the end.

**Reading.** Reading the guide, the reasons, the reference, the calibration file and
two paintings' notes cost one session a few minutes and about thirty thousand tokens,
against far more spent looking at its own rehearsals.

---

## The 0.5.0 cohort's round

Seven painters who are not Claude installed `easel-paint` 0.5.0 from the package, painted
a picture each, and left a verdict on the tool. Acting on them is one round, and its
measuring step is [`scripts/probe_cohort_session.py`](scripts/probe_cohort_session.py):
it rebuilds **every committed painting from its own pass scripts, pass by pass**,
re-measures each claim the round is built on, and counts what each proposed check would
cost in lines printed. Everything in this section is that script's output. Re-run it
rather than trusting the numbers here — it takes about an hour, and `--claims`,
`--corpus` and `--only <name>` cut it down.

**Why a corpus replay at all.** `LESSONS.md`'s first rule is *measure the condition
before writing the rule*, and its seventh is *a warning that fires on almost every pass
is a warning nobody reads*. Neither can be settled by reading code: both are questions
about what a painter would have been told, at the moment they were painting. Replaying
the corpus is the instrument that answers them, and for four of the round's proposed
checks the answer was *no*.

### The corpus, rebuilt

Every painting under `paintings/`, on a fresh session with the canvas arguments
`PAINTINGS.md` records. A pass is a numbered pass script — `p3_rocks.py`,
`pass04_bowl.py` — and for the three cohort painters who wrote one script instead, a pass
is their own numbered section. The painters' `check`, `cost` and `probe` scripts are not
passes and are not run, and nothing that writes a file is allowed to.

| Painting | passes | marks | spent | the page says | rebuild |
|---|---|---|---|---|---|
| `car_wash` | 21 | 212 | 211 | 206 | **off by 5** |
| `pears` | 17 | 241 | 229 | 224 | **off by 5**, and one pass raised |
| `dusk` | 12 | 185 | 184 | 184 | matches |
| `laundromat` | 16 | 301 | 286 | 286 | matches |
| `sonnet` | 10 | 275 | 274 | 274 | matches |
| `opus` | 13 | 313 | 296 | 296 | matches |
| `fable` | 16 | 288 | 284 | 284 | matches |
| `pool` | 31 | 281 | 242 | 221 | not claimed |
| `heron1` | 18 | 302 | 293 | 293 | matches, and one pass raised |
| `heron2` | 14 | 273 | 253 | 253 | matches |
| `greenhouse` | 14 | 422 | 297 | 297 | matches |
| `fogged` | 21 | 354 | 312 | 311 | not claimed |
| `pier` | 15 | 267 | 257 | 257 | matches |
| `hands` | 28 | 350 | 325 | 329 | not claimed |
| `bigpickle` | 8 | 53 | 50 | 50 | matches |
| `deepseek` | 5 | 76 | 68 | 68 | matches |
| `gemini` | 21 | 738 | 725 | 725 | matches |
| `glm` | 8 | 138 | 126 | 126 | matches |
| `gpt` | 44 | 483 | 408 | 408 | matches |
| `grok` | 6 | 155 | 132 | 132 | matches |
| `kimi` | 5 | 183 | 170 | 170 | matches |

**21 paintings, 343 passes, 5,422 strokes paid for**, and 16 of the 21 come back at the
stroke count their own page records. Three things the rebuild turned up that nothing
else would have:

- **`car_wash` and `pears` claim a rebuild and do not come back at their own stroke
  count** — five marks over, each. `car_wash` was re-run with only the nineteen passes
  its notes name, leaving out the two free planning passes, and came back at 211 again:
  it is not the pass list. A stroke count is a weaker test than the byte comparison the
  page claims, and it already fails.
- **Two committed passes do not run at all from a clean session.** `pears`'
  `p9_rehearse_pear.py` asks the palette for `pear_rim`, which no pass before it mixes;
  `heron1`'s `pass1_draw.py` uses `TREES`, which its prelude does not define. Both were
  written in a session that already had the name in scope.
- **`pool` comes back 21 strokes over**, and it is the one painting whose pass order had
  to be guessed: two of its passes share the number 5. Its page claims no rebuild.

### The noise budget, as 0.5.0 stands

What the tool says today, per pass, over that corpus. Lines marked `!` are call-time
warnings; the rest are `report()` findings.

| The rule | passes | share |
|---|---|---|
| bars: a stack of passes at one angle | 47 | **14%** |
| ! pressure changes the paint, not the width | 18 | 6% |
| round tips printing one disc | 21 | 6% |
| a loaded comb under the bristle floor | 17 | 5% |
| ! a clean edge on a narrow mass | 16 | 5% |
| a graded passage laid too narrow | 8 | 2% |
| a pressure list on a chisel | 8 | 2% |
| ! scumble: passes shorter than the brush | 5 | 2% |
| ! a smudge past the size that buys anything | 4 | 1% |
| ! scumble: a brush wider than the band | 3 | 1% |
| ! a tip too small to deposit paint | 3 | 1% |
| ! a round tip blocking in a feature | 2 | 1% |
| detail before the masses are down | 2 | 1% |
| ! sample() averaging over a mixed area | 1 | 0% |

**229 of 325 painted passes (70%) say nothing at all. The median pass prints 0 lines and
the busiest prints 11.** So the engine is quiet today, and the bars rule is half of what
noise there is — it fires on one pass in seven even with its said-once decay, which is
the number behind *it taught two painters to skim*.

What this counts is what asks a painter for something: findings and call-time notices.
The standing lines under a pass are measurements and are not in it — the engine this
table measured prints `ground:` after every painted pass, and the median is still `0` —
so the four canvas lines printed after every pass since 0.6.0 cost this budget nothing,
by design. Whether a longer block gets skimmed is for a painter's run to show, not for
this table.

### What each proposed check would cost

Prototypes of the checks the round proposes, run against every call and every pass of the
corpus. *Passes* is how many of the 325 painted passes it fires on; *guide* is how many
of the guide's 70 runnable python blocks it fires on, which is `LESSONS.md` rule 2 — *ask
what the rule says to a painter doing the right thing* — as a number.

| Candidate | from | fires | passes | share | guide blocks |
|---|---|---|---|---|---|
| `wet-under` | D2 | 241 | 71 | **22%** | **8** |
| `mass-is-a-stroke` | D1 | 118 | 60 | **18%** | **9** |
| `shallow-box` | D1 | 105 | 60 | **18%** | 1 |
| `buried` | D3 | 54 | 54 | **17%** | 0 |
| `holes` | E | 32 | 25 | 8% | 1 |
| `radiating` | D3 | 23 | 23 | 7% | 0 |
| `smudge-long` | D2 | 27 | 20 | 6% | 3 |
| `chisel-staircase` | D1 | 27 | 18 | 6% | 5 |
| `smudge-across` | D2 | 19 | 15 | 5% | 0 |
| `spill` | D1 | 17 | 14 | 4% | 5 |
| `glaze-far` | D2 | 25 | 12 | 4% | 1 |
| `inset-lost` | D1 | 5 | 3 | 1% | 2 |
| `cross-small` | D1 | 2 | 2 | 1% | 0 |
| `one-loop` | D3 | 2 | 2 | 1% | 0 |
| `scumble-few` | D1 | 1 | 1 | 0% | 0 |
| `smudge-again` | D2 | 1 | 1 | 0% | 0 |
| `ring-steps` | D1 | 0 | 0 | 0% | 1 |
| `ring-rim` | D2 | 0 | 0 | 0% | 1 |
| `round-soft-mass` | D1 | 0 | 0 | 0% | 0 |

**Four are over the ceiling.** `wet-under` at 22% of passes, `mass-is-a-stroke` and
`shallow-box` at 18%, `buried` at 17% — against about one pass in six for a habit rule.
The first three also fire on the guide's own blocks, so they are not merely noisy:
`mass-is-a-stroke` fires on **nine** of seventy runnable blocks, including `PAINTER.md`'s
first `block_in`, and `wet-under` on **eight**, because laying an opaque mass over paint
that is still wet is what the guide teaches and `dry()` is the exception.

**Two never fire on a real pass at all.** `ring-steps` and `ring-rim` fire on nothing in
the corpus and on one guide block each — and the pass they were proposed for, GLM's first
take, is the one whose calls were overwritten. Their evidence is seven frames and a
reconstruction, not a pass anybody can replay.

**`spill` and `chisel-staircase` fire where they should and on the guide too.** Each
fires on about one pass in twenty; each fires on five guide blocks, where the plan
expected two. The other three are the bill for the rule, and the round has to say whether
the block or the rule is wrong.

**Five are nearly silent**: `cross-small` (2 passes), `one-loop` (2), `scumble-few` (1),
`smudge-again` (1), `round-soft-mass` (0). `one-loop` is the one that matters: four of the
seven cohort painters reported the fault it names, and the committed scripts hold it
twice — because those painters **rewrote the passage before delivering the painting**.
The reports are real and the corpus cannot see them, which is a limit of this instrument
and not a verdict on the check.

### Where a threshold would sit

Every number the prototypes measured, fired or not. A threshold chosen from the tail that
happened to be over it is not a threshold.

| Measurement | n | median | p90 | max |
|---|---|---|---|---|
| `wet-under`: wetness under an opaque mark | 1749 | 0.091 | 0.410 | 0.654 |
| `mass-is-a-stroke`: brushes across the shorter extent | 299 | 2.33 | 5.17 | 13.49 |
| `spill`: `block_in` painted / place asked for | 234 | 1.126 | 1.474 | 4.249 |
| `spill`: `block_in` share of the paint outside the place | 234 | 0.148 | 0.355 | 1.000 |
| `spill`: `scumble` painted / place asked for | 65 | 1.287 | 1.573 | 2.525 |
| `spill`: `scumble` share of the paint outside the place | 65 | 0.256 | 0.408 | 0.604 |
| `buried`: share of earlier small or subject marks covered | 232 | 0.000 | 0.136 | 1.000 |
| `glaze-far`: value shift over the film's own footprint | 221 | 0.033 | 0.082 | 0.221 |
| `holes`: bare share inside a solid `flat` mass | 124 | 0.000 | 0.061 | 0.660 |
| `holes`: bare share inside a solid `bristle` mass | 18 | 0.000 | 0.042 | 0.092 |
| `radiating`: degrees fanned by the marks sharing a start | 96 | 11.9 | 75.2 | 90.0 |
| `chisel-staircase`: sloped share of the outline | 81 | 0.000 | 0.689 | 1.000 |
| `one-loop`: spread of the mark lengths, over their mean | 67 | 0.332 | 0.566 | 1.249 |
| `one-loop`: spread of the spacing along their own line | 67 | 0.723 | 1.255 | 3.162 |
| `smudge-long`: path length, in brush units | 37 | 0.168 | 0.527 | 0.721 |
| `smudge-across`: change along the path over change across it | 37 | 1.268 | 4.732 | 9.156 |
| `inset-lost`: share of the area kept | 32 | 0.784 | 0.876 | 0.927 |
| `ring-steps`: value step per ring | 5 | 0.014 | 0.019 | 0.021 |
| `ring-rim`: first ring against what the patch meets | 5 | 0.008 | 0.014 | 0.017 |

Three of these settle a threshold by themselves. **`glaze-far`'s `0.08` is the corpus's
own p90**: the films painters lay sit at `0.033` and the ones that make a new mass are
the top tenth, which is the shape a check wants. **A mass is 2.33 brushes across at the
median**, so `mass-is-a-stroke` at two brushes fired on 118 of the corpus's 299 masses —
two in five — which is a rule against the way masses are actually laid. And **every
inward `scumble` anybody committed steps `0.014`-`0.021` a ring**, well under the `0.05`
that draws a contour, so the five committed rings are the cure and not the fault.

### The measurement lines, on the finished canvases

`values:`, `edges:`, `pencil:`, `boxes:` and `unspent:` on every painting are what the
script prints. Three of the cohort's findings are decided by them, and two of those split
the cohort from the paintings that came before it:

| | all 21 | the seven | the fourteen before them |
|---|---|---|---|
| finish under the `0.5%` of bare ground the checklist asks for | 12 of 21 | 5 of 7 | 7 of 14 |
| median bare ground at the end | `0.38%` | `0.06%` | `0.49%` |
| budgeted paintings that stopped under 45% of budget | 5 of 19 | **5 of 6** | **0 of 13** |
| median share of the budget spent | 81% | 42% | 86% |
| share of edges under 2 px wide | 12%-44%, median 27% | 12%-37%, median 19% | 14%-44%, median 27% |

**Finding 15 is the cohort's, and it is sharp.** Five of the six budgeted cohort
paintings stopped under 45% of their budget, at a median of 42% spent; **none of the
thirteen budgeted paintings before them did**, at a median of 86%. Whatever that is, it
is not a property of the engine.

**Finding 11 is not the cohort's.** Half the corpus finishes under the bare-ground floor
the checklist asks for, and half of the fourteen paintings made before the cohort do
too — the seven are further down the same slope, not off it. The contradiction between
the graded-field recipe and the ground line is older than this round.

#### The `edges:` row above is measured with an instrument that did not work

Building workstream E turned this one over, which is the fourth mechanism this round
has had to correct after reporting it as *observed*, and the shape `LESSONS.md`
predicts.

**The rise width was measured on the top percentile of the gradient.** That selection
returns the *sharpest* pixels of whatever picture it is handed, so every canvas comes
back at the same place: painted for the purpose, a hard-edged `flat` mass, a ragged
comb and a fine scumble measured p25–p90 of **1.5–2.1 px** all three. And the
threshold was `2.0` px — which is exactly what the sharpest transition a pixel grid
can hold measures, because a one-pixel step of size *s* has a central-difference
gradient of *s/2* and a rise of `s / (s/2)`. A threshold sitting **on** the
discretisation limit is a coin flip, and it flipped the wrong way: the prototype
called the hard-edged mass **41%** hard and the ragged comb **84%**.

So **the 12%–44%, median 27% in the table above is float dust either side of `2.0`,
not a measurement**, and finding 13 has no number behind it until the corpus is
replayed with the instrument that shipped.

What shipped selects edges two ways instead, neither of them a percentile: a
**ridge** — the gradient at least as large as the gradient a pixel either side along
its own direction, which throws out both the tooth, whose gradients are not ridges,
and the broad interior slope of a graded mass, which has no crest — and a **step of
at least `0.10`** across it, because two masses closer than that read as one and a
transition smaller than that is not a boundary. The threshold moved to **`2.5` px**,
clear of the limit. The same four canvases then sit at 49%, 49%, 53% and **0%**, the
one at zero being the round soft brush, which is the only one of the four a painter
would call soft; and a canvas blurred numerically moves from 2.0 px median to 6.8.

**Still open:** the corpus replay wants re-running with this instrument before 0.6.0
states a spread for finding 13. Nothing else in workstream E is affected — `values:`,
`pencil:`, `holes:`, `boxes:` and `unspent:` all reproduce their prototypes, and
`holes:` reproduces B2's three grounds to the third decimal (`0.1543%` / `0.1350%` /
`3.1601%` against `0.1552%` / `0.1357%` / `3.1550%`, off a different seed).

### The default moves

Each move, with what it buys measured on a scratch canvas and what it would cost measured
over the corpus.

| Move | What it buys | What the corpus leans on |
|---|---|---|
| `cover()` to `edge="hard"` | `ragged` paints **2.32x** the area it is handed, `clean` 1.06x, `hard` 1.01x | **No committed pass script calls `cover()` at all** — the move is free, and so is the evidence for it |
| a round tip on `block_in`/`sweep` to `pressure="even"` | not re-measured; the docs' own claim | **0 committed calls** would move |
| a banded `scumble` to `load=1.0, load_falloff=0.0` | bare **5.17% to 0.01%**, ripple **0.0111 to 0.0031** | **40 of 60** committed banded scumbles type the clause by hand — **moved in 0.6.0**, and re-measured where it landed under *The load a band is laid at* |
| a `scumble` with a `flat` to halved `jitter`/`size_jitter` | ripple down the band **0.0053 to 0.0059**, scallop across it 0.0052 either way | 15 committed scumbles use a `flat`; the halved pair changes nothing this measures |
| `edge="hard"` to two brushes of overhang | B8's table: `0.80%`-`2.86%` bare inside the line to `0.055%`-`0.285%` on a round tip | **55 committed calls at `edge="hard"`, none naming an overhang** — every one would move. **Moved in 0.6.0**, and re-measured where it landed under *The bites just inside a hard edge* |

The banded-scumble default is the one the corpus argues for loudest: two painters in three
type the clause by hand. The `cover()` move costs nothing because nothing uses `cover()`,
and the halved-jitter move buys nothing this measurement can see.

### The claims, re-measured

One row per claim the round is built on, against the engine as it is. *Survived* means
the claim is true and its number is close to what was reported; the others say what
moved.

| Claim | What the probe found |
|---|---|
| **The chisel staircase** (finding 1) | **Survived, and it is a comparison and not a constant.** On the lit band: `flat` at `0.020` leaves **22%** of its strong edges within ten degrees of horizontal and `0.010` leaves **15%**, against **1%** for a `bristle` and **1%** for `round_hard`. On Kimi's rock face, whose boundary slopes the other way, the same brushes give **7% / 19%** against **4%** and **2%**. Several times as many pass ends from a chisel, every time — but the share belongs to the band as much as to the brush. `edge="hard"` does not close it: these are pass ends *inside* the mask. |
| **Holes inside a `solid=True` mass** (finding 2, B2) | **Survived, with the mechanism corrected twice.** A `flat` leaves `0.0000%` bare at every size and density tried. The comb leaves them: `bristle` at `size=0.04, density=0.8` leaves **0.1552%** in **47** blobs, the largest **198 px**; at `density=1.2` it is **0.0000%**. `solid=` cannot close them — it sets `load` and `load_falloff` and nothing else. **And a hole is a contrast, not a gap**: the same call leaves `0.1552%` on `toned_grey`, `0.1357%` on white, and **3.1550% in 373 blobs, the largest 2270 px**, on the dark `#2e332c`. *Bare* means within `10/255` of the ground, which is what `ground_showing()` means by it and what an eye means by it — so a dark mass on a dark ground is where the comb's holes are visible at all. |
| **A smudge drags a thumbprint** (finding 3) | **Survived, and it is a depth.** A hard step from `0.20` to `0.78`, one smudge at `size=0.04`: run **along** the join it lifts 11,024 px and stops **0.5 brushes** into the dark; run **across** it lifts 1,561 px and carries them **4.1 brushes** in — the length of its own path. At 30 degrees, 1.9 brushes. |
| **A glaze far from its ground** (finding 4) | **Survived, with the window measured.** One film at `opacity=0.15` over a mass at `0.30` moves the value `0.014` when it is mixed `0.05` away, `0.052` at `0.25`, **`0.080` at `0.40`** and `0.110` at `0.55`. So the `0.08` that makes a *new* mass rather than shifting an old one is a film mixed about `0.40` off what it lands on, at that opacity. |
| **A scumble lands outside its band** (finding 8, B17) | **Survived, to the second decimal.** A band `0.20` tall at `n=8` with the auto brush paints **1.42x** its own area at `"axis"`, **2.99x** at 30 degrees and **3.62x** at 60 — against the plan's 1.43x / 2.84x / 3.53x. At 60 degrees **72%** of the paint lands outside the band, and the auto brush has gone from `0.075` to `0.297`, because the step is measured across the *bounding box*. |
### The eighteen reported bugs, re-measured

| # | What the probe found |
|---|---|
| B1 | **Confirmed.** `stroke`, `dab`, `glaze` and `smudge` take `clip=`; `block_in`, `sweep`, `cover` and `scumble` raise *`clip=` is not a brush field*, which names neither `stroke(clip=)` nor `edge="hard"`. `scumble(edge="hard")` raises an error that names `block_in()` and `sweep()` and not the caller. |
| B2 | See *Holes inside a `solid=True` mass* above. |
| B3 | **Confirmed.** A rehearsal copy comes back with `timelapse=False` and 0 frames, and `timelapse_gif` on it raises *No time-lapse frames were recorded. Create the session with `timelapse=True`* — which is the one thing the painting already did. |
| B4 | **Confirmed.** A frame of a 1440×960 painting is **360×240**, and nothing on `Session` or the CLI can ask for another size. |
| B5 | **Confirmed, and it prices what it cannot paint.** A stroke plan costs 1 and a mass plan 11; a `sweep` plan raises for a missing `into=` and a `cover` plan raises *a stroke spec needs 'points'*. A scumble-shaped plan carrying `shape=` **quotes 5 where the call lays 8**. |
| B6 | **Confirmed.** A log of four records holding two strokes: `undo(1)` leaves three records and **still two strokes** — it scraped back the `dry`. `log(last=3)` counts the same three records. |
| B7 | **Confirmed to the character.** **35** characters outside cp1252 across the five shipped documents — **31 of them in this file** — and exactly four distinct ones: a rightwards arrow x18, a true minus x10, *approximately equal* x2 and *less-than-or-equal* x1. **0** non-ASCII characters in `src/easel/`, so no notice and no `report()` line can do it: it is `print(easel.docs.read(...))` that dies. (This section says which characters they are rather than showing them, which is the fix the round makes to all five documents.) |
| B8 | **Confirmed, and it is the round tip's bug more than the chisel's.** The 3 px strip inside a sloping outline, `solid=True`: a `flat` leaves `0.02%`–`2.88%` at `ragged` and `0.00%`–`0.41%` at `hard`; a `round_hard` leaves **6.78%–11.07%** at `ragged` and **0.80%–2.86%** at `hard`. At `overhang=2.0` every case is **0.000%–0.285%**. The bites are pass ends arriving at part pressure, so a round tip — which loses width with pressure — is worst. |
| B9 | **Confirmed and reproduced exactly.** Five subject marks, three signature marks and one pencil line: `stroke_count` is **5** and `report()` says *subject: 5 of 8 marks so far (62%)*. |
| B10 | **Confirmed.** `import easel_paint` raises `ModuleNotFoundError`. README's install line is line 103 and its nearest import is line 27 — **76 lines away**; `llms.txt` and the package docstring both put the import beside the install. |
| B11 | **Confirmed both ways.** `palette['toned_grey']` lists every pigment and slot and never mentions that the name is a ground; `Session(ground='ultramarine')` lists every ground and never mentions that the name is a pigment. |
| B12 | **Confirmed, and it is a ninth.** `top`, `bottom`, `left`, `right` and `center` are 0.33 × 0.33 cells of a 3×3. The full-width places are `lower-band` (y 0.600–1.000) and `lower-half` (y 0.500–1.000). |
| B13 | **Confirmed.** `[200, 100, 50]` is accepted in silence and comes back **`#ffffff`**. |
| B14 | **Confirmed.** `solid=True` is accepted by `block_in` and refused by `cover`, `stroke`, `sweep` and `scumble`, with an error that explains it is a pair of brush defaults — which is the argument for accepting it. |
| B15 | **Confirmed as a fixed cost per stroke.** At 1024×768: a snapshot 3.6 ms, a 360 px frame **42.3 ms**, one wide `bristle` pass 330.7 ms. At 1440×960: 6.3 ms, **60.5 ms**, 436.9 ms. One snapshot is 19 MB / 33 MB and 24 are kept — **453 MB / 796 MB resident**. The frame is an order of magnitude dearer than the snapshot, and both land before a dab does. |
| B16 | A feature, as the plan says. A rehearsal is free — the count does not move — and `rehearse(vary=)` does not exist, so a sheet of one mark at four sizes is four rehearsals, each rendering the whole canvas. |
| B17 | See *A scumble lands outside its band* above. |
| B18 | See *GLM's rings* below. |
### GLM's rings (B18)

The concentric rings on the wall right of GLM's monitor cost that session its one
`undo`, and three accounts of them have been wrong: the painter's (*six crossing glazes
laid wet, then a block-in*), the round's first check, and the round's second. The calls
are gone — the first takes of `pass1b.py` and `pass2.py` were overwritten and their
marks undone — so what is left is seven frames from the painter's own working folder,
committed under [`paintings/GLM/terminal_window/rings/`](paintings/GLM/terminal_window/rings/),
and one thing nobody had noticed: **the patch is still in the prelude.** `halo =
blob(span("C1","G6"))` sits beside the `halo2 = blob(span("C2","F4"))` that take three
replaced it with, and the larger one overshoots the glass onto the wall exactly where
frame 6 puts the rings.

Rebuilt on GLM's own canvas after `pass1a.py`, an inward `scumble` over that patch, with
the bezel under it:

| value span | `n` | step per ring | value steps across the patch | darkest band | a wet bezel moves it by |
|---|---|---|---|---|---|
| 0.20–0.26 (take three) | 5 | 0.015 | 3 | 0.20 | 0.075 |
| 0.20–0.26 | 10 | 0.007 | 4 | 0.18 | 0.071 |
| 0.14–0.30 | 5 | 0.040 | 8 | 0.14 | 0.098 |
| 0.14–0.30 | 10 | 0.018 | 8 | 0.14 | 0.078 |
| 0.14–0.35 | 5 | 0.052 | 9 | 0.16 | 0.133 |
| 0.14–0.35 | 10 | 0.023 | 10 | 0.14 | 0.098 |

**Two answers, and both halves of the round's reading survive.** The rings are the
inward scumble's own contours — a step of `0.04` a ring prints eight visible bands
across the patch, and the low-contrast take that replaced it prints three. And the wet
bezel is not innocent: laying the rings over it wet moves pixels by up to **0.13**,
which is past the `0.10` that makes a new mass. The bezel reads `0.14`, and the darkest
band in the wide-span reconstructions reads `0.14` too — which is the band frame 5
shows.
