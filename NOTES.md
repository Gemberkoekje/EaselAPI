# Phase notes: the ninth session's round, painted twice

*To understand this, start by reading [`SUGGESTIONS.md`](SUGGESTIONS.md)'s two tables
headed **What the ninth session found** and **What the ninth session asked of the
documentation** — four engine items and ten documentation items, each with what was
measured before it was built — then [`CALIBRATION.md`](CALIBRATION.md)'s new section
*What a solid mass actually lands at* and the clause under *The band, and the brush
that closes its joins*, then [`LESSONS.md`](LESSONS.md)'s **About the protocol**, which
now carries five questions rather than three. The code is `src/easel/session.py`; the
numbers are reproducible with `python scripts/probe_heron_session.py`.*

Every item both heron paintings left is done, and it is all in **0.3.0**, which had not
been released.

## The shape of it

**This is the round where the register measured itself.** The ninth session is the
restricted arm again — the method, the recipes and the reference, plus `DIAGNOSIS.md`,
which no earlier session had — and two of its three engine items are *measurements
taken against an open item on this page* rather than new complaints. One of them
settles the eighth session's guess, and settles it against the guess. That is the arm
working as intended.

**Two claims did not survive, and neither was the usual kind:**

| The claim | What measuring it found |
|---|---|
| A `direction` sequence is *sized for the steepest angle in it* (the **eighth** session's guess, which it labelled as one) | The cost is the exact sum of the angles' own prices — nine measurements for nine, on three shapes — and in paint `direction=[0, 90]` logs the `0°` stack whole and then the `90°` stack whole. The price walk had already been written from the mechanism rather than the guess, so nothing had to move |
| *A warning when an oriented tip is handed a `size` under about `0.008`* (**measured**, with a table behind it) | The finding is right and the unit is wrong. The cliff is at four **pixels**: `size` is a fraction of the canvas long side, so `0.008` is 2.4px on a 300px canvas — already dead — and 9.6px on a 1200px one. Measured on three canvases the knee is at the same pixel width every time |
| *The across-band ripple counts canvas texture on a rough ground* (observed, from a measurement the painter then discarded) | It does not. The metric reads identically on `smooth`, `linen` and `rough` to four decimals at every window width, and on a *starved* pass `rough` reads **lower**. What it is sensitive to is the **window**: `0.0008` across the full width against `0.0020` through a narrow column, for the same paint |

The second of those is the interesting one for the method, and it is now at the foot of
`SUGGESTIONS.md`: **a measurement is only as general as the conditions it was taken
under.** `CALIBRATION.md`'s standing rule already asks every number to state what it was
measured on; this is what happens when the number states it and the *proposal built on
it* forgets.

**The two paintings separate two kinds of fault cleanly.** Every fault that was a
lookup got fixed by reading the withheld files — `compare({place: value})` ran on the
empty canvas and caught two merges before a stroke, the graded field went down in pass
two with the light already in it, every soft passage took its brush from the verb. The
one fault that was judgement — a bird's body as a smooth mass with marks laid on it —
repeated itself exactly, with the recipe open and quoted in the painter's own notes.

## Decisions worth knowing

**The new check rule is narrow on purpose, and the same session is why.** Its third
engine item is a rule it learned to ignore (the bristle floor, twenty-eight times), so
a new rule that misfires would have cost the other six their credibility. *A graded
passage laid too narrow* fires only on three or more long parallel marks **at three or
more colours** whose step is over half the narrowest brush among them. The colour
condition is what keeps every `block_in` out of it: a mass is one colour however its
passes are spaced, and at `density=1.0` its passes are `0.55` of a brush apart and
right to be. The four-brush ceiling keeps three trunks or three cables out. Checked
against the session's own dawn band, a verb-sized scumble, a narrow one, block-ins at
three densities, a sweep, and three parallel trunks.

**The tip-pixels warning lives in `_resolve_brush`, which is unusual here.** Every
other check is called from its verb with an explicit `stacklevel`. This one keys on
`size` being *named at the call* — a mass hands its own passes the resolved `Brush`
with no `size=`, so it fires once per call rather than once per pass, from every verb
at once, and from `cost()`. A `Brush` built by hand and handed in whole is left alone,
the way a named scumble brush is.

**The bristle floor was narrowed by counting the paintings, not by judgement.** Every
small-bristle call site in both heron paintings names an explicit `load` and not one
uses the preset's own `0.9` — 15 of 16 at or under `0.6` in the first and 12 of 12 in
the second. So the rule was firing on nothing it was written for. `0.6` is the top of
the run-out window `CALIBRATION.md` already publishes; it is not a new number.

**A second rule left the front page, and neither left on its merits.** `PAINTER.md` is
held to 10,000 words and had 27 to spare after 0.3.0; this round needed three items on
it. *You will use too many strokes on detail* is in `PAINTING.md` beside *you will
under-vary your marks*, and its summary bullet in *The first hour* went with it —
a rule that has left the guide should not still be in the guide's own recap. **The word
budget is now the binding constraint on every documentation round**, which is worth
raising with the owner rather than paying twice more without saying so.

**`DIAGNOSIS.md` is not changed on n=1.** The proposal that would fix what the session
saw — rows carrying the repair as well as the pointer — is the fourth copy `LESSONS.md`
refuses. So it is a protocol question instead, and `LESSONS.md`'s **About the protocol**
has two more: hand the index as a file to grep and record which arm was run, and decide
whether a restricted arm gets an index whose rows point into files it does not have.

## Pitfalls hit

- **The first pass at the graded-band rule would have fired on every `block_in` in the
  repository.** `_pass_step` is `size * (1 - 0.45 * density)`, so a mass's passes are
  always under two brushes apart — the exact condition the rule tests. The colour
  condition is not a refinement, it is the whole rule.
- **A test helper shadowed an existing one again.** `_scumbled` last round, and this
  round's first draft reached for the same trick. Three passing tests broke with a
  `TypeError` naming neither. Grep the file before adding a module-level helper.
- **An existing test asserted silence where the new warning correctly speaks.** The
  clean-edge test laid a `flat` at `size=0.005` on a 320px canvas under
  `simplefilter("error")` to prove the *share* rule stays quiet below its threshold —
  and that brush is 1.6 pixels wide. The assertion is about that warning now, not about
  silence, which is what it always meant.
- **Comparing pass angles element-wise between two stacks does not work.** Each pass
  wanders a degree or two off its line and the wander comes off a stream the first
  stack has already spent, so the same angles do not repeat. The claim is about which
  way each *half* of the sequence runs, and the test says that.
- **A recipe's code block with `...` in a comment is silently skipped** by
  `check_guide_blocks.py`. Watch the skipped count, not just the failed one — it is the
  second round running that this has caught something.
- **`DIAGNOSIS.md` has a 130-line cap and this round wanted five rows and a
  paragraph.** Four existing rows pointing at one target were merged, which is what the
  cap is for.

## What changed, by file

**New:** `scripts/probe_heron_session.py`.

**Engine:** `src/easel/session.py` — `_graded_band` and the seventh check rule, with
`_REPORT_BAND_FLOOR`, `_REPORT_BAND_MARKS` and `_REPORT_BAND_COLOURS`;
`_REPORT_STARVED_LOAD` narrowing the bristle floor; `_check_tip_pixels` and
`_CHISEL_MIN_PX`, called from `_resolve_brush`; the axis-cross angle normalised in
`_check_direction_sequence`; `report()`'s and `sample()`'s docstrings.

**Documentation:** `RECIPES.md` (*a graded field that is most of the picture*; the
brush-and-step clause in *a passage brightening toward one side*) · `PAINTER.md` (the
pairs clause, the veil-of-light bullet, the pencil clause; *too many strokes on detail*
removed, and its recap bullet with it) · `PAINTING.md` (that paragraph; *Without a
reference*; `sample`) · `REFERENCE.md` (`direction`, `solid`, `sample`, the check's
rules) · `CALIBRATION.md` (*What a solid mass actually lands at*; the ripple-window
clause) · `DIAGNOSIS.md` (five rows, four merged, the follow-the-pointer note) ·
`PAINTINGS.md` (the pass-script convention and the drawing) · `SUGGESTIONS.md` (the
round closed, four tables, the counts, the re-measurement record at twenty-eight
claims and seven failures) · `LESSONS.md` (two protocol questions, the seven rules,
the second departing rule) · `CHANGELOG.md`.

**Tests:** `tests/test_requests.py` — a *ninth session* section, thirteen tests.

## State

The suite passes with the `mcp` extra and without it; `ruff check src tests scripts
examples mcpb` is clean; `check_guide_blocks.py` runs every block; `PAINTER.md` is at
9,973 words against its 10,000 and `DIAGNOSIS.md` at 128 lines against its 130. Version
bumped in `pyproject.toml`, `src/easel/__init__.py` and `server.json` -- to 0.4.0
at the time, renumbered to 0.3.0 before release because 0.3.0 was never tagged.

## Deliberately not done

- **Which of the three pencil diagnoses is right.** All three are made as documentation
  fixes; picking between them needs a painter working from a guide that carries all
  three. The count is in the probe so the next round can say whether it moved.
- **The depth-order paragraph's rewrite.** Four failed runs now, and this one is a
  different shape from the other three. Still a design job with a measurement attached,
  and still open in `LESSONS.md`.
- **The grep arm of the `DIAGNOSIS.md` experiment**, and the high-key brief the eighth
  session's last item wants. Both are a session's work.
- **Whether a rule can safely leave the guide**, now twice over.
- **The `PAINTER.md` budget itself.** It is at its ceiling and two rounds running have
  paid for their items by evicting rules. Raising it is explicitly forbidden by the test
  that holds it, so the question is whether the eviction mechanism is doing what it was
  meant to or whether the front page needs a different shape. That is the owner's call.
