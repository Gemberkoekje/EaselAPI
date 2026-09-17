# Laundromat at night — painter's notes

**To understand this, start by reading [`prelude.py`](prelude.py) (the palette as
planned values, every mass as a shape function, and the value plan), then the passes
in order `p0_plan.py` → `p14_sign.py`. The finished picture is
[`painting.png`](painting.png) and the time-lapse is [`painting.gif`](painting.gif).**

**Reproducible:** the fourteen pass scripts rebuild `painting.png` **byte for byte**
from a fresh session on easel 0.2.0, verified by sha256.

Subject: a laundromat at night, seen from the sidewalk across the street. 1024×768,
linen, custom ground, seed 11. **286 of 300 strokes**, plus 2 free signature marks.
Value plan came back clean — all five places within 0.04 of plan.

The subject was chosen and written down *before* this repository was opened, which is
what `PAINTER.md` asks for; `paintings/` and `RECIPES.md` were only read afterwards.

---

## Key decisions

- **A custom ground, `#5a5045` (v=0.32).** No preset ground goes below `umber_wash`
  at 0.425, which is far too light for a night picture — every mass would have been
  a hole in it. A warm ground at 0.32 puts the cool night darks in a relationship
  from the first mark, and the flecks it leaves showing through the façade are grit
  on a wall rather than gaps.
- **Three values, planned as numbers first:** façade `0.17` / wet street and
  reflection `0.46` / window interior `0.88`. `palette.at_value()` hit every one of
  the twenty-odd mixtures exactly, so no value was ever guessed.
- **Two light stories, kept separate.** Cold fluorescent out of the window, warm
  sodium from a lamp off-canvas right. Mixing them at 0.45 made the pavement pool
  amber, which read as sodium coming *out of* a laundromat — so the window's own
  spill was re-mixed at 0.82 toward the fluorescent and the warm was confined to the
  right-hand piers, the wall's foot and one highlight on the fascia's end.
- **The window as a hollow thing**, in three depths: lit back wall → machines,
  table and figure → frame and mullions. Painted in that order, the opening's edge
  is where the frame's paint stops and the lit field still shows, and nothing had to
  be cut around anything.
- **Every pass rehearsed before it was paid for.** 56 rehearsals, none charged, and
  essentially every one changed something. Not one stroke was spent repainting a
  mass, and `undo` was never used.

## Gotchas

Six of these became engine requests in `SUGGESTIONS.md`, and the repository re-measured
every one of them before building anything. **Four held up; two did not** -- the first
item below, and the second half of the third. Both are marked in place rather than
quietly deleted, because a wrong finding with its correction attached is worth more
than a tidy list, and because both were marked *observed* rather than *measured* when
they were raised, which is the distinction earning its keep.

1. ~~**Relief shading in the view lightens solid paint well above its pigment
   value.**~~ **Wrong, and left here because it is the most instructive thing in
   these notes.** Four masses — the fascia, the base course, the sidewalk and the
   puddle — looked one to three steps lighter to me than the value I had mixed them
   at, and I reasoned from that to a mechanism: a solid mass builds the most paint
   height, so the relief in the view lifts it. **#33 measured it and the
   mechanism does not exist.** Over a mass the view and the paint agree to `0.000`
   at every load, value and ground tried; the relief is a *gradient*, so it
   brightens one side of each ridge of paint and darkens the other by as much, and
   the worst single pixel anywhere is `0.038`. `look()`, `look(values=True)`,
   `export()` and `export(impasto=False)` all read one mass at `0.314`.

   So what actually happened is the false alarm the guide already warns about, four
   times over: a `0.25` band against a `0.17` wall *does* look like a bright bar,
   because contrast is local, and *"a cool mass on a warm ground reads about two
   steps lighter than it measures... Believe the number."* I did not believe the
   number; I invented a reason for it to be lying. The `0.252` and `0.211`
   measurements were right and were telling me nothing was wrong.

   The one part of the item that survived was the suggested repair rather than the
   diagnosis — what the session lacked was a way to *ask*. `s.sample(place,
   rendered=True)` now samples the view, and `compare()` names which of the two
   surfaces it measured. Reproduce all of it with
   `python scripts/probe_fourth_session.py`.
2. **A hard edge separates two masses at 0.03 of value.** The base course sat 0.03
   above its wall and still came back a bright bar. Edges do the separating, not
   values — so throw an end away rather than lowering a number.
3. **`overhang` lengthens each pass past the ends of the *pass*, and which two edges
   those are turns with `direction`.** At 0.6 on the *vertically* stacked door it
   lengthened the passes downward and ran the glass over its own kick panel onto the
   sidewalk. That half held and is now said in those words in `REFERENCE.md`,
   `PAINTING.md` and the docstring. **The other half did not:** I blamed the dark
   notches in the window's left edge on the shape default of `0`, and #33
   measured that laid solid the strip inside the pass ends is 0% unpainted at every
   setting. The notches were the comb and the brush, not `overhang` — raising it
   covered them, which is not the same as it having caused them.
4. **A cross-direction on a wide shallow band is enormously expensive.** The fascia
   cost **49** strokes at `direction=(4, 94)`, **17** at `(5, 173)` and **8** single.
   `cost_line` said why in one sentence: *2 directions, 24 passes each stepping
   across 0.76 of the canvas.* Cost the call before widening the brush, not after.
5. **`scumble` fails in both directions and I hit both.** At `size=0.050` on a 0.034
   step it left dark gaps between its passes and the brightest mass in the picture
   came back a venetian blind; at `opacity=0.60` over the road its dabs accumulated
   back toward full colour and it came back a pale slab brighter than the sidewalk.
   The brush must be well wider than the step, and a low opacity does not thin a
   passage — it only slows it down.
6. **Four of five `smudge`s failed exactly as documented.** At `size=0.024–0.032` on
   a boundary between a glow and a 0.17 wall it does not blur the join, it walks the
   light mass into the dark and leaves a pale finger-shaped lobe — on both piers, on
   the roofline, and worst as a blob sitting on the open road. The surviving one runs
   at a third of that size. Paint, not smudging, is what removes an edge.
7. **Dark laid into wet light sinks.** The machine doors measured `0.443` against the
   `0.33` they were mixed at, and the figure `0.290` against `0.24`. `dry()` between,
   and mix *below* the target: the figure went in at `0.185` to land on `0.24`.
8. **Default jitter beads a thin member.** The frame's members are 0.009–0.021 wide,
   where the default `jitter=0.02` wanders further than the member is thick — every
   one came back a chain of separate blocks. `jitter=0` and `size_jitter=0` is the
   ruled-line recipe, and a shopfront frame is exactly the one or two things in a
   picture that really are ruled.
9. **`inset()` pinches thin joins off.** The figure's knee became a floating blob;
   the fix was to build a 0.026 overlap into the `union` rather than to inset less.
   And `smooth()`'s default two passes cut the neck notch away and handed back a lump
   with no shoulders — `smooth(1)`.
10. **A brush wide enough to lay a big mass is wide enough to overhang a small step
    away.** The roofline's parapet was eaten three times; the fix was to make the
    parapet *taller* (a 0.105 step), not the brush smaller. `edge="clean"` was worse
    than useless here — with a bristle it left a pale stringy fringe along the whole
    roofline, which the engine warned it would.
11. **Load below about 0.6 lays almost nothing** on this texture. Exercise 3 taught
    me that and I still laid the road's breaking marks at 0.35–0.45, where they
    barely registered.

## The number I said I would write down

**117 of 286 paid marks — 41% — on the subject, against a planned 45%.** The gap is
real and worth naming: the share was at 45% when the window was finished, and passes
11 and 12 (the near foreground and the wall surfaces) took it down, which is the
guide's own instruction to give the last third to the surroundings. Pass 13 then put
the last six marks back on the picture. I did not spend the remaining budget forcing
the ratio back to 45%, because that would have meant adding marks to the strongest
part of the painting to satisfy a number written before I knew what it needed.

**Weakest passage, twice named and twice spent on:** first the left third — the
façade's raw combed edge and a pier with no incident in it at all, which got the
flyers, the soil pipe and the crossing marks. Then the near foreground, which still
banded horizontally and got the drain, the second wet patch and the corner weights.
14 strokes were left in hand at the end, under 5%.

**One mark thrown away deliberately:** an opening through to the back of the shop was
rehearsed into the middle bay and dropped. Cropped in, it read as a pale slab
floating on the wall rather than a hole in it, and with nine small incidents already
in the picture a tenth that does not read is clutter.

## Signature

Two `liner` marks in the bottom-right corner, on the dark side of the road where the
reflection has already died, close in value to what they sit on. Not a name, because
I do not have one, and not a monogram standing in for one: one short stroke and a
shorter one under it, the second saying only that the first was meant. Deliberately
*not* laid across a passage I was unhappy with, which would be a correction wearing
a hat.

## File map

| File | What it does |
|---|---|
| `prelude.py` | palette as planned values, every mass as a shape function, the value plan |
| `p0_plan.py` | no paint: mixtures as numbers, plan against bare ground, every mass costed |
| `p1_far.py` | sky (graded scumble) + haze + façade + roof stack |
| `p2_facade.py` | sodium light on the piers and the wall's foot, fascia, downpipe |
| `p3_street.py` | road (graded), sidewalk, kerb, marks breaking the road's bands |
| `p4_glass.py` | the hollow thing's far depth: the lit back wall, tubes, door glass |
| `p5_inside.py` | its middle depth: folding table, machine run, doors, the figure |
| `p6_frame.py` | its near depth: head, sill, jambs, two mullions, door frame, push bar |
| `p7_light.py` | the light outside the glass: fascia underside, piers, sill, pavement pool, road reflection |
| `p8_edges.py` | edges — soft, lost, and one deliberately found |
| `p9_left.py` | weakest passage #1: the left third — flyers, soil pipe, surface, puddle |
| `p10_accents.py` | eight highlights, smallest brushes |
| `p11_foreground.py` | weakest passage #2: the near foreground — drain, wet patch, corners |
| `p12_wall.py` | surface only, no new objects: stall riser, right wall, upper wall |
| `p13_last.py` | the last marks, back on the subject: machine joints, laundry, notice |
| `p14_sign.py` | the signature (free) |
| `p15_export.py` | final numbers, export, time-lapse, contact sheet |
| `probe.py`, `probe2.py` | before any session existed: what each ground reads at, and every mixture's hex and value |
| `check*.py`, `cost*.py`, `crop*.py`, `share.py`, `review.py`, `diag.py` | measuring and looking; they lay no paint |
