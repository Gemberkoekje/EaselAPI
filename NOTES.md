# Phase notes: the greenhouse round, and the post-pass check

*To understand this, start by reading [`SUGGESTIONS.md`](SUGGESTIONS.md)'s two tables
headed **What the greenhouse sessions found** — eleven engine items and eight
documentation items, each with what was measured before it was built — then
[`CALIBRATION.md`](CALIBRATION.md)'s new sections (*The contour of a clean edge*, *A
clean edge on a narrow mass*, *The chisel staircase*, *The band across a wedge*,
*Chroma*, and *The log, undo, and the stream*), then [`LESSONS.md`](LESSONS.md)'s
rewritten paragraph under **A separate file of warnings**, which is where the post-pass
check is described as built. The code is `src/easel/session.py`; the numbers are
reproducible with `python scripts/probe_greenhouse_session.py`.*

Every item three painters left beside their paintings under
`paintings/lighthouse_greenhouse/` is done, the post-pass check that had been open for
two rounds is built, and it is all in **0.2.0**, which had not been released.

## The shape of it

**Every number the three painters took reproduced, and two of the mechanisms they
proposed were wrong.** That is the character of this round, and it is the opposite of
the last one's: the fourth session's claims were *observed* and two did not survive;
these were mostly *measured* — Opus and Fable shipped probes with their lists — and all
nine held to the percentage point where a number had been taken. What the re-measurement
bought this time was not *nothing to fix* but *the right thing to fix*:

| The claim | What measuring it found |
|---|---|
| `edge="clean"` fails on a narrow mass, and the trigger is the corner spacing (Sonnet) or the brush's share of the shorter extent (Opus) | Both were views of the contour's **spline**, which bowed 45–69px off three different four-cornered shapes. Along the polygon's own edges it is 4px, the ragged fill's own half-brush. The share survives as a second finding — the *corners* go past about a quarter — and is the new warning's threshold |
| CLI `easel undo` drifts 1.06% of the canvas; the mechanism is "accumulated state — the random stream or the wet layer" (Fable) | Two causes. A mass draws its wander *between* the strokes it records, so undoing one left the stream past it and a replay handed back the seed; **and the log rounded every point to five decimals**, so a replay from disk was never quite the painting. The toy cases could not show the second because hand-written coordinates are short decimals already |
| `pencil` "advances the stream" (Fable) | It never touches the stream. It is *logged*, and a mark's texture is seeded from its place in the log — so `dry()` and `erase()` do the same thing, which the probe had not tried |
| A saturated mixture reads more vivid in a low-chroma field; mechanism a guess, simultaneous contrast (Sonnet) | The engine side is nothing: a solid plane reads at the mixture's chroma or a little under, never above, and the view equals the paint. The fifth *measured and nothing to fix*; `chroma_of` is the instrument instead of a rule |

The other five — the chisel staircase, the direction ratios, the wedge, the pairs, the
rehearsal count — reproduced exactly and were built as asked.

**The post-pass check** is `Session.report()`, six rules read off the log and printed by
`easel run` beside the budget line after every pass. Building it needed one thing the log
did not have: a way to tell a pass of a mass from a mark laid by hand. Every record now
carries the verb that laid it (`params["via"]`), which is also what lets two of the rules
— *one brush at one size* and *a stack at one angle* — count **calls** rather than marks,
so a single mass never fires them and two parallel masses do.

## Decisions worth knowing

**The stream's state is taken once per painting call, not per record.** `LESSONS.md` had
left the undo issue open with exactly the reason: a mass draws each pass's wander between
the `stroke()` calls that record it, so a state taken when a record is written is already
one draw past the undone mark. `Session._one_call()` takes it at the start of the outer
call and every record the call makes carries the same one; the contour of a clean
block-in and `cover`'s dry-then-fill nest inside it. `replay()` copies each record's
state across verbatim rather than re-recording it, because a replay never draws.

**The clean contour is a behaviour change and it is deliberate.** Every clean mass in
every painting rebuilds differently now — the dusk example's tower loses an arch its
committed PNG never had — and the draw from the stream was kept identical so that
nothing laid *after* a clean mass moves. `CHANGELOG.md` says so under *Changed*.

**The log's points are exact now, and the format was not bumped.** A record gained two
keys and lost five decimals of rounding; an older build reads the file without noticing
and a file from an older build loads here, minus the one thing it cannot have (its
stream restored on undo, which `_restore_stream` reports rather than guesses).

**`direction`'s default became `None`.** It still means horizontal. The warning fires on
*left off*, not on *chosen*, and there was no other way to tell the two apart.

**The composition recipes are the least certain things written this round.** Opus asked
for them "eventually, collected across paintings, not composed" and said one painting
could not write them. Four paintings' notes had enough for two entries; they are marked
in `RECIPES.md` as what they are, and the third the painter named is a sentence inside
the first.

## Pitfalls hit

- **The first undo fix made the in-process case exact and the CLI case still wrong**,
  and the trace showed the stream was right all the way through. The canvas after the
  replay was what differed — which is how the rounding was found. Measure the thing
  after each fix, not the mechanism you fixed.
- **A replay that re-records the stream state corrupts every later undo.** The first
  version of the fix did; the replay's own marks record the seed. Carry the stored state
  across.
- **The chroma docstring quoted pigment numbers from memory and they were wrong.**
  `cadmium_red` is the most vivid in the box at `0.20`, not `cadmium_yellow`. The probe
  prints the table; the docstring quotes the probe.
- **The guide's word budget is 10,000 and the ninth exercise put it 52 over.** The fix
  was to tighten the round's own additions, not to move anything out — the cadence line,
  the planes line and the exercise are 9,975 with it.
- **The check script skips a code block containing `...` as pseudo-code**, comments
  included. Two ellipses in a recipe's comments hid it from the checker until the count
  said 13 skipped instead of 12.

## What changed, by file

**New:** `scripts/probe_greenhouse_session.py`.

**Engine:** `src/easel/session.py` — `report()` and `_pass_findings`; `_one_call`,
`_stream_state`, `_restore_stream`, `_stream_of`/`_stream_rng`; `params["rng"]` and
`params["via"]` on every record; `_clean_contour` and `_sweep_spine(smooth=)`;
`_check_pressure_on_tip`, `_check_default_direction`, `_check_clean_size`,
`_check_scumble_ends`/`_pass_lengths`; `direction=None`; `_spent_base` and the
rehearsal copy; `replay` carrying the stream; `_mass_reason`'s remedies ·
`src/easel/history.py` — exact points · `src/easel/measure.py` — `Comparison.pairs` ·
`src/easel/palette.py` — `chroma_of` · `src/easel/cli.py` — the check beside the
budget line, `run --check`, `log --check` · `src/easel/mcp_server.py` — the check in
`run`.

**Documentation:** `RECIPES.md` (four recipes, the planes clause, the wedge and the
flat's scallop) · `PAINTER.md` (the cadence, the planes line, the ninth exercise) ·
`PAINTING.md` (the staircase row and paragraph; the pairs; the worked examples' bare
calls; free-but-logged verbs; undo; the check; `chroma_of`) · `REFERENCE.md` (every new
argument, call and flag) · `CALIBRATION.md` (six sections) · `SUGGESTIONS.md` (the two
tables, the counts, *Still open*) · `LESSONS.md` (the check as built, the undo entry
settled, the re-measurement record) · `CHANGELOG.md`, `README.md`, `llms.txt`,
`PAINTINGS.md`, `examples/exercises.py`.

**Tests:** `tests/test_requests.py` — a *greenhouse sessions* section, nineteen tests ·
`tests/test_mcp.py` — the check through the wire.

## State

The suite passes with the `mcp` extra installed and without it; `ruff check src tests
scripts examples mcpb` is clean; `check_guide_blocks.py` runs every block, and
`PAINTER.md` is inside its budget with about 25 words to spare — tighter than it has
ever been. The next paragraph that wants in will have to displace one.

## Deliberately not done

- **The other arm of the split experiment.** All seven painters so far are *given
  everything* arms. The engine cannot close this one.
- **The rules card for a compacted session.** Still no compacted session to judge it
  against.
- **`PAINTINGS.md` and `README.md` do not index the greenhouse paintings as first-class
  examples**, at the owner's request recorded in Fable's notes; nothing here changes that.
- **The `flat`'s scallop on a wide band** (`0.11` peak to peak against `0.03`) is one
  measurement on one committed painting, quoted in the quiet-gradient recipe with its
  source. It has no probe in `scripts/` and no calibration section; it would want one
  before anything is built on it.
