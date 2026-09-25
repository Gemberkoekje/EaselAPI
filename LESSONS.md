# Lessons learned

Easel was built to a brief of nine milestones, and measured by six rehearsal runs in
which fresh sessions painted a picture against nothing but `PAINTER.md` and were then
read. Those write-ups, an adversarial review register of sixty-six findings, and the
brief itself were each recorded at length and have since been deleted: a build note is
worth keeping only while the build it describes is still moving.

This file is what survived them — the method that worked, the engine decisions that are
load-bearing, the traps that cost real time, and what is still open. It is the file to
read before changing the engine or the guide. It is not a changelog, and a new finding
does not get a paragraph here just for being true.

The files beside it: [`PAINTER.md`](PAINTER.md) is the guide a fresh painter reads and
the project's actual deliverable, with [`PAINTING.md`](PAINTING.md) holding the reasons
under its rules, [`RECIPES.md`](RECIPES.md) the procedures,
[`REFERENCE.md`](REFERENCE.md) the facts and [`CALIBRATION.md`](CALIBRATION.md) the
measured numbers. [`SUGGESTIONS.md`](SUGGESTIONS.md) is the request list from the
painting sessions — what each painter found, and what was done about it.

---

## The method that produced this

Every defect worth fixing in this repo was found by looking at a picture. None was found
by the test suite. The suite is what keeps a fixed defect fixed; it has never once
discovered one. That single fact determines the whole method below.

### A guide change is a hypothesis until a fresh session paints against it

This is the rule everything else hangs off. Four consecutive runs demonstrated that
writing a rule down is not the same as the rule working: a paragraph can be correct,
well-placed, repeated three times and in the closing checklist, and still fail every run.
Stating a rule is a *proposal*. The measurement is a session that has never seen the repo
painting a picture and then being read.

### A default is worth more than a warning, and a measurement decides which

Three of the fourth session's six engine items came down to a **default** that sat
outside its own usable window — `smudge`'s `size` four times past the knee of its measured
curve, and `scumble`'s brush left to a preset on both directions of the verb. In every
case the documentation was already correct and already emphatic, and painters followed
the examples rather than the warnings. *When a document has to warn this hard, the
suspect is the default* is the session's own phrasing and it is a good test.

The order matters, though: **measure the curve, then move the default, then warn about
the far end.** The measurement is what tells you where the knee is, and twice here it
also said the default was fine and the request was about something else. A warning is
what is left for the painter who means it — it must still do exactly what was asked, and
say what it will look like, which is the shape `cost()` uses for a budget.

### Warning is not method

The largest single finding across all the runs, and the one that generalises furthest.
Four of six painters independently said the guide tells them a state is bad without
telling them what to do instead — and the guide's response had been to repeat the
warning, which is why a painter could count four instances of a rule it had ignored four
times. Repetition is what a document does instead of having an answer. When a rule keeps
failing, the fix is a procedure, not a louder warning.

**Nor is a measurement.** The lighthouse handover's `edges:` line printed between 54% and
65% of the picture's edges under 2.5 px after every pass from the sea's on — eleven
times, in the range of the two cohort painters who called their own pictures cut-outs —
and the painter kept the hard edge regardless, then named it *the least paint-like thing
in the engine*. A number printed beside the work is a warning with a figure in it. What
moved the edges was the engine, which in 0.7.0 breaks every held edge against the tooth:
where a line was printed and did not change what the painter did, the answer is in the
engine, not in a louder line.

### A separate file of warnings is the fourth copy, and it does not work either

Asked directly whether the warnings should be gathered into their own file for a painter
to keep in context, the third session answered no, and its evidence is its own painting.
It had every warning in context for the whole session — the guide never left its
window — and laid a glow as a solid disc, planes as slabs stuck to a hull, and a picture
in almost nothing but two brushes regardless. The front page lists the mistakes, the
checklist repeats them, and this file records that a rule correct, well placed and
repeated three times still failed every run. **A fourth copy is precisely the thing
that does not work.**

What did catch those mistakes was never a sentence. It was a rehearsal looked at, and
the one line `easel run` prints after a pass. So the form the idea takes is **a check
the tool runs over the pass it just painted**, printed beside the budget line — every
input is already in the log, which carries brush, size, path, colour and load per
record. **Built, in the greenhouse round, as `Session.report()` and the lines `easel
run` prints after every pass** (`--check` widens it to the painting, `easel log --check`
reads it cold). Seven rules, each of which a real pass of a real painting tripped: one
brush at one size for a whole pass of two or more calls; twelve or more long marks
within six degrees of one angle from two or more calls; three or more long parallel
marks at three or more colours stepped further apart than half the narrowest brush
laying them, which is a graded passage that will come back as bars; a `bristle` under
`size=0.025` at a `load` over `0.6`;
eight or more marks under `size=0.02` inside the first sixty; a pressure list on a short
chisel mark; and the subject's share of the marks so far, against the plan's number when
it is given. An eighth — a shaped `block_in` with `direction` left off costing over 2.5×
its axis, or a sequence of directions costing over 2.5× its own dearest angle — needs
the shape and fires at the call. **Each rule that becomes a check can
leave the guide**, which is the growth rule paying for itself.

The count has moved since, and `REFERENCE.md` is where it is kept rather than here:
0.4.0 added an eighth read off the log — three or more small round-tip marks at
`tip_wobble=0`, which is *one disc printed over and over* — a second that needs the
shape, and two standing measurements under the findings, the subject's share and how
much ground is still showing. The list above is what the mechanism was when it was
built; the mechanism is what this file is for.

**One has now left it.** *You will under-vary your marks* is in `PAINTING.md` rather
than on the front page since 0.3.0, because the check names both halves of it after the
pass that did it, with the numbers attached, which the paragraph could not do. It was
moved because the eighth session's two front-page items had nowhere else to come from —
which is the mechanism working as designed rather than a tidy-up. It is still a
hypothesis, and the shape of the test has not changed: a fresh session painting from a
guide with the rule missing. What has changed is that such a guide now exists.

**A fourth session scored its own painting against the candidates and three of the five
would have caught something it did.** It proposed a sixth — *a mass laid solid whose
planned and rendered values differ by more than the `0.10` that separates two masses* —
and that one was **not built**: measuring the gap first found it to be `0.000`, so the
check could never fire. Which is the general rule for this list. A check earns its line
by firing on a real pass of a real painting, and the cheapest way to find out is to
measure the condition before writing the rule, not after a painter reports the symptom.
The two rules the greenhouse painters added were both met by real passes — a pressure
list on a chisel, twice, in two paintings; a shaped mass laid at the default direction,
twice in one pass — and the log could not tell a pass of a mass from a mark laid by
hand until it was made to (`params["via"]`), which is the kind of thing a check needs
that prose never does.

The one form of the file idea with a real mechanism is **a short rules card kept where a
`CLAUDE.md` is kept**, which survives a context compaction where the guide does not.
That only matters for a session that actually gets compacted, and none of the four was,
so there is no evidence either way and it is not written.

### A new finding never adds a paragraph to the guide

It **replaces** an existing rule, **becomes a checklist line**, or **goes to
`CALIBRATION.md` or here**. The guide grew by roughly a paragraph per run — every finding
right, every one added — and went from 8,621 to 10,805 words across a single run's fixes.
No paragraph was wrong; the failure mode is that a fresh session reads the guide exactly
once, at the start, when it matters most, and the tenth run produces a guide nobody
finishes. The test for a candidate paragraph: strip the measurement and the reasoning out
and see what is left. If one line is left, that line is the rule and it goes in the guide,
and the measurement goes to `CALIBRATION.md`. If nothing is left, it was not a rule.

**That test bounds how fast the guide grows and it did not stop it growing.** The rule
was written when the guide was 8,600 words and the guide reached 17,000 under it, every
addition correct and none of them refused. A rule nothing enforces is a preference.

### The essay is finished at its size. Split by function; never cut

*Revised by the tenth round — see [One home per rule](#one-home-per-rule) below. The
split by function stayed; the "never cut" half did not survive a painter who had read
all of it and made the warned-against mistakes anyway.*

Three sessions each said the same two things about the guide and both are true: it is
long, and the essay is what made the rules stick. Every attempt to shrink it by editing
has failed, and the reason is not editorial skill — **the rule you would cut is the one
some painter needed.** Nor is the cost what it looks like: reading the guide, the
reference, the calibration file and two paintings' notes cost one session a few minutes
and about thirty thousand tokens, against far more spent looking at its own rehearsals.
The cost of length is that a rule read once at the start is not in the painter's hand
at the moment it applies, and cutting cannot fix that.

So the answer taken is **a file boundary rather than an instruction, and a move rather
than a cut**:

| | |
|---|---|
| [`PAINTER.md`](PAINTER.md) | the method — the order of work, *What you are bad at*, the checklist, the exercises. Held in the painter's head, and **held to a word budget by `tests/test_guide.py`** |
| [`PAINTING.md`](PAINTING.md) | the essay — colour, wet paint, the brushes, working from a reference, the rest of the API. Read once, after the exercises |
| [`RECIPES.md`](RECIPES.md) | the procedures — the calls in order for a kind of thing, with what it looks like when it goes wrong |
| [`REFERENCE.md`](REFERENCE.md) | the facts — units, defaults, every argument |
| [`CALIBRATION.md`](CALIBRATION.md) | the numbers |

Nothing was deleted in making that split; every word of the old guide is in one of the
first two files. **The standing rule from here on: a finding goes to the engine, to the
recipes, to the reference or to the calibration file. It never adds a paragraph to
`PAINTER.md`**, and if it must, something else in that file is cut in the same commit —
which the budget now forces rather than asks.

**The budget is 10,000 words and not the 5,000–6,000 a painter proposed.** That figure
was never costed against the contents the same list asked the file to keep: the order of
work, *What you are bad at*, the checklist and the exercises come to about 8,500 words
between them, so reaching 6,000 would mean cutting them, which every other item on that
list forbids. A budget that cannot be met on the day it is written enforces nothing.
The honest claim is halving, not fifthing: 17,600 words to 9,400.

**The best shrinking is still the engine absorbing a rule**, and that is the only kind
that has ever removed a paragraph outright: `solid=True` took the load warnings,
`scumble` took the gradient-tool warning, `cost_line` took the arithmetic, `cover` took
the burying recipe, and the inward scumble's own brush-size warning took a paragraph of
guidance about ring steps. **One engine change per paragraph, the paragraph leaving in
the same commit.**

**The split is a hypothesis, like every other guide change.** The test that would settle
it is two fresh sessions under the protocol below: one given only `PAINTER.md`,
`RECIPES.md` and `REFERENCE.md`, one given everything. The prediction, written down so
it can be wrong: the first paints the masses as well and improvises worse, because the
essay is where the judgement came from when no recipe existed. Nothing above depends on
the result except how firmly `PAINTING.md` is recommended.

### A worked example is an instruction, whatever the prose beside it says

A fresh session reads the code blocks as if they were the whole document, because to it
they nearly are. A silhouette recipe that laid a vertical column at every step was
followed exactly, three runs running, producing the combing the same guide warns about
elsewhere. The same applies to nouns, and **the two directions of that leak are not
equally visible**:

- A **subject** leaking *out* of the guide costs the unprompted stage. One run's estuary
  was, word for word, the back-to-front example, and two later sessions painted it
  unprompted. A wrong result, but one that announces itself to anyone reading both files.
- A **copy reference** leaking *in* costs the copy score and **hides**, because the only
  symptom is that the number improves. A guide that teaches depth order using the copy
  reference's own subject hands the painter the answer to the thing being measured. This
  happened while fixing a real defect and was caught by a human reading the diff, not by
  any criterion in the protocol.

So the guide names nothing that appears in a reference, and **a list is not a safe
substitute for a subject**: one depth rule ended "it holds for a boat, an archway, a
barrel, a hood, a cuff, a window reveal, a cave mouth", and six of six fresh sessions then
named an overturned rowing boat, three of them describing the picture as being about
seeing into the hull. Any list is a ranked list and its first item is the answer. Seven
things is a principle; one thing is an instruction. State the rule with a ratio, or with
nothing.

Grep the guide for the references' nouns before every run — and then **read the examples
end to end and name the subject yourself**, because the grep only catches words already
known to be in a reference. That check is two minutes and it is the only one that catches
a noun the guide invented. It has caught its own author: three leaks were introduced by
the very edits that wrote the rule down — and then four more, found by running the grep
while doing something else entirely, a year of runs after the rule was written. The
paintings in `paintings/` are references now, so their nouns are in the list: the guide
had picked up one painting's subject in three examples and two of its places in a
fourth.

**So where does an end-to-end example live?** A painter asked for one: the guide has
eight abstract exercises and no single small picture laid out in order, and sequencing
was the thing they were least sure of at the start — not which call to make but which to
make first. The answer taken is that `paintings/` **is** that example. Each painting has
its numbered pass scripts, its prelude, its notes and an export that re-runs byte for
byte, so the order is readable rather than reconstructed. A later session confirmed the
value from the other side: the pass-script convention and the prelude of masses as
functions came from reading them, and it said it would not have arrived at either from
the guide.

**For a year the trade was to hide them, and that was resolved the wrong way round.**
`README.md` pointed at `paintings/` and `PAINTER.md` deliberately did not, on the
grounds that a worked example leaks its subject — so the cost of hiding it was paid by
the painter who would have benefited most, and paid silently. **The
decide-then-read protocol dissolves it**: a painter who chose the subject before opening
the repository cannot be steered by a noun in a worked example, and one who has not
chosen can be. So the front page now points at them *with the condition attached* — if
you have decided what to paint, these are yours; if you have not, do not open them — and
`PAINTINGS.md` and `README.md` say the same thing in the same words. The condition is
the protocol, which makes it checkable rather than a matter of taste.

The no-nouns discipline inside the guide itself stays, because it is for the reader who
did not follow the protocol. `RECIPES.md` is written under it too: a recipe says what a
shape of paint *does*, never what it is *of*.

### Never change the engine while a measurement is running

Every session in a run paints against one engine, and fixes land after the last of them
exports. Otherwise the run measures a moving target and none of its numbers can be
compared with each other.

### Check the painters' numbers

A painter reporting on its own painting is not a measurement. Every figure in the run
write-ups was re-measured from the exported PNGs. They were mostly right and not entirely.

**Thirty claims have now been re-measured before anything was built on them, and eight
did not survive.** Three are recent — the `rough` ground that was not what a ripple
metric was reading, the `size` threshold that turned out to be a pixel threshold, and
the sampled spread whose two populations turned out to overlap. The first five are the
ones with the clearest shape: the clean contour that was supposed to spill less than a ragged fill,
the smudge said to fail on a slope (it fails on a *bend*), the rendered view said to lift
a solid mass off its planned value (it does not move it at all), the boundary said
to be left bare at `overhang=0` (it is the comb and the brush running dry, and the
*sides*, which `overhang` cannot touch, come back barer than the ends), and the sequence
of directions said to be priced at its steepest angle (it is priced at the *sum* of them
all, one whole pass per angle). The nine from the
greenhouse round all held, to the percentage point where a painter had taken a
number — and two of them had the *mechanism* wrong while the finding was right: the
pencil said to advance the random stream advances the log index, and the CLI undo said
to lose "the random stream or the wet layer" was losing the stream *and* five decimals
of every point in the saved log. A claim that comes with a probe is a claim that can be
wrong in a useful way.

**They have a shape.** Every one of the five was reported as *observed* — a rehearsal
showed the failure plainly, no number was taken, and the painter reasoned back to a
mechanism that sounded right. The failures were all real; the *causes* were invented, and
a cause invented from a real failure is the most convincing kind of wrong claim there is,
because the evidence for it is genuine. The two that carried a measurement both held.

**And the fifth was labelled by the painter who made it**, which is the best version of
this that has happened: the eighth session wrote *observed and offered as a guess, which
this page's own record suggests is the half most likely to be wrong* beside its own
mechanism, and its three measured costs reproduced to the stroke. **Ask every round to
label which half of each finding is measured and which is reasoned.** It costs the
painter one clause, it tells the re-measurement where to look first, and a session that
can draw the line is already doing the check's work.

So: **when a request names a mechanism, measure the mechanism and not the failure.** It
is cheap — the five above cost an afternoon between them — and it changes what gets
built. Four times now it has turned a requested warning into a requested *instrument*: nothing
was wrong with `sample()`'s number, and what the session actually lacked was a way to ask
it the question, which is now `sample(rendered=True)` and a label on `compare()`'s table.
A warning that cannot fire is worse than no warning, because it is read as a promise that
the condition is being watched for.

### The measurement can be right and the instrument still wrong

Two findings were tools that lied: `value_of` returned linear luminance while the
greyscale view showed sRGB, and the first attempt to measure a halftone screen measured
the height map's autocorrelation rather than the paint that landed. Before trusting a
number, check it against the picture the painter actually sees.

### A measurement is only as general as what it was taken over

Two of the eight failures above were neither observed nor guessed: they were *measured*,
every number reproduced, and the rule proposed on top of them was still wrong, because
the measurement was taken over too little. A threshold in `size` turned out to be a
threshold in pixels, because the table behind it came off one canvas. A spread that
separated two populations cleanly over four places on one painting stopped separating
them at 226 places over two — and the false alarms included the very call the proposed
remedy told painters to make.

**So when a request proposes a threshold, re-measure the same claim over more of the same
kind of thing before building on it.** It is cheap: both cases were settled by sweeping
every cell and every span of a painting rebuilt from its own committed passes, which is
an afternoon of compute and no judgement at all. And ask what the rule would say to a
painter *doing the right thing*, because a rule that fires hardest on the remedy it names
is worse than no rule.

### A measure that can be satisfied by damage is not measuring the thing

`compare()` averages a cell, so a bar of dark improves the cell it lands in whatever it
does to the picture. One painter laid exactly that, deliberately, in its last ten strokes
to move two cells inside tolerance, and led its own log with the admission: *"it reads as
tape, and I traded the picture for the number knowingly."* The answer was not a better
threshold but a second measurement no single mark can improve at the same time
(containment: the share of a mass's paint that lands where the reference has nothing like
it), plus a procedural rule — **the last ten strokes may not be value corrections** — that
costs nothing to enforce because the log carries the order.

### Build the tool that tells the painter the truth, then go and fix what it said

`compare()` gained an `unreachable` split — cells whose reference value is below anything
the palette can reach — because two sessions each spent about twenty-five strokes
discovering for themselves that the target was unmeetable. Then the palette's floor was
taken from `0.235` to `0.13` and the list is normally empty, which is the right end state
for a split like that.

### The check reads marks and measures the canvas. It does not judge an arrangement

0.6.0 moved more of the guide into the tool than every release before it together —
new things said at the call, three more findings after a pass, four standing
measurements of the canvas, and a closing checklist that answers its own measured
lines. The line it stops at is the one it stopped at when there was no check at all:
**every one of those is a number about a mark or a pixel.** A picture can pass all of
them and have quietly become a different picture, competently painted.

Two of the 0.5.0 cohort's findings are outside that line on purpose. *No linter catches
a stripe instead of a catch-light* — a recipe followed exactly and expressively wrong —
and the safe, frontal, centred composition five of seven painters stopped short inside.
The instrument for both is the painter's own sentence, `s.plan(why=...)`, quoted back by
`checklist()` at the end, and a human looking. Moving the line is not a measurement
problem; it is a different project.

---

## The protocol, if a run is ever repeated

The build is finished, so the brief that specified it is gone; this is the part of it that
is still live. A run measures the *guide*, not the engine.

A fresh session, given `PAINTER.md` and a reference photograph, produces a recognisable
copy in under 300 strokes without touching source code, then produces **two** paintings
with no prompt. All exports plus their time-lapses exist. The engine's author has not seen
the unprompted paintings before the human has.

- **Two references.** First an ordinary object — a mug on a table will do — and that run
  is the pass: the human recognises the object, `compare()` reports no cell on it more
  than `0.10` from the reference's value, and the painter can point to marks it rejected
  in `preview()` or `rehearse()` before painting them. Then a portrait, which is the
  measure of how far the tools reach rather than a pass: recognisable or not, and the
  write-up says which features got there.
- **The headline result is painted without `sketch(reference)`.** The pencil is the
  painter's own — sketch, look, adjust, then paint — and landmarks, preview and rehearsal
  are how it gets precision below a cell by its own seeing, which is the thing being
  measured. A run that starts from the machine-laid sketch is an assisted mode: worth
  running, reported separately, never the number that says whether the guide works.
- **Two unprompted paintings, and the second must not repeat the first's composition.**
  One is not a sample: 63% of thirty-two fresh sessions named the same subject — a
  rain-wet street at dusk — before opening the guide, so a single unprompted painting says
  almost nothing about the painter, the guide or the engine, and two runs read meaning
  into exactly that. The first is unconstrained. The second must differ in compositional
  structure and that is the *only* constraint — do not prescribe the remedy ("make one
  line-based and the other curve-based"), because that hands over the artistic decision
  the stage exists to observe. Constrain the repeat, not the remedy.
- **Every finished painting is signed.** After the last look, before the export: up to
  five marks noted `signature`, free of the stroke budget and charged in full past five so
  the exemption cannot be spent on painting. The painter chooses what the mark is; the
  guide says nothing about it. It is asked what it chose and why *at that point and never
  before*, because a mark chosen in order to be explained is a different thing from a mark
  chosen. A flourish, not a measurement — but it is the only place in the protocol where
  the painter puts something in a picture that is not of the picture.
- **A cohort of painters that are not this model is worth more than another run of it.**
  Seven installed `easel-paint` 0.5.0 from the package and were told only to install and
  paint — no reading list, no protocol, no subject. That produced more than any single
  run before it: nine failures the guide described and the tool could not see, eighteen
  bugs and API gaps, and a measured account of what a painter reads before the first
  mark, which is the thing no session that was handed a reading list could report. Two
  things to keep if it is run again. **Tell them nothing about what to read**, because
  then what they read is the measurement. And **a painter that cannot see images cannot
  do this**: the one in this cohort installed it, painted, and wrote *I can't see it ...
  so I'm trusting the tool*, which is the whole method's one requirement failing quietly.
  Its verdict was weighted accordingly, and the three front pages now say vision is
  required.
- **A painter told where to start reads what it likes, so record what it read.** The
  lighthouse handover, the first fresh session against the card and body 0.6.0 split
  the guide into, read five documents before its first mark — 194 KB, everything but
  `CALIBRATION.md` — though the card's first paragraph says to start after *The first
  hour*; it is the second painter in two rounds to read everything. It read three rules
  and broke them anyway, and rehearsals caught all three: *looking at rehearsals caught
  those, not reading*. Its instruction for whichever round does cut the documentation
  is the one to keep: **start with what the notices already say at the call.**
- **Stop running verbal naming probes.** Three attempts settled it: 0 of 8 sessions *name*
  water, 4 of 4 *paint* it. A verbal probe measures what a session says when interrupted.
  The finding they did produce is better than any tally — the estuary is not a subject
  this model picks, it is a world it puts things in: given a boat it beaches it on a
  mudflat, and told to break the structure it painted a pond seen from above.

Non-goals, unchanged: no GUI, no fluid simulation, no image-to-image or style transfer
anywhere in the pipeline (the point is that the strokes are *chosen*), not pixel art, not
vector.

---

## Engine decisions that are load-bearing

The six that make output look painted rather than generated — pigment mixing in K/S
space, spacing measured along travel, smoothed wobble, aperiodic tooth grain, the
per-stroke bristle comb, width following pressure — are in [`README.md`](README.md) under
*Design notes*, because they are what a reader needs to understand the engine at all.
These are the rest, which you need before changing it.

- **Strokes are seeded per stroke index**, not drawn from one running stream. That is what
  makes `replay()` exact, which is in turn what makes CLI undo possible without persisting
  snapshots. The canvas tooth and grain are derived from the seed, so a saved session does
  not store them.
- **The tooth gate's threshold is capped at the surface's own tooth ceiling.** Textures are
  all centred near 0.5 but span very different ranges, and an uncapped threshold climbs
  past the highest peak of the narrow ones — which is how a starved brush came to deposit
  *nothing* on linen and smooth while still marking rough. `tooth_ceiling()` in
  `canvas.py`.
- **Every mark records how much paint actually landed**, not how many dabs were stamped.
  Dabs are attempts: a stroke can stamp 278 dabs and change nothing, and before this there
  was no way — from the API or from the log — to tell that apart from a stroke that worked.
- **Graphite is a channel, and paint buries it by what landed, not what was aimed at.**
  `stamp()` does `sketch *= (1 - effective)` with the same per-dab alpha the colour blend
  uses, which gives the whole contract for free: coverage after `k` dabs of alpha `a` is
  `1 - (1-a)^k` and the graphite left is exactly `1 - coverage`. A dab the tooth refused
  leaves the drawing untouched, which is why an underdrawing survives a scumble. Graphite
  accumulates as a *maximum*, not a sum — dabs along a pencil line overlap almost
  completely and any additive rule turns the line into a solid bar within a few dabs.
- **`sketch_lines()` is derived from the log, not stored.** Pencil records accumulate,
  erase records clip; undo and replay are then right for free, because there is no second
  copy of the drawing to keep in step.
- **A rehearsal is seeded as the *next* strokes of the real painting**, so what you try on
  the scrap of canvas is what lands. The trial holds its own generator *object* carrying a
  copy of the session's stream state, which is how it can be both pixel-identical to the
  real call and unable to change the painting that follows. Strokes never needed this —
  they are seeded per index — but `block_in` and `sweep` take their pass wander from the
  running stream.
- **`preview`, `rehearse`, `cost` and `stroke` take the same argument shape.** A plan is a
  list of `stroke()` kwargs, so what was checked is what gets painted without being
  retyped. A plan that has to be rewritten between checking it and painting it is a plan
  that will drift.
- **`block_in` takes an angle, and the four named directions are frozen.** `direction=`
  accepts degrees or a sequence of them, but the horizontal / vertical / diagonal / cross
  branches are byte-for-byte what they were and dispatch happens before them. That is what
  let this land mid-milestone with golden images already stored: every existing painting
  replays identically, so no golden had to be regenerated and nobody had to decide by eye
  whether a mark had got better. **Add capability beside the old path, never through it.**
- **`prepare()` quantises in Oklab, then labels connected components, then merges the small
  ones.** Quantising straight to the target number of masses gives one area per *colour*,
  and a picture has more masses than colours — two separate things the same brown are two
  masses. The connected-components pass is what turns colours into places. Edge hardness is
  the Oklab gradient along a shared boundary, not the value gradient: a warm table against
  a cool wall at the same value is an edge the painter can see, and a value gradient calls
  it lost.
- **Drawing does not count as a stroke** (`History.UNPAINTED_KINDS`), because a painter
  charged for the underdrawing is a painter who skips it. The signature exemption is the
  other shape of the same idea and is per-*record*, capped at five, with everything past
  five charged — a cap that is not a cap can be spent on painting.
- **Region names are deliberately neutral** (`upper-band`, not `sky-band`), because the
  unprompted stage is meant to be unprompted.
- **Mixbox is an opt-in extra, not a dependency.** A better pigment model, but its
  reference implementation is CC BY-NC and this repo is MIT. `EASEL_DISABLE_MIXBOX=1`
  forces the built-in model.
- **What the painter knows and the engine cannot, the painter declares up front — and is
  then held to.** `Session(budget=)` was the first of these and `s.plan(...)` is the rest:
  the values, the place meant to be lightest, the subject's share, and the two standing
  rules that concede something only the painter can know (*unless the subject runs that
  way*, *there should be some ground showing*). It is deliberately **not** an `accept()`
  called after a warning has fired. A declaration made before painting is a thing the
  check can measure the canvas against and the painter can be wrong about, and it turns
  the rule into a number: *how much crosses the bars*, *how many places are painted as
  promised*. A suppression can only ever say *stop talking*, and a rule that can be
  switched off is a rule that gets switched off on the pass where it was right. The
  corollary is that a painter who declares nothing is not nagged for a plan: the
  declarations buy lines, and buying nothing is allowed.

---

## Traps

Each of these cost real time at least once.

1. **Look at `samples/brushes.png` after any engine change — and then paint something.**
   The sampler shows *isolated strokes at full load*: it was perfectly happy with a gate
   that silkscreened the canvas weave across every accumulated mass. Block-ins on top of
   block-ins are a different test. Keep a throwaway abstract script around for it.
2. **A golden failing is an instruction to look, not to regenerate.** The test writes
   `tests/golden/<case>.actual.png` beside the stored `<case>.png` and says how far apart
   they are. Open both. `python scripts/make_golden.py <case>` only after deciding the new
   marks are better. A golden regenerated without looking records that a mark changed and
   asserts that nobody minded, which is worse than having no golden at all.
3. **Assert on the canvas, not on the return value.** Both engine findings of one
   milestone were invisible from the API. Diff `canvas.rgb` either side of a stroke when
   you touch deposition.
4. **Anything linear in per-dab alpha cannot produce a persistent mixture.** If you are
   tuning a wet-blending coefficient and seeing no effect, this is why.
5. **Anything a mask is computed from has to be in its cache key.** The tip-mask cache was
   keyed on `ceil(radius)` while the mask used the exact radius, so what a script painted
   depended on what had run before it *in the same process*. If you add a parameter to
   `tip_mask`, add it to the key **and** quantise it before anything reads it.
6. **A canvas-mutating `Session` method must push an undo snapshot immediately before it
   touches the canvas, in the same method.** `undo()` pairs the top of the snapshot stack
   with the last log record on the assumption that the two always move together: `dry()`
   mutated and logged without snapshotting, so `undo(1)` after a `dry()` popped the
   *previous* action's snapshot while dropping only the `dry` record — correct-looking
   return value, canvas silently two steps back, and `replay()` from the intact log then
   disagreeing with the screen. Grep for `push_snapshot` in `session.py` before adding a
   new kind of mark.
7. **A record that carries a place has to carry the whole place.** A shape logged as its
   bounding box replays as a rectangle; a shape logged as *nothing* replays as the whole
   canvas. `dry` and `erase` log `shape` or `region`, and `_place_from_params` is the one
   place that reads either back.
8. **A tuned constant often encodes a *ratio*, not an absolute, so it moves when the thing
   it is relative to moves.** The mixing exponent was set to give white its real tinting
   strength, without recording strength *compared to what*; darkening the palette widened
   its value range and the same number quietly went from carrying a 50/50 white mix `0.235`
   of the way up that range to `0.158`. Write down the invariant you tuned a constant to
   hold, not just the value you landed on.
9. **An identity in floating point is a claim to be measured, not assumed.** Restoring a
   clipped colour by adding back `c - np.clip(c)` is exactly right on paper; the K/S round
   trip does not land on its own input, so the correction missed by a constant `1.7e-6`
   *in one direction* on every blend and a near-black leaked 23 levels over 5000 dabs. A
   single application looked perfect. Iterate a few thousand times and compare to the
   start.
10. **When a document explains a limit, check which layer imposes it.** Twice a guide
    passage stated a *palette* choice as an *engine* fact and was believed — the `0.23`
    value floor was the swatches, and "nothing in this engine reflects less than `0.01`"
    was the box's range. Both read as physics and both were furniture. The tell is a
    sentence telling the painter what is impossible; go and try it, because the fix for an
    engine limit and the fix for a palette choice are nothing alike.
11. **A workaround built around a defect has to come out when the defect is fixed, and its
    *documentation* is the part that gets left behind.** Grep for the *number* — not just
    the feature — when a limit moves.
12. **Normalised space is not isotropic, and `size` is measured against the long side.** A
    coordinate is a fraction of the *width* in x and of the *height* in y, so on a
    non-square canvas a step of `0.07` down is a different number of pixels from `0.07`
    across — while a brush at `size=0.07` is `0.07` of the long side whichever way it
    travels. `block_in` has always mixed the two and `sweep` follows it on purpose rather
    than introducing a second convention in one call. If this is ever made pixel-true,
    make both pixel-true in the same change and expect every golden to move.
13. **A self-intersecting outline is accepted.** `Polygon` checks for three distinct points
    and a non-zero area, not for simplicity, and everything downstream is even-odd, so a
    bow-tie fills as two triangles. `inset` is a mitre offset and can fold a spiky outline
    through itself, which is why it checks the result's area and centre and falls back to
    pulling the points toward the centre.
14. **Before concluding anything about what a painter chose, ask what it was offered — then
    go and measure it.** An early note asserted, from two paintings, that a painter given
    the guide "will paint a horizontal landscape". Thirty-two fresh sessions later: six of
    eight given the real guide named a street or an interior. What survived is smaller and
    more useful — no estuary appeared in sixteen samples without the guide's landscape
    words, and a painter told what the engine is *bad* at justifies its choice with
    horizontal bands six times in eight. A plausible story about a tool's influence is
    worth about as much as a plausible story about a bug.
15. **Do not write down that something shipped until the thing that ships it has run.**
    `CHANGELOG.md` said 0.5.0 was released on the day 0.5.0 was *cut*, and the tag push
    that would have made that true never happened — so for a day the file announced a
    version that was not on PyPI, and the next round was nearly cut as 0.6.0 over a
    number that was still free, which would have left a hole nothing could fill. The
    rule and what makes it enforceable are in `CHANGELOG.md`'s own header. The shape
    generalises past releases: **a record written in anticipation of a separate act is
    a record of an intention**, and the two are indistinguishable once the page is
    written.

Environment papercuts, for whoever loses ten minutes to one: `np.savez_compressed` appends
`.npz` to a path without it (save through an open file handle; there is a test).
`import easel.brush as b` gets the *function*, because `__init__` rebinds the name — use
`from easel.brush import ...`. `sin(pi)` is slightly negative in float32 and a negative
base with a fractional exponent is NaN. `np.cross` no longer takes 2-D vectors in numpy 2.
numpy rejects a float32 probability vector that misses 1.0 by an ulp, which a quarter of a
million squared distances comfortably does. Check what `import easel` actually resolves to
before trusting a measurement — an editable install can point at a stale copy of the repo.
The repo is LF (`.gitattributes`), even on a Windows checkout. Two builds of numpy can
round a mixture differently in the seventh decimal — `2.4e-7` in one blue channel of the
lighthouse handover's palette — and the wet blend carries it into the export: its
thirteen passes rebuild the log to the stroke on the machine that filed it, and the
export differs from the painter's in 729 of 786,432 pixels, each by one level — the kind
of noise the golden tests' `TOLERANCE` is there for. *Byte for byte* is a claim about one
machine; *to the stroke* is the one that travels.

---

## What is still open

**In the engine, with evidence.**

- ~~**`Session.load()` restores `out_dir` from the session file with no validation.**~~
  **Settled: it warns.** The round-trip is kept, because it is how `easel look p.easel`
  keeps writing to the same place across CLI invocations, and because the same field is
  what a painter legitimately sets with `--out-dir` when *creating* a session —
  rejecting it would break their setup to guard against a file they wrote themselves.
  What changed is that it is no longer silent: loading a session whose `out_dir` is
  neither in the working directory nor beside the session file now says so, once, and
  names the path it is about to write to. Two places count as unsurprising rather than
  one, because a warning that fires on almost every load is a warning nobody reads —
  looks sitting beside the painting is the normal arrangement, not a smuggled path.
- ~~**`undo()`'s fast snapshot path does not rewind `Session.rng`.**~~ **Settled**, once
  a painter measured it: `easel undo` drifted its working session 1.06% of the canvas
  from a clean rebuild. The granularity problem this entry described was real — a mass
  draws its wobble *between* the `stroke()` calls that push each snapshot, so a state
  taken per record is one draw past the undone mark — and the answer was to take the
  state once, at the start of the painting *call*, and write it on every record the
  call makes (`params["rng"]`). Undo restores it on both paths, and `replay(upto=)`
  puts the rebuilt session's stream where the kept painting stood. The other half of
  the drift was the log rounding its points to five decimals, so a replay from disk was
  never quite the painting; it is exact now. Both are in `CALIBRATION.md` under *The
  log, undo, and the stream*, with a test each.
- **Residual dab-frequency ripple** on `flat` and `knife` at large sizes. Much reduced, and
  at this level it reads as ridging from a loaded brush rather than machine stripes. Worth
  another pass if it ever reads as mechanical in a real painting.
- **`block_in` passes can read as parallel hatching.** Mitigated by per-pass wander, by
  alternating the travel direction of successive passes, by `direction="cross"`, and by the
  guide telling the painter to vary direction between passes. Varying the *pass axis*
  automatically is still worth trying.
- **About 200 ms per stroke** on a 1024×768 canvas — a minute for a 300-stroke painting.
  Acceptable, not fast. The hot path is the per-dab window blend.
- **`.easel` files are megabytes**, because the full float32 canvas is stored. Since replay
  is exact, a future format could store only the log and rebuild on load, trading file size
  for load time.

**Not yet reviewed.** The MCP server has never had an adversarial code review of its own.
What such a pass should aim at: `_place` and `_plan` in `easel/mcp_server.py`, the only
code in the repo that turns untyped JSON into engine objects, and the echoed Python beside
them — two defects were already found there by driving the tools rather than by reading
them. The engine itself is untouched by that milestone.

**About the protocol, if it is run again.** Five questions now, and none has been
decided. The last two came out of the ninth session, which was the first to be handed
[`DIAGNOSIS.md`](DIAGNOSIS.md):

- **Record whether the painter used the index, now that using it is one command.**
  `DIAGNOSIS.md` opens with *this file is not for reading* and used to name
  `grep -i rings DIAGNOSIS.md` as the intended interface. The one session that has
  had it was told to read it front to back, and it then worked entirely from recall:
  it recognised *staircase*, *venetian blind*, *floating discs*, *searchlight that
  owns the picture* and *paper cut-out* on sight and repaired each from the
  remembered description, **following zero pointers in 293 strokes** though following
  them was permitted. The recalled version has no measurement attached, which is the
  whole difference between the index and its targets: the one fault it fixed
  properly, the chisel staircase, it fixed with `edge="clean"` while `CALIBRATION.md`
  holds a cheaper repair at the other end of the same row.

  **That was n=1, so the file did not change; what changed is the price of following
  a pointer.** `easel diagnose <what you can see>` matches the rows and prints the
  passage, which is the grep and the open-the-file-and-find-the-heading in one call —
  and the index now ships in the wheel, which it did not when the grep arm was
  proposed, so a painter who installed the package had nothing to grep at all. The
  question the arm was meant to settle is therefore no longer *grep or read*. It is
  **whether a painter reaches for it unprompted at the moment they are stuck**, which
  is what the recall failure above was really about, and the next run should say
  whether the command was in the instructions and how often it was called.

  **One run has said so since.** The lighthouse handover read the documents that name
  both commands and called neither `easel diagnose` nor `easel explain` in 171 marks —
  *the one-line notices were enough*. That is the answer 0.6.0 said to wait for before
  linking a notice's code to its `DIAGNOSIS.md` row, and the link is not built, on the
  evidence. n=1 again.
- **Decide whether a restricted arm gets the index at all, and record it.** Four of
  the rows most relevant to a painter without the essay point into files that arm
  does not have — *two masses you planned as different that read as one* lands in
  `PAINTING.md` → *Painting without a reference*, which is that session's own worst
  fault. **A pointer into a file you were not given is worse than no row**, because
  the answer is visibly there and out of reach. Either ship the index only with the
  files it indexes, or say in the run's own instructions which files the painter has,
  so a row naming one they do not have reads as a prerequisite rather than as a
  destination. This is a property of the run, not of the file.

And three that were already here:

- **The unprompted stage should probably become "chosen before the guide is read".** Four
  of four sessions painted the subject they had named before reading anything, and their
  median structure score was `+0.53` against a baseline where all six first unprompted
  paintings sit between `+8.12` and `+23.83`. That is a different measurement and a better
  one: it measures what the painter chooses rather than what the guide retrieves.

  **But deciding first measures the prior, not the painter, and the lever for that is
  order rather than content.** Across the four decide-then-read runs, the two asked cold
  produced the most-painted subjects in the corpus; the one given a single sentence of
  resistance produced a memory instead. The default is one instruction deep. So if the
  stage is meant to test the painter, ask for *two* subjects and paint the second, or
  ask it to name the obvious choice and then not paint that — both are nudges away from
  the default rather than toward anything, which is the property a named subject lacks.
  **Whichever was used has to be recorded with the run**, because the four above are not
  comparable with each other and nothing says so on their face.
- **The structure probe is partly measuring "has a sky".** It is the variance of the row
  means over the variance of the column means, so it cannot separate a smooth vertical
  gradient from a stack of slabs: a three-step gradient with its joins smudged scores
  `+32.3`, a field of overlapping scumbles at close values `+38.2`. The edge shares beside
  it are the half that discriminates, and a human looking is still the verdict.
- **The value criterion is saturated.** Worst cell on the last three copies: `0.0985`,
  `0.0961`, `0.0987`, against a `0.10` threshold. Three different painters cleared it by a
  thousandth, and on all three runs containment caught a defect it could not see.

**In the guide.** The depth-order paragraph has now failed three runs — containment
`17.5%`, `16.3%`, `13.2%` against a best of `0.1%` — and stating the rule, giving it a
runnable three-mass example *and* putting it in the closing checklist has been shown not to
be sufficient. It needs a rewrite, and that is a design job with a measurement attached
rather than an edit.

**Narrowed in 0.6.0, and not closed.** `report()` now says when a pass took earlier
details out of sight: three or more marks that stood `0.05` off what is round them and
were left under half of that, with a film or the passes of a mass over them. That is the
part of this item a check can see, and over the corpus it fires on 2 of 325 painted
passes, both of them burials. What it cannot see is a burial spread over passes — the
one a painter wrote down went `0.035` to `0.009` under three films and never by half in
any one of them, and catching that needs a memory of each detail's contrast in the saved
file, which this round declined. And the three copy runs whose containment numbers
define the item are not in this repository, so the check has never been run on the
evidence. So the paragraph still wants its rewrite; what changed is that the failure is
visible at the moment it happens in one pass.

Everything else the runs found has been applied.
[`SUGGESTIONS.md`](SUGGESTIONS.md) holds the lists from thirteen painting sessions and
the synthesis across them, and **every item is now done** — seventy-two for the engine,
ninety for the documentation — each with a note saying what it became. The 0.5.0
cohort's round is filed there too, seven painters that are not this model, and no row of
it is blank either; nor is one of the lighthouse handover's, the first painting against
0.6.0, whose ten items were done in 0.7.0.

That is not the same as those items being *right*. Every engine change has a test and a
measurement behind it; every guide change is a hypothesis until a fresh session paints
against one. The ones most worth watching are the ones that changed how the guide is
*read* rather than what it says: **the split into five files**, the exercises stated as
a gate with the cost of skipping them, *rehearse everything* replacing *rehearse what
you would not want to repaint*, and the closing checklist now asking for the subject's
share of strokes as a number rather than as a question. If the next fresh session still
skips the exercises, or still stops with a third of its budget unspent, that is the
finding — and repeating the instruction louder is not the fix, see *Warning is not
method*.

**One data point on the two-goes instruction exists and it is not a clean one.** The
third session read the whole guide *and* the reference before doing the exercises, then
did all eight, then painted — the wrong order, and the exercises still paid: the edge
study showed it the smudge's thumbprint before it could lay one in the picture, the load
study showed it the speckle a starved bristle leaves, and the wet-versus-dry pair is why
every later pass went on dry paint. **So the gate held even when the reading ran past
it**, which is an argument for the exercises and says nothing either way about the
order. Whether the essay gets finished by a painter who does the exercises first is
still unmeasured; it is now a file boundary rather than an instruction, which is the
thing to test.

Three of those lists' own measured claims were re-measured before anything was written
down on them, and two did not survive it. That is the method working as intended.

- The first reported that a contour pass swept along a shape's drawn outline "lays
  nothing outside the outline"; a pass centred on a line puts half its width either
  side of it, and measured on a mass a third of the canvas across it spilled 38px
  against the ragged fill's 20px. Sweeping the contour along the *inset* outline — so the brush's outer
  half lands on the drawn line — reaches 13px, and that is what `edge="clean"` does.
- The second reported that a two-point smudge on a *sloping* boundary moves it five
  times as far as one given four points along the slope. On a straight slope the two
  are the same pass to the pixel — the spline through collinear points is the line —
  so that number cannot have come from a slope. On a boundary that **bends** the
  effect is real and larger: mean `0.51%` of canvas height against `0.01%`. The rule
  survived its evidence and got sharper: *only a straight boundary is two points*.
- The one that held is the same session's solid mass, and it came back nine times
  more even rather than fourteen — a differently sized mass, measured in the values
  view rather than however they measured it. The claim was right and its ratio was
  the instrument's, which is the usual shape of a re-measurement that passes.

**Check the painters' numbers** applies to a painter's numbers about the engine, not
only to the engine's about itself — and a claim that survives the check is usually
worth more afterwards, because the re-measurement says what it is really about.

---

## One home per rule

The tenth session read every file in the corpus before painting, painted a picture of
its own choosing in 297 strokes, and was then asked what it would change about the
documentation. Its answer, and what was done about it:

- **The length was structural, not editorial.** Five files split by kind of content each
  restated their neighbours to stand alone, so one rule lived in up to six places: *paint
  masses, never up to a line* in six, *vary the direction of marks* in six, *paint over,
  never undo* in five, the rehearsal rule and the smudge numbers in four each. And
  `PAINTER.md` held itself three times: a first-hour summary, a body, and a checklist
  that restated the body as questions.
- **The stories were most of the words**, and they did not do what the corpus believed.
  This painter read every warning and still laid its thin members three times too heavy
  and its shadows as a fan of same-width rays; what caught both was a rehearsal looked
  at and the line `easel run` printed after the pass. That is the *warning is not
  method* finding above, arriving from a session that had read the whole essay.
- **So the essay's cost was real and its benefit smaller than believed**, and the
  standing rule above — split by function, never cut — was revised: split by function
  *and* state each rule once. `PAINTER.md` is now a card and a body (9,973 words to
  6,441), with the drawing as step 1 of the order in its own right; `RECIPES.md` holds
  the situations, each with its number; `PAINTING.md` holds
  the engine's behaviour with the photograph material in a skippable last chapter;
  `CALIBRATION.md` indexes each rule to its measurement and holds the painters' own
  reported counts in a section of their own, labelled as reports. `scripts/check_guide_overlap.py`
  says whether a sentence has crept into two files.
- **One thing was added rather than moved**: a recipe for a scene of straight edges,
  because three painters had each built a projection helper from nothing and the guide
  had no paragraph on it.

**This is a hypothesis, like every guide change**, and the test is the one this file
already names: a fresh session painting against the shorter corpus and then being read.
The prediction, written down so it can be wrong: the value structure and the depth
order hold as well as before, because those rules were never the ones painters
violated; the mistakes painters make — the ones with a check behind them — are made at
the same rate, because the prose never prevented them; and the session reaches its
subject earlier, because it spent less of its first hour reading. If the shorter
corpus produces a painter that skips the exercises or paints boxes for backgrounds at a
higher rate, the cut went too far and the row above says where the words went.

**The lighthouse handover did not spend less of its first hour reading**: told by the
card where to start, it read everything anyway (*a painter told where to start reads what
it likes*, in the protocol above). One data point against the prediction's last clause.

## The milestones, as a key

Source comments, test docstrings and `CALIBRATION.md` date things by milestone — *"before
M6b the palette floored at `0.23`"*, *"bumped to 3 by M8"*. The brief that named them is
gone, so this is what the names mean. They also head most of the commits.

| | |
|---|---|
| **M1** | Canvas, round brush, strokes, `look()`, PNG export, seed, the brush sampler. |
| **M2** | Flat and bristle tips, paint load and run-out, canvas texture, wet blending, `dry()`, pigment mixing, palette. |
| **M3** | Regions, grid, relative placement, `block_in`, values view, side-by-side, diff, history and time-lapse. |
| **M4** | The CLI and `PAINTER.md`. |
| **M5** | The first rehearsal: paint a reference from the guide alone, twice, the second time with a fresh session. |
| **M6** | Precision below a grid cell: golden images, matching crops, `preview`, landmarks, `compare`, `prepare`, the pencil, the liner, `rehearse`. |
| **M6b** | Darkened the dark pigments from colour-chart brights to masstones. The palette's floor went `0.235` → `0.13`, which moved every golden. |
| **M6c** | `sweep()` — a mass laid as passes along its own boundary, stepped inward. |
| **M7** | Marks at detail scale: the comb drawn per stroke, a bristle with a width of its own, width following pressure on the round tips. |
| **M8** | Masses that are not rectangles: `Polygon` beside `Region`, and `block_in` cutting each pass against the outline. |
| **M8b** | Took the Kubelka-Munk reflectance floor off the *answer*, leaving it on the arithmetic. |
| **M9** | The MCP server. Nothing in the engine changed. |

M6, M8 and M8b landed before M9 on one rule: **anything that changes the API lands before
the thing that exposes it.**

---

## Verifying a change

```bash
pytest -q                              # 1604 passed with the mcp extra installed;
                                       # the mcp and mixbox tests skip without theirs
ruff check src tests scripts examples mcpb
python scripts/check_guide_blocks.py   # every python block in the guide's three
                                       # files runs (72 ok, 10 pseudo-code), the
                                       # 19 demos fail as they say, and PAINTER.md
                                       # is inside its word budget
python scripts/make_brush_sampler.py   # then LOOK at samples/brushes.png
python scripts/make_shape_sampler.py   # and at samples/shapes.png
python examples/exercises.py           # the guide's warm-ups, writes out/ex_*.png
```

The first two are what CI runs, and `tests/test_guide.py` carries the word budget so
that half of the third is enforced there too. The last four are the ones that have
actually found things.
