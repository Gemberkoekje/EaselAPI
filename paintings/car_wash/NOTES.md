# Inside a car wash, from the driver's seat

A painting made from `PAINTER.md` alone, with no reference photograph. The subject was
chosen before the guide was read: the view out of a windscreen mid-cycle in an
automatic car wash — a magenta foam arch overhead, a bloom of white light down the
tunnel ahead, a red stop light, and a foam-smothered side brush swinging in from the
right. Steering wheel, rear-view mirror and the dashboard's reflection close the near
side. Everything outside the glass is dissolved; nothing in it has a hard edge except
the things inside the car.

- Canvas 1152×720, linen, `umber_wash` ground, seed 23.
- **185 strokes** of a 300 budget, plus one signature mark that did not count.
- Final painting: `painting.png`. Time-lapse: `painting.gif`.
- `prelude.py` holds the palette, the masses as shapes, and the written value plan;
  `p1_far.py` … `p12_sign.py` are the painting in order. Against a fresh
  `easel new painting.easel --size 1152x720 --texture linen --ground umber_wash
  --seed 23 --budget 300` those fourteen passes reproduce `painting.png`
  **byte for byte** — verified by sha256. `p0_plan.py`, `p0b_preview.py` and
  `check.py` paint nothing and are not part of that sequence.

## No assisted modes

There was no reference, so `prepare`, `sketch`, `ref_shape` and `ref_outline` were not
used and nothing was traced. Every mass is a `polygon`, `blob` or `Region` written by
hand and checked with `preview()` before it was filled. No pencil was laid: with no
photograph to measure against, the shapes *were* the drawing, and `preview()` was how
they got looked at before any paint went on them.

## The ground

`umber_wash` reads `0.43`, which is both the darkest ground in the box and almost
exactly the planned mid value. It was chosen for that after the first session was
started on `cool_grey` (`0.54`) and thrown away: nearly everything in this picture is
darker than `cool_grey`, so every gap would have read as a hole. Warm ochre under a
cool dark picture also flecks through the tunnel everywhere the paint is thin, which
is most of what keeps that field alive.

## The plan, and what it cost

Values were written down first, as a `compare({place: value})` sheet in `prelude.py`:
dash `0.16`, brush `0.56`, bloom `0.68`, upper glass `0.47`, lower glass `0.36`. The
three carrying values were frame `0.15`, haze `0.46`, bloom `0.74` — separations of
`0.31` and `0.28` against a `0.10` threshold. The final canvas is within `0.07` of
that sheet in all five places, worst `-0.07`.

| Stage | Strokes | Share |
|---|---|---|
| Far masses: the tunnel field and the foam arch | 54 | 29% |
| The glass: bloom, stop light, water, rivulets, foam, edges, reflection, finishing | 65 | 35% |
| The brush | 23 | 12% |
| The near frame: pillars, mirror, dash, hood, wheel | 43 | 23% |

The subject — the glass and what happens on and through it — was reached at stroke 54:
29% of the strokes actually spent, 18% of the budget. The near frame went on last
because it is nearest, which is the same thing as spending the last third on the
surroundings.

Two masses were costed before the first stroke and redesigned on the number rather
than on the picture. The windscreen header priced at **40** as a `block_in` crossed
two ways across a thin full-width band; it was cut to strokes, and then cut entirely.
The steering wheel priced at **23** as a swept `ribbon`, because a curved mass pays for
the box its bend sweeps out; as a `stroke` along the same path it is 1.

## Rehearsing, and what it saved

Twenty-seven rehearsals, none of them charged. Everything below was found on a copy
of the canvas and thrown away before it cost anything:

- The first arch was **two horizontal bands** with a hard edge between them — the
  picture was a landscape. Rebuilt with an oblique boundary that also comes down the
  left of the glass.
- The first bloom was built from strokes radiating out of one centre. It came back as
  **a daisy**. Rebuilt as a `scumble` stepping across the mass, which is what a light
  broken up by soap actually looks like.
- Three `round_hard` marks laid on that scumble read as **pills**, then as **stickers**
  — a round tip needs about seven times its width before it stops reading as a capsule,
  and a clean-edged mark on a broken passage sits on top of it whatever its value. The
  bloom's core and the water were deferred to the glass pass so they would arrive as
  part of a family of marks rather than two lone ones.
- The first foam was five short starved bristle strokes and five `dab(press=3)`
  highlights. It came back as **a row of floating discs**, the exact failure the guide
  names. Foam on a moving windscreen is dragged, so it became five smears with length
  and a curve in them. Two more dabs were tried in the finishing pass and taken out
  for the same reason: at that scale a dab is a disc.
- The first frame was half again as big and came out as **stepped rectangles** — an
  oriented tip is held square to its travel, so a curved boundary laid in horizontal
  passes arrives as a staircase. `edge="clean"` fixed the staircase; shrinking
  everything and deleting the header fixed the letterbox.
- The instrument hood was first laid in `frame_lt` and came back as **a pale slab**.

Two things were found only after being committed, and both are recorded in the pass
that fixed them. Two smudges along the cowl dragged **finger-shaped lobes** of glass
down into the dash: the cowl slopes and the passes ran flat, so they crossed the
boundary rather than following it. That edge was lost with paint instead. And a `flat`
laid to knock back a stray patch left its **chisel end standing in the glass**; a
`round_soft` at the same place has no chisel and no axis.

## The value correction that was also a picture correction

`compare()` put the bloom `0.12` below plan after the block-in. The honest reading was
not arithmetic: the foam on the brush had become the brightest thing in the picture and
the eye went right, away from the light the picture is about. The fix was a
concentrated core — a second scumble grading `cyan_hi` to `foam` — and then the two
water streaks laid **again** over it, because the water is in front of the light and a
scumble laid on top had quietly put it behind. After that all five places were inside
`0.07`, measuring stopped, and no mark after it was made to move a number.

## What went right

- Back to front throughout. Every edge on the wheel, the mirror and the pillars is
  where their paint stops and the glass still shows.
- The wheel is three depths — the dash, the instrument hood inside its ring, then the
  rim — and one hard gloss streak along the upper left of the rim is the only mark on
  it. That single mark is what makes the whole wheel read; before it the wheel and the
  dash were one dark hump.
- The dashboard's reflection along the cowl does three jobs at once: it fills the
  quietest part of the glass, it ties the dash to the screen, and its lower half laps
  the cowl and loses the hard edge two smudges had made a mess of. `round_soft`
  airbrushes above `size 0.05`, which is wrong everywhere in this picture except the
  upward fade of a reflection.
- The stop light is a sideways smear with its core off the middle of it, and it bleeds
  down the wet glass, so it is part of the picture rather than a dot sitting in it.

## What still bothers me

- The six water sheets all lean the same way. That is what water on a raked screen
  does, and they vary in width, length and opacity, but it is the nearest thing in the
  picture to a repeated mark.
- The boundary between the arch light and the tunnel still runs close to horizontal
  across the middle of the canvas. Three marks were laid across it in `p9` and the
  stop light sits on it, which is what stops it reading as a waterline — but it is
  held rather than solved.
- The brush wanted rotation and got four splayed strips in the last pass. It reads as
  a spinning thing now; it did not before, and one more pass would have helped it.
- 115 strokes went unspent. Some of that is the rehearsals doing their job. Some of it
  is the brush.

## The signature

One mark, in the quiet dark of the cowl at the bottom right, a step lighter than what
it sits on: a liner stroke that starts inside the picture and runs off the edge of it.

It is that because the thing this session learned most concretely, and learned four
separate times, is that a mark which ends inside a picture leaves an edge nobody chose
— the chisel end of a flat, the capsule of a short round stroke, the disc of a dab.
A signature that exits the frame is the one mark in the picture that refuses to have
an end. It is not a name, it is not a title, and it repairs nothing.
