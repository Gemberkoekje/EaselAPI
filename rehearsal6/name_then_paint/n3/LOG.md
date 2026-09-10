# LOG — a cracked white teacup on a windowsill

Session `own.easel`, 1024×768, linen, `toned_grey`, seed 7. 2066 strokes across ~30
scripts run with `easel run`, 47 looks, 3 previews, 2 rehearsals. No reference
photograph, no assisted mode — no `prepare()`, no `sketch()`, no `ref_shape()`. The
drawing is mine: seven landmarks and a set of arcs and béziers computed in the script,
erased once and redrawn.

## What I did

Named the subject before looking at anything, then painted it back to front.

1. **Ground and the far mass.** Toned grey, then the window glare over the upper two
   thirds. Three attempts: a shaped gradient (produced a hard bright oval — a halo), a
   set of value bands (produced a stack of slabs with chisel ends), and finally long
   veils that begin and end off the canvas, which worked.
2. **The sill.** One mid mass with a dark below it. Also three attempts before it stopped
   being stripes.
3. **The cast shadow** on the board, before the cup, so the cup would cover its near end.
4. **Landmarks, then pencil** — after the far masses were down, as the guide says.
5. **The cup, in its four depths**: whole silhouette → the inside → the tea → the near
   wall over both. Then the rim as a lit band, the wall modelled with strokes running
   down its own form, the handle, the tea's reflected window, the crack and the chip.
6. **Repairs.** More of these than of anything else.
7. Three highlights, one signature, export.

## What the guide got right

- **"Look every 5 to 15 strokes."** Every single failure in this painting was found by
  opening the PNG and none by thinking. Not one of my predictions about what a call
  would do survived contact with the image. This rule is the whole engine.
- **Back to front, and the hollow-object rule.** Far edge → inside → near edge gave me
  the cup's front lip as a real edge — the place where the near wall's paint stops and
  the tea still shows — for free, with no cutting-in anywhere. It is the best-built
  thing in the picture and it took four calls.
- **"A short `flat` or `knife` stroke is a rectangle."** True, and I ignored it three
  separate times: pale labels stuck on the sill, dark slots on the board, and a quilt
  of forty grey rectangles across the glass. Each cost a recovery pass.
- **"Do not let the canvas choose your stroke direction."** My first sill was four
  horizontal stripes and my second glare was a stack of bars with vertical ends, exactly
  as predicted, in the same session, twice.
- **Mixing to a *value*, not to a ratio.** The binary search from exercise 1 became a
  helper in nearly every script. It is the most useful thing in either file.
- **`preview` and `rehearse` are free and decisive.** One rehearsal settled the handle's
  thickness. When I stopped rehearsing I started losing strokes.
- **"Before you repaint a mass, look at what is standing on it."** I broke this twice:
  buried the handle under board texture once and under a smudge once, and buried the
  branches under a veil. Three of my most expensive passes.

## What it got wrong, or left out

**1. A shallow shape filled along its long axis comes back as its bounding box.** This
is the single biggest gap. My cup's interior — an ellipse 0.256 × 0.128 — blocked in
with a 0.022 `flat` brush at `direction=4` rendered as a *rectangle*, twice, and I
checked with `preview` that the shape itself was a true ellipse (area 0.0256 against a
box of 0.0326: exactly π/4). CALIBRATION says "keep the brush under about a fifth of the
mass's width"; I was at a *twelfth* of the width and still lost the silhouette, because
the dimension that matters is the extent **perpendicular to the passes** — five
near-horizontal chisel bars with end-spill fill the corners of anything shallow. The fix,
which is nowhere in either file: **run the passes across the shape's short axis.** At
`direction=90` the same ellipse came out as an ellipse.

**2. Nothing about a mark's length-to-width ratio.** The guide tells you `flat` short =
rectangle and that small accents want `round_hard`. It does not tell you that a
`round_hard` mark whose length is only two or three times its width is a **capsule** —
a fat lens that reads as a pebble. I paved my windowsill with gravel twice before working
out that a stroke needs a length of roughly seven times its width before it reads as a
brushstroke rather than an object. This belongs beside the other two mark-shape facts,
which are themselves scattered across two sections. Put them together:
*`flat` short is a rectangle; round and short is a pebble; `bristle` under 0.02 is four
streaks.*

**3. Corrections get one paragraph and they are most of the work.** "When something is
wrong, paint over it" is true and useless on its own, because a `block_in` laid over the
middle of a finished passage introduces **a new hard-edged rectangle wherever its own
boundary does not coincide with a real edge in the picture**. That was my most frequent
failure by a distance. The rules I had to find myself, and which would have saved me
several hundred strokes:
- repaint a region whose boundaries are *already* edges in the painting (I ended up
  re-blocking my three sill polygons four times because their boundaries were the sill's
  real ones);
- or repaint in *exactly the colour already there*, so the join cannot show;
- or cover with many small overlapping marks at scattered angles and near-identical
  values.
The "Put a number on it" section warns about burying what stands on a mass. It says
nothing about the correction's own silhouette, which is the harder problem.

**4. `smudge`'s stated window is optimistic.** CALIBRATION says 0.035–0.045 behaves. At
0.036 on the board it left four pale egg-shaped lobes that read as spillage. At 0.028 —
well inside the window — it **erased my handle**, dragging the cup's pale wall across it
until the handle was a ghost, and mushed the cup's lit edge into a double halo at the
same time. That was two passes to recover. My working rule after this painting: do not
smudge within reach of any feature smaller than about 0.08 of the canvas, at any size.
The asymmetry warning is right, but it is far too gentle about the magnitude.

**5. "Steps, then lose the joins" does not transfer to concentric shapes.** I followed it
by sweeping a band of intermediate value along a scaled-up ellipse and got a bright oval
**ring** — a drawn halo, the exact thing the guide spends a page telling you not to make.
The recipe is for rectangles laid side by side. Sweeping an intermediate value along a
closed boundary makes a ring, every time.

**6. Small things.** `ellipse(place, rx, ry)` accepts a bare `(x, y)` point and is
correct — the guide only shows `ellipse(span(...))`, and I wrongly blamed the constructor
before checking. And "look every 5 to 15 strokes" cannot be followed literally when the
guide's own arithmetic says one `block_in` is 10–30 strokes; in practice the unit is the
pass, not the stroke.

## The painting, honestly

It reads. Cover everything else and you see a chipped white teacup with cold tea in it,
on a windowsill, against a bright winter afternoon, its shadow going right. The subject
and the arrangement I named cold, before touching the engine, are both on the canvas.

The good parts are small and specific. The cup's construction is genuinely right — far
rim, inside, near lip, in that order — and the front lip against the dark tea is the one
edge in this painting that was properly earned rather than drawn. The pale streak of
reflected window lying on the tea is the only mark that says *liquid*, and it is worth
more than the two hundred strokes on either side of it. The crack and the chip are three
marks and do their whole job. The handle, on its third attempt, sits in space and lets
the board show through its loop.

The flaws are larger and there are more of them.

1. **The upper two thirds is dull.** It is a stack of soft horizontal veils. I wrote
   "flat light" into my own brief and then hid behind the phrase. A real window at the
   end of a winter day has more in it than this — a frame, a reflection, a temperature
   change across the glass. What is there is pale wallpaper with three good twigs on it,
   and it is over half the canvas.
2. **The board is nearly as empty.** I repainted it five times, each time to remove
   something worse than what I was replacing, and each reset took the surface with it.
   What survives is a quiet field with a dozen scuffs. Safe, not good. The right third
   of the picture is inert.
3. **The composition is three horizontal bands** — glass, board, dark — and the cup and
   its shadow are the only things that cross them. I tilted everything by a degree or
   two, which is not enough to count. Turn it on its side and it is stripes, which is
   precisely the test the guide's checklist proposes and precisely the answer it warns
   about.
4. **The cup is too clean for its own story.** "Left on a windowsill" means neglect.
   There is no stain ring inside above the tea line, no dust in the foot, no grease on
   the rim. The crack is the only sign of age and even that is tidy.
5. **The interior is too blue and too even**, and the two arcs I laid inside it are still
   legible as arcs. It reads slightly like water in a bowl rather than shadowed china.
6. **The light is only half believed.** I decided on a low sun to the left and behind the
   glass. The shadow obeys. The glare's bright area is a vague patch with no source, and
   the cup's left rim-light has no answering cool along its top. The modelling and the
   lighting are not the same decision.
7. **Some passages are noisy rather than described** — the join at the back of the board,
   the left of the sill. That is the residue of repairs, not brushwork, and it shows.
8. **Nothing is risked.** The darkest dark is 0.17 and the lightest light 0.94, and
   almost nothing in between lives near either end. The picture is quiet because I kept
   flinching, not because I chose quiet.

Of 2066 strokes I would put roughly seven hundred down to repairing my own mistakes. The
cup — the thing the painting is about — cost about two hundred and fifty. That ratio is
the honest summary of this session.

## The signature

One mark: a small crescent in the bottom-left corner, a single `liner` stroke on the dark
band, value 0.33 against 0.22 — visible if you look for it, invisible if you don't. I
chose an arc because this painting is made of nothing but ellipses at different angles —
the rim, the inner wall, the tea, the foot, the shadow, the handle's loop are all the
same curve seen six ways. The mark is that curve at its smallest, so it is the picture's
own unit rather than a name.
