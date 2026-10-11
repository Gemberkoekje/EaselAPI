Overall, Easel is worth using, especially for a game with an oil-painting direction. It's best at what it's built for: single painted compositions. For game assets it got me most of the way, with gaps I had to fill myself. The documentation teaches painting method very well but is thin as an API reference.

## What worked well

* Determinism. A seeded script re-ran to a pixel-identical PNG every time. That's why I could commit the scripts as the source of the art and later repaint four pieces with confidence. This is its biggest practical strength for a pipeline.
* Error messages, the best I've seen in a library.
   * When I asked for a value darker than the mixes can reach, it told me the floor, named a hex colour at the value I wanted, and suggested keeping a little hue in it.
   * When a brush was too small to leave paint, it gave the pixel width, the threshold, and the exact size or brush to use instead.
   * When I misused `press`, it explained why and offered three alternatives.
* The method nudges toward better pictures. Plan your values, lay big masses back to front, keep highlights for last, sign it. The "what you're bad at" list (boxes, combs, outlines) described my early mistakes almost exactly.
* `palette.at_value()`. Asking for a colour at a given lightness is the right abstraction.

## What got in the way

* Paint deposit is hard to predict.
   * `density=1.0` still left gaps; I needed `solid=True`, and sometimes a second pass on top.
   * Shading strokes at opacity 0.6 changed the candle by only a few brightness levels. I had to go to 0.9 and paint each stroke twice.
* Colour drift. Umber plus ultramarine, lightened with white, kept turning lavender: the stones and shelf boards came out purple twice. That may be physically faithful, but it's a trap when you're simply trying to get a warm grey.
* No transparency. Exports are flat RGB. The arch opening, the patron and the candle all needed a separate script (`cut_outline.py`) to cut them out along the outlines I'd painted. For sprites this is the biggest missing feature.
* The checklist assumes a standalone painting. It flagged "no clear light" on shelves I'd deliberately kept dark so they'd sit behind the archway. It can't know a piece is one layer of a scene.
* Geometric subjects fight the method. Shelves, iron bars and arch joints are inherently ruled lines and combs, which the guidance tells you to avoid. I compromised, and those pieces look the stiffest.
* Normalised 0–1 coordinates on wide canvases meant writing a pixel helper in every script. `s.px` exists, but polygons are still given in 0–1 coordinates.

## The documentation

The guide (767 lines) is well written and genuinely teaches painting, but it's heavy on method and light on reference. I repeatedly had to read function signatures and constants from the code itself: `ribbon`'s width, the names of the pressure profiles, the fact that `press` only works with a single point. A one-page table of brushes, parameters and units would have saved several failed runs. It also never says plainly how opacity, density and `solid` combine, which is where most of my trial and error went.

## Caveats

I used only the Python API, not the CLI or the MCP server, and I have nothing comparable to measure it against. The art it got out of me is honest interim quality: it reads as painted and holds together as a set, but it's crude in places, such as flat stones and stiff bars. A more practised hand would get more from it. Your oils will easily outclass it.
