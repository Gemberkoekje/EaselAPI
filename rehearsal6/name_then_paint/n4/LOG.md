# LOG — a cracked terracotta pot of rosemary on a windowsill

Session `own.easel`, 1200×900, linen, `toned_warm_grey`, seed 11. 2820 strokes,
32 scripts, ~40 looks. No reference — I named the subject before I knew anything
about the engine and then had to paint what I had said.

---

## What I did

Named the picture first: pot right of centre on the sill's front edge, shadow
running left, the window's pale rectangle filling the upper left. Then painted it
back to front: pane → wall → glazing bars → jamb → sill → cast shadow → the bush →
the pot (far lip → inside → soil and foliage → near lip) → sprigs spilling over the
rim in front → ten highlights → signature.

Two decisions did most of the work.

**Every colour was mixed to a target value, not to a ratio.** I wrote a bisection
helper on `palette.value_of` — `at(colour, 0.62)` mixes toward white or toward the
ultramarine/umber dark until it reads exactly 0.62 — and planned the whole picture
as numbers before mixing anything: pane 0.82, sill 0.62–0.74, wall 0.40, pot
0.23–0.60, foliage 0.17–0.52, under-sill 0.17. The greyscale view was right from
the first block-in and stayed right. This is the guide's step 3 taken literally and
it is the best advice in the file.

**The rosemary was grown, not drawn.** A recursive branch function: a stem is three
points with a bow and a sag, it subdivides at three fractions of its length with
random pruning, and colour is picked from a light function of position. The
silhouette is made *of* sprigs; nothing draws its outline. And `bristle` below about
`size=0.025` is four streaks with gaps — which is a needled sprig, for free. That is
implied by the comb table in CALIBRATION but never said, and it is the single best
thing I found.

The light: sun raking in from off-frame right, so the plant is dark against the
bright pane on the left and light against the dark wall on the right. That
counterchange is the only compositional idea in the picture and it survived.

---

## What the guide got right

- **"Look every 5 to 15 strokes."** Every failure below was found by looking. Not
  one was predicted. The loop is the whole method.
- **Back to front buys edges.** The jamb covering a torn glass/wall join, the sill
  covering the pane's ragged bottom, the pot covering its own contact shadow — all
  exactly as promised, all free.
- **"Anything with an inside is three masses."** The pot's rim did not read as an
  opening until I laid far lip → dark → contents → near lip in that order. Painted
  any other way it is a dark slot in a pale band.
- **Mixed darks, no black.** Never came near needing a supplied colour; the floor at
  0.13 was never the constraint.
- **"The mass that needed no drawing is the one that will give you away."** Dead
  right, and expensive: roughly 1200 of my 2820 strokes were the wall and the pane,
  repainted five times between them.
- **Highlights last and few.** Ten marks. They carry more than the two hundred
  before them.

---

## What it got wrong, or left out

**1. `smudge` is not a blender, and CALIBRATION's window is wrong.** It says
`0.035–0.045` "behaves". It does not. On any boundary with real contrast it drags
finger-lobes 0.05–0.08 long that read as thumbprints and are permanent. At 0.011 on
the pot it still left pale sausages. Worse, the guide's worked recipe for a
gradient — *paint steps, then walk each join with a smudge* — is the advice that
cost me the most in this session. I followed it on the pane, the wall and the pot
and had to repaint the mass every time.

**What actually works is not in the guide:** lay the gradient as *many overlapping
strokes at closely spaced values*. The pot's body is 27 passes stepping about a
hundredth of a value each, following the taper; every smooth transition in this
picture is that, and none of them is a smudge. "There is no gradient tool" is true;
the substitute the guide offers is worse than the obvious one.

**2. A smudge must run ALONG an edge, never across it.** Both worked examples do,
but neither says so, and "walk each join once" reads as an instruction to cross it.
Crossing a join with ten short smudges gives you a comb of ten fingers. I did this
and it looked like a fringe.

**3. `load` below ~0.6 does not feather anything.** I reached for dry brush three
times to soften a transition. `flat` at `load=0.5` prints a fine, *even* speckled
film over the whole shape and leaves the silhouette perfectly hard. The guide warns
that low load leaves a speckled film; it does not say that low load is useless for
the job you will reach for it to do.

**4. Stacked parallel glazes are stripes.** Five `glaze(opacity=0.13)` strokes laid
parallel across the wall came out as a venetian blind. A glaze is a *mark with a
direction you can see*, not a wash. Two non-parallel ones are fine.

**5. `load_falloff=0.0` is buried in the wrong file.** The guide says don't lay one
broken pass across the whole canvas; I did it anyway on the sill face and got a
band of gravel. The fix is one keyword and it is in CALIBRATION under *Load and
run-out*, nowhere near the warning.

**6. The real omission: there is no procedure for repairing a mass with things
standing on it.** The guide warns about this four times and is right every time. I
did it anyway **four separate times** — a jamb strip painted straight down through
the pot, a glass field that buried the transom and the plant's whole left fringe, a
`rebuild_sill()` that painted a light band across the middle of the standing pot.
Warning is not method. The warnings did not stop me because the correction I wanted
was always geometrically larger than the damage it fixed, and the arithmetic that
would have told me so is never spelled out.

What eventually worked, and what the guide should say: **keep every mass in a named
function, keep the near things in named functions too, and re-run the whole stack in
depth order instead of patching.** "Repair around them, shaping the correction to
what is still bare" is one clause; it deserves the weight given to back-to-front,
because it *is* back-to-front applied to the second half of a painting.

**7. `block_in` on a polygon leaves a stair-stepped silhouette** at the scale of the
brush. The guide calls the spill "the ragged edge you want" — true for a plant,
false for a windowpane, where it reads as torn paper. The real answer (plan so that
every straight boundary gets covered by a nearer mass) follows from step 2 but is
never drawn out.

**8. `blob`'s signature is inconsistent** between the API list (`blob(place, radius,
wobble, seed)`) and exercise 8 (`blob(point, 0.16, 0.30, wobble=…)`, two radii). I
guessed the two-radius form and it worked.

**9. "A few hundred marks, not a few thousand."** Mine is 2820. That is not a budget
I blew; it is a measure of how much of this session was correction rather than
painting. About 40% of it was repainting things I had already painted.

---

## The painting, honestly

It reads. From across the room it is unmistakably a pot of rosemary on a sill with
the light behind it, and the counterchange works. The greyscale has three clean,
separated masses. The pot is the best thing in it — it turns, it sits, the rim is an
opening, the crack is warm and lost at both ends instead of drawn, and the chalky
bloom and the chipped lip earn their keep.

The flaws, worst first:

- **The pane is a third of the canvas and it is empty.** Not quiet — empty. Three
  attempts at dust, gradation and a hint of something outside each made it worse and
  I retreated to a flat field. That is a hole in the picture and I did not solve it.
- **The rosemary is a texture, not a plant.** The branching is real and the
  silhouette is genuinely built from sprigs, but at any distance it is a uniform
  furry mat at one density. Real rosemary has clumps, holes and light falling
  through it in patches. I gave it a left-to-right value ramp and nothing else.
- **Nearly every edge is the same hardness.** I have three lost edges (the plant's
  top-right into the dark wall corner, the far end of the cast shadow, the sill's
  left). Everything else — sill against face, sill against glass, pot against sill,
  wall against jamb — is crisp. This is the checklist question I fail hardest, and
  it is the one the guide says separates a painting from a diagram.
- **The bottom fifth is dead.** A flat dark band with two faint glazes in it.
- **The sill is stratified** — horizontal bands of value that never became one
  receding plane. The left third is visibly slabs.
- **The light is a rescue, not a decision.** I named "window upper left" and "shadow
  running left" in the same breath, which only works if the sun is off-frame to the
  right. It is internally consistent and it gave me the counterchange, but I chose
  the lighting to save a sentence rather than because it was the best light for the
  subject.
- The plant's right edge trails off the frame in thin sprigs that still read a
  little like debris; the glazing bars are too regular and their speckled edges look
  dotted rather than wooden.

If I painted it again I would spend the strokes I wasted on the wall on the pane and
on breaking the plant into clumps, and I would touch `smudge` once, at the end, on
one edge.

---

## The signature

One small hooked liner mark in the bottom-right dark, value 0.275 on 0.175 — a
sprig, the shape I made more of than anything else here, reduced to a single stroke.
It is close enough in value to sit inside the dark rather than on it, and small
enough that it does the picture no harm. I chose it because the sprig is the only
mark in this painting I actually learned to make.
