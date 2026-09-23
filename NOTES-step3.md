# Step 3 of `PLAN-0.7.0.md`: the looking flags, the plan grammar, and the saved reports

**To understand this, start by reading the plan's workstream E and row C0 of workstream
C, then `Session.reports` and `Session._trial_session` in `src/easel/session.py`, then
`_cmd_run` in `src/easel/cli.py` -- and read `NOTES-step2.md` first if you have not,
because this step is built on its rulings.**

Branch: `look-flags-and-saved-reports`, off `main` at `427901a` (steps 1 and 2, #76).

---

## What this step was for

The two rows the plan calls *small and certain*: what the painter needed to look at its
picture without the scaffolding, what it needed to know to put a whole pass into a plan,
and the one change that would have kept its two misfires in the session file. Nothing
here changes what a mark lays: no golden moved, and no painting rebuilds differently.

## What landed

| | |
|---|---|
| **`easel look --no-marks`**, `marks` on the MCP `look` | `look(marks=False)` existed since 0.4.0 and neither surface could say it. The painter's `clean_look.py` is `easel look p.easel --no-marks --no-sketch` |
| **The guides go with `--no-sketch`, and now it says so** | the flag's help, the MCP `sketch` argument, `look()`'s docstring, `PAINTING.md` and `REFERENCE.md`'s `look` line |
| **The plan grammar, whole** | `REFERENCE.md` names all five kinds and the film, twice (the Python section and the MCP one), with *a whole pass is a plan*; the same in `preview`'s and `rehearse`'s docstrings and `_PLAN_HELP` |
| **`reports` in the `.easel` file** | `notices.PassReport` (`scripts`, `mode`, `at`, `text`), `Session.reports()`, `Session._keep_report`, saved and loaded beside `notices`; `easel log --reports [-n N]`; `log(reports=)` on the MCP server |
| **A rehearsal saves the file** | `easel run --rehearse`/`--count` and MCP `run(rehearse=)`/`run(count=)` keep their block on the painting and write it, after printing |
| **A rehearsal copy owns its palette, landmarks and guides** | `_trial_session` copies the three (`Palette._copy()`), where it shared them |
| **Tests** | `test_requests.py` *0.7.0 E* and *0.7.0 C0* sections (9 tests); `test_reference.py` *the plan grammar* (4); `test_mcp.py` (3) |

**The case it was built for.** The headland misfire rebuilt as
`misfires/README.md` says -- `p00` to `p02` committed, then `03_headland_v2.py`
rehearsed -- prints the painter's line to the character, and afterwards the file has
it: `easel log lighthouse.easel --reports -n 1` reads *rehearsed 03_headland_v2.py, from
record 50* and then *19 marks at stepping colours run parallel 0.020 apart, and the
narrowest brush laying them is 0.006 -- 0.3 of that step*. Before this step nothing in
the file could have shown it.

## Decisions and gotchas

**1. The plan's guides claim was wrong, and `guides=` was not built.** `render_look`
draws the overlay only when `sketch` is on (`guides=guides if sketch else None`), so
`look(sketch=False)` -- which the painter's helper passes -- has always hidden the guides
with the pencil: a look with a guide drawn and `sketch=False` differs from one with none
in no pixel (`test_the_drawing_on_the_view_goes_with_the_pencil`). The plan said *nothing
at any level hides the guides* and planned `guides=` on it; with the claim gone the
switch had no painter behind it, so what was built is the sentence that was missing.
Corrected where it stood in the plan and in `SUGGESTIONS.md`.

**2. `REFERENCE.md`'s grammar named three kinds, not five.** *A path, a dict of `stroke`
arguments, `shape=`, `edge=`* -- a mark, a mass and a sweep. The passage (`band=`) and
the burial (`cover=`) were only in the MCP server's `_PLAN_HELP`. The plan said five;
corrected where it stood. The new test holds the grammar to `PLAN_ACCEPTS`' keys, so a
sixth kind fails `test_every_kind_a_plan_lays_has_a_key_here` until it is named. The
plan's own test -- *every `stroke()` keyword a plan can carry is on the page* -- was
already `test_every_parameter_a_painter_can_name_is_somewhere_on_the_page`, so it was
not written twice.

**3. A film in a plan has to carry the verb's defaults.** An entry is `stroke()` kwargs,
so `{"points": band, "glaze": True, "color": c}` is a **bristle** film at the bristle's
`0.88` opacity and `0.11` size -- nothing like `s.glaze(band, c)`, which is `round_soft`
at `0.18` (`test_a_film_left_to_a_strokes_defaults_is_not_the_verbs`). So every place
the grammar is written shows the entry with `"brush": "round_soft"` and an `opacity`,
and the test asserts that entry lays the verb's film to the pixel. `glaze-far` is said
by `stroke()` itself, so the entry keeps the verb's notice; only `to_value=` is the
verb's alone.

**4. The smudge was not named.** The plan asked for it. Written as a mark it is
`{"points": edge, "brush": "smudge"}`, which takes the smudge brush's `size=0.07` -- the
width `smudge()`'s `0.02` default was moved off because four of five smudges at it came
back as lobes -- and `pressure="taper"` rather than `"even"`, and it never runs
`_check_smudge_size` or `_check_smudge_path`, so `smudge-wide`, `smudge-across` and
`smudge-long` cannot fire. Naming it would be a worked example of the failure the verb
exists to stop (`LESSONS.md`, *a worked example is an instruction*), and no painter
asked for a smudge in a plan. **If one does**, the build is a verb-named kind in
`cover`'s pattern -- `{"smudge": edge, ...}` laid through `s.smudge()` -- and the trap
is that `smudge` is already a brush field and `glaze` a stroke keyword, so the kind
would have to be told apart by the value's type (a path or place, not a number or a
bool), and checked after `shape`/`edge`/`band`/`cover` so `{"shape": s, "smudge": 0.3}`
stays a mass with a brush override.

**5. Saving a rehearsal's report meant writing the file after a rehearsal, and that
exposed a leak.** `_trial_session` handed the copy the painting's own `palette`, `marks`
and `guides` objects. A rehearsed pass runs the prelude and its own mixtures, so every
slot it mixed, every landmark and every guide landed on the painting's objects -- and
nothing noticed only because nothing saved the painting after a rehearsal. Now the copy
gets copies (`Palette._copy()`, `dict(marks)`, a list of copied guide dicts), and
`test_a_rehearsal_writes_nothing_of_itself_but_the_report` checks the log, the canvas,
the stream, the palette's slots, the marks and the guides come back as they were. **A
Python script that mixed on a `scratch()` and then used the slot on the painting now
raises `KeyError`**; `CHANGELOG.md` says so. The painter's own harness mixed per
variant, so each variant started on the last one's slots -- but every slot one of its
variants mixes, the others mix again before using it (`try_sky.py`'s `low2` and
`glow_rim`, `try_sky3.py`'s `colours()` and `afterglow()`), so none of its pictures was
changed by it. A variant that used a slot without mixing it would have painted with the
last variant's.

**6. What a save costs, which is now paid by every rehearsal.** On the painter's own
16.4 MB file: `Session.load` 0.33 s, `save` 0.80 s -- and without the time-lapse frames,
which step 4 takes out, 0.30 s and 0.28 s. The load was always paid; what a rehearsal
adds is the save. Against a rehearsal of a pass (the painter's variants were ten
seconds and more of paint) that is a few percent; against `--count`, which is a second
or two, it is a larger share, and counts are kept anyway because a check read off the
log fires on a count exactly as on a rehearsal.

**7. The report is written after the printing.** A session file that cannot be written
raises out of `easel run` with `easel: ...` and exit 1, and the painter has already
seen the rehearsal it was waiting for. The MCP path saves before returning, since a
tool result is one value.

**8. A report is kept only where a block is printed.** A pass that raised prints its
notices to stderr with the traceback and runs no check, so it keeps no report; a
committed pass that raised still saves what it painted, as before. `at` is the log
index in the painting's numbering -- `target._index_base + since`, because a copy's own
log starts at nought -- so `s.replay(upto=r.at)` is the canvas the pass opened on.

**9. Reports follow the notices everywhere else.** Written as a list of dicts under
`reports` (always, empty or not), read with `.get` and forgivingly: a later build's
unknown mode is kept, an unreadable entry is dropped, and a `reports` that is not a list
reads as none (`test_a_saved_report_is_read_forgivingly`). `undo` keeps them (it adopts
only canvas, history and stream); `replay()` returns a session without them, as it does
without notices. **Checked against the tag rather than assumed**: `v0.6.0`'s own `src`
(`git archive v0.6.0 src`), imported in a child process started with `-S` so the
editable install's `.pth` hook cannot hand it the checkout instead, opened a file this
build wrote, painted a stroke into it and saved it -- and that save **drops the
reports**, because 0.6.0 does not know the key. Two traps on the way: with the hook in
place `import easel` in the child loaded the checkout while printing `0.6.0` (the
version is not bumped until the cut), and a bash `$SP` path (`/c/Users/...`) handed to
Windows Python is `C:\c\Users\...`.

**10. One pre-existing behaviour now reaches rehearsals.** `foreign-out-dir` is said at
load and kept on the session, so every save writes it again -- which committed passes
have always done. Rehearsals save now, so they do it too. Rare (a file whose `out_dir`
is neither the working directory nor beside the file) and left alone.

## What step 3 did *not* touch

What any mark lays. No golden, sampler or rebuild moves; the only change a painter can
see in a picture is none.

## File map

| File | What changed |
|---|---|
| `src/easel/notices.py` | `PassReport`, `MODES`, `saved()` |
| `src/easel/palette.py` | `Palette._copy()` |
| `src/easel/session.py` | `_reports`, `reports()`, `_keep_report()`; `save`/`load`; `_trial_session` copies palette, marks and guides; `look()`, `preview()` and `rehearse()` docstrings |
| `src/easel/cli.py` | `look --no-marks`, `--no-sketch`'s help; `log --reports` and `-n`'s help; `_cmd_run` keeps the report and a rehearsal saves |
| `src/easel/mcp_server.py` | `look(marks=)`; `run` keeps the report and a rehearsal saves; `log(reports=)`; `_PLAN_HELP` |
| `REFERENCE.md`, `PAINTING.md` | the grammar; the flags; `s.reports()` |
| `tests/test_requests.py`, `test_reference.py`, `test_mcp.py` | the tests above; *the file is untouched* became *the painting is untouched* in `test_rehearsing_a_pass_commits_nothing` |
| `CHANGELOG.md` | `[Unreleased]`: this step's section |
| `SUGGESTIONS.md` | three rows filled in, two claims struck where they stood, the counts |
| `PLAN-0.7.0.md` | status; the two corrections; E and C0 marked built; the file map |
| `NOTES-step3.md` | this file |

## Next

Step 4, workstream F: the frames out of the file (which also makes every rehearsal's new
save about a third of what it costs today), and the engine stamp with its notice at
load.
