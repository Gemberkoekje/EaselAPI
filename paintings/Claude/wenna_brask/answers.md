# Answers to the questions after filing

*From the painter, 2026-09-26. Each **M** was measured today on Easel 0.7.0: from `wenna.easel`,
the painting's own session file, loaded with `Session.load` and read through `look(values=True)`
and `easel log`; from the committed pass scripts; or from probes on throwaway copies
(`s.scratch()`) and on one scratch session. Each **O** is what my session's transcript shows I
did or saw at the time, with its timestamp (UTC, 2026-09-26). Each **R** is reasoning. The three
probes are in [`probes/`](probes): `light_stats.py` for question E, `flour_probe.py` for the
flour, and `lettering_probe.py` with its two sheets for question D. Each runs from that folder
against `../wenna.easel`.*

## What answering found

Five things. Four of them correct my own verdict or notes.

- **The flour never landed.** `easel log` shows 11 of the 262 charged strokes laid no paint
  (**M**):
  - all eight flour strokes: records 193, 219, 220 and 258 to 262;
  - the nostril's dab (173), the catchlight (237) and the flame's core (240).

  One more mark laid next to nothing: the far eye's iris (167), a `round_hard` dab at 0.006,
  laid 2 units. The near iris, a dab at 0.009, laid 40 (**M**). So every round dab of mine
  under 0.007 laid between 0 and 2 units, which matches the Bell-Warden's ember at 0.0068.

  The why names her floury hands, and the picture has no flour on it. At 09:40:38, looking at the
  flour pass's rehearsal, I wrote *the flour is faint but there*, in the same message that said
  *the edge's brush passes read like a knitted hem* (**O**). What I took for flour was those
  passes (**R**). Nothing said so at the call or after the pass: none of the 32 saved reports
  mentions a mark that laid nothing (**M**, `reports.txt`).
- **Why it landed nothing.** I laid the flour finger stroke (record 258) again on copies of the
  finished canvas, changing only the load. A small bristle lays no paint at a load of 0.22 and a
  trace at 0.35; from 0.5 up it lays paint (**M**):

| Load | Paint laid at size 0.012 | Paint laid at size 0.03 |
|---|---|---|
| 0.22 | none | none |
| 0.35 | 1 | 4 |
| 0.5 | 9 | 72 |
| 0.7 | 58 | 416 |
| 0.9 | 133 | 734 |

  My flour was laid at loads of 0.12 to 0.25. I had learned "starved" from exercise 3, where a
  load of 0.2 laid flecks, but at size 0.07 on rough canvas (**O**). The Bell-Warden's painter
  asked for a fact at the call for any mark that lands far short of its own value. This is a
  second case for it: 4% of the strokes, and every mark of the flour the why names (**R**).
- **The face is the lightest mass, not the lantern.** It is lighter by every reading, as the
  table under question E shows (**M**). My notes' *Lightest: the lantern, as planned* was true
  only of the five places I planned, and the face was not one of them (**O**). The flame was
  mixed at 0.93, yet the brightest pixel in the lantern's place reads 0.714, and the flame's
  core dab (240) landed nothing (**M**).
- **I did not break the upstream rule on the fist.** The transcript shows two moves, each made
  at the second failure (**O**):
  - At 09:34:01, after the disc (the figure pass) and the disc with knuckles (the cloth pass's
    rehearsal): *the fist has failed twice, pointing to a drawing issue rather than shading.
    I'll redraw it.*
  - At 09:38:05 the redrawn fist *still resembles a bread roll*. At 09:39:21, after the cup:
    *Third failure of one passage, so the idea changed, not the brush.*

  My verdict's *I broke that rule on the fist with the rule in front of me* is wrong. The record
  shows a move upstream that did not go far enough: the redraw kept the view, a fist from the
  front, and changed only its outline (**R**).
- **The fist was not too large.** The redrawn fist is 132 px across and the face 253 px from
  the kerchief's hem to the chin: 0.52 (**M**). A fist is about half a face's height, from
  ordinary proportions I have not measured (**R**). So my notes' *half again too large for her
  face* was a figure I eyeballed and never checked (**O**). The fault was the view, not the size
  (**R**).
- **The filing's two half-rights are both right.**
  - `cost()`: my scripts call it nowhere (**M**). The card prices a plan, and every pass I wrote
    was a set of functions (**O**), so it never reached the way I worked (**R**).
  - The four fingers: my fist was not a hand cupped toward the viewer but a fist seen from the
    front. The principle about the view does not reach it (**R**).

## Question A: drawing in pixels

**Yes, and it would have replaced `P()` for every point. On this canvas I would not have used
`s.px(r)`, and it has a trap: as a fraction of the long side it is the unit of a `size`, not of
a shape's radius.**

- **`P()` appears 358 times in the scripts**, 318 of them as literal points inside the passes
  (**M**). It hard-codes 768 and 1024 (**O**, `prelude.py`); `s.px` would read the session's
  own size.
- **Why I wrote it**, at 09:08:53, in the prelude's docstring (**O**): *Drawn in pixels … because
  a face is judged in proportions and pixels keep them honest.*
- **Lengths.** The passes set 45 sizes under 0.01, from 0.0025 to 0.009 (**M**). On a canvas
  whose long side is 1024, a size fraction already reads as pixels (0.005 is five), so I never
  converted one (**O**). On a canvas 768 or 1400 px long it would matter (**R**).
- **The trap.** `ellipse` and `blob` take one radius per axis in coordinate units, and
  `s.circle(r)` takes a fraction of the width (**M**, from the docstrings in `regions.py` and
  `session.py`). So on my canvas, `blob(p, s.px(25), s.px(25))` comes out 19 px across and 25 px
  tall: an oval (**M**, by arithmetic). My first fist was a blob whose two radii I worked out per
  axis by hand (**O**, `prelude_draw1.py`). Either the helper says in its name or its first line
  that `r` is a size, or shapes take pixels themselves, for example `s.circle(p, px=25)`
  (**R**).
- **`Session(units="px")`**: I agree it should not be built. It would make every recipe's
  numbers wrong for the painter who set it (**R**).

## Question B: a group moved as one

**Yes. My `T()` is one scale, by 1.3 about the pixel (300, 266), with no move needed. But the
group is not where my time went. The 32 coordinate pairs I worked out through `T()` and typed
by hand came from building new shapes along the scaled outline, and the shape's own points would
have given me those.**

- **One scale.** `T(x, y) = (300 + 1.3(x − 300), 146 + 1.3(y − 146) − 36)` is exactly a scale by
  1.3 about (300, 266), the old head's middle, halfway between its crown and its chin (**M**, by
  algebra). So `.scaled(1.3, about=s.px(300, 266))` would have been all of it.
- **The hand-typed pairs.** There are 32 decimal pairs in `prelude.py` that are `T()`'s outputs,
  typed by hand (**M**): the roughened kerchief, its lit crescent, and the face's lit plane,
  whose right side is the profile. I typed them because the planes share an edge with the face.
  `polygon(face.closed[i:j] + terminator)` would have taken that edge from the face itself
  (**R**). The recipes do this for a smudge, `mass.closed[3:5]`, and I did not think of it for a
  plane (**O**). One sentence in *A mass built of planes* would carry it (**R**).
- **Nothing else was moved together after the rescale** (**O**).
  - The lantern was redesigned, not moved: held first, then hung from a bracket.
  - The redrawn fist was defined in a pass, not the prelude, so its polygon is typed out three
    times, in `p07`, `p08` and `p10` (**M**). That is a sharing problem, not a group one.
- **Where a group would bite next.** The passes hold 318 literal pixel points, 74 of them in the
  face's pass (**M**). If the head had moved after that pass, a group of shapes would not have
  moved those marks; a frame, local coordinates for drawing features in, would have (**R**). I
  would still build the group as proposed and not the frame. A frame is a second coordinate
  system in every script, and my painting did not need one (**R**).

## Question C: a finding that names its marks

**The script line, with its function. The note would not have found them, and the log index
only by way of the log.**

- **The four marks** are records 174, 176, 177 and 179 (**M**, `easel log` matched to the
  script):
  - 174: the upper lip's shade, in `lay_mouth`;
  - 176: the lower lip's light, in `lay_mouth`;
  - 177: the chin's notch, in `lay_mouth`;
  - 179: the fold from the nose, in `lay_modelling`.
- **The note.** 184 of the 262 marks carry `subject`, all four of these among them (**M**). The
  note cannot tell them apart.
- **The log index.** The log line reads `#174 stroke round_soft #9e6c57 41 dabs 269 paint --
  subject` (**M**). It gives a hex colour where my palette says `lip`. Printing the palette
  slot's name would make the log readable on its own (**R**).
- **What I would have opened** is `p05_face.py:58 (lay_mouth)` (**R**). The function is the
  name I think in: every pass was a set of functions named for what they lay (**O**).
- **Would it have found them? Yes. Would I have changed them? Probably not.** They read as lips
  in every look (**O**), and a lip's highlight is a short round mark (**R**). The finding is
  still worth naming its marks: it lets the painter decide instead of search.

## Question D: lettering

**Two of the pictures in my list need writing:**
- **a short note in a hand:** one to three lines, twelve words at most, about fifty letters;
- **a sketch map:** four to six labels of one word each, and an X.

**Capitals 32 px tall read at the size the table app shows a handout, and a hand wants more
than that. And the recipe has to bring its font with it, because the letters I typed myself
went wrong.**

- **What, and in what** (**O**, from my list of pictures). The note is cramped ink, in a hand.
  The labels are charcoal, in a hand. My list asks for nothing else written. A third picture
  could carry a maker's stamp of a few characters, and that would be type, because it is stamped
  (**R**).
- **The size** (**M**). The app draws a picture at its default size no larger than 42% of the
  screen's width and 56% of its height. On a 1080p projector that shows a 768 × 1024 handout at
  0.59 of its size, and a 1024 × 768 sketch at 0.79.
- **The probe** (**M**, with the reading **O**). On a scratch session with a vellum-coloured
  ground, I laid "OWED 40 GP" six ways: pencil at 32 and 56 px; the liner at 0.003, at 32 and
  56 px; `round_hard` at 0.005 at 56 px and at 0.008 at 80 px. I read each at full size and at
  604 px on the long side.
  - Every row reads at that size. The 32-px pencil reads faintly.
  - All 48 charged strokes landed.
  - A row of eight characters took 12 strokes, 1.5 a letter. So a fifty-letter note is about 75
    strokes, a quarter of a 300 budget. The pencil costs nothing but reads grey.
- **Hand or type.** The probe's letters read as type: an even line, a level baseline, every
  letter alike (**O**). Easel's own wander does not make them a hand. A hand needs a slant, a
  baseline that drifts, pressure through each stroke, and no two a's alike (**R**).
- **The recipe needs the font as data.** My G came out as a ∂, because I ran its arc the wrong
  way round (**O**). Paths a painter types glyph by glyph will go wrong like that (**R**). So ship
  a single-stroke font as data, with a helper that returns its paths placed, slanted and varied:
  something like `letter_paths(text, place, cap=, slant=, seed=)`. The painter then lays them
  with `s.stroke` or `s.pencil`. That is a helper that returns paths, the way `ribbon` returns a
  shape, not a verb that lays paint. It keeps the recipe's promise and removes the part I got
  wrong (**R**).

## Question E: a small light

**Neither reading would have helped me, because my plan was wrong. The face is the lightest
thing in the picture by every reading, and it should be. I would rather have planned the panes
as a place of their own, at the value I actually painted them, and planned the face too. If
`lightest:` reads a light by its brightest part, make that a high percentile and print it beside
the whole.**

- **The readings** (**M**), through the values view at 8 bits. The lantern's mean comes out
  0.005 under the filing's 0.491. Its median, 90th percentile and brightest pixel agree with the
  filing.

| Place | Pixels | Mean | Median | 90th | 95th | 99th | Brightest |
|---|---|---|---|---|---|---|---|
| the lantern, as planned | 9,073 | 0.486 | 0.506 | 0.580 | 0.588 | 0.639 | 0.714 |
| its panes, inside the edge straps | 7,244 | 0.525 | 0.522 | 0.580 | 0.592 | 0.643 | 0.714 |
| the panes' middle third | 1,775 | 0.577 | 0.573 | 0.624 | 0.639 | 0.655 | 0.714 |
| the face, whole | 26,094 | 0.505 | 0.584 | 0.620 | 0.620 | 0.639 | 0.718 |
| the fist, as redrawn | 10,944 | 0.302 | 0.267 | 0.443 | 0.447 | 0.573 | 0.690 |

- **The brightest part would not have rescued the lantern** (**M**). The face still beats it:
  0.62 against 0.58 at the 90th percentile, 0.62 against 0.59 at the 95th, a tie at the 99th,
  and 0.718 against 0.714 at the brightest pixel.
- **My 0.76 was a mixture's value, not a place's.** I painted the panes on a 0.58 base with a
  brighter middle (**O**, `p04_lantern.py`). The panes' middle third reads 0.58 by its mean and
  0.64 at the 95th percentile, which is about what I should have planned (**M**).
- **I did not plan the face**, the subject of the why (**O**, the plan's five places). Planned at
  its lit plane's 0.64, `lightest:` would have named the face (**R**). That is what the why asks
  for: *the lantern finds her face*.
- **If it is built** (**R**):
  - Read the named light at the 95th percentile inside its place, not by its brightest pixel. A
    stray highlight is one pixel, and on my canvas that pixel was the face's.
  - Print both numbers on the line: *lantern 0.49 as a place, 0.59 at its brightest twentieth*.
- **The flame** reads 0.71 against the 0.93 it was mixed at (**M**). A fact at the call for a
  mark that lands short would have told me the lamp's brightest mark never arrived (**R**).

## Question F: a place laid over again and again

**Count masses laid over the painter's own subject marks in one place, rehearsals included,
and speak at the second. On my painting that singles out the fist. But it would have spoken
exactly when the rule did, so it would not have stopped me, and my painting gives no reason to
build it.**

- **Passes do not tell the two apart** (**M**). Five passes laid marks in the fist's place, but
  only four laid paint there (`p03`, `p07`, `p08`, `p09`), because `p10`'s flour landed nothing.
  The face also has four: `p03`, `p05`, `p08` and `p11`.
- **Masses laid over earlier subject marks do** (**M**).
  - The fist has two: `p07`, the fist redrawn, and `p09`, the shawl's edge brought over it.
  - No other place has one after its first masses. After `p03` the face got strokes, dabs and a
    single glaze: `p05`, `p08` and `p11` hold no `block_in`. The one `block_in` left in `p06`
    is never run.
  - Counting rehearsals as well, the fist's masses were: the cloth pass's rehearsal, `p07`, the
    first `p09` rehearsal, then `p09`. The second of them is `p07`.
- **When it would have spoken:** at `p07`, the redraw, which I had already decided on at
  09:34:01 (**O**). It would have added a number to what the rule said, at the same moment.
- **What failed was how far the move went, not the move** (**O**, **R**). My first move
  upstream redrew the fist's outline in the same view. A recipe for a hand closed on something
  would have handed me the third answer first. The rolled edge that worked cost 12 strokes
  (**M**, `p09`'s report).
- **So: build it as a fact only if the corpus separates.** My painting is one case for counting
  masses over subject marks and none for counting passes (**R**).

## Question G: the budget and the card

**It would have changed the number I typed, not the painting. I typed 300 without a thought,
and the painting ended with 38 strokes unspent, so I withdraw *450 would have suited it*. Most
of what I leaned on is not on the card.**

- **I did not choose 300** (**O**, transcript). At 09:08:25 I ran `easel new … --budget 300`,
  and nothing before it mentions the budget. 300 was in the card's example (`PAINTER.md` line
  41), in its shell section (line 735), and in my memory of the first painting (280 of 300).
- **The budget never bound** (**M**, **O**). I spent 262, left 38, and stopped on the passage,
  not the count. Its one effect was the figure's rehearsal coming back at 135 strokes, at
  09:24:32, which made me redesign the face's planes. That was a good effect (**R**).
- **The clause is still right to add** (**R**). It is for painters who do run out, and it would
  have put a decision where I had none.
- **The calls my painting leaned on** (**M**, counted in the text of the committed prelude and
  the eleven passes, including the two functions `p06` defines and never runs):

| Call or argument | Uses | | Call or argument | Uses |
|---|---|---|---|---|
| `opacity=` | 97 | | `s.look` | 25 |
| `pressure=` | 86 | | `load=` | 23 |
| `s.stroke` | 84 | | `direction=` | 23 |
| `p.at_value` | 54 | | `p.mix_many` | 22 |
| `note=` | 51 | | `s.block_in`, `edge=`, `solid=True` | 21 each |
| `clip=` | 41 | | `s.dry` | 17 |
| `p.mix` | 40 | | `s.glaze` / `s.dab` | 7 / 5 |
| `tip_wobble=` | 31 | | `polygon` (through my helper), `blob`, `roughen` | 30, 1, 1 |

  From the shell I used `easel new`; `easel run --rehearse`, 25 times; `easel run`, 11 times;
  and `easel check`, `easel export` and `easel timelapse`.
- **The card** (`PAINTER.md` lines 31–143) names none of `at_value`, `clip=`, `pressure`,
  `opacity`, `sample`, `mix_many` or `note=` (**M**). `clip=` appears nowhere in `PAINTER.md`
  at all (**M**).
- **My twenty, for a first page** (**R**):
  1. `s.stroke`
  2. `s.block_in`, with `solid=`, `direction=` and `edge="hard"`
  3. `clip=`
  4. `s.glaze`
  5. `s.dab`, and the fact that a round dab under about 0.007 lands next to nothing (mine at
     0.0025 to 0.006 laid 0 to 2 units; at 0.009 one laid 40)
  6. `s.dry`
  7. `pressure=`, named and as a list
  8. `opacity=`
  9. `load=`, and the fact that a small bristle under about 0.5 lays nothing
  10. `tip_wobble=`
  11. `note=`
  12. `p.at_value`
  13. `p.mix` and `p.mix_many`
  14. `p.value_of`
  15. `polygon`, `blob` and `roughen`, with slices of `.closed`
  16. `s.look`, with `values=` and `region=`
  17. `s.sample`
  18. `s.plan`, with `why=`, `values=`, `lightest=` and `ground=`
  19. `easel run --rehearse`
  20. `easel log`, for what landed nothing, and `easel check`
- **Never used in the painting** (**M**): `s.smudge`, `s.cover`, `s.sweep`, `s.cost`,
  `s.preview`, `s.rehearse_each`, `s.compare` and `s.pencil`. The drawing was `s.guide` and
  `s.erase` on a scratch canvas, and `s.pencil` ran only in the exercises and today's lettering
  probe. Two I would use next time (**R**): `s.cost` before a mass, and `rehearse_each` for
  something like the glow.

---

*Corrected on my side today: the painting's notes in my own folder, and my memory of the
painting. I have not touched the repository.*
