# Two warm lights handing over: a lighthouse at dusk

Painted with `easel-paint` **0.6.0** installed from PyPI, in a sandbox, from what the
package ships and nothing else. `easel guide --full`, `--painting`, `--recipes`,
`--reference` and `--diagnosis` were all read before the first mark — 194 KB; the painter
counted about 180 — and `CALIBRATION.md` was not. No repository was open and no earlier
painting was seen. It ran `easel demo mistakes`, the demos of the recipes it used, and
five of the nine exercises (`ex/`: the value scale, wet against dry, edges, box against
shape, and the swatch strip with this painting's own mixtures). The subject was chosen
before any of it was read. **It is the first painting made against 0.6.0**, so it is also
the first fresh session to paint against that release's changes to the guide and the
tool, and what it says about them is read in [`PLAN-0.7.0.md`](../../../PLAN-0.7.0.md).

**To understand this, start by reading [`prelude.py`](prelude.py)** — the palette, the
headland's roughened silhouette, the tower, the landmarks and the `s.plan(...)` — then
`p00_draw.py` to `p12_sign.py` in order. [`verdict.md`](verdict.md) is the painter's own
review, written after the export, and [`verify/verify.py`](verify/verify.py) holds the
tests it ran before giving it; [`feelings.md`](feelings.md) is its own account of what
the work was like from the inside, given after the verdict and kept verbatim;
[`answers.md`](answers.md) is its answers to the nine questions `PLAN-0.7.0.md` put to
the owner, forwarded to it because the tool is for painters and the owner is not one;
and [`misfires/`](misfires) is its reconstruction of the two rehearsed passes the check
misfired on. The account of the files below is the painter's; the last section is the
filer's.

## The plan, as declared

Everything the guide asks a painter to write down went through `s.plan(...)` in the
prelude, before the first mark:

| declared | |
|---|---|
| why | *At dusk the sun's glow is going out low on the left while the lamp comes on at the right: two warm lights handing over, and the small made one has to win.* |
| values | the lantern `0.86`; the glow's core above the horizon `0.72`; the top of the sky `0.36`; the sky behind the tower's right `0.50`; the near sea `0.32`; the headland's face `0.16`; the tower `0.29` |
| lightest | the lantern |
| subject share | `0.25` |
| bands | `"subject"` — a dusk sea: the horizontals are the subject's own |
| ground | `"buried"` — sky and sea are continuous fields, with no ground between them |

The palette was checked as a swatch strip first (`ex/swatches.py`). 1024×768, linen,
`burnt_sienna` ground, seed 11. **171 of a 300 budget**, plus two signature marks that
did not count; 21 rehearsals and five variant sheets on throwaway copies, none of them
charged. At the end: subject share `15%` against the `25%` planned, `0.00%` bare ground
as the plan said, `129` of 300 unspent.

## The passes

| File | What it is |
|---|---|
| `prelude.py` | runs before every pass: the palette, the shapes, the landmarks and the `s.plan(...)` |
| `p00_draw.py` | the composition, as guides (free, never exported) |
| `p01_sky.py` | three sky ramps, warmth brought in from the left, two cloud crossers, the afterglow as glazes |
| `p02_sea.py` | the sea ramp with a ruled horizon, and the warm film the reflection sits on |
| `p03_headland.py` | the dark mass (roughened silhouette), its planes, two sea stacks, dry brush |
| `p04_tower.py` | the tower as clipped strokes, gallery, cap, lantern glass, lamp |
| `p05_light.py` | the beam and halo (three glazes), the lantern and lamp laid again |
| `p06_water.py` | the glow broken down the water, and the surf |
| `p07_subject.py` | the tower's incident: door, windows, lamplight on the gallery, lamp core |
| `p08_rock.py` | ledges, crevices, a fissure, dark rocks breaking the warm slope |
| `p09_edges.py` | lost edges in the lower right; the tower seated in its grass |
| `p10_surround.py` | side glints under the broad glow, a surf mark knocked back, foreground swells |
| `p11_final.py` | films turning the cliff face, calming the top of the sky, cool light on the tower |
| `p12_sign.py` | the signature: a small light over a short horizon (two free marks) |

Helpers — not part of the painting, but how the painter worked:

| File | What it did |
|---|---|
| `harness.py` | loads the session and prelude, and tries variants of a pass on throwaway copies |
| `try_sky.py`, `try_sky2.py`, `try_sky3.py` | the sky variants compared before `p01_sky.py` was committed |
| `price.py` | priced the headland's masses with `cost_line` — it found the 32-mark cliff face. It names shapes an earlier prelude had, so it no longer runs as it stands |
| `debug_log.py` | printed a scumble's stroke records while chasing the seam in the sky |
| `clean_look.py` | renders a look without landmark labels or pencil (`easel look` has no `--no-marks`) |
| `export.py` | wrote the PNG and the GIF |
| `montage.py` | stitches several images into one sheet |

## What the painter found

Its own words are in [`verdict.md`](verdict.md). In short: what worked was the
rehearsal — an egg-shaped glow, a panel stuck on the headland, gold-coin reflections and
a stair-stepped tower were all caught before a mark was paid for — the feedback (a glow
too shallow for its technique, pointed at *a volume of lit air*; the grass's brush size;
the lantern at `0.74` losing to the sky glow at `0.77`, which was the one number the
picture depended on), the plan held against the checklist, the cost explanations, and
learning the whole tool from `easel guide`, `demo` and `explain`. What did not: hard
edges that step from `0.59` to `0.28` in a pixel and read as vector graphics — *the least
paint-like thing in the engine, and I relied on it*; dry-brush speckle that reads as
dirt; one check that misfired twice; about 15 seconds a variant; no `--no-marks`; a 16 MB
session file; and a documentation set it calls thorough, accurate about its mistakes, and
too heavy, with one caveat far from its rule and one sentence backwards. Of the picture:
competent, coherent and conventional; the headland the weakest part, failed twice and
patched with brushwork where the guide says to go back to the drawing; and the budget
stopped at 57% partly out of caution.

What it would do differently: a later, darker dusk so the lamp dominates more; fewer,
larger rock planes decided while it is still a drawing; a headland that dissolves into the
water in more places; some of the warm ground left showing.

## What happened when it was filed

Everything under this heading is the filer's, not the painter's.

- **The passes were renamed** from `00_draw.py` … `12_sign.py` to `p00_draw.py` …
  `p12_sign.py`, which is the numbering the corpus probe reads. The painter's README,
  which described the three archives it delivered, is folded into this file. The session
  file (`lighthouse.easel`, 16 MB) is not committed — `*.easel` never is — and the 70
  looks, rehearsals and sheets are not either, except the four crops under
  [`evidence/`](evidence) that the verdict's claims point at: the tower's edges, the
  sky's flecks, the headland, and the tower. `verify/` keeps the painter's tests and the
  four images behind the two claims that stood; the three seam images were dropped with
  the claim, and `verify.py` regenerates them.
- **Rebuilt here, pass by pass, through `easel run`** on the checkout at `v0.6.0`: the
  same 192 records, 171 spent, every mark's geometry and dab count identical to the
  painter's file. The export differs from the painter's own by **729 of 786,432 pixels,
  each by one 8-bit level**, and the first record of the log says why: one mixture's
  blue channel is `0.2033674716949463` here and `0.2033672332763672` there — a `2.4e-7`
  difference in the palette arithmetic between two builds of numpy, carried through the
  wet blend. So the painter's *pixel-identical* holds on its machine, and *to the
  stroke* holds everywhere. To rebuild: `easel new lighthouse.easel --size 1024x768
  --texture linen --ground burnt_sienna --seed 11 --budget 300` in this directory (it
  leaves `prelude.py` alone), then `easel run lighthouse.easel p00_draw.py … p12_sign.py`,
  then `easel export lighthouse.easel rebuilt.png` — about 35 seconds. The helpers then
  find the session file they expect.
- **What the tool said, pass by pass**, from that rebuild: `glaze-far` once, at the call,
  on the sea's warm film (`p02_sea.py`, mixed `0.075` from what it landed on); the
  declared-bands line twice (13 long horizontals after the sky, nothing crossing them
  yet; 18 after the water, 6 crossing); and the standing lines after every pass — the
  `lightest:` line reading the glow's core at `0.77` against the lantern's `0.47` until
  the tower was laid, `0.78` after it and `0.85` after the beam; `edges:` at `19%` under
  2.5 px after the sky, then `60%`, `64%`, `65%` and falling a point or two a pass to
  `54%` at the end, median `2.2` px; the
  `subject:` line behind its planned share on every pass from the tower's. The file
  carries one notice, the same `glaze-far`. `checklist()` on the finished painting: 7 of
  7 planned places inside `0.10`; the lantern the lightest of them at `0.86`; `0 of 10`
  masses in a rectangle; `129 of 300 unspent`.
- **The verdict's measured claims, re-measured.** The edge steps hold: `0.30` in one
  pixel on the tower's left side at `y=0.40`, `0.28` on its right, `0.19` at the
  waterline, `0.44` where the headland meets the sky — and the clip mask the engine
  builds has exactly one fractional pixel per side. The glaze-width claim holds against
  the engine's own source: a round tip's width follows pressure, so the recipe's
  sentence runs the wrong way. The variant timing holds: a three-ramp sky variant as
  `harness.py` ran it takes 11.5 s here, 10.3 s of it the three scumbles themselves.
  The file holds: 16.1 MB, of which the time-lapse frames are 8.8 and the canvas 6.6.
  **One did not survive, and one could not be shown by the scripts.** The *graded
  passage laid too narrow* line fires on none of the thirteen committed passes and not
  on the whole painting: the two passes it misfired on were versions rewritten before
  they were committed. The painter then rebuilt both from its transcript
  ([`misfires/`](misfires)); re-run here, each prints its original line exactly, and
  in both the brush the line names is a thin dark accent laid among wide marks, which
  is the mechanism `PLAN-0.7.0.md`'s workstream C narrows. And the vary sheet does
  take a glaze — `{"points": ..., "glaze": True,
  ...}` is a stroke entry, and a sheet of three opacities rendered in under two seconds
  — so *doesn't support glazes* is a gap in the documentation, which names no such
  entry, rather than in the tool. The seam was already withdrawn by the painter; laid
  again here, the three sky ramps show no column seam wet or dried, though drying
  between them moves a third of the canvas by more than two levels.
- **The model was `claude-opus-5-5` at max effort**, by the session's own metadata --
  configured, current and last-served all the same -- with the painter's caveat that a
  single-turn fallback earlier in the session would not show there. It worked in a
  sandbox on Linux. Its subject was chosen before reading, and the earlier Claude
  [lighthouse at dusk](../lighthouse_dusk) in this directory — glow on the right, a moon
  over it — was never seen.
