# Step 5 of `PLAN-0.8.0.md`: a declared key, a place read by its median, and a light read as a light

**To understand this, start by reading the plan's E1 to E4 with their *Step 2* and *Step 5*
notes, then `PlaceReading`, `read_place` and `Plan.value_line` / `lightest_line` /
`light_reading` in `src/easel/plan.py`, `values_line` and `_key_clause` in
`src/easel/checklist.py`, and `Palette._under_the_default_dark` in `src/easel/palette.py` --
and read `NOTES-step2.md` first if you have not, because this step builds what that one
measured and the painters then decided.**

Branch: `declared-key-and-place-medians`, off `main` at `8f7a1da` (step 4, #93).

---

## What this step was for

The Bell-Warden's `values:` line said *no clear light* on 25 of its 27 reports, of a
picture its notes call low-key by design, and nothing could say so; its `plan:` line called
the head's top a miss, because the eye is in it, and the painter blamed the eye's paint;
and `at_value` told it `0.13` was out of reach, which it read as the box's floor. Wenna
Brask's lantern read `0.49` against `0.76`, because its iron is most of its place. Every
one of these was decided by a painter -- questions 5, 6, 10, W-Q5 and 5f -- and step 2's
bench measured each decision over the corpus, so this step builds them as decided and
checks the engine's lines against the bench's.

## What landed

| | |
|---|---|
| **E1: the key** | `KEY_WORDS`, `Plan.key` (saved, read back with `.get`, printed, cleared with `""`), `plan(key=)` on the session, `easel plan --key`, the server's `plan`, the prelude scaffold. `values_line(key=, light=)` and `_key_clause`: kept or left, and by how much; the clusters printed, not judged |
| **E2: the median** | `PlaceReading` (median, 95th percentile, shares darker and lighter by over `SPLIT_STEP`), `read_place`, `Planned.reading` in place of `mean_value`; `plan:` reads the median and brackets a split place it names; `compare_plan` reads the median too |
| **E3: the floor** | `Palette._under_the_default_dark`: burnt umber's `0.128`, the 7:3 mix's `0.132`, which of them falls short; under `0.128`, a grey at the target's value. Only when `dark=` was left off |
| **E4: the named light** | `lightest:` ranks by the median and prints the named light at its brightest twentieth too; `Plan.light_reading` hands the `values:` line the light under a key, and `_light_clause` asks whether it stands clear by `0.10` |
| **The bench** | `probe_bell_session.py --declared`: both paintings' places read by the engine against the bench's `readings()`, the lines `easel run` printed, the `values:` line under `key="low"`; the key's clause and the median's `plan:` count over the corpus |
| **Tests** | `test_requests.py` *0.8.0 E1* (3), *E2* (2), *E4* (1), *E3* (1); `test_mcp.py`'s plan tool takes `key` |
| **Documents** | `REFERENCE.md`: the plan table's `values=`, `lightest=` and new `key=` rows, the signature, the `values:` sentence, `at_value` and `darkest_value`. `CHANGELOG.md`, `CALIBRATION.md` (*The key, the median and the named light, as built*), `SUGGESTIONS.md` (four rows, the count), the plan |

## Decisions and gotchas

**1. The engine is the bench, to the last bit.** `read_place` is the arithmetic of the
bench's `readings()` -- float64, `np.median`, `np.percentile(.., 95)`, strict `<` and `>`
against the median `-`/`+ 0.15` -- so every place of both plans reads the same at every
pass end (`3.5e-18`, float noise). What `easel run` now prints on both paintings is in
`CALIBRATION.md`.

**2. The split is two shares, and the clause names the side.** The painter's wording,
*24% of it darker by more than 0.15*, names a side, and the bench's `split` counted both.
So `PlaceReading` keeps `darker` and `lighter` apart, `split` is their sum at a tenth, and
the clause names the side that holds it -- or both, when each is at least half a percent.
On `plan:` it goes in brackets after the miss, since `;` separates places there; on
`lightest:` after the verdict, as the painter wrote it.

**3. The median ranks the places; the 95th is printed, not ranked.** As 5f decided: the
lightest place by the 95th is the median's at every pass end of the Bell-Warden, so ranking
by it would change nothing there and would make the two lines disagree about which reading
ranks. The line prints the named light's two numbers and the other place's median.

**4. The key's clause replaces the whole judgement.** Under a key `values_line` returns
after the key's clause and the light's -- neither *no clear light* nor the gap verdict is
asked. With no `reach` (only a direct caller omits it), a key says nothing, as the box's
middle is what it is judged against.

**5. The light under a key is the proposal's, not a painter's decision.** E4's text asked
for it; the painters decided the `lightest:` form. It is built because it costs one reading
of a view the line already has, and says only under a key. On the Bell-Warden it says the
head's top does not stand clear on the room's and plinth's passes -- before the subject
existed -- which is true. The view is `_canvas_lines`'s (graphite out), not `_value_view`,
so the light and the top twentieth are read off one array.

**6. `at_value` still says *out of reach*.** An older test matches it, and a painter's code
may too; the new sentence begins *out of reach of the default dark*. A `dark=` the painter
chose is held to what it reaches, as before, in the old words -- the error only offers
darks when the engine chose the dark.

**7. `mean_value` is gone.** Its one caller was the plan's two lines; the probes read
`plan.value_line`, not it. A 0.7.0 plan file has no `key` and opens with none.

**8. On this machine.** `import easel` from the repo root resolves to the installed 0.7.0
wheel: run pytest and the probes with `PYTHONPATH=src` (and `scripts` for the probes, from
inside `scripts/` on Windows, where the separator is `;`). A bash heredoc holding Python
with nested quotes still dies with *unexpected EOF* -- write the script to the scratchpad
and run it.

## What step 5 did *not* touch

What any mark lays: no golden, sampler or rebuild moves. A painting's plan lines may read
differently after the next pass -- the median where the mean was. E3's documents (one floor
in `PAINTER.md`, `PAINTING.md`, `CALIBRATION.md`'s table and `palette.py`'s docstrings) are
F3's, and E4's rule for the guide -- *plan the place the why names, at the value the place
will read* -- is F's too. `PAINTER.md` is untouched, 45 words from its budget.

## File map

| File | What changed |
|---|---|
| `src/easel/plan.py` | `KEY_WORDS`, `SPLIT_SHARE`, `SPLIT_STEP`, `PlaceReading`, `read_place`; `Planned.reading`; `Plan.key`, `value_line`'s split, `lightest_line`'s two readings, `light_reading`; `build(key=)` |
| `src/easel/checklist.py` | `values_line(key=, light=)`, `_key_clause`, `_light_clause` |
| `src/easel/palette.py` | `at_value`'s error under the default dark, `_under_the_default_dark` |
| `src/easel/measure.py` | `compare_plan` reads the median |
| `src/easel/session.py` | `plan(key=)`; `_canvas_lines` hands the key and the light to the `values:` line |
| `src/easel/cli.py`, `mcp_server.py` | `easel plan --key`, the prelude's `key="low"` line; `key` on the server's `plan` |
| `scripts/probe_bell_session.py` | `--declared`, `probe_declared` |
| `tests/test_requests.py`, `tests/test_mcp.py` | the tests above |
| `REFERENCE.md`, `CHANGELOG.md`, `CALIBRATION.md`, `SUGGESTIONS.md`, `PLAN-0.8.0.md` | as above |
| `NOTES-step5.md` | this file |

## Next

- **Step 6 (A3)**: the thumbnail, as question 4 decided it -- 192 px, no argument the plan's
  places and the masses laid so far, a clip as a `(value, clip)` pair, and `easel run
  --thumbnail` for the pass about to be rehearsed, with its server tool.
- **For step 9 (F)**: the floor said one way (E3), and the rule a light's place is planned
  by (E4), in the documents.
