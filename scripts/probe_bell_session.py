"""The measurements behind the bell-warden's round -- step 2 of ``PLAN-0.8.0.md``.

Two painters painted against 0.7.0 from the package, for the same pack of pictures: the
Bell-Warden, a stone figure on a plinth in a dark undercroft, and the next morning Wenna
Brask, a woman by a lantern at dusk. Their verdicts are filed as open rounds in
``SUGGESTIONS.md``; the plan built on them proposes guides that read on any ground, a
shape handed to ``guide()`` and ``pencil()``, a thumbnail of the masses, two recipes and a
helper for the edge where a form turns, a line naming a pass's dearest calls, a fact for a
mark that lands short, a declared key, a place read by its median, a floor said as it is,
and more. **Every one of those is a candidate until this script has measured it** --
``LESSONS.md``'s first rule, and the reason step 2 comes before every engine change in the
round.

It does four things:

1. **Rebuilds both paintings** from their committed passes, through the CLI's own
   ``run_script``, the way ``easel run`` lays them -- the Bell-Warden in the order its
   saved reports record, its drawing run twice -- keeping a copy of the canvas as each
   pass left it, and every call's verb, script line and function. About a minute each.
2. **Re-measures section 3's claims** on the rebuild, and where a round dab, a short
   stroke and a starved bristle stop landing paint.
3. **Benches the candidates** -- each patched in for the length of one bench and never
   into the engine -- over both paintings, and over the corpus replayed by
   ``probe_cohort_session.py``'s harness with this round's measurements added.
4. **Renders what the numbers cannot decide** into ``out/bell/``: the guides on every
   ground, the thumbnails at four sizes, the terminator candidates, and the darks re-laid
   under the floor -- the sheets the painters' questions 4, 9 and 10 are put with.

    python scripts/probe_bell_session.py              # everything, about an hour
    python scripts/probe_bell_session.py --claims     # section 3 and 3b, re-measured
    python scripts/probe_bell_session.py --guides     # 4A1: the guide candidates
    python scripts/probe_bell_session.py --thumbnail  # 4A3: the painter's masses, flat
    python scripts/probe_bell_session.py --terminator # 4B: the lit form, both paintings
    python scripts/probe_bell_session.py --place      # 4E2: a place's reading
    python scripts/probe_bell_session.py --key        # 4E1: the values line under a key
    python scripts/probe_bell_session.py --short      # 4D: marks that land short or nothing
    python scripts/probe_bell_session.py --cost       # 4C: the dearest line, corpus-wide
    python scripts/probe_bell_session.py --floor      # 4E3: the darks under the floor
    python scripts/probe_bell_session.py --lamp       # 4E4: the named light, read as one
    python scripts/probe_bell_session.py --repaint    # 4H4: a place laid over and over
    python scripts/probe_bell_session.py --rebind     # 4H2: prelude names a pass rebinds
    python scripts/probe_bell_session.py --rings      # 4I2: an inward scumble's rings
    python scripts/probe_bell_session.py --units      # 4A5 and F7: pixel helpers, and units
    python scripts/probe_bell_session.py --corpus     # the corpus replay alone, kept

The corpus benches -- ``--short``, ``--cost``, ``--key``, ``--lamp``, ``--repaint`` and
``--place`` -- share one replay of every committed painting, about half an hour, kept in
``out/bell/corpus.pkl`` and read back until ``--fresh`` asks for another. ``--claims`` also
measures where a round dab, a short stroke and a starved bristle stop landing paint;
``--thumbnail`` draws A4's member that swells and narrows; ``--short`` runs its candidate
over the guide's own code blocks.
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import inspect
import io
import math
import os
import pickle
import re
import sys
import tempfile
import time
import warnings
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_cohort_session as cohort  # noqa: E402

import easel  # noqa: E402
import easel.session as session_module  # noqa: E402
from easel import Session, polygon  # noqa: E402
from easel.canvas import GROUNDS  # noqa: E402
from easel.cli import run_script  # noqa: E402
from easel.color import linear_to_srgb, luminance  # noqa: E402
from easel.history import History  # noqa: E402
from easel.look import label_sheet  # noqa: E402
from easel.regions import Polygon, Region  # noqa: E402

#: The modules themselves. ``import easel.look as look`` would be fine, but the round's
#: other probes take them from ``sys.modules`` for the papercut ``LESSONS.md`` names --
#: ``easel/__init__`` rebinds some module names to functions -- so this one does too.
LOOK_MODULE = sys.modules["easel.look"]
STROKE_MODULE = sys.modules["easel.stroke"]

PAINTINGS = ROOT / "paintings" / "Claude"
BELL = PAINTINGS / "bell_warden"
WENNA = PAINTINGS / "wenna_brask"
OUT = ROOT / "out" / "bell"
CACHE = OUT / "corpus.pkl"

#: How each painting was laid, taken from the corpus probe's own entries so the two
#: probes cannot disagree about an order: the Bell-Warden's drawing ran again after the
#: plinth, and Wenna Brask's drawing ran only on a scratch canvas.
_ENTRIES = {entry.name: entry for entry in cohort.CORPUS}
ORDERS = {"bell": _ENTRIES["bell"].passes, "wenna": _ENTRIES["wenna"].passes}
CANVASES = {"bell": dict(_ENTRIES["bell"].session), "wenna": dict(_ENTRIES["wenna"].session)}
FOLDERS = {"bell": BELL, "wenna": WENNA}

#: Log kinds that are not paint -- what the budget does not charge.
UNPAINTED = History.UNPAINTED_KINDS

#: `easel log` prints a mark under this many units of paint as *NO PAINT LANDED*.
LANDED = 1.0


# -- the paintings, rebuilt -------------------------------------------------------------

@dataclass
class Call:
    """One call a painter's script made, with where it was made and what it laid."""

    run: str                  # the pass (or version) it was laid in
    verb: str
    file: str                 # the script it was called from, by its file's name
    line: int
    func: str                 # the function it was called in, "<module>" at top level
    index: int                # the painting's own index of its first record
    count: int                # how many records it laid
    args: dict
    paid: int = 0             # how many of them the budget charges
    nothing: int = 0          # ...and how many of those laid under LANDED units
    wet: float | None = None  # the wetness under the place it was handed, before it

    @property
    def site(self) -> str:
        return f"{self.file}:{self.line}"


@dataclass
class Rebuilt:
    """A painting rebuilt from its passes, with a copy of the canvas after each."""

    name: str
    session: Session
    labels: list[str] = field(default_factory=list)       # the passes, as run
    starts: dict[str, int] = field(default_factory=dict)  # the index each opened at
    after: dict[str, Session] = field(default_factory=dict)
    said: dict[str, list[str]] = field(default_factory=dict)
    calls: list[Call] = field(default_factory=list)
    fresh: Session | None = None                          # the canvas before any pass
    seconds: float = 0.0

    def opened(self, label: str) -> Session:
        """A copy of the canvas the pass ``label`` opened on, to lay something else on."""
        if label not in self.labels:
            # A rebuild stopped short (``upto``): the next pass opens where it stopped.
            return self.after[self.labels[-1]].scratch()
        i = self.labels.index(label)
        base = self.fresh if i == 0 else self.after[self.labels[i - 1]]
        return base.scratch()

    def calls_in(self, label: str) -> list[Call]:
        return [c for c in self.calls if c.run == label]


def _painter_site() -> tuple[str, int, str]:
    """The script line, and the function, that made the call being watched.

    The first frame outside the engine, outside the probes and outside the standard
    library's context managers: the painter's own pass, or the prelude it ran after --
    ``run_script`` compiles each under its own name, so a helper defined in the prelude
    is reported as ``prelude.py`` and a function in the pass by the pass's name.
    """
    frame = sys._getframe(1)
    while frame is not None:
        name = frame.f_code.co_filename
        base = os.path.basename(name)
        if ("easel" + os.sep not in name and not base.startswith("probe_")
                and base not in ("contextlib.py", "warnings.py")):
            return base, frame.f_lineno, frame.f_code.co_name
        frame = frame.f_back
    return "", 0, ""


_WATCHED = ("stroke", "dab", "smudge", "glaze", "block_in", "sweep", "cover", "scumble",
            "pencil", "erase", "dry")
_STUBBED = ("look", "look_image", "export", "timelapse_gif", "contact_sheet", "save",
            "look_areas", "capture_frame")


def _bound(signature: inspect.Signature, session, args, kw) -> dict:
    try:
        bound = signature.bind(session, *args, **kw)
        bound.apply_defaults()
        named = dict(bound.arguments)
        named.pop("self", None)
        named.update(named.pop("brush_overrides", {}) or {})
        named.update(named.pop("kw", {}) or {})
        return named
    except TypeError:
        return dict(kw)


def _place_of(named: dict):
    for key in ("region", "band", "place", "edge"):
        if key in named and isinstance(named[key], (Polygon, Region)):
            return named[key]
    return None


@contextlib.contextmanager
def watching(calls: list[Call], current: list[str]):
    """Record every outermost call of a painting verb, with its site and its records.

    Only the outermost: a mass calls ``stroke`` once a pass, and ``dab`` calls it once,
    and what a painter wrote is the one call. The wetness under a mass's place is taken
    as it begins, which is how row 4 of the plan asks what the head's plane was laid on.
    """
    saved = {name: getattr(Session, name) for name in _WATCHED}
    depth = [0]

    def wrap(name, original):
        signature = inspect.signature(original)

        def wrapper(session, *args, **kw):
            if depth[0]:
                return original(session, *args, **kw)
            depth[0] += 1
            try:
                file, line, func = _painter_site()
                named = _bound(signature, session, args, kw)
                first = len(session.history.records)
                wet = None
                place = _place_of(named)
                if place is not None and not session._counting:
                    h, w = session.canvas.height, session.canvas.width
                    mask = cohort._mask(place, w, h)
                    if mask is not None and mask.any():
                        wet = float(session.canvas.wetness[mask].mean())
                out = original(session, *args, **kw)
                records = session.history.records[first:]
                paid = [r for r in records if r.kind not in UNPAINTED]
                calls.append(Call(run=current[0], verb=name, file=file, line=line,
                                  func=func, index=session._index_base + first,
                                  count=len(records), args=named, paid=len(paid),
                                  nothing=sum(1 for r in paid if r.paint < LANDED),
                                  wet=wet))
                return out
            finally:
                depth[0] -= 1
        wrapper.__name__ = name
        wrapper.__doc__ = original.__doc__
        return wrapper

    for name, original in saved.items():
        setattr(Session, name, wrap(name, original))
    try:
        yield
    finally:
        for name, original in saved.items():
            setattr(Session, name, original)


@contextlib.contextmanager
def quiet():
    """No looks rendered, no files written, nothing printed, no warnings shown.

    The passes print their looks and write them under ``looks/``; none of that lays a
    mark or touches the stream, and a rebuild that rendered them would spend a third of
    its time on pictures nobody reads. Run from a temporary directory besides, so a
    pass's own ``os.makedirs("looks")`` lands there.
    """
    saved = {name: getattr(Session, name) for name in _STUBBED}
    for name in _STUBBED:
        setattr(Session, name, cohort._stub(name))
    here = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="easel-bell-probe-") as tmp:
        try:
            os.chdir(tmp)
            with warnings.catch_warnings(), contextlib.redirect_stdout(io.StringIO()):
                warnings.simplefilter("ignore")
                yield Path(tmp)
        finally:
            os.chdir(here)
            for name, original in saved.items():
                setattr(Session, name, original)


def new_session(painting: str = "bell", **changes) -> Session:
    """A fresh canvas as the painting's own ``easel new`` made it."""
    spec = {**CANVASES[painting], **changes}
    return Session(timelapse=False, out_dir=OUT / "scratch", **spec)


def run_pass(session: Session, script: Path, prelude: Path | None,
             calls: list[Call] | None = None, label: str = "") -> list[str]:
    """One pass laid on ``session`` as ``easel run`` lays it; what its check said.

    ``calls`` collects the pass's calls, when given. Raises if the pass raises, with
    the traceback the shell would have printed.
    """
    source = prelude.read_text(encoding="utf-8-sig") if prelude else ""
    watcher = (watching(calls, [label or script.name]) if calls is not None
               else contextlib.nullcontext())
    with quiet(), watcher:
        start = session._open_pass()
        result = run_script(session, script.read_text(encoding="utf-8-sig"), str(script),
                            prelude=source, prelude_name="prelude.py")
        if result.code:
            raise RuntimeError(f"{script.name}: {result.report}\n{result.trace}")
        return session.report(since=start).splitlines()


def run_source(session: Session, source: str, name: str, prelude: str = "",
               calls: list[Call] | None = None) -> tuple[list[str], list[str]]:
    """A pass given as source, laid as ``easel run`` lays it: ``(check, notice codes)``.

    For the benches' variants of a pass, which are the painter's own script with a line
    changed: run under the pass's own name, so a call is reported at the line it has.
    """
    watcher = (watching(calls, [name]) if calls is not None else contextlib.nullcontext())
    with quiet(), watcher:
        start = session._open_pass()
        told = len(session.notices())
        result = run_script(session, source, name, prelude=prelude, prelude_name="prelude.py")
        if result.code:
            raise RuntimeError(f"{name}: {result.report}\n{result.trace}")
        codes = [n.code for n in session.notices(since=told)]
        return session.report(since=start).splitlines(), codes


def rebuild(painting: str = "bell", upto: str | None = None, keep: bool = True,
            order: tuple[str, ...] | None = None, **canvas) -> Rebuilt:
    """A painting from its committed passes, through the CLI's own ``run_script``.

    Each pass opens as ``easel run`` opens one, runs in a fresh scope with the prelude
    executed in front of it, and is read by ``report()`` over the pass alone -- so
    ``said`` is what the painter's shell printed after it. With ``keep``, a rehearsal
    copy is kept after every pass (:meth:`Session.scratch`), seeded as the next marks of
    the painting: what a bench lays on it is what the painter would have laid there.
    ``order`` overrides the recorded order, which is how the numbered order is tried.
    """
    folder = FOLDERS[painting]
    prelude = folder / "prelude.py"
    started = time.time()
    session = new_session(painting, **canvas)
    out = Rebuilt(name=painting, session=session, fresh=session.scratch())
    current = [""]
    source = prelude.read_text(encoding="utf-8-sig")
    with quiet(), watching(out.calls, current):
        for name in order or ORDERS[painting]:
            label = f"{name} (again)" if name in out.labels else name
            current[0] = label
            out.labels.append(label)
            start = session._open_pass()
            out.starts[label] = start
            path = folder / name
            result = run_script(session, path.read_text(encoding="utf-8-sig"), str(path),
                                prelude=source, prelude_name="prelude.py")
            if result.code:
                raise RuntimeError(f"{name} failed to rebuild: {result.report}\n"
                                   f"{result.trace}")
            out.said[label] = session.report(since=start).splitlines()
            if keep:
                out.after[label] = session.scratch()
            if label == upto:
                break
    out.seconds = time.time() - started
    return out


def scope_of(painting: str = "bell", prelude: Path | None = None,
             session: Session | None = None) -> dict:
    """The prelude's names -- the palette, the shapes, the helpers -- as a pass sees them."""
    session = session or new_session(painting)
    scope = {name: getattr(easel, name) for name in easel.__all__}
    scope.update({"s": session, "session": session, "palette": session.palette,
                  "__name__": "__easel_script__"})
    path = prelude or FOLDERS[painting] / "prelude.py"
    with warnings.catch_warnings(), contextlib.redirect_stdout(io.StringIO()):
        warnings.simplefilter("ignore")
        exec(compile(path.read_text(encoding="utf-8-sig"), "prelude.py", "exec"),  # noqa: S102
             scope)
    return scope


# -- small instruments ----------------------------------------------------------------

def values(session: Session) -> np.ndarray:
    """The canvas as the check's standing lines read it: values, ``0..1``, no graphite."""
    return session.canvas.values(sketch=False).astype(np.float32) / 255.0


def plan_view(session: Session) -> np.ndarray:
    """The canvas as the plan's lines read it (``Session._value_view``)."""
    return session._value_view()


def values_of_rgb(rgb8: np.ndarray) -> np.ndarray:
    """An 8-bit RGB array as values, the way ``look(values=True)`` shows them."""
    return session_module._values_of(rgb8)


def readings(pixels: np.ndarray) -> dict[str, float]:
    """A place's pixels read every way the plan considers."""
    x = np.asarray(pixels, dtype=np.float64)
    med = float(np.median(x))
    return {"mean": float(x.mean()), "median": med,
            "p75": float(np.percentile(x, 75)), "p90": float(np.percentile(x, 90)),
            "p95": float(np.percentile(x, 95)), "max": float(x.max()),
            "split": float((np.abs(x - med) > 0.15).mean()),
            "darker": float((x < med - 0.15).mean()), "px": int(x.size)}


def pct(values_: list[float], q: float) -> float:
    return float(np.percentile(np.asarray(values_, dtype=np.float64), q)) if values_ else float("nan")


def table(rows: list[list], head: list[str], indent: str = "  ") -> str:
    """A plain aligned table, for the numbers ``CALIBRATION.md`` quotes."""
    cells = [[str(c) for c in row] for row in [head] + rows]
    widths = [max(len(r[i]) for r in cells) for i in range(len(head))]
    out = []
    for n, row in enumerate(cells):
        out.append(indent + "  ".join(c.rjust(w) if n and _numeric(c) else c.ljust(w)
                                      for c, w in zip(row, widths, strict=True)).rstrip())
        if n == 0:
            out.append(indent + "  ".join("-" * w for w in widths))
    return "\n".join(out)


def _numeric(text: str) -> bool:
    return bool(re.fullmatch(r"[-+]?[\d.,%]+( px)?", text.strip()))


def save_sheet(panels: list[tuple[str, Image.Image]], name: str,
               columns: int | None = None) -> Path:
    """Panels side by side, each labelled, into ``out/bell/``."""
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    label_sheet(panels, columns=columns or len(panels)).save(path)
    return path


def crop(session: Session, box: tuple[float, float, float, float], zoom: int = 1,
         values_view: bool = False) -> Image.Image:
    """A part of the canvas as the export shows it, ``box`` in canvas units."""
    x0, y0, x1, y1 = box
    w, h = session.canvas.width, session.canvas.height
    rgb = session.canvas.to_srgb8(impasto=True, sketch=False)
    if values_view:
        grey = (values_of_rgb(rgb) * 255.0 + 0.5).astype(np.uint8)
        rgb = np.repeat(grey[:, :, None], 3, axis=2)
    image = Image.fromarray(rgb[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)])
    if zoom > 1:
        image = image.resize((image.width * zoom, image.height * zoom), Image.LANCZOS)
    return image


def heading(text: str) -> None:
    print(f"\n== {text} ==")


# -- section 3, re-measured -------------------------------------------------------------

def probe_rebuild(rb: Rebuilt) -> None:
    """The rebuild itself, against the painter's own export and the order it records."""
    heading(f"{rb.name}: rebuilt from {len(rb.labels)} passes")
    s = rb.session
    print(f"  {len(s.history.records)} records, {s.stroke_count} strokes spent, "
          f"in {rb.seconds:.0f} s")
    print("  passes open at " + ", ".join(str(rb.starts[k]) for k in rb.labels))
    painted = np.asarray(Image.open(FOLDERS[rb.name] / "painting.png").convert("RGB"))
    ours = s.canvas.to_srgb8(impasto=True, sketch=False)
    if ours.shape == painted.shape:
        diff = np.abs(ours.astype(int) - painted.astype(int)).max(axis=2)
        print(f"  export against the painter's painting.png: {int((diff > 0).sum())} pixels "
              f"differ, the most by {int(diff.max())} levels")
    else:
        print(f"  export shape {ours.shape} against the painter's {painted.shape}")


def probe_numbered_order() -> None:
    """The Bell-Warden in its passes' numbered order, against the recorded order."""
    heading("the Bell-Warden in numbered order, against the order its reports record")
    recorded = rebuild("bell", keep=False)
    numbered = rebuild("bell", keep=False,
                       order=tuple(sorted(set(ORDERS["bell"]))))
    a = recorded.session.canvas.to_srgb8(impasto=True, sketch=False).astype(int)
    b = numbered.session.canvas.to_srgb8(impasto=True, sketch=False).astype(int)
    diff = np.abs(a - b).max(axis=2)
    print(f"  recorded: {len(recorded.session.history.records)} records; numbered: "
          f"{len(numbered.session.history.records)}")
    print(f"  {int((diff > 0).sum()):,} of {diff.size:,} pixels move "
          f"({(diff > 0).mean():.1%}), {int((diff > 8).sum()):,} by more than 8 levels, "
          f"the most by {int(diff.max())}")


def _calls_table(calls: list[Call]) -> str:
    rows = []
    for c in calls:
        if not c.paid:
            continue
        rows.append([c.paid, c.verb, c.site, c.func, c.nothing or ""])
    return table(rows, ["strokes", "verb", "at", "in", "landed nothing"])


def probe_calls(rb: Rebuilt, labels: tuple[str, ...]) -> None:
    """Row 3: what each call of a pass cost, off the calls as they were made."""
    for label in labels:
        calls = [c for c in rb.calls_in(label) if c.paid]
        total = sum(c.paid for c in calls)
        masses = sorted((c for c in calls if c.paid > 1), key=lambda c: -c.paid)
        heading(f"{rb.name} {label}: {total} strokes in {len(calls)} calls")
        print(_calls_table(calls))
        if masses:
            print("  dearest: " + ", ".join(f"{c.paid} {c.verb} at {c.site} ({c.func})"
                                           for c in masses[:4]))


def guide_steps(background: np.ndarray, drawn: np.ndarray) -> np.ndarray:
    """The value step at every pixel an overlay changed: what the eye has to find."""
    changed = np.abs(drawn.astype(int) - background.astype(int)).max(axis=2) > 0
    before = values_of_rgb(background)
    after = values_of_rgb(drawn)
    return np.abs(after - before)[changed]


def _look_rgb(session: Session) -> np.ndarray:
    """What ``look()`` renders the canvas as, before anything is drawn over it."""
    return session.canvas.to_srgb8(impasto=True, sketch=True)


def _frame(rgb: np.ndarray, aspect: float):
    return LOOK_MODULE._Frame(Image.fromarray(rgb), None, aspect)


def probe_guides_claim(rb: Rebuilt) -> None:
    """Row 1: today's guide, over the bare ground and over the finished canvas."""
    heading("row 1: the painter's guides, drawn today, over the ground and over the paint")
    guides = [dict(g) for g in rb.session.guides]
    lines = [dict(g, note="") for g in guides]
    aspect = rb.session.aspect
    for label, rgb in (("bare ground", _look_rgb(rb.fresh)),
                       ("after the room (p02)", _look_rgb(rb.after["p02_room.py"])),
                       ("finished", _look_rgb(rb.session))):
        for what, overlay in (("lines", lines), ("lines and notes", guides)):
            drawn = np.asarray(LOOK_MODULE._draw_guides(_frame(rgb, aspect), overlay))
            steps = guide_steps(rgb, drawn)
            print(f"  {label:<22} {what:<16} {len(guides)} guides, {steps.size:5d} px: "
                  f"median step {np.median(steps):.3f}, {(steps < 0.05).mean():4.0%} "
                  f"under 0.05, min {steps.min():.3f}")


def probe_pencil_claim(rb: Rebuilt) -> None:
    """Row 2: a shape cannot be handed to ``pencil()`` or ``guide()``; the spline bows."""
    heading("row 2: a shape handed to pencil() and guide(), and the spline's bow")
    scope = scope_of("bell")
    plinth = scope["plinth"]
    for verb in ("pencil", "guide"):
        s = new_session("bell")
        try:
            getattr(s, verb)(plinth)
            print(f"  s.{verb}(plinth): accepted")
        except Exception as exc:                                  # noqa: BLE001
            print(f"  s.{verb}(plinth): {type(exc).__name__}: {str(exc)[:90]}")
        try:
            getattr(s, verb)(Region(0.2, 0.2, 0.4, 0.4))
            print(f"  s.{verb}(Region): accepted")
        except Exception as exc:                                  # noqa: BLE001
            print(f"  s.{verb}(Region): {type(exc).__name__}: {str(exc)[:90]}")
    w, h = rb.session.canvas.width, rb.session.canvas.height
    for name in ("plinth", "plinth_top", "plinth_front", "plinth_side", "body"):
        shape = scope[name]
        pts = np.asarray(shape.closed, dtype=np.float32)
        path = STROKE_MODULE.catmull_rom(pts)
        outside = ~shape.inside(path[:, 0], path[:, 1])
        far = _outside_distance(shape, path, w, h)
        print(f"  {name:<13} smoothed: {outside.mean():4.0%} of the path outside the shape, "
              f"the furthest {far:.1f} px")


def _outside_distance(shape: Polygon, path: np.ndarray, w: int, h: int) -> float:
    """How far, in pixels, a path strays outside a shape at its worst."""
    pts = np.asarray(shape.closed, dtype=np.float64) * [w, h]
    best = 0.0
    inside = shape.inside(path[:, 0], path[:, 1])
    for (x, y), ok in zip(path * [w, h], inside, strict=True):
        if ok:
            continue
        a, b = pts[:-1], pts[1:]
        ab = b - a
        t = np.clip(((x - a[:, 0]) * ab[:, 0] + (y - a[:, 1]) * ab[:, 1])
                    / np.maximum((ab ** 2).sum(axis=1), 1e-12), 0.0, 1.0)
        d = np.hypot(a[:, 0] + t * ab[:, 0] - x, a[:, 1] + t * ab[:, 1] - y).min()
        best = max(best, float(d))
    return best


def _without_dry(source: str) -> str:
    """A pass's source with its bare ``s.dry()`` statements taken out."""
    return "\n".join("pass" if line.strip() == "s.dry()" else line
                     for line in source.splitlines())


def probe_wet_claim(rb: Rebuilt) -> None:
    """Row 4: the head's plane and the lights, laid with and without the two dry()s."""
    heading("row 4: the details pass laid with and without its two s.dry() calls")
    head = next((c for c in rb.calls_in("p05_details.py")
                 if c.verb == "block_in" and c.line == 26), None)
    if head is not None:
        print(f"  wetness under the head's top as its plane was laid: {head.wet:.3f}")
    scope = scope_of("bell")
    places = {"head top": scope["head_top"]}
    ridge = {"chest ridge": [(0.294, 0.492), (0.303, 0.545), (0.317, 0.600), (0.321, 0.655)],
             "wing ridge": [(0.421, 0.380), (0.434, 0.298), (0.457, 0.198), (0.473, 0.122)]}
    source = (BELL / "p05_details.py").read_text(encoding="utf-8")
    for label, text in (("as committed", source), ("without the dry()s", _without_dry(source))):
        s = rb.opened("p05_details.py")
        path = OUT / "scratch" / "p05_variant.py"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        run_pass(s, path, BELL / "prelude.py")
        view = plan_view(s)
        h, w = view.shape
        got = readings(view[places["head top"].mask(w, h)])
        lights = []
        for name, pts in ridge.items():
            line = _path_pixels(pts, w, h, s.canvas.long_side * 0.003)
            lights.append(f"{name} {np.median(view[line]):.2f}")
        print(f"  {label:<20} head top median {got['median']:.3f}, mean {got['mean']:.3f}; "
              + ", ".join(lights))


def _path_pixels(points, w: int, h: int, radius_px: float) -> np.ndarray:
    """The pixels within ``radius_px`` of a smoothed path."""
    pts = STROKE_MODULE.catmull_rom(np.asarray(points, dtype=np.float32))
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    xy = [(float(x) * w, float(y) * h) for x, y in pts]
    draw.line(xy, fill=255, width=max(1, int(round(2 * radius_px))))
    return np.asarray(mask) > 0


def probe_place_claim(rb: Rebuilt) -> None:
    """Row 5b: the head's top at the finish, and every planned place, read four ways."""
    heading("row 5b: the planned places at the finish, read every way")
    view = plan_view(rb.session)
    h, w = view.shape
    plan = rb.session._plan
    rows = []
    for p in plan.values:
        got = readings(view[p.outline.mask(w, h)])
        rows.append([p.name, f"{p.value:.2f}", f"{got['mean']:.3f}", f"{got['median']:.3f}",
                     f"{got['p75']:.3f}", f"{got['p90']:.3f}", f"{got['split']:.0%}",
                     f"{got['px']:,}"])
    print(table(rows, ["place", "planned", "mean", "median", "p75", "p90", "split", "px"]))
    head = next(p for p in plan.values if p.name == "head top")
    x = view[head.outline.mask(w, h)]
    print(f"  head top: {(x < 0.35).mean():.0%} of its {x.size:,} pixels under 0.35")


def probe_reports_claim() -> None:
    """Row 5a: *no clear light* in the painter's saved reports."""
    heading("row 5a: the values line in the painter's 27 saved reports")
    text = (BELL / "reports.txt").read_text(encoding="utf-8")
    blocks = saved_reports(BELL / "reports.txt")
    said = sum(1 for b in blocks if "no clear light" in b)
    print(f"  {len(blocks)} reports; {said} say no clear light")
    tops = [float(m) for m in re.findall(r"no clear light -- nothing above (\d\.\d\d)", text)]
    if tops:
        print(f"  the top twentieth they name: {min(tops):.2f} to {max(tops):.2f}")


def saved_reports(path: Path) -> list[str]:
    """The pass reports a painting's ``reports.txt`` holds, one block each, oldest first."""
    text = path.read_text(encoding="utf-8")
    return [b.strip() for b in re.split(r"\n\s*\n(?=(?:painted|rehearsed|counted) )", text)
            if re.match(r"(?:painted|rehearsed|counted) ", b.strip())]


def probe_sizes_claim(rb: Rebuilt) -> None:
    """Row 12: the give-aways in pixels."""
    heading("row 12: the give-aways, in pixels at the painting's size")
    long = rb.session.canvas.long_side
    for name, size in (("the ember", 0.0068), ("the spark", 0.0028), ("the claws", 0.0095),
                       ("", 0.0090), ("", 0.0078), ("the claw lights", 0.0035), ("", 0.0032)):
        print(f"  {name:<16} {size:.4f} of the long side: {size * long:.1f} px")


def probe_floor_claim() -> None:
    """Row 13: the box's floor, what ``at_value`` says under it, and a supplied dark."""
    heading("row 13: the floor")
    s = new_session("bell")
    p = s.palette
    rows = []
    for name in sorted(set(p.pigment_names)):
        rows.append((p.value_of(name), name))
    rows.sort()
    print("  the darkest pigments: " + ", ".join(f"{n} {v:.3f}" for v, n in rows[:4]))
    print(f"  darkest_value: {p.darkest_value:.3f}")
    default_dark = p.mix("ultramarine", "burnt_umber", 0.5)
    print(f"  at_value's default dark (ultramarine and umber, half and half): "
          f"{p.value_of(default_dark):.3f}")
    for t in (0.3, 0.5, 0.7, 0.8):
        print(f"    umber with {t:.0%} ultramarine: "
              f"{p.value_of(p.mix('burnt_umber', 'ultramarine', t)):.3f}")
    try:
        p.at_value(p.mix("ultramarine", "burnt_umber", 0.5), 0.13)
    except ValueError as exc:
        print(f"  at_value(blue-umber, 0.13): {exc}")
    print(f"  shade(burnt_umber, 1.0): {p.value_of(p.shade('burnt_umber', 1.0)):.3f}")
    supplied = "#0d0c10"
    print(f"  a supplied {supplied}: {p.value_of(supplied):.3f}")
    for t in (0.3, 0.5, 0.7):
        mixed = p.mix("burnt_umber", supplied, t)
        print(f"    umber with {t:.0%} of it: {p.value_of(mixed):.3f} as mixed, "
              f"{_laid_value(mixed):.3f} laid solid")


def _laid_value(color) -> float:
    """What a colour lands at, laid as one solid mass on the Bell-Warden's canvas."""
    s = new_session("bell")
    place = Region(0.3, 0.3, 0.7, 0.7)
    with quiet():
        s.block_in(place, "flat", color, size=0.06, density=1.0, solid=True)
    view = values(s)
    h, w = view.shape
    return float(np.median(view[int(0.4 * h):int(0.6 * h), int(0.4 * w):int(0.6 * w)]))


# -- where a mark stops landing ---------------------------------------------------------

#: Round tips across the sizes the two paintings' small marks were laid at, and past.
DAB_SIZES = tuple(round(0.0020 + 0.0005 * i, 4) for i in range(21))


def _flat(session: Session, color) -> Session:
    """The canvas set to one colour, wet nowhere: a field, not a mass, costs nothing."""
    lin = session._resolve_color(color)
    session.canvas.rgb[...] = lin
    session.canvas.wetness[...] = 0.0
    return session


def _window(session: Session, x: float, y: float, reach: int = 40) -> tuple[slice, slice]:
    w, h = session.canvas.width, session.canvas.height
    cx, cy = int(x * w), int(y * h)
    return (slice(max(cy - reach, 0), min(cy + reach, h)),
            slice(max(cx - reach, 0), min(cx + reach, w)))


def _local_values(session: Session, box: tuple[slice, slice]) -> np.ndarray:
    """The values view over one window, as ``Canvas.values(sketch=False)`` computes it."""
    rgb = session.canvas.rgb[box]
    return (linear_to_srgb(luminance(rgb)) * 255.0 + 0.5).astype(np.uint8) / 255.0


_FIELDS: dict[tuple, Session] = {}


def _field_session(width: int, height: int, field_color, texture: str = "linen",
                   seed: int = 11) -> Session:
    """A copy of a canvas set to one colour, made once per size and handed out fresh."""
    key = (width, height, str(field_color), texture, seed)
    if key not in _FIELDS:
        s = Session(width, height, texture=texture, ground="umber_wash", seed=seed,
                    timelapse=False, out_dir=OUT / "scratch")
        _FIELDS[key] = _flat(s, field_color)
    return _FIELDS[key].scratch()


def dab_grid(width: int, height: int, brush: str, color, field_color, press: int = 1,
             wobble: float = 0.0, sizes=DAB_SIZES, n: int = 12,
             texture: str = "linen", stroke: float = 0.0) -> list[dict]:
    """Every size of one round tip laid ``n`` times on a field; what each landed.

    Each size on a fresh copy of one field, each mark ``n`` times at points far enough
    apart not to meet, read over a window round it: the paint the record carries, how
    many pixels it moved by more than ``0.02``, and the median value they read.
    ``stroke`` above nought lays a two-point stroke that long (a fraction of the long
    side, straight down) instead of a dab: the claw lights' shape.
    """
    out = []
    for size in sizes:
        s = _field_session(width, height, field_color, texture)
        own = s.palette.value_of(color)
        paint, px, reads = [], [], []
        with quiet():
            for i in range(n):
                x = 0.1 + 0.8 * (i % 6) / 5.0
                y = 0.3 + 0.4 * (i // 6)
                box = _window(s, x, y)
                before = _local_values(s, box)
                if stroke:
                    dy = stroke * s.canvas.long_side / height
                    rec = s.stroke([(x, y), (x, y + dy)], brush, color, size=size,
                                   opacity=0.85, pressure=[1.0, 0.2], tip_wobble=wobble)
                else:
                    rec = s.dab(x, y, brush, color, size=size, press=press,
                                tip_wobble=wobble)
                after = _local_values(s, box)
                moved = np.abs(after - before) > 0.02
                paint.append(float(rec.paint))
                px.append(int(moved.sum()))
                if moved.any():
                    reads.append(float(np.median(after[moved])))
        out.append({"size": size, "px": size * max(width, height),
                    "paint": float(np.median(paint)),
                    "landed": sum(p >= LANDED for p in paint) / n,
                    "moved": float(np.median(px)),
                    "reads": float(np.median(reads)) if reads else float("nan"),
                    "own": own})
    return out


def _first(rows: list[dict], test) -> str:
    for row in rows:
        if test(row):
            return f"{row['size']:.4f} ({row['px']:.1f} px)"
    return "never"


def probe_landing() -> None:
    """Where a round dab, a short stroke and a starved small bristle stop landing."""
    heading("where a round dab stops landing paint: a light dab on a dark field")
    light, dark = "#f2e2a0", "#2a2622"
    rows = []
    for brush in ("round_hard", "round_soft"):
        for press in (1, 2, 3):
            for wobble in (0.0, 0.7):
                for width, height in ((1024, 768), (1440, 960)):
                    grid = dab_grid(width, height, brush, light, dark, press=press,
                                    wobble=wobble)
                    rows.append([brush, press, wobble, f"{width}x{height}",
                                 _first(grid, lambda r: r["landed"] >= 0.5),
                                 _first(grid, lambda r: r["landed"] == 1.0),
                                 _first(grid, lambda r: r["reads"] == r["reads"]
                                        and r["reads"] >= 0.5 * (r["own"] + 0.16))])
                    if brush == "round_hard" and wobble == 0.7 and width == 1024:
                        print(f"  {brush} press={press} tip_wobble={wobble} at {width}x{height}:")
                        for r in grid[::2]:
                            print(f"    size {r['size']:.4f} ({r['px']:4.1f} px): paint "
                                  f"{r['paint']:6.2f}, {r['landed']:4.0%} landed, "
                                  f"{r['moved']:4.0f} px moved, reads {r['reads']:.2f} "
                                  f"of its own {r['own']:.2f}")
    print(table(rows, ["tip", "press", "wobble", "canvas", "half land from", "all land from",
                       "reads halfway from"]))

    heading("a short stroke of a round tip (the claw lights' shape), on the same field")
    for brush in ("round_hard", "round_soft"):
        grid = dab_grid(1024, 768, brush, light, dark, wobble=0.35, stroke=0.015)
        print(f"  {brush}: all land from {_first(grid, lambda r: r['landed'] == 1.0)}; "
              f"reads halfway from {_first(grid, lambda r: r['reads'] == r['reads'] and r['reads'] >= 0.5 * (r['own'] + 0.16))}")
        for r in grid[::4]:
            print(f"    size {r['size']:.4f} ({r['px']:4.1f} px): paint {r['paint']:7.2f}, "
                  f"reads {r['reads']:.2f} of {r['own']:.2f}")

    heading("a small bristle at the loads the flour was laid at, and above")
    rows = []
    for size in (0.009, 0.012, 0.016, 0.024, 0.03):
        row = [f"{size:.3f}"]
        for load in (0.12, 0.22, 0.35, 0.5, 0.7, 0.9):
            s = _field_session(768, 1024, "#3a302a", seed=23)
            laid = []
            with quiet():
                for i in range(6):
                    y = 0.2 + 0.1 * i
                    rec = s.stroke([(0.3, y), (0.45, y + 0.01), (0.6, y)], "bristle", "#e8e0cc",
                                   size=size, load=load, opacity=0.8)
                    laid.append(rec.paint)
            row.append(f"{np.median(laid):.1f}")
        rows.append(row)
    print(table(rows, ["size", "load 0.12", "0.22", "0.35", "0.5", "0.7", "0.9"]))


def probe_claims(rb: Rebuilt, wb: Rebuilt | None) -> None:
    probe_rebuild(rb)
    if wb is not None:
        probe_rebuild(wb)
    probe_numbered_order()
    probe_guides_claim(rb)
    probe_pencil_claim(rb)
    probe_calls(rb, ("p04_gargoyle.py", "p05_details.py"))
    if wb is not None:
        probe_calls(wb, ("p03_figure.py",))
    probe_wet_claim(rb)
    probe_reports_claim()
    probe_place_claim(rb)
    probe_sizes_claim(rb)
    probe_floor_claim()
    probe_landing()


# -- 4A1: guides that read on any ground --------------------------------------------------

GRAPHITE = LOOK_MODULE._GUIDE_COLOR
#: A light neutral for the casing: as far above the paint a dark picture is made of as
#: the graphite is below a light one.
CASING = (236, 236, 232)
NOTE_BOX, NOTE_INK = LOOK_MODULE._PANEL_LABEL_BG, LOOK_MODULE._PANEL_LABEL_INK
#: The plan's target: no guide pixel under this step in value in one of its tones.
READS = 0.25


def _paths(frame, guides):
    for g in guides:
        pts = [frame.to_px(float(x), float(y)) for x, y in g.get("points", ())]
        if pts:
            yield pts, str(g.get("note") or "")


def _line_layer(size, frame, guides, width: int, colour, alpha: int) -> Image.Image:
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for pts, _ in _paths(frame, guides):
        if len(pts) == 1:
            x, y = pts[0]
            r = 2 + (width - 1) / 2.0
            draw.ellipse([x - r, y - r, x + r, y + r], fill=tuple(colour) + (alpha,))
        else:
            draw.line(pts, fill=tuple(colour) + (alpha,), width=width, joint="curve")
    return overlay


def _note_layer(size, frame, guides, boxed: bool) -> Image.Image:
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for pts, note in _paths(frame, guides):
        if not note:
            continue
        x, y = pts[0]
        if boxed:
            draw.rectangle([x + 2, y - 13, x + 7 + 6 * len(note), y + 1],
                           fill=tuple(NOTE_BOX) + (235,))
            draw.text((x + 4, y - 12), note, fill=tuple(NOTE_INK) + (255,))
        else:
            draw.text((x + 4, y - 11), note, fill=tuple(GRAPHITE) + (LOOK_MODULE._GUIDE_ALPHA,))
    return overlay


def draw_candidate(kind: str, rgb: np.ndarray, guides: list, aspect: float,
                   notes: bool = True) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """One guide candidate over an image: ``(drawn, core pixels, casing pixels)``.

    ``today`` is the engine's own ``_draw_guides``. ``casing`` lays a light line three
    pixels wide under a one-pixel graphite core, and ``casing 150`` the same casing at
    150 of 255; ``ink`` draws the one-pixel line in graphite where what is under it is
    lighter than ``0.45`` and in the casing's colour where it is darker. Every
    candidate but ``today`` boxes its notes, as a landmark's name is boxed.
    """
    base = Image.fromarray(rgb).convert("RGBA")
    frame = LOOK_MODULE._Frame(base, None, aspect)
    size = base.size
    shown = guides if notes else [dict(g, note="") for g in guides]
    bare = [dict(g, note="") for g in guides]
    core = np.asarray(_line_layer(size, frame, bare, 1, GRAPHITE, 255))[..., 3] > 0
    casing = np.zeros_like(core)
    if kind == "today":
        drawn = np.asarray(LOOK_MODULE._draw_guides(LOOK_MODULE._Frame(Image.fromarray(rgb),
                                                                       None, aspect), shown))
        return drawn, core, casing
    out = base
    if kind.startswith("casing"):
        alpha = int(kind.split()[1]) if " " in kind else 255
        layer = _line_layer(size, frame, bare, 3, CASING, alpha)
        casing = (np.asarray(layer)[..., 3] > 0) & ~core
        out = Image.alpha_composite(out, layer)
        out = Image.alpha_composite(out, _line_layer(size, frame, bare, 1, GRAPHITE, 255))
    elif kind == "ink":
        under = values_of_rgb(rgb)
        ink = np.where((under >= 0.45)[..., None], np.asarray(GRAPHITE, np.uint8),
                       np.asarray(CASING, np.uint8))
        arr = np.asarray(out).copy()
        arr[core, :3] = ink[core]
        out = Image.fromarray(arr)
    else:  # pragma: no cover - a typo in a bench
        raise ValueError(kind)
    if notes:
        out = Image.alpha_composite(out, _note_layer(size, frame, shown, boxed=True))
    return np.asarray(out.convert("RGB")), core, casing


def visibility(rgb: np.ndarray, drawn: np.ndarray, core: np.ndarray,
               casing: np.ndarray) -> np.ndarray:
    """At every pixel of the line's core, the larger step of its two tones.

    The core's own step over what is under it, and the largest step of a casing pixel
    beside it (its eight neighbours) -- because a two-tone line reads where either tone
    stands off the paint: the graphite on a light ground, the casing on a dark one.
    """
    step = np.abs(values_of_rgb(drawn) - values_of_rgb(rgb)).astype(np.float32)
    core_step = step[core]
    if not casing.any():
        return core_step
    beside = Image.fromarray(np.where(casing, step, 0.0).astype(np.float32), mode="F")
    near = np.asarray(beside.filter(ImageFilter.MaxFilter(3)))
    return np.maximum(core_step, near[core])


GUIDE_KINDS = ("today", "casing", "casing 150", "ink")


def _corpus_pictures() -> list[tuple[str, np.ndarray]]:
    """Every committed painting's own picture, at the size a look shows it."""
    found = []
    for path in sorted((ROOT / "paintings").rglob("painting.png")):
        image = Image.open(path).convert("RGB")
        image = LOOK_MODULE._downsample(image, LOOK_MODULE.DEFAULT_LOOK_SIZE)
        found.append((str(path.parent.relative_to(ROOT / "paintings")).replace(os.sep, "/"),
                      np.asarray(image)))
    return found


def probe_guides(rb: Rebuilt, wb: Rebuilt | None) -> None:
    """4A1: each candidate's step at every guide pixel, over every ground there is."""
    heading("4A1: the guide candidates -- the step at every pixel of the line")
    guides = [dict(g) for g in rb.session.guides]
    grounds = []
    for name in sorted(GROUNDS):
        s = Session(1024, 768, texture="linen", ground=name, seed=11, timelapse=False,
                    out_dir=OUT / "scratch")
        grounds.append((f"ground {name}", _look_rgb(s)))
    mid = _flat(Session(1024, 768, texture="linen", ground="toned_grey", seed=11,
                        timelapse=False, out_dir=OUT / "scratch"), "#808080")
    grounds.append(("a flat mid-grey (0.50)", _look_rgb(mid)))
    grounds.append(("bell after the room", _look_rgb(rb.after["p02_room.py"])))
    grounds.append(("bell finished", _look_rgb(rb.session)))
    if wb is not None:
        grounds.append(("wenna finished", _look_rgb(wb.session)))
    pictures = _corpus_pictures()
    rows = []
    worst: dict[str, list[float]] = {k: [] for k in GUIDE_KINDS}
    for label, rgb in grounds + [(f"corpus {n}", a) for n, a in pictures]:
        aspect = rgb.shape[1] / rgb.shape[0]
        row = [label[:34], f"{float(np.mean(values_of_rgb(rgb))):.2f}"]
        for kind in GUIDE_KINDS:
            drawn, core, casing = draw_candidate(kind, rgb, guides, aspect, notes=False)
            vis = visibility(rgb, drawn, core, casing)
            under = float((vis < READS).mean())
            worst[kind].append(under)
            row.append(f"{np.median(vis):.2f}/{under:.0%}")
        rows.append(row)
    print(table(rows, ["under the line", "mean", *[f"{k}: med/<{READS}" for k in GUIDE_KINDS]]))
    print("  over all of them, the share of line pixels under the target: "
          + "; ".join(f"{k} median {np.median(v):.0%}, worst {max(v):.0%}"
                      for k, v in worst.items()))
    box = (0.18, 0.03, 0.72, 0.80)
    (OUT / "guides").mkdir(parents=True, exist_ok=True)
    for label, rgb in (("bell_after_room", _look_rgb(rb.after["p02_room.py"])),
                       ("bell_finished", _look_rgb(rb.session)),
                       ("mid_grey", _look_rgb(mid)),
                       ("warm_white", grounds[[g[0] for g in grounds].index("ground warm_white")][1])):
        panels = []
        for kind in GUIDE_KINDS:
            drawn, _, _ = draw_candidate(kind, rgb, guides, rgb.shape[1] / rgb.shape[0])
            panel = _crop_px(drawn, box)
            panel.save(OUT / "guides" / f"{_slug(kind)}_{label}.png")
            panels.append((kind, panel))
        print(f"  sheet: {save_sheet(panels, f'guides_{label}.png')}")


def _crop_px(rgb: np.ndarray, box: tuple[float, float, float, float]) -> Image.Image:
    h, w = rgb.shape[:2]
    x0, y0, x1, y1 = box
    return Image.fromarray(rgb[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)])


# -- 4A3: a thumbnail of the masses, flat, at drawing time -------------------------------

MASS_VERBS = ("block_in", "scumble", "cover")
THUMB_SIZES = (96, 128, 192, 256)


@dataclass
class Mass:
    """One mass a pass laid, as a thumbnail would take it: where, and at what value."""

    run: str
    verb: str
    place: object
    value: float
    holds: tuple = ()           # the outlines it was held to besides its own
    subject: bool = False


@contextlib.contextmanager
def recording(masses: list[Mass], current: list[str]):
    """Every mass verb records what it was handed and lays nothing; every other verb
    lays nothing either. What a thumbnail is: the arrangement, with no paint."""
    saved = {name: getattr(Session, name) for name in _WATCHED}
    sigs = {name: inspect.signature(saved[name]) for name in MASS_VERBS}

    def mass(name):
        def recorder(session, *args, **kw):
            named = _bound(sigs[name], session, args, kw)
            place = named.get("band") if name == "scumble" else named.get(
                "region" if name == "block_in" else "place")
            place = easel.regions.as_place(place)
            if name == "scumble":
                a = session.palette.value_of(session._resolve_color(named["color_a"]))
                b = session.palette.value_of(session._resolve_color(named["color_b"]))
                value = (a + b) / 2.0
            else:
                value = session.palette.value_of(session._resolve_color(named["color"]))
            holds = tuple(session_module._as_outlines(named.get("clip")))
            masses.append(Mass(run=current[0], verb=name, place=place, value=value,
                               holds=holds, subject="subject" in str(named.get("note", ""))))
            return []
        return recorder

    def nothing(session, *args, **kw):
        return None

    for name in _WATCHED:
        setattr(Session, name, mass(name) if name in MASS_VERBS else nothing)
    try:
        yield
    finally:
        for name, original in saved.items():
            setattr(Session, name, original)


def record_masses(runs: list[tuple[str, Path, Path]], painting: str = "bell") -> list[Mass]:
    """The masses a sequence of passes lays, ``(label, script, prelude)`` each, in order."""
    session = new_session(painting)
    masses: list[Mass] = []
    current = [""]
    with quiet(), recording(masses, current):
        for label, script, prelude in runs:
            current[0] = label
            result = run_script(session, script.read_text(encoding="utf-8-sig"), str(script),
                                prelude=prelude.read_text(encoding="utf-8-sig"),
                                prelude_name="prelude.py")
            if result.code:
                raise RuntimeError(f"{label}: {result.report}\n{result.trace}")
    return masses


def thumbnail(masses: list[tuple], width: int, height: int, ground: float,
              size: int | None = None) -> Image.Image:
    """The prototype: each place filled flat at its value, later over earlier, small.

    ``masses`` is ``(place, value)`` or ``(place, value, holds)``, in the order they
    would be painted, on the ground's own value; rendered at the canvas's size, in
    greyscale, and brought down to ``size`` on the long side the way a look is.
    """
    img = np.full((height, width), float(ground), dtype=np.float32)
    for entry in masses:
        place, value = entry[0], entry[1]
        mask = cohort._mask(easel.regions.as_place(place), width, height)
        if mask is None:
            continue
        for hold in (entry[2] if len(entry) > 2 else ()):
            mask = mask & hold.mask(width, height)
        img[mask] = float(value)
    grey = Image.fromarray((np.clip(img, 0.0, 1.0) * 255.0 + 0.5).astype(np.uint8), mode="L")
    return LOOK_MODULE._downsample(grey, size) if size else grey


def _bell_runs(p04: Path | None = None, p04_prelude: Path | None = None,
               p05: Path | None = None) -> list[tuple[str, Path, Path]]:
    prelude = BELL / "prelude.py"
    runs = [("p02_room.py", BELL / "p02_room.py", prelude),
            ("p03_plinth.py", BELL / "p03_plinth.py", prelude)]
    if p04 is not None:
        runs.append((p04.name, p04, p04_prelude or prelude))
    if p05 is not None:
        runs.append((p05.name, p05, prelude))
    return runs


def thumbnail_sets() -> dict[str, tuple[list[tuple], str]]:
    """The painter's own arrangements, as the masses each version laid, in order."""
    versions = BELL / "versions"
    sets = {
        "union": (_bell_runs(), "the first drawing: a union() of eight parts"),
        "cat": (_bell_runs(versions / "p04_v1_cat.py", versions / "prelude_cat.py"),
                "the cat: 32 points and a tail, lit planes on the shadow"),
        "piebald": (_bell_runs(versions / "p04_v2_piebald.py"), "the piebald: the planes as tiles"),
        "arch": (_bell_runs(versions / "p04_v3_arch.py"), "the arch: one lit side"),
        "rim": (_bell_runs(versions / "p04_v4_rim.py"), "the rim: two copies either way"),
        "bars": (_bell_runs(versions / "p04_v5_bars.py"), "the bars: the committed structure"),
        "final": (_bell_runs(BELL / "p04_gargoyle.py", None, BELL / "p05_details.py"),
                  "as committed, with the details pass's masses"),
    }
    out = {}
    for name, (runs, what) in sets.items():
        masses = record_masses(runs)
        entries = [(m.place, m.value, m.holds) for m in masses]
        if name == "union":
            scope = scope_of("bell", versions / "prelude_union.py")
            entries.append((scope["body"], 0.36, ()))
        out[name] = (entries, what)
    return out


def probe_thumbnail() -> None:
    """4A3: the painter's arrangements, flat and small, at four sizes."""
    heading("4A3: the thumbnail -- the painter's own masses, flat, at four sizes")
    w, h = CANVASES["bell"]["width"], CANVASES["bell"]["height"]
    ground = new_session("bell").palette.value_of(GROUNDS[CANVASES["bell"]["ground"]])
    sets = thumbnail_sets()
    started = time.time()
    rows = []
    for name, (entries, what) in sets.items():
        t0 = time.time()
        full = thumbnail(entries, w, h, ground)
        seconds = time.time() - t0
        panels = []
        for size in THUMB_SIZES:
            small = LOOK_MODULE._downsample(full, size)
            (OUT / "thumbnails").mkdir(parents=True, exist_ok=True)
            small.save(OUT / "thumbnails" / f"{name}_{size}.png")
            panels.append((f"{size} px", small.convert("RGB")))
        save_sheet(panels, f"thumbnail_{name}.png")
        rows.append([name, len(entries), f"{seconds * 1000:.0f} ms", what])
    print(table(rows, ["version", "masses", "rendered in", "what it was"]))
    print(f"  {len(sets)} sets in {time.time() - started:.1f} s; the thumbnails are under "
          f"{OUT / 'thumbnails'}, a sheet per version beside them")
    # With no argument the prototype draws the plan's own places -- which, for this
    # painting, are the room, the plinth's planes and the head's top, and no creature.
    s = new_session("bell")
    scope_of("bell", session=s)
    plan = s._plan
    planned = [(p.outline, p.value) for p in plan.values]
    small = thumbnail(planned, w, h, ground, 128)
    small.save(OUT / "thumbnails" / "plan_128.png")
    print(f"  the plan's own {len(planned)} places, with no argument: "
          f"{OUT / 'thumbnails' / 'plan_128.png'}")
    # And the final arrangement at 256 with the drawing over it, in the cased line.
    full = thumbnail(sets["final"][0], w, h, ground, 256).convert("RGB")
    guides = [dict(g, note="") for g in _drawing_guides()]
    drawn, _, _ = draw_candidate("casing 150", np.asarray(full), guides, w / h, notes=False)
    Image.fromarray(drawn).save(OUT / "thumbnails" / "final_256_guides.png")
    print(f"  the final arrangement with its drawing over it: "
          f"{OUT / 'thumbnails' / 'final_256_guides.png'}")
    # And the silhouette alone -- the recipe's `thumbnail({shape: dark})` -- per version.
    panels = []
    for name, (entries, _) in sets.items():
        subject = [e for e in entries[_room_and_plinth_count(sets):]]
        sil = [(e[0], 0.12, e[2]) for e in subject]
        panels.append((name, thumbnail(sil, w, h, 0.85, 128).convert("RGB")))
    print(f"  silhouettes at 128 px: {save_sheet(panels, 'thumbnail_silhouettes_128.png')}")


def _notches(shape: Polygon, w: int, h: int, least: float = 25.0) -> int:
    """How many times an outline turns sharply inward: the waists a union leaves."""
    pts = np.asarray(shape.points, dtype=np.float64) * [w, h]
    area = 0.5 * float(np.sum(pts[:, 0] * np.roll(pts[:, 1], -1)
                              - np.roll(pts[:, 0], -1) * pts[:, 1]))
    sign = 1.0 if area > 0 else -1.0
    a, b, c = np.roll(pts, 1, axis=0), pts, np.roll(pts, -1, axis=0)
    u, v = b - a, c - b
    cross = u[:, 0] * v[:, 1] - u[:, 1] * v[:, 0]
    turn = np.degrees(np.arctan2(cross, (u * v).sum(axis=1)))
    return int(((sign * turn) < -least).sum())


def swelling_member(kind: str, aspect: float, w: int, h: int) -> Polygon:
    """One member that swells and narrows, drawn with the shapes there are or would be.

    ``taper`` is ``ribbon(width, end_width)``, the narrowing there is; ``ellipses`` a
    ``union`` of round lobes along the path, each as wide as the member is there; and
    ``per point`` what ``ribbon(width=[...])`` would draw, emulated as a union of ribbons
    one a segment, each running from its point's width to the next one's.
    """
    regions = easel.regions
    path = [(0.30, 0.20), (0.38, 0.40), (0.46, 0.60), (0.50, 0.82)]
    widths = [0.030, 0.060, 0.042, 0.016]
    if kind == "taper":
        return regions.ribbon(path, widths[0], end_width=widths[-1], name=kind)
    if kind == "per point":
        return regions.union(*[regions.ribbon([path[i], path[i + 1]], widths[i],
                                              end_width=widths[i + 1])
                               for i in range(len(path) - 1)], name=kind)
    if kind == "ellipses, smoothed":
        return swelling_member("ellipses", aspect, w, h).smooth()
    dense = STROKE_MODULE.catmull_rom(np.asarray(path, dtype=np.float32)).astype(np.float64)
    ux, uy = (1.0, 1.0 / aspect) if aspect >= 1 else (aspect, 1.0)
    seg = np.hypot(np.diff(dense[:, 0]) * ux, np.diff(dense[:, 1]) * uy)
    at = np.r_[0.0, np.cumsum(seg)]
    knots = np.r_[0.0, np.cumsum(np.hypot(np.diff(np.asarray(path)[:, 0]) * ux,
                                          np.diff(np.asarray(path)[:, 1]) * uy))]
    knots = knots / knots[-1] * at[-1]
    lobes, d = [], 0.0
    while d <= at[-1]:
        i = min(int(np.searchsorted(at, d)), len(dense) - 1)
        width = float(np.interp(d, knots, widths))
        r = width / 2.0
        lobes.append(regions.ellipse((float(dense[i, 0]), float(dense[i, 1])), r / ux, r / uy))
        d += max(r * 0.8, 0.004)
    return regions.union(*lobes, name=kind)


def probe_parts() -> None:
    """4A4: whether a member that swells and narrows needs a width per point on ``ribbon``."""
    heading("4A4: a member that swells and narrows, three ways")
    w, h = CANVASES["bell"]["width"], CANVASES["bell"]["height"]
    rows, panels = [], []
    for kind in ("taper", "ellipses", "ellipses, smoothed", "per point"):
        shape = swelling_member(kind, w / h, w, h)
        mask = shape.mask(w, h)
        across = [int(mask[int(y * h)].sum()) for y in (0.25, 0.40, 0.60, 0.78)]
        rows.append([kind, len(shape.points), _notches(shape, w, h),
                     "/".join(str(a) for a in across)])
        full = thumbnail([(shape, 0.15)], w, h, 0.80)
        panels.append((f"{kind}, full size", full.crop((int(0.2 * w), int(0.12 * h),
                                                        int(0.62 * w), int(0.9 * h))).convert("RGB")))
        panels.append((f"{kind}, 128", LOOK_MODULE._downsample(full, 128).convert("RGB")))
    print(table(rows, ["member", "outline points", "notches over 25 degrees",
                       "px across at y .25/.40/.60/.78"]))
    print(f"  sheet: {save_sheet(panels, 'parts_member.png', columns=8)}")


def _drawing_guides() -> list[dict]:
    """The painter's own drawing -- ``p01_draw.py``'s guides -- as the view holds them."""
    s = new_session("bell")
    run_pass(s, BELL / "p01_draw.py", BELL / "prelude.py")
    return [dict(g) for g in s.guides]


def _room_and_plinth_count(sets) -> int:
    """How many masses the room and the plinth lay, which every version shares."""
    return len(record_masses(_bell_runs()))


# -- 4B: light on a form -- the terminator, not the feather ------------------------------

def terminator(outline, inside, margin: float = 0.004, step: float = 0.002,
               aspect: float = 4.0 / 3.0, least: float = 0.02) -> list[list[tuple[float, float]]]:
    """B2's helper, as the bench specifies it: where one outline runs inside another shape.

    The runs of ``outline`` that lie inside ``inside`` and at least ``margin`` from its
    edge -- ``margin`` and ``step`` a fraction of the canvas's long side, like a brush's
    size, which is why the canvas's ``aspect`` is needed. For a copy of a silhouette
    shifted away from the light and held to it, that is the terminator: the line
    between the zone the copy covers and the lit rim it leaves. A run shorter than
    ``least`` is left out: a stroke along it would be a dab.
    """
    ux, uy = (1.0, 1.0 / aspect) if aspect >= 1.0 else (aspect, 1.0)
    ring = np.asarray(outline.closed, dtype=np.float64)
    dense = []
    for a, b in zip(ring[:-1], ring[1:], strict=True):
        n = max(1, int(math.ceil(math.hypot((b[0] - a[0]) * ux, (b[1] - a[1]) * uy) / step)))
        dense.extend(a + (b - a) * (i / n) for i in range(n))
    dense = np.asarray(dense)
    edge = np.asarray(inside.closed, dtype=np.float64)
    a, b = edge[:-1], edge[1:]
    px, py = dense[:, 0:1] * ux, dense[:, 1:2] * uy
    ax, ay, bx, by = a[:, 0] * ux, a[:, 1] * uy, b[:, 0] * ux, b[:, 1] * uy
    dx, dy = bx - ax, by - ay
    t = np.clip(((px - ax) * dx + (py - ay) * dy) / np.maximum(dx * dx + dy * dy, 1e-12),
                0.0, 1.0)
    dist = np.hypot(ax + t * dx - px, ay + t * dy - py).min(axis=1)
    ok = inside.inside(dense[:, 0], dense[:, 1]) & (dist > margin)
    if ok.all() or not ok.any():
        return [[(float(x), float(y)) for x, y in dense]] if ok.all() else []
    start = int(np.argmin(ok))                      # begin on a point that is out
    order = np.r_[start:len(dense), 0:start]
    runs, current = [], []
    for i in order:
        if ok[i]:
            current.append((float(dense[i, 0]), float(dense[i, 1])))
        elif current:
            runs.append(current)
            current = []
    if current:
        runs.append(current)
    def length(run):
        xy = np.asarray(run) * [ux, uy]
        return float(np.hypot(*np.diff(xy, axis=0).T).sum())
    return [r for r in runs if len(r) >= 3 and length(r) >= least]


@contextlib.contextmanager
def offered(**names):
    """Names put in a pass's scope for the length of a bench, as ``easel`` would export them."""
    saved_all = list(easel.__all__)
    had = {name: getattr(easel, name, None) for name in names}
    for name, value in names.items():
        setattr(easel, name, value)
        if name not in easel.__all__:
            easel.__all__.append(name)
    try:
        yield
    finally:
        easel.__all__[:] = saved_all
        for name, value in had.items():
            if value is None:
                delattr(easel, name)
            else:
                setattr(easel, name, value)


def _sub(source: str, old: str, new: str, count: int) -> str:
    found = source.count(old)
    if found != count:                                        # pragma: no cover
        raise ValueError(f"expected {count} of {old!r} in the pass, found {found}")
    return source.replace(old, new)


_JOIN = '''
for _copy, _a, _b in ((rim_in, "lit_c", "mid_c"), (mid_in, "mid_c", "stone_shade")):
    for _run in terminator(_copy, body, margin=0.004, aspect=s.aspect):
        s.stroke(_run, "flat", p.mix(_a, _b, 0.5), size={size}, opacity={opacity}, load=1.0,
                 load_falloff=0.0, pressure="even", clip=body, note="subject")
'''
_SMUDGE = '''
for _copy in (rim_in, mid_in):
    for _run in terminator(_copy, body, margin=0.004, aspect=s.aspect):
        s.smudge(_run)
'''

#: Row 9's candidates, as changes to the painter's own subject pass.
TERMINATOR_KINDS = (
    ("as painted", lambda src: src),
    ("feather 0.012", lambda src: _sub(src, 'edge="hard", clip=body',
                                       'edge="hard", clip=body, feather=0.012', 2)),
    ("feather 0.03", lambda src: _sub(src, 'edge="hard", clip=body',
                                      'edge="hard", clip=body, feather=0.03', 2)),
    ("copies ragged", lambda src: _sub(src, 'edge="hard", clip=body', "clip=body", 2)),
    ("join", lambda src: src + _JOIN.format(size=0.010, opacity=0.6)),
    ("smudge", lambda src: src + _SMUDGE),
    ("soft copies", lambda src: _sub(_sub(src, '"flat", "mid_c", size=0.045',
                                          '"round_soft", "mid_c", size=0.045', 1),
                                     '"flat", "stone_shade", size=0.045',
                                     '"round_soft", "stone_shade", size=0.045', 1)),
)


def _bilinear(view: np.ndarray, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
    h, w = view.shape
    xs = np.clip(xs, 0, w - 1.001)
    ys = np.clip(ys, 0, h - 1.001)
    x0, y0 = np.floor(xs).astype(int), np.floor(ys).astype(int)
    fx, fy = xs - x0, ys - y0
    top = view[y0, x0] * (1 - fx) + view[y0, x0 + 1] * fx
    bottom = view[y0 + 1, x0] * (1 - fx) + view[y0 + 1, x0 + 1] * fx
    return top * (1 - fy) + bottom * fy


def rise_widths(view: np.ndarray, runs, reach: float = 12.0, every: float = 4.0,
                least: float = 0.04) -> list[float]:
    """The 10-to-90% rise across a line, in pixels, every few pixels along it.

    Each sample is the profile along the line's normal, averaged over three parallel
    profiles a pixel apart so the canvas's tooth does not decide it, from ``reach``
    pixels one side to ``reach`` the other; its two ends are the plateaus. A place
    where they are closer than ``least`` has no step to measure and is skipped.
    """
    h, w = view.shape
    out = []
    ts = np.arange(-reach, reach + 0.25, 0.5)
    for run in runs:
        pts = np.asarray(run, dtype=np.float64) * [w, h]
        seg = np.hypot(*np.diff(pts, axis=0).T)
        at = np.r_[0.0, np.cumsum(seg)]
        if at[-1] < 3 * every:
            continue
        for d in np.arange(every, at[-1] - every, every):
            i = int(np.searchsorted(at, d))
            p = pts[max(i - 1, 0)] + (pts[min(i, len(pts) - 1)] - pts[max(i - 1, 0)]) * \
                ((d - at[max(i - 1, 0)]) / max(seg[min(max(i - 1, 0), len(seg) - 1)], 1e-9))
            j0, j1 = max(i - 2, 0), min(i + 1, len(pts) - 1)
            tangent = pts[j1] - pts[j0]
            norm = math.hypot(*tangent)
            if norm < 1e-9:
                continue
            n = np.array([-tangent[1], tangent[0]]) / norm
            along = tangent / norm
            prof = np.mean([_bilinear(view, p[0] + ts * n[0] + k * along[0],
                                      p[1] + ts * n[1] + k * along[1]) for k in (-1, 0, 1)],
                           axis=0)
            lo, hi = float(np.median(prof[:5])), float(np.median(prof[-5:]))
            if abs(hi - lo) < least:
                continue
            f = (prof - lo) / (hi - lo)
            t10 = ts[np.argmax(f >= 0.1)]
            t90 = ts[len(f) - 1 - np.argmax(f[::-1] <= 0.9)]
            out.append(float(abs(t90 - t10)))
    return out


def _outline_runs(shape: Polygon) -> list[list[tuple[float, float]]]:
    return [[(float(x), float(y)) for x, y in shape.closed]]


def lay_terminator_kinds(rb: Rebuilt, label: str = "p04_gargoyle.py",
                         kinds=TERMINATOR_KINDS) -> dict[str, tuple[Session, list[str], int]]:
    """Each candidate laid on the canvas the subject's pass opened on."""
    source = (BELL / label).read_text(encoding="utf-8")
    prelude = (BELL / "prelude.py").read_text(encoding="utf-8")
    out = {}
    with offered(terminator=terminator):
        for name, change in kinds:
            s = rb.opened(label)
            _, codes = run_source(s, change(source), label, prelude)
            out[name] = (s, codes, s.history.stroke_count)
    return out


def probe_terminator(rb: Rebuilt, wb: Rebuilt | None) -> None:
    """4B: row 9's candidates at two sizes, the recipe's numbers, and the face (B4)."""
    heading("4B: the painter's subject pass, laid seven ways (row 9)")
    scope = scope_of("bell")
    body = scope["body"]
    rim_in, mid_in = body.shifted(0.010, 0.016), body.shifted(0.026, 0.040)
    rb1440 = rebuild("bell", upto="p01_draw.py (again)", width=1440, height=960)
    boxes = {"whole": (0.18, 0.03, 0.72, 0.80), "chest": (0.24, 0.32, 0.46, 0.62)}
    (OUT / "terminator").mkdir(parents=True, exist_ok=True)
    for size, built in (("1024x768", rb), ("1440x960", rb1440)):
        laid = lay_terminator_kinds(built)
        rows = []
        aspect = built.session.aspect
        t1 = terminator(rim_in, body, aspect=aspect)
        t2 = terminator(mid_in, body, aspect=aspect)
        for name, (s, codes, spent) in laid.items():
            view = plan_view(s)
            r1, r2 = rise_widths(view, t1), rise_widths(view, t2)
            sil = rise_widths(view, _outline_runs(body))
            sub = view[_box_mask(boxes["whole"], view.shape)]
            edges = cohort_edges_share(view, boxes["whole"])
            rows.append([name, spent, f"{np.median(r1):.1f}", f"{np.median(r2):.1f}",
                         f"{np.median(sil):.1f}", f"{edges:.0%}",
                         f"{float(np.std(sub)):.3f}", ", ".join(sorted(set(codes))) or "-"])
            for key, box in boxes.items():
                zoom = 2 if key == "chest" else 1
                crop(s, box, zoom=zoom).save(
                    OUT / "terminator" / f"{_slug(name)}_{size}_{key}.png")
        heading(f"4B at {size}: rise across each terminator and the silhouette, in px")
        print(table(rows, ["candidate", "strokes", "lit/mid", "mid/shade", "silhouette",
                           "edges<2.5", "spread", "said"]))
        for key in boxes:
            panels = [(name, Image.open(OUT / "terminator" / f"{_slug(name)}_{size}_{key}.png"))
                      for name, _ in TERMINATOR_KINDS]
            print(f"  sheet: {save_sheet(panels, f'terminator_{size}_{key}.png', columns=4)}")
    print(f"  the terminators: {len(t1)} run(s) of the mid copy's outline, "
          f"{sum(len(r) for r in t1)} points; {len(t2)} of the shade copy's")
    probe_terminator_numbers()
    if wb is not None:
        probe_face(wb)


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def _box_mask(box, shape) -> np.ndarray:
    h, w = shape
    mask = np.zeros(shape, dtype=bool)
    x0, y0, x1, y1 = box
    mask[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)] = True
    return mask


def cohort_edges_share(view: np.ndarray, box) -> float:
    """The ``edges:`` line's share of hard edges, over one box of the canvas."""
    h, w = view.shape
    x0, y0, x1, y1 = box
    line = easel.checklist.edges_line(view[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)])
    found = re.search(r"(\d+)% of edges", line)
    return int(found.group(1)) / 100.0 if found else float("nan")


# The recipe's own numbers, on an abstract form: one silhouette of parts, lit from the
# upper left, on a dark field. What the recipe's example will be made of.
_FORM_PRELUDE = '''
p = s.palette
p["field"] = p.at_value(p.mix("burnt_umber", "ultramarine", 0.3), 0.18)
p["lit"] = p.at_value(p.mix_many(["yellow_ochre", "burnt_umber", "titanium_white"], [1, 1, 3]), 0.52)
p["mid"] = p.at_value(p.mix_many(["burnt_umber", "ultramarine", "titanium_white"], [2, 1, 2]), 0.37)
p["shade"] = p.at_value(p.mix_many(["burnt_umber", "ultramarine", "titanium_white"], [3, 1.5, 1]), 0.27)
body = {shape}
'''
#: The form: a large mass, a smaller one overlapping it, and two members that narrow.
_FORM_SHAPE = ("union(ellipse((0.50, 0.56), 0.17, 0.21), ellipse((0.33, 0.36), 0.075, 0.09), "
               "ribbon([(0.58, 0.66), (0.66, 0.80), (0.70, 0.95)], 0.05, end_width=0.025), "
               "ribbon([(0.40, 0.70), (0.36, 0.82), (0.37, 0.95)], 0.045, end_width=0.03), "
               "name='form')")
_FORM_PASS = '''
s.block_in(Region(0, 0, 1, 1), "flat", "field", size=0.12, solid=True, direction=5)
s.dry()
rim_in = body.shifted({dx}, {dy})
mid_in = body.shifted({dx2}, {dy2})
s.block_in(body, "flat", "lit", size=0.05, solid=True, direction="axis", edge="hard")
s.block_in(rim_in, "flat", "mid", size=0.045, solid=True, direction=100, edge="hard",
           clip=body, opacity=1.0, pressure="even")
s.block_in(mid_in, "flat", "shade", size=0.045, solid=True, direction=18, edge="hard",
           clip=body, opacity=1.0, pressure="even")
{join}
'''
_FORM_JOIN = '''
for _copy, _a, _b in ((rim_in, "lit", "mid"), (mid_in, "mid", "shade")):
    for _run in terminator(_copy, body, margin=0.004, aspect=s.aspect):
        s.stroke(_run, "flat", p.mix(_a, _b, {value}), size={size}, opacity={opacity},
                 load=1.0, load_falloff=0.0, pressure="even", clip=body)
'''


def lay_form(shift: float = 0.016, join: dict | None = None, width: int = 1024,
             height: int = 768) -> tuple[Session, int]:
    """The abstract form, its copies shifted down and to the right, away from the light.

    ``shift`` is the mid copy's offset along the diagonal, a fraction of the long side
    as a brush's size is -- the painter's own was ``0.016`` -- and the shade copy goes
    two and a half times as far, as the painter's did.
    """
    s = Session(width, height, texture="linen", ground="umber_wash", seed=11,
                timelapse=False, out_dir=OUT / "scratch")
    dx, dy = _shift_xy(shift, s)
    dx2, dy2 = _shift_xy(2.5 * shift, s)
    source = _FORM_PASS.format(dx=dx, dy=dy, dx2=dx2, dy2=dy2,
                               join=_FORM_JOIN.format(**join) if join else "")
    with offered(terminator=terminator):
        run_source(s, source, "form.py", _FORM_PRELUDE.format(shape=_FORM_SHAPE))
    return s, s.history.stroke_count


def _form_body() -> Polygon:
    return eval(_FORM_SHAPE, {n: getattr(easel, n) for n in easel.__all__})  # noqa: S307


def probe_terminator_numbers() -> None:
    """The rim's width, and the join's width and value, on the recipe's abstract form."""
    heading("4B: the recipe's numbers, on an abstract form of parts")
    body = _form_body()
    rows, panels = [], []
    for shift in (0.008, 0.016, 0.024, 0.032):
        s, spent = lay_form(shift)
        view = plan_view(s)
        runs = terminator(body.shifted(*_shift_xy(shift, s)), body, aspect=s.aspect)
        rows.append([f"{shift:.3f}", f"{shift * s.canvas.long_side:.0f} px", spent,
                     f"{np.median(rise_widths(view, runs)):.1f}"])
        panels.append((f"shift {shift}", crop(s, (0.15, 0.15, 0.85, 1.0))))
    print(table(rows, ["shift", "at 1024", "strokes", "rise lit/mid"]))
    print(f"  sheet: {save_sheet(panels, 'form_shifts.png', columns=4)}")
    rows, panels = [], []
    s, spent = lay_form(0.016)
    view = plan_view(s)
    runs = terminator(body.shifted(*_shift_xy(0.016, s)), body, aspect=s.aspect)
    print(f"  without a join: rise {np.median(rise_widths(view, runs)):.1f} px, {spent} strokes")
    panels.append(("no join", crop(s, (0.25, 0.25, 0.60, 0.75))))
    for size in (0.006, 0.010, 0.016):
        for opacity in (0.4, 0.6, 0.8):
            s, spent = lay_form(0.016, join={"value": 0.5, "size": size, "opacity": opacity})
            view = plan_view(s)
            rises = rise_widths(view, runs)
            rows.append([f"{size:.3f}", f"{opacity:.1f}", spent, f"{np.median(rises):.1f}",
                         f"{np.percentile(rises, 90):.1f}"])
            panels.append((f"join {size} at {opacity}", crop(s, (0.25, 0.25, 0.60, 0.75))))
    print(table(rows, ["join size", "opacity", "strokes", "rise median", "rise p90"]))
    print(f"  sheet: {save_sheet(panels, 'form_joins.png', columns=5)}")


def _shift_xy(shift: float, s: Session) -> tuple[float, float]:
    """A shift of ``shift`` of the long side, down and to the right, in canvas units."""
    w, h = s.canvas.width, s.canvas.height
    long = max(w, h)
    d = shift / math.sqrt(2)
    return d * long / w, d * long / h


def probe_face(wb: Rebuilt) -> None:
    """B4: the second painter's face, laid as the shifted copies, the strip, and as painted."""
    heading("4B4: Wenna Brask's face -- the shifted copies, the strip, and the planes")
    versions = WENNA / "versions"
    kinds = (("shifted copies", versions / "p03_v1_profiles.py", versions / "prelude_early.py"),
             ("terminator beside the profile", versions / "p03_v2_strip.py",
              versions / "prelude_strip.py"),
             ("planes sharing the terminator", WENNA / "p03_figure.py", WENNA / "prelude.py"))
    rows, panels = [], []
    for name, script, prelude in kinds:
        s = wb.opened("p03_figure.py")
        run_pass(s, script, prelude)
        scope = scope_of("wenna", prelude)
        face = scope["face"]
        view = plan_view(s)
        h, w = view.shape
        mask = face.mask(w, h)
        p = scope["p"]
        cut = (p.value_of("skin_lit") + p.value_of("skin_shade")) / 2.0
        lit = mask & (view >= cut)
        across = []
        for y in range(h):
            xs = np.nonzero(mask[y])[0]
            if len(xs) < 8:
                continue
            across.append(float(lit[y, xs].mean()))
        x0, y0, x1, y1 = face.bounds
        box = (max(x0 - 0.05, 0), max(y0 - 0.05, 0), min(x1 + 0.05, 1), min(y1 + 0.03, 1))
        rows.append([name, s.history.stroke_count, f"{lit.sum() / mask.sum():.0%}",
                     f"{np.median(across):.0%}", f"{np.percentile(across, 25):.0%}-"
                                                  f"{np.percentile(across, 75):.0%}"])
        panels.append((name, crop(s, box, zoom=2)))
    print(table(rows, ["structure", "strokes", "lit share of the face",
                       "lit share of a row, median", "middle half of rows"]))
    print(f"  sheet: {save_sheet(panels, 'face_structures.png')}")


# -- the corpus, replayed once for every corpus bench ---------------------------------
#
# ``probe_cohort_session.py`` rebuilds every committed painting pass by pass with every
# call watched; this round's watcher is that one with three things added -- the call's
# site (its script, line and function), what each hand-laid mark landed at, and a small
# footprint of what every call painted -- and with the old round's candidates left out,
# which are most of that replay's time. What it keeps is kept in ``out/bell/corpus.pkl``.

#: How much coarser than the canvas a call's footprint is kept: an 8 by 8 block of
#: pixels is one cell, painted if any pixel in it moved.
FOOT = 8


def footprint(moved: np.ndarray) -> np.ndarray:
    h, w = moved.shape
    hh, ww = h // FOOT, w // FOOT
    return moved[:hh * FOOT, :ww * FOOT].reshape(hh, FOOT, ww, FOOT).any(axis=(1, 3))


def _path_px(record, w: int, h: int) -> tuple[np.ndarray, np.ndarray]:
    pts = np.asarray(record.points, dtype=np.float64).reshape(-1, 2)
    if len(pts) >= 3 and record.params.get("smooth", True):
        pts = STROKE_MODULE.catmull_rom(pts.astype(np.float32)).astype(np.float64)
    cols = np.clip((pts[:, 0] * w).astype(int), 0, w - 1)
    rows = np.clip((pts[:, 1] * h).astype(int), 0, h - 1)
    return rows, cols


def hand_mark(record, before: np.ndarray, after: np.ndarray, wet: np.ndarray | None,
              session: Session) -> dict:
    """What a mark laid by hand was meant to land at, and what it landed at.

    ``own`` is the value of the colour it was mixed at; ``under`` the median of what it
    landed on, over the pixels it moved by more than ``0.02`` -- or, for a mark that
    moved none, the canvas under its path; ``landed`` the median those pixels read
    after. And the causes the engine could name at the call: the tip's size in pixels,
    the wetness under the path, how much of the path its clip held out, and its load.
    """
    params = record.params
    h, w = before.shape
    rows, cols = _path_px(record, w, h)
    moved = np.abs(after - before) > 0.02
    under_path = float(np.median(before[rows, cols]))
    if moved.any():
        under, landed = float(np.median(before[moved])), float(np.median(after[moved]))
    else:
        under = landed = under_path
    held = params.get("clip")
    out_share = 0.0
    if held:
        holds = session_module._clips_from_params(held)
        xs, ys = cols / float(w), rows / float(h)
        inside = np.ones(len(xs), dtype=bool)
        for hold in holds:
            inside &= hold.inside(xs, ys)
        out_share = float(1.0 - inside.mean())
    color = np.asarray(params.get("color", (0.0, 0.0, 0.0)), dtype=np.float32)
    return {
        "brush": record.brush, "tip": params.get("tip", ""), "kind": record.kind,
        "size": float(params.get("size", 0.0)),
        "px": float(params.get("size", 0.0)) * session.canvas.long_side,
        "opacity": float(params.get("opacity", 1.0)), "load": float(params.get("load", 1.0)),
        "press": int(params.get("press", 1)), "points": len(record.points),
        "own": session.palette.value_of(color), "under": under, "under_path": under_path,
        "landed": landed, "moved": int(moved.sum()), "paint": float(record.paint),
        "wet": float(wet[rows, cols].mean()) if wet is not None else 0.0,
        "held_out": out_share, "note": str(record.note),
    }


@dataclass
class CorpusData:
    """What one replay of the corpus kept, per call and per pass."""

    calls: list[dict] = field(default_factory=list)
    passes: list[dict] = field(default_factory=list)
    finished: dict[str, dict] = field(default_factory=dict)
    errors: dict[str, list[str]] = field(default_factory=dict)
    seconds: dict[str, float] = field(default_factory=dict)
    engine: str = ""


class SiteWatcher(cohort.Watcher):
    """The corpus probe's watcher, keeping this round's measurements instead of its own."""

    data: CorpusData

    def _open_call(self, name, session, args, kw, line):
        call = super()._open_call(name, session, args, kw, line)
        call.site = _painter_site()
        call.pass_name = self.current.name if self.current is not None else ""
        call.painting = self.replay.painting.name
        return call

    def _judge(self, call, session) -> None:
        records = session.history.records[call.first:call.first + call.count]
        paid = [r for r in records if r.kind not in UNPAINTED]
        file, line, func = call.site
        entry = {"painting": call.painting, "pass": call.pass_name, "verb": call.verb,
                 "file": file, "line": line, "func": func,
                 "index": session._index_base + call.first, "count": call.count,
                 "paid": len(paid), "nothing": sum(1 for r in paid if r.paint < LANDED),
                 "vias": sorted({str(r.params.get("via", "")) for r in paid}),
                 "subject": "subject" in str(call.bound.get("note", "")).lower(),
                 "note": str(call.bound.get("note", "")), "foot": None, "hand": None,
                 "canvas": (session.canvas.width, session.canvas.height)}
        if call.before is not None and paid:
            after = session.canvas.values(sketch=False).astype(np.float32) / 255.0
            moved = np.abs(after - call.before) > 0.02
            entry["foot"] = np.packbits(footprint(moved))
            entry["foot_shape"] = footprint(moved).shape
            if (call.verb in ("stroke", "dab") and len(paid) == 1
                    and paid[0].kind == "stroke"):
                entry["hand"] = hand_mark(paid[0], call.before, after, call.wet, session)
        self.data.calls.append(entry)
        call.before = None
        call.wet = None

    def _judge_pass(self, done, session) -> None:
        view8 = session.canvas.values(sketch=False)
        h, w = view8.shape
        plan = session._plan
        places = []
        lines = []
        if plan.values or plan.lightest is not None:
            pv = session._value_view()
            named = [p for p in plan.values]
            if plan.lightest is not None and plan.lightest.name not in {p.name for p in named}:
                named.append(plan.lightest)
            for p in named:
                mask = p.outline.mask(w, h)
                if mask.any():
                    places.append({"name": p.name, "value": p.value, "area": float(mask.mean()),
                                   **readings(pv[mask])})
            lines = [plan.value_line(pv), plan.lightest_line(pv)]
        self.data.passes.append({
            "painting": self.replay.painting.name, "pass": done.name, "start": done.start,
            "end": done.end, "findings": list(done.findings), "spent": session.stroke_count,
            "flat": view8.reshape(-1)[::17].copy(),
            "reach": (session.palette.darkest_value, session.palette.lightest_value),
            "places": places, "plan_lines": [x for x in lines if x],
            "lightest": plan.lightest.name if plan.lightest is not None else None,
            "canvas": (w, h), "error": done.error})
        self.opened = None


def replay_corpus(names: list[str] | None = None, echo: bool = True) -> CorpusData:
    """Every committed painting rebuilt with this round's watcher; what it kept."""
    data = CorpusData(engine=easel.__version__)
    saved = cohort.Watcher
    cohort.Watcher = SiteWatcher
    SiteWatcher.data = data
    try:
        for entry in cohort.CORPUS:
            if names and entry.name not in names:
                continue
            started = time.time()
            rep = cohort.replay(entry, keep_canvas=True)
            data.seconds[entry.name] = time.time() - started
            data.errors[entry.name] = rep.errors
            if rep.session is not None:
                s = rep.session
                data.finished[entry.name] = {
                    "values": s.canvas.values(sketch=False),
                    "plan": s._value_view().astype(np.float16),
                    "reach": (s.palette.darkest_value, s.palette.lightest_value),
                    "spent": s.stroke_count,
                    "plan_places": [(p.name, p.value, np.asarray(p.outline.points))
                                    for p in s._plan.values],
                    "lightest": (None if s._plan.lightest is None else
                                 (s._plan.lightest.name,
                                  np.asarray(s._plan.lightest.outline.points))),
                }
            if echo:
                print(f"  {entry.name:<12} {len(rep.passes):3d} passes, "
                      f"{rep.spent:4d} strokes, {data.seconds[entry.name]:5.0f} s"
                      + (f"  [{'; '.join(rep.errors)[:80]}]" if rep.errors else ""),
                      flush=True)
    finally:
        cohort.Watcher = saved
    return data


def corpus(fresh: bool = False) -> CorpusData:
    """The corpus replay, from ``out/bell/corpus.pkl`` unless it is stale or asked afresh."""
    if CACHE.exists() and not fresh:
        with CACHE.open("rb") as handle:
            kept = _Unpickler(handle).load()
        data = kept if isinstance(kept, CorpusData) else CorpusData(**kept)
        if data.engine == easel.__version__:
            return data
    heading("the corpus, replayed with this round's watcher (about half an hour)")
    data = replay_corpus()
    OUT.mkdir(parents=True, exist_ok=True)
    with CACHE.open("wb") as handle:
        # Kept as a plain dict, so the cache reads the same whichever module wrote it.
        pickle.dump(vars(data), handle, protocol=pickle.HIGHEST_PROTOCOL)
    return data


class _Unpickler(pickle.Unpickler):
    """Reads a cache written with the probe run as ``__main__`` from anywhere else."""

    def find_class(self, module, name):
        if name == "CorpusData":
            return CorpusData
        return super().find_class(module, name)


# -- 4C: what a pass costs, call by call ------------------------------------------------

def pass_calls(data: CorpusData) -> dict[tuple[str, str], list[dict]]:
    """Every corpus pass's calls, by ``(painting, pass)``, in the order they were made."""
    out: dict[tuple[str, str], list[dict]] = {}
    for c in data.calls:
        out.setdefault((c["painting"], c["pass"]), []).append(c)
    return out


def dearest(calls: list[dict], share: float = 0.75, most: int = 4) -> tuple[list[dict], int]:
    """The calls the line names, as the painter decided it (question 8).

    Only calls that cost more than one stroke, dearest first, up to ``most``, and no
    more once ``share`` of the pass is named. Returns them and the pass's total.
    """
    total = sum(c["paid"] for c in calls)
    costly = sorted((c for c in calls if c["paid"] > 1), key=lambda c: -c["paid"])
    named, summed = [], 0
    for c in costly:
        if len(named) == most or summed >= share * total:
            break
        named.append(c)
        summed += c["paid"]
    return named, total


def dearest_line(named: list[dict], total: int) -> str:
    """The line: each call's strokes, verb and line, the function once per run of calls
    from it, and the strokes of it that landed nothing."""
    if not named:
        return ""
    parts, last = [], (None, None, None)
    for c in named:
        at = f"{c['file']}:{c['line']}" if c["file"] != last[0] else f":{c['line']}"
        verb = f" {c['verb']}" if c["verb"] != last[2] else ""
        said = [c["func"]] if c["func"] != last[1] and c["func"] not in ("<module>", "") else []
        if c["nothing"]:
            said.append(f"{c['nothing']} landing nothing")
        parts.append(f"{c['paid']}{verb} at {at}" + (f" ({', '.join(said)})" if said else ""))
        last = (c["file"], c["func"], c["verb"])
    return f"dearest: {', '.join(parts)} -- {sum(c['paid'] for c in named)} of the {total}"


def probe_cost(data: CorpusData) -> None:
    """4C: the dearest line over every pass of the corpus."""
    heading("4C: the dearest line over every corpus pass")
    passes = pass_calls(data)
    painted = {k: v for k, v in passes.items() if sum(c["paid"] for c in v) > 0}
    printed, lengths, counts, shares, short4 = [], [], {}, [], 0
    fixed3, fixed4 = [], []
    nothing_named = 0
    for key, calls in painted.items():
        named, total = dearest(calls)
        if not named:
            continue
        line = dearest_line(named, total)
        printed.append((key, line))
        lengths.append(len(line))
        counts[len(named)] = counts.get(len(named), 0) + 1
        shares.append(sum(c["paid"] for c in named) / total)
        costly = sorted((c for c in calls if c["paid"] > 1), key=lambda c: -c["paid"])
        fixed3.append(sum(c["paid"] for c in costly[:3]) / total)
        fixed4.append(sum(c["paid"] for c in costly[:4]) / total)
        if len(named) == 4 and shares[-1] < 0.75:
            short4 += 1
        nothing_named += any(c["nothing"] for c in named)
    print(f"  {len(painted)} passes lay paint; the line is printed on {len(printed)} "
          f"({len(printed) / max(len(painted), 1):.0%}) -- a pass with no call dearer than "
          f"one stroke says nothing")
    print("  calls named: " + ", ".join(f"{n}: {counts.get(n, 0)} passes" for n in (1, 2, 3, 4)))
    print(f"  share of the pass named: median {np.median(shares):.0%}, p10 {pct(shares, 10):.0%}; "
          f"four calls fall short of three quarters on {short4} passes")
    print(f"  a fixed three would name a median {np.median(fixed3):.0%} (p10 {pct(fixed3, 10):.0%}); "
          f"a fixed four {np.median(fixed4):.0%} (p10 {pct(fixed4, 10):.0%})")
    print(f"  the line's length: median {np.median(lengths):.0f} characters, p90 "
          f"{pct(lengths, 90):.0f}, longest {max(lengths)}")
    print(f"  a named call that landed strokes of nothing: on {nothing_named} passes")
    for key in (("bell", "p02_room.py"), ("bell", "p04_gargoyle.py"), ("bell", "p05_details.py"),
                ("wenna", "p03_figure.py")):
        line = next((ln for k, ln in printed if k == key), "")
        calls = passes.get(key, [])
        costly = sorted((c for c in calls if c["paid"] > 1), key=lambda c: -c["paid"])
        total = sum(c["paid"] for c in calls)
        three = sum(c["paid"] for c in costly[:3]) / max(total, 1)
        print(f"  {key[0]} {key[1]}: a fixed three names {three:.0%}\n    {line}")
    longest = sorted(printed, key=lambda kv: -len(kv[1]))[:3]
    for (painting, name), line in longest:
        print(f"  longest -- {painting} {name}:\n    {line}")
    heading("4C/4D: strokes charged that landed nothing, over the corpus")
    total_paid = sum(c["paid"] for c in data.calls)
    total_nothing = sum(c["nothing"] for c in data.calls)
    by: dict[str, list[int]] = {}
    for c in data.calls:
        if c["nothing"]:
            kind = c["verb"] if c["verb"] not in ("stroke", "dab") else _nothing_cause(c)
            by.setdefault(kind, [0, 0])
            by[kind][0] += c["nothing"]
            by[kind][1] += 1
    print(f"  {total_nothing} of {total_paid} charged strokes ({total_nothing / total_paid:.1%}) "
          f"laid under {LANDED} unit of paint")
    for kind, (n, calls) in sorted(by.items(), key=lambda kv: -kv[1][0]):
        print(f"    {kind:<34} {n:5d} strokes, from {calls} calls")
    per_painting: dict[str, list[int]] = {}
    for c in data.calls:
        per_painting.setdefault(c["painting"], [0, 0])
        per_painting[c["painting"]][0] += c["nothing"]
        per_painting[c["painting"]][1] += c["paid"]
    print("  by painting: " + "; ".join(f"{k} {v[0]}/{v[1]}" for k, v in per_painting.items()
                                        if v[0]))


def _nothing_cause(c: dict) -> str:
    """Why a mark laid by hand landed nothing, as far as the engine could say at the call."""
    h = c.get("hand")
    if not h:
        return f"{c['verb']} (not read)"
    if h["tip"] in ("round_hard", "round_soft", "liner") and h["points"] == 1:
        return f"a round dab at {h['px']:.1f} px, press={h['press']}"[:34]
    if h["tip"] == "bristle" and h["load"] < 0.5:
        return "a bristle loaded under 0.5"
    if h["held_out"] > 0.5:
        return "a mark its clip held out"
    return f"a {h['tip']} stroke at {h['px']:.1f} px"[:34]


# -- 4D, rewritten: a mark that lands short --------------------------------------------

#: A mark is *meant* to stand off what it lands on when its own value is this far away.
MEANT = 0.10


def shortfall(h: dict) -> dict:
    """How far a hand-laid mark got toward its own value, raw and for its opacity."""
    meant = h["own"] - h["under"]
    got = (h["landed"] - h["under"]) / meant if abs(meant) > 1e-6 else 1.0
    return {"meant": meant, "reached": got, "for_opacity": got / max(h["opacity"], 0.05)}


def probe_short(data: CorpusData, rb: Rebuilt | None) -> None:
    """4D as rewritten: every hand-laid mark's landed shortfall, and the cause it had."""
    heading("4D: every mark laid by hand, how far it got toward its own value")
    hands = [c for c in data.calls if c.get("hand") and c["hand"]["kind"] == "stroke"]
    meant = [c for c in hands if abs(shortfall(c["hand"])["meant"]) >= MEANT]
    reached = [shortfall(c["hand"])["reached"] for c in meant]
    opac = [shortfall(c["hand"])["for_opacity"] for c in meant]
    print(f"  {len(hands)} marks laid by hand; {len(meant)} meant to stand {MEANT:.2f} or more "
          f"off what they landed on")
    for name, xs in (("the way reached", reached), ("...for its opacity", opac)):
        print(f"  {name:<20} p5 {pct(xs, 5):.2f}  p10 {pct(xs, 10):.2f}  p25 {pct(xs, 25):.2f}  "
              f"median {np.median(xs):.2f}  p75 {pct(xs, 75):.2f}")
    bins = np.histogram(np.clip(opac, 0, 1.5), bins=np.arange(0, 1.55, 0.05))[0]
    print("  histogram of the way reached for its opacity, in twentieths from 0 to 1.5:")
    print("    " + " ".join(f"{n}" for n in bins))
    passes = {(p["painting"], p["pass"]) for p in data.passes}
    rows = []
    for threshold in (0.15, 0.25, 0.35, 0.5):
        fires = [c for c in meant if shortfall(c["hand"])["for_opacity"] < threshold]
        fired_passes = {(c["painting"], c["pass"]) for c in fires}
        rows.append([f"{threshold:.2f}", len(fires), len(fired_passes),
                     f"{len(fired_passes) / len(passes):.1%}",
                     ", ".join(sorted({c["painting"] for c in fires}))[:60]])
    print(table(rows, ["under", "marks", "passes", "of all passes", "paintings"]))
    known = {("bell", "p06_finish.py", 39): "the spark", ("bell", "p05_details.py", 50): "the ember",
             ("bell", "p05_details.py", 65): "a claw light", ("bell", "p05_details.py", 67): "a claw light",
             ("bell", "p05_details.py", 40): "a tooth", ("bell", "p05_details.py", 42): "a tooth"}
    heading("4D: the marks the painters named, and the causes the engine could see")
    rows = []
    for c in hands:
        name = known.get((c["painting"], c["file"], c["line"]))
        h = c["hand"]
        f = shortfall(h)
        wenna_small = (c["painting"] == "wenna" and (h["paint"] < LANDED or f["for_opacity"] < 0.35)
                       and abs(f["meant"]) >= MEANT)
        if not name and not wenna_small:
            continue
        rows.append([c["painting"], f"{c['file']}:{c['line']}", name or c["note"][:12],
                     h["tip"], f"{h['px']:.1f}", h["press"], f"{h['load']:.2f}",
                     f"{h['opacity']:.2f}", f"{h['own']:.2f}", f"{h['under']:.2f}",
                     f"{h['landed']:.2f}", f"{f['for_opacity']:.2f}", f"{h['paint']:.1f}",
                     f"{h['wet']:.2f}", f"{h['held_out']:.0%}"])
    print(table(rows, ["painting", "at", "mark", "tip", "px", "press", "load", "opac", "own",
                       "under", "landed", "reached", "paint", "wet", "held out"]))
    heading("4D: what the misses have in common")
    misses = [c for c in meant if shortfall(c["hand"])["for_opacity"] < 0.35]
    causes: dict[str, int] = {}
    for c in misses:
        causes[_short_cause(c["hand"])] = causes.get(_short_cause(c["hand"]), 0) + 1
    for cause, n in sorted(causes.items(), key=lambda kv: -kv[1]):
        print(f"  {cause:<44} {n}")
    probe_short_nothing(data)
    probe_short_guide_blocks()
    if rb is not None:
        probe_short_versions(rb)


#: Where a round tip stops laying paint, in pixels, by how many times it is pressed --
#: the landing grid in ``--claims``, at 1024x768 and at 1440x960 alike.
DAB_CLIFF = {1: 6.5, 2: 5.6, 3: 2.5}


def probe_short_nothing(data: CorpusData) -> None:
    """The narrow form: marks that laid under a unit of paint, and the cause each had."""
    heading("4D: marks laid by hand that landed nothing, by the cause the engine can name")
    passes = {(p["painting"], p["pass"]) for p in data.passes if p["spent"] > 0}
    hands = [c for c in data.calls if c.get("hand") and c["hand"]["kind"] == "stroke"]
    nothing = [c for c in hands if c["nothing"]]
    rows = []
    groups = {"every mark laid by hand": lambda h: True,
              "a round dab": lambda h: h["points"] == 1
              and h["tip"] in ("round_hard", "round_soft", "liner"),
              "...under its cliff at its press": lambda h: h["points"] == 1
              and h["tip"] in ("round_hard", "round_soft", "liner")
              and h["px"] < DAB_CLIFF.get(h["press"], 2.5),
              "a bristle loaded under 0.5": lambda h: h["tip"] == "bristle" and h["load"] < 0.5}
    for label, test in groups.items():
        laid = [c for c in hands if test(c["hand"])]
        none = [c for c in nothing if test(c["hand"])]
        where = {(c["painting"], c["pass"]) for c in none}
        rows.append([label, len(laid), len(none), len(where),
                     f"{len(where) / len(passes):.1%}",
                     ", ".join(sorted({c["painting"] for c in none}))[:56]])
    print(table(rows, ["marks", "laid", "landed nothing", "passes", "of all passes",
                       "paintings"]))
    dabs = [c for c in hands if c["hand"]["points"] == 1
            and c["hand"]["tip"] in ("round_hard", "round_soft", "liner")]
    for press in (1, 2, 3):
        mine = [c for c in dabs if c["hand"]["press"] == press]
        under = [c for c in mine if c["hand"]["px"] < DAB_CLIFF[press]]
        print(f"  press={press}: {len(mine)} round dabs, {sum(bool(c['nothing']) for c in mine)} "
              f"landed nothing; {len(under)} under {DAB_CLIFF[press]} px, "
              f"{sum(bool(c['nothing']) for c in under)} of them landed nothing")
    edges = [0, 0.25, 0.5, 1, 2, 4, 8, 16, 1e9]
    for label, test in (("round dabs", groups["a round dab"]),
                        ("starved bristles", groups["a bristle loaded under 0.5"])):
        counts = np.histogram([c["hand"]["paint"] for c in hands if test(c["hand"])],
                              bins=edges)[0]
        bins = [f"{a:g}-{b:g}" for a, b in zip(edges[:-2], edges[1:-1], strict=True)]
        bins.append(f"{edges[-2]:g} up")
        print(f"  the paint {label} laid, in units: "
              + ", ".join(f"{b} {n}" for b, n in zip(bins, counts, strict=True)))


def _short_cause(h: dict) -> str:
    """The cause a fact at the call could name, in the order the engine could test them."""
    if h["tip"] in ("round_hard", "round_soft") and h["points"] == 1:
        small = {1: 6.5, 2: 5.6}.get(h["press"], 2.5)
        if h["px"] < small:
            return f"a round dab under {small} px at press={h['press']}"
        return f"a round dab at press={h['press']}"
    if h["tip"] == "bristle" and h["load"] < 0.5:
        return "a bristle loaded under 0.5"
    if h["held_out"] >= 0.5:
        return "most of its path outside its clip"
    if h["px"] < 6.0:
        return "a stroke under 6 px"
    if h["wet"] >= 0.3:
        return "laid on paint wet at 0.3 or more"
    return "none of these"


def probe_short_guide_blocks() -> None:
    """Rule 2: the candidate over every python block of the guide."""
    heading("4D: the candidate against the guide's own code blocks")
    guide = cohort._import_script(ROOT / "scripts" / "check_guide_blocks.py")
    blocks = guide.guide_blocks(echo=False)
    data = CorpusData()
    saved = cohort.Watcher
    cohort.Watcher = SiteWatcher
    SiteWatcher.data = data
    ran = 0
    try:
        for number, (doc, block) in enumerate(blocks, 1):
            if guide.is_pseudo_code(block):
                continue
            rep = cohort.Replay(painting=cohort.Painting(name=f"{doc} block {number}", where=doc))
            with SiteWatcher() as watcher, warnings.catch_warnings():
                warnings.simplefilter("ignore")
                watcher.replay = rep
                with contextlib.redirect_stdout(io.StringIO()):
                    watcher.open(f"{doc} block {number}")
                    try:
                        exec(compile(guide.PREAMBLE + guide.runnable(block),  # noqa: S102
                                     f"<block {number}>", "exec"), {})
                    except Exception:                         # noqa: BLE001, S110
                        pass
                    watcher.close()
            ran += 1
    finally:
        cohort.Watcher = saved
    hands = [c for c in data.calls if c.get("hand") and c["hand"]["kind"] == "stroke"]
    nothing = [c for c in data.calls if c["paid"] and c["nothing"]]
    print(f"  marks that landed nothing: {len(nothing)} calls, in "
          f"{len({c['painting'] for c in nothing})} of {ran} blocks")
    for c in nothing:
        h = c.get("hand") or {}
        print(f"    {c['painting']}: {c['verb']}, {c['nothing']} of {c['paid']} strokes -- "
              f"{h.get('tip', '')} {h.get('px', 0.0):.1f} px load={h.get('load', 0.0):.2f}"
              f" on the check's own canvas")
    dabs = [c for c in nothing if (c.get("hand") or {}).get("points") == 1]
    print(f"  ...of them round dabs, which the narrow fact would name: {len(dabs)}")
    for threshold in (0.25, 0.35):
        fires = [c for c in hands if abs(shortfall(c["hand"])["meant"]) >= MEANT
                 and shortfall(c["hand"])["for_opacity"] < threshold]
        blocks_hit = sorted({c["painting"] for c in fires})
        print(f"  under {threshold:.2f}: fires on {len(blocks_hit)} of {ran} blocks "
              f"({len(fires)} marks) " + "; ".join(blocks_hit)[:300])
        for c in fires[:12]:
            h = c["hand"]
            print(f"    {c['painting']}: {h['tip']} {h['px']:.1f} px press={h['press']} "
                  f"load={h['load']:.2f} opacity={h['opacity']:.2f} own {h['own']:.2f} on "
                  f"{h['under']:.2f} landed {h['landed']:.2f} -- {_short_cause(h)}")


def probe_short_versions(rb: Rebuilt) -> None:
    """The two subject-pass versions that read the head's top at 0.56 and 0.54, laid wet
    and with the canvas dried before their planes: the one place a light met wet paint."""
    heading("4D: the head's top in the two versions that laid it wet (piebald, arch)")
    versions = BELL / "versions"
    prelude = (BELL / "prelude.py").read_text(encoding="utf-8")
    scope = scope_of("bell")
    head = scope["head_top"]
    for name in ("p04_v2_piebald.py", "p04_v3_arch.py"):
        source = (versions / name).read_text(encoding="utf-8")
        dried = _sub(source, "\nlay_planes()\n", "\ns.dry()\nlay_planes()\n", 1)
        got = []
        for label, text in (("as rehearsed", source), ("dried first", dried)):
            s = rb.opened("p04_gargoyle.py")
            calls: list[Call] = []
            check, _ = run_source(s, text, name, prelude, calls=calls)
            view = plan_view(s)
            h, w = view.shape
            r = readings(view[head.mask(w, h)])
            plane = next((c for c in calls if c.verb == "block_in"
                          and c.args.get("color") == "face_c"), None)
            lightest = next((x.strip() for x in check if "lightest:" in x), "")
            got.append(f"{label}: median {r['median']:.3f}, mean {r['mean']:.3f}, wet under "
                       f"the plane {plane.wet if plane else float('nan'):.3f} -- {lightest}")
        print(f"  {name}\n    " + "\n    ".join(got))


# -- 4E1: the values line under a declared key ----------------------------------------

def values_reading(flat8: np.ndarray, reach: tuple[float, float]) -> dict:
    """The ``values:`` line's numbers, from the thinned view a pass kept."""
    flat = flat8.astype(np.float32) / 255.0
    low, high = float(np.percentile(flat, 5)), float(np.percentile(flat, 95))
    centres = easel.checklist.clusters(flat)
    gaps = np.diff(centres)
    middle = (reach[0] + reach[1]) / 2.0
    if high < middle and low > middle:                          # pragma: no cover
        verdict = "no clear light or dark"
    elif high < middle:
        verdict = "no clear light"
    elif low > middle:
        verdict = "no clear dark"
    elif float(min(gaps)) < 0.10:
        verdict = "two read as one"
    else:
        verdict = "clear"
    return {"low": low, "high": high, "centres": centres, "gaps": gaps, "middle": middle,
            "verdict": verdict, "top100": float(np.percentile(flat, 99)),
            "range": high - low, "box": reach[1] - reach[0]}


def probe_key(data: CorpusData) -> None:
    """4E1: what the values line says over the corpus, and what it would say under a key."""
    heading("4E1: the values line over every corpus pass, and under key='low'")
    painted = [p for p in data.passes if p["spent"] > 0 and not p["error"]]
    readings_ = [(p, values_reading(p["flat"], p["reach"])) for p in painted]
    verdicts: dict[str, int] = {}
    for _, r in readings_:
        verdicts[r["verdict"]] = verdicts.get(r["verdict"], 0) + 1
    print(f"  {len(painted)} passes that had laid paint: "
          + ", ".join(f"{k} {v}" for k, v in sorted(verdicts.items(), key=lambda kv: -kv[1])))
    last = {}
    for p, r in readings_:
        last[p["painting"]] = r
    low_key = [k for k, r in last.items() if r["verdict"] == "no clear light"]
    high_key = [k for k, r in last.items() if r["verdict"] == "no clear dark"]
    print(f"  finished low-key (no clear light at the end): {', '.join(low_key) or 'none'}")
    print(f"  finished high-key (no clear dark at the end): {', '.join(high_key) or 'none'}")
    rows = []
    gaps_low: list[float] = []
    for name in low_key:
        mine = [(p, r) for p, r in readings_ if p["painting"] == name]
        said = sum(r["verdict"] == "no clear light" for _, r in mine)
        left = [r for _, r in mine if r["high"] >= r["middle"]]
        gaps = [float(min(r["gaps"])) for _, r in mine]
        gaps_low += gaps
        top = [r["high"] for _, r in mine]
        rows.append([name, len(mine), said, len(left), f"{min(top):.2f}-{max(top):.2f}",
                     f"{mine[-1][1]['middle']:.2f}",
                     f"{min(gaps):.3f}-{max(gaps):.3f}",
                     sum(g < 0.10 for g in gaps), sum(g < 0.05 for g in gaps),
                     sum(g < 0.10 * r['range'] / r['box'] for g, (_, r) in zip(gaps, mine, strict=True))])
    print(table(rows, ["low-key picture", "passes", "no clear light", "left its key",
                       "top twentieth", "middle", "closest clusters", "< 0.10", "< 0.05",
                       "< 0.10 scaled"]))
    if gaps_low:
        print(f"  the closest pair of clusters over the low-key pictures' passes: median "
              f"{np.median(gaps_low):.3f}, p10 {pct(gaps_low, 10):.3f}, p90 {pct(gaps_low, 90):.3f}")
    others = [float(min(r["gaps"])) for p, r in readings_ if p["painting"] not in low_key]
    print(f"  ...and over every other pass: median {np.median(others):.3f}, p10 "
          f"{pct(others, 10):.3f}")
    ranges = [r["range"] for p, r in readings_ if p["painting"] in low_key]
    if ranges:
        print(f"  the low-key pictures' 5th-95th range: median {np.median(ranges):.2f} "
              f"(the box {readings_[0][1]['box']:.2f})")


# -- 4E4: the named light, read as a light ------------------------------------------

def probe_lamp(data: CorpusData) -> None:
    """4E4: the lightest place of every plan, pass by pass, read as a place and as a light."""
    heading("4E4: the named light of every plan, pass by pass")
    for painting in sorted({p["painting"] for p in data.passes if p["lightest"]}):
        rows = []
        for p in data.passes:
            if p["painting"] != painting or p["spent"] == 0:
                continue
            light = next((x for x in p["places"] if x["name"] == p["lightest"]), None)
            if light is None:
                continue
            others = [x for x in p["places"] if x["name"] != p["lightest"]]
            best_other = max(others, key=lambda x: x["median"]) if others else None
            flat = p["flat"].astype(np.float32) / 255.0
            rows.append([p["pass"][:22], f"{light['value'] if light['value'] is not None else float('nan'):.2f}",
                         f"{light['median']:.3f}", f"{light['p90']:.3f}", f"{light['p95']:.3f}",
                         f"{light['max']:.3f}", f"{np.percentile(flat, 95):.2f}",
                         f"{np.percentile(flat, 99):.2f}",
                         f"{best_other['name'][:12]} {best_other['median']:.2f}" if best_other else "-",
                         f"{light['area']:.2%}"])
        print(f"  {painting}: the named light is {data.passes[[p['painting'] for p in data.passes].index(painting)]['lightest']!r}")
        print(table(rows, ["pass", "planned", "median", "p90", "p95", "max", "canvas p95",
                           "canvas p99", "lightest other (median)", "area"]))


# -- 4H4: a place laid over and over ----------------------------------------------------

REPAINT_VERBS = ("block_in", "scumble", "cover", "sweep")


def _foot(c: dict) -> np.ndarray | None:
    if c.get("foot") is None:
        return None
    shape = c["foot_shape"]
    return np.unpackbits(c["foot"])[:shape[0] * shape[1]].reshape(shape).astype(bool)


@contextlib.contextmanager
def footprinting(out: list[dict], current: list[str]):
    """Every outermost painting call's footprint, as the corpus watcher keeps it."""
    saved = {name: getattr(Session, name) for name in _WATCHED}
    depth = [0]

    def wrap(name, original):
        signature = inspect.signature(original)

        def wrapper(session, *args, **kw):
            if depth[0] or name in ("pencil", "erase", "dry"):
                return original(session, *args, **kw)
            depth[0] += 1
            try:
                named = _bound(signature, session, args, kw)
                before = values(session)
                first = len(session.history.records)
                result = original(session, *args, **kw)
                paid = [r for r in session.history.records[first:] if r.kind not in UNPAINTED]
                if paid:
                    moved = np.abs(values(session) - before) > 0.02
                    f = footprint(moved)
                    out.append({"run": current[0], "verb": name, "paid": len(paid),
                                "subject": "subject" in str(named.get("note", "")).lower(),
                                "foot": np.packbits(f), "foot_shape": f.shape})
                return result
            finally:
                depth[0] -= 1
        return wrapper

    for name, original in saved.items():
        setattr(Session, name, wrap(name, original))
    try:
        yield
    finally:
        for name, original in saved.items():
            setattr(Session, name, original)


#: The rehearsals filed in each painting's ``versions/``, in the order the painter ran
#: them, each with the prelude it ran on and the committed pass it was a version of --
#: whose canvas it was rehearsed on.
VERSION_RUNS = {
    "bell": [("p04_v1_cat.py", "prelude_cat.py", "p01_draw.py (again)"),
             ("p04_v2_piebald.py", None, "p04_gargoyle.py"),
             ("p04_v3_arch.py", None, "p04_gargoyle.py"),
             ("p04_v4_rim.py", None, "p04_gargoyle.py"),
             ("p04_v5_bars.py", None, "p04_gargoyle.py"),
             ("p05_v1.py", None, "p05_details.py"),
             ("p05_v2.py", None, "p05_details.py"),
             ("p05_v3.py", None, "p05_details.py")],
    "wenna": [("p02_v1.py", "prelude_glow1.py", "p02_setting.py"),
              ("p02_v2.py", "prelude_early.py", "p02_setting.py"),
              ("p02_v4.py", "prelude_early.py", "p02_setting.py"),
              ("p03_v1_profiles.py", "prelude_early.py", "p03_figure.py"),
              ("p03_v2_strip.py", "prelude_strip.py", "p03_figure.py"),
              ("p05_v1.py", None, "p05_face.py"),
              ("p06_v1.py", None, "p06_hand_cloth.py"),
              ("p08_v1.py", None, "p08_finish.py"),
              ("p09_v1.py", None, "p09_cloth_in_hand.py")],
}


def version_footprints(rb: Rebuilt) -> dict[str, list[dict]]:
    """Each filed rehearsal laid on the canvas it was rehearsed on; its calls' footprints."""
    out: dict[str, list[dict]] = {}
    folder = FOLDERS[rb.name]
    for script, prelude, before in VERSION_RUNS[rb.name]:
        calls: list[dict] = []
        s = rb.opened(before)
        with footprinting(calls, [f"{script} (rehearsed)"]):
            run_pass(s, folder / "versions" / script,
                     folder / "versions" / prelude if prelude else folder / "prelude.py")
        out[script] = calls
    return out


def repaint_places(runs: list[tuple[str, bool, list[dict]]], subject_only: bool = True,
                   rehearsed_marks: bool = False, over: float = 0.5,
                   meet: float = 0.3) -> list[dict]:
    """The places masses were laid over earlier marks, and how many runs laid them.

    ``runs`` are ``(label, rehearsal, calls)`` in the order the painter ran them. A mass
    *counts* when ``over`` of its footprint lies on marks laid in earlier runs -- the
    painter's ``subject`` marks, or every mark -- and counted masses whose footprints
    overlap by ``meet`` of the smaller are one place. A rehearsal's own marks are on a
    copy, so they are earlier marks only with ``rehearsed_marks``; its masses count
    either way, which is *rehearsals included*.
    """
    earlier = None
    places: list[dict] = []
    for label, rehearsal, calls in runs:
        mine = None
        for c in calls:
            f = _foot(c)
            if f is None:
                continue
            if earlier is None:
                earlier = np.zeros_like(f)
            if mine is None:
                mine = np.zeros_like(f)
            if c["verb"] in REPAINT_VERBS and f.sum() >= 4:
                share = float((f & earlier).sum()) / float(f.sum())
                if share >= over:
                    home = None
                    for place in places:
                        both = float((f & place["foot"]).sum())
                        if both >= meet * min(float(f.sum()), float(place["foot"].sum())):
                            home = place
                            break
                    if home is None:
                        home = {"foot": np.zeros_like(f), "runs": []}
                        places.append(home)
                    home["foot"] |= f
                    if label not in home["runs"]:
                        home["runs"].append(label)
            if not subject_only or c["subject"]:
                mine |= f
        if mine is not None and (not rehearsal or rehearsed_marks):
            earlier = mine if earlier is None else (earlier | mine)
    return places


def _where(place: dict) -> str:
    rows, cols = np.nonzero(place["foot"])
    h, w = place["foot"].shape
    return f"({cols.mean() / w:.2f}, {rows.mean() / h:.2f})"


def probe_repaint(data: CorpusData, rb: Rebuilt | None, wb: Rebuilt | None) -> None:
    """4H4: masses laid over the painter's own earlier marks, place by place."""
    heading("4H4: masses laid over earlier marks, counted by place")
    by_painting: dict[str, list[tuple[str, bool, list[dict]]]] = {}
    order: dict[str, list[str]] = {}
    for p in data.passes:
        order.setdefault(p["painting"], []).append(p["pass"])
    calls = pass_calls(data)
    for painting, names in order.items():
        by_painting[painting] = [(n, False, calls.get((painting, n), [])) for n in names]
    noted = sorted(k for k, runs in by_painting.items()
                   if any(c["subject"] for _, _, cs in runs for c in cs))
    print(f"  {len(noted)} of {len(by_painting)} paintings note their subject's marks: "
          + ", ".join(noted))
    rows = []
    for painting, runs in by_painting.items():
        subject = repaint_places(runs, subject_only=True) if painting in noted else []
        every = repaint_places(runs, subject_only=False)
        twice_s = [pl for pl in subject if len(pl["runs"]) >= 2]
        twice_e = [pl for pl in every if len(pl["runs"]) >= 2]
        rows.append([painting, len(runs),
                     f"{len(twice_s)}" if painting in noted else "-",
                     "; ".join(f"{_where(pl)} x{len(pl['runs'])}" for pl in twice_s)[:48],
                     len(twice_e), max((len(pl["runs"]) for pl in every), default=0)])
    print(table(rows, ["painting", "passes", "subject places laid over twice", "where",
                       "any places laid over twice", "most"]))
    for built in (rb, wb):
        if built is None:
            continue
        rehearsed = version_footprints(built)
        runs = []
        committed = by_painting.get(built.name, [])
        pending = list(VERSION_RUNS[built.name])
        for label, _, cs in committed:
            for script, _, before in list(pending):
                if before == label:
                    runs.append((f"{script} (rehearsed)", True, rehearsed[script]))
                    pending.remove((script, _, before))
            runs.append((label, False, cs))
        heading(f"4H4: {built.name}, its filed rehearsals included")
        for rehearsed_marks in (False, True):
            places = repaint_places(runs, subject_only=True, rehearsed_marks=rehearsed_marks)
            what = ("a rehearsal's marks count as earlier marks" if rehearsed_marks
                    else "only committed marks are earlier marks")
            print(f"  {what}:")
            for pl in places:
                runs_ = pl["runs"]
                print(f"    at {_where(pl)}, {len(runs_)} runs: {', '.join(runs_)}"
                      + ("  -- speaks at " + runs_[1] if len(runs_) >= 2 else ""))


# -- 4E2: what a place reads -------------------------------------------------------------

READS_AT = ("mean", "median", "p75", "p90")


def probe_place(data: CorpusData) -> None:
    """4E2: the plans' places pass by pass, and places with a detail put in them."""
    heading("4E2: the three plans, pass by pass -- the plan and lightest lines each way")
    for painting in sorted({p["painting"] for p in data.passes if p["places"]}):
        rows = []
        for p in data.passes:
            if p["painting"] != painting or p["spent"] == 0 or not p["places"]:
                continue
            planned = [x for x in p["places"] if x["value"] is not None]
            row = [p["pass"][:22]]
            for how in READS_AT:
                inside = sum(abs(x[how] - x["value"]) <= 0.10 for x in planned)
                row.append(f"{inside}/{len(planned)}")
            for how in READS_AT:
                top = max(p["places"], key=lambda x: x[how])
                row.append("yes" if top["name"] == p["lightest"] else top["name"][:10])
            splits = [f"{x['name'][:10]} {x['split']:.0%}" for x in p["places"] if x["split"] >= 0.10]
            row.append(", ".join(splits) or "-")
            rows.append(row)
        print(f"  {painting}:")
        print(table(rows, ["pass", *[f"plan by {h}" for h in READS_AT],
                           *[f"lightest by {h}" for h in READS_AT], "split >= 10%"]))
    probe_place_synthetic(data)


def probe_place_synthetic(data: CorpusData, per: int = 24, seed: int = 7) -> None:
    """Places on every finished corpus canvas, each given a detail of known size and value.

    A detail is the pixels of the place nearest one point inside it, set ``0.30`` darker
    or lighter than the place's own median: what an eye does to a planned plane. Each
    reading's error is what it reads with the detail against what it read without.
    """
    heading("4E2: a detail put inside a place -- how far each reading moves")
    rng = np.random.default_rng(seed)
    covers = (0.05, 0.10, 0.20, 0.30, 0.45, 0.55)
    errors = {(side, c, how): [] for side in ("dark", "light") for c in covers for how in READS_AT}
    split_fires = {(side, c): [] for side in ("dark", "light") for c in covers}
    natural_split = []
    for fin in data.finished.values():
        view = fin["plan"].astype(np.float32)
        h, w = view.shape
        places = [polygon(pts) for _, _, pts in fin["plan_places"]]
        long = max(w, h)
        for _ in range(per):
            r = rng.uniform(0.04, 0.12)
            cx, cy = rng.uniform(0.15, 0.85), rng.uniform(0.15, 0.85)
            places.append(easel.regions.ellipse((cx, cy), r * long / w, r * long / h))
        for place in places:
            mask = place.mask(w, h)
            if mask.sum() < 400:
                continue
            ys, xs = np.nonzero(mask)
            base = view[mask]
            med = float(np.median(base))
            natural_split.append(float((np.abs(base - med) > 0.15).mean()))
            before = {how: readings(base)[how] for how in READS_AT}
            k = rng.integers(len(ys))
            order = np.argsort((ys - ys[k]) ** 2 + (xs - xs[k]) ** 2)
            for c in covers:
                idx = order[:int(c * len(order))]
                for side, sign in (("dark", -1.0), ("light", 1.0)):
                    x = base.copy()
                    x[idx] = np.clip(med + sign * 0.30, 0.02, 0.98)
                    got = readings(x)
                    for how in READS_AT:
                        errors[(side, c, how)].append(abs(got[how] - before[how]))
                    split_fires[(side, c)].append(got["split"] >= 0.10)
    rows = []
    for side in ("dark", "light"):
        for c in covers:
            rows.append([side, f"{c:.0%}", *[f"{np.median(errors[(side, c, how)]):.3f}"
                                              for how in READS_AT],
                         f"{np.mean(split_fires[(side, c)]):.0%}"])
    print(table(rows, ["detail", "covering", *[f"{h} moves" for h in READS_AT],
                       "split says so"]))
    print(f"  {len(natural_split)} places with no detail put in: the split clause (a tenth "
          f"or more, over 0.15 from the median) fires on {np.mean(np.asarray(natural_split) >= 0.10):.0%}; "
          f"median share {np.median(natural_split):.1%}, p90 {pct(natural_split, 90):.1%}")


# -- 4E3: the floor, and the darks re-laid under it -------------------------------------

@contextlib.contextmanager
def deeper_darks(to: float, top: float = 0.20):
    """Every colour laid darker than ``top`` taken further down, toward ``to`` at the floor.

    The span from the box's floor to ``top`` is stretched to run from ``to`` instead --
    what a painter handed a near-black at ``to`` could lay -- by scaling each colour's
    linear light, so its hue is kept. Colours above ``top`` are laid as they were.
    """
    original = Session._resolve_color
    floor = min(Session().palette.value_of(n) for n in ("burnt_umber",))

    def resolve(self, color):
        lin = np.asarray(original(self, color), dtype=np.float32)
        lum = float(luminance(lin))
        v = float(linear_to_srgb(np.float32(lum)))
        if 0.0 < v < top:
            new = (to + (v - floor) * (top - to) / (top - floor)) if v >= floor else v * to / floor
            target = float(srgb_to_linear_scalar(new))
            lin = np.clip(lin * (target / max(lum, 1e-6)), 0.0, 1.0).astype(np.float32)
        return lin

    Session._resolve_color = resolve
    try:
        yield
    finally:
        Session._resolve_color = original


def srgb_to_linear_scalar(v: float) -> float:
    from easel.color import srgb_to_linear
    return float(srgb_to_linear(np.float32(v)))


#: The low-key pictures that sit on the floor (row 13), and the round's two.
FLOOR_PICTURES = ("bell", "wenna", "glm", "pool", "gemini", "bigpickle")


def probe_floor() -> None:
    """4E3: each low-key picture rebuilt, and rebuilt with its darks taken under the floor."""
    heading("4E3: the darks of the pictures on the floor, re-laid down to 0.07")
    (OUT / "floor").mkdir(parents=True, exist_ok=True)
    rows = []
    for name in FLOOR_PICTURES:
        entry = _ENTRIES[name]
        got = {}
        for label, to in (("as painted", None), ("to 0.07", 0.07)):
            patch = deeper_darks(to) if to is not None else contextlib.nullcontext()
            with patch:
                rep = cohort.replay(entry, keep_canvas=False)
            s = rep.session
            got[label] = (s.canvas.values(sketch=False).astype(np.float32) / 255.0,
                          s.canvas.to_srgb8(impasto=True, sketch=False), s)
            Image.fromarray(got[label][1]).save(OUT / "floor" / f"{name}_{_slug(label)}.png")
        a, b = got["as painted"][0], got["to 0.07"][0]
        row = [name]
        for view in (a, b):
            row += [f"{np.percentile(view, 1):.3f}", f"{np.percentile(view, 5):.3f}",
                    f"{(view < 0.15).mean():.0%}"]
        s = got["as painted"][2]
        if s._plan.values:
            h, w = a.shape
            darks = [p for p in s._plan.values if p.value is not None and p.value <= 0.22]
            spread = []
            for view in (a, b):
                meds = [float(np.median(view[p.outline.mask(w, h)])) for p in darks]
                spread.append(f"{min(meds):.2f}-{max(meds):.2f}")
            row += [" / ".join(spread)]
        else:
            row += ["-"]
        rows.append(row)
        save_sheet([("as painted", Image.fromarray(got["as painted"][1])),
                    ("darks to 0.07", Image.fromarray(got["to 0.07"][1]))],
                   f"floor_{name}.png")
    print(table(rows, ["picture", "p1", "p5", "under 0.15", "p1 re-laid", "p5 re-laid",
                       "under 0.15 re-laid", "planned darks' medians, as painted / re-laid"]))


# -- 4I2: an inward scumble's rings ----------------------------------------------------

def ring_amplitude(view: np.ndarray, place: Polygon, rays: int = 24) -> float:
    """The rings a patch shows, as the ripple left along its radii once the ramp is out.

    Along each ray from the patch's centre to its edge, in pixels, the values are
    smoothed over five pixels (the tooth) and the ramp over thirty-one taken away; what
    is left is the rings. The median over the rays of its RMS is the number.
    """
    h, w = view.shape
    cx, cy = place.center[0] * w, place.center[1] * h
    out = []
    for k in range(rays):
        a = 2 * math.pi * k / rays
        dx, dy = math.cos(a), math.sin(a)
        r = 0.0
        while r < max(w, h) and place.contains((cx + r * dx) / w, (cy + r * dy) / h):
            r += 1.0
        ts = np.arange(0.1 * r, 0.95 * r, 0.5)
        if len(ts) < 80:
            continue
        prof = _bilinear(view, cx + ts * dx, cy + ts * dy)
        smooth = np.convolve(prof, np.ones(10) / 10, mode="valid")
        trend = np.convolve(smooth, np.ones(62) / 62, mode="valid")
        resid = smooth[31:31 + len(trend)] - trend
        out.append(float(np.sqrt(np.mean(resid ** 2))))
    return float(np.median(out)) if out else float("nan")


def probe_rings() -> None:
    """4I2: an inward scumble on a dark ground, ring count by ring count."""
    heading("4I2: an inward scumble's rings on a dark ground")
    cases = (("the Bell-Warden's glow", "bell", "blob((0.30, 0.31), 0.21, 0.29, wobble=0.22, "
              "points=13, seed=5, rotate=-12)", "wall", "glow"),
             ("the lamp's pool", "wenna", "blob(P(598, 300), 0.24, 0.17, wobble=0.2, points=13, "
              "seed=5)", "mill", "glow_wall"))
    (OUT / "rings").mkdir(parents=True, exist_ok=True)
    for label, painting, shape, dark, light in cases:
        rows, panels = [], []
        for n in (4, 6, 8, 10, 12, 14, 16, 18, 20):
            s = new_session(painting)
            scope = scope_of(painting, session=s)
            place = eval(shape, scope)                                     # noqa: S307
            prelude = (FOLDERS[painting] / "prelude.py").read_text(encoding="utf-8")
            run_source(s, f"s.block_in(Region(0, 0, 1, 1), 'flat', {dark!r}, size=0.12, "
                          f"solid=True, direction=5)\ns.dry()\n", "field.py", prelude)
            laid = s.history.stroke_count
            _, codes = run_source(s, f"s.scumble({shape}, {dark!r}, {light!r}, {n}, "
                                     f"direction='inward')\n", "glow.py", prelude)
            view = values(s)
            h, w = view.shape
            mask = place.mask(w, h)
            field = float(np.median(view[~mask]))
            edge_band = mask & ~place.inset(0.02).mask(w, h)
            rows.append([n, s.history.stroke_count - laid, f"{ring_amplitude(view, place):.4f}",
                         f"{float(np.median(view[edge_band])) - field:+.3f}",
                         ", ".join(sorted(set(codes))) or "-"])
            x0, y0, x1, y1 = place.bounds
            panels.append((f"n={n}", crop(s, (max(x0 - 0.03, 0), max(y0 - 0.03, 0),
                                              min(x1 + 0.03, 1), min(y1 + 0.03, 1)))))
        print(f"  {label} ({dark} to {light}):")
        print(table(rows, ["n", "strokes", "ring ripple", "rim against the field",
                           "said at the scumble"]))
        print(f"  sheet: {save_sheet(panels, f'rings_{painting}.png', columns=5)}")


# -- 4H2: names a pass binds again ------------------------------------------------------

def bound_names(source: str) -> dict[str, tuple[int, str, str]]:
    """The names a script binds at its top level: ``{name: (line, value source, how)}``.

    Top level only -- a name bound inside a function is the function's -- but through
    the ``if``, ``for``, ``with`` and ``try`` blocks a script runs at the top. ``how`` is
    ``assign``, ``def``, ``import``, ``loop`` or ``with``: a loop leaves its variable
    bound at the top of a script, and a pass that loops over its own points binds it
    again without meaning anything by it.
    """
    tree = ast.parse(source)
    found: dict[str, tuple[int, str, str]] = {}

    def target(node, line: int, value: str, how: str) -> None:
        if isinstance(node, ast.Name):
            found.setdefault(node.id, (line, value, how))
        elif isinstance(node, (ast.Tuple, ast.List)):
            for elt in node.elts:
                target(elt, line, "", how)
        elif isinstance(node, ast.Starred):
            target(node.value, line, "", how)

    def walk(body) -> None:
        for node in body:
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    target(t, node.lineno, ast.unparse(node.value), "assign")
            elif isinstance(node, (ast.AnnAssign, ast.AugAssign)):
                target(node.target, node.lineno,
                       ast.unparse(node.value) if node.value else "", "assign")
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                found.setdefault(node.name, (node.lineno, f"def {node.name}", "def"))
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    found.setdefault(alias.asname or alias.name.split(".")[0],
                                     (node.lineno, "import", "import"))
            elif isinstance(node, (ast.For, ast.AsyncFor)):
                target(node.target, node.lineno, "", "loop")
                walk(node.body)
                walk(node.orelse)
            elif isinstance(node, (ast.With, ast.AsyncWith)):
                for item in node.items:
                    if item.optional_vars is not None:
                        target(item.optional_vars, node.lineno, "", "with")
                walk(node.body)
            elif isinstance(node, (ast.If, ast.While)):
                walk(node.body)
                walk(node.orelse)
            elif isinstance(node, ast.Try):
                walk(node.body)
                for handler in node.handlers:
                    walk(handler.body)
                walk(node.orelse)
                walk(node.finalbody)
    walk(tree.body)
    return found


def probe_rebind() -> None:
    """4H2: every corpus pass that binds a name its prelude bound, and to what."""
    heading("4H2: names a pass binds that its prelude bound")
    rows = []
    passes = 0
    with_prelude = 0
    for entry in cohort.CORPUS:
        prelude = entry.folder / "prelude.py"
        if entry.driver or not prelude.exists():
            continue
        with_prelude += 1
        mine = bound_names(prelude.read_text(encoding="utf-8-sig"))
        for name in dict.fromkeys(entry.passes):
            path = entry.folder / name
            passes += 1
            theirs = bound_names(path.read_text(encoding="utf-8-sig"))
            for key in sorted(set(mine) & set(theirs)):
                same = mine[key][1] == theirs[key][1] and mine[key][1] != ""
                rows.append([entry.name, name, key, theirs[key][0],
                             "the same value" if same else theirs[key][1][:40],
                             mine[key][2] in ("assign", "def", "import")])
    for painting in ("bell", "wenna"):
        folder = FOLDERS[painting]
        for script, prelude, _ in VERSION_RUNS[painting]:
            mine = bound_names((folder / "versions" / prelude if prelude else
                                folder / "prelude.py").read_text(encoding="utf-8-sig"))
            theirs = bound_names((folder / "versions" / script).read_text(encoding="utf-8-sig"))
            for key in sorted(set(mine) & set(theirs)):
                same = mine[key][1] == theirs[key][1] and mine[key][1] != ""
                rows.append([painting, f"versions/{script}", key, theirs[key][0],
                             "the same value" if same else theirs[key][1][:40],
                             mine[key][2] in ("assign", "def", "import")])
    hit = {(r[0], r[1]) for r in rows}
    print(f"  {passes} committed passes of {with_prelude} paintings run after a prelude; "
          f"{len({h for h in hit if not h[1].startswith('versions/')})} of them bind a name "
          f"the prelude bound, and {len({h for h in hit if h[1].startswith('versions/')})} "
          f"filed rehearsals do")
    print(table([r[:5] + ["the prelude's own" if r[5] else "a loop's variable"] for r in rows],
                ["painting", "pass", "name", "line", "bound again to", "the prelude bound it as"]))
    narrow = [r for r in rows if r[4] != "the same value" and r[5]]
    print(f"  bound again to something else, where the prelude bound it by assignment, def or "
          f"import and not only as a loop's variable: {len({(r[0], r[1]) for r in narrow})} "
          f"passes" + (" -- " + "; ".join(f"{r[0]} {r[1]} {r[2]}" for r in narrow) if narrow else ""))


# -- 4A5: the corpus's own pixel helpers and hand-moved groups --------------------------

_CANVAS_SIDES = {1024, 768, 1440, 960, 1200, 800, 1152, 720, 1120, 860, 900, 600}


def _refs(node, names: set[str]) -> bool:
    return any(isinstance(n, ast.Name) and n.id in names for n in ast.walk(node))


def _pixel_pair(ret, args: set[str]) -> bool:
    return (isinstance(ret, ast.Tuple) and len(ret.elts) == 2
            and all(isinstance(e, ast.BinOp) and isinstance(e.op, ast.Div) and _refs(e.left, args)
                    for e in ret.elts))


def _scale_pair(ret, args: set[str]) -> bool:
    """``(cx + (x - cx) * k, ...)``: points moved or scaled about a centre, by hand.

    Not a projection -- a perspective helper divides by one of its own arguments, and
    that is a unit of the painter's own rather than a group moved as one.
    """
    def offset(n) -> bool:
        """``(x - c)``: a point's own coordinate, less a centre."""
        return (isinstance(n, ast.BinOp) and isinstance(n.op, ast.Sub) and _refs(n.left, args)
                and not _refs(n.right, args))

    def about(e) -> bool:
        divides = any(isinstance(n, ast.BinOp) and isinstance(n.op, ast.Div)
                      and _refs(n.right, args) for n in ast.walk(e))
        return not divides and any(
            isinstance(n, ast.BinOp) and isinstance(n.op, ast.Mult)
            and (offset(n.left) or offset(n.right)) for n in ast.walk(e))
    return isinstance(ret, ast.Tuple) and len(ret.elts) == 2 and all(about(e) for e in ret.elts)


def unit_helpers(source: str) -> dict[str, list]:
    tree = ast.parse(source)
    out = {"pixel helpers": [], "scale helpers": [], "pixel divisions": 0, "shifted": 0,
           "scaled": 0, "aspect=": 0, "s.circle": 0}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.Lambda)):
            args = {a.arg for a in node.args.args}
            rets = ([n.value for n in ast.walk(node) if isinstance(n, ast.Return) and n.value]
                    if isinstance(node, ast.FunctionDef) else [node.body])
            name = getattr(node, "name", "lambda")
            if any(_pixel_pair(r, args) for r in rets):
                out["pixel helpers"].append(name)
            elif any(_scale_pair(r, args) for r in rets):
                out["scale helpers"].append(name)
        elif isinstance(node, (ast.ListComp, ast.GeneratorExp)):
            targets = {n.id for g in node.generators for n in ast.walk(g.target)
                       if isinstance(n, ast.Name)}
            if _scale_pair(node.elt, targets):
                out["scale helpers"].append("a comprehension")
            elif _pixel_pair(node.elt, targets):
                out["pixel helpers"].append("a comprehension")
        elif (isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div)
              and isinstance(node.right, ast.Constant) and node.right.value in _CANVAS_SIDES):
            out["pixel divisions"] += 1
        elif isinstance(node, ast.Attribute) and node.attr in ("shifted", "scaled"):
            out[node.attr] += 1
        elif isinstance(node, ast.keyword) and node.arg == "aspect":
            out["aspect="] += 1
        elif (isinstance(node, ast.Attribute) and node.attr == "circle"
              and isinstance(node.value, ast.Name) and node.value.id in ("s", "session")):
            out["s.circle"] += 1
    return out


def probe_units() -> None:
    """4A5: how many paintings wrote a pixel helper, or moved a group of shapes by hand."""
    heading("4A5: the corpus's own pixel helpers and hand-moved groups")
    rows = []
    for folder in sorted({e.folder for e in cohort.CORPUS}):
        found: dict[str, list] = {"pixel helpers": [], "scale helpers": [], "pixel divisions": 0,
                                  "shifted": 0, "scaled": 0, "aspect=": 0, "s.circle": 0}
        for path in sorted(folder.rglob("*.py")):
            try:
                got = unit_helpers(path.read_text(encoding="utf-8-sig"))
            except SyntaxError:
                continue
            for key, value in got.items():
                if isinstance(value, list):
                    found[key] += [f"{path.name}:{v}" for v in value]
                else:
                    found[key] += value
        rows.append([str(folder.relative_to(ROOT / "paintings")).replace(os.sep, "/")[:32],
                     ", ".join(found["pixel helpers"])[:40] or "-",
                     ", ".join(found["scale helpers"])[:40] or "-",
                     found["pixel divisions"], found["shifted"], found["scaled"],
                     found["aspect="], found["s.circle"]])
    print(table(rows, ["painting", "pixel helpers", "scale helpers", "x / 1024-style",
                       ".shifted", ".scaled", "aspect=", "s.circle"]))
    helpers = sum(1 for r in rows if r[1] != "-")
    scalers = sum(1 for r in rows if r[2] != "-")
    print(f"  {helpers} of {len(rows)} paintings wrote a pixel helper; {scalers} scaled or "
          f"moved points about a centre by hand")
    probe_shape_units()


def probe_shape_units() -> None:
    """F7: what a ribbon's width and a blob's radii are, in pixels, measured off the masks."""
    heading("F7: a ribbon's width and a round shape's radii, in pixels")
    regions = easel.regions
    rows = []
    for w, h in ((1024, 768), (768, 1024)):
        a = 150.0                       # half the diagonal ribbon's run, in pixels
        runs = {"across a level ribbon": (regions.ribbon([(0.2, 0.5), (0.8, 0.5)], 0.05), "col"),
                "across an upright ribbon": (regions.ribbon([(0.5, 0.2), (0.5, 0.8)], 0.05), "row"),
                "across one at 45 degrees in pixels": (regions.ribbon(
                    [(0.5 - a / w, 0.5 - a / h), (0.5 + a / w, 0.5 + a / h)], 0.05), "diag")}
        for label, (shape, how) in runs.items():
            mask = shape.mask(w, h)
            if how == "col":
                px = float(mask[:, w // 2].sum())
            elif how == "row":
                px = float(mask[h // 2].sum())
            else:
                px = float(mask.sum()) / (2.0 * a * math.sqrt(2.0))
            rows.append([f"{w}x{h}", f"ribbon(..., 0.05), {label}", f"{px:.0f} px"])
        for label, shape in (("ellipse(p, 0.05)", regions.ellipse((0.5, 0.5), 0.05)),
                             ("blob(p, 0.05)", regions.blob((0.5, 0.5), 0.05)),
                             ("ellipse(p, 0.05, aspect=s.aspect)",
                              regions.ellipse((0.5, 0.5), 0.05, aspect=w / h))):
            mask = shape.mask(w, h)
            rows.append([f"{w}x{h}", label,
                         f"{int(mask[h // 2].sum())} x {int(mask[:, w // 2].sum())} px"])
    print(table(rows, ["canvas", "shape", "measured"]))
    print("  a brush's size=0.05 is 51 px on either canvas: a fraction of the long side")


# -- main -------------------------------------------------------------------------------

BENCHES = (
    ("claims", "section 3 and 3b re-measured, and where marks stop landing"),
    ("guides", "4A1: the guide candidates over every ground"),
    ("thumbnail", "4A3: the painter's arrangements, flat, at four sizes"),
    ("terminator", "4B: row 9's candidates at two sizes, the recipe's numbers, the face"),
    ("cost", "4C: the dearest line over the corpus, and what landed nothing"),
    ("short", "4D: every hand-laid mark's shortfall, the guide blocks, the two versions"),
    ("key", "4E1: the values line over the corpus, and under a key"),
    ("place", "4E2: the plans pass by pass, and places given a detail"),
    ("floor", "4E3: the darks of the pictures on the floor, re-laid under it"),
    ("lamp", "4E4: the named light of every plan, pass by pass"),
    ("rebind", "4H2: names a pass binds that its prelude bound"),
    ("repaint", "4H4: masses laid over earlier marks, place by place"),
    ("rings", "4I2: an inward scumble's rings, ring count by ring count"),
    ("units", "4A5: the corpus's own pixel helpers and hand-moved groups"),
)
_NEEDS_REBUILD = {"claims", "guides", "terminator", "short", "repaint"}
_NEEDS_CORPUS = {"cost", "short", "key", "place", "lamp", "repaint"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    for flag, what in BENCHES:
        parser.add_argument(f"--{flag}", action="store_true", help=what)
    parser.add_argument("--corpus", action="store_true",
                        help="replay the corpus with this round's watcher and keep it in "
                             "out/bell/corpus.pkl")
    parser.add_argument("--fresh", action="store_true",
                        help="with a corpus bench: replay the corpus again rather than read "
                             "out/bell/corpus.pkl")
    args = parser.parse_args(argv)
    chosen = {k for k, v in vars(args).items() if v and k not in ("fresh", "corpus")}
    every = not chosen and not args.corpus
    run = {name for name, _ in BENCHES} if every else chosen
    print("The bell-warden's round, measured. Engine "
          f"{easel.__version__} from {Path(easel.__file__).parent}", flush=True)
    rb = wb = data = None
    if run & _NEEDS_REBUILD:
        rb = rebuild("bell")
        wb = rebuild("wenna")
    if run & _NEEDS_CORPUS or args.corpus:
        data = corpus(fresh=args.fresh or args.corpus)
        if args.corpus:
            print(f"  kept {len(data.calls)} calls and {len(data.passes)} passes in {CACHE}")
    if "claims" in run:
        probe_claims(rb, wb)
    if "guides" in run:
        probe_guides(rb, wb)
    if "thumbnail" in run:
        probe_thumbnail()
        probe_parts()
    if "terminator" in run:
        probe_terminator(rb, wb)
    if "cost" in run:
        probe_cost(data)
    if "short" in run:
        probe_short(data, rb)
    if "key" in run:
        probe_key(data)
    if "place" in run:
        probe_place(data)
    if "floor" in run:
        probe_floor()
    if "lamp" in run:
        probe_lamp(data)
    if "rebind" in run:
        probe_rebind()
    if "repaint" in run:
        probe_repaint(data, rb, wb)
    if "rings" in run:
        probe_rings()
    if "units" in run:
        probe_units()
    print("\nThe numbers above are the ones CALIBRATION.md quotes under *The bell-warden's "
          "round*;\nthe sheets under out/bell/ are what the painters' questions 4, 9 and 10 "
          "are put with.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
