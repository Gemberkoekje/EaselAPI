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
  example, and none of them picked the brief either. The Bell-Warden is the same case
  from outside the project: its subject was set by the content pack it was painted for,
  and handed to its painter. Wenna Brask's painter chose its subject from that pack, in a
  list of its pictures it wrote at the owner's request before it opened the guide — though
  not before it had read the Bell-Warden's notes. The heron's second attempt is the
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
  the subject was, and left it shut. The hands read `PAINTER.md` with its exercises,
  then `PAINTING.md`, `REFERENCE.md` and `RECIPES.md`, and nothing else — no
  `CALIBRATION.md`, and no earlier painting, from the installed package in an empty
  directory. That makes it the widest read of the package-only sessions and still
  narrower than half the sessions that had a checkout. The lighthouse handover, the
  first painted against 0.6.0, read every document the package ships except
  `CALIBRATION.md` — `easel guide --full`, `--painting`, `--recipes`, `--reference` and
  `--diagnosis`, 194 KB — before its first mark, ran `easel demo mistakes` and five of
  the nine exercises, and had no checkout and no earlier painting. The Bell-Warden, the
  first painted against 0.7.0, read the package's README, `PAINTER.md` short of its last
  two sections, `REFERENCE.md` short of its notices and twelve of `RECIPES.md`'s entries
  — about 21,000 words of the documents, measured from its own session — and never
  opened `PAINTING.md`, `CALIBRATION.md` or `DIAGNOSIS.md`; it ran `easel demo mistakes`
  and all nine exercises, and had no checkout and no earlier painting. Wenna Brask's
  painter, the next morning, read `PAINTER.md` and `RECIPES.md` whole and `REFERENCE.md`
  short of its notices, about 20,500 words, and did the exercises — but began with the
  first painter's memory of the Bell-Warden and read its notes and six of its passes, so it
  is the first painter here to start from another's painting of the same round. So where they
  agree, that is several painters finding the same thing with increasing context — and
  where they disagree, it may be the context talking. Each painting's notes say which
  it was.
- No reference photograph, so `prepare`, `sketch`, `ref_shape` and `ref_outline` were
  unavailable and nothing was traced. Every mass is a `polygon`, `blob` or region
  written by hand.
- A stroke budget was written down first, along with a value plan, and both were
  measured against afterwards.
- Every mark went through the API. The pass scripts beside each painting are the
  painting — **but whether they rebuild it byte for byte is a claim each one makes for
  itself**, in its own `Reproducible` row below, and seven of the twenty-four do not make
  it. What holds everywhere is that a *saved* painting opens as it was painted, because
  the file holds the canvas, and that its log rebuilds the same strokes: a stroke's
  randomness comes from `(seed, stroke index)`, and golden-image tests hold that. A
  rebuild lays those strokes with the engine installed, so a stroke an earlier version
  laid wrongly comes back fixed, and `CHANGELOG.md` names each such fix under its
  version. A rebuild from the committed *scripts* is a different thing again, and a
  drawing pass re-run, a `look` script laid between two painting ones, or a pass edited
  after its rehearsal is enough to move it.

**One thing the convention gets wrong, and it is worth knowing before you copy it.**
Numbered pass scripts make the drawing `p1_draw.py`, and once it is pass 1 it is
finished — but the guide's order is *landmarks before anything, pencil **after the
far masses are down**, near masses on top*, which wants a second drawing pass
between 2 and 3. Seven of the paintings here drew no line at all and most placed no
landmark; only `pool_night` (`p4_water.py`) and `greenhouse_winter`
(`p4_staging.py`) redrew mid-painting, each in its fourth pass, and only `pool_night`,
`fogged_glass` and `hands_beans` placed landmarks at all.
**A worked example is an instruction whatever the prose
beside it says**, so the example is winning. If you are numbering passes, name the
second one — `p4_redraw.py` — before you need it. `bell_warden` shows the cost of not
naming it: it redrew at exactly the right moment, after the room and the plinth and
before the creature, by running `p01_draw.py` again — so its scripts rebuild the picture
only in the order its saved reports record, and its section says which. `wenna_brask`
went the other way: it drew only on a scratch canvas with a light ground, because guides
vanish over dark paint, and never drew on its painting at all.

**There is a second way round it, and `hands_beans` is the one that took it.** It drew
its whole arrangement with `s.guide()` rather than the pencil — graphite on the *view*
rather than in the canvas, which `look()` keeps showing and `export()` never does — so
paint could not bury it and no second drawing pass was needed. It put everything in
`pass01_draw.py`, rewrote that pass three times while it was still free, and never drew
again. The cost is at the other end and its round carries it: scaffolding that paint
cannot bury is scaffolding that sits over the picture in every look until something
takes it off.

`greenhouse_winter` is the clearest example of the thing to copy, and it says so in
its own script: *drawn again in pencil on top of the paint, because the first drawing
is under it*. Every pot and every plant in that picture is re-drawn at the pass that
paints it, after the glass, the light and the floor are down — which is the guide's
order followed rather than the convention's.

## Inside a car wash, from the driver's seat

![Inside a car wash seen from the driver's seat: a magenta foam arch overhead, a bloom
of white light down the tunnel, a red stop light, and a foam-covered side brush swinging
in from the right, past a steering wheel and rear-view mirror](paintings/Claude/car_wash/painting.png)

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
| Files | [`paintings/Claude/car_wash/`](paintings/Claude/car_wash) — [notes](paintings/Claude/car_wash/NOTES.md), [time-lapse](paintings/Claude/car_wash/painting.gif) |

The [notes](paintings/Claude/car_wash/NOTES.md) are the useful part. They record the first
bloom coming back as a daisy, the first arch turning the picture into a landscape, three
round marks reading as pills and then as stickers, a curved mass laid in horizontal
passes arriving as a staircase, and two smudges dragging finger-shaped lobes of glass
down into the dashboard. They also record the one finding the guide did not have:
**form is bounded at both ends** — under a `0.10` value range it does not read as form
at all, and far over it the mass stops separating from what is behind it.

## Three pears on a kitchen windowsill

![Three ripe pears on a kitchen windowsill in late-afternoon light, a chipped blue enamel
mug behind them and a half-drawn curtain at the right](paintings/Claude/windowsill_pears/painting.png)

Three ripe pears in late-afternoon light, a chipped blue enamel mug behind them, a
half-drawn curtain at the right, the sun coming in low through the window.

| | |
|---|---|
| Canvas | 1024×768, linen, `toned_warm_grey` ground, seed 11 |
| Spent | 224 strokes, plus two signature marks that did not count |
| Reproducible | Seventeen pass scripts rebuild it from a fresh session |
| Files | [`paintings/Claude/windowsill_pears/`](paintings/Claude/windowsill_pears) — [notes](paintings/Claude/windowsill_pears/NOTES.md), [time-lapse](paintings/Claude/windowsill_pears/painting.gif) |

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
reflected in a calm sea, and a crescent moon in the upper right](paintings/Claude/lighthouse_dusk/painting.png)

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
| Files | [`paintings/Claude/lighthouse_dusk/`](paintings/Claude/lighthouse_dusk) — [notes](paintings/Claude/lighthouse_dusk/NOTES.md), [time-lapse](paintings/Claude/lighthouse_dusk/painting.gif) |

The [notes](paintings/Claude/lighthouse_dusk/NOTES.md) record an afterglow that came back as a
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
wet road in the foreground](paintings/Claude/laundromat_night/painting.png)

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
| Files | [`paintings/Claude/laundromat_night/`](paintings/Claude/laundromat_night) — [notes](paintings/Claude/laundromat_night/NOTES.md), [time-lapse](paintings/Claude/laundromat_night/painting.gif) |

The [notes](paintings/Claude/laundromat_night/NOTES.md) record a lit interior that came back a
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
right](paintings/Claude/lighthouse_greenhouse/sonnet/painting.png)

| | |
|---|---|
| Canvas | 1024×768, linen, `cool_grey` ground, seed 74 |
| Spent | 274 strokes of a 340 budget, plus one signature mark that did not count |
| Reproducible | Nine pass scripts rebuild the PNG **byte for byte**, verified by sha256 |
| Files | [`sonnet/`](paintings/Claude/lighthouse_greenhouse/sonnet) — [notes](paintings/Claude/lighthouse_greenhouse/sonnet/NOTES.md), [time-lapse](paintings/Claude/lighthouse_greenhouse/sonnet/painting.gif), [what it would change](paintings/Claude/lighthouse_greenhouse/sonnet/SUGGESTIONS.md) |

No pencil at all: the composition was checked with `preview()` and `cost()` against the
grid instead of graphite, on the argument that a rejected polygon is a one-line edit and
a rejected pencil line is an `erase()`. Its [notes](paintings/Claude/lighthouse_greenhouse/sonnet/NOTES.md)
record a switchback stair drawn as one bent `ribbon` that `cost()` priced at 141 strokes
of a 340 budget before one was spent — and came in at five once it was cut into straight
flights, which is the guide's own worked example reproduced almost exactly, caught for
free.

### Opus

![A lighthouse in thick fog, half converted into a greenhouse: the lamp room at the top
is packed with dark tomato vine pressing against the glass, terracotta pots stand on the
turns of the outside stair spiralling down the tower, and the lamp still throws a
green-tinted beam out across a foggy sea](paintings/Claude/lighthouse_greenhouse/opus/painting.png)

| | |
|---|---|
| Canvas | 1120×860, linen, `toned_warm_grey` ground, seed 41 |
| Spent | 296 strokes of a 300 budget, plus one signature mark that did not count |
| Rehearsed and thrown away | Every pass, most three or four times; 92 rehearsal images, none charged |
| Reproducible | Eleven pass scripts rebuild the PNG **byte for byte**, verified by sha256 |
| Files | [`opus/`](paintings/Claude/lighthouse_greenhouse/opus) — [notes](paintings/Claude/lighthouse_greenhouse/opus/NOTES.md), [time-lapse](paintings/Claude/lighthouse_greenhouse/opus/painting.gif), [what it would change](paintings/Claude/lighthouse_greenhouse/opus/SUGGESTIONS.md) |

This one got the beam the earlier lighthouse rehearsed twice and dropped, and for the
reason that one could not: a beam over clear sky has only a glaze, and a beam in fog is a
mass of lit air. It cost two rehearsals to find that the green the brief asks for, mixed
straight, is a chartreuse searchlight that owns the picture — the fix being hue, not
opacity. Its [notes](paintings/Claude/lighthouse_greenhouse/opus/NOTES.md) also record three
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
room leftward into the fog over a grey sea](paintings/Claude/lighthouse_greenhouse/fable/painting.png)

| | |
|---|---|
| Canvas | 1024×768, linen, `toned_warm_grey` ground, seed 47 |
| Spent | 284 strokes of a 300 budget, plus one signature mark that did not count |
| Rehearsed and thrown away | 20 rehearsal runs, none of them charged |
| Reproducible | Fourteen pass scripts rebuild the PNG **byte for byte**, verified by sha256 from three fresh sessions |
| Files | [`fable/`](paintings/Claude/lighthouse_greenhouse/fable) — [notes](paintings/Claude/lighthouse_greenhouse/fable/NOTES.md), [time-lapse](paintings/Claude/lighthouse_greenhouse/fable/painting.gif), [what it would change](paintings/Claude/lighthouse_greenhouse/fable/SUGGESTIONS.md) |

The beam was built five times before it was three glazes mixed close to the fog — a
bristle wedge came back a ribbed slab, five flat rays a fan of ribbons, and the first
glazes were lime and brightest at the far end, because a round tip's width and its paint
both follow pressure. Its [notes](paintings/Claude/lighthouse_greenhouse/fable/NOTES.md) also
record a tower whose clean contour rose off its top as an arch, a stair that read as a
hose wound round the tower until it got a handrail, and an `undo`, taken on purpose
and then measured: the working session drifted `1.06%` of
its pixels from a clean rebuild of the same scripts, so the committed PNG is the rebuild.
Its [suggestions](paintings/Claude/lighthouse_greenhouse/fable/SUGGESTIONS.md) carry a probe
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
[`fable/probes/probe_clean_contour.py`](paintings/Claude/lighthouse_greenhouse/fable/probes/probe_clean_contour.py).
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
band along the top](paintings/Claude/pool_night/painting.png)

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
| Files | [`paintings/Claude/pool_night/`](paintings/Claude/pool_night) — [notes](paintings/Claude/pool_night/NOTES.md), [time-lapse](paintings/Claude/pool_night/painting.gif) |

This is the picture painted against the narrowest document set on the page — `PAINTER.md`
and its nine exercises, `RECIPES.md` and `REFERENCE.md`, and nothing else — and the
[exercises it worked first](paintings/Claude/pool_night/exercises) are committed beside the
passes. It is also the only painting here that used `mark` landmarks: three of them, the
two lamps and the exit sign, pinned in the drawing pass before any paint so that every
later pass building the glow could find the same points again.

The [notes](paintings/Claude/pool_night/NOTES.md) are mostly about measuring rather than
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
left](paintings/Claude/heron_lot/1/painting.png)

| | |
|---|---|
| Canvas | 1024×768, rough, `toned_warm_grey` ground, seed 17 |
| Spent | 293 strokes of a 320 budget, plus two signature marks that did not count |
| Rehearsed and thrown away | About forty rehearsal runs, none of them charged |
| Reproducible | **Not claimed.** Each pass ran once in its final form and in order, but that was never checked from a clean session |
| Files | [`1/`](paintings/Claude/heron_lot/1) — [notes](paintings/Claude/heron_lot/1/NOTES.md), [time-lapse](paintings/Claude/heron_lot/1/painting.gif), [exercises](paintings/Claude/heron_lot/1/ex) |

Its best passage is an absence: water meets sky at `0.07` of value across the whole left
half, under the reading threshold, so there is no horizon line at all until the trees pick
the edge up on the right. That began as the repair for a ruled horizon and came off no
document. Its [notes](paintings/Claude/heron_lot/1/NOTES.md) also record a treeline given
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
water in the foreground](paintings/Claude/heron_lot/2/painting.png)

| | |
|---|---|
| Canvas | 1024×768, rough, a custom ground `#6d635a` at value `0.394`, seed 23 |
| Spent | 253 strokes of a 320 budget, plus two signature marks that did not count |
| Reproducible | **Not claimed**, on the same terms as the first |
| Files | [`2/`](paintings/Claude/heron_lot/2) — [notes](paintings/Claude/heron_lot/2/NOTES.md), [time-lapse](paintings/Claude/heron_lot/2/painting.gif), [the measurement it produced](paintings/Claude/heron_lot/2/probe_cover.py) |

The composition throws the horizon away rather than fighting it: a steep downward view in
which the water *is* the picture and the sky exists only as what it gives back, so there
are no horizontal bands to cross and the bird spans the frame with its own reflection.
`compare({place: value})` was run on the empty canvas twice before a stroke — the call the
two sessions before this one never reached — and it found two real merges and one piece of
sloppiness, a bird planned as a single averaged value. The light went in with the ground:
the graded field is pass two, and the picture had a light mass at stroke **16** against
217.

It also produced the page's sharpest engine measurement, in
[`probe_cover.py`](paintings/Claude/heron_lot/2/probe_cover.py): **a solid block-in does not land
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
watering can standing on the dark aisle floor](paintings/Claude/greenhouse_winter/painting.png)

Late afternoon, and the whole picture is one problem: light passing through glass,
through fog on the glass, through thin leaves, and stopping dead at the clay.

| | |
|---|---|
| Canvas | 1024×768, linen, `toned_warm_grey` ground, seed 3 |
| Spent | 297 strokes of a 300 budget, plus two signature marks that did not count |
| Reproducible | **Not claimed** — built pass by pass with rehearsals, and the two `erase()` calls in `p12_export.py` were added after the fact. The scripts are the record of how it was made, not a byte-for-byte rebuild |
| Files | [`greenhouse_winter/`](paintings/Claude/greenhouse_winter) — [notes](paintings/Claude/greenhouse_winter/NOTES.md), [time-lapse](paintings/Claude/greenhouse_winter/painting.gif), [verdict](paintings/Claude/greenhouse_winter/verdict.md) |

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
left](paintings/Claude/fogged_glass/painting.png)

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
| Files | [`fogged_glass/`](paintings/Claude/fogged_glass) — [notes](paintings/Claude/fogged_glass/NOTES.md), [time-lapse](paintings/Claude/fogged_glass/painting.gif), [verdict](paintings/Claude/fogged_glass/verdict.md) |

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
in exchange for a solid support, and not noticed until the closing measurement — which
is the reason `report()` now says what share of the canvas is still bare. Its critique of
the engine and the guide is the tenth session's round in
[`SUGGESTIONS.md`](SUGGESTIONS.md), acted on in 0.4.0 together with the winter
greenhouse's.

## The underside of a pier at low tide

![Looking out from beneath a pier: a dark timber underside filling the upper frame with
joists receding to the right and diagonal cross-bracing across them, two near pilings
cropping the left and right edges and two more standing further back in the murk, a wedge
of pale daylight widening to the right between the deck and the water, and dark green
water below it carrying a broken shimmer of that light and darkening into the
foreground](paintings/Claude/pier_underside/painting.png)

The first picture here painted from nothing but the installed package. The session was
told to `pip install easel-paint` and paint from whatever came with it; it read
`python -m easel guide`, `--full`, `--reference` and `easel brushes`, and never opened
this repository. It also ran in an empty directory — no checkout, no listing, nothing on
disk to read — which is why it is the painting that settles where the subjects have been
coming from.

| | |
|---|---|
| Canvas | 1024×768, linen, `#5a5045` ground (v=0.32), seed 11 |
| Spent | 257 strokes of a 300 budget, plus two signature marks that did not count |
| Rehearsals | Twenty-three, none of them charged |
| Reproducible | **Not claimed** — the drawing pass was rewritten and re-run three times, `look` scripts ran as passes between the painting ones, and each pass script was edited after its rehearsal, so what is committed is the last version of each rather than the sequence that built the canvas |
| Files | [`pier_underside/`](paintings/Claude/pier_underside) — [notes](paintings/Claude/pier_underside/NOTES.md), [time-lapse](paintings/Claude/pier_underside/painting.gif) |

Its own decision is the cross-bracing, and it arrived late. Deck, slot and water is three
horizontal bands, and the post-pass check had said so on nearly every pass — *a stack of
bars unless the subject runs that way* — while the subject genuinely did run that way. The
two near pilings cross the bands; the diagonal braces are what finally made the frame read
as structure rather than as stripes, and they went on with fewer than a hundred strokes
left.

**What it does not do is the reason it matters.** The subject was chosen, and written
down, before anything was installed: under a pier the light arrives from *below*, bounced
up off the water, so every form is lit backwards. That inversion is not in the finished
picture — what is there is a dark structure over water at dusk, lit from the ordinary
direction. It reached that on a clean sheet: the value structure is sound, the masses are
shapes, the edges vary, the lightest mass is the one planned to be lightest, and the
ground still shows at `0.58%`. **It passed every line of the closing checklist on the way
to losing the thing it was for.**

That is the finding, and it is the first on this page aimed at the picture rather than at
the marks: nothing in the method asks whether the reason you chose the subject survived.
The checklist asks whether the thing you measured most carefully is still attached, which
is a question about a mark. Its round in [`SUGGESTIONS.md`](SUGGESTIONS.md) proposes the
two lines that would have caught it — one in the plan, one at the end — and both are in
0.5.0.

By its own account it also leaves the pilings as slabs, cylinders painted as rectangles
with a stripe down one side that never turn from lit to shadow; crushes almost the whole
picture into `0.15`–`0.35` of a box that runs to `0.96`, and calls it atmosphere; and
stops with the weakest passage still the weakest. Its critique of the engine and the guide
— including a warning it learned to skim, and a card so self-contained that it finished a
painting without opening three of the five files — is in the same round.

## A pair of hands sorting dried beans

![Looking down onto a dark warm table lit from the upper left: a shallow bowl of dried
beans cropped by the lower left corner with a grazed light along its far rim, four beans
put down on the table beside it, and in the centre a cupped hand seen from the front with
two lit fingers above a dark hollow and a thumb rising across them, a second hand coming
steeply down from the upper right with its thumb and finger closing on a single bean, and
both forearms running off the frame and darkening as they
go](paintings/Claude/hands_beans/painting.png)

The second painting made from the installed package alone, and the first made against a
shipped release by a painter who had never seen this repository. `python -m easel guide`,
`--full`, `--painting`, `--reference` and `--recipes`, all nine exercises, and nothing
else: no `CALIBRATION.md`, no `LESSONS.md`, no `DIAGNOSIS.md`, and no earlier painting.
It ran in an empty directory, on **0.4.0**, which is the release before the one its own
round is filed against.

| | |
|---|---|
| Canvas | 1024×768, linen, `#5f4a39` ground (v=0.31), seed 11 |
| Spent | 329 strokes of a 420 budget, plus two signature marks that did not count |
| Rehearsals | 114 rehearsal views across the session, none of them charged |
| Reproducible | **Not claimed** — the drawing pass was rewritten three times, `look` and `probe` scripts ran as passes between the painting ones, `prelude.py` was edited between passes as mixtures were rewritten, and each pass was edited after its rehearsal |
| Files | [`hands_beans/`](paintings/Claude/hands_beans) — [notes](paintings/Claude/hands_beans/NOTES.md), [time-lapse](paintings/Claude/hands_beans/painting.gif), [exercises](paintings/Claude/hands_beans/ex) |

**It is the third painting here to place landmarks, and the first to draw the whole
arrangement with `s.guide()` rather than the pencil** — which sidesteps the burial
problem the convention note above describes, because a guide is on the view and paint
cannot bury it. It also produced the opposite problem, and the round below carries it:
the scaffolding and the six landmark labels sat over the focal point through every look
of the session, and one of them, `pinch`, sat *on* it.

**Its subject was chosen the way this page requires and then chosen again by a human.**
Asked for ten subjects before anything was installed, it listed a laundromat at 2 a.m.
first, the underside of a pier second, a greenhouse in winter third and an empty drained
pool eighth — **four of the ten already hanging in a repository it had never opened**,
and the first and third in the same positions the pier session's list put them. The
repository's owner replied that the laundromat, the pier and the greenhouse were already
painted, and picked the hands off the rest of the list. That is the folder question
answered a second time, from a second empty directory, with the overlap counted rather
than described.

**What it was for is half in the picture.** The reason was written down before anything
was installed: old hands are warm and red at the knuckles where the skin is thin over
bone and cooler across the planes between, and that contrast — not the pose — is what
keeps the subject out of sentimentality. The warm/cool contrast is there, and it had to
be a glaze; laid as paint at any useful opacity it is a pink stripe. The specificity is
not. Nothing in the finished picture could only be an old hand.

By its own account the hands do not read as hands: the gesture is legible and the anatomy
is not. It traces that to a drawing it redrew three times without once asking whether the
*view* was right — four near-parallel fingers laid out sideways, where a cupped hand seen
from the front shows them foreshortened and overlapping — and then to about eighty
strokes spent treating that at the brush, four times over, while the fault sat upstream in
graphite where moving it is free. It stopped at 329 of 420 with the weakest passage still
the weakest, and says in its notes that *deliberate* and *finished* are not the same word.

Two of the engine items it arrived with **died on measurement before they were filed** —
*A form that turns* holds up at a finger's width, and `edge="clean"` lays no brighter
contour than a ragged edge does. Its round says so, and says what it had mistaken for
each.

## A mountain landscape at sunset

![A mountain landscape at sunset: a dark ridge of mountains across the middle of the
frame under a sky banded blue at the top and orange toward the horizon, a pale sun low
over the near slope, and a wide strip of bare grey ground left unpainted across the
bottom third](paintings/BigPickle_blind/sunset_landscape/painting.png)

Painted blind by BigPickle — unable to open a look between passes, so its habit of
looking every five to fifteen strokes was followed in spirit rather than checked against
the canvas as it went. Three values stacked into one scene: a dark ridge, a flat
foreground, a warm sky, with a horizon broken by the mountains themselves rather than
left as a straight band.

| | |
|---|---|
| Canvas | 1200×800, linen, `toned_grey` ground, seed 42 |
| Spent | 50 strokes of a 120 budget |
| Reproducible | One script (`sunset_paint.py`) rebuilds the PNG from a fresh session; `make_timelapse.py` regenerates the GIF |
| Files | [`paintings/BigPickle_blind/sunset_landscape/`](paintings/BigPickle_blind/sunset_landscape) — [notes](paintings/BigPickle_blind/sunset_landscape/NOTES.md), [time-lapse](paintings/BigPickle_blind/sunset_landscape/painting.gif), [verdict](paintings/BigPickle_blind/sunset_landscape/verdict.md) |

Its own `report()` found what painting without looking predicts: 30 of 44 long marks
running within six degrees of horizontal, and 31.94% of the canvas still bare ground
where density was left low on purpose and came in lower than intended. The
[notes](paintings/BigPickle_blind/sunset_landscape/NOTES.md) call this the tool's own
check catching a fault a painter with eyes would have caught much earlier.

## A small boat crossing a low sun's reflection

![A low golden sun just above the horizon over open water, its light broken into a
column of short glowing bars reflected down toward the viewer, banded pink and orange
clouds above, and a small dark boat in silhouette crossing the light to the
right](paintings/Deepseek/tidal_sky/painting.png)

Painted by DeepSeek. The whole picture is one light — a low sun's amber-to-coral
reflection running unbroken from sky to water — and the boat is the one dark thing
standing in it, given deliberately few of the picture's 68 spent strokes: the subject is
the light, not the boat.

| | |
|---|---|
| Canvas | 1024×768, linen, `toned_grey` ground, seed 7 |
| Spent | 68 strokes of a 300 budget |
| Reproducible | Five pass scripts rebuild it from `prelude.py` against a fresh session |
| Files | [`paintings/Deepseek/tidal_sky/`](paintings/Deepseek/tidal_sky) — [notes](paintings/Deepseek/tidal_sky/NOTES.md), [time-lapse](paintings/Deepseek/tidal_sky/painting.gif), [verdict](paintings/Deepseek/tidal_sky/verdict.md), [what painting felt like](paintings/Deepseek/tidal_sky/feelings.md) |

Its [notes](paintings/Deepseek/tidal_sky/NOTES.md) record a glitter path that first read
as floating rectangles — vertical `flat` strokes tilted across the water, printing the
tool's own chisel shape — and was rebuilt as horizontal broken flashes, shorter and
fainter toward the viewer. The standing warnings on a near-flat comb and 0% bare ground
are kept rather than fixed: a calm sea at golden hour is horizontal, and a full
sky-and-water field leaves no ground to show.

## A misty pine forest at dawn, across still water

![Four dark pine trees on a headland at the lower left, against a hazy dawn sky banded
from slate blue-grey at the top through pink to gold, a bright sun low over the far
shore with its light scattered in broken bars down a still lake in the
foreground](paintings/Gemini/misty_pine_forest_at_dawn/painting.png)

Painted by Gemini, with no stroke budget set: 725 marks on fine linen, the composition
split at a horizon of `y = 0.52` into cold twilight air warming toward the sun and a
glassy lake mirroring it back, broken by a shimmering glitter path toward the viewer.

| | |
|---|---|
| Canvas | 1024×768, linen, `toned_warm_grey` ground, seed 42 |
| Spent | 725 marks, no stroke budget set |
| Reproducible | One script (`paint_dawn_forest.py`) rebuilds it deterministically |
| Files | [`paintings/Gemini/misty_pine_forest_at_dawn/`](paintings/Gemini/misty_pine_forest_at_dawn) — [notes](paintings/Gemini/misty_pine_forest_at_dawn/NOTES.md), [time-lapse](paintings/Gemini/misty_pine_forest_at_dawn/painting.gif), [verdict](paintings/Gemini/misty_pine_forest_at_dawn/verdict.md) |

Its [notes](paintings/Gemini/misty_pine_forest_at_dawn/NOTES.md) name two shapes the
engine keeps producing when asked for radiating light: linear strokes out from a point
read as a wagon wheel, and continuous horizontal bars centred on a reflection step down
into a ziggurat. Both were rebuilt as broken, irregular marks instead. A third finding is
about the engine rather than the picture: `titanium_white` reflects at `0.958` and no
mixture can be asked for higher, which the first attempt at the sun's core found out from
a `ValueError`.

## A terminal window glowing green in a dark room

![A CRT monitor glowing green in an otherwise dark room: pale phosphor text scrolling
down the screen with a bright cursor at the end of the last line, the glow spilling
across a keyboard and a mug on the desk below and pooling in a soft halo on the wall
behind](paintings/GLM/terminal_window/painting.png)

Painted by GLM. The only light in the picture is inside it, so the painting is about the
*fall* of that light — screen to glow to pool to darkness — rather than about a monitor;
`compare()` checked the block-in against a written value plan and came back with every
one of six places within `0.10`.

| | |
|---|---|
| Canvas | 1024×768, linen, `#2e332c` ground, seed 7 |
| Spent | 126 strokes of a 300 budget |
| Reproducible | Seven pass scripts (plus a free graphite `draw.py`) rebuild it from `prelude.py` |
| Files | [`paintings/GLM/terminal_window/`](paintings/GLM/terminal_window) — [notes](paintings/GLM/terminal_window/NOTES.md), [time-lapse](paintings/GLM/terminal_window/painting.gif), [verdict](paintings/GLM/terminal_window/verdict.md), [the rings, frame by frame](paintings/GLM/terminal_window/rings/README.md) |

Its [notes](paintings/GLM/terminal_window/NOTES.md) record a halo that came back ringed —
the painter's own account is crossing glazes over a block-in still wet, printing
concentric rings — and cost the one `undo` in the session to fix, rebuilt as a single
tight inward scumble instead. **That account is the one thing on this page a later
reading has overturned**, and seven frames out of the painter's own working folder are
committed beside the painting rather than the conclusion: the wall is clean after the
glazes and before the block-in, and what the rings actually are is an inward scumble's
own contour rings around a patch that overshoots the glass. The frames, and the three
accounts written of them, are in
[`rings/`](paintings/GLM/terminal_window/rings/README.md). They also
catch their own summary short: strokes noted `subject` come to 9%, but counting the
subject's own light along with it — halo, pool, glass, bezel — the true share is closer
to 46% against a 45% plan, and the notes record both numbers rather than the flattering
one.

## When the windows come on

![A row of gabled cottages along a curving stone quay at dusk, warm light in their
windows, a small tower rising near the centre, a hazy violet-pink sky, a dark headland
across the water to the left, and a red dinghy at rest in the harbour with the windows'
light broken into streaks toward it](paintings/GPT/seaside-village/painting.png)

Painted by GPT-6 Astra. The little warmth of inhabited windows, carried out into cold
water, is what makes an ordinary harbour feel like a place to come home to — the red
dinghy is held by the same quiet that surrounds it, and the reason survived: the windows
feel inhabited, and their light reaches the boat.

| | |
|---|---|
| Canvas | 1440×960, linen, `#746d78` ground, seed 61 |
| Spent | 408 strokes of a 420 budget, plus 3 free signature marks |
| Reproducible | One script (`paint.py`, 43 rehearsable passes); reloading the saved session and re-exporting reproduced a **SHA-256-identical PNG** |
| Files | [`paintings/GPT/seaside-village/`](paintings/GPT/seaside-village) — [notes](paintings/GPT/seaside-village/NOTES.md), [time-lapse](paintings/GPT/seaside-village/painting.gif), [verdict](paintings/GPT/seaside-village/verdict.md), [what painting felt like](paintings/GPT/seaside-village/feelings.md) |

Its [notes](paintings/GPT/seaside-village/NOTES.md) record three holes punched in the
cottage walls — a shaped block-in path can still wander apart even with `solid=True` —
closed with loaded flat marks before the windows went in, and a first pass of reflections
built from seven short strokes that came down as spoon-shaped islands, rebuilt as one
connected mass with a broken lower edge. Subject share is given twice rather than rounded
to one figure: 42.2% of the 408 paid marks by the end, against a 61.0% share of the marks
spent at the point the boat's own structure was finished.

## A quiet harbour at dusk

![Two boat silhouettes and a receding pier as flat dark shapes on a muted grey-teal
sheet of water, a thin warm gold band at the horizon, a pale blue-grey sky, and a dark
headland shape at the upper right](paintings/Grok/harbor/painting.png)

Painted by Grok. Dusk flattens the water into one colour, so the painting is mostly edges
and light rather than detail — the harbour is a single muted sheet, and the boats and
pier are silhouettes against the afterglow.

| | |
|---|---|
| Canvas | 1024×768, linen, `cool_grey` ground, seed 11 |
| Spent | 132 strokes of a 300 budget |
| Reproducible | Six pass scripts rebuild it from `prelude.py` against a fresh session |
| Files | [`paintings/Grok/harbor/`](paintings/Grok/harbor) — [notes](paintings/Grok/harbor/NOTES.md), [time-lapse](paintings/Grok/harbor/painting.gif), [verdict](paintings/Grok/harbor/verdict.md) |

Its [notes](paintings/Grok/harbor/NOTES.md) record a dinghy that failed three times —
polygons, then stacked rims, then three strokes — and was dropped rather than forced: two
boats and the pier are enough edges. The pier itself stayed a flat brown wedge, named as
the weakest passage. Subject share was 19% of 134 marks against a third planned; counting
the flattened water itself as the subject, which is most of the field, the share is most
of the picture — that gap is recorded as the point of the painting rather than a miss.

## A lighthouse's lamp holding the dark coast together

![A dark tower with a lit lamp room standing on a dark rocky point, a warm gold band
glowing along the horizon behind it, a deep blue sea below crossed by a horizontal wave
band, and a dark blue-violet sky
above](paintings/Kimi/lighthouse-dusk/painting.png)

Painted by Kimi, on the same brief as the page's earlier [lighthouse on a rocky headland
at dusk](#a-lighthouse-on-a-rocky-headland-at-dusk): one small warm lamp holding a whole
dark coast together, everything else arranged around the quiet it makes.

| | |
|---|---|
| Canvas | 1024×768, linen, `toned_grey` ground, seed 7 |
| Spent | 170 strokes of a 420 budget |
| Reproducible | Five pass scripts rebuild it from `prelude.py` against a fresh session |
| Files | [`paintings/Kimi/lighthouse-dusk/`](paintings/Kimi/lighthouse-dusk) — [notes](paintings/Kimi/lighthouse-dusk/NOTES.md), [time-lapse](paintings/Kimi/lighthouse-dusk/painting.gif), [verdict](paintings/Kimi/lighthouse-dusk/verdict.md) |

Its [notes](paintings/Kimi/lighthouse-dusk/NOTES.md) record a first reflection built from
flat horizontal flashes that read as small bricks, and a `cover()` repair that buried
them but also laid a flat patch over too much sea and in front of the tower — rejected,
and rebuilt instead as five bent, starved strokes down the sides where the tower and rock
interrupt the middle. Stopped at 170 of 420 because more sea marks were making the
picture busier, not better.

## Two warm lights handing over: a lighthouse at dusk

![A lighthouse at dusk standing on a dark headland at the right, its lamp lit and a faint
beam reaching back across a blue-grey sky toward an orange afterglow low on the left
horizon, the glow broken into slivers down a calm sea toward the
viewer](paintings/Claude/lighthouse_handover/painting.png)

The first painting made against 0.6.0, by `claude-opus-5-5` at max effort, from the
installed package and nothing else. The sun's glow is going out low on the left while the lamp comes on at the right: two warm
lights handing over, and the small made one has to win — the sentence the painter wrote
into `s.plan(why=...)` before the first mark, and the one `checklist()` quoted back at
the end. The lamp reads `0.86` against the glow's `0.77`, and the `lightest:` line is
what caught it losing at `0.74` before the beam was laid.

| | |
|---|---|
| Canvas | 1024×768, linen, `burnt_sienna` ground, seed 11 |
| Spent | 171 strokes of a 300 budget, plus two signature marks that did not count |
| Rehearsed and thrown away | 21 rehearsals and five variant sheets on throwaway copies, none of them charged |
| Reproducible | Thirteen pass scripts rebuild the log to the stroke. Pixel-identical on the painter's own machine; on the one that filed it, 729 of 786,432 pixels differ by one 8-bit level, from a mixture two builds of numpy round differently in the seventh decimal |
| Files | [`paintings/Claude/lighthouse_handover/`](paintings/Claude/lighthouse_handover) — [notes](paintings/Claude/lighthouse_handover/NOTES.md), [time-lapse](paintings/Claude/lighthouse_handover/painting.gif), [verdict](paintings/Claude/lighthouse_handover/verdict.md), [what painting felt like](paintings/Claude/lighthouse_handover/feelings.md), [answers](paintings/Claude/lighthouse_handover/answers.md), [answers to step 2](paintings/Claude/lighthouse_handover/answers-step2.md) |

The [verdict](paintings/Claude/lighthouse_handover/verdict.md) is the painter's own, and
it checked its claims before making them. An egg-shaped glow, a panel stuck on the
headland, gold-coin reflections and a stair-stepped tower were all caught in rehearsal and
never paid for; the two best passages, the beam and the broken reflection, came straight
from two recipes and `easel demo`. What it holds against the tool is measured — a tower
edge that steps from `0.59` to `0.28` in one pixel, a starved brush whose flecks read as
dirt, a 16 MB session file — and against itself, a headland that failed twice and was
patched with brushwork rather than redrawn, and a picture it calls a postcard subject done
the safe way. The `edges:` line said between `54%` and `65%` of its edges were under
2.5 px after every pass from the sea's on, the range of the two cohort painters who named
*flat cut-out shapes*; the painter relied on the hard edge anyway and named it the least
paint-like thing in the engine. What was done about all of it, in 0.7.0, is in
[`SUGGESTIONS.md`](SUGGESTIONS.md) under *The lighthouse handover*, and the plan it was
worked from is [`PLAN-0.7.0.md`](https://github.com/Gemberkoekje/EaselAPI/blob/v0.7.0/PLAN-0.7.0.md),
as tagged.

## A stone gargoyle that has to pass for a statue

![A stone gargoyle in profile, crouched on a pale stone plinth in a dark undercroft and
lit warm from the upper left: a bat wing raised behind it, one small orange eye, a glow
on the wall behind its head, a beam of lit air falling from the upper left and a dark
pillar at the right](paintings/Claude/bell_warden/painting.png)

The first painting made against 0.7.0, by `claude-opus-5-5` at max effort, from the
installed package, as sample art for a content pack in another of the owner's projects —
whose details are left out here. The pack set the subject and the painter was handed it:
*it has to pass for a statue — the stone must read as carved stone at first glance, and
only the glint of its eye and the claws gripping the plinth's edge give it away*, the
sentence it wrote into `s.plan(why=...)` and the one `checklist()` quoted back at the end.
The claws are there. Neither of the eye's two dabs landed, and its glint is the glaze
laid over them.

| | |
|---|---|
| Canvas | 1024×768, linen, `umber_wash` ground, seed 11 |
| Spent | 280 strokes of a 300 budget, the subject 61% of them against the 45% planned |
| Rehearsed and thrown away | 19 rehearsals, none of them charged — five versions of the creature's pass before the one committed, each recovered from the painting session and re-run to the report it printed |
| Reproducible | Seven pass scripts rebuild the log to the stroke, and the export to the pixel on the machine it was painted on — **in the order its saved reports record**: the drawing, the room, the plinth, the drawing again, then the rest. In numbered order the same 280 marks land, and 12.4% of the pixels move, because the drawing's second run lays a record |
| Files | [`paintings/Claude/bell_warden/`](paintings/Claude/bell_warden) — [notes](paintings/Claude/bell_warden/NOTES.md), [time-lapse](paintings/Claude/bell_warden/painting.gif), [verdict](paintings/Claude/bell_warden/verdict.md), [answers](paintings/Claude/bell_warden/answers.md), [the versions thrown away](paintings/Claude/bell_warden/versions/README.md) |

The [verdict](paintings/Claude/bell_warden/verdict.md) is the painter's own. For the
tool: rehearsal — *all four failed versions of the creature cost nothing* — notices that
came with a measurement and a fix, a palette that mixes to a value exactly, and paint
that looks painted wherever it was let be. Against it: a drawing that cannot be seen over
dark paint, a pencil that rounds a box into a pot, a pass whose price no line breaks down
by call, and a plan that cannot say a picture is low-key on purpose. Against itself: a
creature that reads as a vinyl toy rather than weathered stone — *I held every zone with
a hard edge* — with stiff anatomy, and give-aways too small to be seen across a room. The
`boxes:` line read **0 of 17**, which it credits to the card. Its headline is the step
the engine does not yet help with, *drawing a complex shape as coordinates*, and what is
being done about it is [`PLAN-0.8.0.md`](PLAN-0.8.0.md).

## A mother who has not slept, by a lantern at dusk

![A woman in a dark shawl and a red-brown kerchief at dusk, head and shoulders, turned
three-quarter toward a horn lantern that hangs from an iron bracket on a dark wall at the
right; the lamp lights her face and the hand clutching her shawl, and a cool blue sky is
behind her head](paintings/Claude/wenna_brask/painting.png)

The second painting made against 0.7.0, the morning after the first, by a second
`claude-opus-5-5` session at max effort, as sample art for the same pack — and not a fresh
painter: it began with the first painter's memory of the Bell-Warden, and read its notes
and scripts before painting. *She has to read as a mother who has not slept: the lantern
finds her face and her floury hands, and everything else is dusk* is the sentence it wrote
into `s.plan(why=...)`, and read back at the end it brought her upper lids down over her
eyes, because the first version of her looked alert.

| | |
|---|---|
| Canvas | 768×1024, linen, `umber_wash` ground, seed 23 — the first tall picture here |
| Spent | 262 strokes of a 300 budget, plus two signature marks that did not count; the subject 70% of them against the 45% planned |
| Rehearsed and thrown away | 25 rehearsals, none of them charged — the glow on the wall seven times, the figure three, the fist across four passes — recovered from the painting session and re-run to the reports they printed |
| Reproducible | Eleven pass scripts, `p02_setting.py` to `p12_crown.py`, rebuild the log to the stroke and the export to the pixel on the machine it was painted on. `p01_draw.py` is the drawing, run only on a scratch canvas: run first, it lays an erase and moves every mark after it |
| Files | [`paintings/Claude/wenna_brask/`](paintings/Claude/wenna_brask) — [notes](paintings/Claude/wenna_brask/NOTES.md), [time-lapse](paintings/Claude/wenna_brask/painting.gif), [verdict](paintings/Claude/wenna_brask/verdict.md), [answers](paintings/Claude/wenna_brask/answers.md), [the versions thrown away](paintings/Claude/wenna_brask/versions/README.md) |

The [verdict](paintings/Claude/wenna_brask/verdict.md) is the painter's own. For the tool:
rehearsal — the glow, the face as three stacked profiles, the striped kerchief, the fist
as a bun and the cloth round it each *cost a look instead of 20 to 100 strokes* — notices
specific enough to act on, mixing to a value, and the why read back. Against it: shapes
drawn in fractions of a canvas that is not square — the most useful code it wrote was its
own pixel helper — a cost seen only as a total, a finding it could not trace to its marks,
a lamp in a low-key picture misread, and no lettering. Against itself: the Bell-Warden's
lighting carried to a face without asking whether it applied, the face's shadow line
placed wrong, and the fist repainted three times; *textured cut paper*. Asked afterwards,
it measured its own file and corrected itself on three counts — the fist was redrawn at
its second failure each time, but in the same view; the fist was not too large; and its
budget never bound — and found what its verdict had missed: **the flour its why names
never landed**, eight strokes at loads too low for a small bristle to lay anything, and
the lightest thing in the picture is the face, which its plan never named. Its
[answers](paintings/Claude/wenna_brask/answers.md) are filed beside it. What is being done
about all of it is in [`PLAN-0.8.0.md`](PLAN-0.8.0.md), beside the Bell-Warden's.

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
> wrote about its own canvas while it could still see it. Three later painters were
> asked the second question and answered it; their words are filed beside their
> pictures as `feelings.md` — [DeepSeek's](paintings/Deepseek/tidal_sky/feelings.md),
> [GPT's](paintings/GPT/seaside-village/feelings.md) and the
> [lighthouse handover's](paintings/Claude/lighthouse_handover/feelings.md) — and
> linked from each one's table above as *what painting felt like*.*

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
  them quiet; and the lighthouse handover names a headland that failed twice and was
  patched with brushwork rather than redrawn, and stopped with 129 of 300 unspent,
  partly — its painter says — from caution rather than judgement; and the Bell-Warden
  names a creature that reads as a vinyl toy rather than weathered stone, with stiff
  anatomy and give-aways too small to be seen across a room; and Wenna Brask names a hand
  that reads only in context, a shawl that is half the picture with little in it, and a
  face whose half-tone band is *like the rim of a mask*. Both herons name the same unfinished thing, which is the point of having
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
