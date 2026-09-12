# Phase notes: the third session's engine list

*To understand this, start by reading `SUGGESTIONS.md` from "Suggestions from a third
session" (line ~686) — the six engine items and the **bold** note under each saying
what it became — then `tests/test_requests.py` from its third-session banner, which is
one test per item, and then the three changed methods in `src/easel/session.py`:
`scumble`, `sweep` and `block_in`.*

All six engine items on the lighthouse session's list are done, including the one that
was a question. The guide list under it is still open, and so is the synthesis after it.

## What each item became

| # | Item | Where |
|---|---|---|
| 1 | Inward scumble sizes its brush from its ring step, and warns when handed a wider one | `session.py`: `_inward_size`, `_check_inward_brush`, `_inward_depth` |
| 2 | `easel run p.easel a.py b.py [--rehearse]` runs passes in order against one session or one copy | `cli.py`: `run_scripts`, `_cmd_run` |
| 3 | A rehearsal carries the painting's last look, so `look(diff=True)` tints what the pass would change | `session.py`: `_trial_session` |
| 4 | A pressure list (and an asymmetric named profile) is read in canvas order on every pass | `session.py`: `_canvas_order_pressure`, threaded through the path generators |
| 5 | `s.sample(place)` returns the colour already there, as the engine's own array | `session.py`: `Session.sample` |
| 6 | The contour of `edge="clean"` does not wander; `sweep` takes `wander=` | `session.py`: `sweep`, `_sweep_paths`, `_sweep_wobble` |

## Decisions worth knowing

**Everything was re-measured before it was built.** `scripts/probe_third_session.py`
reproduced all seven of the session's findings exactly, so the list was taken as
accurate and the work went into acting on it rather than re-litigating it.

**Item 4 was asked for two ways and got the better one.** The item offered
`alternate=False` as an alternative. Turning the alternation off would stack every
pass's run-out along one edge — which is the thing the alternation exists to prevent,
and is written down as such in `_block_paths`' own docstring. So the paint still
alternates and only the *pressure* is reversed to compensate. It was extended to
`sweep`, which had the same defect for the same reason; the item only named `block_in`
and `scumble`.

**Item 6 was a question, and the answer contradicts the fix it proposed.** The item
guessed `jitter=0` on the brush. Measured over ten seeds, the brush's jitter moves the
contour's accuracy not at all (seed-to-seed spread 3.45px against 3.32px); the sweep's
own wobble moves it from 3.32px to 1.14px. The lever is `sweep(wander=)`, not the tip.

## Pitfalls hit, and what they cost

- **Replay stability is the binding constraint on this codebase.** Goldens are hashed
  (`tests/test_golden.py`) and the paintings in `paintings/` rebuild from their own
  scripts to a matching sha256. Three choices fall out of it:
  - `_canvas_order_pressure` passes `taper`, `even` and `swell` through **untouched**
    rather than reversing them into an equal-but-differently-computed array. Every
    painting here was laid at `taper`; reversing it numerically would have moved every
    stored hash by ~1e-5 for no gain.
  - `_sweep_wobble(wander=False)` still **takes its draw from the generator** and
    discards it. Skipping the draw would shift the stream under every mark laid after
    the contour.
  - Nothing that existed used a pressure list on `block_in`/`scumble`/`sweep`, or
    `direction="inward"` without an explicit `size=` — both checked before changing
    defaults. That is why items 1 and 4 could land as behaviour rather than as flags.
- **Multi-script `run` had to be provably equivalent to running the scripts one at a
  time**, or it would be a second, subtly different way to paint. Each script therefore
  gets a **fresh scope with the prelude re-run in front of it** — the canvas carries
  over between passes, the namespace does not. `test_running_two_passes_together_is_
  running_them_one_after_the_other` asserts the two paths pixel for pixel.
- **The path generators now yield `(path, flipped)`** rather than a bare path
  (`_shape_paths`, `_angled_paths`, `_block_paths`, and `(kind, path, flipped)` /
  `(k, path, flipped)` for `_sweep_paths` and `_ring_paths`). The cost counters consume
  them as `sum(1 for _ in ...)` and were unaffected, but any new consumer must unpack.
- **Measuring a silhouette needs a before/after diff of `canvas.rgb`, not a threshold
  against a corner pixel.** The ground's own texture varies with the seed, so a
  "painted or not" test anchored on one pixel reported 85px contour errors that were
  canvas grain. Cost about twenty minutes of chasing a non-existent bug.
- `Session.sample` reads `canvas.rgb` (the paint), not `composite()` (the view). The
  relief shading `look` draws is light on the surface, not pigment in it; mixing it in
  would bake a highlight into the sampled colour.

## Deliberately not done

- **The MCP `run` tool still takes one script.** Item 2 is about the shell path, and a
  server client can already concatenate. If it is wanted there, `run_scripts` in
  `cli.py` is the shared entry point and takes `(source, name)` pairs.
- **`parse_color`'s reading of a raw `(r, g, b)` triple as sRGB is unchanged.** It is
  consistent with how a hex string is read, and item 5 gives the painter a way to never
  need the conversion. Only the documentation of it changed.
- **The third session's guide list** (recipes page, the two-goes data point, the glaze
  and colour note, and the rest) and the synthesis section after it. Those are guide
  items, not engine ones. The guide changes made here are only the ones the engine
  changes made *wrong*: the inward-scumble rule in `PAINTER.md`, the flat-middle
  reading in `CALIBRATION.md`, and the `wander` / `size` / pressure / `sample` /
  multi-script rows in `REFERENCE.md`.

## What this moved in `paintings/`

Item 6 changes pixels wherever `block_in(edge="clean")` was used, which is four masses
in the lighthouse and two in the car wash. Measured by rebuilding each painting from
its own scripts on the engine before and after:

| | committed vs **old** engine | committed vs **new** engine | old vs new (this change) |
|---|---|---|---|
| lighthouse | 0.15% of pixels, none by more than `1` | 8.89%, 1.57% by >`8` | 8.79%, 1.57% by >`8` |
| car wash | **42.19%**, 15.37% by >`8` | 41.44%, 15.13% by >`8` | 9.35%, 1.15% by >`8` |

So the lighthouse *did* reproduce byte for byte (the 0.15% is numpy rounding a handful
of pixels by 1, which is what `golden_cases.close_enough` exists for), and this change
is what moved it. Its `NOTES.md` now says so; the PNG has **not** been re-rendered,
because the painting is somebody's finished picture and re-rendering it is a separate
decision from changing the engine.

**The car wash was already stale before any of this**, by 42% of its pixels, and its
`NOTES.md` claims 206 strokes where its scripts now lay 211 — on the old engine too.
That predates this work (most likely `db49e2e`, which changed `edge="clean"` and
`solid` after the painting was made) and is left alone here rather than quietly folded
into an unrelated change.

## State

`498 passed, 79 skipped` (was `485 passed, 79 skipped`); `ruff check` clean. The
thirteen new tests are all in `tests/test_requests.py` under the third-session banner,
and each was verified to **fail** with its fix reverted.
