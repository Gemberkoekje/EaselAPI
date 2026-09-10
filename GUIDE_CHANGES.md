# Guide changes wanted after REHEARSAL6

**Read this file, then `PAINTER.md` and `CALIBRATION.md`. You do not need to read the
rehearsal write-ups** — everything from them is quoted here.

Six fresh sessions painted against the guide in REHEARSAL6 and the name-then-paint
experiment beside it: the mug, the sitter, two unprompted paintings, and four sessions
that named a subject before reading anything and then painted it. Every item below was
found by one of them, and every factual claim was reproduced against the engine
afterwards rather than taken from a painter's word.

**These are hypotheses.** `NOTES.md`'s standing rule is that a guide change is not a fix
until a fresh session paints against it. Make them, then run the definition of done
again.

> **Status: items 1–12 are applied**, together with the engine fix in item 6. The guide
> grew by 219 lines and gave 16 back; `check_guide_blocks.py` runs 43 blocks with none
> failing; `pytest -q` is 280 passed, 3 skipped, with one test added for the signature
> allowance; and the reference grep is clean on both photographs — **including three
> leaks these very edits introduced and had to have taken back out.** Two of the new
> examples named the sitter photograph (*a portrait in a crowded room*, *the face*, *a
> near-black eye*) and a third used *horizon* for the structure the whole investigation
> is about. That is the leak rule catching its own author, four runs after it was
> written, and it is the best argument in the repo for keeping the grep a precondition
> rather than a habit.
>
> **Items 13–17 are not applied.** They change the brief, and that is the owner's call.

## Ground rules for this work

- **`python rehearsal/check_guide_blocks.py` must stay green.** Every python block in
  `PAINTER.md` runs. If you add a block, it runs.
- **`pytest -q` must stay green** — 279 passed, 3 skipped, about 100 s. Nothing here
  should touch `src/`, with the single exception noted in item 6.
- **Nothing in a reference goes into the guide.** The brief voids the pass criterion if
  the guide names anything in the mug or sitter photographs. Grep before you finish, and
  then read your own examples and try to name the subject. Two borderline items are
  already on the record in `rehearsal6/PREREGISTERED.md` and are item 17 below.
- **Length is a cost.** The guide is ~1,300 lines and every painter read all of it. Four
  of the items below add procedure; pay for them by cutting warnings that repeat.

---

# The five lessons

## 1. Warning is not method — this is the big one

Four of six painters, independently, said the guide tells them a state is bad without
telling them what to do instead. N4 put it in three words:

> The biggest omission is that there is no *procedure* for repairing a mass with things
> standing on it — only a warning, repeated four times, which I ignored four times.
> **Warning is not method.**

And the pass painter, on the same class of gap:

> **There is no advice on how to bury something**, and it is the thing I needed most.
> "When something is wrong, paint over it" — with what? A `bristle` at `opacity=0.9`
> does not bury (the comb leaves the old paint showing between streaks). A `flat` buries
> and leaves a rectangle with chisel ends. A `round_hard` buries and leaves a capsule.

The guide states *"before you repaint a mass, look at what is standing on it"* in three
places — `PAINTER.md:107`, the paragraph at `425–434`, and the checklist at `1250` —
one of which is a full paragraph, and the painter counted four. It is a good rule and it
is repeated because it keeps failing, and it keeps failing because knowing it does not
tell you what to do. **Replace repetition with procedure.** Items 1–4.

## 2. Every tool has a geometry of its own, and the guide documents exactly one

N1's account of its own picture, which generalises all four name-then-paint sessions:

> I generated form with code instead of judging marks, so wherever a tool had a geometry
> of its own — sweep's rings, `block_in`'s cut passes, an even loop over angles —
> **that geometry became the subject, and the picture drifted toward the shape of the
> method.**

The guide has **one** entry of this kind — *"A short `flat` or `knife` stroke is a
rectangle"* — and painters cite it, by name, as one of the most useful lines in the
file. Every other tool needs the same line. Item 5.

## 3. The guide promises four things the engine does not do

Each cost a painter real strokes, and one cost a finished painting a mark. Items 6–9.

## 4. The guide's facts are often present but filed where nobody is standing

Two painters said this in almost the same words. N4: *"`load_falloff=0.0` is filed far
from the warning it fixes."* N2 spent three passes rediscovering the bristle size floor,
which **is** in the guide — one clause in *The brushes* — because it was working on a
shadow band and not reading the brush section. A fact filed under the tool is not found
by a painter working on a passage. Item 10.

## 5. Two closing rules pull against each other and the guide does not say which wins

The pass painter:

> "Spend the last third of your strokes on what is around the thing you measured" and
> "your last ten may not be value corrections" are both good; but every near mass I laid
> on top knocked a cell back out of tolerance, so my last third really was mostly
> corrections and I had to finish the correcting early and deliberately. **The guide
> does not say which rule wins, and it should.**

Item 11.

---

# The changes

## 1. Add: how to bury something

**Where:** `PAINTER.md`, under *When something is wrong, paint over it*, which currently
says to `dry()` and `block_in` and stops.

The answer a painter spent about fifteen strokes across three paintings arriving at, in
its own words:

> **a long stroke, solid tip, `load=1.0`, full opacity, run along the grain of what is
> already there so its own ends fall outside the area you are fixing.**

Every clause of that is load-bearing and none of it is currently anywhere: solid tip
because a bristle's comb leaves the old paint showing between streaks; `load=1.0`
because a low load leaves a speckled film; ends outside the repair because an oriented
tip's chisel end lands *inside* the picture otherwise, which is item 5's problem.

## 2. Add: how to repair a mass that has things standing on it

**Where:** the same section. The rule is already stated three times; state the method
once and cut one of the repetitions.

N4's method, which is the only one in six sessions that worked:

> keeping every mass *and* every near thing in a named function and re-running the whole
> stack in depth order.

That is a real procedure and it is what back-to-front actually costs at repair time.
The guide's own depth-order rule implies it and never says it.

## 3. Add: a budget arithmetic for a *picture*, not only for a mass

**Where:** `PAINTER.md`, near *When to stop measuring*.

The sitter painter spent **176 of 299 strokes before the subject existed** — the guide
warns about spending too much on detail and too little on structure, and this is the
opposite failure, on the run whose whole question was how far the tools reach on a face.
Its proposed rule:

> **decide what fraction of the budget the subject gets, before the first stroke, and
> spend the background out of what remains.** For this picture it should have been 180
> on the head and 120 on everything else. It was 124 and 176.

`extent/step` costs a mass. Nothing costs a picture.

## 4. Add: how to paint a gap

**Where:** near *The shape is a place, not a line*.

N2: *"Background dabbed into foliage reads as floating discs; a gap has to be a broken
sliver at the silhouette with a starved brush."* Two sentences, and it is the difference
between foliage and a pattern of discs.

## 5. Add: the shape each tool leaves behind

**Where:** `PAINTER.md`, *The brushes* and the shapes section, extending the pattern of
*"a short `flat` or `knife` stroke is a rectangle"* to everything else that has a
geometry. Measured or reported this run:

| Tool | The shape it leaves when you were not watching |
|---|---|
| `flat` / `knife`, short | a rectangle — **already in the guide, and painters cite it** |
| `round_hard`, short | a capsule. ~7× longer than wide before it stops reading as one |
| `bristle` below `size≈0.025` | a comb: a woven strap, or a ladder of evenly spaced ticks |
| `sweep` round a closed outline | concentric rings — *"it read as a cinnamon bun"* |
| several overlapping `blob`s | a dome. Similar blobs average to a circle; the irregularities cancel |
| a shallow shape filled along its long axis | its bounding box |
| any procedural generator | its own statistical signature, not clumps and holes |
| additive-only local repair | horizontal strata, one edge per repaint |

Two of those need their own sentence beyond the table:

- **The shallow-shape one is a rule the guide gets wrong.** N3's cup interior — an
  ellipse `0.256 × 0.128`, verified elliptical with `preview` — rendered as a rectangle
  twice with a `flat` at `0.022`, which is a **twelfth** of the mass's width and well
  inside CALIBRATION's "keep the brush under about a fifth" rule. **The dimension that
  matters is the extent perpendicular to the passes, not the mass's width.**
  `direction=90` fixed it instantly.
- **A mass much longer than it is wide is a stroke, not a mass.** `block_in` combed a
  `0.022 × 0.18` band even with `flat`, `pressure="even"`, `density=1.0` and
  `direction="axis"`. A long `stroke()` call is the right tool and the guide offers only
  "fill a shape" or "sweep an edge".

## 6. Fix: the signature exemption, which the engine does not honour

**This is the one item that wants a source change**, and it is `NOTES.md` item 00a.

`PAINTER.md:1265` promises *"Up to five marks, and they do not come out of your stroke
budget, so long as each one carries `note="signature"`."* `History.stroke_count`
(`src/easel/history.py:87`) counts every record whose kind is not `dry`, `look`,
`pencil` or `erase`, so a signature mark is charged. Reproduced: `stroke_count` goes
`1 → 2` on a mark noted `signature`. The exemption exists only in
`rehearsal4/verify_done.py`, which no painter sees.

Both REHEARSAL6 painters found it independently, and it cost one of them a painting:

> Two liner strokes with `note="signature"` took `s.stroke_count` from 299 to **301**
> [...] I had to undo, drop a real mark, and re-sign with one stroke instead of two.

The dropped mark was the mole on the sitter's neck — a real, specific feature of that
face. **Make `stroke_count` honour the exemption**, capped at five, with everything past
five charged so the cap cannot be spent on painting. Deleting the promise from the guide
is the other option and the worse one: a painter that pays for its signature will not
sign.

## 7. Fix: `inset()` by half the brush, on a shape that is not convex

**Where:** `PAINTER.md`'s *"Keep the brush under about a fifth of the mass's width, or
`inset()` the shape by half the brush size"*, and CALIBRATION's coverage figure.

Reproduced on the sitter painter's own 15-point coat outline: **`inset(0.052)` keeps
`62.7%` of the shape's area.** The block-in then covered 98.4% of the inset shape and
**76.2% of the actual coat**, with the near arm at `15.5%` — a whole lobe bare. The
painter did not find the hole until `compare()` showed it twenty strokes later and it
cost six to fill.

CALIBRATION's *"coverage at `density=1.0` is 99% of the shape"* is measured on a blob,
and a blob is convex. Say so, and say: **preview the inset shape, not just the shape.**

## 8. Fix: "a shaped mass costs what its box costs"

**Where:** `PAINTER.md`'s shapes section and CALIBRATION's costing table.

The guide says both *"the passes are counted across the mass, not over its area"* and
*"a shaped `block_in` costs about what its box would"*. For a curved ribbon those
disagree and the box wins. Reproduced: a ribbon **`0.029` wide** at brush `0.015` costs
**19 passes** curved and **3 straight**. The pass painter budgeted 4 and paid 21 — 7% of
its stroke budget on one call, and it nearly ran out of strokes for the mug's handle.

**CALIBRATION should carry a ribbon in its table.** The guide should say the cost
follows the bounding box, which is the honest version of both sentences.

## 9. Fix: `smudge`, which is the highest-value change in this list

**Four of six painters call it the advice that cost them most.** The guide offers it as
the way to lose a join — *"walk each join once, while wet"* — and CALIBRATION calls
`0.035–0.045` the window in which it behaves.

Measured here, as the steepest value step across a join per 1% of canvas height:

| | join sharpness |
|---|---|
| the bare join, no smudge | `0.330` |
| smudge `0.035`, one pass | `0.214` |
| smudge `0.040`, one pass | `0.184` |
| **smudge `0.040`, three passes** | **`0.280`** |

**One pass helps and does not finish the job; a third pass undoes most of the first.**
The guide says *once* and is right to. But a tool that half-works and then punishes the
obvious response leaves a visible horizontal join in every wide soft passage — which is
what all four name-then-paint painters hit, and what six unprompted skies are made of.

Three things to write down, none of which is currently there:

- **What one pass actually buys**: a 40–45% reduction in the step, not a lost join.
- **What to do when once is not enough**, since doing it again is worse. The answer three
  painters arrived at independently: *many overlapping strokes at closely spaced values*,
  which the guide mentions only in passing as scumbling.
- **Smudge runs *along* a boundary, never across it.** The guide's own example runs
  across (`s.smudge([(0.3, 0.4), (0.45, 0.44)])` to soften an edge) and that is the usage
  that failed for three separate painters, with a *"visible pale thumbprint every time"*.

## 10. Fix: exercise 1's `at_value()`, which the guide hands out broken

**Where:** `PAINTER.md`, *Eight small exercises*, exercise 1.

The bisection searches the white ratio, so asking it for a value **below** the base
returns ratio `0.000` and hands back the base, silently. Reproduced: base `0.137`, asked
for `0.037`, got `0.137`. The sitter painter copied it, asked for `0.30` from a base at
`0.41`, and painted a field at `0.41` without noticing.

Either raise on a target below the base, or say in one clause that it only goes up.

## 11. Say which closing rule wins

**Where:** near *spend the last third of your strokes on what is around the thing you
measured*.

Lesson 5 above. The honest answer from the run: **finish the value work early and
deliberately, then spend the last third on the surroundings, and let the last ten be
about the picture.** The pass painter did exactly that and its last ten were the visor,
the rim light, the tag, the string, a stray hair and two deliberately lost edges. Say
so, rather than leaving a painter to discover the two rules collide.

## 12. A batch of small factual corrections

Each cost its painter time and each is one clause:

- **`sweep(cross=0)` raises.** Omitting `cross` works. The guide presents `cross=` as
  advice — *"Take it"* — and CALIBRATION tabulates an uncrossed sweep as a real option.
- **`undo(n)` counts log entries, not paid marks.** `undo(2)` over a stroke and a pencil
  line gives back one stroke. The guide calls undo "scraping the canvas" without saying
  what a unit is.
- **`look(region=)` pads the crop** to the panel's aspect ratio, so you are shown more
  than the span you asked for. Two rounds of a painter's pixel arithmetic died on this.
  The fix worth writing down: calibrate off the drawn `mark()` crosses, whose canvas
  coordinates you know.
- **`compare(region=...)`'s detail lines are `col,row`**, the transpose of the table
  printed above them.
- **`dab(press=2)` is a whisper.** CALIBRATION's numbers are white on three grounds; a
  near-black iris at `press=2` on a lit cheek did not register. Working rule: **`press=3`
  for anything you want to land.**
- **`preview(points)` draws the brush at some default width** and never says which, so a
  silhouette preview comes back as a wide band — fine for placement, useless for an edge.
- **Units on a non-square canvas**: `size` is a fraction of the long side while
  y-coordinates are normalised over the short side, so `block_in`'s overhang spills a
  different amount vertically than horizontally. CALIBRATION spells this out for
  `sweep`'s `depth` and not for `block_in`'s overhang.
- **A cool mass on a warm ground reads about two steps lighter than it measures.** A
  painter concluded three times that its mug was far too light and `compare()` said it
  was within `0.05` every time.
- **Nothing covers a scene with more than one subject.** The depth rule scales; the
  attention rule does not. The sitter photograph has five people at four depths.

---

# Changes to the brief, not the guide

These are the repo owner's call, not a guide editor's.

## 13. Adopt "chosen before the guide is read" for the unprompted stage

The name-then-paint experiment met both pre-registered clauses: **4 of 4 painted the
subject they had named before reading anything, and the median band dB was `+0.53`
against a baseline where all six first unprompted paintings sit between `+8.12` and
`+23.83`.** `rehearsal6/name_then_paint/RESULT.md` has it in full.

The clause *"the first is genuinely unprompted, no constraint of any kind"* would become
*"chosen before the guide is read"*. That is a different measurement and a better one:
it measures what the painter chooses rather than what the guide retrieves.

## 14. `probe_structure`'s band dB is partly measuring "has a sky"

It is the variance of the row means over the variance of the column means, so **it
cannot separate a smooth vertical gradient from a stack of slabs.** Measured: a
three-step gradient with its joins smudged scores `+32.3`; a field of overlapping
scumbles at close values scores `+38.2`. The brief uses this number as its pre-registered
measure of compositional structure. The edge shares beside it are the half that
discriminates, and the human looking is still the verdict. Say so where the brief names
the probe.

## 15. The value criterion is saturated

Worst cell on the last three mugs: `0.0985`, `0.0961`, `0.0987`, against a `0.10`
threshold. Three different painters have cleared it by a thousandth, and on all three
runs `probe_human_notes`'s containment caught a defect it could not see. `NOTES.md`
item 00c.

## 16. The depth-order paragraph has failed three runs

Containment `17.5%`, `16.3%`, `13.2%` against REHEARSAL3's `0.1%`. `NOTES.md` item 00b.
The reason for leaving it alone — one session is not evidence — has expired.

## 17. Does the leak rule need to reach lists of non-objects?

Recorded in `rehearsal6/PREREGISTERED.md` before that run, and neither fired cleanly:
`PAINTER.md:622` heads a list with *grain* while the mug's table is wood grain, and
`PAINTER.md:240` heads one with *a knuckle* while the sitter's foreground is a pair of
hands. Neither names a paintable object, so neither breaks the rule as written. The
hands came out worst in the picture, which answers the knuckle item **no**. The grain
item is unresolved and stays on the record.

---

# What is deliberately not in this list

- **The engine's real defects**, which belong in an engine-changes file: the concave
  `inset()` erosion itself (documented as correct in `ENGINE_CHANGES.md`; item 7 is
  about the *advice*), and the ribbon costing (item 8, same distinction).
- **Anything about what a painter should paint.** Six sessions produced six subjects and
  the guide should keep saying nothing about subject.
- **A rewrite of the depth-order paragraph.** It needs one (item 16) and writing it is a
  design job with a measurement attached, not an edit.

# When you are done

- `python rehearsal/check_guide_blocks.py`, `pytest -q`, and the reference grep.
- Then run the brief's definition of done again. **Every item above is a hypothesis
  until a fresh session paints against it**, and this run is the fourth in a row to
  demonstrate that writing a rule down is not the same as the rule working.
