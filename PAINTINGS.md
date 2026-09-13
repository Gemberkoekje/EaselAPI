# What Easel has painted

> Every picture here was painted by a language model working from the guide — no reference
> photograph, no human hand on the canvas, nothing traced. Every mark is a call to this
> API and every one of them is in the log. This file is the record: what was painted,
> what it cost, what failed, and how good the results actually are.

The engine's claim is that a model can paint rather than generate, so the engine is only
worth what has been painted with it. These are those paintings, at full size, with the
parts that did not work left in.

**One section below per directory under [`paintings/`](paintings).** Nothing in this
file counts them, on purpose: a painting is added by committing its directory and
writing its section, and no sentence elsewhere has to be corrected to match.

**If you are about to paint from the guide: have you decided what to paint?** Every
picture here names a subject, and a named subject chooses for you — six of six fresh
sessions once painted a noun the guide had merely listed in passing. **Decide first,
then read this page.** A painter who chose before opening the repository cannot be
steered by a noun in a worked example, and one who has not chosen can be; that is the
whole of the rule, and it is the protocol in [`LESSONS.md`](LESSONS.md) rather than a
matter of taste. `PAINTER.md` points here on exactly the same condition.

Having decided, read them: the pass scripts beside each painting are the end-to-end
worked example the guide cannot be, and the third painter here said it would not have
arrived at their convention on its own.

## The rules they were all made under

- The subject was chosen **before** the guide was read, so the picture was not steered
  towards what the engine happens to be good at. **That holds for every picture here,
  including those of one subject**: the greenhouse brief was written down before any
  of it was read and then handed to more than one painter unchanged, which is the rule
  satisfied twice over — no painter could be steered by a noun in a worked example, and
  none of them picked the brief either.
- **How much else was read varies, and it matters.** The pears session read
  `PAINTER.md` and nothing else in the repository, which makes it the only clean
  measurement of the guide on its own. The car wash read `README.md`, `LESSONS.md` and
  `CALIBRATION.md` first; the lighthouse read those, `PAINTINGS.md`, and both earlier
  paintings' notes and scripts, and took its pass-script convention, its prelude of
  masses as functions and its `compare()` plan sheet from them rather than from the
  guide. The laundromat read `PAINTING.md`, `RECIPES.md` and `REFERENCE.md` but never
  opened `CALIBRATION.md`, and of the earlier paintings read one prelude and one
  planning pass and nothing else. The greenhouse painters all read the four guide
  files. The Sonnet and Opus attempts each read one earlier painting's scripts and
  differ in one place — Sonnet never opened `CALIBRATION.md`, Opus read the sections its
  rules cite — and the Fable attempt read every earlier painting's notes and the dusk
  painting's scripts, and opened `CALIBRATION.md` and `LESSONS.md` only after its
  picture was finished. So where they
  agree, that is several painters finding the same thing with increasing context — and
  where they disagree, it may be the context talking. Each painting's notes say which
  it was.
- No reference photograph, so `prepare`, `sketch`, `ref_shape` and `ref_outline` were
  unavailable and nothing was traced. Every mass is a `polygon`, `blob` or region
  written by hand.
- A stroke budget was written down first, along with a value plan, and both were
  measured against afterwards.
- Every mark went through the API. The pass scripts beside each painting are the
  painting; run them against a fresh session and the same PNG comes back.

## Inside a car wash, from the driver's seat

![Inside a car wash seen from the driver's seat: a magenta foam arch overhead, a bloom
of white light down the tunnel, a red stop light, and a foam-covered side brush swinging
in from the right, past a steering wheel and rear-view mirror](paintings/car_wash/painting.png)

The view out of a windscreen mid-cycle: a magenta foam arch overhead, a bloom of white
light down the tunnel, a red stop light, and a foam-smothered side brush swinging in
from the right. Everything outside the glass is dissolved; nothing in the picture has a
hard edge except the things inside the car.

| | |
|---|---|
| Canvas | 1152×720, linen, `umber_wash` ground, seed 23 |
| Spent | 206 strokes of a 300 budget, plus one signature mark that did not count |
| Sittings | Two — it stopped at 185 strokes, then resumed for the passage it had named as its own weakest |
| Rehearsed and thrown away | 38 marks, none of them charged |
| Reproducible | Nineteen pass scripts rebuild the PNG **byte for byte**, verified by sha256 |
| Files | [`paintings/car_wash/`](paintings/car_wash) — [notes](paintings/car_wash/NOTES.md), [time-lapse](paintings/car_wash/painting.gif) |

The [notes](paintings/car_wash/NOTES.md) are the useful part. They record the first
bloom coming back as a daisy, the first arch turning the picture into a landscape, three
round marks reading as pills and then as stickers, a curved mass laid in horizontal
passes arriving as a staircase, and two smudges dragging finger-shaped lobes of glass
down into the dashboard. They also record the one finding the guide did not have:
**form is bounded at both ends** — under a `0.10` value range it does not read as form
at all, and far over it the mass stops separating from what is behind it.

## Three pears on a kitchen windowsill

![Three ripe pears on a kitchen windowsill in late-afternoon light, a chipped blue enamel
mug behind them and a half-drawn curtain at the right](paintings/windowsill_pears/painting.png)

Three ripe pears in late-afternoon light, a chipped blue enamel mug behind them, a
half-drawn curtain at the right, the sun coming in low through the window.

| | |
|---|---|
| Canvas | 1024×768, linen, `toned_warm_grey` ground, seed 11 |
| Spent | 224 strokes, plus two signature marks that did not count |
| Reproducible | Seventeen pass scripts rebuild it from a fresh session |
| Files | [`paintings/windowsill_pears/`](paintings/windowsill_pears) — [notes](paintings/windowsill_pears/NOTES.md), [time-lapse](paintings/windowsill_pears/painting.gif) |

Five masses were repainted while nothing stood on them yet: a stripy saturated curtain
redone quiet and grey, a sill too orange and its top edge twice, cast shadows that went
on as black slugs, and four hard-edged bars of sunlight buried and redone as one
soft-edged region. This painting is also the one that started
[`SUGGESTIONS.md`](SUGGESTIONS.md) — the register of what each painter asked for after
using the guide, which every session since has added to, and every item of which is
done.

## A lighthouse on a rocky headland at dusk

![A lighthouse on a rocky headland at dusk: a white tower with a red band standing in
dark rock on the left, its lamp lit, an orange afterglow along the right-hand horizon
reflected in a calm sea, and a crescent moon in the upper right](paintings/lighthouse_dusk/painting.png)

The sun has just gone down off the right edge. The afterglow lies along the horizon and
its reflection under it; the tower's right side takes the last warm light and its left
side goes cool into the dusk; the lamp is lit, with its light in the air around the
lantern; a crescent moon hangs over the glow.

| | |
|---|---|
| Canvas | 1024×768, linen, `burnt_sienna` ground, seed 31 |
| Spent | 184 strokes of a 300 budget, plus one signature mark that did not count |
| Rehearsed and thrown away | Eighteen rehearsal runs, none of them charged |
| Reproducible | Ten pass scripts rebuild the PNG **byte for byte**, verified by sha256 |
| Files | [`paintings/lighthouse_dusk/`](paintings/lighthouse_dusk) — [notes](paintings/lighthouse_dusk/NOTES.md), [time-lapse](paintings/lighthouse_dusk/painting.gif) |

The [notes](paintings/lighthouse_dusk/NOTES.md) record an afterglow that came back as a
solid yellow sun three times before it was laid as passes with no outline, a headland
built three times before it was built from the planes rock is made of, a halo that
arrived as a dark cloud with a bulb in it, and a beam rehearsed twice and dropped. They
also record two things the engine did that the guide did not say — a raw RGB triple
handed to the palette is read as sRGB rather than linear, and a vertical pass stack
starts at the right-hand edge. Both are documented now: the first has a verb of its own,
`s.sample(place)`, and the second is a table in [`REFERENCE.md`](REFERENCE.md).

## A laundromat at night, from across the street

![A laundromat at night seen from the sidewalk opposite: a wide lit shopfront window set
in a dark building, a row of washing machines with round doors inside it, one person
sitting alone at the right-hand end, and the window's light broken into streaks down a
wet road in the foreground](paintings/laundromat_night/painting.png)

One lit window in a dark street. The shopfront is the only light in the picture except a
sodium lamp off-canvas to the right; inside it a run of machines, a folding table and a
single figure sitting backlit against the wall; outside, the light lies on the sidewalk
and breaks into streaks down the wet road. The ground is the first custom one here — no
preset goes below `umber_wash` at `0.425`, and all seven are too light for night, so
every mass would have been a hole in one.

| | |
|---|---|
| Canvas | 1024×768, linen, a custom ground at value `0.32`, seed 11 |
| Spent | 286 strokes of a 300 budget, plus two signature marks that did not count |
| Rehearsed and thrown away | 56 rehearsal runs, none of them charged |
| Reproducible | Fourteen pass scripts rebuild the PNG **byte for byte**, verified by sha256 |
| Files | [`paintings/laundromat_night/`](paintings/laundromat_night) — [notes](paintings/laundromat_night/NOTES.md), [time-lapse](paintings/laundromat_night/painting.gif) |

The [notes](paintings/laundromat_night/NOTES.md) record a lit interior that came back a
venetian blind and then a slab, a reflection that flooded the whole foreground, four
smudges that dragged pale finger-shaped lobes out of the glow, a window frame beaded
into chains of blocks by a default jitter wider than its own members, and a rim light
that put a white cap on the head of the one figure the picture is aimed at. Not one mass
was repainted and `undo` was never called: every bit of that was found on a copy.

They also record something none of the others do. Six of its findings became engine
requests and **two did not survive being re-measured** — including the one it led with —
so the notes keep both struck through in place with the measurement that overturned
them. The rendered view does not lift a solid mass off its planned value; a `0.25` band
against a `0.17` wall merely looks like it does, because contrast is local, and the
painter invented a mechanism rather than believe a number it had already sampled
correctly. Both were the items it had marked *observed* rather than *measured*, which is
the distinction earning its keep.

## A lighthouse half way through becoming a greenhouse

The one subject in this collection that more than one painter was given, and the only
place the pass scripts can be read side by side against the same brief: a lighthouse being
converted into a greenhouse, the lamp room packed with tomato vine pressing against the
glass, terracotta pots down the outside stair, and the beam still sweeping a foggy sea,
tinted green through the leaves. The brief was written before any of the guide was read
and then given to each painter unchanged — so it is the one place in this collection
where the subject is held still, and the differences below are the painters'.

### Sonnet

![A lighthouse mid-conversion into a greenhouse, in fog: a pale tower standing in dark
rock, a black zig-zag switchback stair crossing it with round orange-and-green pots on
the treads, green growth trailing down the shaft, a glazed lamp room full of green at
the top, and a broad pale beam going up to the
right](paintings/lighthouse_greenhouse/sonnet/painting.png)

| | |
|---|---|
| Canvas | 1024×768, linen, `cool_grey` ground, seed 74 |
| Spent | 274 strokes of a 340 budget, plus one signature mark that did not count |
| Reproducible | Nine pass scripts rebuild the PNG **byte for byte**, verified by sha256 |
| Files | [`sonnet/`](paintings/lighthouse_greenhouse/sonnet) — [notes](paintings/lighthouse_greenhouse/sonnet/NOTES.md), [time-lapse](paintings/lighthouse_greenhouse/sonnet/painting.gif), [what it would change](paintings/lighthouse_greenhouse/sonnet/SUGGESTIONS.md) |

No pencil at all: the composition was checked with `preview()` and `cost()` against the
grid instead of graphite, on the argument that a rejected polygon is a one-line edit and
a rejected pencil line is an `erase()`. Its [notes](paintings/lighthouse_greenhouse/sonnet/NOTES.md)
record a switchback stair drawn as one bent `ribbon` that `cost()` priced at 141 strokes
of a 340 budget before one was spent — and came in at five once it was cut into straight
flights, which is the guide's own worked example reproduced almost exactly, caught for
free.

### Opus

![A lighthouse in thick fog, half converted into a greenhouse: the lamp room at the top
is packed with dark tomato vine pressing against the glass, terracotta pots stand on the
turns of the outside stair spiralling down the tower, and the lamp still throws a
green-tinted beam out across a foggy sea](paintings/lighthouse_greenhouse/opus/painting.png)

| | |
|---|---|
| Canvas | 1120×860, linen, `toned_warm_grey` ground, seed 41 |
| Spent | 296 strokes of a 300 budget, plus one signature mark that did not count |
| Rehearsed and thrown away | Every pass, most three or four times; 92 rehearsal images, none charged |
| Reproducible | Eleven pass scripts rebuild the PNG **byte for byte**, verified by sha256 |
| Files | [`opus/`](paintings/lighthouse_greenhouse/opus) — [notes](paintings/lighthouse_greenhouse/opus/NOTES.md), [time-lapse](paintings/lighthouse_greenhouse/opus/painting.gif), [what it would change](paintings/lighthouse_greenhouse/opus/SUGGESTIONS.md) |

This one got the beam the earlier lighthouse rehearsed twice and dropped, and for the
reason that one could not: a beam over clear sky has only a glaze, and a beam in fog is a
mass of lit air. It cost two rehearsals to find that the green the brief asks for, mixed
straight, is a chartreuse searchlight that owns the picture — the fix being hue, not
opacity. Its [notes](paintings/lighthouse_greenhouse/opus/NOTES.md) also record three
flat slabs where a cylinder should have turned, a chisel tip staircasing down every
sloping plane edge it was given, ten pots that were ten bricks until each got a rim, and
`direction` left off two shaped block-ins — which would have been charged 44 and 57
passes against the 9 and 9 they were costed at. All eight places of its value plan
finished inside `0.10`.

### Fable

![A lighthouse in grey sea fog, half converted into a greenhouse: a pale tapered tower
on the right standing in dark rock, its glass lamp room packed with green vine and red
tomatoes, a handrailed stair spiralling down the outside with terracotta pots on the
treads, a vine trailing down from the gallery, and a soft green beam leaving the lamp
room leftward into the fog over a grey sea](paintings/lighthouse_greenhouse/fable/painting.png)

| | |
|---|---|
| Canvas | 1024×768, linen, `toned_warm_grey` ground, seed 47 |
| Spent | 284 strokes of a 300 budget, plus one signature mark that did not count |
| Rehearsed and thrown away | 20 rehearsal runs, none of them charged |
| Reproducible | Fourteen pass scripts rebuild the PNG **byte for byte**, verified by sha256 from three fresh sessions |
| Files | [`fable/`](paintings/lighthouse_greenhouse/fable) — [notes](paintings/lighthouse_greenhouse/fable/NOTES.md), [time-lapse](paintings/lighthouse_greenhouse/fable/painting.gif), [what it would change](paintings/lighthouse_greenhouse/fable/SUGGESTIONS.md) |

The beam was built five times before it was three glazes mixed close to the fog — a
bristle wedge came back a ribbed slab, five flat rays a fan of ribbons, and the first
glazes were lime and brightest at the far end, because a round tip's width and its paint
both follow pressure. Its [notes](paintings/lighthouse_greenhouse/fable/NOTES.md) also
record a tower whose clean contour rose off its top as an arch, a stair that read as a
hose wound round the tower until it got a handrail, and an `undo`, taken on purpose
and then measured: the working session drifted `1.06%` of
its pixels from a clean rebuild of the same scripts, so the committed PNG is the rebuild.
Its [suggestions](paintings/lighthouse_greenhouse/fable/SUGGESTIONS.md) carry a probe
for each engine claim, and two of the session's own claims did not survive them.

### Where they agree

Both hit `edge="clean"` on a shape too narrow for the brush it was given, from opposite
ends: Sonnet on a sharply tapering tower, where the contour drew a pointed arch that is
nowhere in the polygon, and Opus on a cap `0.036` deep, where the half-brush inset ate
half the mass and rounded its corners off. Neither found it in the guide, both propose a
warning, and they disagree about which number should trigger it — the distance between
two outline corners, or the brush's share of the shape's shorter extent. Two independent
painters converging on one call is the strongest single thing to come out of painting
one subject more than once.

The Fable painting hit the same call a third time and put a number under it: its clean
contour stood **65px** above the polygon's top edge where the ragged fill stopped at 3px;
the same call on the dusk example's own four-cornered tower arches **45px** on today's
engine; and subdividing each side into six points brings it to 9px. So the trigger is
neither of the two numbers proposed above but the spline the contour is swept along,
bowing through sparse corners — which is why a tapering tower gets a pointed arch and a
shallow cap loses its corners. The measurement is
[`fable/probes/probe_clean_contour.py`](paintings/lighthouse_greenhouse/fable/probes/probe_clean_contour.py).
Since 0.2.0 the engine sweeps the contour along the polygon's own edges, and every one
of those shapes comes back at 4px — the ragged fill's own half-brush; the share the second
painter measured survives as the *corners* going past about a quarter, which is what
the call now warns about. `scripts/probe_greenhouse_session.py` prints the before
beside the after.

Both also arrived at *the tool has a geometry and it will choose if you do not* by a
different route: Sonnet through a `pressure` list that did nothing to a chisel's width,
Opus through a chisel's pass ends stacking into a staircase.

## The log

There is no separate provenance story here: the log **is** the painting.

```python
s.log(last=10_000)              # every stroke as data: brush, path, colour, load
s.replay()                      # rebuild the whole picture from it; identical export
s.replay(upto=40)               # the state after the first 40 records
s.timelapse_gif("painting.gif") # what the GIFs above are
s.contact_sheet("sheet.png")
```

Every session carries a seed, and a stroke's randomness is drawn from
`(seed, stroke index)` rather than from one running stream — so a mark depends only on
which mark it is, not on how much randomness earlier calls happened to consume. That is
what makes "byte for byte" above a claim rather than a hope, and it is checked by
golden-image tests in CI.

## The painter's own account

> *Reserved, and deliberately empty. What belongs here is the painter's own report on
> its work — the self-grade it gave the car wash, and its answer to what painting
> actually felt like — pasted in verbatim rather than summarised or written on its
> behalf. Until that text is added, the honest reading of these pictures is the "What
> still bothers me" section at the foot of each painting's notes, which the painter
> wrote about its own canvas while it could still see it.*

## What these paintings are not

- They are not photorealistic, and the engine cannot make them so. A limited pigment
  palette with no black, a 300-stroke budget and a canvas with tooth put a ceiling on
  detail that is part of the design.
- They are not evidence that the guide works in general. Six measured runs are behind
  `PAINTER.md`, and the standing rule from them is in
  [`LESSONS.md`](LESSONS.md): *a guide change is a hypothesis until a fresh session
  paints against it.*
- None of them is finished in the sense a painter would mean. The car wash left 94
  strokes unspent and names the passage it did not know how to solve; the pears left
  three rims that are three similar yellow stripes; the lighthouse stopped with 116
  unspent on purpose and says which passage they should have gone to if that was wrong;
  the laundromat spent all but 14 and still calls its own composition — a frontal
  elevation that is a stack of horizontal bands — the thing it would change first; and
  of the two greenhouse attempts, one names nine pots that read closer to fruit than to
  terracotta and the other names a rock that took a quarter of its budget to end up
  adequate.

## Further

- [`README.md`](README.md) — what the engine is and how to install it.
- [`PAINTER.md`](PAINTER.md) — the guide every painter here read: the method, in one
  file meant to be held in the head.
- [`PAINTING.md`](PAINTING.md) — the same rules with their reasons, the failures behind
  them and the numbers.
- [`RECIPES.md`](RECIPES.md) — the procedures these paintings produced, collected:
  the calls in order, and what each looks like when it goes wrong.
- [`REFERENCE.md`](REFERENCE.md) — every fact on one page: units, defaults, and what
  each argument does.
- [`LESSONS.md`](LESSONS.md) — what six measured runs and an adversarial review left
  behind.
- [`CALIBRATION.md`](CALIBRATION.md) — the measured numbers behind the guide's rules.
