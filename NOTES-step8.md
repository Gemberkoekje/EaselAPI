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

**Ruled 2026-09-21: written down as intended.** It already was, in `CALIBRATION.md`,
`CHANGELOG.md` and `scumble`'s docstring; `REFERENCE.md`'s `solid` and `load` rows were
the one place that said otherwise, and now say *a banded `scumble`*.

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

---

# Step 8, part two: F1, a burial held to its place

**To understand this, start by reading `cover()` and `_cover_as_mass` in
[`src/easel/session.py`](src/easel/session.py), then `_check_clean_size` and
`_place_area` beside it, then *A burial and the place it was handed* in
[`CALIBRATION.md`](CALIBRATION.md), then `probe_f1_burial` in
[`scripts/probe_cohort_session.py`](scripts/probe_cohort_session.py), then the two tests
after `_cover_footprint` in [`tests/test_requests.py`](tests/test_requests.py).**

Branch: `f1-cover-hard`, off `main` at `1cd08d6`, after G3 (#67) landed.

---

## What this part was for

F1 was declined in part one because **no committed pass script calls `cover()`**, so
the corpus could say nothing either way. The owner reopened it on 2026-09-21 on a bench
of three passages built in a session scratchpad and ruled that it moves. The plan's
*Loose ends* gave it a *done when* -- the default moves; the docstring, `REFERENCE.md`
and the card say what it does; the changelog moves it out of the declines; the bench
joins the probe and its numbers go into `CALIBRATION.md` -- and a second row the same
bench found: `edge="clean"` on a region was never checked at all.

## What landed

| | |
|---|---|
| **`cover(edge="hard")` by default** | the same passes, every dab masked to the place, two brushes of overhang (part one's F5 rule); `cost()` prices a burial as a held block-in, because `_cover_as_mass` now writes the edge in rather than letting the mass default (`ragged`) stand |
| **`clean-small` on a region** | `block_in` and `preview` ask a region what they ask a shape; the line names the call made (`cover` or `block_in`), and a burial's remedy is its own default rather than the ragged edge |
| **the bench** | `probe_f1_burial`, called from F1's block of `probe_defaults`; the old paints-at-all loop stays beside it, because *The default moves* table quotes it |
| **the documents** | `cover()`'s docstring; `REFERENCE.md`'s `overhang`, `edge` and `clean-small` rows; the card's `undo` row and *What you are bad at*; `CALIBRATION.md`'s new section, a region paragraph under *A clean edge on a narrow mass*, the default-moves row and the spill paragraph; `CHANGELOG.md`; `SUGGESTIONS.md`'s finding-8 row; the MCP plan help |

## Decisions and gotchas

**1. The bench was rebuilt, not copied, and its numbers differ from the ruling's.** The
ruling's bench was never committed. The one in the probe has passages of its own, and
reads `ragged` `4.45x` / `4.14x` against `hard` `0.47x` / `0.51x` on the graded and
worked passages, with an outline step of `0.042` against the passage's `0.010` -- where
the ruling quoted `3.09x` / `0.52x`, `4.55x` / `0.93x` and `0.0285` against `0.0055`.
The same order, the same verdict. `CALIBRATION.md` carries the committed numbers; the
plan's decisions row keeps the ruling's and says so.

**2. *Seen*, not *painted*.** The probe's old measure -- any pixel the call moved --
says `ragged` paints `5.3x`-`6.4x` the place on a flat passage too, where nothing can be
seen. The bench counts the pixels left `0.02` or more off the passage as it stood before
the mistake, the step `_contours` calls visible. That is the number that tells a flat
passage from a worked one, and it is what the docs quote.

**3. The first *worked* passage was not worked.** Ninety marks over 900x600 left its own
outline step at `0.0080` against the graded field's `0.0076`. Four hundred took it to
`0.0097`. A passage worked harder than that would push `hard`'s *seen* up, because more
texture goes under a flat patch; the verdict does not depend on it.

**4. A test that only the old default could pass.** `test_cover_lays_the_burying_recipe`
measured rows 100-140 and columns 140-180 on 320x240 -- D5's top-right corner, not its
middle -- and passed only because a ragged burial ran past the cell. The window is
inside the cell now.

**5. The docstring's old advice trips the new line.** It recommended `edge="clean"` on a
textured passage and quoted the leaf patch at `0.93x`; a `0.06` brush on that patch is
`82%` of its shorter extent, so the call now says so. The `0.93x` measured how much was
painted, never whether the mistake was gone.

**6. `Region.inset` works per axis in canvas fractions**, so on a canvas that is not
square a region's clean inset is not the same in pixels both ways (`0.05` is 45 px
across and 30 px down on 900x600). `_clean_fill` and the check both call it, so the line
describes what the call does; the anisotropy is older than this and is left alone.

**7. The goldens cannot see this move.** `tests/golden_cases.py` calls no `cover()`, as
it called no `scumble` for F3. The bench's nine renders were looked at instead: `ragged`
is a flat panel about three times the place with the neighbouring marks under it;
`clean` leaves both ends of the mistake; `hard` is a crisp rectangle exactly the place.

**8. The probe's `bound` applies defaults**, so a call that names no edge cannot be told
from one that names the new default. The corpus has no `cover()` to tell apart, and the
count line now just prints how many there are.

## Open, and for the owner to rule on

Nothing new. *A repair under things that are standing on it* was the one demo waiting on
F1 (G3), and can be written now.

## What this part did *not* touch

**The corpus replay was not re-run.** No committed pass script calls `cover()`, and
every `edge="clean"` in the corpus and the guide is handed a shape -- read off the
scripts, not replayed. The block check was run, and holds the guide's blocks and the
twelve demos to that.

## File map

| File | What changed |
|---|---|
| `src/easel/session.py` | `cover(edge="hard")` and its docstring; `_cover_as_mass` writes the edge in; `_cover_overhang`'s comment; `block_in` and `_preview_mass` ask a region for `clean-small`; `_check_clean_size` takes a region and the verb; `_place_area` |
| `src/easel/notices.py` | `clean-small`'s summary says *a shape or a region* |
| `src/easel/mcp_server.py` | the plan help says a burial is held to its place unless `edge` says `"ragged"` |
| `scripts/probe_cohort_session.py` | `F1_PLACE`, `SEEN`, `_f1_passage`, `_outline_step`, `probe_f1_burial`; F1's block of `probe_defaults` calls it |
| `tests/test_requests.py` | the overrun test turned round (the default holds, `ragged` runs outside); the bench's `clean` case as a test; the spill-silence test names `edge="ragged"`; the burying-recipe test's window moved into its cell |
| `CALIBRATION.md` | *A burial and the place it was handed*; a region paragraph under *A clean edge on a narrow mass*; *Paint that lands outside the place*'s `cover()` paragraph; the default-moves row |
| `CHANGELOG.md` | F1 under *Defaults moved*; three declines become two; the spill entry's and G7's `cover()` lines |
| `PAINTER.md` | the card's `undo` row, shorter; *What you are bad at* says what the default does |
| `REFERENCE.md` | the `overhang` (`cover`) and `edge` rows; `clean-small`'s row |
| `SUGGESTIONS.md` | finding 8's row |
| `PLAN-0.6.0.md` | status; F; G3's note; the migration row; step 8; *Loose ends* loses F1's two rows and gains finding 12's; the decisions row; a risk row |
| `NOTES-step6.md` | the F1 ruling points here |
