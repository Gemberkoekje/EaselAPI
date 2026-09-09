# M6's final pass — three fresh sessions, and two notes from the human

**To understand this, start by reading `REHEARSAL2.md` (the run this one is measured
against), then this file, then `rehearsal3/HUMAN_NOTES.md` (the two notes and their
probes), then the diff to `PAINTER.md`, then `rehearsal3/*/LOG.md` (each fresh
session in its own words).**

The brief ends M6 with *"then run the M5 protocol again, fresh session, same
reference. That run is the measurement."* This is that run, three times over, on
references the human supplied:

| Run | Reference | Pencil | What it answers |
|---|---|---|---|
| `rehearsal3/pass/` | `Level1.jpg`, a mug on a table | its own | **The pass.** The brief has asked for "a mug on a table will do" since M1. |
| `rehearsal3/sitter/` | `Level3.jpg`, the sitter | its own | **Reach.** The same photograph `REHEARSAL2.md` painted, so the two are directly comparable. |
| `rehearsal3/assisted/` | `Level1.jpg` | `sketch(reference)` | The assisted mode the brief says to run and report separately. |

Each was a session that had read `PAINTER.md` and nothing else — no `src/`, no
`NOTES.md`, no `REVIEW.md`, no earlier rehearsal, no `painting-api-brief.md`, and no
docstrings or signatures out of the installed package. Each kept a running list of
every moment it wanted to look at the source. The engine's author read the notes and
did not paint.

Every number below was re-measured from the exported PNGs by
`rehearsal3/verify_pass.py`, `probe_value_floor.py` and `probe_axis_alignment.py`,
not taken from the painters' reports. Where the two disagree the script wins.

---

## The verdict first

**M6 is not done.** The copy stage passes on everything the brief asks except the
number, and it fails the number for two reasons — one the painter's and one the
tool's.

| Criterion | Result |
|---|---|
| The human recognises the object | **Pass.** With the photograph covered it is a pale ceramic mug on a wooden table, dark tea in it, a spoon standing out, handle right, cast shadow down-left, teabag tag on its string. |
| Under 300 strokes | **Pass.** 295. The pencil (16 lines) and every rehearsal are free, as intended. |
| Strokes rejected in `preview()` / `rehearse()` | **Pass.** Four, recorded with the look that caught each one. |
| No cell **on the object** more than `0.10` out | **Fail.** Seven of the thirteen mug cells. Two of those cannot be painted at all; **five are the painter's**, and every one of the five is too *light*. |
| Headline run without `sketch(reference)` | **Held.** Every pencil line in both paintings is the painter's own. |

**The sitter is the milestone's real result, and it is a large one.** M6 asked
whether a fresh session could get below the size of a grid cell and build a face.
It can. `rehearsal3/sitter_compared.png` puts REHEARSAL2's copy and this one beside
the photograph: where the older one has a dark bar, two grey dots and a red smear,
this one has an eye with a lid, an iris and a catchlight, a brow, a nose with its
shadow, an open mouth with a lit tooth, a beard that is a mass with direction, and
hair with strands in it. The smallest thing placed where it was meant to go was that
catchlight — `round_hard` at `size=0.003`, about 3.6 px, roughly a fortieth of a
cell. All ten landmarks landed first time.

It is still not *the* person. Beside the photograph you would pick it out of five;
with the photograph covered you would not name him. The ear defeated four attempts
and ended as hair. The tools run out at about `size=0.003`, and his eyelid line is
two pixels.

**The unprompted painting is where the human's first note lands hardest.** Given no
subject at all, this session painted an estuary at low tide — luminous sky, headland
dying away to the left, three mooring posts, ribbons of wet sand. REHEARSAL2's fresh
session, given no subject at all, painted a dawn estuary — layered sky, headland in
fog, a dark spit, posts, wet mud. Two independent sessions, no prompt, the same
picture. That is not taste — and it is not the model's own prior either: thirty-two
fresh sessions were asked afterwards to name a subject, and the ones given no guide
produced no estuaries at all. See *How unprompted is unprompted?*

**The assisted run is a wash and slightly worse.** 299 strokes for a blockier, less
convincing mug, one more cell out on the object. See *What the machine sketch
bought*.

---

## The human's two notes

Both arrived from the repo's owner looking at the paintings, both turned out to be
sharper than style preferences, and both are written up with their probes in
`rehearsal3/HUMAN_NOTES.md`. Summarised here because they account for more of what
is wrong with these pictures than anything the three sessions reported.

### 1. Everything is horizontal or vertical

> I see a lot of very horizontal or vertical strokes, which really show the edges of
> those square strokes. Part of the challenge of painting is to either use circular
> strokes … or to rotate the knife or whatever you're using to get e.g. the sides of
> mountains.

Measured as the share of strong edges running within ten degrees of an axis
(`probe_axis_alignment.py`), higher being squarer:

| Picture | Axis-aligned edges |
|---|---|
| `Level1.jpg` / `Level2.jpg` / `Level3.jpg`, the references | 22.8 % / 25.6 % / 31.3 % |
| REHEARSAL1 copy / own | 27.9 % / 31.9 % |
| REHEARSAL2 copy / own | 36.5 % / **47.2 %** |
| REHEARSAL3 mug / sitter / assisted | 27.6 % / 35.6 % / 30.6 % |
| REHEARSAL3 unprompted | **42.9 %** |

Every copy comes out squarer than the photograph it was copied from, and both
unprompted paintings come out squarer than anything else in the set — a subject with
almost no straight line in it, rendered as horizontal bands and vertical bars.

Three causes, and they are not equally important:

- **The stroke path, which is most of it.** `block_in` offered four directions,
  three of them axis-aligned and one pinned at 45°. On the same hillside
  (`probe_axis_mountain.png`): laid with horizontal passes, 34.8 % and 37 strokes;
  swept along its own slope, **20.3 % and 17 strokes**. Running the strokes along
  the form is both truer and cheaper.
- **The guide's own worked example taught the artefact.** *A region is a rectangle*
  gave an `edge()` walk that lays a vertical column at every step across the mass.
  That is the recipe REHEARSAL2 used for the coat. It is the worst-scoring panel in
  the probe.
- **The tip angle, which was already implemented and entirely undocumented.**
  `angle_follow=False, angle=45` turns any oriented tip; the knife lays a clean
  parallelogram, and at 90° it is edge-on and draws a ribbon. `PAINTER.md` listed
  `size`, `opacity`, `hardness`, `jitter`, `load` and `load_falloff` as the things a
  stroke can override, and stopped. On a long sweep pinning is worth about two
  points on top of fixing the path — it earns its keep on ends and short marks.

### 2. Paint from back to front

> Another thing the painter.md should be more clear about: Paint from back to front.

**The guide never said it.** It ordered the work by size and by value; depth was not
an axis it had. The closest it came was a parenthesis inside the `block_in` overhang
warning — advice about *size*, offered as a way round a documented overspill, three
hundred lines below the workflow.

It is the same lesson as the first note. The guide already knew what it wanted:
*"the edge is then where two masses meet, which is the only kind of edge a painting
has"*. Back to front is the order that makes that free. Lay the far mass first and
the near one's silhouette happens the moment you paint over it; lay them the other
way round and the only way to the same edge is to paint *up to* a line, which the
guide spends a whole section forbidding without ever naming the order that prevents
it.

All three runs paid for it and none of them named it:

- **assisted**: "a background `block_in` buries the **whole** underdrawing,
  foreground included." Two entire recovery passes (`c12_lines.py`, `c13_redraw.py`)
  exist only because the mug was drawn before the table behind it was painted. They
  filed it as an engine complaint. It is the missing rule.
- **sitter**: the coat "is visibly striped by eleven repair bands" — the background
  negotiated with after the fact.
- **pass**: "a stray tan wedge in the handle's hole", "two pale slabs in the
  lower-right table".

---

## How unprompted is unprompted?

Two fresh sessions painting the same estuary unprompted is worth stopping on. The
human asked the obvious adversarial question — happenstance, or is something nudging
them? — and the answer is in `rehearsal3/unprompted/`: thirty-two fresh sessions
asked only to *name* a subject, across four conditions, with the buckets and the
thresholds fixed in `PREREGISTERED.md` before any of them ran.

> **This section previously claimed that "a painter reading that and asked to paint
> anything at all will paint a horizontal landscape, because that is the only kind
> of picture the vocabulary describes." That claim was tested and is wrong.** Six of
> the eight sessions given the real guide named a street or an interior. It is left
> recorded here rather than quietly deleted, because it was asserted in this file on
> the strength of two paintings and a reading, and the correction is the more useful
> artefact.

| Condition | built/urban | still life | other landscape | **water-with-horizon** |
|---|---|---|---|---|
| **A** no guide at all | 5 | 3 | 0 | **0 of 8** |
| **B** the guide as read | 5 | 1 | 0 | **2 of 8** |
| **C** the guide, five landscape clauses neutralised | 7 | 1 | 0 | **0 of 8** |
| **D** the guide, plus what a long copy teaches | 5 | 0 | 1 | **2 of 8** |

**What survives:**

- **It is not the model's prior.** Condition A produced no estuaries at all. The
  comfortable explanation is ruled out.
- **It is not happenstance in the ordinary sense either.** All four estuaries in
  thirty-two samples appeared in the two conditions carrying the guide's landscape
  words; none in the sixteen samples without them. Post-hoc pooling, and Fisher
  exact gives p ≈ 0.10 — suggestive, clean in direction, and not proven. About
  thirty words in a 981-line file are the only thing separating four from zero.
- **The real prior is a wet street.** Twenty of thirty-two — 63%, in every condition
  alike — named a rain-wet street or road at dusk with a light smeared across the
  wet ground, several in near-identical words. So the unprompted stage is *not*
  measuring an unprompted choice; it just is not the estuary doing the constraining.
- **And the thing that actually transfers is the band, not the subject.** Condition
  D adds only mechanical facts — the bristle comb, `block_in` filling a rectangle,
  the value floor — and no landscape word anywhere. **Six of its eight sessions
  justify their choice explicitly by horizontal bands or axis-aligned rectangles**,
  against roughly two vaguely in B and none in A: *"the whole subject is bands and
  horizontals — so the rectangular regions are working for me instead of against
  me"*. The noun varies; the composition converges.

That last point is the one that matters, and it is post-hoc, so it is a hypothesis
that earned a test rather than a result. A wet street chosen because "the road and
sky are two big quiet horizontal masses" is the same painting as an estuary chosen
for the same reason — which is the human's first note arrived at from the other end,
and it is what `probe_axis_alignment.py` has been measuring all along.

The vocabulary is still all rectangles, and that is still worth fixing — but on the
evidence it shapes *how* a picture is built, not *what* gets picked. Recorded in
*Still open*.

---

## What the copy stage actually got wrong

Worth its own section, because the failure is a single mistake made thirteen times.

`verify_pass.py`, on the thirteen cells the mug covers:

```
more than 0.10 out       7
  of those, unreachable  2   (reference below the 0.235 floor)
  of those, the painter's 5
worst on the object      D4 ref 0.14 canvas 0.34 +0.20
    D4 +0.20   D3 +0.18   D6 +0.18~  D5 +0.17~   E2 +0.16   D2 +0.12   E5 +0.12
```

**Every single one is positive.** The canvas is too light everywhere it is wrong,
and the errors run straight down the D column — the mug's shadow side and the dark
figure on it, top to bottom. The painter did not make seven mistakes; it made one
decision about how dark it was willing to go, and that decision was wrong in the
same direction thirteen times.

The cause is a collision between two things the guide and the tools each half-said:

- The palette floors at `0.235`. Confirmed from outside
  (`probe_value_floor.py`): darkest pigment `burnt_umber` at `0.235`, unmoved by
  eight dried passes (`0.231`), unmoved by four rounds of glazing (`0.234`), and
  `0.228` with all five darks mixed together. The ground makes no difference.
- `Level1.jpg` has cells down to `0.065`; `Level3.jpg` down to `0.043`, with
  **eighteen of its sixty-four cells** below what any stroke can reach.

The guide *did* say the range was "about `0.23` to `0.96`". But `compare()` went on
reporting those cells as out, with no way to tell them from real errors, and a
painter trusts the tool over the prose. Both fresh sessions worked this out for
themselves, mid-painting, and each reported spending about twenty-five strokes doing
it:

> **sitter**: "**17 of them are unreachable**: the palette floors at 0.23 and those
> cells' *reference* values are 0.04–0.12."
> **pass**: "Six of my final nine out-cells have reference means below 0.23 and are
> physically unreachable. I spent ~25 strokes finding that out."

Neither could check it, because checking it meant reading the palette, which they
were not allowed to do. And neither of them reached the conclusion the failure
actually points at, which the guide never mentioned: **do not match a photograph's
values, compress them.** Map the reference's range onto the palette's instead of
chasing a floor you cannot reach. That is now in the guide, with the arithmetic.

---

## What the machine sketch bought

The brief asks for the assisted run to be reported separately, and it is worth the
separate report: **it is not better.**

**The `prepare()` table did not name the things a painter would name.** Of seven
areas, four — 63 % of the picture — are all *the table*, split by its lighting
gradient. **No area is "the mug".** Its lit side is inside area 4 together with the
lit table; its shaded side is inside area 6 together with the cast shadow. Area 7
fuses tea, figure and shadow core. The spoon and the teabag are in no area at all.
The one genuinely useful column was **edges**: `4:7 = 1.00` and `2:4 = 0.89`
correctly ranked the two hardest edges in the picture.

**Kept** from the sketch: the rim ellipse (accurate to about `0.005`), the handle
loop, and the figure's outline — a silhouette that would otherwise have been
measured point by point. **Erased**: all four wood-grain contours, 770 points, most
of the drawing by length. **Drawn by hand anyway**: the spoon (missed entirely), the
mug's base — which dissolves exactly where mug meets shadow, the one line a painter
most needs — the tea's edge, and the tag. **Wrong**: the mug's left silhouette
drifts about `0.018` left below `y≈0.4`, where the shaded edge matches the table.

It saved no strokes, because drawing is free either way. It saved perhaps three fine
crops and cost three looks plus two entire recovery passes after the background
buried it — a cost that belongs to the missing back-to-front rule, not to
`prepare()`. The painting came out one cell worse on the object and visibly blockier
than the unassisted one.

The assisted run's own summary of what would have helped more is the right one, and
it is not about sketching at all:

> The thing it did *not* buy is the one that decided the painting: `compare()` on
> the **bare ground** reported D5 at 0.06 against my 0.54 — the reference's middle
> is far darker than it looks.

---

## What the guide got right

- **The grid on both panels, read out loud by cell before painting.** Third
  rehearsal running, still the single most consequential instruction in the file.
- **Landmarks.** Ten on the head, all correct first time, and the sitter run says
  plainly that the drawing is what made a face possible.
- **`preview()` and `rehearse()` before spending.** Every run produced its rejected
  marks without being able to point at the ones it would have painted otherwise.
  The sitter run tried the eye three ways on the scrap and painted the third.
- **Matching enlarged crops with `grid="fine"`.** The pupil came out of a look as
  `point(0.65, 0.46)` and went in at that.
- **The 0.10 rule as a *description*** — two masses closer than that read as one —
  was right every time it was used to judge two masses. It only misled as a
  *target*.

---

## What the rehearsal cost, in order of when it bit

The three logs record 12, 13 and 22 numbered items respectively — overlapping
heavily, and not all of them guide gaps. Consolidated here into the seventeen that
are; the per-run lists are in `rehearsal3/*/LOG.md`.

| # | What happened | Fixed in |
|---|---|---|
| 1 | Every mass came out of a horizontal or vertical sweep, so every mass had the canvas's edges; the guide's own silhouette recipe lays vertical columns | `PAINTER.md`, *The angle of the mark* + the recipe rewritten; engine — `block_in(direction=degrees)` |
| 2 | Nothing said to paint back to front; three runs paid for it in buried drawings and repair bands | `PAINTER.md`, workflow step 2 |
| 3 | `compare()` demanded values no paint can reach; two runs spent ~25 strokes each discovering the floor | engine — `Comparison.unreachable` / `.fixable`, `~` in the table; `PAINTER.md` |
| 4 | Nobody thought to compress the reference's range onto the palette's; the whole copy came out uniformly too light | `PAINTER.md`, with the arithmetic |
| 5 | `compare()` on the **empty canvas** is the reference's entire value map, free, and was never suggested; one run had the photograph "two stops too light" by eye | `PAINTER.md` |
| 6 | `erase()` cleared the graphite and left the line in `sketch_lines()`, so re-laying a drawing resurrected what had been rubbed out | engine — **defect**, REVIEW 20 |
| 7 | "It survives under a scumble" read as `density`, which is not thin paint; a seven-stroke `density=0.3` scumble took the drawing off completely | `PAINTER.md`, with the opacity numbers |
| 8 | `block_in`'s overhang paragraph offered a size-based workaround for what is a depth-order problem | `PAINTER.md`, points at the rule now |
| 9 | No documented `save()`; all three inferred persistence from the CLI section | open — see *Still open* |
| 10 | `s.log()` returns a string and `compare()` returns a `Comparison`; both were indexed as if they were lists | open |
| 11 | `out/` is per-session and a throwaway `Session` overwrites it; one run lost six cited looks | open |
| 12 | The guide never says which calls are billed as strokes (`smudge`, `dab`, `glaze` all are) | open |
| 13 | `prepare()` numbers areas; `look_areas()` draws no numbers, and `prep.region(n)` is a bounding box that spanned the whole canvas for four of seven areas | open |
| 14 | `grid=True` on a `region=` crop re-labels the crop locally rather than with the canvas's own cell names | open |
| 15 | Positions read off a multi-cell `span` crop are wrong by about `0.03`; only single-cell fine crops place points | open |
| 16 | `block_in` overhang is asymmetric per axis — `size` is a fraction of the **long** side, so the bottom spill is twice the guide's figure | open |
| 17 | `rehearse()` inherits canvas wetness and a plan cannot express a `dry()`, so it mispredicted three times | open |

Items 9–17 are recorded and not fixed. They are real, none of them decided a
painting, and the ones worth engine changes are listed in *Still open* rather than
being made in the middle of a measurement.

---

## Measurements

All through the public API and exported PNGs. Scripts in `rehearsal3/`.

- **The palette floor** (`probe_value_floor.py`): darkest pigment `burnt_umber`
  `0.235` on canvas, `0.2305` from `palette.value_of`. Two dried passes `0.231`;
  eight, `0.231`. Four rounds of three glazes each, `0.234`. All five darks mixed,
  `0.228`. Identical on every ground. `Level1.jpg` puts 2 of 64 cells out of reach,
  `Level3.jpg` 18 of 64, `Level2.jpg` none.
- **Axis alignment** (`probe_axis_alignment.py`): the table above. The metric
  under-reads a flat fill — a `block_in` box scores a misleadingly low 24.7 %
  because a flat mass has few strong edges at all. It measures stroke character, and
  for that it agrees with the eye every time it was checked against one.
- **The hillside, four ways** (`probe_stroke_axis.py`): box 24.7 % / 21 strokes;
  the guide's columns 34.8 % / 37; along the slope 20.3 % / 17; along the slope with
  the tip pinned 22.4 % / 17.
- **The tip angle** (`probe_axis_tips.png`): works on `flat`, `knife` and `bristle`
  through per-stroke overrides. Default `angle_follow=True` holds the blade square
  to travel, which is why every chisel end in every painting here is square to the
  canvas.
- **The pass criterion** (`verify_pass.py`): the table in *What the copy stage
  actually got wrong*. The assisted run: 8 of 13 out, 2 unreachable.
- **Stroke counts**, read back out of the saved sessions rather than the logs:
  copy 295, unprompted 120, sitter 299, assisted 299. The pencil is uncounted in all
  four (16, 16, 22 and 24 lines), as the brief requires.

---

## What changed outside `rehearsal3/`

**Engine — three changes, all additive. Every existing painting replays unchanged
and no golden image moved.**

- `src/easel/session.py` — `block_in(direction=)` now takes **a number of degrees**,
  or a sequence for one pass each, alongside the four names. The four named branches
  are untouched, so `"cross"` is still exactly a horizontal pass then a vertical one;
  there is a test asserting that.
- `src/easel/session.py` — `sketch_lines()` is derived from the log rather than
  filtered out of it, so `erase()` removes what it erased, cutting a crossing line at
  the region's edge and leaving the pieces outside. Right through undo and replay for
  free, because it is derived. **REVIEW 20.**
- `src/easel/measure.py`, `src/easel/palette.py` — `Palette.darkest_value`, and
  `Comparison.unreachable` / `.fixable`. Cells asking for a value below the palette's
  floor print as `~` instead of `*` and are counted separately: *"17 of those (~) ask
  for a value below the palette's 0.23 floor and cannot be painted. 43 are worth
  strokes."*

**`PAINTER.md` — eight edits.**

- A new workflow step 2, *Paint from back to front* (steps renumbered to 6).
- A new *The angle of the mark* section under the brushes: don't let the canvas
  choose the direction, `block_in` at degrees, the tip angle, and one plain line that
  a round tip is the tip that declares no axis.
- The `edge()` silhouette recipe rewritten to run passes *along* the form. Nine
  strokes instead of thirty, and it renders a headland instead of a fence
  (`rehearsal3/_guide_edge.png`).
- Value compression, with the arithmetic, under the value step.
- `compare()` on the empty canvas, and `fixable` versus `~`.
- The scumble paragraph now says `opacity`, not `density`, with the burial numbers.
- The overhang paragraph points at the depth rule instead of offering a workaround.
- Three more checklist lines: `fixable`, the axis question, and the depth question.

**`tests/test_precision.py`** — six tests (149 total).

---

## Gotchas for the next session

1. **A criterion can be unmeetable and the picture still wrong.** Five of the seven
   failing cells here were the painter's, and the two that were not gave it
   somewhere to file the other five. Split reachable from unreachable *before*
   concluding anything about a run.
2. **Ask what the tool offers before believing a choice was made.** Two unprompted
   sessions painted the same estuary. Neither chose it.
3. **An undocumented capability is an absent one.** The tip angle has worked since
   M2 and no painter has ever used it.
4. **The guide's worked examples are instructions, whatever the prose says.** The
   column recipe was followed exactly and produced exactly what it describes.
5. **Fix nothing while a measurement is running.** These three sessions painted
   against one engine; every change here landed after the last of them exported.

---

## Still open

- **The vocabulary is all rectangles.** Twenty-two named regions, every one
  axis-aligned; one helper named after a thing in the world, and it is `horizon()`.
  On the evidence in `rehearsal3/unprompted/` this shapes how a picture is *built*
  rather than what gets picked — a painter told what this engine is bad at chooses
  band-structured compositions six times in eight and says so. A non-rectangular
  place to name is the largest open item here.
- **The unprompted stage measures less than the brief thinks it does — a decision
  for the human.** The definition of done asks for "a second painting with no
  prompt", and the point of it is that the strokes are chosen rather than traced.
  That purpose is served. But 63% of thirty-two fresh sessions named the same
  subject before opening the guide, so *what* the painter picks carries almost no
  information about the painter, the guide or the engine, and this write-up spent a
  section reading meaning into two samples of it. Three options, and the choice
  belongs to whoever owns the brief:
  1. **Keep it and stop interpreting the subject.** Cheapest. The painting is still
     evidence that the engine can make a picture without a photograph; nothing more
     should be claimed from the choice.
  2. **Have the human name the subject**, with no reference image. That measures
     invention — can it paint a thing it cannot look at? — without measuring the
     model's prior, and it is closer to what the stage was for.
  3. **Ask for two unprompted paintings and require them to be different subjects.**
     Turns the prior from a confound into something the run has to work against.
  Option 2 is the recommendation: same cost, and it answers a question the current
  stage cannot.
- **A pre-registered test of the composition effect.** The 6-of-8 result above is
  post-hoc: it was noticed in condition D's stated reasons, not predicted. It wants
  its own experiment, classified on composition rather than subject, before anything
  is built on it.
- **`block_in` still fills a box** even when swept at an angle — the marks are
  angled, the region is not. A polygon block-in (`ref_outline(n)` already returns
  one) is the obvious next step and is partly the traced-copy question the brief
  reserves for the human.
- **Marks below `size≈0.003`.** An eyelid is two pixels at this canvas size, and the
  sitter run could not paint one. M7's pressure-follows-width change is the thing
  that would help most.
- **`rehearse()` inherits wetness and a plan cannot express `dry()`**, so it
  mispredicts on wet canvas. It is the one M6 tool that lied.
- Items 9–17 of the cost table.
- **M6 needs one more run.** Everything the copy stage failed on now has a fix in the
  guide, and a guide fix is a hypothesis until a fresh session paints against it —
  which is exactly what `REHEARSAL.md` → `REHEARSAL2.md` established. The next run
  should use the mug again, and the question is narrow: does the value error go away?

---

## File map

```
rehearsal3/
  HUMAN_NOTES.md            the two notes from the human, verbatim, and their probes
  pass/                     THE HEADLINE RUN — mug, own pencil
    LOG.md                  the fresh session in its own words
    c1_*.py … c*_*.py       one script per pass
    copy_final.png          295 strokes
    own_final.png           120 strokes, unprompted
    copy_timelapse.gif  own_timelapse.gif
    probe_pencil.py  c9_probe2.py   its two reproducers
  sitter/                   the same photograph REHEARSAL2 painted
    LOG.md  c*_*.py  copy_final.png (299)  copy_timelapse.gif  defect_demo.py
  assisted/                 the machine-laid sketch, reported separately
    LOG.md  GOTCHAS.md  c*_*.py  copy_final.png (299)  copy_timelapse.gif
    t1_coverage.py  t2_erase_sketchlines.py   (t2 is REVIEW 20)
  probe_stroke_axis.py      the tip-angle sheet and the hillside four ways
  probe_axis_alignment.py   the axis-alignment number, on every painting in the repo
  probe_value_floor.py      how dark the palette actually goes
  verify_pass.py            the M6 pass criterion, checked from the PNGs
  make_sheets.py            the two comparison sheets
  sitter_compared.png       reference | REHEARSAL2's copy | this one
  mug_compared.png          reference | own pencil | machine sketch
  probe_axis_tips.png  probe_axis_mountain.png
```
