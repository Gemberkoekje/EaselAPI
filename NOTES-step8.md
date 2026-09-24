# Step 8 of `PLAN-0.7.0.md`: versions of a pass, rehearsed side by side

**To understand this, start by reading the plan's workstream D, then `run_alternatives`
and `_cmd_run` in `src/easel/cli.py`, `Session.rehearse_each` in `src/easel/session.py`,
and the MCP `run` tool in `src/easel/mcp_server.py` -- and read `NOTES-step7.md` first
if you have not, and `NOTES-step3.md`, whose saved reports every version keeps.**

Branch: `rehearse-alternatives-side-by-side`, off `main` at `c053e6e` (step 7, #81).

---

## What this step was for

The painter's finding 4: *about 15 s a variant*. Step 2 measured it and found the paint
-- 10.2 to 10.6 s of the harness's 10.4 to 10.7 is its three 8-pass scumbles -- and the
painter's answer to question 6 said what it wanted instead of speed: *my variants were
whole passes ... what would have replaced the harness is rehearsing scripts as
side-by-side alternatives. `easel run --rehearse a.py b.py` stacks them instead.* D0 is
that. D1, the panels of a sheet in processes of their own, was declined on step 2's bench
(question 14) and is not built.

## What landed

| | |
|---|---|
| **The shell** | `easel run p.easel a.py b.py --alternatives`: each script a version of one pass, rehearsed on a copy of its own, its own check printed and its own report kept, their looks in one sheet (`rehearse_NNN.png`), each panel labelled with the script and the strokes it laid. Implies `--rehearse`; with `--count`, prices each and lays no sheet; `--check` checks each over the painting under it; at most twelve on a sheet |
| **The shared runner** | `run_alternatives` in `cli.py`, with `Alternative` and `Alternatives`, beside `run_scripts`: the shell prints what it returns and the server hands it back |
| **Python** | `s.rehearse_each([...], reference=, region=, grid=, values=, scale=, path=, labels=)`: each version a plan or a function handed the copy |
| **The server** | `run(alternatives=[...] or {name: script})`: the sheet comes back inline, beside the text. **`run` now answers as a list** -- see 3 |
| **Helpers** | `_panel_scale` (the arithmetic `rehearse(vary=)` had inline, now shared), `_panel_label`, `_strayed_text`, `Session._versions` |
| **Words** | `REFERENCE.md` (the signature, the flag, a paragraph under *The session, and the shell*, the grammar's paragraph, the MCP paragraph), `PAINTING.md` (one clause under *Try the mark before you spend it*), `README.md` (one line), the flag's help, `rehearse()`'s and `scratch()`'s docstrings |
| **The probe** | `probe_handover_session.py --alternatives`: the painter's own two skies laid as its harness laid them, by `--alternatives` and by `rehearse_each`, timed, and each held to its panel |
| **Tests** | `test_requests.py` *0.7.0 D0* (8), `test_mcp.py` (1) |

## Decisions and gotchas

**1. A version that raises does not stop the others.** Scripts laid on one copy stop at
the first that fails, because the next stands on it (`run_scripts`). No version stands on
another, so one that raises is said -- on stderr from the shell, with what its calls said,
its report and its trace, and `(bad.py, 2 of 3)` naming it -- keeps no report, is left off
the sheet, and the run exits with its code; the others are rehearsed and laid side by side
as asked. The plan said nothing either way.

**2. In Python a version is a plan or a function.** The plan's row reads *`rehearse_each
([plan_a, plan_b])` for plans, since a function is what a script is inside Python*, and
the painter's own words were *making a script or function the unit of a panel would cover
my case*; so both are taken. A function is handed the copy and paints on it, as the
painter's harness handed each variant `(c, c.palette, ns)`. **Python lets a version's
helper reach the painting** -- a module-level function that paints on `s`, called from one
that was handed the copy -- and the painter's harness rebound its scope's `s` to each copy
for that reason; so `rehearse_each` counts the painting's log across each function and
stops one that moved it, naming the records to `undo`. A version is refused as text (a
script belongs to the shell), and a thing that can only be one plan -- an entry, a path, a
place -- is refused as one; a list of single entries is a version per entry, which is what
it looks like. Panels are labelled by a function's name, a plan's place from 1, or
`labels=`.

**3. The MCP `run` answers as a list now -- found while building.** Its answer was
declared `-> str`, and the SDK builds an output schema from that and **checks every answer
against it**: an answer of `[text, Image]` from a tool declared as text fails as *Error
executing tool*, measured on a two-tool server before anything was built on it. Declared
`-> str | list` it fails the same way, because the list arm is dumped into structured
content and an `Image` does not dump. Declared `-> list`, as `look`, `demo` and the other
looking tools are, the SDK builds no output schema at all and the answer goes out as
content blocks. So every `run` answer is a list, `[text]` or `[text, sheet]`: the text a
client reads is what it was, and **`run` no longer carries `structuredContent`** -- a
client that read its answer from there will find nothing. No test, and nothing in the
repository, read it; `CHANGELOG.md` says so.

**4. The sheet shows each copy as a rehearsal's own look does** -- landmarks, their
labels and the drawing included, at the panel's size (`look_image(scale=...)`) -- and the
Python sheet as `rehearse` does, landmarks without the guides. **The painter's harness
looked at its variants with `marks=False, sketch=False`**, the view its `clean_look.py`
made and finding 6 asked `easel look` for; on the probe's sheet of its two skies the
labels `glow`, `tip`, `lamp` and `base` and the drawing's lines sit on both panels. Not
changed here: `easel run` takes no view flags, and a sheet that drew a different view from
the rehearsal beside it would be one more thing to explain. **If the painter asks for it,
the build is `--no-marks` and `--no-sketch` on `easel run`**, meaning what they mean on
`easel look`, for the rehearsal's look and every panel alike, `marks` and `sketch` on the
MCP `run`, and the same two on `rehearse_each`. Recorded as a question, not a decision.

**5. Each version is checked and kept as a rehearsal is, nothing more.** `run_alternatives`
takes each copy with `scratch()`, opens its pass, runs the script with the prelude in
front, prints `report(since=)` under the notices, and keeps the block with
`_keep_report` -- so `easel log --reports` shows a version as `rehearsed dark.py, from
record 50`, two versions tried from one place reading as two rehearsals from the same
record. No new report mode was made for a version: it is a rehearsal, and the file's
reader keeps any mode it does not know, so a later round could add one without a format
change.

**6. The panels are sized for the sheet, not shrunk into it.** Each copy is drawn at
`_panel_scale(1024, n)` -- four to a row, never under 200 px, the arithmetic `rehearse(vary=)`
had inline -- and dropped, so twelve versions hold twelve small images and not twelve
canvases. A version run for real afterwards and looked at the same way is its panel to the
pixel, above the label drawn over the panel's corner: the probe checks it on the
painter's own skies and `test_the_version_run_for_real_lands_as_its_panel_shows_it` on a
small canvas.

**7. Windows papercuts met on the way.** A script written by PowerShell 5.1's
`Set-Content -Encoding utf8` starts with a byte-order mark, and `easel run` reads scripts
as `utf-8`, so every one fails as *does not parse* with `invalid non-printable character
U+FEFF` -- not this step's, and left alone; it is a one-word fix (`utf-8-sig`) for a later
round, flagged in the PR. And a sheet opened with `Image.open` and not read whole keeps
its file open, so a temporary directory holding it cannot be removed; the probe reads
sheets whole.

## The numbers

On this machine, the probe's (`--alternatives`), on a quiet machine:

| | |
|---|---|
| **The painter's two skies** | `try_sky3.py`'s B and C from the painting's drawing: three 8-pass scumbles each, B's warmth laid from the left in six strokes, three films; B lays 33 strokes, C 27 |
| **Through its harness** | 31.9 to 32.8 s for the two over two runs -- a copy and a look each, then a file each and `montage.py` |
| **Through `easel run --alternatives`** | 32.1 to 32.3 s, loading the session file and saving it included, two reports kept, one sheet |
| **Through `rehearse_each`** | 31.0 to 31.1 s for the same two as functions |
| **Each lands as its panel shows it** | B and C, painted for real on the painting they were tried on, are their panels to the pixel on both sheets |

About 16 s a version -- the painter's own *about 15 s a variant*, for variants with their
films and drying, where step 2's bench timed the three ramps alone at 10.4 to 10.7. The
sheet costs nothing the painter was not already paying: the paint is the cost, as step 2
measured, and what changes is one image where there were two files and a montage, and
each version's own check beside it.

## What step 8 did *not* touch

What any mark lays, the log and the stream: a version is a rehearsal, on a copy. The
single `--rehearse`, stacked scripts on one copy, `rehearse(vary=)`'s pixels (its panel
arithmetic moved into `_panel_scale` unchanged), and **the MCP `run`'s single rehearsal,
which still hands back its look's path and not the picture** -- a client with no file
access cannot see it, which is a gap of its own, flagged in the PR rather than folded in
here. D1 is declined.

## File map

| File | What changed |
|---|---|
| `src/easel/cli.py` | `--alternatives`; `Alternative`, `Alternatives`, `run_alternatives`; `_cmd_run`'s branch |
| `src/easel/session.py` | `rehearse_each`, `_versions`; `_panel_scale`, `_panel_label`, `_strayed_text`; `_rehearse_sheet` uses `_panel_scale`; `rehearse()`'s and `scratch()`'s docstrings |
| `src/easel/mcp_server.py` | `run(alternatives=)`, answering as a list |
| `scripts/probe_handover_session.py` | `trial_versions`, `probe_alternatives`, `--alternatives` |
| `tests/test_requests.py`, `tests/test_mcp.py` | *0.7.0 D0* |
| `REFERENCE.md`, `PAINTING.md`, `README.md` | the flag, the call and the tool argument |
| `CALIBRATION.md` | *A variant's cost*: *Built, in step 8* |
| `CHANGELOG.md` | `[Unreleased]`: this step's section |
| `SUGGESTIONS.md` | finding 4 filled in; the round's counts |
| `PLAN-0.7.0.md` | status; 4D marked built, with what the build found; the order of work |
| `NOTES-step8.md` | this file |

## Next

Step 9, workstream G: the three sentences (G1 the backwards lit-air sentence, G2 the
caveat beside its rule, G4 the wet layering as a number) with
`scripts/check_guide_blocks.py` green, and the record -- `LESSONS.md` (the data points on
the way in and on `explain`; *a measurement is not a method*; the cross-machine
papercut), `SUGGESTIONS.md` closed, #70's line, `README.md` and `llms.txt` where a count
or a claim moves. Then step 10, the cut. Read the plan's 4G and section 6 first.
