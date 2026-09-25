# Changelog

Every release of [`easel-paint`](https://pypi.org/project/easel-paint/), what changed in
it, and why. PyPI links this file from the project sidebar (the `Changelog` entry under
`[project.urls]` in `pyproject.toml`), so this is the page a painter lands on from the
package page.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project uses [semantic versioning](https://semver.org/spec/v2.0.0.html). Before 1.0.0 a
minor bump is where behaviour is allowed to move, and this is what it may move. **A
painting saved to an `.easel` file opens as it was painted**: the file holds the canvas,
and loading never repaints it. **A rebuild from its log lays the same strokes with the
engine installed** — `replay(upto=)`, `timelapse_gif(from_log=True)`, and every `undo`
from the shell or the MCP server, since the file carries no snapshots. Every stroke's own
brush arguments are in the log, so a moved default does not reach a rebuild; a fix to
how the engine lays a stroke does, and a stroke an earlier version laid wrongly comes
back fixed. A *script* that leaves a default off can paint something different after a
minor release. Each entry below says which defaults moved, and names every fix that
changes what a rebuild lays.

**Nothing here may say it shipped until the tag exists.** *Released*, *shipped*, and
*Shipped as `vX.Y.Z`* are claims about the world, and the only thing that makes them
true is a pushed tag: `publish.yml` runs on `v*` and on nothing else, so until the tag
is there no wheel has been built and no file has been uploaded. Writing the claim when
a version is *cut* — in anticipation of a tag push, which is a separate act and can
simply not happen — is how 0.5.0 spent a day saying it was on PyPI while the newest
file there was 0.4.0, and how the round filed after it was nearly cut as 0.6.0 over a
version number that was still free. Cut the version, write the entry **without** the
claim, tag it, and add the claim afterwards. `tests/test_version.py` holds every such
claim in this file to a tag that exists, and holds `pyproject.toml` to the newest
section here so a version cannot be skipped.

The engine's own record of *why* a rule is a rule lives elsewhere and is not duplicated
here: measurements in [`CALIBRATION.md`](CALIBRATION.md), the requests painters made and
what was done about them in [`SUGGESTIONS.md`](SUGGESTIONS.md), and the method in
[`LESSONS.md`](LESSONS.md).

## [Unreleased]

- **A script or prelude saved with a byte-order mark runs** in `easel run` and MCP `run`:
  Windows PowerShell 5.1's `Set-Content -Encoding utf8` writes one, and it did not parse.

### Looking without the labels, a whole pass as a plan, and what a rehearsal was told

Step 3 of the lighthouse handover's round (`PLAN-0.7.0.md`, workstreams E and C0). One
painter against 0.6.0 wrote a helper to take the landmark labels off its looks, ran its
variants through a harness because it believed a glaze could not go into a plan, and
twice saw a check misfire on a rehearsal that left no trace in the file.

- **`easel look --no-marks`**, and `marks` on the MCP `look` tool: `look(marks=False)`
  has existed since 0.4.0 and neither the shell nor the server could say it, so the
  painter's `clean_look.py` is now `easel look p.easel --no-marks --no-sketch`.
  `--no-sketch` has always hidden the guides `s.guide()` draws as well as the pencil;
  its help, the MCP `sketch` argument, `look()`'s docstring and `PAINTING.md` now say
  so. The plan had proposed a `guides=` switch on the belief that nothing hid them, and
  it was not built.
- **The plan grammar is written down whole.** `REFERENCE.md`'s sentence named three of
  the five kinds a plan lays — a mark, a mass, a sweep — and now names the passage
  (`band=`) and the burial (`cover=`) too, and the film: a mark with `glaze=True` and
  the glaze verb's own brush and opacity written out, because an entry takes a stroke's
  defaults and a bristle film at `0.88` is not a glaze. One sentence says a whole pass
  is a plan. The same in `preview`'s and `rehearse`'s docstrings and the MCP plan help;
  `tests/test_reference.py` holds the grammar to every kind a plan can lay. A smudge is
  not named, because as a mark it takes the smudge brush's `0.07` rather than the
  verb's `0.02` and says none of the verb's notices.
- **What a pass was told is saved, rehearsals included.** Every `easel run` and MCP
  `run` keeps the block it prints after a pass — what the calls said, then the check —
  in the `.easel` file, under a new `reports` key beside `notices`: `s.reports()`,
  `easel log --reports`, `log` with `reports` through the server. **A rehearsed or
  counted pass keeps its block too**, marked as such, with the log index it began at.
  Both of the painter's misfires were printed by rehearsals of passes it then
  rewrote, so without this nothing in the file could show that either had happened.
  Older builds do not read the key and open the file as before.
- **So a rehearsal now writes the session file**, and nothing else of the rehearsal goes
  into it: the log, the canvas and the random stream come back as they were, held by a
  test in the *planning verbs leave nothing behind* pattern.
- **A rehearsal copy has its own palette, landmarks and guides.** `scratch()` shared the
  painting's three, so a mixture, a landmark or a guide made on the copy stayed on the
  painting. Nothing saved the painting after a rehearsal, so nothing showed it, until
  the report had to be saved. **A Python script that made a mixture on a `scratch()`
  and then used it on the painting now raises `KeyError`**: make it on the painting.

### The session file without its time-lapse, and the release that saved it

Step 4 of the lighthouse handover's round (`PLAN-0.7.0.md`, workstream F). The painter's
file was 16.1 MB after 171 marks, and 8.8 MB of it was a time-lapse it made once, at the
end. And its notes promise a pixel-identical rebuild that relies on the release it
painted with, which it asked to be told about when that stops holding.

- **The `.easel` file keeps no time-lapse frames.** The painter's painting, rebuilt the
  way it was painted, saves at **7.37 MB** where it saved at 16.43. The `frames` array
  is still written, empty, which is what 0.6.0 writes for a painting with none, so 0.6.0
  opens the file — checked against the tag.
- **A session loaded from a file makes its film from the log.** It records no frames — a
  frame recorded after a load would begin the film in the middle of the painting — and
  `timelapse_gif()`, `contact_sheet()`, `easel timelapse` and the MCP `timelapse` replay
  the log when asked, at the session's own frame size: **frame for frame the film it
  recorded**, for a full repaint where it was a read: **26.6 s** for the painter's
  painting, where reading its frames took 2.4, and the same GIF of 172 frames. A
  painting made in one Python process keeps its frames in memory as before; a file
  saved before 0.7.0 that kept its frames still uses them; `from_log=True` still builds
  at any size. `easel timelapse` says it is rebuilding before it starts.
- **So every pass from the shell or the server is cheaper**: no frame is built after a
  load, and the file is written without them. The painter's thirteen passes through
  `easel run` take **36.5 s** where they took 45.6, and every save — which every
  rehearsal makes since the report went into the file — takes 0.29 s where it took
  0.79. A painting that makes one film at the end spends about 15 s more in all, which
  is the trade the painter chose: *paying that once for a GIF is fine*. An undo from the
  shell or the server builds no frames as it rebuilds.
- **The file says which release saved it** — `engine` in its meta, read with `.get` —
  **and a file saved by an earlier release says so as it opens when a fix since then
  lays some of its marks differently**: `older-engine`, a fact, with how many marks each
  fix moves and the release to rebuild it under. The canvas opens as it was painted
  under any release; what does not is an undo, a replay or a film made from the log,
  which lay every mark again with the engine installed. Said once, since the next save
  stamps the file, and said only where a fix moves something. A file without the stamp is
  dated by what it carries — a `notices` key is 0.6.0, none is 0.5.0 or earlier. The
  fixes are `easel.notices.REBUILDS`, and `tests/test_notices.py` holds them to the ones
  each release below names as changing what a rebuild lays: so far, 0.6.0's smudge.
- **What a file says as it opens reaches the painter.** The shell prints it on stderr,
  under *at load*, where it arrived as a raw Python warning with the engine's own file
  name and line first; the MCP server puts it at the top of the tool's answer, where it
  went to the server's stderr and reached nobody. `foreign-out-dir` arrives the same way.

### An edge that breaks rather than steps, and an outline nobody ruled

Step 5 of the lighthouse handover's round (`PLAN-0.7.0.md`, workstream A). The painter
laid its tower, lantern and headland hard and called the edge *the least paint-like
thing in the engine, and I relied on it*: a clip was cut as one pixel of four values and
then a step, `0.30` of value in one pixel at the tower. Blind, it chose one of four
candidates for every hard edge and every clip, and asked for the rock's outline to
wander.

- **A held edge breaks inward, against the canvas's own tooth** — `feather=`, on every
  verb that takes `clip=` and on `block_in`, `scumble` and `cover` under `edge="hard"`.
  Over the last `0.002` of the long side inside the outline — two pixels at 1024 — the
  tooth decides how much of the edge takes paint, the way it does for a starving brush:
  crisp where the weave is high, broken where it is low. **Nothing lands on or past the
  drawn line.** It reads as paint and not as blur, which a plain ramp did.
- **This is the default, and one moved.** Every hold breaks at `0.002` unless told
  otherwise — `clip=` as well as `edge="hard"`, because four of the painter's nine
  edge-drawing calls were clips — and `feather=0` cuts the edge on the line, which is
  what every hold was before and what a line ruled on purpose wants. **A saved mark
  replays at the feather it was laid with**, and one saved before 0.7.0 carries none and
  replays cut, so no saved painting moves and `older-engine` has nothing new to say;
  **a script that leaves `feather=` off lays the broken edge where it laid a cut one**.
  Over the ten corpus paintings whose scripts hold an edge that moves 0.00% to 1.92% of
  a canvas; the scripts are listed in `NOTES-step5.md`.
- **A share of the long side, like `size`**, benched at 1440, where the painter found the
  bench's copy *a little chewed*: built, the edge there bites at the export's own pixels
  as it does at 1024 (`0.94` px against `0.94`), and a two-pixel count is no closer.
- **The frame is not an edge**: a side lying on the canvas frame never breaks, so a mass
  run off the canvas does not pull back from it. **A thin shape keeps its body**: on a
  shape narrower than four feathers the edge breaks over a quarter of its width, where a
  clip two pixels wide had kept 37% of its paint.
- **Two masses held to one line both break back from it**, and on bare ground the ground
  shows between them — the guide's *paint masses, never up to a line*, now visible where
  a cut edge hid it. No committed painting lays its masses that way; one of
  `RECIPES.md`'s passages did, and lays its first mass past the line now.
- **`roughen(shape, amp=, step=, seed=, calm=)`** walks an outline off its own line with
  a correlated wander — the painter's own fifteen lines — for rock, a shore, anything
  nobody ruled. Nothing on the frame moves; `calm=` stills it where something stands on
  it; an open run of points comes back a run with its two ends where they were. On the
  MCP server it is a place builder beside `blob`.
- The notices that name `edge="hard"` as a remedy — `spill`, `round-fringe`, and
  `clean-small` for a burial — say the edge is broken rather than cut. A new golden
  case, `edges`, holds the edge where it was decided.

### A dry brush that streaks rather than speckles

Step 6 of the lighthouse handover's round (`PLAN-0.7.0.md`, workstream B). At the loads
the guide recommends for a broken mark the painter's starved brushes left dots, not
streaks — *dark flecks in the sky, speckled first swells, and blue specks in the surf* —
and its way round them, films, dropped the texture it wanted. It asked for the engine to
change and for a load to keep its meaning: *the amount was right, the shape was wrong*.

**One fix changes what a rebuild lays**: a brush running dry drags its paint into
streaks along its travel rather than dotting it, so a mark saved before 0.7.0 that ran
dry replays streaked — and a file saved before it says so as it opens, with how many of
its marks (`older-engine`). Over the committed paintings, rebuilt, 2,788 of 5,628 marks
run dry somewhere — a preset bristle's tail drags as surely as a mark laid starved — and
a rebuild moves a median `2.4%` of a canvas, up to `19.8%`: in every painting, the dots
in a dry passage become streaks along its strokes.

- **A brush running dry drags.** Under `0.9` of its load, and wholly by `0.7`, the
  tooth a brush is gated against is read along the stroke's own direction — averaged
  over a thread of linen, `0.0088` of the long side, and given back the tooth's own
  values rank for rank — so what clears the gate is a run of pixels rather than one;
  and a `bristle` comb's bristles run dry one by one, each keeping its own share of the
  canvas, the wettest the most. The sky's own crosser at `load=0.45`: **571 pieces with
  a median of 4 px become 125 with a median of 12**, nearly three times as long along
  the travel as across it, and the specks under 4 px carry 1% of its paint where they
  carried 8%. On the painter's first surf, the blue specks become strokes of foam.
- **Each load lays what it laid.** Summed over 24 strokes at a load, a starving
  `bristle` on linen lays `0.99` to `1.02` of what it laid, from `0.30` to `0.8`; the
  rest of the table is in `CALIBRATION.md`, under *A dry brush that streaks*. One stroke
  on its own can lay a third more or less than the next where one or two bristles carry
  it, as a dry brush does.
- **A loaded brush, and a dab, lay exactly what they laid.** Above `0.9` of its load a
  brush is gated as it always was, to the bit: `solid=True`, every `cover()` and banded
  `scumble` (laid solid since 0.6.0), the inward scumble at the brush's own `0.9`, a
  loaded preset over a short run. A one-point mark has no travel to drag along; a
  `bristle` one still runs dry bristle by bristle.
- **Nothing new touches the stream or the log.** A bristle's share is drawn from its
  comb, not from the stroke's generator, so the log, the stream states in it and every
  mark laid after a starving one are what they were.
- The goldens that carry a brush running dry — the three `marks_*` cases, `shapes`,
  `sweep` and the sampler's hash — were opened and regenerated, and
  `samples/brushes.png` re-rendered: the dry tails' square holes run with the stroke
  now. `scripts/probe_handover_session.py --dry` benches the built gate beside 0.6.0's,
  and `--corpus-dry` rebuilds every committed painting under both.
- Five sentences said *speckle* or *flecks* for what a starved brush leaves and say
  *broken streaks* now: exercise 3 in `PAINTER.md`, the `load` paragraph in
  `PAINTING.md`, the plane recipe's failure in `RECIPES.md` and its row in
  `DIAGNOSIS.md`, and the graded field's row beside it.

### The graded rule, broken where marks lie side by side

Step 7 of the lighthouse handover's round (`PLAN-0.7.0.md`, workstream C). Twice the
check told the painter *graded passage laid too narrow* about marks that were not a
passage, both times on a rehearsal, and both times the brush it named was a thin accent
laid among wider marks: a crevice along the join of two rock faces, a ripple among the
glints of a reflection.

- **A graded passage is laid one stroke over the next, and the rule now asks.** Its run
  of parallel marks breaks between two neighbours across the stack whose reaches *along*
  it share under 30% of the shorter one's. The painter's water misfire — five glints of
  one colour, a foam mark and a `0.006` ripple, one below the next and none over another —
  falls apart into marks and is told nothing; laid again from the painter's rehearsal,
  the rule as 0.6.0 had it prints the painter's line to the character. The recipe's own
  failure block still fires, and its passage still says nothing.
- **Over the committed paintings it fires on 7 of 337 painted passes, where it fired on
  9.** It keeps the three the painter, reading the crops blind, called a passage coming
  back as bars — two beams, and the pier's water, which 0.6.0's rule missed — and goes
  quiet on three of the six it called separate things. What it still tells is separate
  masses stacked edge to edge, which overlap along the stack as a passage does: the
  painter's headland misfire is one, and was the price it chose. On the pier's water the
  brush the line names is a reflection laid across the field, not the field's own.
- **The share is the middle of a plateau**: every share from 10% to 40% fires on the same
  seven passes.
- **Judging the run by its median brush was not built.** On the painter's reading it
  silences every passage among the rule's fires.
- The check reads the log, so nothing a pass lays, and nothing a rebuild lays, changes.
  `scripts/probe_cohort_session.py --graded` holds the engine's own line to the gate on
  every pass of the corpus and sweeps the share; `scripts/probe_handover_session.py
  --misfires` lays the four cases the gate was drawn on.

### Versions of a pass, rehearsed side by side

Step 8 of the lighthouse handover's round (`PLAN-0.7.0.md`, workstream D). The painter
compared its variants as whole passes — scumbles, strokes and films — run one after
another through a harness of its own around `scratch()`, a file each, looked at in turn,
and said what would have replaced the harness: *rehearsing scripts as side-by-side
alternatives. `easel run --rehearse a.py b.py` stacks them instead.* Laying them on one
copy is right for a pass that goes on top of another, and wrong for two versions of one.

- **`easel run p.easel a.py b.py --alternatives`**: the scripts are versions of one pass,
  and each is rehearsed on a copy of its own — its own check printed and its own report
  kept, as a rehearsal's is — and their looks are laid side by side in one sheet,
  `rehearse_NNN.png`, each panel labelled with the script and the strokes it laid. **Every
  copy is seeded as the next marks of the painting, so the version then run for real
  lands as its panel shows it**, to the pixel. It implies `--rehearse`; with `--count` it
  prices each version and lays no sheet; `--check` checks each over the painting under it;
  a sheet holds at most twelve, as `vary=`'s does. A version that raises is said and left
  off the sheet, and the others are still rehearsed, because none stands on another.
- **`s.rehearse_each([...])`** is the same from Python, where a version is a plan or a
  function handed the copy — which is what a script is inside Python. A function whose
  helper paints on the painting instead of the copy is stopped, with the records to undo.
- **Through the MCP server, `run` takes `alternatives`** — a list of scripts, or an
  object naming each — and hands the sheet back inline, as the looking tools do. **So
  `run` answers as a list**: declared as answering in text, it had its answers checked as
  text, and a picture beside the text failed as an error. What a client reads is the same;
  `run` no longer carries `structuredContent`.
- **`run(rehearse=True)` hands back the copy's look inline too**, beside the text that
  still ends in its path: a client that cannot open a file had no way to see it.
- **The painter's own two skies**, `try_sky3.py`'s B and C from the painting's drawing,
  take 32.1 to 32.3 s through `--alternatives`, loading and saving the file included,
  where its harness took 31.9 to 32.8 s for the same two: about 16 s a version, the
  *about 15 s a variant* it timed, because the cost is the paint. What changes is one
  sheet where it had two files and `montage.py`, and each version's own check beside it.
  Each lands as its panel shows it.
- **D1, a sheet's panels in processes of their own, is not built**, as the painter decided
  on step 2's bench: four panels in four processes took 1.6 to 1.7 times one here, against
  a target of 1.5, and a version's cost is its paint, which no sheet takes away.
- A version is a rehearsal, on a copy: nothing a pass lays, and nothing a rebuild lays,
  changes.

### Three sentences put right, and the round recorded

Step 9 of the lighthouse handover's round (`PLAN-0.7.0.md`, workstream G). The painter
found one sentence of prose backwards — *the one factual error I found was in prose* — and
a caveat a file away from its rule; asked what to do about the weight of the
documentation, it answered *watch*.

- **The lit-air recipe says which end of a round tip is wide.** *A volume of lit air*
  called a film at `pressure=[1.0, ..., 0.1]` narrow and bright at the source. A round
  tip's width follows pressure, so it is wide and bright there and narrow and gone at
  the far end, and the wide faint film runs the other way to open the cone; the
  sentence says so and cites *Pressure* in `CALIBRATION.md`. The block and its demo were
  right and are unchanged: laid alone, the core is 49 px across near the light and 16
  where it gives out.
- **The fade arrives late, and the recipe says how late.** *A passage brightening toward
  one side* gains the number beside its rule: the dabs overlap, so at the recipe's own
  `opacity=0.5` a quarter pressure moves the value over half as far as full pressure
  does and a tenth still a quarter as far, and a band at
  `pressure=[1.0, 0.75, 0.25, 0.0]` reads `0.41` over its last third and `0.19` over its
  last twentieth on a `0.15` field. It names the reason where it lives, *`opacity` does
  not thin a long stroke* in `PAINTING.md`, and the table is new under *Pressure* in
  `CALIBRATION.md`.
- **Ramps laid wet, as a number and not a rule**: three ramps laid one on another wet
  change a third of the canvas by more than two levels of colour against the same
  ramps dried between, and draw no seam either way — under *`scumble`* in
  `CALIBRATION.md`. `wet-under` stays declined.
- **The record.** `LESSONS.md`: a measurement printed beside the work is a warning with
  a figure in it — the `edges:` line said 54% to 65% eleven times and the painter kept
  its hard edge; a painter told where to start reads what it likes, and read three rules
  and broke them; `explain` and `diagnose` went uncalled, so a notice's code stays
  unlinked to its `DIAGNOSIS.md` row, on the evidence; and *byte for byte* is a claim
  about one machine, *to the stroke* the one that travels. `SUGGESTIONS.md` closes the
  round, every item in it done.
- **Counts that had moved.** Thirty notices, where the README and `llms.txt` said
  twenty-nine before `older-engine`; the README's rebuild claim is to the stroke, and to
  the byte on one machine; and the documents' sizes are the ones they have — the card is
  about 1,400 words, where six places said a thousand or under (the CLI's help and the
  MCP `guide` tool's among them), and `REFERENCE.md` about 8,800, where `llms.txt` said
  3,600.
- Nothing a mark lays, and nothing a rebuild lays, changes.
  `scripts/probe_handover_session.py --pressure` measures all three sentences.

## [0.6.0] — 2026-09-22

**Released.** Shipped as `v0.6.0`: `easel-paint` 0.6.0 on PyPI, the GitHub release with
`easel.mcpb` attached, and `io.github.Gemberkoekje/easel` 0.6.0 in the MCP registry.
Every job of the publish run passed on its first attempt.

**One round, and the first painted by models other than Claude.** Seven painters — GPT,
GLM, DeepSeek, Gemini, Grok, Kimi and BigPickle — each installed `easel-paint` 0.5.0
from the package and painted one picture, and were told nothing about what to read. They
came back with thirty-two engine items and six documentation items, filed in
`SUGGESTIONS.md` under *The 0.5.0 cohort*; the round was worked from `PLAN-0.6.0.md`.

**Its shape is one sentence taken at its word** — the one two earlier sessions' verdicts
both lead with: *reading the warning did not stop me; the rehearsal image and the
post-pass check did*. So wherever the tool can know a thing it now says it, and the
paragraph that used to say it has left the guide. Twenty-nine notices carry a code and
the measurement behind it, and reach `easel run` and the MCP server alike; the painter
writes the plan down in `s.plan(...)` and the check answers to it; `report()` reads the
canvas as well as the log, and `checklist()` answers the closing lines; `easel explain`,
`easel diagnose` and `easel demo` deliver the reasons, the symptom index, and nineteen
recipes painted beside how they go wrong. Every new check was measured on the corpus
before it was built — all 21 paintings rebuilt pass by pass — and as this release
stands, 197 of their 325 painted passes say nothing at all. The way in is new as well,
and like every change to the guide it is a hypothesis until a fresh session paints
against it.

**Three defaults moved**, each under *Defaults moved* below: a banded `scumble` lays its
passes solid, `edge="hard"` carries two brushes of overhang, and `cover()` holds a
burial to its place. **One fix changes what a rebuild lays**: a smudge no longer starts
loaded with white, so a smudge saved in an `.easel` file replays without its cap (*Three
checks that read the canvas under the mark*).

### One channel for everything the engine says at a call

Step 3 of the 0.5.0 cohort's round (`PLAN-0.6.0.md`, workstream A). Nothing the engine
says has changed its words; what has changed is that it is now one thing with a name,
and that it reaches the painter it was said to.

**The problem.** Every call-time warning was a bare `warnings.warn(str)` from one of
twelve `_check_*` functions, two methods and three inline sites. No class, no code, no
collection — so a pass could say four things and the only place they existed was the
console's scrollback; **and through the MCP server they reached nobody at all**, because
`mcp_server.py` never touched `warnings` and converts exceptions only. For a painter
working through a client, *the tool warns you* was false for everything except
`report()`.

- **`easel.notices`**, new: `EaselWarning`, which subclasses `UserWarning` and carries a
  stable `code`; `Notice`; and `NOTICES`, the registry of all 21 codes with what each one
  is and which passage of the guide measured it. Each is a **fact** — a number about what
  this call will do — or a **habit**, a rule of thumb a painter can be right to break.
- **`Session._notify`**, and all 21 warning sites converted to it. A notice is kept on the
  session and then warned, so a painter at a Python prompt sees exactly what they saw
  before. `s.notices(since=None)` is the list; it round-trips through the `.easel` file
  under a new `notices` key, which older builds do not read, so a 0.5.0 Easel still opens
  a file this one wrote.
- **Notices live beside `history.records`, never in it.** A mark's texture is seeded from
  its place in the log, so anything new that took an index would repaint every painting
  ever made. The *planning verbs leave nothing behind* test covers it, and caught a
  mistake in this very change.
- **`easel run` prints them in one block with the post-pass check**: *at the call* first,
  *over the pass* second, facts before habits, one line per code however many calls
  tripped it, with the stderr copy filtered so it is said once and in order. A pass that
  raised says them too, beside the error. The MCP `run`, `cost`, `preview` and `rehearse`
  results carry the same block — which is the half of this that did not exist.
- **`easel explain <code>`**, `s.explain(code)`, and an `explain` MCP tool: the passage of
  `CALIBRATION.md` or `PAINTING.md` that holds the measurement. This is where a rule's
  reason goes when its paragraph leaves the reading path — not deleted, delivered at the
  moment it applies. `easel.docs.section()` is the new function underneath it.
- **`REFERENCE.md` grows *What the tool will tell you***, a row per code, and
  `tests/test_notices.py` holds the three surfaces against each other: every code the
  engine says is registered, every registered code is a row of that table, and every row
  points at a heading that exists in the document it names. A renamed heading in the
  guide is now a failing test rather than an empty answer.

**0.5.0 is released**, and this paragraph spent a while saying the opposite. `v0.5.0` is
tagged at `54c2a0b` and `publish.yml` ran on it and succeeded, twenty minutes after the
merge that wrote the denial — so the denial was true when it was typed and false by the
time anybody read it. That is trap 15 in `LESSONS.md` twice over from one act: the first
version of this paragraph claimed a release *before* the tag push, and its correction
outlived the tag push that made it wrong. **The pair to check is the tag list and PyPI,
never a paragraph**; `tests/test_version.py` now checks the claim against the tags rather
than against anybody's memory, which is what that trap asked for.

What still holds: releasing is a tag push — `git tag v0.6.0 && git push origin v0.6.0` —
and `publish.yml` refuses a tag that disagrees with `pyproject.toml` before it uploads
anything, because a PyPI version number cannot be reused once taken. The version is
written by hand in `pyproject.toml` and copied into `src/easel/__init__.py` and both
entries in `server.json`; `tests/test_version.py` and `tests/test_server_json.py` hold
every copy to the one in `pyproject.toml`. This round was cut as 0.6.0 in all four of
them, tagged `v0.6.0` at `3d6fe74`, and given its claim only once the tag and the run
it starts had both happened. The round's working file and its step notes left the
repository with the claim; the tagged copies are
[`PLAN-0.6.0.md`](https://github.com/Gemberkoekje/EaselAPI/blob/v0.6.0/PLAN-0.6.0.md)
and `NOTES-step6.md` to `NOTES-step9.md` beside it.

### Eighteen reported bugs, and the API gaps behind them

Step 4 of the 0.5.0 cohort's round (`PLAN-0.6.0.md`, workstream B). Seven painters
reported eighteen bugs and API gaps; **every one was checked against the source before
it was planned, and measured again by the corpus probe** — which is how four of the
reported mechanisms turned out to be something else, one bug turned out larger than
reported, and one turned up a second, silent bug beside it.

**Where the paint may land, and whether the brush may run dry, are now questions every
verb answers.**

- **`clip=` on `block_in`, `sweep`, `cover` and `scumble`.** It was a named argument of
  `stroke` alone, so the four mass verbs answered a question about where their paint
  goes with *`clip=` is not a brush field* — an error naming neither `stroke(clip=)`
  nor `edge="hard"`. `edge="hard"` **is** a clip pointed at the place the call fills,
  so a mass given both is held by both: the coverage masks multiply and the paint lands
  where they agree. A run of points is a clip too, which is what a painter has in hand
  when the boundary came off the reference.
- **`scumble(edge="hard")`**, its mass form. A band crossed at an angle paints up to
  **3.6×** its own area, because the auto brush is measured across the bounding box;
  this is the remedy for it, and `"clean"` is refused with the reason — a passage has
  no contour to draw. The scumble ends check runs on rectangles too, so the guide's own
  `span(...)` bands can trip it at last: a band is not a wedge, so what it is asked is
  whether the **whole band** is narrower than the brush laying it.
- **`solid=` on `stroke`, `sweep` and `scumble`**, as `block_in` has always had it. It
  is `load=1.0, load_falloff=0.0` everywhere, it is the clause painters type by hand
  most often, and an explicit `load=` beside it still wins. `cover()` lays that pair
  already and is the one call that still says so instead of taking it.
- `REFERENCE.md` grows **Which verb takes which hold**, and `tests/test_reference.py`
  holds every cell of it by *making the call* rather than by reading the signature:
  three of these verbs take their holds through `**kw`.

**A plan can hold a passage and a burial, and cannot hold what it cannot paint.**
`scumble` and `cover` could not be planned, priced, previewed or rehearsed at all, and
a scumble-shaped entry carrying `shape=` was **priced as a block-in** — five where the
call lays eight — raising only when `paint()` reached the keys `block_in` does not
take. `{"band": place, "color_a": ..., "color_b": ...}` is a passage now and
`{"cover": place, "color": ...}` a burial, priced by walking the same geometry the
painting walks. And `PLAN_ACCEPTS`, read off the signatures, refuses a key the call
would not take **before the entry is priced**: `cost` never touches the brush
overrides, so a misspelled `size` used to price happily at the default and raise when
the same plan was painted. The MCP server has refused these since it was built and now
imports the registry rather than keeping a second one.

**The time-lapse, and what a mark costs before it is paint.**

- **`Session(timelapse=<px>)`** and **`timelapse_gif(from_log=True, scale=)`**. Frames
  were recorded at 360 px beside a 1440 px painting, stored in the `.easel` file at
  that size, with nothing able to ask for another — so a painting already made could
  not be helped. The film can now be rebuilt by replaying the painting, at any size,
  storing nothing, and that works on a painting that recorded no frames at all.
- **A frame is built only if the thinning would keep it.** Past 200 frames the sequence
  is halved, so most of the 42–60 ms a mark spent building one was spent and thrown
  away. The film that comes out is the one that came out before.
- **A stroke snapshots the box it can reach**, not the whole canvas: 15.7 MB and 5.2 ms
  become 3.5 MB and 1.85 ms at 1024×768, and 377 MB resident becomes 107. Wetness stays
  whole, because drying touches every pixel. Undo is exact or it is nothing: the stack
  unwinds newest first, and a mark that ever landed outside its box drops the stack
  rather than restoring it wrongly, leaving `undo` to rebuild from the log.
- **A rehearsal says where its frames are.** `timelapse_gif` on a rehearsal copy said
  *create the session with `timelapse=True`*, which is the one thing the painting
  already did.

**`s.rehearse(plan, vary={"size": [0.02, 0.05, 0.08]})`** — one labelled panel per
setting, in place, in one image. Calibrating a mark meant four rehearsals, four
whole-canvas renders and four pictures nobody can hold side by side, and a question
about size is a question only comparison answers. Free, like any rehearsal, and each
panel is its own copy seeded as the next marks of the painting, so the setting chosen
lands as it was shown.

**Five smaller ones, each an answer somebody went looking for and did not find.**

- `report()`'s **subject line** built its total out of every mark of paint while the
  budget exempts the first five noted `signature`: a painting read *172 of 411 marks* a
  line under a budget that said 408.
- A **ground name used as a colour** listed every pigment and slot without noticing it
  is a valid ground, and the canvas was blind the other way round. Both say which
  namespace the name belongs to now, and **`s.ground`** is the ground as a colour —
  sampling an unpainted corner was the only route to it.
- A list of **0–255 integers** clamped, so `[13, 12, 16]` came back **white**, in
  silence, and `PAINTING.md` documented the trap. It raises and names both fixes. A
  documented trap the engine can see is a bug.
- **`solid-comb`**, a fact at the call: `solid=` closes the gaps *along* a pass and not
  the ones a comb leaves *across* it — `0.16%` of the mass bare on a mid ground and
  `3.16%` on a dark one, because a hole is a contrast rather than a gap — with what
  each remedy costs. No default moved: a comb is the right brush for anything with
  strands in it.
- **`block_in(dry_first=)`**, off by default, as `cover()` has always had it on.

**And four answers to *where would a painter find that out*.** `undo(n)` and
`log(last=)` say they count **log records**, which is what `replay(upto=)` already
said — and so do `easel undo`'s help and the MCP `undo` tool, which said *strokes* and
*marks, at most 24 kept*, where a session file carries no snapshots and every `undo`
through either is a rebuild from the log, as far back as it is asked; `region("bottom")` is a **ninth** of the canvas and `REFERENCE.md` now prints
every named region's extents, held against the engine by a test; the five shipped
documents are held to **cp1252**, so `print(easel.docs.read("calibration"))` prints on
a Windows console, where 35 characters used to break it; and **`import easel_paint`
works**, because the distribution is `easel-paint` and the guess in the other direction
installs an unrelated package called `easel`. Both import names are the same objects,
and the documents keep teaching the short one.

### What the painter writes down, where the engine can see it

Step 5 of the 0.5.0 cohort's round (`PLAN-0.6.0.md`, workstream C). One painter put the
whole of it in a sentence: *useful heuristics, but they're philosophy, not errors, and it
doesn't know which*. Inventoried and true — before this there was no acknowledge, suppress
or declare mechanism anywhere in the API, so a painter whose subject really was horizontal
could only read the same warning again.

- **`s.plan(why=, values=, lightest=, subject_share=, bands=, ground=)`**, and
  `easel.plan` behind it. `Session(budget=)` was the first of these declarations — a
  number the painter writes down and the engine then holds them to — and these are the
  rest of them. Saved in the `.easel` file under a new `plan` key, read with `.get`, so a
  0.5.0 Easel opens a file this one wrote and a 0.5.0 file opens with no plan. Beside
  `history.records` and never in it, for the reason the notices are: a mark's texture is
  seeded from its place in the log.
- **A declaration, not an acknowledgement.** Written up front rather than as an
  `accept()` called after a warning has fired — the decision taken when this round was
  planned, and the difference is that a painter can be held to a plan and can be wrong
  about it. The check says so either way; a suppression only ever says *stop talking*.
- **Every declaration changes a line of the check.** `values` adds
  *plan: 5 of 6 places inside 0.10; halo +0.14*, and registering it says which planned
  pairs are within `0.10` **and meet** (`plan-pairs`) — asked on the empty canvas, where
  it is free, which three rounds of painters skipped and the two that answered it
  answered wrong. `lightest` says when something else took the light. `subject_share`
  puts *against 40% planned* on the subject line, which `report(subject_share=)` has
  taken since 0.4.0 and **neither `easel run` nor the MCP `run` tool ever passed**, so
  from a shell the comparison had never once been printed.
- **Two standing warnings become numbers.** `bands="subject"` answers what the
  stack-of-bars line concedes it cannot know, and the line then counts what crosses the
  bars instead of warning about them: it is the noisiest rule the engine has — **47 of
  the corpus's 325 painted passes, 14%**, after the decay that already cut the pier's
  seven firings to three, and half of every line the engine prints — and the one two
  painters learnt to skim. `ground="buried"` does the same for the bare-ground floor,
  which five of seven painters in this round accepted by hand.
- **The finding-11 contradiction is resolved in both halves, in one commit.** The
  graded-field recipe buries the ground and the closing checklist asks for some back;
  both are right, so the picture decides. `RECIPES.md` names the declaration where it
  buries the ground and `PAINTER.md`'s checklist line concedes the case, and the floor is
  unchanged for a painting that has not said — because the corpus shows what it is for:
  half of all 21 paintings finish under it, cohort or not, and an earlier one chose a
  warm ground *to be seen through* and finished at `0.07%` without noticing.
- **Declared once, from wherever the painter is.** A `prelude.py` — which `easel new` now
  writes, holding the call commented out, because a worked example is an instruction and
  a plan filled in with somebody else's numbers is worse than none — or `easel plan
  p.easel --value 'A1:H3=0.70' --bands subject`, whose places are names because a shell
  has no `blob()`, or the MCP `plan` tool. Calling it again changes what it is given and
  keeps the rest, and re-declaring the same values says nothing the second time, which is
  what lets a prelude run before every pass without the pairs notice becoming a thing
  printed once a pass.
- **`s.compare(s.plan())`** measures the canvas against the plan the session is holding,
  sheet and all. A plan that has to be retyped to be checked is a plan that drifts, and
  the drift arrives as paint.

**Four claims this round found stale, and the two checks that stop them recurring.**
`PLAN-0.6.0.md` still said only workstream A was built; `SUGGESTIONS.md` said the
right-hand column of every table in the open round was empty, with two of them filled in;
the paragraph above about 0.5.0's release outlived the tag that made it wrong; and `easel
explain --help` offered `spill` as an example of a code, which is one this round planned
and did not build — so the one place the tool demonstrates its own vocabulary was
advertising a word it answers *unknown notice* to. The examples are **generated from the
registry** now, and `scripts/check_guide_overlap.py` **runs in the suite**
(`test_one_home_per_rule`), which is how the fifth one was found: it had been reporting a
duplicate since the notice channel put *a mark's texture is seeded from its place in the
log* into `REFERENCE.md`, where `PAINTING.md` already had it, while `SUGGESTIONS.md` went
on claiming it reported zero. A script somebody has to remember to run is the preference
that rule is about.

### Two checks at the call, off the geometry of the passes

Step 6 of the 0.5.0 cohort's round (`PLAN-0.6.0.md`, workstream D1). Both are faults the
documentation named and the tool did not catch, and both are said at the call — before
a dab lands — from the passes the call is about to lay.

**`chisel-staircase`.** A `flat` or `knife` filling a mass along a straight side it runs
*nearly* along ends its passes down that side in ledges, and the side comes back as a
staircase: finding 1, and Kimi's rock faces were `RECIPES.md`'s own *a mass built of
planes*, character for character. The plan's window of angles measured how irregular a
shape is rather than how it stairs and did not survive being built; the rule is the
mechanism instead — a pass end lands every `step × cot(θ)` down a side, so it is
*nearest parallel* that a chisel steps worst — and it fires on **2%** of the corpus's
painted passes against the prototype's 6%. The three recipes that produced it were fixed
in the same change, and `edge="hard"` stopped being offered as its remedy: these are pass
ends *inside* the mask, and it measures 22% to 20%.

**`spill`.** A ragged `block_in` whose passes will cover **1.6x** the place it was handed
or more says so — the multiple, the share of the paint outside the place, and the brush's
share of it — with the answers `PAINTING.md` gives: inset the place by half the brush, a
brush under a fifth of it, or `edge="hard"`. A banded `scumble` says so at **2.0x**,
because its own brush breaks past the band by design and the band its brush was tuned on
covers 1.69x laid along its axis; a planned band says it when `cost()` walks it. Over the
corpus it fires on 18 calls in 13 of 325 painted passes — **4%**, the prototype's own
share — and on none of the guide's blocks.

- **Predicted off the passes, not read off a rule of thumb.** The plan's version was *a
  brush over a fifth of the shorter extent*, and `PAINTER.md`'s own first `block_in` lays
  a brush 60% of its shape and lands 1.48x of it. So the call walks its passes on a copy
  of the stream and lays each as a strip as far past its line as that tip's paint
  reaches, measured: fitted on 126 masses and bands painted for the purpose, it is within
  2% of the paint on average for a chisel or a band and within 5% for a comb or a round
  tip. Under twelve pixels a brush does not land where its outline says, and the rule
  stays out.
- **A band crossed at an angle (B17)** covered `2.95x` itself at 30 degrees with nothing
  saying so. The notice says `3.0x` and names `edge="hard"` — the same passes, held to the
  band. **The auto brush is not capped**, which was the plan's open question: a cap at
  the band's depth still leaves `2.22x`, and one at half the depth brings the bars back.
  At 60 degrees `scumble-dabs` already fires, and `spill` stands aside for it.
- **Not said inside `cover()`**, whose default holds a burial to its place since F1
  (*Defaults moved*, below). Asked for `edge="ragged"` by name, its ends run outside on
  purpose and paint about three times a cell, and a rule that fires on the form a
  painter asked for is a rule painters learn to ignore.
- **It fired on three of the guide's own blocks, and all three were painting their
  neighbours**, so the blocks moved and the rule did not. The value scale in
  `PAINTER.md`'s exercises covered twice each band; its passes now run along the bands,
  which also takes it from **189 strokes to 27**. The swatch strip lays a brush a fifth
  of each swatch's width. The per-stroke overrides example in `PAINTING.md` filled one
  grid cell with a brush wider than the cell, and now fills a place its brush fits.
- `PAINTING.md`'s paragraph on paint landing outside the shape is one line naming the
  code; the three answers stay, and the measurement lives in `CALIBRATION.md`, *Paint
  that lands outside the place*.

Nothing paints differently: both are notices, and the only code that changed what it lays
is the guide's own.

### Three checks that read the canvas under the mark, and a smudge that lays nothing of its own

Step 6 of the round, workstream D2: the tool reads the paint a mark meets. The two smudge
checks are said at the call, before the smudge lands, off the canvas along the path it
will be stamped down; the film check reads a glaze once it has landed, as `holes` reads a
mass.

**Fixed: a smudge started loaded with white.** Its carried colour began as its nominal
`titanium_white` and took in 45% of the canvas per dab, so its first dabs laid 55%, 30%,
17% white — a light cap at the start of every smudge, on a passage of one colour as
much as at a boundary: `0.13` of value over a mass at `0.45`, where it now moves nothing.
It starts from the first colour it touches. The cap was part of finding 3's
*thumbprint*, and it was what the round's own probe had measured as crossing: light
carried **4.1 brushes** into the dark by a pass that started in the dark. With the start
fixed that pass carries it **0.5**. **This paints differently, and not only for
scripts**: the first brush-width of every smudge moves, a smudge already saved in an
`.easel` file replays without its cap, and the three `marks` goldens and the brush
sampler moved with it — looked at, and regenerated.

**`smudge-across`** (a fact). Dragged across a boundary, a smudge carries the first mass
about a brush into the second — `1.2` brushes at `size=0.04` across a step from `0.20`
to `0.78`, either way round. The call says so when its path crosses a step of `0.10`
or more, with half a brush of path before the line and a quarter after it; a pass that
only starts or stops on the line is not told. Over the corpus it speaks on 11 of 37
smudges, in 9 of 325 painted passes (3%), and on none of the guide's blocks. The
prototype it replaced tested the range of the values under the whole path, fired on both
heron necks — which run *along* a lit edge striped with short marks — and missed the one
pass that dragged a dark hull out into the water.

**`smudge-long`** (a habit). Along a boundary a smudge leaves a strip about a brush tall
at the value halfway between the two, at any length: a softened corner over a short
stretch, a third band over a long one. The call says so when the path follows a step of
`0.05` or more for more than `0.10` of the canvas: 14 smudges, in 11 passes (3%), none
of the guide's blocks. The prototype fired on the path's bare length, and the corpus's
median smudge is `0.168` long.

**`glaze-far`** (a fact). A film that moved the passage under it by `0.08` or more in
value — *a stripe of a different colour*, in the guide's own table — or that was mixed
`0.07` or more from what it lands on in hue and chroma, which no opacity rescues. The
first is not said about a film given `to_value=`, which asked for its shift; the second
is, because the search lands a value and not a colour. Over the corpus: 38 of 222
films, in 17 passes (5%) — 22 by the value line, 16 by the mix line alone — and none
of the guide's blocks once `PAINTING.md`'s own example stopped glazing raw alizarin.

- **The guide's own examples ran the smudges the new rule is about.** `RECIPES.md`'s
  *An edge that is actually lost* smudged half the canvas directly above its own
  paragraph saying not to go past a tenth, and `PAINTER.md`'s step 6 a third of it;
  both now smudge a stretch. `PAINTER.md`'s edge study laid its *soft* edge as a smudge
  down the middle of the light panel, 20 px from the boundary it was meant to soften,
  beside a *hard* line in the panel's own colour, so it showed neither: both are on the
  canvas now. `PAINTING.md`'s glaze example glazed raw alizarin, against the rule in
  the paragraph under it, and now mixes its film from what it lands on.
- The three rules about `smudge` in `PAINTER.md`'s step 6 are one paragraph naming the
  codes, and `RECIPES.md`'s strip paragraph and `PAINTING.md`'s glaze table are a line
  each; the measurements live in `CALIBRATION.md`, *Across a boundary, and along a long
  one* and *A film far from what it lands on*.
- `CALIBRATION.md`'s first line about `smudge` said it pulls the lighter mass into the
  darker more than the reverse. On a dried hard step it is symmetric — `0.49` brushes
  each way, before the fix and after — and the bullet says so now.

**A fourth was proposed and declined: `wet-under`**, an opaque mark laid on paint still
wet and far from it in colour. Its evidence was finding 5's rings, and the painter's own
frames put their cause elsewhere: an inward `scumble`'s own contour rings, laid over a
bezel still wet, which moved them by up to `0.13` (`CALIBRATION.md`, *GLM's rings*). As
a habit rule it fired on **22%** of the corpus's painted passes and on **8** of the
guide's blocks, because laying opaque paint into wet paint is most of what the guide
teaches, and wetness is no gate: the corpus lays its opaque marks on paint at a median
wetness of `0.09`, and a tenth of them over `0.41`. What was left of it, a fact line at
the call, rests on a reconstruction of
a take its painter overwrote, and is not in this release either. *`dry()` first* stays
in `PAINTING.md`.

### Three findings after the pass: a daisy, a loop's signature, and details a layer buried

Step 6 of the round, workstream D3: three new lines in `report()`, the check `easel run`
prints after every pass. The step-2 prototypes of all three fired on the wrong passes —
of the 22 the daisy prototype named, one was a daisy, and the burial prototype's 54 were
mostly a nearer thing painted over a farther thing's details, which is back-to-front done
right — and each was looked at pass by pass and rebuilt on what the pictures showed. All
three are habits: a subject can radiate, a row can be a row, and a pass can bury on
purpose. None fires on the guide's 71 runnable blocks.

**A daisy.** Five or more hand-laid marks, each at least twice as long as its brush is
wide, leaving one point in every direction: no gap in the circle of their directions
over 90 degrees. The point is where consecutive marks' lines meet, so a ray from a
disc's rim counts as well as a petal from its centre. A tree's fork, a tuft of grass, a
fan of rays and a glow of wide films are not one. One pass of the corpus's 325: the
fogged glass's tree, which its painter's verdict calls *spoke-like*.

**A loop's signature.** Six or more consecutive hand-laid marks of one brush at one
length, or a strict ramp of lengths, evenly spaced on a line and far enough apart to read
as marks — finding 7's *floating rectangles* and ziggurat. One pass: DeepSeek's glitter
path, which was the painter's fix for the rectangles — eight flashes meant to shorten
toward the viewer, all `0.100` long.

**Details a film or a mass buried.** Earlier small or `subject` marks that were showing
as the pass opened and were left at under half their contrast by a glaze or by the passes
of a mass. Two passes, both burials: a pier's pile reflections under a graded scumble,
and a pool's far lamp under the films that lifted its water. It needs the canvas as the
pass opened, which `easel run` and the MCP `run` tool now keep, and which a script
calling `report(since=)` after each pass gets from the report before. **It does not see
a detail taken down a little at a time**: the one burial a painter wrote down, a chair
under three deck glazes, lost less than half its contrast in every pass and stood too
close to the deck to count as showing. `CALIBRATION.md` has the numbers; it is open.

- `PAINTER.md` step 5's daisy sentence is gone, and step 3's *veil of light* bullet is
  one line naming the check. `RECIPES.md`'s daisy, `PAINTING.md`'s *any loop or
  generator* row and `scumble`'s docstring say that `report()` names them.

### The canvas, measured, and the closing checklist answered

Step 7 of the 0.5.0 cohort's round (`PLAN-0.6.0.md`, workstreams E and G4). Everything
the check could say until now came off the **log** — brush, size, path, pressure, note
per mark. Four of the closing checklist's questions cannot be answered from a log at
any length, because they are about the canvas rather than about a call, and every one
of them was a question a painter answered by looking. Those are the ones three cohorts
answered wrongly.

**What `report()` now prints after every pass**, beside the findings and the `ground:`
line that was already there:

- **`values:`** — the 5th to 95th percentile of the values view against what the box
  can reach, and the three clusters the picture splits into: *0.15-0.35 of a box that
  reaches 0.13-0.96, clusters at 0.17, 0.25, 0.32; no clear light*. The range is asked
  against the palette first and the clusters against each other after, because a
  picture can have three well-separated clusters and still have nothing light in it —
  which is the pier's own verdict, and heron 1 had nothing light until stroke 217.
- **`edges:`** — how the picture's edge length divides between hard and soft, by the
  rise width of each boundary. Finding 13: `report()` said *nothing to report* over a
  picture whose every boundary was crisp, and GPT's own verdict on it names *equally
  crisp boundaries*. Nothing in the log can see it — an edge is what two neighbouring
  masses do to each other, not either one's arguments.
- **`pencil:`** — graphite still showing, as a share. The one line here whose right
  answer is not zero: a drawing showing through thin paint is worth keeping.

**And one at the call:** a mass laid `solid=True` now says what actually came back
bare inside its own outline, a brush in from the edge so a ragged edge is not counted
as a hole. `solid-comb` predicts the holes from the brush and the density; `holes`
measures the canvas once the paint is on it, which is the only way to answer for the
shape, the ground and the overlap. It is silent where the paint sits within `0.15` of
its ground, because **a hole is a contrast, not a gap**: the same comb leaves `0.16%`
bare on `toned_grey` and `3.16%` on a dark ground, and the second number is the
measurement finding paint that barely registered rather than a hole anybody can see.

**`s.checklist()` / `easel check`** is the closing checklist as output: every line
with a number behind it answered — values, edges, ground, pencil, boxes, the subject's
share, what the plan promised, what the audit found, and what is left of the budget —
and then the three that nothing can measure, printed as questions with the painter's
own `s.plan(why=...)` quoted back. `PAINTER.md`'s checklist shrinks to those three and
the call, which is 239 words out of the front page.

The boundary is the point, and it is kept: *the check cannot see a composition*. Every
line above is a number about a mark or a pixel. A picture can pass all of them and
have quietly become a different picture, competently painted — so *is the thing you
measured most carefully still attached*, *which passage is the weakest*, and *is the
reason you chose this subject still in it* are asked and not answered.

**One published number was wrong, and is withdrawn.** `CALIBRATION.md` reported the
corpus's edges at 12%–44% under 2 px, median 27%. Building the line found that the
prototype selected the top percentile of the gradient — which returns the sharpest
pixels of whatever picture it is handed, so every canvas measures 1.5–2.1 px — and put
its threshold at `2.0` px, which is exactly what the sharpest transition a pixel grid
can hold measures. It called a hard-edged mass 41% hard and a ragged comb 84%, the
wrong way round. What shipped selects edge **ridges** with a step of at least `0.10`
across them and cuts at `2.5` px, which separates a round soft brush (0%) from a
chisel, a comb and a scumble (49%, 49%, 53%) and moves a numerically blurred canvas
from 2.0 px to 6.8. Replayed with it, the corpus runs **21%–62% of edges under
`2.5` px, median 37%**, the cohort no different from the paintings before it, and the
two painters who named *flat cut-out shapes* as their picture's main fault laid the
hardest edges of the 21 but one: Grok's at `62%`, GPT's at `54%`. Nothing else in
workstream E is affected, and `holes:` reproduces B2's three grounds to the third
decimal.

That is the fourth mechanism this round has had to correct after reporting it as
*observed*, which is the shape `LESSONS.md` predicts and the reason the plan puts a
probe in front of every candidate.

### Defaults moved

Step 8 of the 0.5.0 cohort's round (`PLAN-0.6.0.md`, workstream F). Five defaults were
proposed; `scripts/probe_cohort_session.py` measured all five against the corpus and
**two survived**. A third, `cover()`'s edge, was declined for want of evidence and moved
once a bench gave it some. The other two are recorded as declined below, because a
default argued for twice is a default argued for forever.

**A banded `scumble` lays its passes solid** — `load=1.0, load_falloff=0.0`, which is
the pair the `inward` direction has defaulted half of since it was written. A band's
passes have ends and run dry at them, and the verb's own default brush is the one
preset that does not start full (`bristle`, `load=0.9, load_falloff=0.55`), so a wide
pass printed a stripe down the passage that the passes after it did not close.
Measured on a band `0.10–0.90 × 0.40–0.60` at `n=8`: **`5.17%` of it came back within a
hair of bare ground, against `0.01%` now**, with the ripple down it dropping `0.0110`
to `0.0031`. The corpus is what argued for it — **40 of the 60 committed banded
scumbles type the pair by hand** — and that is a default sitting in the wrong place
rather than a rule painters keep forgetting.

- **It is a default and not an override.** `load=` or `load_falloff=` beside the call
  still wins, which is how a band that runs dry on purpose is still asked for.
- **`solid=` therefore moves nothing on a band.** It is still taken, because scripts
  type it; on `direction="inward"` it still raises `load` from the brush's own to
  `1.0`, worth `0.005%` of a patch against `0.012%`. **The inward default was not
  moved**: nothing measured asked for it, and `LESSONS.md`'s first rule is that a
  default moves where a probe says it sits outside its window and nowhere else.
- **What this changes in an existing script.** A banded `scumble` that named neither
  `load=` nor `load_falloff=` now covers its band. Scripts that typed the pair by hand
  paint exactly what they painted before. The graded-field recipe in `RECIPES.md` lost
  the bullet it spent on the clause, and its code block lost the clause with it — the
  paragraph leaving in the commit that made it untrue.

**`edge="hard"` gets two brushes of overhang instead of one** (`block_in`, and `cover`,
which is priced and laid as the block-in it becomes). `"hard"` masks every dab to the
outline, so no paint lands outside it — and it still left the boundary bitten from the
*inside*, in scallops between the pass ends. B8, reported by a painter and isolated
here: the cause is pressure and not reach. The default `pressure="taper"` arrives at
zero one brush out, so at `overhang=1.0` every pass met the outline at part pressure,
and a round tip — which loses *width* with pressure — met it at part width too. On the
3 px strip just inside a sloping outline a `round_hard` left **`0.85%`–`3.26%`** of it
bare at one brush and **`0.055%`–`0.33%`** at two; a `flat`, `0.00%`–`0.66%` against
`0.000%`.

- **It costs dabs and not strokes.** The pass count is identical at one brush and at
  two, so `cost()` quotes exactly what it quoted before. Nothing can cross the mask, so
  the outline does not move either: paint outside it went from 225 px to 227 px on a
  measured case, that difference being the boundary's own feathering, while bare inside
  it went `0.220%` to `0.024%`.
- **`scumble` keeps its own `0.35`.** Its passes are already `pressure="even"`, which is
  the whole mechanism, and it leaves `0.000%` of the same strip bare at every overhang
  tried — so there was nothing to close and nothing was moved.
- **What this changes in an existing script.** Every `edge="hard"` mass that did not
  name an `overhang` — 55 committed calls, none of which do — lays the same passes, the
  same number of them, to the same outline, with the scallops between their ends filled
  in. Looked at as well as measured, on a sloped mass laid with a round tip.

**`cover()` holds a burial to its place** — `edge="hard"` by default, where it was
`"ragged"`. The burying recipe ran its passes a full brush past the place it was handed,
so that no chisel end stopped inside the picture; on a flat passage that cannot be seen,
and on any other it was the fault finding 8 reported — a repair louder than the mistake,
and a painter burying `cover`'s own output by hand. The probe could not weigh it, because
**no committed pass script calls `cover()`**, so it was declined here first and moved
once the owner ruled on a bench of three passages, rebuilt in the probe (`CALIBRATION.md`,
*A burial and the place it was handed*). A repair-sized place, 108×60 px on 900×600,
buried with the default brush in the passage's own colour: on a flat passage neither
edge leaves anything to see; on a graded one `ragged` leaves **`4.45x`** the place
visibly off the passage, nearly all of it outside the place, against **`0.47x`** held;
on a worked one **`4.14x`**, the neighbouring marks under it, against **`0.51x`**.

- **What holding it costs is an outline.** On a worked passage the place's rectangle
  comes back as a value step of `0.042` against the passage's own `0.010` — a crisp
  patch the size of the place, which does read as cut out, and is the smaller fault.
  `edge="ragged"` is the old recipe, one keyword away, and says nothing about its
  overrun.
- **The same passes, priced the same.** Two brushes of overhang under `"hard"`, as for
  any held mass, which costs dabs and not strokes; `cost()` prices a burial as the
  block-in it lays, and now as a held one.
- **`clean-small` asks a region as well as a shape**, and names the call the painter
  made. `cover()` is handed a region far more often than a shape, and at the default
  brush `edge="clean"` on the bench's place left `8%`–`15%` of the mistake showing on a
  painted passage (`22%` on bare ground) with nothing said — the form `cover()`'s
  docstring had recommended for a textured passage. No committed pass script and no
  guide block hands a region to `edge="clean"`.
- **What this changes in an existing script.** A `cover()` that named no `edge` now
  lands inside its place. No committed painting calls it, so none moves.

**Two proposed moves were declined, and the probe is why.** A round tip on
`block_in`/`sweep` to `pressure="even"`: **0 committed calls** would move. A `scumble`
with a `flat` to halved `jitter`/`size_jitter`: the halved pair moves the ripple down a
band from `0.0053` to `0.0059` and the scallop across it not at all, which is nothing
this instrument can see.

### The symptom index, answered rather than grepped

Step 9 of the 0.5.0 cohort's round (`PLAN-0.6.0.md`, G5). `DIAGNOSIS.md` had two
problems and neither was its contents.

**It was not in the wheel.** The build shipped five documents and this was the sixth
file, so `grep -i rings DIAGNOSIS.md` — the interface the file's own first page names —
worked from a checkout and nowhere else. A painter who ran `pip install easel-paint`
never had the index at all.

**And the one session that did have it followed none of its pointers.** In 293 strokes
it recognised five rows on sight — *staircase*, *venetian blind*, *floating discs*,
*searchlight that owns the picture*, *paper cut-out* — and repaired each from the
remembered description, though following the pointers was permitted. A recalled row has
no measurement attached, which is the entire difference between this file and the five
it points into: the one fault it repaired properly, the chisel staircase, it repaired
with `edge="clean"` while the row's own target held a cheaper repair at the other end
of the same table.

- **`easel diagnose <what you can see>`**, `easel.diagnosis.answer()` from Python, and a
  `diagnose` MCP tool. Describe what is wrong on the canvas in your own words and it
  matches the rows and prints **the passage**, not the pointer. There is no step left to
  skip. `--list` (`brief=True`) is the symptoms alone, which is what `grep` used to give.
- **`easel.diagnosis`**, new: the rows, the matching, and a pointer that resolves itself
  to its section. Matching is overlapping words and a plural rule — the rows are written
  in the words a painter uses for the thing in front of them, which is what makes that
  enough. Words that match no row fall back to the `##` section they belong to, so
  *gradient* — a word every group heading has and no row uses — is answered rather than
  refused.
- **`DIAGNOSIS.md` is the sixth shipped document**: `docs.DOCUMENTS`, the wheel's
  force-include table, `easel guide --diagnosis`, and the `guide` MCP tool. It is not a
  sixth guide file — it states no rule, and it still says on its first line that it is
  not for reading.
- **`docs.headings()` and `docs.heading_line()`**, new: one scanner for what a heading
  is, so `section()` and a pointer cannot disagree about where a passage stops, and a
  pointer can go on being readable prose (*`CALIBRATION.md` -> `block_in`*) while still
  resolving to a section. `section()` now steps over fenced code blocks when it looks
  for a heading as well as when it looks for the end of one.
- **`tests/test_diagnosis.py` resolves every pointer to its passage**, all 92, rather
  than only checking that the heading exists. A pointer that lands on a heading whose
  section comes back empty was cosmetic when a person followed it and is a broken
  answer now.

**The file itself is unchanged except its front page**, which is what `LESSONS.md`
asked for: the observation is n=1 and the answer to it is not a row that explains
itself — that row would be the fourth copy the page refuses — but a pointer that costs
nothing to follow. What did change is the arrow: 92 `→` became `->`, because the file
ships now and U+2192 is outside cp1252, which is the B7 fault the other five documents
had already been fixed for.

### The guide's own examples, run past the guide's own checks

Step 9 of the 0.5.0 cohort's round (`PLAN-0.6.0.md`, G7 and G9). Finding 1 was a painter
who laid `RECIPES.md`'s *a mass built of planes* character for character and got the
staircase the guide warns about — **a worked example is an instruction**, and step 6
fixed all three recipes that produced it when it landed `chisel-staircase`. This is the
same question asked of the whole guide, by running every one of its 71 runnable blocks
past every check the engine has and reading what came back.

**Two blocks were teaching the fault the prose beside them forbade.** Neither is visible
to somebody reading the file, because in both cases the prose was right.

- **The three answers under *Masses that are not rectangles*** demonstrated
  `edge="clean"` at `size=0.09` — 34% of that mass's narrowest extent, where the
  paragraph directly beneath it says *under about a quarter*, and where `clean-small`
  fires. The appealing reading was that a clean edge buys back a big brush. It does not,
  and the block now lays the same `0.06` as the answer above it.
- **The graded field drew its own top boundary inside the canvas**, so the passes that
  reached it were cut into stubs of `0.210` against a brush `0.252` wide — dabs that
  bloom past the outline, which is `scumble-wedge`. The recipe's own first line says the
  field has *no outline anywhere in it*; it now runs off the top of the canvas as well
  as the sides. **Turning the pass angle would have silenced the notice without fixing
  the picture** — at 6° and 8° both ends are stubs and the ratio between them falls
  under the threshold — so the shape moved instead. Rendered and looked at, per
  `LESSONS.md`: the old recipe leaves **a patch of bare ground across the top of the
  field**, which is the stub passes failing to close, and the new one covers the canvas.

**Every runnable block in the guide is now notice-clean**, and
`scripts/check_guide_blocks.py` fails if that stops being true: it collects what each
block's session said and names the block, the document and the code. That is the first
half of the plan's G3 invariant, landed early because these fixes needed something to
hold them; the other half — every *failure* block trips exactly the code it names —
landed with the demos, below.

**Three more fixes to what was already there.**

- **`dry()` after the films, not only before**, in *A volume of lit air*. The clause was
  missing, and the measurement is the reason rather than the story the cohort told: B18
  had already shown the films are not wet at full strength, but they do leave `0.14` at
  the core, and an opaque mark laid across the beam afterwards drags what it lands on by
  up to `0.30` in value where a mass crosses it and `0.40` where a stroke does.
- **What `cover()` does to the place it is handed is said where a painter will meet
  it** — the card's `undo` row and `PAINTER.md`'s *What you are bad at*. Finding 8
  reported that the tool had `edge="hard"` and the card did not mention it. For one step
  the documentation carried the keyword; since F1 moved the default (*Defaults moved*,
  above) the row says a burial lands inside the place, and is shorter.
- **Two rules that contradicted each other, reconciled.** `PAINTING.md` said *do not lay
  one broken pass across the whole canvas*; the graded field lays two, edge to edge, at
  `load=0.40` and `0.35`, and calls them required. The rule gives, because it is scoped
  to what it was earned on — a broken pass laid *under* work that has to sit on it — and
  the crossers are laid last, at part opacity, on a passage nothing else will cover.

**And vision is stated as a requirement** (G9), in `README.md`, `llms.txt` and the
package docstring. All three described it — *built for an agent that can see what it
just did* — which is a design note, not a requirement. The blind painter of the cohort
installed it, painted, and wrote *I can't see it … so I'm trusting the tool*. Every pass
of the method ends by looking, so a painter without image input can drive the whole API
without ever learning whether a mark landed. The other four small facts G9 listed were
already in place, closed by the steps that had reason to touch them.

### Recipes that show how they go wrong, and a check that they still do

Step 9 of the 0.5.0 cohort's round (`PLAN-0.6.0.md`, G3). Finding 19 asked for *small
runnable visual comparisons: the recommended call, what it looks like, the common
failure, the smallest fix* — because *the documentation sometimes compensates for
difficult tool behaviour with additional rules*, and a failure described in words is one
more rule to carry.

- **`easel demo <recipe>`** — `demo` through the MCP server, `easel.demo.answer()` from
  Python — paints one recipe of `RECIPES.md` beside its commonest failure and, where it
  is not the recipe itself, the smallest fix, and quotes what the tool said about each
  panel. Name the recipe by the words of its heading (`easel demo crosses a boundary`);
  with none, it lists which recipes have one. It needs no session. The sheet is cut to
  where the panels differ and enlarged up to four times, because five discs of a 5 px
  brush on a whole canvas are five dots nobody can compare.
- **Twelve of the twenty recipes carry a demo block** under their *Goes wrong as*, each
  cut by comment lines into the passage it is laid on, what goes wrong, and the fix. The
  block names what the tool says about the failure: a notice code for eight
  (`chisel-staircase`, `inward-flat`, `glaze-far`, `scumble-wedge`, `round-fringe`,
  `jitter-beads`, `smudge-long`, `smudge-across`), a line of `report()` for three, and
  *nothing says so* for one — flecks where a plane was laid without `solid=True`, which
  only looking finds. `RECIPES.md` now opens by saying a block under *Goes wrong as* is
  the failure on purpose, and not to copy it.
- **The other half of the invariant step 9 began.** `scripts/check_guide_blocks.py`
  holds every demo to what it names: the failure trips exactly those codes and
  `report()` lines, and the recipe and the fix, laid on the same passage, trip none of
  it and say nothing at the call. A recipe can no longer ship producing the fault its
  own paragraph warns about, and a failure block can no longer quietly stop failing. The
  script runs in CI now, as a job of its own, where until this release it ran only when
  somebody remembered to; it takes about two and a quarter minutes here against one and
  a quarter without the demos.
- **What its first run found, and what was done about it.** What `report()` says about a
  recipe that its failure does not name is printed as a note rather than failed on,
  because the answer is sometimes the rule's to change rather than the recipe's. The
  first run printed three notes, on two recipes, and one of each kind came of them.
  - ***A mass built of planes* was the recipe's to change.** As step 6 left it, its
    faces were a `bristle` at `0.014`–`0.02`, and it painted the *woven surface* its own
    paragraph names as a failure, under *59 marks with a bristle under size=0.025* and
    *46 of 64 long marks ... a stack of bars*. Its faces are now a `flat`, laid
    `edge="clean"`, each run along a side of its own, and nothing is said. The advice
    that led there changed with it: **`chisel-staircase` offers a comb only at
    `size=0.025` and over**, and under that `edge="clean"` beside `direction=`.
  - ***A graded field* was the rule's.** In its own colours it paints a smooth field,
    and the stack-of-bars rule said *17 of 17 long marks* over it, because each of a
    `scumble`'s passes counted as a bar. **A `scumble` now counts once** in that rule
    and in the crossings that re-arm it: its passes are one band sized to overlap, and
    whether they show as bars is `scumble-bars`' question at the call. Over the corpus
    that takes 10 of the 46 bars lines painters were shown, each on a pass laid mostly
    with a scumble, and the probe's own replay has the rule on 38 of the 325 painted
    passes, 12%, where it was 47, 14%. It costs the one true positive of the 0.5.0 cohort's round:
    BigPickle's whole-painting line reached its share only by counting the sky passes
    its own painter called fine, and without them its block-ins and crossers fall under
    it.
  - The graded field's demo now lays the field in its own colours, and the planes'
    demo on a ground, so each recipe panel shows the recipe working rather than the
    stand-in palette's strata or the first marks of an empty canvas.
- **One stale line fixed on the way**: the graded field's *Goes wrong as* still blamed
  horizontal strata on *the `load_falloff` clause*, which a banded `scumble` has laid by
  default since step 8. It now names what the recipe's own bullet says makes them — the
  passes run exactly along the frame.
- **Smaller things.** The names every guide block assumes (`s`, `mass`, the palette)
  moved from the check script into `easel.demo.preamble()`, so the demo and the check
  lay the same context under a block. `mcpb/manifest.json` counts seventeen CLI verbs,
  and a test now holds that sentence to the parser, which nothing did while it said
  twelve.

### The closing audit, read as a painting rather than a pass

Finding 12 of the 0.5.0 cohort's round, ruled on 2026-09-22 (`PLAN-0.6.0.md`, the
decisions table). `checklist()` is `report(since=None)`: every rule of the post-pass
check, read over the whole painting. Two of those rules were written for a pass, and
over a whole painting they added it up — *265 marks with a bristle under size=0.025*,
*one disc printed 176 times* — and the painter argued with the first and never answered
the second. Counted over the 21 finished paintings before anything moved
(`scripts/probe_cohort_session.py --closing`; `CALIBRATION.md`, *The closing audit, over
a whole painting*):

- **The small-comb rule says nothing over a whole painting.** What it asks for is a brush
  for the marks about to be laid, and a finished painting has none. Where its count was
  large the pass that laid the marks had said so — 38 of `opus`'s 40, 39 of
  `laundromat`'s 48 — and where no pass had, the marks are mostly strands a comb suits.
  It was on 9 of the 21 checklists and is on none; a pass's own report still says it.
- **The disc rule counts only the discs a painting shows together** — three or more,
  each within `0.06` of another — and says where each group is: *164 small marks with a
  round tip at tip_wobble=0 sit together in 3 places -- 80 around (0.67, 0.61), ...* A
  signature is left out, by the test the budget already waives it with
  (`History.is_signature`, public now). The line was on 14 of the 21 checklists and is
  on 10. The four it left were accents added up across passes — one painting's *one
  disc printed 8 times* was a lamp, a moon, two notches, two edge highlights and a
  glint, from six passes — and every repeated passage stayed, Gemini's rows of glitter
  lozenges among them.
- **A pass's own report is unchanged**, both rules and every word, so the noise budget
  does not move. `report()` with no `since`, `easel run --check`, `easel log --check`,
  `easel check` and the MCP `check` tool all read the painting the way `checklist()`
  does.

### Seven more recipes that show how they go wrong, and a light that comes toward you in pieces

Step 9 of the 0.5.0 cohort's round again (`PLAN-0.6.0.md`, G3 and G6): nineteen of the
twenty-one recipes now carry a demo block, and the one passage four cohort painters
failed alike has a recipe.

- **Seven more demo blocks**, each held by the block check to exactly what it names:
  - *a quiet gradient* — `scumble-bars` and *comes back as bars*, a brush under one
    step. The recipe had no *Goes wrong as* at all, and has one.
  - *a small irregular bright mark* — *one disc printed*, five dabs of one tip.
  - *a tapered arc*, *a picture with an empty half* and *a hollow thing*, all three
    *nothing says so*. They are a disc bitten out with paint, a second thing put in the
    empty half, and a catch-light carried all the way round an opening.
  - *a repair under things that are standing on it* — *earlier details out of sight*,
    the mass repainted and nothing put back on it.
  - the new recipe's, below.
- **A demo's body is opened as a pass**, the way `easel run` opens one. The rule that
  names a burial needs the canvas as the pass began, and until now it could not speak
  in a demo at all.
- **Two recipes changed their own block, so that their demo shows them working.**
  - *A hollow thing*'s catch-light lay on an arc that no hollow in front of it had for
    its near edge. It now lies on the near rim of an opening seen from above, which is
    where the paragraph beside it puts it.
  - *A repair under things that are standing on it* painted its details at
    `size=0.02`, one width over what the burial rule watches. It now paints three
    things standing on the near mass, at `0.012`.
- **Two recipes stay in words, on purpose.**
  - *A form that turns*, laid as a pass on its own, runs both its masses along the
    form's side: 21 long marks at one angle, so the recipe itself gets the stack-of-bars
    line. And the failure it names, no join stroke, is a half-strength stroke a demo's
    scale does not show.
  - *A scene with straight edges*: its block is a drawing, and a panel shows paint.
- **A new recipe, collected rather than composed: *a light broken down a surface toward
  the viewer*.** Four of the cohort's seven painters failed this passage first, and
  alike: floating rectangles, small bricks, a ziggurat, spoon-shaped islands. It had no
  recipe. The versions they kept, taken together, come to four things:
  - a film first, mixed from what it lands on;
  - every piece a different length, bent, its tip drawn afresh;
  - the rows further apart, wider and fainter as the light comes toward you, while the
    pieces keep their lengths;
  - the surface's own dark laid back across the lights.

  Its demo is the ladder one painter committed as its fix: eight marks of one length,
  which `report()` names a loop's signature.

### The way in: six failures painted, the reasons delivered, and two ceilings that bind

Step 9 of the 0.5.0 cohort's round (`PLAN-0.6.0.md`, G2, G8 and G10). Four painters
counted what they read before their first mark — ~2,600 lines, ~2,500 lines, *2000+
lines of docstrings* — and every one of them asked for a quick start. This is the
answer, and it is a hypothesis until a fresh session paints against it.

**`easel demo mistakes`** paints six failures on one sheet: a staircase down a sloped
side, a stack of bands, a film that owns the picture, a thumbprint dragged out of a
mass, a ladder of one length, one disc printed over and over. Each is a recipe's own
*Goes wrong as*, so the sheet stays true by the same invariant the demos do, and each
is something the tool says at the call or after the pass. `demo` over MCP takes the
word too.

**The path is the card, that sheet, the nine exercises, and paint.** What left it is
*read `PAINTING.md` once*, which was about 2,500 words before the first mark.
`PAINTING.md` is **the reasons, delivered rather than read**: every notice carries the
passage its reason lives in, and `easel explain <code>` prints that passage at the
call. Its own first page, the file table, the README and `llms.txt` say so.

**The numbers that were the guide's are the painter's.** The three values, the place
meant to be lightest, the subject's share of the budget and whether this picture's
ground is meant to be buried go in `s.plan(...)`, and the card asks for them there
rather than stating them as universal. What is left as a number says which kind it is:
**measured**, with the `CALIBRATION.md` heading behind it, or a **habit**, as *most
painters so far*. Where a check now says a thing, the rule names it — boxes are the
`boxes:` line, the edges step is the `edges:` line, under-varied objects are *one disc
printed* and *a loop's signature*.

**Two word ceilings, and both bind.** `PAINTER.md`'s was 10,000 against a file of
6,654, which is not a ceiling; it is 6,700 now. The card — *The first hour*, the page
every painter reads and the one the cohort measured as too long — had none at all, and
has 1,400 against 1,369. `tests/test_guide.py` holds both, and
`scripts/check_guide_blocks.py` prints them. The round's plan wanted about 5,000 words
for the file: that is not this, and getting there means cutting the workflow, the
exercises or *What you are bad at*, each of which a session has defended.

- **The README's own count of the server is held to the server now.** It said *fifteen
  tools: the twelve CLI verbs* while there were twenty and seventeen. The manifest's
  copy of that sentence has been held to the parser since step 9's part three; this is
  the other place a client reads it.

### The record

Step 9 of the round, G11: what the project says about itself, brought level with what
it now does.

- **`LESSONS.md` restates the boundary rather than moving it.** This release put more
  of the guide into the tool than every release before it together, and the check still
  reads marks and measures the canvas — every line of it is a number about a mark or a
  pixel. The two cohort findings outside that line stay outside it: a recipe followed
  exactly and expressively wrong, and a safe centred composition. The instrument for
  both is the painter's own `why` and a human looking.
- **A cohort of painters that are not this model is in the protocol now**, with the two
  things worth keeping from this one: tell them nothing about what to read, because
  then what they read is the measurement, and weight a painter that cannot see images
  accordingly — the one here painted a whole picture and wrote *I can't see it ... so
  I'm trusting the tool*.
- **The depth-order item is narrowed, not closed.** `report()` names a burial done in
  one pass, which is the part a check can see — 2 of the corpus's 325 passes, both
  burials — and cannot see one spread over several, which is what the one painter who
  wrote the fault down actually did. The three copy runs whose numbers define the item
  are not in this repository, so the check has never been run on them.
- **What the tool says at the call has a row in the README**, where the check and the
  closing checklist already had one, and `llms.txt` says the same in a sentence: the
  notices carry codes and measurements, `report()` reads the log and measures the
  canvas after every pass, and `checklist()` answers the closing lines at the end.


## [0.5.0] — 2026-09-16

**Two rounds, and both painted from the installed package alone** — the first two
sessions on this page that never had a checkout to read. The first was cut as this entry
before the second arrived, and the tag was never pushed, so the second went in here
rather than into a version of its own.

**The pier.** A session was told to `pip install easel-paint` and paint from whatever the
wheel carried, in an empty directory. It painted the underside of a pier at low tide, 257
of 300 strokes, and came back with five engine items, five documentation items and one
that is neither — the one that is neither being the only one that changed what the method
*asks*. **It is not blind and `SUGGESTIONS.md` says so**: it had spent that morning inside
this repository doing packaging work, so it arrived already knowing several of the guide's
numbers without the method that holds them together. Its engine findings stand, because
they are about marks it laid and warnings it was shown; its reading of the guide is
discounted, and that discount is why one documentation item was answered by compressing
rather than by cutting.

**The hands, and this one is blind.** A session was told to make sure of `easel-paint`
**0.4.0**, not a local editable install, and to treat that wheel as the only thing
available. It painted a pair of hands sorting dried beans, 329 of 420 strokes, and did
not open this repository until the picture was exported and reviewed. Two engine items
and four documentation items, plus one found while filing them. **Five of the frictions
it hit are things the pier round had already fixed in this release**, which it never saw,
so they are an independent painter confirming that round aimed right rather than items of
their own. And where the two agree — the stack-of-bars warning going unread, the front
page being long, the reason for the subject going missing — that is the same fault found
twice, once by a painter who knew the numbers and once by a painter who did not.

**Two items closed by measuring and finding nothing to fix** — the eighth and ninth
times this project has done that, and the ninth is the first to close by declining to
build anything at all.

### Added

- **The closing checklist asks whether the reason you chose the subject is still in the
  picture**, and the card asks you to write that reason down before the first mark. This
  is the round's one real finding and it came from a painting that passed every other
  line on the way to losing what it was for: the pier was chosen because under a pier
  the light arrives from *below*, bounced off the water, so every form is lit backwards.
  What got painted was a competent dark structure lit from the ordinary direction. The
  value structure is sound, the masses are shapes, the edges vary, the ground shows at
  `0.58%`. Nothing failed, and nothing asked. The checklist's preamble now says *every
  line but the last three*, so the question is read at the speed of the two it joins.

- **`sample()` over a rectangle that holds two masses says so, and names both.** A span
  crossing a hand returned `0.342` where the table under it reads `0.258`, and the edge
  painted with that number landed as a pale halo above the hand instead of sharpening
  it. The documentation already says *to measure a mass, hand it the mass*; the painter
  had read it, and the failure is silent, arrives as a number, and goes straight into
  paint. The warning prints what is actually there — *84% of it reads about 0.276 and
  16% about 0.529, so the 0.341 this returns is a measurement of neither* — split at
  Otsu's threshold over the place's own pixels, and repeats the remedy.
  **A shape is never asked the question**, which is the half the request did not
  anticipate: a mass handed in whole is spread by its own turn from lit to shadow, and
  the two hands that raised this measure `0.093` and `0.100` against a threshold of
  `0.06`. The rule would have fired loudest on the call the sentence tells painters to
  make. Measured over every cell and every 2×2 span of two finished paintings rebuilt
  from their own passes — 226 rectangles: of the 35 whose mean misses the value of their
  own dominant mass by more than `0.03`, it catches **all 35**, it fires on **23%** of
  the rest, and on none of the seven masses handed in whole. `compare()` is untouched:
  it samples per cell and would be noisy by the same measure on any picture with an edge
  in it.
- **`look(marks=)` and `look(impasto=)` are on the page.** Both shipped in 0.4.0 and were
  named in none of the five documents; `REFERENCE.md`'s signature line listed eight of
  the ten parameters and stopped. A painter placed six landmarks, judged the picture
  through fifty-two looks with their labels drawn over it — one of them on the focal
  point for the whole session — and never found the way to turn them off, having found
  `unguide()` for the scaffolding because that one *is* named.
- **The band count is asked at both scales, and the drawing step asks what the view is.**
  *Count the horizontal bands* is a question about the arrangement, and the picture that
  raised this passed it easily while sinking on four near-parallel fingers **inside one
  mass**. It now also asks for the count inside the biggest mass and in any row of like
  things. Beside it, the question nothing in the method asked: **what is this thing's
  foreshortening?** Draw the view, not the object. That painter redrew its arrangement
  three times, all three free, and all three were framing, limb angle and the size of a
  bowl.
- **A stopping rule for repainting: if a passage has failed twice, the fault is upstream
  of the brush.** Go back to the drawing — it is still free, and it is the only thing
  that is. About eighty strokes of one painting went on four successive treatments of one
  failing passage, each a brush-level answer to a drawing-level fault, and each making
  the next repaint dearer because more was standing on it. It is a number rather than a
  preference because a preference will not survive the moment it is needed.

### Changed

- **The stack-of-bars warning is said once**, and again only when the picture has picked
  up a long mark 30 degrees or more off the bars it was said about. It is the one check
  rule that can be right and useless: its own text concedes *unless the subject runs that
  way*, it cannot tell whether the subject does, and on a subject that does — joists, a
  waterline, a reflection — it fired on five passes running until the painter stopped
  reading it, which means it was also unread on the pass where it was right. Replaying
  the pier's fifteen passes: **7 firings become 3**, and the three are the first stack,
  the pilings crossing it, and the stack rebuilt afterwards. Every threshold from 20 to
  60 degrees gives those same three on that painting, so 30 is the middle of a plateau
  rather than a knee. `easel run --check` and `log --check` are exempt: what makes a
  warning skimmable is being printed at you after every pass, and an audit was asked
  for. The state rides in the `.easel` file, because a painting worked from the shell is
  loaded and saved once per pass and a rule that decays has to decay across that.
- **A stack of near-horizontal marks is now called horizontal.** Marks along the
  horizontal come back from the log as a mixture of `179` and `1` degrees; the clustering
  read those correctly as two degrees apart and then took a plain median of them, which
  is `90`. So the commonest stack of bars there is was reported as *vertical*, and the
  painter was pointed at right angles to the fault. The same number steers the
  graded-passage rule's normal, where it measured the spread of a horizontal band *along*
  the band rather than across it. Both take a circular mean of the doubled angles now.
  Found by trying to measure the item above against the painting that raised it and
  getting an answer that could not be true.
- **`s.erase()` takes both drawings** — the graphite in the canvas and the `guide()`
  overlay on the view — and takes them the same way: the whole of each with no region,
  and inside a region it cuts an overlay path exactly where it cuts a graphite line. A
  painter redrawing an arrangement reaches for `erase()`, and a scaffolding fan left
  behind puts two convergence points in one look, which is the thing the drawing exists
  to judge. `unguide()` is unchanged and is still how to take back one labelled part.
- **Looks are numbered from the directory, not from the session.** `look_001.png`,
  `preview_001.png`, `compare_001.png` and `rehearse_001.png` each take the next free
  name in `out_dir`. Two sessions sharing a directory no longer write over each other —
  one painter ran four of the nine exercises from one script and got `look_001.png`
  written four times, losing all four images in the one part of the method that is only
  looking. Rehearsals have been numbered this way since 0.4.0 for the same reason. The
  per-session counter is gone, including from `save()`/`load()`, where it was carried
  across so that a reopened painting would not renumber from 1; that workaround is now
  the default. `.easel` files still carry a `look_counter` key so that a 0.4.0 build can
  read them.
- **`easel.guide` is `easel.docs`.** The module that reads the documents and
  `Session.guide()`, which lays scaffolding on the view, were two unrelated things under
  one name, both reached from one session. `from easel import guide` still works and is
  not going away; everything that teaches it says `docs`, and `dir(easel)` lists both.
- **`PAINTER.md` is about 6,000 words, from 6,672.** The seven workflow steps restated
  the nine-hundred-word card at nearly three times the length; they are 1,540 words now
  and open by saying what they are for. Cut: the second telling of back-to-front, of
  what a place is, of hard edges pulling the eye, of the greyscale argument, and every
  code block that showed what the card had already shown. Kept, because they are the
  mechanisms the card has no room for: `compare()` on a value plan, `at_value` reaching
  a value from either side, and the three rules about `smudge`.
- **The nine exercises are no longer called a gate.** Nothing gated them, and a rule
  nothing enforces is a preference — this project's own rule, applied to itself. What is
  left is the cost, stated plainly. Every mechanism considered could only record what it
  was told, which is a preference with a `True` in it.
- **Cross-references on the front page: 25 to 16**, and 12 to 4 across the seven workflow
  steps. At the old density they stopped reading as navigation and a painter skimmed past
  all of them, including the two it needed. Each one that survives is at the moment of a
  situation. The card's closing line now names the situation rather than the file: before
  you lay a passage you have not laid before, open `RECIPES.md` and find it.

- **A pass that raises under `--rehearse` says nothing was committed.** It printed
  `easel: script raised, session saved with 180 strokes` — and the count was the
  *painting's*, because a scratch copy continues the real numbers, so it read exactly
  like a commit. Nothing was committed: the rehearsing branch returns above the save. It
  now says *nothing committed, the copy had laid N of this pass's marks*, with `N` the
  copy's own log. The painter stopped and verified the stroke count by hand before
  trusting it, twice. Read off the session rather than passed in at the call site, so the
  MCP server's `run(rehearse=True)` is fixed by the same change and a caller cannot get
  it wrong; `exit()` on a copy says it too.
- **Every parameter a painter can type is named in `REFERENCE.md`, and a test says so.**
  The `look` line is the second of its kind and the first fix, a sentence, did not
  generalise: the signature lines are hand-maintained and that one had been wrong since
  the parameter shipped. `tests/test_reference.py` now reads each signature off the code
  — two checks, because the page names a parameter two ways and each misses what the
  other catches. Closing what it found: `stroke(clip=)`, `sweep(closed=)`,
  `cover(dry_first=)`, `sketch(areas=)`, `mix(ratio=)`, `mix_many(weights=)` and
  `complement_grey(ratio=)` were named nowhere on the page, and eight more calls were
  written out with parameters left off the end.
- **`PAINTING.md` no longer says looks are numbered per session.** They come from the
  directory as of *Looks are numbered from the directory* above, and the paragraph
  telling painters why a second painting overwrites the first's record of itself had
  outlived the behaviour it described. Reported by the round that read the page against a
  0.4.0 wheel, where that paragraph was still true.
- **`README.md` and `PAINTINGS.md` no longer claim every painting re-runs byte for
  byte.** Seven of the fourteen say **Reproducible: not claimed** in their own tables,
  and both pages made the blanket claim anyway — one of them in the section that sends a
  first-time painter to `paintings/`. The claim that holds everywhere is a different one
  and is now stated as itself: the *log* replays byte for byte, because a stroke's
  randomness is drawn from `(seed, stroke index)`, and golden-image tests hold it.
  Whether the committed scripts rebuild the canvas is per painting, and each painting's
  table says which of the two it claims. Found while filing the round, not by the
  painter — who had spotted it on two paintings. `SUGGESTIONS.md`'s own preamble was
  counting one session short in the same place: the winter greenhouse has a row in its
  table and was never in the sentence, so thirteen sessions and fourteen paintings, and
  the three pages that repeat those numbers agree with it now.

### Tooling

- **Nothing in this file may claim to have shipped until the tag exists**, and
  `tests/test_version.py` holds it to that. The rule is in the header above with what it
  cost: this section announced 0.5.0 as released on the day 0.5.0 was *cut*, the tag push
  never happened, and the round filed after it was nearly cut as 0.6.0 over a version
  number that was still free. Two checks, one per half — every version this file says was
  released has to have a `v` tag, and at most one version section may be untagged, since
  that one is the version being prepared and a second means a release was skipped. Both
  need tags to answer, so the two CI jobs that run the whole suite now check out with
  `fetch-tags`; a tagless clone skips rather than guessing.

### Measured, and nothing to fix

- **The post-pass check cannot see a composition**, and says `nothing to report` to a
  dead one. One painting's largest mistake was its first arrangement — it made the
  distant opening the hero and left the subject an empty band across the top of the
  frame — and every pass the check approved was locally clean. This is written down in
  `report()`'s docstring as a boundary rather than fixed as a fault: a mark is what the
  log holds, composition is carried by the drawing, which is free, and judged by looking
  at it. It is also the argument for putting *why did you choose this subject* on the
  checklist, where a painter answers it, rather than in `report()`, where nothing can.
  The first item on this page to close by declining to build.
- **`unguide()` was not missing.** It has existed since 0.4.0. The painter who asked for
  it never found it and reached for `s.marks.clear()`, which clears landmarks and not
  guides, so what was missing was the sentence naming it — now in `guide()`'s own
  docstring, in step 1 beside the call, and in the units table.

And two the **hands** session arrived with, neither of which survived being measured.
Recorded because a retraction is as much a finding as an item, and both are in
`SUGGESTIONS.md` with their numbers.

- ***A form that turns* does work at feature scale.** Laid at four widths on a
  1024×768 canvas it keeps its transition at 25–40% of the form's own width throughout.
  The recipe was never applied: the fingers were laid as strokes from the first pass.
  **The mapping is the step that failed** — the painter did not think of a finger as a
  form that turns, it thought of it as a finger.
- **`edge="clean"` does not draw a contour that reads as an outline.** Measured on that
  painting's own bowl, rim minus interior is `−0.010` for `clean`, `+0.007` for `ragged`
  and `+0.013` for `hard`: the contour is if anything the *darkest* of the three. What
  the painter saw was a cool mass at too high a value on a warm ground.

### The workshop

A non-editable `easel-paint` install in `site-packages` shadows the checkout, so
`pytest` run in this repository silently tests the published wheel rather than the
working tree. CI is unaffected — it does `pip install -e ".[dev]"` — and that is the
local fix too. Recorded because it is the install session's stale-editable-install
finding wearing the other hat, and because it has now cost time twice.

## [0.4.0] — 2026-09-15

**Released.** Shipped as `v0.4.0`: `easel-paint` 0.4.0 on PyPI, the GitHub release with
`easel.mcpb` attached, and `io.github.Gemberkoekje/easel` 0.4.0 in the MCP registry. The
`bundle` job failed on the first run and was re-run — *The release*, at the foot of this
section, has what happened and why it is worth knowing.

Three rounds. Two of them were filed as one because they raised the same two items from
opposite
directions: the tenth session's **fogged glass** — a greenhouse wall in late winter
seen from outside, 311 of 320 strokes — and the **winter greenhouse** painted before it
and filed after it, an interior at a low sun, 297 of 300. Both painters refused a
frontal elevation on the closing checklist's layer-cake warning and answered it with a
metric perspective projection written before any line was drawn; both then found that
the angle they had computed off the picture was not the angle `direction=` takes.

Fifteen engine items between them and three documentation items left over from the
round that rewrote the five files, every one acted on. `SUGGESTIONS.md` carries no open
section for the first time since the eighth session's round was filed.

**The third round never painted.** An install session was asked to `pip install
easel-paint` and paint from it, and spent its first ten minutes in `site-packages`
instead — one engine item and two documentation items, and the finding that what it came
to report was not a bug but a stale editable install serving 0.1.0 metadata over 0.4.0
code. `SUGGESTIONS.md` carries it closed like the rest.

Two of the items closed by **measuring and finding nothing to fix**, which is this
project's habit and the sixth and seventh time it has happened: `cost_line` does agree
with the picture about `direction=` (the disagreement was a unit nobody had written
down), and a smudge's strip on a long boundary is the calibrated reach and nothing
more (the asymmetric pull the session guessed at is not doing anything extra).

### Added

- **`easel.guide` is bound on the package** and named in `__all__`, so `dir(easel)`
  lists it beside `brush`, `canvas` and `palette`. `from easel import guide` already
  worked; what did not was a bare `import easel` followed by `easel.guide`, which is the
  path taken by an agent that opens a REPL and asks what is in here. Discoverability is
  that module's whole job, and it was the one submodule the listing left out — see
  `SUGGESTIONS.md`, *The install session*.

- **`block_in(shape, ..., edge="hard")`** — a mass masked to its own outline. Every dab
  is multiplied by the shape's coverage, so a pass ends **where the outline is** rather
  than where its chisel falls: no inset, no contour pass, and no paint outside the
  shape. The chisel staircase and the half-brush spill are one defect and it was the
  most common way a mass went wrong in the winter greenhouse — four times, with three
  workarounds used and none of them in the recipes, one of them lowering a polygon
  `0.12` m in world space so the overhang stayed hidden under a bench. Measured with
  the staircase table's own Sobel instrument on that painting's lit face: a `flat` at
  `size=0.020` puts **13%** of its strong edges within ten degrees of horizontal
  ragged and **4%** hard, a `knife` **16%** and **4%**, on a mass with no horizontal
  feature of its own. Furthest paint past the outline: **9.3px** ragged, **2.6px**
  clean, **under one pixel on every side** hard. Ragged stays the default, because a
  mass *behind* other things wants the brush to break past its boundary.
  `overhang` defaults to a full brush here, since nothing can land outside the outline
  and the only thing it still does is carry each pass end up to it. `cover()` takes it
  too, which is the in-bounds burial the fogged-glass round asked for.
- **`stroke(..., clip=place)`** — the same thing by hand, and what `edge="hard"` is made
  of. It changes where the paint lands and nothing else: a clipped stroke and its
  unclipped twin lay the same dabs from the same draws. The clip rides in the log, so a
  clipped painting replays and reloads as it was painted.
- **`direction=((x0, y0), (x1, y1))`** — a line to run along, instead of an angle.
  `direction=` is measured in the **normalised** coordinates, which on a canvas that is
  not square is not the angle on screen: measured, `direction=-23` lays its passes at
  **−12°** on 1000×500, and `45` runs at **37°** on 1024×768. Every instrument agrees
  with every other — `cost_line`'s *stepping across N* is the same space, to the
  hundredth — and all of them disagree with the picture, which is where the painter is
  looking. Three painters wrote a projection, read a screen slope off it and typed that
  in; one laid *passes along the sloped boundary*, the remedy for a gable at 41°, at
  33°. A pair of points is a line; a pair of numbers is still two angles, so
  `direction=(28, 118)` is unchanged.
- **`s.scratch(count_only=True)`, `easel run --count` and `run(count=True)` through the
  MCP server** — a rehearsal with the pixel work skipped. `cost()` prices one
  `block_in` or one `sweep`; a painter's own helper
  that calls a dozen verbs had no price short of painting it on a copy, and the copy
  renders every dab. One budgeted thirteen pots at about 100 strokes, rehearsed at
  **220 against 142 left** at three minutes a go, and rebuilt the recipe from strokes at
  108. The count is exact rather than an estimate — pass geometry is settled before
  anything is stamped — and `tests/test_paintings.py` holds that against the winter
  greenhouse's own scripts, pass by pass: same stroke count, same paths, same dabs.
  Timed on the pot recipe, which is where the saving is: **1.6s rendered against 0.06s
  counted**, a factor of about thirty, and most of it turned out to be the undo snapshot
  rather than the dabs — three canvas-sized arrays per stroke, which a copy that lays no
  paint has nothing to undo to. The one thing
  it cannot answer is a film given `to_value=`, whose search is measured off paint a
  counted run has not laid; that is skipped and said out loud, once.
- **`s.guide(points, note="")` and `s.unguide()`** — a drawing paint cannot bury.
  `mark()` survives the whole painting because it is a point held beside the canvas and
  drawn onto every look; a graphite line does not, because it is *in* the canvas. So
  the method's own order costs a second drawing pass: in the winter greenhouse the
  bench tops buried the first drawing and the pass before the pots redrew every pot and
  the can. Nine of eleven paintings never made that second pass, and the two passages
  one painter never drew were the two it named weakest. This is `mark()` along a path:
  `look()` draws it, `look(sketch=False)` leaves it out, `export()` never sees it, and
  it is not charged. Use `pencil()` for the underdrawing that should show through thin
  paint; this is the scaffolding that should not be in the picture at all.
- **A ground-showing percentage in `report()`**, and `Canvas.ground_showing(tolerance)`
  behind it — a diff against a bare canvas at the session's own ground, texture and
  seed. The closing checklist asks *is there anywhere the ground still shows through?
  There should be*, and there was no way to answer it short of building that canvas and
  diffing it, which one painter did **after** the painting was finished, having already
  spent the warm ground the whole picture was planned around: **0.07%** of it was
  within `10/255` of bare. Per channel rather than by value, so a cool film at the
  ground's own lightness counts as covering it; graphite is not paint and does not
  count. Under `0.5%` the line says so, which is the one judgement in the check.
- **`inset(..., frame=False)`** on a region and a shape, for the erosion that used to be
  the only behaviour. See *Changed*.
- **`Polygon.coverage(width, height, samples=2)`** — fractional coverage per pixel,
  which is what a hard clip is multiplied by. `mask()` asks whether a pixel's *centre*
  is inside, which is the right question for an area and the wrong one for painting
  through.

### Changed

- **`inset()` no longer erodes a boundary that lies on the canvas frame.**
  `edge="clean"` has dropped its inset there since 0.2.0, on the stated principle that
  *a mass that meets the frame should run off it*; plain `inset()` did not, and the
  asymmetry was invisible from the call. A painter's `GLASS.inset(0.024)` pulled a glass
  wall in from `x = 1.0`, the ground showed down the right edge of the finished
  painting, and the defect survived to the final inspection pass and cost a repair.
  Per coordinate, not per point: a point on the bottom frame keeps its `y` and takes the
  inset `x`. `frame=False` is the old behaviour, and growing (a negative amount) is
  untouched. **A script that insets a mass drawn past the frame now paints a little
  more canvas than it did in 0.3.0**; nothing saved to an `.easel` file moves, because
  the log holds the path that was painted.
- **The post-pass check's *detail before the masses are down* rule no longer fires on
  every rehearsal.** It claims to police the painting's first sixty marks and fired at
  135, 162, 190, 243, 260 and 273 strokes spent. A rehearsal copy starts with an empty
  log, so the rule's *earlier* term computed as nought however far along the painting
  was — and since the guide has every painter rehearse first and look, the false
  positive was the answer they always got, while the correct silence only ever arrived
  after the decision it was meant to inform. The audit the item asked for found a
  second rule reading across passes the same way: **the subject's share**, which
  reported a rehearsed pass's own marks as the whole painting. Both now read the
  painting behind the copy.
- **The graded-passage rule is narrowed to a passage.** It fired three times in one
  painting on rows of separate things and once on two `scumble` ramps summed into one
  stack with a remedy three times either band's own step. Four narrowings, each cheap:
  marks that lay no colour of their own are dropped (a `smudge` at `size=0.02` had made
  itself the narrowest brush in a five-mark "passage" it contributed no colour to); the
  marks must form **one run** with no gap wider than four brushes between neighbours
  (ten pots of three strokes each step three quarters of a brush *inside* a pot, and
  only the gaps between pots are wide); the colours must step **one way**, turning at
  most once (a band that brightens and falls back is a passage; ten pots at three
  terracotta values turn nine times); and a passage is now **five** marks rather than
  three, three being also the number of strokes a small container's body takes. The
  ninth session's dawn band still trips it.
- **`report()` gained a seventh rule**: three or more small round-tip marks at
  `tip_wobble=0`, each short enough to be the tip's silhouette rather than a line.
  Both of a round tip's defaults are the bad one — the disc is the default and the fix
  is opt-in — so *several small marks with `round_hard` or `liner`* is the failure
  nobody has to ask for. The closing checklist's *is any small mark a disc, a capsule
  or a rectangle* is this rule's own question, and now points at it.
- **`block_in` warns on a round tip blocking in a small shape.** A `hull` `0.046`
  across at its narrowest with a `round_hard` at `size=0.013` — a leaf pressed on glass
  — printed the shape's own scalloped boundary and came back, in the painter's word, a
  cauliflower. A disc's overhang goes out all the way round, so at that share the mass
  lands **1.61x** the area of the shape and the fringe is the silhouette; a chisel at
  the same share lands **1.34x**. It fires at the same quarter of the shorter extent
  that `edge="clean"` already uses, so it adds no new threshold there, and only on a
  *feature* — a shape under a tenth of the canvas across, which is where the fringe
  lands on a drawing rather than on a soft silhouette a round tip is the right choice
  for. Only on a ragged edge, too: `"clean"` has its own line about the same combination and `"hard"` masks the
  fringe away, which is one of the remedies this names.
- **`jitter=` past five times its default says so.** `jitter=0.5` was accepted in
  silence and beaded every member of a greenhouse frame — twenty-five times the default
  of `0.02`, from a call that otherwise looked exactly like the recipe. It is the
  wander of each dab in tip diameters, so it comes out as width: measured, a stroke
  lands **1.2 brushes** across at the default, **1.8** at `0.1` and **3.7** at `0.5`,
  which is a chain of beads rather than a line. It fires on the override, not on a
  brush's own field: every named brush in the box sits between `0` and `0.03`, and a
  `Brush` built by hand is the painter's own.
- **`compare({place: value})` says which close pairs actually touch.** It used to ask
  *do these two touch?* — three of one painting's four close pairs were masses that
  never met — and the two rounds that followed answered it wrong, the worse of them a
  pair planned `0.00` apart that met along its whole far edge. Every place is a
  rectangle or a shape, so it is one intersection test. Each pair is marked `(touch)`
  or `(apart)` and only the touching ones go under the line that matters.
  `Comparison.pairs` carries the fourth field; `near=` is how close counts, defaulting
  to `0.01` because a value plan carries no brushes to take half of.

### Tooling

- `scripts/probe_tenth_session.py` — every claim these two rounds were built on,
  re-measured on the engine as it now is and runnable. It prints the numbers this entry
  quotes, and the two it overturned print the *before* beside the *after*.

### Documentation

- **The package docstring names the route to the guide, not the filename** —
  `easel.guide.front_page()`, or `python -m easel guide` from a shell, in place of *read
  `PAINTER.md`*. A bare filename sends a reader whose import has just failed into the
  filesystem to look for it, which is where one session spent its first ten minutes.
  `python -m easel` rather than `easel` because the console script is not on `PATH` in
  every install.

- **`direction=` got the worked example the rest of the geometry gets** — one mass at
  three angles, the pass direction and the step direction both named, beside the new
  line form. The unit sentence was already in `REFERENCE.md`'s table from the
  documentation round.
- **The closing checklist's ground line says how to look**, which is the engine item
  above. Its *is any small mark a disc* line names the check that counts them.
- ***An edge that is actually lost*** **says that a smudge loses a *stretch*.** Its
  reach does not grow with the join — `1.3%` of canvas height at the default size over
  join lengths from `0.05` to `0.80`, flat, and the strip comes back at `0.51` between
  masses at `0.19` and `0.78`. So over a short join it reads as a softened corner and
  over `0.4` of the canvas as *dark, mid, light*: two edges where there was one. Past
  about a tenth of the canvas, go to the paint-across recipe from the start.
- **The staircase has a fourth repair**, and it is the cheap one: `edge="hard"`.
- **The fifth painter in a row asked for the prose to move into `report()`.** This round
  adds three checked rules and the answer to *which paragraphs have a rule a check
  could carry* is: those three. Each is now one line pointing at the check rather than
  a paragraph restating the numbers. `PAINTER.md` is 6,672 words against its 10,000
  budget, so nothing had to be cut to pay for them — the question the request really
  poses is what the prose is for, and this round's answer is that it is for the rules
  no check can hold, which is still most of them.

### The release

**The run half-failed, and the half that failed is the one that leaves no trace.**
`build`, `pypi` and `registry` succeeded; `bundle` did not. It unpacks `easel.mcpb` and
resolves `easel-paint[mcp]==<version>` from PyPI to prove the bundle installs — which it
can only do once the upload it is racing has propagated, and its budget for that is `for
delay in 0 15 30 60`: four attempts across 105 seconds. PyPI took longer than that on the
day. Nothing was wrong with the bundle. Re-running the one failed job, once the index had
caught up, passed on the first attempt and attached `easel.mcpb` to the release.

**What it leaves behind is the part to know.** `bundle` is the job that *creates* the
GitHub release — `gh release create` when the tag has none — so while it is failing there
is no release at all, only a bare tag, and `easel.mcpb` is downloadable from nowhere.
PyPI and the registry are already correct and unaffected, which is exactly what makes it
easy to miss. The job is built to be re-run (`create` only if absent, `--clobber` on the
upload) and re-running it is the whole remedy; the retry budget is the thing that would
stop it happening. This is the second release running in which `bundle` was the job that
failed.

One trap for whoever automates this next: **`gh run watch --exit-status` exited 0 on the
half-failed run.** The per-job conclusions are the thing to read, not the exit code.

## [0.3.0] — 2026-09-14

**Released**, and it carries three rounds of work. It was prepared twice and never
tagged — an earlier draft of this file split the same work across a 0.3.0 and a 0.4.0,
neither of which was released — so the eighth session's round, the ninth session's
round and the documentation restructure are all in here, under the version that
follows 0.2.0. **The 0.4.0 that earlier draft described was never released**, and nothing
below ever shipped under any number but this one — the 0.4.0 above is a different release
carrying different work, cut on 2026-09-15.

Shipped on 2026-09-14 as `v0.3.0`: `easel-paint` 0.3.0 on PyPI, the GitHub release with
`easel.mcpb` attached, and `io.github.Gemberkoekje/easel` 0.3.0 in the MCP registry. It
is also the first tag pushed since the release workflow's `bundle` and `registry` jobs
were fixed, and the first run in which either of them succeeded.

Each round kept its own account, in the order the work happened.

### The eighth session's round: a pool at night

The first round the register has carried as *open*. That session is the split test's
other arm — a painter given only the method, the recipes and the reference — and what
it failed at was **lookup rather than judgement**: three
questions the engine could already answer and would not say out loud. So two of its
three engine items are instruments rather than mechanisms, and the third is a price
the walk already knew and never quoted.

Every number it took reproduced, to the stroke. **One mechanism it offered did not**,
and it had marked that one as a guess — a sequence of directions is not a stack sized
for its steepest angle, it is one whole pass per angle, charged as the sum. The entry
below says so, which is this project's habit and the second time it has changed what
was built.

And the first rule has left the front page. `PAINTER.md` is held to 10,000 words, the
two documentation items it needed did not fit, and the growth rule's own answer is
that **a rule the engine checks at the call can leave the guide**. *You will
under-vary your marks* is that rule: the post-pass check names it after every pass,
with the numbers, which the paragraph could not do. Whether a rule can safely leave
is now a question a session can answer, which is the point of moving it.

#### Added

- **`glaze(points, color, to_value=0.42)`** — `at_value` for a film. A glaze's
  strength is its distance from what it lands on, so the usable window is a few
  hundredths of opacity wide and sits somewhere different over every passage; *mix the
  glaze close, then choose an opacity* leaves the second half as a search run by
  rehearsal, and one painting spent six of them on it. This runs the search: films on
  trial canvases until one delivers the value asked for, measured over **the film's own
  footprint**, then that one for real. It costs one stroke like any other glaze, the
  chosen opacity is in the log, and because the trials come off a copy of the stroke
  stream **the film that lands is byte for byte the film that would have landed had its
  opacity been typed out**. A target the film cannot reach raises, naming both ends of
  what it can, for the reason `at_value` raises.
- **The inward scumble warns from the narrow side too.** Its brush is `3 × depth / n`,
  so more rings on a shallow patch buy a *narrower* brush and not finer banding — and
  past `n = 120 × depth` that brush is under the `0.025` where a comb is four streaks
  with gaps. It had warned since the third session when the brush was too *wide* to lay
  a fall-off and said nothing at this end, where a painter met it at `n=12` on a patch
  `0.075` deep, read the post-pass check's bristle complaint as unrelated, and spent
  two more rehearsals. Where no `n` fits at all — under about `0.042` deep, where even
  five rings comb — it names *a volume of lit air* instead, because a glow that shallow
  is not a bloom on a surface.
- **The price walk covers a sequence of directions.** It fired on `direction` left off
  and not on a painter who chose one and chose ten. A list that costs over 2.5× its own
  dearest angle now says so from `cost` and from the call, with every angle's price in
  the line — and two angles can never be more than twice the dearer of them, so the
  cross-at-the-mass's-own-angle idiom every painting here uses stays silent.
- `shape.inside(xs, ys)` is in `REFERENCE.md` beside `contains`, and both are where
  small marks are laid into a larger mass in `RECIPES.md`. One painter hand-rolled
  edge-intersection arithmetic about fifteen times with `contains` listed in the file
  open beside them: a list of methods answers *what exists*, and is read once at the
  start rather than at the moment a mark is placed.

#### Changed

- **`RECIPES.md` separates its two glow recipes at the moment of choosing.** *A passage
  light in the middle* and *a volume of lit air* are the right pair, and the sentence
  that told them apart sat inside the second one, where it is read by a painter who has
  already chosen correctly. The index now says *on a surface* against one and *in a
  medium* against the other, and the first entry says it outright. Four sessions have
  reached the glaze answer the hard way and one of them had the recipe open.
- **`PAINTER.md` step 3 sends the value plan through `compare({place: value})` on the
  empty canvas.** The pairs question lived in `PAINTING.md` and `REFERENCE.md` carried
  the signature without the reason; the arm without the essay never ran it. A painter
  who wrote a nine-value plan, checked the separations by hand and satisfied themselves
  still shipped a frame as light as its subject — which is exactly what the pairs table
  was built to ask.
- **`PAINTER.md` says a low-key picture wants a ground of its own.** *Start on a toned
  ground, not white* is right for a mid-key picture and silently wrong for a night one:
  the lowest preset is `umber_wash` at `0.425`, and a painter who took `cool_grey` at
  `0.53` then had to lay every dark mass `solid=True` to cover it. A ground takes any
  colour, so the mechanism was always there — `Session(ground="#5a5045")` reads `0.32`.
- **`PAINTING.md` has *You will under-vary your marks*, which was on the front page.**
  Moved, not cut, and moved because the post-pass check holds both halves of it at the
  pass with the numbers attached. It is the first rule to leave the guide under the
  growth rule that says one may.
- `CALIBRATION.md` gains the three tables this round measured: a direction sequence
  priced angle by angle, the inward scumble's `n` window, and a film aimed at a value.

#### Measured, and not changed

- **A sequence of directions is not priced at the steepest angle in it.** That was the
  painter's own account of the 51 strokes their ten-angle list cost, and they offered it
  as a guess. Measured on their mass, same brush, same density: `"axis"` 4, a single
  `-17°` 7, `"cross"` 15, and a ten-angle sequence 85 — which is those ten angles'
  prices *added up*, `4 + 5 + 7 + 7 + 9 + 10 + 10 + 11 + 11 + 11`. The finding is real
  and the number reproduces; the mechanism is the sum, and the warning is written from
  the mechanism rather than from the guess.
- **`n ≤ 120 × depth` is exact, and "about `0.07`" is the wall for the recipe's eight
  rings rather than for every `n`.** At `0.0667` deep eight rings stop fitting; five —
  the fewest that read as a fall-off rather than as steps — stop fitting at `0.042`,
  and that is where the verb stops being the answer at all. The warning carries both.
- **The fifth documentation item asked for nothing and gets nothing.** *The worked
  examples may prime toward one kind of picture* was offered as an opinion, unmeasured,
  by a session that had itself chosen a low-light subject before opening anything. It is
  a data point for the hypothesis and cannot test it. The measurement is a brief written
  for a high-key or flatly-lit subject, before anyone reads `paintings/`, and that is a
  session's work rather than a release's.

### The ninth session's round: a heron in a flooded lot at dawn

Painted twice. The first
is the restricted arm again with `DIAGNOSIS.md` added — the only data point that
exists on whether the symptom index works — and the second is the same painter and
the same subject with the withheld files in hand. Fourteen items between them, and
the two paintings together separate the two kinds of fault cleanly: **every fault
that was a lookup got fixed by reading, and the one that was judgement repeated
itself exactly, with the recipe open.**

**Two of its claims did not survive being re-measured, and one of those was the
*eighth* session's guess, which this session was measuring.** A sequence of
directions is priced as the sum of its angles, nine measurements for nine, and
`direction=[0, 90]` logs the `0°` stack whole and then the `90°` stack whole. The
other is this round's own: *a warning when an oriented tip is handed a `size` under
about `0.008`* came with a measured table behind it and still had the wrong unit —
the cliff is at four **pixels**, which is a different `size` on every canvas.

And a second rule has left the front page, for the same reason as the first: the
`PAINTER.md` word budget left three of this round's items nowhere else to come from.
*You will use too many strokes on detail and too few on structure* is in
`PAINTING.md` beside *you will under-vary your marks*, and the post-pass check says
both after the pass that did them.

#### Added

- **A seventh rule of the post-pass check: a graded passage laid too narrow.** Three
  or more long parallel marks at three or more colours, stepped further apart than
  half the narrowest brush laying them — `scumble`'s own `2 ×` wall, applied to a
  stack laid by hand, which is the form `RECIPES.md` teaches and the form that gets
  no protection. Measured on one painting against itself: its sky, laid with the verb,
  sits at 4.0 steps and wobbles `0.037`; its hand-laid dawn band tapers to **1.7**
  steps and wobbles `0.072`. The conditions are narrow on purpose — a mass is one
  colour however its passes are spaced, which keeps every `block_in` out of it, and
  marks more than four brushes apart are separate marks. The first rule to arrive from
  a session asking for a check rule by name.
- **An oriented tip under four pixels says it will lay nothing.** Not an aesthetic
  rule: a `flat`, `bristle` or `knife` that small does not make a poor mark, it makes
  **no mark**, and is charged for it. One stroke deposits *zero* paint at 1–2px
  against a `round_hard`'s 44–51 pixels' worth, and a solid mass laid at 2.7px comes
  back the value of the ground under it. It fires once per call from every verb a
  `size=` reaches, and from `cost()` before a stroke is spent.
- *A graded field that is most of the picture* in `RECIPES.md` — a sky, a far field, a
  sheet of water at a grazing angle, which none of the other light recipes is. Four
  ingredients collected from three paintings, with the one measurement the request did
  not have: `load=1.0, load_falloff=0.0` is not the verb's default on a band, and
  without it `0.9%` of an eleven-pass field comes back within a hair of bare ground.
- *Without a reference* under `The drawing` in `PAINTING.md`: the precision loop with
  the points checked against **each other**, and the parallel-pencil loop written out.
  Eight of the nine painters before this one never drew a line.

#### Changed

- **The check's bristle floor now skips a comb that was starved on purpose.** *A
  bristle under `size=0.025`* fired twenty-eight times in one painting and was
  correctly ignored twenty-eight times: its subject is broken glints on water, grit
  under a flood and feather groups on a bird, where the comb's gaps **are** the mark.
  It now needs a `load` over `0.6`, the top of the run-out window `CALIBRATION.md`
  already publishes. Checked against both of that session's paintings: every
  small-bristle call site in them names an explicit `load` and **not one** uses the
  preset's `0.9`, so the rule was firing on nothing it was written for.
- **`REFERENCE.md`'s `direction` row said the opposite of what a sequence does.** *Or
  a sequence for one pass each* reads as *n passes for n angles* and means *n complete
  stacks*; it now says so, with the pass counts and the 515-stroke quote a sixteen-angle
  list drew. The price walk itself landed in 0.3.0 and fires on all nine of this
  session's cases; one fix of its own, the suggested cross on a mass whose axis is `90`
  was being written as `("axis", 180)` rather than `("axis", 0)`.
- **`solid`'s row and `sample`'s entry both said less than they should.** `solid=True`
  is "what fills a mass" and does not fill it to its colour — a mass lands *between its
  mixture and what it was laid over*, measured in both directions. And `sample`
  averages the place it is given, so a cell hands back the mass averaged with
  everything around it: a bird planned at `0.30` in water at `0.50` reads `0.501` by
  its cell and `0.327` by its own shape. A painter read two masses that way and
  concluded the engine lays everything `0.14` light.
- `PAINTER.md`: the pairs question in step 3 now says the threshold is about two masses
  that **meet**; step 2 names *a veil of light is a mass at a depth* and `look(diff=True)`
  beside it; and the pencil is no longer sold on being free, which a rehearsal also is.
- `CALIBRATION.md` gains *What a solid mass actually lands at*, and the across-band
  ripple table gains the clause a painter spent a measurement discovering it needed.
- `PAINTINGS.md` records what the numbered-pass convention does to the drawing: seven
  of the ten paintings here drew no line at all and nine placed no landmark.

#### Measured, and not changed

- **A sequence of directions is not priced at its steepest angle**, which the eighth
  session guessed and the ninth measured: the cost is the exact sum of what each angle
  costs alone, nine for nine across three shapes, and in paint it is one whole stack
  per angle laid one after the other. The warning was already written from the
  mechanism rather than from the guess, so nothing had to move.
- **The across-band ripple metric does not read canvas texture.** A painter compared a
  hand-laid band against a `scumble` with it, got an answer the wrong way round, and
  put it down to flecking on a `rough` ground. Measured: identical on `smooth`, `linen`
  and `rough` to four decimals at every window width, and on a *starved* pass `rough`
  reads *lower*. What it is sensitive to is the window — `0.0008` across the full width
  against `0.0020` through a narrow column, for the same paint. One clause beside the
  table, and the table itself is unchanged.
- **`DIAGNOSIS.md` is not changed on n=1.** The one session that has had it read it
  front to back, recognised five rows on sight, and followed **zero** pointers in 293
  strokes. An index whose rows carried the repair as well as the pointer would be the
  fourth copy `LESSONS.md` refuses, so the proposal is a protocol question — hand it as
  a file to grep and record which arm was run — and that is where it is written.
- **Which of the three pencil diagnoses is right is left to a run.** All three are
  documentation fixes and all three are made, because each is correct on its own terms;
  picking between them needs a painter working from a guide that carries all three.

### The documentation restructure

No engine behaviour or default moved.

- **One home per rule.** Every rule in `PAINTER.md`, `PAINTING.md`, `RECIPES.md`,
  `REFERENCE.md` and `CALIBRATION.md` is now stated once, in the file it belongs to,
  and linked from the others. The same six rules had been stated in four to six places
  each. `scripts/check_guide_overlap.py` reports any sentence that appears in more than
  one of the five.
- **`PAINTER.md` is a card and a body.** *The first hour* is the loop, the order, the
  five mistakes with their fix on the same row, and a pointer to the checklist, in
  under a thousand words; the body states each step once with its number and links to
  the situation and the measurement. The anecdotes that carried the rules — which
  painter did what, and how many strokes it cost — moved to `CALIBRATION.md` under
  *From the sessions*, where a painter's own count is labelled as such. The drawing is
  step 1 of the order, in its own right. 9,973 words to 6,441.
- **`RECIPES.md` is the situations file.** Same entries, each trimmed to the calls,
  the failure and the number, plus one new entry, *A scene with straight edges*: the
  projection helper three painters had each built for themselves, and the one thing the
  guide had nothing on.
- **`PAINTING.md` is the engine's behaviour**, with the reference-photograph material
  gathered into a last chapter a painter without a photograph can skip, and the MCP
  section moved to `REFERENCE.md` with the rest of the facts. 11,500 words to 6,900.
- **`CALIBRATION.md`** gained an index at the top mapping each rule the guide states to
  the section that measured it, and the *From the sessions* section. No measurement
  changed.
- `DIAGNOSIS.md` gained a row for the new recipe and follows one pointer to the rule's
  new home.

## [0.2.0] — 2026-09-13

The fourth painting session's six engine requests, the guide split by function, the
third session's engine round, and the package finally carrying the guide it is useless
without. Two of the six requests **did not survive being re-measured**, and the entries
below say so where that is the case — checking a painter's numbers before building on
them is the rule in `LESSONS.md`, and it changed what was built twice here.

And, cut into the same release before it shipped, **the greenhouse round**: three
painters handed one subject left three request lists, deduplicated into eleven engine
items and eight documentation items, plus the post-pass check that had been the cheapest
open item on the register for two rounds. Every number the three painters took
reproduced; two of the mechanisms they proposed did not, and the entries say which.

### Added

- **The post-pass check.** `s.report(since=)` reads the guide's standing warnings off
  the log instead of repeating them: one brush at one size for a whole pass, a stack of
  passes at one angle, a bristle under `size=0.025`, small marks before the masses are
  down, a pressure list on a short chisel mark, and the subject's share of the marks so
  far. `easel run` prints it beside the budget line after every pass, rehearsed or
  committed; `--check` widens it to the painting, `easel log --check` reads it without
  painting, and the MCP `run` tool hands it back.
- **Four warnings, in the shape the `smudge` and `scumble` warnings have** — the call
  still does what it was asked and says what it will look like: a pressure list on a
  short hand-laid mark with a `flat`, `bristle` or `knife` (it changes the paint, not
  the width); a shaped `block_in` with `direction` left off costing over 2.5× what
  `"axis"` would, from `cost` and from the call; `edge="clean"` on a mass whose shorter
  extent is under four brushes, from `block_in` and `preview`; and a banded `scumble`
  whose auto-sized brush is wider than its passes at one end, naming both lengths.
- `compare({place: value})` lists every pair of planned places the plan itself puts
  within the threshold of each other and asks whether they touch — the check the sheet
  never ran: a plan finished all-green with two masses planned `0.00` apart.
  `Comparison.pairs` is it as data.
- `palette.chroma_of(color)` — how *coloured* a colour is, beside `value_of` for how
  light. Measured, the engine lays the chroma it is given, so what reads more vivid
  than its number is the eye judging it against the field, and this is the number that
  predicts it.
- Every log record carries the random stream's state at the start of the call that
  made it (`params["rng"]`) and the mass verb that laid it (`params["via"]`). No format
  bump: older files load, and older builds read the new ones.
- A ninth exercise, the swatch strip: every planned mixture laid side by side before
  the first mass, printing value and chroma. In the guide and `examples/exercises.py`.
- Four recipes: *a volume of lit air* (a beam, a shaft, a halo seen from outside), *a
  small container with something spilling from it*, and two composition entries
  collected from the paintings' notes — *a subject that is one thing against a ground*
  and *a picture with an empty half*.
- `scripts/probe_greenhouse_session.py` — the measurements behind this round, runnable.
- `s.sample(place, rendered=True)` — sample the surface `look()` and `export()` draw
  (relief, and graphite the paint has not buried) instead of the pigment, so *is my mass
  darker than it looks?* is one line rather than a belief.
- `easel guide` prints the guide from inside the installed package, and the wheel now
  carries `PAINTER.md`, `PAINTING.md`, `RECIPES.md`, `REFERENCE.md` and
  `CALIBRATION.md` as `easel/docs/*.md`. `pip install easel-paint` used to hand a
  painter sixteen modules and none of the method.
- `easel run p.easel pass_a.py pass_b.py [--rehearse]` runs several passes in order
  against one session, or one copy of it. A pass that goes on top of another pass has to
  be judged on it.
- `s.sweep(..., wander=)`, off for the contour of `block_in(edge="clean")`: measured,
  the sweep's own wobble is what moves a drawn contour off its line (3.3px to 1.1px), and
  the brush's `jitter` moves it not at all.
- A rehearsal carries the painting's last look, so `look(diff=True)` inside a rehearsed
  pass tints what that pass would change.
- `PAINTING.md` (the reasons) and `RECIPES.md` (fourteen procedures collected out of the
  paintings' own pass scripts) — both moved out of `PAINTER.md` rather than written new.
- A one-click `.mcpb` desktop bundle, built and verified by the release workflow, and an
  MCP Registry entry published in step with each release.
- Python 3.14 is supported and tested.
- `scripts/probe_fourth_session.py` and `scripts/probe_third_session.py` — the probes
  behind the numbers in `CALIBRATION.md`, runnable.
- This changelog.

### Changed

- **The contour of `edge="clean"` is swept along the polygon's own edges**, not a
  spline through its corners. Through two sparse corners the spline bowed outward, and
  three painters met it on three shapes: a pointed arch above a tapering tower, a cap
  eaten to a mushroom, and a 65px arch standing off a four-cornered tower. Measured on
  that tower the contour goes from 65px above the top edge to 4px, the ragged fill's own
  half-brush; the dusk example's `tower()` goes from 45px to 4px. **A behaviour change
  for every clean mass**: a script with one paints differently after this, and every
  committed painting with a clean edge rebuilds with its silhouettes where they were
  drawn. The draw from the stream is unchanged, so nothing laid after a clean mass
  moves.
- **A rehearsal copy counts on from the painting.** Inside `s.scratch()` or `easel run
  --rehearse`, `stroke_count`, `spent`, `remaining` and `budget_line()` are the
  painting's own numbers plus what the pass laid; they read `0` and the whole budget
  before, while `compare()` in the same script saw the painted canvas. What the copy
  itself laid is `s.history.stroke_count`, which is what the *Rehearsed* line reports.
- `block_in`'s `direction` defaults to `None`, which means horizontal exactly as before,
  so the engine can tell *left off* from *chosen*.
- `cost_line()` names the remedy beside the mechanism: *cut into N pieces by the outline
  — lay the straight stretches as strokes, or use a wider brush*.
- The log writes every point exactly rather than rounded to five decimals. Session files
  are a little larger; a replay from one is the painting.
- *The shape each tool leaves behind* has a row for the chisel staircase — a `flat` or
  `knife` filling a mass whose boundary is not parallel to its passes — with the
  measurement (13–17% of strong edges horizontal against 3–4% for a comb or a round tip)
  and the one-stroke repair beside it.
- **`smudge()`'s default `size` is `0.02`, was `0.07`**, and anything past `0.03` now
  warns. Measured on a steep join: what `size` buys stops at about `0.02` (a single pass
  takes roughly half the join out and no more) while what it costs keeps growing — at
  `0.07` one pass drags the lighter mass `4.4%` of the canvas height into the darker,
  against `1.3%` at the default. That is the pale finger-shaped lobe four sessions have
  described. Sizes the guide's own examples used were off the end of that table.
- **`scumble()` on a band picks its own brush**, `3 × extent / n`, when no `size=` is
  given — the mechanism `direction="inward"` has used since 0.1.0, now on both
  directions. A preset's default lands at one to one and a half pass steps on an ordinary
  band, which measures as the worst banding of any width tried. Handed a brush under two
  steps it warns and says how many steps wide it is.
- A keyword that is **not** a brush field now raises a `TypeError` naming the call that
  does take it — `solid=` belongs to `block_in`, `glaze=` to `stroke` — instead of
  `Brush.__init__() got an unexpected keyword argument` from a class the painter never
  mentioned.
- `Region` unpacks: `x0, y0, x1, y1 = shape.box`. It raised `'Region' object is not
  iterable`, which said nothing about where the four numbers were.
- `compare()`'s table says which of the two surfaces it measured (the paint) and names
  the call that reports the other one.
- A `pressure` list is read in canvas order on every pass of a `scumble` or a `sweep`,
  so a passage meant to brighten toward one side can be laid with the verb. The paint
  still alternates direction pass to pass; only the profile is compensated, so nothing
  painted before this moves.
- `s.sample(place)` returns the engine's own linear `float32` array, averaged over a
  shape rather than over its box.
- `PAINTER.md` is the method only — 17,625 words became 9,463, with a 10,000-word budget
  asserted by `tests/test_guide.py`. Not one word was deleted; the essay moved to
  `PAINTING.md`.
- `__version__` is checked against `pyproject.toml` by a test. It had already drifted
  once: the whole of 0.1.1 advertised itself to MCP clients as 0.1.0.

### Fixed

- **`undo` puts the random stream back**, in-process and through the session file. A
  mass draws its pass wander from the session's stream between the strokes it records,
  so undoing one left the stream past it, and `easel undo` — which rebuilds from the log
  — handed back a stream sitting at the seed; the next mass then drew wander a clean
  rebuild never had. A painter measured its working session drifting `1.06%` of its
  pixels from a rebuild and committed the rebuild. Every record now carries the state its
  call began from, `undo` restores it on both paths, and `replay(upto=)` puts the rebuilt
  session's stream where the kept painting stood.
- **A replay from a saved log is byte-identical to the painting.** It was not: the log
  rounded every point to five decimals, so every wobbled pass came back from disk a hair
  off its line — the half of the drift above that no toy case could show, because
  hand-written coordinates are short decimals to begin with.
- `easel run --rehearse` with a single script reported `stroke_count` `0` and the whole
  budget *inside* the script. See *Changed*.
- `block_in`'s `overhang` is documented as what it is: it lengthens each pass past **the
  ends of the pass**, and which two edges those are turns with `direction` — so on a mass
  swept vertically it runs the paint down off the mass's foot. Measured, with the
  box-versus-shape default difference given its own clause. Two masses in one painting
  were spoiled learning this.
- `scumble`'s opacity is documented as what it is: the passes overlap, so a low opacity
  accumulates back toward full colour instead of thinning the passage. From `0.40` up it
  delivers the same passage to within `0.04`. To keep a passage quiet, mix its two
  colours closer together.
- The inward scumble's brush comes from its ring step, and `depth` is computed in one
  place so the step a size is derived from and the step the rings are laid on cannot
  drift.

### Measured, and not changed

Five requests were acted on by measuring them first, and the measurement said no:

- **The engine does not make a mixture more vivid than it was mixed.** Two mixtures
  came back far more saturated in a low-chroma field than their numbers suggested. A
  solid plane reads back at the mixture's own chroma or a little *under* it, in the paint
  and in the rendered view alike; what moved was the eye, judging a colour against its
  field. So no rule and no fix — `chroma_of` is the instrument that lets the question be
  asked as a number.
- **Neither trigger proposed for the clean-edge failure was the trigger.** The distance
  between two outline corners and the brush's share of the shorter extent were two views
  of the contour's spline, which is gone. The share survives as a real second finding —
  the corners of a narrow clean mass go past about a quarter — and that is what the new
  warning reads.
- **The default direction stays horizontal.** `"axis"` would be right nearly always,
  and moving it would move every painting ever made; the price walk says so instead.
- **`pencil`, `dry` and `erase` shift the texture of every mark laid after them**, and
  that is left as it is: it is the log index, not the stream — a mark's texture is seeded
  from its place in the log — and seeding from the paint marks alone would move every
  painting with an underdrawing. Documented, with the property the planning verbs do
  have asserted by a test: `look`, `preview`, `rehearse`, `cost` and `compare` leave
  nothing behind.
- **The view does not lift a solid mass off the value it was mixed at.** A session
  priced this as its most expensive item — four masses laid at planned values that came
  back as bright bars while `compare()` reported the plan clean. Over a mass the rendered
  view and the sampled paint agree to `0.000` at every load, value and ground measured;
  the relief is a *gradient*, so it brightens one side of each ridge of paint and darkens
  the other by as much. `solid=True` costs nothing in the view. What was missing was the
  ability to ask, which `sample(rendered=True)` and `compare()`'s new label now give.
- **`overhang=0` does not leave a shape's boundary bare**, so the warning that was asked
  for is not built. Laid solid, the strip inside the pass ends comes back `0%` unpainted
  at every setting; at the default load it is `8.7%` bare — and the strip inside the
  *sides*, where `overhang` does nothing at all, is barer still at `14%`. That is the
  comb's own texture and the brush running dry, and its condition is `block_in`'s own
  defaults.

### Removed

- `glama.json` and `smithery.yaml`. Neither aggregator reads a file from the repository
  any more, and Smithery discontinued the stdio form the file was written in.

## [0.1.1] — 2026-09-12

### Fixed

- The registry marker in `README.md` and a `server.json` that 0.1.0 shipped without.
  0.1.0 published from a commit two merges older than the one that set the release
  version: its `pyproject.toml` already said `0.1.0`, so the tag guard compared `0.1.0`
  to `0.1.0`, matched, and published the older tree. No engine change — the rule the
  version comment states (edit, commit, merge, then tag *that* commit) is the part that
  has to hold.

## [0.1.0] — 2026-09-12

First public release: the whole engine as it stood after two painting sessions and the
two engine rounds they bought.

### Added

- The painting engine — procedural brush tips, paint load and run-out, wet-into-wet
  pickup, canvas tooth, subtractive pigment mixing, impasto relief, a graphite layer,
  undo and replay from the seed.
- The painter's vocabulary: `stroke`, `dab`, `block_in`, `sweep`, `scumble`, `cover`,
  `smudge`, `glaze`, `pencil` and `erase`, over regions, grid cells, spans and shapes
  (`polygon`, `ellipse`, `blob`, `hull`, `ribbon`, `union`, `s.circle`).
- One plan object shared by `cost`, `preview`, `rehearse` and `paint`, so what is tried
  and what is committed cannot diverge; `Session(budget=)` and the budget line;
  `--rehearse`, which commits nothing and seeds the next real marks so a rehearsed pass
  lands pixel for pixel.
- `compare("ref.jpg")` and `compare({place: value})` — the second is how a painter with
  no photograph checks the canvas against their own written value plan.
- `easel` (the CLI), `easel-mcp` (the MCP server), and the guide:
  `PAINTER.md`, `REFERENCE.md`, `CALIBRATION.md`, `LESSONS.md`.

[Unreleased]: https://github.com/Gemberkoekje/EaselAPI/compare/v0.6.0...HEAD
[0.6.0]: https://github.com/Gemberkoekje/EaselAPI/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/Gemberkoekje/EaselAPI/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/Gemberkoekje/EaselAPI/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/Gemberkoekje/EaselAPI/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/Gemberkoekje/EaselAPI/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/Gemberkoekje/EaselAPI/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/Gemberkoekje/EaselAPI/releases/tag/v0.1.0
