# A heron in a flooded parking lot, dawn

**To understand this, start by reading `prelude.py`** — every mixture, every shape and
every mass lives there as a named function. The `passN_*.py` files are one line each:
they call those functions in depth order. Then read the passes in order, then look at
[`painting.png`](painting.png) and [`painting.gif`](painting.gif). The same subject was
painted a second time with every document read; that one is [`../2/`](../2), and its
`NOTES.md` is the other half of this one.

1024×768, rough canvas, `toned_warm_grey` ground, seed 17. **293 of a 320 budget.**
Subject share **33%** against a planned 32%.

## The picture

Grey heron standing in sheet-flood over a parking lot at first light. A sodium lamp
still on and losing to the dawn. Stall lines showing through the water as pale ghosts,
crisp where the sheet is thin at the bottom left.

## Decisions that mattered

- **Value plan first, and swatched.** Dawn band 0.68 / sky and water 0.53–0.55 /
  trees 0.22. The bird carries its own range inside that: white head 0.80, grey back
  0.46, flank 0.30.
- **Counterchange at the focal point.** The head is white against the darkest mass in
  the picture; the bill is dark against the lightest. That pairing — not size, not
  centrality — is what makes the eye go there. The bird is a tenth of the canvas.
- **The far edge is lost across the whole left half.** Water meets sky at 0.07 of
  value, under the reading threshold, so there is no horizon line at all until the
  trees pick it up on the right. That began as a repair for a ruled horizon and ended
  up the best thing in the picture.
- **Five horizontal bands, so five crossers**: the bird, the pole, the lamp's path on
  the water, the bird's reflection, and the stall lines converging left.

## Gotchas, in the order they cost me something

1. **Rehearsing paid for itself on the third pass.** A treeline with four block-in
   directions priced at **515 strokes** — 1.6× the entire budget. One direction: 22.
   `cost()` and `cost_line()` before a shaped mass, every time.
2. **Ochre + any blue in this box is green**, and at high value it shouts. Three of
   twelve planned mixtures came back mint/olive on the swatch strip. Warm with
   `burnt_umber`, or neutralise with `cadmium_red`.
3. **A chisel staircases a sloping silhouette.** The bird's outline came out as
   pixel-art at `size=0.012`. `edge="clean"` fixed it in one go.
4. **A mass thinner than the brush blooms pale.** The bill as a `block_in` landed
   *lighter* than the sky it was meant to read dark against. A bill is a stroke.
5. **Cell-sized planes want strokes, not block-ins.** The breast and shoulder laid as
   shapes read as slabs stuck on; as three or four overlapping marks they read as
   feathers.
6. **Judging a mass on bare ground wastes passes.** Two rehearsals went on a far-edge
   strip that looked like a floating bar because the water under it did not exist yet.
   Rehearse the pass *on* the passes it lands on: `easel run a.py b.py --rehearse`.
7. **Depth order applies to light too.** The dawn band is sky — laid last it went over
   the trees, the pole and the bird's head. Repaired by re-running those three at
   their own depth, which only worked because every mass was already a named function.
8. **A glaze mixed 0.05 from the field at opacity 0.10 is invisible.** Two passes of
   near-invisible glazing over the foreground before I switched to paint.
9. **Two corrections I abandoned rather than fixed.** A dry-asphalt wedge that kept
   coming back as a paper cut-out, and a saturated orange pool under the lamp that
   owned the picture. Cutting both was cheaper than a third attempt, and the sheet-
   flood I painted instead was the thing I actually wanted.

## Files

| File | What |
|---|---|
| `prelude.py` | mixtures, landmarks, shapes, every mass as a named function |
| `pass1_draw.py` | the arrangement in graphite (free) |
| `pass2_sky.py` … `pass8_refl.py` | sky, trees, water, submerged lines, near field, lamp, reflections |
| `pass9`–`pass11` | the bird: dark silhouette, the light on it, legs and water |
| `pass12_dawn.py` | the dawn band — the picture had no light until this |
| `pass13`–`pass17` | near field, feathers, waterline, mid water, repairs |
| `pass18_sign.py` | the signature |
| `ex/` | the nine exercises |
| `painting.png`, `painting.gif` | the painting, and how it got there |

## The signature

Two marks in the bottom-right: a short vertical, and a shorter broken one below it.
A thing standing, and what the water gives back — the painting reduced to the least it
could be made of.
