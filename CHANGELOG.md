# Changelog

Every release of [`easel-paint`](https://pypi.org/project/easel-paint/), what changed in
it, and why. PyPI links this file from the project sidebar (the `Changelog` entry under
`[project.urls]` in `pyproject.toml`), so this is the page a painter lands on from the
package page.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project uses [semantic versioning](https://semver.org/spec/v2.0.0.html). Before 1.0.0 a
minor bump is where behaviour is allowed to move: **a version already saved to an
`.easel` file always replays as it was painted**, because every stroke's own brush
arguments are in the log, but a *script* that leaves a default off can paint something
different after a minor release. Each entry below says which defaults moved.

The engine's own record of *why* a rule is a rule lives elsewhere and is not duplicated
here: measurements in [`CALIBRATION.md`](CALIBRATION.md), the requests painters made and
what was done about them in [`SUGGESTIONS.md`](SUGGESTIONS.md), and the method in
[`LESSONS.md`](LESSONS.md).

## [Unreleased]

The documentation was restructured, and no engine behaviour or default moved.

- **One home per rule.** Every rule in `PAINTER.md`, `PAINTING.md`, `RECIPES.md`,
  `REFERENCE.md` and `CALIBRATION.md` is now stated once, in the file it belongs to,
  and linked from the others. The same six rules had been stated in four to six places
  each. `scripts/check_guide_overlap.py` reports any sentence that appears in more than
  one of the five.
- **`PAINTER.md` is a card and a body.** *The first hour* is the loop, the order, the
  five mistakes with their fix on the same row, and a pointer to the checklist, in
  under a thousand words; the body states each step once with its number and links to
  the situation and the measurement. The anecdotes that carried the rules — which
  painter did what, and how many strokes it cost — moved to `CALIBRATION.md` under
  *From the sessions*, where a painter's own count is labelled as such. The drawing is
  step 1 of the order, in its own right. 9,973 words to 6,441.
- **`RECIPES.md` is the situations file.** Same entries, each trimmed to the calls,
  the failure and the number, plus one new entry, *A scene with straight edges*: the
  projection helper three painters had each built for themselves, and the one thing the
  guide had nothing on.
- **`PAINTING.md` is the engine's behaviour**, with the reference-photograph material
  gathered into a last chapter a painter without a photograph can skip, and the MCP
  section moved to `REFERENCE.md` with the rest of the facts. 11,500 words to 6,900.
- **`CALIBRATION.md`** gained an index at the top mapping each rule the guide states to
  the section that measured it, and the *From the sessions* section. No measurement
  changed.
- `DIAGNOSIS.md` gained a row for the new recipe and follows one pointer to the rule's
  new home.

## [0.4.0] — 2026-09-14

The ninth session's round: a heron in a flooded lot at dawn, painted twice. The first
is the restricted arm again with `DIAGNOSIS.md` added — the only data point that
exists on whether the symptom index works — and the second is the same painter and
the same subject with the withheld files in hand. Fourteen items between them, and
the two paintings together separate the two kinds of fault cleanly: **every fault
that was a lookup got fixed by reading, and the one that was judgement repeated
itself exactly, with the recipe open.**

**Two of its claims did not survive being re-measured, and one of those was the
*eighth* session's guess, which this session was measuring.** A sequence of
directions is priced as the sum of its angles, nine measurements for nine, and
`direction=[0, 90]` logs the `0°` stack whole and then the `90°` stack whole. The
other is this round's own: *a warning when an oriented tip is handed a `size` under
about `0.008`* came with a measured table behind it and still had the wrong unit —
the cliff is at four **pixels**, which is a different `size` on every canvas.

And a second rule has left the front page, for the same reason as the first: the
`PAINTER.md` word budget left three of this round's items nowhere else to come from.
*You will use too many strokes on detail and too few on structure* is in
`PAINTING.md` beside *you will under-vary your marks*, and the post-pass check says
both after the pass that did them.

### Added

- **A seventh rule of the post-pass check: a graded passage laid too narrow.** Three
  or more long parallel marks at three or more colours, stepped further apart than
  half the narrowest brush laying them — `scumble`'s own `2 ×` wall, applied to a
  stack laid by hand, which is the form `RECIPES.md` teaches and the form that gets
  no protection. Measured on one painting against itself: its sky, laid with the verb,
  sits at 4.0 steps and wobbles `0.037`; its hand-laid dawn band tapers to **1.7**
  steps and wobbles `0.072`. The conditions are narrow on purpose — a mass is one
  colour however its passes are spaced, which keeps every `block_in` out of it, and
  marks more than four brushes apart are separate marks. The first rule to arrive from
  a session asking for a check rule by name.
- **An oriented tip under four pixels says it will lay nothing.** Not an aesthetic
  rule: a `flat`, `bristle` or `knife` that small does not make a poor mark, it makes
  **no mark**, and is charged for it. One stroke deposits *zero* paint at 1–2px
  against a `round_hard`'s 44–51 pixels' worth, and a solid mass laid at 2.7px comes
  back the value of the ground under it. It fires once per call from every verb a
  `size=` reaches, and from `cost()` before a stroke is spent.
- *A graded field that is most of the picture* in `RECIPES.md` — a sky, a far field, a
  sheet of water at a grazing angle, which none of the other light recipes is. Four
  ingredients collected from three paintings, with the one measurement the request did
  not have: `load=1.0, load_falloff=0.0` is not the verb's default on a band, and
  without it `0.9%` of an eleven-pass field comes back within a hair of bare ground.
- *Without a reference* under `The drawing` in `PAINTING.md`: the precision loop with
  the points checked against **each other**, and the parallel-pencil loop written out.
  Eight of the nine painters before this one never drew a line.

### Changed

- **The check's bristle floor now skips a comb that was starved on purpose.** *A
  bristle under `size=0.025`* fired twenty-eight times in one painting and was
  correctly ignored twenty-eight times: its subject is broken glints on water, grit
  under a flood and feather groups on a bird, where the comb's gaps **are** the mark.
  It now needs a `load` over `0.6`, the top of the run-out window `CALIBRATION.md`
  already publishes. Checked against both of that session's paintings: every
  small-bristle call site in them names an explicit `load` and **not one** uses the
  preset's `0.9`, so the rule was firing on nothing it was written for.
- **`REFERENCE.md`'s `direction` row said the opposite of what a sequence does.** *Or
  a sequence for one pass each* reads as *n passes for n angles* and means *n complete
  stacks*; it now says so, with the pass counts and the 515-stroke quote a sixteen-angle
  list drew. The price walk itself landed in 0.3.0 and fires on all nine of this
  session's cases; one fix of its own, the suggested cross on a mass whose axis is `90`
  was being written as `("axis", 180)` rather than `("axis", 0)`.
- **`solid`'s row and `sample`'s entry both said less than they should.** `solid=True`
  is "what fills a mass" and does not fill it to its colour — a mass lands *between its
  mixture and what it was laid over*, measured in both directions. And `sample`
  averages the place it is given, so a cell hands back the mass averaged with
  everything around it: a bird planned at `0.30` in water at `0.50` reads `0.501` by
  its cell and `0.327` by its own shape. A painter read two masses that way and
  concluded the engine lays everything `0.14` light.
- `PAINTER.md`: the pairs question in step 3 now says the threshold is about two masses
  that **meet**; step 2 names *a veil of light is a mass at a depth* and `look(diff=True)`
  beside it; and the pencil is no longer sold on being free, which a rehearsal also is.
- `CALIBRATION.md` gains *What a solid mass actually lands at*, and the across-band
  ripple table gains the clause a painter spent a measurement discovering it needed.
- `PAINTINGS.md` records what the numbered-pass convention does to the drawing: seven
  of the ten paintings here drew no line at all and nine placed no landmark.

### Measured, and not changed

- **A sequence of directions is not priced at its steepest angle**, which the eighth
  session guessed and the ninth measured: the cost is the exact sum of what each angle
  costs alone, nine for nine across three shapes, and in paint it is one whole stack
  per angle laid one after the other. The warning was already written from the
  mechanism rather than from the guess, so nothing had to move.
- **The across-band ripple metric does not read canvas texture.** A painter compared a
  hand-laid band against a `scumble` with it, got an answer the wrong way round, and
  put it down to flecking on a `rough` ground. Measured: identical on `smooth`, `linen`
  and `rough` to four decimals at every window width, and on a *starved* pass `rough`
  reads *lower*. What it is sensitive to is the window — `0.0008` across the full width
  against `0.0020` through a narrow column, for the same paint. One clause beside the
  table, and the table itself is unchanged.
- **`DIAGNOSIS.md` is not changed on n=1.** The one session that has had it read it
  front to back, recognised five rows on sight, and followed **zero** pointers in 293
  strokes. An index whose rows carried the repair as well as the pointer would be the
  fourth copy `LESSONS.md` refuses, so the proposal is a protocol question — hand it as
  a file to grep and record which arm was run — and that is where it is written.
- **Which of the three pencil diagnoses is right is left to a run.** All three are
  documentation fixes and all three are made, because each is correct on its own terms;
  picking between them needs a painter working from a guide that carries all three.

## [0.3.0] — 2026-09-14

The eighth session's round, and the first one the register has carried as *open*. That
session is the split test's other arm — a painter given only the method, the recipes
and the reference — and what it failed at was **lookup rather than judgement**: three
questions the engine could already answer and would not say out loud. So two of its
three engine items are instruments rather than mechanisms, and the third is a price
the walk already knew and never quoted.

Every number it took reproduced, to the stroke. **One mechanism it offered did not**,
and it had marked that one as a guess — a sequence of directions is not a stack sized
for its steepest angle, it is one whole pass per angle, charged as the sum. The entry
below says so, which is this project's habit and the second time it has changed what
was built.

And the first rule has left the front page. `PAINTER.md` is held to 10,000 words, the
two documentation items it needed did not fit, and the growth rule's own answer is
that **a rule the engine checks at the call can leave the guide**. *You will
under-vary your marks* is that rule: the post-pass check names it after every pass,
with the numbers, which the paragraph could not do. Whether a rule can safely leave
is now a question a session can answer, which is the point of moving it.

### Added

- **`glaze(points, color, to_value=0.42)`** — `at_value` for a film. A glaze's
  strength is its distance from what it lands on, so the usable window is a few
  hundredths of opacity wide and sits somewhere different over every passage; *mix the
  glaze close, then choose an opacity* leaves the second half as a search run by
  rehearsal, and one painting spent six of them on it. This runs the search: films on
  trial canvases until one delivers the value asked for, measured over **the film's own
  footprint**, then that one for real. It costs one stroke like any other glaze, the
  chosen opacity is in the log, and because the trials come off a copy of the stroke
  stream **the film that lands is byte for byte the film that would have landed had its
  opacity been typed out**. A target the film cannot reach raises, naming both ends of
  what it can, for the reason `at_value` raises.
- **The inward scumble warns from the narrow side too.** Its brush is `3 × depth / n`,
  so more rings on a shallow patch buy a *narrower* brush and not finer banding — and
  past `n = 120 × depth` that brush is under the `0.025` where a comb is four streaks
  with gaps. It had warned since the third session when the brush was too *wide* to lay
  a fall-off and said nothing at this end, where a painter met it at `n=12` on a patch
  `0.075` deep, read the post-pass check's bristle complaint as unrelated, and spent
  two more rehearsals. Where no `n` fits at all — under about `0.042` deep, where even
  five rings comb — it names *a volume of lit air* instead, because a glow that shallow
  is not a bloom on a surface.
- **The price walk covers a sequence of directions.** It fired on `direction` left off
  and not on a painter who chose one and chose ten. A list that costs over 2.5× its own
  dearest angle now says so from `cost` and from the call, with every angle's price in
  the line — and two angles can never be more than twice the dearer of them, so the
  cross-at-the-mass's-own-angle idiom every painting here uses stays silent.
- `shape.inside(xs, ys)` is in `REFERENCE.md` beside `contains`, and both are where
  small marks are laid into a larger mass in `RECIPES.md`. One painter hand-rolled
  edge-intersection arithmetic about fifteen times with `contains` listed in the file
  open beside them: a list of methods answers *what exists*, and is read once at the
  start rather than at the moment a mark is placed.

### Changed

- **`RECIPES.md` separates its two glow recipes at the moment of choosing.** *A passage
  light in the middle* and *a volume of lit air* are the right pair, and the sentence
  that told them apart sat inside the second one, where it is read by a painter who has
  already chosen correctly. The index now says *on a surface* against one and *in a
  medium* against the other, and the first entry says it outright. Four sessions have
  reached the glaze answer the hard way and one of them had the recipe open.
- **`PAINTER.md` step 3 sends the value plan through `compare({place: value})` on the
  empty canvas.** The pairs question lived in `PAINTING.md` and `REFERENCE.md` carried
  the signature without the reason; the arm without the essay never ran it. A painter
  who wrote a nine-value plan, checked the separations by hand and satisfied themselves
  still shipped a frame as light as its subject — which is exactly what the pairs table
  was built to ask.
- **`PAINTER.md` says a low-key picture wants a ground of its own.** *Start on a toned
  ground, not white* is right for a mid-key picture and silently wrong for a night one:
  the lowest preset is `umber_wash` at `0.425`, and a painter who took `cool_grey` at
  `0.53` then had to lay every dark mass `solid=True` to cover it. A ground takes any
  colour, so the mechanism was always there — `Session(ground="#5a5045")` reads `0.32`.
- **`PAINTING.md` has *You will under-vary your marks*, which was on the front page.**
  Moved, not cut, and moved because the post-pass check holds both halves of it at the
  pass with the numbers attached. It is the first rule to leave the guide under the
  growth rule that says one may.
- `CALIBRATION.md` gains the three tables this round measured: a direction sequence
  priced angle by angle, the inward scumble's `n` window, and a film aimed at a value.

### Measured, and not changed

- **A sequence of directions is not priced at the steepest angle in it.** That was the
  painter's own account of the 51 strokes their ten-angle list cost, and they offered it
  as a guess. Measured on their mass, same brush, same density: `"axis"` 4, a single
  `-17°` 7, `"cross"` 15, and a ten-angle sequence 85 — which is those ten angles'
  prices *added up*, `4 + 5 + 7 + 7 + 9 + 10 + 10 + 11 + 11 + 11`. The finding is real
  and the number reproduces; the mechanism is the sum, and the warning is written from
  the mechanism rather than from the guess.
- **`n ≤ 120 × depth` is exact, and "about `0.07`" is the wall for the recipe's eight
  rings rather than for every `n`.** At `0.0667` deep eight rings stop fitting; five —
  the fewest that read as a fall-off rather than as steps — stop fitting at `0.042`,
  and that is where the verb stops being the answer at all. The warning carries both.
- **The fifth documentation item asked for nothing and gets nothing.** *The worked
  examples may prime toward one kind of picture* was offered as an opinion, unmeasured,
  by a session that had itself chosen a low-light subject before opening anything. It is
  a data point for the hypothesis and cannot test it. The measurement is a brief written
  for a high-key or flatly-lit subject, before anyone reads `paintings/`, and that is a
  session's work rather than a release's.

## [0.2.0] — 2026-09-13

The fourth painting session's six engine requests, the guide split by function, the
third session's engine round, and the package finally carrying the guide it is useless
without. Two of the six requests **did not survive being re-measured**, and the entries
below say so where that is the case — checking a painter's numbers before building on
them is the rule in `LESSONS.md`, and it changed what was built twice here.

And, cut into the same release before it shipped, **the greenhouse round**: three
painters handed one subject left three request lists, deduplicated into eleven engine
items and eight documentation items, plus the post-pass check that had been the cheapest
open item on the register for two rounds. Every number the three painters took
reproduced; two of the mechanisms they proposed did not, and the entries say which.

### Added

- **The post-pass check.** `s.report(since=)` reads the guide's standing warnings off
  the log instead of repeating them: one brush at one size for a whole pass, a stack of
  passes at one angle, a bristle under `size=0.025`, small marks before the masses are
  down, a pressure list on a short chisel mark, and the subject's share of the marks so
  far. `easel run` prints it beside the budget line after every pass, rehearsed or
  committed; `--check` widens it to the painting, `easel log --check` reads it without
  painting, and the MCP `run` tool hands it back.
- **Four warnings, in the shape the `smudge` and `scumble` warnings have** — the call
  still does what it was asked and says what it will look like: a pressure list on a
  short hand-laid mark with a `flat`, `bristle` or `knife` (it changes the paint, not
  the width); a shaped `block_in` with `direction` left off costing over 2.5× what
  `"axis"` would, from `cost` and from the call; `edge="clean"` on a mass whose shorter
  extent is under four brushes, from `block_in` and `preview`; and a banded `scumble`
  whose auto-sized brush is wider than its passes at one end, naming both lengths.
- `compare({place: value})` lists every pair of planned places the plan itself puts
  within the threshold of each other and asks whether they touch — the check the sheet
  never ran: a plan finished all-green with two masses planned `0.00` apart.
  `Comparison.pairs` is it as data.
- `palette.chroma_of(color)` — how *coloured* a colour is, beside `value_of` for how
  light. Measured, the engine lays the chroma it is given, so what reads more vivid
  than its number is the eye judging it against the field, and this is the number that
  predicts it.
- Every log record carries the random stream's state at the start of the call that
  made it (`params["rng"]`) and the mass verb that laid it (`params["via"]`). No format
  bump: older files load, and older builds read the new ones.
- A ninth exercise, the swatch strip: every planned mixture laid side by side before
  the first mass, printing value and chroma. In the guide and `examples/exercises.py`.
- Four recipes: *a volume of lit air* (a beam, a shaft, a halo seen from outside), *a
  small container with something spilling from it*, and two composition entries
  collected from the paintings' notes — *a subject that is one thing against a ground*
  and *a picture with an empty half*.
- `scripts/probe_greenhouse_session.py` — the measurements behind this round, runnable.
- `s.sample(place, rendered=True)` — sample the surface `look()` and `export()` draw
  (relief, and graphite the paint has not buried) instead of the pigment, so *is my mass
  darker than it looks?* is one line rather than a belief.
- `easel guide` prints the guide from inside the installed package, and the wheel now
  carries `PAINTER.md`, `PAINTING.md`, `RECIPES.md`, `REFERENCE.md` and
  `CALIBRATION.md` as `easel/docs/*.md`. `pip install easel-paint` used to hand a
  painter sixteen modules and none of the method.
- `easel run p.easel pass_a.py pass_b.py [--rehearse]` runs several passes in order
  against one session, or one copy of it. A pass that goes on top of another pass has to
  be judged on it.
- `s.sweep(..., wander=)`, off for the contour of `block_in(edge="clean")`: measured,
  the sweep's own wobble is what moves a drawn contour off its line (3.3px to 1.1px), and
  the brush's `jitter` moves it not at all.
- A rehearsal carries the painting's last look, so `look(diff=True)` inside a rehearsed
  pass tints what that pass would change.
- `PAINTING.md` (the reasons) and `RECIPES.md` (fourteen procedures collected out of the
  paintings' own pass scripts) — both moved out of `PAINTER.md` rather than written new.
- A one-click `.mcpb` desktop bundle, built and verified by the release workflow, and an
  MCP Registry entry published in step with each release.
- Python 3.14 is supported and tested.
- `scripts/probe_fourth_session.py` and `scripts/probe_third_session.py` — the probes
  behind the numbers in `CALIBRATION.md`, runnable.
- This changelog.

### Changed

- **The contour of `edge="clean"` is swept along the polygon's own edges**, not a
  spline through its corners. Through two sparse corners the spline bowed outward, and
  three painters met it on three shapes: a pointed arch above a tapering tower, a cap
  eaten to a mushroom, and a 65px arch standing off a four-cornered tower. Measured on
  that tower the contour goes from 65px above the top edge to 4px, the ragged fill's own
  half-brush; the dusk example's `tower()` goes from 45px to 4px. **A behaviour change
  for every clean mass**: a script with one paints differently after this, and every
  committed painting with a clean edge rebuilds with its silhouettes where they were
  drawn. The draw from the stream is unchanged, so nothing laid after a clean mass
  moves.
- **A rehearsal copy counts on from the painting.** Inside `s.scratch()` or `easel run
  --rehearse`, `stroke_count`, `spent`, `remaining` and `budget_line()` are the
  painting's own numbers plus what the pass laid; they read `0` and the whole budget
  before, while `compare()` in the same script saw the painted canvas. What the copy
  itself laid is `s.history.stroke_count`, which is what the *Rehearsed* line reports.
- `block_in`'s `direction` defaults to `None`, which means horizontal exactly as before,
  so the engine can tell *left off* from *chosen*.
- `cost_line()` names the remedy beside the mechanism: *cut into N pieces by the outline
  — lay the straight stretches as strokes, or use a wider brush*.
- The log writes every point exactly rather than rounded to five decimals. Session files
  are a little larger; a replay from one is the painting.
- *The shape each tool leaves behind* has a row for the chisel staircase — a `flat` or
  `knife` filling a mass whose boundary is not parallel to its passes — with the
  measurement (13–17% of strong edges horizontal against 3–4% for a comb or a round tip)
  and the one-stroke repair beside it.
- **`smudge()`'s default `size` is `0.02`, was `0.07`**, and anything past `0.03` now
  warns. Measured on a steep join: what `size` buys stops at about `0.02` (a single pass
  takes roughly half the join out and no more) while what it costs keeps growing — at
  `0.07` one pass drags the lighter mass `4.4%` of the canvas height into the darker,
  against `1.3%` at the default. That is the pale finger-shaped lobe four sessions have
  described. Sizes the guide's own examples used were off the end of that table.
- **`scumble()` on a band picks its own brush**, `3 × extent / n`, when no `size=` is
  given — the mechanism `direction="inward"` has used since 0.1.0, now on both
  directions. A preset's default lands at one to one and a half pass steps on an ordinary
  band, which measures as the worst banding of any width tried. Handed a brush under two
  steps it warns and says how many steps wide it is.
- A keyword that is **not** a brush field now raises a `TypeError` naming the call that
  does take it — `solid=` belongs to `block_in`, `glaze=` to `stroke` — instead of
  `Brush.__init__() got an unexpected keyword argument` from a class the painter never
  mentioned.
- `Region` unpacks: `x0, y0, x1, y1 = shape.box`. It raised `'Region' object is not
  iterable`, which said nothing about where the four numbers were.
- `compare()`'s table says which of the two surfaces it measured (the paint) and names
  the call that reports the other one.
- A `pressure` list is read in canvas order on every pass of a `scumble` or a `sweep`,
  so a passage meant to brighten toward one side can be laid with the verb. The paint
  still alternates direction pass to pass; only the profile is compensated, so nothing
  painted before this moves.
- `s.sample(place)` returns the engine's own linear `float32` array, averaged over a
  shape rather than over its box.
- `PAINTER.md` is the method only — 17,625 words became 9,463, with a 10,000-word budget
  asserted by `tests/test_guide.py`. Not one word was deleted; the essay moved to
  `PAINTING.md`.
- `__version__` is checked against `pyproject.toml` by a test. It had already drifted
  once: the whole of 0.1.1 advertised itself to MCP clients as 0.1.0.

### Fixed

- **`undo` puts the random stream back**, in-process and through the session file. A
  mass draws its pass wander from the session's stream between the strokes it records,
  so undoing one left the stream past it, and `easel undo` — which rebuilds from the log
  — handed back a stream sitting at the seed; the next mass then drew wander a clean
  rebuild never had. A painter measured its working session drifting `1.06%` of its
  pixels from a rebuild and committed the rebuild. Every record now carries the state its
  call began from, `undo` restores it on both paths, and `replay(upto=)` puts the rebuilt
  session's stream where the kept painting stood.
- **A replay from a saved log is byte-identical to the painting.** It was not: the log
  rounded every point to five decimals, so every wobbled pass came back from disk a hair
  off its line — the half of the drift above that no toy case could show, because
  hand-written coordinates are short decimals to begin with.
- `easel run --rehearse` with a single script reported `stroke_count` `0` and the whole
  budget *inside* the script. See *Changed*.
- `block_in`'s `overhang` is documented as what it is: it lengthens each pass past **the
  ends of the pass**, and which two edges those are turns with `direction` — so on a mass
  swept vertically it runs the paint down off the mass's foot. Measured, with the
  box-versus-shape default difference given its own clause. Two masses in one painting
  were spoiled learning this.
- `scumble`'s opacity is documented as what it is: the passes overlap, so a low opacity
  accumulates back toward full colour instead of thinning the passage. From `0.40` up it
  delivers the same passage to within `0.04`. To keep a passage quiet, mix its two
  colours closer together.
- The inward scumble's brush comes from its ring step, and `depth` is computed in one
  place so the step a size is derived from and the step the rings are laid on cannot
  drift.

### Measured, and not changed

Five requests were acted on by measuring them first, and the measurement said no:

- **The engine does not make a mixture more vivid than it was mixed.** Two mixtures
  came back far more saturated in a low-chroma field than their numbers suggested. A
  solid plane reads back at the mixture's own chroma or a little *under* it, in the paint
  and in the rendered view alike; what moved was the eye, judging a colour against its
  field. So no rule and no fix — `chroma_of` is the instrument that lets the question be
  asked as a number.
- **Neither trigger proposed for the clean-edge failure was the trigger.** The distance
  between two outline corners and the brush's share of the shorter extent were two views
  of the contour's spline, which is gone. The share survives as a real second finding —
  the corners of a narrow clean mass go past about a quarter — and that is what the new
  warning reads.
- **The default direction stays horizontal.** `"axis"` would be right nearly always,
  and moving it would move every painting ever made; the price walk says so instead.
- **`pencil`, `dry` and `erase` shift the texture of every mark laid after them**, and
  that is left as it is: it is the log index, not the stream — a mark's texture is seeded
  from its place in the log — and seeding from the paint marks alone would move every
  painting with an underdrawing. Documented, with the property the planning verbs do
  have asserted by a test: `look`, `preview`, `rehearse`, `cost` and `compare` leave
  nothing behind.
- **The view does not lift a solid mass off the value it was mixed at.** A session
  priced this as its most expensive item — four masses laid at planned values that came
  back as bright bars while `compare()` reported the plan clean. Over a mass the rendered
  view and the sampled paint agree to `0.000` at every load, value and ground measured;
  the relief is a *gradient*, so it brightens one side of each ridge of paint and darkens
  the other by as much. `solid=True` costs nothing in the view. What was missing was the
  ability to ask, which `sample(rendered=True)` and `compare()`'s new label now give.
- **`overhang=0` does not leave a shape's boundary bare**, so the warning that was asked
  for is not built. Laid solid, the strip inside the pass ends comes back `0%` unpainted
  at every setting; at the default load it is `8.7%` bare — and the strip inside the
  *sides*, where `overhang` does nothing at all, is barer still at `14%`. That is the
  comb's own texture and the brush running dry, and its condition is `block_in`'s own
  defaults.

### Removed

- `glama.json` and `smithery.yaml`. Neither aggregator reads a file from the repository
  any more, and Smithery discontinued the stdio form the file was written in.

## [0.1.1] — 2026-09-12

### Fixed

- The registry marker in `README.md` and a `server.json` that 0.1.0 shipped without.
  0.1.0 published from a commit two merges older than the one that set the release
  version: its `pyproject.toml` already said `0.1.0`, so the tag guard compared `0.1.0`
  to `0.1.0`, matched, and published the older tree. No engine change — the rule the
  version comment states (edit, commit, merge, then tag *that* commit) is the part that
  has to hold.

## [0.1.0] — 2026-09-12

First public release: the whole engine as it stood after two painting sessions and the
two engine rounds they bought.

### Added

- The painting engine — procedural brush tips, paint load and run-out, wet-into-wet
  pickup, canvas tooth, subtractive pigment mixing, impasto relief, a graphite layer,
  undo and replay from the seed.
- The painter's vocabulary: `stroke`, `dab`, `block_in`, `sweep`, `scumble`, `cover`,
  `smudge`, `glaze`, `pencil` and `erase`, over regions, grid cells, spans and shapes
  (`polygon`, `ellipse`, `blob`, `hull`, `ribbon`, `union`, `s.circle`).
- One plan object shared by `cost`, `preview`, `rehearse` and `paint`, so what is tried
  and what is committed cannot diverge; `Session(budget=)` and the budget line;
  `--rehearse`, which commits nothing and seeds the next real marks so a rehearsed pass
  lands pixel for pixel.
- `compare("ref.jpg")` and `compare({place: value})` — the second is how a painter with
  no photograph checks the canvas against their own written value plan.
- `easel` (the CLI), `easel-mcp` (the MCP server), and the guide:
  `PAINTER.md`, `REFERENCE.md`, `CALIBRATION.md`, `LESSONS.md`.

[Unreleased]: https://github.com/Gemberkoekje/EaselAPI/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/Gemberkoekje/EaselAPI/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/Gemberkoekje/EaselAPI/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/Gemberkoekje/EaselAPI/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/Gemberkoekje/EaselAPI/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/Gemberkoekje/EaselAPI/releases/tag/v0.1.0
