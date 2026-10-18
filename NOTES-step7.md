# Step 7 of `PLAN-0.9.0.md`: what a direction costs, and a dark picture's light

**To understand this, start by reading the plan's sections 4G and 4H, and section 6's P7,
*Answered after the bench* (G1, G2) and *Asked back after step 7*, then the painter's own
words, [`answers.md`](paintings/Claude/uktarl_krannoc/answers.md) G and its first section,
and [`answers-step2.md`](paintings/Claude/uktarl_krannoc/answers-step2.md) 5a and 5b, then
`CALIBRATION.md`'s *What a direction costs, and a dark picture's light, as built*, then
[`tests/test_direction.py`](tests/test_direction.py) and
[`tests/test_named_light.py`](tests/test_named_light.py).**

Branch: `ccr-52e9ee7b-rddn15`, off `main` at `be4c863` (#109, step 6, merged).

---

## What landed

| | |
|---|---|
| **`src/easel/session.py`** | `_check_direction_given` (`direction-given`, G1), at `block_in`'s call and in `_plan_price`, so `cost()` says it too and `paint()` and `rehearse()` say it as they lay; `_shape_lines`, the lines a shape is swept along and the spans kept, split out of `_shape_paths` so the passes laid and the strokes counted are one walk; `_pass_pieces`, `(passes, pieces, cut)` off that geometry; the `values:` line handed the named light under any key but `"high"`; `direction=`'s and `plan(key=)`'s docstrings |
| **`src/easel/checklist.py`** | `_named_light_clause`, H2: beside *no clear light* with no key, a planned light `0.10` clear of the rest, and `s.plan(key='low')` |
| **`src/easel/plan.py`** | `Plan.light_reading` reads the light with no key, `None` only under `"high"`; `KEY_WORDS`' comment and the refusal say the rule |
| **`src/easel/notices.py`** | `direction-given`, a fact, measured under *What a mass was charged for its direction* |
| **`src/easel/cli.py`**, **`src/easel/mcp_server.py`** | `--key`'s help, the prelude scaffold's comment and the server's `plan(key=)` say the rule first |
| **`PAINTER.md`** | the card's plan step says the rule, H1; paid for by the painter's own cut (P8), the anecdote under the sentence about `RECIPES.md`, and a *then* in step 1's story. 6,700 words, as before; the card 1,378 |
| **`REFERENCE.md`** | the `key=` row opens with the rule, and says what the line says undeclared; the `values:` row; `direction`'s row and the rules that fire at the call; a row of *What the tool will tell you* |
| **`README.md`**, **`llms.txt`** | thirty-three notices |
| **`scripts/probe_uktarl_session.py`** | `--direction-built` and `--key-built`, the corpus replayed through the built engine and kept in `out/uktarl/built.pkl`, and the two versions; `--pieces-sheet`, every pass of the V and the guide's shapes drawn |
| **`paintings/Claude/uktarl_krannoc/questions-step7/`** | the question back on G2, with `pieces.png` |
| **`tests/test_direction.py`**, **`tests/test_named_light.py`**, **`tests/test_requests.py`** | the new behaviour; the light read with no key; a chosen direction says `direction-given` |
| **`CALIBRATION.md`**, **`SUGGESTIONS.md`**, **`PLAN-0.9.0.md`**, **`LESSONS.md`** | the round's *as built* and an index row; the rows for the direction, the light and The Curator's layer; the status line, step 7's row, 4N's, section 5's revisited ruling and section 6's question back; *the guide's own blocks are part of what it is taken over* |

## Decisions and gotchas

- **As the painter chose**: G1, a notice with both prices (5a); G3 left named, not built
  (6); H1 and H2, not H3 (G). **G2 (a) was built as chosen and is held, on the owner's
  word (2026-10-17)**: at a third more pieces than passes it spoke on three recipes, at
  the calls they teach — the grip's clean fill in *A small cluster of like parts gripping
  an edge*, the shade in *A silhouette lit from one side* and its demo, the half-tone band
  in *A form turned toward the light* — and on `PAINTING.md`'s ribbon round a bend, against
  the plan's rule 2. No count separates them from the V (1.33 to 1.43 against 1.57); a price
  for the parts does. The question is back with the painter, with the sheet. **The count
  stays** in `_pass_pieces`, since `direction-given` prices with it.
- **`direction-given` is one direction given**: a number, a name (`"horizontal"`,
  `"vertical"`, `"diagonal"`) or a line of two points; not `"axis"`, not a sequence
  (`direction-sequence` prices those), not left off (`direction-default`). The threshold
  is `_DIRECTION_RATIO`, the default's 2.5×. A line is said as *the line given, 11
  degrees*.
- **It revisits a 0.6.0 ruling**: `direction-default` was quiet on a direction chosen, and
  a test held it so on the tower's lit band, `"horizontal"` at 55 against 5. That test
  now expects `direction-given`; the plan's section 5 has the row.
- **Priced off the geometry, not a trial copy**: `_pass_pieces` walks `_shape_lines`, the
  lines `_shape_paths` lays, so the price quoted is the strokes laid (a test holds them
  together at four directions) and nothing is drawn from the stream. `_shape_paths` was
  refactored to read its lines from `_shape_lines`: the same spans in the same order, the
  wander drawn per span as before; the golden rebuilds hold.
- **The fill's passes, as the other two notices quote**: a clean edge adds its one contour
  pass, so the facets' notices add to 78 against 21, which is 88 and 31 with the contours.
- **H2 speaks only beside *no clear light***, with no key declared, a light named, and the
  light `0.10` or more clear of everything else (`VALUE_THRESHOLD`, the test the low key's
  clause uses); its numbers are that clause's. A light that does not stand clear adds
  nothing. Under `"high"` it is not read. As built it is the bench's count exactly.
- **H1 on the card took the painter's own cut now, not at step 9**: the anecdote under the
  sentence about `RECIPES.md` (P8's third cut), whose story lives in `SUGGESTIONS.md`. **A
  reading to confirm**, since step 9 is where the card's cuts are measured. The card says
  *when only a small light rises above it*, because the test is the top twentieth: a light
  larger than a twentieth of the picture takes the key with it.
- **Found, not fixed**: `cost_line()`'s reason already names pieces past 1.15 a pass, with
  a remedy of its own (*lay the straight stretches as strokes, or use a wider brush*); the
  painter's answer decides whether the two should say one thing. And `_plan_price` hands
  `_check_direction_sequence` the spec's raw `overhang`, not the resolved one; the count
  does not depend on it.

## Next

Step 8 (I2 to I5: the recipes and sentences, the pixel paragraph, the painter's lines atop
each release entry) starts from the plan's section 4I; *A thing drawn in its own frame*
uses `s.frame()`, and the join's recipe width uses `soft=`. Step 9 counts the reading
path. **G2 waits for the painter's answer to `questions-step7/`.** **4N's `cut=` is not
built**: Q1 makes it one declaration with 4K's `alpha=`, and both wait for the second
painter's batch 2 (the alpha's edge again, the ground line inside a cut, L1 as a backstop,
O3 and M2), which is not written yet.
