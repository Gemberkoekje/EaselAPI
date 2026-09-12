# A lighthouse on a rocky headland at dusk

A painting made from `PAINTER.md` alone, with no reference photograph. The subject was
chosen before the guide or anything else in the repository was read: a lighthouse on
the left third, standing in a dark headland; the sun just gone down off the right edge,
so the afterglow sits at the right-hand horizon and its reflection lies under it; a
crescent moon above the glow; the tower's right side catching the last warm light while
its left side goes cool; the lamp lit, and its light in the air around the lantern.

- Canvas 1024×768, linen, `burnt_sienna` ground, seed 31.
- **184 strokes** of a 300 budget, plus one signature mark that did not count.
- Final painting: `painting.png`. Time-lapse: `painting.gif`.
- `prelude.py` holds the palette mixed to planned values, the masses as shapes, the
  written value plan and the budget split; `p1_sky.py` … `p10_sign.py` are the painting
  in order. Against a fresh `easel new painting.easel --size 1024x768 --texture linen
  --ground burnt_sienna --seed 31 --budget 300` those ten passes reproduce
  `painting.png` **byte for byte** — verified by sha256. `p0_plan.py`, `check.py` and
  `p11_export.py` paint nothing and are not part of that sequence.

## No assisted modes

There was no reference, so `prepare`, `sketch`, `ref_shape` and `ref_outline` were not
used and nothing was traced; `s.assisted` is empty. Every mass is a `polygon`, `blob`,
`ellipse` or `Region` written by hand and looked at with `preview()` before it was
filled. No pencil was laid: with nothing to measure against, the shapes were the
drawing, and the composition preview was how they got checked.

## The ground

`burnt_sienna` reads `0.45`, which is almost exactly the picture's middle value, and it
is warm under a picture whose big masses are cool. It flecks through the indigo at the
top of the sky like faint stars, through the pass gaps of the sea, and through the
rock, where it is most of what keeps a dark mass from being a hole.

## The plan, and what it cost

Values were written down first, as a `compare({place: value})` sheet in `prelude.py`:
sky top `0.30`, sky mid `0.46`, the glow `0.72`, the left horizon `0.60`, far sea
`0.50`, near sea `0.34`, rock `0.17`. The three carrying values were rock `0.16`, sea
`0.50` and glow `0.74`. Every mixture was made with `at_value()` and landed on its
number to the hundredth. Measured on the finished canvas, six of the seven places are
inside `0.10`. The glow sits at `-0.10` exactly: the band is a step quieter than
planned and is still the lightest large mass, which is what the plan was for. The left
horizon reads `-0.16`, and that is a miss in the plan rather than the painting: the
ridge was raised and made jagged after the sheet was written, so the place is now half
rock.

The split written before the first stroke: sky 50, sea 35, rocks 35, tower and lantern
75, halo and moon and beam 20, edges and finish 25, reserve 60. What was spent:

| Stage | Strokes | Share |
|---|---|---|
| Sky: underlayer, two passages, the afterglow as fading passes | 38 | 21% |
| Sea: two passages, the horizon, the reflection | 21 | 11% |
| Headland: mass and its three planes, crevices, dry brush | 41 | 22% |
| Tower: halo, mass, lit face, band, gallery, glass, posts, cap, lamp | 41 | 22% |
| Near boulder and the water's edge | 14 | 8% |
| Moon | 1 | 1% |
| Finishing: rock 15, sea and sky 10, tower 3 | 28 | 15% |

The subject was reached at stroke 100: a third of the budget, but 54% of the strokes
actually spent, and the tower got 24% of them against a planned 32%. The rocks overran
their share by six because the mass was built three times in rehearsal and the third
recipe had more parts. Nothing was repainted after it was committed: every one of the
recipes below was thrown away on a copy of the canvas.

## Rehearsing, and what it saved

Eighteen rehearsal runs, none charged. Everything here was found on a copy and never
cost a stroke:

- **The afterglow as an inward scumble on an ellipse came back as a solid yellow sun**,
  three times, with three brushes: the rings converge and fill the middle with the full
  colour whatever the brush. It became six horizontal passes that land with no pressure
  at the left and press on toward the right edge — a brightening with no outline at
  all — plus one straight stroke at the horizon.
- **The flat's wander scallops a scumble's band edges**; with the wander turned off the
  same passage was hard straight stripes, which is worse. The scallops stayed and read
  as thin cloud; two soft streaks across them at the end made that deliberate.
- **The horizon wandered.** One flat stroke with `jitter=0` along it is the only ruled
  line in the picture.
- **The reflection laid with a starved bristle was a row of dotted rectangles**; laid
  as six tapered marks alike it was stripes. It became five marks, no two the same
  length, opacity or colour, with a dark ripple across the widest.
- **The headland was built three times.** A bristle block-in flew past its own
  silhouette as hairs; a smoothed outline came back as a hull; facets laid on the mass
  — flat slabs, then bristle streaks — read as things stuck on it. What worked was a
  jagged unsmoothed outline with `edge="clean"`, and then the *planes the rock is made
  of* as three shapes tiling the mass: a narrow uneven strip under the ridge taking the
  sky's cool light, a seaward face taking the glow's warm light, a mid bulk between,
  all at full opacity and even pressure so they are planes and not stacks of passes.
- **The halo as an inward scumble came back as a dark cloud with a bulb in it.** Two
  glazes with the soft round tip, one wide and faint and one small and warmer, are the
  light in the air.
- **The tower's form as a pass ramp across it came out nearly flat, and once with the
  light on the wrong side.** The lit face is its own shape on top of the cool mass, with
  one half-strength stroke down the join. The red band is the same recipe.
- **The moon as a disc with a sky-coloured disc bitten out of it left a ghost.** It is
  one stroke: a tapered arc on the round tip, pressure `[0.05, 0.6, 1.0, 0.6, 0.05]`,
  the horns thinning to nothing.
- **The beam was rehearsed twice and dropped.** As a gold glaze it was a mustard stripe
  across the sky; faint enough not to be one, it was not there. The halo carries the
  light.
- The water's edge, laid on the rock, read as scribbles; moved to the water side of the
  boundary it reads as surf. Three dark cloud streaks at `0.42` read as wires; two soft
  ones at `0.50` read as cloud. The near ripples a step too dark were bars.

## Two things the engine did that the guide does not say

- **A raw `(r, g, b)` triple handed to the palette is read as sRGB, not linear.** The
  guide and the reference both say linear. The sky colour sampled from `s.canvas.rgb`
  for the first halo landed as a near-black ring, which is the dark cloud above. The
  moon pass encodes the sampled mean to sRGB by hand before assigning it.
- **A vertical pass stack starts at the right.** `scumble(place, a, b, direction=90)`
  puts `a` on the right-hand edge and `b` on the left, on a `Region` and on a
  `polygon` alike; measured with a red-to-blue scumble on a scratch session. The tower
  and band recipes stopped depending on it.

## What went right

- Back to front throughout: sky, sea, headland, tower, near boulders. Every edge on the
  tower is where its paint stops and the sky still shows, and the tower stands *in* the
  rock because the boulders went on after it.
- The value structure held from the first sky pass to the end: light glow, mid sea and
  sky, dark rock, with the lit face of the tower and the glass above the glow. The
  greyscale look reads without the colour.
- The edges vary. The tower's cool side is lost into the indigo at the top and found
  against the peach at the bottom, while its lit side does the opposite; the mid plane's
  lower edge on the rock was ruled and is now lost with one smudge along its straight
  length; the horizon and the silhouette of the headland are the hard ones.
- Small things are three marks or fewer: the lamp is a stamped dab, the moon one arc,
  the gallery one flat stroke with its chisel ends where a plate's ends are.

## What still bothers me

- The seaward face of the headland still shows the stack of strata it was laid in,
  under the cracks that cross it. It reads as rock, but as rock made of slabs.
- The lit face of the tower is chalky, and the vertical pass edges show in it. It is
  the second-lightest thing in the picture, as planned, and a little too clean for a
  tower at dusk.
- The water's edge along the seaward face is a thin pale broken line along a
  silhouette, which is the thing the guide says not to draw. It is surf, and it is
  also a line.
- 116 strokes unspent, and this time on purpose. Every mark I can name to spend them
  on is a correction to a passage that already reads, in the one corner of the picture
  that is already busy; the guide's rule that the last marks may not be corrections
  weighed more than the rule about leaving a third unspent. If I am wrong about that,
  the strata on the seaward face are where the strokes should go.

## The signature

One mark, in the near water at the bottom right, a step lighter than the sea it sits
on: a shallow arc on the round tip that thins to nothing at both ends. It is that
because the shape this session came to trust is the mark with no ends — the tool's own
shapes, a disc, a slab, a comb, a ring, were each thrown away in rehearsal at least
once, and the tapered arc is what the moon is made of. It lies in the water like a
ripple. It is not a name and it repairs nothing.
