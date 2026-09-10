# rehearsal4/pass — painting log

To understand this, start by reading `p23_mug2.py` (the pass that got the mug right,
and the one whose comment explains the mistake that cost the most), then
`o2d_fix.py` (the same lesson in a different disguise), then this file's
**Marks I rejected** section beside the images in `rejected/`.

Three paintings, one reference. `sketch(reference)` was **not** called. `prepare()`
was used for *reading only* — the reference's mass values and mass colours — and
`ref_shape()`, `ref_outline()` and `sketch()` were never called at all. Every line
in the underdrawing is `pencil()` through landmarks I placed and checked myself.

## Stroke counts

| painting | strokes | file |
|---|---|---|
| the copy | **299** | `copy_final.png`, `copy_timelapse.gif` |
| own1, *Flood, low sun* | **236** | `own1_final.png`, `own1_timelapse.gif` |
| own2, sunflower | **235** | `own2_final.png`, `own2_timelapse.gif` |

**Value criterion: passed.** Final `compare()` on the copy: *0 of 64 cells more than
0.10 out, largest 0.10.* That is every cell on the canvas, not only the ones on the
object. The run before the last two passes was 7 cells out at 0.20; the run before
that, 11 cells out at 0.34.

---

## What I did

**The copy.** Empty-canvas `compare()` first, as the guide says. That one call was
the most valuable thing I did all session: my eye read the mug as *white* and the
photograph says its front face is 0.44 and the tea is 0.05. I would have painted a
pale mug on a pale table and failed the whole test. I read the reference's 8×8 value
map out of that table, planned five named mixtures against it with a brute-force
search over `mix`/`tint`/`desaturate` (`mixsearch.py`), and supplied raw hex for the
three darks below the box's 0.13 floor (tea, crewmate, spoon).

Then: seven landmarks, each checked at feature scale with
`look(region=cell(...), reference=..., grid="fine")` — reading the two digits off the
label, never estimating a fraction. Table (three times, see below), cast shadow,
pencil drawing over the far masses, mug, tea, crewmate, spoon, tag, fourteen counted
finishing marks, one last stroke.

**own1** is a flooded field under a low sun: horizontal bands stacked in depth.
**own2** is a sunflower head face-on: one centre, everything radiating.

---

## What the guide got right

- **"Look every 5 to 15 strokes."** Every single disaster in this session was caught
  by a look and would have been invisible without one. Not one of them was
  predictable from the code I had just written.
- **"Run `compare()` twice, not continuously" — and once on the *empty* canvas.**
  See above. This is the guide's best single piece of advice for a copy and it is
  slightly buried; it deserves to be nearer the top of *Working from a reference*.
- **The fine grid.** "Read the two digits off the label; do not estimate a fraction"
  is exactly right, and it is why the mug's silhouette landed on the reference on the
  first try (`out/look_032.png` — the pencil against the photograph). Nineteen points
  read this way cost nothing and were all usable.
- **Back to front.** Laying the cast shadow before the mug meant the mug's base has a
  real edge that I never drew. The one time I deliberately used the *other* half of
  that rule — "sharpen an edge by painting the mass on the other side of it" — one
  stroke both cut the mug's lower-right edge and fixed cell E6. Best stroke in the
  painting.
- **Planning values as numbers before mixing.** `value_of` on five named mixtures,
  checked for 0.10 separation, took a minute and meant the block-in was right first
  time (11 cells out, all of them cells the object had not been painted into yet).
- **"Use a bigger brush than feels comfortable, especially early."** Correct for the
  table. Dangerously wrong for a shaped mass — see the next section.

## What the guide got wrong, or left out

Ordered by what they cost me.

1. **A shaped `block_in` spills up to three-quarters of a brush past its own
   silhouette, so the brush must be small *relative to the mass* — and the guide
   phrases this fact as reassurance.** *Masses that are not rectangles* says a
   shape's passes "stop at the boundary rather than a third of a brush past it", and
   CALIBRATION says "paint stops within three-quarters of a brush width past the
   silhouette". Both are true. Neither reads as a warning. I blocked a mug 0.32 wide
   with `flat` at `size=0.12`, the paint landed 0.06 outside the drawing on every
   side, the silhouette vanished and the handle was buried
   (`rejected/copy_04_mug_flat_size012_spilled_off_silhouette.png`). That cost 72
   strokes and the one `undo` of the session. The guide needs a sentence like:
   *"Half the brush lands outside the shape. Inset the shape by half the brush size,
   or keep the brush under about a fifth of the mass's width."* `shape.inset(0.045)`
   with `size=0.09` landed the paint exactly on the drawing (`p23_mug2.py`).

2. **Low `opacity` on a long stroke still saturates to nearly full colour.** The
   guide says this — under **pressure**: *"the light end of a taper is thin, not
   faint: dabs overlap by more than 90%, so it still accumulates to nearly full
   colour."* It never says it about `opacity`, and `opacity` is the knob the
   *Per-stroke overrides* section hands you. I laid wood grain at `opacity=0.08`
   expecting a whisper and got eleven shouting striped ribbons across the whole
   canvas (`rejected/copy_03_grain_opacity008_shouting.png`), which forced a third
   repaint of the table. The working numbers I ended up with: `stroke(opacity=0.04)`
   is nearly invisible; `glaze(opacity=0.10)` is a clearly visible soft film.

3. **`smudge(size=)` is much stronger than the guide implies.** "Move paint around"
   and one example at `size=0.06`. At 0.10 it dragged pale finger-shaped lobes out of
   the lit half of the table and deep into the dark half
   (`rejected/copy_02_smudge_size010_pulled_lobes.png`). It also pulls the *lighter*
   mass into the darker one, not symmetrically. It needs a size warning and that
   asymmetry noted. Everything at 0.035–0.045 behaved.

4. **There is no syntax anywhere for supplying your own colour**, though both files
   promise you can ("A colour you supply yourself lands exactly as written, black
   included"; "a literal `#000000` renders as `#000000`"). I had to probe it. For the
   record: `p["ink"] = "#0d0c10"` works and `p["ink"] = (0.05, 0.05, 0.07)` works;
   `p["ink"] = [13, 12, 16]` silently clamps to **white**, which is a trap. This
   mattered: the photograph's tea is 0.05 and its crewmate 0.08, both below the box's
   0.13 floor, so without raw colour those cells could not have been brought inside
   0.10.

5. **A short `flat` stroke is a rectangle.** The guide says oriented tips are held
   square to their travel — in the *angle of the mark* section, about masses. It never
   connects that to accents, and *Highlights last, smallest brush* does not say which
   brush. I made this mistake twice: eleven "petal ridges" that landed as sticky-note
   bars stuck on the flower (`rejected/own2_02_flat_ridges_as_stickynote_bars.png`),
   and a reflected light at the mug's base that came out as a white dashed bar
   (`rejected/copy_07_white_bar_at_the_base.png`). Rule the guide should state:
   *small accents want `round_hard`; `flat` and `knife` want a length.* Related and
   also unstated: on a `flat` tip `pressure=[1.0, 0.25]` does not taper the mark, it
   only fades the paint, so you get a bar with a weak end.

6. **Crossing a *small* shaped mass serrates its own boundary.** `direction=("axis",
   68)` on the tea gave a sawtooth edge; the same crossing on a big table mass was
   fine. The guide recommends the crossing unconditionally ("Take it"). It should say
   the crossing is for masses several brushes across.

7. **`block_in` over a rectangle overhangs by a third of a brush and will bury a thin
   neighbour.** This *is* in the guide, and I still walked into it: the water band in
   own1 started at `y=0.478` with `size=0.14` and swallowed the far bank I had just
   swept at `y=0.462` (`rejected/own1_02_water_buried_the_far_bank.png`). The guide's
   fix — `overhang=0` — is mentioned once and would have saved the pass.

8. **The `out/` counter is per-session, and the CLI workflow the guide recommends
   makes that destructive.** The guide does warn. It is not a strong enough warning
   for the actual workflow it teaches: three `.easel` files in one directory means
   painting #2's looks are silently overwritten by painting #3's. I lost all of
   own1's looks and had to recover the rejected frames out of its own timelapse GIF
   (`keep_rejects.py`). Either the numbering should be keyed to the session file, or
   the warning should say *"a second painting in the same directory overwrites the
   first's looks."*

9. **No way to budget.** `block_in` and `sweep` costs are only knowable after the
   call. CALIBRATION has the rule (`step = size × (1 − 0.45 × density)`, so
   `passes ≈ extent / step`, times about three if crossed) but PAINTER.md, which is
   where the 300-stroke budget bites, does not. One line would let a painter plan the
   pass instead of discovering it.

10. **Undocumented but real:** `prepare(level="fine")` works (2785 areas) though only
    `"coarse"` is documented; `shape.inset()` works on `polygon`, `ellipse` and
    `ribbon` alike; `undo(72)` restored the canvas exactly, including wetness, so
    "scraping" undersells it.

---

## Marks I rejected, and why

Every one of these is a look I took, disliked, and painted over or scraped. Images in
`rejected/`.

| # | the mark | the look that caught it | why it went |
|---|---|---|---|
| 1 | Lit band on the table as a concave `polygon` block-in, `flat` 0.17 | `copy_01_jagged_polygon_lit_band.png` | The passes were cut against a notched outline and came back as a staircase of slabs with flat ends. A soft gradient wants a convex shape; I replaced it with overlapping `ellipse` masses. |
| 2 | Seven `smudge`s at `size=0.10–0.11` along the block-in shoulders | `copy_02_smudge_size010_pulled_lobes.png` | Dragged pale lobes out of the lit half and into the dark left third — it looked like a thumbprint. Repainted with `table_dark`. |
| 3 | Fourteen wood-grain strokes, `bristle` 0.03–0.05, `opacity=0.08–0.10`, edge to edge | `copy_03_grain_opacity008_shouting.png` | Read as bold striped ribbons. Two faults at once: opacity saturating along a long stroke, and the guide's own "do not lay one broken pass across the whole canvas". Whole table repainted; grain redone as two `glaze`s. |
| 4 | The entire first mug pass, 72 strokes, `flat` at `size=0.12` on the mug shape | `copy_04_mug_flat_size012_spilled_off_silhouette.png` | The paint landed ~0.06 outside the drawing all round; the silhouette was gone and the handle painted over. The only `undo` of the session. |
| 5 | Cast shadow blocked in with `bristle` 0.11–0.13, crossed | `copy_05_after_undo_spiky_black_shadow.png` (visible once the mug was scraped off it) | A black spiky starburst with a hard bright rim, nothing like a soft cast shadow. Relaid with `flat` over two ellipses, penumbra under core. |
| 6 | Handle's cast shadow, `bristle` 0.05 at `load=0.8` | same look | A speckled comb that read *lighter* than the table it sat on. Painted out; the handle shadow is now one soft ellipse. |
| 7 | Crewmate lit with two `bristle` strokes at `opacity 0.45–0.50` | `copy_06_crewmate_milk_chocolate.png` | Turned the figure milk-chocolate and put cell D4 0.13 out of tolerance. Re-blocked darker at `#191210`. |
| 8 | Reflected light at the mug's base, `flat` 0.015 | `copy_07_white_bar_at_the_base.png` | A white dashed bar sticking out below the mug — a `flat` accent, square ends and all. The last stroke of the painting buries the half of it that fell on the shadow. |
| 9 | Sun path as a solid `ribbon(..., end_width=0.30)` block-in | `own1_01_sun_path_solid_trapezoid.png` | A hard-edged geometric tower with two perfectly straight vertical sides. Rebuilt as broken horizontals cut *from outside* the column. |
| 10 | Water band starting at `y=0.478`, `flat` 0.14 | `own1_02_water_buried_the_far_bank.png` | The overhang buried the far bank. Bank re-swept on top. |
| 11 | Leaf veins as `liner` strokes along each leaf's full ribbon path | `own2_01_leaf_veins_overshot_the_leaves.png` | The ribbon tapers, the path does not, so four bright chartreuse hairlines shot out past the leaves into the background. |
| 12 | Eleven petal ridges, `flat` 0.008–0.016 | `own2_02_flat_ridges_as_stickynote_bars.png` | Hard rectangular bars pasted on the petals. Repainted with `round_hard`, which declares no axis and does taper in width. |
| 13 | Eight dark "gaps" between petals at v 0.15 against petals at v 0.70 | `own2_03_dark_gaps_as_black_slugs.png` | Four values below their neighbours, so they read as black slugs lying on top rather than as shadow between petals. Found again by replaying the same seeded RNG (`o2e_finish.py`) and painted out; the separations are now two values, not four. |

---

## Honest opinion of each painting

### The copy — 299 strokes

It passes and it is not good. Somebody would say "mug of black tea, spoon in it,
wooden table, teabag on the right", which is the bar, and the value map is right
everywhere. Past that:

- The mug's body is **three flat vertical stripes** of blue-grey with visible zigzag
  joins, because I swept the lit and shadowed sides along the silhouette and then
  never blended them into the middle. A cylinder should turn; this one has facets.
- The rim is a **chalky horseshoe**, far too thick, with a dotted speckle across its
  top right I never removed.
- The crewmate is a **blob**. His legs do not read, the backpack does not read, and
  the visor is a white pill.
- The cast shadow is a set of **blocky rectangles with hard steps** — the block-in's
  pass ends, never softened.
- **Almost every edge in it is equally hard**, which the guide names as the single
  commonest failure. I had no strokes left to lose any.
- The allocation is wrong: **138 of 299 strokes went on the table**, because I painted
  it three times. The subject got 160. It should have been the other way round, and
  the reason it was not is that all three table failures were things I could not have
  predicted without painting them.

The table is the best passage in it — the warm gradient and the light coming from the
right are convincing. That is faint praise for a picture of a mug.

### own1, *Flood, low sun* — 236 strokes

The best of the three as a picture, and the least interesting as a decision. The
value structure is clean and the greyscale reads: light sky, mid water, dark bank and
near shore, three masses well clear of each other. The dead tree is the best-drawn
thing I made all session — `pressure=[1.0, 0.5, 0.1]` on a `liner` gives branches
that actually thin. The birds work.

Flaws: the water is a **mechanical stack of horizontal dashes**, too even in length
and spacing — exactly the "evenly spaced marks" the checklist warns about. The sun
path still has a squarish lower-right corner where I stopped breaking it. The cloud
band across the middle sky has a hard ragged top that reads like torn paper. The nine
reeds are nine near-identical strokes. And the subject is a **cliché**: sunset, water,
dead tree, three birds. I picked it because it suited the engine — bands, sweeps,
lost edges — rather than because I had anything to say, and it shows.

### own2, sunflower — 235 strokes

The most successful structurally and the most laboured. The corona reads, the light
rotates convincingly from upper-left to lower-right around the ring, and the seed disc
has real texture from the golden-angle marks — that is the passage I would keep.

But it took **three repair passes**: soft airbrushed lozenges, then rectangular bars
stuck on them, then black slugs, then finally petals. The archaeology still shows —
there is a striped patch on the upper-left petals I painted over twice and never
fully killed, and the petals below the disc are muddier than they should be from
repeated overpainting. The **leaves are the worst thing in it**: four pale mint slabs
pasted at the corners with hard edges, doing no work, and I spent six strokes trying
to rescue them instead of painting them out. The background is flat dark green with
block-in rectangles still visible behind the flower. And the flower sits nearly in the
middle of a square, which is the least interesting place to put anything — my 0.03
offset from centre was not nearly enough.

---

## How own2 differs from own1 in compositional structure

Not subject, not palette — structure.

| | own1 | own2 |
|---|---|---|
| organising principle | **height on the canvas** | **angle and radius from one point** |
| masses | four horizontal bands stacked in depth | one centre, one ring, one field |
| space | deep — a horizon, aerial recession, things behind other things | flat — no horizon, no ground plane, nothing recedes |
| direction of marks | almost all horizontal | almost all radial |
| what "back to front" means | literal depth: sky, far bank, water, near bank | **radius**: back row of petals under the front row |
| value structure | a vertical gradient, dark at the bottom and at the horizon | figure against ground, with the dark at the centre *and* the perimeter at once |
| format | 1200×720, wide — up/down asymmetry is the whole composition | 900×900, square — that asymmetry is deliberately removed |
| how the masses were made | `block_in` over rectangles, `sweep` along a horizon edge | one computed stroke per petal, angle by angle |

The square format is doing real work here: own1's composition cannot survive being
turned on its side, and own2's barely notices.

---

## Every moment I wanted to open the source

Kept as I went. This is the list the exercise is for.

1. **`block_in`'s spill on a shape** — I wanted the signature to see whether
   `overhang=` applies to shapes and what the default really was. Reading the guide
   twice did not tell me a 0.12 brush would eat a 0.32 mass. *Cost: 72 strokes.*
2. **How `opacity` composites along a stroke** — after grain at 0.08 came out at what
   looked like full strength, I wanted the blend code.
3. **`smudge`'s implementation** — what `size` means physically, and why it drags
   light into dark and not the reverse.
4. **The palette's `__setitem__`** — the one thing I actually had to reverse-engineer
   by experiment (`p01_marks.py`), because neither file gives the syntax for a colour
   you supply yourself.
5. **`ribbon(points, width)`** — full width or half? I guessed full. It looked right.
   I never confirmed it.
6. **`shape.inset(d)`** — units, and whether it works on `ellipse`/`ribbon` as well as
   `polygon`. It does; I was guessing when I used it.
7. **`sweep`'s pass count with `cross=`** — CALIBRATION gives one measured example.
   With a hard stroke budget I wanted the formula, not an example.
8. **What `compare()` averages** — linear light or sRGB? A cell holding a dark mass
   and a light one came back far darker than either weighting predicted, which changed
   how I sized the crewmate. I still do not know, and I painted around the question.
9. **Whether `undo(n)` restores wetness and the RNG position** — the guide calls it
   "scraping", which sounds lossy. It looked exact. I wanted to be sure before betting
   72 strokes on it.
10. **Where the `out/` look counter lives** — after own1's looks vanished, to find out
    whether it was per-directory or per-session and whether I could have set it.
11. **`glaze` vs `stroke(opacity=)`** — whether a glaze is a different operator or the
    same one with a low number.
12. **`erase(region=)`** — whether it takes a shape as well as a region, when I wanted
    to take the pencil out of just the crewmate.
13. **`prepare(level=)`'s legal values** — I guessed `"fine"` and it worked. Only
    `"coarse"` is documented.
14. **`dab(press=n)`'s stroke accounting** — the guide says one; with 16 strokes left
    I wanted to verify rather than trust.
15. **`direction=("axis", N)`'s pass geometry on a small concave shape** — after the
    tea came back serrated, to understand whether the sawtooth was the crossing or the
    cut.

I opened none of them.

---

## File map

| file | what it is |
|---|---|
| `warmup.py`, `mixsearch.py` | guide exercises 1/6 condensed; the mixture search against the reference's mass colours |
| `p01_marks.py` | landmarks + the probe that found how to supply a raw colour |
| `p02_read.py`, `p03_values.py` | reading the reference — `prepare()` and per-cell `compare()`. Reading only |
| `p10`–`p14` | the table, three times. `p10` and `p12`/`p13` are the failures |
| `p20_shadow_draw.py` | cast shadow + the whole pencil drawing |
| `p21_mug.py` | the mug pass that was scraped |
| `p22_undo.py` | the scrape |
| `p23_mug2.py` | **the mug, done right — start here** |
| `p24`–`p27` | tea, crewmate, spoon, tag; the two value-fixing passes; the last stroke |
| `o1a`–`o1e` | own1, five passes |
| `o2a`–`o2f` | own2, six passes. `o2d_fix.py` is where the flat-brush lesson repeats |
| `keep_rejects.py` | preserves the rejected-mark looks and recovers own1's from its GIF |
| `rejected/` | thirteen images, one per rejected mark |
| `out/` | live looks and compare heat maps (own1's overwritten, see above) |
