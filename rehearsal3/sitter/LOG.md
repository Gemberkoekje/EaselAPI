# Sitting for Level3.jpg — one fresh session, guide only

Reference: `C:\temp\Level3.jpg`. Canvas 1200×810, `linen`, ground `umber_wash`, seed 11.
Final: **299 strokes** (`s.stroke_count`). The pencil drawing and the five
rehearsals/previews cost nothing and are not in that number.

Deliverables: `copy_final.png`, `copy_timelapse.gif`.

---

## 1. The verdict

**Recognisable as a person, not yet as *the* person.** Open `copy_final.png`: it is a
bearded man seen in near-profile, mouth open mid-sentence, wide eye under a heavy
brow, a shaggy mid-brown mop, a dark coat, a raised hand on the left, an orange
carton on the table. Put it beside the photograph and you would pick it out of five;
cover the photograph and you would not name him. The previous session got "a
recognisable scene made of unrecognisable things"; this one has a face that is built
rather than implied, and that is the difference the landmarks and the fine grid made.

Feature by feature, honestly:

| Feature | Verdict | Why |
|---|---|---|
| **Eye** | **Got there.** | Iris, both whites, a lid line above it, a catchlight, a socket shadow. Placed off `cell("D3")` at `grid="fine"` and it landed within a couple of pixels. The best thing in the painting. |
| **Brow** | **Got there.** | Right length, right slight arch, right value; it sits a touch high above the eye — in the reference there is less skin between them. |
| **Nose** | **Partly.** | The profile silhouette, the nostril, the shadow under the base and a lit ridge all read. It is blunter and shorter than his; no wing, no bridge structure. |
| **Mouth** | **Partly.** | An open dark cavity in the right place, one light tooth, a lower lip. Reads as a shouting mouth at canvas scale; at feature scale the teeth are one lump where the reference has two incisors, and the far corner is lost. |
| **Moustache** | **Partly.** | A dark band on the right diagonal, but too thin, and it merges into the beard instead of sitting over the lip. |
| **Beard** | **Got there as a mass.** | Correct footprint (moustache → chin → back along the jaw → sideburn), correct value, correct direction of growth. No individual hair texture; it is a shape, not a beard. |
| **Hair mass** | **Got there.** | Shape, fall, the lighter crown, the darker back merging into the coat, wisps at the top. The single most improved thing versus a "mass with streaks" — because it was painted as twelve graded strands with four different pressure profiles, not as one tone. |
| **Hairline** | **Partly.** | The strands falling over the temple work. The arc across the forehead is vague and the forehead reads slightly too tall and too pale. |
| **Jaw** | **Got there** — carried entirely by the beard's lower edge and the under-jaw shadow. |
| **Ear** | **Did not get there.** Three attempts (`c17`, `c19`, `c20`, `c25`, `c26`). It was an orange horseshoe, then a hard dark slab, and it ended as hair. In the reference it is a clear lit shape. See stuck-log #6 for why the repaints would not cover. |
| **The hand** | **Partly.** | Four fingers and a thumb in the right places, the palm joined, a knuckle shadow. They read as separate pale bars rather than one spread hand, and the fingerless glove does not read at all. |
| **The objects** | Carton: **got there** (shape, orange, the white cap, the label strip). Glasses bottom-left and the phone bottom-right: two pale streaks each, placeholders. |
| **The coat** | Silhouette and value right; **surface wrong** — eleven horizontal repair bands left it visibly striped, the most mechanical thing on the canvas. |

---

## 2. Marks I tried and rejected

All three were judged on a rehearsal or preview and never painted. The full text is
in `STUCK.md`; here is what each one showed.

### Rejected 1 — the hair repaint as flat/even slabs at value 0.30
**Planned:** twelve `flat` strokes, `pressure="even"`, `load=1.0`, colour `#61482c`
(0.30), along the strand paths, to darken a first hair pass that had come out pale
blond.
**The rehearsal showed** (`out/rehearse_021.png`): `flat` at `even` covers
completely, so twelve overlapping passes fused into one opaque slab — a wig-shaped
silhouette with no internal value and no direction, burying the ear and the temple.
**Painted instead:** the same paths with `bristle`, graded colours per strand and
four alternating pressure profiles (`out/rehearse_023.png`, painted in `c11`).

### Rejected 2 — the same repaint at the palette floor (0.23)
**Planned:** identical strokes in `#46372c` (value 0.23), on the theory that the
reference hair reads dark.
**The rehearsal showed** (`out/rehearse_022.png`): the head became a single black
hood continuous with the coat. Hair and coat at the same value collapsed the whole
silhouette and the back of the head disappeared.
**Painted instead:** graded — 0.23 only on the two lowest back strands (where the
reference *does* lose the edge into the coat), 0.27–0.30 through the body, 0.36–0.51
on the lit strands.

### Rejected 3 — the face as eleven vertical `flat` bars
**Planned:** eleven vertical `flat` strokes at `size=0.040`, `pressure="even"`, each
running from the hairline down to the beard line at its own x, plus eleven `bristle`
modelling strokes (forehead light, cheek light, socket, nose side, neck).
**The rehearsal showed** (`out/rehearse_025.png`): three separate failures at once.
(a) Every bar had its own length, so the mass came out as a **staircase** — hard
rectangular steps down both the brow and the jaw. (b) The `bristle` modelling strokes
at `load=1.0` printed as fat combed ribbons: the under-cheekbone shadow read as a
dark caterpillar lying on the cheek, not as a plane turning away. (c) The skin, mixed
from ochre + cadmium_red, was frankly orange (`#dfa95d`).
**Painted instead** (`out/rehearse_026.png`, painted in `c14`): thirteen *horizontal*
sweeps, one per 0.025 of height, each running from the profile edge to the jaw edge
at that height, at `size=0.026` so consecutive rows overlap — the left ends of the
sweeps *are* the profile, so there is no staircase. Skin re-mixed from burnt_sienna +
ochre + white. Modelling cut to two small `round_soft` marks.

(There was a fourth, unplanned rejection: the "blue flash" on his zip, painted in
`c22` as one `liner` stroke, turned out at head scale to be a bright teal slug lying
on the coat — `out/look_046.png`. Killed with one `flat` stroke in `c25`.)

---

## 3. Did the precision tools reach below a cell?

**Yes, and by a lot — but they stop about a factor of two above the finest thing in
this photograph.**

One cell here is 150 × 101 px. The smallest thing I placed *where I meant to* was the
**catchlight in the eye**, a `round_hard` dab at `size=0.0030` — 3.6 px, about
1/40th of a cell across. The tool that told me where it went was
`s.look(region=cell("D3"), reference=..., grid="fine")`: the crop is blown up ~5.5×
and labelled in tenths, so I read the pupil off as `cell("D3").point(0.65, 0.46)`
rather than estimating "about two-thirds across". `s.preview()` then drew the whole
eye plan — brow, lid, iris, both whites, lower lid — as brush-width bands over *both*
panels at that scale (`out/preview_029.png`), and I could see before spending a
stroke that the iris band sat on the reference's iris and the teeth band sat on the
reference's teeth (`out/preview_030.png`). Every one of the ten landmarks landed on
its feature on the reference panel; not one had to be moved.

**Where they run out.** Three places, concretely:

1. **Brush width.** The reference's upper eyelid line is ~2 px on this canvas
   (`size≈0.0018`). The guide says `round_hard` holds down to about `size=0.003`
   (3.6 px) and that is genuinely the floor. I painted the lid at 0.0034 and it is
   twice as thick as his. Below that the *drawing* is still exact and the *mark* is
   not.
2. **Reading a position off a `span()` crop.** The fine single-cell view is reliable;
   a multi-cell `span` crop with `grid=True` is not, and it is not obviously
   different. I read the nose tip as y=0.354 off `span("D2","F5")` and y=0.385 off
   `cell("D4")` with `grid="fine"` — a third of a nose apart. Same for the ear:
   0.523 vs 0.582. (Stuck-log #1 and #2.)
3. **Rehearsals judge marks, not passages.** `rehearse` was decisive for the three
   big rejections above because each was a *set* of strokes with one visual question.
   It could not tell me the ear would end up a slab, because the failure there was
   coverage after two earlier layers, not the mark itself.

---

## 4. The `compare()` numbers

Final table, 299 strokes: **28 of 64 cells more than 0.10 out; largest 0.23.**

```
       A      B      C      D      E      F      G      H
  1  -0.02  -0.02  -0.03  +0.01  -0.02  -0.03  +0.04  +0.04
  2  +0.13* -0.05  +0.23* +0.18* +0.08  -0.05  -0.05  -0.01
  3  +0.02  -0.02  +0.19* +0.15* +0.02  -0.00  -0.01  -0.01
  4  +0.05  -0.00  +0.10* +0.05  -0.02  +0.12* -0.02  -0.06
  5  +0.08  +0.05  +0.10* +0.21* +0.10* +0.19* +0.02  +0.07
  6  +0.07  +0.13* +0.10  +0.17* +0.17* +0.19* +0.08  +0.11*
  7  +0.11* +0.11* +0.06  +0.18* +0.19* +0.19* +0.14* +0.22*
  8  -0.03  +0.15* +0.09  +0.17* +0.17* -0.05  +0.11* +0.12*
```

Worst six, as `compare()` prints them:

```
C2 ref 0.07 canvas 0.30 +0.23   H7 ref 0.09 canvas 0.31 +0.22
D5 ref 0.12 canvas 0.32 +0.21   F7 ref 0.05 canvas 0.24 +0.19
F5 ref 0.04 canvas 0.23 +0.19   F6 ref 0.05 canvas 0.23 +0.19
```

**Seventeen of those cells cannot be fixed.** `c28_analyse.py` splits them: the
palette's darkest mixture is 0.23, so any cell whose *reference* value is under 0.13
can never come within 0.10 no matter what is painted there. Run it:

```
17 unreachable, 8 reachable
UNREACHABLE   C2(ref 0.07) H7(0.09) D5(0.11) C3(0.06) F5(0.04) F6(0.04)
              E7(0.05) F7(0.05) D7(0.06) D6(0.06) E6(0.06) D8(0.06)
              E8(0.06) G7(0.10) B6(0.12) H8(0.11) G8(0.12)
REACHABLE     D2(+0.18) D3(+0.15) B8(+0.15) A2(+0.13)
              F4(+0.12) H6(+0.11) A7(+0.11) B7(+0.11)
```

F5, F6, F7 already sit at 0.23–0.24, i.e. *at the floor*. There is no stroke left to
spend on them. The eight reachable ones are my error: `D2`/`D3` are the hair and
forehead, still lighter than his; `B7`/`B8` the carton, painted brighter than the
photograph; `A2`/`A7` the dark left background, not dark enough; `F4` the hair's back
edge; `H6` the table.

**What repairs actually did.** At 249 strokes the table was 34 cells out. The single
biggest gain was `c22`: the first coat pass had been long vertical strokes that ran
dry, leaving rows 5–8 sitting 0.15–0.20 light; eleven short horizontal bands at
`load_falloff=0.0` brought most of them to the floor. The single most efficient
stroke of the whole session was the last one: `H5` was `+0.32` (I had painted a lit
table where the reference has his shoulder) and one `flat` stroke took it to `+0.07`.

---

## 5. What the guide cost me, in the order it bit

Running notes were kept live in `STUCK.md`; this is the same list with the fix I
would put in `PAINTER.md`.

| # | Where I got stuck | What I expected | What happened | What I'd add to PAINTER.md |
|---|---|---|---|---|
| 1 | `s.look(region=span("D2","F5"), grid=True)` | The crop labelled with the canvas's own D2…F5 cells | The crop carries a **fresh local A–H/1–8 lattice** — 3 canvas cells wide, 8 labels across. Cost a wasted look and the same arithmetic done twice. The misleading sentence is *"the same A-H / 1-8 cells on each"*: true of the two panels, false of a crop against the whole canvas. | One line under *Looking*: "A `region=` crop is re-gridded 8×8 **in its own space**. `grid=True` on a crop never shows the canvas's cell names." |
| 2 | Reading feature positions off that span crop | Positions accurate enough for a landmark | Nose tip y=0.354 from the span crop, y=0.385 from `cell("D4")` fine — 25 px, a third of a nose. Ear 0.523 vs 0.582. I nearly opened `Region.point` over it. | "Span crops name masses. **Single-cell fine crops place points.** Never take a landmark off a multi-cell crop." |
| 3 | First `compare()`, 35 strokes in | The 0.10 rule to be a to-do list | 29 of 64 cells out, and the named ones were cells I had *just* painted with the darkest mixture that exists. Nothing I could paint would move them. The checklist line *"does `s.compare` leave any cell more than 0.10 out? Those are the last strokes worth spending"* is, on a low-key photograph, an instruction to spend strokes that cannot work. | "Before you use the 0.10 rule, subtract the floor: run `compare()` on the bare ground and note every cell whose *reference* value is below 0.13. Those can never come in. Contrast there is made by lightening their neighbours, not by darkening them." |
| 4 | Predicting where a `block_in` would land | Overhang symmetric and small | `size` is a fraction of the **long** side, so on 1200×810 a brush of `size=0.13` is 0.13 of the width and 0.19 of the height in 0..1 space. Every overhang estimate has to be done twice, once per axis. Measured spill for `size=0.10`: sides 0.050/0.042 ✓, **top 0.032, bottom 0.058** — the bottom is over twice the guide's "0.025 taller", and asymmetric. | Say the anisotropy out loud next to the `size` line, and correct the overhang figures: "roughly 0.05 on each side, 0.03 above and **0.06 below**." |
| 5 | The first coat pass (16 long vertical strokes, `load=1.0`) | A dark mass | Rows 5–8 came out 0.15–0.20 too light. The strokes were 0.4–0.6 of the canvas long; the brush emptied. 22 strokes wasted, ~7% of the budget. The guide *does* warn ("a long stroke shows it") but the warning is in the brushes section and the temptation is in the workflow section. | Put it where the silhouette-walk recipe is: "The walk strokes in this example are long. Pass `load_falloff=0.0`, or lay the mass in short bands, or it will come out a value light and you will not see it until `compare()`." |
| 6 | Repainting the ear with `bristle` at `load=1.0` over dry paint | Coverage | The orange stayed. Twice. *"Pass `load=1.0` explicitly when you are covering"* and *"a bristle is never solid: one pass covers about three-quarters of its width"* are forty lines apart and only the first is memorable when you are fixing something. Measured: same colour, same size, same load — bristle band 0.29, flat band 0.23, paint's own value 0.23. | One sentence in the brush table: "`bristle` **cannot cover**. If the point of the stroke is to remove what is underneath, use `flat` or `round_hard`; `load` does not change this." |
| 7 | Painting an eyelid | To go as small as the feature | The lid line here is ~2 px (`size≈0.0018`); the floor is `size=0.003`. The guide says the floor but never says what to do when the feature is under it. | "Below `size≈0.003` you cannot make the mark thinner — you make it *shorter and lighter*. A feature under 3 px wide is painted as its shadow, not as its line." |
| 8 | Starting each pass script | Not knowing whether `palette[...]` and `mark()` survive between `easel run` calls | The guide says a script has "`s`, `palette`, and the whole API already in scope" but never says whether *my* additions persist. I defensively re-declared every mixture in all fourteen paint scripts. (They do persist; so do marks. I tested it at the end.) | One line under *Working from a shell*: "Everything you add to the session — mixtures, marks, the drawing — is saved in the `.easel` file and is there in the next `run`." |
| 9 | `s.look(sketch=False)` for the "cover the reference" check | A clean picture | `sketch=False` hides the pencil; the named **marks stay on**, yellow crosshairs and labels, on every look. The checklist asks you to look at the painting alone, and there is no `look()` that gives you that. | "`export()` is the only mark-free view. `sketch=False` hides graphite, not landmarks." |
| 10 | Deciding how many landmarks | Guidance | "six or seven, checked at feature scale. A dozen is not twice as good" — for a *face* six or seven is not enough; I used ten (eye, both brow ends, nose, mouth, chin, ear, temple, crown, back of hair) and every one earned itself. The rule is right for a still life and wrong for a head. | "On a head, the six-or-seven rule is a floor, not a ceiling: eye, brow, nose tip, mouth, chin and the two ends of the hair mass are all load-bearing, and none substitutes for another." |

---

## 6. What the guide got right — the instructions that changed the outcome

- **"Look every 5 to 15 strokes."** Every single correction in this session came from
  an image, never from reasoning. The two worst marks (the teal zip slug, the orange
  ear horseshoe) were invisible in the plan and obvious in the first look.
- **The fine grid + landmarks section.** *"Read the two digits off the label; do not
  estimate a fraction."* This is the whole reason the eye is in the right place. Ten
  landmarks read off tenths, ten landmarks correct on the first try. The previous
  session's face failed at exactly the step this section exists to fix.
- **Marks are drawn on both panels.** That is what makes a landmark verifiable rather
  than hopeful. `look_012.png` — the pencil drawing with all ten crosses on both
  panels — is the single most useful image of the run.
- **`rehearse` before spending.** Three of my planned passes were bad and all three
  were killed for free. A 12-stroke hair pass and a 22-stroke face pass rejected on
  a rehearsal is 34 strokes — more than a tenth of the budget — saved.
- **"Paint the mass on the *other* side of the edge."** The profile only started to
  read when I stopped trying to draw it and instead laid the dark background *up to*
  it with a `size=0.034` `flat` (`c15`). Immediate, obvious improvement.
- **"A region is a rectangle. Almost nothing you want to paint is."** The `edge()`
  silhouette walk is the right shape of tool and gave a real coat outline. (Its
  strokes ran dry — see gap #5 — but the technique was right.)
- **"You build contrast by pushing the lights up, not the darks down."** Correct, and
  load-bearing on this reference, where two thirds of the picture is below the floor.
- **"Print `hex()` of a mixture before you paint a field of it."** My first skin mix
  was `#dfa95d` — traffic-cone orange — and printing it is what caught it.

The instruction I found least useful was *"stop when no cell is more than 0.10 out"*
(gap #3) and the one I under-weighted was *"you will under-vary your marks"* — the
coat's eleven identical horizontal bands are exactly the failure it warns about, and
I made it anyway because I was chasing a `compare()` number.

---

## 7. Possible engine defects

`defect_demo.py` (plain `python defect_demo.py`) demonstrates two, by painting and
then measuring the exported PNG. Neither reads the engine's source.

**A. `block_in` overhang is asymmetric and the guide's vertical figure is 2× low.**
A single `cell("D4")` blocked in at `size=0.10` on 1200×810:

```
cell D4 asked for : x 450..600  y 304..405  (px)
paint actually at : x 390..650  y 278..452  (px)
spill left/right  : 0.050 / 0.042 of canvas width
spill top/bottom  : 0.032 / 0.058 of canvas height
```

Documentation defect rather than a code defect, but it is the kind that puts a shirt
on a face: something blocked in *above* a neighbour drops onto it more than twice as
far as the guide leads you to inset for.

**B. `bristle` at `load=1.0` cannot cover, and nothing in the API tells you.**
Same colour (value 0.23), same size, same load, over the same dry bright ground:

```
under-colour  #fec51d value 0.80
over-colour   #393942 value 0.23
bristle band  measured value 0.29
flat band     measured value 0.23
```

A 0.06 error — more than half of `compare()`'s own threshold — from one stroke that
you *believe* is a solid correction. `s.log()` reports it as having laid plenty of
paint, so the diagnostic the guide points you at does not catch it.

**Not defects, checked and cleared:**
- `compare()`'s greyscale is plain Rec.709 luma on the cell's mean colour — I verified
  it against its own printout (`#18110D → 0.07` ✓, `#21140E → 0.09` ✓, `#271B12 →
  0.11` vs its 0.12), which is how `c28_analyse.py` reproduces it to within 0.01. The
  numbers are honest.
- The eleven "coat" bands in `c22` *looked* pale blue-grey in the downsampled look and
  I wrote them off as a failed call; `s.log()` and `compare(region=…)` both said
  `#413F43`, value 0.25, i.e. correct. That was simultaneous contrast against the
  ochre next to it, in me, not in the engine. Worth recording because it nearly cost
  me a repaint: **check a suspicious passage with `compare(region=…)` before you
  believe your eye about a small dark area next to a bright one.**
- Palette entries and named marks do persist across `easel run` invocations.

---

## 8. File map

*To understand this run, read in this order:* `LOG.md` (this file) → `STUCK.md` (the
live stuck-log) → `c5_pencil.py` (the drawing and the ten landmarks) → `c13`/`c14`
(the face rehearsal that was rejected and the one that was painted) → `c16`/`c17`
(the feature preview and the features) → `defect_demo.py`.

| File | What it is |
|---|---|
| `LOG.md` | this write-up |
| `STUCK.md` | the running stuck-log, written as it happened, 9 entries + the 3 rejections |
| `painting.easel` | the session; `python -m easel run painting.easel <script>` continues it |
| `copy_final.png` | the finished painting, 1200×810 |
| `copy_timelapse.gif` | the whole session |
| `c1_setup.py` | value plan, first gridded look at the reference |
| `c2_lookhead.py`, `c3_lookmore.py`, `c4_lookear.py` | looking only — head passage, then `cell(...)` + `grid="fine"` for D2, D3, D4, D5, E3, E5, and the hand |
| `c5_pencil.py` | ten landmarks + the pencil drawing (22 lines, 0 strokes) |
| `c6_background.py` | background masses (35 strokes) |
| `c7_coat.py` | the `edge()` silhouette walk for the coat + background darks (49) |
| `c8_hair.py` | first hair pass — came out pale blond (22) |
| `c9_hair2.py` | **rehearsals 1 and 2, both rejected** (0) |
| `c10_hair3.py` | **rehearsal 3, accepted** (0) |
| `c11_hairpaint.py` | the hair, painted (18) |
| `c12_face_try.py` | **face rehearsal, rejected** — the staircase (0) |
| `c13_face_try2.py` | **face rehearsal B, accepted** (0) |
| `c14_face.py` | the face mass, painted (18) |
| `c15_beard.py` | the profile cut, the beard, the moustache (15) |
| `c16_feat_prev.py` | **`preview()` of the eye and the mouth over `grid="fine"`** (0) |
| `c17_features.py` | eye, brow, nose, mouth, ear (21) |
| `c18_repair_head.py` | the eye was a dark crescent, the mouth a cream bar — rebuilt (27) |
| `c19_headfinish.py` | ear, beard mass, forehead glaze, strands (18) |
| `c20_hand_objects.py` | hand, glove, carton, glasses, background figures (26) |
| `c21_measure.py` | `compare()` at 249 strokes (0) |
| `c22_darken.py` | the coat re-laid in bands with `load_falloff=0` (23) |
| `c23_diag.py` | `s.log()` + `compare(region=…)` diagnosis of those bands (0) |
| `c24_scene_fix.py` | scene tidy (6) |
| `c25_final_head.py` | kill the teal slug and the ear blob, blend, two highlights (14) |
| `c26_last.py` | last six accents (6) |
| `c27_export.py` | the 299th stroke (worst cell H5), final `compare()`, export (1) |
| `c28_analyse.py` | splits `compare()`'s out-cells into reachable / unreachable |
| `defect_demo.py` | the two measured findings in §7 |
| `demo_a.png`, `demo_b.png` | that script's output |
| `out/` | 58 images: `look_001`–`look_058`, `preview_029`–`030`, `rehearse_021`–`026`, `compare_018/040/045/053/054` |

Only `PAINTER.md` was read. No engine source, no `help()`, no `inspect`, no
docstrings; `s.sketch()` was never called and the drawing is entirely `s.pencil()`.
`s.prepare()` was **not** used either — I read the reference with gridded looks and
fine crops only.
