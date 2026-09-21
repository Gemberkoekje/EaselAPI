# Step 7 of `PLAN-0.6.0.md`: measurements (E) and `s.checklist()` (G4)

**To understand this, start by reading [`src/easel/checklist.py`](src/easel/checklist.py),
then `Session.checklist` and `Session._canvas_lines` in
[`src/easel/session.py`](src/easel/session.py), then the new tests at the end of
[`tests/test_requests.py`](tests/test_requests.py).**

Branch: `e-measurements-and-checklist`, off `main` at `b7d6bab`.

---

## What this step was for

Everything the check could say until now came off the **log** — brush, size, path,
pressure, note per mark. Four of the closing checklist's questions cannot be answered
from a log at any length, because they are about the canvas rather than about a call,
and each of the last three cohorts answered them wrongly by looking. Workstream E puts
a number on them; G4 turns the whole checklist into output and shrinks `PAINTER.md`'s
list to the three questions nothing can measure.

## What landed

**A new module, `src/easel/checklist.py`** — the measurement lines and the thresholds
behind them, each with its evidence in the docstring. Deliberately pure: every
function takes arrays or counts and returns a string, so the thresholds can be tested
without painting anything.

| Line | Where it prints | Notes |
|---|---|---|
| `values:` | every `report()` | 5–95 percentile against what the palette reaches, plus three clusters. **Range first, clusters second** — a picture can have three separated clusters and no light in it (the pier). |
| `edges:` | every `report()` | rise width per boundary. **The prototype did not work; see below.** |
| `ground:` | every `report()` | was already there; factored out to `_ground_line()` so `checklist()` says it in the same words |
| `pencil:` | every `report()` | skipped entirely when `canvas.has_sketch` is false |
| `holes:` | at the call, after a mass laid solid | a notice, code `holes`, beside `solid-comb`. `solid=True` **or** a brush already carrying `load=1.0, load_falloff=0.0`, which is what `cover()` lays |
| `boxes:` | `checklist()` only | needs the log to know a mass was handed a rectangle — see the `boxed` param below |
| `unspent:` | `checklist()` only | finding 15 |

**`Session.checklist()` / `easel check` / the MCP `check` tool.** Everything
`report()` prints over the whole painting, plus `boxes:`, `unspent:`, and the three
questions with the plan's own `why` quoted back. Read-only: `easel check` does not
write the session file.

**`PAINTER.md`'s checklist shrank 743 → 504 words** and is now the call plus the three
questions. The file is 6,299 words (was 6,522).

## Decisions and gotchas

**1. `edges:` — the prototype measured the wrong pixels, and one published number is
withdrawn.** `CALIBRATION.md` reported the corpus at 12%–44% under 2 px, median 27%.
Building the line found two faults that compound:

- It selected the **top percentile of the gradient**, which returns the sharpest
  pixels of *whatever* picture it is handed. Four canvases painted for the purpose all
  came back p25–p90 of 1.5–2.1 px.
- Its threshold was **2.0 px**, which is exactly what the sharpest transition a pixel
  grid can hold measures (a one-pixel step of size *s* has a central-difference
  gradient of *s/2*, so the rise is `s / (s/2)`). A threshold on the discretisation
  limit is a coin flip, and it flipped the wrong way: a hard-edged `flat` mass read
  **41%** hard and a ragged comb **84%**.

What shipped selects edge **ridges** (gradient at least as large as the gradient a
pixel either side along its own direction — this throws out both the tooth, whose
gradients are not ridges, and the broad interior slope of a graded mass, which has no
crest) with a **step of at least `0.10`** across them, and cuts at **2.5 px**. The
same four canvases then read 49% / 49% / 53% / **0%**, the zero being the round soft
brush; a numerically blurred canvas moves from 2.0 px median to 6.8.

**The corpus replay wants re-running before finding 13 states a spread again.** That
is the one open item this step leaves. Nothing else in E is affected.

**2. `holes:` fires on what the paint did, not on which keyword was typed.** The gate
is `solid or (b.load >= 1.0 and b.load_falloff <= 0.0)` — the same test
`_check_solid_comb` already asks. `cover()` lays that pair itself and *refuses*
`solid=` as a duplicate of its own recipe, so without the second clause a burying pass
would have been the one solid mass nobody measured, and burying is exactly where a
hole is worth knowing.

**3. `holes:` is gated on contrast, and that is not what it first looks like.**
`CALIBRATION.md` B2 says *a hole is a contrast, not a gap* and gives `0.16%` on
`toned_grey` against `3.16%` on a dark ground for the same call. The 3.16% is the
measurement finding **paint that barely registered** — burnt umber on near-black moves
no pixel more than `10/255`, so the interior reads as bare — not a hole anybody can
see. So the line is silent under `_HOLES_CONTRAST = 0.15` of value between the paid
colour and the ground, which is what turns the prototype's 8%-of-passes into something
worth printing. The engine reproduces B2's three grounds to the third decimal
(`0.1543` / `0.1350` / `3.1601`), and `tests/test_requests.py` holds it there.

**4. `boxes:` needed the log to carry something new.** A mass records the points of
each of its passes and never the outline it was filling, so a box and the shape
inscribed in it left the same log. `_one_call(verb, place)` now also rides
`params["boxed"]` when the place is a `Region`. Written only when true and read with
`.get`, so a 0.5.0 file opens unchanged (the plan's own compatibility guard).

**Counting calls, not records.** A mass is many records, so counting records would
report one wide band as thirty rectangles. `checklist.mass_counts` walks the log and
groups by `(via, rng)` — every record of one call carries the generator's state **as
the call began**, which is one value for the whole call and a different one for the
next. That invariant already existed for undo; this is the second thing leaning on it.

**5. `ground_showing(where=)`.** A mask parameter, so *bare inside a mass* and *bare
over the picture* go through one definition. Two definitions of "bare" is how
`CALIBRATION.md` and the engine would drift apart.

**6. Cost.** `_canvas_lines()` is ~314 ms on a 1024×768 canvas — `ground_showing` 122
(already there), `edges_line` 145, the rest ~45. Paid once per `report()`, not per
mark; a pass is many ~200 ms strokes. `edges_line` finds the ridge over the whole
canvas (two gathers) and then walks only the ridge pixels; walking the whole canvas
nine times cost 216 ms instead of 145.

**7. Everything is skipped on a counted copy.** A `scratch(count_only=True)` borrowed
the canvas and laid no paint on it, so every number read off that canvas would be the
painting's and not the pass's — and `holes:` would report every pixel of a counted
mass as bare. Held by `test_the_standing_lines_are_left_off_a_counted_copy`.

## Open, and for the owner to rule on

**The noise budget.** `report()` now prints four standing lines on every pass. E says
*standing lines under the findings, like `ground:`*, and `ground:` has printed every
pass since 0.4.0 — so this is the plan as written. But the risk table's target is
*fewer than three lines on a median pass*, and four standing lines alone exceed it.
`values:` and `edges:` barely move pass to pass; if the target is to hold, they are
the two to move into `checklist()` and `--check` only. **Not changed here** — it is a
plan decision, not an implementation one.

**Ruled 2026-09-21: kept on every pass.** The target counts findings and call-time
notices — what `scripts/probe_cohort_session.py` has always counted, which is why
`ground:` printing after every pass never showed in it. A standing measurement is not a
finding; whether the longer block gets skimmed is the next run's to show.
`PLAN-0.6.0.md`'s decisions table has the ruling, and `CALIBRATION.md`'s noise budget
now says what it counts.

## What step 7 did *not* touch

Step 6 is still part-done and is untouched by this branch: `spill` (D1) is not built,
and D2 (`glaze-far`, `smudge-across`, `smudge-long`) and D3 (`radiating`, `one-loop`)
are not started. G4's checklist names a `buried` line, which is D3's check — the plan
already says `buried` needs a narrower gate before it is built, so the checklist has
no `buried` line and will gain one when D3 lands.

## File map

| File | What changed |
|---|---|
| `src/easel/checklist.py` | **new** — the five measurement lines, `mass_counts`, and the three thresholds |
| `src/easel/session.py` | `checklist()`, `_questions()`, `_canvas_lines()`, `_ground_line()`, `_subject_line()` extracted from `report()`; `_check_holes()`; `_one_call(verb, place)` and the `boxed` param; `_call_boxed` on three init sites and in `replay` |
| `src/easel/canvas.py` | `ground_showing(where=)` |
| `src/easel/palette.py` | `lightest_value` property, beside `darkest_value` |
| `src/easel/notices.py` | the `holes` notice |
| `src/easel/cli.py` | `easel check` |
| `src/easel/mcp_server.py` | the `check` tool |
| `tests/test_requests.py` | 11 tests at the end of the file |
| `PAINTER.md` | the checklist section rewritten; two cross-references |
| `REFERENCE.md` | the `holes` row, `easel check`, `s.checklist()` |
| `CALIBRATION.md` | the `edges:` correction, under *The measurement lines* |
| `CHANGELOG.md` | the step's entry under `[Unreleased]` |
| `README.md` | the check row, and a closing-checklist row beside it |
