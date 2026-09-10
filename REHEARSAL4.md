# REHEARSAL4 — the definition of done, run end to end

**To understand this, start by reading the brief's *Definition of done* section
(`painting-api-brief.md`), then this file, then `rehearsal4/HUMAN_NOTES.md` (the
human's note and its two probes), then `rehearsal4/pass/LOG.md` and
`rehearsal4/sitter/LOG.md` — each fresh session in its own words. `rehearsal4/PREREGISTERED.md`
was written before the paintings existed and should be read before the unprompted
section, not after.**

Two fresh sessions, launched in parallel, each given `PAINTER.md` and `CALIBRATION.md`
and nothing else: no `src/`, no `NOTES.md`, no `REVIEW.md`, no brief, no earlier
rehearsal, no docstrings, no `help()`. The prompts are in `rehearsal4/launch_note.md`
in full. The engine's author read the notes and did not paint, did not edit a painting
script, and sent the unprompted paintings to the human before opening them.

Every number below is re-measured from the exported PNGs and the saved sessions by
`rehearsal4/verify_done.py`, `probe_structure.py` and `probe_human_notes.py`. Where a
painter's log and a script disagree, the script wins.

| Run | Reference | Stage |
|---|---|---|
| `rehearsal4/pass/` | `Level1.jpg`, a mug on a table | The copy, then the two unprompted paintings |
| `rehearsal4/sitter/` | `Level3.jpg`, the sitter | How far the tools reach |

---

## The verdict first

**The pass run meets every criterion but one, and the one it fails is not the one
anybody was watching.** The value criterion that M6 was left open on is met, cleanly
and for the first time. The criterion it fails is *"the painter can point to strokes
it rejected in `preview()` or `rehearse()` before painting them"* — **the pass session
called `preview()` once and `rehearse()` never.** Its thirteen rejected marks were all
caught by `look()` after they had been paid for, which is a correction, not a
rejection. See *The criterion that failed*, below; it is the same defect the human's
note found, arriving from a third direction.

| Criterion | Result |
|---|---|
| Recognisable copy of an ordinary object | **Pass.** A mug of black tea, spoon, wooden table, teabag and tag. |
| Under 300 strokes | **Pass.** 299 on the mug, 299 on the sitter. |
| Without touching source code | **Pass.** `git status` clean across `src/`, `tests/`, `scripts/`, `examples/`, both guide files. |
| No cell **on the object** more than `0.10` out | **Pass.** 0 of 64 cells out — the whole canvas, not just the object. Worst `0.0985`. |
| Strokes rejected in `preview()`/`rehearse()` **before painting them** | **FAIL on the pass run.** 1 `preview`, 0 `rehearse`. Its 13 rejected marks were all caught by `look()` after being painted. **Met on the sitter run**: 6 previews, 6 rehearsals, 9 marks that never touched the canvas. |
| Headline run without `sketch(reference)` | **Pass**, and checked from the engine's own record rather than the painter's word: `assisted=[]` on all four sessions. |
| Two unprompted paintings | **Pass.** 236 and 235 strokes. |
| The second not repeating the first's composition | **Pass**, on both pre-registered clauses. |
| All exports plus time-lapses exist | **Pass.** 8 of 8. |
| Golden-image tests still pass | **Pass.** 276 passed, 3 skipped, no golden regenerated. |
| The sitter: how far do the tools reach? | Answered below. Not a pass criterion. |

**And the numbers it passes are thinner than the table makes them look.** Three things
are worth more than the ticks:

1. **The copy passes every number and is not a good painting**, and the human found
   the reason by looking at it — see the next section. The criterion missed it by
   `0.0015`.
2. **The value criterion is close to saturated.** Worst cell on the mug `0.0985`
   against a `0.10` threshold; worst on the sitter `0.0951`. Both runs cleared it by
   less than a hundredth.
3. **The one session in five that never rehearsed is also the one that produced the
   defects the human saw.** That is an argument for the tool, not evidence of a guide
   failure — four of five fresh sessions reach for `rehearse` unprompted.

---

## The criterion that failed

The brief's pass clause is three things at once, and the third is about *when* a mark
is judged:

> the human recognises the object, `compare()` reports no reachable cell on it more
> than `0.10` from the reference's value, and the painter can point to strokes it
> rejected in `preview()` or `rehearse()` **before painting them**.

Counted from the sessions' own output directories:

| Run | `preview` | `rehearse` | Marks rejected before touching the canvas |
|---|---|---|---|
| `pass` (the mug) | **1** | **0** | **0** of 13 |
| `sitter` | 6 | 6 | 9 of 13 |

The pass session's rejected-marks table is a good and honest document, but every row
in it is a mark that was painted, looked at, disliked and painted over — including
*"the entire first mug pass, 72 strokes"*, which took the session's only `undo`. That
is the loop the guide is built to replace, and the cost is measurable: 138 of 299
strokes went on the table because it was painted three times.

The sitter session ran the other experiment without being asked to, and wrote the
conclusion itself:

> **`rehearse` is the best thing in this toolkit** and I under-used it early — the one
> pass I skipped it on is also the one that cost me 31 strokes.

Five rehearsals of one square of that face cost nothing and are why its eye works.

**But this is one session, and it does not replicate.** Counted across every fresh
session the repo has run:

| Session | `preview` | `rehearse` |
|---|---|---|
| REHEARSAL3 `pass` | 0 | 8 |
| REHEARSAL3 `sitter` | 2 | 5 |
| REHEARSAL3 `assisted` | 0 | 4 |
| REHEARSAL4 `sitter` | 6 | 6 |
| **REHEARSAL4 `pass`** | **1** | **0** |

Four of five rehearsed, one did not. **So the honest reading is painter variance, not
a guide that fails to teach the tool** — and the tempting conclusion, that `rehearse`
should be moved into the block-in workflow, is not supported by this evidence. What
the run does show is what happens *when* a session skips it: the human's note, the
five whole-canvas block-ins, and 138 of 299 strokes on one table are all downstream of
the same session being the one that never rehearsed. That is a strong argument for the
tool and a weak one for a guide edit.

The criterion failure is still a failure — the brief asks the pass run to point at
marks it rejected before painting them, and this one cannot. It is evidence about this
painter, and a reason to re-run, rather than a defect to fix in prose.

---

## The human's note, which is the most important result here

The repo's owner, looking at the pass session's `look_046.png` while it was still
painting:

> It is not first painting the back of the mug, then the tea, then the front of the
> mug, and because of it, the tea kinda flows out of the mug. Also something went
> wrong with the table, where it looks a table correction was done after the mug ear
> was drawn.

It was **not** passed to the painter. A fresh session that gets coached stops
measuring the guide, which is the only reason the protocol uses one. `HUMAN_NOTES.md`
has the full write-up and the probes; the short version:

| | REHEARSAL4 | REHEARSAL3 |
|---|---|---|
| Dark that escaped the cup | **17.5 %** of the tea's own area | 0.1 % |
| Worst excursion | **0.150** of the picture's width | 0.046 |
| Standing detail buried by later masses | **117.7 %** | 33.5 % |

**Neither defect is visible to any criterion in the brief.** `compare()` averages a
cell, so tea that has escaped onto the handle-side shadow lands where the reference is
*also* dark — it can improve the value number while making the picture worse. In fact
the escaped tea is exactly what the worst surviving cell is: D2, the mug's mouth, too
**dark** by `0.098`, `0.0015` short of failing the run.

Two findings follow.

**The guide has no rule for depth order inside a single object.** Section 2, *Paint
from back to front*, is entirely about depth between separate things — "Background,
middle distance, foreground, in that order, every time", with a landscape for its
worked example. A mug has three depths that are all the same mug: far rim, contents,
near wall. So do a bowl, a glass, a sleeve, an eye socket, an open mouth. The rule
covers all of them and none of its words do.

**The rule against correcting a background under finished foreground is present and
inert.** The guide says it: *"A mistake in the background is cheap while the
foreground is not there yet. It stops being cheap the moment something is standing in
front of it."* The probe names the marks that broke it — **#113, #115, #117, #118,
#119, every one `block-in all 8.0`**, a whole-canvas block-in, #119 burying 100% of
the detail standing when it landed. The painter's own log reaches the same place
counting strokes instead of pixels: *"138 of 299 strokes went on the table because I
painted it three times, and the subject got 160."* The rule is not weak, it is in the
wrong place — a painter fixing a value it has just measured is never prompted to ask
what is standing in front of that mass.

---

## The pass — the mug

299 strokes, own pencil (7 lines), `assisted=[]`, 0 of 64 cells out.

The painter's own verdict is the honest one and there is no reason to soften it:

> It passes and it is not good. [...] the mug's body is three flat vertical stripes
> with visible zigzag joins because I swept the lit and shadowed sides along the
> silhouette and never blended them, so a cylinder came out faceted; the rim is a
> chalky horseshoe far too thick [...] almost every edge in it is equally hard, which
> the guide names as the commonest failure and which I had no budget left to fix.

Against REHEARSAL3, the value failure that milestone M6 was left open on is gone:

| | max &#124;delta&#124; | cells out of 64 | character of the error |
|---|---|---|---|
| REHEARSAL3 | 0.1989 | 8 | D3–D6, all too **light**, straight down the shadow side |
| REHEARSAL4 | 0.0985 | **0** | D2 too **dark** — the escaped tea |

**The narrow question `NOTES.md` set for this run is answered: yes, the value error
goes away.** The guide changes made after REHEARSAL3 — `compare()` on the empty
canvas, planning the three values as numbers, painting back to front — survive their
first fresh-session test. What replaced the error is a *drawing* failure that no
number in the brief detects.

---

## Two unprompted paintings

`PREREGISTERED.md` was written while `rehearsal4/pass/` held one empty session file,
because a probe whose reading is chosen after seeing the result measures nothing. It
recorded that all three unprompted paintings this engine had ever produced were stacks
of horizontal bands (`+10.9` to `+16.6` dB, four to seven times as many horizontal
strong edges as vertical), and fixed in advance what would count as a break: **at
least 8 dB below the first, and the edge split reversed or levelled to within a factor
of 1.5.**

| | band dB | horiz % | vert % | axis-aligned |
|---|---|---|---|---|
| **own1** — no constraint at all | **+8.37** | 29.8 | 7.4 | 37.2 % |
| **own2** — must not repeat own1 | **+0.09** | 8.4 | 9.0 | 17.4 % |
| REHEARSAL3 unprompted | +13.51 | 36.1 | 6.8 | 42.9 % |
| REHEARSAL2 unprompted | +16.60 | 41.3 | 5.9 | — |
| REHEARSAL1 unprompted | +10.93 | 25.4 | 6.6 | — |

**A break on both clauses.** The gap is `8.28` dB, and the split does not merely level
— it inverts, from 4.0:1 horizontal to 0.93:1. The blunt probe the brief actually
names, `probe_axis_alignment.py`, shows it too: `37.2 %` to `17.4 %`.

**own1 is a sunset over water with a bare tree, birds and reeds** — the fourth
water-and-sky picture in four runs, and at `+8.37` dB still the least banded of them.
The painter is clear-eyed about it: *"a cliché — sunset, water, dead tree, three birds
— chosen because it suited the engine rather than because I had anything to say."*
Read `rehearsal3/unprompted/`'s 63% result before reading anything into the subject.

**own2 is a sunflower**: radial, centred, on a square canvas the painter chose for the
purpose. It organises by angle and radius from one point instead of by height, and it
applies *back to front in radius* — the back row of petals under the front row — which
is the guide's rule transposed to a structure the guide never mentions. It is also the
better painting of the two. The painter names its flaws without prompting: three
repair passes whose archaeology still shows, four leaves that are "pale mint slabs
pasted at the corners", and the flower sitting nearly dead centre.

**What this does and does not show.** The capability is there: told only not to repeat
a structure, and told nothing about marks, subject or palette, the painter changed the
organising principle *and the canvas format* and carried the guide's depth rule across
to the new structure. What it cannot show is preference — own1, the free one, is the
fourth estuary-adjacent landscape in a row.

---

## The sitter — how far the tools reach

299 strokes, **zero pencil marks** (no underdrawing at all), 0 of 64 cells out, worst
`0.0951`.

`rehearsal4/sitter_compared.png` puts it beside REHEARSAL3's and REHEARSAL2's. **This
is the best-drawn of the three and the pose is the thing that improved**: a sharp left
profile that matches the photograph, with the gloved hand, the orange carton and the
coat mass all placed. REHEARSAL3's head is better finished and facing the wrong way.

The painter's answer to "is it him":

> Someone holding the photograph would match them instantly. Someone who wasn't would
> say "a bearded man in profile in a dim bar", not "him".

What got there: the profile — brow, bridge, nose, upper-lip shelf, chin — laid as
background painted back up to the edge rather than as a drawn line; the eye, with a
three-pixel catchlight; the hair, lank and dark over the forehead and lit gold across
the crown. What did not: the open mouth, which is the photograph's whole subject and
came out a dark smear; and the face as a *head* rather than a mask, for a reason worth
recording as an engine finding —

> there is no way in this API to grade a mass from one value to another (wet-into-wet
> dies in eleven strokes, `round_soft` airbrushes above 0.05, `smudge` only moves what
> is there), so a cheek is one flat slab with bars laid on it.

### The floor, and M6b

17 of the sitter's 64 reference cells sit below the box's `0.128` floor — a third of
the figure, not "a handful at most" as the brief expects. **All 17 landed inside
tolerance anyway**, and the sitter session worked out why on its own:

> the floor is 0.13 and the threshold is 0.10, so anything the reference puts at 0.03
> or above is reachable — you just have to cover the cell completely.

It verified that a supplied colour escapes the floor (`#101014` reads `0.064`) and
then did not need it. **M6b is vindicated precisely**: the darkened masstones did not
make dark references *comfortable*, they made them *reachable*, and the margin on the
worst cell is `0.005`. The brief's "a handful at most on the sitter" should be
rewritten — the right claim is about tolerance, not about cell counts.

Also worth fixing: `compare()` never printed a `~` at any stage, including on an empty
canvas with six cells at 0.04–0.06. Neither session ever saw the marker the guide
describes.

---

## What the two sessions found in the guide

Both logs end with a list of moments the painter wanted the source. Fifteen and
thirteen. The ones that cost real strokes, consolidated — these are the M9-blocking
guide changes, and **every one of them is a hypothesis until a fresh session paints
against it** (`REHEARSAL.md` → `REHEARSAL2.md` is the standing lesson):

1. **No syntax anywhere for supplying your own colour**, though `PAINTER.md:154` and
   `CALIBRATION.md:48` both promise it works, black included. Every `s.palette[...]`
   example in the guide assigns from `mix`, `tint` or `desaturate`. Both sessions had
   to probe it. `p["ink"] = "#0d0c10"` works, `(0.05, 0.05, 0.07)` works, and
   `[13, 12, 16]` **silently clamps to white**, which is a trap. On a palette with no
   black this is the one escape hatch a dark reference needs.
2. **A shaped `block_in` spills up to three-quarters of a brush past its own
   silhouette, and the guide phrases this as reassurance.** Cost the pass run 72
   strokes and the session's only `undo`. Wanted: *"inset the shape by half the brush
   size, or keep the brush under about a fifth of the mass's width."*
3. **Low `opacity` on a long stroke still saturates.** The guide says this about
   `pressure` and never about `opacity`, which is the knob it hands you. Wood grain at
   `opacity=0.08` came out as eleven shouting ribbons and forced the third table
   repaint — the repaint that caused the human's second note.
4. **No feature-scale rule.** "Use a bigger brush than feels comfortable" appears four
   times with no counterweight; the sitter repainted twice for it.
5. **`bristle` is destructive below about `size=0.02`** — four stripes, so it is the
   wrong brush for a cheek. The pitch is in `CALIBRATION.md`; nobody draws the
   conclusion.
6. **A short `flat` stroke is a rectangle.** Two rejected marks in the pass run are
   this. Wanted: *small accents want `round_hard`; `flat` and `knife` want a length.*
7. **`smudge` and `glaze` count against the budget and the guide never says so** — the
   sitter measured it with three strokes left.
8. **No way to budget a `block_in` before calling it.** The formula is in
   `CALIBRATION.md`; the 300-stroke budget bites in `PAINTER.md`.
9. **The `out/` counter is per-session**, so a second painting in the same directory
   silently overwrites the first's looks. The pass run lost all of own1's and
   recovered its rejected frames out of the time-lapse GIF.
10. **No gradient story.** Either name a technique for grading a mass or say there
    isn't one.

Plus three from this run's own failures, which are the ones that change a picture
rather than save strokes:

11. **Depth order inside a single object** — the guide has no rule for it, and the mug
    is the case that proves it. (Human's note.)
12. **Move "don't correct a background under finished foreground" into the measuring
    loop**, where the correction actually gets decided, instead of leaving it as
    section 2's third sub-bullet. (Human's note.)
13. ~~**`preview` and `rehearse` belong in the block-in workflow.**~~ **Withdrawn —
    the evidence does not support it.** Four of five fresh sessions rehearse without
    being told to (8, 5, 4 and 6 times); only REHEARSAL4's pass run did not. This is
    painter variance, and rewriting the guide for it would be fixing prose to chase
    one session. Watch the count instead — `verify_done.py` now reports it — and
    revisit only if a second run skips the tool.

### One open question closed

`NOTES.md` asked whether a fresh session would reach for M8's shaped masses. **Both
did, without being told they existed**: the pass run called `ellipse` 30 times,
`polygon` 13 and `ribbon` 3; the sitter called `polygon` 21 and `ribbon` 4. The
vocabulary is found and used. What has *not* gone away is the patchwork of rectangles
in both backgrounds, and the sitter's log blames the region vocabulary for it while
itself calling `polygon` 21 times — so the complaint is narrower than it sounds: the
painters reach for shapes on the subject and fall back to boxes on everything behind
it.

---

## The human's verdict on the paintings

Recognition is the human's call, not a script's, so it is recorded here in the human's
own words rather than paraphrased.

**The mug — the pass.** *"R4 is the right painting and R3 was the pretty one. R4 has
the far rim, the tea, and the near wall in the correct order, the crewmate as a dark
shape with one pale mark, the string reaching a tag, and a shadow on the correct side.
It's rougher than R3 everywhere, and it's a better copy everywhere, which is what under
300 strokes with its own pencil should look like."* Note what this does to the reading
above: the depth-order defect the same human caught mid-run is a defect in *this*
painting and R4 still has the order more right than R3 did. The remaining tell is the
table — *"square patches, every one axis-aligned. The mass that needed no drawing is
the one that shows the grid."*

**The sitter — reach, and a tension in the method.** *"R3 reads more as a person than
R4 does. R4 has a face — an eye in a socket, a mouth, hair with direction — and lost
the figure around it; the head is a collage of planes with the body and hand dissolved
into the background. R3 has a worse face and a clear silhouette, a hand, a carton,
someone at a table."*

**This is the sharpest finding in the run and it is about M6 itself:** *"landmarks buy
features and cost the mass, and the guide's own line 'an eye sitting on a face rather
than in it' now applies to a face sitting on a painting rather than in it."* The M6
tools do what they were built to do — the sitter session placed a three-pixel
catchlight where it meant to — and the budget that precision consumes comes out of the
silhouette, the support and the surroundings, which is where recognition actually
lives. My own earlier reading of the sitter comparison sheet said this run was "the
best-drawn of the three"; on likeness, which is what the stage measures, that is wrong.
Both readings can hold — the drawing is better placed and the picture is less of a
person — and the second is the one the milestone is about.

**The unprompted pair.** *"A sunset over water with a bare tree and three birds, and a
sunflower. Those are the two most painted subjects on earth [...] they're also the most
confident paintings in the set, the sunflower especially, where the petals are single
directed strokes and the centre is dabs and the leaves are dry. The marks finally do
what the guide says. But given 'paint something of your own' with nothing else, the
prior handed over its two safest answers."*

Two facts make that cleaner evidence than it first looks. The guide this session read
had already had its estuary example removed after the REHEARSAL3 critique, so the
sunset is not an echo of the guide; and nothing of the mug carried into either painting
— no cup, no table, no cast shadow — so it is not an echo of the copy either. The
subjects came from the painter.

### The second painting is not unprompted, and the write-up has to say so

The brief already anticipated this — *"The second painting is therefore partly a
capability probe rather than a free choice, and the write-up says so"* — and this run
makes the point concrete. The instruction was two *distinctly different* paintings,
which defines the second against the first. The sunflower is landscape-versus-close-up,
cool-versus-warm, wide-versus-centred: **a contrast chosen, not a subject chosen.**

So the protocol's own reading has to be split:

- **The first painting is the result.** It is the only fully unprompted one, and the
  sunset is what the prior offers when nothing is asked.
- **The second is commentary on the first** — it says how this painter reasons about
  difference, which is worth having and is not the same measurement.

Keep the two-painting protocol: it is cheap and it doubles the material. But score the
first and read the second. And **if a fresh run's first painting is a sunset again,
that is itself the finding** — at that point the subject is the prior speaking, and no
amount of further unprompted runs will say anything new.

## What was changed in `PAINTER.md`

Made after this run, before any re-run. **All of it is a hypothesis until a fresh
session paints against it** — that is the standing lesson of `REHEARSAL.md` →
`REHEARSAL2.md`, and none of the numbers below have been re-measured against a guide
that says these things.

Fourteen edits covering the twelve findings; `+196 −22` lines, and every one of the
guide's 37 Python blocks still runs (`python rehearsal/check_guide_blocks.py`).

**The two that are meant to change a picture:**

| Where | What |
|---|---|
| §2 *Paint from back to front* | New: **an object with an inside has its own depth order** — far rim, contents, near wall — with a runnable three-mass example and the list of other hollow things it applies to. |
| §2 + *Put a number on it* | The background-correction rule keeps a short form in §2 and gains its operative form in the measuring loop, where corrections are actually decided: **look at what is standing on a mass before repainting it**, with a three-option ladder (repaint before the near things go on / repair around them / repaint and restore on purpose). |
| Checklist | Two lines: *anything with an inside — is its far edge under its contents?* and *did a correction bury something?* |

**The ten that are meant to save strokes:**

| Where | What |
|---|---|
| *Colour* | **Supplying a colour of your own** — the syntax the guide promised twice and never showed, plus the trap that a 0–255 list silently clamps to white. |
| §3 values | The floor arithmetic: `0.13` floor against a `0.10` threshold means **anything at `0.03` or above is reachable if you cover the cell**. Reframes the floor from a wall to a margin. |
| *Masses that are not rectangles* | The shaped-block-in spill turned from reassurance into a **warning**, with the inset rule and a runnable example; plus: do not cross a small shaped mass. |
| *Per-stroke overrides* | **`opacity` accumulates back to full colour on a long stroke**, with working numbers; and `block_in`/`sweep` take the same overrides. |
| *The brushes* | `bristle` below `size≈0.02` is four stripes, not a brush; a short `flat`/`knife` is a rectangle and small accents want `round_hard`; and the **feature-scale counterweight** to "use a bigger brush than feels comfortable". |
| §5 edges | `smudge` is much stronger than "move paint around" implies, and it is **asymmetric** — it pulls light into dark. |
| §4 mid-tones | **There is no gradient tool** — said plainly, with the steps-and-lose-the-joins technique that replaces it. |
| *The rest of the API* | How to cost a `block_in` before calling it, and what counts against the budget (`smudge` and `glaze` do; `pencil`, `preview`, `rehearse`, `compare` do not). |
| *Looking* | The `out/` counter is per-session, so **a second painting in the same directory destroys the first's record**. |
| §6 highlights | The three-marks rule moved out of the pressure section into the workflow step where it is needed. |

**Then two more findings from the human, and one defect in the edits themselves.**

| Where | What |
|---|---|
| *Masses that are not rectangles* | **The mass that needed no drawing is the one that gives you away** — painters reach for shapes on the subject and boxes on the background. Cross-referenced to *The angle of the mark* rather than restating it. Plus a checklist line: check the background hardest. |
| *When to stop measuring* | **Precision is paid for somewhere else in the picture.** Landmarks buy accuracy where you point them out of the budget for everything you did not; spend the last third of the strokes on what is *around* the thing you measured. Plus a checklist line: cover the thing you measured most carefully and look at what is left. |

### The leak, and why it mattered

**The first version of these edits put the copy reference into the painter's manual.**
The depth-order rule was written with a mug as its worked example — mug, tea, cup, rim,
table — and the feature-scale rule with a head and a cheek. Neither word appeared in
`PAINTER.md` before this session; both copy references did (`git show HEAD:PAINTER.md`
confirms zero). The human caught it: *"the mug is now in the guide by name. The copy
reference in the painter's manual is the one leak that feeds straight back into the
copy score."*

That is exactly right, and it is worse than an aesthetic problem. The pass criterion is
how well a fresh session copies `Level1.jpg`; a guide that teaches depth order *using
that photograph's subject* hands the painter the answer to the thing being scored, and
every future mug run would have been measuring the guide's worked example instead of
the painter. It would also have been invisible in the numbers — the score would simply
have improved.

Fixed: the depth-order rule now names no subject and gives a list (a boat, an archway,
a barrel, a hood, a cuff, a window reveal, a cave mouth); the scale rule is stated as a
ratio ("inside a mass `0.3` across, a plane wants `0.015–0.025`") instead of a head and
a cheek. `mug`, `tea`, `cup`, `face` and `cheek` now appear zero times.

**The rule this run establishes: nothing that appears in a copy reference goes into
`PAINTER.md` as an example.** Worth applying to the guide periodically, not just after
an edit — it is a one-line grep and it protects the only number the copy stage has.

**Deliberately not changed:** `preview`/`rehearse` stay where they are — see *The
criterion that failed*.

### On length, and the rule that came out of it

The edits took the guide to **10,805 words against 8,621**, and the human's diagnosis
of why was sharper than the number: *"what's grown in them isn't rules, it's
explanations of engine behaviour dressed as advice [...] Every one of those is a
measurement with a rule attached. The rule stays in the guide as one line; the
measurement and the reasoning already have a home in `CALIBRATION.md`."*

My own proposal — cut *Eight small exercises* — was rejected, correctly: *"They're the
only part of the guide where the painter learns by doing instead of by being told, and
a fresh session that skips them paints worse."*

So the split was done instead. **`PAINTER.md` 10,805 → 10,168; `CALIBRATION.md`
3,849 → 4,572.** Moved, rule kept as one line in each case: the shaped-mass spill and
its inset rule, the `opacity` accumulation and its working numbers, the `load` window
and falloff, the `bristle` floor at `size=0.02`, the oriented-tip non-taper, the
feature-scale ratios, the `smudge` window and its asymmetry, the floor arithmetic, the
`block_in` cost formula, and the crossing's stringiness. The guide is **+18% on where
this session started, not +25%**.

**That is 637 words, not the couple of thousand the human estimated.** The
measurement-with-a-rule-attached category is now empty — a scan for number-dense
paragraphs returns only `grid="fine"`'s tenths, which is how to use the tool. The
remaining bulk is not that kind of text: *Working from a reference* (2,151) is M6's
tools and is mostly how-to, and *What you are bad at* (1,351) is the shape and sweep
vocabulary. Getting to 2,000 would mean cutting how-to, which is a different decision
and the human's to make.

**The standing rule is now in `NOTES.md`'s key decisions**, because the pattern
mattered more than this instance: *a new finding never adds a paragraph to
`PAINTER.md`. It replaces an existing rule, becomes a checklist line, or goes to
`CALIBRATION.md` or `NOTES.md`.* The guide had been growing by about a paragraph per
rehearsal — every finding right, every one added — and the failure mode is not that any
paragraph is wrong but that **a fresh session reads the guide exactly once, at the
start, when it matters most.** The test for a candidate: strip the measurement and the
reasoning out and see what is left. If it is one line, that line is the rule. If
nothing is left, it was not a rule.

## What to do next

1. **M6 is not finished. The guide changes are made; run one more fresh session on
   `Level1.jpg` against them.** Everything above is a hypothesis until then. Five
   questions, all already instrumented, none of them told to the painter:
   - Does the tea stay in the cup? (`probe_human_notes.py` note 1 — 17.5% now.)
   - Does the table stop eating the handle? (note 2 — 117.7% now.)
   - **Is the table still a grid of square patches?** (`probe_axis_alignment.py`, and
     the human looking at it. This is the one the guide has just been changed for.)
   - Does the painter rehearse a mass before laying it? (`verify_done.py`, *Marks
     judged before they were paid for*. One session in five did not; a second would
     make it a pattern.)
   - Does the value result hold? Both runs cleared it by under a hundredth, so watch
     it rather than re-litigate it.
2. **Re-run the sitter too, which the previous plan said to skip.** The human's read
   changes this: R4's face is better and R4 is *less* a person than R3, so the
   milestone's real question — how far the tools reach — now has an answer that points
   at the method rather than the tools. The guide change for it (*precision is paid for
   somewhere else*) needs the same test as the rest, and the sitter is the only
   reference that exercises it.
3. **Keep the two-painting unprompted protocol, and score only the first.** See *The
   second painting is not unprompted*. If the first is a sunset again, stop running the
   stage: at that point it is measuring the prior, and the recommendation in
   `REHEARSAL3.md` — have the human name a subject with no reference image — becomes
   the cheaper experiment.
4. **Grep the guide for the copy references before every run.** `mug`, `tea`, `cup`,
   and whatever the current references contain. See *The leak*.
5. **Rewrite the brief's *Reachable* paragraph.** "A handful at most on the sitter" is
   wrong — 17 of 64 cells are below the floor and all of them passed. The claim that
   holds is that the floor now sits within one threshold of anything a photograph
   holds.
6. **Then M9, the MCP server.** Everything that changes the API is done. Nothing in
   this run asks for an engine change; item 10 above (no way to grade a mass) is the
   only candidate, and it should be argued on a picture first.

## Files

| Path | What |
|---|---|
| `rehearsal4/PREREGISTERED.md` | Baselines and break criteria, written before the paintings |
| `rehearsal4/HUMAN_NOTES.md` | The human's note, both probes, proposed fixes |
| `rehearsal4/launch_note.md` | The exact prompts both sessions were given |
| `rehearsal4/verify_done.py` | Every criterion in the definition of done, from the artefacts |
| `rehearsal4/probe_structure.py` | Banding, edge split, mass centroid |
| `rehearsal4/probe_human_notes.py` | Containment, and detail buried by later masses |
| `rehearsal4/grid_reference.py` | The gridded references the cell masks were read from |
| `rehearsal4/make_sheets.py` | The comparison sheets |
| `rehearsal4/pass/LOG.md` | The pass session in its own words |
| `rehearsal4/sitter/LOG.md` | The sitter session in its own words |
| `rehearsal4/pass/rejected/` | 12 rejected marks with the look that caught each |
| `rehearsal4/human_note_exhibit.png` | The frame the human's note was written against |
| `rehearsal4/mug_compared.png`, `sitter_compared.png`, `unprompted_pair.png` | Side by side |
