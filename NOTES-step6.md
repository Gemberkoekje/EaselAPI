# Step 6 of `PLAN-0.8.0.md`: the arrangement, flat and small

**To understand this, start by reading the plan's A3 with its *Step 2*, *Decided by the
painter* and *Step 6* notes, and the painter's own answers to 4a, 4c and 4d in
[`answers-step2.md`](paintings/Claude/bell_warden/answers-step2.md); then
`Session.thumbnail`, `_thumbnail`, `_laid_masses` and `_one_call` in `src/easel/session.py`,
`render_thumbnail` in `src/easel/look.py`, `thumbnail_line`, `run_alternatives` and
`_cmd_run` in `src/easel/cli.py`, and the `thumbnail` tool in `src/easel/mcp_server.py` --
and read `NOTES-step2.md` first if you have not, because this step builds the prototype
that one drew.**

Branch: `thumbnail-of-the-masses`, off `main` at `0391074` (step 5, #94).

---

## What this step was for

The Bell-Warden's subject failed three times in paint -- two matching peaks read as ears, lit
planes laid as islands read as a piebald, a lit band round the body read as an arch -- and
each was a drawing failure that cost a rehearsal of 85 to 113 marks to see. Its first
suggestion was *a free silhouette and value thumbnail at drawing time*. Step 2 drew the
prototype from its own passes and put four questions to it (4a to 4d); it answered them the
same day: 192 px, the plan's places *and* the masses laid so far with no argument, a clip as
part of a place, never the drawing over a thumbnail and no look of the drawing alone -- and
a second door, `easel run pass.py --thumbnail`, *the thumbnail I would use every pass*.

## What landed

| | |
|---|---|
| **The verb** | `s.thumbnail(places=None, size=None, path=None)`: `{place: value}`, a value `0..1` or a colour read through `value_of`, a pair `(value, clip)` held inside the clip or a list of them; in the order given, on the ground's own value, greyscale, 192 px; written as `thumbnail_NNN.png` |
| **With no argument** | the plan's places at their planned values, and over them every `block_in`, `cover`, `scumble` and `sweep` laid, at its colour's value (a passage halfway between its two), held as it was held, in log order -- a rehearsal copy's painting under it included |
| **The log keeps the place** | `_one_call(verb, place, mass=)`; the call's first record carries `params["mass"] = {"place": [[x, y], ...], "value": v}` (`_mass_params`); `_replay_records` carries it; `_laid_masses` reads it back, grouping records by `_call_of` |
| **The render** | `look.render_thumbnail(layers, width, height, ground, size)` -- the bench's arithmetic: masks at the canvas's size, filled in order, brought down with a look's filter; `THUMBNAIL_SIZE = 192` |
| **The door** | `easel run --thumbnail`: counted unless `--rehearse` is given too; prints `Thumbnail of the plan's 7 places and 14 masses laid, 6 of them by this pass, at 192 px: <path>` (`cli.thumbnail_line`) -- *these passes* when several share the copy -- and under it, when there are any, the masses a release before 0.8.0 laid without a place |
| **Versions** | `--alternatives --thumbnail`: each version counted, the sheet their thumbnails, `thumbnail_NNN.png`; `label_sheet(below=True)` puts each label under its panel in a cell wide enough for it |
| **The server** | a `thumbnail` tool -- places as `plan` reads its `values`, or `[place, value]` pairs, `[value, clip]` for a clip (`_thumbnail_pairs`, `_thumbnail_value`); `run(thumbnail=true)`, alternatives included. Twenty-one tools, counted in the README, the bundle manifest and `tests/test_mcp.py` |
| **The bench** | `probe_bell_session.py --thumbnailed`: the painter's six arrangements counted as the door counts a pass, the engine's masses against `record_masses`, both drawn at 192 px; the door timed beside a rehearsal; both paintings' mass calls, rebuilt |
| **Tests** | `test_requests.py` *0.8.0 A3* (8), and `thumbnail` in the planning verbs' *changes nothing* test; `test_mcp.py` (2), `thumbnail` and `run(thumbnail=true)` in *planning does not spend the stream*, and the tool count |
| **Documents** | `REFERENCE.md` (the signature, a paragraph and example, the file's name, `--thumbnail` and its paragraph, the server's forms), the README's planning row and tool count, the bundle manifest, `CHANGELOG.md`, `CALIBRATION.md` (*The thumbnail, as built*), `SUGGESTIONS.md` (the row's right-hand column), the plan |

## Decisions and gotchas

**1. The log did not know the masses.** The step-2 package asked the painter whether no
argument should draw *the masses the painting has laid so far, say, which the log knows* --
and the log knew every pass of a mass and never the place it was filling (`boxed`, since
0.6.0, is the one bit of it that was kept). Drawn from the passes instead, a ragged mass's
footprint is its place widened by half a brush all round, three thumbnail pixels at 192 for
a brush of `0.03`, and a mass laid at `density` under 1 would come out striped: not the flat
place the painter judged. So each mass call's first record carries the place it was handed
and the value its colour reads, as `params["mass"]`, beside the stream -- read with `.get`,
by nothing that lays paint, carried by a rebuild the way `rng`, `via`, `boxed` and
`color_name` are, and ignored by an older build (`_brush_from_params` takes only a brush's
fields). It takes no index and draws nothing from the stream, which is rule 7. The only
cost is the file: one outline and a number per mass call.

**2. A place kept as its outline.** A rectangle is kept as its four corners and masked by
pixel centres, as every shape is; the bench masked a `Region` as `int(x * width)` columns,
which can differ by one column at the canvas's size. None of the six arrangements the
bench drew has a rectangle among its masses, so its parity does not test one; at 192 px a
column is under a fifth of a pixel.

**3. The plan under the masses.** The plan is what the painter wrote down before the first
mark, so it is the first layer and every mass lies over it: where a mass has been laid the
thumbnail shows the mass, and where none has, the plan. Drawn the other way, the thumbnail
of a finished painting would be its plan.

**4. The door counts.** *The pass is counted, not painted* -- the painter's words -- so
`--thumbnail` is `--count` with a picture. A painter who also says `--rehearse` gets the
paint as well: the look and the thumbnail, both written. Under `--alternatives` a sheet
holds one picture per version, so `--thumbnail` makes it a sheet of thumbnails and counts
every version -- two sheets for one run would be two answers to one question; a sheet of
looks is `--alternatives` without it, and `--rehearse` beside them changes nothing, as it
never has under `--alternatives`.

**5. Labels under the panels.** A panel label is 13 pixels high over the panel's bottom
left, which on a thumbnail 144 pixels high lies across the bottom tenth of the
arrangement -- the floor, in the painter's picture. `label_sheet(below=True)` gives each
cell room under its panel and widens a cell to its label; every other sheet is laid as
it was.

**6. The server's pairs.** A JSON key is a string, so an object's keys can only be the
places `plan` reads -- names, cells, spans -- and a shape, which is what *does this
silhouette read?* hands over, could not go in. A list of `[place, value]` pairs takes a
place in any of the six forms. The Python verb takes a dict, as decided; the pairs are the
server's way in (`_thumbnail_places` reads both).

**7. What a mass's value is.** A mass's colour's value, as `value_of` reads it -- the value
it was mixed to, which is what a notan is of, not what the paint landed at. A passage is
halfway between its two colours' values, as the bench drew it; a sweep's place is the
ground `preview` draws it covering (`_sweep_cover`); a burial's mass is on its first mark,
not on the `dry` before it, and a burial's own `block_in` is the burial's, since the
outermost call's is the one kept. A pass that mixes a colour off `s.sample()` is drawn at
what the canvas so far holds there, since a counted copy lays no paint of its own -- as the
bench's was (`NOTES-step2.md`, gotcha 7).

**8. Older masses, said.** A mass laid by a release before 0.8.0 has no place; it is left
out, and the shell and the server say how many on a line of their own under the
thumbnail's. The Python verb returns a path and says nothing; its docstring says so. Every
painting from here on is painted on 0.8.0 (O8), so this is a painting from an earlier round,
reopened.

**9. Nothing new speaks at the call.** An empty thumbnail -- no plan, no mass -- draws the
ground, and the shell and the server say so (*the ground alone: no place planned, and no
mass laid*), rather than raising in the middle of a pass. A value outside `0..1`, a clip that is not a place, a list
where a dict belongs and a size under 1 are refused in words.

**10. On this machine.** As before: `PYTHONPATH=src`, and the probes from inside
`scripts/`. A bash heredoc holding Python with nested quotes still dies with *unexpected
EOF*; the tests were appended with the Edit tool.

## What step 6 did *not* touch

What any mark lays: no golden, sampler or rebuild moves. The card's clause naming the
thumbnail at its step 1, *Draw it first*, is F's, paid for there (4F); the recipe that ends
in `thumbnail({shape: dark})` and exercise 10 are step 7's (A4). `PAINTING.md`'s list of the
verbs that *leave nothing behind* does not name `thumbnail` yet, and the README's *The plan*
row does not name step 5's `key=` -- both claims for F, with the rest of the documents.
`PAINTER.md` is untouched, 45 words from its budget.

## File map

| File | What changed |
|---|---|
| `src/easel/session.py` | `thumbnail`, `_thumbnail`, `_thumbnail_places`, `_laid_masses`; `_colour_value`, `_passage_value`; `_one_call(mass=)` and `_call_mass`, set in `__init__`, `load` and `_trial_session`; `stroke()` writing `params["mass"]` on the call's first record; `_replay_records` carrying it; `block_in`, `cover`, `scumble` (both cases) and `sweep` handing their mass over; `_MASS_VIAS`, `_Drawn`, `_thumbnail_said`, `_mass_params` |
| `src/easel/look.py` | `THUMBNAIL_SIZE`, `render_thumbnail`; `label_sheet(below=)`, `_label_width`, `_LABEL_HEIGHT` |
| `src/easel/cli.py` | `--thumbnail`; `thumbnail_line`; `run_alternatives(thumbnail=)` |
| `src/easel/mcp_server.py` | the `thumbnail` tool, `_thumbnail_pairs`, `_thumbnail_value`; `run(thumbnail=)` |
| `scripts/probe_bell_session.py` | `--thumbnailed`, `probe_thumbnailed`; `thumbnail_runs` split out of `thumbnail_sets` |
| `tests/test_requests.py`, `tests/test_mcp.py` | the tests above |
| `REFERENCE.md`, `README.md`, `mcpb/manifest.json`, `CHANGELOG.md`, `CALIBRATION.md`, `SUGGESTIONS.md`, `PLAN-0.8.0.md` | as above |
| `NOTES-step6.md` | this file |

## Next

- **Step 7 (A4 and B)**: the recipe for a silhouette built from parts, which ends in
  `s.thumbnail({shape: dark})`, and exercise 10, *Three silhouettes*, each thumbnailed; the
  join for a lit form, and a feather said for what it reads as, fur; B1 scoped, B4's recipe,
  F8's two recipes, I1 and I2 as recipes.
- **For step 9 (F)**: the card's clause for the thumbnail at step 1, and the two claims
  above.
