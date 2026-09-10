# LOG — cracked pot of white peonies

Session `own.easel`, 1024×768, linen, `umber_wash` ground, seed 7.
3415 strokes, 49 pass scripts, 62 looks, **1** rehearsal, one `undo(46)`.
Outputs: `final.png`, `timelapse.gif`.

## What I painted

What I named before I started: a cracked terracotta pot of overblown white peonies,
three fallen petals, bare wooden table; pot just left of centre in the lower third,
blooms leaning right into open dark space, petals scattered to the bottom right.

That is what is on the canvas. The arrangement survived intact; the subject only
half did — see the flaws.

## What I did

1. **Ground and far masses** (passes 1–8, ~700 strokes). Dark warm background, then
   the table. I repainted both **four times**. First attempt: a stippled "glow" and
   wavy stripes. Second: concentric ellipses that read as a bullseye. Third: bristle
   ribbons that printed parallel wavy stripes. Fourth: `flat` at `pressure="even"`
   with the modulation held under 0.02 of a value, which finally read as air rather
   than as a shape. Then I raised the table's far edge because the pot rim was landing
   exactly on it — a tangency I should have seen in the drawing.
2. **Drawing** (pencil, free). Landmarks, pot, bouquet silhouette, three petals.
   Looked at it, found the bouquet undersized and the tangency, redrew larger.
3. **Pot** (passes 9–12). Three attempts. The one that worked: solid mid terracotta,
   then eight overlapping steps across the form with `bristle`, then marks running
   *round* the cylinder to break the vertical joins, then the rim as far lip → inside
   → near lip, then the crack as a dark line with a light lip on one side.
4. **Foliage** (13–15). Two attempts; the first was turquoise and buried the rim.
5. **Blooms** (16–48, and this is where the session went). Roughly eight distinct
   approaches: flat blob masses, `sweep` round the outline, concentric arc "domes",
   radiating petal strokes, big described petals, scumble, dry brush, rim lobes.
6. **Fallen petals** (29–31). Three attempts: scribbles, then sticking plasters
   (`flat`), then round-tip tapered marks, which worked.
7. Signature, export.

## What the guide got right

- **"Look every 5 to 15 strokes."** Everything I fixed, I found by looking. Nothing
  I predicted about a mark before looking at it was reliable. This is the whole game.
- **Back to front, and the hollow-thing rule** — far edge, then the inside, then the
  near edge. The pot rim is the best-built thing in the picture and it is built
  entirely out of that one paragraph. Painted in that order the near lip's edge is a
  real edge and I drew none of it.
- **Toned ground**, and planning the three values as numbers with `value_of` before
  mixing. The 0.10 separation threshold is correct and useful: my background sits at
  0.134–0.168, table 0.144–0.30, blooms 0.40–0.95, and the greyscale reads cleanly.
- **The box has no black and does not need one.** `mix("ultramarine","burnt_umber",0.62)`
  at 0.134 was ample for a night-dark still life. I never reached for a supplied colour.
- **"A short `flat` or `knife` stroke is a rectangle. Small accents want `round_hard`."**
  Dead right, and I proved it the expensive way: my first fallen petals were `flat`
  strokes and came out as sticking plasters with square ends. Same three petals with
  `round_hard` and a `[0.3, 1.0, 0.3]` pressure list read as petals immediately.
- **"Don't let the canvas choose your stroke direction."** Every mass here is laid at
  an odd angle for that reason and the picture is better for it.
- **Paint over rather than undo.** Ninety-five percent of my repairs were paint. The
  one `undo` was for 46 marks that were unambiguously wrong.

## What the guide got wrong, or left out

1. **`smudge` at the "behaves" size does not behave.** CALIBRATION says
   `0.035–0.045` is safe. At `0.042` it dragged pale finger-lobes several cells long
   across my background and table — exactly the thumbprint effect the file attributes
   to `0.10`. It cost me a full repaint of two masses. The asymmetry warning is there;
   the size window is wrong. Treat anything above ~0.02 as needing a rehearsal.
2. **`overhang=0` does not stop the spill, and the guide implies it does.** It is
   offered in "The rest of the API" as the fix for two masses meeting at the same
   depth. It only pulls in the pass *ends*; the pass centres still stop at the
   boundary and the brush still spreads half its width past it. My table edge landed
   0.055 above where I put it, twice, before I worked that out. The "inset by half the
   brush" advice needs to be in the `overhang` paragraph, not only in the shapes section.
3. **`round_hard` for a mass scallops the mass's boundary.** The guide recommends it
   as "the tip that declares no axis" when a passage keeps coming out square. True —
   and it turns the silhouette into a row of circles. My background modulation came
   out as cartoon clouds. It trades squareness for scalloping; say so.
4. **`bristle` + `direction="axis"` on a curved `ribbon` prints parallel wavy stripes** —
   the exact failure the guide warns about two sections earlier ("the marks inside it
   are not parallel lines"), produced by a feature the guide recommends warmly.
5. **A `block_in` on a *small* shape serrates it.** The brush-to-mass ratio advice is
   about big masses being swallowed. The small-scale failure is different and not
   stated: on a shape 0.03 across, even a 0.008 brush lays only a few passes, and
   passes cut against a small curved boundary read as sawtooth teeth. Small shapes
   want one or two strokes, not a fill.
6. **`glaze` is much stronger than the example.** `glaze(opacity=0.16)` over a small
   area took my bud from value 0.50 to near-black in one call — a coat, not a film.
   CALIBRATION's `0.10` figure is nearer the truth; the guide's `0.15` example is not.
7. **Low `load` near a boundary leaves dirt that later passes cannot ignore.** The
   guide covers the speckled-film problem for whole passes. The case that actually bit
   me was low-load strokes laid *along* a boundary to soften it: they left a chalk
   outline round a background shape, and a crust of dark speckle on my lightest flower
   that took two passes to remove.
8. **The signature exemption did not happen.** Two marks carrying `note="signature"`
   took `stroke_count` from 3413 to 3415. Either the exemption is a convention for the
   painter's own bookkeeping or it is not implemented; the counter moved.
9. **`undo(n)` is expensive in wall-clock time, not just in principle.** `undo(46)` on
   a 3178-stroke session took several minutes, presumably replaying from the start.
   Worth a line, because it changes when you would reach for it.
10. **There is no guidance for painting without a reference, and that is the gap that
    cost me this painting.** Everything about precision — the grid, landmarks,
    `compare`, `prepare` — assumes a photograph. With nothing to copy, the only tool
    that helps is `rehearse`, and it is filed inside the reference workflow where it
    reads as optional. It is not optional: it is the *only* way to see a mark before
    paying for it, and with no reference it is the closest thing to one you have. I
    used it once in 3415 strokes, and that once saved me from a bad petal set. The
    guide should say plainly: with no reference, `rehearse` **is** your reference.

One more, smaller: **"look every 5 to 15 strokes" cannot be obeyed literally**, because
one `block_in` is 10–30 marks and the API gives you no way to look inside it. In
practice the rule is "look after every decision". Mine averaged one look per 55 strokes.

## My own mistakes, which were the larger half

- I spent ~530 strokes repainting background and table before the subject existed. Not
  the engine's fault: I kept reaching for procedural texture instead of deciding what
  the background was supposed to be. The version that worked was the plainest one.
- **I generated flower structure with code instead of judging marks.** Eight batches of
  30–100 procedural strokes, each with an unmistakable machine signature: concentric
  rings (cinnamon bun), radiating strokes (pinwheel), big radial petals (propeller),
  rim lobes (pom-poms). Each cost as much to remove as to make. A loop that places
  seventeen petals at even angles will always read as seventeen petals at even angles,
  whatever jitter you put on it.
- I twice cut into a finished mass with background strokes at a fixed radius, and twice
  gouged black holes in the thing I was cleaning up. Additive repair (paint the flower
  outward) is safe; subtractive repair at a computed radius is not.

## The painting, honestly

It works as a **tonal picture** and fails as a **flower painting**.

What is genuinely good: the value structure — dark ground, mid table and pot, the
bouquet as the one light mass — is clean and does the job a still life needs it to do.
The composition is sound: the pot sits where I said, the mass leans right into open
dark, the fallen petals carry the eye to the bottom-right corner and stop there. The
pot is the best-made object in it — it turns, it has a lit flank and a reflected light,
the rim reads as a rim with an inside, and the crack reads as a crack in a surface
rather than a line drawn on one. The fallen petals are small, warm, in shadow, and
correctly subordinate. The background is quiet and I stopped fiddling with it.

What is bad, and it is the subject: **the peony heads read as smooth pale eggs.** They
have form — they turn from a warm lit shoulder to a cool shadow flank — but they have
no petals. Every attempt to put petal structure in produced something worse than
nothing (pinwheel, propeller, pom-pom), and the version I shipped is the one where I
scrubbed all of it back out. The silhouettes are near-perfect ovals; nothing about them
says "overblown", which was the whole adjective in my subject sentence. A blowsy peony
is defined by its ragged edge and I have four smooth ones.

Also bad: the bud is a lollipop on a stick. The foliage is a token dark smear with two
green highlights and no leaf you could name. The edges are almost uniformly soft
everywhere — I passed the "some hard, some soft, one lost" checklist item at the
table's far edge and the pot's shadow side, and failed it completely inside the
bouquet, where every boundary has the same slightly-fuzzy quality. There is speckle
dirt still visible along the bottom edge of the right-hand bloom. The pale patch at
top-left of the background is a leftover I softened rather than removed. And the mark
variation in the heads is poor: a lot of same-size arcs.

If I painted it again I would spend a third of the strokes I spent, make the flower
heads out of six or eight hand-placed petals each — every one rehearsed before it was
spent — and let the rest of each head stay unresolved. The engine did not stop me
doing that. I did.

## The signature

Two short ticks in the bottom-right corner of the table, drawn with a `liner` at 0.005,
running upper-left to lower-right, in a value 0.045 above the wood they sit on.

They are the angle of the light. The entire picture is organised around one source in
the upper left — the pot's lit flank, the warm shoulder on each bloom, the cast shadow
running to the lower right, the lit edge on each fallen petal — and the mark is two
strokes lying parallel to those rays. It is not a letter and not a symbol; it is the
one fact the painting is built on, written down in the corner where it does no harm.
