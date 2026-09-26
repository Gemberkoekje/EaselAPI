*The painter's own review of the tool, the documentation and its picture, written after
the export when the owner asked for its honest opinions and its suggestions, and kept here
verbatim from its session — but for two marked cuts that name the pack's other pictures,
left out at the owner's choice. Before writing it, the painter checked one thing, whether
the command line really exits non-zero after a run that worked, and the review opens with
what it found. Its measured claims were re-measured when the painting was filed; what
survived and what did not is in [`NOTES.md`](NOTES.md). The question it ends on was
answered by the owner: the report is filed here, and nothing was posted.*

---

Here's my honest take on each. One correction first: my notes blamed Easel for exiting with code 255 after runs. That was my own PowerShell piping, not Easel. Under Git Bash it exits 0 with a clean stderr, and I've corrected the notes and my memory.

## The tool

**What works**
- **Rehearsal is the best part.** Five passages would have gone wrong on the canvas: the glow on the wall, the face as three stacked profiles, the striped kerchief, the fist as a bun, and the cloth ring around it. Each cost a look instead of 20 to 100 strokes.
- **The notices are specific enough to act on.** For example:
  - `inward-comb` explained why the glow failed and how many rings would fit.
  - `at_value` refused a value the paints can't reach and named the lowest one they can.
  - `glaze(to_value=)` said exactly how far a film could move the value.
- **Mixing to a value** (`at_value`, `value_of`, `chroma_of`) makes value planning something you can actually do, not just intend.
- **The prelude, pass scripts and replayable log** make the work reviewable, and repairs are just re-runs.
- **`s.plan(why=…)` read back at the end changed the picture.** It's the reason the last pass lowered her eyelids.

**What hurt**
- **Drawing precise shapes in 0–1 coordinates on a non-square canvas.** The most useful code I wrote was my own: a pixel helper `P()` and a `T()` that scaled the first drawing up by 1.3.
- **Cost is invisible until after a rehearsal, and then only as a total.** The figure pass came back at 135 strokes, and I had to guess which masses ate them.
- **Some findings can't be traced.** The checklist's "4 small marks … around (0.55, 0.37)" never told me which marks it meant.
- **Low-key pictures with a small light get misread.** Every pass said "no clear light, nothing above 0.42" (a percentile can't see a lamp), and "lantern reads 0.49" averages in the iron straps.
- **No lettering.** The next two briefs, *[two of the pack's pictures, named here]*, both need text.
- **Small snags:** `timelapse --scale` only takes whole numbers, and a pass can silently overwrite a prelude name. My `H` replaced the canvas height.

**Suggestions**
1. A drawing unit (`s.px()` or `Session(units="px")`), and a way to scale or move a group of shapes together.
2. A per-call cost table in each rehearsal report.
3. Every finding names its marks: the log index, the `note`, or the script line.
4. Plan declarations for a low-key picture and for a small light source.
5. **Turn "failed twice, go back to the drawing" into a notice.** The log can see one region being repainted. I broke that rule on the fist with the rule in front of me.
6. A lettering verb, and a glow verb for lamps and windows.
7. A warning when a pass overwrites a name the prelude defined.

## The documentation

**What works**
- **PAINTER.md is the right shape:** the order of work, each mistake with its fix on the same row, the exercises, the checklist.
- **"What you are bad at" predicted me exactly,** including the fist.
- **The recipes with their "Goes wrong as" blocks help.** *A mass built of planes* is what rescued the face.

**What hurt**
- **Volume.** I read over 2,000 lines before the first stroke. Stating each rule once and linking to it everywhere is rigorous, but it means chasing links mid-task.
- **`paintings/` isn't in the pip package**, though PAINTER.md and RECIPES.md both send you there for worked examples.
- **`rehearse_each` and `cost_line` appear only in REFERENCE.** PAINTER.md's loop never mentions them, so I never used them.
- **The gaps are where most of my rehearsals went:**
  - A light's glow on a nearby wall. Fourteen rings showed as rings, eighteen tripped `inward-comb`, and the fallback of wide films couldn't reach the value.
  - A hand. The docs show the four-finger failure twice but never a fix.
  - Lettering.
  - Units for `ribbon` width and `blob` radius.

**Suggestions:** a one-page quickstart of the 20 calls a painting actually uses; ship `paintings/` in the package or link to the repo; mention `rehearse_each` and `cost` in the loop; and recipes for a light pool on a surface, a head turned toward a light, a hand holding something, and lettering.

## The painting

- **It works as a mood piece.** It reads at a glance as a worried woman by a lamp at dusk. The lit profile sits against the dark wall and the shadowed head against the sky, with a warm lamp against cool dusk. The lantern is the best passage.
- **It doesn't work as a painting.**
  - **The face** is a lit mask: a flat lit plane, hard edges all round (47% of all edges are hard), and an even band down its shadow side.
  - **The hand** only reads in context.
  - **Half the canvas** is flat dark shawl.
  - **Overall** it looks like textured cut paper. That's partly the medium and partly me, because I held nearly everything to hard edges for control.
- **Projector risk.** It's a dark picture, and beamers wash out darks. I'd check it on the real projector before painting five more in the same key.
- **My own mistakes:**
  - I carried the gargoyle trick to a face without asking whether it applied.
  - I placed the face's shadow line wrong the first time.
  - I repainted the fist three times.
  - I took the docs' example budget of 300 strokes for a portrait when 450 would have suited it.

**If I revise it:** there are 38 strokes left. I'd lighten the face a little for the projector, soften the jaw and the edges beside the kerchief, and spend the rest on the shawl's drape. The better fix would be a repaint with a bigger budget.

*[A line on the rest of the pack's pictures, naming each, is left out here.]*

Should I draft these points as issues for Gemberkoekje/EaselAPI for you to post, or revise the painting first?
