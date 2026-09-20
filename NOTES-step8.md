# Step 8 of `PLAN-0.6.0.md`: the default moves (F)

**To understand this, start by reading `_mass_overhang` and `_scumble_paths` in
[`src/easel/session.py`](src/easel/session.py) — two lines of engine between them —
then *The load a band is laid at* and *The bites just inside a hard edge* in
[`CALIBRATION.md`](CALIBRATION.md), which are where the numbers behind those two lines
now live, then the nine tests at the end of
[`tests/test_requests.py`](tests/test_requests.py).**

Branch: `f-default-moves`, off `main` at `ce184ba`.

---

## What this step was for

Workstream F proposed **five** default moves. `scripts/probe_cohort_session.py`
measured all five in step 2 and **two survived**; this step lands those two, each in
its own commit with the goldens looked at, and writes the other three down as declined
so they are not re-argued.

`LESSONS.md` rule 3 is the whole reason the workstream exists: *a default is worth more
than a warning.* Both moves close a fault the documentation used to spend a paragraph
on, and both paragraphs left in the commit that made them untrue.

## What landed

| Move | Engine | What it buys |
|---|---|---|
| **F3** — a banded `scumble` lays its passes solid | `_scumble_paths`, the band branch, takes `{"load": 1.0, "load_falloff": 0.0, **brush_overrides}` | bare `5.17%` → `0.01%`, ripple `0.0110` → `0.0031` |
| **F5** — `edge="hard"` carries two brushes of overhang | `_mass_overhang` returns `2.0` | the strip inside a sloping outline, `round_hard`: `0.85%`–`3.26%` bare → `0.055%`–`0.33%` |

| Declined | Why the probe said no |
|---|---|
| F1, `cover()` → `edge="hard"` | **no committed pass script calls `cover()` at all** — the move is free and so is the evidence. It waits for the `spill` notice (D1, not built) |
| F2, a round tip → `pressure="even"` | **0 committed calls** would move |
| F4, a `flat` scumble → halved `jitter`/`size_jitter` | ripple `0.0053` → `0.0059`, scallop unchanged — nothing this instrument can see |

## Decisions and gotchas

**1. `bristle` is the one preset that does not start full, and it is `scumble`'s own
default brush.** `load=0.9, load_falloff=0.55`. That is why F3 is worth anything at
all: on any other preset the `load` half would have been cosmetic. It is also why *two
painters in three typed the clause by hand* — the corpus was routing around a default
in the wrong place.

**2. `solid=` is now a no-op on a banded scumble, and it stays.** After F3 the pair is
the default, and `{**solid_pair, **brush_overrides}` means an explicit keyword wins
either way — so `solid=True` changes nothing on a band. It is still accepted, because
scripts type it and `REFERENCE.md`'s hold matrix asserts it is accepted (the test
*makes the call*; a cell that is not `"yes"` asserts `TypeError`, which is `cover`'s
row). The docstring says plainly that it moves nothing rather than implying it does.

**3. The inward scumble's `load` was measured and deliberately not moved.** The plan's
reason column says *the inward form already defaults this way*, which is true of
`load_falloff` and not of `load` — `direction="inward"` still runs `bristle` at `0.9`.
Measured: `0.005%` of a patch bare against `0.012%`, mean value `0.5442` against
`0.5398`. Nothing asked for it, so under rule 1 it did not move. **This is the one
asymmetry the step leaves behind** and it is the obvious thing for a later round to
either close or write down as intended.

**4. B8's mechanism is pressure, and that is what made F5 safe.** The bites are pass
ends arriving at part pressure, because `pressure="taper"` reaches zero one brush out
and the old default was exactly one brush. Two consequences fell out of it:

- **It is the round tip's fault more than the chisel's** — a round tip loses *width*
  with pressure as well as opacity. This is the opposite way round from the chisel
  staircase, which is a chisel's fault and not a round tip's.
- **`scumble` needed no move at all.** Its passes are `pressure="even"` by default, so
  it has no bites: `0.000%` of the same strip at `0.35`, `1.0` and `2.0` alike, with
  either brush. It keeps its own `0.35`. `scumble` never called `_mass_overhang`, so
  this was luck rather than design, but it is measured luck now.

**5. F5 costs dabs and not strokes, which is the whole reason it is affordable.** The
pass count is identical at one brush and at two — 15, 18, 22 and 25 on the four slopes
measured — so `cost()` quotes exactly what it quoted before. `_mass_overhang` sits
where it does precisely so that `cost` and `block_in` cannot disagree, and this move
tested that: one constant, both callers.

**6. Nothing crosses the mask, so `edge="hard"` keeps its promise.** Paint outside the
outline went `225 px` → `227 px` on the measured case, that difference being the
boundary's own feathering, while bare *inside* went `0.220%` → `0.024%`. `cover`'s
published area ratios are unchanged (`1.00x` at `hard`, at every overhang).

**7. The goldens did not move, and that is not the same as not looking.**
`tests/golden_cases.py` calls no `scumble` and no `edge="hard"`, so both moves are
invisible to it — a green golden suite here proves nothing about either move. Both were
rendered before-and-after and **looked at** instead: the 0.5.0 band is peppered with
ground showing through, heaviest in its light half; the 0.5.0 hard edge has deep bright
notches along its bottom boundary which close to hairlines at two brushes.

**8. A misfiled changelog entry, fixed in passing.** Step 7's entry (`### The canvas,
measured, and the closing checklist answered`) had landed *inside* the `## [0.5.0]`
section in #61 rather than under `## [Unreleased]`. Moved, with the round's other three
entries. Worth knowing because `tests/test_version.py` holds release claims to tags but
does not hold an entry to the right section, so nothing caught it.

## Open, and for the owner to rule on

**The committed paintings were not repainted.** Both moves change what a script that
leaves the default off paints, and `paintings/` holds 21 of them. That is what the
`CHANGELOG.md` preamble's minor-bump rule is for — *a script that leaves a default off
can paint something different after a minor release*, while a `.easel` file always
replays as painted — so nothing here is broken. But `PAINTINGS.md`'s rebuild claims are
now one more version further from true, on top of the two the step-2 probe already
found (`car_wash` and `pears` come back five marks over; `pears/p9_rehearse_pear.py`
and `heron1/pass1_draw.py` do not run from a clean session at all). **That is one issue,
not three, and it is not this round's.**

**The inward `load` asymmetry** (gotcha 3) — close it or write it down as intended.

## What step 8 did *not* touch

Step 6 is still part-done, unchanged by this branch: `spill` (D1) is not built, and D2
(`glaze-far`, `smudge-across`, `smudge-long`) and D3 (`radiating`, `one-loop`) are not
started. F1 depends on `spill` and waits for it. `RECIPES.md`'s *quiet gradient: a
`flat` scallops* paragraph is listed in the migration map as leaving with *F (default);
`scumble-few`* — **both of its carriers were dropped**, so the paragraph stays and the
migration map's row for it is now wrong. Step 9 (docs) is where that gets settled.

## File map

| File | What changed |
|---|---|
| `src/easel/session.py` | `_scumble_paths` band branch takes the load pair (F3); `_mass_overhang` returns `2.0` (F5); three docstrings — `scumble`'s body and its `solid:`, `block_in`'s `edge:` |
| `tests/test_requests.py` | 9 tests at the end — 4 for F3, 5 for F5 |
| `CALIBRATION.md` | two new subsections, *The load a band is laid at* and *The bites just inside a hard edge*; both default-move rows marked as moved |
| `CHANGELOG.md` | a new `### Defaults moved` under `[Unreleased]`, with the three declines; step 7's entry moved out of `[0.5.0]` |
| `REFERENCE.md` | the `solid`, `load`, `load_falloff` and `edge` rows; a new `overhang` row for `edge="hard"`; the hold-matrix prose |
| `RECIPES.md` | the graded field loses the `load=1.0, load_falloff=0.0` bullet and the clause in its code block; four things becomes three |
| `SUGGESTIONS.md` | B8's *Not this step* becomes what was done |
