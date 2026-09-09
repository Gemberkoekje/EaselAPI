# The human's note on the paintings

Raised by the repo's owner during the M6 final pass, looking at the paintings this
protocol has produced so far. Recorded verbatim before it was investigated, so the
investigation cannot quietly reshape it.

> I see a lot of very horizontal or vertical strokes, which really show the edges of
> those square strokes. Part of the challenge of painting is to either use circular
> strokes (which has less of an edge to begin with) or to rotate the knife or
> whatever you're using to get e.g. the sides of mountains. This might be something
> to add to the tools and/or make more clear in the painter.md file.

## First reading, before probing

Three separate causes are tangled together in that observation, and they want
different fixes:

1. **The tip angle is undocumented.** `Brush` has `angle_follow` and `angle`, and a
   `flat`, `bristle` or `knife` can be pinned to a fixed angle by passing them as
   per-stroke overrides. `PAINTER.md` mentions neither. Its brush table says only
   that `flat` "Turns to follow the stroke", and its list of overridable properties
   gives `size`, `opacity`, `hardness`, `jitter`, `load` and `load_falloff` — so a
   painter reading the guide has no way to learn that the tip can be rotated at all.
   A painter who cannot rotate the blade cannot cut the side of a mountain.

2. **`block_in` has four directions and three of them are axis-aligned.**
   `"horizontal"`, `"vertical"`, `"diagonal"` (fixed at 45 degrees) and `"cross"`.
   There is no way to sweep a mass along its own form at 28 degrees, which is what a
   hillside, a roof, a cheek or a shoulder asks for. This is sharper than the open
   item already in `NOTES.md` ("consider varying `block_in`'s pass axis
   automatically between passes"): the painter needs to *choose* the axis, at any
   angle. Automatic alternation would not have fixed what the human is looking at.

3. **The guide's own silhouette recipe drives every stroke vertically.** In *A
   region is a rectangle*, the `edge()` walk lays `[(x, top(x)), (x, 1.02)]` — a
   column, at every x. That is the recipe the second rehearsal used for the coat,
   and it is a vertical comb by construction. The recipe is right about starting
   each stroke where the edge is and wrong about where it should then go.

The user's own suggested alternative — round tips, which have less edge to begin
with — is already half in the guide, but only as a warning (`round_soft` "airbrushes
above about `size=0.05`"), never as the positive advice that a round tip is the
right choice when you do not want the mark to declare an axis.

See `probe_stroke_axis.py` for what was measured.

---

## What was measured

Two probes, both run against the engine as the three fresh sessions found it, so
nothing here is an artefact of a fix made afterwards.

### 1. The tip angle works, and nothing tells the painter it exists

`rehearsal3/probe_stroke_axis.py`, sheet `probe_axis_tips.png`. The same horizontal
stroke, laid with `flat`, `knife` and `bristle`, first with the tip following travel
and then pinned at 0, 45 and 90 degrees through per-stroke overrides:

```python
s.stroke(path, "knife", "white", size=0.09, angle_follow=False, angle=45)
```

It works on every oriented tip. At 45 degrees the knife lays a clean parallelogram —
a blade turned to the slope, which is exactly what the note asks for. At 90 the
blade is edge-on to its travel and draws a thin ribbon instead of a slab, which is a
different brush for free. **The capability is complete, reachable, and completely
undocumented.** `PAINTER.md` names `size`, `opacity`, `hardness`, `jitter`, `load`
and `load_falloff` as things that can be overridden per stroke, and stops there.

The default is what produces the square ends: `angle_follow=True` holds the blade
perpendicular to travel, so a horizontal stroke necessarily terminates on a vertical
edge and a vertical stroke on a horizontal one. Every chisel end in every painting
here is square to the canvas because every stroke ran along the canvas.

### 2. The direction the stroke runs matters more than the angle it is held at

`probe_axis_mountain.png`: the same hillside laid four ways. Measured with
`probe_axis_alignment.py` — the share of strong edges running within ten degrees of
horizontal or vertical, so higher is squarer:

| The same hillside | Axis-aligned edges | Strokes |
|---|---|---|
| `block_in` box | 24.7 % | 21 |
| the guide's own `edge()` columns | **34.8 %** | 37 |
| strokes along the slope, tip following | **20.3 %** | 17 |
| strokes along the slope, tip pinned at −34° | 22.4 % | 17 |

Reading it honestly: **running the strokes along the form is the whole win** — 14
points and twenty fewer strokes — and pinning the tip on top of that is worth
little on a long sweep. Pinning earns its keep on *ends and short marks*, which is
what sheet 1 shows and this sheet cannot. The `block_in` box scores low for a
misleading reason: a flat mass has few strong edges at all, so the metric under-reads
it. Look at the panel — it is a rectangle, and no number was needed to say so.

### 3. The paintings already made are squarer than the photographs they came from

Same measurement, whole pictures:

| Picture | Axis-aligned edges |
|---|---|
| `Level1.jpg`, the mug on a table | 22.8 % |
| `Level2.jpg`, the painted landscape | 25.6 % |
| `Level3.jpg`, the sitter | 31.3 % |
| REHEARSAL1 copy | 27.9 % |
| REHEARSAL1 own | 31.9 % |
| REHEARSAL2 copy (of `Level3.jpg`) | 36.5 % |
| **REHEARSAL2 own (the dawn estuary)** | **47.2 %** |

The copy of the sitter came out five points squarer than a photograph of a room
full of tables and door frames. The unprompted estuary — a subject with almost no
straight line in it — came out **half again squarer than any reference in the set,
and squarer than everything else here**. Open `rehearsal2/own_final.png` and the
number needs no defending: the sky is horizontal strips, the water is horizontal
strips, the mud is horizontal strips, the posts are vertical bars, and the one
feature that is neither is the headland the write-up already admits was airbrushed.
The painter had no reason to choose the canvas's axes. It chose them because every
tool it was handed offered them and nothing offered anything else.

## The three fixes this asks for

1. **Engine — `block_in` should take an angle.** Today `direction=` is one of
   `"horizontal"`, `"vertical"`, `"diagonal"` (pinned at 45°) and `"cross"`. A
   hillside, a roof, a cheek, a shoulder or a furrow wants its own axis. Accepting a
   number of degrees alongside the four names is additive — every existing call
   keeps its output, so the golden images do not move.
2. **Guide — document the tip angle**, in *The brushes*, beside the other
   overrides, with the knife-at-45 mark as the reason to care.
3. **Guide — fix the `edge()` recipe**, which currently walks across a mass laying a
   *column* at every step and is the source of the combing in its own worked
   example; and say plainly, once, that a round tip is the tip that declares no
   axis — the guide currently mentions round tips only to warn that `round_soft`
   airbrushes.

---

# Second note: paint from back to front

> Another thing the painter.md should be more clear about: Paint from back to front.

## Checked

**The guide never says it.** `PAINTER.md` orders the work twice — once by size
("it keeps you making *large* decisions before *small* ones") and once by value
(darks, midtones, lights, highlights last). Depth is not an axis it has. Searching
the guide for *back to front*, *background first*, *behind*, *in front*, *overlap*
or *furthest* returns nothing about picture order.

The closest it comes is a parenthesis inside the `block_in` overhang warning:
"block in the big thing first and let the small thing be painted over it
afterwards". That is advice about **size**, offered as a way to dodge a documented
overspill bug, in an API caveat three hundred lines below the workflow. A painter
following the workflow section will never meet it.

## It is the same lesson as the first note

The guide already knows what it wants the *result* to be — from *Edges: lost and
found*:

> The edge is then where two masses meet, which is the only kind of edge a
> painting has.

Back to front is the **order that makes that possible**. If the far mass is already
down, the near one's silhouette happens for free the moment you paint it over the
top: a real edge, made by overlap, with no boundary drawn by anyone. Paint them in
the other order and the only way to get the same edge is to paint *up to* a line —
which is the one thing the guide spends a whole section telling the painter never to
do, without ever saying which order prevents it.

So the two notes are one lesson approached from two sides. The first says stop
letting the canvas choose your stroke direction; this one says stop letting arrival
order decide which mass has to be cut around. Both end at: overlap masses, do not
trace boundaries.

## What it cost these three runs

Every one of them paid for it, and none of them named it:

- **assisted, gap 5**: "A background `block_in` buries the **whole** underdrawing,
  foreground included." They drew the mug, then laid the table behind it, and lost
  the drawing. Two entire recovery passes (`c12_lines.py`, `c13_redraw.py`) exist
  only because of this. Back to front says: table first, *then* draw the mug on top
  of it — and the problem cannot arise.
- **sitter**: the coat's "surface is visibly striped by eleven repair bands". The
  repairs are the background being negotiated with after the fact.
- **pass**: "a stray tan wedge in the handle's hole", "two pale slabs in the
  lower-right table" — both are background patched in around a foreground already
  standing there.

The assisted run reported its version as an engine complaint ("not warned;
`sketch_lines()` is the undocumented recovery route"). It is not an engine
complaint. It is the missing rule.

## The fix

A step of its own in *The workflow*, before the value check, in the guide's own
voice: the order is **furthest thing first**, and it is what makes an edge without
drawing one. Then the `block_in` overhang paragraph can stop offering its
size-based workaround and point at the rule instead.
