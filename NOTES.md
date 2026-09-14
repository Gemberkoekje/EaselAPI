# Phase notes: the eighth session's round, and the first rule to leave the guide

*To understand this, start by reading [`SUGGESTIONS.md`](SUGGESTIONS.md)'s two tables
headed **What the eighth session found** and **What the eighth session asked of the
documentation** — three engine items and five documentation items, each with what was
measured before it was built — then [`CALIBRATION.md`](CALIBRATION.md)'s new sections
(*`direction` given a sequence*, *And the other wall: `n` is bounded by the patch*, and
*Aiming a film at a value*), then [`LESSONS.md`](LESSONS.md)'s paragraph under **A
separate file of warnings**, which is where the departing rule is recorded. The code is
`src/easel/session.py`; the numbers are reproducible with `python
scripts/probe_pool_session.py`.*

Every item the eighth session left is done — the first round this page ever carried as
*open*, and it is closed — and it is all in **0.3.0**, which had not been released.

## The shape of it

**It is a round of instruments, and that follows from what the session was.** It is the
split test's other arm: a painter given the method, the recipes and the reference and
nothing else. The prediction was that such an arm paints the masses as well and
improvises worse. The masses held; the improvisation held too, and what it was short of
was **three lookups it could not make**. So two of its three engine items are questions
the engine could already answer and would not say out loud, and the third is a price the
walk already knew and never quoted. Nothing here is a new mechanism.

**Every number reproduced to the stroke, and one mechanism did not survive** — which the
painter had predicted of itself, in the clause that makes this the best-labelled round
on the page:

| The claim | What measuring it found |
|---|---|
| A `direction` sequence is priced far above any single angle in it; the mechanism is that *the stack is sized for the steepest angle in the list* (**offered as a guess**) | The costs reproduce exactly — `"axis"` 4, `-17°` 7, `"cross"` 15 on the same mass. The mechanism is the **sum**: a ten-angle list costs 85, which is `4 + 5 + 7 + 7 + 9 + 10 + 10 + 11 + 11 + 11`, and the steepest alone is 11. One whole pass per angle |
| The inward scumble's `n` is bounded by the patch: `n ≤ 120 × depth`, and under about `0.07` deep no `n` fits (**arithmetic exact**) | Exact, and the wall is two walls. `0.0667` is where the recipe's *eight* rings stop fitting; where *nothing* fits is `0.042`, five rings, which is the verb's own floor for reading as a fall-off. Both are in the warning |
| A glaze's usable window is a few hundredths wide and there is no instrument for it (**measured by `CALIBRATION.md`; the cost observed**) | Held. The film's delivery is monotone and smooth in opacity but not analytic, so the instrument is a search, the way `at_value` is |

**The one documentation item that asked for nothing gets nothing**, and the register says
so rather than quietly dropping it: *the worked examples may prime toward one kind of
picture* was offered as an unmeasured opinion by a session that had itself chosen a
low-light subject. The measurement it wants is a brief written for a high-key subject
before anyone reads `paintings/`, which is a session's work rather than a release's.

## Decisions worth knowing

**`glaze(to_value=)` searches on trial canvases, and that is the whole design.** What a
film delivers is the pigment model, the tooth and whatever is already there; none of it
is available as a formula, so the honest instrument lays real films on copies until one
lands. Three things make it affordable and safe:

- it is measured over **the film's own footprint** — the pixels a probe at `opacity=1.0`
  changes — rather than a region named by hand, so the search compares like with like
  and never widens as the film strengthens;
- the trials come off a *copy* of the stroke stream (`_trial_session`), so the film that
  lands is byte for byte the film that would have landed had its opacity been typed out.
  A test holds that, and it is the property that made the feature possible at all;
- it exits as soon as a probe is within `0.002` of the target, which is a fifth of the
  precision a value plan is written to. Eight probes in practice — nothing on a halo,
  about a second on a band across the whole canvas.

**The sequence warning's threshold is the request's own words.** *Priced far above any
single angle in it*, at the same 2.5× the default-direction check uses. Two angles can
never be more than twice the dearer of them, so the pair idiom every painting in this
repository uses — `(4, 94)`, a cross at the mass's own angle — is silent by
construction, and a list that is really a stack fires. That property is worth more than
a tuned constant: it means the check cannot become noise on correct code.

**The comb floor gets a rounding tolerance and the comment says why.** A polygon of an
ellipse comes a hair short of its own extents, so the `n` sitting exactly on the boundary
derives `0.024998` rather than `0.025`, and a warning reading *0.025, under the 0.025*
is noise. The check compares against `0.0245` and the remedy's arithmetic uses the same
number, so the two cannot disagree.

**A rule left the front page, and it left because the budget made it.** `PAINTER.md` is
held to 10,000 words and had 25 to spare; the two documentation items that belong on it
are 74. The growth rule's standing answer is that a rule the engine checks at the call
can leave the guide, and none had. *You will under-vary your marks* is the first: the
post-pass check names both halves of it after the pass that did it, with the numbers. It
is in `PAINTING.md` — moved, not cut — with a paragraph saying where it came from and
that whether this works is still unknown. The front page is at 9,996.

## Pitfalls hit

- **`opacity` had to become `None`-defaulted to tell *given* from *default*.** The same
  shape as `direction=None` last round. `GLAZE_OPACITY = 0.18` is the value; the
  signature says so and a test holds that the default film is the film it always was,
  byte for byte.
- **A target a hair *below* the field raises as out of reach, and that is correct but
  looks odd.** Ask for `0.317` under paint reading `0.319` and the film cannot get
  there — it can only travel away from the field. The message names both ends, which is
  what makes it actionable; `at_value` behaves the same way.
- **The first sequence warning recommended an alternative that cost more.** On a mass
  where three near-parallel angles cost 13, the axis cross costs 15. The line now states
  the cross's price rather than promising a saving — a warning that oversells its remedy
  is a warning that gets ignored the second time.
- **A test helper named `_scumbled` already existed in `tests/test_requests.py`** and the
  new one shadowed it silently, breaking three passing tests with a `TypeError` that
  named neither. Module-level helpers in a 1,900-line test file need checking before
  they are added.
- **A recipe's code block has to run under the checker's preamble.** The point-in-shape
  block was written with `pool` and `rng`, neither of which exists there; it uses `mass`
  and its own `numpy` import now. `check_guide_blocks.py` catches this and the count of
  skipped blocks is the thing to watch, because a block containing `...` is skipped
  rather than failed.

## What changed, by file

**New:** `scripts/probe_pool_session.py`.

**Engine:** `src/easel/session.py` — `glaze(to_value=)` and `_glaze_opacity`, with
`GLAZE_OPACITY` and the four search constants; `_check_inward_comb` and
`_INWARD_MIN_RINGS`; `_check_direction_sequence`, called from `block_in` and from
`_plan_price`; the `scumble` and `block_in` docstrings for both windows.

**Documentation:** `RECIPES.md` (the two glow recipes told apart in the index and in the
first entry; point-in-shape where small marks go into a mass) · `PAINTER.md` (the pairs
question in step 3; a ground of its own under *Getting started*; *under-vary your marks*
removed) · `PAINTING.md` (that paragraph, with its provenance) · `REFERENCE.md`
(`glaze(to_value=)`, `shape.inside`) · `CALIBRATION.md` (three sections) ·
`SUGGESTIONS.md` (the round closed, two tables, the counts, the departing rule) ·
`LESSONS.md` (the first rule to leave, the re-measurement record at twenty claims and
five failures, and the standing ask that painters label which half of a finding is
measured) · `CHANGELOG.md`, `README.md`.

**Tests:** `tests/test_requests.py` — an *eighth session* section, thirteen tests.

## State

The suite passes; `ruff check src tests scripts examples mcpb` is clean;
`check_guide_blocks.py` runs every block, and `PAINTER.md` is at 9,996 words against its
10,000 budget. Version bumped to 0.3.0 in `pyproject.toml`, `src/easel/__init__.py` and
`server.json`.

## Deliberately not done

- **Whether a rule can safely leave the guide.** The experiment is now *runnable* rather
  than run: it needs a fresh session painting from a guide with the rule missing.
- **The high-key brief.** The fifth documentation item's own measurement, and it has to
  be written before anyone reads `paintings/`.
- **`glaze(to_value=)` has no public "what opacity would that be" call.** The chosen
  opacity is in the log and that is enough for the rehearse-then-commit loop; a second
  entry point is worth adding only if a painter asks for one.
- **The MCP server does not expose `glaze`**, and did not before. Nothing in this round
  changes the wire.
