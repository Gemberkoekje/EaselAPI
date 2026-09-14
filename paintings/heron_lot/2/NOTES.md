# A heron in a flooded parking lot, dawn — second attempt

**Start with `prelude.py`**: every mixture, shape and mass is a named function there
and the `passN_*.py` files are one line each. `probe_cover.py` is the measurement this
painting produced. The output is [`painting.png`](painting.png) and
[`painting.gif`](painting.gif). Painting 1 is in [`../1/`](../1); its `NOTES.md` is
the other half of this one.

1024×768, rough, custom ground `#6d635a` (0.394), seed 23. **253 of a 320 budget.**
Subject share **42%** at the moment the subject was finished, against a planned 40%.

## The experiment

Same subject, same engine, same painter — but with all five documentation files read
and painting 1's own post-mortem in hand. The question was which of the faults I named
were **lookup failures** and which were **judgement failures**.

| | painting 1 | painting 2 |
|---|---|---|
| strokes | 293 / 320 | 253 / 320 |
| subject share | 33% | 42% |
| subject's share of canvas | ~8.5% | ~11% |
| stroke at which the picture had a light mass | **217** | **16** |
| masses repainted | 0 | 0 |
| depth-order violations | 1 | 0 |
| passages abandoned after two rehearsals | 2 | 1 |

## What changed, and why

- **`compare({place: value})` on the empty canvas, twice, before a stroke.** It found
  two real merges and one piece of my own sloppiness — I had planned the bird as a
  single averaged value, which is meaningless. The plan that survived has no unintended
  merge in it. Painting 1's worst fault was `sky_hi` and `water_mid` planned `0.00`
  apart along the edge where they meet.
- **The composition lost its horizon.** A steep downward view: the water *is* the
  picture and the sky exists only as what it reflects, so there are no horizontal bands
  to fight. The bird spans the frame top to bottom with its reflection, and the stall
  lines radiate across everything.
- **The light went in with the ground.** The graded field is pass two. In painting 1 the
  greyscale had a dark and a mid and nothing else until stroke 217.
- **Two ramps, not one.** A single scumble made the whole field warm; splitting it gives
  warm at the horizon, cool in the middle where the water reflects the sky overhead, and
  warm-dark near where you look through to asphalt.
- **Every graded passage got its brush from the verb.** Painting 1's one hand-laid band
  is the passage I most disliked.
- **The reflection is pale, not dark** — a white bird in dark water reflects light. The
  plan had this wrong and the pairs check caught it mid-painting.

## The measurement this painting produced

**A solid block-in does not land its colour, and the oriented tips never do.** Bare
ground, `density=1.0, solid=True, opacity=1.0, pressure="even"` — every clause of
*a plane that is a plane* — a mixture at `0.865`:

| brush px (600px canvas) | `flat` | `bristle` | `round_hard` |
|---|---|---|---|
| 1.8 | 0.427 | 0.415 | 0.581 |
| 2.7 | **0.403** | 0.407 | 0.669 |
| 4.8 | 0.681 | 0.582 | 0.834 |
| 7.2 | 0.768 | 0.656 | 0.853 |
| 18.0 | 0.826 | 0.773 | 0.856 |

The ground is `0.394`. **Below about 4px a chisel lands the ground and nothing else**,
and even at 18px a `flat` is `0.04` short and a `bristle` `0.09` short — most of the
`0.10` that separates two masses. Only a round tip holds its colour small. This is why
the bird's head, laid at `size=0.005`, was a dark fuzzy ball for four rehearsals, and it
is probably also why painting 1's bill "bloomed pale". `probe_cover.py` reproduces it.

## What did not transfer

**The body is still a smooth pebble.** *A mass built of planes* says to decide the
tiling *with* the silhouette, before the block-in; I read that, wrote it in painting 1's
notes as the named fault, and then invented the planes in the pass again. Same failure,
both paintings, with the recipe open.

That is the useful result. Almost every improvement above was a **lookup** — a number or
a verb I did not have. The one fault that was a matter of **judgement** repeated itself
exactly.

## Honest comparison

Painting 2 is the better-made picture: braver composition, a real focal counterchange
(white head on the darkest mass, dark bill on the lightest), no depth violation, fewer
strokes for more subject. Painting 1 has the better single passage — its far edge is
genuinely lost across half the canvas, sky meeting water under the reading threshold,
and nothing here is as good as that. Painting 2 is also narrower in colour and its glow
band came out `0.15` below plan, so it is lower-key than intended.

**One measurement I tried and threw away.** I wanted to show painting 2's verb-picked
scumbles were smoother than painting 1's hand-laid band, and the across-band wobble says
the opposite — because it counts the rough ground's flecking as ripple, and painting 2
has far more ground showing through by design. The instrument does not separate pass
banding from canvas texture, so the number is not evidence either way and is not quoted.
The visual claim, marked as an observation: painting 1's band shows parallel ribbons in
its left half and painting 2's field shows none.

## The signature

The same two marks as painting 1, bottom right: a short vertical and the shorter broken
one the water gives back. Same hand, same thought, carried out a second time.
