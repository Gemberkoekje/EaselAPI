# The underside of a pier at low tide

Painted with `easel-paint` 0.4.0 installed from PyPI, working only from what the package
ships — `python -m easel guide`, `--full`, `--reference`, and `easel brushes`. **The
repository was not opened at any point**, and the session ran in an empty directory: no
checkout, no listing, nothing to read but the package.

**To understand this, start by reading `prelude.py`** — the mixtures and the masses as
functions — then `pass1_draw.py` through `pass15_sign.py` in numerical order. Every pass
was rehearsed with `--rehearse` and looked at before it was paid for.

## The plan, as numbers, before anything was mixed

| mass | planned | mix |
|---|---|---|
| deck underside | 0.22 | `burnt_umber` + `viridian` |
| water | 0.28 | `viridian` + `burnt_umber` |
| the slot of daylight | 0.80 | `yellow_ochre` + `titanium_white` |

Ground `#5a5045` (v=0.32) — warm and dark, chosen so that whatever showed through would
read as warmth under cool paint rather than as holes. 1024×768, linen, seed 11. **257 of
a 300 stroke budget**, plus two signature marks that did not count. Twenty-three
rehearsals, none of them charged. Bare ground at the end: **0.58%**.

## Why this subject, and what happened to the reason

Chosen before anything was installed, and written down: under a pier the light arrives
from **below**, bounced up off the water, so every form is lit backwards — caustics
crawling on wood, a ceiling brighter than the floor. That is a thing paint can do and a
camera mostly cannot, and it was the whole reason for picking it over nine other subjects.

**It is not in the finished picture.** What is there is a competent dark structure over
water at dusk, lit from the ordinary direction. The painting passed every line of the
closing checklist on the way to losing it: the value structure is sound, the masses are
shapes, the edges vary, the lightest mass is the one that was planned to be lightest.
Nothing failed. Nothing asked.

That is this painting's contribution to the project, and it is worth more than the
picture: **nothing in the method asks whether the reason you chose the subject is still
there at the end.** The checklist asks whether the thing you measured most carefully is
still attached, which is a question about a mark. The round in
[`SUGGESTIONS.md`](../../SUGGESTIONS.md) proposes the two lines that would have caught it.

## Decisions

- **The composition was wrong twice before any paint.** The first arrangement made the
  distant opening the hero and left the underside — the actual subject — an empty band
  across the top. Drawing is free, so it was redrawn until the underside owned the top
  60% of the frame. Both wrong versions cost nothing, which is the argument for step 1.
- **Three bands, crossed.** Deck / slot / water is three horizontal bands, which the guide
  allows only if something crosses them. The two near pilings cross all three. The
  cross-bracing, added late in `pass8_structure.py`, is what finally broke the banding
  the post-pass check had flagged on nearly every pass — and it is the best decision in
  the picture.
- **The joists are graded, not uniform.** Near-black deep under the pier, lit where the
  bounce off the water reaches them. Joist 2's lit face is deliberately omitted so that
  not every edge is found.
- **The signature** is a short mark with a shorter, fainter one beneath it, bottom left,
  close in value to the water it sits on: a thing and the light thrown back up at it,
  which is the logic the picture was supposed to be about.

## Pitfalls, each of which cost a rehearsal and no strokes

- A single `direction=` across a mass that size combs the whole thing into hatching.
  `"cross"` fixed it.
- A ragged `block_in` breaks past its outline by about half a brush width. At `size=0.20`
  that swallowed the slot of daylight entirely; `edge="hard"` was right where the eye goes.
- Caustics laid as short round-tip marks are blobs stuck to the ceiling. They are
  filaments — `liner`, wavy multi-point paths.
- A foreground darkened with wide glazes lands as a bar with a hard lid. `scumble` grades
  it.
- A ripple colour held fixed while the water under it darkens becomes a pale floating
  stone. A ripple is only ever a step off its own local value.

## What it does not do

- **The pilings are slabs.** They are cylinders, painted as rectangles with a stripe down
  one side, and they never turn from lit to shadow. *A form that turns* is a recipe in a
  file this session never opened.
- **The range is crushed.** The box runs 0.14 to 0.96; almost the whole picture sits
  between 0.15 and 0.35, and the painter had been calling that atmosphere.
- **It stopped at 257 of 300 with the weakest passage still the weakest** — the thing the
  checklist warns about by name, two lines from its end.

## Reproducible

**Not claimed.** The drawing pass was rewritten and re-run three times, several `look`
scripts ran as passes between the painting ones, and each pass script was edited after its
rehearsal — so the committed scripts are the last version of each, not the sequence that
actually built the canvas. A mark's texture is seeded from its place in the log, so a
clean rebuild would not come back byte for byte.
