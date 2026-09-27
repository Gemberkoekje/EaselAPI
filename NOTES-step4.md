# Step 4 of `PLAN-0.8.0.md`: what each call cost, which marks a finding counted, and a prelude's name bound again

**To understand this, start by reading the plan's C, H1, H2 and H3 with their *Step 2* and
*Step 4* notes, then `Session._dearest_line`, `Session._marks_named`, `_CallSite` and
`_painter_site` in `src/easel/session.py`, `pass_block` and `_rebound` in `src/easel/cli.py`,
and `_place_notes` in `src/easel/look.py` -- and read `NOTES-step2.md` first if you have
not, because this step builds what that one measured and the painters then decided.**

Branch: `dearest-calls-and-named-marks`, off `main` at `25e80c9` (the first painter's
step-2 answers, #92).

---

## What this step was for

Both painters' passes came back from rehearsal with one total -- the Bell-Warden's subject
pass at 85 to 113 strokes over five rehearsals, Wenna Brask's figure at 135, 101 and 99 --
and neither could tell which call had grown, though the log knew. A finding counted marks
it did not name, so the second painter found the mouth's four marks by hand; its log
printed `#9e6c57` where its palette said `lip`; and a pass replaced a name its prelude bound
without a word, twice. Every one of these was decided by a painter (questions 8, W-Q3) or
narrowed by step 2's bench, so this step builds them as decided, and checks the engine's
line against the bench's over every pass the corpus has. Two small things ride with it: a
guide note's box moved off the boxes already drawn (4b), and the error `s.px(25)` raises
naming the oval (O9).

## What landed

| | |
|---|---|
| **C: the dearest calls** | `_CallSite` and `_painter_site`: the painter's line, found once per mass call in `_one_call` and once per mark laid by hand in `stroke()`, kept in `Session._sites` by the mark's index. `_calls_in` groups records by call; `_dearest_line(since)` says the line. `cli.pass_block` puts it under the total in `easel run` (rehearsed, counted, committed), per version in `run_alternatives`, and in the MCP server's `run` -- and so in every saved report |
| **H1: a finding's marks** | `_pass_findings(named=)`: every rule that counts marks hands them to `_marks_named`, whose line goes under the finding; `_buried` hands back the details it counted too. `_graded_band`, `_daisy` and `_loop_runs` return their marks; `_disc_group_marks` beside `_disc_groups`, whose shape the corpus probe reads |
| **H1: the colour's name** | `params["color_name"]` on a stroke record (`_colour_named`), carried by a replay; `History.summary` prints it in place of the hex |
| **H2: a prelude's name bound again** | `cli._top_level_names`, `_rebound`: said as `prelude-rebind`, a fact, before the pass runs; registered in `notices.py` and `REFERENCE.md`'s table |
| **H3: `--scale`** | `type=float` on `look` and `timelapse`, `_SCALE_HELP` first, `_scale_px`: a number under 1 a share of the long side |
| **A1: notes kept apart** | `look._place_notes`, `_overlap`; `_draw_guides` draws a leader to a note moved a row or more out |
| **A5: the error** | `Session.px` names a brush's `size=`, the pencil's `width=`, `feather=`, `s.circle(p, px=)` and `ellipse(p, *s.px(rx, ry))` |
| **The bench** | `probe_bell_session.py --built`: both paintings rebuilt with no watcher and compared with the watched rebuild's line pass by pass; the corpus replayed with `BuiltWatcher`, the engine's line beside the bench's; the findings' names; `prelude-rebind` over the corpus's scripts. `--answers` gains the engine's note placement; `--guides` compares the line with the notes left aside |
| **Tests** | `test_requests.py` *0.8.0 C* (6), *H1* (3), *H2* (2), *H3* (1), *A1* notes (1), *A5* error (1); `test_mcp.py` one for `run` |
| **Documents** | `REFERENCE.md`: the dearest line under the shell's *After every pass*, a finding's names in `report()`'s paragraph, `prelude-rebind`'s row and the prelude's paragraph, `--scale`, the log's colour names. The README's check and budget rows; `CHANGELOG.md`; `CALIBRATION.md`; `SUGGESTIONS.md` (six rows, the count); the plan |

## Decisions and gotchas

**1. The painter's line is the first frame outside the engine -- by module, not by path.**
`_painter_site` steps past every frame whose module is `easel` or `easel.*`, and past
`contextlib`'s, which `_one_call` adds; the first other frame is the painter's -- a pass,
the prelude (compiled as `prelude.py`), a painter's own module, `<stdin>`. The verb of a
mark laid by hand is the outermost public engine method the painter's line called (`dab`,
`glaze`, `paint`); a mass names itself. **A harness that wraps the verbs sits where the
painter's line would be**, so the probe rebuilds both paintings with no watcher for the
engine's line, and replays the corpus with the engine's walk patched to step past `probe_*`
modules too (`_site_past_probes`): the corpus checks the grouping, counting and words, and
the two paintings check the walk.

**2. Where a call was made is this process's, and is never saved.** `Session._sites` maps a
mark's index to its `_CallSite` -- compared by identity, so two calls from one line of a
loop are two. Keyed by index, it survives an `undo` that rebuilds from the log (the kept
marks keep their indices); a rehearsal copy starts from a copy of the painting's, so a
finding on the copy can name the painting's own marks, and what the copy lays stays its
own; a file keeps none, so `easel check`, reading a painting in another process, names
marks by record alone. A stale entry an `undo` left behind is never read: every mark
writes its own when it is laid, and only marks in the log are ever named. Nothing about
it touches a record, the log's indices or the stream: a test lays the same marks from other
lines and gets the same log, byte for byte.

**3. A call made inside a helper is named at the helper's line.** Step 2's decision 2 left
it to the build. The Bell-Warden's three dearest calls are three lines of one helper,
`lay_body`, called once -- the pass's own line would have named all three as one. So the
line names where the verb was called, as the bench did and as the painter chose from the
bench's example; 19 of the corpus's 143 lines name a prelude's helper, and 21 name two calls
at one line, most of them a loop's.

**4. The line counts the painting's own log, and nothing else.** Its total is the pass's
charged marks, `History.paid_marks` over the pass, which is the number the rehearsal's head
line prints; the bench summed every mark of paint, which differs only where a pass lays a
signature, and no pass of either painting did. **And the corpus found the bench's one
miscount**: over the replay the engine's line is the bench's word for word on 140 of the
143 passes where either prints one, and the other three -- the pears' `p9_rehearse_pear.py`,
`p10_rehearse_pear.py` and `p11_pears12.py` -- each call `s.rehearse(plan)`, which lays the
plan on a copy. The bench's watcher wraps the class, so it saw the copy's `block_in` and
counted it as the pass's; the engine never sees it, because the copy's marks are in the
copy's log. So the engine prints nothing on the first two, whose own calls are a stroke
each, and *23 of the 31* on the third, which laid 31 marks of its own -- where the bench
said *36 of the 48*. Step 2's figures for the line (43% of painted passes, a median 76% named)
count those three passes as the bench saw them; the difference is three lines of 143.

**5. The line goes under the total, as the first line of the pass's block** -- so it is in
every saved report's text -- and not in `report()`. A painter at a Python prompt calls
`report(since=)`, which is over a pass or over the whole painting, and a cost line over the
whole painting says nothing; the line stays `easel run`'s and the server's, as the plan
wrote it. `s._dearest_line(since)` is there if a painter asks.

**6. A finding's names are a line of their own.** Under the finding, four spaces in, so the
finding's own sentence -- which probes and tests match -- is unchanged: *laid at
p05_face.py:58 (lay_mouth), :62, :64, :72 (lay_modelling) -- records 174, 176, 177, 179*,
the script once per run of it, the function once per run of calls from it, as the dearest
line names them. A loop's line is named once with its count of calls (*pass.py:5 (4
calls)*), at most six lines and eight runs of records are written, and a run of three or
more records is a range. The rule that counts every mark of a pass, one brush at one size,
names none: its marks are the pass.

**7. The helpers' shapes.** `_graded_band`, `_daisy` and `_loop_runs` hand back the marks
they counted, and `_buried` the details it lost: private, one caller each.
`probe_cohort_session.py` reads `_disc_groups` as `(count, (x, y))` pairs, so
`_disc_group_marks` sits beside it with the marks, and `_disc_groups` is that without them.

**8. A colour's name.** A string that is not a hex is kept as the palette reads it
(lower case, spaces as underscores) -- a slot, or a pigment, `white` included; numbers are
named when they are exactly one slot's colour, which is what `palette["lip"]` hands over,
and a hex or an unmatched colour has no name but itself. A smudge lays no colour and gets
none (the verb hands it `titanium_white`). `_replay_records` carries the key over, since a
replay is handed the colour and not the name.

**9. `prelude-rebind` is read off the text, and said first.** As the bench counted it:
top-level bindings through `if`, `for`, `with`, `try` and `match`; the prelude's by
assignment, `def` or import only; *something else* by what the name is bound to, as source
-- finer than the bench in three ways: a whole `def`, where the bench counted any `def` of a
name the same; an import name by name, so `from easel import polygon, ellipse` after `from
easel import polygon` is the same `polygon`; and a tuple unpacked from a tuple element by
element, so `W = 768` after the prelude's `W, H = 768, 1024` is the same `W`, where the bench
counted every unpacked name as something else. A bare annotation, `x: int`, binds nothing.
Told on none of the corpus's 284 passes or 17 filed rehearsals, as the bench found. Said before the pass runs, because the painter's case was
a pass that raised on the rebinding -- `failed()` prints what was said, so the traceback
arrives with its cause.

**10. `--scale` is a float now**, on `look` and `timelapse`; under 1 it is a share of the
canvas's long side, at least one pixel, and `look --scale 0` is still the canvas's own size.
The server's `look` and `timelapse` take `int`, which the SDK puts in their schemas, and a
client is told so before it sends a fraction; they are left alone.

**11. A note moves only when it must.** Up and right of its guide's first point, as before,
unless a box is there; then that point's other three corners; then the four a row further
out, up to eight rows, with a leader -- a dark line under a light one, like the box and its
letters. A note whose guide begins outside the view (a crop) is left where it was. A
drawing whose notes never met draws exactly as before, which is why the bench's
`casing 150` sheets -- the ones the painter judged -- keep their notes, and its identity
check is of the line alone now.

**12. On this machine.** A bash heredoc holding Python with nested quotes failed with
*unexpected EOF* -- append long text with the editor. `pytest -x` stops at the first
failure; the first full run stopped at the missing `REFERENCE.md` row, as it should have.

## What step 4 did *not* touch

What any mark lays. No golden, no sampler and no rebuild moves: the one key a record gains,
`color_name`, is read by nothing that lays paint, and where a call was made never reaches a
record. `PAINTER.md` is untouched, 45 words from its budget. The MCP server's tools take
what they took.

## File map

| File | What changed |
|---|---|
| `src/easel/session.py` | `_CallSite`, `_painter_site`, `_index_runs`, `_colour_named`; `_sites` and `_call_site` on a session, a copy and a loaded file; `_one_call` and `stroke()` note the site; `_calls_in`, `_dearest_line`, `_marks_named`; `_pass_findings(named=)` and its helpers' marks; `report()` and `checklist()` name them; `px`'s error; `color_name` on a record and through a replay |
| `src/easel/cli.py` | `pass_block`; `_top_level_names`, `_rebound`, `_said_as_list` and the notice in `run_script`; `_SCALE_HELP`, `_scale_px`, `--scale` as a float |
| `src/easel/mcp_server.py` | `run` says the dearest line through `pass_block` |
| `src/easel/look.py` | `_place_notes`, `_overlap`, the leader; `_GUIDE_CASING_ALPHA`'s comment (4b answered) |
| `src/easel/history.py` | the log line's colour by its name |
| `src/easel/notices.py` | `prelude-rebind` |
| `scripts/probe_bell_session.py` | `--built`, `BuiltWatcher`, `_site_past_probes`, `replay_built`, `probe_built`; `rebuild(watch=)`; `engine_note_boxes` in `--answers`; `--guides` checks the line alone |
| `tests/test_requests.py`, `tests/test_mcp.py` | the tests above |
| `REFERENCE.md`, `README.md`, `CHANGELOG.md`, `CALIBRATION.md`, `SUGGESTIONS.md`, `PLAN-0.8.0.md` | as above |
| `NOTES-step4.md` | this file |

## Next

- **Step 5 (E)**: the key and the place reading -- `plan(key=)` with the clusters printed
  and not judged (E1), the median (E2), `at_value`'s error at the floor (E3's part that is
  built), and the named light's 95th percentile beside its median (E4). Nothing waits on a
  painter.
- **For step 9 (F)**: `REFERENCE.md`'s `report()` paragraph gained a sentence here, which
  F2 turns into tables with the rest; the dearest line's paragraph under the shell is new.
