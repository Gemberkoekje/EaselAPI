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
| **E2: the median** | `PlaceReading` (median, 95th percentile, shares darker and lighter by over `SPLIT_STEP`, `split_clause`, `said`), `read_place`, `Planned.reading` in place of `mean_value`; `plan:` reads the median and brackets a split place it names; `compare_plan` reads the median too |
| **E3: the floor** | `Palette._under_the_default_dark`: burnt umber's `0.128`, the 7:3 mix's `0.132`, which of them falls short; a darker pigment the box holds; under the floor, a grey at the target's value. Only when `dark=` was left off |
| **E4: the named light** | `lightest:` ranks by the median, prints the named light at its brightest twentieth too, and brackets the split of every place it names; `Plan.light_reading` hands the `values:` line, under `key="low"`, the light and the brightest twentieth of everything else, off the plan's view; `_light_clause` says whether it stands clear by `0.10`, both numbers said |
| **Fixed on the way** | `report()` kept the plan's view -- graphite in -- as the canvas the next pass's buried details are read against, whenever a plan was declared; it keeps the canvas without graphite, as `_open_pass` does. `_canvas_lines(plan_view=)` |
| **The bench** | `probe_bell_session.py --declared`: both paintings' places read by the engine against the bench's `readings()`, the lines `easel run` printed, the `values:` line under `key="low"`; the key's clause and the median's `plan:` count over the corpus |
| **Tests** | `test_requests.py` *0.8.0 E1* (4), *E2* (4, with the kept view), *E4* (2), *E3* (1); `test_mcp.py`'s plan tool takes `key`. Every test the second look added fails on the first commit, `67c232d`, for the reason it names |
| **Documents** | `REFERENCE.md`: the plan table's `values=`, `lightest=` and new `key=` rows, the signature, the `values:` sentence, `at_value` and `darkest_value`. `CHANGELOG.md`, `CALIBRATION.md` (*The key, the median and the named light, as built*), `SUGGESTIONS.md` (four rows, the count), the plan |

## Decisions and gotchas

**1. The engine is the bench, to the last bit.** `read_place` is the arithmetic of the
bench's `readings()` -- float64, `np.median`, `np.percentile(.., 95)`, strict `<` and `>`
against the median `-`/`+ 0.15` -- so every place of both plans reads the same at every
pass end (`3.5e-18`, float noise). What `easel run` now prints on both paintings is in
`CALIBRATION.md`.

**2. The split is two shares, each said with its own number.** The painter's wording,
*24% of it darker by more than 0.15*, names a side, and the bench's `split` counted both.
So `PlaceReading` keeps `darker` and `lighter` apart, `split` is their sum at a tenth, and
the clause says each side that prints as more than `0%`, with its own share. It goes **in
brackets after what the place reads**, on both lines: `;` separates places on `plan:`, and
on `lightest:` a clause at the end of the line would say *it* of two places at once.

**3. On `lightest:` every place the line names says it is split** -- the named light, and
a place that took the light from it. The painter's answer to question 5 said where the
clause would appear, *for the plinth's top while that line named it the lightest place, and
for the head's top after*; so the plinth's top is said split on the subject's pass, the one
pass that line names it, and `plan:`, which never misses it, never does.

**4. The median ranks the places; the 95th is printed, not ranked.** As 5f decided: the
lightest place by the 95th is the median's at every pass end of the Bell-Warden, so ranking
by it would change nothing there and would make the two lines disagree about which reading
ranks. The line prints the named light's two numbers and the other place's median.

**5. The key's clause replaces the whole judgement.** Under `"low"` or `"high"`,
`values_line` returns after the key's clause and the light's -- neither *no clear light*
nor the gap verdict is asked. With no `reach` (only a direct caller omits it) or a word it
does not know, the line judges as it always has; `Plan.from_json` drops a word it does not
know, as it drops a field.

**6. The light under a key is the proposal's, not a painter's decision** -- E4's text asked
for it; the painters decided the `lightest:` form -- **and it is asked under `"low"`
only**: E4 asks it of a low-key picture with a small light, and a high-key picture's light
has no room above the rest to clear by `0.10`, so it would be told *no* on every pass. It
reads the light off **the plan's view**, `_value_view()` -- the one `lightest:` reads, so
the two lines print one number for one place -- and against the brightest twentieth of the
canvas **outside the light's place**, off the same view, so a light that is its own top
twentieth is not measured against itself. Both numbers are said, since neither is the
line's own. On the Bell-Warden it says the head's top does not stand clear on the room's
and plinth's passes -- before the subject existed -- which is true.

**7. `at_value` still says *out of reach*.** An older test matches it, and a painter's code
may too; the new sentence begins *out of reach of the default dark*. A `dark=` the painter
chose is held to what it reaches, as before, in the old words -- the error only offers
darks when the engine chose the dark. It names burnt umber while umber reaches the target,
and otherwise the darkest pigment the box holds, which is umber unless a painter's own
`Palette(pigments)` holds a darker one.

**8. `mean_value` is gone.** Its one caller was the plan's two lines; the probes read
`plan.value_line`, not it. A 0.7.0 plan file has no `key` and opens with none.

**9. On this machine.** `import easel` from the repo root resolves to the installed 0.7.0
wheel: run pytest and the probes with `PYTHONPATH=src` (and `scripts` for the probes, from
inside `scripts/` on Windows, where the separator is `;`). A bash heredoc holding Python
with nested quotes still dies with *unexpected EOF* -- write the script to the scratchpad
and run it.

## What the second look found

The step was built at a lower effort setting and then read again, line by line, the same
day, against the painters' own answers and the bench. What it found, all fixed in the PR:

- **The split, on `lightest:`, only for the named light.** The painter's answer says where
  it appears, the usurping place included (decision 3); the CALIBRATION text then said the
  plinth's split was never printed, which that answer contradicts.
- **A sum printed under one side's word** -- *13% of it lighter* where 12% was -- and a
  side under half a percent printed as `0%` (decision 2).
- **The light's number read off a second view.** `_canvas_lines` read it off the canvas
  without graphite, the value rounded after; `lightest:` reads `_value_view()`, graphite in,
  each channel rounded first. On Wenna Brask's setting pass the lantern read `0.32` on one
  line and `0.33` on the next. And the rest was the canvas's whole top twentieth, which
  holds the light (decision 6).
- **A key word this build does not know read as `"high"`**, from a file or a direct call
  (decision 5).
- **The view `report()` kept for the next pass**: with a plan declared, the plan's view
  overwrote the graphite-free one under the same name, and `_opened` kept it -- since
  0.6.0, found because this step hands that view on. It reaches only a script that runs
  passes and reports after each; `easel run` opens every pass with `_open_pass`.
- **The error for a box with a darker pigment** offered umber for a target umber could not
  reach (decision 7), and one line ran past the file's width.
- **The documents**: `report()`'s own example printed the old `lightest:` line; `compare()`
  did not say it reads the median; CALIBRATION had a garbled cell and called the 7:3 mix
  *the lowest chroma* where it is within a ten-thousandth of it; the release a fix shipped
  in was one too late.

The test that holds the light's number to the `lightest:` line's hands the session a plan
view of its own: graphite cannot move a 95th percentile unless it covers nearly all of a
place, and the two views' rounding differs by thousandths, so a painted case tells them
apart only by chance.

## What step 5 did *not* touch

What any mark lays: no golden, sampler or rebuild moves. A painting's plan lines may read
differently after the next pass -- the median where the mean was. E3's documents (one floor
in `PAINTER.md`, `PAINTING.md`, `CALIBRATION.md`'s table and `palette.py`'s docstrings) are
F3's, and E4's rule for the guide -- *plan the place the why names, at the value the place
will read* -- is F's too, in `PAINTER.md` and the recipe for a light: `REFERENCE.md`'s plan
table carries its second half beside the `lightest=` row, where the two numbers it explains
are described. `PAINTER.md` is untouched, 45 words from its budget.

## File map

| File | What changed |
|---|---|
| `src/easel/plan.py` | `KEY_WORDS`, `SPLIT_SHARE`, `SPLIT_STEP`, `PlaceReading`, `read_place`; `Planned.reading`; `Plan.key` (an unknown word dropped on load), `value_line`'s split, `lightest_line`'s two readings and splits, `light_reading`; `build(key=)` |
| `src/easel/checklist.py` | `values_line(key=, light=)`, `_key_clause`, `_light_clause` |
| `src/easel/palette.py` | `at_value`'s error under the default dark, `_under_the_default_dark` |
| `src/easel/measure.py` | `compare_plan` reads the median |
| `src/easel/session.py` | `plan(key=)`; `report()` and `checklist()` name the plan's view `plan_view` and hand it to `_canvas_lines(plan_view=)`, which reads the light off it; `_opened` keeps the canvas without graphite; the docstrings of `report()`, `compare()` and `plan()` |
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
