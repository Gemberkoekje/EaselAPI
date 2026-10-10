# Answers to the questions after filing

*Uktarl's Room, answered 2026-10-10 in the painting's own session. The evidence comes from
the session file `uktarl.easel`, its 46 saved reports (`easel log --reports -n 100`, kept
as `out/all_reports.txt`), the log's records and the export. **M** means measured, **O**
observed, **R** reasoned. The figures are Uktarl; the lady (the bandit in the black wig);
the doppelganger; and the near bandit (hooded, back to us).*

## First: where the five points change my verdict

- **Low-key (G).** I misread the documents; the tool was right. When I weighed
  `key="low"` in the session, I decided it meant "nothing above 0.35 at the top
  twentieth". That is the *example* in REFERENCE.md's `key=` row, not the rule. The rule
  is in the same row, but only as the condition for leaving the key: "once the top
  twentieth rises past the middle". **(O)**
- **The mountain (my seventh point).** I blamed the facets' shape, but it was the
  direction I gave them. What would have caught it is `direction-default`'s comparison
  applied to a direction I named, not only to one left off. 88 strokes against 31 is
  2.8×, past its 2.5× line. The collar point stands. **(R, on the owner's numbers)**
- **The discs.** There are 20 face marks, not 21: I had counted the ridge with them.
  **(M, in C)**
- **The label.** The `sun` landmark was my own leftover from the first drawing pass. I
  never unmarked it. **(O)**
- **The filtering.** This one matters most. My verdict said the habit warnings misfired
  "often enough that I stopped reading them". The truth is simpler and worse. From the
  body's second rehearsal on, I grep-filtered every run but one, so I never saw most of
  them. The reports show what I filtered away, including one fact that was right (C).

## A: painting outside a shape. **R**, with **M** on the edge

**`clip_out=` alone would have done all of the painting.** Eight calls were held by three
polygons I typed by hand to share Uktarl's outline: seven in `p08_backlight.py` and the
glare in `p15_light_edges.py`. The polygons are `glow_left`, `glow_right` and
`glow_above`, about 45 points between them. Each call would have been
`clip=wall, clip_out=uktarl`. `intersection()` I had no use for: `clip=` with a list
already does it for paint. **(O, from the scripts)**

**`difference()` I would have used only for places that are read, not painted.** Two
examples:
- The backlight's colour was mixed from `s.sample()` of a small ellipse I placed by hand
  beside him.
- The plan's light place had to be moved onto a single ray, because I could not name
  "the relief round his head". That place is a ring, so it has a hole, and the proposal
  would refuse it.

For a place that is only measured (plan, sample, thumbnail, compare), a hole does no
harm. I would let those take one and keep the refusal for the mass verbs. **(R)**

**The figure's edge should be held, not softened, and held tighter than any hold today.**
I measured across the cape's left edge at four rows (y = 460, 490, 520 and 550):
- The backlight reads 0.43 to 0.45, and the cape reads 0.14.
- The light stops 1 to 3 px short of the cape, leaving a seam of the wall as it was
  before the light, at 0.22 to 0.25.
- That seam is the default feather, breaking the hold inward, into the light.
- At the wing's outer edge, the light comes within a pixel of the edge. **(M)**

A soft hold there would widen the seam into a dark ring round him. That is the opposite
of backlight, where the wall nearest the figure is the brightest. So `clip_out=` should
not break into the paint it holds. Either let its break fall on the figure's side of the
line, where nothing more will land, or give it a feather of 0 by default. **(R)**

## B: the soft edge. **O** for the list, **R** for the rest

These are the edges I would soften, looked at over the export at 1:1 and 2×
(`out/edges_2x.png`):

| Edge | Soften over | Why |
|---|---|---|
| The lit planes' edges inside the faces: the lady's terminator, the doppelganger's, Uktarl's far cheek | 8 px | A face here is about 45 px across, and skin turns over about a sixth of it (see I). |
| The lady's far side: the plum dress against the dark relief | 10–12 px | It turns away from both lights. I smudged 80 px of it by hand. |
| The lady's wig against the relief | 3 px | Hair. |
| The doppelganger's far side, against the relief and the tub | 8–10 px | As for the lady; also smudged by hand. |
| The near bandit's hood and shoulders, where no rim light falls | 6–8 px | It is the nearest thing in the picture, and dark on dark. |
| The mountain's outline at the far ends, in the dark corners | 3–4 px | Crisp only where the lamp is. |
| The ends of the six crag strokes | 4–6 px | They read as slabs laid on top. |
| The blanket heap against the tub's far wall | 2–3 px | Cloth. |

Kept crisp: Uktarl's whole silhouette against the glow, the collar, the wing's hem, the
rays, every lit rim, the table's far edge, the candle and the cards. **(O)**

**Each hold its own softness.** Every soft edge on that list belongs to a call with a
second hold that must stay crisp:
- The lady's lit plane was `edge="hard", clip=a_face`. It should be soft at the
  terminator and crisp at the face's outline against the wig.
- The cape's lit lining was `edge="hard", clip=uk_wing`. It should be soft where the cloth
  turns and crisp at the hem.

One softness for the whole call would soften the silhouette too. The documents already
say the same thing against `feather=`. **(O, from the scripts; R)**

**Units: a fraction of the long side, like `size` and `feather=`.** Write it
`soft=s.px_size(8)` in the examples. I thought in pixels throughout, but `s.px_size()`
already converts, and one unit for every length the brush and the holds take is worth
more than my habit. **(R)**

**A soft hold, not a priced verb.** Every edge in the table is decided when its mass is
laid; none of them is a repair. My two smudges were repairs of edges that should have
been laid soft in the first place. If only one is built, build the hold. **(R)**

## C: a habit declared. **M**

**What the check said and what I saw.** The 46 saved reports hold 39 finding lines. From
the body's second rehearsal on, only one run printed them unfiltered: the near bandit's
commit. The 29 runs I filtered printed 29 findings. I read two of them again in that one
unfiltered run; the other 27 went unread:
- *one disc printed*, 17 times: every face, the candle, the relief, the cards and the
  signature;
- *a stack of bars*, 6 times: the vertical passes of the doppelganger, the lady and their
  laps;
- the **fact** `chisel-pressure` and its habit twin, twice each, on the six crag strokes.
  These are flat strokes given a pressure list, which "come back a rectangle with a
  lighter end". The check was right: they are the "slabs laid on top" in B's table. I
  learned this from the reports, nine days late. **(M)**

**Why I filtered: the standing lines.** Of the 246 standing lines printed, 150 (61%) were
word for word the line before them. "No clear light" was printed in 43 of the 46
reports. **(M)** The findings were a few lines buried under six that repeat. A smaller
fix than any rule change: print a standing line only when it changes, and print the
findings above it. **(R)**

**Which habits I would have declared.**
- **The disc habit, per place and not per painting:** the three faces and the fan of
  cards. Per painting would also have silenced it on the candle and the relief, and those
  are places where printed marks are a real risk. My first dwarves were two alike
  upright marks to a cave, and they read as eyes. The rule never saw them: they carried
  `tip_wobble=0.4` and came in pairs. **(O)**
- **The bars habit: none.** Its six findings were vertical passes inside solid masses. At
  4× the faces do show faint vertical striping from those passes (see I). So the warning
  was not wrong; it just did not say where. **(O)**

**The disc rule itself.** I rebuilt it from the log and tried three discriminators. The
candidates are the painting's 37 marks that are round-tipped, laid by hand, under
`0.02`, with no wobble, and under seven times as long as they are wide. My replica flags
30 of them in five places: the three faces, the candle and the fan of cards. The check's
own count is 28 to 33. **(M)**

| Discriminator | Result | |
|---|---|---|
| A pressure list or three points exempts a mark | 4 still flagged | It exempts marks for how they were laid, not how they look: a loop of identical strokes with `pressure=[0.5, 1, 0.6]` would pass. **(M, then R)** |
| Alike in length, width, direction and value (±30%, ±20%, ±20°, ±0.10) | 12 still flagged | A face's features really are a set of small dark horizontal marks and small light dots. **(M)** |
| Near-copies, three or more (width ±8%, length ±12%, direction ±8°, value ±0.04) | nothing flagged | See below. **(M)** |

The near-copy test finds only pairs: each face's two eyes, Uktarl's two glints and two
fangs, and two of the fan's pips. A pair is not a print run. A row of printed dabs is
copies by construction, so the test would still catch one. At looser tolerances (±12%,
±20%, ±12°, ±0.06), Uktarl's two glints and two fangs join into a group of four. **(M)**

So my answer is something else: **near-copies, three or more, measured on what landed,
plus the per-place declaration for what that measure cannot know.** **(R)**

## D: a local frame. **R**, with **M** on rotation

Instead of `hp()`, `dp()` and `ah()` I would have written:

```python
head = s.frame(s.px(512, 344), 24, 34, tilt=-6)
eye = head.at(-0.42, -0.10)        # a point
plane = head.polygon(points)       # a plane, in head units
```

That replaces all three helpers exactly: each was a centre, two radii and a tilt.

**It replaces their outline functions only in part.** Each lit plane was an arc of the
head's outline plus the terminator's points, so the two shared an edge exactly:
`uk_face_lit = poly_px(head_arc(-26, 168, 20) + UK_TERM[::-1][1:-1])`. In local units
that arc is one list comprehension over cos and sin. The chin's taper and the
doppelganger's dome were my own warps, and I would keep them mine. What I would ask for
is `head.arc(t0, t1, n)`: the outline's own points in local units, so an arc and a
terminator meet without retyping. **(R)**

**Pixels, and above all rotation in pixel space.** Turned in fractions on this 4:3
canvas, a 100 px square comes back skewed:
- tilted 6°, it comes back at 4.5°, with a 93.5° corner;
- tilted 30°, it comes back at 23.4°, with a 104° corner and sides of 94 and 109 px.
  **(M, computed)**

A frame's tilt, and `.rotated()` on shapes and groups, must turn in pixels whatever unit
they are handed.

## E: a share for each part. **M** for what I spent, **R** for the split

**Of the budget.** A share of the marks so far measures the order I painted in. After his
head, Uktarl's 102 marks were 48% of the 212 laid. By the card game that had fallen to
29%, while he got one mark more. Of the budget he had 23% at that point, under the 30% I
planned, while the line said "48% against 30% planned". **(M)** I discounted it at the
time, because I knew it would fall. That means it told me nothing I could act on.
**(O)**

What I spent on each part, from the pass totals and the script lines, against what I
would have planned:

| Part | Spent | Of 450 | I would have planned |
|---|---|---|---|
| Uktarl | 117 | 26% | 25% (112) |
| The doppelganger | 53 | 12% | 11% (50) |
| The lady | 47 | 10% | 11% (50) |
| The near bandit | 22 | 5% | 10% (45) |
| The relief: wall, rays, mountain, lamplight | 108 | 24% | 25% (112) |
| The table and the game | 34 | 8% | 8% (36) |
| The floor and the tub | 29 | 6% | 5% (22) |
| Left in hand | 40 | 9% | 5% (23) |

**(M; R for the last column)** The plan I would have written is close to what I did,
with one exception. The near bandit was painted last at half its share, with 40 strokes
in hand that could have been its own. A line saying "near bandit: 22 of 45" at the end
would have sent them there. **(R)**

## F: passes outside a clip. **R**, with **M** on the stakes

**The stakes in this painting were small.** One committed pass fell outside its clip:
record 186, the far cheek. One rehearsal of the floor had nine, from a diagonal mass
clipped to half a polygon, and I rebuilt it as two polygons before committing. The price
taught me a construction, not a picture: the clipped version would have looked the
same. **(M; O)**

**Skip them, if the random stream can be kept.**
- A pass that falls wholly outside its clip lays exactly nothing, so skipping its paint
  changes no pixel.
- What moves the later marks is the random stream. If a skipped pass draws and discards
  the same randomness it would have used, nothing after it moves, and an old script
  rebuilds to the pixel. Only its stroke count falls, which `older-engine` can say.
- If the stream cannot be kept, do not skip them. A rebuild that moves is worse than a
  stroke charged for nothing.
- Either way, keep naming them under `landed nothing:`, as "skipped, not charged", so the
  geometry is still told.
- Passes that are only partly outside should stay as they are. **(R)**

## G: a dark picture's light. **(1), and (2) as well.** **O** for (1), **R** for the rest

**(1) is not optional.** I misread the example as the rule (see the first section), and
one sentence where `key=` is introduced would have stopped me: *"A picture is low-key
while its top twentieth stays under the box's middle, 0.54."* With it, I would have
declared `key="low"` in the prelude, because the picture was planned dark around one
light. **(O; R)**

**(2) catches the painter who never reads that row, at the moment it matters.** From the
head's pass on, the line would have said that Uktarl's face stood clear, 0.69 against
0.50, and pointed at the declaration. That is the information I wanted, and the engine
does not have to change what the line judges to give it. **(R)**

**Not (3).** Judging the light under any key with nothing declared makes `key=` pointless
for the light, and moves the judgment from what the painter declared to what the engine
guesses. My own form was a fix for a misreading. **(R)**

## H: the documentation. **O** for what I used, **R** for the card and the cuts

These are all the rules I used, in one line each.

*Method.*
- Decide the subject, and write why, before looking at examples.
- Draw first: guides are free. Take a thumbnail at the planned values before any paint.
- Lay masses back to front. Anything you can see into is far edge, then inside, then near
  edge.
- Plan values as numbers with `at_value`. Two masses within 0.10 read as one. Plan a
  light at the value its place will read.
- Rehearse every pass, and read `dearest:` and `landed nothing:`.
- Keep every mass a named shape in the prelude.
- Look in values, and look small.

*Masses.*
- A plane is flat, `solid=True`, opacity 1, even pressure, laid along its own axis.
- Use a shape, not a box.
- `edge="hard"` ends a mass on its outline; `clip=` holds a call inside another shape; a
  list of clips intersects.
- Lay each mass along its own length: the direction sets both the price and the grain.
- A block-in costs a stroke per pass.

*Light and form.*
- A form turned toward the light is a shadow mass, then a half-tone and a lit plane
  sharing one edge, joined at the halfway value. Form marks go on at about 0.22.
- A light's pool on a dark surface is three soft strokes, each smaller and lighter, mixed
  from the surface: +0.10, +0.17, +0.24.
- Lit air is glazes close to the field's own value, with `dry()` before and after.
- Light multiplies, so after a pool, re-strike the lit part of the pattern under it.

*Marks.*
- A round dab under about 6.5 px lands nothing at one touch; `press=3` lands from 2.5 px.
- A bristle under load 0.5 lays nothing: read `easel log` for NO PAINT LANDED.
- Pressure changes a chisel's paint, not its width.
- Vary repeated small marks.
- A hollow thing gets one broken catch-light on its near rim.

*Space, edges, finish.*
- For straight edges, write the projection.
- A smudge loses a stretch of edge under a tenth of the canvas, once; past that, paint
  across it.
- Highlights go last.
- Up to five signature marks are free.
- Then answer the three closing questions.

*Units.*
- Coordinates run 0 to 1; `size` is a fraction of the long side.
- `s.px` and `s.px_size` convert from pixels.
- An ellipse's radii are fractions of the width and the height, so use `s.px(rx, ry)`.

With the call signatures, that is two pages.

**The one-page card must hold:**
- the loop: draw, thumbnail, rehearse, read the whole check, commit, look small;
- the seven steps of the order of work, one line each;
- about fifteen calls, with only the arguments that change the result;
- the numbers that bite: 0.10; 0.128; 6.5 px and 2.5 px; load 0.5; the halfway join;
  0.22; +0.10/+0.17/+0.24; a tenth of the canvas; low-key under 0.54; five signature
  marks; a stroke per pass;
- where to go next: RECIPES.md for any passage you have not laid before, and
  `easel explain` for a code.

**From *The first hour* I would cut:**
- *And six failures, painted*, down to its one command;
- *When you think it is finished*, which the end of the file says again;
- the anecdote under the sentence about RECIPES.md, keeping the instruction;
- "Say a place; do not compute a coordinate". `s.px()` and the last two painters'
  drawings now contradict it.

In their place I would put one sentence: **read every line the check prints after a
pass; do not filter it.** I knew that rule. It is in my own notes from the earlier
paintings, and I still broke it in 29 of 30 runs. **(O)**

## I: the join on skin. **M**, **O**

At 1:1 it reads as a facet.
- **The lady.** Across three rows, the step from shade (0.30 to 0.37) to light (0.55 to
  0.60) happens within 1 to 2 px, with almost no value in between. My join did not bridge
  it, because I mixed it from the half-tone and the light, at about 0.62. It should have
  been halfway between the two planes it joins, about 0.54. So it merged into the light.
  That was my error, not the recipe's.
- **The doppelganger.** Joined at the right value, its step became an intermediate band 1
  to 3 px wide. That is still a facet.
- **Uktarl.** His terminator sits under the wig, and his far-cheek band is about 2 px
  wide, so his face reads as a flat lit oval. **(M, value profiles across each
  terminator)**

At 4×, all three faces look like folded paper masks: one flat shaded strip with a hard
boundary, plus faint vertical striping from the passes. **(O, `out/heads_4x.png`)**

**Why.** A join at `size=0.006` is about 4 to 6 px wide, and a cheek on a face 45 px
across turns over about a sixth of it, around 8 px. Skin would want a join about twice
as wide, at the halfway value, or the lit plane's own edge held soft over about 8 px.
That second option is the first row of B's table. **(R)**
