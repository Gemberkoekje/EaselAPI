# Rehearsal 3 — `pass` — log

Two paintings, made from `PAINTER.md` alone. No file in `src/`, `tests/`, `examples/`,
`scripts/`, any other rehearsal directory, or the installed package was opened, and no
`help()`, `inspect`, `dir()` or docstring was read. Everything below that isn't in the
guide was found by writing code and looking at pictures.

---

## The verdict, first

**Copy — is it recognisable as the object? Yes, but as a generic mug, not as *this* mug.**

Looking at `copy_final.png` with the photograph covered up, a viewer would say without
hesitation: a pale ceramic mug with a handle, full of something nearly black, with a
spoon standing up out of it, sitting on a wooden table in low light, casting a soft
shadow down and to the left, with a dark tea-bag tag on a pale string lying to the right.
The drawing is in the right place — the rim, the foot, the handle's outer sweep and the
spoon all land within about a fifth of a cell of where they are in the photograph.

What a viewer would **not** get:

- **That the figure on the mug is an Among Us crewmate.** The silhouette is there — head,
  backpack, the notch between two legs — but it reads as a mid-brown blob. The visor, the
  one mark that names it, is a faint pale smear rather than the crisp light oval it needs
  to be. This is the single biggest miss.
- **That the mug is glazed ceramic.** It reads closer to painted metal; the body is
  patchy with visible rectangles left over from earlier passes.
- **The wood.** The table is a warm field of the right values with a couple of grain
  marks; nobody would call it oak.
- **The label on the tag**, the bright rim highlight on the near lip, and the fine
  second hair of string in the foreground: all absent.

Honest flaws I can see and did not have the strokes to fix: the coffee's ellipse has a
stair-stepped top-left edge; the lower-right of the table has two pale slabs with harder
edges than anything in the photograph; there is a stray tan wedge inside the handle's hole.

**Own painting — `own_final.png`, "Low tide".** An estuary at dusk: luminous sky, a low
dark headland dying away on the left, three mooring posts with broken reflections, wet
sand in ribbons and a channel curving in from the bottom left. It reads as what it is.
Its flaw is horizontal banding — long horizontal strokes on a horizontal subject stack
into stripes, and the ripple marks I ran across them only half cure it.

**Stroke counts** (`s.stroke_count`; pencil and rehearsals cost nothing):

| painting | strokes |
|---|---|
| `copy_final.png` | **295** (budget 300) |
| `own_final.png` | **120** |

---

## The marks I tried and rejected

All three were tried with `rehearse()` on a copy of the canvas before any of them was
paid for. None appears in `s.log()`.

### 1. The rim as a drawn line — `out_copy/rehearse_011.png`

**Planned**: the whole back half of the rim in one `liner` pass at `size=0.005`, colour
at value 0.80, following the outer ellipse.
**What the rehearsal showed**: exactly the failure PAINTER.md predicts at line 396 —
"a drawn line around a painted shape". A broken white hairline sitting *on* the mug
rather than being the lit edge of a lip, and it left the cup's opening reading as bare
table underneath.
**Painted instead**: the same arc as a **mass** — `round_hard` at `size=0.024`, value
graded 0.76 on the back-left down to 0.505 on the front, in four arcs rather than one.
Compare `out_copy/rehearse_012.png` (the mass, at `size=0.028`, which showed me it was
*also* too thick and one flat value) with what shipped in `c9_cup.py`.

### 2. The crewmate as a block — `out_copy/rehearse_013.png`

**Planned**: fill `span("D4","E6")` with horizontal strokes — the fast way.
**What the rehearsal showed**: a brick rectangle, and it made the guide's warning at
line 405 ("If you block in a figure as a box you get a box") concrete in one image. It
also revealed the wetness problem below — the colour asked for value 0.235 and arrived
around 0.47.
**Painted instead**: strokes driven along the figure's own silhouette, top and bottom
edges from an interpolator (`c9_cup.py`, `ctop`/`cbot`).

### 3. The crewmate as bristle columns — `out_copy/rehearse_014.png`

**Planned**: the silhouette version above, `bristle` at `size=0.036` stepped `0.020`.
**What the rehearsal showed**: the shape was right and the mass was **not solid** —
visible ceramic between the columns, because a bristle stroke covers about three quarters
of its width and a half-width step does not close that. The mass averaged out pink.
**Painted instead**: `flat`, `pressure="even"`, `load=1.0`, stepped at half the brush
width (`c10_fix.py`).

### 4. (bonus) The coffee as bristle arcs — `out_copy/rehearse_016.png`

**Planned**: five bristle arcs at `size=0.038` following the ellipse.
**Showed**: a torn streaky rectangle that did not reach the rim at either end, mid-brown
where I wanted near-black.
**Painted instead**: vertical chords of the ellipse in `flat` at `load=1.0` on a dried
canvas, plus a crossed pass (`c11_repair.py`).

---

## The `compare()` numbers

First call, on the **empty** canvas: 41 of 64 cells out, largest 0.48.
Final call, after 295 strokes (`out_copy/compare_030.png`):

```
       A      B      C      D      E      F      G      H
  1  +0.04  -0.01  -0.02  -0.05  +0.05  +0.00  +0.04 +0.11*
  2  +0.02  -0.02  +0.01 +0.12* +0.16*  -0.02  +0.02  +0.04
  3  +0.01  -0.04  +0.07 +0.18*  +0.09  -0.02  -0.03  +0.01
  4  -0.00  -0.04  +0.03 +0.20*  +0.07  -0.04  -0.02  -0.00
  5  +0.02  -0.03  -0.01 +0.17* +0.12*  +0.01  -0.04  +0.02
  6  +0.03  -0.02  -0.00 +0.18*  +0.02  -0.06  -0.02  +0.04
  7  +0.06  -0.00  -0.03  +0.05  -0.03  -0.02  +0.04  +0.06
  8  +0.09  +0.01  +0.06  -0.01  -0.04  +0.04  +0.09  +0.06
8 of 64 cells more than 0.10 out; largest 0.20.
```

**Cells covering the main object that are still more than 0.10 out — seven of them, all
positive, i.e. my canvas is too light in every one:**

| cell | ref | canvas | delta | best reachable | whose fault |
|---|---|---|---|---|---|
| D4 | 0.14 | 0.34 | **+0.20** | ~+0.15 | mostly the palette floor |
| D3 | 0.22 | 0.40 | **+0.18** | ~+0.05 | **mine** |
| D6 | 0.12 | 0.30 | **+0.18** | ~+0.10 | mostly the palette floor |
| D5 | 0.06 | 0.23 | **+0.17** | **+0.16** | **entirely the palette floor** |
| E2 | 0.19 | 0.35 | **+0.16** | ~+0.03 | **mine** |
| D2 | 0.18 | 0.30 | **+0.12** | ~+0.09 | mixed |
| E5 | 0.32 | 0.44 | **+0.12** | ~+0.02 | **mine** |

(H1 at +0.11 is the dark corner of the table, not the object.)

**What I repaired, and what happened**: the c11 pass took it from 12 cells out to 8 —
`E7` went from -0.17 to +0.03 and `F6` from -0.15 to -0.02 by painting bright table back
over a shadow that overreached. But that repair was **value-correct and picture-wrong**:
it put a flat pale wedge with hard ends on top of the shadow, which `c12`/`c13` then had
to break up again. And `c12`'s own repair — a stroke meant to soften a light band on the
mug's upper body — ran straight across the crewmate's **head** and took D4 from +0.14 to
+0.23. `c14_head.py` exists only to undo that; it got D4 back to +0.20, not to +0.14.
That is the whole "chasing the number makes the painting worse" warning, twice, in my
own transcript.

**The residual is honestly about half floor and half budget.** D5 is at the floor already
(canvas 0.23; the darkest mixable value is 0.2182). D4 and D6 are nearly all crewmate and
near-black shadow in the reference and cannot get much closer. D3, E2 and E5 are mine: the
rim's front lip and the far inner wall are still wider and lighter than they should be, and
I ran out of the 300-stroke budget before fixing them.

---

## What the guide cost me, in the order it bit

Numbered as I hit them. Every one of these is a place I wanted to open the source and
didn't.

| # | Where I got stuck | What I expected | What actually happened | What I'd add to PAINTER.md |
|---|---|---|---|---|
| 0 | Session persistence | A documented `s.save()`/`s.load()`, since the brief asks for it | The API list (lines 727-749) has `export`, `timelapse_gif`, `log` and no `save`. I did not grep for one | Say plainly in *Working from a shell instead*: "There is no in-process `save`. Persistence is the `.easel` state file: `easel new` once, then `easel run state.easel pass1.py` per pass." |
| 1 | Picking a value plan | My read of the photograph would be roughly right | It was two stops out. I wrote "table ~0.70, mug lit ~0.85"; the reference is **0.06 to 0.58** end to end. `compare()` on the *empty* canvas gave me the reference's whole value map in one call | Add to *Put a number on it*: "**Run `compare()` before your first stroke.** On a blank canvas the delta column is the reference's own value map, per cell. It tells you the ground to pick and the values to mix, and it costs nothing." This is the highest-value call in the tool and the guide never suggests it |
| 2 | Choosing a ground | The seven grounds would be described enough to choose between | Names only, no values. I picked `toned_warm_grey` (0.54) for a picture whose mean is 0.41, so every gap read too light, and threw away the canvas | Print each ground's value in `easel brushes`, and one line: "pick the ground nearest the reference's mean value" |
| 3 | `compare()` in code | `str`-like, since the guide only ever `print`s it | `AttributeError: 'Comparison' object has no attribute 'splitlines'`. Same question unanswered for `prepare()` | One line in the API list: "`compare` returns a `Comparison` and `prepare` a preparation object; `str()` either for the table" |
| 4 | Matching the darks | "about `0.23` to `0.96`" would be a soft floor a glaze could push past | It is hard. I sanity-checked it myself (`probe_dark.py`): darkest mixable is **0.2182** (`desaturate(mix("ultramarine","alizarin",0.5), 1.0)` = `#383838`), and **six stacked glazes of it changed the canvas value by 0.00** | "Glazing dark over dark does not go below the pigment floor. If a passage in your reference is under 0.20 you cannot match it — match its neighbours and let it be the darkest thing you have." |
| 5 | **`rehearse()` lied — three times** | Guide line 272: "what you rehearsed is what lands" | It rehearses on the canvas **as it stands, wetness included**. Three marks came back mid-brown at ~0.47 when I had asked for 0.225. I lost real time assuming a coverage bug and wrote `probe_cover.py`. `c9_probe2.py` settles it: same stroke, `rehearse_017` (wet) mid-brown, `rehearse_018` (after `dry()`) a solid near-black slab | "`rehearse` and `preview` use the canvas exactly as it stands, **wetness included**. The plan list cannot express a `dry()`, so if the real mark will follow one, call `dry()` before you rehearse." Better: give `rehearse` a `dry=True` argument |
| 6 | Trusting `value_of` | That it predicted what a mark would look like | It predicts the *pigment*, not the mark. On dry canvas one pass gets 95% of the way (0.266 vs a 0.225 target, `probe_cover.py`); into wet paint it lands anywhere between | Next to `value_of`: "the value the paint reaches on **dry** canvas at full load" |
| 7 | **The pencil vanished under the first block-in** | Line 220: "it survives under a scumble and in the ground" | `block_in(region("all"), "flat", c, density=0.78, size=0.22)` erased the whole drawing. `probe_pencil.py` shows it goes at **`density=0.30`** too — 100% of the graphite signal gone in 7 strokes | Either fix the compositing or say: "a `block_in` with `flat` at any density erases graphite under it. Keep the drawing in your script, not only on the canvas." |
| 8 | Sharpening the mug's silhouette | Line 399: "a brush at least `0.03` wide, running along the boundary with its centre outside the shape" | I did exactly that and cut two tan stripes *into* the mug (`out_copy/look_010.png`), because "centre outside" isn't a number: with a brush of width `S` the centre has to be at `wall ± S/2` **and the stroke has to follow the wall**, not cross it. Mine drifted 0.028 inward over its length | Give the arithmetic: "centre the stroke at `edge ± size/2` so its inner half stops on the boundary, and give it the *same* slope as the edge — a straight stroke across a slanting edge crosses it" |
| 9 | Every block-in edge | That `block_in` regions would blend | The **value step between two adjacent block-ins reads as a rectangle**, which is a different problem from the documented `overhang`. My first table pass (`c4`) left four visible pale boxes that took three later passes to break up | Add to the `block_in` note: "adjacent regions at different values leave a visible step. Overlap them, vary size and density, and cross the boundary with a later pass" |
| 10 | Long horizontal strokes | Varying `size`, `pressure` and direction would be enough | On a horizontal subject they still **stack into bands** — visible in both paintings. The cure is marks that run *across* them, which is a composition decision, not a brush setting | One line beside "You will under-vary your marks": "strokes that all run the same way band, however you vary them. The cure is a pass that crosses them" |
| 11 | Losing my own evidence | The output numbering warning at line 703 is a parenthesis | Starting the second painting in the same directory reset `out/` to `look_001` and **overwrote six of the first painting's looks**, including three I had cited. There is no flag to set the output directory | Promote it out of the parenthesis, and add `--out DIR` to the CLI. Meanwhile: "copy `out/` before you start a second session in the same folder" — which is what I did after losing them (`out_pencil/`, `out_copy/`, `out_own/`) |

---

## What the guide got right — the instructions that changed the outcome

- **"Look every 5 to 15 strokes."** Not negotiable. Every single error above was found by
  opening a PNG, never by reasoning. `look_010` (tan stripes down the mug), `look_022`
  (the rim's front lip three times too wide), `look_023` (a pale slab where a number said
  the value was right) — none of those were visible in any number.
- **"A region is a rectangle. Almost nothing you want to paint is."** The one paragraph
  that most changed the picture. The mug, the crewmate and the shadow are all driven with
  the `edge(knots)` recipe straight out of line 414; the table is the only thing blocked
  in, and it is the only thing that came out looking like a field.
- **The fine grid and reading two digits off a label.** `look(region=cell("C2"),
  reference=..., grid="fine")` caught three placement errors — the mug's foot 0.023 too
  high, the shadow's left bulge 0.025 too far out, the tea tag 0.045 too wide — that I
  would have sworn were right by eye. Corrected before any paint, for nothing.
- **"Paint that lands on wet paint mixes with it."** The single most consequential
  sentence in the file. Everything dark in the copy was wrong until I put `s.dry()` in
  front of it.
- **"`pencil()` does not count as a stroke."** Two full drawings, one thrown away and
  redrawn from measurements, for zero budget.
- **"You build contrast by pushing the lights up, not the darks down."** Correct, and it
  stopped me wasting strokes trying to reach a black that does not exist.
- **`prepare()` as a reading tool** — used, and declared. `s.prepare("Level1.jpg")` gave
  me the reference's masses with values and hex in one call (lit ceramic 0.56, the mug's
  cool planes 0.44 `#70707A`, the darks 0.14) and told me the hardest edge in the picture
  is the crewmate against the white mug. I did **not** call `s.sketch()` and did not use
  its outlines; every pencil line in both paintings is mine, in `c1`/`c2`/`c3` and `o1`.

---

## Things that look like engine defects

### A. Graphite does not survive a scumble — `probe_pencil.py`

PAINTER.md line 220-221: paint covers the drawing "in proportion to how much actually
lands: **it survives under a scumble and in the ground**". It does not survive anything.

```
$ python probe_pencil.py
density 0.30: graphite band sd   9.78 ->  0.76 | signal left  0.00 of  9.38 (7 strokes)
density 0.50: graphite band sd   9.78 ->  0.76 | signal left  0.00 of  9.38 (8 strokes)
density 0.78: graphite band sd   9.78 ->  0.82 | signal left  0.08 of  9.38 (10 strokes)
density 1.00: graphite band sd   9.78 ->  0.66 | signal left  0.06 of  9.38 (12 strokes)
```

Nine heavy pencil lines at `pressure=0.85`, then one `block_in(region("all"), "flat", …,
size=0.22)`. At `density=0.30` — seven strokes, a scumble by any reading — 100% of the
graphite signal is gone. Either the compositing is wrong or the sentence is.

### B. `rehearse()` shows a different mark from the one you will paint — `c9_probe2.py`

Not a crash, but a tool that quietly returns the wrong answer, which is worse. The plan
list has no way to express the `dry()` the guide tells you to make, so any rehearsal of a
dark over recent paint is a rehearsal of a different colour. Reproducer: one stroke,
rehearsed twice, `rehearse_017.png` (mid-brown) vs `rehearse_018.png` (near-black slab).

### C. Not a defect, but worth a line in the docs

`compare()` returns a `Comparison` object. The guide only ever `print`s it, so the first
time you try to read one line out of it in code you get an `AttributeError`.

Nothing else lied. `block_in`'s overhang, the bristle's three-quarter coverage, the
`0.23` floor, `load_falloff`, the wet-paint mixing and the `0.10` compare threshold all
behaved exactly as documented once I had measured them.

---

## File map

**Deliverables**

| file | what |
|---|---|
| `copy_final.png` | Painting 1, the copy of `C:\temp\Level1.jpg`. 295 strokes |
| `copy_timelapse.gif` | its timelapse |
| `own_final.png` | Painting 2, "Low tide". 120 strokes, no reference |
| `own_timelapse.gif` | its timelapse |
| `LOG.md` | this file |

**Session state** — `copy.easel`, `own.easel`. Re-runnable: `python -m easel run copy.easel cN_*.py`.

**Painting 1, one script per pass, in order**

| script | pass |
|---|---|
| `c1_draw.py` | landmarks + first pencil drawing |
| `c2_fixdraw.py` | erase and redraw with three fine-grid corrections; first value plan |
| `c3_draw.py` | same drawing on the new `umber_wash` ground; two region compares to read the reference's local values |
| `c4_table.py` | the table, three value bands (34 strokes) |
| `c5_shadow.py` | cast shadow, first attempt (came out a hard bar) + wood grain |
| `c6_mug.py` | shadow repainted; mug blocked (came out a blue staircase) |
| `c7_mugfix.py` | mug repainted neutral; silhouette cut — which cut *into* the mug |
| `c8_rehearse.py` | the three rejected marks. No strokes |
| `c9_probe2.py` | wet vs dry rehearsal of the same stroke. No strokes |
| `c9_cup.py` | coffee, rim, crewmate |
| `c10_fix.py` | crewmate solid, rim knocked back, silhouette re-cut, handle, spoon |
| `c11_repair.py` | compare-driven repair — 12 cells out down to 8 |
| `c12_finish.py` | visor, tea tag, string, lit edge of the foot |
| `c13_last.py` | tag desaturated, string lost in two places, banding broken |
| `c14_head.py` | undoing `c12`'s stroke across the crewmate's head |

**Painting 2** — `o1_draw.py` (pencil), `o2_sky.py` (sky + wet sand), `o3_land.py`
(headland, posts, reflections), `o4_finish.py` (repairs + glints), `o5_last.py`
(cross-marks, birds).

**Probes** (my own diagnostic code, scratch sessions only) — `probe_dark.py` (palette
floor + glaze stacking), `probe_cover.py` (passes needed to reach a value), `probe_pencil.py`
(graphite survival), `probe_prep.py` (the `prepare()` read of the reference).

**Looks** — `out/` is live output. Preserved because a second session in the same
directory overwrites it:

| folder | what |
|---|---|
| `out_pencil/` | painting 1's pencil stage on the discarded `toned_warm_grey` ground, incl. the fine-grid measurements `look_005`/`look_006` and the first `compare_008` |
| `out_copy/` | painting 1's paint stage: `rehearse_011`-`018` (the rejected marks), `look_022` (the rim, close), `look_029` (final beside the reference), `compare_021`/`024`/`028`/`030`, `prepare_007` |
| `out_own/` | painting 2's looks, `look_001`-`008` |
