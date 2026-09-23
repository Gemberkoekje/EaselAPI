# Step 4 of `PLAN-0.7.0.md`: the session file without its time-lapse, and the release that saved it

**To understand this, start by reading the plan's workstream F, then `Session._film`,
`Session.load` and `_warn_older_engine` (at the foot of `src/easel/session.py`), then
`REBUILDS` in `src/easel/notices.py` and `_load` in `cli.py` and `mcp_server.py` -- and
read `NOTES-step3.md` first if you have not, because every rehearsal saves the file since
step 3 and this step is what makes that save cheap.**

Branch: `session-file-and-engine-stamp`, off `main` at `17844ef` (step 3, #77).

---

## What this step was for

The painter's file was 16.1 MB after 171 marks, and 8.8 MB of it was a time-lapse it made
once, at the end (finding 7; decided, question 4). And its notes promise a pixel-identical
rebuild that relies on the release it painted with, so it asked to be told when a later
release stops keeping that promise (question 8). Nothing here changes what a mark lays:
no golden moved.

## What landed

| | |
|---|---|
| **The file keeps no frames** | `save()` writes `frames` empty -- the shape 0.6.0 writes for a painting with none, so 0.6.0 opens the file |
| **A loaded session's film is the log's** | `Session._film_from_log`, set by `load` on a frameless file: no frame is recorded after the load, and `timelapse_gif()`, `contact_sheet()`, `easel timelapse` and the MCP `timelapse` rebuild the film at the session's frame size through `Session._film()` |
| **An undo from a file builds no frames** | `undo`'s rebuild passes `frames=False` when the film is the log's |
| **A file that kept its frames keeps them** | an older file loads with its film and goes on recording, as before |
| **The engine stamp** | `engine` in the meta; `_saved_by(meta)` dates a file without one by its `notices` key |
| **`older-engine`** | a fact, said at load when a fix since the file's release lays some of its marks differently, counted per fix; registered, in `REFERENCE.md`'s table, pointing at `CALIBRATION.md`'s *The log, undo, and the stream* |
| **`notices.REBUILDS`** | `RebuildChange(version, what, heading, moves)`, one row so far (0.6.0's smudge); `rebuild_moves()`, `version_key()` |
| **What a file says at load reaches the painter** | the shell prints it on stderr under `at load`; the MCP server puts it at the top of the tool's answer (`_load`, `_said_first`, `_tool`); `notices.block(when=)` |
| **The probe** | `probe_handover_session.py --shell [--engine SRC]`: the painter's passes through `easel run`, the file and `easel timelapse`, each engine in a `-S` child; `--file` puts the frames back so it still measures the file 0.6.0 wrote |
| **Tests** | `test_requests.py` *0.7.0 F1* (6) and *0.7.0 F2* (6); `test_notices.py`, the fixes against `CHANGELOG.md` (3); `test_mcp.py` (1) |

## The numbers

The painter's workflow as it ran it -- `easel new`, the thirteen passes through `easel
run` one at a time, then `easel timelapse` -- under `main`'s engine (`17844ef`) and this
branch's, each in a `-S` child on a quiet machine
(`probe_handover_session.py --shell --engine <main's src> --engine src`):

| | before | after |
|---|---|---|
| the thirteen passes through `easel run` | 45.6 s | **36.5 s** |
| the file | 16.43 MB, 174 frames | **7.37 MB**, none |
| load, save (best of three) | 0.30 s, 0.79 s | 0.24 s, 0.29 s |
| `easel timelapse` at the end | 2.4 s, a read | **26.6 s**, a rebuild |
| the GIF | 172 frames at 341x256, 1.14 MB | the same |

The passes are a fifth quicker -- no frame built after any mark, a smaller file to read
and write -- and the film at the end costs 24 s more, so this painting's whole workflow
spends about 15 s more than it did: the trade the painter chose (*paying that once for a
GIF is fine*). Not counted in the table, and on the same side of it: every rehearsal
saves the file since step 3, at 0.29 s where it was 0.79.

## Decisions and gotchas

**1. A session loaded from a frameless file records no frames -- or its film would start
in the middle.** The plan's F1 said a loaded session has no frames and rebuilds them;
left at that, a script that loaded a file, painted a pass and asked for a GIF would have
got a film of its own pass, because the frames recorded after the load are frames and
`timelapse_gif()` would have used them. So the loaded session records none
(`_auto_frame`), and its film is always rebuilt. The same fact makes every pass from the
shell or the server cheaper: each is a load, and each built a frame after every mark --
42 ms at 1024x768 (`CALIBRATION.md`, B15) -- for a file that now throws it away.

**2. The film is rebuilt at the session's frame size, and it is the recorded film, frame
for frame.** Not at the canvas's size, which is what `from_log=True` builds at: the
fallback exists so that `easel timelapse p.easel p.gif` goes on writing the film it
always wrote, and the test holds the rebuilt frames equal to the recorded ones, array for
array. `from_log=True` keeps its meaning -- any size, the canvas's own by default.
`--from-log` on a `.png` was ignored before and still is; a contact sheet has no size.

**3. `older-engine` is said at load.** The plan said *loaded, replayed or undone*; every
undo and replay of a file starts with a load, and a notice said at the load is said
before anything moves, which is when it can still change what a painter does. Said once:
the next save stamps the file with this release. A command that does not save --
`check`, `export`, `log`, `timelapse` -- says it again next time, until one does.

**4. Only where something moves, and counted.** Each fix carries a `moves(record)`
predicate, and the notice counts the marks each one lays differently; a painting with no
smudge in it is not told about the smudge fix. A notice that fired on every older file
whether or not a fix touched it would be `LESSONS.md`'s second rule broken -- a painter
doing nothing wrong, warned. When step 6 builds B, its row's predicate is the one piece
of it that has to be exact enough to count.

**5. A file without the stamp is dated by its `notices` key.** 0.6.0 writes one on every
save and nothing before it writes one at all (checked against both tags), so a file with
the key is 0.6.0 -- or step 3's build, which lays as 0.6.0 does -- and one without is 0.5.0
or earlier. That is finer than the plan's *0.6.0 or earlier*, and it matters: told
*0.6.0 or earlier*, a 0.6.0 painting with a smudge would have been told its smudges
replay without a cap they never had.

**6. The list starts at 0.6.0, and the test holds it by count.** 0.6.0 is the first
release whose `CHANGELOG.md` summary names its rebuild-changing fixes in a fixed form --
*One fix changes what a rebuild lays* -- so that form is what `test_notices.py` reads:
every row's heading is under its release, and every release that says *N fixes* has N
rows. A fix before 0.6.0 is in its entry's prose and not in the list, and a file dated
before 0.6.0 is told so rather than told the list is complete. A release not yet cut is
read from `[Unreleased]`.

**7. Until the cut, this build calls itself 0.6.0.** `__version__` moves in step 10, so
the stamp says `0.6.0` on every file saved until then, and the gate -- a file is told only
when its release is older than this one -- keeps a file this build saved from being
told about fixes it already has. The cost is the other side: between step 6 (B, keyed
`0.7.0`) and the cut, a 0.6.0 file loaded here is not told either. Both end at the cut.
The tests do not depend on it: they patch `_engine` and add a stand-in fix.

**8. What a file says at load now reaches both surfaces.** It reached the shell as a raw
Python warning, the engine's own file name and line first, and the MCP server not at
all -- the gap 0.6.0 closed for what a call says and left open for what a file says. The
shell prints it on **stderr**, because stdout is where `easel look` prints the path a
painter's script reads back; the server puts it above the first text of the answer, or
of a failure. `foreign-out-dir` arrives the same way, and until now had never reached an
MCP painter.

**9. What 0.6.0 does with a file this build wrote -- checked against the tag.** `v0.6.0`'s
own `src`, in a `-S` child: it opens the file with 0 frames; its `timelapse_gif()` says
*No time-lapse frames were recorded*, which is 0.6.0's own message and points at
`from_log`, which works; and its save drops `engine` and `reports` and keeps `notices`.
This build then dates that file 0.6.0, by the key, and says nothing.

**10. A frame captured by hand lives in the process.** `capture_frame()` still records,
and its film is written by `timelapse_gif()` in the same process; the file does not keep
it. Said in its docstring and in `REFERENCE.md`.

## What step 4 did *not* touch

What any mark lays. No golden, sampler or rebuild moves.

## File map

| File | What changed |
|---|---|
| `src/easel/session.py` | `_film_from_log`, `_load_notices`; `save` writes no frames and the stamp; `load` dates the file, keeps an older file's frames, says `older-engine`; `_film`, `timelapse_gif`, `contact_sheet`, `_auto_frame`, `undo`; `_engine`, `_saved_by`, `_warn_older_engine`; docstrings |
| `src/easel/notices.py` | `older-engine`; `RebuildChange`, `REBUILDS`, `rebuild_moves`, `version_key`; `block(when=)` |
| `src/easel/history.py` | the two constants' comments; the no-frames message names `--from-log` |
| `src/easel/cli.py` | `_load`; `timelapse`'s description and help, and its line before a rebuild; `new --frame-px` and `--no-timelapse` help |
| `src/easel/mcp_server.py` | `_load`, `_OPENED`, `_said_first`, `_tool`; the `new` and `timelapse` docstrings |
| `scripts/probe_handover_session.py` | `--shell`, `--engine`; `--file` puts the frames back |
| `REFERENCE.md`, `CALIBRATION.md`, `README.md` | the row; the session file; the paragraph `older-engine` points at, and the film; the index row; the undo paragraph |
| `tests/test_requests.py`, `test_notices.py`, `test_mcp.py` | the tests above |
| `CHANGELOG.md` | `[Unreleased]`: this step's section |
| `SUGGESTIONS.md` | finding 7 filled in; the counts |
| `PLAN-0.7.0.md` | status; F1 and F2 marked built, with what the build changed |
| `NOTES-step4.md` | this file |

## Next

Step 5, workstream A: `feather=`, inward and broken by the tooth, as the default on every
hard edge and every clip; `roughen()`; the goldens opened and looked at. Read the bench
note in 4A first -- the feather's unit at 1440 is still open.
