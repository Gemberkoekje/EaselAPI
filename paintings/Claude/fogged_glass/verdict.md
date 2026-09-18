Three honest assessments, with the evidence from this session.

## The tool

**The rehearsal loop is the best thing here, and it's not close.** `rehearse` being seeded as if its marks were the next real strokes means what you preview is what lands, pixel for pixel. That converts an expensive irreversible medium into a cheap iterative one *without* removing the discipline, because you still pay on commit. I rehearsed about 44 times and paid 311 strokes; without it I'd have spent the budget on the four failed versions of the sky and ground alone.

**`cost_line` and the error messages are unusually good.** "42 passes stepping across 0.34 of the canvas, each cut into 1.8 pieces by the outline" doesn't just price the plan, it names the lever — that turned a 130-stroke foliage pass into 38. And the glaze refusal ("the paint under this film reads 0.412, at opacity 1.0 it reaches 0.496, a film can only travel between those two") taught me the constraint rather than rejecting the call. More libraries should fail like that.

**Four things I'd change:**

- **`jitter=0.5` should not be silently accepted.** The default is `0.02`. I passed 25× that and every member of the frame came back as a chain of disconnected beads. The tool warns me about a pressure list on a chisel tip but not about a jitter value an order of magnitude past anything usable.
- **`cover()` is a trap dressed as a convenience.** It's offered as the answer to "you will reach for undo," but its ends run outside the area by design, so on a worked passage it lays a rectangle *bigger* than the mistake. I had to bury its output with hand-shaped marks. It needs a shape-aware form.
- **`inset()` should drop at the frame.** `GLASS.inset(0.024)` eroded the boundary that lay on the canvas edge and left a pale strip down the right side of the picture. `edge="clean"` reportedly handles this; plain `inset()` doesn't, and the asymmetry cost me a repair pass.
- **`direction=` is the one thing I never actually understood.** Whether it names the direction passes *run* or the direction they *step* — my empirical results and the cost output disagreed, and I resolved it by rehearsing rather than by knowing. For an argument that central, that's a real gap.

## The documentation

**The calibration is the point, and it earns its length.** "A smudge removes 40% of a step, once, and a second pass undoes most of the first." "Two masses within 0.10 read as one." "A brush narrower than twice the step brings the bars back." These are measured and traceable, and I used all three. The `Goes wrong as:` line closing each recipe is the best convention in the set.

**But reading it did not stop me making the mistakes it describes.** I painted a box in the background, filled an outline (the cauliflower), got the tool's own shape four separate times, and drew a daisy — every one after reading the paragraph naming it. What *did* stop me was the post-pass check and the rehearsal image. The docs already say this — "a line printed after the pass that did it is worth more than the paragraph" — and I think that's the most important sentence in the whole set. They should take their own advice much further: move more prose into `report()` rules. Roughly 210KB of guidance across five files produced a working set of maybe fifteen rules and the warnings.

Two concrete defects. The `jitter` guidance ("halving both halves the wander") reads as an operation to name rather than a number to compute, and the actual defaults are buried in a run-on line of "every other Brush field" — the recipe should just print `jitter=0.01`. And the "detail before the masses are down" warning fired at strokes 175, 243 and 273 while claiming to police "the painting's first 60"; I learned to ignore it, which is the worst thing a warning can teach.

## The painting

It works, and I'd rank it a solid piece rather than a good one.

**What it earns:** the projection was the right call and carries the whole composition — converging eave, sill and bars, with the far end dissolving instead of terminating. The near pane genuinely reads as wet misted glass. And holding the saturated green back until the runnels was the decision that turned it from a picture of a building into a picture about seeing through something.

**What it doesn't:** it's more *atmospheric* than *constructed*. Large areas are soft haze doing very little work, and the left third slid from "quiet by design" into "empty," which I then patched with late strokes rather than having composed it that way. The tree is the weakest thing in it — I spent on it twice and it's still a grey mass with spoke-like branches; I'd either rebuild it or cut it. The whole thing is low-key to a fault: a 0.26–0.69 range with the two largest areas 0.008 apart reads as generally foggy rather than as fog *in one place*.

The failure that annoys me most is the buried ground. Choosing `umber_wash` so that anything left showing would read as warmth coming through the cool film was the plan's best idea, and I spent it for a solid support without noticing until the final measurement. And the pot has the look of something argued into place — flare, then form, then glazed back — rather than something seen.

One caveat on my own judgement: the medium has a characteristic look, and the comb texture and soft glazes are doing some of the work of "looking painted" that I didn't earn through drawing.