"""The closing checklist as output, and the standing lines it is made of.

`PAINTER.md` has always ended with a list of questions to ask a finished painting,
and until 0.6.0 every one of them was a question a painter answered by looking.
Three cohorts running showed what that costs: the questions that have a *number*
behind them were the ones answered wrongly, because looking afresh is exactly what
a painter who has been staring at the canvas for four hours cannot do. One painter
finished a picture planned around a warm ground and then built the bare canvas by
hand to discover the ground was 0.07% of it; five of six in the next cohort stopped
with well over a third of the budget unspent.

So the measured lines answer themselves. Each is **a number, its scale, and -- where
a threshold is a judgement rather than an arithmetic fact -- the threshold said out
loud**, because a line that hides its judgement is a line a painter cannot disagree
with. `values:` says *under 0.10 apart reads as one mass* rather than quietly
calling a picture flat.

**Three questions are not here, and that is the boundary.** *Why did you choose this
subject*, *is the thing you measured most carefully still attached*, and *which
passage is the weakest* are the ones nothing in this file can ask: the check reads
marks and measures pixels, and every line below is one or the other.
:meth:`~easel.session.Session.checklist` prints those three as questions with the
painter's own ``why`` quoted back, which is the whole of what an instrument can do
for them. `LESSONS.md` and :meth:`~easel.session.Session.report` both say *the check
cannot see a composition*; this module is written to keep that true while taking
everything else off the painter's hands.

Every threshold here is calibrated on the 21 finished paintings of the corpus and
their own notes, which say which pictures have which fault -- `CALIBRATION.md`,
*The measurement lines, on the finished canvases*.
"""

from __future__ import annotations

import json

import numpy as np

from easel.measure import VALUE_THRESHOLD

__all__ = ["values_line", "edges_line", "pencil_line", "boxes_line", "unspent_line",
           "clusters", "mass_counts", "HARD_EDGE_PX", "PENCIL_STEP", "UNSPENT_SHARE"]

#: An edge narrower than this reads as hard. **Not two pixels**, which is where the
#: plan's prototype put it and is the one number in workstream E that had to move:
#: the sharpest transition a pixel grid can hold measures ``2.0`` exactly -- a step
#: from one value to another across one pixel has a central-difference gradient of
#: half the step, so the rise is ``step / (step/2)`` -- and a threshold sitting *on*
#: that limit is a coin flip. Measured on four canvases painted for the purpose, the
#: prototype called a hard-edged mass ``41%`` hard and a ragged comb ``84%``, which
#: is the wrong way round and is float dust either side of ``2.0`` rather than a
#: measurement. At ``2.5`` the same four sit at 49%, 49%, 53% and **0%** -- the one
#: at zero being the soft round brush, which is the only one of the four a painter
#: would call soft.
#:
#: Finding 13 is the share under it: GPT's own verdict on its picture names *equally
#: crisp boundaries*, and `DIAGNOSIS.md`'s clip-art row is the same fault reached
#: from the other side. Replayed over the 21 paintings of the corpus, the share runs
#: **21%-62%, median 37%**, and the two painters who named flat cut-out shapes as
#: their picture's main fault laid the hardest edges of them but one -- Grok's at 62%,
#: GPT's at 54% (`CALIBRATION.md`, *The `edges:` row, measured twice*). The 12%-44%
#: first published there was the prototype's, and described nothing.
HARD_EDGE_PX = 2.5

#: How far a pixel has to move when the graphite is composited in before it counts as
#: pencil showing. Two levels of 255: under that the drawing is beneath enough paint
#: to be the good kind of showing through, which the checklist explicitly wants kept.
PENCIL_STEP = 2

#: A painter who stops with this much of the budget unspent has left the picture
#: short without deciding to (finding 15). Five of the six budgeted paintings in the
#: 0.5.0 cohort stopped under 45% spent, at a median of 42%; **none of the thirteen
#: budgeted paintings before them did**, at a median of 86%.
UNSPENT_SHARE = 0.33


def clusters(flat: np.ndarray, k: int = 3, rounds: int = 25) -> np.ndarray:
    """Lloyd's algorithm on one dimension: cheap, and it is only ever three clusters.

    Seeded at evenly-spaced percentiles rather than at random, so the same canvas
    always returns the same three numbers. A measurement that moved between two calls
    on an unchanged picture would be worse than no measurement.

    Args:
        flat: the values to cluster, already flattened and thinned.
        k: how many clusters. Three, because the question is *light, mid and dark*.
        rounds: the iteration ceiling. It converges well under this on a canvas.

    Returns:
        The cluster centres, ascending.
    """
    centres = np.percentile(flat, np.linspace(100 / (k + 1), 100 * k / (k + 1), k))
    for _ in range(rounds):
        which = np.abs(flat[:, None] - centres[None, :]).argmin(axis=1)
        moved = np.array([flat[which == i].mean() if np.any(which == i) else centres[i]
                          for i in range(k)])
        if np.allclose(moved, centres, atol=1e-4):
            break
        centres = moved
    return np.sort(centres)


def values_line(view: np.ndarray, reach: tuple[float, float] | None = None,
                key: str = "", light: tuple[str, float, float] | None = None) -> str:
    """Where the picture's values sit, against what the box can reach.

    The checklist asks *does the greyscale view have a clear light, mid and dark*.
    The answer is the 5th to 95th percentile of the values view -- the range the
    picture actually occupies, with the few brightest and darkest pixels trimmed so
    that one signature stroke of white does not report a light the picture has not
    got -- and the three clusters it splits into.

    **The judgement is the gap**, and it is :data:`~easel.measure.VALUE_THRESHOLD`:
    two masses closer than a tenth read as one mass, so three clusters inside
    ``0.10`` of each other are not a light, a mid and a dark, they are one value
    painted three times. The line prints the number and the threshold both, because
    a painter whose subject really is a fog bank should be able to read it and
    disagree.

    Evidence: the pier finished with no clear light at all; heron 1 had nothing light
    in it until stroke 217; the fogged glass's two largest areas came in ``0.008``
    apart (`CALIBRATION.md`).

    **Under a declared key** (``plan(key="low")`` or ``"high"``) the line asks the
    key's own question instead. A low-key picture is told it is low-key as planned
    while its top twentieth stays under the box's middle, and how far past it once it
    rises -- silent while kept, speaking when left, which is the shape the Bell-Warden
    asked for (its top twentieth ran ``0.28`` to ``0.38`` over 25 reports, never within
    ``0.16`` of the middle). ``"high"`` is the same the other way, on the bottom
    twentieth. **The clusters are printed and not judged**: a key compresses the range,
    and the corpus's low-key pictures hold their closest two clusters a median
    ``0.078`` apart against ``0.141`` on every other pass, so a fixed ``0.10`` would call
    61 of their 74 passes one mass -- the next *no clear light* -- and no scaled gap has
    been measured to replace it. Under ``"low"``, with a light named in the plan, the
    line asks whether it stands clear of the rest: its brightest twentieth against the
    brightest twentieth of the canvas outside it, by
    :data:`~easel.measure.VALUE_THRESHOLD`. On both plans of the 0.8.0 round the named
    light clears it by ``0.14`` to ``0.28`` from the pass that paints it on, and not
    before.

    Args:
        view: the canvas as values, ``0..1``, graphite excluded.
        reach: what the palette can reach, darkest and lightest, for the *of a box
            that reaches* clause. Omitted, the clause is left off, and so is a key's.
        key: the plan's ``key``, ``""``, ``"low"`` or ``"high"``. Any other word is
            no key.
        light: the named light under ``key="low"``, as ``(name, its brightest
            twentieth, the brightest twentieth of everything else)`` --
            :meth:`easel.plan.Plan.light_reading`.

    Returns:
        The line, e.g. ``values: 0.15-0.35 of a box that reaches 0.14-0.96, clusters
        at 0.19, 0.24, 0.29; no clear light -- ...``.
    """
    flat = np.asarray(view, dtype=np.float32).reshape(-1)[::17]
    low, high = float(np.percentile(flat, 5)), float(np.percentile(flat, 95))
    centres = clusters(flat)
    gaps = np.diff(centres)
    line = f"values: {low:.2f}-{high:.2f}"
    if reach is not None:
        line += f" of a box that reaches {reach[0]:.2f}-{reach[1]:.2f}"
    line += ", clusters at " + ", ".join(f"{c:.2f}" for c in centres)
    # **Two different faults, and they are not the same question.** A picture can
    # have three well-separated clusters and still have no light in it -- the pier
    # did -- because all three sit in the bottom third of what the box can reach.
    # So the range is asked against the box first, and the clusters only after: a
    # painter told *no clear light* when the picture is all light would stop reading
    # this line, which is exactly what `LESSONS.md` rule 2 is about.
    middle = None if reach is None else (reach[0] + reach[1]) / 2.0
    if key in ("low", "high") and middle is not None:
        return line + _key_clause(key, low, high, middle) + _light_clause(light)
    dark, unlit = (middle is not None and low > middle), (middle is not None
                                                          and high < middle)
    if middle is not None and (dark or unlit):
        missing = ("no clear light or dark" if dark and unlit
                   else ("no clear light" if unlit else "no clear dark"))
        side = (f"nothing above {high:.2f}" if unlit else f"nothing below {low:.2f}")
        line += f"; {missing} -- {side}, and the box's own middle is {middle:.2f}"
    elif float(min(gaps)) < VALUE_THRESHOLD:
        # Which pair, because the two send a painter to opposite ends of the
        # picture. The closest pair alone -- all the prototype printed -- says
        # neither.
        which = "top" if float(gaps[1]) <= float(gaps[0]) else "bottom"
        line += (f"; the {which} two clusters are {float(min(gaps)):.3f} apart, under "
                 f"{VALUE_THRESHOLD:.2f}, so they read as one mass")
    else:
        line += "; a clear light, mid and dark"
    return line


def _key_clause(key: str, low: float, high: float, middle: float) -> str:
    """What the ``values:`` line says of a declared key: kept, or left and by how much."""
    if key == "low":
        if high < middle:
            return (f"; low-key, as the plan says -- nothing above {high:.2f}, under "
                    f"the box's middle {middle:.2f}")
        return (f"; the plan says low-key, and its top twentieth has risen to "
                f"{high:.2f}, {high - middle:.2f} over the box's middle {middle:.2f}")
    if low > middle:
        return (f"; high-key, as the plan says -- nothing below {low:.2f}, over the "
                f"box's middle {middle:.2f}")
    return (f"; the plan says high-key, and its bottom twentieth has fallen to "
            f"{low:.2f}, {middle - low:.2f} under the box's middle {middle:.2f}")


def _light_clause(light: tuple[str, float, float] | None) -> str:
    """Whether the plan's named light stands clear of the rest, under ``key="low"``.

    Both numbers are said, because the rest's is not the line's own top twentieth: it
    is read outside the light's place, off the view the ``lightest:`` line reads.
    """
    if light is None:
        return ""
    name, bright, rest = light
    clear = bright - rest
    said = (f"{bright:.2f} at its brightest twentieth against {rest:.2f} for "
            f"everything else")
    if clear >= VALUE_THRESHOLD:
        return f"; {name} stands clear -- {said}, {clear:.2f} over"
    if abs(clear) < 0.005:
        return f"; {name} does not stand clear -- {said}, level with it"
    if clear >= 0:
        return (f"; {name} does not stand clear -- {said}, {clear:.2f} over, under "
                f"{VALUE_THRESHOLD:.2f}")
    return f"; {name} does not stand clear -- {said}, {-clear:.2f} under"


def edges_line(view: np.ndarray) -> str:
    """How the picture's edge length divides between hard and soft.

    The checklist asks *are the edges varied -- some hard, some soft, at least one
    lost*, and finding 13 is that :meth:`~easel.session.Session.report` said *nothing
    to report* over a picture whose every boundary was crisp. Nothing in the log can
    see it: an edge is made by what two neighbouring masses do to each other, not by
    either one's arguments, so this is measured off the canvas.

    The rise width is the step the edge crosses over how fast it crosses it -- the
    value range within four pixels either side of the gradient's own direction,
    divided by the gradient there.

    **Which pixels count is the whole measurement**, and it is where the prototype
    went wrong. Taking the top percentile of the gradient, as it did, guarantees a
    sample of the *sharpest* pixels the picture has, whatever picture it is: every
    canvas painted for the purpose came back between 1.5 and 2.1 px, because that is
    what the sharpest pixels of anything measure. So the pixels here are chosen two
    ways instead, and neither is a percentile:

    * **a ridge** -- the gradient is at least as large as the gradient a pixel either
      side of it along its own direction. That is an edge's crest, and it throws out
      both the canvas tooth, whose gradients are not ridges at this scale, and the
      broad interior gradation of a graded mass, which is a slope and has no crest;
    * **a step of at least** :data:`~easel.measure.VALUE_THRESHOLD` across it. Two
      masses closer than a tenth read as one mass, so a transition smaller than that
      is not a boundary between two things and has no business being called an edge.

    Timed on a 1024x768 canvas, this is about **145 ms**, which is the dearest of
    the four standing lines and rather less than one stroke of paint. It is paid once
    per :meth:`~easel.session.Session.report` and not once per mark.

    So this line reports a number rather than passing judgement on it. What the
    number separates is the genuinely soft passage -- a round soft brush at low
    density measures **0%** under :data:`HARD_EDGE_PX` -- from everything laid with a
    chisel, a comb or a scumble, which all sit near half. A picture whose edges are
    *all* narrow says so whatever produced them, which is the counterweight the plan
    this came from asks for against remedies that push toward cut-outs.

    Args:
        view: the canvas as values, ``0..1``, graphite excluded.
    """
    view = np.asarray(view, dtype=np.float32)
    dy, dx = np.gradient(view)
    grad = np.hypot(dx, dy)
    height, width = view.shape
    ux, uy = dx / np.maximum(grad, 1e-6), dy / np.maximum(grad, 1e-6)
    rows, cols = np.mgrid[0:height, 0:width]

    def along(field: np.ndarray, t: float, r=None, c=None):
        """``field``, sampled ``t`` pixels along each pixel's own gradient.

        Over the whole canvas, or over the ``(r, c)`` pixels alone. The ridge is
        found over the whole canvas -- two gathers -- and the nine-sample walk that
        measures the rise then runs over the ridge only, which is a few percent of
        the pixels. Walking the whole canvas nine times costs about 200 ms on a
        1024x768 canvas and this costs about 20.
        """
        gr, gc = (rows, cols) if r is None else (r, c)
        uyt, uxt = (uy, ux) if r is None else (uy[r, c], ux[r, c])
        return field[np.clip((gr + uyt * t).astype(int), 0, height - 1),
                     np.clip((gc + uxt * t).astype(int), 0, width - 1)]

    ridge = (grad >= along(grad, 1.0)) & (grad >= along(grad, -1.0)) & (grad > 1e-4)
    r, c = np.nonzero(ridge)
    if not len(r):
        return "edges: nothing with an edge yet"
    samples = np.stack([along(view, float(t), r, c) for t in np.arange(-4, 5)])
    step = samples.max(axis=0) - samples.min(axis=0)
    keep = step >= VALUE_THRESHOLD
    if not keep.any():
        return "edges: nothing with an edge yet"
    rise = np.clip(step[keep] / np.maximum(grad[r, c][keep], 1e-6), 0.5, 12.0)
    share = float((rise < HARD_EDGE_PX).mean())
    return (f"edges: {share:.0%} of edges are under {HARD_EDGE_PX:.1f} px wide, "
            f"median {float(np.median(rise)):.1f} px")


def pencil_line(with_sketch: np.ndarray, without: np.ndarray) -> str:
    """Graphite still showing, as a share of the canvas.

    The checklist's own question -- *is there pencil still showing where you did not
    mean it to* -- and the one line here whose right answer is not zero: a drawing
    showing through thin paint is a good thing and worth keeping, which is why this
    is a number and not a warning. :meth:`~easel.session.Session.erase` takes it out
    and ``export(path, sketch=False)`` hides all of it.

    Measured as the share of pixels the graphite moves at all, rather than as the
    share of the drawing still uncovered: what a painter sees is the canvas with the
    pencil on it against the same canvas without.

    Args:
        with_sketch: the canvas as 8-bit values, graphite composited in.
        without: the same canvas, graphite left out.
    """
    moved = np.abs(np.asarray(with_sketch, dtype=np.int16)
                   - np.asarray(without, dtype=np.int16)) > PENCIL_STEP
    return f"pencil: {float(moved.mean()):.2%} of the canvas still has graphite showing"


def mass_counts(records) -> tuple[int, int]:
    """How many mass calls the log holds, and how many were handed a rectangle.

    A mass is *many* records -- one per pass -- so counting records would report a
    wide band as thirty rectangles and a small shape as three. The log already
    carries what separates one call from the next: every record a call makes is
    stamped with the generator's state **as the call began** (see
    :meth:`~easel.session.Session._one_call`), which is one value for the whole call
    and a different one for the call after it. So a call is a consecutive run of
    records sharing a verb and that stamp, and this walks the log once counting the
    runs.

    Records written before 0.6.0 carry no ``boxed`` key and are counted as shapes,
    which is the honest answer: the log does not say, and guessing from the points
    would call every band-shaped polygon a box.

    Args:
        records: the log, in order. Marks laid by hand carry no ``via`` and are
            skipped -- a mass is what a mass verb laid.

    Returns:
        ``(boxed, masses)``.
    """
    boxed = masses = 0
    last = None
    for record in records:
        params = record.params or {}
        via = params.get("via")
        if not via or via == "replay":
            continue
        # Sorted, because a dict that came back from JSON may be in another order
        # than the one that went in, and two calls would then look like four.
        here = (via, json.dumps(params.get("rng"), sort_keys=True))
        if here == last:
            continue
        last = here
        masses += 1
        boxed += bool(params.get("boxed"))
    return boxed, masses


def boxes_line(boxed: int, masses: int) -> str:
    """The share of the masses laid in a rectangle rather than in a shape.

    The checklist asks *is any mass a rectangle that should have been a shape? Check
    the background hardest*, and it is the fault the fogged glass and the pier were
    both partly built out of. A rectangle is not wrong -- a window is a rectangle --
    so this counts rather than warns, and it repeats *check the background* because
    that is where the box nobody meant to lay always is.

    Args:
        boxed: how many mass calls were handed a region rather than a shape.
        masses: how many mass calls there were.
    """
    if not masses:
        return "boxes: no masses laid yet"
    return (f"boxes: {boxed} of {masses} masses were laid in a rectangle "
            f"({boxed / masses:.0%}) -- check the background hardest")


def unspent_line(spent: int, budget: int | None) -> str:
    """What is left of the budget, and the one instruction that goes with it.

    Finding 15, and the sharpest number the 0.5.0 cohort produced: five of its six
    budgeted paintings stopped under 45% of budget at a median of 42% spent, and
    **none of the thirteen budgeted paintings before them did**, at a median of 86%.
    Whatever that is, it is not a property of the engine -- so this line prints the
    number and names the job the strokes are for rather than warning about it.

    *Name the weakest passage* is the instruction, because the passage a painter
    would apologise for is the one that wants the marks and it is never the one they
    have most recently been enjoying. Naming it is the painter's, which is why this
    asks for it rather than printing it.

    Args:
        spent: marks charged against the budget so far.
        budget: the budget, or ``None`` for a painting that set none.
    """
    if budget is None:
        return f"unspent: no budget set; {spent} marks laid"
    left = max(0, int(budget) - int(spent))
    line = f"unspent: {left} of {budget} unspent ({left / budget:.0%})"
    if left / budget >= UNSPENT_SHARE:
        line += " -- name the weakest passage and spend them there"
    return line
