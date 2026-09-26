# The key -- open after Part 1

## The letters

| sheet | letters |
|---|---|
| 4a, the thumbnails | **W** 96 px on the long side, **X** 192, **Y** 256, **Z** 128 |
| 4b, the guides | **E** the cased line with its casing at 150 of 255, **F** today's line, **G** an ink chosen per pixel -- graphite over what is lighter than `0.45`, the casing's colour over what is darker -- and **H** the cased line with its casing opaque |
| 9a, the terminators | **A** the two copies held at `feather=0.012`, **B** the copies laid with a soft round brush, **C** your pass as you painted it, **D** your pass and a smudge along each terminator, **E** the copies held at `feather=0.03`, **F** your pass and a half-value join stroke along each terminator, **G** the copies' own edges left ragged, held to the body alone |
| 10a, the darks | **P** every dark under `0.20` laid further down, the box's floor at `0.07`; **Q** your painting |

## What the bench read in the same pictures

These are one eye's readings, and a number's where there is one. Where you read a picture
otherwise, say so: that is the answer the round is asking for.

### 4a -- the thumbnails

Every thumbnail took 14 to 36 ms to draw at the canvas's size, and nothing against the
budget. Read here, each at its own size and not enlarged: **the cat's two peaks are there
at W and plain as ears from Z up**; the piebald's scatter of light islands shows at every
size; **the arch's lit band wrapped round the body reads only from X up**, and at W and Z
is a paler body. The bench's own pick for a default is X, 192 px, the smallest at which all
four read; Z, 128, reads three of them.

The silhouettes alone -- every mass of the creature in one dark on a light ground, the
recipe's `thumbnail({shape: dark})` -- are `labelled/thumbnail_silhouettes_128.png`. The
union of your first drawing reads as a small spiky blob; the cat as a cat; the piebald, the
arch and the committed pass share one outline, as they should: their faults were inside it.

### 4b -- the guides

Over the 35 grounds the bench drew your seventeen guides on -- the seven ground presets
bare, a flat mid-grey, your canvas after the room and finished, Wenna Brask's finished
canvas, and every committed painting's picture, both of this round's among them -- **the
share of the line's pixels that step the value by less than `0.25`**, the plan's target for
a line that reads:

| candidate | median over the 35 | worst |
|---|---|---|
| F, today's line | 88% | 100% |
| H, the casing opaque | 0% | 0% |
| E, the casing at 150 | 0% | 0% |
| G, the ink per pixel | 2% | 100% -- on the burnt sienna ground, whose value sits at the ink's switch |

Over your canvas after the room, today's line steps the value by a median `0.026`, and 96%
of its pixels by under `0.05`: the drawing you could not see. Read here: H is the most
legible and the loudest -- a white line with a dark core on the dark canvas, and a double
line on the grey; **E reads everywhere and gives way to the paint most**; G reads best of
all where it works and breaks where the paint crosses its switch. The notes are boxed in
E, G and H.

### 9a -- the terminators

The step across each terminator, 10 to 90% of the way, in pixels along the line's normal,
the median over the line; and the silhouette's own step:

| | strokes | lit to mid | mid to shade | silhouette | at 1440x960: lit to mid, mid to shade, silhouette |
|---|---|---|---|---|---|
| C, as you painted it | 102 | 0.5 | 1.0 | 0.5 | 1.0, 0.5, 1.0 |
| A, `feather=0.012` | 102 | 0.5 | 10.0 | 0.5 | 2.8, 10.5, 1.0 |
| E, `feather=0.03` | 102 | 14.8 | 14.5 | 1.5 | 15.0, 16.0, 1.5 |
| G, the copies ragged | 102 | 9.2 | 2.5 | 1.0 | 7.5, 4.0, 1.0 |
| F, a join | 111 | 9.0 | 10.5 | 0.5 | 14.0, 14.0, 1.0 |
| D, a smudge | 111 | 2.0 | 17.5 | 1.0 | 20.5, 20.5, 1.0 |
| B, soft copies | 102 | 0.5 | 1.0 | 0.5 | 1.0, 1.0, 1.0 |

The join is nine strokes, one along each run of a copy's outline that lies inside the body,
four pixels or more from its edge -- five runs of the mid copy's outline, four of the
shade's. D said `smudge-across` and `smudge-long` at the call. Read here: **F turns the form
and keeps the silhouette**; A and E read as a speckled band along every held edge, and E
breaks the silhouette with them; G is a staircase down the terminator; D softens it into a
smear; B is C again, because a soft brush held hard is held hard.

### 10a -- the darks

P lays the darks lower: its darkest hundredth reads `0.122` against your `0.157`, and a
quarter of its canvas is under `0.15` against a hundredth of yours. **But your planned
darks move down together**: the wall and the floor, both planned at `0.17`, read `0.17` and
`0.18` in Q and `0.15` and `0.16` in P, still `0.01` apart. What a darker dark separates is
only what was already apart -- your room's mixtures, mixed from `0.15` to `0.21`, would have
run from `0.11` to `0.21`. Read here: P is a darker picture with the same arrangement of
darks. Five other low-key pictures of the corpus, re-laid the same way, are in
`numbers/`.

## What the bench recommends, for you to overrule

- **4**: the thumbnail at 192 px when no size is given; places as the plan reads them, and
  a colour's value where a colour is given; with no argument, the plan's places **and the
  masses the painting has laid** -- your plan named none of the creature. No drawing over it.
- **4b**: the cased line with its casing translucent, E. Not a look of the drawing alone.
- **9**: F, the join, as the recipe's step after the copies; the sentence on `feather=`
  as the plan writes it.
- **10**: no black this round -- the room wanted its darks planned apart.
- **D**: name them: a line after a pass, printed only when the pass laid a mark that landed
  nothing, with its line in the script and the cause the engine can see.
- **5f**: keep the median for `plan:`, and read a named light at its 95th percentile for
  `lightest:`, printed beside its median -- what the second painter asked for.
