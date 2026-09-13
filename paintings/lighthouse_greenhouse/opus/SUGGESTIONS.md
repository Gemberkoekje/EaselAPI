# What this session would change

A fifth painter, a lighthouse being converted into a greenhouse, 296 strokes of
300, in [`paintings/lighthouse_greenhouse/opus/`](.). This is that session's
list, in the shape the repository's own [`SUGGESTIONS.md`](../../../SUGGESTIONS.md)
keeps: **what was wrong, and what I would do about it.** Nothing here is done —
that file is a register of completed work and this is a request against it.

It is short on purpose. Thirty-one engine items and forty-two documentation items
are already closed, and most of what I would have asked for on a blank sheet is
in that list with a test behind it. What is below is what survived checking
against it.

**Which claims are measured.** `LESSONS.md`'s standing rule is that a claim with
no test behind it says so, and the register notes that every one of the four
painters' claims that has failed re-measurement so far was reported as
*observed*. So: items 1, 2 and 3 are **measured**, by
[`probe.py`](probe.py) beside this file, which prints every number quoted here.
Items 4, 5 and 6 are **not measured** — 4 and 5 are one painting's experience and
6 is an opinion about scope. They are marked as such and should be discounted
accordingly.

**What I read**, because the register says it matters and the split is still an
open hypothesis: `PAINTER.md`, the eight exercises, then `PAINTING.md`,
`RECIPES.md`, `REFERENCE.md`, the sections of `CALIBRATION.md` the rules cite, and
`lighthouse_dusk`'s prelude and notes. That is the **"given everything" arm again**
— the same arm the fourth session was. *The other arm still has not been run*, and
nothing in this file is evidence about it.

---

## The engine

### 1. A chisel tip puts horizontal edges into a mass that has none — measured

**What was wrong.** The tower's lit band is `0.06 × 0.64` with boundaries sloping
about three degrees off vertical, filled with vertical passes. Laid with `flat` it
came back a staircase: each pass of a chisel tip ends in a hard *horizontal* edge,
the boundary slopes so consecutive passes end at different heights, and the ends
stack into steps. Two rehearsals went on diagnosing it as a shape problem — I
smoothed the polygon twice — before it turned out to be the tip.

Measured, as the share of strong edges running within ten degrees of horizontal
over a mass that has no horizontal feature in it at all, so every one of them is
the tool's. Same shape, same passes, same `size`, same `solid=True`:

| tip | `size` | horizontal edges |
|---|---|---|
| `flat` | `0.020` | **13%** |
| `flat` | `0.010` | **17%** |
| `knife` | `0.020` | **16%** |
| `bristle` | `0.022` | 4% |
| `bristle` | `0.012` | 7% |
| `round_hard` | `0.020` | 3% |

Three to four times as many, and a smaller chisel is *worse* because there are
more pass ends. This is the same mechanism as *a shallow shape, passes along its
long axis → its bounding box*, one dimension over, and it is not in the table.

**What I would do.** A row in *The shape each tool leaves behind*:

> | `flat` or `knife` filling a mass whose boundary is not parallel to the passes | **a staircase down that boundary** — each pass ends in a chisel square to its travel, and where the boundary slopes the ends stop at different heights and stack |

with the repair beside it, which is the one that worked here and costs one stroke:
**lay the mass with a comb and put the core back with a single solid stroke down
its middle.** A `bristle` will not lay a solid plane, and a `flat` will not lay a
sloping one; the two together do.

This is a documentation item rather than an engine one, and I would rather it were
an engine one — but I do not know what the engine should do instead. Breaking the
pass ends on an oriented tip would change every mass ever laid, which is the
argument the register already used to refuse folding `solid` into `density=1.0`.

### 2. `edge="clean"` eats a small mass, and does not say so — measured

**What was wrong.** The lantern's cap is `0.214 × 0.036`. Blocked in clean with a
`flat` at `size=0.016` it came back a rounded mushroom instead of a cap with
corners. `edge="clean"` insets the fill by half the brush, and half a brush is a
rim on a large mass and most of a small one.

The number that predicts it is the brush's share of the shape's **shorter**
extent. Area of `shape.inset(size/2)` as a fraction of the shape, on this
painting's own masses:

| mass | `size` | brush / shorter extent | area kept |
|---|---|---|---|
| the lantern cap | `0.016` | 44% | **51%** |
| the same cap, half the brush | `0.008` | 22% | 74% |
| the tower's lit band | `0.022` | 25% | **51%** |
| the lantern box | `0.045` | 36% | **49%** |
| the tower's mid plane | `0.027` | 16% | 75% |
| the whole tower | `0.035` | 12% | 79% |

Half the mass, on three of six, and the corners go first. `PAINTING.md` warns that
`inset()` on a **concave** shape eats the thin parts first, and gives the 62.7% /
76.2% measurement for it. Every shape in the table above is convex, and three of
them lose more than that warning's worst case.

**What I would do.** `edge="clean"` should warn, in the same shape as the warning
`scumble` already gives when its brush is under two steps:

> `edge="clean"` at `size=0.016` insets a mass `0.036` across by 44% of its shorter extent; the fill keeps 51% of it. Use a smaller brush or leave the edge ragged.

The condition is `size / min(box.width, box.height)`, computable before a pass is
laid, and the threshold that separates the two halves of that table is about a
fifth. `preview()` should print the same line, because `PAINTING.md` already says
*preview the inset shape, not the shape* and this is that sentence with a number
on it.

### 3. A shaped `block_in` with `direction` left off costs three to eleven times its price — measured

**What was wrong.** I costed the tower's two planes at 9 and 9 with
`direction=90`, wrote the calls without it, and the rehearsal came back charging
124 strokes for a pass budgeted at 40. `direction` defaults to `"horizontal"`, so
a mass taller than it is wide gets passes stepping down its whole height.

The same masses, priced three ways:

| mass | `"axis"` | `90` | default | ratio |
|---|---|---|---|---|
| the tower's mid plane | 11 | 11 | **43** | 3.9× |
| the tower's lit band | 5 | 7 | **55** | 11.0× |
| the vine mass (wider than tall) | 5 | 8 | 5 | 1.0× |

(The live numbers during the session were 44 and 57 rather than 43 and 55: the
painting laid the mid plane with a `bristle` and the probe prices both with a
`flat`, so the table above is the same phenomenon on one tip rather than two.)

**What I would do — and what I would not.** Not change the default: `"axis"` would
be right nearly always and moving it would move every painting ever made. Instead,
a warning from data the price walk already has: **when a shaped `block_in`'s pass
count is more than about 2.5× what the same fill along the shape's own axis would
cost, say so and name `direction="axis"`.** It fires on both of the masses above
and on nothing else in this painting.

The register's *post-pass check* — queued in `LESSONS.md`, still not built — is
where this belongs if it is built. This is a fourth rule for it, and unlike the
one that session proposed and this one dropped, its condition is met by real
paintings: mine, twice, in one pass.

**And the deeper cause is a conflict between two things this repository
recommends.** `s.paint(plan)` exists precisely so a priced plan and a painted call
cannot drift — the first session asked for it and it was built. But the pass-script
convention in `paintings/`, which the guide points every painter at as the
end-to-end worked example, writes bare `s.block_in(...)` calls. I followed the
convention and the plan drifted, in exactly the way the other recommendation
exists to prevent. Either the worked examples should paint plans, or `PAINTING.md`'s
*a plan that is checked and then retyped is a plan that will drift* should say that
the paintings do it the other way and why.

### 4. Nothing checks the separation *between* two planned places — not measured

**What was wrong.** `compare({place: value})` scores each place against its own
target and flags anything more than `0.10` out. But what `0.10` *means* in this
guide is the distance below which two masses read as one — which is a statement
about a **pair**, and no pair is ever checked. My plan finished with all eight
places inside tolerance and two of them planned `0.00` apart.

Run over my own sheet, written before the first stroke:

| | | apart |
|---|---|---|
| near sea `0.40` | tower `0.40` | **0.00** |
| fog high `0.58` | far sea `0.54` | 0.04 |
| rock `0.21` | vines `0.26` | 0.05 |
| fog low `0.68` | beam `0.75` | 0.07 |

Four pairs of twenty-eight under `0.10`, and the first pair is the two masses that
actually touch on the canvas. The tower's foot dissolved into the water exactly
there. I turned it into a lost edge with two late strokes and wrote it up as a
decision, which it was not.

**What I would do.** `compare({place: value})` should print the pairs of planned
places whose targets are within `0.10` — at plan time, on the empty canvas, which
is the run the guide already tells you to make and the moment it is free to fix.
Three of my four pairs are fine, because those masses do not touch; one was not.
So it is a question, not an error, and the sheet should ask it: *these two are
`0.00` apart — do they touch?*

Not measured, in the sense that the failure is one painting's and the fix is
untested. But the arithmetic is exact and it is in `probe.py`.

---

## The documentation

### 5. The planes are part of the drawing, not part of the finish — not measured

**What was wrong.** `RECIPES.md`'s *a mass built of planes* is the best entry in
that file and I used it twice. It says a mass like this **is** the planes it is
made of, tiling it, and it is right. What it does not say is *when you decide what
the planes are*.

I designed the tower's three planes before the block-in, as polygons in the
prelude beside the silhouette, and the tower turns. I designed the rock's
silhouette with the same care and then invented its planes in the pass, and the
rock is the weakest passage in the painting by a distance — it took 67 strokes
against a budget of 28, six of them repairs of its own committed paint, and it
ended up better rather than good. Same recipe, same painter, one pass apart. The
difference is which side of the block-in the tiling was decided on.

**What I would do.** One clause in the recipe, and one line in step 1 of
`PAINTER.md` where the drawing is made:

> **Draw the planes with the silhouette.** A mass built of planes has two
> drawings in it and the second one is not the finish — decided after the mass is
> down, the planes arrive as things laid *on* a hull, which is the failure this
> recipe already names, one level up.

This is the *observed* kind of claim the register warns about, on a sample of two
masses in one painting. It is worth what that is worth. What makes me put it
forward anyway is that the failure mode it predicts is the one the recipe already
documents, so it is a mechanism for something already known rather than a new
one.

### 6. Composition is the missing fifth leg — an opinion, not a finding

**What was wrong.** The guide is complete on value, on edges, on the marks, and on
depth order. On composition it has exactly one rule — *count the horizontal bands
in the arrangement before the first mass; more than three, and find something that
crosses them* — and that rule is excellent. It is the single most useful sentence
in the guide for this subject, it saved this picture, and everything structural
about the painting came out of obeying it.

But it is one rule, and I made every other compositional decision out of general
knowledge rather than out of the guide: where to put the tower, how much of the
frame the subject should take, what to do with the empty third of the canvas, how
big the beam had to be before it did structural work as well as narrative work.
The guide has a great deal to say about *how much of the budget* the subject gets
and nothing about *how much of the canvas*.

**What I would do — carefully.** Not add a composition section to `PAINTER.md`:
the no-growth rule forbids it, the word budget is CI-held, and this is the
speculative end of the list. But `RECIPES.md` is noun-free procedures and this is
the one thing painters need that has no procedure in it. If it is worth anything,
it is worth three or four entries there — *a subject that is one thing against a
ground*, *a picture with an empty half*, *two things that both want to be the
subject* — collected out of the four paintings the way the existing recipes were,
rather than composed. Which means it cannot be written yet by me: I have one
painting and the recipes were taken from three.

I am putting it forward as the gap I noticed, not as a request I can specify.

---

## What I would not change

Everything in the register's *What none of them would change* section, and for the
same reasons, so I will not repeat the list. Three of those I would put above the
rest after this painting:

**The seeded rehearsal.** Every failure in this picture was caught on a copy and
cost nothing: a chartreuse searchlight of a beam, twice; three flat slabs where a
cylinder should have turned; a chisel staircase down two plane edges; a rock the
same value as the sea; ten pots that were ten bricks; a halo drawn twice the size
of the thing it surrounded; three astragals that made a cage. Every pass was
rehearsed, most three or four times, ninety-two rehearsal images, none charged.
Nothing committed was repainted except six late strokes on the rock, and those
were a decision rather than a rescue. I was told to expect this and still could
not have guessed which passes would go wrong.

**`at_value`, and that it raises.** Twenty-three planned values, every one landing
on its number to the hundredth. And when I asked the rock mixture for `0.135` it
stopped the pass and said the floor was `0.137`, which is how the darkest crevices
in this picture ended up at the bottom of the box on purpose instead of somewhere
above it by accident.

**`compare({place: value})`.** It carried a picture with no photograph to lean on,
and it is the reason all eight places finished inside `0.10`. Item 4 above is a
request to make it better, not a complaint: the reason I can say precisely what it
does not check is that everything else it checks, it checked.

---

## One number for the open hypothesis

The register's remaining open question is whether the essay is load-bearing: two
fresh sessions, one given only the method, the recipes and the reference, one
given everything. **I am the second arm, again, so this settles nothing** — but
the fourth session named the two places the essay paid for it, and I can name
mine, which is the same kind of evidence and points the same way.

Three passages of `PAINTING.md` that are in no other file did specific work here:

- ***Masses that are not rectangles*** — that a pass stops when its *centre*
  reaches the boundary, so the brush hangs over by up to three-quarters of its
  width. That is why the vine mass is sized to let its own spill reach the glass
  instead of being drawn to it, and why the rock's ragged edge was a choice.
- ***The shape each tool leaves behind*** — not any single row, but the idea that
  a tool has a geometry and it will choose if you do not. That is what let me
  diagnose item 1 as the tip rather than the polygon, two rehearsals in.
- **The glaze table.** I never tried a glazed beam. The earlier lighthouse
  rehearsed one twice and dropped it. Four lines of measurement is what the
  difference cost.

None of those is a rule I could have followed from `RECIPES.md` or looked up in
`REFERENCE.md`. All three are the essay being the place the judgement came from
when no recipe applied — which is the third painter's prediction, stated in the
register, arriving from a painter who cannot test it.
