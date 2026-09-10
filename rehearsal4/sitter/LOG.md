# Level3 — copy log

**Stroke count: 299.** `compare("ref.jpg")`: **0 of 64 cells more than 0.10 out**, largest
deviation 0.10 (B6). No cell was ever flagged `~`.

---

## Is it him? — the honest answer first

**Partly.** In the finished picture the *pose* is unmistakable: a shaggy-haired man
seen in near-profile, head turned left, lit from behind and above, packed into the
right half of a dark room. If you had the photograph in your hand you would match
them without hesitation.

If you did not, you would say "a bearded man in profile in a dim bar". You would not
pick him out of three other bearded men in profile. **The likeness is in the
silhouette, not in the face.**

**What got there:**

- The **profile line** — brow ridge, the dip at the bridge, the nose, the shelf of
  the upper lip, the chin pushed forward. That is the best passage in the painting
  and it cost three strokes, laid as *background painted back up to the edge*, not
  as a drawn line.
- The **eye** — a dark almond, a pale wedge of sclera on the ear side, the iris
  crowded to the nose side, one 3-pixel catchlight. It looks at something. In the
  photograph the whole expression hangs on that eye and it survived.
- The **hair** — dark and lank over the forehead, lit and gold across the crown and
  down the right, falling onto the shoulder. Right shape, right value, right place.
- The **head's size and position in the frame**, and the coat's silhouette and its
  value. The big black diagonal is the composition and it is correct.
- The **brow**, and the mole on his neck.

**What defeated me:**

- **The open mouth.** This is the failure that matters, because the photograph is a
  picture of a man talking. In my copy it is a dark smear with a pink dot below it.
  The teeth — the brightest small thing in the reference and the thing that says
  *mid-sentence* — went on as a `dab` at `size=0.0055` and are invisible. I could
  not find a way to state a 20 × 8 pixel light shape inside a dark shape without it
  reading as either a blob or nothing.
- **The beard.** It is a dark polygon, not hair. It has a silhouette and no texture,
  so it reads as shadow under the jaw rather than as a beard.
- **The cheek and jaw.** One flat tan slab with two lighter bars laid on it. See
  "where the tools ran out".
- **The ear.** Two dabs. It is a smudge in roughly the right place.
- **The background people.** The raised gloved hand — a strong, memorable shape in
  the photograph — is a pink blob with three black claws. The man on the right is a
  striped patch. The beret woman I abandoned entirely after a preview showed my
  shape was in the wrong place.
- **The whole background reads as a patchwork of rectangles.** The checklist item
  "Is any mass a rectangle that should have been a shape?" fails, hard, across the
  left third and the right edge.

---

## What I did

Canvas 1200×800 (the reference is 1600×1068, same 3:2), `linen`, `toned_grey`,
seed 11.

1. **Surveyed before painting.** `compare()` on the empty canvas. That table is the
   photograph's value map in numbers and it is worth more than any amount of
   squinting: it told me the coat cells sit at **0.04–0.07**, the lit wall at
   0.58–0.68, and the *face* — the subject — at 0.28–0.36, i.e. a mid-tone. My eye
   would have painted the face as the light mass. It is not.
2. **Eight landmarks**, each read off a `grid="fine"` crop and then verified by a
   look with the marks drawn on both panels: `hair_top, brow, eye, nose, mouth,
   chin, ear, hair_r`. Two of them were wrong on the first placement and one
   (`nose`) was still ~0.011 too far left when the fine grid finally caught it, at
   which point the paint was already down.
3. **Two masses.** `upper-half` warm mid (0.36), `lower-half` near-black (0.134),
   both `flat`, big brush, one direction. **Ten strokes for the entire value
   structure of the painting.** This is the guide's best advice and it is not
   exaggerated.
4. Background modulation — lit wall right, dark shelf left, pale blur, table.
5. **Figure, back to front**: coat polygon → hair polygon → face polygon → beard.
6. Left-hand group (hand, glove, carton, glasses, the far man).
7. Head modelling — twice, because the first attempt was wrong (below).
8. Profile re-cut, eye, nose, mouth, beard corrections — all four rehearsed first.
9. Value corrections driven straight off the `compare()` table: 15 cells out → 12 →
   6 → 0.
10. Two smudges to lose two edges; export.

### No assisted modes

I did not call `sketch()`, `ref_shape()`, `ref_outline()` or `prepare()`. Every
coordinate in every script was read by me off a `look(..., grid=True)` or
`grid="fine"` crop and typed in. I also **did not use `pencil()` at all** — the guide
makes the underdrawing optional and I went straight from eight verified `mark()`
points to blocked-in masses. In hindsight that was a mistake: a pencil drawing of the
lower face would have cost nothing and would have caught the beard/mouth problem
before I had spent 24 strokes on it.

---

## Marks I tried and rejected

Every one of these was caught by a picture. The file named is the picture.

| # | The mark | The look that caught it | Why it was wrong |
|---|---|---|---|
| 1 | Coat polygon with the shoulder peaking at `(0.848, 0.376)` | `out/preview_015.png` | The shoulder ran up over the other man and the lit wall. Re-measured on `look_016.png`; the true peak is `(0.706, 0.372)`, a tenth of the canvas lower. |
| 2 | Hand polygon, 19 points | `out/preview_021.png` | Too small, too high, too far right — the fingers stopped where the reference's palm begins. Rebuilt 0.06 taller. |
| 3 | Beret polygon | `out/preview_022.png` | Landed on the fingers, not the head. Dropped the beret from the painting rather than spend more strokes finding it. |
| 4 | **16 hair strokes**, `bristle`, `size=0.022–0.040`, in `hair_l`/`hair_h`, sweeping along the hair's outer curve | `out/look_024.png` | Concentric golden arcs. A wig, not hair. Two faults at once: sizes 3× too big for a head 0.3 of the canvas wide, and every path following the *silhouette* instead of crossing the mass. **This one I paid for** — 16 strokes spent and 15 more to paint over. It is the only pass in the session I did not rehearse. |
| 5 | Face mass in `mix(burnt_sienna, cadmium_red, 0.30)` at 0.38 | `out/look_017.png`, `look_024.png` | A pink slab. The reference face is a desaturated tan. Repainted with `desaturate(mix(burnt_sienna, yellow_ochre, 0.42), 0.30)`. |
| 6 | Beard as 6 strokes at `size=0.026–0.030` | `out/rehearse_026.png` | Ran out onto the neck and read as a dark horseshoe. Never painted. |
| 7 | Hair lights as 6 strokes following the silhouette | `out/rehearse_027.png` | A rope tied round the head. Never painted. Replaced by a `ribbon` mass + strands crossing it. |
| 8 | Beard as a ring of strokes round the chin | `out/rehearse_029.png` | Left the chin light in the middle. Never painted. Replaced by a filled `polygon`. |
| 9 | Profile re-cut with `bristle` at `size=0.036` | `out/rehearse_035.png` | The comb chewed dark fingers into the cheek. Re-done with `flat` + `pressure="even"` in `rehearse_036` — clean chisel edge, and that is what got painted. |
| 10 | Eye as two `round_hard` discs side by side | `out/rehearse_035.png` | Two circles, a cartoon. Replaced by dark almond → pale wedge → iris → catchlight, which is the guide's own "three marks: the dark, the light, and the edge between them". |
| 11 | Nose highlight, `skin_v` at `size=0.009` | `out/rehearse_035.png` | A fat yellow oval sitting *on* the profile. Halved and dulled. |
| 12 | Coat's lit shoulder and lapel in `coat_l` (0.20) | `out/look_038.png` | Over a 0.134 coat it read as a pale grey scarf draped over him. Painted out with 7 strokes of `coat`. |
| 13 | Lower-left scumble, `opacity=0.5, load=0.8` | `out/look_033.png` | Orange glitter over the juice carton. Covered by restating the carton solid. |

Thirteen marks rejected: **nine of them never touched the canvas** (#1–3 caught by
`preview`, #6–11 by `rehearse`), and four had to be painted over (#4, #5, #12, #13).
Five rehearsals of the same square of face (`rehearse_026/027/029/035/036`) cost
nothing and are the reason the eye works. **`rehearse` is the best thing in this
toolkit** and I under-used it early — the one pass I skipped it on is also the one
that cost me 31 strokes.

---

## The smallest thing I placed where I meant it

`s.dab(0.4502, 0.3028, "round_hard", "titanium_white", size=0.0026, press=3)` — the
catchlight. Three pixels of white on the upper-left of a ten-pixel iris, positioned by
reading label `(6.1, 2.0)` off a `grid="fine"` crop of `D3:D4` and converting. It
landed exactly where I aimed and it is the mark that makes the eye look at something.

Runner-up: the mole on his neck, `(0.590, 0.441)`, `size=0.005`. It is there. Nobody
will ever see it.

---

## Where the tools ran out

**At the point where a mass had to change value across itself.**

Everything in the API stamps a flat colour with a shaped edge. To grade a cheek from
0.50 at the bone to 0.30 at the jaw there are three offered routes and all three fail
at mass scale:

- **wet-into-wet** — wetness drops ~6% per mark and a `block_in` is 4–18 marks, so by
  the time the mass exists it is dry. Usable for two strokes, not for a plane.
- **`round_soft`** — the guide itself says it airbrushes above `size=0.05`, which is
  exactly the size a facial plane needs.
- **`smudge`** — only redistributes what is already there; it softens a boundary, it
  does not build a gradient.

So a face becomes: one flat slab, plus bars of a second flat value laid on top. That
is what mine is, and it is why the face reads as a mask rather than a head. Nothing in
the guide told me this because the guide never has to grade a mass.

**Second place it ran out: the background vocabulary is rectangular.** `region`,
`cell`, `span`, `horizon`, `above`/`below` are all axis-aligned boxes. The guide is
emphatic that a box is the wrong decision "everywhere except a band or a flat plane",
and offers `blob/ellipse/hull/ribbon/polygon` as the answer — but for a blurred bar
interior with fifteen soft patches of tone, hand-writing fifteen polygons is not
affordable inside 300 strokes. So I laid boxes, and the finished painting is a
patchwork. That trade-off is real and the guide does not acknowledge it.

**Third: feature scale.** Below about `size=0.008` a `bristle` mark is four visible
stripes (the comb pitch is fixed at 0.005 of the long side), `flat` is a hard
rectangle, and `round_hard` is a disc. There is no mark that is small, soft *and*
directional — which is what teeth, an ear, a lip, an eyelid all want.

---

## The dark floor — the arithmetic the guide should do for you

15 of the 64 reference cells ask for a value **below the box's 0.13 floor**: C2 (0.07),
C3 (0.06), D5 (0.12), D6 (0.07), D7 (0.07), D8 (0.06), E6 (0.07), E7 (0.05), E8 (0.06),
F5 (0.04), F6 (0.05), F7 (0.05), G7 (0.11), H7 (0.10), H8 (0.12). That is a third of
the figure, not "a handful", and it is because the subject is wearing a black coat in a
lamplit room.

**None of them ended up out of tolerance**, and the reason is arithmetic the guide
states in two separate places without ever putting together: the floor is 0.13 and the
threshold is 0.10, so **anything the reference puts at 0.03 or above is reachable** —
you just have to cover the cell completely, at `density=1.0` and `load=1.0`, with the
darkest mixture. My worst dark cell finished at +0.09. The margin is thin (any light
mark you add inside such a cell spends it — my "lit shoulder" experiment pushed F5–F7
out by itself), but the wall the guide implies is not there.

I confirmed a supplied colour escapes the floor (`p.hex("#101014")` → `#101014`,
`value_of` 0.064) and then **did not use it**, because I did not need to. Worth saying
plainly: on this photograph the box was enough.

`compare()` never printed a `~` on any cell at any stage, including on the empty
canvas where six cells sat at 0.04–0.06. So I still do not know what triggers that
marker.

---

## What the guide got right

- **"Look every 5 to 15 strokes."** Every disaster in this session was caught by a
  look. The single pass I did not look at first (#4 above) is the only one that cost
  me strokes.
- **`preview` and `rehearse`.** Nine rejected marks above, eight of them killed before
  they touched the canvas. Free. Use them more than feels necessary.
- **The fine grid, and "read the two digits off the label; do not estimate a
  fraction."** Exactly right. Estimating off the coarse crop put my eye 0.009 off and
  my nose 0.011 off. The fine grid found both. The instruction is not padding.
- **"Sharpen an edge by painting the mass on the *other side* of it."** Three `flat`
  strokes of background laid down the left of the profile, centre outside the face.
  Best passage in the painting.
- **`compare()` twice, and the first one on an empty canvas.** The reference column is
  the whole plan. I would have painted this two stops light without it.
- **Mix to a value, not to a ratio** (exercise 1). The bisection helper from that
  exercise produced *every* colour in this painting. It should be in the API, not in
  an exercise.
- **"Use a bigger brush than feels comfortable, especially early."** Ten strokes for
  the two governing masses.
- **Back to front.** The hair went under the face, the face went over it, the
  background went back over the profile. Every edge in the head came out of ordering
  rather than drawing.

## What the guide got wrong, or left out

1. **It has no scale rule for features, and it needs one.** "Use a bigger brush than
   feels comfortable" is repeated four times and there is no counterweight. On a
   1200-px canvas with a head 0.3 wide, a facial plane wants `size≈0.015–0.025` and a
   feature `0.004–0.010`; I used 0.03–0.04 three separate times and had to repaint
   twice. A single line — *a mark should be a fraction of the thing it describes, and
   a head is 0.3 of the canvas* — would have saved me forty strokes.
2. **It never says the `bristle` comb is destructive below a certain size.**
   CALIBRATION gives the pitch (0.005 of the long side, fixed) but nobody draws the
   conclusion: a `bristle` stroke at `size=0.02` is four stripes, so it is the wrong
   brush for a cheek. `flat` at `pressure="even"` or `round_hard` is what small planes
   want. I learned this from `rehearse_035.png`, not from the guide.
3. **"Three marks at most — the dark, the light, and the edge between them"** is the
   most useful sentence in the document for painting a face, and it is buried at the
   bottom of the pressure section. It belongs in the workflow, next to step 6.
4. **No gradient story.** See "where the tools ran out". The guide should either name
   a technique for grading a mass or admit there isn't one.
5. **Nothing on what counts against the budget except the free list.** `pencil`,
   `erase`, `mark`, `preview`, `rehearse` are documented as free. It is never stated
   that `smudge` and `glaze` *do* count. I measured it (297 → 299 for two smudges) at
   a point where I had three strokes left and could not afford a surprise.
6. **`block_in`'s undocumented kwargs.** The guide says "anything about a brush can be
   overridden per stroke" but shows that only for `stroke()`. `block_in(...,
   opacity=0.5, load=0.8)` works — I guessed. Say so.
7. **The dark-floor arithmetic** (above). The guide frames the floor as a limit to be
   reported; it is mostly a limit to be beaten by covering properly.
8. **The region vocabulary contradicts the "no boxes" advice** and the guide never
   admits the tension.

---

## Moments I wanted to open the source, and what I wanted to know

1. **`ribbon(points, width)`** — is `width` the full width or the half-width? My lit-
   hair shell came out wider than intended and I could not tell whether that was the
   ribbon or the brush spilling.
2. **Does `smudge()` count against `stroke_count`?** (It does.) Same question for
   `glaze()`. The free list is exhaustive-looking but only lists the free things.
3. **Does `block_in` forward `opacity=` / `load=` / `pressure=` to its strokes?**
4. **What triggers `compare()`'s `~` marker?** Six cells at ref 0.04–0.06 against a
   0.54 canvas produced no `~`. Is it keyed on the reference value, on the delta, on
   the canvas value, or on something else?
5. **Does a named palette entry survive between `easel run` invocations?** (It does —
   I tested it with a print.) Nothing says so, so I pasted `to_value()` into all
   fourteen scripts.
6. **What width does `preview(shape.closed)` draw** when I pass no brush and no size?
   The blue band it renders is much wider than any brush I used, and I never knew
   whether I was looking at a silhouette or at a projected mark.
7. **Default `size` for `stroke`, `smudge` and `glaze`** when omitted.
8. **Does `undo(n)` decrement `stroke_count`?** I wanted to know whether "the number
   that counts" could be walked backwards. I did not use `undo` once — I painted over
   instead, as instructed — but I wanted to know.
9. **`direction=("axis", 62)`** — is the second element absolute degrees from
   horizontal, or degrees relative to the resolved axis? I assumed absolute and the
   results were plausible either way, which is the worst case.
10. **How far does paint actually spill past a `flat` stroke's nominal half-width?**
    My profile re-cut landed its edge about 0.006 to the right of where half-width
    arithmetic predicted, consistently, and I never worked out why. This mattered:
    it is the difference between a nose and no nose.
11. **What does `polygon()` do with winding order, or with a ring that self-
    intersects?** I hand-wrote five rings of 12–22 points and my only validation was
    `preview`.
12. **Whether `hull()` would have been cheaper than my hand-written polygons** for
    the face and coat — the guide mentions it in one line and never uses it on
    anything with more than three points.

---

## Files

- `copy_final.png` — the painting
- `copy_timelapse.gif` — the time-lapse
- `copy.easel` — the session (299 strokes, no assisted modes in the log)
- `p1_masses.py` … `p24_export.py` — the passes, in order
- `probe_palette.py`, `probe_palette2.py` — colour probes, run on `scratch.easel`
- `out/` — every look, preview, rehearsal and heat map, numbered

To understand this run, start by reading `p1_masses.py` (the two governing masses),
then `p19_rehearse4.py` and `p20_face.py` (the rehearse-then-paint loop that produced
the only good passage), then this log's rejected-marks table alongside
`out/rehearse_035.png` and `out/rehearse_036.png` — the before and after of the one
correction that mattered.
