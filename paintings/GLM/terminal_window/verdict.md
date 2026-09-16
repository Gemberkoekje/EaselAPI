Honest opinions, all three:

## The tool

Genuinely good, with rough edges. The simulation is the point: finite loads, wet-in-wet mixing, canvas tooth — these create real decisions instead of "draw shapes". The plan pipeline (`cost` → `preview` → `rehearse` → `paint` on one object) is excellent interaction design, `at_value`/`compare` turn vague judgement into checkable numbers, and the post-pass `report()` caught real mistakes I made (the disc-printed marks in pass 4).

Where it bit me:
- **Undocumented failure mode**: six crossing glazes laid wet, then a block-in on top → concentric ring artifacts. It cost a full scrape. The "volume of lit air" recipe practically invites that structure, and nothing warns about the interaction.
- **`edge="hard"` prints pass-end bites** at the outline, for both flat and round tips. The docs' "shape each tool leaves behind" table gets you close but not to this one.
- Plans can't price all verbs (`cost_line` failed on a scumble), `replay(upto)` semantics are murky, and on Windows the cp1252 console chokes on the docs' unicode.
- To its credit: error messages are good (the `direction` ValueError lists valid options), and determinism/seeded rebuilding is solid.

## The documentation

The best part of the package — some of the most honest tool docs I've read. It teaches a *method* rather than an API, attaches numbers to every claim, and — rare thing — documents failure modes with their fixes on the same row. It predicted my specific failures as an LLM painter ("you will draw outlines and fill them", "you will reach for undo", "you will paint boxes") and was right about every one. The self-skepticism ("every recipe is a recipe that worked once", "the most speculative things in this file") is the opposite of the usual docs voice.

Criticisms: the prose is very dense and aphoristic — scanability suffers, and the constant cross-referencing between five files means ~2,500 lines before the first stroke. And for all that, the two things that actually cost me work (the ring interaction, the hard-edge bites) weren't in it.

## The painting

A solid first painting, not a good one — call it B-minus. What works: the value structure is clean (one light, clear fall from screen → halo → pool → dark), the text reads as a real buffer with the cursor as focal accent, and the rim lights on keyboard and mug correctly point back to the source. The reason I chose the subject is still in the picture.

What's weak, honestly: the composition is safe — near-frontal monitor, dead-center, symmetric pool; the guide's perspective recipe exists precisely to break that and I never challenged my first drawing. The glass glow is faint enough that the text does all the work in the screen's lower half. The halo's oval edge is faintly detectable as a shape. And at 1024×768 the paint quality reads more "textured illustration" than oil — the process was painterly (see the contact sheet), the final resolution doesn't fully sing. The fixes are all upstream of the brush: a viewpoint change and a bolder halo would move it more than any amount of texture work.