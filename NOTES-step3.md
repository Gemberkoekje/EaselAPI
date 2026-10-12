# Step 3 of `PLAN-0.9.0.md`: paint held outside a shape, and a rehearsal's look

**To understand this, start by reading the plan's section 4A and 4D, and section 6's rows
P1 and *After the bench* 4A, then `CALIBRATION.md`'s *Paint held outside a shape, as
built*, then [`tests/test_clip_out.py`](tests/test_clip_out.py).**

Branch: `ccr-6544d06d-6o24n7`, off `main` at `6a02419` (#104, step 2b, merged).

---

## What landed

| | |
|---|---|
| **`src/easel/session.py`** | `clip_out=` on `stroke`, and so on `dab`, `smudge` and `glaze`, and on `block_in`, `sweep`, `cover` and `scumble`; `_clip_cover` multiplies the mask by one minus each excluded shape's coverage, cut on the line, with the shapes in the memo's key; the record's new form and its replay; `_nothing_cause` and the thumbnail's laid masses read the exclusion; `_paintable` refuses a `difference()` on every verb that lays paint; `unguide()`'s docstring says landmarks are `unmark()`'s |
| **`src/easel/regions.py`** | `difference(place, *taken, name="")` and `Difference`, a `Polygon` whose `inside`, `mask`, `coverage` and `area` leave its holes out |
| **`src/easel/plan.py`** | a planned place that is a difference saves its holes beside its outline and reads them back |
| **`src/easel/cli.py`**, **`src/easel/mcp_server.py`** | `easel run --region --scale --no-sketch --no-marks`, and the server's `run(region=, scale=, sketch=, marks=)`, for a rehearsal's look and each panel of an alternatives sheet; refused where no look is written |
| **`PAINTER.md`** | the drawing step: a landmark is taken back by `unmark()` (within the 6,700-word budget) |
| **`REFERENCE.md`** | `clip_out=` under *Which verb takes which hold*, rule first; `difference()` among the shapes; the `easel run` flags |
| **`CALIBRATION.md`** | the round's *Paint held outside a shape, as built* |
| **`SUGGESTIONS.md`** | the round's rows for paint held outside a shape and for the rehearsal's look, filled in |
| **`scripts/probe_uktarl_session.py`** | `--clip-out` lays the backlight through the built `clip_out=` beside the bench's candidates; its patch takes `_clip_cover`'s new argument |
| **`tests/test_clip_out.py`**, **`tests/test_mcp.py`**, **`tests/test_reference.py`** | the new behaviour; `difference` among the calls `REFERENCE.md` answers for |

## Decisions and gotchas

- **As the painter chose (P1)**: `clip_out=` alone for paint; no `intersection()`;
  `difference()` only for places that are read. Every verb that lays paint refuses a
  difference, whether as the place, as `clip=` or as `clip_out=`, and the error names
  `clip_out=`. **One reading of P1 to confirm**: a difference that happens to have no hole
  (a bite out of an edge) is refused for paint too. The plan's first proposal would have
  traced and allowed it; P1 says *only for places that are read*, so it is refused.
- **The exclusion is cut on the line whatever `feather=` is.** `feather=` still breaks the
  edges of `clip=` and `edge="hard"`. `clip_out=` alone holds nothing in, so a non-zero
  `feather=` beside it is refused as before.
- **The record**: `params["clip"]` becomes `{"in": [outlines], "out": [outlines]}` only when
  a mark is held out of something. One hold and a list of holds are logged as they were.
  0.8.0 reads the mapping as an outline and raises `KeyError: 0` at `held[0]` — a refusal,
  but a cryptic one; no form 0.8.0 can read gives a better message. Tested against `v0.8.0`
  from `git archive` by hand (the session loads, `replay()` raises); the test suite carries
  0.8.0's reader verbatim instead.
- **A plan that names a difference** saves `holes` beside `points`. 0.8.0 ignores the key
  and reads the place without its holes: a misread line, not misplaced paint.
- **An exclusion changes paint past the figure.** A pass that crosses him lays nothing
  there, so it carries its load and wet pickup further. The test checks the seam (the
  value just outside the figure against the wall further out), not pixel equality with
  the hold alone.
- **`Difference.inset()` and `.smooth()` refuse**: shape the places first, then take one
  from the other. `.scaled()`, `.shifted()` and `.renamed()` carry the holes. A hole keeps
  its outline only, not its name, so a plan read back from the file compares equal.
- **Found, not fixed**: the server's `look` tool builds its docstring as `"""...""" +
  _PLACE_HELP + """..."""`, which is an expression, not a docstring, so the tool goes out
  with no description. `run`'s new arguments are written without it.
- **The step-2 probe's patch** on `_clip_cover` had to take the new `outs` argument, or every
  stroke under it raised.

## Next

Step 4 (B, the soft hold, B1 per hold and per stretch) starts from the plan's section 4B
and *Answered after the bench*. K's alpha (`export(alpha=)`, `plan(cut=)`) takes
`difference()` for the arch's hole once Q1 is answered again.
