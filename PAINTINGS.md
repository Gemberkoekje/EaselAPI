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
  including those of one subject**: the lighthouse-greenhouse brief was written down
  before any of it was read and then handed to more than one painter unchanged, which is
  the rule satisfied twice over — no painter could be steered by a noun in a worked
  example, and none of them picked the brief either. The heron's second attempt is the
  one deliberate exception: the subject was chosen under the rule the first time and then
  repainted on purpose, by the same painter, to find out what reading the rest of the
  files was worth. Two painters have since chosen *near* neighbours independently — a
  greenhouse interior down the aisle at a low sun, and a greenhouse wall seen from
  outside through fogged glass — the second finding the first's directory only after
  choosing, and declining to open it. **That is not a held subject and is not a
  control**, which is the difference between those two pictures and the ones filed
  under one directory: it is the rule working twice over rather than an experiment.
- **How much else was read varies, and it matters.** The pears session read
  `PAINTER.md` and nothing else in the repository, which makes it the only clean
  measurement of the guide on its own. The car wash read `README.md`, `LESSONS.md` and
  `CALIBRATION.md` first; the lighthouse read those, `PAINTINGS.md`, and both earlier
  paintings' notes and scripts, and took its pass-script convention, its prelude of
  masses as functions and its `compare()` plan sheet from them rather than from the
  guide. The laundromat read `PAINTING.md`, `RECIPES.md` and `REFERENCE.md` but never
  opened `CALIBRATION.md`, and of the earlier paintings read one prelude and one
  planning pass and nothing else. The lighthouse-greenhouse painters all read the four
  guide files. The Sonnet and Opus attempts each read one earlier painting's scripts and
  differ in one place — Sonnet never opened `CALIBRATION.md`, Opus read the sections its
  rules cite — and the Fable attempt read every earlier painting's notes and the dusk
  painting's scripts, and opened `CALIBRATION.md` and `LESSONS.md` only after its
  picture was finished. The pool read the narrowest set of any of them: `PAINTER.md`
  and its nine exercises, `RECIPES.md` and `REFERENCE.md`, and nothing else — no earlier
  painting and no `CALIBRATION.md` — which makes it the method measured without the
  numbers underneath it. The heron's first attempt read that set plus `DIAGNOSIS.md`, and
  its second read everything, which is the one place on this page where the same painter
  appears at both ends of the range. The winter greenhouse's notes record `PAINTER.md`
  and nothing wider. The fogged glass read `PAINTER.md` with its exercises, then
  `PAINTING.md`, then `RECIPES.md` where a passage called for one, grepping
  `REFERENCE.md` and `CALIBRATION.md` rather than reading them, and read no earlier
  painting at all — it found the winter greenhouse in `git status`, recognised how close
  the subject was, and left it shut. So where they
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

**One thing the convention gets wrong, and it is worth knowing before you copy it.**
Numbered pass scripts make the drawing `p1_draw.py`, and once it is pass 1 it is
finished — but the guide's order is *landmarks before anything, pencil **after the
far masses are down**, near masses on top*, which wants a second drawing pass
between 2 and 3. Seven of the paintings here drew no line at all and all but two
placed no landmark; only `pool_night` (`p4_water.py`) and `greenhouse_winter`
(`p4_staging.py`) redrew mid-painting, each in its fourth pass, and only `pool_night`
and `fogged_glass` placed landmarks at all.
**A worked example is an instruction whatever the prose
beside it says**, so the example is winning. If you are numbering passes, name the
second one — `p4_redraw.py` — before you need it.

`greenhouse_winter` is the clearest example of the thing to copy, and it says so in
its own script: *drawn again in pencil on top of the paint, because the first drawing
is under it*. Every pot and every plant in that picture is re-drawn at the pass that
paints it, after the glass, the light and the floor are down — which is the guide's
order followed rather than the convention's.

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

## An empty municipal pool at night, lit from underwater

![An empty municipal pool at night seen from a high corner: the water a bright pale-cyan
diamond crossing the frame, two soft cores of light burning up through it from lamps set
in the pool's own walls, dark deck all around, a chair and one small orange sign at the
left, a board entering from the right edge, and roof members crossing the near-black
band along the top](paintings/pool_night/painting.png)

One light source, and it is underneath everything, so every form in the room is underlit
and the value structure cannot fail: one bright plane against near-black. Square on the
subject is a layer cake — ceiling, wall, far deck, water, near deck — so the viewpoint is
a high corner and the pool is a diamond crossing every band, with the roof members
crossing them again on the other diagonal, a chair crossing them at the left and a board
entering from the right.

| | |
|---|---|
| Canvas | 1024×768, linen, `cool_grey` ground, seed 11 |
| Spent | 221 strokes of a 300 budget, plus two signature marks that did not count |
| Rehearsed and thrown away | Every pass was rehearsed against a copy before it was committed — about forty runs, none of them charged |
| Reproducible | **Not claimed.** Each committed pass ran once in its final form and in order, but that was never checked from a clean session, so nothing here says the scripts rebuild the PNG |
| Files | [`paintings/pool_night/`](paintings/pool_night) — [notes](paintings/pool_night/NOTES.md), [time-lapse](paintings/pool_night/painting.gif) |

This is the picture painted against the narrowest document set on the page — `PAINTER.md`
and its nine exercises, `RECIPES.md` and `REFERENCE.md`, and nothing else — and the
[exercises it worked first](paintings/pool_night/exercises) are committed beside the
passes. It is also the only painting here that used `mark` landmarks: three of them, the
two lamps and the exit sign, pinned in the drawing pass before any paint so that every
later pass building the glow could find the same points again.

The [notes](paintings/pool_night/NOTES.md) are mostly about measuring rather than
looking, because twice the painter's eye was simply wrong and one line of numbers settled
it. A deck that *looked* too light at `0.40` was the `0.39` it had been mixed to — local
contrast against a dark room, the same false alarm the laundromat above talked itself
into. A coping that looked fine had quietly climbed to `0.50` against water at
`0.45`–`0.55`, which is the frame around the subject going as light as the subject, and
nothing but `sample()` was ever going to say so. The deck came down to `0.30` and the
whole stack was re-run for 21 strokes, early, while nothing was standing on it yet.
Three deck glazes later ran straight over the chair and erased it, caught only by
cropping in for the post-pass check's *did a correction bury something?*, and it was
re-laid at its own depth a step darker to suit the darker deck it now stands on.

## A heron in a flooded parking lot at dawn

The other subject here painted more than once, and the only one painted twice by the same
painter. The first attempt was made under the narrowest reading set on the page bar one —
`PAINTER.md` and its nine exercises, then `RECIPES.md`, `REFERENCE.md` and
`DIAGNOSIS.md`. It then wrote its own post-mortem, was shown the files it had been denied,
and painted the subject again with those and that post-mortem in hand. It is not a
controlled experiment — same painter, and it knew what it had got wrong — but it separates
two kinds of fault, which is what it is here for: what a painter gets wrong for want of a
number or a verb, and what it gets wrong for want of judgement.

### First attempt

![A grey heron standing in shallow floodwater over a parking lot at first light: a wide
pale sky with a yellow dawn band low in it, a dark treeline along the right, a lamp
standard still lit at the left and given back by the water as a broken chain of pale
discs, the bird at the middle right with a white head and a dark bill read against the
trees, and painted stall lines showing through the water and converging to the bottom
left](paintings/heron_lot/1/painting.png)

| | |
|---|---|
| Canvas | 1024×768, rough, `toned_warm_grey` ground, seed 17 |
| Spent | 293 strokes of a 320 budget, plus two signature marks that did not count |
| Rehearsed and thrown away | About forty rehearsal runs, none of them charged |
| Reproducible | **Not claimed.** Each pass ran once in its final form and in order, but that was never checked from a clean session |
| Files | [`1/`](paintings/heron_lot/1) — [notes](paintings/heron_lot/1/NOTES.md), [time-lapse](paintings/heron_lot/1/painting.gif), [exercises](paintings/heron_lot/1/ex) |

Its best passage is an absence: water meets sky at `0.07` of value across the whole left
half, under the reading threshold, so there is no horizon line at all until the trees pick
the edge up on the right. That began as the repair for a ruled horizon and came off no
document. Its [notes](paintings/heron_lot/1/NOTES.md) also record a treeline given
sixteen directions to break its comb — on the guide's own advice to vary direction — which
`cost()` priced at **515 strokes against 22 for one direction**, 1.6× the whole budget,
caught before a stroke was spent. And a fault the picture never quite recovers from: the
sky and the mid water were planned `0.00` apart along the entire edge where they meet, so
the greyscale view had a dark and a mid and **no light at all until stroke 217 of 293**.
The dawn band that fixed it was then laid last, because it is light — over the far trees,
the pole and the bird's head, all of which stand in front of the sky. It was repairable
for twelve marks only because every mass in `prelude.py` is a named function that can be
re-run at its own depth.

### Second attempt

![The same heron seen from much higher up, so the flooded asphalt fills nearly the whole
frame: a near-black band of trees across the top with a warm yellow reflection under it,
the bird standing large and high in the picture with a white head and a long ochre bill,
its own pale reflection directly below it, and painted stall lines running away across the
water in the foreground](paintings/heron_lot/2/painting.png)

| | |
|---|---|
| Canvas | 1024×768, rough, a custom ground `#6d635a` at value `0.394`, seed 23 |
| Spent | 253 strokes of a 320 budget, plus two signature marks that did not count |
| Reproducible | **Not claimed**, on the same terms as the first |
| Files | [`2/`](paintings/heron_lot/2) — [notes](paintings/heron_lot/2/NOTES.md), [time-lapse](paintings/heron_lot/2/painting.gif), [the measurement it produced](paintings/heron_lot/2/probe_cover.py) |

The composition throws the horizon away rather than fighting it: a steep downward view in
which the water *is* the picture and the sky exists only as what it gives back, so there
are no horizontal bands to cross and the bird spans the frame with its own reflection.
`compare({place: value})` was run on the empty canvas twice before a stroke — the call the
two sessions before this one never reached — and it found two real merges and one piece of
sloppiness, a bird planned as a single averaged value. The light went in with the ground:
the graded field is pass two, and the picture had a light mass at stroke **16** against
217.

It also produced the page's sharpest engine measurement, in
[`probe_cover.py`](paintings/heron_lot/2/probe_cover.py): **a solid block-in does not land
its colour.** On bare ground at `0.394`, with every clause of a plane that is a plane set
— `density=1.0, solid=True, opacity=1.0, pressure="even"` — a mixture at `0.865` comes
back at `0.403` from a 2.7px `flat`, which is the ground and nothing else, and at 18px is
still `0.04` short. Only a round tip holds its colour small. That is why a bird's head
laid at `size=0.005` was a dark fuzzy ball for four rehearsals, and it is the likelier
account of the first painting's bill "blooming pale" than the one the first painting gave.

### What the second attempt settles

Almost everything that improved was a **lookup** — a number or a verb the first painter
did not have. The one fault that was a matter of judgement repeated itself exactly: *a
mass built of planes* says to decide the tiling with the silhouette, before the block-in;
the painter read it, wrote it into the first painting's notes as the named fault, and then
invented the planes in the pass again. Both birds have a smooth pebble for a body, with
the recipe open the second time.

Which is the better picture is not the same question, and the notes refuse to collapse
them. The second is the better-made one — braver composition, a real focal counterchange,
no depth violation, fewer strokes for more subject — and it is narrower in colour and
came out `0.15` under plan on its glow band. The first has the better single passage, and
nothing in the second is as good as that lost edge. The second also tried to prove one
thing and could not: a wobble measurement meant to show its verb-picked scumbles were
smoother than the first's hand-laid band counts the rough ground's flecking as ripple, so
it says the opposite and is not quoted as evidence either way.

## A greenhouse in winter, looking down the aisle at a low sun

![Inside a small greenhouse in winter, looking straight down the central aisle: a low
sun blooming pale gold behind the fogged end wall, glazing bars and rafters converging
on it, wooden staging down both sides carrying a row of terracotta pots — most holding
dry stalks, two or three still green — deep shadow under the benches, and a galvanised
watering can standing on the dark aisle floor](paintings/greenhouse_winter/painting.png)

Late afternoon, and the whole picture is one problem: light passing through glass,
through fog on the glass, through thin leaves, and stopping dead at the clay.

| | |
|---|---|
| Canvas | 1024×768, linen, `toned_warm_grey` ground, seed 3 |
| Spent | 297 strokes of a 300 budget, plus two signature marks that did not count |
| Reproducible | **Not claimed** — built pass by pass with rehearsals, and the two `erase()` calls in `p12_export.py` were added after the fact. The scripts are the record of how it was made, not a byte-for-byte rebuild |
| Files | [`greenhouse_winter/`](paintings/greenhouse_winter) — [notes](paintings/greenhouse_winter/NOTES.md), [time-lapse](paintings/greenhouse_winter/painting.gif) |

**A frontal elevation of a greenhouse is a layer cake** — plinth, glass, transom, eaves,
ridge, all horizontal — and this painting's first decision was to refuse it. The
viewpoint is one-point perspective straight down the aisle, so the staging, the glazing
bars and the rafters all converge on a vanishing point low and left of centre, and over
the sun's third of the picture there is no horizontal at all. Counting the bands before
the first mass and choosing a viewpoint that crosses them was the whole composition, made
in `p0_draw.py` before a stroke was spent — the closing checklist's warning acted on
rather than discovered afterwards.

It is also the page's best example of the pencil used the way the guide asks. Every pot
and plant is drawn *again*, in graphite on top of the paint, at the pass that paints it;
`p4_staging.py` says why in a comment. And it is the one painting here that spent more
than a third of its budget on a single class of object: 110 strokes of 297 went on the
pots, which is where its own notes locate both its best passage and its worst, nine of
them reading closer to fruit than to terracotta.

## A greenhouse wall in late winter, from outside

![A greenhouse wall seen from outside at a low angle in flat grey winter light: misted
glass running away to the left, dark glazing bars and horizontal pane laps converging, a
green blur of plants pressing behind the film, vertical runnels of water where the fog
has cleared, one leaf pressed flat against the pane and a terracotta pot glowing orange
through the mist, with frozen ground and a bare tree in haze at the
left](paintings/fogged_glass/painting.png)

Standing outside on a flat grey afternoon: the glass fogged from the inside, water run
down it in tracks that clear the film, and the green coming part of the way through. The
picture is almost all one surface, and it has to read as three depths at once — the water
on the near side, the plants behind it, the winter beyond.

| | |
|---|---|
| Canvas | 1200×800, rough, `umber_wash` ground, seed 11 |
| Spent | 311 strokes of a 320 budget, plus two signature marks that did not count |
| Rehearsals | About forty-four, none of them charged |
| Reproducible | **Not claimed** — the drawing pass was run twice and several measuring scripts ran as passes between the painting ones, and a mark's texture is seeded from its place in the log, so a clean rebuild would not come back byte for byte |
| Files | [`fogged_glass/`](paintings/fogged_glass) — [notes](paintings/fogged_glass/NOTES.md), [time-lapse](paintings/fogged_glass/painting.gif) |

This picture reached the same first decision as the one above, by the same route and
independently: a wall of glass painted frontally is a layer cake, so the projection was
written before any line was drawn — every mass placed in metres by a `P(xm, hm, dm)`
helper, eye at 1.70 m, the eave and sill converging and the glazing bars thinning as
`0.8 × 0.045 / dm`. **Two painters who had read the same warning and not each other
arrived at the same helper with the same signature**, which is the closest thing on this
page to a controlled result that nobody controlled for.

Its own decision is the second one: the saturated green is held back everywhere except
where the water has cleared the film, so the only real colour in the picture runs in
narrow vertical tracks down the near pane. One leaf pressed flat against the glass and
one pot seen through the mist are the two marks that say *through*, and they carry it.

What it does not do, by its own account: the bare tree at the left was spent on twice and
is still a grey mass with spokes, the left third is haze rather than fog in one place, and
the warm ground — chosen so that anything left showing would read as warmth coming
through the cool film, which is the whole subject — was buried to `0.07%` of the canvas
in exchange for a solid support, and not noticed until the closing measurement. Its
critique of the engine and the guide is the open section at the top of
[`SUGGESTIONS.md`](SUGGESTIONS.md), the only part of that register that is still a
request list.

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
  elevation that is a stack of horizontal bands — the thing it would change first; among
  the lighthouse-greenhouse attempts, one names nine pots that read closer to fruit than
  to terracotta and another a rock that took a quarter of its budget to end up adequate;
  the winter greenhouse names an aisle floor that is a large quiet mid-brown with
  little incident in it; the fogged glass names a bare tree it spent on twice and still
  calls a grey mass with spokes, a left third that is haze rather than fog in one place,
  and a warm ground chosen so it would show through the cool film and then buried to
  `0.07%` of the canvas;
  and the pool stopped 79 strokes early on purpose and names the dark it left thin —
  the upper-left quarter and the deck corners — while arguing that a night picture needs
  them quiet. Both herons name the same unfinished thing, which is the point of having
  two of them: a bird's body that is a smooth pebble where it should be built of planes,
  abandoned once for want of the recipe and once with the recipe open.

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
