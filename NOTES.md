# Phase notes: the fourth session's engine round, and 0.2.0

*To understand this, start by reading [`SUGGESTIONS.md`](SUGGESTIONS.md)'s new section
**What the fourth session found** — the six requests and what each one turned into —
then [`CALIBRATION.md`](CALIBRATION.md)'s new **The paint and the view of it**, then
[`LESSONS.md`](LESSONS.md)'s new **A default is worth more than a warning** and the
rewritten **Check the painters' numbers**, which is where this round's method lives.
The code is `src/easel/session.py`; the numbers are reproducible with
`python scripts/probe_fourth_session.py`.*

Every open item from the fourth painting session is done — six engine, five
documentation — and the release is cut as **0.2.0**, with a `CHANGELOG.md` that PyPI
links from the project sidebar.

## The shape of it

**Two of the six requests were answered by measuring them, and the measurement said
there was nothing to fix.** That is the whole character of this round. Both were marked
*observed* rather than *measured* by the session that raised them, and both reasoned
back from a real failure to a mechanism that sounded right:

| The claim | What measuring it found |
|---|---|
| The rendered view lifts a solid mass off its planned value, which is why four masses came back as bright bars while `compare()` read clean | The view and the paint agree to `0.000` over a mass at every load, value and ground tried. The relief is a *gradient* — it lifts one side of each ridge of paint and drops the other by as much, so it cancels over any area bigger than a ridge. Worst single pixel anywhere: `0.038` |
| A shape blocked in at `overhang=0` is left bare at its pass ends by the wobble | Laid solid: `0%` bare at every setting. At the default load: `8.7%` bare at the ends — and `14%` along the *sides*, which `overhang` cannot touch. It is the comb and the brush running dry |

Both still produced work, because **what the session actually lacked in the first case
was a way to ask**: `s.sample(place, rendered=True)` samples the view, and `compare()`'s
table now names which of the two surfaces it measured. A warning that can never fire was
not built, and `SUGGESTIONS.md` says so beside the request rather than quietly dropping
it.

The other four were real and all four came down to a **default or a message**:

- `smudge`'s default `size` was `0.07`. Measured, what `size` buys stops at about `0.02`
  (half the join, and no more) while the reach keeps growing — `1.3%` of canvas height
  at `0.02`, `4.4%` at `0.07`. The default is now `0.02` and past `0.03` it warns.
- `scumble` on a band kept a preset's brush, which lands at one to one and a half pass
  steps — measurably the worst width of any tried. It now derives `3 × extent / n`, the
  mechanism the `inward` direction has used since the third session, and warns under two
  steps.
- `overhang`'s "ends" rotate with `direction`, and nothing said so.
- `solid=`, `glaze=` and five other neighbours' keywords were swallowed by
  `**brush_overrides` and came back as `Brush.__init__() got an unexpected keyword
  argument`. They now name the call that takes them, and `Region` unpacks.

## Decisions worth knowing

**Changing a default is the right fix and it is a behaviour change.** A saved `.easel`
replays exactly as it was painted — every stroke's own brush arguments are in the log —
but a *script* that leaves `size` off a `smudge` or a `scumble` paints something
different after this release. That is why it is 0.2.0 and not 0.1.2, and why
`CHANGELOG.md` opens by saying which defaults moved. Nothing in `tests/golden_cases.py`
or `examples/` passes those calls without a size, so no golden image moved.

**The guide's own examples were the transmission route.** Every `smudge` in
`PAINTER.md`, `RECIPES.md` and `PAINTING.md` ran at `0.04`–`0.09`, all past the window,
while three paragraphs of correct prose told the reader to keep it small. The examples
now leave `size` off entirely. *When a document has to warn this hard, the suspect is
the default* — written up in `LESSONS.md`.

**`CALIBRATION.md`'s old smudge window was `0.035`–`0.045`, and it is now contradicted.**
It was not wrong about what it measured; it measured only what a smudge *buys* and never
what it costs, on a canvas nobody recorded. Both halves are in one table now, with its
conditions, and the old table is kept underneath with a line saying what it is good for
(what a second and third pass do) and what it is not.

**The five documentation items were four one-line fixes and one deletion.** The
subject-share contradiction is resolved by saying *when* the share is compared (at the
moment the subject is finished, after which the last-third rule is meant to pull it
down); a checklist line asks whether the bands are in the marks or in the subject that
was chosen; step 1 says what the pencil buys that `preview` does not; `CALIBRATION.md`
is cited from the rules that have numbers in it rather than only from a contents table.
The fifth asked for a warning about planned-versus-seen value, and the honest content
for it turned out to be that they are the same number.

**The changelog covers from the first tag, because there is no `v1.0`.** The repository's
tags are `v0.1.0` and `v0.1.1`; `CHANGELOG.md` has an entry for each, plus 0.2.0
carrying everything merged since `v0.1.1` (ten PRs: the guide split, the third session's
engine round, the guide shipping inside the wheel, the `.mcpb` bundle, Python 3.14, the
registry publishing, the `__version__` drift fix). PyPI renders `[project.urls]`
`Changelog` as a sidebar link — that is the whole of wiring it up.

## Pitfalls hit

- **The first measurement of the relief gap was taken with the wrong metric and said
  `0.000` for the right reason by luck.** A mass's *mean* cannot show a gradient effect;
  it took a per-pixel distribution, an edge-strip measurement and an end-to-end check of
  five rendered outputs before the answer was trustworthy. If you re-open this, measure
  the distribution, not the mean.
- **A smudge run along a boundary that is not where you drew it does nothing**, and
  measures as `0.000` at every size. `block_in` lays paint half a brush past the outline,
  so a mass blocked in at `size=0.10` puts its own boundary 30px from where the shape
  says. Every probe here finds the join empirically (steepest row) instead of assuming
  it; the first three attempts did not, and produced a table of zeroes.
- **`pytest.mark.filterwarnings` patterns are regexes and need raw strings.**
  `"ignore:smudge\(size=:UserWarning"` is a `SyntaxWarning` and then a silent
  non-match.
- **Three existing tests and one golden fixture now call into the new warnings on
  purpose** — they pin behaviour at sizes the engine advises against. Each is marked or
  wrapped at the call site with a comment saying why, rather than being moved inside the
  new windows, which would have changed what they measure.

## What changed, by file

**New:** `CHANGELOG.md`, `scripts/probe_fourth_session.py`.

**Engine:** `src/easel/session.py` — `sample(rendered=)`, `SMUDGE_SIZE`/`SMUDGE_MAX` and
`_check_smudge_size`, `_LINEAR_STEPS`/`_linear_size`/`_check_linear_brush`,
`_NOT_BRUSH_FIELDS`/`_check_brush_overrides`, and the `block_in`/`scumble`/`smudge`
docstrings · `src/easel/regions.py` — `Region.__iter__` · `src/easel/measure.py` —
`Comparison.measured_on` and the table's second header line.

**Documentation:** `CALIBRATION.md` (*The paint and the view of it*; the smudge window;
the band's brush-in-steps and opacity tables; `overhang`'s rotation and the bare-boundary
measurement) · `REFERENCE.md` (the owning call beside `solid`, `glaze`, `overhang`,
`density`; the smudge default; both scumble derivations; `shape.box` unpacking;
`sample(rendered=)`) · `PAINTER.md` (the smudge window and examples; the pencil in step
1; the banding-in-the-subject checklist line; when the subject's share is measured;
`CALIBRATION.md` given a *moment* rather than a curiosity) · `PAINTING.md` (the
rendered/paint pair; `overhang`'s rotation; the last-third arithmetic; the API lines) ·
`RECIPES.md` (smudge sizes) · `SUGGESTIONS.md` (the fourth session's rows; *Still open*
moved to the front and reduced to two genuinely open things) · `LESSONS.md` (the defaults
lesson; the re-measurement record and what shape of claim fails it; current counts) ·
`README.md`, `llms.txt` (the fourth round, the changelog).

**Release:** `pyproject.toml` (0.2.0, and the `Changelog` URL) · `src/easel/__init__.py`
· `server.json` (both copies).

**Tests:** `tests/test_requests.py` — twelve tests in a *fourth session* section, two of
which guard an answer that is not the one the request asked for ·
`tests/golden_cases.py` — the pinned wide smudge, with its reason.

## State

`596 passed, 3 skipped` (was `584 passed`); `ruff check src tests scripts examples mcpb`
clean; `check_guide_blocks.py` `75 ok, 0 failed, 12 skipped` and `PAINTER.md` 9,769 words
against its 10,000 budget — **231 to spare, which is the tightest it has been**. The next
finding that wants to be a paragraph will have to displace one.

## Deliberately not done

- **The post-pass check** (`Session.report()` / `easel run --check`), still the cheapest
  open item, now with three of its five candidate rules scored against a real painting in
  `LESSONS.md` — and one candidate ruled out, because the gap it would check for is
  `0.000`.
- **The other arm of the split experiment**: a fresh session given only the method, the
  recipes and the reference. The fourth session is the "given everything" arm and points
  the way the prediction did.
- **The fourth painting is not in `paintings/`.** `laundromat_night/` is untracked
  working material, and `PAINTINGS.md` still reads three paintings. Adding it is a
  separate piece of work with its own verification (the pass scripts have to rebuild the
  PNG byte for byte).
- **The rules card for a compacted session.** Still no compacted session to judge it
  against.
