# What Easel has painted

> Four pictures, each painted by a language model working from the guide — no reference
> photograph, no human hand on the canvas, nothing traced. Every mark is a call to this
> API and every one of them is in the log. This file is the record: what was painted,
> what it cost, what failed, and how good the results actually are.

The engine's claim is that a model can paint rather than generate, so the engine is only
worth what has been painted with it. These are those paintings, at full size, with the
parts that did not work left in.

**If you are about to paint from the guide: have you decided what to paint?** All four
pictures here name a subject, and a named subject chooses for you — six of six fresh
sessions once painted a noun the guide had merely listed in passing. **Decide first,
then read this page.** A painter who chose before opening the repository cannot be
steered by a noun in a worked example, and one who has not chosen can be; that is the
whole of the rule, and it is the protocol in [`LESSONS.md`](LESSONS.md) rather than a
matter of taste. `PAINTER.md` points here on exactly the same condition.

Having decided, read them: the pass scripts beside each painting are the end-to-end
worked example the guide cannot be, and the third painter here said it would not have
arrived at their convention on its own.

## The rules all four were made under

- The subject was chosen **before** the guide was read, so the picture was not steered
  towards what the engine happens to be good at.
- **How much else was read varies, and it matters.** The pears session read
  `PAINTER.md` and nothing else in the repository, which makes it the only clean
  measurement of the guide on its own. The car wash read `README.md`, `LESSONS.md` and
  `CALIBRATION.md` first; the lighthouse at dusk read those, `PAINTINGS.md`, and both
  earlier paintings' notes and scripts, and took its pass-script convention, its prelude
  of masses as functions and its `compare()` plan sheet from them rather than from the
  guide; the greenhouse read the four guide files and that lighthouse's prelude and
  notes, and took the same convention from it at one further remove. So where they
  agree, that is four painters finding the same thing with increasing context — and
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
using the guide, which all three have since added to and every item of which is done.

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

## A lighthouse half way through becoming a greenhouse

![A lighthouse in thick fog, half converted into a greenhouse: the lamp room at the top
is packed with dark tomato vine pressing against the glass, terracotta pots stand on the
turns of the outside stair spiralling down the tower, and the lamp still throws a
green-tinted beam out across a foggy sea](paintings/lighthouse_greenhouse/painting.png)

Somebody is growing tomatoes in the lantern. The vine fills the glass and presses
against it, pots come down the outside stair, a creeper has gone up the shaft on its
own — and the lamp is still turning, so the beam that crosses the fog comes out through
the leaves and arrives green.

| | |
|---|---|
| Canvas | 1120×860, linen, `toned_warm_grey` ground, seed 41 |
| Spent | 296 strokes of a 300 budget, plus one signature mark that did not count |
| Rehearsed and thrown away | Every pass, most of them three or four times; 92 rehearsal images, none charged |
| Reproducible | Eleven pass scripts rebuild the PNG **byte for byte**, verified by sha256 |
| Files | [`paintings/lighthouse_greenhouse/`](paintings/lighthouse_greenhouse) — [notes](paintings/lighthouse_greenhouse/NOTES.md), [time-lapse](paintings/lighthouse_greenhouse/painting.gif) |

This one had the beam the earlier lighthouse rehearsed twice and dropped, and got it for
the same reason that one could not: a beam over clear sky has only a glaze, and a beam
in fog is a mass of lit air. What it cost was two rehearsals spent discovering that the
green the subject asks for, mixed straight, is a chartreuse searchlight that owns the
picture — the fix being hue, not opacity, which the calibration says plainly and a
painter believed only after seeing it. The [notes](paintings/lighthouse_greenhouse/NOTES.md)
also record three flat slabs where a cylinder should have turned, a `flat` tip
staircasing down every sloping plane edge it was given, ten pots that came back as ten
bricks until each got a rim, a lit band held a hair inside its silhouette so that the
dark left over read as a drawn outline, and `direction` left off two shaped block-ins —
which would have been charged 44 and 57 passes against the 9 and 9 they were costed at.
All eight places of its value plan finished inside `0.10`.

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
- None of the four is finished in the sense a painter would mean. The car wash left 94
  strokes unspent and names the passage it did not know how to solve; the pears left
  three rims that are three similar yellow stripes; the lighthouse at dusk stopped with
  116 unspent on purpose and says which passage they should have gone to if that was
  wrong; the greenhouse spent all but four of its budget and still names its rock as a
  passage made better rather than good, and says why the fault was upstream of the paint.

## Further

- [`README.md`](README.md) — what the engine is and how to install it.
- [`PAINTER.md`](PAINTER.md) — the guide all three painters read: the method, in one
  file meant to be held in the head.
- [`PAINTING.md`](PAINTING.md) — the same rules with their reasons, the failures behind
  them and the numbers.
- [`RECIPES.md`](RECIPES.md) — the procedures these three paintings produced, collected:
  the calls in order, and what each looks like when it goes wrong.
- [`REFERENCE.md`](REFERENCE.md) — every fact on one page: units, defaults, and what
  each argument does.
- [`LESSONS.md`](LESSONS.md) — what six measured runs and an adversarial review left
  behind.
- [`CALIBRATION.md`](CALIBRATION.md) — the measured numbers behind the guide's rules.
