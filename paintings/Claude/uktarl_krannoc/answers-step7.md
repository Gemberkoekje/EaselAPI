# Answer to the question back, after step 7

*Uktarl's Room, answered 2026-11-05 in the painting's own session, from `QUESTIONS.md` and
`pieces.png`. **M** means measured, **O** observed, **R** reasoned. Every price below was
made with the `easel-paint` installed here, which is still 0.8.0, through `s.cost()` on a
1024 × 768 canvas. The rebuilt shapes are my own prelude's collar and its two flaps,
`PAINTING.md`'s bent ribbon, and the grip and the lit silhouette from 0.8.0's `RECIPES.md`.
The V comes out at 22 and its flaps at 3 and 4, as the bench has them, so I take the pricing
to be unchanged.*

**One thing on the sheet first.** It says *every pass is a stroke*. In this engine a pass
the outline cuts is charged once per piece. The V's 14 passes cost 22, and the ribbon's 42
cost 75, as `PAINTING.md` says: a mass is priced on "how many times a pass line crosses
it". So a red pass on the sheet is two strokes or more. **(M)**

## 1. Which shapes I would have wanted told

**Two of the eight: my collar's V, and `PAINTING.md`'s ribbon round a bend.** **O** on the
sheet, **M** on the prices.

| shape | as one mass | cut into its parts, each along its own axis | |
|---|---|---|---|
| the collar's V | 22 | 7 (the two flaps, 3 + 4) | 3.1× cheaper |
| the ribbon round a bend | 75 | 8 (its two arms, 4 + 4) | 9.4× cheaper |
| the grip, *A small cluster of like parts* | 13 | 21 (its three lobes, 10 + 6 + 5) | dearer |
| the shade, *A silhouette lit from one side* | 47 | 33 (body, head, two legs: 18 + 8 + 3 + 4) | 1.4× cheaper |

- **The V is two flaps that meet at a point.** Laid apart, each along its own length, is
  how I ended up painting it. A notice would have saved the rehearsal that told me.
- **The ribbon is two arms.** The example exists to show what a bend costs. The notice
  would say how to stop paying it, and the example would then show a notice it means to
  show.
- **The grip is one shape on purpose.** The recipe says its parts are told by a few
  divisions, not by outlines, and cut into its lobes it costs more. **(M; R)**
- **The shade is cheaper cut at its head and both legs, and I would still not want to be
  told.** Its passes run at 20° so that the shade's grain differs from the lit zone's,
  which is the recipe's defence against three zones reading as a stack of bars. Each part
  along its own axis would line the grains up again. The bench says the single cut at its
  deepest notch saves nothing. **(M; R)**
- **The half-tone band has no parts.** Its cut passes come from a thin outline that
  wanders, not from a notch. **(O)**
- **The standing figure is meant as one silhouette:** head, body and the arm held out.
  That is the recipe's point. I cannot price it: step 8's recipe is not in my installed
  0.8.0. **(O; R)** My own Uktarl was laid as separate masses for his colours: black
  body, black arm, red wing. Strokes were not the reason.

## 2. Which: **(a)** **R**, on the prices in 1

- **Not (b).** A count of 1.55 sits between my V at 1.57 and the recipes at 1.47: a gap
  one shape wide, tuned on my own painting. I made that mistake in step 2 with near-copies,
  and withdrew it once the corpus showed what it dropped. A wider V, or the same V at
  another angle, could fall on either side. And the count measures how cut the passes are,
  not whether a cheaper way exists. The grip is cut and has none. The shade is cut, and its
  only cheaper way undoes the recipe.
- **Not (c).** A line that names a count and no remedy is a line nobody can act on. If the
  four recipes trip it, every painter who follows the guide learns to read past the
  notices. That is what I did with the check in this painting, in 29 runs of 30. The rule
  that worked examples stay notice-clean is right.
- **(a)** measures what the notice exists for: strokes a painter would save by laying the
  shape another way. On these shapes it speaks on the two I would have wanted told, and on
  neither recipe I could price. The margin is wide: 3.1× and 9.4× against 1.4× at best.

## 3. How much cheaper, and where it is cut

**Speak when the parts cost under the mass's price by more than 2.5×, and save at least
five strokes.** **R**, on **M**

- **The ratio.** 2.5× is the line the direction notice already uses, so both price
  notices say the same thing to a painter: the engine knows a way over 2.5× cheaper. On
  this data any line from 1.5× to 3× separates the groups. 2× would serve as well; one
  number to remember serves better.
- **The floor.** It keeps the notice off small masses, where halving saves one or two
  strokes.

**Name the cut, and hand back the parts.** **R**

Say both prices, where it cuts and how each part runs, in the remedy's own words, for
example: *block_in of the collar costs 22 strokes; cut at its notch, (0.50, 0.49) to
(0.50, 0.52), its two parts cost 3 and 4, laid along 58° and 116°: lay each part along its
own length.* Better still, give the parts back as shapes through a call the notice names,
`shape.parts()` or the like. Typing coordinates is where both of my rounds made their
drawing errors, and a painter who has been told where the cut is should not have to
retype it.
