"""One channel for everything the engine says at the call.

Until 0.6.0 every call-time warning was a bare ``warnings.warn(str)`` from one of
twelve `_check_*` functions, two methods and three inline sites in `session.py`.
There was no class, no code and no collection, and that cost three things:

* **Nothing could be collected.** A pass laid twenty marks and said four things, and
  the only place they existed was the console's scrollback, interleaved with
  whatever else was on stderr.
* **An MCP painter never heard any of it.** `mcp_server.py` never touched
  `warnings`, and `_tool` converts exceptions only -- so for a painter working
  through the server "the tool warns you" was false for everything except
  `report()`, which is a string the tool returns.
* **The prose and the tool could drift apart with nothing to catch it.** A document
  saying *the call says so* was a promise no test could check, because there was no
  name for the thing being promised.

So each of them gets a **code** -- a short stable name like ``chisel-blank`` -- and
lands in :data:`NOTICES`, the registry `REFERENCE.md` is held against. A notice
carries its code, its text, what **kind** of thing it is, and **where** the reason
lives, which is what `easel explain <code>` prints.

**Fact or habit.** A *fact* is a number about what this call is going to do: the mark
lands nothing, the mass costs 3.9x its own axis, the value that comes back measures
neither of the two masses it averaged. A *habit* is a rule of thumb about the picture
that a painter can be right to break -- the comb floor a painting made of broken
glints tripped twenty-eight times and was right to ignore every time. The test is
`LESSONS.md`'s second rule: *ask what the rule says to a painter doing the right
thing*. If a painter doing the right thing can trip it, it is a habit. Facts print
first, because a painter reading one line should read that one.

`EaselWarning` subclasses `UserWarning` rather than replacing it: every
``pytest.warns(UserWarning, match=...)`` in the suite, and every painter's own
filter, goes on working, and ``str(notice)`` is still exactly the sentence it was
before there was a class at all.
"""

from __future__ import annotations

from dataclasses import dataclass

from easel import docs

__all__ = ["EaselWarning", "Notice", "NoticeSpec", "NOTICES", "KINDS", "MODES",
           "PassReport", "explain"]

#: The two kinds, in the order they are printed. A fact is a number about what this
#: call will do; a habit is a judgement about the picture that a painter may be right
#: to break. See the module docstring for the test that decides which a rule is.
KINDS = ("fact", "habit")


class EaselWarning(UserWarning):
    """A warning the engine gives at the call, carrying the code it is registered under.

    Subclasses `UserWarning` so that nothing which already filters, catches or
    asserts on the engine's warnings has to know this class exists. ``str()`` is the
    message and nothing else: the code, the kind and the reference to the reason ride
    as attributes, so a console that has always printed the sentence goes on printing
    the same sentence.
    """

    def __init__(self, text: str, code: str):
        super().__init__(text)
        self.code = code
        self.text = text

    @property
    def spec(self) -> NoticeSpec:
        return NOTICES[self.code]

    @property
    def kind(self) -> str:
        return self.spec.kind

    @property
    def where(self) -> tuple[str, str]:
        return self.spec.where


@dataclass(frozen=True)
class NoticeSpec:
    """One row of the registry: what a code is, and where its reason lives.

    ``about`` is the line that appears in `REFERENCE.md`'s *What the tool will tell
    you* table -- the fault named in one clause, not the message itself, which is
    written at the call with the painter's own numbers in it.

    ``where`` is ``(document, heading)``: a key of :data:`easel.docs.DOCUMENTS` and a
    heading line in that document, exactly as it is written there. It is checked by
    `tests/test_notices.py`, so renaming a heading in the guide breaks a test rather
    than quietly emptying `easel explain`.
    """

    code: str
    kind: str
    about: str
    where: tuple[str, str]

    @property
    def document(self) -> str:
        return self.where[0]

    @property
    def heading(self) -> str:
        """The heading's own words, without its ``#``s."""
        return self.where[1].lstrip("#").strip()


@dataclass(frozen=True)
class Notice:
    """One thing the engine said, kept beside the log rather than in it.

    Beside, because a mark's texture is seeded from its place in the log: anything
    that took an index would move every painting made before it. See
    :meth:`easel.session.Session._notify`.
    """

    code: str
    text: str

    @property
    def spec(self) -> NoticeSpec:
        return NOTICES[self.code]

    @property
    def kind(self) -> str:
        return self.spec.kind

    @property
    def where(self) -> tuple[str, str]:
        return self.spec.where

    def __str__(self) -> str:
        return self.text


#: How a pass was run, as a saved report says it: laid on the painting, laid on a
#: rehearsal copy, or worked out on a copy that lays no paint (``--count``).
MODES = ("painted", "rehearsed", "counted")


@dataclass(frozen=True)
class PassReport:
    """What one pass was told after it ran: the block ``easel run`` printed, kept.

    Saved in the ``.easel`` file beside the notices and never in the log, for the
    notices' reason -- and saved for a **rehearsed** pass as well, which commits
    nothing else. That is what keeping it is for. Both of the times a painter saw
    *graded passage laid too narrow* fire on marks that were not a passage, a
    rehearsal printed it, of a pass rewritten before it was committed; nothing in the
    file said the rule had fired at all, and the painter rebuilt both from its own
    transcript to show that it had.

    ``scripts`` is what ran, as the pass named it. ``mode`` is one of :data:`MODES`.
    ``at`` is the log index the pass began at, in the painting's own numbering, so
    ``s.replay(upto=at)`` is the canvas it opened on. ``text`` is the block itself:
    what was said at the calls, and then the check.
    """

    scripts: str
    mode: str
    at: int
    text: str

    def __str__(self) -> str:
        head = f"{self.mode} {self.scripts}, from record {self.at}:"
        return "\n".join([head] + [f"  {line}" for line in self.text.splitlines()])

    def to_json(self) -> dict:
        return {"scripts": self.scripts, "mode": self.mode, "at": self.at,
                "text": self.text}

    @classmethod
    def from_json(cls, data) -> PassReport | None:
        """One saved report, or ``None`` for an entry this build cannot read.

        Forgiving on purpose, as the plan's reader is: a file written by a later
        Easel may carry a mode this one does not know, which is kept as it is, and a
        damaged entry costs its own line and not the file.
        """
        if not isinstance(data, dict) or not isinstance(data.get("text"), str):
            return None
        try:
            at = int(data.get("at", 0))
        except (TypeError, ValueError):
            return None
        return cls(str(data.get("scripts", "")), str(data.get("mode", "")), at,
                   data["text"])


def saved(reports, last: int | None = None) -> str:
    """The saved reports as ``easel log --reports`` prints them: the last ``last``.

    Oldest first, as the notices are, so a rehearsal reads above the pass it became.
    """
    kept = list(reports)
    if not kept:
        return ("No pass reports saved. Every `easel run` keeps the block it prints "
                "after a pass here, rehearsed and counted passes included; a file "
                "saved by 0.6.0 or earlier has none.")
    shown = kept[-last:] if last is not None and last > 0 else kept
    head = (f"{len(kept)} pass report{'s' if len(kept) != 1 else ''} saved, oldest first"
            + (f"; the last {len(shown)}:" if len(shown) < len(kept) else ":"))
    return "\n\n".join([head] + [str(r) for r in shown])


def _spec(code: str, kind: str, about: str, document: str, heading: str) -> NoticeSpec:
    return NoticeSpec(code=code, kind=kind, about=about, where=(document, heading))


#: Every code the engine can say, and what each one is. The keys are stable: they are
#: printed after a pass, typed into `easel explain`, written into `REFERENCE.md` and
#: quoted in `SUGGESTIONS.md` when a painter reports one, so a code is renamed the way
#: a public function is renamed and not more often.
#:
#: `tests/test_notices.py` holds three things against this table: every code
#: `session.py` notifies is here, every code here is a row of `REFERENCE.md`, and
#: every `where` names a document that exists and a heading that is in it.
NOTICES: dict[str, NoticeSpec] = {
    spec.code: spec
    for spec in (
        # -- the budget, and plans ---------------------------------------------------
        _spec(
            "budget-spent", "fact",
            "a plan was priced against a budget that is already spent",
            "calibration", "## Budget",
        ),
        _spec(
            "budget-share", "fact",
            "a plan would eat more than its share of what is left of the budget",
            "calibration", "## Budget",
        ),
        _spec(
            "count-only", "fact",
            "a counted copy was asked something counting cannot answer",
            "painting", "## Try the mark before you spend it",
        ),
        _spec(
            "plan-pairs", "fact",
            "two places a plan puts closer than `0.10` meet on the canvas, so one will "
            "read as the other exactly where they join",
            "calibration", "## The plan a painter declares",
        ),
        # -- the brush, at the size it was given --------------------------------------
        _spec(
            "chisel-blank", "fact",
            "an oriented tip under four pixels wide lays no paint, and is charged for it",
            "calibration", "### What a solid mass actually lands at",
        ),
        _spec(
            "chisel-pressure", "fact",
            "a pressure list on a chisel tip changes the paint, not the width",
            "calibration", "## Pressure",
        ),
        _spec(
            "jitter-beads", "fact",
            "`jitter=` a multiple of its default, which comes out as width: a chain of "
            "beads rather than a line",
            "painting", "### Per-stroke overrides",
        ),
        # -- masses ------------------------------------------------------------------
        _spec(
            "direction-default", "fact",
            "a shaped `block_in` with `direction` left off, costing far more than its "
            "own axis",
            "calibration", "### A shaped mass with `direction` left off",
        ),
        _spec(
            "direction-sequence", "fact",
            "a sequence of directions is one whole pass per angle, and is charged the sum",
            "calibration", "### `direction` given a sequence",
        ),
        _spec(
            "chisel-staircase", "fact",
            "a chisel filling a mass along a straight side it runs nearly along: the "
            "pass ends step down that side instead of drawing it",
            "calibration", "### The chisel staircase",
        ),
        _spec(
            "spill", "fact",
            "a mass or a band whose passes will cover well over the place they were "
            "handed: the brush hangs past every pass, over whatever is beside it",
            "calibration", "### Paint that lands outside the place",
        ),
        _spec(
            "clean-small", "fact",
            "a clean edge whose brush is a large share of the place it fills, a shape "
            "or a region: the inset takes the mass rather than a rim off it",
            "calibration", "### A clean edge on a narrow mass",
        ),
        _spec(
            "clean-comb", "habit",
            "a clean edge drawn with a bristle, whose comb covers about three-quarters "
            "of its width",
            "calibration", "### The contour of a clean edge",
        ),
        _spec(
            "round-fringe", "fact",
            "a round tip blocking in a feature lays about half again the shape's area, "
            "and the fringe is the silhouette",
            "calibration", "### A clean edge on a narrow mass",
        ),
        _spec(
            "solid-comb", "fact",
            "a mass laid solid with a bristle: solid= closes the gaps along a pass "
            "and not the ones the comb leaves across it",
            "calibration", "### The holes a solid comb leaves",
        ),
        _spec(
            "holes", "fact",
            "what a mass laid solid actually came back with: the share of its own "
            "interior still showing ground, measured, and only where that reads",
            "calibration", "### The holes a solid comb leaves",
        ),
        _spec(
            "cover-comb", "fact",
            "`cover()` with a bristle does not bury: the comb leaves the old paint "
            "showing between the streaks at any opacity",
            "calibration", "## The bristle comb",
        ),
        # -- scumble -----------------------------------------------------------------
        _spec(
            "inward-comb", "habit",
            "an inward scumble laid with a bristle under the comb floor: four streaks "
            "with gaps rather than a brush",
            "calibration", "## The bristle comb",
        ),
        _spec(
            "inward-flat", "fact",
            "an inward scumble's brush wider than about three ring steps: the last rings "
            "bury the first and the middle comes back flat",
            "calibration", "## `scumble`",
        ),
        _spec(
            "scumble-bars", "fact",
            "a banded scumble whose passes do not overlap: bars with the ground showing "
            "between them",
            "calibration", "### The band, and the brush that closes its joins",
        ),
        _spec(
            "scumble-wedge", "fact",
            "a scumble across a shape whose width varies: no one brush is right for both "
            "ends, and the narrow end blooms",
            "calibration", "### The band across a wedge",
        ),
        _spec(
            "scumble-dabs", "fact",
            "a scumble whose every pass is shorter than the brush laying it: dabs, and "
            "the paint blooms past the outline",
            "calibration", "### The band across a wedge",
        ),
        # -- the other verbs ---------------------------------------------------------
        _spec(
            "smudge-across", "fact",
            "a smudge whose path crosses a boundary: it carries the first mass about a "
            "brush into the second, a thumbprint",
            "calibration", "### Across a boundary, and along a long one",
        ),
        _spec(
            "smudge-long", "habit",
            "a smudge run along a boundary for more than a tenth of the canvas: its "
            "strip reads as a third band, two edges where there was one",
            "calibration", "### Across a boundary, and along a long one",
        ),
        _spec(
            "smudge-wide", "habit",
            "a smudge past `0.02`, where one pass stops softening a join and starts "
            "dragging a lobe",
            "calibration", "## `smudge`",
        ),
        _spec(
            "glaze-far", "fact",
            "a film that moved the passage under it past what a film is for: a new mass "
            "in value, or a colour of its own in hue",
            "calibration", "### A film far from what it lands on",
        ),
        _spec(
            "glaze-nothing", "fact",
            "a film aimed at a value the paint under it already reads solves to no "
            "opacity, and still costs a stroke",
            "calibration", "### Aiming a film at a value",
        ),
        _spec(
            "sample-split", "fact",
            "`sample()` averaged two masses, so the value it returns is a measurement of "
            "neither",
            "painting", "## Colour",
        ),
        # -- the session file ---------------------------------------------------------
        _spec(
            "foreign-out-dir", "fact",
            "a loaded session file writes its looks somewhere that is neither the working "
            "directory nor beside the file",
            "reference", "## The session, and the shell",
        ),
    )
}


def collapse(said) -> list[tuple[Notice, int]]:
    """The notices to print: identical codes collapsed, facts before habits.

    A pass that blocks in nine masses with ``direction`` left off has said one thing
    nine times, and printing it nine times is how `LESSONS.md`'s seventh rule -- *a
    warning that fires on almost every pass is a warning nobody reads* -- gets broken
    by a channel rather than by a check. The first of each code is kept, because it
    is the one whose numbers a painter can go and look at; the count says how many
    calls were like it.

    Within a kind the order is the order they were said, which is the order the calls
    were made.
    """
    first: dict[str, Notice] = {}
    counts: dict[str, int] = {}
    for notice in said:
        first.setdefault(notice.code, notice)
        counts[notice.code] = counts.get(notice.code, 0) + 1
    ordered = sorted(first.values(), key=lambda n: KINDS.index(n.kind))
    return [(n, counts[n.code]) for n in ordered]


def lines(said) -> list[str]:
    """:func:`collapse` as the lines that go under the heading."""
    out = []
    for notice, count in collapse(said):
        calls = f" ({count} calls)" if count > 1 else ""
        out.append(f"  - {notice.code}{calls}: {notice.text}")
    return out


def block(said, check: str = "") -> str:
    """The pass's notices and its post-pass check, in one block.

    What is said **at the call** comes first and what is found **over the pass**
    second, because the first is about a call the painter can still change their mind
    about and the second is about paint that has landed. Both are printed by
    ``easel run`` and returned by the MCP server's `run`, so a painter gets the same
    words for the same pass whichever way the pass was run -- which was not true
    before 0.6.0, when the MCP path printed the check and dropped every warning.
    """
    said = list(said)
    parts = []
    if said:
        shown = lines(said)
        head = f"at the call, {len(shown)} thing{'s' if len(shown) != 1 else ''} said"
        parts.append("\n".join([head + ":"] + shown
                               + ["  (easel explain <code> for the measurement "
                                  "behind any of these)"]))
    if check:
        parts.append(check)
    return "\n".join(parts)


def explain(code: str) -> str:
    """The passage the reason for ``code`` lives in, with a line saying which it is.

    This is where the *why* goes when its paragraph leaves the reading path. A rule
    that moves out of `PAINTER.md` and into the engine does not lose its reason; the
    reason stops being read in advance and starts being delivered at the moment it
    applies, which is the one moment a painter is certain to want it.
    """
    try:
        spec = NOTICES[code]
    except KeyError:
        known = ", ".join(sorted(NOTICES))
        raise KeyError(
            f"unknown notice {code!r}. The engine says: {known}."
        ) from None
    passage = docs.section(spec.document, spec.where[1])
    where = f"{docs.DOCUMENTS[spec.document]}, {spec.heading}"
    return f"{spec.code} ({spec.kind}) -- {spec.about}\nThe measurement is in {where}.\n\n{passage}"
