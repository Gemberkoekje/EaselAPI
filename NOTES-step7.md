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
no `buried` line and will gain one when D3 lands. **Ruled 2026-09-21: it does not** --
`checklist()` is `report(since=None)`, and a burial over a whole painting needs a
per-detail memory that was declined (`PLAN-0.6.0.md`, the decisions table).

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

---

# Step 7, part two: finding 12, the closing audit read as a painting

**To understand this, start by reading `_pass_findings` in
[`src/easel/session.py`](src/easel/session.py) — its `whole` parameter and the two rules
it changes — then `_small_combs`, `_discs` and `_disc_groups` just above it, then
`report_closing_audit` in
[`scripts/probe_cohort_session.py`](scripts/probe_cohort_session.py), then *The closing
audit, over a whole painting* in [`CALIBRATION.md`](CALIBRATION.md).**

Branch: `f12-closing-audit`, off `main` at `986d0a2`, after F1's build (#68) landed.

---

## What this part was for

`checklist()` is `report(since=None)`, and part one built it that way on purpose: one
instrument, so a number printed after the last pass and a number printed at the end
cannot disagree. But every rule of `_pass_findings` was written for a pass, and two of
them add a painting up. Gemini's closing check read *265 marks with a bristle under
size=0.025* and *one disc printed 176 times*; its painter argued with the first and
never answered the second (finding 12). No workstream row named it, and *Loose ends*
gave it to the owner's ruling on a count taken first. The count and the ruling were on
2026-09-22 (`PLAN-0.6.0.md`, the decisions table): the comb line leaves the closing
audit, and the disc line counts only discs seen together.

## What landed

| | |
|---|---|
| **`_pass_findings(whole=True)`** | the closing audit's scope: `checklist()` passes it, and `report()` passes `since is None`, which reaches `easel run --check`, `easel log --check`, `easel check` and the MCP `check` tool. Every other rule reads the whole painting as it did |
| **the small comb over a whole painting** | says nothing. A pass's report is unchanged to the byte |
| **the discs over a whole painting** | only groups of three or more, each within `_REPORT_DISC_RADIUS = 0.06` of another, signature marks left out; the line names each group's place, up to three and largest first, then *and N more*. One group reads *... sit together around (x, y): that is one disc printed N times* |
| **`_small_combs`, `_discs`, `_disc_groups`** | the two rules' filters lifted out of `_pass_findings`, and the grouping, so the probe reads the corpus with the engine's own definitions rather than a copy of them |
| **`History.is_signature`** | public, was `_is_signature`: the budget and the disc count share one definition of a signature mark |
| **the probe** | `report_closing_audit`, in the corpus run and on its own as `--closing` — every painting rebuilt without the candidates' canvas reads, about twenty minutes |
| **the documents** | `report()`'s and `_pass_findings`' docstrings; `REFERENCE.md`'s `report()` paragraph; `CALIBRATION.md`'s new section; `CHANGELOG.md`; `SUGGESTIONS.md`'s finding-12 row; the plan's status, decisions row and *Loose ends* |

## Decisions and gotchas

**1. The count needed looking, not only counting.** The first table — the disc line on
14 of the 21 checklists, the comb line on 9 — could not say whether a line was right.
Cropping the counted marks out of the finished canvases did. The large disc counts
were passages of repeated marks (Gemini's glitter lozenges, `sonnet`'s and the
greenhouse's pots); the small ones were accents from different passes, and `dusk`'s
*one disc printed 8 times* was a lamp, a moon, two notches, two edge highlights and a
glint from six passes. The comb split the same way, and there the large counts had been
said by their passes already.

**2. Why the comb leaves and the discs stay.** Neither line is noise everywhere; what
separates them is what each asks for at the end of a painting. The comb asks for a
brush for the next marks, and a finished painting has none. The disc line is the
closing checklist's own question — *is any small mark a disc, a capsule or a
rectangle* — which part one took out of `PAINTER.md` because this rule answers it.
Dropping it would have left the question unasked, and a painter who writes one script,
as Gemini did, never sees a pass's report and would never have heard about its glitter.

**3. The radius sits on a plateau.** `0.04` gives 8 checklists, `0.06` and `0.08` give
10, `0.10` and `0.15` give 11 (`car_wash`'s three join at `0.10`). Under `0.06` real
passages start splitting — `opus`'s and `pier`'s groups go at `0.04`.

**4. A mark is placed at the middle of its own path's box**, and distances are in the
brush's unit (the long side), the unit `_mark_length_and_angle` already works in, so a
canvas that is not square does not stretch the groups one way.

**5. The grouping walks one row at a time** rather than building the whole distance
table, which a painting of a few thousand dots would make a few hundred megabytes of.
Joined by union-find: quadratic in time, linear in memory. Gemini's 176 discs group in
about 2 ms, against about 110 ms for the whole of `_pass_findings` over its 726 marks.

**6. A signature is left out over a whole painting and nowhere else.** The ruling kept a
pass's own report as it was, so a pass that signs with three round dots is still told
*one disc printed 3 times*. No pass of the corpus does (`heron1`'s signature pass lays
two). Left as ruled, and written down here in case a run shows it.

**7. Three tests read these rules over the whole painting**, with `s.report()` — the comb
test, `_combs()` and the disc test. All three were tests of the pass rule that happened
to leave `since` off; they now pass it, and four new tests hold the whole-painting
behaviour: the comb left to the pass, discs standing apart, the groups and their
places, and a signature.

**8. The pressure-list rule has the same shape and was not touched.** It prints over a
whole painting on 4 of the 21 checklists; it is not finding 12, and its line calls the
marks *rectangles*, which answers the old checklist's *or a rectangle*.

## Open, and for the owner to rule on

Nothing new. Gotcha 6 is the one thing to watch for in the next run.

## What this part did *not* touch

**The noise table.** A pass's report is unchanged, so its rows do not move; the re-run
*Loose ends* asks for before 0.6.0 quotes a noise figure is still G11's. **The full
corpus run** (`--corpus`) was not re-run: `--closing` replays the same 21 paintings
through the same harness, without the candidates' canvas reads, and the corpus run now
prints the same table.

## File map

| File | What changed |
|---|---|
| `src/easel/session.py` | `_REPORT_DISC_RADIUS` and its comment; `_small_combs`, `_discs`, `_disc_groups`; `_pass_findings(whole=)` and the two rules; `report()` passes `whole=since is None`, `checklist()` passes `whole=True`; `report()`'s docstring |
| `src/easel/history.py` | `is_signature`, public and documented |
| `scripts/probe_cohort_session.py` | `CLOSING_RADII`, `_counted`, `_said_by_their_pass`, `report_closing_audit`; `--closing`; the corpus run prints the table |
| `tests/test_requests.py` | three tests take `since=`; four new ones after the comb and disc tests |
| `CALIBRATION.md` | *The closing audit, over a whole painting* |
| `REFERENCE.md` | the `report()` paragraph says what the whole painting is asked |
| `CHANGELOG.md` | *The closing audit, read as a painting rather than a pass*, under `[Unreleased]` |
| `SUGGESTIONS.md` | finding 12's row |
| `PLAN-0.6.0.md` | the status, the decisions row, *Loose ends* loses finding 12's row |
