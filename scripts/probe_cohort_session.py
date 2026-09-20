"""The measurements behind the 0.5.0 cohort's round -- step 2 of ``PLAN-0.6.0.md``.

Seven painters that are not Claude installed ``easel-paint`` 0.5.0, painted a picture
each and left a verdict. Their findings are filed as an open round in
``SUGGESTIONS.md``; the plan built on them proposes new checks, new measurement lines
and five moved defaults. **Every one of those is a candidate until this script has
measured it**, which is ``LESSONS.md``'s first rule and the reason step 2 comes before
every engine change in the round:

    Measure the condition before writing the rule. A check earns its line by firing
    on a real pass of a real painting.

So this script does three things, in this order:

1. **Rebuilds the corpus.** Every committed painting, from its own pass scripts, pass
   by pass, on the engine as it now is -- with every call watched. That
   gives the one thing no amount of reading gives: what a rule would have said, to a
   painter who was painting, at the moment they painted it.
2. **Re-measures the painters' claims** -- section 2a of the plan (the nine failures the
   documentation already names) and section 2d (the eighteen bugs), each against the
   code rather than against the verdict that reported it. Four of the reported
   mechanisms had already failed that test while the plan was being written; this is
   the runnable version, and it prints the *before* beside the *after* wherever the
   before can still be reproduced.
3. **Counts the candidates.** For every check in workstream D, every line in E and
   every default move in F: how often it fires over the corpus, on which passes, and
   whether it fires on a code block of the guide itself. Rule 2 -- *ask what the rule
   says to a painter doing the right thing* -- is the guide-block column, and a
   candidate that fires there is not narrowed but wrong.

The numbers it prints are the ones quoted in ``CALIBRATION.md``. **Its output decides
which rows of the plan survive**, so it is meant to be re-run and read, not trusted
from memory.

    python scripts/probe_cohort_session.py                # everything, about an hour
    python scripts/probe_cohort_session.py --list         # the corpus, and nothing else
    python scripts/probe_cohort_session.py --claims       # 2a and 2d, no corpus replay
    python scripts/probe_cohort_session.py --corpus       # the replay and its tables
    python scripts/probe_cohort_session.py --corpus --only kimi glm

**The rebuild is itself a measurement.** ``PAINTINGS.md`` claims a byte-for-byte
rebuild for some of these paintings and explicitly declines to for others; where a
painting rebuilds to the stroke count and subject share its own notes record, the
corpus numbers below are that painting. Where it does not, the run says so and the
painting still counts as passes -- a pass that cannot be rebuilt is still a pass a
painter wrote, and the noise budget is about how often a line is printed.
"""

from __future__ import annotations

import argparse
import contextlib
import importlib.util
import inspect
import io
import math
import os
import re
import shutil
import sys
import tempfile
import time
import warnings
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

import easel
import easel.session as session_module
from easel import Region, Session, polygon
from easel.color import linear_to_srgb
from easel.history import MAX_SNAPSHOTS
from easel.regions import Polygon

ROOT = Path(__file__).resolve().parents[1]
PAINTINGS = ROOT / "paintings"
OUT = ROOT / "out"


# -- the corpus ---------------------------------------------------------------------
#
# One entry per painting under `paintings/`, which is the same list `PAINTINGS.md`
# carries a section for and `tests/test_paintings.py` counts. The canvas arguments are
# that page's own `Canvas` row; `spent` is its `Spent` row, and is what the rebuild is
# checked against. A painting whose page says the rebuild is *not claimed* is marked
# so here rather than left out: its passes are still passes a painter wrote, and the
# noise budget is a question about how often a line gets printed, not about pixels.

_PASS_NAME = re.compile(r"^(?:p|pass)(\d+)([a-z]?)(?:_.*)?\.py$")


def _passes(folder: Path, first: tuple[str, ...] = ()) -> tuple[str, ...]:
    """The pass scripts in a painting's directory, in the order they were run.

    Every painter here numbered their passes -- ``p3_rocks.py``, ``pass04_bowl.py``,
    ``pass1b.py`` -- and the number is the order. Read off the directory rather than
    listed painting by painting so that a probe of a painting that gains a pass does
    not quietly measure the old one; ``first`` carries the handful of files that come
    before the numbering (GLM's free graphite ``draw.py``).

    What this deliberately leaves out is every file beside them that is not a pass:
    ``prelude.py`` and its helpers, and the painters' own ``check``, ``cost``,
    ``probe`` and ``crop`` scripts. Those ran between the passes and painted nothing,
    which is why none of the byte-for-byte rebuild claims counts them either.
    """
    found = []
    for path in sorted(folder.glob("*.py")):
        match = _PASS_NAME.match(path.name)
        if match:
            found.append(((int(match.group(1)), match.group(2)), path.name))
    return tuple(first) + tuple(name for _, name in sorted(found))


@dataclass(frozen=True)
class Painting:
    """One painting of the corpus, and how to build it again."""

    name: str                       # the handle `--only` takes
    where: str                      # under paintings/
    session: dict = field(default_factory=dict)
    first: tuple[str, ...] = ()     # pass scripts that come before the numbering
    driver: str = ""                # a painting written as one script, not as passes
    spent: int = 0                  # what PAINTINGS.md says it cost
    rebuilds: bool = True           # whether that page claims the scripts rebuild it
    cohort: bool = False            # one of the seven 0.5.0 verdicts this round is about

    @property
    def folder(self) -> Path:
        return PAINTINGS / self.where

    @property
    def passes(self) -> tuple[str, ...]:
        return () if self.driver else _passes(self.folder, self.first)


CORPUS = [
    Painting("car_wash", "Claude/car_wash", spent=206,
             session=dict(width=1152, height=720, texture="linen",
                          ground="umber_wash", seed=23, budget=300)),
    Painting("pears", "Claude/windowsill_pears", spent=224,
             session=dict(width=1024, height=768, texture="linen",
                          ground="toned_warm_grey", seed=11)),
    Painting("dusk", "Claude/lighthouse_dusk", spent=184,
             session=dict(width=1024, height=768, texture="linen",
                          ground="burnt_sienna", seed=31, budget=300)),
    Painting("laundromat", "Claude/laundromat_night", spent=286,
             session=dict(width=1024, height=768, texture="linen",
                          ground="#5a5045", seed=11, budget=300)),
    Painting("sonnet", "Claude/lighthouse_greenhouse/sonnet", spent=274,
             session=dict(width=1024, height=768, texture="linen",
                          ground="cool_grey", seed=74, budget=340)),
    Painting("opus", "Claude/lighthouse_greenhouse/opus", spent=296,
             session=dict(width=1120, height=860, texture="linen",
                          ground="toned_warm_grey", seed=41, budget=300)),
    Painting("fable", "Claude/lighthouse_greenhouse/fable", spent=284,
             session=dict(width=1024, height=768, texture="linen",
                          ground="toned_warm_grey", seed=47, budget=300)),
    # Two passes share the number 5 here and the page claims no rebuild, so the order
    # between them is this script's guess (alphabetical, as everywhere else).
    Painting("pool", "Claude/pool_night", spent=221, rebuilds=False,
             session=dict(width=1024, height=768, texture="linen",
                          ground="cool_grey", seed=11, budget=300)),
    Painting("heron1", "Claude/heron_lot/1", spent=293, rebuilds=False,
             session=dict(width=1024, height=768, texture="rough",
                          ground="toned_warm_grey", seed=17, budget=320)),
    Painting("heron2", "Claude/heron_lot/2", spent=253, rebuilds=False,
             session=dict(width=1024, height=768, texture="rough",
                          ground="#6d635a", seed=23, budget=320)),
    Painting("greenhouse", "Claude/greenhouse_winter", spent=297, rebuilds=False,
             session=dict(width=1024, height=768, texture="linen",
                          ground="toned_warm_grey", seed=3, budget=300)),
    Painting("fogged", "Claude/fogged_glass", spent=311, rebuilds=False,
             session=dict(width=1200, height=800, texture="rough",
                          ground="umber_wash", seed=11, budget=320)),
    Painting("pier", "Claude/pier_underside", spent=257, rebuilds=False,
             session=dict(width=1024, height=768, texture="linen",
                          ground="#5a5045", seed=11, budget=300)),
    Painting("hands", "Claude/hands_beans", spent=329, rebuilds=False,
             session=dict(width=1024, height=768, texture="linen",
                          ground="#5f4a39", seed=11, budget=420)),
    # The 0.5.0 cohort. Three of the seven wrote one script rather than passes.
    Painting("bigpickle", "BigPickle_blind/sunset_landscape", cohort=True, spent=50,
             driver="sunset_paint.py"),
    Painting("deepseek", "Deepseek/tidal_sky", cohort=True, spent=68,
             session=dict(width=1024, height=768, texture="linen",
                          ground="toned_grey", seed=7, budget=300)),
    Painting("gemini", "Gemini/misty_pine_forest_at_dawn", cohort=True, spent=725,
             driver="paint_dawn_forest.py"),
    Painting("glm", "GLM/terminal_window", cohort=True, spent=126, first=("draw.py",),
             session=dict(width=1024, height=768, texture="linen",
                          ground="#2e332c", seed=7, budget=300)),
    Painting("gpt", "GPT/seaside-village", cohort=True, spent=408, driver="paint.py"),
    Painting("grok", "Grok/harbor", cohort=True, spent=132,
             session=dict(width=1024, height=768, texture="linen",
                          ground="cool_grey", seed=11, budget=300)),
    Painting("kimi", "Kimi/lighthouse-dusk", cohort=True, spent=170,
             session=dict(width=1024, height=768, texture="linen",
                          ground="toned_grey", seed=7, budget=420)),
]


# -- the replay harness -------------------------------------------------------------
#
# What a rule would have said, to a painter who was painting, at the moment they
# painted it. Every verb that lays paint is wrapped for the length of a replay; each
# call records what it was handed, what it laid, what the engine warned about, and --
# for the checks in D2, which read the canvas under the footprint -- the canvas as it
# stood before the mark landed.
#
# Mass verbs go through `Session.stroke` themselves, so the wrapper counts depth and
# only the outermost call is a call. Anything that writes a file is stubbed: a replay
# runs in a copy of the painting's directory, but a pass that exports would otherwise
# spend a minute of it rebuilding a PNG the repository already has.

WATCHED = ("stroke", "dab", "smudge", "glaze", "block_in", "sweep", "cover",
           "scumble", "pencil", "erase", "dry", "undo")

#: Verbs whose candidate check wants the canvas under the footprint (workstream D2).
READS_CANVAS = ("smudge", "glaze", "scumble", "block_in", "cover", "stroke", "dab")

#: What a replay must not do: write into the repository, or spend its time drawing.
STUBBED = ("look", "look_image", "export", "timelapse_gif", "contact_sheet", "save",
           "look_areas", "capture_frame")


@dataclass
class Call:
    """One call of one verb, with what it was handed and what it laid."""

    verb: str
    bound: dict                       # the call's arguments, by name
    line: int                         # the line of the painter's own script
    first: int                        # index of the first log record it laid
    count: int = 0                    # how many records
    notices: tuple[str, ...] = ()     # what the engine warned about, at the call
    before: np.ndarray | None = None  # the values view before the mark landed
    wet: np.ndarray | None = None     # and the wetness under it, if any was wet
    place: object = None              # the shape or region it was given, if any

    @property
    def brush(self) -> str:
        b = self.bound.get("brush", "")
        return b if isinstance(b, str) else getattr(b, "name", "")

    @property
    def size(self) -> float:
        size = self.bound.get("size")
        return float(size) if size else 0.0


@dataclass
class Pass:
    """One pass: a committed pass script, or a numbered section of a painter's script."""

    painting: str
    name: str
    start: int                        # log index the pass began at
    end: int = 0
    calls: list[Call] = field(default_factory=list)
    findings: list[str] = field(default_factory=list)   # what report() said
    notices: list[str] = field(default_factory=list)    # what the calls warned about
    fires: dict[str, list[str]] = field(default_factory=dict)  # candidate code -> lines
    seconds: float = 0.0
    error: str = ""

    @property
    def marks(self) -> int:
        return self.end - self.start

    @property
    def label(self) -> str:
        return f"{self.painting}/{self.name}"


@dataclass
class Replay:
    """One painting, rebuilt."""

    painting: Painting
    session: Session | None = None
    passes: list[Pass] = field(default_factory=list)
    spent: int = 0
    seconds: float = 0.0
    error: str = ""
    #: Every number a candidate measured, fired or not: what a threshold is chosen from.
    samples: dict[str, list[float]] = field(default_factory=dict)

    @property
    def calls(self) -> list[Call]:
        return [c for p in self.passes for c in p.calls]

    @property
    def matched(self) -> bool:
        """Whether the rebuild came back at the stroke count the page records."""
        return self.spent == self.painting.spent

    @property
    def errors(self) -> list[str]:
        return ([self.error] if self.error else
                [f"{p.name}: {p.error}" for p in self.passes if p.error])


def _stub(name: str):
    """A verb that writes a file or draws a picture, for a run that wants neither."""
    def stubbed(self, *args, **kw):
        return f"({name} skipped by the probe)"
    stubbed.__name__ = name
    return stubbed


def _said(caught) -> list[str]:
    """What the engine warned about, out of everything Python warned about.

    A painter's own ``exec(open("helpers.py").read())`` leaves a ResourceWarning
    behind, and counting that as a line the tool printed would put three paintings'
    file handles into the noise budget.
    """
    return [str(w.message) for w in caught if issubclass(w.category, UserWarning)]


def _painter_line() -> int:
    """The line of the painter's own script that made this call.

    The first frame outside the engine and outside this file, which is what tells one
    numbered section of a one-script painting from the next.
    """
    frame = sys._getframe(1)
    while frame is not None:
        name = frame.f_code.co_filename
        if "easel" + os.sep not in name and "probe_cohort" not in name:
            return frame.f_lineno
        frame = frame.f_back
    return 0


class Watcher:
    """Wraps the painting verbs for the length of a replay. Not re-entrant."""

    def __init__(self, keep_canvas: bool = True, echo: bool = False) -> None:
        self.keep_canvas = keep_canvas
        self.echo = echo
        # A painting's own passes print: budget lines, looks, the painter's own
        # report(). All of it is swallowed for the length of the replay, so the echo
        # keeps a stream of its own from before that.
        self.stream = sys.stdout
        self.current: Pass | None = None
        self.replay: Replay | None = None
        self.session: Session | None = None
        #: (line, name) per numbered section, for a painting written as one script.
        self.sections: list[tuple[int, str]] = []
        self.depth = 0
        self.insetting = 0
        #: The canvas as the open pass found it. See `open`.
        self.opened: np.ndarray | None = None
        self._saved: dict[str, object] = {}
        self._signatures: dict[str, inspect.Signature] = {}

    def __enter__(self) -> Watcher:
        for name in WATCHED:
            original = getattr(Session, name)
            self._saved[name] = original
            self._signatures[name] = inspect.signature(original)
            setattr(Session, name, self._wrap(name, original))
        for name in STUBBED:
            self._saved[name] = getattr(Session, name)
            setattr(Session, name, _stub(name))
        # `inset-lost` (D1) is the one candidate that is not about a verb: it is about
        # what a shape came back as. Wrapped here so a painter's own `inset()` is seen
        # and the engine's -- `edge="clean"` insets the shape it fills -- is not,
        # which is what the depth guard already distinguishes.
        for shape in (Polygon, Region):
            self._saved[f"{shape.__name__}.inset"] = shape.inset
            shape.inset = self._wrap_inset(shape.inset)
        return self

    def __exit__(self, *exc) -> None:
        for name, original in self._saved.items():
            if "." in name:
                {"Polygon": Polygon, "Region": Region}[name.split(".")[0]].inset = original
            else:
                setattr(Session, name, original)

    # -- passes ------------------------------------------------------------------
    def open(self, name: str, session: Session | None = None) -> Pass:
        self.close()
        if session is not None:
            self.session = session
        started = len(self.session.history.records) if self.session else 0
        made = Pass(painting=self.replay.painting.name, name=name, start=started)
        made.seconds = time.time()
        # The canvas as it stood when the pass began, which is what `buried` needs and
        # what `look(diff=True)` cannot give: that one diffs against the last *look*.
        self.opened = (self.session.canvas.values(sketch=False).astype(np.float32) / 255.0
                       if self.session is not None and self.keep_canvas else None)
        self.current = made
        self.replay.passes.append(made)
        return made

    def close(self) -> None:
        open_pass, self.current = self.current, None
        if open_pass is None:
            return
        session = self.session
        open_pass.end = len(session.history.records) if session else 0
        open_pass.seconds = time.time() - open_pass.seconds
        if session is not None:
            # The check as the painter saw it: over the pass alone, off the session,
            # so the one rule that decays -- the stack of bars -- decays here exactly
            # as it does under `easel run`.
            said = session.report(since=open_pass.start)
            open_pass.findings = [line.strip()[2:] for line in said.splitlines()
                                  if line.strip().startswith("- ")]
            self._judge_pass(open_pass, session)
        if self.echo:
            print(f"    {open_pass.name:<26} {open_pass.marks:4d} records "
                  f"{open_pass.seconds:6.1f}s  {len(open_pass.notices)} notices, "
                  f"{len(open_pass.findings)} findings"
                  + (f"  [{open_pass.error}]" if open_pass.error else ""),
                  file=self.stream)

    def _section_of(self, line: int) -> str | None:
        name = None
        for start, label in self.sections:
            if line >= start:
                name = label
            else:
                break
        return name

    # -- the wrapper -------------------------------------------------------------
    def _wrap(self, name: str, original):
        def wrapper(session, *args, **kw):
            if self.depth or self.replay is None:
                return original(session, *args, **kw)
            self.depth += 1
            try:
                self.session = self.session or session
                line = _painter_line()
                if self.sections:
                    section = self._section_of(line)
                    if section and (self.current is None
                                    or self.current.name != section):
                        self.open(section, session)
                if self.current is None:
                    self.open("(unsectioned)", session)
                call = self._open_call(name, session, args, kw, line)
                with warnings.catch_warnings(record=True) as caught:
                    warnings.simplefilter("always")
                    out = original(session, *args, **kw)
                call.notices = tuple(_said(caught))
                self.current.notices.extend(call.notices)
                call.count = len(session.history.records) - call.first
                self.current.calls.append(call)
                self._judge(call, session)
                return out
            finally:
                self.depth -= 1
        wrapper.__name__ = name
        wrapper.__doc__ = getattr(original, "__doc__", "")
        return wrapper

    def _wrap_inset(self, original):
        def wrapper(place, amount, *args, **kw):
            # `inset` calls itself to keep a shape that meets the frame on it, so this
            # needs a guard of its own beside the verb depth: one call, one answer.
            self.insetting += 1
            try:
                kept = original(place, amount, *args, **kw)
            finally:
                self.insetting -= 1
            if self.depth or self.insetting or self.current is None:
                return kept
            said = inset_lost(place, kept, float(amount), self.replay.samples)
            if said:
                self.current.fires.setdefault("inset-lost", []).append(said)
            return kept
        wrapper.__name__ = "inset"
        wrapper.__doc__ = getattr(original, "__doc__", "")
        return wrapper

    def _judge_pass(self, done: Pass, session: Session) -> None:
        """Run every after-the-pass candidate: the new rows workstream D3 proposes."""
        if not self.keep_canvas:
            return
        now = session.canvas.values(sketch=False).astype(np.float32) / 255.0
        ctx = Done(session=session, made=done, opened=self.opened, now=now,
                   records=session.history.records, samples=self.replay.samples)
        for code, check in PASS_CHECKS.items():
            try:
                said = check(done, ctx)
            except Exception as exc:                    # noqa: BLE001 - a candidate
                said = f"(the {code} prototype raised {type(exc).__name__}: {exc})"
            if said:
                done.fires.setdefault(code, []).append(said)
        self.opened = None

    def _judge(self, call: Call, session: Session) -> None:
        """Run every call-time candidate against the call that has just landed.

        Here rather than afterwards because the checks in D2 read the canvas *under
        the footprint*, and the canvas the mark met exists only for the length of the
        call. Both views are dropped again as soon as the checks have had them: a
        corpus replay that kept one per call would hold several gigabytes of canvas
        nobody looks at.
        """
        if not self.keep_canvas or call.before is None:
            call.before = None
            return
        after = session.canvas.values(sketch=False).astype(np.float32) / 255.0
        ctx = Seen(session=session, call=call, before=call.before, after=after,
                   wet=call.wet,
                   records=session.history.records[call.first:call.first + call.count],
                   samples=self.replay.samples)
        call.wet = None
        for code, check in CALL_CHECKS.items():
            try:
                said = check(call, ctx)
            except Exception as exc:                    # noqa: BLE001 - a candidate
                said = f"(the {code} prototype raised {type(exc).__name__}: {exc})"
            if said:
                self.current.fires.setdefault(code, []).append(said)
        call.before = None

    def _open_call(self, name, session, args, kw, line: int) -> Call:
        """What the call was handed, normalised -- and the canvas it is about to meet."""
        try:
            bound = self._signatures[name].bind(session, *args, **kw)
            bound.apply_defaults()
            named = dict(bound.arguments)
            named.pop("self", None)
            named.update(named.pop("brush_overrides", {}) or {})
            named.update(named.pop("kw", {}) or {})
        except TypeError:                       # a call that is about to raise anyway
            named = {"args": args, **kw}
        place = None
        for key in ("region", "band", "place", "edge", "points"):
            if key in named:
                place = named[key]
                break
        before = wet = None
        if self.keep_canvas and name in READS_CANVAS:
            before = session.canvas.values(sketch=False).astype(np.float32) / 255.0
            # Only where there is something to find: `wet-under` is the one candidate
            # that needs it, and on a dry canvas the whole array is zero.
            if float(session.canvas.wetness.max()) > 0.0:
                wet = session.canvas.wetness.copy()
        return Call(verb=name, bound=named, line=line,
                    first=len(session.history.records), before=before, place=place,
                    wet=wet)


_SECTION = re.compile(r"^\s*#\s*(\d+)[.)]\s+(.+?)\s*$")


def _sections(source: str) -> list[tuple[int, str]]:
    """Where a one-script painting's own numbered sections start.

    Three of the cohort wrote one script rather than a pass per file, and all three
    numbered their sections in comments -- ``# 1. Graphite drawing``, ``# 4. MID-GROUND
    RIDGE``. That numbering is the painter's own unit of work, so it is what this calls
    a pass: the alternative is one pass of 725 marks, which would make every *share of
    passes* below meaningless for the paintings that most need one.
    """
    found: list[tuple[int, str]] = []
    for number, line in enumerate(source.splitlines(), start=1):
        match = _SECTION.match(line)
        if not match:
            continue
        label = f"{match.group(1)}. {match.group(2)[:36]}"
        if found and found[-1][1] == label:     # a banner repeated above and below
            continue
        found.append((number, label))
    return found


def _namespace(session: Session, path: Path) -> dict:
    ns = {name: getattr(easel, name) for name in easel.__all__}
    ns.update({"s": session, "session": session, "palette": session.palette,
               "__name__": "__easel_script__", "__file__": str(path)})
    return ns


def _import_script(path: Path):
    """A painting written as an importable module, imported without running its main."""
    spec = importlib.util.spec_from_file_location(f"painting_{path.stem}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replay(entry: Painting, keep_canvas: bool = True, echo: bool = False,
           limit: int | None = None) -> Replay:
    """Rebuild one painting from its committed scripts, pass by pass.

    The scripts run the way ``easel run`` runs them: the prelude re-executed in a
    fresh scope in front of every pass, so a pass that quietly depended on the last
    one's variables fails here the way it would there. They run in a **copy** of the
    painting's directory holding its ``.py`` files and nothing else, so a pass that
    writes lands in the copy -- several of them export the committed PNG, and a probe
    that overwrote what it was measuring would be a poor probe.

    Time-lapse capture is off: it records no marks and changes no pixel, and at 25 ms
    a stroke (B15) it is a third of what a corpus replay would cost.
    """
    out = Replay(painting=entry)
    started = time.time()
    with tempfile.TemporaryDirectory(prefix=f"easel-{entry.name}-") as tmp:
        work = Path(tmp)
        for path in entry.folder.glob("*.py"):
            shutil.copy2(path, work / path.name)
        here = Path.cwd()
        try:
            os.chdir(work)
            with Watcher(keep_canvas=keep_canvas, echo=echo) as watcher:
                watcher.replay = out
                with contextlib.redirect_stdout(io.StringIO()):
                    try:
                        if entry.driver:
                            _replay_driver(entry, work, watcher)
                        else:
                            _replay_passes(entry, work, watcher)
                    except Exception as exc:                # noqa: BLE001 - reported
                        out.error = f"{type(exc).__name__}: {exc}"
                    watcher.close()
                out.session = watcher.session
        finally:
            os.chdir(here)
    out.seconds = time.time() - started
    if out.session is not None:
        out.spent = out.session.history.stroke_count
    return out


def _replay_passes(entry: Painting, work: Path, watcher: Watcher,
                   limit: int | None = None) -> None:
    session = Session(out_dir=work / "out", timelapse=False, **entry.session)
    watcher.session = session
    prelude = work / "prelude.py"
    source = prelude.read_text(encoding="utf-8") if prelude.exists() else ""
    for name in entry.passes[:limit]:
        path = work / name
        made = watcher.open(name, session)
        ns = _namespace(session, path)
        # Around the whole pass as well as around each call: the planning verbs warn
        # too -- `cost()` says what a mass with `direction=` left off would charge --
        # and a painter under `easel run` reads those on the same screen. Caught here
        # they are counted; left alone they would go to stderr past the probe.
        with warnings.catch_warnings(record=True) as loose:
            warnings.simplefilter("always")
            try:
                if source:
                    exec(compile(source, str(prelude), "exec"), ns)      # noqa: S102
                exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), ns)
            except Exception as exc:                                     # noqa: BLE001
                made.error = f"{type(exc).__name__}: {exc}"
        made.notices.extend(_said(loose))
        watcher.close()


def _replay_driver(entry: Painting, work: Path, watcher: Watcher) -> None:
    """The three paintings written as one script.

    GPT's is a module of named stages and is driven stage by stage, which is how its
    own painter ran it. The other two run once and build their own session, and the
    watcher cuts them into their own numbered sections as the calls arrive -- which is
    why every call carries the line of the painter's script that made it.
    """
    path = work / entry.driver
    source = path.read_text(encoding="utf-8")
    if entry.name == "gpt":
        module = _import_script(path)
        session = Session(module.WIDTH, module.HEIGHT, texture="linen",
                          ground="#746d78", seed=61, texture_strength=0.72,
                          budget=module.BUDGET, timelapse=False, out_dir=work / "out")
        watcher.session = session
        module.palette(session)
        watcher.open("00-sketch", session)
        module.sketch(session)
        for name, stage in module.STAGES.items():
            made = watcher.open(name, session)
            with warnings.catch_warnings(record=True) as loose:
                warnings.simplefilter("always")
                try:
                    stage(session)
                except Exception as exc:                                 # noqa: BLE001
                    made.error = f"{type(exc).__name__}: {exc}"
            made.notices.extend(_said(loose))
        watcher.close()
        return

    watcher.sections = _sections(source)
    ns = {"__name__": "__easel_script__", "__file__": str(path)}
    with warnings.catch_warnings(record=True) as loose:
        warnings.simplefilter("always")
        exec(compile(source, str(path), "exec"), ns)                     # noqa: S102
        if entry.name == "gemini":
            ns["paint"]()
    if watcher.current is not None:
        watcher.current.notices.extend(_said(loose))


# -- the candidates -----------------------------------------------------------------
#
# One function per row of workstreams D and E, each returning the line it would print
# or None. They are prototypes and not the engine's own checks: what they are for is
# the three numbers the plan asks step 2 for -- how often it fires, on which passes,
# and whether it fires on a code block of the guide. Where a row of the plan gives no
# threshold, the number used here is stated in the function's own docstring, because a
# count is only worth reading beside the line that produced it.

CALL_CHECKS: dict[str, object] = {}
PASS_CHECKS: dict[str, object] = {}

#: Which workstream each candidate comes from, for the table at the end.
FROM: dict[str, str] = {}


def call_check(code: str, where: str):
    def register(fn):
        CALL_CHECKS[code] = fn
        FROM[code] = where
        return fn
    return register


def pass_check(code: str, where: str):
    def register(fn):
        PASS_CHECKS[code] = fn
        FROM[code] = where
        return fn
    return register


MASS_VERBS = ("block_in", "sweep", "cover", "scumble")
CHISEL = ("flat", "knife")


def _units(canvas) -> tuple[float, float]:
    """What one normalised step in x and in y is worth in brush units.

    A brush ``size`` is a share of the canvas's long side; a place is in normalised
    0..1 coordinates on both axes. Everything below that compares the two goes
    through here, which is the arithmetic ``_mark_length_and_angle`` already does for
    a mark.
    """
    long = float(canvas.long_side)
    return canvas.width / long, canvas.height / long


def _extents(place, canvas) -> tuple[float, float]:
    """A place's width and height in brush units."""
    ux, uy = _units(canvas)
    x0, y0, x1, y1 = place.bounds
    return abs(x1 - x0) * ux, abs(y1 - y0) * uy


def _segments(place) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    """A place's outline, as the segments a pass can end against."""
    if isinstance(place, Polygon):
        pts = place.closed
    elif isinstance(place, Region):
        pts = [(place.x0, place.y0), (place.x1, place.y0), (place.x1, place.y1),
               (place.x0, place.y1), (place.x0, place.y0)]
    else:
        return []
    return list(zip(pts, pts[1:], strict=False))


def _angle(p0, p1, canvas) -> float:
    ux, uy = _units(canvas)
    dx, dy = (p1[0] - p0[0]) * ux, (p1[1] - p0[1]) * uy
    return math.degrees(math.atan2(dy, dx)) % 180.0


def _length(p0, p1, canvas) -> float:
    ux, uy = _units(canvas)
    return math.hypot((p1[0] - p0[0]) * ux, (p1[1] - p0[1]) * uy)


def _off(a: float, b: float) -> float:
    """How far two angles mod 180 are apart."""
    d = abs(a - b) % 180.0
    return min(d, 180.0 - d)


def _pass_angle(call: Call, session: Session) -> float | None:
    """The angle the call's own passes actually ran at, off the marks it laid.

    Read from the log rather than worked out from ``direction=``: the engine resolves
    a mass's default direction from the shape, ``"cross"`` is two passes, and a probe
    that re-derived any of that would be measuring its own copy of the rule.
    """
    records = session.history.records[call.first:call.first + call.count]
    angles = [_mark_length_and_angle(r, session.canvas) for r in records]
    angles = [a for length, a in angles if length > 0.0]
    return _angle_centre(angles) if angles else None


_mark_length_and_angle = session_module._mark_length_and_angle
_angle_centre = session_module._angle_centre
_normal_extent = session_module._normal_extent
_angle_of = session_module._angle_of
_pass_step = session_module._pass_step
_pass_directions = session_module._pass_directions


def _resolved_size(call: Call, ctx: Seen) -> float:
    """The brush size the call actually ran at, not the one it was handed.

    ``size=`` is left off in most of the corpus and the brush's own default stands,
    so reading ``call.bound`` alone measures a third of the calls and skips the rest.
    Every record carries the resolved brush in ``params``, so the first mark the call
    laid is asked instead.
    """
    if call.bound.get("size"):
        return float(call.bound["size"])
    records = ctx.session.history.records[call.first:call.first + call.count]
    for record in records:
        size = record.params.get("size")
        if size:
            return float(size)
    return 0.0


@dataclass
class Seen:
    """What a call-time candidate is handed: the call, and the canvas either side of it."""

    session: Session
    call: Call
    before: np.ndarray                 # the values view, 0..1, before the mark landed
    after: np.ndarray                  # and after
    records: list                      # the log records the call laid
    wet: np.ndarray | None = None      # the wetness under it, where there was any
    samples: dict[str, list[float]] = field(default_factory=dict)

    @property
    def canvas(self):
        return self.session.canvas

    def note(self, name: str, value: float) -> float:
        """Keep a number whether or not the rule fires. A threshold is chosen from the
        whole distribution, not from the tail that happened to be over it."""
        self.samples.setdefault(name, []).append(float(value))
        return float(value)

    @property
    def changed(self) -> np.ndarray:
        return np.abs(self.after - self.before) > 0.004

    def value_at(self, xs, ys, view: np.ndarray | None = None) -> np.ndarray:
        """The canvas value at normalised points -- sampled, never rasterised."""
        view = self.before if view is None else view
        h, w = view.shape
        cols = np.clip((np.asarray(xs) * w).astype(int), 0, w - 1)
        rows = np.clip((np.asarray(ys) * h).astype(int), 0, h - 1)
        return view[rows, cols]


@dataclass
class Done:
    """What an after-the-pass candidate is handed: the pass, and the canvas either side."""

    session: Session
    made: Pass
    opened: np.ndarray | None          # the canvas when the pass began
    now: np.ndarray                    # and when it ended
    records: list                      # the whole log
    samples: dict[str, list[float]] = field(default_factory=dict)

    @property
    def canvas(self):
        return self.session.canvas

    def note(self, name: str, value: float) -> float:
        self.samples.setdefault(name, []).append(float(value))
        return float(value)

    @property
    def marks(self) -> list:
        """What this pass laid, paint only."""
        return [r for r in self.records[self.made.start:self.made.end]
                if r.kind not in ("dry", "look", "pencil", "erase")]

    @property
    def earlier(self) -> list:
        return [r for r in self.records[:self.made.start]
                if r.kind not in ("dry", "look", "pencil", "erase")]


def _mask(place, width: int, height: int) -> np.ndarray | None:
    """The pixels a place covers. A shape knows; a region is its rectangle."""
    if isinstance(place, Polygon):
        return place.mask(width, height)
    if isinstance(place, Region):
        mask = np.zeros((height, width), dtype=bool)
        x0, x1 = sorted((int(place.x0 * width), int(place.x1 * width)))
        y0, y1 = sorted((int(place.y0 * height), int(place.y1 * height)))
        mask[max(y0, 0):max(y1, 0), max(x0, 0):max(x1, 0)] = True
        return mask
    return None


def _spread(place, ctx: Seen) -> tuple[float, float] | None:
    """What the call painted, against the place it was handed.

    Returns ``(painted / asked, share of the paint that landed outside)`` -- the
    measurement B17 made by hand for one band, taken here on every mass of the
    corpus. Measured off the canvas rather than predicted, because the prediction is
    what the check would do and the point of the probe is to say whether it is right.
    """
    height, width = ctx.before.shape
    mask = _mask(place, width, height)
    if mask is None or not mask.any():
        return None
    changed = ctx.changed
    painted = int(changed.sum())
    if not painted:
        return 0.0, 0.0
    return painted / float(mask.sum()), float((changed & ~mask).sum()) / painted


# -- D1: at the call, from geometry alone --------------------------------------------

#: What a mass may paint of the place it was handed before `spill` says so. B17
#: measured 1.43x for a band at its own axis and 3.53x at 60 degrees; the corpus says
#: where between those two an ordinary mass sits.
SPILL_RATIO = 1.6

#: How tall a ledge has to be, in brush widths, before it reads as a step rather than
#: as the ragged edge a block-in has anyway. Two brushes is the floor the sweep below
#: settles on: at the lit band's own `0.020` that is a 40-thousandth ledge, and the
#: band the calibration measured steps **8.4**.
STAIR_RISE = 2.0
#: ...and this many of them have to land on the outline before it is a staircase and
#: not a jag. The corpus and the guide put a clean break here: every case anybody has
#: called a staircase leaves **3.4 or more** such ends (the lit band 5.8, Kimi's rock
#: face 5.0, *a mass built of planes* 11.7 on its lit plane), and the one guide block
#: that came nearest without being one -- a half-canvas rectangle swept six degrees
#: off its own top edge, which takes one end on each -- leaves **2.0**.
STAIR_LEDGES = 3.0


def _pass_unit(place, direction, canvas) -> tuple[float, float]:
    """The pass direction as a unit vector **in brush units**.

    ``direction=`` and ``Polygon.axis`` are both angles in the normalised 0..1 space
    the places are written in; a segment's angle, and the staircase a painter sees,
    are in pixels. On a 4:3 canvas the two differ by up to seven degrees, which is
    more than the whole window this rule lives in -- so both ends of every comparison
    below are brought here first. The prototype this replaces compared a brush-unit
    segment against a normalised pass angle and was wrong by that much.
    """
    degrees = place.axis if direction == "axis" else _angle_of(direction)
    ux, uy = _units(canvas)
    # `_angle_of` has already turned a name or a pair of points into degrees.
    theta = math.radians(degrees)
    dx, dy = math.cos(theta) * ux, math.sin(theta) * uy
    length = math.hypot(dx, dy) or 1.0
    return dx / length, dy / length


def _ledges(place, direction, size: float, density: float, canvas):
    """Per straight side: how many pass ends land on it, and how far apart they step.

    The mechanism, rather than a window of angles fitted to it. Passes run along
    ``d`` spaced ``step`` apart along the normal ``n``, and each one ends where it
    leaves the outline. So a side whose extent **across** the passes is ``across``
    takes ``across / step`` of those ends, and they are spread over its extent
    **along** them -- which makes each step

        rise = along / (across / step) = step x cot(theta)

    and says the whole of it. At ``theta = 0`` the passes run along the side and no
    pass ends on it at all (``across`` is nothing, so is the count). At ``theta =
    90`` every end lands on the same line and ``rise`` goes to nothing. The fault is
    in between and, because ``cot`` is steep near zero, it is **nearest parallel that
    it is worst** -- which is the half of the range the prototype excluded.

    ``direction`` is taken the way ``_block_in_paths`` takes it -- left off means
    horizontal, ``"cross"`` and a sequence are one pass per angle -- and every angle
    is walked, because a mass swept twice stairs on whichever of the two is nearest
    one of its sides.

    Yields ``(ledges, rise_in_brushes, side_length)`` per side, tallest step first.
    """
    ux, uy = _units(canvas)
    step = _pass_step(size, density)
    out = []
    for pass_dir in _pass_directions("horizontal" if direction is None else direction):
        dx, dy = _pass_unit(place, pass_dir, canvas)
        nx, ny = -dy, dx
        for p0, p1 in _segments(place):
            ex, ey = (p1[0] - p0[0]) * ux, (p1[1] - p0[1]) * uy
            across, along = abs(ex * nx + ey * ny), abs(ex * dx + ey * dy)
            ledges = across / step
            if ledges < 1e-9:
                continue
            out.append((ledges, (along / ledges) / size, math.hypot(ex, ey)))
    return sorted(out, key=lambda row: -row[1])


@call_check("chisel-staircase", "D1")
def chisel_staircase(call: Call, ctx: Seen) -> str | None:
    """A chisel filling a mass along a straight side it is *nearly* parallel to.

    Finding 1, and the one the plan calls the most common way a mass goes wrong.
    ``PAINTING.md`` measures it and ``RECIPES.md`` demonstrates it: Kimi's rock faces
    are *a mass built of planes* character for character.

    **Rewritten against the measurement**, which the prototype did not survive. It
    asked what share of the outline was more than fifteen degrees from both parallel
    and square, and that is a measure of how irregular a shape is, not of how it
    stairs: it was **silent on the lit band** ``CALIBRATION.md`` measures the
    staircase on (22% of its strong edges horizontal against 1% for a comb) and
    silent on Kimi's rock face, while firing on an ellipse, a blob and a rectangle
    swept at 28 degrees -- three shapes with no straight side to align to and so no
    remedy to offer. See :func:`_ledges` for what replaced it.
    """
    if call.verb not in ("block_in", "cover") or call.brush not in CHISEL:
        return None
    if str(call.bound.get("edge", "ragged")) != "ragged":
        return None
    if not isinstance(call.place, (Polygon, Region)):
        return None
    size, density = _resolved_size(call, ctx), float(call.bound.get("density", 1.0))
    if not size:
        return None
    rows = _ledges(call.place, call.bound.get("direction"), size, density, ctx.canvas)
    # A side that does not take one whole pass end has no ledge on it at all, and its
    # `rise` is the arithmetic running away towards parallel -- 110 brush widths on a
    # canvas one wide. It is dropped before the step is read off, not after.
    tall = [row for row in rows if row[0] >= 1.0 and row[1] >= STAIR_RISE]
    ends = sum(row[0] for row in tall)
    ctx.note("chisel-staircase: pass ends on a side that steps", ends)
    if ends < STAIR_LEDGES:
        return None
    ctx.note("chisel-staircase: tallest ledge, in brush widths", tall[0][1])
    return (f"a {call.brush} filling this shape ends {ends:.0f} of its passes on "
            f"straight sides it runs nearly along, stepping up to {tall[0][1]:.0f} "
            f"brush widths from one to the next: those sides come back as a "
            f"staircase. Give direction= the two points of the side that matters, "
            f"or lay it with a comb and put a solid stroke down its core.")


@call_check("spill", "D1")
def spill(call: Call, ctx: Seen) -> str | None:
    """Paint that lands well outside the place it was given.

    Finding 8 and B17. Two shapes of the same fault: a ragged mass whose brush is a
    large part of the shorter extent, and a banded ``scumble`` whose auto brush is
    three of its own steps and whose steps are measured across the *bounding box*.
    The number printed is measured, not predicted: what share of the paint this call
    laid fell outside the place, and what multiple of that place it covered.
    """
    if call.verb not in MASS_VERBS or not isinstance(call.place, (Polygon, Region)):
        return None
    spread = _spread(call.place, ctx)
    if spread is None:
        return None
    ratio, outside = spread
    ctx.note(f"spill: {call.verb} painted / place asked for", ratio)
    ctx.note(f"spill: {call.verb} share of the paint outside the place", outside)
    if ratio < SPILL_RATIO:
        return None
    short = min(_extents(call.place, ctx.canvas))
    return (f"{call.verb} covered {ratio:.2f}x the place it was handed and {outside:.0%} "
            f"of its paint fell outside it (shorter extent {short:.3f}). "
            f"clip=, or edge=\"hard\".")


@call_check("ring-steps", "D1")
def ring_steps(call: Call, ctx: Seen) -> str | None:
    """An inward scumble whose rings step far enough apart to read as contour lines.

    B18: GLM's concentric rings, and the pool painting's *contour map*. Palette
    arithmetic only -- the two colours and ``n`` are all it needs.
    """
    if call.verb != "scumble" or call.bound.get("direction") != "inward":
        return None
    palette = ctx.session.palette
    n = int(call.bound.get("n", 8))
    a = palette.value_of(call.bound.get("color_a"))
    b = palette.value_of(call.bound.get("color_b"))
    step = ctx.note("ring-steps: value step per ring", abs(b - a) / max(n - 1, 1))
    if step < RING_STEP:
        return None
    want = math.ceil(abs(b - a) / RING_STEP) + 1
    return (f"{n} rings over a value span of {abs(b - a):.2f} step {step:.3f} a ring, "
            f"over the {RING_STEP:.02f} that reads as a contour line. n={want}, or a "
            f"closer pair of colours.")


#: The value step per ring at which rings stop blending and start drawing contours.
#: The number to calibrate: the probe prints every inward scumble of the corpus beside
#: what its own painting's notes say about rings.
RING_STEP = 0.05


@call_check("scumble-few", "D1")
def scumble_few(call: Call, ctx: Seen) -> str | None:
    """``scumble(n=)`` under five: a passage laid as bars, which is what it exists to stop."""
    if call.verb != "scumble":
        return None
    n = int(call.bound.get("n", 8))
    return (f"scumble(n={n}): under five passes a graded passage comes back as bars."
            if n < 5 else None)


@call_check("round-soft-mass", "D1")
def round_soft_mass(call: Call, ctx: Seen) -> str | None:
    """A mass laid with the one brush the reference calls the least painterly."""
    if call.verb not in MASS_VERBS or call.brush != "round_soft":
        return None
    return f"{call.verb} with round_soft: the least painterly tip, over a whole mass."


@call_check("mass-is-a-stroke", "D1")
def mass_is_a_stroke(call: Call, ctx: Seen) -> str | None:
    """A mass narrower than two brushes: one or two passes wearing a mass's clothes."""
    if call.verb not in MASS_VERBS or not isinstance(call.place, (Polygon, Region)):
        return None
    size = call.size or _laid_size(call, ctx)
    short = min(_extents(call.place, ctx.canvas))
    if not size:
        return None
    ctx.note("mass-is-a-stroke: brushes across the shorter extent", short / size)
    if short > 2.0 * size:
        return None
    return (f"{call.verb} on a place {short:.3f} across at size={size:g}: "
            f"{short / size:.1f} brushes, which is a stroke, not a mass.")


@call_check("shallow-box", "D1")
def shallow_box(call: Call, ctx: Seen) -> str | None:
    """A shallow shape with the passes along its long axis: it comes back as its box."""
    if call.verb not in MASS_VERBS or not isinstance(call.place, Polygon):
        return None
    size = call.size or _laid_size(call, ctx)
    wide, tall = _extents(call.place, ctx.canvas)
    short, long = min(wide, tall), max(wide, tall)
    if not size or short > 4.0 * size or long < 3.0 * short:
        return None
    angle = _pass_angle(call, ctx.session)
    axis = 0.0 if wide >= tall else 90.0
    if angle is None or _off(angle, axis) > 20.0:
        return None
    return (f"a shape {short / size:.1f} brushes deep and {long / short:.1f} times as "
            f"long, with the passes along it: this lands as its bounding box.")


@call_check("cross-small", "D1")
def cross_small(call: Call, ctx: Seen) -> str | None:
    """Crossed passes on a mass too small to hold two of them."""
    if call.verb not in MASS_VERBS or call.bound.get("direction") != "cross":
        return None
    size = call.size or _laid_size(call, ctx)
    short = min(_extents(call.place, ctx.canvas))
    if not size or short > 4.0 * size:
        return None
    return (f"direction=\"cross\" on a place {short / size:.1f} brushes across: the "
            f"second pass prints the first.")


#: How much of a shape's area an `inset()` may lose before it is not that shape.
INSET_KEPT = 0.70

FROM["inset-lost"] = "D1"


def _area(place) -> float:
    if isinstance(place, Polygon):
        return float(place.area)
    if isinstance(place, Region):
        return abs(place.width * place.height)
    return 0.0


def inset_lost(before, after, amount: float, samples: dict) -> str | None:
    """``inset()`` that keeps well under the shape it was given.

    Measured earlier at 62.7% kept on a shape that was not convex, which is the case
    the prose in ``REFERENCE.md`` describes. Only the area half of the plan's row is
    measured here: *or drops a lobe* needs the shape's components, and a shape that
    drops one loses the area with it, so the area is the cheaper half of the same
    question.
    """
    was, now = _area(before), _area(after)
    if was <= 0.0 or amount <= 0.0:
        return None
    kept = now / was
    samples.setdefault("inset-lost: share of the area kept", []).append(kept)
    if kept >= INSET_KEPT:
        return None
    return (f"inset({amount:g}) kept {kept:.0%} of this shape: an inset walks every "
            f"edge inward, so a shape that is not convex loses more than the border.")


def _laid_size(call: Call, ctx: Seen) -> float:
    """The size the call actually laid, when it left the brush's own default on."""
    sizes = [float(r.params.get("size", 0.0)) for r in ctx.records]
    return float(np.median(sizes)) if sizes else 0.0


# -- D2: at the call, reading the canvas under the footprint --------------------------
#
# New in this round: the tool can see what the mark is about to land on. Every one of
# these samples along the path rather than rasterising it -- the cost has to stay
# under a stroke's own, and a stroke is already ~200 ms.

def _path(ctx: Seen) -> np.ndarray:
    """The path the call actually laid, off the log rather than off the argument.

    ``smudge`` handed a shape walks its own outline, so the argument is not the path
    and the record is.
    """
    pts = [np.asarray(r.points, dtype=np.float64) for r in ctx.records if len(r.points) > 1]
    return pts[0] if pts else np.empty((0, 2))


def _arc(points: np.ndarray, canvas) -> float:
    ux, uy = _units(canvas)
    if len(points) < 2:
        return 0.0
    d = np.diff(points, axis=0) * np.array([ux, uy])
    return float(np.hypot(d[:, 0], d[:, 1]).sum())


def _walk(points: np.ndarray, samples: int = 24) -> np.ndarray:
    """``samples`` points spread evenly along a path, by arc length."""
    if len(points) < 2:
        return points
    d = np.hypot(*np.diff(points, axis=0).T)
    cum = np.concatenate([[0.0], np.cumsum(d)])
    if cum[-1] <= 0:
        return points[:1]
    want = np.linspace(0.0, cum[-1], samples)
    return np.stack([np.interp(want, cum, points[:, 0]),
                     np.interp(want, cum, points[:, 1])], axis=1)


@call_check("smudge-across", "D2")
def smudge_across(call: Call, ctx: Seen) -> str | None:
    """A smudge whose path crosses a boundary instead of following one (finding 3).

    Measured as the value change *along* the path against the change *across* it. A
    smudge run along a join sees one value ahead of it and two either side; run across
    one it sees the step in front of it, and drags a thumbprint out of the light mass.
    """
    if call.verb != "smudge":
        return None
    points = _walk(_path(ctx))
    if len(points) < 4:
        return None
    size = float(ctx.records[0].params.get("size", 0.03)) or 0.03
    along = ctx.value_at(points[:, 0], points[:, 1])
    step = np.diff(points, axis=0)
    normal = np.stack([-step[:, 1], step[:, 0]], axis=1)
    normal /= np.maximum(np.hypot(normal[:, 0], normal[:, 1]), 1e-9)[:, None]
    mid = (points[:-1] + points[1:]) * 0.5
    one = mid + normal * size
    other = mid - normal * size
    across = float(np.mean(np.abs(ctx.value_at(one[:, 0], one[:, 1])
                                  - ctx.value_at(other[:, 0], other[:, 1]))))
    ran = float(np.percentile(along, 95) - np.percentile(along, 5))
    ctx.note("smudge-across: change along the path, over change across it",
             ran / max(across, 1e-3))
    if ran < across or ran < 0.06:
        return None
    return (f"the value changes {ran:.2f} along this smudge and {across:.2f} across it: "
            f"the path crosses a boundary instead of following one.")


@call_check("smudge-again", "D2")
def smudge_again(call: Call, ctx: Seen) -> str | None:
    """A second smudge down a join the first one already took 40% off. Log only."""
    if call.verb != "smudge":
        return None
    points = _walk(_path(ctx), 16)
    if len(points) < 4:
        return None
    size = float(ctx.records[0].params.get("size", 0.03)) or 0.03
    ux, uy = _units(ctx.canvas)
    near = np.zeros(len(points), dtype=bool)
    for record in ctx.session.history.records[:call.first]:
        if record.kind != "smudge" and record.params.get("tip") != "smudge":
            continue
        earlier = np.asarray(record.points, dtype=np.float64)
        if len(earlier) < 2:
            continue
        earlier = _walk(earlier, 48)
        dx = (points[:, None, 0] - earlier[None, :, 0]) * ux
        dy = (points[:, None, 1] - earlier[None, :, 1]) * uy
        near |= np.hypot(dx, dy).min(axis=1) < size
    share = ctx.note("smudge-again: share of the path over an earlier smudge",
                     float(near.mean()))
    if share < 0.6:
        return None
    return (f"{share:.0%} of this path lies within a brush of an earlier smudge: a "
            f"second pass undoes most of the first. Lay paint across it instead.")


#: A smudge longer than this leaves a mid-value strip rather than a softened join.
SMUDGE_LONG = 0.10


@call_check("smudge-long", "D2")
def smudge_long(call: Call, ctx: Seen) -> str | None:
    """A smudge run further than about a tenth of the canvas (the winter greenhouse)."""
    if call.verb != "smudge":
        return None
    length = ctx.note("smudge-long: path length, in brush units",
                      _arc(_path(ctx), ctx.canvas))
    if length < SMUDGE_LONG:
        return None
    return (f"a smudge {length:.2f} of the canvas long: over this length it leaves a "
            f"mid-value strip -- two edges where there was one.")


#: The value shift at which a film stops shifting a mass and becomes a new one.
GLAZE_NEW_MASS = 0.08


@call_check("glaze-far", "D2")
def glaze_far(call: Call, ctx: Seen) -> str | None:
    """A film that lands as a new mass rather than as a shift of an old one (finding 4).

    The number is the shift the film actually made over its own footprint, measured
    here rather than predicted: the check the plan proposes predicts it from the
    colour and the canvas under it, and this is what that prediction has to match.
    """
    glazing = call.verb == "glaze" or bool(call.bound.get("glaze"))
    if not glazing:
        return None
    changed = ctx.changed
    if not changed.any():
        return None
    shift = ctx.note("glaze-far: value shift over the film's own footprint",
                     float(np.abs(ctx.after - ctx.before)[changed].mean()))
    if shift < GLAZE_NEW_MASS:
        return None
    return (f"this film moved the value under it by {shift:.3f} -- at {GLAZE_NEW_MASS:.2f} "
            f"a film stops shifting a mass and becomes a new one. to_value=, or mix it "
            f"closer to what it lands on.")


#: How far an inward scumble's first ring may sit from what the patch meets its
#: surroundings at before it draws a rim.
RIM_OFF = 0.06


@call_check("ring-rim", "D2")
def ring_rim(call: Call, ctx: Seen) -> str | None:
    """An inward scumble whose first ring lands on the boundary at the wrong value."""
    if call.verb != "scumble" or call.bound.get("direction") != "inward":
        return None
    place = call.place
    if not isinstance(place, (Polygon, Region)):
        return None
    outline = np.asarray(place.closed if isinstance(place, Polygon)
                         else [(place.x0, place.y0), (place.x1, place.y0),
                               (place.x1, place.y1), (place.x0, place.y1),
                               (place.x0, place.y0)], dtype=np.float64)
    ring = _walk(outline, 48)
    met = float(np.median(ctx.value_at(ring[:, 0], ring[:, 1])))
    first = ctx.session.palette.value_of(call.bound.get("color_a"))
    off = ctx.note("ring-rim: first ring against what the patch meets",
                   abs(first - met))
    if off < RIM_OFF:
        return None
    return (f"the first ring is {off:.2f} off the {met:.2f} this patch meets its "
            f"surroundings at: that draws a rim. Give it the value it meets.")


#: Wetness at which paint laid over paint still counts as wet-into-wet.
WET_ENOUGH = 0.15


@call_check("wet-under", "D2")
def wet_under(call: Call, ctx: Seen) -> str | None:
    """An opaque mark landing on paint that is still wet, and far from it in colour (5).

    Only measured where the canvas had any wetness at all. B18 found that the rings
    GLM lost a pass to were **not** this -- so what the corpus says about how often it
    would fire, and over what wetness, is what decides whether it is built.
    """
    if ctx.wet is None or call.verb in ("smudge", "dry"):
        return None
    if float(call.bound.get("opacity") or 1.0) < 0.8:
        return None
    points = np.vstack([np.asarray(r.points, dtype=np.float64)
                        for r in ctx.records if len(r.points)]) if ctx.records else None
    if points is None or not len(points):
        return None
    points = _walk(points, 48) if len(points) > 1 else points
    height, width = ctx.wet.shape
    cols = np.clip((points[:, 0] * width).astype(int), 0, width - 1)
    rows = np.clip((points[:, 1] * height).astype(int), 0, height - 1)
    wetness = float(np.mean(ctx.wet[rows, cols]))
    under = float(np.mean(ctx.before[rows, cols]))
    laid = float(np.mean(ctx.after[rows, cols]))
    ctx.note("wet-under: wetness under an opaque mark", wetness)
    if wetness < WET_ENOUGH or abs(laid - under) < 0.10:
        return None
    return (f"this lands on paint {wetness:.2f} wet and {abs(laid - under):.2f} away "
            f"from it in value: dry() first, or it will lift what is under it.")


@call_check("holes", "E")
def holes(call: Call, ctx: Seen) -> str | None:
    """How much of a ``solid=True`` mass came back bare (finding 2, B2).

    A measurement line rather than a finding -- but it only has an answer after a
    solid mass, so it is measured at the call. The share is of the shape's own
    interior, a brush in from the outline so the ragged edge is not counted as a hole.
    """
    if not call.bound.get("solid") or call.verb not in MASS_VERBS:
        return None
    place = call.place
    if not isinstance(place, (Polygon, Region)):
        return None
    size = call.size or _laid_size(call, ctx)
    inner = place.inset(size * 0.6) if size else place
    height, width = ctx.before.shape
    mask = _mask(inner, width, height)
    if mask is None or mask.sum() < 64:
        return None
    bare = mask & ~ctx.changed
    share = ctx.note(f"holes: bare share inside a solid {call.brush} mass",
                     float(bare.sum()) / float(mask.sum()))
    if share < 0.005:
        return None
    return (f"{share:.2%} of this solid {call.brush} mass came back bare "
            f"({int(bare.sum())} px inside the shape).")


# -- D3: after the pass, off the log --------------------------------------------------
#
# New rows for `_pass_findings`, in its own pattern: everything they read is already
# in the log, which carries brush, colour, size, path, pressure and note per mark.

def _hand(records: list) -> list:
    """The marks a painter laid by hand: not the passes of a mass verb."""
    return [r for r in records if not r.params.get("via")]


def _ends(record) -> tuple[np.ndarray, np.ndarray]:
    pts = np.asarray(record.points, dtype=np.float64)
    return pts[0], pts[-1]


#: How close the starts have to be, in brush units, for a fan to be a daisy.
FAN_RADIUS = 0.06
#: ...and how far the marks have to fan out before it reads as one.
FAN_DEGREES = 40.0


@pass_check("radiating", "D3")
def radiating(made: Pass, ctx: Done) -> str | None:
    """Four or more hand-laid marks starting in one place and fanning out (finding 6).

    The daisy: ``PAINTER.md`` step 5 says it, ``RECIPES.md`` says it twice and
    ``scumble``'s own docstring says it a fourth time, and a painter drew one anyway.
    """
    marks = [r for r in _hand(ctx.marks) if len(r.points) > 1]
    if len(marks) < 4:
        return None
    ux, uy = _units(ctx.canvas)
    best = None
    for which in (0, -1):
        origins = np.array([np.asarray(r.points, dtype=np.float64)[which] for r in marks])
        angles = np.array([_angle(*(_ends(r) if which == 0 else _ends(r)[::-1]),
                                  ctx.canvas) for r in marks])
        for centre in origins:
            near = np.hypot((origins[:, 0] - centre[0]) * ux,
                            (origins[:, 1] - centre[1]) * uy) < FAN_RADIUS
            if int(near.sum()) < 4:
                continue
            spread = float(np.ptp(np.sort(angles[near])))
            spread = min(spread, 180.0 - spread) if spread > 90.0 else spread
            if best is None or (int(near.sum()), spread) > best[:2]:
                best = (int(near.sum()), spread)
    if best is None:
        return None
    count, spread = best
    ctx.note("radiating: degrees fanned by the marks sharing a start", spread)
    if spread < FAN_DEGREES:
        return None
    return (f"{count} hand-laid marks start within {FAN_RADIUS:g} of each other and "
            f"fan {spread:.0f} degrees: that is a daisy. Give them different origins, "
            f"or lay the form with scumble(direction=\"inward\").")


#: A loop's signature: this many marks of one brush and colour...
LOOP_MARKS = 6
#: ...whose lengths vary by less than this share of their own mean...
LOOP_LENGTH_CV = 0.15
#: ...and whose spacing along their own line varies by less than this.
LOOP_SPACING_CV = 0.30


@pass_check("one-loop", "D3")
def one_loop(made: Pass, ctx: Done) -> str | None:
    """One loop's signature: one brush, one colour, one length, evenly spaced (finding 7).

    Four of the seven cohort painters failed the same passage the same way -- a column
    of same-length marks for a reflection on water -- and ``RECIPES.md`` has no entry
    for it. This is the shape of what they wrote, read off the log.
    """
    groups: dict[tuple, list] = {}
    for record in _hand(ctx.marks):
        if len(record.points) < 2:
            continue
        groups.setdefault((record.brush, record.color_hex), []).append(record)
    for (brush, _), marks in groups.items():
        if len(marks) < LOOP_MARKS:
            continue
        lengths = np.array([_arc(np.asarray(r.points, dtype=np.float64), ctx.canvas)
                            for r in marks])
        if lengths.mean() <= 0:
            continue
        cv = float(lengths.std() / lengths.mean())
        ramp = bool(np.all(np.diff(lengths) > 0) or np.all(np.diff(lengths) < 0))
        centres = np.array([np.asarray(r.points, dtype=np.float64).mean(axis=0)
                            for r in marks])
        ux, uy = _units(ctx.canvas)
        pts = centres * np.array([ux, uy])
        pts = pts - pts.mean(axis=0)
        # The line they sit on: their own first principal axis, and how evenly they
        # are spread along it. A hand-placed row has clumps and holes; a loop does not.
        axis = np.linalg.svd(pts, full_matrices=False)[2][0]
        along = np.sort(pts @ axis)
        gaps = np.diff(along)
        straight = float(np.abs(pts @ np.array([-axis[1], axis[0]])).max())
        if gaps.mean() <= 0:
            continue
        spacing_cv = float(gaps.std() / gaps.mean())
        ctx.note("one-loop: spread of the mark lengths, as a share of their mean", cv)
        ctx.note("one-loop: spread of the spacing along their own line", spacing_cv)
        if (cv > LOOP_LENGTH_CV and not ramp) or spacing_cv > LOOP_SPACING_CV:
            continue
        if straight > 3.0 * float(gaps.mean()):
            continue
        return (f"{len(marks)} {brush} marks in one colour, "
                f"{'stepping in length' if ramp else f'all {lengths.mean():.3f} long'}, "
                f"evenly spaced on one line (spacing varies {spacing_cv:.0%}): that is "
                f"a loop's signature, not a row of things.")
    return None


#: A mark counts as buried when this share of it is under the pass's own paint.
BURIED_SHARE = 0.5
#: ...and the pass says so once this many earlier marks have gone.
BURIED_MARKS = 4


@pass_check("buried", "D3")
def buried(made: Pass, ctx: Done) -> str | None:
    """A pass that covers what was standing in front of it (finding 9).

    ``LESSONS.md`` lists the depth-order paragraph as failed in three runs and still
    open. This is the check that would close it: the pixels this pass changed, against
    the earlier marks that were small or noted ``subject``.
    """
    if ctx.opened is None:
        return None
    changed = np.abs(ctx.now - ctx.opened) > 0.02
    if not changed.any():
        return None
    height, width = changed.shape
    watch = [r for r in ctx.earlier
             if float(r.params.get("size", 1.0)) < 0.02 or "subject" in str(r.note).lower()]
    if len(watch) < BURIED_MARKS:
        return None
    gone = 0
    for record in watch:
        pts = np.asarray(record.points, dtype=np.float64)
        pts = _walk(pts, 8) if len(pts) > 1 else pts
        cols = np.clip((pts[:, 0] * width).astype(int), 0, width - 1)
        rows = np.clip((pts[:, 1] * height).astype(int), 0, height - 1)
        if float(changed[rows, cols].mean()) >= BURIED_SHARE:
            gone += 1
    share = ctx.note("buried: share of the earlier small or subject marks covered",
                     gone / len(watch))
    if gone < BURIED_MARKS:
        return None
    return (f"this pass covered {share:.0%} of {len(watch)} earlier small or subject "
            f"marks ({gone} of them): a film is a mass at a depth. Lay it before they go on.")


# -- E: the canvas measurements -------------------------------------------------------
#
# Standing lines under the findings, like `ground:` -- a number, its scale, and where a
# threshold is a judgement it says so. They are measured on the finished canvas here;
# in the engine they would be printed after a pass.

def values_line(session: Session) -> str:
    """Where the picture's values sit, and whether it has a light.

    The 5th to 95th percentile of the values view, and the three clusters the picture
    actually has. Evidence: the pier (no clear light), the heron (nothing light until
    stroke 217), the fogged glass (its two largest areas 0.008 apart).
    """
    view = session.canvas.values(sketch=False).astype(np.float32) / 255.0
    flat = view.reshape(-1)[::17]
    low, high = float(np.percentile(flat, 5)), float(np.percentile(flat, 95))
    centres = _clusters(flat, 3)
    gaps = np.diff(centres)
    return (f"values: {low:.2f}-{high:.2f}, three clusters at "
            + ", ".join(f"{c:.2f}" for c in centres)
            + f" (closest pair {gaps.min():.3f} apart)")


def _clusters(flat: np.ndarray, k: int, rounds: int = 25) -> np.ndarray:
    """Lloyd's algorithm on one dimension: cheap, and it is only ever three clusters."""
    centres = np.percentile(flat, np.linspace(100 / (k + 1), 100 * k / (k + 1), k))
    for _ in range(rounds):
        which = np.abs(flat[:, None] - centres[None, :]).argmin(axis=1)
        moved = np.array([flat[which == i].mean() if np.any(which == i) else centres[i]
                          for i in range(k)])
        if np.allclose(moved, centres, atol=1e-4):
            break
        centres = moved
    return np.sort(centres)


def edges_line(session: Session) -> str:
    """How the picture's edge length divides between hard and soft.

    Finding 13: ``report()`` said *nothing to report* over uniform edge handling, and
    GPT's own verdict names *equally crisp boundaries*. The rise width is measured
    across the gradient: the step the edge crosses, over how fast it crosses it.
    """
    view = session.canvas.values(sketch=False).astype(np.float32) / 255.0
    dy, dx = np.gradient(view)
    grad = np.hypot(dx, dy)
    edge = grad > max(float(np.percentile(grad, 99.0)), 0.01)
    rows, cols = np.nonzero(edge)
    if not len(rows):
        return "edges: nothing with an edge yet"
    keep = np.linspace(0, len(rows) - 1, min(len(rows), 20000)).astype(int)
    rows, cols = rows[keep], cols[keep]
    ux = dx[rows, cols] / np.maximum(grad[rows, cols], 1e-6)
    uy = dy[rows, cols] / np.maximum(grad[rows, cols], 1e-6)
    walk = np.arange(-4, 5)
    height, width = view.shape
    samples = np.stack([
        view[np.clip((rows + uy * t).astype(int), 0, height - 1),
             np.clip((cols + ux * t).astype(int), 0, width - 1)] for t in walk])
    step = samples.max(axis=0) - samples.min(axis=0)
    rise = np.clip(step / np.maximum(grad[rows, cols], 1e-6), 0.5, 12.0)
    return (f"edges: {float((rise < 2.0).mean()):.0%} of edges are under 2 px wide, "
            f"median {float(np.median(rise)):.1f} px")


def pencil_line(session: Session) -> str:
    """Graphite still showing, as a share: the closing checklist's own question."""
    with_sketch = session.canvas.values(sketch=True).astype(np.int16)
    without = session.canvas.values(sketch=False).astype(np.int16)
    share = float((np.abs(with_sketch - without) > 2).mean())
    return f"pencil: {share:.2%} of the canvas still has graphite showing"


def boxes_line(rep: Replay) -> str:
    """The share of the masses whose place is a rectangle (the fogged glass, the pier)."""
    masses = [c for c in rep.calls if c.verb in MASS_VERBS]
    if not masses:
        return "boxes: no masses"
    boxed = sum(1 for c in masses if isinstance(c.place, Region))
    return (f"boxes: {boxed} of {len(masses)} masses were laid in a rectangle "
            f"({boxed / len(masses):.0%})")


def unspent_line(session: Session) -> str:
    """What ``checklist()`` would say about the budget (finding 15)."""
    if session.budget is None:
        return f"unspent: no budget set; {session.stroke_count} marks laid"
    left = session.budget - session.stroke_count
    return (f"unspent: {left} of {session.budget} unspent "
            f"({left / session.budget:.0%}) -- name the weakest passage")


def measurements(rep: Replay) -> list[str]:
    session = rep.session
    if session is None:
        return []
    return [values_line(session), edges_line(session), pencil_line(session),
            boxes_line(rep), unspent_line(session),
            f"ground: {session.canvas.ground_showing():.2%} of the canvas is bare ground"]


# -- rule 2: what the candidates say to the guide's own code blocks --------------------

def probe_guide_blocks() -> dict[str, list[str]]:
    """Run every python block of the guide past every candidate.

    ``LESSONS.md`` rule 2: *a rule that fires on the remedy it names, or on a recipe's
    own code block, is worse than no rule*. A candidate that fires here is not narrowed
    -- either it is wrong, or the block is, and the plan says which it expects
    (``chisel-staircase`` on *a mass built of planes*, whose faces the round fixes in
    the same commit).
    """
    guide = _import_script(ROOT / "scripts" / "check_guide_blocks.py")
    fires: dict[str, list[str]] = {}
    blocks = guide.guide_blocks(echo=False)
    print(f"\n== the candidates against the guide's own {len(blocks)} code blocks ==")
    ran = 0
    for number, (doc, block) in enumerate(blocks, 1):
        if guide.is_pseudo_code(block):
            continue
        rep = Replay(painting=Painting(name=f"block {number}", where=doc))
        with Watcher() as watcher:
            watcher.replay = rep
            with contextlib.redirect_stdout(io.StringIO()):
                watcher.open(f"{doc} block {number}")
                try:
                    exec(compile(guide.PREAMBLE + guide.runnable(block),   # noqa: S102
                                 f"<block {number}>", "exec"), {})
                except Exception:                            # noqa: BLE001, S110
                    pass                                     # check_guide_blocks owns this
                watcher.close()
        ran += 1
        for made in rep.passes:
            for code, lines in made.fires.items():
                fires.setdefault(code, []).append(
                    f"{doc} block {number}: {lines[0]}")
    for code in sorted(CALL_CHECKS) + sorted(PASS_CHECKS) + ["inset-lost"]:
        hit = fires.get(code, [])
        mark = "FIRES" if hit else "silent"
        print(f"  {code:<20} {mark:>6} on {len(hit)} of {ran} blocks"
              + (f"   {hit[0][:88]}" if hit else ""))
    return fires


# -- 2a: the failures the documentation already names ---------------------------------

def new(width: int = 1024, height: int = 768, ground: str = "toned_grey",
        seed: int = 7) -> Session:
    return Session(width, height, texture="linen", ground=ground, seed=seed,
                   timelapse=False, out_dir=OUT)


def _painted(session: Session, before: np.ndarray) -> np.ndarray:
    return np.abs(session.canvas.rgb - before).sum(axis=2) > 1e-3


def _horizontal_share(view: np.ndarray, mask: np.ndarray) -> float:
    """The share of a mass's strong edges that run within ten degrees of horizontal.

    ``CALIBRATION.md``'s own measurement of the staircase, so the numbers below are
    comparable with the ones already written down: the top decile of the Sobel
    magnitude inside the mass, by the angle of its gradient.
    """
    gy, gx = np.gradient(view)
    strength = np.hypot(gx, gy)
    inside = strength[mask]
    if not inside.size:
        return 0.0
    strong = mask & (strength >= float(np.percentile(inside, 90)))
    if not strong.any():
        return 0.0
    # A horizontal edge has a vertical gradient.
    angle = np.degrees(np.arctan2(np.abs(gx[strong]), np.abs(gy[strong])))
    return float((angle <= 10.0).mean())


def probe_staircase() -> None:
    """Finding 1: a chisel down a boundary that is not parallel to its passes.

    ``CALIBRATION.md`` measured this on one painter's lit band and wrote the table
    down; this re-runs that case to the percentage point, and adds the cohort's --
    Kimi's rock faces, which are ``RECIPES.md``'s *a mass built of planes* character
    for character, and whose boundaries slope the other way.
    """
    print("\n== the chisel staircase, re-measured ==")
    band = polygon([(0.470, 0.180), (0.530, 0.180), (0.562, 0.820), (0.502, 0.820)])
    face = polygon([(0.470, 0.745), (0.560, 0.690), (0.650, 0.648), (0.610, 0.760),
                    (0.500, 0.820)])
    print("  share of a mass's strong edges running within 10 degrees of horizontal")
    print(f"  {'case':<22}{'tip':<12}{'size':>7}{'edge':>9}{'horizontal edges':>18}")
    cases = (("the lit band", band, 1120, 860, "vertical",
              (("flat", 0.020), ("flat", 0.010), ("knife", 0.020),
               ("bristle", 0.022), ("bristle", 0.012), ("round_hard", 0.020))),
             ("Kimi's rock face", face, 1024, 768, "axis",
              (("flat", 0.020), ("flat", 0.010), ("bristle", 0.020),
               ("round_hard", 0.020))))
    for label, place, width, height, direction, brushes in cases:
        for tip, size in brushes:
            for edge in ("ragged", "hard"):
                s = new(width, height, ground="toned_warm_grey", seed=41)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    s.block_in(place, tip, "titanium_white", size=size, density=1.0,
                               solid=True, direction=direction, edge=edge,
                               opacity=1.0, pressure="even")
                view = s.canvas.values(sketch=False).astype(np.float32) / 255.0
                mask = _mask(place.inset(size), width, height)
                share = _horizontal_share(view, mask)
                print(f"  {label:<22}{tip:<12}{size:>7}{edge:>9}{share:>17.0%}")
    print("  read: the ordering holds -- a chisel leaves several times the horizontal")
    print("  pass ends a comb or a round tip does -- but the share is the band's as much")
    print("  as the brush's, so it is a comparison and not a constant. `edge=\"hard\"` does")
    print("  not close it: these are pass ends inside the mask, not paint past it.")


def _bare(session: Session) -> np.ndarray:
    """Where the canvas is still within ``10/255`` of its own bare ground.

    ``Canvas.ground_showing``'s own definition, per channel in sRGB, so *a hole* here
    means the same thing as *ground showing* does everywhere else in the project. The
    difference this makes is the whole of B2: any-paint-at-all says a comb leaves
    nothing bare, and the thing a painter sees is the ground coming back through.
    """
    now = linear_to_srgb(session.canvas.composite(impasto=False, sketch=False))
    was = linear_to_srgb(session.canvas.bare())
    return np.abs(now - was).max(axis=2) <= 10.0 / 255.0


def probe_solid_holes() -> None:
    """Finding 2 and B2: what is left bare inside a ``solid=True`` mass, and by what.

    The plan's own check found a ``flat`` leaves nothing at any size and a ``bristle``
    -- ``block_in``'s default brush -- leaves blobs. Run across the grid it turns up a
    third thing neither the painters nor the plan had: **a hole is a contrast, not a
    gap**. The same comb over the same shape leaves nothing measurable when the paint
    is far from the ground in colour and leaves blobs when it is near it, because
    *bare* means within ``10/255`` of the ground -- which is the definition
    ``ground_showing()`` uses and the one a painter's eye uses too.
    """
    print("\n== holes inside a solid mass: which brush, and what closes them ==")
    place = Region(0.10, 0.10, 0.90, 0.90)
    print("  Region(0.10,0.10,0.90,0.90), solid=True, direction=37, 1440x960 on toned_grey")
    print("  bare = within 10/255 of bare ground, a brush in from the outline")
    print(f"  {'brush':<10}{'size':>7}{'density':>9}{'passes':>8}{'bare inside':>13}"
          f"{'blobs':>7}{'largest':>9}")
    grid = ((("flat", 0.04, 1.0), ("flat", 0.06, 1.0))
            + tuple(("bristle", 0.04, d) for d in (0.8, 1.0, 1.2, 1.5))
            + tuple(("bristle", 0.06, d) for d in (0.8, 1.0, 1.2)))
    for brush, size, density in grid:
        share, blobs, largest, passes = _holes_at(place, brush, size, density,
                                                  "toned_grey")
        print(f"  {brush:<10}{size:>7}{density:>9}{passes:>8}{share:>12.4%}"
              f"{blobs:>7}{largest:>9}")
    print("  read: the flat closes at every size. The comb leaves them, `solid=` cannot "
          "close them -- it sets load and load_falloff and nothing else -- and the")
    print("  density that closes them is about 1.2.")

    print("\n  the same call, over three grounds")
    for ground in ("toned_grey", "white", "#2e332c"):
        share, blobs, largest, _ = _holes_at(place, "bristle", 0.04, 0.8, ground)
        print(f"    burnt_umber on {ground:<12} bare {share:7.4%}  {blobs:>3} blobs, "
              f"largest {largest}")
    print("  read: a hole is a contrast, not a gap. The same comb over the same shape "
          "leaves nothing measurable when the paint is far from the ground it was")
    print("  laid over, because *bare* means within 10/255 of that ground -- which is "
          "what ground_showing() means by it, and what an eye means by it.")


def _holes_at(place, brush: str, size: float, density: float,
              ground: str) -> tuple[float, int, int, int]:
    """One cell of the table above: what one solid mass left bare, on one ground."""
    s = new(1440, 960, ground=ground)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        laid = s.block_in(place, brush, "burnt_umber", size=size, density=density,
                          solid=True, direction=37)
    inside = _mask(place.inset(size * 0.8), 1440, 960)
    bare = inside & _bare(s)
    blobs, largest = _blobs(bare)
    return float(bare.sum()) / int(inside.sum()), blobs, largest, len(laid)


def _blobs(mask: np.ndarray) -> tuple[int, int]:
    """How many separate runs of bare canvas there are, and how big the biggest is.

    A flood fill rather than a label pass, because the project takes numpy and pillow
    and nothing else, and a probe may not add a dependency to the engine's own floor.
    """
    if not mask.any():
        return 0, 0
    seen = np.zeros_like(mask)
    count = best = 0
    for r, c in zip(*np.nonzero(mask), strict=False):
        if seen[r, c]:
            continue
        count += 1
        stack, size = [(int(r), int(c))], 0
        while stack:
            y, x = stack.pop()
            if not (0 <= y < mask.shape[0] and 0 <= x < mask.shape[1]):
                continue
            if seen[y, x] or not mask[y, x]:
                continue
            seen[y, x] = True
            size += 1
            stack += [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
        best = max(best, size)
    return count, best


def probe_smudge_thumbprint() -> None:
    """Finding 3: a smudge across a boundary drags a thumbprint of the light mass in.

    Measured as *how far in*: a smudge run along a join softens it a brush either side,
    and one run across it carries the light mass the length of its own path.
    """
    print("\n== a smudge across a boundary, against one along it ==")
    print("  a hard step from 0.20 to 0.78 across the middle, one smudge at size=0.04")
    print(f"  {'path':<16}{'px lifted in the dark':>23}{'deepest, in brushes':>21}")
    for label, path in (("along the join", [(0.20, 0.50), (0.80, 0.50)]),
                        ("across it", [(0.50, 0.30), (0.50, 0.70)]),
                        ("at 30 degrees", [(0.30, 0.42), (0.70, 0.58)])):
        s = new(ground="white")
        p = s.palette
        p["dark"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.5), 0.20)
        p["lit"] = p.at_value(p.mix("yellow_ochre", "titanium_white", 0.5), 0.78)
        for place, colour in ((Region(0.0, 0.0, 1.0, 0.5), "dark"),
                              (Region(0.0, 0.5, 1.0, 1.0), "lit")):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                s.block_in(place, "flat", colour, size=0.06, solid=True, opacity=1.0,
                           pressure="even", direction="horizontal", edge="hard")
        s.dry()
        before = s.canvas.values(sketch=False).astype(np.float32) / 255.0
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            s.smudge(path, size=0.04)
        after = s.canvas.values(sketch=False).astype(np.float32) / 255.0
        join = int(0.5 * 768)
        lift = (after - before)[:join] > 0.05
        rows = np.nonzero(lift.any(axis=1))[0]
        deep = (join - int(rows.min())) / (0.04 * 1024) if len(rows) else 0.0
        print(f"  {label:<16}{int(lift.sum()):>23}{deep:>21.1f}")
    print("  read: along the join the lift stops about a brush in; across it, it is "
          "carried the length of the path.")


def probe_glaze_far() -> None:
    """Finding 4: how far a film sits from what it lands on, before it is a new mass."""
    print("\n== a film's own shift, against the distance it was mixed at ==")
    print("  one glaze over a mass at 0.30, opacity=0.15, 1024x768")
    print(f"  {'film value':>11}{'shift':>9}{'new mass?':>11}")
    for target in (0.35, 0.45, 0.55, 0.70, 0.85):
        s = new(ground="white")
        p = s.palette
        p["under"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.5), 0.30)
        p["film"] = p.at_value(p.mix("yellow_ochre", "titanium_white", 0.5), target)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            s.block_in(Region(0.1, 0.1, 0.9, 0.9), "flat", "under", size=0.08,
                       solid=True, opacity=1.0, pressure="even")
        s.dry()
        before = s.canvas.values(sketch=False).astype(np.float32) / 255.0
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            s.glaze([(0.2, 0.5), (0.8, 0.5)], "film", size=0.30, opacity=0.15)
        after = s.canvas.values(sketch=False).astype(np.float32) / 255.0
        moved = np.abs(after - before)
        shift = float(moved[moved > 0.004].mean()) if (moved > 0.004).any() else 0.0
        print(f"  {target:>11.2f}{shift:>9.3f}{'yes' if shift >= GLAZE_NEW_MASS else 'no':>11}")
    print(f"  read: at opacity=0.15 the {GLAZE_NEW_MASS:.2f} that makes a new mass is a "
          f"film mixed about 0.40 off what it lands on.")


def probe_scumble_spill() -> None:
    """Finding 8 and B17: what a banded scumble paints, against the band it was given."""
    print("\n== a banded scumble's reach, against its own band (B17) ==")
    band = Region(0.10, 0.40, 0.90, 0.60)                    # 0.20 tall, as B17 measured
    print("  Region(0.10,0.40,0.90,0.60), n=8, the auto brush, 1024x768")
    print(f"  {'direction':>12}{'auto brush':>12}{'painted/band':>14}{'outside':>10}")
    for direction in ("axis", 0, 30, 60):
        s = new(ground="white")
        before = s.canvas.rgb.copy()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            laid = s.scumble(band, "burnt_umber", "titanium_white", 8,
                             direction=direction)
        painted = _painted(s, before)
        mask = _mask(band, 1024, 768)
        size = float(laid[0].params.get("size", 0.0))
        print(f"  {str(direction):>12}{size:>12.3f}"
              f"{painted.sum() / mask.sum():>13.2f}x"
              f"{float((painted & ~mask).sum()) / max(painted.sum(), 1):>9.0%}")
    print("  read: the step is measured on the bounding box, so an oblique angle inflates it.")


# -- 2d: the eighteen bugs ------------------------------------------------------------
#
# Every row of workstream B, as something that runs. The plan checked them by reading
# the code and painting the cheap ones on a scratch canvas; this is that, made
# repeatable, so the round can be re-checked against a changed engine rather than
# against a paragraph.

def _raises(fn) -> str:
    try:
        fn()
    except Exception as exc:                                 # noqa: BLE001 - the point
        return f"{type(exc).__name__}: {exc}"
    return "(no error)"


def probe_b1_clip() -> None:
    """B1: ``clip=`` is a parameter of ``stroke`` only, and the error does not say so."""
    print("\n== B1: clip= on the verbs that lay paint ==")
    band = Region(0.2, 0.2, 0.8, 0.5)
    hold = polygon([(0.2, 0.2), (0.8, 0.2), (0.8, 0.5), (0.2, 0.5)])
    for label, call in (
        ("stroke(clip=)", lambda: new(400, 300).stroke(
            [(0.2, 0.3), (0.8, 0.3)], "flat", "burnt_umber", clip=hold)),
        ("dab(clip=)", lambda: new(400, 300).dab(0.5, 0.3, clip=hold)),
        ("glaze(clip=)", lambda: new(400, 300).glaze(
            [(0.2, 0.3), (0.8, 0.3)], "burnt_umber", clip=hold)),
        ("smudge(clip=)", lambda: new(400, 300).smudge(
            [(0.2, 0.3), (0.8, 0.3)], clip=hold)),
        ("block_in(clip=)", lambda: new(400, 300).block_in(
            band, "flat", "burnt_umber", clip=hold)),
        ("sweep(clip=)", lambda: new(400, 300).sweep(
            [(0.2, 0.3), (0.8, 0.3)], "flat", "burnt_umber", clip=hold)),
        ("cover(clip=)", lambda: new(400, 300).cover(band, "burnt_umber", clip=hold)),
        ("scumble(clip=)", lambda: new(400, 300).scumble(
            band, "burnt_umber", "titanium_white", 6, clip=hold)),
        ("scumble(edge=)", lambda: new(400, 300).scumble(
            band, "burnt_umber", "titanium_white", 6, edge="hard")),
    ):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            said = _raises(call)
        print(f"  {label:<18} {said[:96]}")
    print("  read: four verbs take it, four cannot, and the error names neither "
          "stroke(clip=) nor edge=\"hard\".")


def probe_b3_b4_timelapse() -> None:
    """B3: a rehearsal copy records no frames. B4: the frames are 360 px, unreachably."""
    print("\n== B3, B4: the time-lapse ==")
    s = new(1440, 960)
    s.timelapse = True
    s.stroke([(0.2, 0.3), (0.8, 0.3)], "flat", "burnt_umber")
    s.capture_frame()
    copy = s.scratch()
    print(f"  the painting holds {len(s.history._frames)} frames; "
          f"its rehearsal copy holds {len(copy.history._frames)} "
          f"(timelapse={copy.timelapse})")
    print(f"  timelapse_gif on the copy -> {_raises(lambda: copy.timelapse_gif(OUT / 'x.gif'))[:120]}")
    if s.history._frames:
        frame = s.history._frames[0]
        print(f"  a frame of a {s.canvas.width}x{s.canvas.height} painting is "
              f"{frame.shape[1]}x{frame.shape[0]} px, and nothing on Session or the CLI "
              f"can ask for another size")
    print("  read: the first remedy the error gives -- create the session with "
          "timelapse=True -- is the one thing that was already true.")


def probe_b5_plans() -> None:
    """B5: what ``cost``/``preview``/``rehearse`` can be handed, and what prices silently."""
    print("\n== B5: the plan object, and what it knows ==")
    s = new(400, 300)
    s.palette["pale"] = s.palette.tint("yellow_ochre", 0.5)
    band = Region(0.2, 0.2, 0.8, 0.5)
    plans = {
        "a stroke": {"points": [(0.2, 0.3), (0.8, 0.3)], "brush": "flat",
                     "color": "burnt_umber", "size": 0.05},
        "a mass": {"region": band, "brush": "flat", "color": "burnt_umber",
                   "size": 0.05},
        "a sweep": {"edge": [(0.2, 0.3), (0.8, 0.3)], "brush": "flat",
                    "color": "burnt_umber", "depth": 0.1},
        "a scumble": {"shape": band, "color_a": "burnt_umber", "color_b": "pale",
                      "n": 8, "kind": "scumble"},
        "a cover": {"place": band, "color": "burnt_umber", "kind": "cover"},
    }
    for label, plan in plans.items():
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            priced = _raises(lambda plan=plan, label=label:
                         print(f"  {label:<12} cost {s.cost([plan])}", end=""))
        print("" if priced == "(no error)" else f"  {label:<12} {priced[:88]}")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        quoted = s.cost([{"shape": band, "color_a": "burnt_umber", "color_b": "pale",
                          "n": 8, "kind": "scumble"}])
        real = len(new(400, 300).scumble(band, "burnt_umber",
                                         s.palette["pale"], 8))
    print(f"  a scumble-shaped plan quotes {quoted} and the call lays {real}")
    print("  read: the library prices what the server already refuses -- a quote for a "
          "plan that cannot be painted.")


def probe_b6_records() -> None:
    """B6: ``replay(upto=)``, ``undo(n)`` and ``log(last=)`` count records, not strokes."""
    print("\n== B6: records or strokes ==")
    s = new(400, 300)
    s.pencil([(0.1, 0.1), (0.9, 0.9)])
    s.stroke([(0.2, 0.3), (0.8, 0.3)], "flat", "burnt_umber")
    s.stroke([(0.2, 0.5), (0.8, 0.5)], "flat", "burnt_umber")
    s.dry()
    print(f"  {len(s.history.records)} log records, of which {s.stroke_count} are strokes")
    s.undo(1)
    print(f"  after undo(1): {len(s.history.records)} records, {s.stroke_count} strokes "
          f"-- undo(1) scraped back the dry, and no paint came off")
    print(f"  log(last=3) covers {len(s.log(last=3).splitlines())} lines of a log holding "
          f"{len(s.history.records)} records, {s.stroke_count} of them paint")
    print("  read: all three count records. Only replay's docstring says so.")


def probe_b7_cp1252() -> None:
    """B7: what a painter's own ``print(easel.docs.read(...))`` does on a cp1252 console."""
    print("\n== B7: the shipped documents, through cp1252 ==")
    total = 0
    for name in sorted(easel.docs.DOCUMENTS):
        text = easel.docs.read(name)
        bad: dict[str, int] = {}
        for ch in text:
            try:
                ch.encode("cp1252")
            except UnicodeEncodeError:
                bad[ch] = bad.get(ch, 0) + 1
        total += sum(bad.values())
        shown = ", ".join(f"{ch!r} x{n}" for ch, n in sorted(bad.items(),
                                                             key=lambda kv: -kv[1]))
        print(f"  {name:<14} {sum(bad.values()):>4} characters outside cp1252"
              + (f"   {shown}" if bad else ""))
    source = sum(1 for path in (ROOT / "src" / "easel").glob("*.py")
                 for ch in path.read_text(encoding="utf-8") if ord(ch) > 127)
    print(f"  {total} in the documents; {source} non-ASCII characters in src/easel/")
    print("  read: the tool's own output is safe; reading a document from Python is not.")


def probe_b8_hard_edges() -> None:
    """B8: ``edge="hard"`` leaves pass-end bites just inside a slanted outline.

    Over a range of slopes rather than one, because the plan's own check found the
    share on a single outline and the share is the outline's as much as the brush's.
    """
    print("\n== B8: what is left bare inside a hard edge, and what closes it ==")
    print("  a mass whose left and right edges slope, solid=True, 1024x768;")
    print("  the share of the 3 px strip inside the outline that came back bare")
    print(f"  {'brush':<12}{'slope':>7}{'ragged':>10}{'hard':>10}{'hard, overhang=2':>19}")
    for brush in ("flat", "round_hard"):
        for slope in (0, 10, 20, 30):
            lean = math.tan(math.radians(slope)) * 0.6
            place = polygon([(0.30, 0.20), (0.70, 0.20),
                             (0.70 + lean, 0.80), (0.30 + lean, 0.80)])
            shares = []
            for edge, overhang in (("ragged", None), ("hard", None), ("hard", 2.0)):
                s = new(ground="white")
                before = s.canvas.rgb.copy()
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    s.block_in(place, brush, "burnt_umber", size=0.05, density=1.0,
                               solid=True, edge=edge, overhang=overhang,
                               direction="vertical")
                painted = _painted(s, before)
                strip = (_mask(place, 1024, 768)
                         & ~_mask(place.inset(3.0 / 1024), 1024, 768))
                shares.append(float((strip & ~painted).sum()) / max(int(strip.sum()), 1))
            print(f"  {brush:<12}{slope:>6}d{shares[0]:>9.2%}{shares[1]:>10.2%}"
                  f"{shares[2]:>19.3%}")
    print("  read: the bites are the pass ends arriving at part pressure, so they are "
          "worst on a round tip and on a slope; two brushes of overhang closes them.")


def probe_b9_subject_share() -> None:
    """B9: the subject's share counts free signature marks as spent."""
    print("\n== B9: the subject's share, against what was paid for ==")
    s = new(400, 300)
    for i in range(5):
        s.stroke([(0.2, 0.2 + i * 0.1), (0.5, 0.2 + i * 0.1)], "flat", "burnt_umber",
                 note="subject")
    for _ in range(3):
        s.stroke([(0.7, 0.8), (0.75, 0.85)], "liner", "burnt_umber", note="signature")
    s.pencil([(0.1, 0.1), (0.9, 0.9)])
    line = [ln for ln in s.report().splitlines() if "subject:" in ln]
    print("  five subject marks, three signature marks, one pencil line")
    print(f"  stroke_count (what the budget charges): {s.stroke_count}")
    print(f"  report says: {line[0].strip() if line else '(nothing)'}")
    print("  read: History.stroke_count exempts the signature; report() builds its own "
          "denominator and does not.")


def probe_b10_import_name() -> None:
    """B10: ``import easel_paint`` -- the one import name that is certainly this project's."""
    print("\n== B10: the import name ==")
    print(f"  import easel        -> {easel.__file__}")
    print(f"  import easel_paint  -> {_raises(lambda: importlib.import_module('easel_paint'))}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8").splitlines()
    install = next(i for i, line in enumerate(readme) if "pip install" in line)
    imports = [i for i, line in enumerate(readme) if re.search(r"\b(from|import) easel\b", line)]
    nearest = min(imports, key=lambda i: abs(i - install)) if imports else None
    print(f"  README: the install line is line {install + 1}; its nearest import is "
          + (f"line {nearest + 1}, {abs(nearest - install)} lines away" if nearest is not None
             else "nowhere on the page"))
    for name in ("llms.txt", "src/easel/__init__.py"):
        text = (ROOT / name).read_text(encoding="utf-8")
        print(f"  {name:<22} says `from easel import`: "
              f"{'yes' if 'from easel import' in text else 'no'}")
    print("  read: the distribution is easel-paint, the package is easel, and PyPI "
          "carries an unrelated `easel`.")


def probe_b11_b12_b13_b14() -> None:
    """B11 a ground as a colour, B12 the named regions, B13 a 0-255 list, B14 solid=."""
    print("\n== B11: a ground name used as a colour, and the other way round ==")
    s = new(400, 300, ground="toned_grey")
    print(f"  palette['toned_grey'] -> {_raises(lambda: s.palette['toned_grey'])[:150]}")
    print(f"  Session(ground='ultramarine') -> "
          f"{_raises(lambda: Session(40, 30, ground='ultramarine', out_dir=OUT))[:110]}")
    print(f"  the ground as a colour: ground_name={s.canvas.ground_name!r}, "
          f"and the only route to its colour is s.sample() of bare canvas")

    print("\n== B12: what the named regions actually cover ==")
    for name in ("top", "bottom", "left", "right", "center", "lower-band", "lower-half"):
        r = easel.region(name)
        print(f"  {name:<12} x {r.x0:.3f}-{r.x1:.3f}  y {r.y0:.3f}-{r.y1:.3f}"
              f"   ({r.width:.2f} x {r.height:.2f} of the canvas)")
    print("  read: `bottom` is a ninth, not a third. `lower-band` is the foreground band.")

    print("\n== B13: a colour given as 0-255 integers ==")
    s = new(400, 300)
    for value in ([200, 100, 50], (0.78, 0.39, 0.20), "#c86432"):
        said = _raises(lambda v=value: s.palette.__setitem__("x", v))
        got = s.palette.hex(s.palette["x"]) if said == "(no error)" else "-"
        print(f"  {str(value):<22} {said[:60]:<62} -> {got}")
    print("  read: a documented trap the engine can detect is a bug.")

    print("\n== B14: where solid= is accepted ==")
    band = Region(0.2, 0.2, 0.8, 0.5)
    for label, call in (
        ("block_in(solid=True)", lambda: new(400, 300).block_in(
            band, "flat", "burnt_umber", solid=True)),
        ("cover(solid=True)", lambda: new(400, 300).cover(
            band, "burnt_umber", solid=True)),
        ("stroke(solid=True)", lambda: new(400, 300).stroke(
            [(0.2, 0.3), (0.8, 0.3)], "flat", "burnt_umber", solid=True)),
        ("sweep(solid=True)", lambda: new(400, 300).sweep(
            [(0.2, 0.3), (0.8, 0.3)], "flat", "burnt_umber", solid=True)),
        ("scumble(solid=True)", lambda: new(400, 300).scumble(
            band, "burnt_umber", "titanium_white", 6, solid=True)),
    ):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            print(f"  {label:<22} {_raises(call)[:96]}")
    print("  read: it is load=1.0, load_falloff=0.0 everywhere, and it is the clause "
          "painters type by hand most often.")


def probe_b15_cost_per_stroke() -> None:
    """B15: where 30-45 s for 500-800 marks goes. Fixed cost per stroke; nothing quadratic."""
    print("\n== B15: what a stroke costs before any paint lands ==")
    for width, height in ((1024, 768), (1440, 960)):
        s = Session(width, height, texture="linen", ground="toned_grey", seed=7,
                    timelapse=False, out_dir=OUT)
        snap = _time(lambda s=s: s.canvas.snapshot())
        frame = _time(lambda s=s: s.canvas.thumbnail_srgb8(360))
        mark = _time(lambda s=s: s.stroke([(0.2, 0.3), (0.8, 0.32)], "bristle",
                                          "burnt_umber", size=0.06))
        held = s.canvas.rgb.nbytes + s.canvas.wetness.nbytes * 3
        print(f"  {width}x{height}: snapshot {snap * 1e3:6.1f} ms, a 360 px frame "
              f"{frame * 1e3:6.1f} ms, one wide bristle pass {mark * 1e3:7.1f} ms")
        print(f"             one snapshot is {held / 1e6:.0f} MB, and "
              f"{MAX_SNAPSHOTS} are kept -- about "
              f"{held * MAX_SNAPSHOTS / 1e6:.0f} MB resident; snapshot plus frame is "
              f"{(snap + frame) * 1e3:.0f} ms before a dab lands")
    print("  read: fixed cost per stroke, nothing quadratic, and the frame is most of "
          "it -- the painter's 30-45 s for 500-800 marks is this, plus the per-dab")
    print("  loop, which dominates the wide ones. The numbers are the machine's; what "
          "does not move is the shape -- a frame costs an order more than a snapshot.")


def _time(fn, rounds: int = 3) -> float:
    best = math.inf
    for _ in range(rounds):
        started = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - started)
    return best


def probe_b16_rehearsal() -> None:
    """B16: easier calibration of size, load and pressure before committing.

    A feature request rather than a bug, so what there is to measure is what it would
    be built on: a rehearsal is free against the budget, and a sheet of the same mark
    at several sizes is today several rehearsals of one mark.
    """
    print("\n== B16: calibrating a mark before committing it ==")
    s = new(400, 300)
    s.stroke([(0.1, 0.2), (0.9, 0.2)], "flat", "burnt_umber")
    plan = [{"points": [(0.1, 0.5), (0.9, 0.5)], "brush": "bristle",
             "color": "burnt_umber", "size": 0.04}]
    before = s.stroke_count
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.rehearse(plan)
    print(f"  the painting spent {before} before a rehearsal and {s.stroke_count} after")
    print(f"  rehearse(vary=) -> "
          f"{_raises(lambda: s.rehearse(plan, vary={'size': [0.02, 0.04]}))[:96]}")
    sizes = (0.01, 0.02, 0.04, 0.08)
    print(f"  one sheet of {len(sizes)} sizes is {len(sizes)} rehearsals today, each "
          f"rendering the whole canvas")
    print("  read: free, and the thing a painter actually wants -- one labelled sheet "
          "of the same mark, in place -- is not one call.")


def probe_b18_rings() -> None:
    """B18: what printed the concentric rings on GLM's wall.

    The calls are gone -- the first takes of ``pass1b.py`` and ``pass2.py`` were
    overwritten and their marks undone -- so this is a reconstruction, and
    ``paintings/GLM/terminal_window/rings/`` is what it has to match. **The patch is
    not gone**: the prelude still carries the original ``halo = blob(span("C1","G6"))``
    beside the ``halo2 = blob(span("C2","F4"))`` that take three replaced it with, and
    the larger one overshoots the glass onto the wall exactly where frame 6 puts the
    rings.

    Two things are measured here: what value step per ring prints a contour, and
    whether the bezel being wet under them is needed to make one band as dark as the
    bezel -- which is the question that decides whether ``wet-under`` (D2) is built.
    """
    print("\n== B18: GLM's rings, reconstructed against its own frames ==")
    glm = next(e for e in CORPUS if e.name == "glm")
    built = replay(glm, keep_canvas=False, limit=2)          # draw.py and pass1a.py
    session = built.session
    if session is None:
        print("  (GLM would not rebuild)")
        return
    work = _glm_names(glm)
    patch, palette = work["halo"], session.palette
    bezel, bezel_colour = work["bezel"], palette["bezel"]
    print(f"  the prelude's own first-take patch: {patch!r}")
    print(f"  {'span':>12}{'n':>4}{'step/ring':>11}{'value steps across it':>23}"
          f"{'darkest band':>14}{'wet bezel moves it':>20}")
    for low, high in ((0.20, 0.26), (0.14, 0.30), (0.14, 0.35)):
        for n in (5, 10):
            views = {}
            for wet in (False, True):
                s = replay(glm, keep_canvas=False, limit=2).session
                p = s.palette
                p["a"] = p.at_value(p.mix("viridian", "burnt_umber", 0.40), low)
                p["b"] = p.at_value(p.mix("viridian", "burnt_umber", 0.40), high)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    s.block_in(bezel, "flat", bezel_colour, size=0.035, solid=True,
                               opacity=1.0, pressure="even", edge="clean")
                    if not wet:
                        s.dry()
                    s.scumble(patch, "a", "b", n, direction="inward")
                views[wet] = s.canvas.values(sketch=False).astype(np.float32) / 255.0
            mask = patch.mask(1024, 768)
            steps, darkest = _contours(views[False], mask)
            moved = float(np.abs(views[True] - views[False])[mask].max())
            print(f"  {f'{low:.2f}-{high:.2f}':>12}{n:>4}{abs(high - low) / (n - 1):>11.3f}"
                  f"{steps:>23}{darkest:>14.2f}{moved:>20.3f}")
    print(f"  the bezel itself reads {palette.value_of(bezel_colour):.2f}")
    print("  read, two answers. The rings are the inward scumble's own contours: a step")
    print("  of 0.04 a ring prints eight visible bands across the patch, and the tight")
    print("  low-contrast take that replaced it prints three. And the wet bezel is not")
    print("  innocent -- laying the rings over it wet moves pixels by up to 0.13, which")
    print("  is past the 0.10 that makes a new mass. Both halves of the round's reading")
    print("  survive; neither of the painter's does.")


def _glm_names(entry: Painting) -> dict:
    """The shapes GLM's prelude builds, evaluated once against a throwaway session."""
    session = Session(1024, 768, texture="linen", ground="#2e332c", seed=7,
                      timelapse=False, out_dir=OUT)
    ns = _namespace(session, entry.folder / "prelude.py")
    exec(compile((entry.folder / "prelude.py").read_text(encoding="utf-8"),   # noqa: S102
                 "prelude.py", "exec"), ns)
    return ns


def _contours(view: np.ndarray, mask: np.ndarray) -> tuple[int, float]:
    """How many value steps a patch has across it, and how dark its darkest band is.

    A contour map read as a number: the values inside the patch, binned at the
    ``0.02`` a step has to clear to be visible, counting the bins that hold a real
    share of the patch.
    """
    inside = view[mask]
    if not inside.size:
        return 0, 0.0
    counts, edges = np.histogram(inside, bins=np.arange(0.0, 1.02, 0.02))
    real = counts > 0.02 * inside.size
    darkest = float(edges[np.argmax(real)]) if real.any() else float(inside.min())
    return int(real.sum()), darkest


# -- F: the default moves, each behind its probe --------------------------------------

def probe_defaults(replays: list[Replay]) -> None:
    """Workstream F: five candidate moves, and what each would cost the corpus.

    Two numbers per row. What the move buys, measured on a scratch canvas; and **how
    many committed calls would move**, counted over the corpus -- because a default
    that no committed painting relies on is cheap to move and one that half of them
    lean on is not.
    """
    print("\n== F: the default moves, and what the corpus leans on ==")
    calls = [c for rep in replays for c in rep.calls]

    print("\n  F1. cover() -> edge=\"hard\"")
    patch = Region(0.40, 0.40, 0.60, 0.55)
    for edge in ("ragged", "clean", "hard"):
        s = new(ground="white")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            s.block_in(Region(0.0, 0.0, 1.0, 1.0), "flat", "burnt_umber", size=0.12,
                       solid=True)
            s.dry()
            before = s.canvas.rgb.copy()
            s.cover(patch, "titanium_white", size=0.06, edge=edge)
        painted = _painted(s, before)
        asked = _mask(patch, 1024, 768)
        print(f"     edge={edge:<7} {painted.sum() / asked.sum():5.2f}x the area it was "
              f"handed")
    moving = [c for c in calls if c.verb == "cover"
              and str(c.bound.get("edge", "ragged")) == "ragged"]
    print(f"     committed cover() calls that would move: {len(moving)} of "
          f"{sum(1 for c in calls if c.verb == 'cover')}")

    print("\n  F2. a round tip on block_in/sweep -> pressure=\"even\"")
    moving = [c for c in calls if c.verb in ("block_in", "sweep")
              and c.brush in ("round_hard", "round_soft", "liner")
              and c.bound.get("pressure") == "taper"]
    print(f"     committed calls that would move: {len(moving)}")
    for c in moving[:4]:
        print(f"       {c.verb}({c.brush}) at line {c.line}")

    print("\n  F3. a banded scumble -> load=1.0, load_falloff=0.0")
    band = Region(0.10, 0.40, 0.90, 0.60)
    for label, kw in (("as shipped", {}),
                      ("with the clause", {"load": 1.0, "load_falloff": 0.0})):
        s = new(ground="toned_grey")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            s.scumble(band, "burnt_umber", "titanium_white", 8, **kw)
        view = s.canvas.values(sketch=False).astype(np.float32) / 255.0
        mask = _mask(band, 1024, 768)
        bare = float((mask & _bare(s)).sum()) / int(mask.sum())
        down = view[mask.any(axis=1)][:, int(0.2 * 1024):int(0.8 * 1024)].mean(axis=1)
        ripple = float(np.abs(np.diff(down, n=2)).mean())
        print(f"     {label:<16} bare {bare:.2%}, ripple {ripple:.4f}")
    typed = [c for c in calls if c.verb == "scumble"
             and c.bound.get("direction") != "inward"
             and float(c.bound.get("load") or 0.0) >= 1.0]
    banded = [c for c in calls if c.verb == "scumble"
              and c.bound.get("direction") != "inward"]
    print(f"     committed banded scumbles that type the clause by hand: "
          f"{len(typed)} of {len(banded)}")

    print("\n  F4. a scumble with a flat -> halved jitter/size_jitter")
    for label, kw in (("as shipped", {}),
                      ("halved", {"jitter": 0.01, "size_jitter": 0.04})):
        s = new(ground="toned_grey")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            s.scumble(band, "burnt_umber", "titanium_white", 8, brush="flat", **kw)
        view = s.canvas.values(sketch=False).astype(np.float32) / 255.0
        rows = view[int(0.42 * 768):int(0.58 * 768), int(0.2 * 1024):int(0.8 * 1024)]
        down = rows.mean(axis=1)
        # The ripple, not the ramp: a graded band is *meant* to change down its own
        # normal, so what a scallop shows up in is the second difference.
        print(f"     {label:<16} ripple down the band "
              f"{float(np.abs(np.diff(down, n=2)).mean()):.4f}, scallop across it "
              f"{float(np.abs(np.diff(rows.mean(axis=0), n=2)).mean()):.4f}")
    flats = [c for c in calls if c.verb == "scumble" and c.brush == "flat"]
    print(f"     committed scumbles laid with a flat: {len(flats)}")

    print("\n  F5. edge=\"hard\" -> two brushes of overhang")
    hard = [c for c in calls if str(c.bound.get("edge", "")) == "hard"]
    named = [c for c in hard if c.bound.get("overhang") is not None]
    print(f"     committed calls at edge=\"hard\": {len(hard)}, of which "
          f"{len(named)} already name an overhang; {len(hard) - len(named)} would move")
    print("     what it buys is in the B8 table above.")


# -- the tables ------------------------------------------------------------------------

def report_corpus(replays: list[Replay]) -> None:
    print("\n== the corpus, rebuilt ==")
    print(f"  {'painting':<12}{'passes':>7}{'marks':>7}{'spent':>7}{'page':>7}"
          f"{'notices':>9}{'findings':>10}{'seconds':>9}  rebuild")
    for rep in replays:
        notices = sum(len(p.notices) for p in rep.passes)
        findings = sum(len(p.findings) for p in rep.passes)
        marks = sum(p.marks for p in rep.passes)
        state = ("matches" if rep.matched else
                 ("not claimed" if not rep.painting.rebuilds else "OFF"))
        if rep.errors:
            state += f" ({len(rep.errors)} errors)"
        print(f"  {rep.painting.name:<12}{len(rep.passes):>7}{marks:>7}{rep.spent:>7}"
              f"{rep.painting.spent:>7}{notices:>9}{findings:>10}{rep.seconds:>8.0f}s"
              f"  {state}")
    for rep in replays:
        for line in rep.errors[:3]:
            print(f"  ! {rep.painting.name}: {line[:120]}")
    passes = sum(len(rep.passes) for rep in replays)
    print(f"  {len(replays)} paintings, {passes} passes, "
          f"{sum(rep.spent for rep in replays)} strokes paid for")


def report_noise(replays: list[Replay]) -> None:
    """What the tool says today, per pass: the baseline every candidate is budgeted against.

    ``LESSONS.md`` rule 7 -- *a warning that fires on almost every pass is a warning
    nobody reads* -- as a number, for the rules that already exist. The bars rule is
    the one the plan says taught two painters to skim.
    """
    print("\n== the noise budget, as it stands today ==")
    passes = [p for rep in replays for p in rep.passes]
    painted = [p for p in passes if p.marks]
    counted: dict[str, int] = {}
    for made in painted:
        for line in made.findings:
            counted[_rule_of(line)] = counted.get(_rule_of(line), 0) + 1
        for line in made.notices:
            counted["! " + _rule_of(line)] = counted.get("! " + _rule_of(line), 0) + 1
    print(f"  {len(painted)} passes that laid paint, of {len(passes)}")
    print(f"  {'rule':<44}{'passes':>8}{'share':>8}")
    for rule, count in sorted(counted.items(), key=lambda kv: -kv[1]):
        print(f"  {rule[:43]:<44}{count:>8}{count / len(painted):>8.0%}")
    quiet = sum(1 for p in painted if not p.findings and not p.notices)
    lines = [len(p.findings) + len(p.notices) for p in painted]
    print(f"  {quiet} of {len(painted)} passes said nothing at all "
          f"({quiet / len(painted):.0%}); the median pass prints "
          f"{float(np.median(lines)):.0f} lines, the busiest {max(lines)}")
    print("  read: the plan's target is fewer than three lines on a median pass.")


_RULES = (
    ("long marks run within", "bars: a stack of passes at one angle"),
    ("are {brush} at size", "one brush at one size for a whole pass"),
    ("marks at stepping colours", "a graded passage laid too narrow"),
    ("bristle under size", "a loaded comb under the bristle floor"),
    ("inside the painting's first", "detail before the masses are down"),
    ("small marks with a round tip", "round tips printing one disc"),
    ("pressure list on a", "a pressure list on a chisel"),
    ("tip changes the paint, not the width", "pressure changes the paint, not the width"),
    ("scumble on this shape", "scumble: passes shorter than the brush"),
    ("wide on a band", "scumble: a brush wider than the band"),
    ("wide on a patch", "scumble: a brush wider than the patch's rings"),
    ("edge='clean') at size", "a clean edge on a narrow mass"),
    ("is not a brush field", "an override that is not a brush field"),
    ("pixels wide on this canvas", "a tip too small to deposit paint"),
    ("with a round tip", "a round tip blocking in a feature"),
    ("is past the 0.03 where", "a smudge past the size that buys anything"),
    ("is averaging", "sample() averaging over a mixed area"),
    ("direction= left off", "a shaped mass with direction= left off"),
    ("cross the shape", "a mass whose passes cross it"),
)


def _rule_of(line: str) -> str:
    """Which rule a line came from, by the phrase only that rule prints."""
    for needle, name in _RULES:
        if needle.replace("{brush}", "") in line or needle in line:
            return name
    return line.split(":")[0][:40]


def report_candidates(replays: list[Replay], guide: dict[str, list[str]]) -> None:
    """The table step 2 exists to produce: what every candidate would cost, in lines.

    *Passes* is how many passes of the corpus it fires on and *share* is that against
    the passes that laid paint -- ``LESSONS.md`` rule 7's own number, whose ceiling the
    plan puts at about one pass in six for a habit rule. *Guide* is rule 2: a candidate
    that fires on the guide's own code blocks is telling a painter doing the right
    thing that they are wrong.
    """
    print("\n== the candidates, over the corpus ==")
    passes = [p for rep in replays for p in rep.passes if p.marks]
    print(f"  {len(passes)} passes that laid paint, over {len(replays)} paintings")
    print(f"  {'candidate':<20}{'from':>5}{'fires':>7}{'passes':>8}{'share':>7}"
          f"{'guide':>7}  paintings")
    for code in list(CALL_CHECKS) + list(PASS_CHECKS) + ["inset-lost"]:
        fired = [p for p in passes if code in p.fires]
        times = sum(len(p.fires[code]) for p in fired)
        where = sorted({p.painting for p in fired})
        blocks = len(guide.get(code, []))
        print(f"  {code:<20}{FROM[code]:>5}{times:>7}{len(fired):>8}"
              f"{len(fired) / max(len(passes), 1):>7.0%}{blocks or '-':>7}  "
              + ", ".join(where[:6]) + (" ..." if len(where) > 6 else ""))
    print("  read: a habit rule over about one pass in six is narrowed, made said-once")
    print("  or demoted to a measurement; one that fires on a guide block is wrong,")
    print("  or the block is, and the round has to say which.")


def report_samples(replays: list[Replay]) -> None:
    """Every number the candidates measured, fired or not -- where a threshold comes from."""
    print("\n== what the candidates measured, over the whole corpus ==")
    pooled: dict[str, list[float]] = {}
    for rep in replays:
        for name, values in rep.samples.items():
            pooled.setdefault(name, []).extend(values)
    print(f"  {'measurement':<58}{'n':>5}{'median':>9}{'p90':>9}{'max':>9}")
    for name, values in sorted(pooled.items()):
        arr = np.array(values)
        print(f"  {name[:57]:<58}{len(arr):>5}{np.median(arr):>9.3f}"
              f"{np.percentile(arr, 90):>9.3f}{arr.max():>9.3f}")


def report_measurements(replays: list[Replay]) -> None:
    """Workstream E, on every finished painting: the standing lines, with their numbers."""
    print("\n== E: the measurement lines, on the finished canvases ==")
    done = [rep for rep in replays if rep.session is not None]
    for rep in done:
        print(f"  {rep.painting.name}")
        for line in measurements(rep):
            print(f"    {line}")
    if not done:
        return
    # Findings 11, 13 and 15, as the corpus answers them -- and the cohort apart
    # from the paintings that came before it, because two of the three findings are
    # about how the seven painted and not about how anybody paints.
    floor = session_module._GROUND_FLOOR
    for label, group in (("all", done),
                         ("the cohort", [r for r in done if r.painting.cohort]),
                         ("before it", [r for r in done if not r.painting.cohort])):
        if not group:
            continue
        bare = [r.session.canvas.ground_showing() for r in group]
        budgeted = [(r.spent / r.session.budget) for r in group if r.session.budget]
        crisp = [float(re.search(r"(\d+)%", edges_line(r.session)).group(1))
                 for r in group]
        print(f"\n  {label} ({len(group)} paintings)")
        print(f"    finding 11 -- the ground line: "
              f"{sum(1 for b in bare if b < floor)} of {len(group)} finish under the "
              f"{floor:.1%} the checklist asks for, median {float(np.median(bare)):.2%}")
        if budgeted:
            print(f"    finding 15 -- where painters stop: "
                  f"{sum(1 for r in budgeted if r < 0.45)} of {len(budgeted)} budgeted "
                  f"paintings stopped under 45% of budget, median "
                  f"{float(np.median(budgeted)):.0%} spent")
        print(f"    finding 13 -- uniform edges: the share under 2 px runs "
              f"{min(crisp):.0f}%-{max(crisp):.0f}%, median "
              f"{float(np.median(crisp)):.0f}%")


def probe_gpt_joins(replays: list[Replay]) -> None:
    """B2's last question: GPT's three holes, re-measured from its own script.

    The plan's reading is that they are the joins between neighbouring hard-edged
    walls -- B8 -- and not the comb. The three are at x = 0.552, 0.694 and 0.904 in
    its finished picture.
    """
    print("\n== B2: GPT's three holes, from its own painting ==")
    rep = next((r for r in replays if r.painting.name == "gpt"), None)
    if rep is None or rep.session is None:
        print("  (GPT was not replayed this run)")
        return
    session = rep.session
    bare = _bare(session)
    height, width = bare.shape
    print(f"  the finished canvas is {bare.mean():.3%} bare ground overall")
    for x in (0.552, 0.694, 0.904):
        col = int(x * width)
        strip = bare[:, max(col - 6, 0):col + 7]
        rows = np.nonzero(strip.any(axis=1))[0]
        if not len(rows):
            print(f"  x={x:.3f}: nothing bare within 6 px of that column")
            continue
        print(f"  x={x:.3f}: {int(strip.sum()):>5} bare px in a 13 px column, "
              f"y {rows.min() / height:.3f}-{rows.max() / height:.3f}")
    solid = [c for c in rep.calls if c.bound.get("solid")]
    combs = [c for c in solid if c.brush == "bristle"]
    print(f"  GPT laid {len(solid)} solid masses, {len(combs)} of them with a comb")
    print("  read: a hole at a join is B8's, and a hole in the middle of a mass is B2's.")


# -- running it -------------------------------------------------------------------------

CLAIMS = (
    ("2a.1 the chisel staircase", probe_staircase),
    ("2a.2 / B2 holes in a solid mass", probe_solid_holes),
    ("2a.3 the smudge thumbprint", probe_smudge_thumbprint),
    ("2a.4 a glaze far from its ground", probe_glaze_far),
    ("2a.8 / B17 a scumble's reach", probe_scumble_spill),
    ("B1 clip= and edge= across the verbs", probe_b1_clip),
    ("B3, B4 the time-lapse", probe_b3_b4_timelapse),
    ("B5 the plan object", probe_b5_plans),
    ("B6 records or strokes", probe_b6_records),
    ("B7 the documents through cp1252", probe_b7_cp1252),
    ("B8 the hard edge's bites", probe_b8_hard_edges),
    ("B9 the subject's share", probe_b9_subject_share),
    ("B10 the import name", probe_b10_import_name),
    ("B11-B14 grounds, regions, colours, solid=", probe_b11_b12_b13_b14),
    ("B15 what a stroke costs", probe_b15_cost_per_stroke),
    ("B16 calibrating a mark", probe_b16_rehearsal),
    ("B18 GLM's rings", probe_b18_rings),
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--only", nargs="+", metavar="NAME",
                        help="replay these paintings and no others")
    parser.add_argument("--list", action="store_true",
                        help="print the corpus and stop")
    parser.add_argument("--claims", action="store_true",
                        help="the 2a and 2d measurements, without the corpus replay")
    parser.add_argument("--corpus", action="store_true",
                        help="the corpus replay and its tables, without 2a and 2d")
    parser.add_argument("--quiet", action="store_true",
                        help="no per-pass echo while the corpus rebuilds")
    args = parser.parse_args(argv)

    if args.list:
        print(f"{'painting':<12}{'where':<42}{'passes':>7}{'spent':>7}  rebuild claimed")
        for entry in CORPUS:
            count = 1 if entry.driver else len(entry.passes)
            print(f"{entry.name:<12}{entry.where:<42}{count:>7}{entry.spent:>7}"
                  f"  {'yes' if entry.rebuilds else 'no'}")
        return 0

    print("The 0.5.0 cohort's round, measured. Engine "
          f"{easel.__version__} from {Path(easel.__file__).parent}")
    if not args.corpus:
        for label, probe in CLAIMS:
            print(f"\n{'-' * 78}\n{label}")
            probe()
    if args.claims:
        return 0

    wanted = [e for e in CORPUS if not args.only or e.name in set(args.only)]
    missing = set(args.only or ()) - {e.name for e in CORPUS}
    if missing:
        parser.error(f"no painting called {', '.join(sorted(missing))}")
    print(f"\n{'-' * 78}\nthe corpus: {len(wanted)} paintings, rebuilt pass by pass")
    replays = []
    for entry in wanted:
        print(f"  {entry.name} ...", flush=True)
        replays.append(replay(entry, echo=not args.quiet))
    report_corpus(replays)
    report_noise(replays)
    guide = probe_guide_blocks()
    report_candidates(replays, guide)
    report_samples(replays)
    report_measurements(replays)
    probe_gpt_joins(replays)
    probe_defaults(replays)
    print("\nThe numbers above are the ones CALIBRATION.md quotes. What they decide is "
          "which rows of PLAN-0.6.0.md survive into the round.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
