*The painter's own review of the tool, the documentation and its picture, written after
the export and pasted here verbatim. Its measured claims were re-measured when the
painting was filed; what survived and what did not is in [`NOTES.md`](NOTES.md).*

---

That's a judgement call, and you've said you'd rather have questions than
confident-sounding answers. Before I give opinions, I'll check a few claims I'd otherwise
be making from memory. Some of my impressions came from zoomed looks or single tests, and
I want to know which were the tool and which were me.

I checked the specific claims below with small tests first. Two impressions from the
painting session didn't survive, so I've dropped them.

## The tool

It's very good at what it's for: letting an AI paint through text, with feedback built
in. It has some rough edges.

What worked:

- Rehearsal: a rehearsal of a pass is exactly what lands when you commit it. That's how I
  caught most of my failures before spending marks on them: the egg-shaped glow, the
  panel stuck on the headland, the gold-coin reflections, the stair-stepped tower.
- Feedback: the warnings name the problem and the fix.
  - One told me my glow was too shallow for the technique I'd used and pointed me to the
    "lit air" recipe. The afterglow got better.
  - One gave me the exact brush size to use on the grass.
  - The most valuable one caught the lantern (0.74) losing to the sky glow (0.77). That
    was the one number my whole idea depended on.
- Planning:
  - Declaring what the painting is for, then having the checklist hold you to it, is a
    strong idea.
  - The cost explanations found a cliff face that would have cost 32 marks, when 15 did
    the job.
  - When I asked for a colour lighter than the paints can reach, the error message gave
    me the exact numbers.
- Docs from the command line: I could learn the whole tool through `easel guide`, `demo`
  and `explain` without opening a single file.

What didn't:

- Hard edges are all-or-nothing. At the tower's edge the brightness jumps from 0.59 to
  0.28 within one pixel, and at the waterline from 0.36 to 0.17. They read as vector
  graphics. It's the least paint-like thing in the engine, and I relied on it.
- Dry-brush speckle reads as dirt more often than texture, as in the flecks in my sky and
  my first try at the swells.
- One check misfired: "graded passage laid too narrow" flagged marks that weren't a
  graded passage, twice.
- Working with it was slow:
  - About 15 s per variant, in the one run I timed.
  - As far as I could tell, the built-in side-by-side comparison doesn't support soft
    blends or glazes.
  - `easel look` has `--no-sketch` but no `--no-marks`, so landmark labels covered small
    details. I wrote my own helper to get clean views and comparisons.
- Session files are large: 16 MB after 171 marks.
- The vertical seam I blamed on the sky blends didn't reproduce in a minimal test. It's
  probably how I layered wet paint, so I'm not counting it against the tool.

## The documentation

It's thorough and aimed at the right reader, but too heavy.

- Its predictions about my mistakes were accurate. My first headland plane was the "slab
  stuck on a smooth shape" it warns about. My first reflections were the "spoon-shaped
  islands" the recipe lists. The two best passages in the painting (the beam and the
  reflection) came straight from recipes and `easel demo`.
- Good design choices:
  - Rules arrive at the moment they apply, through `explain <code>`.
  - It asks you to pick a subject before looking at example paintings.
  - It quotes your stated reason back to you at the end.
- Too much text. It's about 340 KB across six documents, and I read about 180 KB before
  the first mark. The prose is essay-like, with dense cross-references and key facts
  buried in paragraphs.
- Caveats can sit far from the rules they qualify. RECIPES says a pressure list fades a
  soft blend to nothing at one end. Measured at opacity 0.9, it only went from 0.86 to
  0.41 over a field of about 0.14; at 0.5 it reached 0.29. The docs do explain this, just
  in a different file.
- One sentence seems backwards. The lit-air recipe says a glaze with pressure
  [1.0 … 0.1] is "narrow-and-bright at the source and wide-and-gone at the far end." I
  measured 80 px tall at the source and 32 px at the far end. The brightness part is
  right, but the width runs the other way. The recipe's code still works, because its
  three glazes taper in opposite directions.

## The painting

It's competent and coherent, but conventional.

- It does what I set out to do. The lamp is the brightest place in the picture (0.86,
  against 0.77 for the glow), the beam ties it to the glow, and the colours hold
  together. The glow, the beam and the broken reflection are the best parts.
- It's a postcard subject done the safe way. It looks more like digital illustration than
  paint: ruled tower edges, flat fills, crisp masked outlines. The paint quality lives
  mostly in the sky, and even there the brush bands look a bit like contour lines.
- The headland is the weakest part: big, flat and heavy. It failed twice, and the guide
  says that means go back to the drawing. I patched it with brushwork instead.
- I stopped with 43% of the budget unspent. I told you that was to avoid marks made for
  the checklist's sake. Honestly, it was also caution: repainting the headland would have
  buried everything standing on it.
- What I'd do differently:
  - Paint a later, darker dusk so the lamp dominates more.
  - Decide fewer, larger rock planes while it's still a drawing.
  - Let the headland dissolve into the water in more places.
  - Let some of the warm ground show; I covered it completely.

If this is feeding into easel's development, I can turn the concrete items into
reproducible issue reports: the hard-edge masks, the backwards sentence, the missing
`--no-marks`, and the misfiring check. I can also chase the sky seam, but that would mean
reading the package source, so I'd want your OK first.
