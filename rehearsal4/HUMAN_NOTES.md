# The human's note, and what it measures

One note, arriving while the `pass` session was still painting, from the repo's owner
looking at `human_note_exhibit.png` (the session's own `pass/out/look_046.png`, copied
here so the write-up has a stable pointer into the painter's working directory):

> It is not first painting the back of the mug, then the tea, then the front of the
> mug, and because of it, the tea kinda flows out of the mug. Also something went
> wrong with the table, where it looks a table correction was done after the mug ear
> was drawn.

**It was not passed to the painter.** A fresh session that gets coached mid-run stops
measuring the guide, which is the whole reason the protocol runs a fresh session at
all. The note is a result about `PAINTER.md`, and it is treated like one: measured
afterwards, written up, and turned into a guide change that the *next* fresh session
has to test. `REHEARSAL.md` -> `REHEARSAL2.md` is the standing lesson here — a guide
fix is a hypothesis until somebody paints against it.

Both halves turned out to be sharper than a style preference, and the first one is
large. `probe_human_notes.py` has the code; it was written after the defect was seen,
which is what it is good for and the only thing it is good for.

---

## Note 1 — the mug is a container, and the guide never says so

The order the note asks for is far rim, then the liquid, then the near wall. Painted
in that order the liquid's near edge is a real edge: the place where the front wall's
paint stops and the dark behind it still shows. Painted in the other order there is
nothing for the dark to stop against, and it runs off the side of the cup.

Measured as: dark paint inside the mouth's bounding box that is nowhere near dark in
the photograph, with 2% of the picture's width of slack for a soft edge — the guide
tells a painter to let a silhouette overlap, so a mark that laps a little is not a
defect.

| Painting | Dark that escaped | Worst excursion |
|---|---|---|
| **REHEARSAL4 `pass`** | **17.5 %** of the tea's own area | **0.150** of the picture's width |
| REHEARSAL3 `pass` | 0.1 % | 0.046 |
| REHEARSAL3 `assisted` | 0.1 % | 0.204 |

175 times REHEARSAL3's figure, on the same reference, from the same guide. The human
found it by looking; no criterion in the brief catches it. `compare()` cannot: it
averages a cell, and dark paint that has escaped the cup lands in a cell whose
reference is the *dark handle-side shadow*, so it can make the value number better
while making the picture worse.

**What the guide says now.** Section 2, *Paint from back to front*, is entirely about
depth between separate things: "Background, middle distance, foreground, in that
order, every time", with a landscape for its example. There is nothing about depth
order *within one object*. A mug has three depths and they are all the same mug: far
rim, contents, near wall. So does a bowl, a glass, a pocket, an open mouth, a sleeve,
an eye socket. The guide's rule covers all of them and none of its words do.

**Proposed fix, to be tested and not assumed:** one short paragraph in section 2
saying that an object with an inside has its own depth order, naming the mug as the
worked case, and one line in the *Before you call it finished* checklist — "anything
with an inside: is its far edge under its contents, and its contents under its near
edge?" No new API; the engine already does this correctly if the strokes arrive in
the right order.

## Note 2 — the guide already forbids this, in a line nobody acts on

The second half of the note is a correction to the table laid down after the handle
was painted, which cut hard-edged slabs of table colour through it. The guide's own
words, section 2, third sub-bullet:

> **A mistake in the background is cheap while the foreground is not there yet.** It
> stops being cheap the moment something is standing in front of it.

So the rule is present, stated correctly, and was not followed. Measured from the log
— the only place the order of events survives — as how much broad mass paint landed on
ground already carrying a fine mark:

| Session | Broad marks landing on earlier fine work | Standing detail buried |
|---|---|---|
| **REHEARSAL4 `pass`** | 18 | **117.7 %** |
| REHEARSAL3 `pass` | 18 | 33.5 % |

The share runs over 100% because it is cumulative: the same ground was drawn, buried,
redrawn and buried again. The same eighteen marks in both runs, and three and a half
times the damage.

The probe names the culprits, and they are one event: marks **#113, #115, #117, #118,
#119**, every one of them `block-in all 8.0` — a *whole-canvas* block-in at eight
degrees. #119 alone buried 100% of the detail standing when it landed. That is the
table being repainted over everything, and the painter's own log arrives at the same
place from the other direction, counting strokes rather than pixels:

> The allocation was wrong — 138 of 299 strokes went on the table because I painted it
> three times, and the subject got 160.

So both halves of the human's note and the painter's own worst self-criticism are one
defect: **the table was blocked in across the full canvas, three times, after the
object was under way.** REHEARSAL3's 33.5% says burying detail is chronic; what is new
here is the scale, and that it landed on the handle.

**Proposed fix, to be tested and not assumed:** the rule is not weak, it is
unenforceable as written, because a painter fixing a value it has just measured has no
prompt to ask what is standing in front of that mass. Move it out of section 2's
sub-bullets into the measuring loop, where the correction actually gets decided:
before repainting a mass, look at what is in front of it, and if something is, repair
around it or repaint it afterwards on purpose. That is a change to where the sentence
lives, not to what it says — which is the cheapest kind of guide fix and the easiest
to over-claim, so it needs the same fresh-session test as anything else.
