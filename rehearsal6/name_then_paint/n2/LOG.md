# LOG — cracked pot of geraniums on a windowsill

Session `own.easel`, 1024×768, linen, `toned_warm_grey`, seed 11. 2057 strokes across
25 scripts. No reference photograph — everything here came out of the sentence I wrote
before I opened the guide:

> A single cracked terracotta pot of drooping geraniums on a windowsill, the red blooms
> still lit while the room behind falls into shadow. The pot sits slightly right of
> centre on a broad sill running across the lower third, backed by an open window whose
> light falls from the upper left and leaves the right side of the frame in deep
> interior dark.

Outputs: `final.png`, `timelapse.gif` (177 frames), 47 looks under `out/`.

---

## What I did

Planned the values as numbers before mixing anything — window 0.85–0.92, sill ramping
0.74 → 0.27 left to right, interior wall 0.15, terracotta 0.16–0.60, foliage 0.15–0.49,
blooms 0.29–0.63. Printed every mixture's hex and `value_of` twice before painting a
field of it. That was the single most useful habit of the session and it caught a real
error before it cost anything: my first sill plan sat at 0.85, the same value as the
window, and I only noticed because the number was on screen.

Then, back to front, one pass at a time, looking after every one:

1. The light outside the window (three bands, joins smudged).
2. Knocked that back — my first "outside" was a saturated teal that read as a seascape.
3. The interior wall, cut over the light, so the window's aperture is where the wall's
   paint stops. I never drew that edge.
4. The sill: top plane, front face, dark beneath, laid as value steps.
5. Rebuilt the sill — my step-then-smudge joins left five pale thumbprints.
6. Pencilled the pot and plant.
7–9. The pot: block, then form. Repainted it twice — first pass came out pink, second
   had no turn.
10. A mullion in the window and its shadow on the sill, to stop both being empty.
11–14. The plant: whole mass, then leaves, then rebuilt its light structure.
15. The blooms and three fallen petals.
16–17. The rim's near edge restated over the leaf bases; the crack and its chip.
18–20. Three attempts at the mullion's shadow.
21–24. The window's banding, the far dark, lost edges, and repairs to repairs.
25. One highlight that had landed on a leaf, moved onto the rim.

Depth order held throughout, including inside the pot: rim disc → dark interior →
body → plant → front lip restated over the stems' bases. That worked exactly as
described and gave me the lip's overhang for free.

I used `rehearse()` twice — once on the crack (two ways plus a control), once on the
shadow band. Both paid for themselves. The crack rehearsal told me my light edge was
too dark to read before I spent it; the shadow rehearsal told me `stroke` would work
where `block_in` had failed twice.

---

## What the guide got right

- **"Look every 5 to 15 strokes."** Correct, and not negotiable. Every single problem
  in this painting was found by looking, not one by predicting. Most of my passes are
  corrections to something I could not have known without the PNG in front of me.
- **Back to front.** The window's aperture, the rim's overhang, the leaves against the
  wall — all edges I got without drawing them. The "anything with an inside is three
  depths" rule mapped straight onto a flowerpot with a plant in it and was right.
- **"Repaint before the near things go on."** I repainted the sill and the pot twice
  each while they were still bare, and it cost nothing. The one time I forgot — a wall
  patch laid next to the window in pass 22 — it spilled a dark tongue into the light
  and took two more passes to undo.
- **Mix to a value, not to a ratio.** A bisection on `value_of` was the workhorse of
  this session.
- **"White is a weaker lightener than you expect"** and **"a yellow and a blue make
  green even when you were after a grey."** Both true and both cost me something. My
  first terracotta was `tint(tc, 0.52)` and came out salmon pink; the fix was to
  lighten with ochre-plus-white rather than white, which is the same lesson.
- **The 0.10 threshold**, and printing values before committing to a field.
- **"Do not let the canvas choose your stroke direction."** The passages I gave explicit
  angles look painted. Anywhere I let a default through, it looks like bars.
- **Shapes, not boxes, and inset for the spill.** The pot, the leaf clumps and the
  window's masses all held their silhouettes.
- **Smudge is stronger than it sounds and walks the light into the dark.** Painfully
  confirmed.

## What it got wrong, or left out

**1. The bristle floor. This was the most expensive thing in the session.**
The guide says bristle is "the workhorse for any mark with a direction" and mentions in
passing that below `size≈0.02` it is "four streaks with gaps". CALIBRATION explains why
(fixed 0.005 pitch). Neither says the thing you actually need: **never use bristle below
about `size=0.025` for anything that has to read as solid.** I used it at 0.008–0.014
three separate times — for a shadow band, for the sill's transition strips, for the
sill lip — and got back a woven strap, a ladder of rungs, and a dashed line. Three
passes lost. The guide's own tone pushes you toward bristle; the warning needs to be as
loud as the recommendation.

**2. A mass much longer than it is wide is a stroke, not a mass.**
The mullion's cast shadow is ~0.022 across and ~0.18 long. `block_in` combed it even
with `flat`, `pressure="even"`, `density=1.0`, `direction="axis"`. Twice. What finally
worked was three long `stroke()` calls and a soft one over the join. The guide's
vocabulary is "fill a shape" or "sweep an edge"; there is a third case it doesn't name,
and its answer is "stop calling it a mass".

**3. Painting a gap is not covered.**
The guide spends a lot of words telling you not to draw outlines and to let masses meet.
It never says that when you paint background *into* a foliage mass to break its
silhouette, a round mark reads as a floating disc, not a hole. I put four pale discs in
the plant and they looked like bubbles. A gap has to be a broken sliver *at* the
silhouette, laid with a starved brush. One pass lost.

**4. Steps-and-smudge is the weaker of the two gradient recipes the guide gives.**
Section 4 leads with "paint the gradient as steps and lose the joins" with `smudge`.
That produced five thumbprints across my sill on the first try, at sizes inside
CALIBRATION's supposedly safe 0.035–0.045 window — the window is optimistic when the
value step across the join is 0.20. What actually worked, and what the guide mentions
only glancingly, is **overlapping scumbles of the intermediate value across each join**.
That should be the headline recipe and smudge the footnote.

**5. The 3/4-brush shape spill bites hardest on small repair patches.**
The guide warns about this for masses you are building. But the shapes you make in a
hurry are *repairs*, and a `block_in` at `size=0.024` over a 0.09-wide patch throws
paint 0.018 outside it, which is how a wall patch ends up hanging in the middle of a
window. Worth saying where corrections are discussed, not only where shapes are.

**6. `s.mark()` labels are drawn on every look and there is no "hide" flag documented.**
`look(sketch=False)` hides the pencil; nothing hides the landmarks. You have to
`unmark` them one by one. Trivial, but I nearly exported with the labels on.

**7. And the guide's own warning about precision being paid for elsewhere is correct,
and I fell for it anyway.** I spent about a third of the session on the pot and on one
cast shadow. The window is a third of the canvas and never got resolved.

---

## The painting, honestly

**What works.** The value structure. In greyscale there is an unambiguous light mass, a
mid mass and a dark, and the picture reads with the colour taken away — which is the
one thing I would have wanted if I could only have one. The red against the dark wall is
the best passage and it is the thing the picture is about. The pot is decent: the
terracotta is a real terracotta and not an orange, it turns from light to core shadow
to a warm reflected edge, the lip overhangs and casts onto the body, and the crack and
the chip in the rim read at normal size without shouting. The mullion's shadow, on the
fourth attempt, does what it was for — it stops the left half of the sill being dead and
it explains where the light comes from.

**What doesn't.**

- **The window is a failure.** It is the largest light in the picture and it reads as
  scratchy horizontal weather, or as a distant sea, rather than as light coming into a
  room. I scumbled it three times; each pass made it busier without making it more
  luminous. There is still a faintly mismatched patch around the upper right of the
  aperture where a botched repair shows through. If I painted this again I would keep
  the window almost bare — two values, softly joined, nothing else — and let the plant
  do the work.
- **The leaves are lozenges.** Every one of them is the same short round stroke at a
  different angle and size. A geranium leaf is round, scalloped, and carries a dark
  zonal ring; none of that is here. Cover the flowers and this could be any shrub.
- **"Drooping" is not delivered.** It's in my own sentence and the painting does not say
  it. Four leaves over the rim and two hanging stalks is not a drooping plant; the mass
  reads upright, full and healthy. That is the biggest gap between what I said I would
  paint and what is on the canvas.
- **The sill's left half is under-painted** relative to everything else — a big pale
  field with four marks in it — and its right half is slabby, with rectangular patches
  still visible from the value strips.
- **Too many accidental horizontals.** The sill top/face join, the line under the sill,
  the boundaries between sill steps. I broke the worst of them; several survive.
- **The pot's lit left edge half-dissolves into the window reveal** — same value, same
  warm hue. I darkened the reveal twice and it is still the weakest edge on the subject.
- **2057 strokes is far too many.** The guide says a few hundred. Most of the excess is
  me repainting the same four passages, and the reason I had to repaint them is in the
  "what it got wrong" list above — but not all of it. Some of it is just not thinking
  before spending.

If I had one more hour: leave the pot alone entirely, repaint the window flat and quiet
in two values, and rebuild the plant as fewer, larger, scalloped leaf shapes with real
gaps and two stalks genuinely hanging below the rim.

## The signature

A small cross-tick at the lower left, on the sill's front face: one short downstroke
with a hook, and a shorter stroke laid across it. `liner`, `size` 0.004 and 0.0032, in a
value one step darker than the paint it sits on (0.295 against about 0.40), both marked
`note="signature"`.

I chose it because it isn't a letter and can't be read as one. It's the mark you make
with the wrong end of a brush in wet paint to say *this one is finished* — a tally, not
a name. I put it in the quietest corner of the picture, well away from anything that
matters, and kept it close enough in value that you have to go looking for it. Two marks
was enough; five would have been a decoration.
