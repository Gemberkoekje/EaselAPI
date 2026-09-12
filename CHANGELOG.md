# Changelog

Every release of [`easel-paint`](https://pypi.org/project/easel-paint/), what changed in
it, and why. PyPI links this file from the project sidebar (the `Changelog` entry under
`[project.urls]` in `pyproject.toml`), so this is the page a painter lands on from the
package page.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project uses [semantic versioning](https://semver.org/spec/v2.0.0.html). Before 1.0.0 a
minor bump is where behaviour is allowed to move: **a version already saved to an
`.easel` file always replays as it was painted**, because every stroke's own brush
arguments are in the log, but a *script* that leaves a default off can paint something
different after a minor release. Each entry below says which defaults moved.

The engine's own record of *why* a rule is a rule lives elsewhere and is not duplicated
here: measurements in [`CALIBRATION.md`](CALIBRATION.md), the requests painters made and
what was done about them in [`SUGGESTIONS.md`](SUGGESTIONS.md), and the method in
[`LESSONS.md`](LESSONS.md).

## [Unreleased]

Nothing yet.

## [0.2.0] — 2026-09-12

The fourth painting session's six engine requests, the guide split by function, the
third session's engine round, and the package finally carrying the guide it is useless
without. Two of the six requests **did not survive being re-measured**, and the entries
below say so where that is the case — checking a painter's numbers before building on
them is the rule in `LESSONS.md`, and it changed what was built twice here.

### Added

- `s.sample(place, rendered=True)` — sample the surface `look()` and `export()` draw
  (relief, and graphite the paint has not buried) instead of the pigment, so *is my mass
  darker than it looks?* is one line rather than a belief.
- `easel guide` prints the guide from inside the installed package, and the wheel now
  carries `PAINTER.md`, `PAINTING.md`, `RECIPES.md`, `REFERENCE.md` and
  `CALIBRATION.md` as `easel/docs/*.md`. `pip install easel-paint` used to hand a
  painter sixteen modules and none of the method.
- `easel run p.easel pass_a.py pass_b.py [--rehearse]` runs several passes in order
  against one session, or one copy of it. A pass that goes on top of another pass has to
  be judged on it.
- `s.sweep(..., wander=)`, off for the contour of `block_in(edge="clean")`: measured,
  the sweep's own wobble is what moves a drawn contour off its line (3.3px to 1.1px), and
  the brush's `jitter` moves it not at all.
- A rehearsal carries the painting's last look, so `look(diff=True)` inside a rehearsed
  pass tints what that pass would change.
- `PAINTING.md` (the reasons) and `RECIPES.md` (fourteen procedures collected out of the
  paintings' own pass scripts) — both moved out of `PAINTER.md` rather than written new.
- A one-click `.mcpb` desktop bundle, built and verified by the release workflow, and an
  MCP Registry entry published in step with each release.
- Python 3.14 is supported and tested.
- `scripts/probe_fourth_session.py` and `scripts/probe_third_session.py` — the probes
  behind the numbers in `CALIBRATION.md`, runnable.
- This changelog.

### Changed

- **`smudge()`'s default `size` is `0.02`, was `0.07`**, and anything past `0.03` now
  warns. Measured on a steep join: what `size` buys stops at about `0.02` (a single pass
  takes roughly half the join out and no more) while what it costs keeps growing — at
  `0.07` one pass drags the lighter mass `4.4%` of the canvas height into the darker,
  against `1.3%` at the default. That is the pale finger-shaped lobe four sessions have
  described. Sizes the guide's own examples used were off the end of that table.
- **`scumble()` on a band picks its own brush**, `3 × extent / n`, when no `size=` is
  given — the mechanism `direction="inward"` has used since 0.1.0, now on both
  directions. A preset's default lands at one to one and a half pass steps on an ordinary
  band, which measures as the worst banding of any width tried. Handed a brush under two
  steps it warns and says how many steps wide it is.
- A keyword that is **not** a brush field now raises a `TypeError` naming the call that
  does take it — `solid=` belongs to `block_in`, `glaze=` to `stroke` — instead of
  `Brush.__init__() got an unexpected keyword argument` from a class the painter never
  mentioned.
- `Region` unpacks: `x0, y0, x1, y1 = shape.box`. It raised `'Region' object is not
  iterable`, which said nothing about where the four numbers were.
- `compare()`'s table says which of the two surfaces it measured (the paint) and names
  the call that reports the other one.
- A `pressure` list is read in canvas order on every pass of a `scumble` or a `sweep`,
  so a passage meant to brighten toward one side can be laid with the verb. The paint
  still alternates direction pass to pass; only the profile is compensated, so nothing
  painted before this moves.
- `s.sample(place)` returns the engine's own linear `float32` array, averaged over a
  shape rather than over its box.
- `PAINTER.md` is the method only — 17,625 words became 9,463, with a 10,000-word budget
  asserted by `tests/test_guide.py`. Not one word was deleted; the essay moved to
  `PAINTING.md`.
- `__version__` is checked against `pyproject.toml` by a test. It had already drifted
  once: the whole of 0.1.1 advertised itself to MCP clients as 0.1.0.

### Fixed

- `block_in`'s `overhang` is documented as what it is: it lengthens each pass past **the
  ends of the pass**, and which two edges those are turns with `direction` — so on a mass
  swept vertically it runs the paint down off the mass's foot. Measured, with the
  box-versus-shape default difference given its own clause. Two masses in one painting
  were spoiled learning this.
- `scumble`'s opacity is documented as what it is: the passes overlap, so a low opacity
  accumulates back toward full colour instead of thinning the passage. From `0.40` up it
  delivers the same passage to within `0.04`. To keep a passage quiet, mix its two
  colours closer together.
- The inward scumble's brush comes from its ring step, and `depth` is computed in one
  place so the step a size is derived from and the step the rings are laid on cannot
  drift.

### Measured, and not changed

Two requests were acted on by measuring them first, and the measurement said no:

- **The view does not lift a solid mass off the value it was mixed at.** A session
  priced this as its most expensive item — four masses laid at planned values that came
  back as bright bars while `compare()` reported the plan clean. Over a mass the rendered
  view and the sampled paint agree to `0.000` at every load, value and ground measured;
  the relief is a *gradient*, so it brightens one side of each ridge of paint and darkens
  the other by as much. `solid=True` costs nothing in the view. What was missing was the
  ability to ask, which `sample(rendered=True)` and `compare()`'s new label now give.
- **`overhang=0` does not leave a shape's boundary bare**, so the warning that was asked
  for is not built. Laid solid, the strip inside the pass ends comes back `0%` unpainted
  at every setting; at the default load it is `8.7%` bare — and the strip inside the
  *sides*, where `overhang` does nothing at all, is barer still at `14%`. That is the
  comb's own texture and the brush running dry, and its condition is `block_in`'s own
  defaults.

### Removed

- `glama.json` and `smithery.yaml`. Neither aggregator reads a file from the repository
  any more, and Smithery discontinued the stdio form the file was written in.

## [0.1.1] — 2026-09-12

### Fixed

- The registry marker in `README.md` and a `server.json` that 0.1.0 shipped without.
  0.1.0 published from a commit two merges older than the one that set the release
  version: its `pyproject.toml` already said `0.1.0`, so the tag guard compared `0.1.0`
  to `0.1.0`, matched, and published the older tree. No engine change — the rule the
  version comment states (edit, commit, merge, then tag *that* commit) is the part that
  has to hold.

## [0.1.0] — 2026-09-12

First public release: the whole engine as it stood after two painting sessions and the
two engine rounds they bought.

### Added

- The painting engine — procedural brush tips, paint load and run-out, wet-into-wet
  pickup, canvas tooth, subtractive pigment mixing, impasto relief, a graphite layer,
  undo and replay from the seed.
- The painter's vocabulary: `stroke`, `dab`, `block_in`, `sweep`, `scumble`, `cover`,
  `smudge`, `glaze`, `pencil` and `erase`, over regions, grid cells, spans and shapes
  (`polygon`, `ellipse`, `blob`, `hull`, `ribbon`, `union`, `s.circle`).
- One plan object shared by `cost`, `preview`, `rehearse` and `paint`, so what is tried
  and what is committed cannot diverge; `Session(budget=)` and the budget line;
  `--rehearse`, which commits nothing and seeds the next real marks so a rehearsed pass
  lands pixel for pixel.
- `compare("ref.jpg")` and `compare({place: value})` — the second is how a painter with
  no photograph checks the canvas against their own written value plan.
- `easel` (the CLI), `easel-mcp` (the MCP server), and the guide:
  `PAINTER.md`, `REFERENCE.md`, `CALIBRATION.md`, `LESSONS.md`.

[Unreleased]: https://github.com/Gemberkoekje/EaselAPI/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/Gemberkoekje/EaselAPI/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/Gemberkoekje/EaselAPI/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/Gemberkoekje/EaselAPI/releases/tag/v0.1.0
