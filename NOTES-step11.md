# Step 11 of `PLAN-0.9.0.md`: a piece cut out of its canvas (K, N and M1)

**To understand this, start by reading the plan's section 6, *For the second painter,
batch 2*, and the painter's own words,
[`the_curator/answers-step2.md`](paintings/Claude/the_curator/answers-step2.md) 1, 2 and 4
with its first [`answers.md`](paintings/Claude/the_curator/answers.md) 1 and 4; then
`Plan.cut` in `src/easel/plan.py`, `Session.export` and `_canvas_lines` in
`src/easel/session.py`, and `CALIBRATION.md`'s *A piece cut out of its canvas*.**

Branch: `step-11-cut-and-alpha`, stacked on `step-10-parts-price` (#115) at `a658eee`.

---

## What landed

| | |
|---|---|
| **`src/easel/plan.py`** | `Plan.cut`, a tuple of named places; `plan(cut=)` takes a place, a list, or a `difference()`, `[]` clears; `cut_coverage()` at four samples a side and `inside_cut()` over half of it; saved in the file under `cut`, which a build before reads past; `plan:`, `lightest:` and the named light's reading take the cut, a place wholly outside named and not counted |
| **`src/easel/checklist.py`** | `edge_rises()`, the `edges:` measure split out so it can read inside a cut; `cut_ground_line()`, canvas with nothing laid on it and its 2 px fringe; `cut_line()`, the cut's edge against the picture's median and hardest tenth, compared as printed; `boxes_line(background=)` |
| **`src/easel/session.py`** | `plan(cut=)` and its check that a cut covers pixels; under a cut, `report()` and `checklist()` read every canvas line inside it and add `cut:`; `export(alpha=, soften=, size=)`, RGBA from the plan's cut, the alpha built at the size that ships; `_soften_sigma` (the painter's measure on a slanted edge), `_blurred`, `_soft_edge`, the cut's coverage kept until it changes |
| **`src/easel/cli.py`** | `easel plan --cut PLACE`; `easel export --no-alpha --soften --size`; the prelude template names `cut=` |
| **`src/easel/mcp_server.py`** | the `plan` tool's `cut`, the `export` tool's `alpha`, `soften`, `size` |
| **`tests/test_cut.py`** | the declaration, a hole, the file; the alpha, with and without a cut; `soften` as the width a slanted edge reads, the default at sigma 0.383; `size` and its refusals, the alpha at the shipped size; the checklist and a pass inside the cut, a place outside it, the fringe |
| **`scripts/probe_curator_session.py`** | `--cut-built`: the three cut-outs declared, their lines whole and cut, the alpha's widths three ways, a close-up sheet, and the candle exported from 4x |
| **`REFERENCE.md`**, **`llms.txt`** | the signatures, the `ground:` and `cut:` rows, the plan's `cut=` row, the paragraph on painting large and exporting small; the reference's size, ~12,700 |
| **`CALIBRATION.md`**, **`SUGGESTIONS.md`**, **`PLAN-0.9.0.md`** | the passage; The Curator's transparency, deposit and layer rows; the status line and step 11's row |

## Decisions and gotchas

- **`soften=` is the painter's own measure, on a straight edge at a slant.** The first
  build took it as the Gaussian's own 10-90% width, which put the default at sigma 0.33:
  on the pixel grid that blur moves almost nothing, and the close-up looked like the bare
  coverage. The painter's 0.85 came from its *band between 10% and 90% over the length*,
  which on an outline along the pixel rows jumps from half a pixel to nearly two; at a
  slant it is continuous. Solved there once, the default lands at sigma 0.383, the 0.39
  the painter solved on the patron, and one softening serves every outline. **Under about
  1.3 px it still moves in steps** (0.77 for the coverage, 1.0 for the first softening),
  so 0.8 to 1.0 soften alike; the docstring says so. On the jamb and the candle's sides
  the default reads 0.52 and 0.31, below the step the painter's sheet took there (sigma
  0.49): **a reading for the painter to confirm**, with `out/curator/cut_edges.png`.
- **The `cut:` line compares the widths as it prints them.** The edge measure reads a
  one-pixel step as `2.0`, and a cut and the hardest painted edges both sit there; compared
  raw, the candle was told *harder than any edge the paint made* at 2.02 against 2.00. To
  a tenth of a pixel it is level, and silent, as the painter expected with the default.
- **The ground line inside a cut counts nothing laid, not the ground's colour** -- the
  painter's own finding: by colour the wall's cut was 5.31% ground, all stones and joints.
  The whole picture's ground line is unchanged.
- **The alpha is built at the size that ships**, from the places in canvas fractions, so a
  candle painted at 4x and exported at 120x300 has the 1x export's alpha to the level.
- **`size=` reduces and never enlarges**, and refuses other proportions (beyond a pixel).
  Lanczos on the sRGB, as the painter reduced; the bench found the box mean in linear light
  within 0.01.
- **The cut's coverage is kept on the session** until the cut changes: sixteen samples a
  pixel over the 1920-wide wall take two seconds, and a report read it three times.
- **The shipped size on the plan is not built.** The painter asked for it so lines in
  pixels read at the size that ships (the candle's 2.3 px median edge at 4x is under a pixel
  at 120x300); it is left a candidate, as the plan said.
- **Heredocs holding Python with quotes broke Bash three more times**: every patch went
  through a script file.

## Not done here

The plan does not know the size that ships. The deposit table in pixels, O3 and the word
for a faint mark, `p.grey()`, and `easel run` taking a self-built script are step 12. The
closing checklist's *looked at small* question does not yet mean *at the size the game
shows it* for a cut-out.

## Next

Step 12 (O3 at `s.look()` and after a pass, `easel run` with a self-built session,
`p.grey()` and the hue on the swatch, the deposit table); then the cut, step 13.
