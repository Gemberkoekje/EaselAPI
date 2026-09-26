# The Bell-Warden: a stone figure that has to pass for a statue

Painted with `easel-paint` **0.7.0**, installed from PyPI by the painter itself — it
upgraded 0.5.0 to 0.7.0 before anything else — in a session of another of the owner's
projects, on the owner's Windows machine, as sample art for a content pack there. The
pack's details are left out of this filing at the owner's choice. The subject was set by
the pack and not chosen after reading, which is the lighthouse-greenhouse brief's case:
a stone gargoyle crouched on a plinth in a dark undercroft, lit warm from the upper left.
Before the first mark it read the package's README and three of its guide files, in part,
from the installed wheel: about 22,300 words printed, which it counted as about 20,000
(measured from its session, below). `PAINTING.md`, `CALIBRATION.md` and `DIAGNOSIS.md`
were not opened, and neither was the repository: it never saw `paintings/`. It ran
`easel demo mistakes` and all nine of `PAINTER.md`'s exercises in one script
([`ex/exercises.py`](ex/exercises.py)). **It is the first painting made against 0.7.0**,
and what it says about that release is read in [`PLAN-0.8.0.md`](../../../PLAN-0.8.0.md).

**To understand this, start by reading [`prelude.py`](prelude.py)** — the mixtures, the
room, the plinth's three planes, the 42-point silhouette and the planes the light finds on
it, and the `s.plan(...)` — then the passes **in the order they rebuild in**:
`p01_draw.py`, `p02_room.py`, `p03_plinth.py`, `p01_draw.py` again, then `p04_gargoyle.py`
to `p07_glow.py`. [`verdict.md`](verdict.md) is the painter's own review, written after the
export, and [`answers.md`](answers.md) is its answers to the questions put to it after the
filing ([`questions-step1.md`](questions-step1.md)), with the measurements it made for
them. [`reports.txt`](reports.txt) is every block `easel run` printed after a pass, as
the session file kept them — 27 of them, rehearsals included. [`versions/`](versions)
holds the first drawing and every version of the subject's pass and of the details pass
that was rehearsed and thrown away, recovered from the session's transcript and each
re-run here to the report it printed then. [`evidence/`](evidence) holds the seven
pictures the verdict's claims point at. The account under *The painter's notes* is the
painter's; everything else here is the filer's.

## The plan, as declared

Everything the guide asks a painter to write down went through `s.plan(...)` in the
prelude, before the first mark:

| declared | |
|---|---|
| why | *It has to pass for a statue: the stone must read as carved stone at first glance, and only the glint of its eye and the claws gripping the plinth's edge give it away.* |
| values | the head's top plane `0.66`; the plinth's top `0.54`, front `0.40` and side `0.27`; the glow on the wall behind the head `0.31`; the wall's upper right (`G1`–`H3`) and the floor `0.17` |
| lightest | the head's top plane (declared as `face_lit`, which the prelude sets to `head_top`) |
| subject share | `0.45` |
| ground | `"buried"` |

1024×768, linen, `umber_wash` ground (`0.43`), seed 11. **280 of a 300 budget**; 19
rehearsals, 18 of them saved with what their checks said (the nineteenth raised before it
laid a mark), none of them charged. At the end: the subject `170` of the 280 marks, `61%`
against the `45%` planned; `0.06%` bare ground, buried as declared; `0 of 17` masses in a
rectangle; `20` of 300 unspent.

## The passes

| File | What it is |
|---|---|
| `prelude.py` | runs before every pass: the mixtures, each mixed to the value it is planned at; the masses; the `s.plan(...)` |
| `p01_draw.py` | the drawing, as guides (free, never exported); run again after the plinth, when the creature was redrawn |
| `p02_room.py` | the room, back to front: the wall as one scumbled field, the glow behind the head as an inward scumble, the beam of lit air as three glazes, the floor and its light as two soft strokes, the pillar |
| `p03_plinth.py` | the plinth as a mass built of planes, a film aimed at a value down its front, the lip, a crack, dry brush, and the shadow it casts |
| `p04_gargoyle.py` | the creature's masses: the wing behind; then the whole silhouette in the light, and two copies of it shifted away from the light laid over it in mid and in shade, each held to its own outline and to the body |
| `p05_details.py` | the core shadow from a copy shifted further off, the head's lit plane and its horns, the maw, the eye's ember, the claws over the plinth's edge, the lights along the edges that face the lamp, and a film keeping the plinth's front under the head |
| `p06_finish.py` | dry brush across the stone, three carving seams, lost edges where the shade meets the wall, and a spark in the eye |
| `p07_glow.py` | four films mixed from the glow's own colour, laid to soften its rings |

## The painter's notes

What follows is the painter's own `NOTES.md` as it stood on 2026-09-26, after it answered
the questions and corrected two passages — verbatim but for its headings, which are set
here as bold lines, and where marked. The first filing quoted the version of 2026-09-25,
whose wet-paint passage the painter has since withdrawn.

> *[The painter's title, its picture, and a paragraph saying which pack the picture was
> made for and where its copy goes are left out here, at the owner's choice.]*
>
> _To understand this, start by reading `prelude.py` (the mixtures, the masses and the
> plan), then the passes in order, `p01_draw.py` to `p07_glow.py`. Painted 2026-09-25
> with Easel 0.7.0 (`easel-paint`), following its `PAINTER.md`; the nine exercises were
> done first._
>
> **Why this subject** (the `why=` in the plan): *it has to pass for a statue — the stone
> must read as carved stone at first glance, and only the glint of its eye and the claws
> gripping the plinth's edge give it away.* Both give-aways are in: one ember-orange eye,
> the only saturated colour in the picture, and three claws hooked over the plinth's front
> edge.
>
> | | |
> |---|---|
> | Canvas | 1024 × 768, linen, `umber_wash` ground (0.43), seed 11 |
> | Budget | 280 of 300 strokes; the subject 170 of them (62%, against 45% planned) |
> | Lightest | the head's top plane, as planned. The plan's measure, a mean, reads it at 0.52 because the eye sits inside the place; by its median it reads 0.61 |
> | Masses laid as rectangles | 0 of 17 |
> | Ground | buried, declared in the plan |
> | Reproducible | the log replays to the stroke. The pass scripts are the final versions: each was rehearsed, often several times, before it was run once |
>
> **What went wrong, and what fixed it**
>
> - **The first drawing was a box with a spiky blob on it.** The plinth was nearly as
>   wide as the creature, and the creature was a union of an ellipse, a circle and a thin
>   arm. Redrawn, twice, while it was still free.
> - **The first painted silhouette read as a cat.** Two symmetric wing peaks are ears.
>   The fix was the drawing, not the brush: a profile, facing the light, with one bat wing
>   raised behind — four fingers fanning from a clawed wrist, scallops between them.
> - **Lit planes laid as islands read as a piebald cow**, and a lit band wrapped round the
>   body read as an arch. Both were too much contrast inside one mass, laid as patches.
>   What worked was cutting the zones from the silhouette itself: the whole creature in
>   the light, then a copy shifted *away* from the light in mid, then a copy shifted
>   further in shade, each held to its own outline and to the body (`clip=body,
>   edge="hard"`). The lit rim then follows every edge that faces the lamp, the jaw and
>   the horn included, with nothing drawn by hand.
> - **The head's lit plane read 0.52, not the 0.64 it was mixed at.** I blamed wet paint
>   and added `s.dry()` before the lights. It changed nothing (measured 2026-09-26,
>   `answers.md`). The 0.52 is the plan's *mean* over a place with the dark eye inside it;
>   by its median the plane reads 0.61. Wet paint barely touched this painting: wetness
>   falls ×0.94 a stroke, so it only reaches a light laid within a few strokes of the paint
>   under it. That happened only on the claw lights, which lost 0.05 to it.
> - **A pillar laid as a gradient read as a tree trunk** (six passes are stripes). Solid
>   dark, then two soft films on its lit side, reads as round stone.
> - **Rings.** The inward scumble behind the head showed its rings like a target; four
>   soft films mixed from the glow's own colour softened them afterwards. A floor pool of
>   light laid the same way read as a rug and was replaced by two soft tapered strokes.
> - **A pencil smooths its path by default**, which turned the plinth into a pot in the
>   drawing check: `smooth=False` for straight-edged shapes.
>
> **What it still is**
>
> A low-key picture: the tool's `values:` line says so (nothing above 0.35 at the 95th
> percentile), and that is the design, not a fault. The creature's broad shade is still
> smoother than weathered stone — the dry brush and three carving seams only begin on it.
> That is the passage to spend strokes on if it is ever taken further.
>
> **The give-aways landed short** (measured 2026-09-26). The eye's spark, a `0.0028` dab,
> landed no paint, and `easel log` says *NO PAINT LANDED*. The ember dab under it, at
> `0.0068`, laid 1.6 units over five pixels. The eye's glint is the glaze laid over both.
> The claw lights, `0.0032` to `0.0035` strokes, reach about half their value step even on
> dry paint. Round marks this small do not lay their colour, so read `easel log` after a
> pass of small marks.
>
> *[A last section, the pack's catalogue entry for the picture, is left out for the same
> reason.]*

## What happened when it was filed

Everything under this heading is the filer's, not the painter's.

- **What was filed, and what was not.** The passes keep the painter's names, which are
  already the numbering the corpus probe reads, and take the repository's line endings.
  The session file (`bell.easel`, 6.1 MB) is not committed — `*.easel` never is — so its
  27 saved reports are written out as [`reports.txt`](reports.txt), which is `easel log
  bell.easel --reports`. The export and the time-lapse are `painting.png` and
  `painting.gif`. The pack's WebP copy is not filed, and neither is the painter's account
  of the pack. Of the 39 looks and rehearsal pictures, seven are under
  [`evidence/`](evidence), renamed: `drawing_first.png` (the first drawing, guides on the
  bare ground), `drawing_over_paint.png` (the second, over the painted room — the guides
  are nearly gone), `drawing_check_smooth.png` and `drawing_check_corners.png` (that
  drawing in pencil on a throwaway light canvas, with the spline and with
  `smooth=False`), and `subject_cat.png`, `subject_piebald.png` and `subject_arch.png`
  (the subject's pass as it was rehearsed the first three times).
- **Rebuilt here, pass by pass, through `easel run`**, on the checkout at `v0.7.0`: the
  same 292 records, 280 spent, every record's geometry, dab count, brush and colour as
  the painter's file has them, and an export identical to the painter's PNG to the pixel
  — this is the machine it was painted on. **Only in the order the saved reports
  record**: the drawing, the room, the plinth, the drawing again, then the rest. The
  second drawing lays the `erase all` that is record 96, and a record's texture is seeded
  from its index, so in numbered order the same 280 marks land one index early from the
  subject's pass on, and 97,126 of 786,432 pixels (12.4%) move, by up to 87 levels. So
  the painter's *the log replays to the stroke* is right, and its *each was run once* is
  right of every pass but the drawing, which ran three times: twice before the room — the
  second time adding the `s.erase()` that is record 0 — and once after the plinth, when
  the creature was redrawn. To rebuild: `easel new bell.easel --size 1024x768 --texture
  linen --ground umber_wash --seed 11 --budget 300` in this directory (it leaves
  `prelude.py` alone), then `easel run bell.easel p01_draw.py p02_room.py p03_plinth.py
  p01_draw.py p04_gargoyle.py p05_details.py p06_finish.py p07_glow.py`, then `easel
  export bell.easel rebuilt.png` — about a minute. The passes write their looks into
  `looks/`.
- **What the tool said, pass by pass**, from the saved reports. At the call:
  `plan-pairs` at the drawing, before a mark — the plinth's side and the floor `0.03`
  apart, its top and front `0.10`; `solid-comb`, `scumble-dabs` and `inward-comb` on the
  room's rehearsals, the last on the floor's pool — twelve rings on a patch `0.066` deep,
  told to drop to eight; the pool was later replaced by two strokes — and `scumble-dabs`
  on the committed room as well; `clean-small` and `glaze-far` on the plinth's
  rehearsals, the film down its front having moved what it covered by `0.112`, which
  `to_value=` answered; and `glaze-far` on every version of the details pass, on the film
  over the eye, mixed `0.164` and then `0.100` off what it landed on in hue and chroma.
  After the pass: the stack-of-bars line four times, all on rehearsals and never on a
  committed pass — the room's first two rehearsals (12 of 19, then 12 of 20 long marks
  within 6° of vertical), the plinth's first (22 of 29 within 6° of horizontal) and the
  subject's fifth version (63 of 101 within 6° of 48°); the small-comb line on the room's
  second and third rehearsals, and the early-detail line on its second; and the one-disc
  line on every version of the details pass, at 11, 6, 6 and 4 small round marks, the
  last four committed. The standing lines: `values:` *no clear light* on every report from the
  first mark on, 25 of 27; `lightest:` naming the plinth's top until the subject's pass,
  then the head's top at `0.46` and, from the details pass on, `0.52`; `plan:` *6 of 7
  places inside 0.10; head top -0.14* at the end; `edges:` `36%` under 2.5 px after the
  room, `46%` after the plinth, `61%` after the subject and `48%` at the end; `subject:`
  ahead of its planned share after every pass it was painted in, `53%` to `65%`.
- **The verdict's measured claims, re-measured** — in full in `PLAN-0.8.0.md`, section 3.
  **Confirmed:** the guides vanish over dark paint (a guide is a one-pixel line of value
  `0.23` at 75% alpha; over the finished canvas 69% of its pixels step the value by less
  than `0.05`, on the bare ground none do); the pencil's spline rounds a closed outline,
  and a shape cannot be handed to `pencil()` or `guide()` at all; the subject's pass
  rehearsed at 85 to 113 marks, and the log can say which calls laid them (four
  `block_in`s laid 79 of the committed 102); *no clear light* on 25 of 27 reports; the
  head's top reads `0.524` by its mean and `0.606` by its median, with 14% of its pixels
  under `0.35`; the post-pass paragraph is 678 words. **Changed shape:** the highlights
  *at 0.52 instead of 0.64 until I added dry()* — the session shows the head's top
  reading `0.52` before the two `s.dry()` calls were added and `0.52` after them, on the
  details pass's second and third rehearsals ([`versions/p05_v2.py`](versions/p05_v2.py)
  and [`p05_v3.py`](versions/p05_v3.py)). The `0.64` is the value the plane was mixed
  at, the `0.52` is what the plan's line reads for the plane with the eye inside it, and
  at the time the painter put the reading down to the eye itself. Asked, it withdrew the
  warning it had suggested, as written, and corrected its notes. The feather: `REFERENCE.md`'s
  paragraph on holds and its arguments table both say what `feather=` does — break a held
  edge inward against the tooth — and both were in what the painter read; benched on its
  own pass, a feather speckles rather than softens. The floor: `0.13` is inside the box —
  burnt umber alone reads `0.128` — and the `0.14` it met was `at_value`'s default dark.
- **Found while filing, not by the painter.** *A union of parts came first:* the first
  drawing's creature was `union(head, muzzle, torso, near_wing, far_wing, haunch,
  hind_foot, arm)`, eight ellipses and ribbons, which read as a spiky blob beside a plinth
  nearly as wide ([`evidence/drawing_first.png`](evidence/drawing_first.png)); the next
  two drawings were typed polygons, of 32 points and then 42. *The spark is not in the
  picture:* `p06_finish.py`'s last mark, a `round_hard` dab at `0.0028` — three pixels
  across — changed two pixels, by at most 21 levels of 255. `easel log` lists it as *NO
  PAINT LANDED*, and nothing at the call said so. ~~The glint in the picture is the ember
  under it, at `0.0068`, seven pixels.~~ *Corrected by the painter's answers, and
  re-measured: the ember dab under it laid `1.62` units and moved five pixels by more
  than `0.02`, by at most 22 levels, to a dull `0.22`; the glint in the picture is the
  glaze laid over both, `133` units over hundreds of pixels.* *What it read*, from the session's transcript: the
  README's first 400 lines of 417 (4,295 words); `PAINTER.md` to line 700 of 754 (6,260
  of its 6,655 words — *Sign it* and *Working from a shell instead* went unread, and the
  painting is unsigned); `REFERENCE.md` to line 520 of 723 (6,266 of 8,904 words: the
  units table, the verbs, the arguments, the shapes and *Looking, planning, measuring*,
  but not the notices, the shell or the server); and the list of `RECIPES.md`'s headings
  and seven parts of it (4,441 of 7,823 words), which leave out *A scene with straight
  edges*, the one recipe that draws a closed outline with `smooth=False`. It never ran
  `--count`, `cost()`, `cost_line()`, `--alternatives`, `explain`, `diagnose`,
  `preview()` or `compare()`.
- **What its answers found, re-measured here.** Asked after the filing
  ([`answers.md`](answers.md)), the painter measured its own file again and found two
  more things, and both hold. **Thirteen of its 280 strokes laid under one unit of
  paint**: the spark, and twelve passes of three clipped `block_in`s — 2 of the 23 at
  `p04_gargoyle.py:40`, 6 of the 24 at `p05_details.py:12` and 4 of the 17 at
  `p05_details.py:14` — eleven of them laying `0.00` and one `0.11`: paid for and laying
  nothing, passes of a shifted copy that fall outside the body they are held to, by the
  painter's reading. And **wet paint cost the claw lights little and their size a great
  deal**: laid again on paint dried first, they land `0.01` to `0.05` higher, depending on
  how the moved pixels are read, and still `0.27` to `0.31` short of their own `0.60`. Its
  place readings hold to the hundredth: at the finish the floor's 90th percentile reads
  `0.286` against its planned `0.17`, because the lamp's pool lies in it, and the share of
  a place more than `0.15` from its own median is `18%` for the plinth's top and `24%` for
  the head's top, and under `8%` everywhere else at every pass end.
- **Its nouns, for the guide's grep** — which `LESSONS.md` describes as a check run by
  hand, with no committed list: *gargoyle*, *statue*, *plinth*, *wing*, *horn*, *claw*,
  *ember*, *eye* (of a creature), *pillar*, *undercroft*, *nave*, *chapel*, *bell*,
  *stone*, *creature*, *bat*. Grepped when it was filed, the five guide files hold none
  of them in this painting's sense but one: `RECIPES.md`'s *A tapered arc* calls a
  crescent's two points *the horns*, a sentence older than the painting.
- **The model was `claude-opus-5-5` at max effort**, by the session's own metadata, on
  every turn of it. It worked on Windows under Python 3.14, without `pymixbox`.
