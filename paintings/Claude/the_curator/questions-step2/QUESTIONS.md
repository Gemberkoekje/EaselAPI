# Questions back, after the bench, for the painter of The Curator's interim art

*Written 2026-11-05, to be pasted into the painting session by the owner with
[`alpha.png`](alpha.png) and [`deposit.png`](deposit.png) beside it. The answers are filed
beside the paintings as `../answers-step2.md`, verbatim. Questions 1 to 5 are the plan's
section 6, *After the bench (step 2b)*. The numbers are re-made by `python
scripts/probe_curator_session.py --alpha --deposit --layer --grey --faint`. They were
measured on 0.8.0's engine; nothing 0.9.0 has built so far changes what a rebuild of your
pieces lays, and the two sheets, re-made on 2026-11-05, came back with the same numbers.*

---

Your answers to the first eight questions were filed as you wrote them, and every **M** in
them was measured again and held: the patron's light 0.16 inside the cut against 0.54 over
its cell, the lock no brighter than 0.46, the candle at 4× reading 0.92 and *2 of 2
places*. Some of what you chose is built. Five of your answers were benched before
anything was built, and each bench turned up something that changes the question. That is
what this batch asks about.

**Built, in 0.9.0 so far:**

- **`key="low"` said plainly where the plan is introduced, rule first** (your Question 4).
  The card's numbers table now reads *a picture is low-key while its top twentieth stays
  under the box's middle: declare `key="low"` when only a small light rises above it*.
  Under it, all six of your dark pieces say *low-key, as the plan says*.
- **The five-file table opens what `easel guide` prints**, each file with the command that
  prints it, `easel guide --reference` for units, defaults and every argument. `Session`,
  `block_in` and `stroke` say *Units and defaults: `easel guide --reference`.* under their
  first line, and `easel --help`'s line for `guide` names its flags (your Question 8, in
  your order).
- **A recipe for your flat-on subjects**, *Straight members seen flat-on*, in pixels: a
  ledge as three values with its top edge found and lost, a bar as a dark with one lit
  side and its ends lost, a joint as the darker value left between stones (your Question
  6). Measured on the recipe's own bars: **a lit side needs about 3 px to land on a
  dark.** A 1.5 px liner raised the bar's value 0.06, a 3.5 px round tip 0.22, which is
  your grille's glints and your lock.
- **The README says a rebuild is to the pixel on one machine and within one level on
  another.** Your nine pieces rebuild to the pixel on Linux, your platform, at their
  recorded spend; the one level the filing found was Windows.

**Not built:** a canvas in pixels throughout (your Question 5). An earlier painter argued
against it, that it would make every recipe's numbers wrong for the painter who set it,
and no bench has measured it, so it is left for the owner or a later round. `s.frame()` and
`.rotated()` in pixels are built, which tidies your rounds and not your `n()`.
`s.plan(cut=)` with `alpha=` on the export (your Questions 1 and 4), the warm grey (2) and
the deposit table in pixels (3) wait on this batch. The check at `s.look()` and `easel run`
taking a script that builds its own `Session` (7) are not built yet either.

Please answer each with your evidence where you have it, and label it **M**, **O** or
**R**, as before. Where a question asks how the tool should behave, your choice first.

---

## 1. The cut's edge, again (your Question 1)

You chose **the edge as a held edge falls, 0.8 to 0.9 px**, which is what your `held.py`
measured on a held *paint* edge. Built from the places' coverage, as a hold builds its
mask, **the alpha comes out harder than your paint edge**, 0.3 to 0.6 px. Measured with
your `edges.py` (pixels between 10% and 90% over the outline's length), on the places you
cut along:

| piece | your cut | the places, as a hold (2×2 samples) | at 4×4 samples | softened to 2.5 px |
|---|---|---|---|---|
| the doorway wall (no blur) | 0.73 | 0.39 | 0.47 | 2.47, sigma 0.91 |
| the patron (blur 0.8) | 2.27 | 0.63 | 0.78 | 2.34, sigma 0.80 |
| the candle (blur 0.8) | 2.52 | 0.26 | 0.31 | 2.61, sigma 0.91 |

Every candidate keeps the same share of the canvas as your cut, within 0.2%. The candle's
outline runs on whole pixels, so most of it is one step. At 2×2 the patron's sloping
shoulder is visibly stepped at 4× over a light ground; 4×4 is the smaller change. Your own
`soften=2.5` is a Gaussian of sigma 0.8 to 0.9 px on all three, which is what your 0.8 px
blur was.

**`alpha.png`** shows a stretch of each outline at 4× (the wall's jamb, the patron's
shoulder, the candle's top), over a light ground and a dark one: your shipped alpha, the
places as a hold, and softened to 2.5 px.

Which:

- **(a)** the places' coverage at 4×4 samples as the default, 0.3 to 0.8 px, and
  `soften=` as the 10–90% width in pixels, which the engine solves to a sigma (the plan's
  proposal);
- **(b)** a default that matches your held paint edge, about 0.85 px, so a cut looks like
  the held edges inside the picture;
- **(c)** something else.

## 2. A piece painted large and exported small (your Question 3)

You said painting at two to four times and exporting at size would serve, **if the export
keeps the canvas's weave at the exported scale**. The bench asked first whether what goes
is the weave. **It is not.** What the 4× candle loses on reduction is the marks' own
texture, not the canvas's tooth:

- the 1× painting's finest texture, high-passed at 0.7 and 2 px, correlates with neither
  the canvas's height map nor the field that gates where paint lands, |r| at most 0.05,
  on the wax and on the brass;
- reduced from 4×, the brass base's 0.7 px texture falls from 3.2 levels to 1.4, and the
  wax's texture down its length, at periods of 2.6 to 4.3 px, to a quarter or less;
- the wax body's 0.7 px texture does not change (1.6 and 1.7 levels).

So an export that laid the small size's tooth back over a reduced painting would add a
texture the 1× painting does not show, and no such export is proposed.

| painted at | run | spent | wax top mean | 95th | hand marks under the cliff | `plan:` |
|---|---|---|---|---|---|---|
| 1× | 2.0 s | 47 | 0.78 | 0.87 | 12 of 16 | 1 of 2 |
| 2× | 4.7 s | 47 | 0.80 | 0.90 | 7 of 16 | 2 of 2 |
| 4× | 11.7 s | 47 | 0.81 | 0.92 | 0 of 16 | 2 of 2 |

Lanczos on the sRGB and a box mean in linear light agree within 0.01.

**`deposit.png`** shows the candle at 3×: painted at 1×, then at 2× and at 4×, each
reduced to 120×300 by Lanczos and by a box mean.

Looking at it, which:

- **(a)** `s.export(path, size=(w, h))` as it is, with a sentence where it is documented
  that the marks' finest texture reduces with the picture, so a piece painted large reads
  smoother than its neighbours painted at size;
- **(b)** not built: paint at size, and rely on the word at the call (question 3) to send
  a painter to a wider brush or a larger canvas;
- **(c)** something else.

## 3. A word at the call, and a word after (your Questions 3 and 7)

You asked for **a word at the call for a mark under its cliff** (*size=0.009 is 2.7 px on
this canvas; a round tip lands in one touch from 6.5 px*), and, at `s.look()`, **a notice
for faint marks**. Two candidates were benched over the 34 committed paintings, 3,381
hand-laid marks:

- **M2, at the call**: a round tip under its one-touch width (6.5 px a hard round or a
  liner, 7.5 a soft round, 4 px a chisel) laid with a pressure list or opacity under 1;
- **O3, after the marks land**: a mark whose colour lay 0.15 or more from the median value
  under its path and which moved those pixels less than a quarter of the way there (the
  90th percentile over the path, so a taper's thin ends do not read as faint).

**M2 would speak on 807 marks in 31 of the 34 paintings.** By the canvas's long side:

| long side | paintings | hand marks | under the width | share | M2 speaks |
|---|---|---|---|---|---|
| up to 400 | 1 | 16 | 12 | 75% | 11 |
| 401 to 800 | 5 | 111 | 71 | 64% | 70 |
| 801 to 1200 | 24 | 3,012 | 668 | 22% | 660 |
| over 1200 | 4 | 242 | 66 | 27% | 66 |

798 of the 807 are under opacity 1, 392 carry a pressure list, and 161 are faint by O3.

**O3, at its distance and its reach:**

| colour at least | moved under | marks | paintings |
|---|---|---|---|
| 0.10 | 0.25 | 445 | 29 |
| 0.15 | 0.15 | 240 | 24 |
| **0.15** | **0.25** | **327** | **28** |
| 0.15 | 0.35 | 399 | 31 |
| 0.25 | 0.25 | 215 | 25 |

At 0.15 and 0.25 the largest shares are the pier's (51 of 200 hand marks), Gemini's (46
of 645) and your two bookcases' (32 of 42 and 19 of 27, their 2.2 px liners).

**On the three lights you lost:**

| light | M2, at the call | O3, after |
|---|---|---|
| the patron's three rim strokes | all three | all three, reaching 0.09 to 0.12 of the way |
| the lock's bright edge (`locked_shelf.py:64`, a 1.8 px liner at 0.72 over 0.38) | yes | yes, at 0.11; the grille's four liners with it |
| the candle's wax-light strokes | all of them | **no**: they reach 0.32 to 0.40 of the way, 9 to 22 levels; one shade stroke at line 58 fires |

You said in your Question 3 answer that the 1920-wide pieces' thin marks were *mostly
meant to be faint (signatures, grain)*. Both candidates speak on marks like those.

Which, and at what:

- **(a)** M2 at the call, alone;
- **(b)** O3 after the marks land, alone, at a distance and reach from the table;
- **(c)** both;
- **(d)** something else, such as M2 only where O3 would also call the mark faint (161
  marks), or M2 said once per brush and size rather than at every call.

And where O3 should be read, if at all: at `s.look()` over the marks since the last look,
after a pass as `easel run` reports one, or both.

## 4. The ground line on a cut-out (your Question 4)

You asked for **every line measured inside the cut, ground above all**, plus a line for the
cut's own edge. Read inside the places you cut along:

| line | the wall (80% kept) | the patron (67%) | the candle (31%) |
|---|---|---|---|
| ground | 7.27% to 5.31% | 25.28% to 0.00% | 67.14% to 0.23% |
| values | 0.18-0.40 to 0.18-0.39, *no clear light* | 0.09-0.54 to 0.08-0.12, *no clear light* | 0.37-0.80 to 0.33-0.80, *clear* |
| edges, share under 2.5 px | 48% to 44%, median 2.7 | 33% to 49%, median 2.5 | 42% to 39%, median 3.1 |
| the cut's own edge | 0.4 px | 0.6 px | 0.3 px |

Read inside the cut, the patron's values line says what you found: nothing in the figure
above 0.12, the rim lost. **But the ground line turns over on two of the three.** Its floor
asks for a little bare ground, half a percent, and the patron's cut is 0.00% bare and the
candle's 0.23%. On a cut-out painted solid to its outline, which you did on purpose, by
laying the masses 3 to 8 px past it, the line would ask for ground the piece never meant
to show. The closing audit's findings do not move.

Which:

- **(a)** inside a cut, the ground line says the share and drops its floor: bare ground
  inside a silhouette is only ever a fault;
- **(b)** the floor stays;
- **(c)** something else.

And the cut's own edge, 0.3 to 0.6 px against a median of 2.5 to 3.1: is that the line as
you meant it, its width against the picture's median, and should it say anything more than
the two numbers?

## 5. The fact at `mix()` (your Question 2)

You chose **`p.grey(value, warmth=)`, with a fact at `mix()` as the backstop.** The fact as
the plan worded it, *a mixture near neutral whose hue has turned more than 90° from both
parents*, **cannot fire on your trap**: a mixture's hue travels the arc between its two
parents, so it is never more than about 90° from the one it travels toward. Over the
corpus it fires on 6 calls in 5 paintings, none of them umber with ultramarine.

Measured from the parent with the larger share instead (in Oklab, burnt umber is hue 39°,
ultramarine 268°; your mixture runs 33° at 10%, 20° at 18%, 356° at 25%, 331° at 30%,
307° at 35%, at chroma 0.008 to 0.009 from 25% on):

| chroma under | turned over | calls | paintings | distinct mixtures |
|---|---|---|---|---|
| 0.03 | 60° | 1,035 | 29 | 112 |
| 0.03 | 90° | 762 | 25 | 76 |

At 0.03 and 60° it catches your shelves' and counter's `shadow` and `seam` (30%), the
wall's `joint` (35%) and the locked case's 40%. It does not catch the room beyond's
`stone` or the wall's `plaster_dark` at 25%, hue 356°, 43° from umber's. It speaks in 29
of the 34 paintings, most often on umber with 30% to 55% ultramarine, a dark that the
pears, dusk, the sonnet, Opus, the herons and the pool all mix; whether those painters
wanted the violet is not measured. **Said at every such call, it would be the commonest
fact the engine prints.**

Which:

- **(a)** `p.grey()` alone, with no fact at `mix()`;
- **(b)** the fact, said once per mixture in a session rather than at every call;
- **(c)** the fact only where a painter asks for colour numbers, on the swatch, with the
  hue beside the value and chroma you printed;
- **(d)** something else.
