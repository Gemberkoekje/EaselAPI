# Assisted run — copying `C:\temp\Level1.jpg` with Easel

Reference: a pale blue mug with an Among Us crewmate printed on it, a spoon in it,
on a light wood table, with a big soft cast shadow and a navy teabag tag to the
right. **This run started from the machine underdrawing** (`prepare()` + `sketch()`),
as required, and says so everywhere it matters.

---

## The verdict, first

**Final stroke count: 299** (`s.stroke_count`; pencil, previews and rehearsals not
counted). Under 300 by one — `c27_final.py` landed exactly on 300 and `c28_finish.py`
scrapes one mark with `undo(1)`.

**Is it recognisable?** Partly, and I want to be exact about which parts.

- Recognisable with the reference covered: a **mug** — pale rim ellipse, pale body,
  a handle loop on the right, dark liquid inside, a dark spoon standing up out of
  it, a cast shadow under it, a small navy tag on the table to the right, all on a
  warm wooden surface. Someone shown `copy_final.png` cold would say "a mug of
  coffee or tea on a table".
- **Not** recognisable: the crewmate on the mug's face. It is there as a dark shape
  with a light visor, but it fuses with the shadow at the mug's base into one brown
  mass, and it does not read as a figure. That is the single biggest failure of the
  copy.
- Also weak: the mug looks squat (the dark tea mass eats too much of its upper
  half), the cast shadow is smaller and lighter than the reference's, and the
  surface is blocky — a lot of hard-edged rectangular passages, because almost
  every mass was laid with `flat` at `pressure="even"` and I never got back to
  breaking them up.

---

## What the machine sketch actually bought

### The `prepare()` area table

```
  #  share  value  colour   cells                     edges
  3   22.0%  0.43  #7D6B53  F1,G1,H1,F2,G2,H2...      4:0.16
  2   21.1%  0.36  #685848  B1,C1,D1,E1,A2,B2...      1:0.07, 4:0.89, 5:0.07, 7:0.45
  4   20.2%  0.56  #9F8D79  E1,F1,C2,E2,F2,G2...      2:0.89, 3:0.16, 5:0.16, 6:0.65, 7:1.00
  1   13.2%  0.36  #6F583D  A1,B1,A2,B2,A3,A4...      2:0.07
  7    9.2%  0.14  #29221D  C3,D3,C4,D4,E4,C5...      2:0.45, 4:1.00, 5:0.65, 6:0.68
  5    7.1%  0.48  #8C765D  B2,C2,B3,C3,B4,C4...      2:0.07, 4:0.16, 7:0.65
  6    7.1%  0.44  #70707A  D3,E3,F3,D4,E4,F4...      4:0.65, 7:0.68
```

**Did the numbered masses match the things I would have named? No.** I would have
named: table, mug, tea, spoon, crewmate, handle, cast shadow, teabag. What I got:

- **Four of the seven areas (1, 2, 3, 5 — 63% of the picture) are all the table**,
  cut along its lighting gradient. Merging them was the first thing I did.
- **No area is "the mug".** Its lit side is inside area 4 *together with the lit
  table*; its shaded side is inside area 6 *together with the cast shadow*. The
  one object in the picture is the one the map cannot see.
- Area 7 (the useful one) fuses **tea + crewmate + the shadow's core** into one
  "dark stuff" mass. Its bbox, 0.309–0.559 × 0.240–0.823, spans three different
  objects.
- **The spoon and the teabag are in no area at all.**

Two columns were genuinely worth having:

- The **edges** column was the best thing in the table. `4:7 = 1.00` (the mug's
  lit side against the dark stuff) really is the hardest edge in the picture, and
  `2:4 = 0.89` (the table's light/shade terminator) really is the second. That
  matched where I ended up wanting hard edges, and I would not have ranked them
  as confidently by eye.
- The **cells** column was useful for areas 6 and 7 and worthless for 1–5, which
  each span every cell of the canvas.

`prep.region(n)` returns only a bounding box, and `look_areas()` draws the contours
with **no numbers on them**, so working out which numbered mass was which took a
whole extra pass (`c2_areas.py`) and still ended in guesswork.

### The `sketch()` lines

Seven contours, 770+ points. What happened to each:

| Line | What it was | Kept / erased / wrong |
|---|---|---|
| 3 | area 4's boundary — contains the **mug's outer silhouette** | **Kept**, clipped to x 0.275–0.78. Rim ellipse accurate to about 0.005 against my own fine-grid reads. Left silhouette drifts ~0.018 too far left below y≈0.4. |
| 5 | area 6 — the **handle's loop** and the mug's right side | **Kept.** Handle shape right, sitting about 0.02 too far right. |
| 6 | area 7 — the **crewmate's outline** and the shadow's core | **Kept.** This was the single most valuable line in the run: a silhouette I would otherwise have had to measure point by point off `grid="fine"`. |
| 0, 1, 2, 4 | wood-grain / lighting contours across the whole table | **Erased**, all four. 770 points of ragged zigzag, i.e. most of the drawing by length. |

Erased with `s.erase(span("A1","B8"))`, `span("G1","H8")`, `span("C8","F8")`,
`span("C1","C2")`. That also took the teabag tag with it, so I redrew that by hand.

**Drawn by hand, because the machine missed them:**

1. **The spoon.** Completely absent — the segmenter put it inside the tea's mass,
   which is correct on colour and useless on subject. This is the object that
   sticks up out of the mug's silhouette; it is the second thing a viewer sees.
2. **The mug's base.** The contour dissolves exactly where the mug meets its own
   cast shadow — the one line a painter most needs, because it is where the object
   sits on the table. I got a 0.04-long fragment near x=0.44 and nothing else.
3. **The tea's own edge inside the rim** — the boundary between dark liquid and
   pale inner wall was inside area 7, not on it.
4. **The teabag tag** (collateral of erasing the right-hand junk).

**Honest cost/benefit.** The drawing costs no strokes either way, so the sketch
saved no strokes at all — the saving would have to show up in *looking*. It bought
me maybe three fine-grid reads (the rim ellipse, the handle, the crewmate). It cost
me three looks and two whole passes (`c12_lines.py`, `c13_redraw.py`) working out
which unlabeled contour was which and putting the useful ones back after the
background block-in buried them, plus one wrong belief I painted to (the mug's
left silhouette). **Net: about a wash, with the accuracy on the crewmate's outline
as the real gain.**

And the thing it emphatically did **not** buy: the value map. The error that
actually decided this painting was that the reference's middle is far darker than
it looks — `compare()` against the bare ground reported D5 at 0.06 and D4 at 0.14
against my ground's 0.54. `prepare()` had told me area 7 was "value 0.14" and I
still did not act on it until `compare()` put it in a grid. **`compare()` on an
empty canvas is worth more than `prepare()`** and is not presented that way in the
guide.

---

## The rejected marks

Four, all caught by `rehearse()` before a stroke was spent.

**1. `c14a_rehearse.py` — the mug's light mass, 15 vertical strokes, step 0.022,
size 0.030–0.044, starting at the rim's *upper* arc.**
The rehearsal showed: a slab of visible vertical **slats** with a sawtooth top edge;
the whole opening buried in pale so the mug read as a solid cylinder with no hole;
the leftmost column (`mug_dark`, value 0.30) reading as a separate blue-violet
object stuck to the side; and brown speckle across the bottom half where the long
strokes had run dry.
*Painted instead:* step 0.013 at size up to 0.050 (about 60% overlap),
`load_falloff=0.1`, starting at the rim's **front** arc so the opening stays open,
six tones instead of five, plus a crossing horizontal pass.

**2. `c14b_rehearse2.py` — the same pass with the highlight built by
`at_value(mix("cerulean","titanium_white",0.94), 0.80)`.**
The rehearsal came back **olive**: `#bfd0cb` and `#afb5a8`. My `at_value` helper
reaches a target below the base's value by *shading*, and `shade()` adds umber, so
asking a cerulean-white to come down to 0.80 turned it green. A mug the colour of
a swimming pool.
*Painted instead:* every mug tone as a **tint of one blue-grey**
(`desaturate(mix("cerulean","burnt_umber",0.32), 0.22)`), so they stay one family.
(I later moved that base to `ultramarine` — the cerulean version was still too
teal on the canvas, which no rehearsal caught because it only shows against the
warm wood.)

**3. `c16a_rehearse.py` — the tea plus a pale rim ring.**
Two things wrong at once. (a) The tea, mixed at value 0.23, rehearsed as a **milky
mid-brown around 0.45**: it was going onto still-wet mug paint. (b) The pale ring,
painted as a band following the ellipse, read as a **rope laid on the mug** — a
drawn outline round a painted hole, which is precisely what PAINTER.md tells you
not to do, and I did it anyway because "rim" sounds like a line.
*Painted instead:* `dry()`, fill the **whole** opening with the inner-wall tone so
it is continuous with the body, `dry()` again, lay the tea on top, and let the pale
crescent be **what is left over**. Also re-read the tea's left edge off the crop:
0.391, not the 0.352 I had.

**4. `c19_darks.py` — the crewmate, one pass at size 0.020.**
The rehearsal landed near 0.35 against a target of 0.23, and showed my outline
running to x=0.550 where the reference stops at 0.525, with the gap between the
legs in the wrong place.
*Painted instead:* corrected silhouette, two crossed passes, then a third
restatement with a fat brush (size 0.038–0.048) because small brushes do not cover.

---

## The `compare()` numbers

Progress across the run (8×8 cells, threshold 0.10):

| Stage | Cells out | Largest |
|---|---|---|
| bare ground (`c8_refvalues.py`) | 40 / 64 | 0.48 (D5) |
| after the block-in (`c22`) | 15 / 64 | 0.22 (D5) |
| after the features (`c25`) | 16 / 64 | 0.26 (D3) |
| **final (`c28`, 299 strokes)** | **9 / 64** | **0.23 (D4)** |

Final table:

```
       A      B      C      D      E      F      G      H
  1  +0.01  -0.01  -0.06  -0.06  +0.09  +0.04  +0.01  +0.07
  2  -0.00  -0.02  +0.08 +0.14* +0.11*  +0.06  -0.01  -0.06
  3  -0.01  -0.04  +0.05 +0.11*  +0.04  +0.07  -0.06  -0.08
  4  -0.02  -0.04  -0.03 +0.23* +0.11*  +0.01 -0.10*  -0.09
  5  +0.00  -0.02  -0.06 +0.21* +0.12*  +0.05  -0.06  -0.08
  6  +0.01  -0.02  -0.03 +0.13*  -0.03  -0.00  -0.06  -0.06
  7  +0.04  -0.00  -0.07  -0.02  -0.03  +0.03  -0.02  -0.04
  8  +0.07  +0.01  -0.01  -0.10  -0.01  +0.07  +0.04  +0.02
```

**Cells covering the main object that are still more than 0.10 out — all eight of
them, and every one is my canvas being too LIGHT:**

| Cell | ref | canvas | delta | what is there | reachable? |
|---|---|---|---|---|---|
| D4 | 0.14 | 0.37 | +0.23 | crewmate's head | **no** — ref below the 0.23 floor |
| D5 | 0.06 | 0.28 | +0.21 | crewmate's body | **no** — 0.17 below the floor |
| D2 | 0.18 | 0.33 | +0.14 | the tea | **no** |
| D6 | 0.12 | 0.25 | +0.13 | shadow core + legs | **no** |
| E5 | 0.31 | 0.44 | +0.12 | backpack + shadow right of the mug | yes — ran out of budget |
| E2 | 0.19 | 0.30 | +0.11 | tea + spoon | **no** |
| E4 | 0.42 | 0.53 | +0.11 | mug's right face | yes — ran out of budget |
| D3 | 0.22 | 0.33 | +0.11 | tea's front + lip shadow | **no** (0.22 is at the floor) |

G4 (−0.10) is the only cell off the object and it is exactly on the line.

**Six of the nine are physically unreachable.** The palette bottoms out at 0.23 and
the reference's darkest cell mean is 0.06. I spent about 25 strokes discovering
this the slow way (three separate darkening passes on the tea and the crewmate,
each of which moved the number a little and then stopped moving). Repairs I did
make, in order: lifted the wood in F/E7/E8/D8 (fixed 8 cells at once, the single
best-value pass in the run), then over-lifted G/H and had to put them back, then
pushed the tea's front edge down to y=0.345 which the cell arithmetic said it had
to be at, then deepened the shadow core.

---

## What the guide cost me, in the order it bit

| # | Where | What I expected | What happened | What I would add to PAINTER.md |
|---|---|---|---|---|
| 1 | before the first mark | `s.save()` / `s.load()` — the brief says "save the session as the guide describes" | The API list has no persistence at all. The only persistent form is the CLI at the very bottom (`easel run p.easel script.py`), which I had to infer. | One line in *The rest of the API*: a `Session` built in a plain script is not persistent; `easel run` is the only way to continue a painting across processes. |
| 2 | `c3_sketch.py` | `prep.merge(2, 1)` merges 2 into 1 | It does, but the guide's only example is `prep.merge(3, 7)` with no statement of which number survives. My next line `merge(2, 3)` raised `KeyError: No area 2`. | Say which argument survives, and mention `prep.numbers`. |
| 3 | `c3_sketch.py` | `s.sketch()` returns nothing much | It returns the full list of `StrokeRecord`s. `print(s.sketch(...))` dumped 35 KB into my terminal. | "`sketch()` returns the pencil strokes it laid; don't print it." |
| 4 | `c2`, `c3` | `prepare()` numbers the masses, so I can see which is which | `look_areas()` draws contours with **no numbers on them**, and `prep.region(n)` returns a bounding box — four of seven were the full canvas height, so the boxes told me nothing. Identifying the masses took a whole extra pass. | Number the overlay, or document `look(region=prep.region(n))` as *the* way to identify an area — and warn that a bbox is useless for areas that wrap the canvas. |
| 5 | `c11` → `c12` | the pencil survives under thin paint | A `block_in` of the background over the whole canvas buried the **entire** underdrawing, including all the foreground lines I still needed. | Say it plainly: draw the background first if you must, but re-lay the foreground's drawing *after* the background is in — and that `sketch_lines()` is how you get it back. |
| 6 | `c13` | `erase(region)` removes those lines | It removes the graphite from the canvas but **`sketch_lines()` still returns the line whole**. Re-laying from `sketch_lines()` silently resurrects everything you rubbed out. See *Engine defect* below. | Either drop erased points from `sketch_lines()`, or document that it is a record of what was *drawn*, not what is *there*. |
| 7 | `c17` | `s.log()` is a sequence of records | It is a **string**. `for rec in s.log()[-6:]` iterated over six characters and printed `p a i n t`. | Say what `log()` returns. |
| 8 | `c17` | `tint(c, 0.80)` gives value ≈ 0.80 | `tint`'s amount is a mix ratio, not a value: `tint(NEUT, 0.80)` came out at 0.648, and I painted three strokes at the wrong value before noticing. The guide *does* warn that white is a weak lightener, but the fix is arithmetic. | Ship a `palette.at_value(c, v)`, or show the four-line binary search. I wrote it five times in this run (`at_value` in c14a onward). |
| 9 | `c16` → `c17` → `c23` | one pass of `flat` at `load=1.0` covers | It does at `size=0.16` (I tested — `t1_coverage.py`) and it does **not** at `size=0.02`. Three separate passes on the tea to get from 0.42 to 0.28. | The "a single dab lands at about a third of its colour's strength" line is buried in the feature-scale section. It needs to be next to `load`: *a mass laid with a small brush needs two or three crossed passes to reach its own value.* |
| 10 | `c23` → `c24` | `block_in(span("F1","G8"), size=0.16)` stays in F–G | Overhang is 0.35 × brush, so it reached x≈0.572 and **ate the mug's right edge and the handle's cast shadow**. Cost about 15 strokes to restore. The guide warns about this — I had read it, and read it again afterwards. | Put `overhang=0` in the *example*, not in the warning paragraph. The default is the trap. |
| 11 | throughout | a cell over 0.10 is a cell I can fix | Six of my final nine have reference means **below the palette's floor**. `compare()` flags them identically to fixable ones and I chased them for ~25 strokes. | `compare()` should mark cells whose reference value is unreachable, and the guide should join up "the range is 0.23–0.96" with "the number that matters is 0.10". |
| 12 | `t1_coverage.py` | a throwaway test session is harmless | It writes to `out/look_001.png` in the same directory and would have overwritten the real session's looks. The guide does say this; it does not say to keep experiments in another directory. | "Run experiments from a different directory." |
| 13 | `c27` | I knew what counts as a stroke | `pencil`, `preview`, `rehearse` are explicitly free. `smudge`, `dab` and `glaze` are unstated — all three are billed. Three smudges and three dabs took me from 293 to 299. | One line listing exactly which calls increment `stroke_count`. |

Two more, lower down but worth saying:

14. The guide's "use a bigger brush than feels comfortable" and "`block_in` paints
    past its region" pull in opposite directions for any mass with a silhouette.
    The `edge(knots)` helper is the resolution and it appears once, in prose, in a
    section titled *A region is a rectangle*. It should be presented as the normal
    way to lay **any** shaped mass, with the guide's own `while x < 1.0` loop as
    the template. It is what I used for the mug, the crewmate and the shadow, and
    it is the only reason any of them has an outline.
15. `pressure="even"` on a `flat` brush is what you reach for when you want a solid
    mass, and using it for every mass is how I ended up with a blocky painting.
    The guide warns "you will under-vary your marks" but the concrete advice is
    "change `size`" — which does not help when the alternative (`bristle`) is
    ruled out above size 0.12.

---

## Engine defect

`s.erase(region)` clears the graphite from the canvas but leaves the line in
`s.sketch_lines()` complete, including every point inside the erased region.
There is no way to ask which lines are still actually drawn, so any workflow that
re-lays the drawing from `sketch_lines()` — which is the *documented* recovery
route, and the one I needed after the background block-in buried the underdrawing —
silently brings back the lines you deliberately rubbed out.

`t2_erase_sketchlines.py`:

```python
from easel import Session, span

s = Session(600, 400, ground="toned_grey", seed=1)
s.pencil([(0.05, 0.5), (0.45, 0.5)])          # wholly inside A1:D8
s.pencil([(0.55, 0.5), (0.95, 0.5)])          # wholly outside it

print("lines before erase:", len(s.sketch_lines()))
s.erase(span("A1", "D8"))
print("lines after  erase:", len(s.sketch_lines()))
for i, ln in enumerate(s.sketch_lines()):
    xs = [q[0] for q in ln]
    print(f"  line {i}: x {min(xs):.2f}-{max(xs):.2f}  ({len(ln)} pts)")
```

```
lines before erase: 2
lines after  erase: 2
  line 0: x 0.05-0.45  (2 pts)      <- erased, still returned whole
  line 1: x 0.55-0.95  (2 pts)
```

Not a defect but worth recording as measured behaviour: **the palette floor is
0.23 and nothing gets below it.** `shade(mix("ultramarine","burnt_umber", r), 1.0)`
lands on `#4a3728`, value 0.230, for every ratio I tried. That is documented; what
is not documented is what to do when the reference has a 0.06 in it.

---

## File map

Start by reading `c6_fixdrawing.py` (what I kept and threw away from the machine
sketch), then `c14a`/`c14b`/`c16a`/`c19` (the rehearsals that were rejected), then
`c23`/`c26` (working down the `compare()` list).

| File | What it is |
|---|---|
| `LOG.md` | this |
| `GOTCHAS.md` | the running record kept during the run, before this was written |
| `painting.easel` | the session; `python -m easel run painting.easel <script>.py` continues it |
| `copy_final.png` | the finished copy, 1200×900 |
| `copy_timelapse.gif` | the timelapse |
| `c1_prepare.py` | `prepare()` the reference, print the area table |
| `c2_areas.py` | try to work out which numbered area is which (bboxes only) |
| `c3_sketch.py` | merge the four wood areas, lay the machine sketch |
| `c4_inspect.py` | read the machine's drawing at the size of the mug |
| `c5_fine.py` | `grid="fine"` on the base and the spoon — the two things it missed |
| `c6_fixdrawing.py` | **erase the junk, set 8 landmarks, draw the spoon / base / tea / tag by hand** |
| `c7_values.py` | first value plan (throwaway session, plain `python`) |
| `c8_refvalues.py` | `compare()` against the bare ground — the reference's value map |
| `c9_values2.py` | second value plan, after the numbers said the table is 0.36–0.58 |
| `c10_wood.py` | the table, blocked in |
| `c11_woodfix.py` | cross the block-in seams, lay the grain, the dark corner |
| `c12_lines.py` | identify the sketch lines by bounding box after the paint buried them |
| `c13_redraw.py` | re-lay lines 3, 5, 6 clipped to the mug's neighbourhood |
| `c14a_rehearse.py` | **rejected mark 1** — slats, sawtooth, buried opening |
| `c14b_rehearse2.py` | **rejected mark 2** — olive highlights from `shade()` |
| `c15_mugpaint.py` | the mug's light mass, third try |
| `c16a_rehearse.py` | **rejected mark 3** — tea into wet paint, rim as a rope |
| `c16_opening.py` | fill the opening, dry, lay the tea on top |
| `c17_tea2.py` | cross the tea; re-state the mug in a blue grey instead of a teal |
| `c18_probe.py` | `compare(region=...)` in tenths, to find out what the tea landed at |
| `c19_darks.py` | the lip's shadow and the mug's shaded face; **rejected mark 4** |
| `c20_figure.py` | the crewmate |
| `c21_shadow.py` | darken the crewmate, lay the cast shadow row by row |
| `c22_compare1.py` | full `compare()` (re-run several times) |
| `c23_repair.py` | lift the wood, solidify the darks |
| `c24_restore.py` | undo the block-in's overhang damage to the mug's right side |
| `c25_features.py` | rim ring, handle, spoon, teabag, string |
| `c26_values3.py` | third value correction from `compare()` |
| `c27_final.py` | the last thirteen marks — scumbles, shadow, spoon, 3 lost edges, 3 highlights |
| `c28_finish.py` | `undo(1)` to get under 300, final compare, export, timelapse |
| `t1_coverage.py` | coverage probe — six patches of the same dark pigment |
| `t2_erase_sketchlines.py` | **the defect probe above** |
| `out/` | every `look`, `rehearse`, `prepare` and `compare` image, numbered |
