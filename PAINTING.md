# How the paint behaves: colour, wet paint, the brushes, the planning tools, and copying a photograph

This is the second half of [`PAINTER.md`](PAINTER.md), which is the method and the
file to read first. That one is the order of work and the mistakes; this one is how
the engine behaves — what a mixture does, what a brush leaves, what a shaped mass
costs, what the planning verbs answer — each rule stated once, with its number, and
the measurement behind the number in [`CALIBRATION.md`](CALIBRATION.md). The
procedures for particular passages are in [`RECIPES.md`](RECIPES.md).

**Read it once, after the nine exercises and before the painting.** You are not meant
to hold it in your head; you are meant to have read it, so that when the guide says a
mass wants a shape rather than a box you already know what a box costs. **The last
chapter is for a painter with a photograph to copy.** Skip it if you have none.

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
keep a painting coherent — the same three or four mixtures repeated across a canvas is
most of what "colour harmony" means.

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
| `at_value(base, target)` | The mixture of `base` that reads at `target`, from either side. Raises if the box cannot reach it. |
| `value_of(c)` | How light it reads, `0.0`–`1.0`: the number `look(values=True)` shows. |
| `chroma_of(c)` | How *coloured* it is: `0` for a grey, `0.20` for `cadmium_red`. |
| `hex(c)` | The sRGB hex, for your own notes. |

Three things about the mixing that will surprise you:

- **Blue and yellow make green**, red and blue make violet, and complements make lively
  greys. This is subtractive pigment mixing, not RGB averaging.
- **White is a weaker lightener than you expect.** For a really pale colour, use more
  white than feels right; `at_value` does that arithmetic for you.
- **A yellow and a blue make green even when you were after a grey**, and tinting does
  not undo it. Neutral greys come from complements, or from earth and white, or from
  `desaturate`. Print `hex()` of a mixture before you paint a field of it, and lay the
  mixtures you plan to use side by side first (exercise 9 in the guide).

**The engine lays the chroma it is given, never more.** A mixture that comes back more
vivid than its number is the eye judging it against the field it sits in; compare
`chroma_of(mix)` with `chroma_of(s.sample(field))` before laying a plane of it
(*Chroma* in [`CALIBRATION.md`](CALIBRATION.md#chroma-the-engine-lays-what-it-is-given)).

**Supplying a colour of your own.** A slot takes a hex string, or an `(r, g, b)` triple
of `0.0`–`1.0` **read as sRGB, exactly as the hex string is**. What you supply lands as
written — including a black, and anything below the darkest mixture the box can reach:

```python
s.palette["ink"] = "#0d0c10"           # hex string
s.palette["ink"] = (0.05, 0.05, 0.07)  # sRGB, 0.0-1.0 — the same as "#0d0d12"
```

**The triple is the trap, in exactly one place: matching a colour that is already on
the canvas.** The engine's own colours are *linear* arrays, so one read off the canvas
and handed back as a tuple is re-read as sRGB and comes back much darker — a
`toned_grey` ground reads `0.53`, and its own mean passed back as a triple reads
`0.25`. Do not convert it. Ask for it, and pass what you are given straight on:

```python
s.palette["already_there"] = s.sample(cell("D5"))   # the engine's own array
s.palette["matched"] = s.sample()                   # the whole canvas, averaged
```

`s.sample(place)` returns the paint's own array, which every colour argument takes
untouched, and it averages over a shape rather than over the shape's box. **It
averages what is in the place, so to measure a mass, hand it the mass**: sample the
cell and you get the mass averaged with everything around it, which reads exactly like
a measurement and is not one. A number that disagrees with `at_value` by more than a
hundredth is almost always the place, not the paint. `s.sample(place, rendered=True)`
reads the *view* — the relief `look()` draws, and any graphite the paint has not
buried — and over a mass the two agree to `0.001`:

```python
s.palette.value_of(s.sample(mass))                  # the paint
s.palette.value_of(s.sample(mass, rendered=True))   # the view of it
```

A list of 0–255 integers is not one of the forms, and it does not raise — it clamps,
so `[13, 12, 16]` gives you white. Reach for a supplied colour when a reference
genuinely goes below the palette's floor of `0.14` (*What the box reaches* in
[`CALIBRATION.md`](CALIBRATION.md#what-the-box-reaches)), and not otherwise.

---

## Wet paint

Paint lands wet and stays wet for a while. Paint that lands on wet paint **mixes** with
it instead of covering it: yellow over still-wet blue is green. Used deliberately it is
how you get soft transitions for free.

```python
# Blend on purpose: work into wet paint.
s.block_in(cell("C3"), "bristle", "cerulean", density=1.0)
s.stroke([(0.3, 0.3), (0.5, 0.35)], "bristle", "titanium_white")   # blends in

# Or cover cleanly: dry first.
s.dry()                                                    # whole canvas
s.dry(0.5, region="upper-half")                            # partial, one region
s.stroke([(0.3, 0.3), (0.5, 0.35)], "bristle", "titanium_white")   # sits on top
```

**If you want the new colour to read as itself, `dry()` first.** Wet is a matter of a
few strokes, not a whole pass: wetness fades with every mark made anywhere on the
canvas, and one `block_in` is many marks, so by the time you have blocked in a second
mass the first is most of the way dry. If two colours are to mix on the canvas, put the
second down within a few strokes of the first (*Wetness* in
[`CALIBRATION.md`](CALIBRATION.md#wetness)).

A `glaze` is the opposite move — a thin transparent film over dry paint that shifts the
colour underneath without hiding it:

```python
s.glaze([(0.2, 0.6), (0.8, 0.6)], "alizarin", opacity=0.15)
```

**A glaze is strong in proportion to its *distance* from what it lands on, in hue as
well as in value**, and `opacity` is the wrong knob to reach for first. A warm light
film over a cool dark mass:

| `opacity` | what it does to the value under it | and to the hue |
|---|---|---|
| `0.05` | `+0.028` | already neutral — the cool is gone and nothing warm has arrived |
| `0.10` | `+0.061` | warm |
| `0.14` | `+0.087` | a stripe of a different colour |
| `0.20` | `+0.123` | a different mass |

At `0.14` the film has moved the value by nearly the whole `0.10` that separates two
masses. **So mix the glaze close to what it lands on, in value and in hue, and then
choose an opacity** — or let `glaze(..., to_value=)` search for the opacity that lands
the passage on a value, which costs the same one stroke (*`glaze`* in
[`CALIBRATION.md`](CALIBRATION.md#glaze)). And a film is a mass at a depth: a glaze
laid last because it is *light* still lands on top of whatever it crosses, so keep it
off the near things, or lay them again after it — two painters in a row lost a near
edge to a late one (step 3 in [`PAINTER.md`](PAINTER.md#3-paint-from-back-to-front)).

---

## Try the mark before you spend it

Three tools sit between deciding on a mark and paying for it, and they answer the three
questions you have about a mark you have not made: *where does it go*, *what will it
look like*, and *what does it cost*. None touches the canvas, none writes to the log,
and all three take the same plan.

```python
plan = [{"points": [s.pt("top_l"), (0.40, 0.62)], "brush": "liner",
         "size": 0.006, "color": "light", "label": "edge"}]

s.preview(plan,  region=span("C3", "F6"), grid="fine")
s.rehearse(plan, region=span("C3", "F6"))
s.cost(plan)                                   # 1
```

`preview` draws the intended points and the brush's *width* — at a default width if
you gave it bare points, which is fine for placement and useless for checking an edge.
`rehearse` paints it on a copy and shows you the result, with its tooth and its edge
and how it mixes with what is already there. `cost` returns what the plan would
charge. **For a mark that is 1 and you did not need to ask. For a mass it is the number
you cannot work out by hand**, because a mass is priced on the extent of its box along
the direction the passes stack *and* on how many times a pass line crosses it:

```python
straight = ribbon([(0.20, 0.50), (0.78, 0.50)], 0.029)
s.cost({"shape": straight, "size": 0.015})                  # 4

bent = ribbon([(0.20, 0.30), (0.45, 0.62), (0.78, 0.34)], 0.029)   # same width
s.cost({"shape": bent, "size": 0.015})                      # 75 -- round a bend
s.cost({"shape": bent, "size": 0.03})                       # 38 -- a wider brush

# and the price is on the preview, beside each mass and sweep, without asking
s.preview({"shape": bent, "size": 0.015, "label": "mass"})  # reads "mass  75 strokes"
```

Nineteen times the price for the same width of paint, because the box a bend sweeps
out is ten times the band's own width, and a pass line crosses a curve twice. If the
number is more than you want to pay, a wider brush or a thinner `density` is the lever.
**`cost_line` says *why* the number is what it is**: the passes crossed a second
direction, they stepped across a bounding box much bigger than the mass, or a concave
outline cut each one into pieces — and each names its own lever.

```python
print(s.cost_line({"shape": bent, "size": 0.015}))
# 75 strokes -- 25% of the 300 left of a 300-stroke budget
#   75  42 passes stepping across 0.34 of the canvas, each cut into 1.8 pieces by the outline
```

**And there is a fourth verb, which paints the plan you just checked.** `cost`,
`preview`, `rehearse` and `paint` all read one object, so nothing is retyped between
checking a plan and painting it; a plan that is retyped will drift, and the drift
arrives as paint. Marks, masses and sweeps may be mixed in one list and are painted in
the order given:

```python
s.paint([{"shape": blob(cell("D5"), 0.12, seed=3), "brush": "bristle",
          "color": "dark", "size": 0.07},
         {"points": [(0.31, 0.62), (0.55, 0.58)], "brush": "liner", "size": 0.005}])
```

A rehearsal is seeded as if its marks were the next strokes of the real painting, so
what you rehearse is what lands, pixel for pixel. That is the property *rehearse every
pass* in the guide rests on. From the shell it is `easel run pass.py --rehearse`; in
Python it is `s.scratch()`, the same throwaway copy, and several scripts rehearse
together onto one copy so a pass that lands on another is judged on it. `look`,
`preview`, `rehearse`, `cost` and `compare` leave nothing behind; `pencil`, `dry` and
`erase` are free but logged, and a mark's texture is seeded from its place in the log,
so adding or removing one shifts the texture of every mark after it — deterministic,
and a painting still rebuilds from its scripts (*The log, undo, and the stream* in
[`CALIBRATION.md`](CALIBRATION.md#the-log-undo-and-the-stream)).

---

## The brushes

One line each. Reach for `bristle` for marks that have a direction and `flat` for quiet
masses.

| Brush | What it is for |
|---|---|
| `bristle` | **The workhorse** for any mark with a direction. Broken, streaky, alive — and never solid. |
| `flat` | Block-in, chisel edges, flat planes. Turns to follow the stroke. |
| `round_hard` | Deliberate marks, accents, small shapes, final highlights. |
| `liner` | Fine lines at the scale of a feature. `round_hard` at `size=0.005` with no jitter, and it holds its load. |
| `round_soft` | Blending and soft edges. The least painterly — use it sparingly, and never for a mass: above about `size=0.05` it airbrushes. |
| `knife` | Thick slabs with a hard edge. Drags what it crosses. Use rarely, and keep it close in value to what it lands on or it reads as something stuck to the surface. |
| `smudge` | Carries no paint; moves what is already there. For losing edges. |

**A `bristle` stroke is never solid** — it lays a comb of streaks, which is what makes
it alive on a mark whose direction you mean. Lay a big quiet mass with `flat`, or with
bristle passes that *cross*; single parallel passes rib it. Below about `size=0.02` a
bristle is four streaks with gaps, not a brush: small solid planes want `flat` at
`pressure="even"`, or `round_hard`.

**A short `flat` or `knife` stroke is a rectangle.** The oriented tips hold a chisel
square to their travel — right for a mass, wrong for an accent — and they do not taper
under a pressure list. **Small accents want `round_hard`. `flat` and `knife` want a
length.**

Size is a fraction of the canvas's long side: `0.2` is a big brush, `0.02` a small one.
**Use a bigger brush than feels comfortable for a mass**, and **scale a mark off the
thing it describes, not off the canvas**: inside a mass `0.3` of the canvas across, a
plane within it wants about `0.015–0.025` and a detail within that plane `0.004–0.010`.
Under about four *pixels* an oriented tip lands the ground and nothing else, and a solid
mass lands a little short of its mixture on any brush but a round one (*What a solid
mass actually lands at* in [`CALIBRATION.md`](CALIBRATION.md#what-a-solid-mass-actually-lands-at)).

### The shape each tool leaves behind

**Every tool here has a geometry of its own, and if you do not decide the shape, the
tool decides it for you** — then you spend twenty marks fighting a structure you never
chose. What each one leaves when you are not watching:

| Reach for | and if you are not watching, you get |
|---|---|
| `flat` / `knife`, short | a rectangle with chisel ends |
| `flat` / `knife` filling a mass whose boundary is not parallel to the passes | **a staircase down that boundary** — each pass ends in a chisel square to its travel, and where the boundary slopes the ends stop at different heights and stack |
| `round_hard`, short | a capsule. It needs to be about **7×** longer than it is wide before it stops reading as one |
| `round_hard` or `liner`, several small marks | **one disc, printed over and over** — unless `tip_wobble=0.7` redraws the outline per mark. `report()` counts them |
| `bristle` below `size≈0.025` | a comb: a woven strap across a band, or a ladder of ticks along an edge |
| `sweep` round a closed shape, or an inward `scumble` with too many rings | **concentric rings** |
| several overlapping `blob`s | a dome — blobs of similar size average to a circle |
| a shallow shape, passes along its long axis | **its bounding box** |
| any loop or generator you write | its own statistical signature: one density, one mark length, no clumps and no holes |
| repair laid on repair, always additive | horizontal strata, one visible edge per repaint |

Three of those need more than a row.

**The staircase is the most common way a mass goes wrong here, and it is measured.** A
chisel leaves three to four times as many horizontal pass-ends down a sloping boundary
as a comb or a round tip, and a *smaller* chisel is worse (*The chisel staircase* in
[`CALIBRATION.md`](CALIBRATION.md#the-chisel-staircase)). Four repairs, cheapest
first: run the passes *along* the sloped boundary — `direction=` in degrees, or the
two points of the boundary itself — so the chisel ends fall on an edge that is square
to them; lay the plane with a comb and put the core back with one solid stroke down its
middle; `edge="clean"`, which draws the contour along the outline for one stroke more
(*Masses that are not rectangles*, below); or `edge="hard"`, which masks every dab to
the outline, costs no extra stroke and takes the staircase out rather than hiding it —
`13%` of strong edges horizontal against `4%`, on a mass with no horizontal feature.
It is opt-in because a mass standing *behind* other things wants the brush to break
past its boundary, which is what ragged is for.

**The shallow shape is not covered by the brush-width rule.** An ellipse `0.256 ×
0.128` filled with a `flat` at `0.022` — a twelfth of its width — came out a rectangle.
**The dimension that matters is the mass's extent *perpendicular to the passes*.** Run
the passes across the short way, or turn them:

```python
s.block_in(ellipse(span("D4", "F5")), "flat", "mid", direction=90, size=0.022)
```

**And a mass much longer than it is wide is a stroke, not a mass.** `block_in` will
comb a `0.022 × 0.18` band even at `density=1.0`; a long `stroke()` is the right tool,
and `block_in` is for something with two dimensions.

### The angle of the mark

**Do not let the canvas choose your stroke direction.** Left alone, everything here
runs horizontally or vertically: `block_in`'s named directions are horizontal,
vertical and a 45° diagonal, every named region is an axis-aligned rectangle, and an
oriented tip is held square to its travel. Paint a sloping mass with horizontal passes
and you get a stack of bars with flat ends.

**Sweep a mass along its own axis.** `block_in` takes degrees, clockwise from
horizontal, as well as the four names, and `"axis"` is the mass answering the question
itself:

```python
s.block_in(span("A4", "F7"), "flat", "shadow", direction=28, size=0.12)
s.block_in(span("A4", "F7"), "flat", "shadow", direction=(28, 118), size=0.12)  # crossed
s.block_in(ribbon([(0.2, 0.8), (0.8, 0.4)], 0.2), "flat", "shadow", direction="axis")
```

**What the number names.** Take one mass, a band twice as wide as it is tall, and give
it three angles. At `0` each pass is a horizontal line the full width of the band, and
the stack of them climbs from the top edge to the bottom — the marks lie along the
long side, and there are as many of them as the *short* side divides into part-brushes.
At `90` each pass is a vertical line the height of the band, and the stack marches
left to right: the same mass, many more passes, each one short. At `45` the passes run
down-right at a slant, and the stack steps down-left, perpendicular to them. So: **the
passes run along the angle, and the stack steps across it.** That is also what
`cost_line` counts when it says *N passes stepping across 0.50 of the canvas* — the
`0.50` is the mass measured perpendicular to the angle, and the two instruments have
always agreed.

Passes that run along the form cover it in fewer strokes than passes that step down
it, and come out visibly less square (*Laying a mass along its own axis* in
[`CALIBRATION.md`](CALIBRATION.md#laying-a-mass-along-its-own-axis)). **The angle is in
the `0..1` coordinates, not on the screen**: on a canvas that is not square, an angle
you measured off the picture will not run along the edge you measured it on
(*Units* in [`REFERENCE.md`](REFERENCE.md#units-which-is-where-the-surprises-are)).
So do not convert it — hand over the line itself, and let the engine do the arithmetic:

```python
eave = ((0.33, 0.012), (0.58, 0.286))        # two points off the drawing, or a projection
s.block_in(blob(span("C1", "G5"), 0.2), "bristle", "shadow", direction=eave, size=0.10)
```

A pair of *points* is a line to run along; a pair of *numbers* is still two angles, so
`direction=(28, 118)` is unchanged. This is what to reach for whenever the angle came
off the picture — a gable, a sill, a cable — because that is the case the conversion
was needed for and nobody did it.
**Two directions are what breaks a comb, and more do not break it further**: a sequence
lays a full stack per angle and is charged the sum, so a ten-angle list costs a mass
eight times over.

**Turn the blade.** Any oriented tip can be pinned instead of following its travel:

```python
s.stroke(path, "knife", "light", size=0.09, angle_follow=False, angle=45)
```

At 45° the knife lays a parallelogram; at 90° it is edge-on and draws a ribbon. This
matters at the *ends* of marks and on short ones; on a long sweep the path does nearly
all the work.

**A round tip is the tip that declares no axis.** `round_hard` has no orientation, so
it cannot print the canvas's grain into a mass however you drive it. When a passage
keeps coming out square and you have already fixed the direction, that is the brush to
change to — not `round_soft`, which airbrushes at any size a mass needs.

### Per-stroke overrides

Anything about a brush can be overridden per stroke — and per **mass**: `block_in`,
`sweep` and `scumble` take the same keywords and pass them down to every stroke they
emit.

```python
s.stroke(path, "bristle", "shadow", size=0.14, opacity=0.5)
s.stroke(path, "flat", "light", hardness=0.9, jitter=0.05, load=0.4)
s.stroke(path, "bristle", "shadow", size=0.12, load_falloff=0.25)   # runs dry slower
s.block_in(cell("D5"), "flat", "shadow", opacity=0.5, load=0.8)     # masses too
```

**`opacity` does not thin a long stroke, it only slows it down.** Dabs overlap, so a
low opacity accumulates back to nearly full colour. A soft film is what `glaze()` is
for, and a quiet passage is two colours mixed closer together, not a lower opacity.

**`load` is how much paint the brush carries**, and dropping it is how you get dry
brush — one of the best tools you have for making a surface look worked. The window for
a deliberately broken mark is about `0.4` to `0.6`. But pass `load=1.0` for anything
that has to read as a *solid* mass, a correction included: a pass laid low because it
sounded painterly leaves a speckled film that everything after it sits on. On a mass,
`solid=True` is that clause together with the `load_falloff=0.0` that keeps the far end
of each pass from running dry.

**A loaded brush runs dry along a stroke**, so where a long stroke ends is where its
texture is loudest — run the next one back the other way. **Do not lay one broken pass
across the whole canvas**: edge to edge on a single load prints the canvas's own texture
as an even field over everything, and it stays visible under every later stroke.

**`tip_wobble` gives a round tip a silhouette of its own**, redrawn for every mark the
way a bristle's comb is, so a handful of small marks are not a handful of copies of one
disc: `0` is the disc, `0.35` a brush set down once, `0.7` and up a clot. Only the round
tips take it.

```python
s.dab(0.42, 0.36, "round_hard", "light", size=0.016, press=3, tip_wobble=0.7)
```

### Pressure

`pressure` shapes the stroke along its length: `"taper"` (the default, and usually
right), `"press_in"`, `"lift_off"`, `"even"` (the flattest-looking option),
`"swell"`, `"dab"`, or a number, or a list interpolated along the stroke:
`pressure=[0.2, 1.0, 0.3]`.

**On a round tip — `round_hard`, `round_soft`, `liner` — pressure changes how wide the
mark is as well as how much paint lands.** `size` is its width at full pressure, and it
never thins below about a pixel and a half. **On the oriented tips — `flat`, `bristle`,
`knife` — it changes only how much paint lands**, because a flat brush's width is the
mass it lays. So:

- **A mark that tapers is one stroke.** `pressure=[1, 0]` on a round tip starts at the
  width you asked for and ends at a point. A pressure list on a short chisel mark
  fades the paint without narrowing it, and the call says so.
- The *paint* half of the profile shows on short strokes and on a colour not already at
  full strength; on a long stroke the overlapping dabs saturate.
- **Varying the width of your masses is still your job**, because the brushes that lay
  masses do not vary with pressure. Pass a different `size` — the single most
  effective thing you can do to stop a painting looking mechanical.

**At the scale of a feature** a single dab is a *light touch* — the start of a taper,
landing a fraction of its colour at about half the width — and a small highlight is
`s.dab(x, y, ..., press=3)`: three stamps on the same spot, the middle one at full
pressure, and **one** stroke against your budget. **Use `press=3` for anything you
actually want to land**; `press=1` and `press=2` are whispers (*At the scale of a
feature* in [`CALIBRATION.md`](CALIBRATION.md#at-the-scale-of-a-feature)). On a mass,
a pressure list runs the same way on every pass whichever way the pass travels, which
is what *a passage brightening toward one side* in
[`RECIPES.md`](RECIPES.md#a-passage-brightening-toward-one-side) is built on; the
details, and which side a stack starts from, are under *Pressure* and *Where a stack of
passes starts* in [`REFERENCE.md`](REFERENCE.md#where-a-stack-of-passes-starts).

---

## Masses that are not rectangles

Almost nothing you want to paint is a box. There are two ways not to paint one, and
they answer different questions.

**When you can say what shape the mass is**, build it and fill it. Five ways to make
one, none of which needs you to invent coordinates:

```python
blob(cell("D5"), 0.22, wobble=0.3, seed=2)     # an irregular mass filling a cell
ellipse(span("C3", "E5"))                      # a round mass filling a run of cells
hull([s.pt("top_l"), s.pt("top_r"), s.pt("base")])   # the mass around your landmarks
ribbon([(0.15, 0.8), (0.5, 0.55), (0.9, 0.62)], 0.18)   # a mass following a line
polygon([(0.2, 0.9), (0.35, 0.4), (0.6, 0.5), (0.7, 0.95)])   # an outline you have
```

Look at it before you spend twenty passes on it, then fill it along its own axis:

```python
shape = blob(span("D4", "F6"), wobble=0.35, seed=5)
s.preview(shape)                                    # the silhouette, painting nothing
s.block_in(shape, "bristle", "dark", direction="axis", density=0.9, size=0.12)
```

A shaped block-in costs about what its box would, because the passes are counted
across the mass and not over its area — **and for a long curved shape the box is the
whole story**: a ribbon `0.029` wide costs 4 passes laid straight and 75 with a bend in
it, because the passes step across the *bounding box* and a pass line crosses a curve
twice. A mass with a bite out of it costs more than its box for the same reason.
**Before you block in anything long or concave, look at `shape.box` and ask
`s.cost(...)`.**

**The paint lands outside the shape, and it is the most expensive first mistake with
shapes.** A pass stops when its *centre* reaches the boundary, so the brush hangs over
by up to three-quarters of its width — and with a brush that is a large fraction of the
mass, the silhouette you built simply disappears, taking its neighbours with it. Three
answers:

```python
mass = blob(span("D4", "F6"), wobble=0.3, seed=2)
s.block_in(mass.inset(0.045), "flat", "dark", size=0.09)   # inset by half the brush
s.block_in(mass, "flat", "dark", size=0.06)                # or keep the brush small
s.block_in(mass, "flat", "dark", size=0.09, edge="clean")  # or ask for a drawn contour
```

**Keep the brush under about a fifth of the mass's width, or `inset()` the shape by
half the brush size.** **`edge="clean"` is those two steps and a third**: it insets the
fill by half the brush, lays it, and sweeps one pass along the inset outline in the
same colour, so the *outer half* of the brush lands on the line you drew, for one
stroke more than the same mass ragged. Reach for it when the silhouette **is** the
drawing — and use a solid tip, because one comb pass along a contour leaves a stringier
outline than the ragged fill did. It needs a brush under about a quarter of the shape's
shorter extent; past that the contour pass lays the strip the inset gave up as one
chisel stroke with rounded corners, and the call says so (*A clean edge on a narrow
mass* in [`CALIBRATION.md`](CALIBRATION.md#a-clean-edge-on-a-narrow-mass)). Where an
outline runs off the canvas the inset is dropped, because **a mass that meets the frame
should run off it**: draw it past the edge and let it.

The default, `edge="ragged"`, is right for everything else: a mass sitting behind other
things wants the brush to break past its boundary, because the mass in front will cover
it.

**`overhang` is not the remedy for a spill, because it moves the ends of each pass and
not its sides** — and *the ends* turn with `direction`: swept vertically, the same
number runs a mass down off its foot onto whatever it stands on. For two masses at the
same depth, inset by half the brush (*`block_in`* in
[`CALIBRATION.md`](CALIBRATION.md#block_in)).

**On a shape that is not convex, `inset()` takes far more than a rim, and it takes it
out of the thin parts first.** Erosion pulls in from every boundary at once, so a lobe
narrower than twice the inset disappears entirely while the body of the mass barely
changes. **So preview the inset shape, not the shape.**

```python
mass = polygon([(0.30, 0.30), (0.70, 0.30), (0.70, 0.44), (0.44, 0.44),
                (0.44, 0.62), (0.70, 0.62), (0.70, 0.78), (0.30, 0.78)])
s.preview(mass.inset(0.045))                # what you are about to fill, not what you drew
```

And **do not cross a small shaped mass**: the crossing is for masses several brushes
across, and on a small one the two pass directions serrate its own boundary.

**When what you have is one boundary** — the edge that matters — give it to `sweep` and
let the passes follow it:

```python
edge = [(0.06, 0.68), (0.31, 0.48), (0.56, 0.63), (0.84, 0.45)]   # read off the grid
s.sweep(edge, "bristle", "dark", into="down", depth=0.30, size=0.12, cross=25)
```

`sweep` runs its first pass along the edge and steps each one after it a part-brush
further into the mass. Passes that run *along* the edge describe the form; columns that
hang *down* from it comb the mass into strands. `into=` is which side the mass is on —
a compass word or an angle steps every pass the same way, and an `(x, y)` point
*inside* the mass makes the passes follow a curved edge instead of shearing off it; a
boundary that closes on itself needs neither, and a shape is such a boundary. `cross=`
is a second set of passes leaning that many degrees across the first — **take it**, at
twenty to thirty degrees, because one sweep on its own comes out stringy; a shaped
`block_in` has the same problem and the same answer, `direction=("axis", 90)`. `depth=`
is how far into the mass to go, and the brush decides how many passes unless you say
`passes=`.

**Which one?** Fill a shape when you can see the whole silhouette and want it covered;
sweep when one edge is the thing you care about, or when the passes following the form
is the point. If the mass is close enough to a box that either feels like overkill,
`block_in` at the angle the mass runs at is the cheaper version of the same idea.

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
s.look(region=cell("D4"), reference="ref.jpg", grid="fine")   # both panels, tenths
s.look(sketch=False)                      # hide the pencil underdrawing
```

A `region=` crop is at full resolution, and a small one is enlarged so that a single
cell fills the panel. `region=span("D2", "E4")` is the usual size for inspecting a
passage, a single cell the size for a feature. Regions can be written as strings
anywhere: `region="D4"`, `region="C3:F6"`, `region="upper-band"`.

Each look writes a numbered PNG under `out/` and returns the path; rehearsals have
their own run of numbers, so a pass can be tried three ways and the three put side by
side. The numbering belongs to the session, so **give each painting its own
directory**, or a second painting silently overwrites the first's whole record of
itself. Use `values=True` far more often than feels necessary, and `diff=True` after a
pass to confirm you changed what you meant to and nothing else. When a mark seems to
have gone missing, `s.log()` says how much paint each one laid and prints `NO PAINT
LANDED` for one that changed nothing — usually an opacity of zero, or a glaze into
paint that is still wet.

---

## The rest of the API

What each call *is*, in the order you reach for them. What each argument means, its
unit and its default is one page in [`REFERENCE.md`](REFERENCE.md).

```python
s.stroke(points, brush, color, pressure="taper", size=None, opacity=None, note="")
s.dab(x, y, brush, color, size=..., press=1)       # one mark; press stamps it again
s.block_in(place, brush, color, direction=, density=, overhang=, edge=, solid=)  # a mass
s.sweep(edge, brush, color, into=, depth=, cross=, passes=)         # a mass with a shape
s.scumble(band, color_a, color_b, n=8)             # a soft passage, as n strokes
s.scumble(patch, a, b, n, direction="inward")      # ...falling off from its middle
s.cover(place, color)                              # bury a mistake; the whole recipe
s.smudge(edge, size=0.02)                          # move paint along a boundary:
                                                   # points, or a shape's own outline
s.glaze(points, color, opacity=)                   # thin transparent film
s.dry(amount=1.0, region=None)
s.undo(n)                                          # scraping, not free
s.look(...)
s.report(since=None, subject_share=None)           # the post-pass check, off the log

s.pencil(points, pressure=0.55)                    # graphite; not a stroke
s.erase(region=None)                               # rub the drawing out
s.sketch_lines()                                   # every line drawn, as points
s.mark(name, x, y)   s.pt(name)   s.unmark(name)   # named landmarks
s.preview(strokes, reference=, region=, grid=)     # where a mark would go
s.rehearse(strokes, reference=, region=)           # what it would look like
s.cost(strokes)                                    # what it would charge
s.cost_line(strokes)                               # ...and why it charges it
s.paint(plan)                                      # ...and now paint that same plan
s.scratch()                                        # a throwaway copy to try a pass on
s.compare(reference, region=None)                  # per-cell value numbers
s.compare({place: value, ...})                     # ...or against your own value plan
s.prepare(reference, level="coarse")               # the reference, cut up
s.look_areas()                                     # the map again, after merging
s.export("painting.png")
s.timelapse_gif("painting.gif", fps=8.0, every=1, scale=None)
s.contact_sheet("sheet.png", columns=6)            # the time-lapse as a grid
s.log(last=10)                                     # last=10_000 for the whole record
s.spent  s.remaining  s.budget_line()              # if the session carries a budget
```

`block_in` and `sweep` space their passes a part-brush apart, which assumes a pass is
one brush wide all along — true of `flat`, `bristle` and `knife`, and not of a round
tip under a varying pressure. Lay masses with `flat` or `bristle`; if you want a round
tip for one, give it `pressure="even"` or it will show its passes at their ends.

**What counts against the budget:** `stroke`, `dab`, `block_in`, `sweep`, `scumble` and
`cover` per pass, and also **`smudge` and `glaze`**. What is free: `pencil`, `erase`,
`mark`, `look`, `preview`, `rehearse`, `cost` and `compare`. Do not discover the first
list with three strokes left.

**After every pass, `easel run` prints a check**, and `s.report(since=n)` is the same
lines in Python: the guide's standing warnings read off the log rather than repeated —
one brush at one size for a whole pass, a stack of passes at one angle, a graded
passage laid too narrow, a starved comb, small marks before the masses, a pressure list
on a chisel, and the subject's share so far. The rules and their thresholds are listed
under `report()` in [`REFERENCE.md`](REFERENCE.md#looking-planning-measuring). Every
one of them was once a paragraph in the guide, and a line printed after the pass that
did it is worth more than the paragraph.

---

## Working from a photograph

Everything above holds whether or not you have a reference. This chapter is for a
painter who has been given a photograph to copy: it is the difference between a
likeness and a set of coloured rectangles. Do not start placing strokes from your
impression of the picture — that impression is wrong about position in exactly the way
you are worst at.

**Put the same grid on both, and never take a coordinate out of your head.**

```python
s.look(reference="ref.jpg", grid=True)     # the same A-H / 1-8 cells on each
```

Both panels carry the same labelled cells, so a place you can *see* on the reference
has a name you can *paint* into. Work like this:

1. **Name the big masses by cell, out loud, before painting anything.** "The dark mass
   fills E5 to H8. The light shape is D3 to F3." Four or five of those sentences is a
   drawing.
2. **Paint the masses into those cells** and look again with the grid on. Compare cell
   against cell, not impression against impression.
3. **Correct by cell too.** Errors of placement only show up against the grid, because
   your own painting looks internally consistent.

A mass is rarely one cell. `span("E5", "H8")` is the rectangle from one cell to
another, both included, and the right size of crop for inspecting a passage:

```python
s.block_in(span("E5", "H8"), "bristle", "dark", density=1.0, size=0.14)
s.look(region=span("D2", "E4"))                # one passage, close up
```

### The drawing

A cell is a large place, and a feature is smaller than one. Named by cell alone a
feature lands somewhere in the right neighbourhood, which is how a painting comes out a
recognisable scene made of unrecognisable things. So: six or seven points, each one
verified. That is a drawing, and everything else hangs on it.

```python
s.mark("top_l", 0.335, 0.315)          # a named point, shown on every look after
s.mark("top_r", 0.630, 0.315)
s.mark("base",  0.480, 0.715)
```

Marks are drawn on **both** panels, so one look tells you whether the point you chose
is the point you meant. Check each one at the size of the feature, not the size of the
canvas:

```python
s.look(region=cell("D4"), reference="ref.jpg", grid="fine")
```

`grid="fine"` divides what is on screen into tenths and labels them, and the crop is
enlarged so a single cell fills the panel. **The crop is padded out to the panel's
shape, so you are shown a little more than the span you asked for** — measure off the
`mark()` crosses, whose canvas coordinates you already know, not off the crop's edges.
**Read the two digits off the label; do not estimate a fraction.** A label pair `(3, 6)`
is `cell("D4").point(0.3, 0.6)` — the near corner of that little square — and its
middle is `point(0.35, 0.65)`. Reading a label is something you do reliably.

```python
s.mark("a", *cell("D4").point(0.35, 0.55))     # read off the fine grid
```

Then, once the far masses are down, draw with the pencil through the points:

```python
s.pencil([s.pt("top_l"), (0.36, 0.68), s.pt("base"), (0.60, 0.68), s.pt("top_r")])
s.look(reference="ref.jpg")             # is the drawing right, before any paint?
```

Draw through the shapes, not around them — a line you painted *up to* is an outline
filled in. If a line is wrong, `s.erase(region)` and redraw; arguing with a wrong line
while painting costs strokes and loses every time. The drawing says where the mass is;
it does not say what the marks inside it do. `s.sketch_lines()` gives every line back as
points, so a stroke can be swept along one.

### Compare values, not colours

```python
s.look(reference="ref.jpg", values=True)   # both panels greyscale, same scale
```

Both sides are converted the same way, so the greys are directly comparable. This is
the fastest way to find the error that will otherwise sink the painting: a background
far lighter than the reference's, a light mass that is not actually the lightest, two
masses separate in colour and identical in value. **Get the value map right before you
care about the drawing.** A copy with the right values and a clumsy drawing still reads
as the scene; an exact drawing with flat values reads as nothing.

### Put a number on it — twice

```python
print(s.compare("ref.jpg"))
```

Per cell: the reference's mean value, yours, the difference, and a heat map beside the
two greyscales. Negative means your canvas is *darker* there. **The number that matters
is `0.10`**: a cell further out than that is a separation the painting has lost, and
every one of them is yours to fix. A cell marked `~` asks for a value below anything
the box reaches and is not work; on most references there are none.

Run it **twice**, not continuously:

- **Once on the empty canvas**, before the first stroke. The difference column is
  meaningless but the reference column is the photograph's whole value map in numbers:
  its lightest cell, its darkest, and where every mass sits between. Your eye will
  guess the range of a dim photograph two stops too light; this will not.
- **Once after the block-in**, before any feature. If the three masses are within
  `0.10` the structure is right; if a mass is out, fix the *mass* — a bigger brush, not
  a smaller one — and fix it *now*, before the near things go on, because a mass
  repainted later buries every fine mark lying on it.

The mean colour is in the table too, coarse on purpose: it is there to catch "that
whole passage is too warm", not to be sampled and matched. **Matching cell by cell is
tracing**, and it produces a painting nobody would look at twice.

### When to stop measuring

Measuring is not painting, and every tool in this chapter can be used to avoid making
a mark. Stop when the three masses are within `0.10`, the six or seven landmarks are
verified at feature scale, and you can see the subject in your own painting with the
reference covered up. Past that point more measuring makes the painting worse: it turns
marks into corrections and corrections into mud.

**And precision is paid for somewhere else in the picture.** Landmarks buy accuracy
exactly where you point them, out of the budget for everything you did not. The
failure is a well-built feature in a picture that has not come up with it: its mass has
dissolved into the background because silhouette, support and surroundings never got
their own passes. The guide's closing checklist holds the two rules that answer this —
the subject's share as a number, and the last third on the surroundings — and they
collide on a copy that is being scored, because every near mass laid late knocks a
cell back out of tolerance. **Finish the value work early and deliberately**, check
`compare()` comes back clean, and then stop measuring. The last ten strokes may not be
value corrections: a painter that has to spend its last marks on the score has already
lost the picture.

### Letting the reference be cut up for you (optional)

`s.prepare("ref.jpg")` quantises the photograph and hands back its masses, numbered,
with an overlay to look at and a table of each one's share, value, colour, the cells it
covers, and how hard its edge is against each neighbour.

```python
prep = s.prepare("ref.jpg")            # "coarse": five to eight masses
print(prep)
prep.merge(3, 7)                       # both of those are one thing
s.look_areas()                         # the corrected map, over both panels
s.look(region=prep.region(4), reference="ref.jpg", grid="fine")
```

**The map is not the truth.** It joins two things of the same colour into one area and
cuts one thing along its own shading, because it knows about colours and a painting is
made of things; `merge` and `split` are how you say so. `s.sketch()` lays those outlines
as pencil in one call, and `s.ref_shape(n)` hands one back as a shape. **Both are
assisted modes**, and so is handing `s.ref_outline(n)` straight to `sweep()`: the
boundary of a mass is a drawing, and if the machine found it, say so — the log records
`sketch()` and `ref_shape(n)` for you, and where you copied points out by hand nothing
can. Prefer `prepare` for *reading* the reference: look at the area, then lay your own
outline over it.
