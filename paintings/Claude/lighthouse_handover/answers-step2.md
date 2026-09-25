*The painter's answers to the five questions step 2 of
[`PLAN-0.7.0.md`](https://github.com/Gemberkoekje/EaselAPI/blob/v0.7.0/PLAN-0.7.0.md) left, pasted here verbatim. They were put to
it as a package -- the candidates under letters first, blind, and the key after -- which
is filed as [`questions-step2/`](questions-step2); the letters and crop numbers below
are that package's. Its one measurement is
[`verify/measure_ground_edges.py`](verify/measure_ground_edges.py), re-run on the same
sheet to the hundredth. On question 13 it left the deciding crop to the owner, who read
`crop_01` as speckle.*

---

# Answers to the five questions from the bench

*For each answer, say which half you looked at (O), measured (M) or reasoned (R). "Can't
tell" is an answer.*

## Part 1 -- blind (before opening `KEY.md`)

*One thing to declare before the blind half: the message that came with this package
already named the bench's picks (A2 at 0.002, and B1+B2). It did not say which letters
those are, and I have not opened `KEY.md`, `labelled/` (bar the two graded references
Part 1 allows) or anything else before writing this part.*

### 10a. Which edge reads as paint?

- Ranking, most paint-like to least, at the painting's size (A-D): **B, A, C, D** -- with
  C and D nearly a tie at 1:1, and A's place depending on the subject (below).
- Does any read as a painted edge? Which? **B.** The geometry holds -- the tower stays a
  tower, the burial stays a rectangle -- and the edge breaks, the way a loaded brush
  stops. It is the only one that does both on the tower at 1024x768. At 1440x960 1:1 it
  starts to read a little chewed on the shaft, less than A; the bites may want to scale
  with the canvas rather than stay the same size.
- Does any read as blur? Which? **C**, enlarged: the tower x3, the mass on bare ground and
  the burial each show a soft, even ramp. At 1:1 it is barely distinguishable from D --
  clean, and no more painted.
- Does any read as ragged or damaged? Which? **A.** The shaft looks crumbling at 1:1 and
  at 1440, the burial is a torn patch, the mass on bare ground is torn. It is the only
  one I would call paint-like on the rock (the plain-outline headland, where the fringe
  reads as grass and broken stone), and wrong on everything made.
- Kind (O/M/R): **O** on all six sheets; **M** on `q10_ground.png`, the steep left edge of
  each mass, per row, in canvas pixels (the sheet is x2):

  | | wander about a straight line (sd) | largest bite | pixels of in-between value across the edge (median) |
  |---|---|---|---|
  | A | 0.50 | 1.27 | 0.5 |
  | B | 0.38 | 0.91 | 0.5 |
  | C | 0.14 | 0.29 | 1.0 |
  | D | 0.24 | 0.44 | 0.5 |

  So A and B are as sharp as D and broken; C is the only soft one, and the straightest;
  D's wander is its stair-steps. That matches what I saw.
- Anything else: D is hard with stair-steps down the tower's taper -- what I measured on
  my own export -- so I guess D is the engine I painted with; that is a guess, not a
  reading. On the burial, all four still read as a rectangle: an edge treatment changes a
  cut-out patch (D) into a painted patch (B), not into something that is not a patch.

### 12a. Which starved brush reads as a dry brush?

- Ranking, most like a dry brush dragged to least (P-T): **S, T, Q, R, P.**
  - **S** -- streaks along the stroke, broken inside by the tooth, chunky and varied: a
    dry brush dragged. Clearest on exercise 3 at 0.35 and on the surf.
  - **T** -- streaks too, thinner, more regular and more continuous: combed more than
    dragged. A close second; it lays the heaviest surf.
  - **Q** -- short separate dashes along the stroke: a fine woven grain on exercise 3, fish
    scales on the flat sky.
  - **R**, **P** -- the same pattern of blotches and square flecks (Swiss cheese at 0.6,
    crumbs below), R fainter than P. Dots, not streaks.
- Which read as dirt? **P** plainly -- the dark flecks on the sky and the blue specks in the
  surf are what I got in my own session. **R**, fainter. **Q** on the flat sky field at
  0.45 and 0.6, where separate dashes in a smooth field read as flecks.
- Kind (O/M/R): **O**, all three sheets.
- Anything else: S and T lay visibly more paint at the same load -- on the crosser at 0.3
  they show clear streaks where P and R show almost nothing, and T's surf is much the
  brightest. So by eye I cannot separate "streaks" from "more paint"; the version I would
  want to see is S or T tuned to lay what P lays at each load.

### 13a. Graded passage, or separate things? (T / F / ?)

| crop | T / F / ? | a few words on why |
|---|---|---|
| crop_01 | F | a mixed set -- the passes of one light patch, a long stroke up a finger and a separate cream highlight; the patch reads as speckle, no bars |
| crop_02 | ? | it does come back as vertical bars; but it may be a row of hanging strips, and then the bars are the subject (F). One surface (T) or strips (F), I can't tell from the crop |
| crop_03 | F | the passes of three masses -- a dark field, a pale plank, a green field -- strung together because they run parallel; none reads as bars. My headland misfire's shape |
| crop_04 | T | one mass, water darkening toward the viewer, and the passes show as faint horizontal bands; on water they half-pass as swells, but they are bars |
| crop_05 | T | one beam laid as five strokes from a source; it comes back ribbed, a fan of streaks rather than a cone |
| crop_06 | F | two pot rims, a bowl's rim and base, a handle: five objects in five places |
| crop_07 | F | a slab and four thin dark lines ruled across it (x3 to see). They do read as mechanical hatching -- a real fault -- but not as a graded passage: one colour of line laid on a mass, not a passage stepping between values |
| crop_08 | F | a rowboat's near side reads as a lit gunwale over a darker hull -- structure, no bars |
| crop_09 | T | one pale band laid as nine strokes across it; faint vertical seams show, as if built of panels |
| crop_10 | F | a passage -- the inside of a bowl -- but it does not come back as bars. Not "separate things"; the line's prediction just doesn't hold here |

Kind: **O** on all ten, plus the two references; crop_07 enlarged three times to see.

## Part 2 -- open

*Blind and open agree on the edges: my B is A2 at `0.002`, my A is A2 at `0.003`, my C is
A1 at `0.002`, my D is today -- the one guess I made in Part 1. On the dry brush my S is B2
and my T is B1+B2, so I put B2 a little above the bench's pick. On the crops I agree with
the bench on five and differ on five.*

### 10b. The edge, by name

- For made things (the tower, the lantern, the cap), the candidate and the feather:
  **A2 at `0.002`.** It was my first pick blind, before I knew it was the bench's.
- For rock: **`roughen()` (A3 as written) for the outline, and the default edge on top of
  it** -- no wider feather. A2 at `0.003` was the only place A read well to me, on the
  *plain* outline, where its fringe passes for grass and broken stone; that is a
  `feather=0.003` a painter without a rough outline can ask for, not a default. The bench
  is right that the outline moves the headland more than any feather does: the two rows
  of `q10_headland.png` differ at a glance, the four columns barely.
- Or: none reads as paint, so ship the feather opt-in at 0: **no** -- A2 at `0.002` does.
- Kind (O/M/R): **O** blind and labelled; **M** on the bare-ground sheet (10a's table).
- One reservation, **O**: at 1440x960, 1:1 and on `edges_tower_1440x960_x3.png`, A2 at
  `0.002` reads a little chewed to me -- nearer A2 `0.003` at 1024 than A2 `0.002` at 1024.
  The feather there is 2.9 px, about the 3.1 px where both of us call it ragged at 1024.
  **Can't tell** why from here: if the weave is a fixed number of pixels, the feather that
  reads as paint may be a pixel count (about 2) rather than a share of the long side; if
  the weave scales with the canvas, ignore this.

### 11. Should the default reach `clip=`?

- (a) as decided / (b) `clip=` feathers too, inward / (c) something else: **(b).**
- Why: it is not a reversal of my decision -- it is my decision, which (a) mistranslated.
  I listed 9 edge-drawing calls and four of them were clips: the tower, its lit side and
  the lantern twice, the exact strokes my verdict was about. I kept containment clips hard
  *only because of an outward feather*, and offered the other way out in the same
  sentence: "feather inward, or leave containment clips hard". Since the engine cannot
  tell the two kinds of clip apart, "`clip=` keeps 0" drops the half of the decision that
  mattered, and the `default only` panels of `edges_tower_1024x768.png` show it: the tower
  is today's, and only the cap moves. Inward, a clip cannot carry paint past its outline,
  and on `edges_containment_x4.png` I see no rim of the mass beneath at any candidate,
  `0.003` included. **The horizon takes `feather=0`**: it is the one line I ruled on
  purpose, and no sheet shows it feathered, so I can't say whether A2 would harm it.
- Kind (O/M/R): **O** (`edges_containment_x4.png`, `edges_tower_1024x768.png`),
  **R** on the decision.

### 12b. The dry brush, by name

- The candidate: **B1+B2** -- I accept the bench's pick over my own blind order, for its
  reason: B2 does nothing on a flat or a round, and B1 does (`flecks_sampler.png`, the
  lower rows). On bristles alone I slightly preferred B2 (my S): it keeps some tooth among
  its streaks, where B1+B2 reads cleaner and more regular -- combed rather than dragged.
  After tuning, both will look different; I'd look at the crosser at `0.45` again with
  B2 and B1+B2 side by side, and if B1+B2 reads combed, shorten B1's kernel on tips that
  have a comb.
- Tuned to lay about today's paint at each load: **yes -- that is exactly what I meant.**
  I chose my loads from the guide's broken-mark window, and their weight was right; what
  was wrong was the shape, dots instead of streaks. A tuned B keeps the loads' meaning and
  changes only the shape.
- Kind (O/M/R): **O** (blind sheets and `flecks_sampler.png`), **R**; the amounts are the
  bench's **M**.

### 13b. The graded rule

- (a) the plan's gate / (b) the bench's variant / (c) leave it as it stands / (d) something else:
  **(d): the 30% overlap break on its own, without the median clause -- if the owner reads
  `crop_01` as I do. If the owner reads it as the bench does, (c).**
- Why: the plan's condition is a gate that keeps every true positive the human calls a
  passage. By my Part 1 T/F (T: 04, 05, 09; F: 01, 03, 06, 07, 08, 10; ?: 02), against
  the gate table in `KEY.md`:

  | gate | keeps my T's | still fires on my F's |
  |---|---|---|
  | as it stands | 05, 09 -- misses 04 | 01, 03, 06, 07, 08, 10 |
  | median | none | 01, 06, 07, 10 |
  | overlap 30% | **04, 05, 09 -- all three** | 03, 07, 10 |
  | both (the plan's) | none | 07, 10 |
  | trimmed | 09 | 01, 03, 06, 07, 10 |
  | trimmed, 10% | 09 | 03, 07, 10 |

  **The overlap break alone is the only gate that keeps every passage I called**, and it
  halves the false ones. On the four cases it silences my water misfire, keeps the
  recipe's passage silent and its failure block firing. What it leaves is one kind of
  false positive: the fields of separate masses stacked, like my headland misfire and
  `crop_03`. The median clause does not fix that kind without losing both beams, so that
  kind wants another clause if it wants one at all. The deciding crop is `crop_01`:
  the bench reads it as a finger hatched in stripes, and on a second, open look at the
  left half enlarged I still see speckle, not stripes -- `?` at most. Two readers split
  on the one crop that decides it, so the owner's own look at `crop_01` settles it.
  (If B lands, starved hatching like `crop_01`'s turns from dots into streaks, and may
  start to read as the stripes the bench sees.)
- Kind (O/M/R): **O** for the readings, **R** against the table.

### 14. Parallel panels

- D1 declined -- yes or no: **yes.** The target was missed (1.6-1.7x against 1.5), and
  the bench shows my variants' cost was the paint (10.2-10.6 s of 10.4-10.7), which
  parallel panels would not have taken away. What I needed was D0 -- scripts as
  side-by-side alternatives -- and that is built either way.
- Kind (O/M/R): **R**, on the bench's **M** and my own timing.

## Anything the bench got wrong

1. **Question 11's framing.** (b) does not reverse my decision; (a) mistranslated it (see
   11). The plan quotes my answer 1 correctly; its *what it changes here* column --
   "`edge="hard"` moves, `clip=` does not" -- is the plan's reading of it, and that
   reading is what (a) builds.
2. **A2 at `0.002` at 1440** reads a little chewed to me, where the bench says it holds
   (see 10b). One eye against one eye.
3. **The crops.** I differ from the bench's readings on five: `crop_01` F (bench T),
   `crop_02` ? (T), `crop_04` T (?), `crop_07` F (?), `crop_10` F (T). Two of those decide
   13b.
4. **The fade, a small one.** "It does reach the field at the very end" is generous at
   opacity 0.9: the last 4% reads `0.183` on a `0.149` field, `0.034` above; at 0.5, `0.018`
   above; the recipe's own passage, `0.012`. It gets close; at 0.9 it doesn't arrive.
5. **A small attribution.** "A GIF rebuilt from the log takes 36 to 49 s -- the painter
   measured 35": my 35 s was the thirteen passes replayed through `easel run`, not a GIF.
   The numbers agree anyway.
6. **And one the bench got right against me**: a glaze does go into a plan, as a stroke
   entry with `glaze: True`. My verdict's "as far as I could tell" was wrong there, and
   should be corrected wherever it is quoted.
