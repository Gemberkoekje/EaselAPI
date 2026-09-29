# Step 7 of `PLAN-0.8.0.md`: silhouettes, terminators, and letters

**To understand this, start by reading the plan's A4, B (B1 to B4), F8, I1 and I2 with
their *Step 2* and *Step 7* notes, and the painter's answers to 9a and 9b in
[`answers-step2.md`](paintings/Claude/bell_warden/answers-step2.md) and to W-Q4 in
[`answers.md`](paintings/Claude/wenna_brask/answers.md); then `terminator` in
`src/easel/regions.py`, `src/easel/letters.py`, `_check_holes` in `src/easel/session.py`,
and the six new sections of `RECIPES.md` -- and read `NOTES-step2.md` first if you have
not, because the terminator and the recipes' numbers are that bench's.**

Branch: `silhouettes-and-terminators`, off `main` at `c38a8a3` (step 6, #95).

---

## What this step was for

The Bell-Warden's hardest part was a silhouette built from parts and lit from one side;
it found the right lighting -- copies of the silhouette shifted away from the lamp and
held to it -- and no recipe had it, or the join that turns it, or said what `feather=`
does to it. The second painter carried that lighting to a form facing the lamp and got
its profiles stacked like cut paper, found a light's pool where an inward scumble had
left rings, and asked for letters. Step 2 measured every one of these and the painters
decided them; this step writes them down as recipes, with the one helper each needed.

## What landed

| | |
|---|---|
| **`terminator()`** | `regions.terminator(outline, inside, margin=0.004, step=0.002, least=0.02, aspect=None)`: the runs of one outline inside another shape, a margin off its edge, as lists of points in order -- B2, the bench's function with its validation and a closed run for an outline wholly inside. Exported from `easel` |
| **`letter_paths()`** | new `src/easel/letters.py`: `GLYPHS` (74 characters and a space, one to three paths each, arcs kept as their points), `LETTERS`, and `letter_paths(text, place, cap=0.04, slant=0, seed=None, aspect=None)`, which places, slants and -- with a seed -- varies them. Lays nothing. Exported from `easel` |
| **`holes`, measured where the paint landed** | `_check_holes(..., clip=)`: the interior measured is the shape's and every hold's alike, each a brush in from its outline (`_interior_mask`) |
| **Recipes** | *A silhouette built from parts* and *A small cluster of like parts gripping an edge* (*Before the first stroke*); *A silhouette lit from one side* and *A form turned toward the light* (*Surfaces*); *A light's pool on a surface* (*Light*); *A line of lettering* (*Marks*). Three demos, each *nothing says so*: a matching pair of peaks, the cut-out, the rings |
| **Said** | `feather=` in `REFERENCE.md`'s row, *A form that turns* and the lit-side recipe; the rings of an inward scumble on a dark ground in *A passage light in the middle*; `union()` as `PAINTING.md`'s sixth way; `terminator()` and `letter_paths()` in `REFERENCE.md`'s *Shapes* and the units table |
| **Exercise 10** | *Three silhouettes* in `PAINTER.md`, now *Ten small exercises*; the README, `llms.txt` and the server's `guide` text say ten |
| **The guide's preamble** | `demo.preamble` imports `roughen`, `terminator` and `letter_paths`, which a reader of the recipes has |
| **The bench** | `probe_bell_session.py --recipes`: the helper against the bench's (identical on six copies), the lit-side recipe's steps, the form turned toward the light lighting 81% and 84% of itself, the font's 1.54 strokes a character, and `holes` counted both ways |
| **Tests** | `test_requests.py` *0.8.0 B2* (1), the holes fix (1), *0.8.0 I1* (3); `test_reference.py`'s shape list names the two helpers |

## Decisions and gotchas

**1. The recipe found an engine bug.** *A silhouette lit from one side*, laid on the
guide's bare `toned_grey` canvas, said `holes` at the shade copy: *11.62% of this solid
mass came back bare*. The copy is held to the silhouette, so the part of it past the
silhouette is bare by design, and `_check_holes` measured the copy's shape alone. On the
bench's dark field it never spoke, because the ground was within `0.25` of the shade --
the contrast gate hid it. Fixed at the check, not routed round in the recipe: the
measured interior is intersected with every `clip=` hold. It can only say less. Counted
both ways over both paintings and the corpus's 196 solid masses, it says what it said
before on every one (`--recipes`): the recipe's shade copy is the only case it answers.

**2. The recipe's zones each run their own way.** All three along the axis, the check
called them a stack of bars (*64 of 87 long marks within 6 degrees*); at one size, one
tool. The bench's `100` and `18` degrees, and `0.045` and `0.035`, are what the recipe
lays, and its paragraph says why.

**3. The join tapers.** The painter asked for runs *tapered at both ends*; laid, an even
join leaves a blot where a run ends at a waist of the silhouette, and `pressure="taper"`
a smaller one. It does not change the turn's width: laid at 1024x768 the recipe's joins
turn the step at each terminator from `0.5` and `1.0` px to `9.0` and `10.0` whether
tapered or even, and leave the silhouette at `0.5`.

**4. What the typed polygon did that the union did not.** The plan asked the recipe to
say it. It is not the outline's notches -- smoothed, the painter's union keeps 16 turns
sharper than 25 degrees against the polygon's 9 -- but the arrangement, read off both
thumbnails: eight round or short parts gathered round the middle one, with two matching
peaks, against one long mass standing on members that reached the plinth. The recipe's
*Goes wrong as* says so, and its third rule adds *parts crowded round one centre read as
a clump*.

**5. PAINTER.md's room.** Exercise 10 needed about 110 words and the file had 45. The
painter's question 7 had already decided to drop the four near-parallel fingers and the
arrangement redrawn three times, whose rules now carry their own instruments -- the
cluster recipe and the thumbnail -- and the framing *every painter so far* on lines 109
and 373. Those four moves pay for it, 6,672 of 6,700; the anecdotes are in
`CALIBRATION.md`'s *From the sessions*, as F1 said they would be. Line 407's *Every
painter so far has painted boxes* is F3's, since it needs a new claim rather than a cut.

**6. The font is the part that goes wrong**, so it was looked at, not reasoned: every
character laid with the pencil with capitals 50 and 100 px tall, and a seeded line at 35.
The `G` opens right and ends on its bar, and a test holds `C`, `G` and `c` to opening
rightward. The dots started too short to read and were lengthened. A `∂` in the recipe
text fails the cp1252 test for shipped documents, so the recipe says *another letter*.

**7. A lettering pass, and what the check says of it.** Laid alone on a fresh canvas,
the post-pass check says *one brush at one size* and *detail before the masses*; with
`tip_wobble=0`, *one disc printed*, which `tip_wobble=0.35` in the recipe answers. The
first two are rules about masses that a line of writing trips by design; the recipe says
so rather than bending the rule, and whether the rule should know a stroke laid along a
glyph is `LESSONS.md`'s rule 2 for another round.

**8. No nouns.** The lettering example first wrote a sentence naming the second
painting's setting; it writes *Written in a hand of its own*. The exercise's and demo's
`legs` are `members` and `stems`. The grep ran over every added line with both
paintings' nouns.

**9. On this machine.** As before: `PYTHONPATH=src`. A Python heredoc that wrote a
markdown code line holding `\n` wrote a real newline once and broke the block; the
Edit tool fixed it, and `check_guide_blocks.py` is what caught it.

## What step 7 did *not* touch

What any mark lays: no golden, sampler or rebuild moves. `ribbon(width=[...])` (a union
of lobes does it). F7's units rows for a ribbon's width and a blob's radii, F1's move and
budget, F3's claims, F6's clause and the card's line for the thumbnail -- step 9, with the
rest of the documents. A notice for a zone held hard inside its own silhouette stays
declined (section G).

## File map

| File | What changed |
|---|---|
| `src/easel/regions.py` | `terminator()`, in `__all__` |
| `src/easel/letters.py` (new) | `GLYPHS`, `LETTERS`, `letter_paths()` |
| `src/easel/__init__.py` | exports `terminator`, `letter_paths`, `LETTERS` |
| `src/easel/session.py` | `_check_holes(clip=)`, `_interior_mask`; `block_in` passes its `clip` |
| `src/easel/demo.py` | the preamble's imports |
| `src/easel/mcp_server.py` | the `guide` tool's text: ten exercises |
| `scripts/probe_bell_session.py` | `--recipes`, `probe_recipes`, `_HoleCount`, `_recipe_block`, `_laid_recipe` |
| `tests/test_requests.py`, `tests/test_reference.py` | the tests above |
| `RECIPES.md`, `PAINTER.md`, `PAINTING.md`, `REFERENCE.md`, `README.md`, `llms.txt`, `CHANGELOG.md`, `CALIBRATION.md`, `SUGGESTIONS.md`, `PLAN-0.8.0.md` | as above |
| `NOTES-step7.md` | this file |

## Next

- **Step 8 (D)**: the fact at the call for a round dab under its cliff, and a line after
  the pass for every mark that landed nothing.
- **For step 9 (F)**: F7's two units rows; line 407's boxes claim; the card's clause for
  the thumbnail; and whether the lettering pass's two findings are the rule's to change.
