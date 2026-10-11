# Step 2b of `PLAN-0.9.0.md`: measure the second painter's

**To understand this, start by reading the plan's status line and section 6's *After the
bench (step 2b)*, then [`CALIBRATION.md`](CALIBRATION.md)'s *Step 2b: the second painter's
candidates, benched*, then
[`scripts/probe_curator_session.py`](scripts/probe_curator_session.py)'s docstring.**

Branch: `claude/step-2b-continuation-bln1h2`, off `main` at `04cf66f` (#103, merged).

---

## What landed

| | |
|---|---|
| **`scripts/probe_curator_session.py`** | the plan's step 2b: `--claims`, `--alpha` (K), `--deposit` (M), `--layer` (N), `--grey` (L1), `--faint` (O3 and M2), `--corpus` |
| **`CALIBRATION.md`** | the round's *Step 2b* |
| **`PLAN-0.9.0.md`** | the status line; section 6's *After the bench (step 2b)* |

## What it measured, in one line each

The numbers are in `CALIBRATION.md`; what each proposes or asks is in the plan's section 6.

- **The rebuild**: all nine to the pixel on Linux, at their spend. The filing's one level
  was Windows.
- **K**: a hold's coverage as the alpha is harder than the painter's held paint edge (0.3 to
  0.6 px against 0.8 to 0.9), and stepped on a diagonal at two samples a side. Its
  *soften=2.5* is sigma 0.8 to 0.9.
- **M**: the candle at 4× lands its light (0.92, *2 of 2 places*) in 11.7 s against 2.0. The
  texture it loses on reduction is the marks' own, not the canvas tooth's.
- **M2**: a round tip under its width with a pressure list or opacity under 1: 807 marks
  in 31 of 34 paintings.
- **N**: `key="low"` says *low-key* on all six dark pieces; read inside the cut, the
  patron's values line finds its lost rim, and the ground line asks two solid cut-outs for
  ground.
- **L1**: as worded it cannot fire on the umber-and-ultramarine trap. Measured from the
  larger parent instead, it speaks in 29 of 34 paintings.
- **O3**: 327 faint marks in 28 paintings at 0.15 and a quarter of the way. It catches the
  patron's rim and the lock, not the candle's wax light, which M2 catches.

## Decisions and gotchas

- **The pieces are run, not replayed through the cohort harness**, for the four benches on
  the pieces: each script in a scratch copy of its folder with its own `argv`, a `Session`
  caught on construction, `look` stubbed, the time-lapse off. Painting at 2× or 4× rewrites
  the `Session` line alone, as the painter's `commands.sh` did.
- **The corpus replay is this probe's own**: the cohort harness with its candidates swapped
  out for one `CALL_CHECKS` entry, the canvas kept round each hand-laid mark, and
  `Palette.mix` patched to record what a script typed (not what `at_value` and `tint` mix
  inside the engine). About 26 minutes, kept in `out/curator/corpus.pkl`.
- **Heron 1's `pass1_draw.py` fails to replay** (`TREES` undefined) beside the pears'
  `p9_rehearse_pear.py`; it lays no paint, and heron 1 spends its recorded 293.
- **An alpha's edge read along rows has a floor**: linear interpolation across a one-pixel
  step reads 1.6 px whatever its levels. The painter's measure, the 10-90% band over the
  outline's length, is the one quoted.
- **The first weave candidate was dropped once measured**: laying the 1× tooth back over a
  reduced export assumed the 1× texture was the tooth. It correlates with neither the
  height map nor the gate (|r| at most 0.05).
- **L1's wording was tested before it was trusted**: two hues can only turn more than 90°
  from both parents when the parents are near opposite. The bench measures the plan's
  wording and the larger-parent form beside it.
- **O3's thresholds are not chosen here.** The tables give the counts at three distances
  and three reaches. *Reach* is a 90th percentile over the path's pixels at full width, so
  a tapered stroke's thin ends do not read as faint.

## Next

Questions back to the second painter, from the plan's section 6 *After the bench (step
2b)*: the alpha's edge against the held edge it chose (Q1 again), the reduced export with
`out/curator/deposit.png`, the ground line inside a cut, L1 as a backstop, and O3 and M2's
form and thresholds. To make the sheets: `python scripts/probe_curator_session.py --alpha
--deposit`. Steps 3 to 9 go on meanwhile; step 3's `difference()` is also K's hole.
