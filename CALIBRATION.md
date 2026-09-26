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
| A held edge breaks inward over `0.002` of the long side; a thin shape keeps its body; two masses held to one line leave the ground between them | *A held edge, broken (0.7.0: the default moved)* |
| A shaped mass with `direction` left off can cost many times its axis | *A shaped mass with `direction` left off* |
| A sequence of directions is priced as the sum | *`direction` given a sequence* |
| A sweep follows an edge; crossing closes it | *`sweep`* |
| A smudge buys nothing past `0.02`, removes about half a join once, and works along not across | *`smudge`* |
| A glaze far from its ground has no usable opacity | *`glaze`* |
| An inward scumble is a glow; three steps of brush is the window; `n` is bounded by the patch | *`scumble`* |
| A band's brush is three steps; a wedge needs two bands; `opacity` does not quieten a passage | *The band, and the brush that closes its joins*, *The band across a wedge*, *Opacity does not make a passage quieter* |
| A chisel does not taper; a chisel ending on a slope is a staircase; a pressure list's fade arrives late | *Pressure*, *The chisel staircase* |
| A dab is a light touch; `press=3` lands; scale a mark off the thing | *At the scale of a feature* |
| A bristle under `0.025` is four streaks; round tips repeat, `tip_wobble` redraws | *The bristle comb* |
| A rehearsal is the next strokes; `pencil`, `dry` and `erase` are logged | *The log, undo, and the stream* |
| A file opens as painted and rebuilds as the engine installed lays; its time-lapse is the log | *The log, undo, and the stream* |
| What a mass costs, before the call | *Budget* |
| A daisy leaves one point every way; a loop is one length at one spacing; a film or a mass takes what was showing | *What the check reads after a pass* |
| Rehearsal counts, subject shares, the form window, the cast-shadow steps | *From the sessions* |
| What the 0.5.0 round measured: the corpus replay, the noise budget, the candidates | *The 0.5.0 cohort's round* |
| What the lighthouse handover's round measured: an edge that is not a step, a dry brush that streaks, the graded rule's misfires, the file | *The lighthouse handover's round* |
| What the bell-warden's round measured: guides on any ground, the arrangement flat and small, the terminator, what a pass costs call by call, marks that land short or nothing, a key, what a place reads, the floor, a named light, a place laid over, rings, drawing units | *The bell-warden's round* |

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
- A pass laid at `0.5` because it sounded painterly leaves a broken film that
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
- The texture decides the breakup and the travel its direction: `rough` skips in
  chunky islands, and `linen` and `smooth` break into dashes that run with the
  stroke, because since 0.7.0 a brush under `0.9` of its load is gated against the
  tooth read along its travel, a thread of linen long, and a comb's bristles run dry
  one by one. Before that `linen` speckled at the scale of the weave; *A dry brush
  that streaks*, under the lighthouse handover's round, has the numbers.
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

**A region is asked the same, since 0.6.0.** The rule was a shape's only, and `cover()`
is handed a region far more often than a shape. F1's bench found the gap: with the
default `flat` at `size=0.1`, the brush is `150%` of a repair-sized place's shorter
extent, 108×60 px on 900×600; the inset keeps a sliver, the fill is two stubs in its
middle, and `8%` to `15%` of the mistake being buried stays showing on a painted passage
(*A burial and the place it was handed*, below). The line names the call the painter
made, and a burial's remedy is its own default rather than the ragged edge. Read off
the committed pass scripts, every `edge="clean"` in the corpus and in the guide is
handed a shape, so the rule's count does not move.

### Paint that lands outside the place

A pass stops where its *centre* meets the outline, the brush hangs half its width past
it, and the ends run on by the overhang — so the multiple of its place a call covers
grows with the brush's share of that place, and past a point the call is painting its
neighbours as well. `block_in` (ragged) and a banded `scumble` say so at the call
(`spill`) once the passes they are about to lay will cover **1.6x** the place or more —
**2.0x** for a band, whose own brush breaks past it by design (below).

**Predicted off the passes, not read off a rule of thumb.** The plan's version was *a
brush over a fifth of the shorter extent*, and `PAINTER.md`'s own first `block_in` lays
a brush 60% of its shape and lands 1.48x of it: the fraction does not paint the
neighbours, the multiple does. So the call walks the passes it will lay, on a copy of
the stream, and lays each as a strip reaching this far past its line, in half-brush
widths — fitted on 126 masses and bands laid for the purpose on 400×300, 1024×768 and
900×200 canvases, painted, and measured the way the corpus replay measures a call (a
pixel whose value moved by more than `0.004` is painted):

| tip | across the pass | past its ends | mean error against the paint |
|---|---|---|---|
| `flat`, `knife` | 1.00 | 0.2, square | 1.8% |
| `bristle`, running dry | 0.90 | 0.4, square | 4.7% |
| `bristle` laid solid (a banded `scumble`, or `solid=True`) | 1.05 | 0.2, square | 1.7% |
| `round_hard`, `round_soft` | 0.80 | 0.8, round | 4.2% |

The solid comb's row was fitted on bands and borrowed for masses, so it was checked on
90 more: `block_in(..., "bristle", solid=True)` on five places, two canvases, three
sizes and three directions comes in at 1.7% on average and 6.5% at worst.

**Under 12 pixels a brush does not land where its outline says**, and the rule stays out:
a comb that narrow is a few streaks with gaps and a chisel lays next to nothing
(`chisel-blank`). On the same bench a 7 px `flat` predicted at 1.68x came back at
0.65x, and a 10 px comb at 1.65x came back at 0.47x.

**The threshold is over the corpus's tail and over the guide.** Over the 299 masses of
the 21 paintings, a `block_in` covers `1.126` times its place at the median and `1.474`
at p90, a banded `scumble` `1.287` and `1.573` (*Where a threshold would sit*, below);
no mass the guide recommends lands over `1.49`. On the bench, `1.6`
with the pixel floor fired on 78 calls whose paint was over it, missed none, and fired
twice on calls whose paint was not — both predicted at `1.63`–`1.65` and measured at
`1.55`.

**A band's line is `2.0`**, and the suite is what said so. A banded `scumble`'s brush is
three of its own steps and breaks past the band on purpose — and on a canvas that is not
square the step is taken in the canvas's *height* while the brush is sized against its
long side, so in pixels it is more than three. The band the verb's brush was tuned on,
`0.80 × 0.40` at `n=8`, covers **1.69x** itself laid along its own axis at 320×240, and a
square scumbled in six passes 2.29x; at `1.6` the first would have been told it spills by
the very test that asserts it is the case to copy. Mapped by prediction over seven
canvases, seven places and six pass counts, bands laid along their own axis cover a
median of `1.63x` (p90 `2.42x`) and the same bands crossed at 30 to 60 degrees `2.90x`–
`3.03x`. At `2.0` three in four of the first stay silent — the rest are squares given
four to six passes, whose own brush is two-thirds of the place or more, and which do lay
a smear twice their size — and 85% of the second are told. A rule on the mechanism instead
(*the brush is wider than the band is deep*) was tried and missed angled squares at
`3.2x`–`3.5x`.

**Over the corpus** the engine's own `spill` fires on 18 calls in 13 of the 325 painted
passes — **4%**, the prototype's share — and where it spoke the paint measured a median
of `1.71x` (p90 `2.42x`). On 4 of the 18 it measured under `1.6x` (`1.23x`–`1.58x`). The
replay's only test for *painted* is a value moved by more than `0.004`, so paint laid on
paint of its own value is invisible to it and the measured multiple is a floor; that
those four are such cases is a reading, not checked call by call. Whether a spill onto
paint of its own value is worth saying at all would take the canvas under the
footprint, a D2 question asked of a D1 rule, and was **ruled not this round**
(2026-09-22): the line says where the passes land, which is true either way.

**Its first remedy can set it off again, at sizes the guide never uses.**
`Polygon.inset()` keeps no record of the shape it came from, so a mass inset by half its
brush is measured against the inset shape rather than the outline it was inset to stay
inside. At the guide's own numbers that is silent (`1.44x`), and a test holds it; a
brush that is itself most of its mass, inset the same way, would be told it spills when
the paint it counts as outside is the margin the inset left for the brush. Seeing
through it needs a field on `Polygon`, which rides in the log, and was **ruled not this
round** (2026-09-22).

**It fired on three of the guide's own blocks**, and all three were painting their
neighbours, so the blocks moved and the rule did not:

| block | as written | now |
|---|---|---|
| `PAINTER.md`, exercise 1, the value scale | `2.00x`, 189 strokes | `direction="axis"`, `1.36x`, **27** strokes |
| `PAINTER.md`, exercise 9, the swatch strip | `1.96x` | `size=0.04`, a fifth of the swatch's width, `1.45x` |
| `PAINTING.md`, *Per-stroke overrides* | `2.79x`, a `flat` wider than its cell | `span("C4", "F6")`, `1.38x` |

**Not said inside `cover()`.** Since 0.6.0 its default holds a burial to its place (*A
burial and the place it was handed*, below), so there is nothing to say; asked for
`edge="ragged"` by name, it runs its ends outside on purpose and paints about three
times a cell, and a rule that fires on the form a painter asked for is a rule painters
learn to ignore.

**A band crossed at an angle (B17).** A banded `scumble` picks its brush from the step
between its passes, and the step from the band's extent *across the passes* — which,
crossed at an angle, is most of the band's length rather than its depth. A band `0.10–
0.90 × 0.40–0.60` on 1024×768, `n=8`, painted from burnt umber to ultramarine on
`toned_grey`; *bare* is the band's own area left unpainted between passes:

| direction | auto brush | covers | capped at the band's depth | capped at half its depth |
|---|---|---|---|---|
| along its axis | `0.075` | `1.49x` | `1.49x` | `1.49x` |
| 30 degrees | `0.215` | **`2.95x`**, 66% outside | `2.22x` | `1.36x`, `3.2%` bare |
| 60 degrees | `0.297` | **`3.57x`**, 72% outside | `2.04x` | `1.16x`, `15.8%` bare |

**So the auto brush is not capped.** A cap that stops the spill brings the bars back,
and the angle is the painter's, with the gradient running along it. The remedy that
keeps both is the hold: `edge="hard"` lays the same passes and masks every dab to the
band, and the notice names it first. At 60 degrees every pass is shorter than the brush
and `scumble-dabs` already says the paint blooms past the band, so `spill` stands
aside: one notice per bloom.

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

These were measured with the edge cut on the line, as it was then. Since 0.7.0 the edge
itself breaks over the feather's depth on purpose (*A held edge, broken*, next), which is
a different thing from a bite between pass ends, and the tests hold this table at
`feather=0`.

### A held edge, broken (0.7.0: the default moved)

Until 0.7.0 a hold -- `clip=`, `edge="hard"`, `cover()` -- cut its edge on the line: the
mask was the outline's coverage at two samples a pixel, so a boundary was one pixel of
four possible values and then a step, `0.30` of value in one pixel at the lighthouse
handover's tower. The edge now breaks **inward, against the canvas's own tooth**: over
`feather=` of the long side inside the outline (`0.002` left off), each pixel's need
falls with its depth, from the tooth's own ceiling on the drawn line to nothing at the
feather's depth, and the pixel takes paint as far as its tooth clears the need, over the
stamp's own band. Near the line only the peaks of the weave take paint; deeper in, the
valleys do too. **Nothing lands on or past the line**, a side lying on the canvas frame
is not an edge, and where a shape is narrower than four feathers the edge reaches full
paint a quarter of the way across it. The bench it was chosen on, blind, is *An edge
that is not a step*, under *The lighthouse handover's round*.

**Neither of the check's two numbers for an edge can see it**, by construction: every
pixel stays crisp and the boundary breaks where the tooth is low, so the one-pixel step
and the `edges:` line read it as a cut. Laid by the lighthouse handover's own thirteen
scripts, the tower's step reads `0.288` against `0.290` cut, and the `edges:` line ends
at `54%` either way. The eye is the instrument.

**The unit is a share of the long side, like `size`**, measured at 1440x960, where the
painter found the bench's copy *a little chewed*. The painter's own measure on a rock laid
hard on bare ground -- its steep left side row by row: how far the edge wanders about a
straight line (sd) and its largest bite, in pixels -- at the export's own pixels, and in a
look at the default 1024 long side (`probe_handover_session.py --edges`):

| canvas | feather | wander | largest bite | in a look: wander | bite |
|---|---|---|---|---|---|
| 1024x768 | cut | 0.28 | 0.46 | 0.28 | 0.46 |
| 1024x768 | `0.002`, 2.0 px | 0.40 | 0.94 | 0.40 | 0.94 |
| 1024x768 | `0.003`, 3.1 px | 0.51 | 1.29 | 0.51 | 1.29 |
| 1440x960 | cut | 0.24 | 0.27 | 0.17 | 0.19 |
| 1440x960 | `0.002`, 2.9 px | 0.44 | 0.94 | 0.32 | 0.67 |
| 1440x960 | two pixels, `0.0014` | 0.38 | 1.06 | 0.27 | 0.75 |

At 1440 the share bites at the export's own pixels as 1024's does, and two pixels are no
closer; in the look both are crisper than 1024's, as anything shrunk is. The weave the
edge breaks against scales with the canvas and the grain does not, which is why neither
unit is exact. The largest bite is one row's and noisy; the wander is the steadier number.

**A thin shape keeps its body.** A strip narrower than two feathers has no inside as deep
as the feather, and ramped over the whole feather it would be broken from both sides into
its middle. A stroke clipped to a strip, `flat` at `size=0.03`, laid solid, 1024x768
linen, at the default -- the share of the strip's pixels that took paint:

| strip | cut | ramped over the whole feather | over a quarter of the width (built) |
|---|---|---|---|
| 2 px | 100% | 37% | **100%** |
| 3 px | 100% | 60% | 68% |
| 4 px | 100% | 70% | **99%** |
| 6 px | 100% | 79% | 91% |
| 8 px | 100% | 84% | 87% |
| 12 px | 100% | 90% | 90% |

The 3 px strip's top line runs through a row of pixel centres, and that row, being on the
line, takes nothing -- a third of the strip. A shape wider than four feathers is untouched.

**Two masses held to one line both break back from it.** A mass laid over paint breaks
over that paint, which is what the feather is for. Two laid *up to one line* on bare
ground, each held to it -- `block_in(..., solid=True, edge="hard")` either side of
`x=0.42`, `flat` at `0.08`, 1024x768 -- both break back from it, and the ground shows
along the seam. The share of an 8 px band on the seam within `10/255` of bare:

| ground | cut | broken | broken, the first laid past the line |
|---|---|---|---|
| `burnt_sienna` | 0.0% | 14.6% | 0.0% |
| `toned_grey` | 0.0% | 14.6% | 0.0% |

A broken line of ground where two masses meet is an outline: the guide's *paint masses,
never up to a line*, arriving as a picture. No committed painting lays its masses that
way -- over the ten whose scripts hold an edge, the longest run of ground the feather
uncovers is 12 px (*The lighthouse handover's round*) -- so it is a number here and not a
check. One of `RECIPES.md`'s passages did, and lays its first mass past the line now.

### A burial and the place it was handed (0.6.0: the default moved)

Until 0.6.0 `cover()` ran its passes a full brush past the place it was handed — the
burying recipe's ends outside, so no chisel end stops inside the picture. On a flat
passage that cannot be seen. Burying a mis-made leaf in a finished pane of glass, it
laid a flat pale panel across a patch visibly larger than the leaf's, and the painter
buried `cover`'s own output by hand. The default is `edge="hard"` now: the same passes,
every dab masked to the place, and two brushes of overhang carrying every pass end up to
the outline (*The bites just inside a hard edge*, above).

The bench it was ruled on, rebuilt as `probe_f1_burial` in
`scripts/probe_cohort_session.py`: a place `0.44–0.56 × 0.42–0.52`, 108×60 px on a
900×600 `toned_grey` canvas, with a light stroke laid across its middle and dried, then
buried in the passage's own colour — sampled from the place before the mistake went
down, which is what a painter mixing to match would do — with the default `flat` at
`size=0.1`, 90 px, most of the place. Three passages under it: *flat*, one solid mass;
*graded*, a scumble from `0.25` at the top of the canvas to `0.75` at its foot, so the
value moves about `0.05` across the place; *worked*, the same field with four hundred
short bristle marks at values scattered round its own. *Seen* is what a viewer can find
— the pixels left `0.02` or more off the passage as it stood before the mistake — as a
multiple of the place, and how much of that lies outside it; *showing* is the share of
the mistake's own pixels still nearer the mistake than the passage; *outline* is the
mean value step across the place's rectangle, 2 px either side of it, beside the
passage's own step there:

| passage | edge | seen | of it outside | showing | outline (the passage's own) |
|---|---|---|---|---|---|
| flat | `ragged` | `0.00x` | `0.00x` | `0.0%` | `0.0000` (`0.0000`) |
| flat | `hard` | `0.00x` | `0.00x` | `0.0%` | `0.0010` (`0.0000`) |
| flat | `clean` | `0.05x` | `0.00x` | `8.0%` | `0.0001` (`0.0000`) |
| graded | `ragged` | **`4.45x`** | `3.98x` | `0.0%` | `0.0003` (`0.0076`) |
| graded | `hard` | **`0.47x`** | `0.00x` | `0.0%` | `0.0450` (`0.0076`) |
| graded | `clean` | `0.53x` | `0.21x` | **`12.7%`** | `0.0077` (`0.0076`) |
| worked | `ragged` | **`4.14x`** | `3.63x` | `0.0%` | `0.0001` (`0.0097`) |
| worked | `hard` | **`0.51x`** | `0.00x` | `0.0%` | `0.0417` (`0.0097`) |
| worked | `clean` | `0.51x` | `0.18x` | **`14.9%`** | `0.0104` (`0.0097`) |

Every pixel the call moved at all is `5.3x`–`6.4x` the place laid ragged and `1.00x`
held; on a flat passage that multiple is all there is, and none of it can be seen.

**Held, the fault is the rectangle.** On a worked passage the place's own outline comes
back as a step of `0.042` where the passage has `0.010`: a crisp patch exactly the size
of the place, which does read as cut out. Ragged leaves no step at the place, because
its patch ends a brush and more further out — in a burial eight times the size of the
held one on the same passage, with the neighbouring marks under it. The smaller fault is
the default. **Since 0.7.0 the patch's border is broken rather than cut** (*A held edge,
broken*, above), and the rectangle is still there: a feather inward changes how the
place is crossed and not what it is, so the outline's step stays `0.0417` while its
largest one-pixel step goes `0.047` to `0.043`, and *seen* `0.51x` to `0.48x`.

**`clean` is the worst of the three at this size.** The inset takes the place rather
than a rim of it, the fill is two stubs in the middle, and the contour pass does not
reach the place's ends, so the mistake shows at both — `22.4%` of it on bare ground.
Nothing said so, because `clean-small` asked shapes only; it asks regions too now (*A
clean edge on a narrow mass*, above). **No committed pass script calls `cover()`**, so
no committed painting moves.

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

- **It is much stronger than "moves paint around" suggests, and along a join it is
  symmetric.** One pass at `size=0.04` along a dried hard step from `0.20` to `0.78`,
  1024×768: the light carried `0.49` brushes into the dark and the dark `0.49` into the
  light, `5,510` px against `5,674`. This bullet used to say it pulled the lighter mass
  into the darker more than the reverse. That claim recorded no conditions, it does
  not reproduce on this step with 0.5.0's engine or 0.6.0's, and the light cap every
  smudge laid at its start until 0.6.0 (below) is the likeliest thing it saw.
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
  of the first mass into the second, either way round, and leaves a finger-shaped
  thumbprint about a brush long (below); run along the boundary in short passes it does
  what it is for.
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

### Across a boundary, and along a long one

**A smudge carries only what it has picked up (0.6.0: fixed).** Until 0.6.0 a smudge
started loaded with its nominal colour — titanium white — and mixed `45%` of the
canvas into it per dab, so its first dabs laid `55%`, `30%`, `17%` white: a light cap
at the start of every smudge, on a passage of one colour as much as at a boundary.
Over a mass of one colour at `0.45` the first brush of the path came back `0.13`
lighter, and `0.11` over one at `0.15`; it now moves nothing there. The cap is part of
what painters called *a thumbprint at the end of a smudge*, and it is what the round's
own probe measured as crossing: the thumbprint row under *The claims, re-measured*
carried the light `4.1` brushes into the dark on a pass that *started* in the dark —
the cap, laid from the first dab on. With the start fixed the same pass carries it
`0.5` brushes, no further than a pass along the join.

**Across a boundary it drags the first mass about a brush into the second.** One pass
at `size=0.04` straight across that step: from the light into the dark, `1,577` px
lifted, reaching `1.2` brushes in; from the dark into the light, `1,623` px darkened,
reaching `1.2` brushes in. That is the finger-shaped lobe, and `smudge-across` says it
at the call, off the canvas the smudge is about to meet: along the path the stroke will
be stamped down — the spline, a quarter-brush at a time — the value half a brush
behind and ahead, and half a brush either side. A **step of `0.10`** or more, more of
it along the path than across it, with half a brush of path before the line and a
quarter after it, is a crossing; the line is where the value on the path passes
halfway between the two masses. A pass that only starts or stops on the line carries
half a brush across at most, which a pass along the join does as well, and is not told.

**Along a long boundary it leaves a band** — the strip in the table above, about a brush
tall at the value halfway between the two, the same over `0.05` as over `0.80`. Laid
on a step, it is a pill at `0.05` and a drawn line of a third value from `0.10`, and the
same at a step of `0.07` between two colours as at `0.59` between two greys: a join
between colours at close values still leaves a strip of a third colour. `smudge-long`
says it when the path follows a **step of `0.05`** or more across it — half the `0.10`,
because the strip lands halfway — for more than **`0.10` of the canvas**. A habit and
not a fact: two paintings smoothed the broken lit edge of a heron's neck this way and it
read as intended.

**Over the corpus**, of its 37 smudges, `smudge-across` speaks on 11, in 9 of the 325
painted passes (3%), and `smudge-long` on 14, in 11 (3%) — neither on any of the
guide's blocks. Every crossing it names is a real one, at steps of `0.11` to `0.36`: a
dark hull dragged out into the water, a lamp housing dragged down the column under
it, a post's edge run down over the rungs that cross it, finger stripes smeared into
each other. Both herons' necks are among the long ones — passes run along a lit edge,
where the band was the smoothing their painters wanted — which is why that one is a
habit.

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

### A film far from what it lands on

Finding 4 of the 0.5.0 cohort: *green blooms over blue water, a searchlight on a flat
sheet*. `glaze-far` reads a film once it has landed, over its own footprint — every
pixel whose colour moved more than `0.005` in Oklab — and says it two ways:

| | the line | why there |
|---|---|---|
| **the value moved** | `0.08` | the table at the top of this section: a warm film at `0.14` moves it `0.085`, *a stripe of a different colour*. The corpus's own p90 is `0.081` |
| **the film was mixed far**, in hue and chroma (Oklab *a/b*) from the colour it lands on | `0.07` | the recipes mix their films `0.031`-`0.051` from the field; every film the corpus shows as a bloom sits at `0.080` or more — the harbour's searchlight `0.085`, a lighthouse's orange glow over a violet sky `0.190`. The corpus's p90 is `0.068` |

The value line is not said about a film given `to_value=`, which asked for its shift.
The mix line is: the search lands a value, and the colour it lands at is still the
film's. None of the thirteen aimed films in the corpus was mixed further than `0.033`.

**The distance is in the mixing, not in the result**, and the first instrument tried
was the result: how far the film moved the hue. It does not separate the two cases.
The lit-air recipe's own film moves the hue `0.018` and the harbour's searchlight
`0.026`, and this section's own table says why: the far film moves the hue `0.034` at
`0.05` — *already neutral* — and `0.057` at `0.10`, where it reads *warm*. What is
wrong at every opacity is where the film was mixed, which is what *mix the glaze close*
has always said.

**Over the corpus** it speaks on 38 of the 222 films, in 17 of the 325 painted passes
(5%) — 22 by the value line, 16 by the mix line alone — and on none of the guide's
blocks. Thirteen of the 38 are one pass of one painting's glitter path, which the
notice block prints once with its count. The mix line is what reaches the films the
value line could not see: the harbour's searchlight moved the value `0.020`, and the
orange glow over a violet sky `0.061`.

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

### Ramps laid over one another, wet or dried between

A graded field is two or three ramps, overlapped, and whether the one underneath is
still wet decides how much each takes from the other. The lighthouse handover's sky —
`p01_sky.py`'s three 8-pass scumbles at `opacity=0.95`, 1024×768 linen on
`burnt_sienna` — laid one after another on a fresh canvas, and again with `dry()`
between them: **drying between the ramps moves 16% of the canvas by more than two 8-bit
levels of value and 5% by more than eight, and 34% and 13% in the export's colour, any
channel.** Neither draws a seam: the median jump from one column to the next is `0.0002`
both ways, the largest at the canvas's own edges.

**A number for choosing, not a rule.** Laid wet, a ramp picks up what it crosses where
the two overlap; dried between, each lands as it was mixed. `wet-under`, a notice at the
call for an opaque mark laid on paint still wet, was declined in 0.6.0, and this reopens
nothing. The number is `probe_handover_session.py --pressure`'s, under *The fade and the
wet bands* below.

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

**On a long pass a light pressure makes far more than its share of the change**,
because the dabs overlap and each lays its fraction over the last: *`opacity` does not
thin a long stroke*, one argument over. The table above counts the paint a mark lays;
what a painter sees is the value it moves, and that saturates. A pass laid at one
pressure along its whole length, as a share of the change the same pass makes at full
pressure on the same field — *a passage brightening toward one side*'s own six `flat`
strokes, read in the values view, and a six-pass `scumble` on its own `bristle` at
`0.20`, read in the painter's measure, both at 1024×768:

| pressure | six `flat` strokes, `opacity=0.5` | at `0.9` | the `scumble`, `opacity=0.5` | at `0.9` |
|---|---|---|---|---|
| 0.50 | 0.85 | 1.00 | 0.76 | 0.92 |
| 0.25 | 0.56 | 0.82 | 0.43 | 0.67 |
| 0.10 | 0.24 | 0.43 | 0.15 | 0.28 |

**So a pressure list's fade arrives late.** The same `scumble` at
`pressure=[1.0, 0.75, 0.25, 0.0]` over a `0.149` field — the test a painter took the
recipe's word to — reads `0.858`, `0.787` and `0.408` by thirds at `opacity=0.9`, and
still `0.188` over its last twentieth, where its list runs out at the frame; at `0.5`,
`0.800`, `0.644`, `0.291` and `0.170`. `probe_handover_session.py --pressure` takes both.

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

**Except that the comb in that table is `0.022`, under the small-comb floor**, where a
bristle is four streaks with gaps (*The bristle comb*): it closes the steps and weaves
the plane instead. *A mass built of planes* took that repair for faces of `0.014` to
`0.02` in step 6 of the 0.6.0 round and painted, from then until G3's demo showed it,
the *woven surface* its own *Goes wrong as* names — while `report()` said *59 marks
with a bristle under size=0.025* over it. So the notice offers the comb only at
`size=0.025` and over. Under that it offers `direction=` along a side, which closes the
sides that run with it, and `edge="clean"`, which halves the rest (`22%` to `11%`
above) — the pair that recipe lays now, whose faces rendered at 1024×768 read as
planes ([`NOTES-step9.md`](https://github.com/Gemberkoekje/EaselAPI/blob/v0.6.0/NOTES-step9.md) at `v0.6.0`, part three).

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

**A file saved by an earlier release opens as it was painted, and rebuilds as this one
lays.** The file holds the canvas, so loading never repaints it; an `undo` from the shell
or the server, `replay()` and a time-lapse made from the log lay every mark again with
the engine installed, so a fix to how a mark is laid reaches every mark of that kind in
every painting ever saved. The smudge fix of 0.6.0 is the size of it: a smudge that
started loaded with white laid a cap `0.13` of value over a mass at `0.45`, and a rebuild
lays it without one. So since 0.7.0 a file says which release saved it, and a file from
before the stamp is dated by what it carries — a `notices` key is 0.6.0, which wrote one
on every save, and none is 0.5.0 or earlier. Opened under a later release, a file whose
log holds marks a fix since then lays differently says so once, with how many for each
fix (`older-engine`); the next save stamps it with the release that saved it. The fixes
are the ones each release's entry in `CHANGELOG.md` names as changing what a rebuild
lays, which a test holds against the engine's own list. Rebuilt under the release that
saved it, a painting comes back as painted, byte for byte on the same machine.

**The time-lapse is not in the file, and comes back from the log.** A session loaded from
a file records no frames — every pass run from the shell or the server is such a
session, and a frame is the dearest thing a mark does that is not paint — and its film is
rebuilt when one is asked for, at the frame size the painting was made with. Rebuilt,
it is the film the painting recorded, frame for frame: the per-index seeding that makes
a replay the painting makes each frame of it the frame that was taken.

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

**Since G3 of the 0.6.0 round a `scumble` counts once in it**, and in the crossings that
re-arm it. `RECIPES.md`'s own graded field — in its own colours a smooth field — came
back *17 of 17 long marks … a stack of bars*, because every pass of a band laid by the
one verb that sizes its passes to overlap counted as a bar; whether those passes show as
bars is `scumble-bars`' question, at the call. Replayed over the corpus, the condition
holds on 47 passes rather than 62, and the line painters are shown, decay and all, falls
from **47 passes to 38 — 14% to 12%**. Every line that went was a pass laid mostly with a
scumble: skies, fog, water, a field. One of them was the round's only true positive —
BigPickle's, over the whole painting, which reached its share only by counting the sky
passes its own painter called fine; without them its block-ins and crossers fall under
it. That was ruled a price worth paying ([`PLAN-0.6.0.md`](https://github.com/Gemberkoekje/EaselAPI/blob/v0.6.0/PLAN-0.6.0.md) at
`v0.6.0`, the decisions table).

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

## What the check reads after a pass

Three of `report()`'s findings came out of the 0.5.0 cohort's round, and none of them is
the rule its step-2 prototype was (*What each proposed check would cost*, below). Each
prototype was looked at pass by pass, and each had fired on the wrong passes. All three
are habits rather than facts — a subject can radiate, a row can be a row, a pass can bury
on purpose — so each line says what it measured and leaves the call to the painter. Over
the corpus's 325 painted passes they fire on **one, one and two**. None fires on the
guide's 71 runnable blocks, and the third cannot: each block paints one pass on a fresh
canvas, so no block has an earlier detail to bury.

### A daisy

Finding 6 of the cohort: *strokes radiating from one point — a wagon wheel*. The
prototype gathered marks that start within `0.06` of one another and fan over `40`
degrees. Re-run for this step it fired on **22** passes (23 in the step-2 table), and
looked at one by one, one of them was a daisy. The rest were pine branches, pot rims, a
greenhouse's perspective bars, fingers, and a fan of sun rays, which radiate for real.
What a daisy is, is marks that leave **one point** in **every direction**:

- **the point** is where two consecutive marks' lines meet, because a daisy or a sunburst
  is one loop over angles. A mark near them counts if its line runs through the point
  (within a sixth of its length), it points away from it, and it starts within its own
  length of it — so a ray from a disc's rim counts as well as a petal from its centre;
- **every direction** is no gap in the circle of their directions wider than **`90`
  degrees**, with at least **five** marks at least `0.02` long;
- **a mark is a line**: at least **twice as long as its brush is wide**. Films as wide as
  they are long, crossing at a point, are a glow.

A tree's fork leaves gaps of `120` degrees (branches up, trunk down), a tuft of grass and
a fan of rays one of nearly `300`; a daisy of eight petals leaves `45` and a sun given
twelve rays by a loop `30`. **It fires on one pass of the corpus**, the fogged glass's
tree: nine branches leaving the fork with no gap over `88` degrees, which the painter's
own verdict calls *a grey mass with spoke-like branches*. Before the third clause the
closest miss was the heron's lamp at `94` — five films of its glow, each about as wide as
it is long, its pole and the two strokes of its fixture. One film more would have been
called a daisy, and that is what the clause is for. With it, the next nearest is six marks of the
winter greenhouse at `118`, so `90` sits between `88` and `118`.

### A loop's signature

Finding 7: a reflection laid as a column of same-length marks — *floating rectangles,
small bricks, a ziggurat, spoon-shaped islands* — four of the seven cohort painters'
first take. The prototype grouped marks by brush and colour, which a loop that steps its
colour gets past, and it fired on two passes: DeepSeek's reflection, and the pier's six
sparkles. Those were placed by hand, and their lengths ramp only in the order they were
typed. The rule:

- **six or more consecutive** hand-laid marks of one brush — a loop lays its marks one
  call after another;
- **one length** (the spread of their lengths under `15%` of their mean) **or a strict
  ramp** of lengths along their line, which is the ziggurat;
- **one spacing**: the gaps between them along their own line spread under **`35%`** of
  their mean. Of the corpus's runs at one length or a ramp, the one loop measures `0.24`
  and the next run `0.45`; a row placed by hand measures well over half;
- **far enough apart to read as marks**: the gap at least a mark's own width. Nine passes
  of one film `0.018` apart with a brush `0.11` wide are a graded pool, not a row, and the
  corpus holds exactly that.

**It fires on one pass of the corpus**, and it is the painter's own fix. DeepSeek's first
glitter path read as floating rectangles; the second is eight horizontal flashes its
comment calls *shorter and fainter as they come toward the viewer*. They are fainter and
thinner, and every one is `0.100` long, their gaps varying `24%` — in the finished
picture, a ladder of bars under the sun. The other three painters' committed passages
do not trip it, so *the committed scripts hold it twice*, under *What each proposed check
would cost* below, is once.

### A detail buried by a film or a mass

Finding 9, and the depth-order paragraph `LESSONS.md` lists as failed three runs running:
*a late pass buries what stands in front of it*. The prototype counted earlier small
marks whose pixels the pass changed, and fired on **54** passes. Most of them were a
nearer thing painted over a farther thing's details, which is back-to-front done right.
The rule counts a **detail** — a mark under `0.02`, or noted `subject` — when:

- it was **showing** as the pass opened: `0.05` or more off what is round it, in value;
- the pass left it at **under half** that contrast;
- and what went over it was **a film or the passes of a mass** (`block_in`, `sweep`,
  `scumble`, `cover`), not another thing painted in front of it by hand;

and the pass is told when **three or more** went. It needs the canvas as the pass
opened, which the log cannot give back without a replay: `easel run` and the MCP `run`
tool keep it as the pass begins, and a painter calling `report(since=)` after each pass
in one script is given it by the report before.

**It fires on two passes of the corpus, and both are burials**: the pier's second water
pass, whose graded scumble took the broken reflections under three piles, and the
pool's `p14_lift`, whose films lifting the water took the far lamp out of it and two
ripples beside it.

**The one burial a painter wrote down, it does not see.** The pool's own notes say three
deck glazes *ran straight over the chair and erased it*, found by cropping in. Measured,
the chair was never showing by this rule's measure: laid a step darker than the deck on
purpose, its marks stood `0.017`-`0.046` off it in value. And the deck's passes took it
down a little at a time — its right leg `0.035` as laid, then `0.021`, `0.015` and
`0.009` — never by half in one pass. Seeing it would take a lower floor for *showing*
and a memory of each detail's contrast that outlives an `easel run` call; both are
open.

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
warnings; the rest are `report()` findings. **The `!` rows count sayings, not passes**:
a call-time warning is said at every call that trips it, and this column added one for
each, so those rows are ceilings on the passes they name. The `report()` rows are
right, because a finding prints once a pass. *As 0.6.0 stands*, below, counts each rule
once a pass. Two `!` labels are corrected from the table as first printed, which matched
the warnings by a phrase: the scumble row counted two warnings that both opened *scumble
on this shape*, and the band row was the brush too *narrow* for its steps.

| The rule | passes | share |
|---|---|---|
| bars: a stack of passes at one angle | 47 | **14%** |
| ! pressure changes the paint, not the width | 18 | 6% |
| round tips printing one disc | 21 | 6% |
| a loaded comb under the bristle floor | 17 | 5% |
| ! a clean edge on a narrow mass | 16 | 5% |
| a graded passage laid too narrow | 8 | 2% |
| a pressure list on a chisel | 8 | 2% |
| ! scumble: a band whose width varies, or passes shorter than the brush | 5 | 2% |
| ! a smudge past the size that buys anything | 4 | 1% |
| ! scumble: a brush under two of the band's steps | 3 | 1% |
| ! a tip too small to deposit paint | 3 | 1% |
| ! a round tip blocking in a feature | 2 | 1% |
| detail before the masses are down | 2 | 1% |
| ! sample() averaging over a mixed area | 1 | 0% |

**229 of 325 painted passes (70%) say nothing at all. The median pass prints 0 lines and
the busiest prints 11.** So the engine is quiet today, and the bars rule is half of what
noise there is — it fires on one pass in seven even with its said-once decay, which is
the number behind *it taught two painters to skim*. Since a `scumble` counts once in it
(*The plan a painter declares*, above), the same replay gives **38, 12%**.

What this counts is what asks a painter for something: findings and call-time notices.
The standing lines under a pass are measurements and are not in it — the engine this
table measured prints `ground:` after every painted pass, and the median is still `0` —
so the four canvas lines printed after every pass since 0.6.0 cost this budget nothing,
by design. Whether a longer block gets skimmed is for a painter's run to show, not for
this table.

### The noise budget, as 0.6.0 stands

The same corpus replayed on the engine this round releases, each rule counted once a
pass: a finding prints once, and `easel run` prints a notice said at several calls of
one pass once, with a count. Lines marked `!` are said at the call, under the code shown.

| The rule | passes | share |
|---|---|---|
| bars: a stack of passes at one angle | 38 | **12%** |
| round tips printing one disc | 21 | 6% |
| ! `glaze-far`: a film past what a film is for | 17 | 5% |
| a loaded comb under the bristle floor | 17 | 5% |
| ! `solid-comb`: `solid=` does not close a comb | 16 | 5% |
| ! `spill`: paint outside the place it was handed | 13 | 4% |
| ! `clean-small`: a clean edge on a narrow mass | 11 | 3% |
| ! `smudge-long`: a smudge run along a long boundary | 11 | 3% |
| ! `smudge-across`: a smudge dragged across a boundary | 9 | 3% |
| a graded passage laid too narrow | 9 | 3% |
| a pressure list on a chisel | 8 | 2% |
| ! `chisel-pressure`: pressure changes the paint, not the width | 8 | 2% |
| ! `chisel-staircase`: pass ends down a side | 5 | 2% |
| ! `scumble-wedge`: a band whose width varies | 4 | 1% |
| ! `chisel-blank`: a tip too small to deposit paint | 3 | 1% |
| ! `smudge-wide`: a smudge past the size that buys anything | 2 | 1% |
| ! `scumble-bars`: a brush under two of the band's steps | 2 | 1% |
| details a film or a mass took out of sight | 2 | 1% |
| ! `holes`: a solid mass came back bare | 2 | 1% |
| ! `round-fringe`: a round tip blocking in a feature | 2 | 1% |
| detail before the masses are down | 2 | 1% |
| ! `sample-split`: `sample()` averaging over a mixed area | 1 | 0% |
| a daisy: marks leaving one point every way | 1 | 0% |
| a loop's signature: one length, one spacing | 1 | 0% |

**197 of 325 painted passes (61%) say nothing at all; the median pass prints 0 lines and
the busiest 8.** Against 0.5.0's 70% and 11, the round added seven notices and three
findings, and the quiet share fell by nine points while the median held at `0` — inside
the target of fewer than three findings and call-time notices on a median pass. The bars
line is still the loudest, at one pass in eight rather than one in seven, and every new
rule is at about one pass in twenty or under, `glaze-far` the most at 17. Where the two
tables share a `!` row, read them with care: the old column counted sayings.

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
| share of edges under 2.5 px wide, replayed on 0.6.0 | 21%-62%, median 37% | 21%-62%, median 37% | 23%-59%, median 38% |

The first four rows are the replay on 0.5.0, in step 2, and the last is the `edges:`
line that shipped, replayed on 0.6.0 (*The `edges:` row, measured twice*, below). On
0.6.0 the bare-ground rows move too — 14 of 21 under the floor, median `0.17%`; the
seven `0.07%`, the fourteen `0.29%` — because the round's default moves lay solid the
banded scumbles and fill the hard edges that the older scripts left those arguments off.
That is the replay's and not the paintings': the pictures their painters looked at are
the 0.5.0 rows.

**Finding 15 is the cohort's, and it is sharp.** Five of the six budgeted cohort
paintings stopped under 45% of their budget, at a median of 42% spent; **none of the
thirteen budgeted paintings before them did**, at a median of 86%. Whatever that is, it
is not a property of the engine.

**Finding 11 is not the cohort's.** Half the corpus finishes under the bare-ground floor
the checklist asks for, and half of the fourteen paintings made before the cohort do
too — the seven are further down the same slope, not off it. The contradiction between
the graded-field recipe and the ground line is older than this round.

#### The `edges:` row, measured twice

The table first printed this row as *share of edges under 2 px wide*, `12%-44%, median
27%`, from a prototype that did not work. Building workstream E turned this one over, which is the fourth mechanism this round
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

So **the 12%–44%, median 27% was float dust either side of `2.0`, not a measurement**,
and finding 13 had no number behind it until the corpus was replayed with the
instrument that shipped.

What shipped selects edges two ways instead, neither of them a percentile: a
**ridge** — the gradient at least as large as the gradient a pixel either side along
its own direction, which throws out both the tooth, whose gradients are not ridges,
and the broad interior slope of a graded mass, which has no crest — and a **step of
at least `0.10`** across it, because two masses closer than that read as one and a
transition smaller than that is not a boundary. The threshold moved to **`2.5` px**,
clear of the limit. The same four canvases then sit at 49%, 49%, 53% and **0%**, the
one at zero being the round soft brush, which is the only one of the four a painter
would call soft; and a canvas blurred numerically moves from 2.0 px median to 6.8.

**Replayed with it**, all 21 paintings on the 0.6.0 engine, the share of edges under
`2.5` px runs **21%–62%, median 37%**: the seven `21%`–`62%`, median `37%`, and the
fourteen before them `23%`–`59%`, median `38%`. Unlike findings 11 and 15 this one does
not split the cohort from the rest — the line separates pictures, not painters. **And it
separates the two finding 13 is about.** The two painters who named *flat cut-out
shapes* as their picture's main fault laid the hardest edges in the corpus but one:
Grok's harbour at `62%` (median `2.1` px) and GPT's village at `54%` (`2.4` px), with
only the winter greenhouse between them, at `59%`. The softest are Gemini's mist at
`21%` (`4.9` px) and the pool at `23%`. So a picture whose every boundary is crisp does
say so, as a number and not a verdict. `scripts/probe_cohort_session.py` reads it with
the engine's own `easel.checklist.edges_line`.

Nothing else in workstream E is affected — `values:`,
`pencil:`, `holes:`, `boxes:` and `unspent:` all reproduce their prototypes, and
`holes:` reproduces B2's three grounds to the third decimal (`0.1543%` / `0.1350%` /
`3.1601%` against `0.1552%` / `0.1357%` / `3.1550%`, off a different seed).

### The closing audit, over a whole painting

`checklist()` is `report(since=None)`: every rule of the post-pass check, read over the
whole painting rather than a pass. Two of those rules were written for a pass, and over
all 726 of Gemini's marks they added the painting up — *265 marks with a bristle under
size=0.025*, *one disc printed 176 times* — which is finding 12.
`scripts/probe_cohort_session.py --closing` reads both rules over every finished
painting the way the audit used to, beside what `checklist()` says now, and counts how
much of each old line had already been said by the pass that laid the marks:

| | the small comb | the discs |
|---|---|---|
| read as a pass over every mark — the closing audit until 0.6.0 | on 9 of 21 checklists | on 14 of 21 |
| the closing audit now | on none | on **10 of 21** |

**The comb's large counts had been said already, and its small ones are mostly
strands.** `opus`'s 40 and `laundromat`'s 48 came out of passes whose own report had
said so for 38 and 39 of the marks. Where no pass had, the count was three marks over
two passes — `car_wash`'s and each heron's — and cropped out of the finished canvases
they are mostly what a comb is for: a car-wash brush's bristles, streaks of light and
reflections on water, with one small plane on a heron's neck among them. Gemini's 265
are pine boughs, and the streaks are the needles it wanted. The rule asks for a brush
for the marks about to be laid, and a finished painting has none, so over a whole
painting it says nothing.

**The discs split the same way, and theirs is the checklist's own question** — *is any
small mark a disc, a capsule or a rectangle*. Where the count is large it is a passage
of repeated marks, which is the fault: Gemini's rows of identical glitter lozenges,
176 of them, every one in a section whose own report would have said so; `sonnet`'s
pots and trailing plants; the greenhouse's pots. Where it is small it added up accents
from different passes: `dusk`'s *one disc printed 8 times* was a lamp, a moon, two
notches, two edge highlights and a glint, from six passes, and six checklists were
counting a signature. So over a whole painting a disc counts only in a group of three
or more, each within a radius of another in the brush's unit, a signature left out,
and the line says where each group is:

| radius | `0.04` | **`0.06`** | `0.08` | `0.10` | `0.15` |
|---|---|---|---|---|---|
| checklists with a disc line | 8 | **10** | 10 | 11 | 11 |

The four that `0.06` drops — `car_wash`, `dusk`, `laundromat`, `glm` — are discs
standing apart, and from `0.06` to `0.15` only `car_wash`'s three join up, at `0.10`.
Under `0.06` the groups that are passages start going: `opus`'s and `pier`'s at `0.04`.

A pass's own report is unchanged for both rules, so *The noise budget, as 0.5.0 stands*
above — the comb on 17 passes, the discs on 21 — does not move.

### The default moves

Each move, with what it buys measured on a scratch canvas and what it would cost measured
over the corpus.

| Move | What it buys | What the corpus leans on |
|---|---|---|
| `cover()` to `edge="hard"` | `ragged` paints **2.32x** the area it is handed, `clean` 1.06x, `hard` 1.01x | **No committed pass script calls `cover()` at all** — the move is free, and so is the evidence for it. **Moved in 0.6.0**, once a bench of three passages gave it some: *A burial and the place it was handed* |
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
| **A smudge drags a thumbprint** (finding 3) | **Survived, and half of it was the engine's.** A hard step from `0.20` to `0.78`, one smudge at `size=0.04`: run **along** the join it lifts 11,024 px and stops **0.5 brushes** into the dark; run **across** it, starting in the dark, it lifted 1,561 px and carried them **4.1 brushes** in — which was the light cap every smudge laid from its first dab, fixed in 0.6.0, after which the same pass lifts 527 px and stops 0.5 brushes in. What is left of the thumbprint is the first mass dragged about a brush into the second, either way round (*Across a boundary, and along a long one*, under `smudge`). |
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

---

## The lighthouse handover's round

One painter, `claude-opus-5-5`, installed `easel-paint` 0.6.0 from the package, painted a
lighthouse at dusk in 171 of 300 strokes, and checked its claims before making them.
Acting on its verdict is one round, and its measuring step is
[`scripts/probe_handover_session.py`](scripts/probe_handover_session.py): it rebuilds
the painting from its thirteen committed passes through the CLI's own `run_script`,
keeps a rehearsal copy of the canvas after each pass, and benches every candidate of
the round on the canvas the painter actually had -- each candidate patched in for one
bench and never into the engine. The corpus half of the graded rule is
`scripts/probe_cohort_session.py --graded`. Everything in this section is those two
scripts' output; re-run them rather than trusting the numbers here. The probe takes
about fifteen minutes, `--claims`, `--edges`, `--flecks`, `--misfires`, `--sheet`,
`--file` and `--pressure` cut it down, and `--graded` is about twenty-five on its own.

**What the numbers cannot decide, the probe renders**, into `out/handover/`: the edge
candidates in the painting at its own size, and the flecks each dry-brush gate leaves.
Two of the round's questions are *does it read as paint*, which is the eye's.

### The painting, rebuilt

192 records, **171 strokes spent**, in about 40 seconds -- the painter's own count, and
every mark's geometry the painter's. What the check printed after each pass, as the
painter's shell printed it:

| pass | `edges:` under 2.5 px | median rise |
|---|---|---|
| `p01_sky.py` | 19% | 5.0 px |
| `p02_sea.py` | 60% | 2.1 px |
| `p03_headland.py` | 64% | 2.0 px |
| `p04_tower.py` | 65% | 2.0 px |
| `p05_light.py` | 63% | 2.0 px |
| `p06_water.py` | 59% | 2.1 px |
| `p07_subject.py` to `p09_edges.py` | 57% | 2.2 px |
| `p10_surround.py` | 56% | 2.2 px |
| `p11_final.py`, `p12_sign.py` | 54% | 2.2 px |

Over half the painting's edges under 2.5 px on every pass from the sea's, which is the
range of the two cohort paintings whose painters named *flat cut-out shapes* (Grok's
`62%`, GPT's `54%`).

### The claims, re-measured

| Claim | What the probe found |
|---|---|
| **Hard edges are all-or-nothing** (1) | **Survived, to the hundredth.** In the painter's own measure -- Rec. 709 weights on the export's bytes -- the tower's left side at `y=0.40` goes `0.59` to `0.28` in one pixel (a step of **`0.30`**), its right side `0.31` to `0.59` (**`0.28`**), the waterline at `y=0.70` **`0.19`**, and the headland against the sky at `x=0.60` **`0.48`**. The clip mask (`Polygon.coverage`, two samples a pixel) leaves at most one fractional pixel a side on any of the tower's rows, and the rest of the boundary is a step. |
| **The side-by-side sheet cannot take a glaze** (5) | **Did not survive.** `{"points": ..., "glaze": True, ...}` is a stroke entry of a plan; a `vary=` sheet of three opacities of a glaze renders in under two seconds (*A variant's cost*, below). |
| **About 15 s a variant** (4) | **Survived, and it is the paint**: see *A variant's cost*, below. |
| **16 MB a session** (7) | **Survived**: see *The session file*, below. |
| **A vertical seam from the sky blends** (8, withdrawn) | **Not reproduced**, wet or dried: the three sky ramps on a fresh canvas give a median column jump of `0.0002`, largest at the canvas's own edges. See *The fade and the wet bands*. |
| **A pressure list fades less than the recipe says** (10) | **Both are right**: see *The fade and the wet bands*. |
| **The lit-air sentence is backwards** (11) | **Survived.** A `round_soft` glaze at pressure `[1.0, 0.55, 0.1]`, `size=0.10`, is **80 px** tall near its source, 64 in the middle and **30** at the far end: full pressure is the wide end of a round tip. |

### An edge that is not a step

**Which calls a default would move.** The painter counted 33 calls that clip or lay hard,
and sorted them: 9 draw an edge and 24 only keep paint inside a shape. The probe reads the
same 33 off the calls as they are made -- the log carries a clip's outline but not the
`edge=` its call was given -- and the same 9 by the painter's own list:

| the 9 that draw an edge | how | under the decided default |
|---|---|---|
| the horizon (`scumble` of the sea) | `edge="hard"` | feathers -- and the painter wanted it ruled |
| the headland, two sea stacks, the cap | `edge="hard"` | feather |
| the tower, its lit side, the lantern twice | `clip=` | **stay hard** |

**The decided default -- `edge="hard"` feathers, `clip=` keeps `0` -- moves 5 of the 9,
and not the four the verdict named.** The tower and the lantern are clipped strokes;
under it they are exactly what they are today (the probe's *default only* rows below).

**The curve, inward.** The tower's two clipped strokes on a canvas set to the sky's
value (`0.59`), so the tower's are the only edges there are. *Step* is the largest
one-pixel move either side of the tower, median over its rows.

| canvas | candidate | feather | px | step | `edges:` under 2.5 px | median rise |
|---|---|---|---|---|---|---|
| 1024x768 | today | 0 | 0 | 0.298 | 77% | 2.0 px |
| | A1 | 0.001 | 1.0 | 0.294 | 76% | 2.0 px |
| | A1 | 0.002 | 2.0 | 0.247 | 69% | 2.0 px |
| | A1 | 0.003 | 3.1 | 0.210 | 66% | 2.2 px |
| | A1 | 0.005 | 5.1 | 0.167 | 42% | 2.6 px |
| | A2 | 0.002 | 2.0 | 0.306 | 81% | 2.0 px |
| | A2 | 0.003 | 3.1 | 0.298 | 80% | 2.0 px |
| | A2 | 0.005 | 5.1 | 0.280 | 78% | 2.0 px |
| 1440x960 | today | 0 | 0 | 0.294 | 70% | 2.0 px |
| | A1 | 0.002 | 2.9 | 0.222 | 64% | 2.1 px |
| | A1 | 0.003 | 4.3 | 0.188 | 56% | 2.4 px |
| | A1 | 0.005 | 7.2 | 0.133 | 13% | 2.9 px |
| | A2 | 0.002 | 2.9 | 0.298 | 75% | 2.0 px |
| | A2 | 0.003 | 4.3 | 0.294 | 72% | 2.0 px |

**The knee is not where the plan's table put it.** That table was a *centred* Gaussian,
which spreads a 2 px feather over about eight pixels and reaches outward; an inward ramp
over `F` pixels rises over about `F/1.5`, so the `edges:` line reads it as hard until the
ramp is past 3.75 px. **A2 is invisible to both numbers by construction** -- it keeps
every pixel crisp and breaks the boundary where the tooth is low -- so neither the step
nor the line can tell it from today. The two strokes cost 0.2 s today and about a second
feathered, most of it the distance to the outline, which the build would memoise as the
engine's own mask is.

**In the painting**, each candidate laid by the committed pass on the canvas the painter
had: the tower's step goes `0.294` to `0.227` under A1 at `0.002` and stays at `0.294`
under A2 -- and under the decided default, with only `edge="hard"` feathered, it stays
at `0.294` for every candidate. The sheets:

| sheet | what it shows |
|---|---|
| `edges_tower_1024x768.png`, `..._x3.png` | the tower as `p04_tower.py` laid it: today, A1 `0.002`, A2 `0.002` and `0.003` with every edge feathered, and the three again under the decided default |
| `edges_tower_1440x960.png`, `..._x3.png` | the same on the painting rebuilt at 1440x960 |
| `edges_headland.png` | `p03_headland.py`'s mass, its own outline feathered, on the prelude's roughened outline and on the plain one |
| `edges_containment.png`, `..._x4.png` | the planes held inside the headland, their `clip=` feathered: the rim the plan's risk table names |
| `edges_ground.png` | a hard mass on bare ground |
| `edges_burial.png` | `cover()` over a worked passage |

The painting's own `edges:` line hardly moves under any of them, because the tower is a
small part of it: `65%` today, `62%` with A1 `0.002` on every edge, `65%` with A2. **The
headland**, laid by `p03_headland.py` with only its own outline feathered, keeps a step of
`0.425` across its top today, `0.398` under A1 and `0.416` under A2 -- and the outline
it is laid in moves it further than any feather does: the prelude's roughened silhouette
and the plain one the painter drew first differ at a glance on `edges_headland.png`,
where no feather at `0.002` does. **The containment clip**, the planes held inside the
headland with their `clip=` feathered, leaves the `edges:` line at `64%` for every
candidate and shows no rim of the mass beneath at four times on `edges_containment_x4.png`.

**Read blind by the painter.** The four were put to the painter under letters, in an
order it did not know ([`answers-step2.md`](paintings/Claude/lighthouse_handover/answers-step2.md),
10a). It ranked A2 at `0.002` first; A2 at `0.003` second, ragged on anything made and
paint-like only on the plain rock outline; A1 third; today last, A1 and today nearly a
tie at 1:1. And it measured the steep side of the mass on bare ground itself, in canvas
pixels -- re-run here on the same sheet, to the hundredth
([`verify/measure_ground_edges.py`](paintings/Claude/lighthouse_handover/verify/measure_ground_edges.py)):

| | wander about a straight line (sd, px) | largest bite (px) | in-between pixels across the edge (median) |
|---|---|---|---|
| today | 0.24 | 0.44 | 0.5 |
| A1 `0.002` | 0.14 | 0.29 | 1.0 |
| A2 `0.002` | 0.38 | 0.91 | 0.5 |
| A2 `0.003` | 0.50 | 1.27 | 0.5 |

A2 is as sharp as today and broken; A1 is the only soft one, and the straightest; today's
wander is its stair-steps. At 1440x960 the painter found A2 at `0.002` *a little chewed*.
The tooth A2 breaks against is two fields: a linen thread is 1/130 of the long side
(7.9 px at 1024, 11.1 at 1440), and the grain mixed into the gate is about 3 px at any
size. A feather set as a share of the long side -- 2.9 px at 1440 -- grows against the
grain while the weave keeps pace, which is a bench for the build: the feather's unit.

**What the feather leaves showing.** A mass laid hard on bare ground takes paint on
every pixel of its own area today; feathered, **117** of them at A1 `0.002` and
**662** and **981** at A2 `0.002` and `0.003` are left within `10/255` of the ground --
the broken boundary, which on bare ground *is* the ground. The `ground:` line moves
from `92.28%` to `92.44%`, which says nothing either way on a canvas that is mostly
ground. A burial -- 0.6.0's F1 bench, `cover()` over a worked passage -- keeps its
contrast whatever the feather: *seen* goes `0.51x` to `0.47x` the place, and the
outline, sampled two pixels either side, stays `0.0417` against the passage's own
`0.0097`, because a feather inward changes how the rectangle is crossed and not what it
is. How the rectangle is crossed does move: its largest one-pixel step goes `0.047` today, `0.031` under A1 `0.002`, `0.043` and `0.039` under A2 `0.002` and `0.003`.

#### Built, in step 5

**What shipped is A2 at `0.002` on every hold** -- *A held edge, broken (0.7.0: the
default moved)*, in the `block_in` chapter, has the rule's numbers -- and the probe's A2
has been the engine's own since, so re-running the tables above prints the build's; they
stand here as what the painter was shown. The build differs from the bench's copy in
three places, each on purpose: nothing lands on or past the drawn line, where the copy
let the weave's highest peaks through; a side on the canvas frame is not an edge; and a
shape narrower than four feathers breaks over a quarter of its width. **The unit is a
share of the long side**: built, the edge at 1440 bites at the export's own pixels as
1024's does (`0.94` against `0.94`), where the copy the painter found *a little chewed*
measured `1.32`, wandering `0.49` against the build's `0.44`.

**The painting as 0.7.0 lays its own scripts.** None of the thirteen passes a feather, so
all 33 holds break, the horizon too. Rebuilt both ways, the `edges:` line moves by two
points at most after any pass (`64%` to `62%` after the headland) and ends at `54%`
either way; the tower's step reads `0.288` against `0.290`, and `ground:` `0.00%` both;
`edges_built.png` shows the tower and the headland. **It costs nothing a painting can
measure**: the thirteen scripts rebuild in 41.7 and 41.9 s broken against 42.2 and 41.2 s
cut, each in a fresh process on a quiet machine. **At the horizon** the sea's top row
takes the sky's colour with the weave's highest peaks of sea left in it: the line sits a
pixel lower and frays by a pixel. That is the broken edge on a line ruled on purpose,
and the painter's answer for it was `feather=0` (`answers-step2.md`, 11).

**The corpus.** Every painting whose committed scripts hold an edge -- `edge="hard"`,
`clip=` or `cover()` -- rebuilt from its scripts twice, cut as its painter had it and as
this engine lays the same scripts (`probe_handover_session.py --corpus-edges`). *Moved*
is the share of the canvas more than two 8-bit levels apart; *ground* is
`Canvas.ground_showing`'s own; *new bare* is ground the broken edges uncover that the cut
ones covered, and the longest run of it is the question the seam asks:

| painting | moved | ground, cut | ground, broken | new bare px | its longest run |
|---|---|---|---|---|---|
| lighthouse handover | 0.46% | 0.00% | 0.00% | 0 | -- |
| fogged glass | 0.00% | 0.16% | 0.16% | 0 | -- |
| hands | 0.05% | 24.69% | 24.69% | 73 | 12 px |
| pier | 0.34% | 0.40% | 0.39% | 80 | 11 px |
| BigPickle | 0.30% | 31.94% | 31.94% | 0 | -- |
| DeepSeek | 0.34% | 0.00% | 0.00% | 0 | -- |
| GLM | 0.15% | 12.78% | 12.71% | 5 | 1 px |
| GPT | 1.92% | 0.07% | 0.06% | 136 | 5 px |
| Grok | 0.53% | 0.00% | 0.00% | 0 | -- |
| Kimi | 0.36% | 0.00% | 0.00% | 0 | -- |

**No seam.** No painting's `ground:` rises, and the ground the feather uncovers is specks
of a few pixels where a hard mass's broken rim met bare ground -- none of it a line. The
fogged glass's scripts name `cover()` only in a comment, and nothing in it moves. GPT's
painting moves the most, because its own helper lays every mass hard -- each house, roof
and the quay -- besides its thirteen clips, and **it moves at its edges**: of the 19,748
pixels more than eight levels apart, all but 19 lie within 3 px of a hold's outline, none
of them further than 10 px, and a map of the change is a line drawing of the village.
Past 3 px nothing moves more than 12 levels -- the brush picking up what shows through a
broken rim.

### A dry brush that streaks

**The gate as it stands, and three candidates, on the marks the painter starved.**
*B1* reads the tooth along the travel: a nine-pixel line kernel in the dab's own
direction, rescaled to the tooth's own mean and spread so a load lets through about the
same share. *B2* gives each bristle of the comb its own load -- the stroke's, raised to
a power drawn per bristle between a third and three, so a full brush is full in every
bristle and an empty one in none -- and a bristle under `0.10` lays nothing. *B3* thins
what a starved brush lays by its load. A piece is eight-connected pixels moved one 8-bit
level or more; *specks* is the share of the paint in pieces under four pixels; *long*
is a piece's extent along the travel over its extent across, median over pieces, and
*paint* the same for the piece the median pixel of paint sits in.

**The sky's crosser** (`bristle`, `size=0.065`, `opacity=0.40`, `pressure="swell"`,
its load running down along the stroke as every stroke's does) on a canvas set to the
sky's value, `0.56`:

| gate | load | landed | pieces | median | under 4 px | specks | long | paint |
|---|---|---|---|---|---|---|---|---|
| today | 0.30 | 1,954 | 475 | 3 | 62% | 26% | 1.0 | 1.0 |
| | 0.45 | 6,060 | 571 | 4 | 49% | 8% | 1.0 | 1.0 |
| | 0.60 | 16,363 | 531 | 5 | 42% | 2% | 1.0 | 3.4 |
| | 0.80 | 34,504 | 426 | 7 | 31% | 1% | 1.0 | 6.2 |
| B1 | 0.30 | 2,534 | 205 | 7 | 31% | 5% | 2.5 | 2.8 |
| | 0.45 | 6,710 | 218 | 9 | 28% | 2% | 2.5 | 2.8 |
| | 0.60 | 17,104 | 226 | 11 | 25% | 1% | 2.6 | 4.3 |
| | 0.80 | 33,816 | 205 | 15 | 17% | 0% | 2.6 | 7.0 |
| B2 | 0.30 | 7,256 | 548 | 4 | 46% | 6% | 1.3 | 1.8 |
| | 0.45 | 14,405 | 542 | 5 | 41% | 3% | 1.3 | 3.2 |
| | 0.60 | 22,589 | 445 | 5 | 39% | 1% | 1.3 | 15.1 |
| | 0.80 | 34,222 | 269 | 6 | 38% | 1% | 1.3 | 13.0 |
| B1+B2 | 0.30 | 7,510 | 239 | 8 | 27% | 2% | 2.8 | 4.4 |
| | 0.45 | 14,641 | 230 | 13 | 21% | 1% | 2.9 | 8.0 |
| | 0.60 | 22,736 | 203 | 13 | 21% | 0% | 2.8 | 20.1 |
| | 0.80 | 34,662 | 124 | 14 | 27% | 0% | 3.2 | 13.0 |
| B3 | 0.30 | 789 | 257 | 2 | 73% | 39% | 1.0 | 1.0 |
| | 0.45 | 4,430 | 432 | 4 | 48% | 8% | 1.0 | 1.1 |
| | 0.60 | 14,495 | 450 | 4 | 42% | 2% | 1.0 | 3.4 |
| | 0.80 | 32,625 | 414 | 8 | 30% | 1% | 1.0 | 6.3 |

At the loads the guide recommends for a broken mark, today's gate lays confetti: at
`0.45`, 571 pieces with a median of 4 px, as long across the travel as along it. B1 makes
the same paint into 218 pieces of 9, two and a half times as long as they are wide. B2
lays long streaks along the comb -- the *paint* column, 15 and 20 at `0.60` -- among its
flecks, which the median over pieces cannot see. B3 thins and changes nothing else.

**Exercise 3**, as `PAINTER.md` gives it -- one `bristle` stroke at `size=0.07` and four
loads, `load_falloff=0`, on rough canvas:

| gate | load | landed | pieces | median | long | paint |
|---|---|---|---|---|---|---|
| today | 0.60 | 35,052 | 15 | 176 | 1.4 | 7.5 |
| | 0.35 | 6,060 | 54 | 50 | 1.2 | 1.1 |
| | 0.20 | 2,725 | 51 | 23 | 1.0 | 1.2 |
| B1 | 0.60 | 42,939 | 9 | 8 | 4.2 | 10.7 |
| | 0.35 | 5,347 | 263 | 11 | 2.7 | 2.8 |
| | 0.20 | 2,616 | 181 | 8 | 3.0 | 3.2 |
| B2 | 0.60 | 35,075 | 30 | 72 | 2.4 | 10.0 |
| | 0.35 | 21,109 | 67 | 29 | 2.0 | 5.6 |
| | 0.20 | 7,367 | 61 | 28 | 1.4 | 1.5 |
| B1+B2 | 0.60 | 39,781 | 25 | 15 | 3.7 | 10.8 |
| | 0.35 | 23,069 | 147 | 14 | 3.0 | 19.8 |
| | 0.20 | 7,775 | 237 | 13 | 2.7 | 3.3 |
| B3 | 0.35 | 5,385 | 53 | 57 | 1.3 | 1.1 |

At full load every gate lays the same 51,119 pixels. **Two costs are in the *landed*
column.** B1 keeps the tooth's mean and spread but not its shape, so a load lays a
different amount under it -- 22% more at `0.60` on rough, 12% less at `0.35`; a build
would match the tooth's whole distribution. And **B2 as benched makes a starved brush
heavier**: at `0.35` it lays 3.5 times today's paint, because the bristles that keep
their load keep all of it. Its spread is a number the build tunes until a load lays
about what it lays today; the streaks, not the weight, are what the candidate is for.

**The painting's five starved flats** -- `p08_rock.py`'s ledges, `size` 0.009 to 0.016
at loads 0.7 and 0.8 -- barely starve: 6,346 pixels in 25 pieces today, the same under
B2 (a flat has no comb for it to hold the load in), 26 pieces three times as long under
B1. **The planes recipe's scrape** (`bristle`, `size=0.03`, `load=0.35`) lands 76
pixels, a trace, whatever the gate.

**What the sheets show** -- `flecks_crosser.png`, `flecks_exercise3.png`,
`flecks_water.png`, `flecks_ledges.png`, `flecks_planes.png`, `flecks_sampler.png` --
is the numbers' order made visible: today's starved bristle is a halftone of dots, B1's
is dashes running with the brush, B2's is thin continuous streaks along the comb with
body between them, and B1+B2 is the most like a dry brush dragged; on the painting's
first surf, today's blue specks become strokes of foam under B2. B3 is today's dots,
fainter.

**Read blind by the painter**, the five under letters
([`answers-step2.md`](paintings/Claude/lighthouse_handover/answers-step2.md), 12a): B2
first -- *streaks along the stroke, broken inside by the tooth, chunky and varied: a dry
brush dragged* -- B1+B2 a close second, *combed more than dragged*, then B1, B3 and
today, today plainly dirt. It could not tell the streaks from the extra paint by eye, and
asked to see them tuned to lay what today lays -- which is what was decided (the plan's
question 12): B1+B2, tuned, since B2 does nothing on a tip without a comb.

#### Built, in step 6

**What shipped is B1+B2, tuned** (`Canvas.drag`, `tooth_along`, `DryComb`), and it
differs from the bench's copies in four places, each on purpose. **It drags only as the
brush runs dry**: nothing at `0.9` of the load and over, all of it from `0.7` down, a
smoothstep between -- because on linen and rough the lowest tooth lies under the gate's
own band (`0.116` and `0.053` at 1024), so the gate reads the tooth even for a full
brush, and a gate read along the travel wherever it reads anything would have moved
every loaded mark on those surfaces. **The tooth read along is given back the tooth's own
values rank for rank**, where B1's copy kept only its mean and spread. **Each bristle's
share of the paint comes from its comb, stratified, and the comb is matched to the
stroke's share stroke by stroke**, each bristle weighed by how much of the tip it is.
And **a bristle running out fades as the fourth power** of how far it is under `0.05` of
the canvas, where the copy cut it off at `0.10` of its load. The distributions all of this
is matched to are read at pixels drawn at random: every fourth pixel each way -- the grid
`tooth_ceiling` reads -- lands on smooth's grain, a lattice four pixels apart, and reads
its tooth wider than the field is (a 90th percentile of `0.667` against `0.637`), which
let a first build lay twice its paint on smooth. `tooth_ceiling` reads that grid still,
as it always has, so smooth's ceiling is `0.692` where the field's own 95th percentile is
`0.667`. The probe's `--dry` benches
it beside 0.6.0's gate -- *today*, which is the engine with `Canvas.drag` held at `0`,
0.6.0's own lines -- and beside B2 alone as built, which the painter asked to see:

| gate | load | laid | pieces | median | under 4 px | specks | long | paint |
|---|---|---|---|---|---|---|---|---|
| today | 0.30 | 277 | 475 | 3 | 62% | 26% | 1.0 | 1.0 |
| | 0.45 | 1,321 | 571 | 4 | 49% | 8% | 1.0 | 1.0 |
| | 0.60 | 5,482 | 531 | 5 | 42% | 2% | 1.0 | 3.4 |
| | 0.80 | 16,363 | 426 | 7 | 31% | 1% | 1.0 | 6.2 |
| B2 alone, built | 0.30 | 247 | 230 | 3 | 51% | 12% | 1.1 | 1.1 |
| | 0.45 | 1,225 | 320 | 5 | 43% | 4% | 1.1 | 1.4 |
| | 0.60 | 5,389 | 341 | 6 | 37% | 1% | 1.1 | 3.4 |
| **built** | 0.30 | 246 | 101 | 7 | 26% | 3% | 2.3 | 2.4 |
| | 0.45 | 1,400 | 125 | 12 | 25% | 1% | 2.8 | 3.5 |
| | 0.60 | 5,750 | 156 | 13 | 24% | 0% | 2.9 | 3.8 |
| | 0.80 | 16,318 | 143 | 16 | 16% | 0% | 2.8 | 7.0 |

*Laid* is the stroke's own count of the paint it put down. **Tuned to lay today's paint,
B2 alone is dots again, in the comb's rows** -- the bench's B2 read as streaks at more than
three times the paint -- and B1+B2 is chunky dashes of every length running with the
brush: dragged, not combed, so B1's kernel was not shortened on a comb (the painter's
12b). A 5 px kernel, looked at beside it, sits between the two.

**What each load lays**, summed over 24 strokes at random places and directions, each
with its own comb (`bench_amounts`), against the same strokes under 0.6.0's gate, with
the tenth and ninetieth percentile stroke by stroke:

| mark | load | built / today | one stroke |
|---|---|---|---|
| `bristle` `0.065`, linen | 0.30 | `1.02` | `0.79`-`1.33` |
| | 0.45 | `1.00` | `0.90`-`1.06` |
| | 0.60 | `0.99` | `0.94`-`1.06` |
| | 0.80 | `1.00` | `0.97`-`1.02` |
| `bristle` `0.07`, rough, no falloff | 0.20 | `0.92` | `0.64`-`2.49` |
| | 0.35 | `0.95` | `0.82`-`1.25` |
| | 0.60 | `0.99` | `0.97`-`1.02` |
| `bristle` `0.05`, smooth | 0.30 | `1.06` | `0.42`-`2.76` |
| | 0.45 | `0.94` | `0.78`-`1.14` |
| | 0.60 | `0.98` | `0.93`-`1.02` |
| `flat` `0.03`, linen | 0.35 | `0.99` | `0.88`-`1.11` |
| | 0.50 | `1.00` | `0.93`-`1.08` |
| | 0.70 | `0.99` | `0.95`-`1.03` |
| `round_hard` `0.02`, linen | 0.30 | `1.01` | `0.93`-`1.09` |
| | 0.50 | `1.00` | `0.96`-`1.04` |
| | 0.70 | `1.00` | `0.97`-`1.02` |

**One stroke is a lottery where one or two bristles carry it**, as a dry brush is, and the
sums hold. Cut off hard, a bristle under `0.05` laid nothing, and the comb's total jumped
from nothing to one bristle's worth: a `bristle` at `0.30` on smooth, whose need sits at
the tooth's ceiling, laid **an eighth** of what it had, summed. The fade is what the
table above is built with.

**Exercise 3** on rough: at `0.6` the stroke lays `36,968` against `37,435`, in 25 pieces
with a median of 26 px, `2.5` times as long along the travel as across, where 0.6.0's
gate left 15 islands with a median of 176 px, `1.4` times; at `0.35`, `3,584` against
`3,221`, 41 pieces of a median 80 px, `2.0` times. **The painter's five ledges** (`flat`,
`0.7` and `0.8`): 26 pieces with a median of 11 px, `3.9` times as long as wide, where
they were 25 of 52 px at `1.3` -- the same paint as dashes. **The planes recipe's scrape**
lays a trace under either.

**What the sheets show** -- `dry_crosser.png`, `dry_exercise3.png`, `dry_water.png`,
`dry_ledges.png`, `dry_sampler.png` -- is the dots gone: the crosser's flecks become
dashes dragged with it, the painter's first surf strokes of foam along the rock, the
sampler's dry tails gaps that run with the stroke. Rough changes least, because rough's
tooth is coarse islands already -- at 1024x768, four pixels on, it correlates `0.83`
either way -- so the read along hardly moves it (`0.89` along, `0.85` across) and its
streaks come from the comb. Linen's, at the same size and distance, correlates `0.08`
either way raw and `0.73` along against `-0.04` across once it is read along.

**The corpus, rebuilt under each gate** (`--corpus-dry`): every committed painting from
its scripts, holds cut on the line both times -- a saved clip replays at the feather it was
laid with, and none was laid with one -- so what differs is the gate alone. This is what a
rebuild of each saved painting lays now. *Run dry* is the marks `stroke.drags()` counts,
which is what the rebuild notice counts; *moved* is the share of the canvas more than two
8-bit levels apart, and more than eight; *ground* is `Canvas.ground_showing`'s own, under
0.6.0's gate and this one:

| painting | marks | run dry | moved | past 8 levels | ground |
|---|---|---|---|---|---|
| car wash | 212 | 143 | 16.94% | 9.30% | 0.02% -> 0.00% |
| pears | 231 | 198 | 3.28% | 1.45% | 1.27% -> 1.27% |
| lighthouse at dusk | 185 | 50 | 0.60% | 0.24% | 0.01% -> 0.01% |
| laundromat | 288 | 142 | 5.82% | 1.64% | 0.48% -> 0.47% |
| greenhouse lighthouse, Sonnet | 275 | 59 | 0.26% | 0.10% | 13.70% -> 13.70% |
| greenhouse lighthouse, Opus | 297 | 142 | 19.79% | 7.00% | 0.17% -> 0.07% |
| greenhouse lighthouse, Fable | 285 | 87 | 0.38% | 0.08% | 0.01% -> 0.01% |
| pool | 244 | 118 | 7.52% | 1.91% | 0.03% -> 0.01% |
| heron, first | 295 | 143 | 2.55% | 0.56% | 0.11% -> 0.11% |
| heron, second | 255 | 147 | 2.91% | 0.97% | 1.31% -> 1.32% |
| winter greenhouse | 299 | 95 | 0.18% | 0.07% | 0.52% -> 0.52% |
| fogged glass | 314 | 193 | 6.19% | 1.27% | 0.16% -> 0.16% |
| pier | 259 | 222 | 7.14% | 2.44% | 0.40% -> 0.30% |
| hands | 327 | 133 | 2.77% | 0.86% | 24.69% -> 24.74% |
| **lighthouse handover** | 173 | **65** | 1.02% | 0.13% | 0.00% -> 0.00% |
| BigPickle | 50 | 26 | 7.08% | 3.93% | 31.94% -> 31.94% |
| DeepSeek | 69 | 19 | 0.60% | 0.22% | 0.00% -> 0.00% |
| Gemini | 726 | 517 | 2.21% | 0.86% | 0.38% -> 0.37% |
| GLM | 127 | 44 | 1.14% | 0.22% | 12.78% -> 12.80% |
| GPT | 411 | 170 | 0.64% | 0.29% | 0.07% -> 0.07% |
| Grok | 134 | 34 | 0.39% | 0.05% | 0.00% -> 0.00% |
| Kimi | 172 | 41 | 0.36% | 0.12% | 0.00% -> 0.00% |

**Half the corpus's marks run dry somewhere**: 2,788 of 5,628, because a brush spends its
load along every stroke and the `bristle` preset starts at `0.9`, so a preset bristle's
tail drags as surely as a mark laid starved. The plan counted *sixteen* of the handover's
own -- the marks laid starved on purpose -- and it is 65. What a rebuild moves is a median
of `2.4%` of a canvas, from `0.18%` to `19.8%`, most where a painting lays large passages
with the bristle at its own load -- the Opus greenhouse and the car wash. **What moves is
what was meant to**: `dry_corpus.png` crops the largest change in each painting, and in
every one it is a dry passage's dots become streaks along its strokes -- the car wash's
pale verticals, the pool's glints, BigPickle's sky, GPT's roofs. **`ground:` rises by
`0.05` of a point at most** (the hands), in three paintings, and falls in six.

**What it costs**: the painter's thirteen passes rebuild in `31.5` s under this gate
against `29.6` under 0.6.0's, best of three each in fresh processes on a quiet machine --
a sixteenth more. Part of it is the tooth read along: one field per ten degrees of travel
a starving brush meets, built once per canvas and shared with its rehearsals -- 16 for
this painting, `50` MB at 1024x768.

### The graded rule's two misfires

The rule as it stands, the plan's two clauses -- judge the run by its **median** brush;
**break** the run where two neighbours overlap along the stack's axis by less than 30% of
the shorter -- and both, on the four cases the clauses were drawn on, each rebuilt as its
own README says:

| case | wanted | the engine | as it stands | median | overlap 30% | both | trimmed | trimmed, 10% |
|---|---|---|---|---|---|---|---|---|
| the headland misfire (19 marks, sizes `0.006`-`0.07`, step `0.020`) | silent | fires | fires | -- | fires | -- | -- | -- |
| the water misfire (7 marks, `0.006`-`0.0095`, step `0.009`) | silent | fires | fires | fires | -- | -- | fires | -- |
| the recipe's passage (6 marks at `0.085`) | silent | -- | -- | -- | -- | -- | -- | -- |
| the recipe's failure block (6 marks at `0.02`) | fires | fires | fires | fires | fires | fires | fires | fires |

The engine and the probe's re-implementation agree on every case. *Trimmed* is not the
plan's: it judges by the narrowest brush that is at least half the run's median, which
drops a lone accent and keeps a taper. It is here because of what the corpus showed.

**Over the corpus** -- all 22 paintings replayed pass by pass, 337 passes that laid paint,
each firing pass cropped as it left the canvas with the marks the rule counted drawn
over it (`out/graded/`, from `probe_cohort_session.py --graded`). How each crop reads is
**a reading, not a measurement**, and two readers are given: the bench's, and the
painter's, made blind -- the crops shuffled and numbered, the gates' verdicts unseen
([`answers-step2.md`](paintings/Claude/lighthouse_handover/answers-step2.md), 13a). T is a
graded passage coming back as bars, F is not, ? can't tell.

| pass | run | the bench read | the painter, blind | as it stands | median | overlap 30% | both | trimmed | trimmed, 10% |
|---|---|---|---|---|---|---|---|---|---|
| `car_wash/p13_form.py` | 9 marks, `0.024`-`0.046`, step `0.038` | T, a graded curtain in visible bars | ?, bars, or hanging strips | fires | fires | fires | fires | fires | fires |
| `sonnet/p3_beam.py` | 11, `0.0405`-`0.0874`, step `0.027` | T, a beam banded across its width | T | fires | -- | fires | -- | fires | fires |
| `opus/p3_beam.py` | 6, `0.01`-`0.048`, step `0.007` | T, a beam laid as rays | T | fires | -- | fires | -- | -- | -- |
| `fable/p8_base.py` | 6, `0.005`-`0.014`, step `0.012` | F, pot rims, an arch's band, a base line | F | fires | fires | -- | -- | fires | -- |
| `heron2/pass11_last.py` | 7, `0.0045`-`0.036`, step `0.007` | ?, lines across one plank | F, ruled lines on a slab | fires | fires | fires | fires | fires | fires |
| `pier/pass2_masses.py` | 10, `0.1`-`0.18`, step `0.077` | F, the pier's big fields stacked | F | fires | -- | fires | -- | fires | fires |
| `pier/pass4_water.py` | -- | ?, faint bands in the water | T | -- | -- | fires | -- | -- | -- |
| `hands/pass08_pickmass.py` | 9, `0.015`-`0.05`, step `0.017` | T, a finger hatched in stripes | F, speckle | fires | fires | -- | -- | fires | -- |
| `hands/pass22_bowl3.py` | 5, `0.038`-`0.05`, step `0.038` | T, a bowl's inside in bands | F, no bars | fires | fires | fires | fires | fires | fires |
| `gpt/25-boat-near-hull` | 7, `0.009`-`0.027`, step `0.005` | F, a hull that reads smooth | F | fires | -- | -- | -- | -- | -- |
| **passes it fires on** | | | | **9** | **5** | **7** | **3** | **7** | **5** |

**No gate is free on the bench's reading, and one is on the painter's.** Read by the
bench, every gate that silences both misfires also silences at least two stacks read as
passages coming back as bars. Read blind by the painter -- three true (the two beams
and the pier's water), six false, one can't tell -- the overlap break alone keeps all
three, fires on three of the six false ones where the rule as it stands fires on all
six, and silences the painter's water misfire; the median clause silences all three
true ones. The two readings split on five crops, and the one that decided it was the
hands' finger: stripes to the bench, speckle to the painter -- and speckle to the owner,
whose look the painter left it to. **So the overlap break alone is built, and the median
clause is not** (the plan's question 13). It fires on 7 of 337 passes, and it still
fires on the painter's headland misfire: fields of separate masses stacked are the kind
of false positive it leaves.

#### Built, in step 7

**What shipped is the overlap break alone, at `0.30`** (`_REPORT_BAND_OVERLAP`,
`_longest_run`): the run breaks between two neighbours across the stack whose reaches
along it share under 30% of the shorter one's. Replayed over the corpus
(`probe_cohort_session.py --graded`), **the engine's own line fires on 7 of 337 painted
passes**, the seven of the table above, and agrees with the re-implementation on every
pass. Laid again from the painter's rehearsal, the water misfire is silent, and under
0.6.0's rule prints the painter's line to the character; the recipe's passage is silent
and its failure block fires.

**The share, swept.** On the four cases in hand it does not matter: the headland misfire
fires at every share from 5% to 90%, because its planes run along the rock's strata over
one span and overlap along the stack as a passage does; the water misfire is silent at
every share, because its glints and ripple share no reach at all; the recipe's failure
block fires at every share. Over the corpus:

| share | fires on | against `0.30` |
|---|---|---|
| 5% | 8 | the laundromat's `p5_inside.py` as well |
| **10% to 40%** | **7** | the same seven |
| 50% | 6 | not the pier's stacked masses (`pass2_masses.py`) |
| 70% | 7 | not those; the laundromat's street (`p3_street.py`) instead |
| 90% | 4 | not the pier's masses, the pier's water or the hands' bowl |

So `0.30` is the middle of a plateau and not a knee. At 50% one more of the painter's false
positives goes quiet -- the kind the break was said to leave -- but that is one pass at the
plateau's edge, and past it passes nobody has read start to fire. It stays at `0.30`.

**What the line says on the pass it adds.** The pier's water (`pass4_water.py`), which the
painter read blind as a passage coming back as bars and 0.6.0's rule missed, is told *8
marks at stepping colours run parallel 0.025 apart, and the narrowest brush laying them is
0.02 -- 0.8 of that step*. Under 0.6.0's rule the pass was one run of 14 -- the nine passes
of its `scumble` and the five reflections laid across the field after it, lighter than
the passes they lie among -- whose colours turn three times, so it said nothing. The break
cuts that run where the reflections lie side by side, into 8, 4 and 2, and the longest
piece is seven of the field's passes with one reflection at its end. **The brush the line
names is that reflection's**: the field's own is `0.108`, over four of its steps, so the
line is right that the field shows bands and wrong about why, and the size it offers,
`0.075`, is narrower than the field was laid with. Judged by the median brush it would
have named the field's own and gone silent; that clause was declined (question 13). Read
without this crop as a kept passage, the break still keeps both beams and fires on three
false positives where 0.6.0's rule fires on six, so the choice does not move.

**The hands' finger, after step 6.** The painter chose the break on condition that the
hands' `pass08_pickmass.py` read as speckle, and warned that the dry brush, once fixed,
might turn the speckle into the stripes the bench saw. Under step 6's gate the dots are
gone: the patch is crossed streaks dragged along its two directions, most of them across
the nine counted marks rather than along them. Re-read by the owner on 2026-09-24, before
and after side by side: still not a passage coming back as bars. The run is unchanged --
9 marks, step `0.017`, sizes `0.015` to `0.05` -- and so is every gate's verdict.

### A variant's cost, and a sheet in four processes

**The painter's harness, part by part** -- a copy of the session after the drawing,
`p01_sky.py`'s three 8-pass scumbles, a look -- takes **10.4 to 10.7 s**: the copy
`0.00 s`, the three scumbles **10.2 to 10.6 s**, the look `0.16 s`. One band is 3.1 s,
`0.39` s a pass. The verdict's fifteen seconds is the paint, not the bookkeeping 0.6.0
already cut. A `rehearse(vary=)` sheet of one band at two opacities takes 5.4 to 5.6 s,
and a sheet of three opacities of a glaze -- `{"points": ..., "glaze": True, ...}`, the
plan entry no document names -- **1.7 s**.

**A sheet in four processes.** Four panels of one band: one panel **2.8 to 2.9 s**; the
four in one process 11.1 to 11.6 s, four times one; in four spawned processes **4.4 to
4.7 s, 1.6 to 1.7 times one panel**, of which starting the four processes and importing
the engine in each is `0.4 s` and each panel's own load of the session file about
1.4 s. **The plan's target for D1 was under 1.5 times, and it is missed on this
machine**; what it would cost to get under it is sending the session to a pool that is
already warm, which is a larger thing than D1 was proposed as.

**Built (step 8): versions side by side, and not in parallel.** The painter's own two
skies -- `try_sky3.py`'s B, a cool rose horizon with warmth laid in from the left, and C,
a peach horizon -- from the painting's drawing, each three 8-pass scumbles and three films
(B lays 33 strokes, C 27), laid three ways (`probe_handover_session.py --alternatives`):

| | the two versions |
|---|---|
| through the painter's harness: a copy and a look each | 31.9 to 32.8 s |
| `easel run --alternatives`, loading and saving the session file included | 32.1 to 32.3 s |
| `s.rehearse_each`, the same two as functions | 31.0 to 31.1 s |

About 16 s a version, over two runs: the painter's own *about 15 s a variant*, for
versions that lay their films and dry between them, where the three ramps alone took the
10.4 to 10.7 s above.

Each version, painted for real on the painting it was tried on, is its panel **to the
pixel** on both sheets, above the label drawn over the panel's corner. The paint is the
cost, as it was: what the sheet changes is one image where the harness wrote two files for
`montage.py` to stitch, and each version's own check printed beside it. D1 was declined on
the numbers above.

### The session file

The painting rebuilt with its time-lapse, as `easel new` and `easel run` make it, and
saved: **16.43 MB**, with 174 frames of 341 x 256 -- the painter's own file was 16.12.
Each array compressed on its own: the frames **9.07 MB**, the colour 6.93, the thickness
0.14, the log 0.28.

| the file re-saved with | size |
|---|---|
| nothing changed | 16.43 MB |
| **the time-lapse frames left out** | **7.36 MB** |
| colour as float16 | 11.98 MB |
| every canvas plane as float16 | 11.90 MB |
| both: frames out, colour float16 | 2.91 MB |
| the frames stored as PNG bytes | 14.88 MB |

Colour through float16 and back moves **20,455 of 786,432 export pixels (2.6%)**, each
by one level, so a file that stored it would stop opening as it was painted. PNG frames
save a sixth of the frames' share and are not worth a format. A GIF rebuilt from the log
of a file with no frames takes **36 to 49 s** over two runs. The painter's own 35 s was
its thirteen passes rebuilt through `easel run`, not a GIF, and one GIF at the end was
the only use it had for the frames.

**Built (step 4): the file keeps no frames, and a loaded session records none.** The
painter's workflow as it ran it — `easel new`, the thirteen passes through `easel run`
one at a time, `easel timelapse` at the end — timed under the engine before the change
and after it, each in a process of its own (`probe_handover_session.py --shell`):

| | before | after |
|---|---|---|
| the thirteen passes through `easel run` | 45.6 s | **36.5 s** |
| the file | 16.43 MB | **7.37 MB** |
| load, save | 0.30 s, 0.79 s | 0.24 s, 0.29 s |
| `easel timelapse` at the end | 2.4 s, the frames read | **26.6 s**, the log replayed |

The GIF is the same, 172 frames at 341 x 256 and 1.14 MB: the film is rebuilt at the
frame size the painting was made with, and the rebuilt frames are the recorded ones,
array for array. It costs a full repaint at 341 px rather than at the canvas's own size,
which is why it is under the 36 to 49 s above.

### The fade and the wet bands

**A pressure list's fade, on the painter's own test** -- a `scumble` at `pressure=[1.0,
0.75, 0.25, 0.0]` on a `0.149` field, read in the painter's measure:

| opacity | left third | middle third | right third | last twentieth | last 4% |
|---|---|---|---|---|---|
| 0.9 | 0.858 | 0.787 | 0.408 | 0.188 | 0.183 |
| 0.5 | 0.800 | 0.644 | 0.291 | 0.170 | 0.167 |

The painter read the right third, where the profile averages `0.135` of full pressure
*(corrected in step 9: this said a quarter, and the passes run from the frame to the
frame, so the list's `0` is the canvas's last column)*. Over the last 4% it reads
`0.183`, which is `0.034` above the field at opacity 0.9 and `0.018` at 0.5; the
recipe's own passage -- *a passage brightening toward one side*, six `flat` strokes at
`pressure=[0.0, 0.55, 1.0]` -- reads `0.162` at its no-pressure end on a `0.150` field,
`0.012` above, and `0.466` at the other. **So the fade gets close and does not arrive**,
which the painter pointed out when this section first said it did; what the recipe does
not say is how close, and how late.

**Three sky ramps, wet and dried.** `p01_sky.py`'s three scumbles on a fresh canvas, one
after another wet and again with `dry()` between them: drying between the bands moves
**16%** of the canvas by more than two 8-bit levels of value and **5%** by more than
eight -- **34%** and **13%** in the export's colour, any channel. Neither draws a seam:
the median column jump is `0.0002` both ways, the largest at the canvas's own edges.

#### Written, in step 9

Three sentences, each written on the probe's own numbers, re-taken on the engine the
round built (`--pressure`). Every figure above came back to the third decimal.

**The lit-air sentence, the right way round.** *A volume of lit air* says a round tip at
`[1.0, ..., 0.1]` is wide and bright at the source and narrow and gone at the far end,
and cites *Pressure*. Its block was right and is unchanged, and its own three films, each
laid alone in titanium white over the painter's dark field and read down the canvas near
the light and near where it gives out, say so:

| film | near the light | where it gives out |
|---|---|---|
| the core, `0.06` at `[1.0, 0.7, 0.12]` | 49 px, peak `0.30` | 16 px, peak `0.02` |
| the body, `0.11` at `[1.0, 0.8, 0.4]` | 97 px, peak `0.29` | 60 px, peak `0.08` |
| the wide faint one, `0.20` at `[0.4, 0.8, 1.0]` | 90 px, peak `0.04` | **159 px**, peak `0.13` |

The last is the film that opens the cone.

**How late the fade arrives, beside its rule.** *A passage brightening toward one side*
says it now, with the table under *Pressure*: at the recipe's own `opacity=0.5` a
quarter pressure makes `0.56` of the change full pressure makes and a tenth `0.24`, and
the painter's band reads `0.41` over its last third and `0.19` over its last twentieth.
**The plan's own sentence for it was wrong** -- *a quarter pressure still lays a quarter
of the step* -- reasoned from the thirds above rather than measured: on the painter's
band a quarter lays two-thirds of the step. The table accounts for the thirds: the right
third's mean pressure is `0.135`, between the table's `0.10` and `0.25` at `0.28` and
`0.67` of the step, and the band's right third reads `0.365` of it.

**The wet bands, as a number**, under *`scumble`*: *Ramps laid over one another, wet or
dried between*. The plan put it under the graded-field recipe's measurement, and this
file has no section of that name -- the recipe's band and its brush are measured under
*`scumble`*, so the ramps went beside them.

## The bell-warden's round

One painter, `claude-opus-5-5`, installed `easel-paint` 0.7.0 from the package and painted
a stone figure on a plinth that has to pass for a statue, in 280 of 300 strokes, as sample
art for another of the owner's projects; a second session painted the next picture for the
same pack the following morning. Acting on both verdicts is one round,
[`PLAN-0.8.0.md`](PLAN-0.8.0.md), and its measuring step is
[`scripts/probe_bell_session.py`](scripts/probe_bell_session.py): it rebuilds both paintings
from their committed passes through the CLI's own `run_script` -- the Bell-Warden in the
order its saved reports record -- keeps a copy of the canvas after each pass and every call's
script line and function, and benches every candidate of the round on the canvas the painter
actually had, each patched in for one bench and never into the engine. Its corpus benches
read one replay of every committed painting with this round's watcher -- the corpus probe's,
keeping each call's site, what each hand-laid mark landed at and a footprint of what each
call painted -- kept in `out/bell/corpus.pkl` after the first run. Everything from
*Section 3, re-measured* on is that script's output; re-run it rather than trusting the
numbers here. The whole probe takes about fifty minutes, half an hour more the first time,
and its flags cut it down.

**What the numbers cannot decide, the probe renders**, into `out/bell/`: the guide
candidates on every ground, the painter's arrangements flat at four sizes, its subject's
pass laid seven ways, and its painting with the darks re-laid under the box's floor. Three
of the round's questions -- 4, 9 and 10 -- are the eye's, and went to the painter with those
sheets.

### The painting, rebuilt

292 records, **280 strokes spent**, in about a minute through `easel run`: every record's
geometry, dab count, brush and colour the painter's, and the export the painter's own PNG
to the pixel, on the machine it was painted on. **Only in the order its saved reports
record** -- `p01_draw.py`, `p02_room.py`, `p03_plinth.py`, `p01_draw.py` again, then
`p04_gargoyle.py` to `p07_glow.py`. In numbered order the second drawing's `erase` is
missing, every mark from the subject's pass on lands one index early, and 97,126 of
786,432 pixels (12.4%) move, 2,131 of them by more than 8 levels and the most by 87. The
corpus probe lays it in the recorded order, and its passes open at the records the saved
reports name: 1, 46, 96, 97, 199, 269 and 286.

What the check printed after each committed pass, as the painter's file saved it:

| pass | `edges:` under 2.5 px | median | `values:` | `lightest:` |
|---|---|---|---|---|
| `p02_room.py` | 36% | 3.6 px | `0.16`-`0.28` | the head's place, unpainted, `0.29` |
| `p03_plinth.py` | 46% | 2.7 px | `0.16`-`0.31` | the plinth's top `0.49`; the head's place `0.20` under |
| `p01_draw.py`, again | 46% | 2.7 px | `0.16`-`0.31` | the plinth's top `0.49`; the head's top `0.19` under |
| `p04_gargoyle.py` | 61% | 2.1 px | `0.16`-`0.36` | the plinth's top `0.47`; the head's top `0.00` under |
| `p05_details.py` to `p07_glow.py` | 48% | 2.6 px | `0.16`-`0.35` | the head's top, `0.52` |

Every one of them, and every rehearsal's, said *no clear light*: 25 of the file's 27
reports, all but the two before the first mark.

### The versions, recovered

The painter rewrote every rehearsed version in place, so its folder held only the last
version of each pass. Its session's transcript holds every change it made to a script
there -- ten whole files written, fifteen in-place Python edits, one shell heredoc and
one `sed` -- and **replayed in order, they end byte for byte on the folder the painter
left**. Each of the 28 `easel run`s in the transcript is then a snapshot of the prelude
and the pass it ran, and run on `s.replay(upto=at)` of the painter's file -- the canvas
that pass opened on -- **every one of the file's 27 saved reports comes back word for
word**; the twenty-eighth run raised, on `at_value(..., 0.13)`, and raises again. One
needs the plan as it stood: the room's first rehearsal ran before the prelude declared
`ground=`, `plan()` keeps what it is not given, and a session replayed from the finished
file carries the finished plan's `ground="buried"` into it. What this round needs of
them -- the first drawing, the eight rehearsed versions of the subject's and the details
passes, and the drawing check -- is filed in
[`versions/`](paintings/Claude/bell_warden/versions/README.md) with the command lines
that run it; run from the shell, each version prints its saved report word for word,
and each drawing redraws its picture to the pixel.

### The marks that did not land

Found filing the painting and in the painter's answers, and re-measured here: the
painter's log laid by a fresh session record by record, and each mark laid again on two
copies of the canvas it met -- as painted, and dried first -- reading the pixels it moved
by more than `0.02` in value.

| records | mark | paint | pixels moved | reads, as painted / dried first | its own value |
|---|---|---|---|---|---|
| 285 | the eye's spark, `round_hard` `0.0028`, `press=1` | `0.19` | 1 (2 by a level or more; at most 21) | `0.39` / `0.37` | `0.86` |
| 253 | the eye's ember, `round_hard` `0.0068`, `press=2` | `1.62` | 5 (at most 22 levels) | `0.22` / `0.25` | `0.62` |
| 254 | the glaze over the eye, `round_soft` `0.022` | `133.5` | 268 (at most 41 levels) | `0.27` / `0.29` | `0.53` |
| 259, 260 | the claw lights, `round_hard` `0.0035` and `0.0032` | `12.5`, `9.7` | 22, 24 | `0.31` / `0.33`; `0.27` / `0.29` | `0.60` |
| 250, 251 | the teeth, `round_hard` `0.0035` and `0.003` | `7.7`, `3.2` | 16, 8 | `0.44` / `0.41`; `0.37` / `0.39` | `0.72`, `0.60` |

`easel log` prints any record under `1.0` as *NO PAINT LANDED*. **The eye's glint is the
glaze**: neither of the two dabs under it landed, and the ember reads a dull `0.22`. On a
fresh canvas the same spark dab carries `0.19` to `0.21` whatever its wobble, at `0.0040`
about `0.2`, and at `0.0068` `1.05` to `1.64`. The claw lights lose `0.01` to `0.05` to the
wet paint under them, as the moved pixels are read, and `0.27` to `0.31` to their size.
Nothing at the call says so for a round tip: `chisel-blank` is for an oriented tip under
four pixels, and a round tip is said to have no such cliff.

**Thirteen of the 280 strokes laid under `1.0`**: the spark, and twelve passes of three
clipped `block_in`s -- records 163 and 164 of the 23 at `p04_gargoyle.py:40`; 214, 216,
218 and 220 to 222 of the 24 at `p05_details.py:12`; 223 to 225 and 239 of the 17 at
`p05_details.py:14`. Eleven laid `0.00` and one `0.11`: charged, and laying nothing.

### The places, read four ways

Every planned place at every pass end, by its mean, median, 75th and 90th percentiles,
and by the share of it more than `0.15` from its own median. At the finish:

| place | planned | mean | median | 75th | 90th | split |
|---|---|---|---|---|---|---|
| the wall, `G1`-`H3` | `0.17` | `0.182` | `0.176` | `0.180` | `0.235` | 0% |
| the glow | `0.31` | `0.277` | `0.263` | `0.290` | `0.361` | 5% |
| the plinth's top | `0.54` | `0.458` | `0.502` | `0.522` | `0.525` | 18% |
| the plinth's front | `0.40` | `0.326` | `0.333` | `0.349` | `0.357` | 1% |
| the plinth's side | `0.27` | `0.255` | `0.267` | `0.267` | `0.267` | 0% |
| the head's top | `0.66` | `0.524` | `0.608` | `0.620` | `0.627` | 24% |
| the floor | `0.17` | `0.197` | `0.169` | `0.212` | `0.286` | 4% |

By the mean the head's top misses by `0.14`; by the 90th the floor misses by `0.12`, from
the plinth's pass on, because the lamp's pool lies in it; by the median and the 75th
every place is inside `0.10`. The split reaches a tenth twice: the plinth's top from the
subject's pass on (15%, then 18%), where the creature's feet stand in it, and the head's
top from the details pass on (24%), the eye and its socket. Nothing else reaches a
tenth at any pass end; the floor comes nearest, at 7%, over the lamp's pool.

### What it read

Measured from the session's transcript rather than asked: before the first mark, about
22,300 words were printed to it, 21,262 of them the documents' --

| document | read | words |
|---|---|---|
| the README (the package's description) | its first 400 lines of 417 | 4,295 of 4,428 |
| `PAINTER.md` | lines 1-700 of 754: not *Sign it* or *Working from a shell instead* | 6,260 of 6,655 |
| `REFERENCE.md` | lines 1-520 of 723: through *Looking, planning, measuring*, not the notices, the shell or the server | 6,266 of 8,904 |
| `RECIPES.md` | its headings, and seven stretches holding twelve of its twenty-one entries: not *A scene with straight edges* or eight later ones | 4,441 of 7,823 |

`PAINTING.md`, `CALIBRATION.md` and `DIAGNOSIS.md` were not opened. It never ran
`--count`, `cost()`, `cost_line()`, `--alternatives`, `explain`, `diagnose`, `preview()`
or `compare()`; it ran `easel demo mistakes`, the nine exercises, 19 rehearsals and
`easel check` once.

### Wenna Brask, the second painting

A second session painted the pack's next picture the following morning, with the first
painter's notes and scripts in hand. Filed as `paintings/Claude/wenna_brask/`.

**Rebuilt** through `easel run` from `p02_setting.py` to `p12_crown.py` in their numbering:
281 records, **262 strokes spent**, every record's geometry, dab count and brush the
painter's, and the export the painter's PNG to the pixel, on the machine it was painted on,
in 43 seconds. `p01_draw.py` is left out: it ran only on a scratch canvas with a light
ground, and it begins `s.erase()`, which lays a record. The corpus probe lays it the same
way, and its passes open at the records the saved reports name: 0, 31, 130, 161, 186, 194,
221, 244, 257, 266 and 278.

**The versions, recovered** from its transcript: 53 changes to its scripts -- Write, Edit
and two PowerShell `-replace`s -- replayed in order end on the painter's folder in every
script, but for the byte-order mark `Set-Content -Encoding utf8` wrote into two of them.
Each of the 36 `easel run`s on the painting's own session gives its saved report word for
word, **all 31**, and the five with none raise again. Fourteen of the 31, from the
figure's pass to the fist's, need the plan as it then stood: the eighth pass, not the
prelude, declared the ground buried.

**What it read**: `PAINTER.md` whole (754 lines, 6,655 words), `RECIPES.md` whole (973
lines, 7,823 words) and `REFERENCE.md` to line 500 (6,068 of 8,904 words, stopping at
*What the tool will tell you*) -- 20,546 words of the guide, the *over 2,000 lines* it
counted -- and before them the first painter's memory note, the Bell-Warden's notes, its
prelude and six of its passes. Not `PAINTING.md`, `CALIBRATION.md` or `DIAGNOSIS.md`.

**The places, read four ways**, at the finish:

| place | planned | mean | median | 75th | 90th | brightest | split |
|---|---|---|---|---|---|---|---|
| the sky high, `A1`-`B2` | `0.29` | `0.307` | `0.302` | `0.318` | `0.341` | `0.416` | 0% |
| the sky low, `A4` | `0.43` | `0.390` | `0.388` | `0.392` | `0.400` | `0.408` | 0% |
| the wall, `H5` | `0.145` | `0.165` | `0.165` | `0.165` | `0.165` | `0.165` | 0% |
| the shawl, `B7` | `0.16` | `0.154` | `0.153` | `0.157` | `0.165` | `0.176` | 0% |
| the lantern | `0.76` | `0.491` | `0.506` | `0.549` | `0.580` | `0.714` | 10% |

**The lantern is the median's own failure**: its iron is most of its place, so no reading
of the whole place finds the lit panes, and by every one of them it misses by `0.18` or
more. The picture's top twentieth, which the `values:` line reads, is `0.42`; its top
hundredth `0.61`; and `1.4%` of the canvas is above `0.60` -- the lamp, its glow and the
lit face, too little of the canvas for a percentile of a twentieth to see.

**What its answers measured, re-measured here.** The painter answered its questions with
three scripts on its own file, filed in `paintings/Claude/wenna_brask/probes/`; run again
on a copy of its folder, the two that read the painting print its tables exactly.

- **Eleven strokes laid no paint**, `4.2%` of the 262 charged -- records 173 (a
  `round_hard` dab at `0.006`, the nostril), 237 (`0.0025`, the catchlight), 240 (`0.004`,
  the flame's core), and all eight of the flour's, 193, 219, 220 and 258 to 262, a
  `bristle` at `0.009` to `0.024` loaded `0.12` to `0.25`. The far iris, a dab at `0.006`,
  laid `2.1` units.
- **The flour's finger stroke, laid again at other loads** on copies of the finished
  canvas:

| load | at size `0.012` | at size `0.03` |
|---|---|---|
| `0.22` | nothing | nothing |
| `0.35` | `1` unit | `4` |
| `0.5` | `9` | `72` |
| `0.7` | `58` | `416` |
| `0.9` | `133` | `734` |

- **The face against the lantern**, read on the values view:

| place | pixels | mean | median | 90th | 95th | 99th | brightest |
|---|---|---|---|---|---|---|---|
| the lantern, as planned | 9,073 | `0.486` | `0.506` | `0.580` | `0.588` | `0.639` | `0.714` |
| its panes, inside the edge straps | 7,244 | `0.525` | `0.522` | `0.580` | `0.592` | `0.643` | `0.714` |
| the panes' middle third | 1,775 | `0.577` | `0.573` | `0.624` | `0.639` | `0.655` | `0.714` |
| the face, whole | 26,094 | `0.505` | `0.584` | `0.620` | `0.620` | `0.639` | `0.718` |
| the fist, as redrawn | 10,944 | `0.302` | `0.267` | `0.443` | `0.447` | `0.573` | `0.690` |

  The face is the lightest mass by every reading, its mean included. The lantern's mean
  here, `0.486`, is `0.005` under the `0.491` above because the two masks differ: the
  table above reads the plan's own mask of the place, 8,880 pixels, and the painter's probe
  draws the polygon itself, 9,073.

### Section 3, re-measured

`--claims`. Both rebuilds come back exact: the Bell-Warden in 44 seconds, 292 records and
280 strokes spent, its passes opening at records 0, 1, 46, 96, 97, 199, 269 and 286; Wenna
Brask in 35 seconds, 281 and 262, opening at 0, 31, 130, 161, 186, 194, 221, 244, 257, 266
and 278; **each export the painter's PNG to the pixel**. Laid in numbered order the
Bell-Warden has 291 records and 97,126 of its 786,432 pixels move (12.4%), 2,131 by more than
8 levels and the most by 87.

| row | what the probe found |
|---|---|
| **1**, the guides vanish | The painter's seventeen guides, drawn by `_draw_guides` at the look's own pixels, and the value step at every pixel they change: over the bare ground a median of **`0.147`**, none under `0.05`; over the room -- the canvas the second drawing went on -- **`0.026`, 96% under `0.05`**; over the finished canvas `0.042`, 65% under. The notes add about 1,600 pixels and change none of it. The plan's `0.045` and 69% were measured once by hand on a different set of pixels. |
| **2**, a shape handed to the drawing | `s.pencil(plinth)` and `s.guide(plinth)` raise `TypeError` (*float() argument must be a string or a real number, not 'Polygon'*), and so does a `Region`. The spline through a closed outline bows every side outward: 99% of the plinth's smoothed path lies outside the plinth, **as far as 21.6 px**; its front plane's, 30.7 px; the body's 42-point outline, 61% outside and 6.7 px at most. |
| **3**, what the calls cost | The subject's pass: 102 strokes in 12 calls, the four `block_in`s at lines 40, 38, 36 and 18 laying 23, 22, 20 and 14 -- two of the 23 landing nothing. The details pass: 68 in 26 calls, the `block_in`s at lines 12 and 14 laying 24 and 17, six and four of them landing nothing. Wenna Brask's figure pass: 99 in 17 calls, its dearest four 13, 10, 9 and 9. |
| **4**, a light into wet paint | The wetness under the head's top as its plane was laid: `0.000`. The details pass laid again without its two `s.dry()` calls: the plane's median `0.607` against `0.606`, the chest's and the wing's ridge lights `0.50` and `0.58` either way. **And the two versions of the subject's pass that laid the plane in the same pass as the body under it** -- the piebald and the arch, which read it at `0.56` and `0.54` -- laid again with the canvas dried before the planes: `0.595` against `0.591`, and `0.567` against `0.563`, with `0.014` and `0.005` of wetness under the plane. There was no wet damage in any version of this painting. |
| **5a**, *no clear light* | 25 of the 27 saved reports, the top twentieth they name running `0.28` to `0.38`. |
| **5b**, the place read by its mean | As *The places, read four ways*, above, to the thousandth; 14% of the head's top's 1,592 pixels under `0.35`. |
| **12**, the give-aways | The ember `7.0` px, the spark `2.9`, the claws `8.0` to `9.7`, the claw lights `3.3` and `3.6`. |
| **13**, the floor | Burnt umber alone reads **`0.128`**, which is `darkest_value`, and `shade("burnt_umber", 1.0)` reaches it; `at_value`'s default dark, ultramarine and umber half and half, reads `0.137`, and umber with 30% ultramarine `0.132`. `at_value(<that mix>, 0.13)` raises *value 0.130 is out of reach: #21232d reads 0.137 and mixing it toward #21232d only gets to 0.137* -- it names nothing else. A supplied `#0d0c10` reads `0.049`; umber with 30, 50 and 70% of it reads `0.107`, `0.093` and `0.077` as mixed, and lands at `0.125`, `0.114` and `0.102` laid as a solid mass on the Bell-Warden's canvas. |

### Where a mark stops landing

A light colour (`0.89`) laid on a flat dark field (`0.16`), twelve marks a size, reading the
paint each record carries and the pixels it moved by more than `0.02`. A mark carrying under
one unit of paint is what `easel log` calls *NO PAINT LANDED*.

| tip | `press` | every dab lands from, at 1024x768 | at 1440x960 | reads halfway to its value from |
|---|---|---|---|---|
| `round_hard` | 1 | `0.0065`, 6.7 px | `0.0045`, 6.5 px | never, to 12 px: it reads `0.22` |
| `round_hard` | 2 | `0.0055`, 5.6 px | `0.0040`, 5.8 px | never: `0.29` at most |
| `round_hard` | 3 | `0.0020`, 2.0 px | `0.0020`, 2.9 px | `0.0035`, 3.6 px (4.3 at 1440) |
| `round_soft` | 1 | `0.0075`, 7.7 px | `0.0055`, 7.9 px | never |
| `round_soft` | 2 | `0.0055`, 5.6 px | `0.0040`, 5.8 px | never |
| `round_soft` | 3 | `0.0025`, 2.6 px | `0.0020`, 2.9 px | never |

**The cliff is in pixels, not in the fraction of the long side a size is given in**: at
1440 the same dab lands at a size a third smaller. A dab at `tip_wobble=0.7` lands where one
at `0` does. A one-touch dab never reads more than about a tenth of the way to its colour at
any size -- it is a light touch by design, which is what the guide says -- and a two-touch
dab a fifth. A short stroke of the claw lights' shape, `0.015` long, pressure `[1.0, 0.2]`,
`opacity=0.85`, lands at every size from 2 px, but reads halfway to its value only from
`0.0060` (6.1 px) with a `round_hard` and at no size to 12 px with a `round_soft`.

A small `bristle` at the loads the flour was laid at, a stroke `0.30` across on a canvas
768x1024 at `opacity=0.8`, the median paint of six:

| size | load `0.12` | `0.22` | `0.35` | `0.5` | `0.7` | `0.9` |
|---|---|---|---|---|---|---|
| `0.009` | `0.9` | `1.0` | `1.5` | `19.6` | `93` | `202` |
| `0.012` | `1.9` | `2.1` | `3.3` | `40.7` | `218` | `491` |
| `0.016` | `3.9` | `4.3` | `6.9` | `103` | `515` | `1,153` |
| `0.024` | `15.3` | `17.1` | `30.5` | `367` | `1,921` | `4,051` |
| `0.030` | `20.2` | `22.8` | `55.4` | `538` | `2,774` | `5,470` |

A cliff between `0.35` and `0.5` at every size -- ten to twelve times the paint -- which is
the painter's *a small bristle under about 0.5 lays nothing*, for a stroke this long. The
flour's own strokes were shorter, and laid under a unit.

### A guide that reads on any ground

`--guides`. Four candidates: **today's** graphite line; **the cased line**, a light neutral
(`236, 236, 232`) three pixels wide under a one-pixel graphite core, opaque and at 150 of
255; and **an ink chosen per pixel**, the graphite over what is lighter than `0.45` and the
casing's colour over what is darker. Every one but today's boxes its notes. Drawn over 35
grounds -- the seven ground presets bare, a flat mid-grey, the Bell-Warden after the room and
finished, Wenna Brask finished, and all 24 committed paintings' pictures brought to a
look's size -- and at every pixel of the line's core, **the larger step of its two tones**: the
core's own over what is under it, and the largest of the casing pixels beside it.

| candidate | share of the line under a step of `0.25` -- median over the 35 | worst | median step, over the room |
|---|---|---|---|
| today | 88% | 100% | `0.03` |
| the cased line, opaque | **0%** | **0%** | `0.73` |
| the cased line at 150 | **0%** | **0%** | `0.43` |
| the ink per pixel | 2% | 100%, on the `burnt_sienna` ground | `0.73` |

Today's line reaches the target only over the two white grounds, and over the lightest
painting of the corpus (`0.55` mean) 36% of it is still under. The per-pixel ink fails
where the paint sits at its own switch -- `burnt_sienna` reads `0.46` -- and up to 12% of a
line elsewhere. **Looked at** (`out/bell/guides_*.png`): the opaque casing is the loudest, a
white line on a dark canvas and a double line on the grey; the translucent one reads on
every ground and gives way to the paint most; the per-pixel ink reads as one clean line
where it works and breaks where the paint crosses its switch.

### The arrangement, flat and small

`--thumbnail`. The prototype fills each mass flat at the value its colour was mixed to, in
the order laid, later over earlier, on the ground's value, at the canvas's size, and brings
it down the way a look is brought down. The painter's arrangements were taken from what
each version's passes handed the mass verbs, run with every verb recording and laying
nothing:

| arrangement | masses | drawn in |
|---|---|---|
| the first drawing: the room, the plinth and the `union()` | 9 | 15 ms |
| the cat | 16 | 14 ms |
| the piebald | 18 | 14 ms |
| the arch | 15 | 16 ms |
| the rim | 14 | 28 ms |
| the bars | 14 | 25 ms |
| as committed, with the details pass's masses | 17 | 36 ms |

**Looked at, at their own sizes and not enlarged**: the cat's two peaks show at 96 px and
read as ears from 128 up; the piebald's islands of light show at every size; the arch's band
wrapped round the body reads only from 192, and at 96 and 128 is a paler body. **With no
argument the prototype draws the plan's own places** -- for this painting the room, the
plinth's three planes and the head's top, and no creature, because the plan named no mass
of it (`out/bell/thumbnails/plan_128.png`). The drawing drawn over a 256-px thumbnail in the
cased line buries the silhouette under its own lines.

### A member that swells and narrows

`--thumbnail`'s last bench, for A4's question whether `ribbon()` needs a width per point.
One member running down four points, widths `0.030`, `0.060`, `0.042` and `0.016`:

| drawn as | outline points | notches sharper than 25 degrees | pixels across at four heights |
|---|---|---|---|
| `ribbon(..., 0.030, end_width=0.016)`, the taper there is | 50 | 0 | 32, 28, 22, 18 |
| a `union()` of round lobes along the path, each as wide as the member there | 154 | **51** | 40, 63, 42, 20 |
| the same union, `.smooth()` | 616 | 3 | 40, 64, 42, 20 |
| a width per point, drawn as a union of one ribbon a segment | 29 | 3 | 41, 64, 44, 20 |

The union swells as a width per point would; unsmoothed its outline is a string of beads,
smoothed it keeps three notches, the same as the segments' joints, and a faint bead along
its edge at full size that does not show at 128 px.

### A lit form: the terminator, not the feather

`--terminator`. Row 9's candidates: the painter's subject pass laid seven ways on the canvas
it opened on. The step across each terminator -- 10 to 90% of the way, along the line's
normal, averaged over three parallel profiles a pixel apart, sampled every 4 px -- and across
the silhouette, in pixels, the median over the line. **The terminator is B2's helper as
benched**: the runs of a copy's outline lying inside the body and 4 px or more from its edge,
runs shorter than `0.02` of the long side left out -- five runs of the mid copy's outline and
four of the shade copy's.

| candidate | strokes | lit to mid | mid to shade | silhouette | `edges:` in the box | said at the call |
|---|---|---|---|---|---|---|
| as painted | 102 | 0.5 | 1.0 | 0.5 | 61% | -- |
| the copies at `feather=0.012` | 102 | 0.5 | 10.0 | 0.5 | 63% | -- |
| the copies at `feather=0.03` | 102 | 14.8 | 14.5 | **1.5** | 65% | -- |
| the copies' own edges left ragged, held to the body | 102 | 9.2 | 2.5 | 1.0 | 55% | -- |
| as painted, and a half-value join along each terminator | 111 | **9.0** | **10.5** | **0.5** | 56% | -- |
| as painted, and a smudge along each terminator | 111 | 2.0 | 17.5 | 1.0 | 54% | `smudge-across`, `smudge-long` |
| the copies laid with `round_soft` | 102 | 0.5 | 1.0 | 0.5 | 62% | -- |

At 1440x960 the same passes give 1.0, 0.5 and 1.0 as painted; 14.0, 14.0 and 1.0 with the
join; 15.0, 16.0 and 1.5 at `feather=0.03`. The join is `flat`, `size=0.010`,
`opacity=0.6`, `pressure="even"`, the two zones' colours mixed half and half, held to the
body: **it widens the step at each terminator to about ten pixels and leaves the silhouette
a step**, which is what *turns the form* is as a number. **Looked at**
(`out/bell/terminator_*.png`): the feathers read as a speckled band along every held edge,
the silhouette's included at `0.03`; the ragged copies as a staircase down the terminator;
the smudge as a smear; the soft copies as the painting, because a soft tip held hard is
held hard. The join leaves a blot where a run ends against the silhouette -- a taper at its
ends is the recipe's to try.

The recipe's own numbers, on an abstract form of parts -- a large mass, a smaller one
overlapping it, two members that narrow -- lit from the upper left on a dark field, the shade
copy two and a half times as far as the mid:

| shift of the mid copy, along the diagonal | at 1024 | strokes | step lit to mid |
|---|---|---|---|
| `0.008` | 8 px | 98 | 18.5 -- the rim is narrower than the profile's reach, so it reads across it |
| `0.016` | 16 px | 98 | 0.5 |
| `0.024` | 25 px | 99 | 0.5 |
| `0.032` | 33 px | 97 | 1.0 |

| join size | `opacity` 0.4 | 0.6 | 0.8 |
|---|---|---|---|
| `0.006` | 2.5 | 3.8 | 4.5 |
| `0.010` | 8.5 | 9.5 | 9.5 |
| `0.016` | 15.0 | 15.0 | 15.0 |

The median step, in pixels, at the mid copy's terminator, ten strokes more than the form's
98. **The join's width is the turn's width**, and past `0.6` its opacity barely matters.

### A head turned toward a light

B4, on Wenna Brask's face at its own size: the figure pass's three structures laid on the
canvas it opened on -- its first rehearsal, the Bell-Warden's shifted copies; its second, a
half-tone band and a lit plane sharing a terminator run beside the profile; and the pass it
committed, the terminator run back past the near eye. The share of the face reading lighter
than halfway between the lit and the shadow mixtures:

| structure | strokes | lit share of the face | of each row, median | middle half of the rows |
|---|---|---|---|---|
| the shifted copies | 135 | 35% | 36% | 26% to 55% |
| the terminator beside the profile | 101 | 24% | 27% | 17% to 41% |
| **the planes sharing the terminator, as painted** | 99 | **74%** | **81%** | 64% to 89% |

The face that worked lights three quarters of what is seen of it, four fifths of a row.

### What a pass costs, call by call

`--cost`, over the 331 corpus passes that lay paint, the line as the painter decided it:
every call dearer than one stroke, dearest first, up to four and no more once three quarters
of the pass is named; its function once per run of calls from it, every call's line, and the
strokes of it that landed nothing.

- **Printed on 143 passes (43%)**; the rest have no call dearer than one stroke.
- Calls named: one on 53 passes, two on 41, three on 29, four on 20. **The share of the pass
  named: a median of 76%**, the tenth percentile 41%; four calls fall short of three quarters
  on 10 passes. A fixed three would have named a median of 74% (the room's pass 71%, the
  subject's 64%), a fixed four 78%.
- **Its length: a median of 67 characters**, the ninetieth percentile 90, the longest 163.
- A named call carrying strokes that landed nothing: on 2 passes, both the Bell-Warden's.
- A call made inside a helper the prelude defines is named at the helper's line in
  `prelude.py`, with the helper's name: *8 scumble at prelude.py:117 (sea_mass)*.

The subject's pass, as the line would have said it:
*dearest: 23 block_in at p04_gargoyle.py:40 (lay_body, 2 landing nothing), 22 at :38, 20 at
:36, 14 at :18 (lay_wing) -- 79 of the 102*.

**Over the whole corpus, 142 of 6,219 charged strokes (2.3%) laid under one unit of paint**:
65 starved `bristle` strokes, 42 two-touch round dabs of about 5 px (the misty forest's), 12
passes of three clipped `block_in`s (the Bell-Warden's), and a tail of small marks.

### A mark that lands short

`--short`. Every mark laid by hand -- a `stroke` or a `dab`, not a film -- over the corpus:
3,096 of them, 2,047 **meant** to stand `0.10` or more off what they landed on. How far each
got toward its own value, over the pixels it moved -- and, for its opacity, that divided by
the opacity it was laid at:

| | 5th pct | 10th | 25th | median | 75th |
|---|---|---|---|---|---|
| the way reached | `0.10` | `0.17` | `0.31` | `0.57` | `0.79` |
| ...for its opacity | `0.15` | `0.27` | `0.50` | `0.75` | `0.94` |

**No gap**: in twentieths from 0, the counts run 68, 2, 29, 37, 34, 64, 60 ... with the
marks that landed nothing the only cluster. A fact at the call for a mark reaching under a
share of its way would fire on 13.7% of the corpus's passes at `0.15`, 18.9% at `0.25`, 29%
at `0.35` and 39% at `0.5` -- because most marks that land short do it on purpose: a starved
bristle is the dry brush, and a translucent stroke is a film laid as paint. What the misses
under `0.35` have in common: a bristle loaded under `0.5` (101), a stroke under 6 px (66),
none of the causes (47), a two-touch round dab under 5.6 px (46), wet paint at `0.3` or more
under the mark (9). On the guide's own code blocks it fires on 2 of 72 at `0.25` and 4 at
`0.35`. **One guide block lays a mark that lands nothing**: *A mass built of planes*'s
dry-brush stroke, a `bristle` 12 px wide at `load=0.35` on the check's own 400x300 canvas;
no block lays a round dab that does.

**The narrow form**: a mark laid by hand that landed under one unit of paint.

| marks | laid | landed nothing | passes | of the corpus's |
|---|---|---|---|---|
| every mark laid by hand | 3,096 | 130 | 48 | 14.1% |
| a round dab | 196 | 57 | 11 | **3.2%** |
| ...under its cliff at its `press` | 60 | 56 | 10 | 2.9% |
| a `bristle` loaded under `0.5` | 388 | 65 | 33 | 9.7% |

**A round dab that lands nothing is predicted by its size in pixels at its `press`**: of the
196 hand-laid round dabs, 5 of the 10 at `press=1` landed nothing, all under 6.5 px; 51 of
94 at `press=2`, 50 of them under 5.6 px; 1 of 92 at `press=3`. It fires on 11 passes of 8
paintings and on no guide block. A starved bristle that lays nothing is a continuum -- the
paint such strokes laid runs 46 under a quarter of a unit, 7, 12, 24, 34, 26, 54 and 185 over
16 in doubling bins -- and falls on 33 passes.

The painters' own marks: the spark reaches `0.12` of its way (`0.19` units, 2.9 px,
`press=1`), the ember `0.11` (`1.6` units, 7.0 px, `press=2`), the claw lights `0.29` and
`0.22`, the teeth `0.40` and `0.34`; Wenna Brask's catchlight `0.05`, the flame's core
`0.19`, the flour's strokes `0.00` to `0.14`, and the nostril's dab, centred outside
the clip it was held to, `0.26`.

### The values line under a key

`--key`, over the 349 corpus passes that had laid paint: the `values:` line says *a clear
light, mid and dark* on 228, **no clear light on 78**, that two clusters read as one on 42 and
no clear dark on 1. Seven pictures finish with no clear light -- the pier, the hands, the
Bell-Warden, Wenna Brask, the terminal window, the harbour and Kimi's lighthouse -- and none
with no clear dark. Under `plan(key="low")` as decided -- the top twentieth held under the
box's middle, `0.54`:

| low-key picture | passes | *no clear light* today | would have left its key | top twentieth | closest two clusters | under `0.10` | under `0.05` |
|---|---|---|---|---|---|---|---|
| the pier | 14 | 12 | **2** | `0.36`-`0.73` | `0.068`-`0.108` | 13 | 0 |
| the hands | 26 | 26 | 0 | `0.29`-`0.41` | `0.036`-`0.103` | 25 | 2 |
| the Bell-Warden | 7 | 7 | 0 | `0.28`-`0.36` | `0.033`-`0.090` | 7 | 1 |
| Wenna Brask | 11 | 11 | 0 | `0.40`-`0.45` | `0.118`-`0.164` | 0 | 0 |
| the terminal window | 7 | 7 | 0 | `0.21`-`0.29` | `0.016`-`0.050` | 7 | 7 |
| the harbour | 5 | 5 | 0 | `0.42`-`0.43` | `0.030`-`0.064` | 5 | 1 |
| Kimi's lighthouse | 4 | 4 | 0 | `0.37`-`0.48` | `0.076`-`0.087` | 4 | 0 |

A declared key would have said nothing on 72 of these 74 passes and spoken on the two where
the pier's top twentieth rose to `0.73`. **The clusters inside a key sit close**: their closest
pair a median of `0.078` apart (`0.047` at the tenth percentile) against `0.141` on every other
pass, so at today's `0.10` the line would have judged 61 of the 74 as two masses read as one.
Scaled to the picture's range -- `0.10` times its 5th-to-95th span over the box's -- the
threshold falls to about `0.027` and fires on none. The low-key pictures' range is a median
of `0.22` of the box's `0.83`.

### What a place reads

`--place`. **The three plans, pass by pass** -- the Bell-Warden's seven places, Wenna
Brask's five, the lighthouse handover's seven -- under each reading:

- The Bell-Warden: at the finish the `plan:` line has 6 of 7 inside by the mean, **7 of 7 by
  the median** and the 75th percentile, 6 by the 90th (the floor, over the lamp's pool). The
  `lightest:` line names the head's top from the details pass on under every reading.
- The handover: 7 of 7 from the tower's pass on under every reading -- and **on the tower's
  pass the mean names another place the lightest and the median names the lantern**.
- Wenna Brask: 4 of 5 under every reading at every pass; the lantern the lightest of the
  planned places from its own pass on, under every reading -- the face, lighter by every
  reading, was not planned.
- **The split** -- a tenth of a place or more over `0.15` from its own median -- marks four of
  the nineteen planned places: the Bell-Warden's plinth top (15%, then 18%) and head top
  (24%), the handover's lantern (12% to 14%) and Wenna Brask's (10%).

**A detail put inside a place**: on every finished corpus canvas, the plans' places and 24
round places a picture, drawn at random, 595 in all; into each, the pixels nearest one point
inside it set `0.30` darker or lighter than the place's median, and each reading's move:

| detail | covering | mean moves | median | 75th pct | 90th pct | the split says so |
|---|---|---|---|---|---|---|
| dark | 5% | `0.014` | `0.000` | `0.000` | `0.000` | 42% |
| dark | 20% | `0.056` | `0.007` | `0.003` | `0.000` | 92% |
| dark | 30% | `0.085` | `0.015` | `0.006` | `0.002` | 91% |
| dark | 45% | `0.128` | `0.045` | `0.016` | `0.007` | 88% |
| dark | 55% | `0.156` | **`0.300`** | `0.026` | `0.013` | 97% |
| light | 5% | `0.015` | `0.000` | `0.004` | `0.009` | 42% |
| light | 10% | `0.030` | `0.003` | `0.010` | `0.058` | 72% |
| light | 20% | `0.060` | `0.008` | `0.032` | **`0.237`** | 100% |
| light | 30% | `0.090` | `0.017` | **`0.272`** | `0.237` | 100% |
| light | 55% | `0.164` | **`0.300`** | `0.272` | `0.237` | 100% |

**The median holds either way to 45% and flips past half**; the mean moves `0.03` for every
tenth; the upper percentiles hold a dark detail and give way to a light one at 10 to 30%.
Undisturbed, **the split fires on 31% of the 595** -- a place drawn at random straddles two
masses as often as not, which is what the clause is for -- and on 4 of the 19 planned.

### The floor, and the darks under it

`--floor`. Six low-key pictures rebuilt twice: as painted, and with every colour laid darker
than `0.20` taken further down -- the span from the box's floor to `0.20` stretched to run from
`0.07`, each colour's linear light scaled so its hue is kept.

| picture | darkest 1% | 5% | under `0.15` | re-laid: 1% | 5% | under `0.15` | planned darks' medians, as painted and re-laid |
|---|---|---|---|---|---|---|---|
| the Bell-Warden | `0.157` | `0.161` | 1% | `0.122` | `0.129` | 25% | `0.17`-`0.18`, then `0.15`-`0.16` |
| Wenna Brask | `0.149` | `0.149` | 9% | `0.102` | `0.106` | 62% | `0.15`-`0.16`, then `0.11`-`0.12` |
| the terminal window | `0.141` | `0.141` | 18% | `0.090` | `0.094` | 38% | -- |
| the night pool | `0.141` | `0.161` | 4% | `0.098` | `0.129` | 20% | -- |
| the misty forest | `0.137` | `0.145` | 10% | `0.090` | `0.098` | 22% | -- |
| the sunset | `0.137` | `0.149` | 7% | `0.086` | `0.098` | 18% | -- |

**A darker dark moves a picture's darks down together; it separates only what was already
apart.** The Bell-Warden's planned darks -- the wall and the floor, both planned at `0.17` --
stay `0.01` apart either way; its room's mixtures, `0.15` to `0.21`, would have run `0.11`
to `0.21`. The sheets are `out/bell/floor_*.png`.

### A light the plan names

`--lamp`, the named light of each plan pass by pass. At the finish:

| plan | the light | planned | median | 90th | 95th | brightest | the canvas's top twentieth | its share of the canvas |
|---|---|---|---|---|---|---|---|---|
| the Bell-Warden | the head's top | `0.66` | `0.606` | `0.626` | `0.630` | `0.699` | `0.35` | 0.20% |
| the handover | the lantern | `0.86` | `0.881` | `0.900` | `0.907` | `0.946` | `0.69` | 0.08% |
| Wenna Brask | the lantern | `0.76` | `0.507` | `0.579` | `0.590` | `0.713` | `0.42` | 1.13% |

**Every named light is under a twentieth of its canvas** -- under a fiftieth -- **and every one
stands clear of the canvas's top twentieth** by `0.17` to `0.28` at its 95th percentile, the
reading the `values:` line cannot give. Read at its 95th percentile, no plan's `lightest:`
verdict changes; the number printed does.

### Names a pass binds again

`--rebind`, parsed rather than run: of the 284 committed passes of the 20 paintings whose
passes run after a prelude, **20 bind a name the prelude bound** -- 17 to the same thing (the
pier's `p = s.palette` in twelve passes, the fogged glass's `from easel import polygon`, the
handover's `import random`) and 3 to a loop's variable the prelude's own loop had left bound
(the handover's `x` and `y`). **Bound again to something else, where the prelude bound it by
assignment, definition or import: none.** Wenna Brask's `H`, which a dict replaced, was in
rehearsals that raised on it and are not filed.

### A place laid over and over

`--repaint`: masses (`block_in`, `scumble`, `cover`, `sweep`) half or more of whose footprint
lies on marks laid in an earlier run, grouped by place, counted by run.

- **Over the corpus's committed passes**, counting the painter's `subject` marks -- 17 of the
  24 paintings note them: a place reaches two runs in two paintings, Wenna Brask's fist
  (twice) and the night pool's water at (`0.50`, `0.67`) (three times). Counting every mark
  instead, every painting but two has such a place, and the seaside village one laid over
  nineteen times.
- **The Bell-Warden, its filed rehearsals included**: counting only committed marks as
  earlier, the count first reaches two at the details pass's second rehearsal -- the creature
  being built -- and never sees the head's failures, which were laid on a canvas holding no
  subject yet; counting a rehearsal's own marks as earlier, it reaches two at the arch, the
  third version, after the upstream rule had already sent the painter back twice.
- **Wenna Brask, likewise**: committed marks only, the fist reaches two at `p07_fist.py`, the
  redraw -- exactly as its painter counted; with rehearsals' marks, the figure's place reaches
  two at `p03_figure.py` itself, the committed pass after its two rehearsals.

The count finds the fist, and speaks on a subject being built as readily as on a passage
failing.

### An inward scumble's rings

`--rings`: an inward scumble laid on a flat dark field, the Bell-Warden's glow and Wenna
Brask's first pool, ring count by ring count. The ripple is the RMS of what is left along 24
radii once a 31-pixel running mean is taken out.

| `n` | the glow, `wall` to `glow` | the pool, `mill` to `glow_wall` |
|---|---|---|
| 4 | `0.0065` | `0.0065` |
| 8 | `0.0040` | `0.0088` |
| 12 | `0.0035` | `0.0048` |
| 16 | `0.0027` | `0.0076` |
| 20 | `0.0026` | `0.0061` |

**Looked at** (`out/bell/rings_*.png`): at every count from 4 to 20 both read as rings -- a
target on the wall. More rings are finer and fainter, never gone. `inward-comb` spoke only at
20 on the pool. No ring count answers it: the pool the second painter found was three soft
strokes of paint.

### Drawing units

`--units`, parsed. **One of the 24 paintings wrote a pixel helper** -- Wenna Brask's `P()`,
and again in two of its probes -- and **two moved or scaled points about a centre by hand**:
its `T()`, and the heron's second attempt, whose prelude scales a list of points about a
centre by `k`. One more drew in units of its own, metres through a perspective projection
(the winter greenhouse's `P()`). `.shifted()` appears in eight paintings, 13 times in the
Bell-Warden's scripts and 11 in Wenna Brask's; `aspect=` in seven; `s.circle` in eight.

**What a shape's numbers are, in pixels**, off the masks:

| on a canvas | the shape | measured |
|---|---|---|
| 1024x768 | `ribbon(..., 0.05)` across a level ribbon | 38 px |
| | across an upright one | 52 px |
| | across one at 45 degrees in pixels | 45 px |
| | `ellipse(p, 0.05)`, `blob(p, 0.05)` | 102 x 76, 102 x 74 px |
| | `ellipse(p, 0.05, aspect=s.aspect)` | 102 x 102 px |
| 768x1024 | `ribbon(..., 0.05)` level, upright, 45 degrees | 52, 38, 45 px |
| | `ellipse(p, 0.05)` | 76 x 102 px |
| | `ellipse(p, 0.05, aspect=s.aspect)` | 76 x 76 px |

**A ribbon's width is in the canvas's coordinates across its line** -- a fraction of the height
across a level ribbon, of the width across an upright one -- so one ribbon changes width as it
turns. A round shape's radius is a fraction of the width across and of the height down; with
`aspect=` it is round in pixels, the width's. A brush's `size` of `0.05` is 51 px either way:
a fraction of the long side.
