# A pair of hands sorting dried beans

Painted with `easel-paint` **0.4.0** installed from PyPI, working only from what the
package ships — `python -m easel guide`, `--full`, `--painting`, `--reference` and
`--recipes`. **The repository was not opened at any point**, and the session ran in an
empty directory: no checkout, no listing, nothing to read but the package. All nine
exercises were run before the first mass (`ex/`), exercise 9 with this painting's own
mixtures rather than the guide's.

`CALIBRATION.md` was never opened, so where a calibrated figure would have settled
something this session measured it again itself. So were `LESSONS.md`, `DIAGNOSIS.md`,
`README.md`, `PAINTINGS.md` and every earlier painting.

**To understand this, start by reading `prelude.py`** — the mixtures, the landmarks, and
every silhouette and plane — then `pass01_draw.py` through `pass28_sign.py` in numerical
order. Every pass was rehearsed with `--rehearse` and looked at before it was paid for.

## The plan, as numbers, before anything was mixed

| mass | planned | mix |
|---|---|---|
| table | 0.23 | `burnt_umber` + `burnt_sienna`, cooled with `ultramarine` |
| bowl, and the beans in it | 0.25 / 0.28 | the same dark, warmed |
| the cupped hand | 0.55 | `yellow_ochre` + `burnt_sienna` |
| the palm's hollow | 0.36 | that flesh, cooled |
| the picking hand's back | 0.62 | that flesh, desaturated |
| the pinch | 0.85 → 0.905 | flesh + `titanium_white` |

Ground `#5f4a39` (v=0.31) — **no preset was dark enough**. Most of this canvas is table
at 0.16–0.35, and the darkest preset below `toned_grey` is `umber_wash` at 0.43. A
custom ground at 0.31 sits *above* the table, so what breathes through reads as warm
wood rather than as holes. 1024×768, linen, seed 11. **329 of a 420 stroke budget**,
plus two signature marks that did not count. 114 rehearsal views across the session,
none of them charged. Bare ground at the end: **25.14%**. Subject share: **65%**, down
from 71% at the pinch, which is the direction the checklist asks for.

The value plan went through `compare({place: value})` on the empty canvas before the
first mass. It returned one touching pair inside `0.10` — the palm and its own forearm,
`0.05` apart — which was **accepted deliberately**: a wrist is not a boundary and an arm
should read as one thing. The forearm was later dropped to 0.44 anyway, for composition
rather than for the threshold.

## Why this subject, and what happened to the reason

Chosen before anything was installed, and written down: **old hands are warm and red at
the knuckles where the skin is thin over bone, and cooler and paler across the planes
between** — and that contrast, not the pose, is what keeps a picture of a grandmother's
hands out of sentimentality. Specificity was the whole reason.

That reason is **half in the picture**. The warm/cool contrast is there and it is a
glaze: laid as paint at any opacity worth having it is a pink stripe, and `PAINTING.md`'s
own table puts the window at 0.10–0.12 (`pass19_warmth.py`, which is the third attempt —
the first two are described below). What is not there is the specificity. The knuckles
are marks that *stand for* knuckles; nothing in this picture could only be an old hand.

The directory is `hands_beans` and not `grandmother_hands` on purpose: the grandmother is
not in the frame, and naming her in the filename would be the sentimentality arriving by
the back door.

## Decisions

- **The bowl was rewritten from cool to warm, and from light to nearly lost.** It began
  as a desaturated cerulean foil at 0.42 and was the loudest thing on the canvas — one
  cold mass in a warm picture pulls harder than its number predicts, and the greyscale
  view settled it: the bowl was the lightest mass in the painting and the subject was
  not. It is 0.25 now, warm-neutral, half lost into the table, with one grazed arc along
  the far rim. Its *contents* face the light; its outer wall does not. That was backwards
  the first time.
- **Two fingers are described and two are not.** Four fingers treated equally are four
  parallel bars and no brushwork rescues that — uniform, varied, broken and with core
  darks were all tried, and all four read as a grille. The lower two are knocked back
  into the palm's shadow in `pass13_darks.py`. Three fingertips are lost into the table
  and one is found (`pass26_beans.py`), which is the varied edge the checklist asks for;
  four lost is just a soft passage.
- **The limbs are how the subject enters, not the subject.** They had become a bright X
  across the canvas. `pass09_recede.py` walks each one down toward the table with dark
  glazes, hardest at the frame, using `to_value=` so the opacity is solved rather than
  guessed.
- **A correction of rank, not of drawing.** `pass16_knockback.py` exists because three
  passages had quietly become brighter than the subject. The two lit fingers were left
  alone — they sit beside the pinch and belong to the same focal cluster — and what was
  walked back is what had grown bright *far* from it: the bowl's rim, in a corner, and
  the broad plane on the back of the picking hand.
- **Four beans on the table.** The cheapest four marks in the painting and the ones that
  explain it. Sorting means some are put down.
- **Signed** with two small bean-shaped marks along the bottom edge, one set a little
  apart from the other: the picture's own gesture at the smallest size it survives, at
  0.25 on a 0.17 ground.

## Pitfalls, each of which cost a rehearsal and no strokes

- **A pale pass laid late is still in front of what it crosses.** The first fall of light
  on the table was a `scumble` over a polygon that reached the hands, and it buried the
  fingers whole. The guide warns about this twice.
- **`sample()` averages the place it is given, and says so confidently.** The background
  colour for a found edge was sampled with `span("C3","D4")`, which straddles hand and
  table; it came back **0.342** where the local table is **0.258**, and the edge painted
  with it landed as a pale halo above the hand. Sampled from a small patch known to be
  clear, it is right. This is the engine item in `SUGGESTIONS.md`.
- **A `scumble`'s polygon leaves its own boundary across the picture.** Replaced with
  overlapping strokes that lose their ends — no shape, no seam.
- **Driving a dark below 0.20 with `ultramarine` in the mix gives navy.** The first core
  shadows were blue slashes across the hands. Warm darks come from `burnt_umber` +
  `burnt_sienna`.
- **A starved bristle under `size=0.025` is confetti; a hard-edged `block_in` on the same
  shape is a smooth egg.** The back of the picking hand was built three times before
  solid crossed strokes with their ends running off the shape.
- **Four small round-tip marks in one small area are the tool printing itself**, whatever
  `tip_wobble` says. The first pinch was four white discs in a cluster. It is one spark
  now, and the knuckles were given a length instead.

## What it does not do

**The hands do not read as hands.** The gesture is legible — two hands, one reaching into
the other, over a bowl — and the anatomy is not. A viewer sees something organic over a
bowl. That is the painting's central failure and it is not marginal.

The root cause is a drawing decision made early and noticed late: **four near-parallel
fingers laid out sideways is the wrong view of a cupped hand**, which seen from the front
shows its fingers foreshortened and overlapping. The drawing was redone three times and
all three were fixes to the *arrangement* — framing, limb angles, the bowl's size. None
of them asked whether the view was right.

The second failure is worse, because the method covers the first. **About eighty strokes
went on treating symptoms.** Fingers read as bars, so the brushes were varied; still
bars, so the lights were broken; still bars, so core darks went in; still bars, so two
fingers were abandoned. Four treatments at the brush, and the fault was upstream in the
drawing the whole time — where moving it is free. The honest move at the second failure
was to go back to graphite.

Also true, and smaller: the range is narrow. The box runs 0.13 to 0.96 and most of this
picture sits between 0.20 and 0.55.

It stopped at **329 of 420 with the weakest passage still the weakest**. That stop was
deliberate — the cupped hand had been repainted four times and each attempt bought less
than the one before — but *deliberate* and *finished* are not the same word, and the
first one sounds better than what happened.

## Reproducible

**Not claimed.** The drawing pass was rewritten and re-run three times; `look` and
`probe` scripts ran as passes between the painting ones and were overwritten each time,
so they are not committed; `prelude.py` was edited between passes as mixtures were
rewritten; and each pass script was edited after its rehearsal and before it was
committed. What is here is the last version of each, not the sequence that built the
canvas. The `.easel` file replays byte for byte from its own log, which is the claim the
engine actually makes.
