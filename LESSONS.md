# Lessons learned

Easel was built to a brief of nine milestones, and measured by six rehearsal runs in
which fresh sessions painted a picture against nothing but `PAINTER.md` and were then
read. Those write-ups, an adversarial review register of sixty-six findings, and the
brief itself were each recorded at length and have since been deleted: a build note is
worth keeping only while the build it describes is still moving.

This file is what survived them — the method that worked, the engine decisions that are
load-bearing, the traps that cost real time, and what is still open. It is the file to
read before changing the engine or the guide. It is not a changelog, and a new finding
does not get a paragraph here just for being true.

The two things beside it: [`PAINTER.md`](PAINTER.md) is the guide a fresh painter reads
and the project's actual deliverable; [`CALIBRATION.md`](CALIBRATION.md) holds the
measured numbers behind it. [`SUGGESTIONS.md`](SUGGESTIONS.md) is the open request list
from the most recent painting session and is the newest input in the repo.

---

## The method that produced this

Every defect worth fixing in this repo was found by looking at a picture. None was found
by the test suite. The suite is what keeps a fixed defect fixed; it has never once
discovered one. That single fact determines the whole method below.

### A guide change is a hypothesis until a fresh session paints against it

This is the rule everything else hangs off. Four consecutive runs demonstrated that
writing a rule down is not the same as the rule working: a paragraph can be correct,
well-placed, repeated three times and in the closing checklist, and still fail every run.
Stating a rule is a *proposal*. The measurement is a session that has never seen the repo
painting a picture and then being read.

### Warning is not method

The largest single finding across all the runs, and the one that generalises furthest.
Four of six painters independently said the guide tells them a state is bad without
telling them what to do instead — and the guide's response had been to repeat the
warning, which is why a painter could count four instances of a rule it had ignored four
times. Repetition is what a document does instead of having an answer. When a rule keeps
failing, the fix is a procedure, not a louder warning.

### A new finding never adds a paragraph to the guide

It **replaces** an existing rule, **becomes a checklist line**, or **goes to
`CALIBRATION.md` or here**. The guide grew by roughly a paragraph per run — every finding
right, every one added — and went from 8,621 to 10,805 words across a single run's fixes.
No paragraph was wrong; the failure mode is that a fresh session reads the guide exactly
once, at the start, when it matters most, and the tenth run produces a guide nobody
finishes. The test for a candidate paragraph: strip the measurement and the reasoning out
and see what is left. If one line is left, that line is the rule and it goes in the guide,
and the measurement goes to `CALIBRATION.md`. If nothing is left, it was not a rule.

### A worked example is an instruction, whatever the prose beside it says

A fresh session reads the code blocks as if they were the whole document, because to it
they nearly are. A silhouette recipe that laid a vertical column at every step was
followed exactly, three runs running, producing the combing the same guide warns about
elsewhere. The same applies to nouns, and **the two directions of that leak are not
equally visible**:

- A **subject** leaking *out* of the guide costs the unprompted stage. One run's estuary
  was, word for word, the back-to-front example, and two later sessions painted it
  unprompted. A wrong result, but one that announces itself to anyone reading both files.
- A **copy reference** leaking *in* costs the copy score and **hides**, because the only
  symptom is that the number improves. A guide that teaches depth order using the copy
  reference's own subject hands the painter the answer to the thing being measured. This
  happened while fixing a real defect and was caught by a human reading the diff, not by
  any criterion in the protocol.

So the guide names nothing that appears in a reference, and **a list is not a safe
substitute for a subject**: one depth rule ended "it holds for a boat, an archway, a
barrel, a hood, a cuff, a window reveal, a cave mouth", and six of six fresh sessions then
named an overturned rowing boat, three of them describing the picture as being about
seeing into the hull. Any list is a ranked list and its first item is the answer. Seven
things is a principle; one thing is an instruction. State the rule with a ratio, or with
nothing.

Grep the guide for the references' nouns before every run — and then **read the examples
end to end and name the subject yourself**, because the grep only catches words already
known to be in a reference. That check is two minutes and it is the only one that catches
a noun the guide invented. It has caught its own author: three leaks were introduced by
the very edits that wrote the rule down.

### Never change the engine while a measurement is running

Every session in a run paints against one engine, and fixes land after the last of them
exports. Otherwise the run measures a moving target and none of its numbers can be
compared with each other.

### Check the painters' numbers

A painter reporting on its own painting is not a measurement. Every figure in the run
write-ups was re-measured from the exported PNGs. They were mostly right and not entirely.

### The measurement can be right and the instrument still wrong

Two findings were tools that lied: `value_of` returned linear luminance while the
greyscale view showed sRGB, and the first attempt to measure a halftone screen measured
the height map's autocorrelation rather than the paint that landed. Before trusting a
number, check it against the picture the painter actually sees.

### A measure that can be satisfied by damage is not measuring the thing

`compare()` averages a cell, so a bar of dark improves the cell it lands in whatever it
does to the picture. One painter laid exactly that, deliberately, in its last ten strokes
to move two cells inside tolerance, and led its own log with the admission: *"it reads as
tape, and I traded the picture for the number knowingly."* The answer was not a better
threshold but a second measurement no single mark can improve at the same time
(containment: the share of a mass's paint that lands where the reference has nothing like
it), plus a procedural rule — **the last ten strokes may not be value corrections** — that
costs nothing to enforce because the log carries the order.

### Build the tool that tells the painter the truth, then go and fix what it said

`compare()` gained an `unreachable` split — cells whose reference value is below anything
the palette can reach — because two sessions each spent about twenty-five strokes
discovering for themselves that the target was unmeetable. Then the palette's floor was
taken from `0.235` to `0.13` and the list is normally empty, which is the right end state
for a split like that.

---

## The protocol, if a run is ever repeated

The build is finished, so the brief that specified it is gone; this is the part of it that
is still live. A run measures the *guide*, not the engine.

A fresh session, given `PAINTER.md` and a reference photograph, produces a recognisable
copy in under 300 strokes without touching source code, then produces **two** paintings
with no prompt. All exports plus their time-lapses exist. The engine's author has not seen
the unprompted paintings before the human has.

- **Two references.** First an ordinary object — a mug on a table will do — and that run
  is the pass: the human recognises the object, `compare()` reports no cell on it more
  than `0.10` from the reference's value, and the painter can point to marks it rejected
  in `preview()` or `rehearse()` before painting them. Then a portrait, which is the
  measure of how far the tools reach rather than a pass: recognisable or not, and the
  write-up says which features got there.
- **The headline result is painted without `sketch(reference)`.** The pencil is the
  painter's own — sketch, look, adjust, then paint — and landmarks, preview and rehearsal
  are how it gets precision below a cell by its own seeing, which is the thing being
  measured. A run that starts from the machine-laid sketch is an assisted mode: worth
  running, reported separately, never the number that says whether the guide works.
- **Two unprompted paintings, and the second must not repeat the first's composition.**
  One is not a sample: 63% of thirty-two fresh sessions named the same subject — a
  rain-wet street at dusk — before opening the guide, so a single unprompted painting says
  almost nothing about the painter, the guide or the engine, and two runs read meaning
  into exactly that. The first is unconstrained. The second must differ in compositional
  structure and that is the *only* constraint — do not prescribe the remedy ("make one
  line-based and the other curve-based"), because that hands over the artistic decision
  the stage exists to observe. Constrain the repeat, not the remedy.
- **Every finished painting is signed.** After the last look, before the export: up to
  five marks noted `signature`, free of the stroke budget and charged in full past five so
  the exemption cannot be spent on painting. The painter chooses what the mark is; the
  guide says nothing about it. It is asked what it chose and why *at that point and never
  before*, because a mark chosen in order to be explained is a different thing from a mark
  chosen. A flourish, not a measurement — but it is the only place in the protocol where
  the painter puts something in a picture that is not of the picture.
- **Stop running verbal naming probes.** Three attempts settled it: 0 of 8 sessions *name*
  water, 4 of 4 *paint* it. A verbal probe measures what a session says when interrupted.
  The finding they did produce is better than any tally — the estuary is not a subject
  this model picks, it is a world it puts things in: given a boat it beaches it on a
  mudflat, and told to break the structure it painted a pond seen from above.

Non-goals, unchanged: no GUI, no fluid simulation, no image-to-image or style transfer
anywhere in the pipeline (the point is that the strokes are *chosen*), not pixel art, not
vector.

---

## Engine decisions that are load-bearing

The six that make output look painted rather than generated — pigment mixing in K/S
space, spacing measured along travel, smoothed wobble, aperiodic tooth grain, the
per-stroke bristle comb, width following pressure — are in [`README.md`](README.md) under
*Design notes*, because they are what a reader needs to understand the engine at all.
These are the rest, which you need before changing it.

- **Strokes are seeded per stroke index**, not drawn from one running stream. That is what
  makes `replay()` exact, which is in turn what makes CLI undo possible without persisting
  snapshots. The canvas tooth and grain are derived from the seed, so a saved session does
  not store them.
- **The tooth gate's threshold is capped at the surface's own tooth ceiling.** Textures are
  all centred near 0.5 but span very different ranges, and an uncapped threshold climbs
  past the highest peak of the narrow ones — which is how a starved brush came to deposit
  *nothing* on linen and smooth while still marking rough. `tooth_ceiling()` in
  `canvas.py`.
- **Every mark records how much paint actually landed**, not how many dabs were stamped.
  Dabs are attempts: a stroke can stamp 278 dabs and change nothing, and before this there
  was no way — from the API or from the log — to tell that apart from a stroke that worked.
- **Graphite is a channel, and paint buries it by what landed, not what was aimed at.**
  `stamp()` does `sketch *= (1 - effective)` with the same per-dab alpha the colour blend
  uses, which gives the whole contract for free: coverage after `k` dabs of alpha `a` is
  `1 - (1-a)^k` and the graphite left is exactly `1 - coverage`. A dab the tooth refused
  leaves the drawing untouched, which is why an underdrawing survives a scumble. Graphite
  accumulates as a *maximum*, not a sum — dabs along a pencil line overlap almost
  completely and any additive rule turns the line into a solid bar within a few dabs.
- **`sketch_lines()` is derived from the log, not stored.** Pencil records accumulate,
  erase records clip; undo and replay are then right for free, because there is no second
  copy of the drawing to keep in step.
- **A rehearsal is seeded as the *next* strokes of the real painting**, so what you try on
  the scrap of canvas is what lands. The trial holds its own generator *object* carrying a
  copy of the session's stream state, which is how it can be both pixel-identical to the
  real call and unable to change the painting that follows. Strokes never needed this —
  they are seeded per index — but `block_in` and `sweep` take their pass wander from the
  running stream.
- **`preview`, `rehearse`, `cost` and `stroke` take the same argument shape.** A plan is a
  list of `stroke()` kwargs, so what was checked is what gets painted without being
  retyped. A plan that has to be rewritten between checking it and painting it is a plan
  that will drift.
- **`block_in` takes an angle, and the four named directions are frozen.** `direction=`
  accepts degrees or a sequence of them, but the horizontal / vertical / diagonal / cross
  branches are byte-for-byte what they were and dispatch happens before them. That is what
  let this land mid-milestone with golden images already stored: every existing painting
  replays identically, so no golden had to be regenerated and nobody had to decide by eye
  whether a mark had got better. **Add capability beside the old path, never through it.**
- **`prepare()` quantises in Oklab, then labels connected components, then merges the small
  ones.** Quantising straight to the target number of masses gives one area per *colour*,
  and a picture has more masses than colours — two separate things the same brown are two
  masses. The connected-components pass is what turns colours into places. Edge hardness is
  the Oklab gradient along a shared boundary, not the value gradient: a warm table against
  a cool wall at the same value is an edge the painter can see, and a value gradient calls
  it lost.
- **Drawing does not count as a stroke** (`History.UNPAINTED_KINDS`), because a painter
  charged for the underdrawing is a painter who skips it. The signature exemption is the
  other shape of the same idea and is per-*record*, capped at five, with everything past
  five charged — a cap that is not a cap can be spent on painting.
- **Region names are deliberately neutral** (`upper-band`, not `sky-band`), because the
  unprompted stage is meant to be unprompted.
- **Mixbox is an opt-in extra, not a dependency.** A better pigment model, but its
  reference implementation is CC BY-NC and this repo is MIT. `EASEL_DISABLE_MIXBOX=1`
  forces the built-in model.

---

## Traps

Each of these cost real time at least once.

1. **Look at `samples/brushes.png` after any engine change — and then paint something.**
   The sampler shows *isolated strokes at full load*: it was perfectly happy with a gate
   that silkscreened the canvas weave across every accumulated mass. Block-ins on top of
   block-ins are a different test. Keep a throwaway abstract script around for it.
2. **A golden failing is an instruction to look, not to regenerate.** The test writes
   `tests/golden/<case>.actual.png` beside the stored `<case>.png` and says how far apart
   they are. Open both. `python scripts/make_golden.py <case>` only after deciding the new
   marks are better. A golden regenerated without looking records that a mark changed and
   asserts that nobody minded, which is worse than having no golden at all.
3. **Assert on the canvas, not on the return value.** Both engine findings of one
   milestone were invisible from the API. Diff `canvas.rgb` either side of a stroke when
   you touch deposition.
4. **Anything linear in per-dab alpha cannot produce a persistent mixture.** If you are
   tuning a wet-blending coefficient and seeing no effect, this is why.
5. **Anything a mask is computed from has to be in its cache key.** The tip-mask cache was
   keyed on `ceil(radius)` while the mask used the exact radius, so what a script painted
   depended on what had run before it *in the same process*. If you add a parameter to
   `tip_mask`, add it to the key **and** quantise it before anything reads it.
6. **A canvas-mutating `Session` method must push an undo snapshot immediately before it
   touches the canvas, in the same method.** `undo()` pairs the top of the snapshot stack
   with the last log record on the assumption that the two always move together: `dry()`
   mutated and logged without snapshotting, so `undo(1)` after a `dry()` popped the
   *previous* action's snapshot while dropping only the `dry` record — correct-looking
   return value, canvas silently two steps back, and `replay()` from the intact log then
   disagreeing with the screen. Grep for `push_snapshot` in `session.py` before adding a
   new kind of mark.
7. **A record that carries a place has to carry the whole place.** A shape logged as its
   bounding box replays as a rectangle; a shape logged as *nothing* replays as the whole
   canvas. `dry` and `erase` log `shape` or `region`, and `_place_from_params` is the one
   place that reads either back.
8. **A tuned constant often encodes a *ratio*, not an absolute, so it moves when the thing
   it is relative to moves.** The mixing exponent was set to give white its real tinting
   strength, without recording strength *compared to what*; darkening the palette widened
   its value range and the same number quietly went from carrying a 50/50 white mix `0.235`
   of the way up that range to `0.158`. Write down the invariant you tuned a constant to
   hold, not just the value you landed on.
9. **An identity in floating point is a claim to be measured, not assumed.** Restoring a
   clipped colour by adding back `c - np.clip(c)` is exactly right on paper; the K/S round
   trip does not land on its own input, so the correction missed by a constant `1.7e-6`
   *in one direction* on every blend and a near-black leaked 23 levels over 5000 dabs. A
   single application looked perfect. Iterate a few thousand times and compare to the
   start.
10. **When a document explains a limit, check which layer imposes it.** Twice a guide
    passage stated a *palette* choice as an *engine* fact and was believed — the `0.23`
    value floor was the swatches, and "nothing in this engine reflects less than `0.01`"
    was the box's range. Both read as physics and both were furniture. The tell is a
    sentence telling the painter what is impossible; go and try it, because the fix for an
    engine limit and the fix for a palette choice are nothing alike.
11. **A workaround built around a defect has to come out when the defect is fixed, and its
    *documentation* is the part that gets left behind.** Grep for the *number* — not just
    the feature — when a limit moves.
12. **Normalised space is not isotropic, and `size` is measured against the long side.** A
    coordinate is a fraction of the *width* in x and of the *height* in y, so on a
    non-square canvas a step of `0.07` down is a different number of pixels from `0.07`
    across — while a brush at `size=0.07` is `0.07` of the long side whichever way it
    travels. `block_in` has always mixed the two and `sweep` follows it on purpose rather
    than introducing a second convention in one call. If this is ever made pixel-true,
    make both pixel-true in the same change and expect every golden to move.
13. **A self-intersecting outline is accepted.** `Polygon` checks for three distinct points
    and a non-zero area, not for simplicity, and everything downstream is even-odd, so a
    bow-tie fills as two triangles. `inset` is a mitre offset and can fold a spiky outline
    through itself, which is why it checks the result's area and centre and falls back to
    pulling the points toward the centre.
14. **Before concluding anything about what a painter chose, ask what it was offered — then
    go and measure it.** An early note asserted, from two paintings, that a painter given
    the guide "will paint a horizontal landscape". Thirty-two fresh sessions later: six of
    eight given the real guide named a street or an interior. What survived is smaller and
    more useful — no estuary appeared in sixteen samples without the guide's landscape
    words, and a painter told what the engine is *bad* at justifies its choice with
    horizontal bands six times in eight. A plausible story about a tool's influence is
    worth about as much as a plausible story about a bug.

Environment papercuts, for whoever loses ten minutes to one: `np.savez_compressed` appends
`.npz` to a path without it (save through an open file handle; there is a test).
`import easel.brush as b` gets the *function*, because `__init__` rebinds the name — use
`from easel.brush import ...`. `sin(pi)` is slightly negative in float32 and a negative
base with a fractional exponent is NaN. `np.cross` no longer takes 2-D vectors in numpy 2.
numpy rejects a float32 probability vector that misses 1.0 by an ulp, which a quarter of a
million squared distances comfortably does. Check what `import easel` actually resolves to
before trusting a measurement — an editable install can point at a stale copy of the repo.
The repo is LF (`.gitattributes`), even on a Windows checkout.

---

## What is still open

**In the engine, with evidence.**

- **`Session.load()` restores `out_dir` from the session file with no validation.** It
  round-trips because that is how `easel look p.easel` keeps writing to the same place
  across CLI invocations — load-bearing, not an oversight. But loading and then `look()`ing
  a `.easel` file someone handed you writes wherever *they* set `out_dir`, silently,
  including an absolute path outside the working directory. Rejecting absolute or
  `..`-escaping paths outright would also reject what a user legitimately sets with
  `--out-dir` when *creating* a session: it is the same field either way. Wants a product
  decision (a flag to override the stored value? a warning when it differs from the cwd?),
  not a rule a reviewer picks unilaterally.
- **`undo()`'s fast snapshot path does not rewind `Session.rng`.** So
  `s.block_in(...); s.undo(1); s.block_in(...)` draws different wobble than a fresh session
  doing the same two calls. A correct fix needs an `rng` snapshot at the same granularity
  as the canvas snapshot, but `block_in`/`sweep` draw their wobble from lazily-evaluated
  generators interleaved *between* the per-path `stroke()` calls that push each snapshot —
  so by the time a stroke's snapshot is pushed, that path's wobble has already been drawn.
  Snapshotting there would leave the stream advanced past the undone stroke rather than
  rewound to before it, which is subtly wrong in a way a quick fix is more likely to get
  wrong than right. Only that sequence is affected; `stroke()`, `pencil()`, `dry()` and
  `erase()` never touch `self.rng`.
- **Residual dab-frequency ripple** on `flat` and `knife` at large sizes. Much reduced, and
  at this level it reads as ridging from a loaded brush rather than machine stripes. Worth
  another pass if it ever reads as mechanical in a real painting.
- **`block_in` passes can read as parallel hatching.** Mitigated by per-pass wander, by
  alternating the travel direction of successive passes, by `direction="cross"`, and by the
  guide telling the painter to vary direction between passes. Varying the *pass axis*
  automatically is still worth trying.
- **About 200 ms per stroke** on a 1024×768 canvas — a minute for a 300-stroke painting.
  Acceptable, not fast. The hot path is the per-dab window blend.
- **`.easel` files are megabytes**, because the full float32 canvas is stored. Since replay
  is exact, a future format could store only the log and rebuild on load, trading file size
  for load time.

**Not yet reviewed.** The MCP server has never had an adversarial code review of its own.
What such a pass should aim at: `_place` and `_plan` in `easel/mcp_server.py`, the only
code in the repo that turns untyped JSON into engine objects, and the echoed Python beside
them — two defects were already found there by driving the tools rather than by reading
them. The engine itself is untouched by that milestone.

**About the protocol, if it is run again.** Three questions were left to the repo's owner
and none has been decided:

- **The unprompted stage should probably become "chosen before the guide is read".** Four
  of four sessions painted the subject they had named before reading anything, and their
  median structure score was `+0.53` against a baseline where all six first unprompted
  paintings sit between `+8.12` and `+23.83`. That is a different measurement and a better
  one: it measures what the painter chooses rather than what the guide retrieves.
- **The structure probe is partly measuring "has a sky".** It is the variance of the row
  means over the variance of the column means, so it cannot separate a smooth vertical
  gradient from a stack of slabs: a three-step gradient with its joins smudged scores
  `+32.3`, a field of overlapping scumbles at close values `+38.2`. The edge shares beside
  it are the half that discriminates, and a human looking is still the verdict.
- **The value criterion is saturated.** Worst cell on the last three copies: `0.0985`,
  `0.0961`, `0.0987`, against a `0.10` threshold. Three different painters cleared it by a
  thousandth, and on all three runs containment caught a defect it could not see.

**In the guide.** The depth-order paragraph has now failed three runs — containment
`17.5%`, `16.3%`, `13.2%` against a best of `0.1%` — and stating the rule, giving it a
runnable three-mass example *and* putting it in the closing checklist has been shown not to
be sufficient. It needs a rewrite, and that is a design job with a measurement attached
rather than an edit. Everything else the last run found has been applied.
`SUGGESTIONS.md` is the list from the most recent session and nothing on it has been
actioned yet.

---

## The milestones, as a key

Source comments, test docstrings and `CALIBRATION.md` date things by milestone — *"before
M6b the palette floored at `0.23`"*, *"bumped to 3 by M8"*. The brief that named them is
gone, so this is what the names mean. They also head most of the commits.

| | |
|---|---|
| **M1** | Canvas, round brush, strokes, `look()`, PNG export, seed, the brush sampler. |
| **M2** | Flat and bristle tips, paint load and run-out, canvas texture, wet blending, `dry()`, pigment mixing, palette. |
| **M3** | Regions, grid, relative placement, `block_in`, values view, side-by-side, diff, history and time-lapse. |
| **M4** | The CLI and `PAINTER.md`. |
| **M5** | The first rehearsal: paint a reference from the guide alone, twice, the second time with a fresh session. |
| **M6** | Precision below a grid cell: golden images, matching crops, `preview`, landmarks, `compare`, `prepare`, the pencil, the liner, `rehearse`. |
| **M6b** | Darkened the dark pigments from colour-chart brights to masstones. The palette's floor went `0.235` → `0.13`, which moved every golden. |
| **M6c** | `sweep()` — a mass laid as passes along its own boundary, stepped inward. |
| **M7** | Marks at detail scale: the comb drawn per stroke, a bristle with a width of its own, width following pressure on the round tips. |
| **M8** | Masses that are not rectangles: `Polygon` beside `Region`, and `block_in` cutting each pass against the outline. |
| **M8b** | Took the Kubelka-Munk reflectance floor off the *answer*, leaving it on the arithmetic. |
| **M9** | The MCP server. Nothing in the engine changed. |

M6, M8 and M8b landed before M9 on one rule: **anything that changes the API lands before
the thing that exposes it.**

---

## Verifying a change

```bash
pytest -q                              # 286 passed; the mcp and mixbox tests
                                       # skip unless their extras are installed
ruff check src tests scripts examples
python scripts/check_guide_blocks.py   # every python block in PAINTER.md runs: 44 ok
python scripts/make_brush_sampler.py   # then LOOK at samples/brushes.png
python scripts/make_shape_sampler.py   # and at samples/shapes.png
python examples/exercises.py           # the guide's warm-ups, writes out/ex_*.png
```

The first two are what CI runs. The last four are the ones that have actually found
things.
