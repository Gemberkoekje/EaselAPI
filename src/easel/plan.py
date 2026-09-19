"""What a painter writes down before painting, held by the engine.

The guide has always told a painter to decide four things before the first mark: what
the picture is *for*, what value each place is going to be, which place is meant to be
the lightest thing in it, and how much of the budget the subject gets. Until 0.6.0
none of that existed anywhere the engine could see it, and one painter said so as
plainly as it can be said:

    Useful heuristics, but they're philosophy, not errors, and it doesn't know which.

That is the whole of this module. ``Session(budget=)`` was the first of these
declarations -- a number the painter writes down and the engine then holds them to --
and :class:`Plan` is the rest of them.

**What a declaration buys.** Each one turns a rule of thumb into arithmetic:

* ``values`` gives the post-pass check something to measure the canvas *against*. A
  plan compared on the empty canvas also answers the one question three rounds of
  painters skipped -- which two of these places are planned so close together that
  they will read as one where they meet.
* ``lightest`` names the place the picture is lit by, so *is the light the lightest
  thing in the picture* stops being a question a painter has to remember to ask.
* ``subject_share`` is the split the guide asks for in numbers. It was already a
  parameter of :meth:`~easel.session.Session.report`, and neither ``easel run`` nor
  the MCP ``run`` tool passed it, so a painter working from a shell had never once
  seen the comparison.
* ``bands="subject"`` answers the standing warning the corpus shows firing on one
  pass in seven: *a stack of bars unless the subject runs that way*. The warning
  cannot tell whether the subject runs that way and the painter can, so a declaration
  replaces the warning with the method's next question -- how much crosses them.
* ``ground="buried"`` does the same for the bare-ground floor, which five of seven
  painters in one cohort accepted by hand.
* ``why`` is the sentence the painting is for. Nothing measures it;
  :meth:`~easel.session.Session.checklist` quotes it back.

**A declaration, not an acknowledgement.** It is written up front and saved in the
``.easel`` file, rather than being an ``accept()`` called after a warning has fired.
The difference matters: a plan is a thing a painter can be held to and can be wrong
about, and the check says so either way. A suppression only ever says *stop talking*.

The plan lives **beside** ``history.records``, never in it -- a mark's texture is
seeded from its place in the log, so anything new that took an index would repaint
every painting made before it.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np

from easel.measure import VALUE_THRESHOLD
from easel.regions import Polygon, as_place, polygon

__all__ = ["Plan", "Planned", "BAND_WORDS", "GROUND_WORDS", "named_place",
           "planned"]

#: What ``bands=`` accepts. ``"subject"`` declares that the picture's own subject runs
#: in one direction, which is what the stack-of-bars warning concedes it cannot know.
BAND_WORDS = ("", "subject")

#: What ``ground=`` accepts. ``"showing"`` is the default expectation and the one the
#: closing checklist is written for; ``"buried"`` says this picture covers its ground
#: on purpose, which is what a graded field edge to edge does.
GROUND_WORDS = ("", "showing", "buried")


@dataclass(frozen=True)
class Planned:
    """One place a plan names: what it is called, its outline, the value promised.

    ``value`` is ``None`` for a place named for some other reason than its value --
    ``lightest=`` names a place and promises it nothing in particular.

    The outline rather than the region or the name the painter typed, because the plan
    is saved in the ``.easel`` file and read back by a later pass: a shape has points
    and a name, both of which survive JSON, and a ``blob(..., seed=3)`` rebuilt from
    its arguments would not be the same blob.
    """

    name: str
    outline: Polygon
    value: float | None = None

    def mean_value(self, value_view: np.ndarray) -> float:
        """What this place actually reads, over the canvas as it now stands.

        ``value_view`` is the whole canvas as values, 0..1, the way
        :func:`easel.measure.compare_plan` computes it -- passed in rather than taken,
        because every place in a plan reads the same view and building it per place is
        the same arithmetic over and over.
        """
        h, w = value_view.shape[:2]
        mask = self.outline.mask(w, h)
        if not mask.any():  # pragma: no cover - a place off-canvas raises at plan time
            return float("nan")
        return float(value_view[mask].mean())

    def to_json(self) -> dict:
        return {
            "name": self.name,
            # Exact rather than rounded, for the reason the log's own points are:
            # a shape rounded on the way to disk is a different shape coming back,
            # and the plan is compared against the one registered in the session.
            "points": [[float(x), float(y)] for x, y in self.outline.points],
            "value": None if self.value is None else float(self.value),
        }

    @classmethod
    def from_json(cls, data: dict) -> Planned:
        name = str(data.get("name", ""))
        points = [(float(x), float(y)) for x, y in data.get("points", ())]
        value = data.get("value")
        return cls(name=name, outline=polygon(points, name=name),
                   value=None if value is None else float(value))


def named_place(where, index: int = 0) -> tuple[str, Polygon]:
    """Whatever a painter hands a value plan, as a name and one closed outline.

    One home for it, because a value plan is written in two places that have to agree:
    :meth:`easel.session.Session.compare` takes ``{place: value}`` and so does
    :meth:`easel.session.Session.plan`, and a place that is called ``near_mass`` in
    one table and ``place 3`` in the other is two tables.

    The name is the place's own if it has one -- ``blob(cell('D5'),
    name='near_mass')`` -- then the shape's, then the string that was typed, and
    failing all three its position in the plan.
    """
    try:
        place = as_place(where)
    except (KeyError, ValueError) as exc:
        raise KeyError(
            f"{where!r} is not a place, so it cannot carry a planned value. "
            f"The keys of a value plan are places -- a cell like 'D5', a "
            f"span like 'C3:F6', a Region, or a shape. To see a name of your "
            f"own in the table, build the shape with one: "
            f"blob(cell('D5'), name='near_mass')."
        ) from exc
    poly = place if isinstance(place, Polygon) else polygon(place)
    name = (place.name or poly.name
            or (where if isinstance(where, str) else f"place {index + 1}"))
    return str(name), poly


def _named_only(where) -> Planned:
    """A place a plan names for some reason other than its value -- ``lightest=``."""
    name, poly = named_place(where)
    return Planned(name=name, outline=poly, value=None)


def planned(where, value, index: int = 0) -> Planned:
    """One entry of a value plan: the place named, and its value checked against the scale.

    Shared with :meth:`easel.session.Session.compare`, which takes the same
    ``{place: value}`` dict -- so a value out of range is refused in the same words
    whichever of the two was handed it, and there is one sentence to fix if the words are
    ever wrong.
    """
    name, poly = named_place(where, index)
    if value is None:
        raise ValueError(
            f"The plan gives {name!r} no value. A value plan is places and the values "
            f"you mean to paint them -- s.plan(values={{sky: 0.70}}) -- so a place with "
            f"nothing promised has nothing to check. To name a place for another reason, "
            f"that is what lightest= is."
        )
    number = float(value)
    if not 0.0 <= number <= 1.0:
        raise ValueError(
            f"The plan gives {name!r} a value of {number}, and a value runs "
            f"0..1 the way palette.value_of() reports it."
        )
    return Planned(name=name, outline=poly, value=number)


@dataclass(frozen=True)
class Plan:
    """What the painter wrote down, as the engine holds it. See :mod:`easel.plan`.

    Built by :meth:`easel.session.Session.plan` rather than directly: that is where
    the arguments are checked and where the plan is registered on the session.
    Frozen and comparable, so re-registering the same plan -- which a ``prelude.py``
    running before every pass does -- is a thing the engine can recognise and stay
    quiet about.
    """

    why: str = ""
    values: tuple[Planned, ...] = ()
    lightest: Planned | None = None
    subject_share: float | None = None
    bands: str = ""
    ground: str = ""

    @property
    def declared(self) -> bool:
        """Whether anything at all was declared. An empty plan is no plan."""
        return bool(self.why or self.values or self.lightest is not None
                    or self.subject_share is not None or self.bands or self.ground)

    def as_dict(self) -> dict:
        """The values as ``{place: value}``, which is what ``compare()`` takes.

        So a plan written once can be handed to
        :meth:`easel.session.Session.compare` unchanged -- ``s.compare(s.plan())``
        measures the canvas against the plan the session is holding, and writes the
        sheet. A plan that has to be retyped to be checked is a plan that drifts.
        """
        return {p.outline: float(p.value) for p in self.values if p.value is not None}

    # -- the lines the check prints ----------------------------------------------
    def value_line(self, value_view: np.ndarray,
                   threshold: float = VALUE_THRESHOLD) -> str:
        """One line: how many places are painted as promised, and which are not.

            plan: 5 of 6 places inside 0.10; halo +0.14

        The signed number is the canvas minus the plan, so ``+`` is lighter than
        promised. Worst first, three at most: the line is printed after every pass and
        a line that runs to six places is one nobody finishes reading.
        """
        if not self.values:
            return ""
        deltas = [(p, p.mean_value(value_view) - float(p.value)) for p in self.values
                  if p.value is not None]
        if not deltas:  # pragma: no cover - plan() refuses a values= entry with no value
            return ""
        out = sorted((pair for pair in deltas if abs(pair[1]) > threshold),
                     key=lambda pair: -abs(pair[1]))
        inside = len(deltas) - len(out)
        line = f"plan: {inside} of {len(deltas)} places inside {threshold:.2f}"
        if out:
            shown = "; ".join(f"{p.name} {delta:+.2f}" for p, delta in out[:3])
            more = f"; and {len(out) - 3} more" if len(out) > 3 else ""
            line += f"; {shown}{more}"
        return line

    def lightest_line(self, value_view: np.ndarray) -> str:
        """One line: whether the place meant to be lightest is the lightest.

            lightest: lamp reads 0.78, the lightest of the 4 places planned
            lightest: horizon reads 0.61 and lamp, the plan's own light, 0.48 -- 0.13 under

        The candidates are the plan's own places. Ranking them is the cheapest
        possible version of the question, and it is the version that can be answered
        at all: what the *canvas* holds that is lightest is a pixel, and a pixel is not
        a place.
        """
        if self.lightest is None:
            return ""
        others = [p for p in self.values if p.name != self.lightest.name]
        candidates = [self.lightest, *others]
        if len(candidates) < 2:
            # Nothing to rank it against. The declaration is still held -- checklist()
            # quotes it -- but a line saying one place reads what it reads is not a
            # measurement of anything.
            return ""
        read = {p.name: p.mean_value(value_view) for p in candidates}
        mine = read[self.lightest.name]
        top = max(candidates, key=lambda p: read[p.name])
        if top.name == self.lightest.name:
            return (f"lightest: {self.lightest.name} reads {mine:.2f}, the lightest "
                    f"of the {len(candidates)} places planned")
        return (f"lightest: {top.name} reads {read[top.name]:.2f} and "
                f"{self.lightest.name}, the plan's own light, {mine:.2f} -- "
                f"{read[top.name] - mine:.2f} under")

    # -- the pairs, asked on the empty canvas ------------------------------------
    def pairs(self, width: int, height: int, meet, threshold: float = VALUE_THRESHOLD):
        """Planned pairs closer than ``threshold``, with whether the two places meet.

        Returns ``(a, b, gap, meets)`` tuples, closest first, exactly as
        :attr:`easel.measure.Comparison.pairs` carries them -- so the plan and
        ``compare()`` answer this question in the same shape.

        ``meet`` is the test for two masks touching, handed in rather than imported:
        it is the session's, and the distance it allows is the session's canvas.
        """
        masks = {p.name: p.outline.mask(width, height) for p in self.values}
        return sorted(
            ((a.name, b.name, abs(float(a.value) - float(b.value)),
              meet(masks[a.name], masks[b.name]))
             for i, a in enumerate(self.values) if a.value is not None
             for b in self.values[i + 1:] if b.value is not None
             if abs(float(a.value) - float(b.value)) < threshold),
            key=lambda row: row[2],
        )

    def pairs_text(self, rows, threshold: float = VALUE_THRESHOLD) -> str:
        """The pairs as the lines ``plan`` prints, the ones that meet marked.

        Two masses closer than ``threshold`` read as one; that only *matters* where
        the two places actually meet, which is why the mark is the whole point of the
        table. One plan finished all-green with two places planned ``0.00`` apart, and
        they were the two that met.
        """
        if not rows:
            return f"no two planned places are inside {threshold:.2f} of each other"
        out = [f"planned pairs inside {threshold:.2f}:"]
        for a, b, gap, meets in rows:
            where = "and they meet" if meets else "but they never meet"
            out.append(f"  {a} / {b}: {gap:.2f} apart, {where}")
        return "\n".join(out)

    # -- the file -----------------------------------------------------------------
    def to_json(self) -> dict:
        """The plan as the ``.easel`` file holds it, under its own ``plan`` key."""
        return {
            "why": self.why,
            "values": [p.to_json() for p in self.values],
            "lightest": None if self.lightest is None else self.lightest.to_json(),
            "subject_share": self.subject_share,
            "bands": self.bands,
            "ground": self.ground,
        }

    @classmethod
    def from_json(cls, data) -> Plan:
        """A plan read back from a session file, or an empty one from anything else.

        Forgiving on purpose. The key is new in 0.6.0 and read with ``.get``, so a
        0.5.0 file simply has no plan; and a plan written by some later Easel with a
        field this build does not know about loads as the fields it does know, the way
        a notice whose code is unregistered is dropped rather than refused. A session
        file is a painting, and a painting should open.
        """
        if not isinstance(data, dict):
            return cls()
        share = data.get("subject_share")
        lightest = data.get("lightest")
        return cls(
            why=str(data.get("why", "")),
            values=tuple(Planned.from_json(p) for p in data.get("values", ())),
            lightest=None if lightest is None else Planned.from_json(lightest),
            subject_share=None if share is None else float(share),
            bands=str(data.get("bands", "")),
            ground=str(data.get("ground", "")),
        )

    def __str__(self) -> str:
        """The plan as a painter reads it back. ``print(s.plan(...))``."""
        if not self.declared:
            return "no plan registered"
        out = []
        if self.why:
            out.append(f'why: "{self.why}"')
        for p in self.values:
            out.append(f"  {p.name}: {float(p.value):.2f}")
        if self.lightest is not None:
            out.append(f"lightest: {self.lightest.name}")
        if self.subject_share is not None:
            out.append(f"subject: {self.subject_share:.0%} of the budget")
        if self.bands:
            out.append(f"bands: {self.bands}")
        if self.ground:
            out.append(f"ground: {self.ground}")
        return "\n".join(out)


def build(why=None, values=None, lightest=None, subject_share=None,
          bands=None, ground=None, onto: Plan | None = None) -> Plan:
    """A checked :class:`Plan`, or the one already registered with these fields changed.

    Every argument left off -- which is ``None``, not the empty version of itself --
    keeps what ``onto`` already declared, so a painter can add the lightest place to a
    plan written in a ``prelude.py`` without retyping its values. Passing the empty
    version *clears* that field: ``values={}``, ``bands=""``, ``lightest=""``.
    """
    base = onto if onto is not None else Plan()
    fields = {}
    if why is not None:
        fields["why"] = str(why)
    if values is not None:
        fields["values"] = tuple(
            planned(where, value, i) for i, (where, value) in enumerate(values.items())
        )
    if lightest is not None:
        cleared = isinstance(lightest, str) and not lightest
        fields["lightest"] = None if cleared else _named_only(lightest)
    if subject_share is not None:
        share = float(subject_share)
        if not 0.0 <= share <= 1.0:
            raise ValueError(
                f"plan(subject_share={subject_share!r}) is a share of the budget and "
                f"runs 0..1 -- 0.4 for the two fifths the guide asks for, not 40."
            )
        fields["subject_share"] = share
    if bands is not None:
        if bands not in BAND_WORDS:
            raise ValueError(
                f"plan(bands={bands!r}) says whether the picture's own subject runs "
                f"in one direction: the word is 'subject'. It is what the "
                f"stack-of-bars line concedes it cannot know."
            )
        fields["bands"] = str(bands)
    if ground is not None:
        if ground not in GROUND_WORDS:
            raise ValueError(
                f"plan(ground={ground!r}) is 'showing' -- some ground is meant to be "
                f"left breathing, which is the default expectation -- or 'buried', "
                f"which is what a graded field edge to edge does on purpose."
            )
        fields["ground"] = str(ground)
    return replace(base, **fields) if fields else base
