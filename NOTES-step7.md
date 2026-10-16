# Step 7 of `PLAN-0.9.0.md`: what a direction costs, and a dark picture's light

**To understand this, start by reading the plan's sections 4G and 4H, and section 6's P7
and *Answered after the bench* (G1, G2), then the painter's own words,
[`answers.md`](paintings/Claude/uktarl_krannoc/answers.md) G and its first section, and
[`answers-step2.md`](paintings/Claude/uktarl_krannoc/answers-step2.md) 5a and 5b, then
`CALIBRATION.md`'s *What a direction costs, and a dark picture's light, as built*, then
[`tests/test_direction.py`](tests/test_direction.py) and
[`tests/test_named_light.py`](tests/test_named_light.py).**

Branch: `ccr-52e9ee7b-rddn15`, off `main` at `be4c863` (#109, step 6, merged).

---

## What landed

| | |
|---|---|
| **`src/easel/session.py`** | `_check_direction_given` (`direction-given`, G1) and `_check_pieces` (`pieces`, G2 (a)), at `block_in`'s call and in `_plan_price`, so `cost()`, `rehearse()` and `paint()` say them too; `_shape_lines`, the lines a shape is swept along and the spans kept, split out of `_shape_paths` so the passes laid and the pieces counted are one walk; `_pass_pieces`, `(passes, pieces, cut)` off that geometry; the `values:` line handed the named light under any key but `"high"`; `direction=`'s docstring |
| **`src/easel/checklist.py`** | `_named_light_clause`, H2: beside *no clear light* with no key, a planned light `0.10` clear of the rest, and `s.plan(key='low')` |
| **`src/easel/plan.py`** | `Plan.light_reading` reads the light with no key, `None` only under `"high"` |
| **`src/easel/notices.py`** | the two codes, both facts, both measured under *What a mass was charged for its direction* |
| **`src/easel/cli.py`**, **`src/easel/mcp_server.py`** | `--key`'s help and the server's `plan(key=)` say the rule first |
| **`PAINTER.md`** | the card's plan step says the rule, H1; paid for by the painter's own cut (P8), the anecdote under the sentence about `RECIPES.md`. 6,700 words, as before; the card 1,377 |
| **`REFERENCE.md`** | the `key=` row opens with the rule, and says what the line says undeclared; the `values:` row; `direction`'s row and the rules that fire at the call; two rows of *What the tool will tell you* |
| **`scripts/probe_uktarl_session.py`** | `--direction-built` and `--key-built`: the corpus replayed through the built engine, and the two versions |
| **`tests/test_direction.py`**, **`tests/test_named_light.py`**, **`tests/test_requests.py`** | the new behaviour; the light read with no key |
| **`CALIBRATION.md`**, **`SUGGESTIONS.md`**, **`PLAN-0.9.0.md`** | the round's *as built*; the rows for the direction and the light; the status line, step 7's row and 4N's |

## Decisions and gotchas

{{DECISIONS}}

## Next

Step 8 (I2 to I5: the recipes and sentences, the pixel paragraph, the painter's lines atop
each release entry) starts from the plan's section 4I; *A thing drawn in its own frame*
uses `s.frame()`, and the join's recipe width uses `soft=`. Step 9 counts the reading
path. **4N's `cut=` is not built**: Q1 makes it one declaration with 4K's `alpha=`, and
both wait for the second painter's batch 2 (the alpha's edge again, the ground line
inside a cut, L1 as a backstop, O3 and M2), which is not written yet.
