# Wenna Brask: a mother who has not slept, by a lantern at dusk

Painted with `easel-paint` **0.7.0** on 2026-09-26, the morning after the Bell-Warden, by a
**second session** in the same project of the owner's — `claude-opus-5-5` at max effort —
as sample art for the same content pack, whose details are left out of this filing at the
owner's choice. Asked by the owner to choose the pack's pictures, it wrote a list of them
first, and then painted the first. The subject was set by that list and the pack rather
than chosen after reading the guide. **It is not a fresh painter.** It began with the first
painter's memory note, which carried the Bell-Warden's lessons — the shifted copies that lit
the gargoyle, `s.dry()` before highlights, `smooth=False` for straight edges, and drawings
judged on a light scratch canvas because guides vanish on a dark one — and it read the
Bell-Warden's notes, its prelude and six of its passes before painting. Then it read
`PAINTER.md` whole, did the nine exercises and a swatch strip of its own mixtures, and read
`RECIPES.md` whole and `REFERENCE.md` to line 500: about 20,500 words of the guide, which it
counted as *over 2,000 lines*. It never opened `PAINTING.md`, `CALIBRATION.md` or
`DIAGNOSIS.md`, or the repository. What it says about 0.7.0 is read in
[`PLAN-0.8.0.md`](../../../PLAN-0.8.0.md), beside the Bell-Warden's.

**To understand this, start by reading [`prelude.py`](prelude.py)** — the mixtures, the
drawing in pixels through `P()` and `T()`, and the `s.plan(...)` — then `p02_setting.py` to
`p12_crown.py` in order. **`p01_draw.py` is not part of the rebuild**: the drawing was
judged on a scratch canvas with a light ground, and never run on this painting's own
session. [`verdict.md`](verdict.md) is the painter's own review, written after the export,
and [`answers.md`](answers.md) its answers to the questions put to it after the filing
([`questions-step1.md`](questions-step1.md)), measured with the three scripts in
[`probes/`](probes) — each run from that folder against the painting's session file one
level up, which is rebuilt as below.
[`reports.txt`](reports.txt) is every block `easel run` printed after a pass, as the
session file kept them — 32, rehearsals included. [`versions/`](versions/README.md) holds
the first drawing and the versions of five passes that were rehearsed and thrown away,
recovered from the session's transcript and each re-run here to the report it printed
then. [`evidence/`](evidence) holds nine of its pictures. The account under *The painter's
notes* is the painter's; everything else here is the filer's.

## The plan, as declared

| declared | |
|---|---|
| why | *She has to read as a mother who has not slept: the lantern finds her face and her floury hands, and everything else is dusk.* |
| values | the lantern `0.76`; the sky high at the left (`A1`–`B2`) `0.29` and low (`A4`) `0.43`; the wall (`H5`) `0.145`; the shawl (`B7`) `0.16` |
| lightest | the lantern |
| subject share | `0.45` |
| ground | `"buried"` — declared by the eighth pass, `s.plan(ground="buried")`, not the prelude |

768×1024, linen, `umber_wash` ground, seed 23. **262 of a 300 budget**, plus two signature
marks that did not count; 25 rehearsals, 20 of them saved with what their checks said (five
raised), none of them charged. At the end: the subject `184` of the 262 marks, `70%`
against the `45%` planned; `0.06%` bare ground, buried as declared; `0 of 22` masses in a
rectangle; `38` of 300 unspent; `plan:` *4 of 5 places inside 0.10; lantern -0.27*.

## The passes

| File | What it is |
|---|---|
| `prelude.py` | runs before every pass: the mixtures; the drawing, in pixels on the 768×1024 canvas and converted by `P()`, the head drawn at a smaller size first and scaled up by `T()`; the `s.plan(...)` |
| `p01_draw.py` | the drawing, as guides — run only on the scratch canvas, three times; not part of the rebuild |
| `p02_setting.py` | the setting, back to front: the dusk sky, the mill's gable wall, the lantern's light on the wall as three soft strokes |
| `p03_figure.py` | her masses, back to front — the neck, the shawl, the knot, the kerchief, the face, the fist — each in its shadow colour, with its lit planes laid on it as shapes drawn with the silhouette |
| `p04_lantern.py` | the lantern: the bracket and ring, the horn panes lit from inside, the flame, the iron straps, cap and base, and the light it throws into the air |
| `p05_face.py` | the face: the sockets and eyes, the brows, the nose's shadow and the one it throws, the mouth, the jaw |
| `p06_hand_cloth.py` | the hand and the cloth: the shawl bunched in the fist, the folds fading away from the lamp, the sky's cool light on the shoulder and the kerchief |
| `p07_fist.py` | the fist, redrawn as four finger segments with the thumb across them |
| `p08_finish.py` | the last third: the fist taken down into the dark it sits in, the shawl's drape, and the ground declared buried |
| `p09_cloth_in_hand.py` | the shawl's rolled edge brought up over the fist, the fingers curled over it |
| `p10_flour_and_folds.py` | flour on the fingers and on the shawl, and light on the folds |
| `p11_last.py` | the why read back: the upper lids brought down, the lower left of the shawl into the dusk, and the signature |
| `p12_crown.py` | the kerchief's crown cooled with a film of the sky |
| `swatches.py`, `exercises/exercises.py` | the swatch strip of this painting's own mixtures, and the nine exercises, each on a throwaway session |

## The painter's notes

What follows is the painter's own `NOTES.md` as it stood on 2026-09-26, after it answered
the questions and added a section of corrections at its end — verbatim but for its
headings, which are set here as bold lines, and where marked.

> *[The painter's title, its picture, and a paragraph saying where the picture sits in the
> pack's list, who she is in the pack, and where its copy goes are left out here, at the
> owner's choice.]*
>
> _To understand this, start by reading `prelude.py` (the mixtures, the drawing in pixels,
> the plan), then the passes in order, `p01_draw.py` to `p12_crown.py`; each pass's
> docstring says what the one before it got wrong. Painted 2026-09-26 with Easel 0.7.0
> (`easel-paint`), following its `PAINTER.md`. The nine exercises and a swatch strip of this
> painting's own mixtures were done first (`exercises/`, `swatches.py`)._
>
> **Why this subject** (the `why=` in the plan): *she has to read as a mother who has not
> slept: the lantern finds her face and her floury hands, and everything else is dusk.* The
> face and the hand are the only lit skin, the lamp the only light, and the lids came down
> over her eyes in the last pass because the first version of her looked alert.
>
> | | |
> |---|---|
> | Canvas | 768 × 1024, linen, `umber_wash` ground, seed 23 |
> | Budget | 262 of 300 strokes; the subject 183 of them (70%, against 45% planned: the sky and the wall were cheap) |
> | Lightest | the lantern, as planned |
> | Masses laid as rectangles | 0 of 22 |
> | Ground | buried, declared in the plan |
> | Reproducible | the log replays to the stroke. The pass scripts are the final versions; each was rehearsed, most several times, before it ran once |
>
> **Changes from the brief**
>
> - **The lantern hangs from an iron bracket** on the wall instead of being held up. The
>   first drawing had her arm raised with the elbow out, and the forearm read as sticks;
>   the bracket frees both the arm and the composition.
> - **One hand, at her throat,** clutching the shawl shut, instead of the lantern hand. It
>   is the worried gesture, and it keeps "floury hands" in the picture.
>
> **What went wrong, and what fixed it**
>
> - **The Bell-Warden's trick does not paint a face.** Copies of the silhouette moved away
>   from the light, each held to the mass, lit the gargoyle. On a face turned toward the
>   light, a horizontal shift of a jagged profile stacks copies of the profile inside it:
>   three profiles, like cut paper, and on the kerchief a striped helmet. What worked is *A
>   mass built of planes*: the shadow mass first, then a half-tone band and a lit plane drawn
>   as polygons with the silhouette, sharing one edge, the terminator.
> - **Where the terminator goes.** The first planes put the light in a strip 30 px wide
>   along the profile. A head turned toward a lamp lights its whole front plane, which is
>   more than half of the face you can see in a three-quarter view. Moving the terminator
>   back past the near eye's outer corner turned a stripe into a face.
> - **The fist failed three times,** each time answered with the brush: a disc, then a bun,
>   then a bun in a dark cup with a lid. The drawing was the fault. A fist seen from the
>   front at this size is an oval, and this one was half again too large for her face. What
>   worked was a different idea: the shawl's rolled edge comes up over the lower half of the
>   fist, and the fingers curl over it, like a hand gripping a blanket's edge. That also
>   hides the bulk.
> - **A lamp's glow on a wall.** An inward scumble left rings and then a dark rim (the tool
>   said `inward-comb`). Glazes that wide spread too thin to show past the lantern
>   (`to_value` was refused as out of reach). Three soft round-tip strokes of paint, each
>   smaller and lighter, made the pool.
> - **Form marks on the face were too strong.** The nose's cast shadow and the cheek's
>   hollow, laid as soft strokes at 0.45–0.65 opacity, read as smears and a bruise. At
>   about 0.22 they read as form.
> - **Tired is in the lids.** More dark under the eyes looked like a black eye. Bringing the
>   upper lid down over the top of each iris, with one stroke of skin colour, is what reads
>   as a night without sleep.
> - **The swatch strip caught an orange half-tone.** Skin mixed from sienna and red read as
>   terracotta. Mixing the half-tone from the lit and the shadow skin keeps it in the
>   family.
> - **A pass script's `H`** (a dict of shared arguments) shadowed the prelude's canvas
>   height, and `P()` then divided by a dict. Name a prelude's constants so a pass cannot
>   reuse them.
>
> **What it still is**
>
> - **The hand is the weakest passage.** In context it reads as fingers over the shawl's
>   edge; close up, the joints are thin lines and the knuckles barely turn.
> - **The shawl is half the picture and has little in it.** That is partly the design
>   ("everything else is dusk"), but a better painting would spend its last marks on the
>   drape.
> - **The kerchief's body is one flat dark shape.** Its crown reads as sky on cloth now,
>   after a cool film in the last pass.
> - **The half-tone band down the face's shadow side** is still a little even, like the rim
>   of a mask.
> - **A low-key picture:** nothing above 0.42 at the 95th percentile. That is the design,
>   but it leaves the lamp and the face carrying all of it.
>
> **The signature**
>
> Two marks in the wall's own dark at the bottom right, free under `note="signature"`: a
> bell's outline with no clapper. *[A sentence naming the pack is left out here.]*
>
> *[A section with the pack's catalogue entry for the picture, and a paragraph on how the
> pack shows it, are left out for the same reason.]*
>
> **Working notes**
>
> - Many `easel run` calls in this session reported exit code 255. That was not Easel: it
>   came from piping the output into PowerShell's `Select-Object -First N`, which stops the
>   pipeline early and kills the process. Run under Git Bash, a rehearsal and `easel check`
>   both exit 0 and write nothing to stderr (measured afterwards).
> - `easel timelapse` takes `--scale` as a whole number. `--every 2` halves the frames
>   instead.
> - `draft.easel` (the drawing judged on a light ground) and `swatch.easel` are scratch,
>   kept in `exercises/`.
>
> **Corrected after filing (2026-09-26)**
>
> Measured while answering the owner's questions; the evidence is in [answers.md](answers.md).
> The text above is left as it was filed.
>
> - **There is no flour in the picture.** All eight flour strokes laid no paint (`easel log`:
>   *NO PAINT LANDED*), because a small bristle lays nothing below a load of about 0.5 and
>   mine were laid at 0.12–0.25. The nostril, the catchlight and the flame's core landed
>   nothing either, and the far iris next to nothing. After every pass, read `easel log` for
>   *NO PAINT LANDED*.
> - **The lightest mass is the face, not the lantern.** It is lighter by the mean, the median
>   and every high percentile. *Lightest: the lantern, as planned* was true only of the
>   planned places, and I never planned the face. The flame, mixed at 0.93, reads 0.71 at
>   best.
> - **The upstream rule was followed on the fist,** at the second failure each time: I redrew
>   it, then changed the idea. The first redraw kept the view, a fist from the front.
> - **The fist was about the right size**: 0.52 of the face's height. *Half again too large*
>   was eyeballed and wrong. The fault was the view.

## What happened when it was filed

Everything under this heading is the filer's, not the painter's.

- **What was filed, and what was not.** The passes keep the painter's names; two of them,
  `p07_fist.py` and `p08_finish.py`, had been rewritten by a PowerShell `Set-Content
  -Encoding utf8`, which saves a byte-order mark, and are filed without it — 0.7.0 reads a
  script with one, since #84. The prelude's docstring named her place in the pack; it names
  her instead, and nothing it lays changes. The session file (`wenna.easel`) and the two
  scratch files (`draft.easel`, `swatch.easel`) are not committed; the 32 saved reports are
  written out as [`reports.txt`](reports.txt). The export and the time-lapse are
  `painting.png` and `painting.gif`; the pack's WebP copy is not filed. Of the 52 looks
  and rehearsal pictures, nine are under [`evidence/`](evidence), renamed:
  `drawing_first.png` (the first drawing, on the light scratch canvas — the raised arm as
  sticks), `glow_rings.png` and `glow_rim.png` (the lamp's glow as an inward scumble, first
  a rusty patch of rings and then a dark rim like a knot in wood), `face_profiles.png` (the
  figure's first rehearsal: the Bell-Warden's shifted copies stacking three profiles in the
  face and stripes in the kerchief), `face_strip.png` (the light as a strip along the
  profile), `face_marks.png` (the face's form marks as smears), and `fist_disc.png`,
  `fist_bun.png` and `fist_cup.png` (the fist's three failures).
- **Rebuilt here, pass by pass, through `easel run`**, on the checkout at `v0.7.0`, from
  `p02_setting.py` to `p12_crown.py` in their numbered order: the same 281 records, 262
  spent, every record's geometry, dab count and brush as the painter's file has them, and
  an export identical to the painter's PNG to the pixel, on the machine it was painted on.
  **`p01_draw.py` must be left out**: it begins `s.erase()`, which lays a record, and it was
  never run on this session — run first, it moves every mark after it. To rebuild: `easel
  new wenna.easel --size 768x1024 --texture linen --ground umber_wash --seed 23 --budget
  300` in this directory (it leaves `prelude.py` alone), then `easel run wenna.easel
  p02_setting.py p03_figure.py p04_lantern.py p05_face.py p06_hand_cloth.py p07_fist.py
  p08_finish.py p09_cloth_in_hand.py p10_flour_and_folds.py p11_last.py p12_crown.py`, then
  `easel export wenna.easel rebuilt.png` — under a minute.
- **The versions, recovered.** The painter rewrote its passes in place — with the Write and
  Edit tools, and twice with a PowerShell `-replace` — so its session's transcript was read
  when the painting was filed, and every one of those 53 changes replayed in order. The
  replay ends on the painter's folder in every script, the byte-order marks aside. Each of
  the 36 `easel run`s on the painting's own session, run again on the canvas it opened on,
  **gives the report the file saved for it, word for word, for all 31** — fourteen of them,
  from the figure's pass to the fist's, with the plan as it then stood, because the eighth
  pass declared the ground — and the five that saved
  none raise again: two early rehearsals of the setting, two of the fist on the `H` that
  shadowed the canvas's height, and one of the finish.
- **What the tool said, and what it read.** From the saved reports: `inward-comb` on the
  glow's second rehearsal; `holes` on one rehearsal of the figure; `glaze-far` on the
  lantern's pass and on the finish; the one-disc line on the face's pass, at 7, 7 and then
  6 small round marks — and over the whole painting, in the closing checklist, *4 small
  marks … sit together around (0.55, 0.37)*, the finding the painter could not trace to its
  marks; `values:` *no clear light* on all 32 reports, the picture's top twentieth between
  `0.39` and `0.45`; and `lightest:` reading the lantern at `0.49` from its own pass on,
  against the `0.76` planned — `plan:` *lantern -0.27* at the end. **The lantern is a place
  most of whose pixels are its iron**: by its median it
  reads `0.51`, at its 90th percentile `0.58`, and its brightest pixel `0.71` — so the
  median the Bell-Warden's painter chose does not rescue this case, which is the median's
  own failure that painter named, a detail covering more than half its place. And **a
  percentile cannot see a lamp**: the picture's top twentieth reads `0.42`, while `1.4%` of
  the canvas lies above `0.60`.
- **What its answers found, re-measured here** ([`answers.md`](answers.md)). Its two probes
  on the painting, run again on a copy of its folder, print its tables exactly, and its
  counts hold. **The flour never landed**: 11 of the 262 charged strokes laid under one unit
  of paint — the eight flour strokes, records 193, 219, 220 and 258 to 262, at loads of
  `0.12` to `0.25`, and the nostril's dab (173), the catchlight (237) and the flame's core
  (240) — `4.2%` of the strokes and every mark of the flour the why names. Laid again at
  other loads, the flour's finger stroke lays nothing at `0.22`, a trace at `0.35` and
  paint from `0.5` up (`probes/flour_probe.py`). **The face is the lightest mass**, by every
  reading — median `0.584` against the lantern's `0.506`, `0.620` against `0.588` at the
  95th percentile, `0.718` against `0.714` at the brightest pixel — so the plan's
  *lightest: the lantern* held only among the places it planned, and it never planned the
  face (`probes/light_stats.py`). And three of its own sentences are withdrawn by it: the
  fist was not too large (132 px across, `0.52` of the face's height), the upstream rule
  was followed on it at the second failure each time, and *450 would have suited it* — the
  budget never bound. Its scripts lean on `opacity=` 97 times, `pressure=` 86 and
  `s.stroke` 84, and the card names none of `at_value`, `clip=`, `pressure`, `opacity`,
  `sample`, `mix_many` or `note=`; `clip=`, `sample` and `mix_many` are nowhere in
  `PAINTER.md` at all.
- **The model was `claude-opus-5-5` at max effort**, by the session's own metadata, on
  every turn of it; Windows, Python 3.14, PowerShell as its shell.
- **Its nouns, for the guide's grep**: *lantern*, *lamp*, *mill*, *door*, *gable*, *wall*,
  *bracket*, *kerchief*, *shawl*, *fist*, *hand*, *fingers*, *knuckles*, *face*, *eye*,
  *lid*, *mother*, *flour*, *dusk*. Many are ordinary words the guide uses in its own
  sense; the grep before a recipe is written looks for them used as a subject.
