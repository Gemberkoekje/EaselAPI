"""The measurements behind the lighthouse handover's round -- step 2 of ``PLAN-0.7.0.md``.

One painter, ``claude-opus-5-5``, painted a lighthouse at dusk against 0.6.0 from the
package, and checked its claims before making them. Its verdict is filed as an open round
in ``SUGGESTIONS.md``; the plan built on it proposes an edge that is not a step, a dry
brush that streaks, a narrowed rule, a quicker way to compare alternatives, a smaller
file, and three sentences. **Every one of those is a candidate until this script has
measured it** -- ``LESSONS.md``'s first rule, and the reason step 2 comes before every
engine change in the round.

It does four things:

1. **Rebuilds the painting** from its thirteen committed passes, through the CLI's own
   ``run_script``, the way ``easel run`` lays them -- and keeps a rehearsal copy of the
   canvas after each pass, so every bench below starts from the canvas the painter
   actually had rather than from a blank one. About forty seconds.
2. **Re-measures section 3's claims** on that rebuild: the edge steps, the clip mask's
   one fractional pixel, the ``edges:`` line pass by pass, the glaze's width, and which
   of the painting's calls a default feather would move.
3. **Benches the candidates** of workstreams A, B, C, D and F, each patched in for the
   length of one bench and never into the engine: the edge feathered inward (A1) or
   broken by the tooth (A2); the tooth gate read along the travel (B1), per bristle
   (B2), or thinned (B3); the narrowed graded rule on the four cases in hand; a
   ``vary=`` sheet in one process and in four; the session file saved each way; the
   pressure-list fade and the wet bands.
4. **Renders what the numbers cannot decide** into ``out/handover/``. The ``edges:``
   line and the one-pixel step are numbers, and A2 is built to keep the second high on
   purpose; **the eye is the verdict**, which the painter could not give because it has
   not seen them. The sheets are what the owner looks at for the plan's question 2.

    python scripts/probe_handover_session.py              # everything, about fifteen minutes
    python scripts/probe_handover_session.py --claims     # section 3, re-measured
    python scripts/probe_handover_session.py --edges      # 4A, with its sheets
    python scripts/probe_handover_session.py --flecks     # 4B, with its sheets
    python scripts/probe_handover_session.py --misfires   # 4C: the four cases, and the built gate
    python scripts/probe_handover_session.py --sheet      # 4D
    python scripts/probe_handover_session.py --file       # 4F
    python scripts/probe_handover_session.py --shell      # 4F built: the passes from a shell
    python scripts/probe_handover_session.py --shell --engine DIR/src   # ...under another
    python scripts/probe_handover_session.py --pressure   # 4G: the fade and the wet bands
    python scripts/probe_handover_session.py --corpus-edges   # 4A built, on the corpus
    python scripts/probe_handover_session.py --dry        # 4B built, beside 0.6.0's gate
    python scripts/probe_handover_session.py --corpus-dry # 4B built, on the corpus

The corpus half of workstream C -- every pass of the twenty-two paintings the graded rule
fires on, cropped, with each narrowed gate's verdict -- is
``python scripts/probe_cohort_session.py --graded``, because the corpus replay lives there
and the gate is written once, beside it.
"""

from __future__ import annotations

import argparse
import contextlib
import inspect
import io
import math
import multiprocessing
import sys
import tempfile
import time
import warnings
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_cohort_session as cohort  # noqa: E402

import easel  # noqa: E402
import easel.session as session_module  # noqa: E402
from easel import Region, Session, polygon  # noqa: E402
from easel.canvas import _GATE_BAND, _TOOTH_GRAIN_W, _TOOTH_HEIGHT_W  # noqa: E402
from easel.checklist import edges_line  # noqa: E402
from easel.cli import run_script  # noqa: E402
from easel.demo import demos, preamble  # noqa: E402
from easel.look import label_sheet, render_look  # noqa: E402

#: The modules themselves. ``import easel.brush as b`` gets the *function*, because
#: ``easel/__init__`` rebinds the name -- ``LESSONS.md``'s papercuts, met again here.
BRUSH_MODULE = sys.modules["easel.brush"]
CANVAS_MODULE = sys.modules["easel.canvas"]

HERE = ROOT / "paintings" / "Claude" / "lighthouse_handover"
MISFIRES = HERE / "misfires"
OUT = ROOT / "out" / "handover"
PASSES = tuple(sorted(p.name for p in HERE.glob("p[0-9][0-9]_*.py")))
#: The canvas `PAINTINGS.md` records for the painting, which `easel new` was given.
PAINTING = {"texture": "linen", "ground": "burnt_sienna", "seed": 11, "budget": 300}
#: The tooth gate's own band in `Canvas.stamp`, which B reuses rather than restates --
#: and A2 with it, since step 5 built A2 on the same constant (`Canvas.broken_edge`).
GATE_BAND = _GATE_BAND


# -- the painting, rebuilt ------------------------------------------------------------

@dataclass
class Rebuilt:
    """The painting rebuilt, with a copy of the canvas kept after each pass."""

    session: Session
    after: dict[str, Session] = field(default_factory=dict)
    said: dict[str, list[str]] = field(default_factory=dict)
    calls: list[dict] = field(default_factory=list)
    seconds: float = 0.0


#: The verbs whose calls the inventory reads, for the ones that clip or lay hard.
_INVENTORIED = ("stroke", "glaze", "dab", "block_in", "scumble", "cover", "sweep")


@contextlib.contextmanager
def _watching(calls: list[dict], current: list[str]):
    """Record every outermost call of a painting verb, with its arguments bound.

    The log carries the outline a clipped stroke was held to but not the ``edge=`` its
    call was given, so which of the painting's calls a default feather would move can
    only be read off the calls as they are made -- which is also how the painter
    counted them.
    """
    saved = {name: getattr(Session, name) for name in _INVENTORIED}
    depth = [0]

    def wrap(name, original):
        signature = inspect.signature(original)

        def wrapper(session, *args, **kw):
            if depth[0]:
                return original(session, *args, **kw)
            depth[0] += 1
            try:
                try:
                    bound = signature.bind(session, *args, **kw)
                    bound.apply_defaults()
                    named = dict(bound.arguments)
                    named.pop("self", None)
                    named.update(named.pop("brush_overrides", {}) or {})
                    named.update(named.pop("kw", {}) or {})
                except TypeError:
                    named = dict(kw)
                calls.append({"pass": current[0], "verb": name, "args": named})
                return original(session, *args, **kw)
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


def rebuild(width: int = 1024, height: int = 768, timelapse: bool = False,
            upto: str | None = None, prelude: Path | None = None,
            keep: bool = True, watch: bool = False, cut: bool = True) -> Rebuilt:
    """The painting from its committed passes, through the CLI's own ``run_script``.

    ``cut`` lays the painting as 0.6.0 laid it -- every hold cut on the line, every
    starving brush gated a pixel at a time -- the painting the painter had, which every
    claim and bench here starts from. Since step 5 the engine breaks every hold it is
    not told otherwise about, and since step 6 a starving brush drags; ``cut=False`` is
    the painting as this engine lays the same scripts.

    Each pass opens as ``easel run`` opens one, runs in a fresh scope with the prelude
    executed in front of it, and is then read by ``report()`` over the pass alone --
    so ``said`` is what the painter's shell printed after it. ``upto`` stops after the
    named pass; ``prelude`` swaps the painting's prelude for another, which is how the
    two misfires are rebuilt on the prelude of their own moment.

    With ``keep``, a rehearsal copy is taken after every pass (:meth:`Session.scratch`),
    which is seeded as the next marks of the painting: what a bench lays on it is what
    the painter would have laid there.
    """
    source = (prelude or HERE / "prelude.py").read_text(encoding="utf-8")
    started = time.time()
    with tempfile.TemporaryDirectory(prefix="easel-handover-") as tmp:
        session = Session(width, height, timelapse=timelapse, out_dir=Path(tmp), **PAINTING)
        out = Rebuilt(session=session)
        current = [""]
        watcher = _watching(out.calls, current) if watch else contextlib.nullcontext()
        edges = feather("today", 0.0) if cut else contextlib.nullcontext()
        dry = gate("today") if cut else contextlib.nullcontext()
        with watcher, edges, dry, warnings.catch_warnings(), \
                contextlib.redirect_stdout(io.StringIO()):
            warnings.simplefilter("ignore")
            for name in PASSES:
                current[0] = name
                start = session._open_pass()
                path = HERE / name
                result = run_script(session, path.read_text(encoding="utf-8"), str(path),
                                    prelude=source, prelude_name="prelude.py")
                if result.code:
                    raise RuntimeError(f"{name} failed to rebuild: {result.report} "
                                       f"{result.trace}")
                out.said[name] = session.report(since=start).splitlines()
                if keep:
                    out.after[name] = session.scratch()
                if name == upto:
                    break
    out.seconds = time.time() - started
    return out


def scope_of(session: Session, prelude: Path | None = None, extra: str = "") -> dict:
    """The prelude's names -- the palette, the shapes, the helpers -- bound to ``session``.

    What a pass script sees when ``easel run`` runs it. ``extra`` is source run after
    the prelude in the same scope, which is how a bench swaps one of its shapes.
    """
    scope = {name: getattr(easel, name) for name in easel.__all__}
    scope.update({"s": session, "session": session, "palette": session.palette,
                  "__name__": "__easel_script__"})
    with warnings.catch_warnings(), contextlib.redirect_stdout(io.StringIO()):
        warnings.simplefilter("ignore")
        exec(compile((prelude or HERE / "prelude.py").read_text(encoding="utf-8")  # noqa: S102
                     + "\n" + extra, "prelude.py", "exec"), scope)
    return scope


def lay_pass(session: Session, name: str, prelude: Path | None = None,
             extra: str = "", folder: Path = HERE) -> list[str]:
    """One pass script laid on ``session``, as ``easel run`` lays it; what the check said."""
    source = (prelude or HERE / "prelude.py").read_text(encoding="utf-8") + "\n" + extra
    start = session._open_pass()
    path = folder / name
    with warnings.catch_warnings(), contextlib.redirect_stdout(io.StringIO()):
        warnings.simplefilter("ignore")
        result = run_script(session, path.read_text(encoding="utf-8"), str(path),
                            prelude=source, prelude_name="prelude.py")
    if result.code:
        raise RuntimeError(f"{name} failed: {result.report} {result.trace}")
    return session.report(since=start).splitlines()


# -- small instruments ------------------------------------------------------------------

def values(session: Session) -> np.ndarray:
    """The canvas as the check reads it: values, ``0..1``, graphite left out."""
    return session.canvas.values(sketch=False).astype(np.float32) / 255.0


def painters_lum(rgb8: np.ndarray) -> np.ndarray:
    """The painter's own measure in ``verify.py``: Rec. 709 weights on the sRGB bytes."""
    a = rgb8.astype(np.float64) / 255.0
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def smooth(t) -> np.ndarray:
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def crop(session: Session, box: tuple[float, float, float, float], zoom: int = 1,
         impasto: bool = True) -> Image.Image:
    """A part of the canvas as the painter's export shows it, ``box`` in canvas units."""
    x0, y0, x1, y1 = box
    w, h = session.canvas.width, session.canvas.height
    rgb = session.canvas.to_srgb8(impasto=impasto, sketch=False)
    image = Image.fromarray(rgb[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)])
    if zoom > 1:
        image = image.resize((image.width * zoom, image.height * zoom), Image.LANCZOS)
    return image


def save_sheet(panels: list[tuple[str, Image.Image]], name: str,
               columns: int | None = None) -> Path:
    """Panels side by side, each labelled, into ``out/handover/``."""
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    label_sheet(panels, columns=columns or len(panels)).save(path)
    return path


def one_pixel_steps(view: np.ndarray, shape, rows) -> list[float]:
    """The largest one-pixel value step within five pixels of a shape's left and right side.

    Row by row, over the rows given in canvas units. What the painter measured at the
    tower -- *0.59 to 0.28 in one pixel* -- as a number per side per row.
    """
    height, width = view.shape
    mask = shape.mask(width, height)
    out = []
    for fy in rows:
        y = int(fy * height)
        xs = np.nonzero(mask[y])[0]
        if not len(xs):
            continue
        for x in (int(xs.min()), int(xs.max()) + 1):
            seg = view[y, max(x - 5, 0):x + 6]
            out.append(float(np.abs(np.diff(seg)).max()))
    return out


def top_edge_steps(view: np.ndarray, shape, columns) -> list[float]:
    """The largest one-pixel step within five pixels of a shape's top, column by column.

    The headland's edge against the sky runs across the canvas rather than up it, so it
    is read down each column, where :func:`one_pixel_steps` reads along each row.
    """
    height, width = view.shape
    mask = shape.mask(width, height)
    out = []
    for fx in columns:
        x = int(fx * width)
        ys = np.nonzero(mask[:, x])[0]
        if not len(ys):
            continue
        y = int(ys.min())
        out.append(float(np.abs(np.diff(view[max(y - 5, 0):y + 6, x])).max()))
    return out


def label_components(mask: np.ndarray) -> np.ndarray:
    """Eight-connected components, by min-label propagation with pointer jumping.

    The repository takes numpy and pillow and nothing else, and a flood fill in Python
    is minutes over a canvas of flecks; this is a few dozen array passes.
    """
    h, w = mask.shape
    labels = np.where(mask, np.arange(1, h * w + 1).reshape(h, w), 0).astype(np.int64)
    big = h * w + 10
    while True:
        cur = np.where(mask, labels, big)
        pad = np.pad(cur, 1, constant_values=big)
        low = cur.copy()
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                np.minimum(low, pad[1 + dy:1 + dy + h, 1 + dx:1 + dx + w], out=low)
        low = np.where(mask, low, 0)
        flat = low.ravel()
        live = flat > 0
        jumped = flat.copy()
        jumped[live] = np.minimum(flat[live], flat[flat[live] - 1])
        low = jumped.reshape(h, w)
        if np.array_equal(low, labels):
            return labels
        labels = low


@dataclass
class Flecks:
    """What one starved mark left, as pieces of paint."""

    landed: int         # pixels moved one 8-bit level or more
    pieces: int         # eight-connected pieces of them
    median: float       # the median piece, in pixels
    small: float        # the share of pieces under four pixels
    specks: float       # the share of the paint that is in pieces under four pixels
    elongation: float   # median length along the travel over width across, pieces of 4+
    streak: float       # the same, for the piece the median pixel of paint is in
    reads: int          # pixels moved 0.02 or more: the paint a viewer finds
    contrast: float     # the median move of a pixel that landed

    def row(self) -> str:
        return (f"{self.landed:>7}{self.pieces:>7}{self.median:>6.0f}{self.small:>7.0%}"
                f"{self.specks:>7.0%}{self.elongation:>6.1f}{self.streak:>7.1f}{self.reads:>7}"
                f"{self.contrast:>8.3f}")


FLECK_HEAD = f"{'landed':>7}{'pieces':>7}{'med':>6}{'<4px':>7}{'specks':>7}{'long':>6}{'paint':>7}" \
             f"{'reads':>7}{'contrast':>8}"


def flecks(moved: np.ndarray, angle: float) -> Flecks:
    """Pieces of paint in ``moved`` (the value change a mark made), read along ``angle``.

    *Landed* is one 8-bit level: the least a viewer's screen can show. *Specks* is the
    confetti the verdict calls dirt, as a share of the paint rather than of the pieces,
    because a hundred single pixels are a small share of a streak's worth of paint and
    a large share of what the eye picks out. *Long* is each piece's extent along the
    travel over its extent across it: one for a dot, two or more for a streak -- the
    median over the pieces, which the many small ones dominate, and again (*paint*)
    for the piece the median pixel of paint sits in, which is what a streak made of
    few long pieces among many flecks shows up in.
    """
    landed = moved >= 1.0 / 255.0
    if not landed.any():
        return Flecks(0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0)
    labels = label_components(landed)
    ids, inverse, counts = np.unique(labels[landed], return_inverse=True, return_counts=True)
    ys, xs = np.nonzero(landed)
    c, s = math.cos(angle), math.sin(angle)
    along_px, across_px = xs * c + ys * s, -xs * s + ys * c

    def extent(a: np.ndarray) -> np.ndarray:
        low = np.full(len(ids), np.inf)
        high = np.full(len(ids), -np.inf)
        np.minimum.at(low, inverse, a)
        np.maximum.at(high, inverse, a)
        return high - low + 1.0

    along, across = extent(along_px), extent(across_px)
    small = counts < 4
    big = ~small
    ratio = along / across
    order = np.argsort(ratio)
    weight = np.cumsum(counts[order])
    streak = float(ratio[order][np.searchsorted(weight, weight[-1] / 2.0)])
    return Flecks(
        landed=int(landed.sum()), pieces=len(ids), median=float(np.median(counts)),
        small=float(small.mean()), specks=float(counts[small].sum() / counts.sum()),
        elongation=float(np.median(ratio[big])) if big.any() else 0.0, streak=streak,
        reads=int((moved >= 0.02).sum()), contrast=float(np.median(moved[landed])),
    )


def _time(fn) -> tuple[float, object]:
    started = time.perf_counter()
    result = fn()
    return time.perf_counter() - started, result


# -- 3. the claims, re-measured -----------------------------------------------------------

def _window(line: np.ndarray, at: int, reach: int = 4) -> tuple[str, float]:
    seg = line[max(at - reach, 0):at + reach + 1]
    return " ".join(f"{v:.2f}" for v in seg), float(np.abs(np.diff(seg)).max())


def probe_claims(rb: Rebuilt) -> None:
    """Section 3, re-measured on the rebuild rather than taken from the plan."""
    print("\n== 3. the verdict's measured claims, re-measured on the rebuild ==")
    session = rb.session
    width, height = session.canvas.width, session.canvas.height
    names = scope_of(session.scratch())
    lum = painters_lum(session.canvas.to_srgb8())
    print(f"  rebuilt: {len(session.history.records)} records, {session.stroke_count} "
          f"strokes spent, in {rb.seconds:.0f}s")

    print("\n  1. the hard edge, in the painter's own measure (Rec. 709 on the export)")
    tower = names["tower"]
    y = int(0.40 * height)
    inside = np.nonzero(tower.mask(width, height)[y])[0]
    for label, x in (("tower, left side, y=0.40", int(inside.min())),
                     ("tower, right side, y=0.40", int(inside.max()) + 1)):
        seg, step = _window(lum[y], x)
        print(f"     {label:<30} {seg}   largest one-pixel step {step:.2f}")
    y = int(0.70 * height)
    row = lum[y, int(0.50 * width):int(0.70 * width)]
    x = int(np.argmax(np.abs(np.diff(row)))) + int(0.50 * width)
    seg, step = _window(lum[y], x)
    print(f"     {'the waterline, y=0.70':<30} {seg}   largest one-pixel step {step:.2f}")
    col = lum[int(0.50 * height):int(0.58 * height), int(0.60 * width)]
    yy = int(np.argmax(np.abs(np.diff(col)))) + int(0.50 * height)
    seg, step = _window(lum[:, int(0.60 * width)], yy)
    print(f"     {'headland against sky, x=0.60':<30} {seg}   largest one-pixel step {step:.2f}")
    cover = tower.coverage(width, height)
    middle = int(0.70 * width)
    rows = range(int(0.22 * height), int(0.53 * height))
    per_side = [(int(((cover[y, :middle] > 0) & (cover[y, :middle] < 1)).sum()),
                 int(((cover[y, middle:] > 0) & (cover[y, middle:] < 1)).sum())) for y in rows]
    counts = np.asarray(per_side)
    print(f"     the clip mask (Polygon.coverage, two samples a pixel), over the tower's "
          f"{len(counts)} rows: at most {int(counts.max())} fractional pixel a side, "
          f"{counts.mean(axis=0)[0]:.2f} on the left and {counts.mean(axis=0)[1]:.2f} on "
          f"the right on average -- the rest is a step")

    print("\n  the edges: line after every pass, as the painter's shell printed it")
    for name, lines in rb.said.items():
        edge = next((line.strip() for line in lines if line.strip().startswith("edges:")),
                    "(no edges line)")
        print(f"     {name:<18} {edge}")

    print("\n  the painting's clipped and hard-edged calls, and what a default feather moves")
    probe_inventory(rb)

    print("\n  11. a round tip's glaze at pressure [1.0 ... 0.1]: which end is wide")
    s = Session(1024, 768, ground="toned_grey", seed=3, timelapse=False)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.canvas.rgb[...] = s.palette.mix("ultramarine", "burnt_umber", 0.5)
        before = painters_lum(s.canvas.to_srgb8(sketch=False))
        s.glaze([(0.10, 0.5), (0.50, 0.5), (0.90, 0.5)], "titanium_white", opacity=0.3,
                size=0.10, pressure=[1.0, 0.55, 0.1])
    moved = np.abs(painters_lum(s.canvas.to_srgb8(sketch=False)) - before)
    for fx, where in ((0.2, "near the source"), (0.5, "the middle"), (0.8, "the far end")):
        column = moved[:, int(fx * 1024)]
        print(f"     x={fx} ({where}): painted {int((column > 0.01).sum())} px tall, "
              f"peak change {float(column.max()):.3f}")
    print("     read: full pressure is the wide end of a round tip; the recipe's sentence "
          "has it the other way round.")


def probe_inventory(rb: Rebuilt) -> None:
    """Which of the painting's calls clip or lay hard, and which of them draw an edge.

    The painter counted 33 and sorted them itself: nine draw an edge -- the headland,
    two sea stacks, the cap, the horizon, and the tower, its lit side and the lantern
    twice -- and the rest only keep paint inside a shape. The nine are told apart here
    by what the painter named: every ``edge="hard"`` call, and the clipped strokes whose
    colour is the shape's own body.
    """
    body = {"tower", "tower_lit", "lantern", "lantern2"}
    rows = []
    for call in rb.calls:
        args = call["args"]
        hard = args.get("edge") == "hard"
        clip = args.get("clip") is not None
        if not (hard or clip):
            continue
        colour = args.get("color", args.get("color_a", ""))
        colour = colour if isinstance(colour, str) else "(mixed)"
        draws = hard or colour in body
        moves = hard and call["verb"] in ("block_in", "cover", "scumble")
        rows.append((call["pass"], call["verb"], "hard" if hard else "clip", colour,
                     draws, moves))
    drawn = [r for r in rows if r[4]]
    print(f"     {len(rows)} calls clip or lay hard; {len(drawn)} of them draw an edge "
          f"by the painter's own list, {len(rows) - len(drawn)} only keep paint inside")
    for pass_name, verb, how, colour, _, moves in drawn:
        print(f"       {pass_name:<17} {verb:<9} {how:<5} {colour:<10} "
              f"{'feathers under the decided default' if moves else 'stays hard: a clip'}")
    moved = sum(1 for r in rows if r[5])
    moved_drawn = sum(1 for r in drawn if r[5])
    print(f"     under the decided default (edge=\"hard\" feathers, clip= stays hard): "
          f"{moved} calls move, {moved_drawn} of the {len(drawn)} that draw an edge -- "
          f"and the clipped strokes the verdict named, the tower and the lantern, "
          f"are not among them")


# -- 4A. an edge that is not a step ---------------------------------------------------------

#: The feathers benched, as fractions of the long side like `size`: 0.002 is 2 px on a
#: 1024 canvas and about 3 on a 1440 one.
FEATHERS = (0.0, 0.001, 0.002, 0.003, 0.005)

#: What the sheets show: today, and each candidate at the knee.
SHOWN = (("today", 0.0), ("A1", 0.002), ("A2", 0.002), ("A2", 0.003))


def inside_depth(poly, width: int, height: int, reach: float):
    """How far inside ``poly`` each pixel's centre sits, in pixels; negative outside.

    Exact to the outline rather than to the coverage mask: the distance from every
    pixel centre within ``reach`` of the line to the nearest segment of it, signed by
    the shape's own even-odd test. Pixels further in are ``+inf``, further out ``-inf``.
    """
    pts = np.asarray(poly.points, dtype=np.float64) * [width, height]
    ends = np.roll(pts, -1, axis=0)
    inside = poly.mask(width, height)
    k = int(math.ceil(reach)) + 2
    image = Image.fromarray(inside.astype(np.float32), mode="F")
    low = np.asarray(image.filter(ImageFilter.MinFilter(2 * k + 1)))
    high = np.asarray(image.filter(ImageFilter.MaxFilter(2 * k + 1)))
    rows, cols = np.nonzero(low != high)
    px, py = cols + 0.5, rows + 0.5
    nearest = np.full(px.shape, np.inf)
    for start in range(0, len(pts), 64):
        a, b = pts[start:start + 64], ends[start:start + 64]
        d = b - a
        length2 = np.maximum((d ** 2).sum(axis=1), 1e-12)
        t = np.clip(((px[:, None] - a[None, :, 0]) * d[None, :, 0]
                     + (py[:, None] - a[None, :, 1]) * d[None, :, 1]) / length2[None, :],
                    0.0, 1.0)
        dist = np.hypot(px[:, None] - (a[None, :, 0] + t * d[None, :, 0]),
                        py[:, None] - (a[None, :, 1] + t * d[None, :, 1])).min(axis=1)
        nearest = np.minimum(nearest, dist)
    depth = np.where(inside, np.inf, -np.inf)
    depth[rows, cols] = np.where(inside[rows, cols], nearest, -nearest)
    return depth


def feathered(poly, canvas, px: float, kind: str) -> np.ndarray:
    """A clip mask ramped **inward** over ``px`` pixels: nothing lands outside the line.

    *A1* is the ramp itself, from nothing at the drawn line to full paint at the
    feather's depth -- the probe's own, as step 2 benched it. *A2* is the same ramp
    read against the canvas tooth, the way ``Canvas.stamp`` reads a starving brush:
    near the line only the peaks of the weave take paint, and deeper in the valleys do
    too -- so the boundary breaks at the weave's scale and stays crisp where the tooth
    is high. **Since step 5, A2 is the engine's own** (``Polygon._edge_depth`` and
    ``Canvas.broken_edge``, which ``Session._clip_cover`` lays), so what this measures
    is what shipped; it differs from step 2's copy in two places, both built on
    purpose: a side on the canvas frame is not an edge, and nothing lands past the
    line even on the peaks. Both are clamped under today's coverage.
    """
    width, height = canvas.width, canvas.height
    cover = poly.coverage(width, height)
    if kind == "A1":
        ramp = np.clip(inside_depth(poly, width, height, px) / px, 0.0, 1.0)
        return np.minimum(cover, smooth(ramp)).astype(np.float32)
    rows, cols, depth, full = poly._edge_depth(width, height, px, cover)
    if len(rows):
        cover[rows, cols] = np.minimum(cover[rows, cols],
                                       canvas.broken_edge(rows, cols, depth, full))
    return cover


@contextlib.contextmanager
def feather(kind: str, amount: float, which: str = "all"):
    """``Session._clip_cover`` held to one candidate for the length of a bench.

    ``which`` is whose outline feathers: ``"all"`` of them; ``"hard"``, only the outline
    a mass holds itself to under ``edge="hard"`` -- the default step 2 first read the
    painter's answer as, which leaves every ``clip=`` as it is; or ``"clip"``, only the
    ``clip=`` outlines, which is the containment bench. A mass's own outline is told
    apart by catching it as ``_mass_hold`` builds it, since the mask is asked with the
    outlines alone.

    **Every candidate patches, "today" included**, because since step 5 the engine's
    own default breaks every hold at ``0.002``: left alone, a bench of *today* would
    have measured the new default under the old name. The feather each call resolves
    is ignored here, so the benches mean what they meant in step 2.
    """
    if kind == "today":
        amount = 0.0
    own: list = []
    memo: dict = {}
    original_cover = Session._clip_cover
    original_hold = session_module._mass_hold

    def mass_hold(place, edge, clip):
        holds = original_hold(place, edge, clip)
        if holds and edge == "hard":
            own.append(holds[0])
        return holds

    def clip_cover(self, holds, feather=0.0):
        canvas = self.canvas
        px = amount * canvas.long_side
        out = None
        for poly in holds:
            mine = any(poly is one for one in own)
            soft = px > 0.0 and (which == "all" or (which == "hard" and mine)
                                 or (which == "clip" and not mine))
            key = (poly.points, canvas.width, canvas.height, soft)
            if key not in memo:
                if len(memo) > 8:
                    memo.clear()
                memo[key] = (feathered(poly, canvas, px, kind) if soft
                             else poly.coverage(canvas.width, canvas.height))
            out = memo[key] if out is None else out * memo[key]
        return out

    Session._clip_cover = clip_cover
    session_module._mass_hold = mass_hold
    try:
        yield
    finally:
        Session._clip_cover = original_cover
        session_module._mass_hold = original_hold


def _flat_field(width: int, height: int, value: float) -> Session:
    """A canvas set to one colour rather than painted, so the only edges on it are laid."""
    s = Session(width, height, timelapse=False, **PAINTING)
    s.palette["field"] = s.palette.at_value(s.palette.mix("cerulean", "titanium_white", 0.7),
                                            value)
    s.canvas.rgb[...] = s.palette["field"]
    return s


def _tower_strokes(s: Session, names: dict) -> None:
    """``p04_tower.py``'s first two strokes: the tower and its lit side, each clipped."""
    tx = names["TX"]
    flat = {"opacity": 1.0, "load": 1.0, "load_falloff": 0.0, "pressure": "even",
            "jitter": 0.0, "size_jitter": 0.0}
    s.stroke([(tx, 0.548), (tx, 0.203)], "flat", "tower", size=0.043,
             clip=names["tower"], **flat)
    s.stroke([(tx - 0.0115, 0.548), (tx - 0.0078, 0.205)], "flat", "tower_lit", size=0.016,
             clip=names["tower_lit_side"], **flat)


def bench_edge_curve() -> None:
    """The plan's table, rebuilt inward: the tower's two strokes on a flat field.

    The table in ``PLAN-0.7.0.md`` was a *centred* Gaussian, which reaches outward and
    is the one thing the build must not do. Each row here is the ramp inward only, at
    each feather, on a field at the sky's value beside the tower. The step is the
    largest one-pixel move either side of the tower, median over its rows; the
    ``edges:`` line is the engine's own, and on a flat field it reads nothing but the
    tower.
    """
    print("\n  the curve: the tower's two strokes on a flat field at the sky's value (0.59)")
    print(f"     {'size':<10}{'candidate':<11}{'feather':>8}{'px':>6}{'step':>7}{'max':>7}"
          f"{'under 2.5 px':>14}{'median rise':>13}{'time':>7}")
    for width, height in ((1024, 768), (1440, 960)):
        base = _flat_field(width, height, 0.59)
        names = scope_of(base)
        for kind in ("A1", "A2"):
            for amount in FEATHERS:
                if kind == "A2" and amount == 0.0:
                    continue
                s = base.scratch()
                with warnings.catch_warnings(), feather(kind, amount, "all"):
                    warnings.simplefilter("ignore")
                    took, _ = _time(lambda s=s, names=names: _tower_strokes(s, names))
                view = values(s)
                steps = one_pixel_steps(view, names["tower"], np.linspace(0.25, 0.52, 14))
                line = edges_line(view)
                share, rise = _edges_numbers(line)
                label = "today" if amount == 0.0 else kind
                print(f"     {width}x{height:<5}{label:<11}{amount:>8.3f}"
                      f"{amount * max(width, height):>6.1f}{np.median(steps):>7.3f}"
                      f"{max(steps):>7.3f}{share:>14}{rise:>13}{took:>6.2f}s")


def _edges_numbers(line: str) -> tuple[str, str]:
    """The share and the median rise out of an ``edges:`` line."""
    parts = line.replace(",", "").split()
    share = next((p for p in parts if p.endswith("%")), "-")
    rise = parts[-2] + " px" if parts[-1] == "px" else "-"
    return share, rise


def bench_edge_sheets(rb: Rebuilt, rb1440: Rebuilt | None) -> None:
    """The candidates in the painting, where the eye can judge them.

    Five places, each a sheet under ``out/handover/``: the tower as ``p04_tower.py``
    laid it (and again at 1440x960); the headland as ``p03_headland.py`` laid it, with
    the prelude's wandering outline and with the plain one the painter drew first; the
    planes held inside the headland by ``clip=``, which is the rim the plan's risk
    table names; a hard mass on bare ground, read by the ``ground:`` line; and a burial,
    ``cover()``'s patch over a worked passage.
    """
    print("\n  the painting: each candidate laid by the committed pass on the canvas the "
          "painter had")
    view_rows = np.linspace(0.25, 0.52, 14)
    for label, source, size_rb in (("1024x768", "p03_headland.py", rb),
                                   ("1440x960", "p03_headland.py", rb1440)):
        if size_rb is None:
            continue
        panels, zoomed = [], []
        for which in ("all", "hard"):
            for kind, amount in SHOWN:
                if which == "hard" and kind == "today":
                    continue
                s = size_rb.after[source].scratch()
                with feather(kind, amount, which):
                    lay_pass(s, "p04_tower.py")
                names = scope_of(s.scratch())
                steps = one_pixel_steps(values(s), names["tower"], view_rows)
                tag = "today" if kind == "today" else (
                    f"{kind} {amount}" + ("" if which == "all" else ", default only"))
                print(f"     tower, {label}: {tag:<26} step {np.median(steps):.3f}   "
                      f"{edges_line(values(s))}")
                panels.append((tag, crop(s, (0.64, 0.12, 0.76, 0.60))))
                zoomed.append((tag, crop(s, (0.665, 0.30, 0.735, 0.42), zoom=3)))
        print(f"       -> {save_sheet(panels, f'edges_tower_{label}.png').relative_to(ROOT)}")
        print(f"       -> {save_sheet(zoomed, f'edges_tower_{label}_x3.png').relative_to(ROOT)}")

    plain = ("headland = polygon(TOP[:-1] + [(1.06, 0.506), (1.06, 1.06)] + WATER[:-1], "
             "name='headland')\n")
    panels = []
    for outline, extra in (("roughened", ""), ("plain", plain)):
        for kind, amount in SHOWN:
            s = rb.after["p02_sea.py"].scratch()
            with feather(kind, amount, "hard"):
                lay_pass(s, "p03_headland.py", extra=extra)
            tag = f"{outline}, {'today' if kind == 'today' else f'{kind} {amount}'}"
            top = top_edge_steps(values(s), scope_of(s.scratch(), extra=extra)["headland"],
                                 np.linspace(0.45, 0.95, 40))
            print(f"     the headland, {tag:<22} step along its top {np.median(top):.3f}   "
                  f"{edges_line(values(s))}")
            panels.append((tag, crop(s, (0.36, 0.46, 0.80, 0.72))))
    print(f"     the headland, its own outline feathered (the decided default), "
          f"roughened and plain\n       -> "
          f"{save_sheet(panels, 'edges_headland.png', columns=4).relative_to(ROOT)}")

    panels, zoomed = [], []
    for kind, amount in SHOWN:
        s = rb.after["p02_sea.py"].scratch()
        with feather(kind, amount, "clip"):
            lay_pass(s, "p03_headland.py")
        tag = "today" if kind == "today" else f"{kind} {amount}, clip= feathered"
        print(f"     containment, {tag:<28} {edges_line(values(s))}")
        panels.append((tag, crop(s, (0.40, 0.50, 0.72, 0.70), zoom=2)))
        zoomed.append((tag, crop(s, (0.43, 0.59, 0.53, 0.67), zoom=4)))
    print(f"     containment: the planes held inside the headland, their clip feathered\n"
          f"       -> {save_sheet(panels, 'edges_containment.png', columns=2).relative_to(ROOT)}"
          f"\n       -> {save_sheet(zoomed, 'edges_containment_x4.png', columns=4).relative_to(ROOT)}")

    bench_edge_ground()
    bench_edge_burial()


def bench_edge_ground() -> None:
    """A hard mass laid on bare ground: what an inward feather leaves showing round it.

    The plan's risk: the feather's zone is where the mass lands thinner, so whatever
    is under it shows through -- here, the ground, which the ``ground:`` line counts.
    """
    print("     a hard mass on bare ground: what the feather leaves showing")
    rock = polygon([(0.30, 0.70), (0.36, 0.52), (0.46, 0.44), (0.58, 0.47), (0.66, 0.58),
                    (0.70, 0.72)], name="rock")
    panels = []
    for kind, amount in SHOWN:
        s = Session(1024, 768, timelapse=False, **PAINTING)
        s.palette["rock"] = s.palette.at_value(s.palette.mix("ultramarine", "burnt_umber",
                                                             0.5), 0.18)
        with warnings.catch_warnings(), feather(kind, amount, "hard"):
            warnings.simplefilter("ignore")
            s.block_in(rock, "flat", "rock", size=0.05, density=1.0, solid=True,
                       edge="hard", direction=15)
        bare = rock.mask(1024, 768) & cohort._bare(s)
        tag = "today" if kind == "today" else f"{kind} {amount}"
        print(f"       {tag:<12} {s._ground_line()};  {int(bare.sum())} px of the rock's "
              f"own area took no paint")
        panels.append((tag, crop(s, (0.28, 0.42, 0.50, 0.62), zoom=2)))
    print(f"       -> {save_sheet(panels, 'edges_ground.png', columns=4).relative_to(ROOT)}")


def _region_steps(view: np.ndarray, place: Region, reach: int = 4) -> float:
    """The largest one-pixel step across a rectangle's four sides, median along them.

    ``_outline_step`` compares a sample inside with one outside, which is the patch's
    contrast and is the same whatever happens between the two; this is how the
    boundary is crossed.
    """
    height, width = view.shape
    x0, x1 = int(place.x0 * width), int(place.x1 * width)
    y0, y1 = int(place.y0 * height), int(place.y1 * height)
    steps = []
    for x in range(x0 + reach, x1 - reach):
        for y in (y0, y1):
            steps.append(float(np.abs(np.diff(view[y - reach:y + reach + 1, x])).max()))
    for y in range(y0 + reach, y1 - reach):
        for x in (x0, x1):
            steps.append(float(np.abs(np.diff(view[y, x - reach:x + reach + 1])).max()))
    return float(np.median(steps))


def bench_edge_burial() -> None:
    """``cover()``'s patch over a worked passage: F1's bench from 0.6.0, feathered.

    A burial laid hard draws its place's rectangle in the passage, which is what made
    0.6.0 hold it to its place at all; a feather inward softens the rectangle and lets
    the passage show through its edge zone. *Outline* against *own* is the rectangle
    as a number, as ``probe_cohort_session.probe_f1_burial`` printed it.
    """
    print("     a burial: cover() over a worked passage, 108x60 px on 900x600")
    base = cohort._f1_passage("worked")
    clean = values(base)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        base.palette["passage"] = base.sample(cohort.F1_PLACE)
        base.palette["mistake"] = base.palette.at_value("titanium_white", 0.92)
        base.stroke([(0.465, 0.458), (0.535, 0.482)], "round_hard", "mistake", size=0.018,
                    opacity=1.0, pressure="even")
        base.dry()
    marred = values(base)
    mistake = np.abs(marred - clean) >= 0.10
    asked = cohort._mask(cohort.F1_PLACE, 900, 600)
    own = cohort._outline_step(clean, cohort.F1_PLACE, 900, 600)
    panels = []
    for kind, amount in SHOWN:
        s = base.scratch()
        with warnings.catch_warnings(), feather(kind, amount, "hard"):
            warnings.simplefilter("ignore")
            s.cover(cohort.F1_PLACE, "passage")
        view = values(s)
        seen = np.abs(view - clean) >= cohort.SEEN
        showing = (np.abs(view - marred) < np.abs(view - clean)) & mistake
        tag = "today" if kind == "today" else f"{kind} {amount}"
        print(f"       {tag:<12} seen {seen.sum() / asked.sum():.2f}x the place, "
              f"showing {showing.sum() / max(mistake.sum(), 1):.1%} of the mistake, "
              f"outline {cohort._outline_step(view, cohort.F1_PLACE, 900, 600):.4f} "
              f"against the passage's own {own:.4f}, largest one-pixel step across it "
              f"{_region_steps(view, cohort.F1_PLACE):.3f}")
        panels.append((tag, crop(s, (0.40, 0.37, 0.60, 0.57), zoom=3)))
    print(f"       -> {save_sheet(panels, 'edges_burial.png', columns=4).relative_to(ROOT)}")


def _look_px(image: Image.Image) -> Image.Image:
    """The image as a look at the default size shows it: a long side of 1024."""
    f = 1024 / max(image.size)
    return image if f >= 1.0 else image.resize((round(image.width * f),
                                                round(image.height * f)), Image.LANCZOS)


def ground_edge_numbers(s: Session, box=(0.28, 0.42, 0.50, 0.62)) -> tuple[float, float]:
    """The painter's ``measure_ground_edges.py``, read off the canvas at its own pixels.

    The steep left side of the rock on bare ground, row by row: where each row first
    crosses half way from the ground to the rock, the wander of that line about a
    straight one (sd), and its largest departure -- the biggest bite. In canvas pixels;
    the painter measured the same on a sheet enlarged twice and halved it.
    """
    w, h = s.canvas.width, s.canvas.height
    x0, y0, x1, y1 = box
    lum = painters_lum(s.canvas.to_srgb8(impasto=True, sketch=False)
                       [int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)])
    lo, hi = np.percentile(lum, 5), np.percentile(lum, 95)
    level = (lum - lo) / (hi - lo)
    pos, ys = [], []
    for y in range(int(0.55 * level.shape[0]), int(0.92 * level.shape[0])):
        k = np.nonzero(level[y] < 0.5)[0]
        if not len(k) or k[0] < 2:
            continue
        e = k[0]
        pos.append(e - 1 + (level[y, e - 1] - 0.5) / max(level[y, e - 1] - level[y, e], 1e-6))
        ys.append(y)
    ys, pos = np.array(ys), np.array(pos)
    off = pos - np.polyval(np.polyfit(ys, pos, 1), ys)
    return float(off.std()), float(np.abs(off).max())


#: The feather's unit at 1440: the knee at 1024 as a share (0.002) and as two pixels.
UNIT = (("1024x768", 1024, 768, "today", 0.0, ""), ("1024x768", 1024, 768, "A2", 2.048, "0.002"),
        ("1024x768", 1024, 768, "A2", 3.072, "0.003"), ("1440x960", 1440, 960, "today", 0.0, ""),
        ("1440x960", 1440, 960, "A2", 2.88, "0.002"), ("1440x960", 1440, 960, "A2", 2.0, ""))


def bench_edge_unit() -> None:
    """The one bench step 2 left for the build: the feather as a share, or in pixels.

    At 1440x960 the painter found A2 at ``0.002`` -- 2.9 px there -- *a little chewed*,
    and could not tell whether a pixel count would read better (``answers-step2.md``,
    10b). The tooth it breaks against is a weave that scales with the canvas and a
    grain that does not. So the rock on bare ground and the tower's two strokes, at
    both sizes, the feather as a share of the long side and as two pixels: the
    painter's own numbers at the export's pixels and as a look at the default size
    shows them, and a sheet of each at four times.
    """
    print("     the feather's unit: the painter's measure on the rock's steep side, in px "
          "at the export's size and in a look at 1024")
    print(f"       {'canvas':<10}{'candidate':<22}{'wander':>8}{'bite':>7}"
          f"{'look: wander':>15}{'bite':>7}")
    rock = polygon([(0.30, 0.70), (0.36, 0.52), (0.46, 0.44), (0.58, 0.47), (0.66, 0.58),
                    (0.70, 0.72)], name="rock")
    towers, towers_look, rocks, rocks_look = [], [], [], []
    for size, width, height, kind, px, share in UNIT:
        amount = px / max(width, height)
        s = Session(width, height, timelapse=False, **PAINTING)
        s.palette["rock"] = s.palette.at_value(s.palette.mix("ultramarine", "burnt_umber",
                                                             0.5), 0.18)
        with warnings.catch_warnings(), feather(kind, amount, "hard"):
            warnings.simplefilter("ignore")
            s.block_in(rock, "flat", "rock", size=0.05, density=1.0, solid=True,
                       edge="hard", direction=15)
        wander, bite = ground_edge_numbers(s)
        f = 1024 / max(width, height)
        tag = "today" if kind == "today" else (
            f"A2 {px:.1f} px" + (f" (={share})" if share else ""))
        print(f"       {size:<10}{tag:<22}{wander:>8.2f}{bite:>7.2f}{wander * f:>15.2f}"
              f"{bite * f:>7.2f}")
        tower = _flat_field(width, height, 0.59)
        names = scope_of(tower)
        with warnings.catch_warnings(), feather(kind, amount, "all"):
            warnings.simplefilter("ignore")
            _tower_strokes(tower, names)
        label = f"{size} {tag}"
        for session, box, native, looked in ((tower, (0.665, 0.30, 0.735, 0.42), towers,
                                              towers_look),
                                             (s, (0.30, 0.50, 0.40, 0.64), rocks,
                                              rocks_look)):
            whole = Image.fromarray(session.canvas.to_srgb8(impasto=True, sketch=False))
            for picture, into in ((whole, native), (_look_px(whole), looked)):
                w, h = picture.size
                part = picture.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w),
                                     int(box[3] * h)))
                into.append((label, part.resize((part.width * 4, part.height * 4),
                                                Image.NEAREST)))
    for name, panels in (("edges_unit_tower.png", towers),
                         ("edges_unit_tower_look.png", towers_look),
                         ("edges_unit_rock.png", rocks),
                         ("edges_unit_rock_look.png", rocks_look)):
        print(f"       -> {save_sheet(panels, name, columns=3).relative_to(ROOT)}")


def bench_edge_seam() -> None:
    """Two hard masses that share a seam, each laid on bare ground -- a case step 2 missed.

    A mass laid back to front breaks over the paint behind it, which is what the
    feather is for. Two masses laid *up to one line*, each held to it, both break back
    from it, and what shows between them is the ground: a broken line along the seam,
    which is an outline. The far mass laid past the line first -- the guide's *paint
    masses, never up to a line* -- leaves the near one's edge breaking over paint.
    """
    print("     two hard masses sharing a seam on bare ground: the ground within 4 px of it")
    panels = []
    for ground in ("burnt_sienna", "toned_grey"):
        for kind, amount, past in (("today", 0.0, 0.0), ("A2", 0.002, 0.0),
                                   ("A2", 0.002, 0.01)):
            s = Session(1024, 768, texture="linen", ground=ground, seed=11, timelapse=False)
            p = s.palette
            p["dark"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.5), 0.20)
            p["light"] = p.at_value(p.mix("yellow_ochre", "titanium_white", 0.6), 0.75)
            with warnings.catch_warnings(), feather(kind, amount, "all"):
                warnings.simplefilter("ignore")
                s.block_in(Region(0.0, 0.0, 0.42 + past, 1.0), "flat", "dark", size=0.08,
                           solid=True, edge="hard")
                s.block_in(Region(0.42, 0.0, 1.0, 1.0), "flat", "light", size=0.08,
                           solid=True, edge="hard")
            seam = np.zeros((768, 1024), dtype=bool)
            seam[20:748, 430 - 4:430 + 4] = True
            tag = (f"{ground}, {'today' if kind == 'today' else f'A2 {amount}'}"
                   + (", the far one past the line" if past else ""))
            print(f"       {tag:<50} {s.canvas.ground_showing(where=seam):6.1%}")
            rgb = Image.fromarray(s.canvas.to_srgb8(impasto=True, sketch=False))
            part = rgb.crop((400, 300, 460, 380))
            panels.append((tag, part.resize((part.width * 5, part.height * 5),
                                            Image.NEAREST)))
    print(f"       -> {save_sheet(panels, 'edges_seam.png', columns=3).relative_to(ROOT)}")


def bench_edge_built(rb: Rebuilt) -> None:
    """The painting as this engine lays its thirteen scripts, against the one it had.

    None of the scripts passes ``feather=``, so every one of the 33 holds breaks at the
    default -- the horizon too, which its painter wants ruled and would now write
    ``feather=0`` for. What the check says after each pass, the tower's step, the
    ground, and the two places the verdict named, side by side.
    """
    built = rebuild(keep=False, cut=False)
    print(f"     the painting as this engine lays its scripts ({built.seconds:.0f} s), "
          f"against the one the painter had")
    for name in PASSES:
        was = next((line.strip() for line in rb.said[name] if "edges:" in line), "-")
        now = next((line.strip() for line in built.said[name] if "edges:" in line), "-")
        print(f"       {name:<18} {_edges_numbers(was)[0]:>5} -> {_edges_numbers(now)[0]:>5}")
    names = scope_of(built.session.scratch())
    rows = np.linspace(0.25, 0.52, 14)
    for label, session in (("had", rb.session), ("built", built.session)):
        steps = one_pixel_steps(values(session), names["tower"], rows)
        print(f"       {label:<6} tower's step {np.median(steps):.3f}   "
              f"{session._ground_line()}   {edges_line(values(session))}")
    panels = []
    for label, session in (("had", rb.session), ("built", built.session)):
        panels.append((f"tower, {label}", crop(session, (0.665, 0.18, 0.735, 0.42), zoom=3)))
        panels.append((f"headland, {label}", crop(session, (0.36, 0.46, 0.62, 0.66),
                                                  zoom=2)))
    print(f"       -> {save_sheet(panels, 'edges_built.png', columns=2).relative_to(ROOT)}")


def probe_edges(rb: Rebuilt, rb1440: Rebuilt | None) -> None:
    print("\n== 4A. an edge that is not a step: A1 feathered inward, A2 broken by the tooth ==")
    bench_edge_curve()
    bench_edge_sheets(rb, rb1440)
    print("  read: the step and the edges: line are the numbers, and A2 keeps each pixel "
          "crisp on purpose,\n  so neither can tell it from today. The sheets are the "
          "verdict.")
    print("\n  built (step 5): A2 at 0.002 on every hold")
    bench_edge_unit()
    bench_edge_seam()
    bench_edge_built(rb)


#: The corpus paintings whose scripts hold an edge somewhere -- `edge="hard"`, `clip=`
#: or `cover()` -- and so are the ones a moved default lays differently.
HELD = ("handover", "fogged", "hands", "pier", "bigpickle", "deepseek", "glm", "gpt",
        "grok", "kimi")


def _runs(mask: np.ndarray) -> list[tuple[int, tuple[int, int, int, int]]]:
    """The eight-connected runs of ``mask``, largest first, as (pixels, box)."""
    labels = label_components(mask)
    ys, xs = np.nonzero(labels)
    if not len(ys):
        return []
    lab = labels[ys, xs]
    order = np.argsort(lab, kind="stable")
    lab, ys, xs = lab[order], ys[order], xs[order]
    starts = np.flatnonzero(np.r_[True, lab[1:] != lab[:-1]])
    sizes = np.diff(np.r_[starts, len(lab)])
    boxes = zip(np.minimum.reduceat(xs, starts), np.minimum.reduceat(ys, starts),
                np.maximum.reduceat(xs, starts) + 1, np.maximum.reduceat(ys, starts) + 1,
                strict=True)
    return sorted(((int(n), tuple(int(v) for v in box)) for n, box in zip(sizes, boxes,
                                                                          strict=True)),
                  reverse=True)


def probe_corpus_edges() -> None:
    """Every corpus painting that holds an edge, laid cut and laid broken, and what shows.

    The seam bench's question asked of real paintings: where two held masses were laid
    up to one line, both break back from it and the ground shows along it. Each
    painting is replayed from its committed scripts twice -- every hold cut on the line
    as its painter had it, then as this engine lays the same scripts -- and the second
    is read against the first for the ground it leaves showing that the first did not,
    and for how that ground lies: a seam is a long thin run of it, a broken silhouette
    on bare ground a fringe. The runs that are longest are cropped for looking.
    """
    print("\n== 4A built: the corpus's held edges, cut and broken, and the ground each leaves ==")
    print(f"     {'painting':<11}{'moved':>8}{'ground cut':>12}{'broken':>9}{'new bare px':>13}"
          f"{'longest run':>13}{'runs over 60 px':>17}")
    panels = []
    for name in HELD:
        entry = next(p for p in cohort.CORPUS if p.name == name)
        with feather("today", 0.0):
            cut = cohort.replay(entry, keep_canvas=False)
        broken = cohort.replay(entry, keep_canvas=False)
        if cut.session is None or broken.session is None:
            print(f"     {name:<11} did not rebuild: {cut.error or broken.error}")
            continue
        a = cut.session.canvas.to_srgb8(impasto=False, sketch=False).astype(int)
        b = broken.session.canvas.to_srgb8(impasto=False, sketch=False).astype(int)
        moved = float((np.abs(a - b).max(axis=2) > 2).mean())
        was = cohort._bare(cut.session)
        now = cohort._bare(broken.session)
        new = now & ~was
        runs = _runs(new)
        longest = max((max(box[2] - box[0], box[3] - box[1]) for _, box in runs), default=0)
        long_runs = [r for r in runs if max(r[1][2] - r[1][0], r[1][3] - r[1][1]) > 60]
        print(f"     {name:<11}{moved:>8.2%}{float(was.mean()):>12.2%}{float(now.mean()):>9.2%}"
              f"{int(new.sum()):>13}{longest:>11} px{len(long_runs):>17}")
        for size, (x0, y0, x1, y1) in runs[:2]:
            if size < 20:
                continue
            pad = 12
            box = (max(0, x0 - pad), max(0, y0 - pad), min(a.shape[1], x1 + pad),
                   min(a.shape[0], y1 + pad))
            for tag, rgb in (("cut", a), ("broken", b)):
                part = Image.fromarray(rgb.astype(np.uint8)).crop(box)
                zoom = max(1, min(4, 240 // max(part.width, part.height, 1)))
                panels.append((f"{name} {tag} {size} px",
                               part.resize((part.width * zoom, part.height * zoom),
                                           Image.NEAREST)))
    if panels:
        print(f"       -> {save_sheet(panels, 'edges_corpus.png', columns=4).relative_to(ROOT)}")


# -- 4B. dry brush that streaks rather than speckles ------------------------------------

#: The candidates as step 2 benched them: copies of the stamp patched in for one bench.
GATES = ("today", "B1", "B2", "B1+B2", "B3")
#: The gate as step 6 built it (``Canvas.drag``, ``tooth_along``, ``DryComb``), beside
#: 0.6.0's -- and without its read along the travel, which is B2 alone as built, because
#: the painter asked to see the two side by side once they were tuned (12b).
BUILT = ("today", "built B2", "built")
#: How far along the travel B1 reads the tooth, in pixels: about one weave of linen.
ALONG = 9
#: B2: a bristle's own load is the stroke's raised to a power drawn per bristle between
#: a third and three -- a full brush is full in every bristle, an empty one in none,
#: and between the two some bristles hold their paint and some are dry.
B2_REACH = 3.0
#: B2: a bristle whose own load is under this lays nothing, whatever the tooth.
B2_EMPTY = 0.10

_GATE = {"name": "today", "angle": 0.0, "share": None}
_ALONG_CACHE: dict = {}


def _tooth_along(canvas, angle: float) -> np.ndarray:
    """The canvas tooth smoothed along one direction, kept to the field's own spread.

    A short line kernel along the travel, then rescaled to the tooth's own mean and
    standard deviation, so the gate at a given load still lets through about the same
    share of the canvas -- what changes is that what clears it is a run, not a pixel.
    """
    bucket = int(round(math.degrees(angle) / 10.0)) % 18
    key = (id(canvas), bucket)
    if key not in _ALONG_CACHE:
        tooth = canvas.height_map * _TOOTH_HEIGHT_W + canvas.grain * _TOOTH_GRAIN_W
        theta = math.radians(bucket * 10.0)
        acc = np.zeros_like(tooth)
        for k in range(-(ALONG // 2), ALONG // 2 + 1):
            dx, dy = int(round(k * math.cos(theta))), int(round(k * math.sin(theta)))
            acc += np.roll(np.roll(tooth, dy, axis=0), dx, axis=1)
        acc /= ALONG
        acc = tooth.mean() + (acc - acc.mean()) * (tooth.std() / max(float(acc.std()), 1e-6))
        if len(_ALONG_CACHE) > 36:
            _ALONG_CACHE.clear()
        _ALONG_CACHE[key] = acc.astype(np.float32)
    return _ALONG_CACHE[key]


def _gated_mask(self, radius_px, angle_rad, *args, **kw):
    """``Brush.mask``, noting the travel and, for a comb under B2, which bristle is where.

    The comb's per-bristle strengths are what the body is multiplied by (``strengths``
    from ``_bristle_index``), so the stamp over the body without the comb is each
    pixel's bristle strength;
    a hash of it gives each bristle its own draw, the same for the length of the stroke.
    """
    mask = _MASK(self, radius_px, angle_rad, *args, **kw)
    _GATE["angle"] = float(angle_rad)
    _GATE["share"] = None
    if "B2" in _GATE["name"] and self.tip == "bristle":
        body = _MASK(self.with_(tip="flat"), radius_px, angle_rad, *args,
                     **{k: v for k, v in kw.items() if k not in ("comb", "count")})
        if body.shape == mask.shape:
            strength = np.where(body > 1e-3, mask / np.maximum(body, 1e-3), 0.0)
            draw = np.modf(np.round(strength, 4) * 7919.0 + 0.137)[0]
            _GATE["share"] = np.where(body > 1e-3, draw, 0.5).astype(np.float32)
    return mask


def _gated_stamp(self, cx, cy, mask, color, strength, load, wetness_gain, thickness_gain,
                 texture_sensitivity, glaze=False, clip=None, travel=None, bristles=None):
    """``Canvas.stamp`` with the tooth gate swapped for the bench's candidate.

    A copy of the engine's own body at ``v0.6.0``, line for line, except inside the gate:
    B1 reads the tooth along the travel, B2 reads each bristle's own load, B3 thins what
    a starved brush lays. Anything the engine does after the gate is the engine's. The
    travel and the comb step 6's stroke hands the stamp are ignored: these are step 2's
    candidates as benched, not the gate that was built from them.
    """
    name = _GATE["name"]
    n = mask.shape[0]
    r = n // 2
    ix, iy = int(round(cx)), int(round(cy))
    x0, y0 = ix - r, iy - r
    sx0, sy0 = max(0, -x0), max(0, -y0)
    cx0, cy0 = max(0, x0), max(0, y0)
    cx1, cy1 = min(self.width, x0 + n), min(self.height, y0 + n)
    if cx1 <= cx0 or cy1 <= cy0:
        return 0.0
    sub = mask[sy0:sy0 + (cy1 - cy0), sx0:sx0 + (cx1 - cx0)]
    if clip is not None:
        sub = sub * clip[cy0:cy1, cx0:cx1]
        if not np.any(sub > 1e-4):
            return 0.0
    if "B1" in name:
        tooth = _tooth_along(self, _GATE["angle"])[cy0:cy1, cx0:cx1]
    else:
        tooth = (self.height_map[cy0:cy1, cx0:cx1] * _TOOTH_HEIGHT_W
                 + self.grain[cy0:cy1, cx0:cx1] * _TOOTH_GRAIN_W)
    wet = self.wetness[cy0:cy1, cx0:cx1]
    thick = self.thickness[cy0:cy1, cx0:cx1]
    dst = self.rgb[cy0:cy1, cx0:cx1]
    alpha = sub * float(np.clip(strength, 0.0, 1.0))
    ts = float(np.clip(texture_sensitivity, 0.0, 1.0))
    ld = float(np.clip(load, 0.0, 1.0))
    if ts > 0.0:
        share = _GATE["share"]
        if share is not None:
            own = ld ** (B2_REACH ** (2.0 * share[sy0:sy0 + (cy1 - cy0),
                                                 sx0:sx0 + (cx1 - cx0)] - 1.0))
            need = np.minimum((1.0 - own) * ts, self.tooth_ceiling)
        else:
            own = None
            need = min((1.0 - ld) * ts, self.tooth_ceiling)
        gate = np.clip((tooth - need) / GATE_BAND, 0.0, 1.0)
        gate = gate * gate * (3.0 - 2.0 * gate)
        gate = gate * (1.0 - 0.22 * ts * (1.0 - tooth))
        if own is not None:
            gate = gate * smooth(own / B2_EMPTY)
        alpha = alpha * gate
        if name == "B3" and ld < 1.0:
            alpha = alpha * ld
    alpha = alpha * (1.0 - 0.12 * np.clip(thick, 0.0, 1.0))
    effective = alpha * (1.0 - 0.55 * wet)
    np.clip(effective, 0.0, 1.0, out=effective)
    if not np.any(effective > 1e-4):
        return 0.0
    self.rgb[cy0:cy1, cx0:cx1] = CANVAS_MODULE.blend_wet(dst, color, effective)
    if self.has_sketch:
        sk = self.sketch[cy0:cy1, cx0:cx1]
        np.multiply(sk, 1.0 - effective, out=sk)
    if not glaze:
        np.add(thick, alpha * float(thickness_gain), out=thick)
        np.clip(thick, 0.0, CANVAS_MODULE._MAX_THICKNESS, out=thick)
    np.maximum(wet, alpha * float(wetness_gain), out=wet)
    np.clip(wet, 0.0, 1.0, out=wet)
    return float(effective.sum())


_MASK = BRUSH_MODULE.Brush.mask
_STAMP = CANVAS_MODULE.Canvas.stamp


_DRAG = CANVAS_MODULE.Canvas.drag
_ALONG = CANVAS_MODULE.Canvas.tooth_along


def _raw_tooth(self, travel):
    return self.height_map * _TOOTH_HEIGHT_W + self.grain * _TOOTH_GRAIN_W


@contextlib.contextmanager
def gate(name: str):
    """The tooth gate as candidate ``name``, for the length of a bench.

    **"today" patches too**, as ``feather("today")`` does for the edge: since step 6 the
    engine drags a starving brush, and 0.6.0's gate is what it lays when ``Canvas.drag``
    says a brush never drags -- the same code path, line for line, not a copy. "built" is
    the engine as it stands, and "built B2" the same with the tooth read where it lies
    rather than along the travel. The rest are step 2's copies.
    """
    if name == "built":
        yield
        return
    if name in ("today", "built B2"):
        if name == "today":
            CANVAS_MODULE.Canvas.drag = lambda self, load, need: 0.0
        else:
            CANVAS_MODULE.Canvas.tooth_along = _raw_tooth
        try:
            yield
        finally:
            CANVAS_MODULE.Canvas.drag = _DRAG
            CANVAS_MODULE.Canvas.tooth_along = _ALONG
        return
    _GATE["name"] = name
    BRUSH_MODULE.Brush.mask = _gated_mask
    CANVAS_MODULE.Canvas.stamp = _gated_stamp
    try:
        yield
    finally:
        BRUSH_MODULE.Brush.mask = _MASK
        CANVAS_MODULE.Canvas.stamp = _STAMP
        _GATE.update(name="today", share=None)


def bench_crosser(gates=GATES, prefix: str = "flecks") -> None:
    """The sky's own crosser, starved at four loads, on a field of the sky it crossed.

    ``p01_sky.py``'s first crosser -- ``bristle``, ``size=0.065``, ``opacity=0.40``,
    ``pressure="swell"`` -- on a canvas set to the sky's value, so what is counted is
    the mark and nothing under it. Its load runs down along the stroke as every
    stroke's does, so each row is a range of loads and the first number is where it
    starts. *Laid* is the stroke's own count of the paint it put down
    (``StrokeResult.paint``), which is what a gate tuned to lay today's paint keeps.
    """
    print("\n  the sky's crosser at four starting loads, on the sky's own value (0.56)")
    print(f"     {'gate':<9}{'load':>5}{'laid':>8}  {FLECK_HEAD}")
    path = [(-0.06, 0.40), (0.45, 0.46), (1.06, 0.52)]
    angle = math.atan2((0.52 - 0.40) * 768, 1.12 * 1024)
    panels = []
    for name in gates:
        for load in (0.3, 0.45, 0.6, 0.8):
            s = _flat_field(1024, 768, 0.56)
            s.palette["cloud"] = s.palette.at_value(
                s.palette.mix("ultramarine", "alizarin", 0.25), 0.39)
            before = values(s)
            with warnings.catch_warnings(), gate(name):
                warnings.simplefilter("ignore")
                laid = s.stroke(path, "bristle", "cloud", size=0.065, load=load,
                                opacity=0.40, pressure="swell").paint
            print(f"     {name:<9}{load:>5.2f}{laid:>8.0f}  "
                  f"{flecks(np.abs(values(s) - before), angle).row()}")
            if load in (0.3, 0.45, 0.6):
                panels.append((f"{name} load {load}", crop(s, (0.10, 0.36, 0.40, 0.56))))
    print(f"     -> {save_sheet(panels, f'{prefix}_crosser.png', columns=3).relative_to(ROOT)}")


#: ``p08_rock.py``'s five ledges, as the painter wrote them: the painting's five starved
#: ``flat`` marks, and the only ones -- its other eleven starved marks are bristles.
LEDGES = (
    ([(0.515, 0.641), (0.585, 0.628), (0.650, 0.622)], "ledge_warm", 0.010, 0.6, 0.8,
     [0.3, 1.0, 0.2]),
    ([(0.715, 0.603), (0.790, 0.591), (0.895, 0.588)], "ledge", 0.013, 0.55, 0.8,
     [0.2, 1.0, 0.5, 0.1]),
    ([(0.628, 0.703), (0.672, 0.689), (0.738, 0.687)], "ledge", 0.009, 0.6, 0.7,
     [0.4, 1.0, 0.1]),
    ([(0.855, 0.676), (0.925, 0.672), (1.03, 0.649)], "ledge", 0.016, 0.5, 0.8,
     [0.1, 0.9, 1.0]),
    ([(0.790, 0.806), (0.842, 0.790), (0.905, 0.793)], "ledge", 0.011, 0.5, 0.7,
     [0.2, 1.0, 0.3]),
)


def bench_ledges(rb: Rebuilt, gates=GATES, prefix: str = "flecks") -> None:
    """The painting's five starved flats, laid on the canvas they were laid on.

    A flat has no comb, so B2 has nothing to hold the load in and changes nothing here;
    what a gate can do for a starved chisel is B1's or B3's.
    """
    print("\n  the rock's five ledges (flat, size 0.009-0.016, load 0.7-0.8), on the canvas "
          "after p07")
    print(f"     {'gate':<9}  {FLECK_HEAD}")
    panels = []
    for name in gates:
        s = rb.after["p07_subject.py"].scratch()
        names = scope_of(s)
        p = names["p"]
        p["ledge"] = p.at_value(p.mix("cliff", "pale", 0.3), 0.245)
        p["ledge_warm"] = p.at_value(p.mix("lit_dim", "glow", 0.2), 0.27)
        before = values(s)
        with warnings.catch_warnings(), gate(name):
            warnings.simplefilter("ignore")
            for points, colour, size, opacity, load, pressure in LEDGES:
                s.stroke(points, "flat", colour, size=size, opacity=opacity, load=load,
                         pressure=pressure, clip=names["headland"])
        print(f"     {name:<9}  {flecks(np.abs(values(s) - before), 0.0).row()}")
        panels.append((name, crop(s, (0.50, 0.57, 1.0, 0.83), zoom=2)))
    print(f"     -> {save_sheet(panels, f'{prefix}_ledges.png', columns=1).relative_to(ROOT)}")


def bench_exercise_three(gates=GATES, prefix: str = "flecks") -> None:
    """``PAINTER.md``'s exercise 3, exactly: one stroke at four loads, on rough canvas."""
    print("\n  exercise 3: the same bristle stroke at four loads on rough canvas, no falloff")
    print(f"     {'gate':<9}{'load':>5}{'laid':>8}  {FLECK_HEAD}")
    panels = []
    for name in gates:
        s = Session(900, 400, texture="rough", ground="toned_grey", seed=3, timelapse=False)
        moved = []
        with warnings.catch_warnings(), gate(name):
            warnings.simplefilter("ignore")
            for i, load in enumerate([1.0, 0.6, 0.35, 0.2]):
                y = 0.15 + i * 0.22
                before = values(s)
                laid = s.stroke([(0.06, y), (0.94, y)], "bristle", "titanium_white",
                                size=0.07, load=load, load_falloff=0.0,
                                pressure="even").paint
                moved.append((load, laid, np.abs(values(s) - before)))
        for load, laid, diff in moved:
            print(f"     {name:<9}{load:>5.2f}{laid:>8.0f}  {flecks(diff, 0.0).row()}")
        panels.append((name, crop(s, (0.0, 0.0, 1.0, 1.0))))
    print(f"     -> {save_sheet(panels, f'{prefix}_exercise3.png', columns=1).relative_to(ROOT)}")


def _recipe_scope(width: int = 1024, height: int = 768) -> dict:
    """The names the guide's blocks assume -- ``easel.demo.preamble`` -- at a painting's size."""
    scope: dict = {}
    source = preamble(tempfile.gettempdir(), timelapse=False).replace(
        "Session(400, 300,", f"Session({width}, {height},")
    exec(compile(source, "<preamble>", "exec"), scope)  # noqa: S102
    return scope


def bench_planes_recipe(gates=GATES, prefix: str = "flecks") -> None:
    """*A mass built of planes*, which lays ``load=0.35`` for its surface, at 1024x768."""
    print("\n  the planes recipe's dry-brush scrape (bristle 0.03, load=0.35, opacity 0.6)")
    print(f"     {'gate':<9}  {FLECK_HEAD}")
    block = next(d for d in demos() if d.heading == "A mass built of planes").recipe
    body, scrape = block.rsplit("s.stroke([(0.14, 0.72)", 1)
    scrape = "s.stroke([(0.14, 0.72)" + scrape
    angle = math.atan2(0.04 * 768, 0.12 * 1024)
    panels = []
    for name in gates:
        scope = _recipe_scope()
        with warnings.catch_warnings(), gate(name):
            warnings.simplefilter("ignore")
            exec(compile(body, "<planes>", "exec"), scope)  # noqa: S102
            before = values(scope["s"])
            exec(compile(scrape, "<scrape>", "exec"), scope)  # noqa: S102
        print(f"     {name:<9}  {flecks(np.abs(values(scope['s']) - before), angle).row()}")
        panels.append((name, crop(scope["s"], (0.04, 0.54, 0.60, 0.94))))
    print(f"     -> {save_sheet(panels, f'{prefix}_planes.png', columns=5).relative_to(ROOT)}")


def bench_water(rb: Rebuilt, gates=GATES, prefix: str = "flecks") -> None:
    """The painter's first swells and surf: its water pass as rehearsed, on the painting."""
    print("\n  the first water pass, as rehearsed (misfires/water): surf and swells, to look at")
    panels = []
    for name in gates:
        s = rb.after["p05_light.py"].scratch()
        with gate(name):
            lay_pass(s, "06_water_v1.py", prelude=MISFIRES / "water" / "prelude.py",
                     folder=MISFIRES / "water")
        panels.append((name, crop(s, (0.30, 0.60, 0.86, 0.99))))
    print(f"     -> {save_sheet(panels, f'{prefix}_water.png', columns=2).relative_to(ROOT)}")


def bench_sampler(gates=GATES, prefix: str = "flecks") -> None:
    """The brush sampler's linen rows for the two brushes a painting starves, under each gate.

    ``LESSONS.md`` trap 1: the sampler shows isolated strokes at full load, and a full
    stroke's load still runs down along it, so its tail is the part to read.
    """
    import make_brush_sampler as sampler

    print("\n  the sampler, bristle and flat on linen: every size and pressure")
    panels = []
    for name in gates:
        with gate(name):
            cells = [sampler.render_cell(brush, size, pressure, "linen", 100 + r * 31 + c * 7)
                     for r, brush in enumerate(("bristle", "flat"))
                     for c, (size, pressure) in enumerate(
                         (v, p) for _, v in sampler.SIZES for p in sampler.PRESSURES)]
        cw, ch = cells[0].size
        grid = Image.new("RGB", (cw * 9, ch * 2), (20, 20, 22))
        for i, cell in enumerate(cells):
            grid.paste(cell, ((i % 9) * cw, (i // 9) * ch))
        panels.append((name, grid))
    print(f"     -> {save_sheet(panels, f'{prefix}_sampler.png', columns=1).relative_to(ROOT)}")


def probe_flecks(rb: Rebuilt) -> None:
    print("\n== 4B. dry brush: B1 the tooth read along the travel, B2 per bristle, "
          "B3 thinner ==")
    bench_crosser()
    bench_ledges(rb)
    bench_exercise_three()
    bench_planes_recipe()
    bench_water(rb)
    bench_sampler()
    print("  read: *specks* is the confetti, *long* is whether the pieces run with the "
          "brush. B3 changes\n  contrast and nothing else, as the plan expected; look at "
          "the sheets before any number.")


def _starving_paths(n: int, seed: int) -> list[list[tuple[float, float]]]:
    """``n`` three-point strokes at random places and directions, a third of them backwards."""
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        x0, y0 = rng.uniform(0.05, 0.35), rng.uniform(0.15, 0.85)
        turn = rng.uniform(-0.6, 0.6) + (math.pi if rng.random() < 0.3 else 0.0)
        length = rng.uniform(0.3, 0.6)
        x1, y1 = x0 + length * math.cos(turn) * 0.75, y0 + length * math.sin(turn)
        bend = rng.uniform(-0.03, 0.03, 2)
        out.append([(x0, y0), ((x0 + x1) / 2 + bend[0], (y0 + y1) / 2 + bend[1]), (x1, y1)])
    return out


#: The marks the amounts are counted over: the painting's own starving bristle, the
#: guide's exercise, and a flat and a round, which have no comb and drag only along.
AMOUNTS = (
    ("bristle", "linen", 0.065, None, (0.3, 0.45, 0.6, 0.8)),
    ("bristle", "rough", 0.07, 0.0, (0.2, 0.35, 0.6)),
    ("bristle", "smooth", 0.05, None, (0.3, 0.45, 0.6)),
    ("flat", "linen", 0.03, None, (0.35, 0.5, 0.7)),
    ("round_hard", "linen", 0.02, None, (0.3, 0.5, 0.7)),
)


def bench_amounts(gates=BUILT, n: int = 24) -> None:
    """Does each load still lay today's paint? ``n`` strokes a row, summed, against today's.

    The painter's condition on B: *the amount was right, the shape was wrong*. One stroke
    says little -- which bristles hold their paint, and where a stroke's footprint falls
    on the tooth, move a single mark's weight either way -- so each row is ``n`` strokes
    at random places and directions, each with its own comb, and the ratio is their
    paint against the same strokes today, with the tenth and ninetieth percentile of the
    ratio stroke by stroke.
    """
    print(f"\n  what each load lays, {n} strokes a row, against today's")
    paths = _starving_paths(n, 7)
    for tip, texture, size, falloff, loads in AMOUNTS:
        print(f"     {tip} size {size} on {texture}"
              + ("" if falloff is None else f", load_falloff={falloff}"))
        for load in loads:
            laid = {}
            for name in gates:
                per = []
                for path in paths:
                    s = Session(1024, 768, texture=texture, ground="toned_grey", seed=11,
                                timelapse=False)
                    kw = {"load": load, "size": size, "opacity": 0.6}
                    if falloff is not None:
                        kw["load_falloff"] = falloff
                    with warnings.catch_warnings(), gate(name):
                        warnings.simplefilter("ignore")
                        per.append(s.stroke(path, tip, "titanium_white", **kw).paint)
                laid[name] = np.array(per)
            base = laid[gates[0]]
            cells = []
            for name in gates[1:]:
                ratio = laid[name] / np.maximum(base, 1e-6)
                cells.append(f"{name} x{laid[name].sum() / max(base.sum(), 1e-6):.2f} "
                             f"({np.percentile(ratio, 10):.2f}-{np.percentile(ratio, 90):.2f})")
            print(f"       load {load:.2f}  today {base.sum():>9.0f}   " + "   ".join(cells))


def probe_dry(rb: Rebuilt) -> None:
    """4B as built, beside 0.6.0's gate: the painter's marks, the amounts, the sheets."""
    print("\n== 4B built: a brush running dry, as the engine drags it, beside 0.6.0's gate ==")
    bench_crosser(BUILT, "dry")
    bench_exercise_three(BUILT, "dry")
    bench_ledges(rb, BUILT, "dry")
    bench_planes_recipe(BUILT, "dry")
    bench_water(rb, BUILT, "dry")
    bench_sampler(BUILT, "dry")
    bench_amounts()
    print("  read: *laid* and the ratios are the painter's condition, the pieces and their "
          "length the shape;\n  the sheets are the verdict.")


def probe_corpus_dry() -> None:
    """Every corpus painting rebuilt under 0.6.0's gate and under this one: what moves.

    A saved painting's log replays with the engine installed, so this is what a rebuild
    of each committed painting lays now -- its holds cut on the line both times, since a
    saved clip replays at the feather it was laid with and none was laid with one. For
    each: how much of the canvas moves, how many of its marks the rebuild notice counts
    as dragging (``notices.REBUILDS``, ``easel.stroke.drags``), and the two canvases'
    ground. The largest change in each is cropped for looking.
    """
    from easel import notices

    print("\n== 4B built: the corpus rebuilt under 0.6.0's gate and this one ==")
    print(f"     {'painting':<11}{'marks':>7}{'drag':>6}{'moved >2':>10}{'>8':>8}"
          f"{'ground was':>12}{'now':>7}{'seconds':>9}")
    dry = next(c for c in notices.REBUILDS if c.version == "0.7.0")
    panels = []
    for entry in cohort.CORPUS:
        started = time.time()
        with feather("today", 0.0), gate("today"):
            was = cohort.replay(entry, keep_canvas=False)
        with feather("today", 0.0):
            now = cohort.replay(entry, keep_canvas=False)
        if was.session is None or now.session is None:
            print(f"     {entry.name:<11} did not rebuild: {was.error or now.error}")
            continue
        records = [r for r in now.session.history.records if r.kind in ("stroke", "glaze",
                                                                          "smudge")]
        dragging = sum(1 for r in records if dry.moves(r, now.session.canvas))
        a = was.session.canvas.to_srgb8(impasto=False, sketch=False).astype(int)
        b = now.session.canvas.to_srgb8(impasto=False, sketch=False).astype(int)
        moved = np.abs(a - b).max(axis=2)
        print(f"     {entry.name:<11}{len(records):>7}{dragging:>6}{float((moved > 2).mean()):>10.2%}"
              f"{float((moved > 8).mean()):>8.2%}{float(cohort._bare(was.session).mean()):>12.2%}"
              f"{float(cohort._bare(now.session).mean()):>7.2%}{time.time() - started:>9.0f}")
        runs = _runs(moved > 8)
        if runs and runs[0][0] >= 40:
            x0, y0, x1, y1 = runs[0][1]
            pad = 16
            box = (max(0, x0 - pad), max(0, y0 - pad), min(a.shape[1], x1 + pad),
                   min(a.shape[0], y1 + pad))
            for tag, rgb in (("0.6.0", a), ("now", b)):
                part = Image.fromarray(rgb.astype(np.uint8)).crop(box)
                zoom = max(1, min(3, 300 // max(part.width, part.height, 1)))
                panels.append((f"{entry.name} {tag}",
                               part.resize((part.width * zoom, part.height * zoom),
                                           Image.LANCZOS)))
    if panels:
        print(f"       -> {save_sheet(panels, 'dry_corpus.png', columns=4).relative_to(ROOT)}")


# -- 4C. the four cases in hand ------------------------------------------------------------

def _pass_marks(session: Session, start: int) -> list:
    from easel.history import History

    return [r for r in session.history.records[start:]
            if r.kind not in History.UNPAINTED_KINDS]


def probe_misfires() -> None:
    """The narrowed rule on the four cases the plan drew it on.

    The two misfires, each rebuilt as the painter's README says -- on the prelude of
    their own moment, through the passes before them -- and rehearsed; and the recipe's
    own passage and failure block (*A passage brightening toward one side*), which the
    rule must stay silent on and must fire on. A gate that silences both misfires and
    keeps the failure was the candidate, and the corpus decided otherwise
    (``probe_cohort_session.py --graded``): step 7 built the overlap break alone, which
    silences the water and leaves the headland. The *engine* column is the engine's own
    line, held to the re-implementation of the built gate.
    """
    print("\n== 4C. graded passage laid too narrow: the four cases in hand ==")
    cases = []
    for case, upto, script in (("headland", "p02_sea.py", "03_headland_v2.py"),
                               ("water", "p05_light.py", "06_water_v1.py")):
        folder = MISFIRES / case
        rb = rebuild(upto=upto, prelude=folder / "prelude.py", keep=False)
        s = rb.session.scratch()
        start = s._open_pass()
        said = lay_pass(s, script, prelude=folder / "prelude.py", folder=folder)
        cases.append((f"the {case} misfire", s, _pass_marks(s, start), said, "silent"))
    demo = next(d for d in demos() if d.heading == "A passage brightening toward one side")
    for label, body, want in (("the recipe's passage", demo.recipe, "silent"),
                              ("the recipe's failure block", demo.failure, "fires")):
        scope = _recipe_scope(400, 300)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            exec(compile(demo.passage, "<passage>", "exec"), scope)  # noqa: S102
            start = scope["s"]._open_pass()
            exec(compile(body, f"<{label}>", "exec"), scope)  # noqa: S102
        s = scope["s"]
        cases.append((label, s, _pass_marks(s, start), s.report(since=start).splitlines(),
                      want))
    names = list(cohort.GATES)
    print(f"  {'case':<28}{'wanted':>8}{'engine':>8}  " + "".join(f"{n:>15}" for n in names))
    for label, s, marks, said, want in cases:
        engine = any(cohort.GRADED_WORDS in line for line in said)
        verdicts = cohort.graded_verdicts(marks, s.canvas)
        cells = "".join(f"{'FIRES' if v is not None and v.fires else '-':>15}"
                        for v in (verdicts[name] for name in names))
        print(f"  {label:<28}{want:>8}{'FIRES' if engine else '-':>8}  {cells}")
        built = verdicts[cohort.BUILT]
        if engine != (built is not None and built.fires):
            print(f"  {'':<28}  (the engine disagrees with the re-implementation of "
                  f"'{cohort.BUILT}')")
        for name in ("0.6.0", cohort.BUILT):
            run = verdicts[name]
            if run is None:
                continue
            sizes = sorted(float(r.params.get("size", 0.0)) for r in run.marks)
            print(f"  {'':<28}  {name}: {len(run.marks)} marks, step {run.step:.3f}, sizes "
                  f"{sizes[0]:.3g}..{sizes[-1]:.3g}, median {float(np.median(sizes)):.3g}, "
                  f"{run.per_step:.2f} of a step")
        swept = [share for share in cohort.SWEEP
                 if verdicts[cohort.swept(share)] is not None
                 and verdicts[cohort.swept(share)].fires]
        print(f"  {'':<28}  the break swept: fires at "
              + (", ".join(f"{share:.0%}" for share in swept) if swept else "no share"))
        run = verdicts["0.6.0"]
        if run is not None and run.fires and want == "silent":
            slug = label.split()[1]
            path = cohort.crop_graded(s.canvas, run, OUT / f"graded_{slug}.png")
            print(f"  {'':<28}  -> {path.relative_to(ROOT)}")
    print(f"  read: the engine is '{cohort.BUILT}' since step 7 -- silent on the water, "
          f"firing on the failure block, and still on the headland's stacked masses.")


# -- 4D. rehearsing alternatives side by side ---------------------------------------------

def _warm(_: int) -> int:
    """Nothing, in a worker: what makes a spawned pool start its processes and import."""
    time.sleep(0.05)
    return 0


def _panel_worker(job: tuple) -> tuple[str, bytes, float]:
    """One panel of a sheet, in a process of its own: load, lay, render, hand back PNG."""
    path, strokes, setting, scale = job
    started = time.perf_counter()
    s = Session.load(path)
    trial = s._trial_session()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for kind, spec in s._plan_specs(strokes):
            trial._lay(kind, dict(spec, **setting))
    image = render_look(trial.canvas, scale=scale, marks=s.marks or None)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    label = " ".join(f"{k}={v}" for k, v in setting.items())
    return label, buffer.getvalue(), time.perf_counter() - started


def probe_sheet() -> None:
    """What a variant costs, and whether a sheet in several processes pays.

    The painter's harness: a copy of the session, three sky ramps, a look -- timed part
    by part, because the verdict's fifteen seconds is either bookkeeping or paint and
    only the parts say which. Then a ``vary=`` sheet of one band, and the same sheet's
    four panels in four spawned processes, Windows' spawn cost included. The plan's
    target for D1 is a four-panel sheet in under 1.5 times one panel.
    """
    print("\n== 4D. what a variant costs, and a sheet in one process and in four ==")
    state = rebuild(upto="p00_draw.py", keep=False).session
    names = scope_of(state)
    names["p"]["low_cool"] = names["p"].at_value(names["p"].mix("alizarin", "yellow_ochre",
                                                                0.6), 0.64)
    top = polygon([(-0.06, -0.06), (1.06, -0.06), (1.06, 0.27), (-0.06, 0.29)])
    mid = polygon([(-0.06, 0.17), (1.06, 0.15), (1.06, 0.45), (-0.06, 0.47)])
    low = polygon([(-0.06, 0.35), (1.06, 0.33), (1.06, 0.62), (-0.06, 0.62)])
    kw = {"opacity": 0.95, "jitter": 0.01, "size_jitter": 0.03}
    with warnings.catch_warnings(), tempfile.TemporaryDirectory() as tmp:
        warnings.simplefilter("ignore")
        copy_s, c = _time(state.scratch)
        bands = []
        for place, a, b, d in ((top, "zenith", "high", 3), (mid, "high", "pale", -2),
                               (low, "pale", "low_cool", 2)):
            took, _ = _time(lambda place=place, a=a, b=b, d=d: c.scumble(
                place, a, b, 8, direction=d, **kw))
            bands.append(took)
        look_s, _ = _time(lambda: c.look(path=Path(tmp) / "variant.png", marks=False,
                                         sketch=False))
        total = copy_s + sum(bands) + look_s
        print(f"  the harness's three-band sky variant: {total:.1f}s -- the copy "
              f"{copy_s:.2f}s, the three 8-pass scumbles {sum(bands):.1f}s "
              f"({', '.join(f'{t:.1f}' for t in bands)}), the look {look_s:.2f}s")
        print(f"  one band is {bands[0]:.1f}s, {bands[0] / 8:.2f}s a pass")

        plan = [{"band": top, "color_a": "zenith", "color_b": "high", "n": 8,
                 "direction": 3, **kw}]
        state.palette["low_cool"] = names["p"]["low_cool"]
        took, _ = _time(lambda: state.rehearse(plan, path=Path(tmp) / "two.png",
                                               vary={"opacity": [0.95, 0.7]}))
        print(f"  a rehearse(vary=) sheet of the same band at two opacities: {took:.1f}s")

        beam = [{"points": [(0.697, 0.178), (0.30, 0.292), (-0.08, 0.388)], "glaze": True,
                 "color": "sea_far", "opacity": 0.09, "size": 0.20,
                 "pressure": [0.4, 0.8, 1.0]}]
        took, _ = _time(lambda: state.rehearse(beam, path=Path(tmp) / "glaze.png",
                                               vary={"opacity": [0.06, 0.09, 0.12]}))
        print(f"  a vary= sheet of three opacities of a glaze -- a plan entry with "
              f"\"glaze\": True, which no document names: {took:.1f}s")

        settings = [{"opacity": v} for v in (0.95, 0.85, 0.75, 0.65)]
        one, _ = _time(lambda: state.rehearse(plan, path=Path(tmp) / "one.png"))
        four, _ = _time(lambda: state.rehearse(plan, path=Path(tmp) / "four.png",
                                               vary={"opacity": [s["opacity"]
                                                                 for s in settings]}))
        state.out_dir = Path(tmp)
        saved = state.save(Path(tmp) / "state.easel")
        panel = max(int(session_module.DEFAULT_LOOK_SIZE) // 4, 200)
        jobs = [(str(saved), plan, setting, panel) for setting in settings]
        started = time.perf_counter()
        context = multiprocessing.get_context("spawn")
        with context.Pool(4) as pool:
            # A spawned pool starts its processes lazily; one trivial job each is what
            # makes all four start and import the engine, which is the cost Windows pays.
            pool.map(_warm, range(4), chunksize=1)
            ready = time.perf_counter() - started
            results = pool.map(_panel_worker, jobs, chunksize=1)
        sheet = label_sheet([(label, Image.open(io.BytesIO(png))) for label, png, _ in results],
                            columns=4)
        sheet.save(Path(tmp) / "parallel.png")
        parallel = time.perf_counter() - started
        inside = max(t for _, _, t in results)
        print(f"  one panel {one:.1f}s; a four-panel sheet in one process {four:.1f}s "
              f"({four / one:.1f}x); in four spawned processes {parallel:.1f}s "
              f"({parallel / one:.1f}x), of which starting four processes and importing "
              f"the engine in each {ready:.1f}s, and the slowest panel -- loading the "
              f"session file included -- {inside:.1f}s")
        print(f"  the plan's target for D1: under {1.5 * one:.1f}s (1.5x one panel) -- "
              f"{'met' if parallel < 1.5 * one else 'missed'} on this machine")


# -- 4F. the session file -------------------------------------------------------------------

def _resave(data: dict, path: Path, **changes) -> float:
    """The session file written again with some arrays changed; its size in megabytes."""
    arrays = {k: v for k, v in data.items()}
    arrays.update(changes)
    with path.open("wb") as fh:
        np.savez_compressed(fh, **arrays)
    return path.stat().st_size / 1e6


def probe_file() -> None:
    """The painting's session file, saved as the painter's was, and again each way."""
    print("\n== 4F. the session file, and what is in it ==")
    rb = rebuild(timelapse=True, keep=False)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        rb.session.out_dir = tmp
        saved = rb.session.save(tmp / "lighthouse.easel")
        with np.load(saved, allow_pickle=False) as npz:
            data = {k: npz[k] for k in npz.files}
        if not data["frames"].size and rb.session.history._frames:
            # Since step 4 a save keeps no frames; put them back, so what is measured
            # here is still the file as 0.6.0 wrote it -- the one the round began from.
            data["frames"] = np.stack(rb.session.history._frames)
            _resave(data, saved)
        frames = data["frames"]
        print(f"  as saved: {saved.stat().st_size / 1e6:.2f} MB, with {len(frames)} "
              f"time-lapse frames of {frames.shape[1:] if frames.size else '-'}")
        for key in ("frames", "rgb", "wetness", "thickness", "log", "last_look", "sketch"):
            alone = _resave({key: data[key]}, tmp / f"{key}.npz")
            print(f"     {key:<10} {alone:6.2f} MB compressed on its own")
        empty = np.zeros((0, 1, 1, 3), dtype=np.uint8)
        rows = [("the time-lapse frames left out", {"frames": empty}),
                ("colour as float16", {"rgb": data["rgb"].astype(np.float16)}),
                ("every canvas plane as float16",
                 {k: data[k].astype(np.float16) for k in ("rgb", "wetness", "thickness")}),
                ("both: frames out, colour float16",
                 {"frames": empty, "rgb": data["rgb"].astype(np.float16)})]
        for label, changes in rows:
            print(f"  {label:<34} {_resave(data, tmp / 'variant.npz', **changes):6.2f} MB")
        packed, offsets = [], [0]
        for frame in frames:
            buffer = io.BytesIO()
            Image.fromarray(frame).save(buffer, format="PNG")
            packed.append(np.frombuffer(buffer.getvalue(), dtype=np.uint8))
            offsets.append(offsets[-1] + len(packed[-1]))
        if packed:
            as_png = {"frames": empty, "frames_png": np.concatenate(packed),
                      "frames_at": np.asarray(offsets, dtype=np.int64)}
            print(f"  {'the frames stored as PNG bytes':<34} "
                  f"{_resave(data, tmp / 'variant.npz', **as_png):6.2f} MB")
        export = rb.session.canvas.to_srgb8()
        half = rb.session.canvas.rgb.astype(np.float16).astype(np.float32)
        original = rb.session.canvas.rgb.copy()
        rb.session.canvas.rgb[...] = half
        moved = np.abs(rb.session.canvas.to_srgb8().astype(np.int16) - export.astype(np.int16))
        rb.session.canvas.rgb[...] = original
        changed = int((moved.max(axis=2) > 0).sum())
        print(f"  colour through float16 and back: {changed} of {export.shape[0] * export.shape[1]}"
              f" export pixels move ({changed / (export.shape[0] * export.shape[1]):.1%}), "
              f"by at most {int(moved.max())} level(s) -- 'opens as it was painted' "
              f"would stop being true")
        _resave(data, tmp / "noframes.easel", frames=empty)
        loaded = Session.load(tmp / "noframes.easel")
        took, _ = _time(lambda: loaded.timelapse_gif(tmp / "rebuilt.gif", from_log=True))
        print(f"  a GIF rebuilt from the log of a file with no frames: {took:.0f}s")


#: The painter's own workflow, run in a process of its own: ``easel new``, the thirteen
#: passes through ``easel run`` one at a time -- each a load, a pass and a save, which is
#: what the shell does -- then the file, and ``easel timelapse`` at the end. A child
#: started with ``-S`` so that an editable install's import hook cannot hand it the
#: checkout instead of the engine named (``LESSONS.md``'s papercut); site-packages are
#: put back by hand for numpy and PIL.
_SHELL_CHILD = r'''
import contextlib, io, shutil, site, sys, tempfile, time, warnings
from pathlib import Path
sys.path.insert(0, sys.argv[1])
sys.path.extend(site.getsitepackages())
import easel
from easel import Session
from easel.cli import main
from PIL import Image

here, painting = Path(sys.argv[2]), sys.argv[3:]
warnings.simplefilter("ignore")
print(f"  engine {easel.__version__} from {Path(easel.__file__).parent}")
with tempfile.TemporaryDirectory(prefix="easel-shell-") as tmp:
    tmp = Path(tmp)
    shutil.copy(here / "prelude.py", tmp / "prelude.py")
    session, sink = tmp / "lighthouse.easel", io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        assert main(["new", str(session), *painting, "--out-dir", str(tmp / "out")]) == 0
    took = []
    for script in sorted(here.glob("p[0-9][0-9]_*.py")):
        started = time.perf_counter()
        with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
            assert main(["run", str(session), str(script)]) == 0, sink.getvalue()[-2000:]
        took.append(time.perf_counter() - started)
    loads, saves = [], []
    for _ in range(3):
        started = time.perf_counter()
        s = Session.load(session)
        loads.append(time.perf_counter() - started)
        started = time.perf_counter()
        s.save(tmp / "again.easel")
        saves.append(time.perf_counter() - started)
    started = time.perf_counter()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        assert main(["timelapse", str(session), str(tmp / "film.gif")]) == 0
    film = time.perf_counter() - started
    with Image.open(tmp / "film.gif") as im:
        frames, size = im.n_frames, im.size
    print(f"  the {len(took)} passes through `easel run`: {sum(took):.1f} s "
          f"({', '.join(f'{t:.1f}' for t in took)})")
    print(f"  the file: {session.stat().st_size / 1e6:.2f} MB, {len(s.history.records)} "
          f"records, {s.history.frame_count} time-lapse frames in it; load "
          f"{min(loads):.2f} s, save {min(saves):.2f} s, best of three")
    print(f"  `easel timelapse` at the end: {film:.1f} s, {frames} frames at {size}, "
          f"{(tmp / 'film.gif').stat().st_size / 1e6:.2f} MB")
'''


def probe_shell(engines: list[str]) -> None:
    """4F, built: what the painter's workflow costs from the shell, engine by engine.

    Each engine is a ``src`` directory; the checkout's own when none is named. To set
    this build beside the one before it: ``git archive <commit> src | tar -x -C DIR``
    and pass ``--engine DIR/src`` as well. Timings only on a quiet machine.
    """
    import subprocess

    print("\n== 4F, built: the painter's passes through the shell ==")
    painting = ["--size", "1024x768", "--texture", PAINTING["texture"], "--ground",
                PAINTING["ground"], "--seed", str(PAINTING["seed"]), "--budget",
                str(PAINTING["budget"])]
    for src in engines or [str(ROOT / "src")]:
        subprocess.run([sys.executable, "-S", "-c", _SHELL_CHILD, src, str(HERE), *painting],
                       check=True)


# -- 4G. the pressure-list fade, and the wet bands -------------------------------------------

def probe_pressure() -> None:
    """Finding 10: how fast a pressure list's fade arrives, on the painter's test and the recipe's.

    The painter's own test from ``verify.py`` -- a scumble at ``pressure=[1.0, 0.75,
    0.25, 0.0]`` on a dark field, read by thirds -- and the same band read over its last
    twentieth and its last 4%, where the profile reaches nothing. Then the recipe's own
    passage, *a passage brightening toward one side*, read at its no-pressure end.
    """
    print("\n== 4G. a pressure list's fade, and three bands laid wet ==")
    for opacity in (0.9, 0.5):
        s = Session(1024, 768, ground="toned_grey", seed=2, timelapse=False)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            s.block_in(Region(0, 0, 1, 1), "flat",
                       s.palette.mix("ultramarine", "burnt_umber", 0.5), size=0.1,
                       solid=True, edge="hard")
            s.dry()
            field_lum = painters_lum(s.canvas.to_srgb8(sketch=False))
            s.scumble(Region(-0.06, 0.30, 1.06, 0.70), "cadmium_yellow", "titanium_white",
                      6, opacity=opacity, pressure=[1.0, 0.75, 0.25, 0.0])
        lum = painters_lum(s.canvas.to_srgb8(sketch=False))[int(0.35 * 768):int(0.65 * 768)]
        field = float(field_lum[int(0.35 * 768):int(0.65 * 768)].mean())

        def over(a: float, b: float, lum=lum) -> float:
            return float(lum[:, int(a * 1024):int(b * 1024)].mean())

        print(f"  the painter's test at opacity {opacity}: {over(0.02, 0.33):.3f} / "
              f"{over(0.33, 0.66):.3f} / {over(0.66, 0.98):.3f} by thirds on a "
              f"{field:.3f} field; {over(0.95, 1.0):.3f} over the last twentieth, "
              f"{over(0.96, 1.0):.3f} over the last 4%")

    demo = next(d for d in demos() if d.heading == "A passage brightening toward one side")
    scope = _recipe_scope()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s = scope["s"]
        s.block_in(Region(0, 0, 1, 1), "flat", "dark", size=0.1, solid=True, edge="hard")
        s.dry()
        view = values(s)
        field = float(view[int(0.44 * 768):int(0.58 * 768), int(0.24 * 1024):int(0.32 * 1024)]
                      .mean())
        exec(compile(demo.recipe, "<recipe>", "exec"), scope)  # noqa: S102
    view = values(s)
    rows = slice(int(0.44 * 768), int(0.58 * 768))
    start = float(view[rows, int(0.24 * 1024):int(0.32 * 1024)].mean())
    end = float(view[rows, int(0.90 * 1024):int(1.0 * 1024)].mean())
    print(f"  the recipe's own passage: {start:.3f} at its no-pressure end on a {field:.3f} "
          f"field, {end:.3f} at the full-pressure end")
    probe_wet_bands()


def probe_wet_bands() -> None:
    """Finding 8's seam, withdrawn, and the wet layering that is real.

    ``p01_sky.py``'s three ramps on a fresh canvas, laid one after another wet and then
    again with ``dry()`` between them: how much of the canvas the wet layering moves,
    and whether either draws a column seam.
    """
    views = {}
    for label, dry in (("wet", False), ("dried between", True)):
        s = Session(1024, 768, timelapse=False, **PAINTING)
        names = scope_of(s)
        p = names["p"]
        p["low_cool"] = p.at_value(p.mix("alizarin", "yellow_ochre", 0.6), 0.64)
        kw = {"opacity": 0.95, "jitter": 0.01, "size_jitter": 0.03}
        bands = ((polygon([(-0.06, -0.06), (1.06, -0.06), (1.06, 0.27), (-0.06, 0.29)]),
                  "zenith", "high", 3),
                 (polygon([(-0.06, 0.17), (1.06, 0.15), (1.06, 0.45), (-0.06, 0.47)]),
                  "high", "pale", -2),
                 (polygon([(-0.06, 0.35), (1.06, 0.33), (1.06, 0.62), (-0.06, 0.62)]),
                  "pale", "low_cool", 2))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for place, a, b, d in bands:
                s.scumble(place, a, b, 8, direction=d, **kw)
                if dry:
                    s.dry()
        view = s.canvas.values(sketch=False).astype(np.int16)
        views[label] = view
        views[f"{label}, colour"] = s.canvas.to_srgb8(sketch=False).astype(np.int16)
        band = view[int(0.08 * 768):int(0.55 * 768)].astype(np.float32) / 255.0
        jumps = np.abs(np.diff(band, axis=1)).mean(axis=0)
        top = np.argsort(jumps)[::-1][:3]
        print(f"  the three sky ramps, {label}: median column jump {np.median(jumps):.4f}, "
              f"largest at x = " + ", ".join(f"{t / 1024:.3f} ({jumps[t]:.4f})" for t in top))
    moved = np.abs(views["wet"] - views["dried between"])
    colour = np.abs(views["wet, colour"] - views["dried between, colour"]).max(axis=2)
    print(f"  drying between the bands moves {float((moved > 2).mean()):.0%} of the canvas "
          f"by more than two 8-bit levels of value and {float((moved > 8).mean()):.0%} by "
          f"more than eight; in the export's colour, any channel, "
          f"{float((colour > 2).mean()):.0%} and {float((colour > 8).mean()):.0%}")


# -- running it ------------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    for flag, what in (("--claims", "section 3, re-measured"),
                       ("--edges", "4A: the edge candidates, and their sheets"),
                       ("--flecks", "4B: the dry-brush gates, and their sheets"),
                       ("--misfires", "4C: the narrowed rule on the four cases in hand"),
                       ("--sheet", "4D: a variant's cost, and a sheet in four processes"),
                       ("--file", "4F: the session file, saved each way"),
                       ("--shell", "4F, built: the passes through `easel run`, the file "
                                   "and `easel timelapse`, engine by engine"),
                       ("--pressure", "4G: the pressure-list fade and the wet bands"),
                       ("--corpus-edges", "4A built: the corpus's held edges, cut and "
                                          "broken, and the ground each leaves"),
                       ("--dry", "4B built: the gate as built beside 0.6.0's, the "
                                 "amounts each load lays, and their sheets"),
                       ("--corpus-dry", "4B built: every corpus painting rebuilt under "
                                        "each gate, and what moves")):
        parser.add_argument(flag, action="store_true", help=what)
    parser.add_argument("--engine", action="append", default=[], metavar="SRC",
                        help="with --shell: an engine's src directory to time, "
                             "repeatable; the checkout's own when left off")
    args = parser.parse_args(argv)
    engines = args.engine
    chosen = {k for k, v in vars(args).items() if v and k != "engine"}
    every = not chosen

    print("The lighthouse handover's round, measured. Engine "
          f"{easel.__version__} from {Path(easel.__file__).parent}")
    rb = None
    if every or chosen & {"claims", "edges", "flecks", "dry"}:
        rb = rebuild(watch=True)
    if every or "claims" in chosen:
        probe_claims(rb)
    if every or "edges" in chosen:
        rb1440 = rebuild(1440, 960, upto="p03_headland.py")
        probe_edges(rb, rb1440)
    if every or "flecks" in chosen:
        probe_flecks(rb)
    if every or "misfires" in chosen:
        probe_misfires()
    if every or "sheet" in chosen:
        probe_sheet()
    if every or "file" in chosen:
        probe_file()
    if every or "shell" in chosen:
        probe_shell(engines)
    if every or "pressure" in chosen:
        probe_pressure()
    if every or "corpus_edges" in chosen:
        probe_corpus_edges()
    if every or "dry" in chosen:
        probe_dry(rb)
    if every or "corpus_dry" in chosen:
        probe_corpus_dry()
    print("\nThe numbers above are the ones CALIBRATION.md quotes under *The lighthouse "
          "handover's round*.\nThe sheets under out/handover/ are what decides the plan's "
          "question 2.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
