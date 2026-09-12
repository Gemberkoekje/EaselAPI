# The reasons: colour, paint, brushes, and working from a reference

This is the second half of [`PAINTER.md`](PAINTER.md), which is the guide and the file
to read first. That one is the method: the order of work, the mistakes, the exercises
and the checklist — everything you need in your head while you are painting. This one
is the same rules with their reasons, the failures behind them and the numbers, plus
the parts of the API you reach for rather than hold.

**Read it once, after the eight exercises and before the painting.** You are not meant
to hold it in your head. You are meant to have read it, so that when the guide says a
mass wants a shape rather than a box you already know what a box costs.

Nothing here is cut from anywhere. Two other files sit beside these:
[`RECIPES.md`](RECIPES.md) is the procedures — how a thing that is made of planes gets
painted, what a glow is laid as — and [`REFERENCE.md`](REFERENCE.md) is every fact on
one page, with [`CALIBRATION.md`](CALIBRATION.md) holding the measured numbers.

---

## Working from a reference

If you have been given a photograph to copy, this section is the difference
between a likeness and a set of coloured rectangles. Do not start placing strokes
from your impression of the picture — that impression is wrong about position in
exactly the way you are worst at.

**Put the same grid on both, and never take a coordinate out of your head.**

```python
s.look(reference="ref.jpg", grid=True)     # the same A-H / 1-8 cells on each
```

Both panels carry the same labelled cells, so a place you can *see* on the
reference has a name you can *paint* into. That is the whole trick. Work like this:

1. **Name the big masses by cell, out loud, before painting anything.** "The dark
   mass fills E5 to H8. The light shape is D3 to F3. The lit plane is G1 to H2."
   Four or five of those sentences is a drawing.
2. **Paint the masses into those cells** and look again with the grid on. Compare
   cell against cell, not impression against impression: *my* light shape is D3–D4
   but on the reference it runs D3–D5, so it is half a cell too high and too short.
3. **Correct by cell too.** Errors of placement are the ones you cannot see by
   looking at your own painting alone, because it looks internally consistent. They
   only show up against the grid.

A mass is rarely one cell. `span("E5", "H8")` is the rectangle from one cell to
another, both included, so what you said out loud is what you block in — and it is
the right size of crop for inspecting a passage:

```python
s.block_in(span("E5", "H8"), "bristle", "dark", density=1.0, size=0.14)
s.look(region=span("D2", "E4"))                # one passage, close up
```

### The drawing

A cell is a large place, and a feature is smaller than one. Named by cell alone a
feature lands somewhere in the right neighbourhood, which is how a painting comes
out a recognisable scene made of unrecognisable things.

The order, in one sentence: **landmarks before anything, pencil after the far
masses are down, near masses on top.** Landmarks are points, and paint cannot bury
them. The pencil can be buried, so it goes on over the far masses and under the
near ones — that is what back to front buys you here.

So: six or seven points, each one verified. That is a drawing, and everything else
hangs on it.

```python
s.mark("top_l", 0.335, 0.315)          # a named point, shown on every look after
s.mark("top_r", 0.630, 0.315)
s.mark("base",  0.480, 0.715)
```

Marks are drawn on **both** panels, so one look tells you whether the point you
chose is the point you meant. Check each one at the size of the feature, not at the
size of the canvas:

```python
s.look(region=cell("D4"), reference="ref.jpg", grid="fine")
```

`grid="fine"` divides what is on screen into tenths and labels them, and the crop is
enlarged so a single cell fills the panel. **The crop is also padded out to the
panel's shape, so you are shown a little more than the span you asked for** — do not
do pixel arithmetic off its edges. Measure off the `mark()` crosses instead, which are
drawn on both panels and whose canvas coordinates you already know. **Read the two digits off the label; do
not estimate a fraction.** A label pair `(3, 6)` is `cell("D4").point(0.3, 0.6)` —
the near corner of that little square — and its middle is `point(0.35, 0.65)`.
Reading a label is something you do reliably. Estimating "about a third across" is
not, and that gap is the whole reason this view exists.

```python
s.mark("a", *cell("D4").point(0.35, 0.55))     # read off the fine grid
```

Then, once the far masses are down, draw with the pencil through the points:

```python
s.pencil([s.pt("top_l"), (0.36, 0.68), s.pt("base"), (0.60, 0.68), s.pt("top_r")])
s.look(reference="ref.jpg")             # is the drawing right, before any paint?
```

`pencil()` puts graphite into the canvas — no paint, no wetness, and **it does not
count as a stroke**, so the drawing is free. Paint covers it in proportion to how
much actually lands, so it survives thin paint and disappears under solid paint.
Making it disappear is the painting. **Thin means `opacity`, not `density`** — a
`block_in` at low density is the same full-strength paint with the passes spaced
out, and it takes a drawing off completely.

Four things about drawing that are easy to get wrong:

- **Draw through the shapes, not around them.** A line you painted *up to* is an
  outline filled in, and that is the clearest possible sign nobody was looking at
  masses. Paint across your own lines.
- **Erase rather than argue.** If a line is wrong, `s.erase(region)` and redraw.
  Arguing with a wrong line while painting costs strokes and loses every time.
- **The drawing says where the mass is. It does not say what the marks inside it
  do.** A mass drawn along a line still gets painted in every direction the form
  asks for.
- **Fix the drawing before you paint it.** A look at the pencil alone is the
  cheapest correction available to you — it costs nothing and no paint has been
  spent yet.

`s.sketch_lines()` gives every line back as points, so a stroke can be swept along
one, aimed at one, or ignore it.

### Try the mark before you spend it

Three tools sit between deciding on a mark and paying for it. They answer the three
questions you have about a mark you have not made yet — *where does it go*, *what
will it look like*, and *what does it cost*. None of them touches the canvas, none
writes to the log, and all three take the same plan.

```python
plan = [{"points": [s.pt("top_l"), (0.40, 0.62)], "brush": "liner",
         "size": 0.006, "color": "light", "label": "edge"}]

s.preview(plan,  reference="ref.jpg", region=span("C3", "F6"), grid="fine")
s.rehearse(plan, reference="ref.jpg", region=span("C3", "F6"))
s.cost(plan)                                   # 1
```

`preview` draws your intended points and the brush's *width* over both panels — at a
default width if you gave it bare points rather than a plan, which is fine for checking
placement and useless for checking an edge —
where the mark will go, checked against the photograph. `rehearse` paints it on a
copy of the canvas and shows you the result — what it will look like, with its
tooth and its edge and how it mixes with what is already there. A feature smaller
than a cell can be tried three ways and judged before a stroke is spent.

`cost` returns the number of strokes the plan would charge. For a mark that is 1 and
you did not need to ask. **For a mass it is the number you cannot work out by hand,
and getting it wrong is expensive**: a mass is priced on the extent of its box along
the direction the passes stack, *and* on how many times a pass line crosses it. Both
factors run against you on exactly the shapes worth painting.

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
out is ten times the band's own width, and because a pass line crosses a curve twice.
That is not a defect to route around — it is what the mass costs, and the picture it
makes is the better one. It is a number to *know* before you spend a quarter of your
budget on it. A painter who did not know it budgeted 4 and paid 21.

If the number is more than you want to pay, a wider brush or a thinner `density` is
the lever, and `cost` will tell you what either buys before you commit to it.

**And `cost_line` says *why* the number is what it is**, which is the difference
between fixing the call and redesigning the mass. There are only three answers — the
passes crossed a second direction, they stepped across a bounding box much bigger than
the mass, or a concave outline cut each one into pieces — and each names its own lever:

```python
print(s.cost_line({"shape": bent, "size": 0.015}))
# 75 strokes -- 25% of the 300 left of a 300-stroke budget
#   75  42 passes stepping across 0.34 of the canvas, each cut into 1.8 pieces by the outline
```

The same sentence rides on the budget warning, so a plan that would eat what is left
says what it is spending it on.

**And there is a fourth verb, which paints the plan you just checked.**

```python
s.paint(plan)
```

That is the whole point of the plan being one object: `cost`, `preview`, `rehearse`
and `paint` all read it, so no line of it is written twice. A plan that is checked
and then *retyped* into the call that paints it is a plan that will drift, and the
drift arrives as paint. Marks, masses and sweeps may be mixed in one list and are
painted in the order given:

```python
s.paint([{"shape": blob(cell("D5"), 0.12, seed=3), "brush": "bristle",
          "color": "dark", "size": 0.07},
         {"points": [(0.31, 0.62), (0.55, 0.58)], "brush": "liner", "size": 0.005}])
```

The rehearsal is seeded as if these were the next strokes of the real painting, so
what you rehearsed is what lands — rehearse a plan, paint that same plan with nothing
in between, and it arrives pixel for pixel as it was rehearsed. This is what the scrap
of canvas beside a real easel is for, and it is the last reason to reach for `undo`.

**Rehearse everything.** The tools above are written around a mark smaller than a cell,
because that is where a painter expects to need them. The expensive mistakes are the
other way up: a `block_in` of a big mass is one call and twenty strokes, and it is
cheap to repaint only until something else stands on it.

The rule here used to be *rehearse any block-in you will not want to repaint*, and it
was too weak. It asks you to sort your passes into the ones that will go wrong and the
ones that will not, which is a prediction, and predicting the picture is the thing this
whole engine is built around your being unable to do. The numbers say so plainly:
**eighteen rehearsals in one painting, every one of which changed something, none of
which was charged, and not one stroke of that painting spent on repainting anything.**
Another painter rehearsed and threw away 38 marks across two sittings, at a cost of
nothing. The painter who rehearsed no masses at all spent about 60 of its 224 strokes
repainting five of them.

So: **every pass gets a rehearsal, and it costs a look.** From the shell that is a
flag, `easel run pass.py --rehearse`; in Python it is `s.scratch()`, the same throwaway
copy. Several scripts rehearse together onto one copy, which is how a pass that lands
on top of another pass gets judged on it rather than on bare ground.

### Compare values, not colours

```python
s.look(reference="ref.jpg", values=True)   # both panels greyscale, same scale
```

**A cool mass on a warm ground reads about two steps lighter than it measures**, so this
is also the tool for the commonest false alarm there is: a painter concluded three times
that its subject was far too light and `compare()` said it was inside `0.05` every time.
Believe the number.

Both sides are converted the same way, so the greys are directly comparable. This
is the fastest way to find the error that will otherwise sink the painting: a
background far lighter than the reference's, a light mass that is not actually the
lightest thing, two masses that are separate in colour and identical in value.

**Get the value map right before you care about the drawing.** A copy with the
right values and a clumsy drawing still reads as the scene. A copy with an exact
drawing and flat values reads as nothing.

### Put a number on it — twice

Squinting says something is off. It does not say which mass or by how much.

```python
print(s.compare("ref.jpg"))
```

Per cell: the reference's mean value, yours, the difference, and a heat map beside
the two greyscales. Negative means your canvas is *darker* there. Narrowed to one
place with `region=`, the per-cell detail lines beneath the table are `col,row` — the
transpose of the table above them, so read the header before you trust a pair. **The number that
matters is `0.10`**: a cell further out than that is a separation the painting has
lost. Every one of them is yours to fix. A cell marked `~` asks for a value below
anything the box reaches (see step 3 of [`PAINTER.md`](PAINTER.md)) and is not work — on most references there
will be none, and if a photograph does hold one or two, they are its deepest
shadows and nothing else.

Run it **twice**, not continuously:

- **Once on the empty canvas**, before the first stroke. The difference column is
  meaningless but the reference column is the photograph's whole value map, in
  numbers: its lightest cell, its darkest, and where every mass sits between. That
  is what you plan the three values from. Your eye will guess the range of a dim
  photograph two stops too light; this will not.
- **Once after the block-in**, before any feature. If the three masses are within
  `0.10`, the structure is right; if a mass is out, fix the *mass* — a bigger brush,
  not a smaller one.

**Before you repaint a mass, look at what is standing on it.** This is where step 2's
rule in [`PAINTER.md`](PAINTER.md) actually bites, and a number you have just measured is the most convincing
possible reason to ignore it: a mass repainted at block-in size buries every fine mark
lying on it, and those are the expensive ones, while what you are fixing is a tenth of
a value. Cheapest first: repaint it *before* the near things go on, which is what the
two-`compare()` rhythm is for. After that it is a repair, and *When something is wrong,
paint over it* in [`PAINTER.md`](PAINTER.md) has the method. Look at the picture afterwards, not just the number:
`compare()` will happily report the cell improved while the mark you buried was the
reason the painting read.

The mean colour is in the table too, coarse on purpose: it is there to catch "that
whole passage is too warm", not to be sampled and matched. **Matching cell by cell
is tracing**, and it produces a painting nobody would look at twice. If you find
yourself working down the table one cell at a time, you have stopped painting.

### Painting without a reference

Half the tooling above assumes a photograph. If you are painting something you can
only see in your head, everything here still applies except that *you* are the
reference — so write the value plan down in numbers before a stroke, and measure
against that instead:

```python
upper, lower = span("A1", "H4"), span("A5", "H8")
s.compare({upper: 0.72, lower: 0.38})       # the same table, the same sheet
```

The keys are places and the values are what `value_of` reports, so a plan is a few
lines written before you start and checkable after every mass. The sheet shows the
plan, the canvas, and each planned place outlined with its miss written across it.
Give a place a name to see it listed under one: `blob(cell("D5"), name="near_mass")`.

The rest of the method is the same discipline without the crutch:

- **Draw first anyway.** The pencil is free and does not count against the budget, and
  with nothing to check a drawing *against* it is still the cheapest place to find out
  that the proportions in your head do not fit the canvas — which is a thing you can
  see the moment it is down. → *The drawing*
- `print(p.value_of(mix))` for every mixture as you make it, and for the ground.
- `p.at_value(base, target)` to *hit* a planned value rather than guess at it.
- `look(values=True)` after every mass, read against the numbers you wrote down.

**Re-read the plan's places whenever you move a silhouette.** A plan written before the
first stroke names its places against masses that did not exist yet, and a place is
just a rectangle: raise a boundary, make it jagger, push a mass across, and the place
that used to sit on one thing now straddles two. `compare()` cannot know that, and it
will report the average of the two as a miss in a confident voice. A painter got a
`-0.16` on a place that had quietly become half one mass and half another, and there
was nothing wrong with the painting. **When a silhouette moves, the plan's places move
with it** — look at the sheet's outlines, not only at its numbers, because the sheet
draws every place on the canvas for exactly this reason.

The failure this prevents is the one a reference makes impossible: a value plan that
lives only in the painter's head drifts a step per mass, and by the fourth mass the
picture has no value structure at all — and nothing said so.

### When to stop measuring

Measuring is not painting, and every tool in this section can be used to avoid
making a mark. Stop when:

- **the three masses are within `0.10`** — value is what carries a copy;
- **the landmarks are verified** — six or seven, checked at feature scale. A dozen
  is not twice as good; it is a session spent on arithmetic;
- **you can see the subject in your own painting with the reference covered up.**

Past that point, more measuring makes the painting worse, not better: it turns
marks into corrections and corrections into mud. The grid gets the masses into the
right cells and the landmarks get the features into the right places. Neither will
paint a feature for you.

**And precision is paid for somewhere else in the picture.** Landmarks buy accuracy
exactly where you point them, out of the budget for everything you did not. The
failure: the part you measured is built, and the mass it belongs to has dissolved into
the background — silhouette, support and surroundings never got their own passes. A
small mass sitting *on* a bigger one instead of *in* it is the closing checklist's
question at
feature scale; **it happens at picture scale too, and there it is far harder to see,
because everything you have been looking at looks right.**

So **spend the last third of your strokes on what is around the thing you measured.**
A well-built feature in an unfinished picture reads as a detail come loose; a rough one
in a picture that holds together reads as the thing itself. A viewer recognises a
subject from its mass and its placement long before they can see a feature at all.

**Decide what share of the budget the subject gets before your first stroke, and spend
everything else out of what is left.** There is arithmetic here for what a *mass*
costs — `extent / step`, below — and none at all for what a *picture* costs, and the
gap is expensive in exactly one direction. The guide warns you about spending too much
on detail; the commoner failure is quieter. A painter working to 300 spent **59% of
them before it began the subject at all**, reached the thing the picture was about with
41% left, and its own verdict was that the part it came for is the weakest passage in
the finished painting. Nothing told it that was happening, because every one of those
marks was a reasonable mark.

Write the split down. Something is the picture and everything else is what it stands
in, and the second is not entitled to half.

**This is also the rule that has to carry a busy picture.** Depth order scales to any
number of masses without changing; attention does not. Everything else here assumes one
subject against a ground, and once several things could plausibly be the subject the
checklist's question — *is the thing you measured most carefully still attached to the
picture?* — has a harder version: **is the thing you measured most carefully still the
thing the picture is about?**

**And when the two closing rules collide, this is the order.** *Spend the last third on
the surroundings* and *your last marks should be about the picture* pull against each
other on a copy that is being scored, because every near mass you lay late knocks a cell
back out of tolerance. **Finish the value work early and deliberately** — check
`compare()` comes back clean, and then stop measuring. The last third is then free for
the surroundings, and the last few marks for the picture: an accent, an incident, an
edge thrown away on purpose. A painter that has to spend its last marks on the score has
already lost the picture.

**That settles the order and not the arithmetic, so here is the arithmetic.** If the
last third goes on the surroundings, the subject's share *has* to end lower than it was
when the subject was finished — so the share is compared against the plan **at the
moment the subject is done**, and after that it is expected to fall. Checked at the end
instead, a painter who followed the last-third rule correctly is told by the checklist
that they are not finished, which is the fastest way to teach somebody to stop reading
a checklist.

### Letting the reference be cut up for you (optional)

`s.prepare("ref.jpg")` quantises the photograph and hands back its masses,
numbered, with an overlay to look at and a table of each one's share, value,
colour, the cells it covers, and how hard its edge is against each neighbour.

```python
prep = s.prepare("ref.jpg")            # "coarse": five to eight masses
print(prep)
prep.merge(3, 7)                       # both of those are one thing
s.look_areas()                         # the corrected map, over both panels
s.look(region=prep.region(4), reference="ref.jpg", grid="fine")
```

**The map is not the truth.** It joins two things of the same colour into one area
and cuts one thing along its own shading, because it knows about colours and a
painting is made of things. `merge` and `split` are how you say so.

`s.sketch()` lays those outlines as pencil in one call, and `s.ref_shape(n)` hands
one back as a shape. **Both are assisted modes**, and so is handing
`s.ref_outline(n)` straight to `sweep()`: the boundary of a mass is a drawing, and
if the machine found it, say so. The drawing is meant to be yours, and any write-up
has to say one was used — where you went through `sketch()` or `ref_shape(n)` the
painting records it for you (`s.log()` prints it, and it is in the saved session),
and where you copied the points out by hand nothing can, so it is on you.

Prefer `prepare` for *reading* the reference: look at the area, then lay your own
outline over it — `hull` on three or four verified landmarks, a `blob` sized to the
cells the table says it covers, or an edge you read off the grid and `sweep`.


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
keep a painting coherent — the same three or four mixtures repeated across a canvas
is most of what "colour harmony" actually means.

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
| `value_of(c)` | How light it reads, `0.0`–`1.0`. Useful for planning values. |
| `hex(c)` | The sRGB hex, for your own notes. |

**Supplying a colour of your own.** A slot takes a hex string, or an `(r, g, b)` triple
of `0.0`–`1.0` **read as sRGB, exactly as the hex string is**. What you supply lands as
written — including a black, and including anything below the darkest mixture the box
can reach:

```python
s.palette["ink"] = "#0d0c10"           # hex string
s.palette["ink"] = (0.05, 0.05, 0.07)  # sRGB, 0.0-1.0 — the same as "#0d0d12"
```

**The triple is the trap, and it catches you in exactly one place: matching a colour
that is already on the canvas.** The engine's own colours are *linear* arrays, so one
read off the canvas and handed back as a tuple is re-read as sRGB and comes back much
darker — a `toned_grey` ground reads `0.53`, and its own mean passed back as a triple
reads `0.25`. Do not convert it. Ask for it, and pass what you are given straight on:

```python
s.palette["already_there"] = s.sample(cell("D5"))   # the engine's own array
s.palette["matched"] = s.sample()                   # the whole canvas, averaged
```

`s.sample(place)` returns a `float32` array, which every colour argument takes
untouched, and it averages over a shape rather than over the shape's box. It samples
the **paint**, not the view of it: the relief shading `look()` draws is light falling
on the surface, not pigment in it. That is what to reach for when a mark has to meet
what is already there — a halo's outer ring, a repair, the far side of a lost edge.

`s.sample(place, rendered=True)` is the other one — the surface `look()` and `export()`
draw, relief and unburied graphite and all — so the question *is my mass darker than it
looks?* is one line rather than a belief:

```python
s.palette.value_of(s.sample(mass))                  # the paint
s.palette.value_of(s.sample(mass, rendered=True))   # the view of it
```

**The answer is normally that they agree.** Measured over a mass they are the same to
`0.001` at every load and every value tried, because the relief is a gradient: it lifts
one side of each ridge of paint and drops the other by as much. `compare()` measures
the paint too, and says so in its own table. A mass that looks lighter than the number
you mixed it at is telling you about the value it stands against, not about the view —
the numbers are in [`CALIBRATION.md`](CALIBRATION.md) under *The paint and the view of
it*.

**A list of 0–255 integers is not one of the forms**, and it does not raise — it
clamps, so `[13, 12, 16]` gives you white. If you supply a colour, print
`value_of()` on it before you paint a field of it.

Reach for this when a reference genuinely goes below the palette's floor (step 3 of
[`PAINTER.md`](PAINTER.md)), and not otherwise: the box has no black because mixed darks are alive, and a slot
full of tube black is the fastest way to a dead painting. Most dark references do not
need it — see the floor arithmetic in step 3 of [`PAINTER.md`](PAINTER.md).

Three things about the mixing that will surprise you:

- **Blue and yellow make green**, red and blue make violet, and complements make
  lively greys. This is subtractive pigment mixing, not RGB averaging.
- **White is a weaker lightener than you expect.** If you want a really pale colour,
  use more white than feels right.
- **A yellow and a blue make green even when you were after a grey**, and tinting
  does not undo it. Neutral greys come from complements, or from earth and white,
  or from `desaturate`. Print `hex()` of a mixture before you paint a field of it.

---

## Wet paint

Paint lands wet and stays wet for a while. Paint that lands on wet paint **mixes**
with it instead of covering it.

This is the single most common surprise. Lay yellow over still-wet blue and you get
green, not yellow. That is not a bug — it is how paint works, and used deliberately
it is how you get soft transitions for free.

```python
# Blend on purpose: work into wet paint.
s.block_in(cell("C3"), "bristle", "cerulean", density=1.0)
s.stroke([(0.3, 0.3), (0.5, 0.35)], "bristle", "titanium_white")   # blends in

# Or cover cleanly: dry first.
s.dry()                                                    # whole canvas
s.dry(0.5, region="upper-half")                            # partial, one region
s.stroke([(0.3, 0.3), (0.5, 0.35)], "bristle", "titanium_white")   # sits on top
```

**Rule of thumb: if you want the new colour to read as itself, `dry()` first.**

**Wet is a matter of a few strokes, not a whole pass.** Wetness fades with every
mark you make anywhere on the canvas, and one `block_in` is many marks — so by the
time you have blocked in a second mass, the first is already most of the way dry.
If you actually want two colours to mix on the canvas, put the second one down
within a few strokes of the first.

A `glaze` is the opposite move — a thin transparent film over dry paint that shifts
the colour underneath without hiding it:

```python
s.glaze([(0.2, 0.6), (0.8, 0.6)], "alizarin", opacity=0.15)
```

**A glaze is strong in proportion to its *distance* from what it lands on, and that is
true of hue as well as value** — the same rule the `knife` carries, arriving by another
route. The knob you have is `opacity`, and it is the wrong knob to reach for first: the
film either announces itself or is not there, with very little between. Measured, a
warm light glaze over a cool dark mass, `flat` at `size=0.18` on a 512×384 canvas:

| `opacity` | what it does to the value under it | and to the hue |
|---|---|---|
| `0.05` | `+0.028` | already neutral — the cool is gone and nothing warm has arrived |
| `0.10` | `+0.061` | warm |
| `0.14` | `+0.087` | a stripe of a different colour |
| `0.20` | `+0.123` | a different mass |

At `0.14` the film has moved the value by nearly the whole `0.10` that separates two
masses, so what was meant to tint a passage has instead made a new one; at `0.05` the
underlying hue is already dead and the glaze's own is not yet visible. **So mix the
glaze close to what it lands on, in value and in hue, and then choose an opacity** —
a glaze far away in hue has no usable opacity at all. A painter spent two rehearsals
discovering that from the other end and dropped the mark.

---

## The brushes

One line each. Reach for `bristle` for marks that have a direction and `flat` for
quiet masses.

| Brush | What it is for |
|---|---|
| `bristle` | **The workhorse** for any mark with a direction. Broken, streaky, alive — and never solid. |
| `flat` | Block-in, chisel edges, flat planes. Turns to follow the stroke. |
| `round_hard` | Deliberate marks, accents, small shapes, final highlights. |
| `liner` | Fine lines at the scale of a feature. `round_hard` at `size=0.005` with no jitter at all, and it holds its load. |
| `round_soft` | Blending and soft edges. The least painterly — use it sparingly, and never for a mass: above about `size=0.05` it airbrushes. |
| `knife` | Thick slabs with a hard edge. Drags what it crosses. Use rarely, for punctuation, and keep it close in value to what it lands on or it reads as something stuck to the surface. |
| `smudge` | Carries no paint; moves what is already there. For losing edges. |

**A `bristle` stroke is never solid** — it lays a comb of streaks, which is what makes
it alive on a mark whose direction you mean. Lay a big quiet mass with `flat`, or with
bristle passes that *cross*; single parallel passes rib it. Below about `size=0.02` a
bristle is four streaks with gaps, not a brush: small solid planes want `flat` at
`pressure="even"`, or `round_hard`.

**A short `flat` or `knife` stroke is a rectangle.** The oriented tips hold a chisel
square to their travel — right for a mass, wrong for an accent, and they do not taper
under a pressure list. **Small accents want `round_hard`. `flat` and `knife` want a
length.**

### The shape each tool leaves behind

That last rule is the most useful sentence in this guide, and it is one of a family.
**Every tool here has a geometry of its own, and if you do not decide the shape, the
tool decides it for you** — then you spend twenty marks fighting a structure you never
chose. What each one leaves when you are not watching:

| Reach for | and if you are not watching, you get |
|---|---|
| `flat` / `knife`, short | a rectangle with chisel ends |
| `round_hard`, short | a capsule. It needs to be about **7×** longer than it is wide before it stops reading as one |
| `round_hard` or `liner`, several small marks | **one disc, printed over and over.** A round tip draws the same silhouette every time, so five small marks are five copies — unless you give the tip an outline of its own with `tip_wobble=0.7`, which redraws it per mark |
| `bristle` below `size≈0.025` | a comb: a woven strap across a band, or a ladder of evenly spaced ticks along an edge |
| `sweep` round a closed shape | **concentric rings**, because the passes step inward from the boundary |
| several overlapping `blob`s | a dome — blobs of similar size average to a circle and the irregularities cancel |
| a shallow shape, passes along its long axis | **its bounding box** |
| any loop or generator you write | its own statistical signature: one density, one mark length, no clumps and no holes |
| repair laid on repair, always additive | horizontal strata, one visible edge per repaint |

Two of those need more than a row.

**The shallow-shape one is not covered by the brush-width rule.** An ellipse
`0.256 × 0.128` filled with a `flat` at `0.022` — a twelfth of the mass's width, well
inside the "keep the brush under about a fifth" rule below — came out a rectangle.
**The dimension that matters is the mass's extent *perpendicular to the passes*, not
its width.** Run the passes across the short way, or turn them:

```python
s.block_in(ellipse(span("D4", "F5")), "flat", "mid", direction=90, size=0.022)
```

**And a mass much longer than it is wide is a stroke, not a mass.** `block_in` will
comb a `0.022 × 0.18` band even at `density=1.0` with `direction="axis"`. A long
`stroke()` is the right tool; `block_in` is for something with two dimensions.

Size is a fraction of the canvas's long side. `0.2` is a big brush, `0.02` a small one.
**On a canvas that is not square that is not the same unit as a coordinate**: `size` is a
fraction of the long side while `y` is normalised over the short one, so a brush hangs
over a shape by a different amount vertically than horizontally. It is the reason a
mass you placed by number comes back a little taller than you drew it.
**Use a bigger brush than feels comfortable**, especially early — but that is advice
about *masses*. **Scale a mark off the thing it describes, not off the canvas**;
carrying the big brush down to something small costs a repaint. The numbers are in
`CALIBRATION.md`.

### The angle of the mark

**Do not let the canvas choose your stroke direction.** This is the loudest tell in
every painting made with this engine so far, and it is the easiest to fix. Left
alone, everything here runs horizontally or vertically: `block_in`'s named
directions are horizontal, vertical and a 45° diagonal; every named region is an
axis-aligned rectangle; and an oriented tip is held square to its travel, so a
horizontal stroke necessarily ends on a vertical edge. Paint a sloping mass with
horizontal passes and you get a stack of bars with flat ends.

**Sweep a mass along its own axis.** `block_in` takes a number of degrees, clockwise
from horizontal, as well as the four names:

```python
s.block_in(span("A4", "F7"), "flat", "shadow", direction=28, size=0.12)
s.block_in(span("A4", "F7"), "flat", "shadow", direction=(28, 118), size=0.12)  # crossed
s.block_in(ribbon([(0.2, 0.8), (0.8, 0.4)], 0.2), "flat", "shadow", direction="axis")
```

`direction="axis"` is the mass answering the question itself: it sweeps along the
long axis of the shape (or of the rectangle) you gave it, so you do not have to work
the angle out.

Passes that run along the form cover it in fewer strokes than passes that step
down it, and they come out visibly less square. Measured, if you want the numbers,
in `CALIBRATION.md`.

**Turn the blade.** Any oriented tip can be pinned instead of following its travel:

```python
s.stroke(path, "knife", "light", size=0.09, angle_follow=False, angle=45)
```

At 45° the knife lays a parallelogram; at 90° it is edge-on and draws a ribbon
instead of a slab. This matters most at the *ends* of marks and on short ones — on a
long sweep the path direction does nearly all the work, so fix the path first and
reach for the angle for a mark whose termination you can see.

**A round tip is the tip that declares no axis.** `round_hard` has no orientation at
all, so it cannot print the canvas's grain into a mass however you drive it. When a
passage keeps coming out square and you have already fixed the direction, that is
the brush to change to — not `round_soft`, which airbrushes at any size a mass needs.

### Per-stroke overrides

Anything about a brush can be overridden per stroke — and per **mass**: `block_in`
and `sweep` take the same keywords and pass them down to every stroke they emit.

```python
s.stroke(path, "bristle", "shadow", size=0.14, opacity=0.5)
s.stroke(path, "flat", "light", hardness=0.9, jitter=0.05, load=0.4)
s.stroke(path, "bristle", "shadow", size=0.12, load_falloff=0.25)   # runs dry slower
s.block_in(cell("D5"), "flat", "shadow", opacity=0.5, load=0.8)     # masses too
```

**`opacity` does not thin a long stroke, it only slows it down.** Dabs overlap, so a
low opacity accumulates back to nearly full colour. If you want a soft film, that is
what `glaze()` is for.

**`load` is how much paint the brush carries**, and dropping it is how you get dry
brush — one of the best tools you have for making a surface look worked. But pass
`load=1.0` explicitly for anything that has to read as a *solid* mass, a correction
included; a pass laid low because it sounded painterly leaves a speckled film that
everything after it sits on. On a mass, `solid=True` is that clause, together with the
`load_falloff=0.0` that keeps the far end of each pass from running dry as well.

**`tip_wobble` gives a round tip a silhouette of its own**, redrawn for every mark the
way a bristle's comb is, so a handful of small marks are not a handful of copies of one
disc. `0` is the disc; `0.35` is a brush set down once; `0.7` and up is a clot. Only
the round tips take it — a `flat` or a `knife` is a chisel, and its rectangle is the
mass it lays.

```python
s.dab(0.42, 0.36, "round_hard", "light", size=0.016, press=3, tip_wobble=0.7)
```

**A loaded brush runs dry along a stroke**, so where a long stroke ends is where its
texture is loudest — and if every stroke in a field runs the same way, one side of the
field speckles. Run the next one back the other way. **Do not lay one broken pass
across the whole canvas**: edge to edge on a single load prints the canvas's own
texture as an even field over everything, and it stays visible under every later
stroke.

Windows, falloff numbers and what each texture does are in `CALIBRATION.md`; if a
stroke seems to have vanished, `s.log()` says how much paint it laid.

### Pressure

`pressure` shapes the stroke along its length:

- `"taper"` — lands light, presses, lifts off. **The default, and usually right.**
- `"press_in"` — starts light, ends heavy.
- `"lift_off"` — starts heavy, trails away.
- `"even"` — constant. Use it deliberately; it is the flattest-looking option.
- `"swell"` — thin, thick in the middle, thin.
- `"dab"` — heavy at the start, gone quickly.

Or pass a number, or a list interpolated along the stroke: `pressure=[0.2, 1.0, 0.3]`.

**On a round tip — `round_hard`, `round_soft`, `liner` — pressure changes how wide
the mark is as well as how much paint lands.** `size` is its width at full pressure,
and it never thins below about a pixel and a half however light the touch. **On the
oriented tips — `flat`, `bristle`, `knife` — it changes only how much paint lands**,
because a flat brush's width is the mass it lays and you want that to be the width
you asked for. So:

- **A mark that tapers is one stroke.** `pressure=[1, 0]` starts at the width you
  asked for and ends at a point.
- The *paint* half of the profile shows most clearly on short strokes and on a
  colour that is not already at full strength — on a long stroke the overlapping
  dabs saturate and `taper` and `even` land much the same weight, even where they
  differ in width.
- **Varying the width of your masses is still your job**, because the brushes that
  lay masses do not vary with pressure. Pass a different `size`. That is the single
  most effective thing you can do to stop a painting looking mechanical.

**At the scale of a feature** the brushes go as small as anything you will paint.
What changes is not the brush: a single dab is a *light touch* — the start of a
`taper`, so it lands a fraction of its colour at about half the width you asked for
— and a small highlight is `s.dab(x, y, ..., press=3)`, three stamps on the same
spot, the middle one at full pressure, and **one** stroke against your budget. The
three-marks rule for anything cell-sized or smaller is in step 6 of [`PAINTER.md`](PAINTER.md), where you
will be when you need it.

**Use `press=3` for anything you actually want to land.** `CALIBRATION.md`'s numbers
for the lighter touches are measured with white on three grounds, and a dark accent on
a lit passage behaves nothing like that: a near-black accent at `press=2` did not
register at all, and cost a painter one of its last ten strokes to lay again. `press=1` and
`press=2` are whispers — reach for them when a whisper is the mark you want, not when
you are being careful.

---

---

## Masses that are not rectangles

Almost nothing you want to paint is a box, and
you will be tempted to paint boxes anyway, because a rectangle is the easiest place
to name. If you block in a shaped mass as a box you get a box, and no amount of
later work removes that. There are two ways not to, and they answer different
questions.

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

A shaped block-in costs about what its box would: the passes are counted across the
mass, not over its area. A mass with a bite out of it keeps the bite — one pass across
a concave shape comes back as the two pieces that are really inside it.

**Read "what its box would" literally, because for a long curved shape the box is the
whole story and the mass is not.** The passes step across the *bounding box*, so a
ribbon that bends pays for the box its bend sweeps out rather than for its own width. A
ribbon `0.029` wide at `size=0.015` costs **3 passes** laid straight and **19** with a
curve in it — the same ribbon, the same brush. A painter budgeted 4 for one and paid
21, which was 7% of its stroke budget on a single call and nearly cost it the strokes
for the rest of the picture. **Before you block in anything long and curved, look at
`shape.box` and cost it off that.**

**The paint still lands outside the shape, and it is the most expensive first mistake
with shapes.** A pass stops when its *centre* reaches the boundary, so the brush hangs
over — and with a brush that is a large fraction of the mass, the silhouette you built
simply disappears, taking its neighbours with it. **Keep the brush under about a fifth
of the mass's width, or `inset()` the shape by half the brush size.**

```python
mass = blob(span("D4", "F6"), wobble=0.3, seed=2)
s.block_in(mass.inset(0.045), "flat", "dark", size=0.09)   # inset by half the brush
s.block_in(mass, "flat", "dark", size=0.06)                # or keep the brush small
s.block_in(mass, "flat", "dark", size=0.09, edge="clean")  # or ask for a drawn contour
```

**`edge="clean"` is those two steps and a third.** It insets the fill by half the
brush, lays it, and then sweeps one pass along the inset outline in the same colour,
so the *outer half* of the brush lands on the line you drew. It costs one stroke more
than the same mass ragged. Reach for it when the silhouette **is** the drawing, and
especially with a round tip on a small mass, where the half-brush overhang arrives as
a fringe of separate discs around the shape rather than as a soft edge, and reads as
spray. Measured on a mass a third of the canvas across with a round
tip at `size=0.05`: paint reaches **20px** past the outline ragged and **13px** clean,
and the clean silhouette is the less ragged of the two.

**Use a solid tip for it.** A `bristle` pulls the paint in too, but one comb pass
along a contour covers about three-quarters of its width, so it leaves a *stringier*
outline than the ragged fill did — and says so when you ask for it.

Where your outline runs off the canvas the inset is dropped, because there is no drawn
line out there for the brush to land on and **a mass that meets the frame should run
off it** — so draw it past the edge and let it.

The default, `edge="ragged"`, is right for everything else: a mass sitting behind
other things wants the brush to break past its boundary, because that is what a brush
does and the mass in front will cover it.

**On a shape that is not convex, `inset()` takes far more than a rim, and it takes it
out of the thin parts first.** Erosion pulls in from every boundary at once, so a lobe
narrower than twice the inset disappears entirely while the body of the mass barely
changes. Measured on a real fifteen-point outline, `inset(0.052)` kept **62.7%** of the
shape's area: the block-in then covered 98.4% of what it was given and **76.2% of the
mass the painter meant**, with one whole limb at 15.5% — bare canvas, found twenty
strokes later by `compare()` and six strokes to fill.

**So preview the inset shape, not the shape.** `CALIBRATION.md`'s coverage figure is
measured on a blob, and a blob is convex.

```python
mass = polygon([(0.30, 0.30), (0.70, 0.30), (0.70, 0.44), (0.44, 0.44),
                (0.44, 0.62), (0.70, 0.62), (0.70, 0.78), (0.30, 0.78)])
s.preview(mass.inset(0.045))                # what you are about to fill, not what you drew
```

Worth a `preview()` every time. And **do not cross a small shaped mass** — the
crossing below is for masses several brushes across; on a small one it serrates its own
boundary.

**When what you have is one boundary** — the edge that matters, read off the grid —
give it to `sweep` and let the passes follow it:

```python
edge = [(0.06, 0.68), (0.31, 0.48), (0.56, 0.63), (0.84, 0.45)]   # read off the grid
s.sweep(edge, "bristle", "dark", into="down", depth=0.30, size=0.12, cross=25)
```

`sweep` runs its first pass along the edge and steps each one after it a part-brush
further into the mass, alternating direction the way `block_in` does. Passes that
run *along* the edge describe the form; columns that hang *down* from it comb the
mass into strands and print the canvas's axis over the whole thing.

- `into=` is which side of the edge the mass is on, and you have to say: a compass
  word or an angle steps every pass the same way, which is the hand working down a
  near-horizontal edge, and an `(x, y)` point *inside* the mass makes the passes
  follow a curved edge instead of shearing off it. A boundary that closes on itself
  needs neither — `closed=True`, and the mass is what it encloses. A shape is such a
  boundary: `s.sweep(shape, "bristle", "dark", depth=0.2)` sweeps round its own
  outline.
- `cross=` is the second set of passes, leaning that many degrees across the first.
  **Take it** — one sweep on its own comes out stringy, and the crossing is what
  closes the mass up. Twenty to thirty degrees is usually enough, and **`cross=0` is not how you decline it** — that raises. Leave the argument out. A shaped `block_in`
  has the same problem and the same answer, `direction=("axis", 90)`.
- `depth=` is how far into the mass to go, and the brush decides how many passes
  that takes unless you say `passes=`.

**Which one?** Fill a shape when you can see the whole silhouette and want it
covered; sweep when one edge is the thing you care about, or when the passes
following the form is the point. And if the mass is close enough to a box that
either feels like overkill, `block_in` at the angle the mass runs at is the cheaper
version of the same idea.

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
passage, and a single cell is the size for a feature. Regions can be written as
strings anywhere: `region="D4"`, `region="C3:F6"`, `region="upper-band"`.

With a reference, a `region=` crop crops **both** panels to the same place,
`grid=True` labels both with the same cells, and `values=True` converts both to
greyscale on the same scale — every view is a like-for-like comparison.

Each look writes a numbered PNG under `out/` — `out/look_001.png`, `out/look_002.png`
and so on — and returns the path. Print it and open that file. Rehearsals have their
own run of numbers, `rehearse_001.png` upward, and each takes the next free name: that
is what lets you rehearse a pass three ways and put the three side by side, which is
most of what rehearsing is for. The look numbering belongs to the session, so a second
session started in the same directory begins again at `look_001.png` and writes over
the first one's; copy anything you want to keep.
**This bites hardest when you paint more than one picture**: a second painting in the
same directory silently overwrites the first painting's entire record of itself, looks
and rehearsals alike. Give each painting its own directory, or copy out the frames
that matter before you start the next one.

Use `values=True` far more often than feels necessary. Use `diff=True` after a pass
to confirm you changed what you meant to change and nothing else.

When a mark seems to have gone missing, `s.log()` says how much paint each one
actually laid, and prints `NO PAINT LANDED` for a mark that changed nothing at all —
usually an opacity of zero, or a glaze into paint that is still soaking wet.

---

## The rest of the API

What each call *is*, in the order you reach for them. What each argument means, what
unit it is in and what it defaults to is one page in
[`REFERENCE.md`](REFERENCE.md) — look a fact up there rather than hunting it here.

```python
s.stroke(points, brush, color, pressure="taper", size=None, opacity=None, note="")
s.dab(x, y, brush, color, size=..., press=1)       # one mark; press stamps it again
s.block_in(place, brush, color, direction=, density=, overhang=, edge=, solid=)  # a mass
s.sweep(edge, brush, color, into=, depth=, cross=, passes=)         # a mass with a shape
s.scumble(band, color_a, color_b, n=8)             # a soft passage, as n strokes
s.scumble(patch, a, b, n, direction="inward")      # ...falling off from its middle
                                                   # leave size off on both: the verb
                                                   # picks it from its own step
s.cover(place, color)                              # bury a mistake; the whole recipe
s.smudge(edge, size=0.02)                          # move paint along a boundary:
                                                   # points, or a shape's own outline
s.glaze(points, color, opacity=)                   # thin transparent film
s.dry(amount=1.0, region=None)
s.undo(n)                                          # scraping, not free
s.look(...)

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

`block_in` takes `direction=` of `"horizontal"`, `"vertical"`, `"diagonal"`,
`"cross"`, `"axis"` (the place's own long axis), **a number of degrees**, or a
sequence of any of those for one pass each. Two passes of parallel strokes look like
hatching; crossed passes look like paint.

Both space their passes a part-brush apart, which assumes a pass is one brush wide
all along — true of `flat`, `bristle` and `knife`, and not of a round tip under a
varying pressure. Lay masses with `flat` or `bristle`; if you want a round tip for
one, give it `pressure="even"` or it will show its passes at their ends.

One `block_in` is not one stroke: it lays a pass for every brush-width of the
region, so a big region with a small brush is twenty or thirty of them. Neither is
one `sweep` — a pass per part-brush of `depth`, and two or three times that again
if you cross it. Check `s.stroke_count` if you are keeping a budget — a whole
painting is usually a few hundred marks, not a few thousand.

**A mass can be costed before the call rather than discovered after it** —
`CALIBRATION.md` has the arithmetic, and it is the difference between planning a pass
and finding out.

**What counts against the budget:** `stroke`, `dab`, `block_in` and `sweep` per pass,
and also **`smudge` and `glaze`** — those two are marks like any other. What is free:
`pencil`, `erase`, `mark`, `look`, `preview`, `rehearse` and `compare`. Do not
discover the first list with three strokes left.

**`block_in` paints past a rectangle** by a fraction of a brush on every side, and
past a *shape* by up to three-quarters of a brush — see **Masses that are not
rectangles** for what that costs and how to inset for it. That spill is fine for a
band and wrong for a mass that meets another at the *same* depth, where it lands on
its neighbour. Painting back to front is the real answer — the far mass spilling into
where the near one is going does no harm, because the near one goes on over it next.

**`overhang` is not the remedy: it controls the ends of each pass, not its sides.**
Measured on a band at `x 0.2–0.8, y 0.585–0.775` with a `bristle` at `size=0.11`, the
passes running horizontally: `overhang=0` laid paint from `x 0.181` to `0.825`, the
default `0.35` from `0.145` to `0.854`, and `1.0` from `0.072` to `0.924` — while the
*sides* sat at `y 0.530–0.844` in all three, about half a brush past the band either
way, unmoved. **For two masses at the same depth, inset the place by half the brush
size.** That is the half of the old advice that works.

**And "the ends" are the ends of the *pass*, which turn with `direction`.** The same
number that keeps a horizontally-swept mass clear of its own left and right edges runs
a vertically-swept one down off its foot and onto whatever it is standing on — and
`"axis"` picks vertical the moment a mass is taller than it is wide. Measured on a shape
`0.40 × 0.30`, bristle at `size=0.030`: swept horizontally, `overhang` takes the paint
from 3px to 22px past the left edge while the top and bottom stay at 6px; swept
vertically, the same settings move the top and bottom from 4px to 18px and leave the
sides where they were. Two masses in one painting were spoiled learning this, one at
each end of the range.

`compare(region=cell("D4"))` measures the tenths of one cell and labels them the
way `grid="fine"` does.

Places:

```python
region("top-left")   # also: top, center, upper-half, lower-half, left-half,
                     # inner, middle-band, upper-band, lower-band, all, ...
cell("D6")           # a grid cell, matching look(grid=True)
span("E5", "H8")     # the rectangle from one cell to another, both included
horizon(0.42)        # a thin band at that height
below(r, 0.15)  above(r, ...)  left_of(r, ...)  right_of(r, ...)  between(a, b)
r.point(0.5, 0.5)    # a point inside a region, in the region's own 0–1 space
r.inset(0.05)  r.scaled(0.8)  r.split_h(3)  r.split_v(2)
```

Shapes — a mass that is not a box. Every one of these is a place like the ones
above, and goes anywhere a region goes:

```python
blob(place, radius, wobble=0.25, seed=0)   # an irregular silhouette
ellipse(place, rx, ry, rotate=0)           # round, or filling the place given
s.circle(place, r, wobble=0)               # round *in pixels* on any canvas
hull([p1, p2, p3])                         # the mass around three or four points
union(a, b)                                # one silhouette round two that overlap
ribbon(points, width, end_width=None)      # a mass running along a line
polygon(points)                            # an outline you already have
shape.inset(0.03)  shape.scaled(0.9)  shape.shifted(0.02, 0)   # ... as a region does
shape.smooth()                             # cut the corners off an outline
shape.axis   shape.area   shape.center   shape.contains(x, y)   shape.closed
```

**`hull` and `union` are not the same join.** A hull covers everything given, but
convexly: two circles come back as a lozenge with the waist between them filled in.
`union` keeps the waist, which is usually the reason there were two circles. The
shapes have to overlap, because what comes back is one silhouette:

```python
lobed = union(s.circle((0.45, 0.42), 0.05), s.circle((0.45, 0.56), 0.08)).smooth()
s.block_in(lobed, "flat", "ochre", size=0.04, edge="clean")
```

`smooth()` cuts the corners off an outline, twice by default. A shape built from a
dozen points has a dozen corners, and a round tip laid along it leaves a scalloped
edge that reads as faceting rather than as form.

`place` is a point `(x, y)` or any region — `blob(cell("D5"))` is an irregular mass
filling that cell. `shape.closed` is the outline as a path, for `s.pencil(...)` or
`s.preview(...)`; `s.sweep(shape, ...)` takes the shape itself. `shape.box` is the
rectangle around it.

Under `easel run` all of these are already in scope. In a plain Python script,
import them: `from easel import Session, Region, region, cell, span, horizon,
below, above, left_of, right_of, between, blob, ellipse, hull, ribbon, polygon`.

---

## Or through the MCP server

If your client speaks MCP, the same verbs are there as tools, and the difference
worth having is that **the looking tools hand you the picture**. `look`, `preview`,
`rehearse`, `compare` and `prepare` return their PNG beside the path they wrote it
to, so looking every five to fifteen strokes costs one call instead of a call and a
file read.

Marks are still made by `run`, which takes the script as text — the same Python
this guide teaches, with `s` and the whole API already in scope. Nothing has to be
written to a file first.

Three tools have no shell equivalent, and they are the three questions about a mark
you have not made yet: `preview` (where does it go), `rehearse` (what will it look
like) and `cost` (what does it charge). They take the same plan, and each hands
back the Python that paints it — so paste that into `run` rather than retyping it.
A plan you retype between checking it and painting it is a plan that will drift.

A **place** arrives as JSON in any of six forms — a named region, a grid cell, a
span, a rectangle, an outline, or a shape builder with its own arguments:

```text
"upper-band"                                    a named region
"D4"                                            one grid cell
"C3:F6"                                         a run of cells
[0.10, 0.10, 0.45, 0.30]                        a rectangle
[[0.2, 0.2], [0.6, 0.15], [0.7, 0.5]]           an outline you have
{"blob": "D5", "radius": 0.12, "seed": 3}       and the builders: blob, ellipse,
{"ribbon": [[0.2, 0.8], [0.5, 0.5]], "width": 0.09}      hull, ribbon, polygon
```

A **plan** is a list of those three kinds of thing, or one on its own. A mass is an
object with `shape` and any `block_in` argument; a sweep is one with `edge` and any
`sweep` argument; a mark is a list of points, or an object with `points`. A place
on its own is a mass, and a bare list of points on its own is a mark.

```json
{"shape": {"blob": "D5", "radius": 0.12, "seed": 3},
 "brush": "bristle", "color": "dark", "size": 0.05, "direction": "axis"}
```

Ask `cost` what that charges before you widen the brush, not after. Then `rehearse`
it, then paste the line it gives you back into `run`.

The server is `easel-mcp`, or `python -m easel.mcp_server` when the scripts
directory is not on `PATH`. It needs one extra: `pip install easel-paint[mcp]`.
