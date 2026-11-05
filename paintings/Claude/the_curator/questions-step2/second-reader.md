# The batch's five questions, answered by a reader who did not paint the pieces

*Pasted by the owner on 2026-11-05 beside the painter's own `../answers-step2.md`, and filed
here as it came, apart from the painter's answers. Its writer says it did not paint the
nine pieces and labels nothing **M**: each answer is **O**, from looking at the two
sheets, or **R**. **The decisions are the painter's**, on the owner's ruling, so this is a
second reading of the sheets and not a choice. Where it differs from the painter's, the
plan's section 6 says so.*

---

They weren’t written for me, but here’s what I’d answer. I didn’t paint the Curator pieces, so nothing below is M. I’ve labelled each answer O where it comes from looking at the two sheets and R where it’s reasoning.

1. The cut’s edge: (b), with (a)’s soften= in pixels. O: On alpha.png, the hold’s patron shoulder steps visibly on the light ground, and the candle’s top corners step too. Your 0.8 px blur and the 2.5 px version both read like paint. R: In a game the cut is the silhouette against a background the painter never saw. If it’s harder than every edge painted inside the piece, it becomes the hardest edge in the composited scene, and the sprite reads as a sticker. So the default should match a held paint edge, about 0.85 px. Build it from 4×4 coverage plus whatever small blur gets it there, and keep soften= as the 10–90% width, solved to a sigma.

2. Painted large, exported small: (a), plus one rule. O: The 1× candle has the weave in the wax, and that’s what makes it read as paint. The 4× reductions are cleaner, and the drips and lights actually landed (0 of 16 marks under the cliff, against 12 of 16 at 1×). But the wax reads closer to plastic, and the brass base loses its marks. Each version is better at one thing. R: So build the size option, document the trade, and add the rule that actually matters: paint a set at one scale. A 4× candle next to 1× shelves shows exactly the mismatch the bench measured.

3. A word at the call, and after: (d). Say M2 once per brush and size per session, not at every call. Read O3 after a pass, at 0.15 / 0.25, and not at s.look(). R: 807 warnings across 31 of 34 paintings is the stack-of-bars warning all over again, and every painter learned to ignore that one. O3 is the one that says what actually landed. M2 says why, so it only needs saying once. Looking should stay free of findings. And let note= carry an opt-out (“signature”, “grain”), so marks that are meant to be faint stop being flagged. That’s the same pattern as key="low": a declaration replaces a guess.

4. Ground line on a cut-out: (a). R: Inside a silhouette, bare ground is a hole, never a breath. On the cut’s edge: two numbers is right. It should only say more when the cut is harder than the hardest tenth of the piece’s own edges, because then the outline is the hardest edge in the picture. If (b) is chosen in question 1, that should rarely fire.

5. The fact at mix(): (a) and (c), no fact at the call. R: A line that fires on 1,035 calls, on the commonest dark in the corpus, would be the most-ignored thing the engine prints. Whether the herons and the pool wanted that violet isn’t measured, so it shouldn’t be said as a fault. p.grey(value, warmth=) fixes it for the painter who wanted a grey. Printing the hue beside value and chroma on the swatch lets the painter who’s looking see it, without telling everyone else.

The same thread runs through 3, 4 and 5, and it’s the one the reports have pushed for all along: a warning the painter can’t silence by stating their intent eventually trains them to ignore all warnings.
