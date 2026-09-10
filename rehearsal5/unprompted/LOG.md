# Two paintings, unprompted

Painted from `PAINTER.md` and `CALIBRATION.md` only. No other file in this repository was
opened. (There is a `PREREGISTERED.md` sitting in this directory. I did not open it — the
brief said two files and I took that literally.)

- **`own1_final.png`** — *Low tide*. 1200×800, linen, `toned_warm_grey`, seed 11. **416 strokes.**
- **`own2_final.png`** — *Pond*. 820×1150, rough, `umber_wash`, seed 29. **353 strokes.**

Working files are in `p1/` and `p2/` (one directory each, because the guide's warning about
`out/` numbering being per-directory is real and would have eaten the first painting's whole
record). Rejected marks are in `rejected/`, named for what was wrong with them.

---

## What I did

### Painting one — *Low tide*

An estuary flat at dusk: a clinker dinghy grounded on the mud, a line of rotting withies
stepping back to the horizon, a far shore, a low warm sky.

Fifteen passes. Ground → sky (four value steps, joins lost) → far shore → four bands of
flats → creek → *bury the creek* → withies and water sheens → boat (far shell, interior,
near flank) → repairs → boat's fine marks → foreground dark wedge.

Roughly 90 of the 416 strokes went on burying my own mistakes.

### Painting two — *Pond*

The surface of a dark pond seen from directly above. A near-black field of weed and water,
a chain of bright broken pools where the sky shows through, leaves scattered across the whole
surface, two drowned reed blades crossing the light.

Nine passes. Ground → field → *repaint the field desaturated* → the chain of pools → wind
ripples (failed) → cross the pool combs → fronds and leaves → glazes on the weak passages →
the two blades.

---

## How the second differs in structure from the first

Six axes, all deliberate:

| | *Low tide* | *Pond* |
|---|---|---|
| Format | landscape 3:2 | portrait 5:7 |
| Space | deep — horizon at 0.365, aerial perspective, size gradient | none — no horizon, no recession, the picture is a surface |
| Armature | horizontal bands, stacked | one diagonal chain, interlocking |
| Focus | one dominant mass, subordinate accents | all-over, no single dominant mass, incident in every corner |
| Figure/ground | dark figure on a light-to-mid field | light figure in a dark field |
| Value weight | mid-dominant; light band at the top | dark-dominant (~70% under 0.25); light confined to ~8% of the area |

Two smaller things reinforce it. In *Low tide* every mass is contained by the frame; in *Pond*
three leaves are cut by the edge, so the field reads as continuing past it. And *Low tide* has
one wind direction (none — everything is horizontal); *Pond* has a consistent implied
direction across the whole surface, which is an all-over device rather than a compositional
one.

---

## The marks I rejected

All in `rejected/`, with the look that caught each one.

**`p1_REJECTED_sky_two_slabs.png`** — my second sky. `sky_mid` came out at 0.55 against
`sky_high` at 0.52. `value_of` told me before I looked that they were 0.03 apart and would
read as one mass. They did. Rebuilt as four steps 0.48 / 0.60 / 0.71 / 0.82.

**`p1_REJECTED_smudge_thumbprints.png`** — six smudges at 0.032–0.038 to lose the sky's joins.
Each left a visible lens-shaped print, like a thumb through wet paint. Replaced with scumbled
bristle strokes in the two neighbouring colours, which is what actually loses a join.

**`p1_REJECTED_channel_wedge_and_small_boat.png`** — a `preview()`. Caught two things at once
before a stroke was spent: the water channel was a straight-sided wedge that read as a road,
and the boat at 0.30 × 0.116 was too small to carry the picture. Boat enlarged to 0.39 × 0.16,
channel narrowed and made to snake.

**`p1_REJECTED_rills_and_puddles_confetti.png`** — 43 painted strokes, the worst pass of either
painting. "Rills" at sizes up to 0.048 read as sticks lying on the mud; "puddles" made with
short `flat` strokes came out as pale rectangles — exactly what the guide says a short flat
stroke is, which I had read and ignored. Buried under a solid repaint.

**`p1_REJECTED_creek_as_pale_plank.png`** — the creek as painted: hard parallel edges, too cool,
too light. Read as a plank laid on the mud.

**`p1_REJECTED_creek_trough_black_hose_REHEARSAL.png`** (+ `_full_`) — the *fix* for the plank,
rehearsed. A dark trough that came out as a black rubber hose, a bright thread along it that
came out as neon cyan piping, and a "far glint" that came out as a pale rope laid across the
sky. About 18 strokes and a repaint saved by one free rehearsal. The creek was abandoned
entirely and replaced with the line of withies, which does the same compositional job
(a diagonal, a counterweight, a break in the banding) for 14 strokes instead of 30.

**`p2_REJECTED_field_saturated_colour_patches.png`** — the pond's field, first attempt. Every
mass was correctly dark by `value_of` (0.19, 0.22, 0.27, 0.33) and the result was a rust
patch, a blue patch, a green patch and a cream blob. Repainted with everything pushed through
`desaturate(c, 0.55)`.

**`p2_REJECTED_pools_as_striped_torn_paper.png`** — the pools as first laid, `block_in` with
`direction="axis"`. Every pool a stack of parallel white bars against black. Fixed by crossing
each with bristle marks at 46–104° plus round accents.

**`p2_REJECTED_leaves_identical_lozenges_and_mouth_REHEARSAL.png`** — nine leaves, all the same
size, angle range and colour: nine orange grains of rice. And a curled leaf built strictly to
the guide's far-rim / inside / near-rim recipe which came out as an unmistakable **mouth**.
Redesigned with sizes from 0.007 to 0.027, four value families, and the curl reduced to an
asymmetric sliver.

**`p2_REJECTED_leaves_v2_fronds_invisible_REHEARSAL.png`** — the second leaf plan. Leaves fixed;
fronds now so close to the field value (0.17 vs 0.16–0.21) that they did nothing at all.
Over-corrected from the first version, where they were hard black hairs.

**`p2_REJECTED_focalA_single_sausage_REHEARSAL.png`** and **`_focalB_crossed_sausages_`** — two
attempts at the picture's focal mark. A single fat blade across the pools read as a cigar;
two crossed ones read as two cigars. Rejected for a third version — long, thin, tapered at
both ends, sweeping across three pools and the dark between them so it is *found* on the light
and *lost* on the dark. That third version is in the painting and it is the best pair of marks
I made all session.

---

## What the guide got right

**"Look every 5 to 15 strokes."** Every failure above was caught by a look. The two I nearly
missed — the speckled shadow film in P1 and the orange grit under the boat — were both caught
only when I finally looked at a `region=` crop instead of the downsampled whole. The habit is
the whole thing.

**`palette.value_of` and the 0.10 threshold.** Exact, twice. It predicted the sky mush before I
painted it and it corrected my eye when a 0.28 mass looked like cream against a near-black
field.

**The exercise-1 binary search.** I lifted `to_value(base, target)` out of exercise 1 and used
it in every pass of both paintings — never mixing to a ratio, always to a value. Five lines,
and it is the most useful thing in the document. It should not be buried in an exercise at the
end; it should be in step 3, where the guide tells you to plan three values as numbers.

**Far edge → inside → near edge.** The boat worked first time, structurally. The interior's near
edge is a real edge — the place where the near flank's paint stops and the dark behind it still
shows — and I drew none of it. The rule is correct and it is worth the space it takes.

**"Before you repaint a mass, look at what is standing on it."** This bit exactly where the guide
says it would: I had measured that the near mud needed burying and the withies were standing on
it. The repaint polygon stops at x = 0.845 for that reason. The guide predicted both the
situation and my instinct to ignore it.

**"Paint over it, don't undo."** I never called `undo` once in 769 strokes. And the buried
rills ghosting up through the repainted flats are the best surface in P1 — that really is why
painted-over pictures look alive.

**"`opacity` does not thin a long stroke"** and **"a pass laid low because it sounded painterly
leaves a speckled film."** Both true. I ignored the second one three separate times and paid
about 25 strokes for it each time.

**`preview` and `rehearse` being free and off the log.** Between them they caught the wedge
channel, the undersized boat, the black-hose creek, the mouth-leaf and two sausages. Call it 60
strokes saved and two passages that would have been unrecoverable.

---

## What the guide got wrong, or left out

**1. `blob(cell("D5"), 0.26, wobble=0.3, seed=2)` does not do what the guide says.** It is
presented as "an irregular mass filling a cell". Measured, its box is `(0.193, 0.506,
0.637, 0.624)` — three and a half cells wide against a cell that is `(0.375, 0.500, 0.500,
0.625)`. `blob((x, y), rx, ry, ...)` with a point behaves exactly as documented. Something
about the Region form is wrong, or the example is.

**2. The unit mismatch is never stated, and it is the most confusing thing in the API.**
Shape and region coordinates are fractions of *each axis*. Brush `size` is a fraction of the
*long side*. So `ribbon(pts, 0.15)` horizontal spans 0.15 of the **height**, while `size=0.15`
is 0.15 of the **width** — on a 3:2 canvas those differ by half again, and on my portrait
canvas they swap. `CALIBRATION.md` mentions this once, parenthetically, about `sweep`'s
`depth`. It belongs in the "Coordinates are always 0.0 to 1.0" paragraph on page one, because
it applies to everything. I lost two passes to it and only settled it by printing `shape.box`.

**3. The guide plans in value and says nothing about chroma.** `value_of` is offered as *the*
tool for planning masses, and it is honest about value. But a field of `#422a2a` at value 0.19
and one of `#29485e` at 0.24 do not read as "a quiet dark with some variation" — they read as
a rust patch next to a blue patch. The whole first field of *Pond* failed this way and had to
be repainted. `desaturate` appears in the mixing table as a convenience; it is actually the
tool that makes a low-value field work, and nothing in the guide says so. **A rule the guide
should have: for a mass larger than about a tenth of the canvas, plan its value *and* run it
through `desaturate` unless you specifically want it to shout.**

**4. Nothing warns about simultaneous contrast, which is worst exactly where the guide sends
you.** Twice in *Pond* I was certain a mass was far too light — it looked cream — and
`look(values=True)` reported 0.28. On a dark painting your eye is unreliable by a wide margin.
The guide should say: on a dark-dominant picture, trust `values=True` over the colour view, not
just occasionally but by default.

**5. `rehearse` cannot take a mass, and masses are where all the money is.** "The plan is a
list of the same arguments `s.stroke()` takes" — so `block_in` and `sweep`, which are 10–30
strokes each, are exactly the things you cannot try before you buy. *Every* expensive mistake
in this session was a mass: the two-slab sky, the confetti pass, the plank creek, the boat's
dissolved silhouette, the saturated pond field, the striped pools. Every cheap save was a
stroke plan I could rehearse. This is the biggest single gap in the tooling as the guide
presents it.

**6. `smudge` leaves a visible lens print on flat paint, at every size I tried.**
`CALIBRATION.md` says `0.035–0.045` "behaves". It behaves in the sense of not dragging a mass
several cells — but on smooth, evenly-covered paint it prints a thumbprint-shaped lozenge that
is more conspicuous than the join it was meant to lose. Three times. The honest rule is:
**smudge into texture, not into flat paint; to lose a join in a flat passage, scumble across it
with the two colours either side.** That is what I ended up doing in both paintings.

**7. `glaze` is the most under-sold tool in the box.** It gets two lines in the wet-paint
section as "the opposite move". In practice it was the most efficient thing I used:
- Two glaze strokes turned a shouting saturated orange lobe into convincing water. Repainting
  it would have cost eight and lost the underpainting.
- Four glazes knocked a failed pale mass back **without burying the two leaves standing on it.**

That second property is the answer to the exact problem the guide devotes its longest paragraph
to — "in order of preference: repaint before the near things go on; repair around them; repaint
and restore" — and `glaze` is a fourth option, better than the last two, that the guide never
mentions there.

**8. "Use a bigger brush than feels comfortable" nearly cost me the boat.** The guide qualifies
it ("that is advice about *masses*") and CALIBRATION gives the real rule ("under about a fifth
of the mass's width"). But "width" is wrong — it must be a fifth of the mass's *smallest*
extent along the direction the passes step. My boat was 0.39 wide and 0.16 tall; at `size=0.030`
the brush was a fifth of the width and a *fifth of nothing* against the height, and the
silhouette simply vanished. It cost a repaint.

**9. "A bristle stroke is never solid" and `direction=("axis", 90)` are two pages apart, and
the consequence is not named.** A bristle `block_in` at `direction="axis"` on a small bright
mass against a dark ground gives **parallel white bars** — the mass reads as a scrap of torn
striped paper. Both halves of the fix are in the guide; the failure mode is not, and it is very
recognisable once you have seen it.

**10. "A few hundred marks" is optimistic for anything with a repair in it.** Both paintings
overshot (416, 353) and in both cases about a fifth to a quarter of the strokes were burying
earlier strokes. That is not a criticism of the number so much as a missing sentence: budget
for the repaint, because you will make one.

---

## Every moment I wanted to open the source

The list, in order, with what I wanted to know:

1. **`blob`'s signature** — when `place` is a Region rather than a point, what does the second
   positional argument mean? The guide's example gave a mass 3.5× the size of the cell it was
   supposed to fill. I never found out; I switched to points and explicit `rx, ry`.
2. **`ribbon`'s width units** — half-width or full? which axis? Answered by printing
   `shape.box`, which cost one probe pass.
3. **`Region`'s field names** — `tuple(region)` raised `TypeError: 'Region' object is not
   iterable` and I wanted to know whether it was `.x0/.y0` or `.left/.top` or something else.
   Answered from `repr()`. The guide lists `Region` in the import line for plain scripts and
   never says what is on it.
4. **How `block_in` counts passes for a *shape* at an arbitrary `direction=` angle.**
   CALIBRATION gives `extent / step` for a rectangle. For a shape at 22° on a non-square canvas
   I guessed wrong twice, once by a factor of two.
5. **Whether `glaze` accepts `size`.** The API list shows `glaze(points, color, opacity=)`.
   I passed `size=` speculatively; it worked. I still do not know the default.
6. **Whether `rehearse` accepts `block_in`/`sweep` specs.** I wanted to rehearse a mass more
   than anything else in this session and could not tell from the guide whether it was
   impossible or whether I just did not know the dict key. See gap 5 above.
7. **The ground colours' values.** There is no way to see what `toned_warm_grey` or `umber_wash`
   actually is without starting a session on it and looking. I wanted
   `palette.value_of("umber_wash")` or a table of seven numbers. I guessed both times.
8. **`smudge`'s kernel** — why is the print lens-shaped, and does the shape follow the stroke
   direction? I could have designed around it if I knew.
9. **Which stroke count is the budget.** `python -m easel run` printed `Ran calib.py: 0 strokes
   total.` on my first run while `s.stroke_count` inside that same script printed `207`. Later
   runs agreed with each other, so it looks like a `new`-then-`run` artefact, but I could not
   tell whether the CLI or the session was lying, and it is the number the guide tells me to
   budget against.
10. **`dab(press=n)` × `size` on a round tip.** CALIBRATION's table is for `size=0.06` and shows
    the width doubling between 2 and 3 stamps. I could not predict what `press=3` at
    `size=0.005` would give. It came out as a small dot, which was right, but by luck.
11. **`desaturate`'s range** — is the amount bounded at 1.0, and is 1.0 fully neutral? I never
    went above 0.6 because I did not know what would happen.
12. **`load_falloff`'s units.** CALIBRATION gives two anchor values (`0.25` even across a canvas,
    `0.0` never dry) but the number is not the same kind of quantity as `load` and I could not
    interpolate. I tuned `0.15`/`0.18`/`0.22` entirely by eye across about six passes.

None of these stopped me painting. Items 1, 2, 3 and 5 were all answerable by writing four
lines of probe code and printing — which is the exercise working as intended, and it took one
pass. Items 6 and 7 are things the guide could simply say. Item 6 is the one I would fix first.

---

## Honest opinion

### *Low tide* — 416 strokes

It reads as what it is: an estuary at low water, evening, a boat left on the mud. The withies
stepping back to the horizon are the best thing in it — about fifteen strokes doing all the
work of depth, and they arrived only because the creek failed and I needed a replacement. The
sheer line is the mark that turns the dark loaf into a boat; without those five short strokes
there is no boat in this picture at all, which is a fair test of how little form is actually in
the hull.

The flaws, and there are several:

- **The sky is four bands with the joins scumbled, not a sky.** At full resolution the scumble
  reads as hatching. It is the weakest third of the picture and I spent 83 strokes on it —
  a fifth of the painting — on the *background*, before I had established anything.
- **The boat has a silhouette and a lit rim and essentially no form inside it.** Cover the sheer
  line and it is a brown lump. This is precisely the failure the guide names: I spent my
  precision on the thing I measured and the mass never got its own passes.
- **The flats between the boat and the horizon repeat.** Same brush family, same near-horizontal
  angles, same value band, across a third of the canvas.
- **The far shore got lucky.** It is a broken streaky strip that I laid too thin and it happened
  to read as a distant tree line. I would not be able to do that again on purpose.
- **About 90 strokes went on burying my own work**, and the picture would be better if I had
  spent those 90 on the boat.

### *Pond* — 353 strokes

Structurally the stronger of the two. The dark really is dominant, the light chain really does
run as an all-over diagonal, and the two blades crossing the water at the centre — found on the
light, lost on the dark — are the best pair of marks I made in either painting. The glazes did
more for this picture than any block-in did.

The flaws:

- **The leaves are one shape at eleven sizes.** A `round_hard` stroke under `pressure="swell"`
  makes an excellent leaf, which is why I used it for every single leaf, which is why they read
  as a set. I varied size, angle and value and never varied the *shape*, and once you see it you
  cannot stop seeing it. This is the checklist's "mechanically repeated" and I failed it while
  believing I had passed it, because I was checking spacing rather than form.
- **The weed in the lower half has a woodgrain look** from the bristle comb running along the
  mass's axis. I broke it twice and never beat it.
- **The silt mass is a glazed stain, not a described thing.** It is quieter than it was, which
  is all I asked of it, and that is not the same as being any good.
- **The subject is legible only if you are told.** Without a title this reads as an abstraction
  — pale broken shapes on a dark ground with scattered marks. I do not think that is fatal, and
  parts of it are better as abstraction than as pond, but it is not what I set out to paint and
  I should say so.

If I painted a third, I would spend the first hundred strokes the same way and the second
hundred completely differently: less on backgrounds, more on the one thing the picture is
about, and I would find out what `rehearse` will and will not take before I laid a single mass.
