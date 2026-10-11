"""The measurements behind The Curator's rows -- step 2b of ``PLAN-0.9.0.md``.

A second painter joined 0.9.0's round: nine pieces of interim art for the owner's game,
one seeded script per piece at the slot's own size, three of them cut out afterwards by
scripts the painter wrote. Its verdict and answers added five workstreams to the plan:
an export with an alpha (K), a warm grey (L), how a mark deposits (M), a piece that is
one layer of a scene (N), and the check where a script already stops (O). **Every one of
those is a candidate until this script has measured it** -- ``LESSONS.md``'s first rule.

Each piece is rebuilt by running its own script, as its painter ran it, in a scratch
copy of its folder: its ``Session`` line is the one it typed, and a stage argument of
``99`` writes what shipped. Every candidate is patched in for the length of one bench
and never into the engine. The corpus benches reuse ``probe_cohort_session.py``'s
harness, with checks of their own in place of its candidates.

    python scripts/probe_curator_session.py              # every flag below
    python scripts/probe_curator_session.py --claims     # the nine rebuilt, against their PNGs
    python scripts/probe_curator_session.py --alpha      # K: export(alpha=), against its cuts
    python scripts/probe_curator_session.py --deposit    # M: the candle at 1x, 2x, 4x
    python scripts/probe_curator_session.py --layer      # N: the nine checklists, key= and cut=
    python scripts/probe_curator_session.py --grey       # L1: the fact at mix(), over the corpus
    python scripts/probe_curator_session.py --faint      # O3, M2: faint marks, under the cliff
    python scripts/probe_curator_session.py --corpus     # the corpus replay alone, kept

``--grey`` and ``--faint`` read one replay of every committed painting with the canvas
kept around each hand-laid mark, about twenty-five minutes, kept in
``out/curator/corpus.pkl`` until ``--corpus`` asks for another or the engine is a release
other than the one that replayed it. ``--claims`` runs the nine once, about five minutes,
and ``--alpha``, ``--deposit`` and ``--layer`` reuse those runs. Pictures go to
``out/curator/``.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import math
import pickle
import re
import shutil
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

import probe_bell_session as bell  # noqa: E402
import probe_cohort_session as cohort  # noqa: E402

import easel  # noqa: E402
import easel.palette as palette_module  # noqa: E402
import easel.session as session_module  # noqa: E402
from easel import Session, checklist  # noqa: E402
from easel.color import linear_to_oklab, linear_to_srgb, parse_color  # noqa: E402
from easel.look import label_sheet  # noqa: E402
from easel.measure import VALUE_THRESHOLD  # noqa: E402
from easel.plan import read_place  # noqa: E402
from easel.regions import Polygon, polygon  # noqa: E402
from easel.stroke import catmull_rom  # noqa: E402

CURATOR = ROOT / "paintings" / "Claude" / "the_curator"
OUT = ROOT / "out" / "curator"
heading = bell.heading
table = bell.table
pct = bell.pct


@dataclass(frozen=True)
class Piece:
    """One of the nine, as its painter ran it."""

    name: str
    folder: str
    script: str
    argv: tuple[str, ...] = ("99",)
    export: str = ""          # the file its stage 99 writes
    cut: str = ""             # the painter's own cut-out, beside painting.png

    @property
    def path(self) -> Path:
        return CURATOR / self.folder


PIECES = (
    Piece("the room beyond", "beyond", "beyond_doorway.py", export="beyond_doorway.png"),
    Piece("the desk", "desk", "desk.py", export="desk.png"),
    Piece("the counter", "counter", "counter.py", export="counter.png"),
    Piece("the left bookcase", "shelf_left", "shelves.py", ("left", "99")),
    Piece("the right bookcase", "shelf_right", "shelves.py", ("right", "99")),
    Piece("the locked case", "locked_shelf", "locked_shelf.py"),
    Piece("the doorway wall", "wall", "doorway_wall.py", cut="doorway_wall.png"),
    Piece("the patron", "patron", "patron_default.py", cut="patron_default.png"),
    Piece("the candle", "candle", "candle.py", cut="candle.png"),
)
BY_FOLDER = {p.folder: p for p in PIECES}

#: The six whose checklists say *no clear light*, and the three that ship cut out.
DARK = ("counter", "wall", "locked_shelf", "patron", "shelf_left", "shelf_right")
CUT_OUT = ("wall", "patron", "candle")


def save_sheet(panels: list[tuple[str, Image.Image]], name: str,
               columns: int | None = None) -> Path:
    """Panels side by side, each labelled, into ``out/curator/``."""
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    label_sheet(panels, columns=columns or len(panels)).save(path)
    return path


# -- the nine, rebuilt -------------------------------------------------------------------

@dataclass
class Run:
    """One piece run once: its session, what it printed, and what it wrote."""

    piece: Piece
    session: Session
    printed: str
    files: dict[str, bytes]
    seconds: float
    scale: int = 1
    notices: list[str] = field(default_factory=list)   # what the engine warned, at the call

    @property
    def checklist(self) -> list[str]:
        """The closing checklist, as the script printed it."""
        lines = self.printed.splitlines()
        start = next((i for i, line in enumerate(lines)
                      if line.startswith("checklist for this painting")), None)
        if start is None:
            return []
        out = []
        for line in lines[start:]:
            if line.startswith("three this cannot answer"):
                break
            out.append(line)
        return [line for line in out if line.strip()]

    def line(self, word: str) -> str:
        """The checklist's line that opens with ``word``."""
        return next((line.strip() for line in self.checklist
                     if line.strip().startswith(word)), "")

    def rgb(self) -> np.ndarray:
        return self.session.canvas.to_srgb8(impasto=True, sketch=True)


@contextlib.contextmanager
def _caught_session(made: list, plan_extra: dict | None = None):
    """Every ``Session`` the script builds, kept; ``plan_extra`` added to its plan."""
    init, plan, look = Session.__init__, Session.plan, Session.look

    def keeping(self, *args, **kw):
        kw["timelapse"] = False
        init(self, *args, **kw)
        made.append(self)

    def planning(self, *args, **kw):
        return plan(self, *args, **{**kw, **(plan_extra or {})})

    Session.__init__ = keeping
    Session.plan = planning
    Session.look = lambda self, *a, **k: "(look skipped by the probe)"
    try:
        yield
    finally:
        Session.__init__, Session.plan, Session.look = init, plan, look


def run_piece(piece: Piece, scale: int = 1, plan_extra: dict | None = None) -> Run:
    """Run one piece's script at stage 99 in a scratch copy of its folder.

    ``scale`` paints it at that many times its canvas, as its painter did for the candle
    in its answer 3: the ``Session`` line alone changed, so every coordinate, size and
    seed is the same. ``plan_extra`` is added to its ``s.plan()``.
    """
    made: list[Session] = []
    with tempfile.TemporaryDirectory(prefix=f"curator-{piece.folder}-") as tmp:
        work = Path(tmp)
        for path in piece.path.glob("*.py"):
            shutil.copy2(path, work / path.name)
        script = work / piece.script
        source = script.read_text(encoding="utf-8")
        if scale != 1:
            source, count = re.subn(r"^s = Session\(([^,]+), ([^,]+), ",
                                    rf"s = Session((\1) * {scale}, (\2) * {scale}, ",
                                    source, flags=re.M)
            assert count == 1, f"{piece.script}: no Session line to scale"
        here, argv = Path.cwd(), sys.argv
        printed = io.StringIO()
        started = time.time()
        try:
            import os
            os.chdir(work)
            sys.argv = [str(script), *piece.argv]
            with _caught_session(made, plan_extra), contextlib.redirect_stdout(printed), \
                    warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                exec(compile(source, str(script), "exec"),                     # noqa: S102
                     {"__name__": "__main__", "__file__": str(script)})
        finally:
            os.chdir(here)
            sys.argv = argv
        seconds = time.time() - started
        files = {p.name: p.read_bytes() for p in work.iterdir()
                 if p.suffix in (".png", ".json")}
    notices = [str(w.message) for w in caught if issubclass(w.category, UserWarning)]
    return Run(piece, made[-1], printed.getvalue(), files, seconds, scale, notices)


_RUNS: dict[str, Run] = {}


def rebuilt(folder: str) -> Run:
    """Each piece run once at its own size, and kept for every bench that reads it."""
    if folder not in _RUNS:
        _RUNS[folder] = run_piece(BY_FOLDER[folder])
    return _RUNS[folder]


def probe_claims() -> None:
    """The nine rebuilt, against the PNG each folder ships, and their spend."""
    heading("the nine, rebuilt at stage 99 against painting.png")
    print(f"  engine {easel.__version__}, on {sys.platform}")
    rows = []
    for piece in PIECES:
        run = rebuilt(piece.folder)
        shipped = np.asarray(Image.open(piece.path / "painting.png").convert("RGB"),
                             dtype=np.int16)
        ours = run.rgb().astype(np.int16)
        differ = np.abs(ours - shipped).max(axis=2)
        s = run.session
        rows.append([piece.name, f"{s.canvas.width}x{s.canvas.height}",
                     f"{s.stroke_count} of {s.budget}", int((differ > 0).sum()),
                     int(differ.max()), len(run.notices), f"{run.seconds:.1f} s"])
    print(table(rows, ["piece", "canvas", "spent", "pixels that differ", "by at most",
                       "notices at the call", "run"]))
    for piece in PIECES:
        for notice in rebuilt(piece.folder).notices:
            print(f"    {piece.folder}: {notice[:110]}")


# -- K: an export with an alpha ----------------------------------------------------------

def _outlines(run: Run) -> dict[str, list]:
    """The pixel outlines the painting script wrote for its cut script to read back."""
    import json
    return json.loads(run.files["outline.json"])


#: The arch the wall's cut removes, as ``cut_arch.py`` types it a second time.
ARCH = {"cx": 960, "cy": 400, "r": 260, "bottom": 720}


def arch_polygon(w: int, h: int, steps: int = 96) -> Polygon:
    """The arch's opening, as a shape: a half circle over a rectangle to the floor."""
    cx, cy, r, bottom = ARCH["cx"], ARCH["cy"], ARCH["r"], ARCH["bottom"] + 10
    top = [(cx + r * math.cos(math.pi + math.pi * k / steps),
            cy + r * math.sin(math.pi + math.pi * k / steps)) for k in range(steps + 1)]
    pts = top + [(cx + r, bottom), (cx - r, bottom)]
    return polygon([(x / w, y / h) for x, y in pts], name="arch")


def cut_places(run: Run) -> tuple[list[Polygon], bool]:
    """The places a piece is cut along, as shapes, and whether the cut keeps them (False
    for the wall, whose cut is a hole)."""
    s = run.session
    w, h = s.canvas.width, s.canvas.height
    k = run.scale
    if run.piece.folder == "wall":
        return [arch_polygon(w // k, h // k)], False
    return [polygon([(x / (w / k), y / (h / k)) for x, y in pts], name=name)
            for name, pts in sorted(_outlines(run).items())], True


def alpha_candidate(places: list[Polygon], keep: bool, w: int, h: int,
                    soften: float = 0.0, samples: int = 2) -> np.ndarray:
    """K's candidate: the alpha as the coverage of the places, antialiased as a hold's mask
    is (``Polygon.coverage``, what ``edge="hard"`` clips against, at two samples a side,
    five levels); the union by the greater coverage. ``samples`` raises the levels, and
    ``soften`` is a Gaussian's sigma in pixels, the painter's option."""
    cover = np.zeros((h, w), dtype=np.float32)
    for place in places:
        cover = np.maximum(cover, place.coverage(w, h, samples=samples))
    alpha = cover if keep else 1.0 - cover
    if soften > 0.0:
        img = Image.fromarray((alpha * 255.0 + 0.5).astype(np.uint8))
        alpha = np.asarray(img.filter(ImageFilter.GaussianBlur(soften)),
                           dtype=np.float32) / 255.0
    return alpha


def painters_cut(run: Run, places_px: dict[str, list] | None, blur: float) -> np.ndarray:
    """The painter's own cut, rebuilt: its polygons drawn at 4x, reduced, blurred."""
    s = run.session
    w, h = s.canvas.width, s.canvas.height
    k = 4
    if run.piece.folder == "wall":
        mask = Image.new("L", (w * k, h * k), 255)
        d = ImageDraw.Draw(mask)
        cx, cy, r, bottom = ARCH["cx"], ARCH["cy"], ARCH["r"], ARCH["bottom"]
        d.ellipse([(cx - r) * k, (cy - r) * k, (cx + r) * k, (cy + r) * k], fill=0)
        d.rectangle([(cx - r) * k, cy * k, (cx + r) * k, (bottom + 10) * k], fill=0)
        mask = mask.resize((w, h), Image.LANCZOS)
    else:
        mask = Image.new("L", (w * k, h * k), 0)
        d = ImageDraw.Draw(mask)
        for name in sorted(places_px):
            d.polygon([(x * k, y * k) for x, y in places_px[name]], fill=255)
        mask = mask.resize((w, h), Image.LANCZOS)
        if blur:
            mask = mask.filter(ImageFilter.GaussianBlur(blur))
    return np.asarray(mask, dtype=np.float32) / 255.0


def edge_width(alpha: np.ndarray, places_px: list[list] | None = None,
               perimeter: float | None = None) -> tuple[float, float]:
    """The edge's 10-90% width, two ways: the band of pixels between 10% and 90% over the
    outline's length (the painter's ``edges.py``), and the median of the rise along rows
    crossing a side (``held.py``'s width profile)."""
    band = float(((alpha >= 0.1) & (alpha <= 0.9)).sum())
    per_length = band / perimeter if perimeter else float("nan")
    widths = []
    h, w = alpha.shape
    for y in range(h):
        row = alpha[y]
        part = np.nonzero((row > 0.02) & (row < 0.98))[0]
        if not len(part):
            continue
        for x0 in (part[0], part[-1]):
            lo, hi = max(0, x0 - 6), min(w, x0 + 7)
            seg = row[lo:hi]
            if seg[0] > seg[-1]:
                seg = seg[::-1]
            if seg[0] > 0.05 or seg[-1] < 0.95:
                continue
            a = _crossing(seg, 0.1)
            b = _crossing(seg, 0.9)
            if a is not None and b is not None:
                widths.append(b - a)
    return per_length, (float(np.median(widths)) if widths else float("nan"))


def _crossing(seg: np.ndarray, level: float) -> float | None:
    for i in range(len(seg) - 1):
        if seg[i] < level <= seg[i + 1]:
            return i + (level - seg[i]) / (seg[i + 1] - seg[i])
    return None


def _perimeter(points: list) -> float:
    return sum(math.dist(points[i], points[(i + 1) % len(points)])
               for i in range(len(points)))


def _union_perimeter(alpha: np.ndarray) -> float:
    """The outline's length in pixels, off the alpha itself: half-level crossings
    between neighbours, horizontal and vertical, weighted for the diagonals by the
    usual pi/4. Good to a few percent, and the same instrument for every candidate."""
    inside = alpha >= 0.5
    cross = (np.count_nonzero(inside[:, 1:] != inside[:, :-1])
             + np.count_nonzero(inside[1:, :] != inside[:-1, :]))
    return cross * math.pi / 4.0


def _soften_for(target: float, places: list[Polygon], keep: bool, w: int, h: int,
                perimeter: float) -> tuple[float, float]:
    """The Gaussian sigma that makes the candidate's edge ``target`` px, by bisection."""
    lo, hi = 0.0, 3.0
    for _ in range(18):
        mid = (lo + hi) / 2.0
        width = edge_width(alpha_candidate(places, keep, w, h, mid), None, perimeter)[1]
        lo, hi = (mid, hi) if width < target else (lo, mid)
    return (lo + hi) / 2.0, edge_width(alpha_candidate(places, keep, w, h, (lo + hi) / 2.0),
                                       None, perimeter)[1]


def _over(rgb: np.ndarray, alpha: np.ndarray, ground: tuple[int, int, int]) -> Image.Image:
    a = alpha[..., None]
    out = rgb.astype(np.float32) * a + np.asarray(ground, dtype=np.float32) * (1.0 - a)
    return Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8))


#: Two grounds a sprite is laid over: a doorway's light (the patron stands against it)
#: and a dark wall's.
GROUNDS = {"light": (196, 178, 140), "dark": (52, 44, 38)}


def probe_alpha() -> None:
    """K: the alpha from the places, against the painter's cuts, on the three cut-outs."""
    heading("K: export(alpha=place) against the painter's own cuts")
    rows = []
    sheets = []
    for folder in CUT_OUT:
        run = rebuilt(folder)
        s = run.session
        w, h = s.canvas.width, s.canvas.height
        places, keep = cut_places(run)
        px = None if folder == "wall" else _outlines(run)
        shipped = np.asarray(Image.open(run.piece.path / run.piece.cut).convert("RGBA"),
                             dtype=np.float32)[..., 3] / 255.0
        blur = 0.0 if folder == "wall" else 0.8
        theirs = painters_cut(run, px, blur)
        ours = alpha_candidate(places, keep, w, h)
        perimeter = _union_perimeter(ours)
        fine = alpha_candidate(places, keep, w, h, samples=4)
        sigma, reached = _soften_for(2.5, places, keep, w, h, perimeter)
        soft = alpha_candidate(places, keep, w, h, sigma)
        same = np.abs(theirs - shipped) * 255.0
        for label, alpha in (("shipped", shipped), ("the painter's cut, rebuilt", theirs),
                             ("candidate, as a hold", ours),
                             ("candidate, 4x4 samples", fine),
                             (f"candidate, soften={sigma:.2f}", soft)):
            band, rise = edge_width(alpha, None, perimeter)
            diff = np.abs(alpha - shipped) * 255.0
            rows.append([run.piece.name, label, f"{band:.2f}", f"{rise:.2f}",
                         int((diff > 1.0).sum()), int((diff > 25.5).sum()),
                         f"{float((alpha > 0.5).mean()):.1%}"])
        print(f"  {run.piece.name}: the painter's cut rebuilt against the shipped alpha: "
              f"{int((same > 1.0).sum())} pixels differ by over one level; outline "
              f"{perimeter:.0f} px; soften={sigma:.2f} px of sigma gives a "
              f"{reached:.2f} px edge")
        rgb = run.session.canvas.to_srgb8(impasto=True, sketch=True)
        box = _sheet_box(folder, w, h)
        for ground, colour in GROUNDS.items():
            for label, alpha in (("painter", shipped), ("hold", ours), ("2.5 px", soft)):
                img = _over(rgb, alpha, colour).crop(box)
                img = img.resize((img.width * 4, img.height * 4), Image.NEAREST)
                sheets.append((f"{folder} {label} on {ground}", img))
    print(table(rows, ["piece", "alpha", "10-90% band / length", "10-90% across a side",
                       "px over 1 level from shipped", "over 10%", "kept"]))
    print("  *band / length* is the painter's edges.py: pixels between 10% and 90% over the "
          "outline's length. *Across a side* interpolates linearly along rows, so a step "
          "made in one pixel reads 1.6 on it, whatever its levels.")
    print(f"  sheet: {save_sheet(sheets, 'alpha.png', columns=6)}")
    print("  The places are the painter's own outlines (outline.json) and the arch as "
          "cut_arch.py types it; the hole is one minus the arch's coverage, which is "
          "difference()'s job (4A).")


def _sheet_box(folder: str, w: int, h: int) -> tuple[int, int, int, int]:
    """A stretch of each outline worth looking at 4x: a shoulder, the wax's top, a jamb."""
    if folder == "patron":
        return (60, 200, 160, 300)
    if folder == "candle":
        return (20, 10, 100, 70)
    return (660, 360, 760, 460)


# -- M: how a mark deposits, and the canvas's size ----------------------------------------

#: Where a hand-laid mark stops landing in one touch, in pixels across: a round tip's
#: one-touch dab cliff (``session._DAB_CLIFF_PX``) and an oriented tip's floor
#: (``session._CHISEL_MIN_PX``). The candidate M2 reads a stroke against the first.
ROUND_TIPS = ("round_hard", "round_soft")
CHISELS = session_module._CHISEL_TIPS


def landing_px(tip: str) -> float | None:
    """The width under which a hand-laid mark of ``tip`` is under its cliff."""
    if tip in CHISELS:
        return session_module._CHISEL_MIN_PX
    return session_module._dab_cliff(tip, 1)


#: The candle's wax top and interior, in its own 120x300 pixels: the painter's measure
#: (``compare4x.py``, y 30-80, x 45-75 inside the cut) and a flat stretch of the body to
#: read the weave on.
WAX_TOP = (slice(30, 80), slice(45, 75))
WAX_BODY = (slice(90, 220), slice(50, 64))
BRASS_BASE = (slice(266, 288), slice(38, 82))


def _values(rgb8: np.ndarray) -> np.ndarray:
    return (rgb8.astype(np.float32) / 255.0) @ np.asarray([0.2126, 0.7152, 0.0722],
                                                          dtype=np.float32)


def _highpass(view: np.ndarray, radius: float = 2.0) -> np.ndarray:
    """What a 2 px Gaussian leaves: the weave and the bristle, not the form."""
    img = Image.fromarray(np.clip(view * 255.0, 0, 255).astype(np.uint8))
    smooth = np.asarray(img.filter(ImageFilter.GaussianBlur(radius)),
                        dtype=np.float32) / 255.0
    return view - smooth


def reduced(run: Run, size: tuple[int, int], how: str = "lanczos") -> np.ndarray:
    """A run's export brought to ``size``: by Lanczos on the sRGB (the painter's), or by a
    box mean in linear light (what the engine's own thumbnails do)."""
    if how == "lanczos":
        img = Image.fromarray(run.rgb()).resize(size, Image.LANCZOS)
        return np.asarray(img)
    canvas = run.session.canvas
    k = run.scale
    full = canvas.composite(impasto=True, sketch=True)
    h, w = size[1] * k, size[0] * k
    small = full[:h, :w].reshape(size[1], k, size[0], k, 3).mean(axis=(1, 3))
    return (linear_to_srgb(small) * 255.0 + 0.5).astype(np.uint8)


def probe_deposit() -> None:
    """M: the candle at one, two and four times its canvas, and reduced to its size."""
    heading("M: the candle painted at 1x, 2x and 4x, exported at 120x300")
    one = rebuilt("candle")
    size = (one.session.canvas.width, one.session.canvas.height)
    places, keep = cut_places(one)
    alpha = alpha_candidate(places, keep, *size) >= 0.5
    runs = {1: one, 2: run_piece(BY_FOLDER["candle"], scale=2),
            4: run_piece(BY_FOLDER["candle"], scale=4)}

    # What the painter called the weave: the 1x painting's finest texture. Asked first
    # whether it is the canvas's tooth -- the field that gates deposition -- because a
    # candidate that lays the exported size's tooth back is only worth building if so.
    from easel.canvas import _TOOTH_GRAIN_W, _TOOTH_HEIGHT_W
    c = one.session.canvas
    gate = (c.height_map * _TOOTH_HEIGHT_W + c.grain * _TOOTH_GRAIN_W).astype(np.float32)
    v1 = _values(one.rgb())
    v4 = _values(reduced(runs[4], size, "box"))
    rows = []
    for label, region in (("the wax's body", WAX_BODY), ("the brass base", BRASS_BASE)):
        for radius in (0.7, 2.0):
            h1, h4 = _highpass(v1, radius)[region], _highpass(v4, radius)[region]
            g = _highpass(gate, radius)[region]
            hm = _highpass(c.height_map.astype(np.float32), radius)[region]
            rows.append([label, f"{radius:g} px", f"{h1.std() * 255:.1f}",
                         f"{h4.std() * 255:.1f}",
                         f"{np.corrcoef(h1.ravel(), hm.ravel())[0, 1]:+.2f}",
                         f"{np.corrcoef(h1.ravel(), g.ravel())[0, 1]:+.2f}"])
    print(table(rows, ["where", "high-pass", "1x sd, levels", "4x reduced sd",
                       "1x against the height map", "against the gate"]))
    body = v1[90:220, 50:64] - v1[90:220, 50:64].mean()
    body4 = v4[90:220, 50:64] - v4[90:220, 50:64].mean()
    spec1 = np.abs(np.fft.rfft(body, axis=0)).mean(axis=1) * 255 / 130
    spec4 = np.abs(np.fft.rfft(body4, axis=0)).mean(axis=1) * 255 / 130
    print("  the body's texture down its length, by period (px): amplitude at 1x / 4x "
          "reduced: " + ", ".join(f"{130 / k:.1f}: {spec1[k]:.2f}/{spec4[k]:.2f}"
                                  for k in (20, 30, 40, 50, 60)))

    rows = []
    panels = []
    grey = (96, 92, 88)
    for k, run in runs.items():
        variants = [("as painted", run.rgb())] if k == 1 else [
            ("lanczos", reduced(run, size, "lanczos")),
            ("box, linear", reduced(run, size, "box"))]
        lines = {w: run.line(w) for w in ("plan:", "lightest:")}
        for label, rgb in variants:
            v = _values(rgb)
            top = v[WAX_TOP][alpha[WAX_TOP]]
            weave = float(np.std(_highpass(v, 0.7)[BRASS_BASE]))
            rows.append([f"{k}x", label, f"{run.seconds:.1f} s", run.session.stroke_count,
                         f"{top.mean():.2f}", f"{np.percentile(top, 95):.2f}",
                         f"{weave * 255:.1f}"])
            img = _over(rgb, alpha.astype(np.float32), grey)
            panels.append((f"{k}x {label}", img.resize((img.width * 3, img.height * 3),
                                                       Image.NEAREST)))
        print(f"  {k}x: {lines['plan:']}")
        print(f"      {lines['lightest:']}")
        under = [r for r in _hand_marks(run.session) if r[1] is not None and r[0] < r[1]]
        print(f"      hand-laid marks under their one-touch width: {len(under)} of "
              f"{len(_hand_marks(run.session))}")
    print(table(rows, ["canvas", "export", "run", "spent", "wax top mean", "95th",
                       "base's finest texture (sd)"]))
    print(f"  sheet: {save_sheet(panels, 'deposit.png', columns=len(panels))}")


def _hand_marks(session: Session) -> list[tuple[float, float | None]]:
    """``(pixels across, its tip's landing width)`` for every mark laid by hand."""
    long = float(session.canvas.long_side)
    out = []
    for r in session.history.records:
        if r.kind != "stroke" or (r.params or {}).get("via") or r.note == "signature":
            continue
        tip = str((r.params or {}).get("tip", ""))
        out.append((float((r.params or {}).get("size", 0.0)) * long, landing_px(tip)))
    return out


# -- N: a piece that is one layer of a scene -----------------------------------------------

def _edges_inside(view: np.ndarray, inside: np.ndarray) -> tuple[float, float, int]:
    """``checklist.edges_line``'s measure, counting only ridges whose whole nine-pixel
    walk stays inside the cut: an edge of the picture, not the cut's own."""
    view = np.asarray(view, dtype=np.float32)
    dy, dx = np.gradient(view)
    grad = np.hypot(dx, dy)
    height, width = view.shape
    ux, uy = dx / np.maximum(grad, 1e-6), dy / np.maximum(grad, 1e-6)
    rows, cols = np.mgrid[0:height, 0:width]

    def along(field_, t, r=None, c=None):
        gr, gc = (rows, cols) if r is None else (r, c)
        uyt, uxt = (uy, ux) if r is None else (uy[r, c], ux[r, c])
        return field_[np.clip((gr + uyt * t).astype(int), 0, height - 1),
                      np.clip((gc + uxt * t).astype(int), 0, width - 1)]

    ridge = (grad >= along(grad, 1.0)) & (grad >= along(grad, -1.0)) & (grad > 1e-4)
    r, c = np.nonzero(ridge)
    walk = np.stack([along(inside.astype(np.float32), float(t), r, c)
                     for t in np.arange(-4, 5)])
    held = walk.min(axis=0) > 0.5
    r, c = r[held], c[held]
    if not len(r):
        return float("nan"), float("nan"), 0
    samples = np.stack([along(view, float(t), r, c) for t in np.arange(-4, 5)])
    step = samples.max(axis=0) - samples.min(axis=0)
    keep = step >= VALUE_THRESHOLD
    if not keep.any():
        return float("nan"), float("nan"), 0
    rise = np.clip(step[keep] / np.maximum(grad[r, c][keep], 1e-6), 0.5, 12.0)
    return (float((rise < checklist.HARD_EDGE_PX).mean()), float(np.median(rise)),
            int(keep.sum()))


def lines_inside(run: Run, alpha: np.ndarray, key: str = "") -> list[str]:
    """N's candidate: the standing lines read inside the cut, and one for the cut's edge.

    The cut is where the alpha is over half. Each line is the engine's own arithmetic on
    the pixels inside it: ``plan:`` and ``lightest:`` on each place clipped to the cut,
    ``values:`` on the cut's pixels with the light against the rest *of the cut*,
    ``edges:`` on ridges whose walk stays inside, ``ground:`` through
    ``ground_showing(where=)``, ``boxes:`` without the background clause. ``cut:`` is the
    alpha's own 10-90% width against the picture's median edge."""
    s = run.session
    plan = s._plan
    w, h = s.canvas.width, s.canvas.height
    inside = alpha >= 0.5
    pv = s._value_view()
    lines = []
    if plan.values:
        out, total = [], 0
        for place in plan.values:
            if place.value is None:
                continue
            mask = place.outline.mask(w, h) & inside
            if not mask.any():
                out.append(f"{place.name} wholly outside the cut")
                continue
            total += 1
            got = read_place(pv[mask])
            delta = got.median - float(place.value)
            if abs(delta) > VALUE_THRESHOLD:
                out.append(f"{place.name} {delta:+.2f}")
        lines.append(f"plan: {total - len([o for o in out if 'outside' not in o])} of "
                     f"{total} places inside {VALUE_THRESHOLD:.2f}"
                     + (f"; {'; '.join(out)}" if out else ""))
    light = None
    if plan.lightest is not None:
        mask = plan.lightest.outline.mask(w, h) & inside
        rest = pv[inside & ~plan.lightest.outline.mask(w, h)]
        if mask.any() and rest.size:
            light = (plan.lightest.name, read_place(pv[mask]).brightest,
                     float(np.percentile(rest, 95)))
            lines.append(f"lightest: {plan.lightest.name} {light[1]:.2f} at its brightest "
                         f"twentieth inside the cut, against {light[2]:.2f} for the rest "
                         f"of the cut ({float(mask.sum()) / plan.lightest.outline.mask(w, h).sum():.0%} "
                         f"of the place is inside)")
    view = s.canvas.values(sketch=False).astype(np.float32) / 255.0
    reach = (s.palette.darkest_value, s.palette.lightest_value)
    keyed = key or plan.key
    lines.append(checklist.values_line(view[inside], reach=reach, key=keyed,
                                       light=light if keyed == "low" else None))
    share, median, n = _edges_inside(view, inside)
    lines.append(f"edges: {share:.0%} of edges are under {checklist.HARD_EDGE_PX:.1f} px "
                 f"wide, median {median:.1f} px ({n} ridge pixels inside)")
    bare = s.canvas.ground_showing(where=inside)
    lines.append(f"ground: {bare:.2%} of the cut is still bare ground")
    boxed, masses = checklist.mass_counts(s.history.records)
    lines.append(f"boxes: {boxed} of {masses} masses were laid in a rectangle")
    cut_width, _rise = edge_width(alpha, None, _union_perimeter(alpha))
    lines.append(f"cut: the cut's edge is {cut_width:.1f} px (10-90%, band over length), "
                 f"against the "
                 f"picture's median edge {median:.1f} px")
    if bare < session_module._GROUND_FLOOR:
        lines[-3] += (f" -- under {session_module._GROUND_FLOOR:.1%}, and the checklist "
                      "asks for some")
    return lines


def probe_layer() -> None:
    """N: the nine checklists as shipped, under ``key="low"``, and read inside the cut."""
    heading("N: the nine checklists, as shipped")
    for piece in PIECES:
        run = rebuilt(piece.folder)
        print(f"  {piece.name}:")
        for word in ("plan:", "lightest:", "values:", "edges:", "ground:"):
            if run.line(word):
                print(f"    {run.line(word)}")
        found = [line.strip() for line in run.checklist if line.strip().startswith("- ")]
        for line in found:
            print(f"    {line[:150]}")

    heading("N: the six dark pieces under plan(key=\"low\")")
    for folder in DARK:
        run = run_piece(BY_FOLDER[folder], plan_extra={"key": "low"})
        print(f"  {run.piece.name}: {run.line('values:')}")

    heading("N: the three cut-outs, read inside the cut (the candidate's alpha)")
    for folder in CUT_OUT:
        run = rebuilt(folder)
        s = run.session
        places, keep = cut_places(run)
        alpha = alpha_candidate(places, keep, s.canvas.width, s.canvas.height)
        print(f"  {run.piece.name}: the cut keeps {float((alpha >= 0.5).mean()):.1%} of "
              f"the canvas")
        for line in lines_inside(run, alpha):
            print(f"    {line}")
        if folder in DARK:
            print(f"    under key=\"low\": {lines_inside(run, alpha, key='low')[2]}")
        found = [line.strip() for line in run.checklist if line.strip().startswith("- ")]
        if found:
            print("    the closing audit's findings, and how much of their marks lie "
                  "outside the cut:")
            for line in found:
                print(f"      {line[:140]}")
            _outside(run, alpha)


def _outside(run: Run, alpha: np.ndarray) -> None:
    """How many of the hand-laid marks lie mostly outside the cut, and which lines."""
    s = run.session
    w, h = s.canvas.width, s.canvas.height
    out = []
    for r in s.history.records:
        if r.kind != "stroke" or (r.params or {}).get("via"):
            continue
        pts = np.asarray(r.points, dtype=np.float32).reshape(-1, 2)
        xs = np.clip((pts[:, 0] * (w - 1)).round().astype(int), 0, w - 1)
        ys = np.clip((pts[:, 1] * (h - 1)).round().astype(int), 0, h - 1)
        if float((alpha[ys, xs] >= 0.5).mean()) < 0.5:
            out.append(r)
    hand = sum(1 for r in s.history.records
               if r.kind == "stroke" and not (r.params or {}).get("via"))
    print(f"      {len(out)} of {hand} hand-laid marks lie mostly outside it"
          + (": " + ", ".join(f"#{r.index} {r.brush}" for r in out[:8]) if out else ""))


# -- the corpus, replayed once for L1, O3 and M2 -------------------------------------------

CACHE = OUT / "corpus.pkl"


@dataclass
class Kept:
    """What one replay of the corpus kept: every mixture typed, every mark laid by hand."""

    mixes: list[dict] = field(default_factory=list)
    marks: list[dict] = field(default_factory=list)
    spent: dict[str, int] = field(default_factory=dict)
    errors: dict[str, list[str]] = field(default_factory=dict)
    engine: str = ""


_KEEPING: list[Kept] = []
_PAINTING: list[str] = [""]


def _from_painter() -> bool:
    """Whether the frame that called ``mix`` is outside the engine: ``at_value`` and
    ``tint`` mix too, and the fact L1 proposes is for the mixture a painter typed."""
    return not _engine(sys._getframe(2).f_code.co_filename)


def _engine(filename: str) -> bool:
    name = filename.replace("\\", "/")
    return "/src/easel/" in name or "/site-packages/easel/" in name


@contextlib.contextmanager
def keeping_mixes():
    """``Palette.mix``, recording each two-colour mixture a painter's script typed."""
    original = palette_module.Palette.mix

    def mix(self, a, b, ratio=0.5):
        out = original(self, a, b, ratio)
        if _KEEPING and _from_painter():
            try:
                pa = parse_color(self._resolve(a))
                pb = parse_color(self._resolve(b))
            except Exception:                                    # noqa: BLE001 - kept out
                return out
            line = 0
            frame = sys._getframe(1)
            while frame is not None:
                if not _engine(frame.f_code.co_filename):
                    line = frame.f_lineno
                    break
                frame = frame.f_back
            _KEEPING[0].mixes.append({
                "painting": _PAINTING[0], "a": _name(a), "b": _name(b),
                "ratio": float(ratio), "pa": np.asarray(pa, dtype=np.float64),
                "pb": np.asarray(pb, dtype=np.float64),
                "out": np.asarray(parse_color(out), dtype=np.float64), "line": line})
        return out

    palette_module.Palette.mix = mix
    try:
        yield
    finally:
        palette_module.Palette.mix = original


def _name(color) -> str:
    return color if isinstance(color, str) else "(a mixture)"


def _footprint(r, canvas, grow: float = 0.0) -> tuple[np.ndarray, tuple[int, int, int, int]]:
    """Where a hand-laid mark's path runs, at its full width: ``(mask, box)``."""
    w, h = canvas.width, canvas.height
    width = float((r.params or {}).get("size", 0.0)) * float(canvas.long_side) + grow
    pts = np.asarray(r.points, dtype=np.float32).reshape(-1, 2)
    if len(pts) >= 3 and (r.params or {}).get("smooth", True):
        pts = catmull_rom(pts)
    px = np.stack([pts[:, 0] * (w - 1), pts[:, 1] * (h - 1)], axis=1)
    reach = width / 2.0 + 2.0
    x0 = max(0, int(math.floor(px[:, 0].min() - reach)))
    y0 = max(0, int(math.floor(px[:, 1].min() - reach)))
    x1 = min(w, int(math.ceil(px[:, 0].max() + reach)) + 1)
    y1 = min(h, int(math.ceil(px[:, 1].max() + reach)) + 1)
    if x1 <= x0 or y1 <= y0:
        return np.zeros((0, 0), dtype=bool), (0, 0, 0, 0)
    img = Image.new("L", (x1 - x0, y1 - y0), 0)
    d = ImageDraw.Draw(img)
    local = [(float(x - x0), float(y - y0)) for x, y in px]
    rad = max(width / 2.0, 0.5)
    if len(local) > 1:
        d.line(local, fill=255, width=max(1, int(round(width))))
    for x, y in (local[0], local[-1]):
        d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=255)
    return np.asarray(img) > 0, (x0, y0, x1, y1)


def _faint_call(call, ctx) -> None:
    """A CALL_CHECKS entry: every hand-laid mark, with what it moved under its path.

    Kept, not judged: the thresholds are chosen afterwards from what was kept. ``reach``
    is how far toward its own colour the mark moved the canvas under its path, its
    90th percentile over the path's pixels -- ``(after - before) / (colour - before)``
    -- so a mark that left the canvas where it was reads 0 and one that covered it 1."""
    if not _KEEPING or call.verb not in ("stroke", "dab"):
        return None
    s = ctx.session
    canvas = s.canvas
    for r in ctx.records:
        if r.kind != "stroke" or (r.params or {}).get("via"):
            continue
        params = r.params or {}
        colour = s.palette.value_of(r.color_hex) if r.color_hex else float("nan")
        mask, (x0, y0, x1, y1) = _footprint(r, canvas)
        entry = {"painting": _PAINTING[0], "line": call.line,
                 "verb": call.verb, "index": r.index, "tip": str(params.get("tip", "")),
                 "brush": r.brush, "px": float(params.get("size", 0.0))
                 * float(canvas.long_side), "long": int(canvas.long_side),
                 "canvas": (canvas.width, canvas.height),
                 "opacity": float(params.get("opacity", 1.0)),
                 "listed": not isinstance(r.pressure, str), "pressure":
                 r.pressure if isinstance(r.pressure, str) else "list",
                 "points": len(r.points), "paint": float(r.paint), "note": r.note,
                 "colour": colour, "under": float("nan"), "reach": float("nan"),
                 "moved": float("nan"), "pixels": 0}
        if mask.size and mask.any():
            before = ctx.before[y0:y1, x0:x1][mask]
            after = ctx.after[y0:y1, x0:x1][mask]
            gap = colour - before
            far = np.abs(gap) >= 0.02
            entry["under"] = float(np.median(before))
            entry["pixels"] = int(mask.sum())
            entry["moved"] = float(np.percentile(np.abs(after - before), 90) * 255.0)
            if far.any():
                toward = np.clip((after[far] - before[far]) / gap[far], -1.0, 1.5)
                entry["reach"] = float(np.percentile(toward, 90))
        _KEEPING[0].marks.append(entry)
    return None


def replay_corpus(names: tuple[str, ...] = ()) -> Kept:
    """Every committed painting rebuilt through the corpus probe's harness, the canvas kept
    around each hand-laid mark, with this probe's one check in place of its candidates."""
    kept = Kept(engine=easel.__version__)
    _KEEPING[:] = [kept]
    saved = dict(cohort.CALL_CHECKS), dict(cohort.PASS_CHECKS)
    cohort.CALL_CHECKS.clear()
    cohort.PASS_CHECKS.clear()
    cohort.CALL_CHECKS["faint"] = _faint_call
    try:
        with keeping_mixes():
            for entry in cohort.CORPUS:
                if names and entry.name not in names:
                    continue
                _PAINTING[0] = entry.name
                started = time.time()
                rep = cohort.replay(entry, keep_canvas=True)
                kept.errors[entry.name] = rep.errors
                kept.spent[entry.name] = rep.spent
                print(f"  {entry.name:<20} {rep.spent:4d} strokes, "
                      f"{time.time() - started:5.0f} s"
                      + (f"  [{'; '.join(rep.errors)[:80]}]" if rep.errors else ""),
                      flush=True)
    finally:
        cohort.CALL_CHECKS.clear()
        cohort.CALL_CHECKS.update(saved[0])
        cohort.PASS_CHECKS.clear()
        cohort.PASS_CHECKS.update(saved[1])
        _KEEPING.clear()
    return kept


def corpus(fresh: bool = False) -> Kept:
    """The corpus replay, from ``out/curator/corpus.pkl`` unless stale or asked afresh."""
    if CACHE.exists() and not fresh:
        with CACHE.open("rb") as handle:
            kept = Kept(**pickle.load(handle))
        if kept.engine == easel.__version__:
            return kept
    heading("the corpus, replayed with the canvas kept round every hand-laid mark")
    kept = replay_corpus()
    OUT.mkdir(parents=True, exist_ok=True)
    with CACHE.open("wb") as handle:
        pickle.dump(vars(kept), handle, protocol=pickle.HIGHEST_PROTOCOL)
    return kept


# -- L1: a fact at mix() --------------------------------------------------------------------

def _lab(lin: np.ndarray) -> tuple[float, float]:
    """``(chroma, hue in degrees)`` in Oklab, the engine's own ``chroma_of``."""
    lab = linear_to_oklab(np.asarray(lin, dtype=np.float32))
    return float(math.hypot(float(lab[1]), float(lab[2]))), \
        float(math.degrees(math.atan2(float(lab[2]), float(lab[1]))) % 360.0)


def _hsv_hue(lin: np.ndarray) -> float:
    """The sRGB HSV hue the filing and the painter read, in degrees."""
    r, g, b = (float(v) for v in linear_to_srgb(np.asarray(lin, dtype=np.float32)))
    hi, lo = max(r, g, b), min(r, g, b)
    if hi - lo < 1e-9:
        return float("nan")
    if hi == r:
        hue = (g - b) / (hi - lo) % 6.0
    elif hi == g:
        hue = (b - r) / (hi - lo) + 2.0
    else:
        hue = (r - g) / (hi - lo) + 4.0
    return hue * 60.0


def _turn(h1: float, h2: float) -> float:
    d = abs(h1 - h2) % 360.0
    return min(d, 360.0 - d)


#: A parent this grey or greyer has no hue to turn from: white, the blacks, the greys.
#: Under burnt umber's own ``0.020``, which is the parent the trap turns away from.
NEUTRAL_PARENT = 0.015


def l1(mix: dict, near: float, turn: float = 90.0, larger: bool = False) -> bool:
    """L1: the mixture lies within ``near`` of neutral (Oklab chroma) and its hue has
    turned more than ``turn`` degrees from every parent that has a hue -- as the plan
    words it -- or, with ``larger``, from the parent with the larger share alone."""
    chroma, hue = _lab(mix["out"])
    if chroma >= near:
        return False
    parents = [_lab(mix["pa"]), _lab(mix["pb"])]
    if larger:
        parents = [parents[0] if mix["ratio"] <= 0.5 else parents[1]]
    hued = [h for c, h in parents if c >= NEUTRAL_PARENT]
    return bool(hued) and all(_turn(hue, h) > turn for h in hued)


def probe_grey(kept: Kept) -> None:
    """L1 over every two-colour mixture the corpus's scripts typed."""
    heading("L1: the band where umber and ultramarine turn, at mix() itself")
    p = easel.Palette()
    rows = []
    for t in (0.0, 0.10, 0.18, 0.25, 0.30, 0.35, 0.50):
        lin = parse_color(p.mix("burnt_umber", "ultramarine", t))
        chroma, hue = _lab(lin)
        one = {"pa": parse_color(p["burnt_umber"]), "pb": parse_color(p["ultramarine"]),
               "out": lin, "ratio": t}
        at = parse_color(p.at_value(lin, 0.40))
        rows.append([f"{t:.2f}", f"{p.value_of(lin):.2f}", f"{chroma:.3f}", f"{hue:.0f}",
                     f"{_hsv_hue(lin):.0f}", f"{_hsv_hue(at):.0f}",
                     "yes" if l1(one, 0.03) else "",
                     "yes" if l1(one, 0.03, 60.0, larger=True) else "",
                     "yes" if l1(one, 0.03, 90.0, larger=True) else ""])
    print(table(rows, ["ultramarine", "value", "Oklab chroma", "Oklab hue", "HSV hue",
                       "HSV at 0.40", "L1 as worded", "from the larger, > 60",
                       "from the larger, > 90"]))
    print("  L1 as worded (chroma under 0.03, turned over 90 degrees from both parents) "
          "cannot fire on two pigments whose mixture's hue travels the arc between them: "
          "it is never far from the one it is travelling to")
    um, ul = (_lab(parse_color(p[n])) for n in ("burnt_umber", "ultramarine"))
    print(f"  burnt umber: chroma {um[0]:.3f}, hue {um[1]:.0f}; ultramarine: chroma "
          f"{ul[0]:.3f}, hue {ul[1]:.0f}")

    heading("L1 over the corpus's mixtures")
    mixes = kept.mixes
    paintings = sorted({m["painting"] for m in mixes})
    print(f"  {len(mixes)} two-colour mixtures typed, in {len(paintings)} paintings")
    rows = []
    for near, turn, larger in ((0.03, 90.0, False), (0.06, 90.0, False),
                               (0.02, 60.0, True), (0.03, 60.0, True), (0.04, 60.0, True),
                               (0.03, 90.0, True), (0.04, 90.0, True)):
        fired = [m for m in mixes if l1(m, near, turn, larger)]
        rows.append(["the larger" if larger else "both", f"{near:.2f}", f"{turn:.0f}",
                     len(fired), len({m['painting'] for m in fired}),
                     len({(m['painting'], m['a'], m['b'], round(m['ratio'], 3))
                          for m in fired})])
    print(table(rows, ["from", "chroma under", "turned over", "calls", "paintings",
                       "distinct mixtures"]))
    fired = [m for m in mixes if l1(m, 0.03, 60.0, larger=True)]
    seen = set()
    rows = []
    for m in fired:
        key = (m["painting"], m["a"], m["b"], round(m["ratio"], 3))
        if key in seen:
            continue
        seen.add(key)
        chroma, hue = _lab(m["out"])
        rows.append([m["painting"], m["line"], f"{m['a']} + {m['b']}", f"{m['ratio']:.2f}",
                     f"{chroma:.3f}", f"{hue:.0f}",
                     " / ".join(f"{_lab(m[k])[1]:.0f}" for k in ("pa", "pb"))])
    print(table(rows[:40], ["painting", "line", "mixture", "share", "chroma", "hue",
                            "parents' hues"]))
    if len(rows) > 40:
        print(f"  ... and {len(rows) - 40} more")
    cur = [m for m in mixes if m["painting"].startswith("curator")]
    turned = [m for m in cur if {m["a"], m["b"]} == {"burnt_umber", "ultramarine"}]
    print(f"  the Curator's: {len(cur)} mixtures typed, {len(turned)} of them umber with "
          f"ultramarine; L1 from the larger at 0.03 and 60 degrees fires on "
          f"{sum(1 for m in cur if l1(m, 0.03, 60.0, True))}, of those on "
          f"{sum(1 for m in turned if l1(m, 0.03, 60.0, True))}")
    for m in sorted(turned, key=lambda m: (m["painting"], m["ratio"])):
        chroma, hue = _lab(m["out"])
        share = m["ratio"] if m["b"] == "ultramarine" else 1.0 - m["ratio"]
        print(f"    {m['painting']}:{m['line']} ultramarine {share:.2f}: chroma "
              f"{chroma:.3f}, hue {hue:.0f}, HSV {_hsv_hue(m['out']):.0f}"
              f"{'  <- L1' if l1(m, 0.03, 60.0, True) else ''}")


# -- O3 and M2: a faint mark, and a mark under its cliff -------------------------------------

def _bucket(long: int) -> str:
    for top, label in ((400, "up to 400"), (800, "401-800"), (1200, "801-1200")):
        if long <= top:
            return label
    return "over 1200"


def faint(m: dict, far: float = 0.15, reach: float = 0.25) -> bool:
    """O3: the mark's colour lay ``far`` or more from what it landed on, and it moved the
    canvas under less than ``reach`` of the way there."""
    return (not math.isnan(m["reach"]) and abs(m["colour"] - m["under"]) >= far
            and m["reach"] < reach)


def m2(m: dict) -> bool:
    """M2: a round tip under its one-touch width, laid with a pressure list or opacity
    under 1."""
    cliff = landing_px(m["tip"])
    return (m["tip"] in ROUND_TIPS and cliff is not None and m["px"] < cliff
            and (m["listed"] or m["opacity"] < 1.0))


def probe_faint(kept: Kept) -> None:
    """O3 over the corpus's hand-laid marks, M's share under the cliff, and M2."""
    marks = [m for m in kept.marks if m["note"] != "signature"]
    heading("M: the corpus's hand-laid marks under their one-touch width, by canvas size")
    rows = []
    for label in ("up to 400", "401-800", "801-1200", "over 1200"):
        here = [m for m in marks if _bucket(m["long"]) == label]
        if not here:
            continue
        under = [m for m in here if landing_px(m["tip"]) is not None
                 and m["px"] < landing_px(m["tip"])]
        rounds = [m for m in here if m["tip"] in ROUND_TIPS]
        rounds_under = [m for m in under if m["tip"] in ROUND_TIPS]
        rows.append([label, len({m['painting'] for m in here}), len(here), len(under),
                     f"{len(under) / len(here):.0%}", len(rounds), len(rounds_under),
                     sum(1 for m in here if m2(m)),
                     len({m["painting"] for m in here if m2(m)})])
    print(table(rows, ["long side", "paintings", "hand marks", "under the width", "share",
                       "round", "round, under", "M2 would speak", "in paintings"]))
    spoke = [m for m in marks if m2(m)]
    print(f"  M2 over the corpus: {len(spoke)} marks in "
          f"{len({m['painting'] for m in spoke})} of {len({m['painting'] for m in marks})} "
          f"paintings; {sum(1 for m in spoke if faint(m))} of them faint by O3's "
          f"0.15 and 0.25; laid with a pressure list "
          f"{sum(1 for m in spoke if m['listed'])}, at opacity under 1 "
          f"{sum(1 for m in spoke if m['opacity'] < 1.0)}")
    print("  the width: a round tip's one-touch dab cliff (6.5 px round_hard and liner, "
          "7.5 round_soft); 4 px for a flat, bristle or knife")

    heading("O3: a faint mark -- far from what it landed on, and it barely moved it")
    judged = [m for m in marks if not math.isnan(m["reach"])]
    print(f"  {len(marks)} hand-laid marks over {len({m['painting'] for m in marks})} "
          f"paintings; {len(judged)} with a path over pixels its colour was not already")
    rows = []
    for far in (0.10, 0.15, 0.25):
        for reach in (0.15, 0.25, 0.35):
            hit = [m for m in judged if faint(m, far, reach)]
            rows.append([f"{far:.2f}", f"{reach:.2f}", len(hit),
                         len({m['painting'] for m in hit}),
                         sum(1 for m in hit if m["opacity"] < 0.35),
                         sum(1 for m in hit if m2(m))])
    print(table(rows, ["colour over", "moved under", "marks", "paintings",
                       "at opacity under 0.35", "also M2"]))
    hit = [m for m in judged if faint(m)]
    by = {}
    for m in hit:
        by.setdefault(m["painting"], []).append(m)
    rows = [[name, len(ms), len([m for m in marks if m["painting"] == name]),
             f"{pct([m['px'] for m in ms], 50):.1f}",
             f"{pct([m['opacity'] for m in ms], 50):.2f}",
             sum(1 for m in ms if m2(m))]
            for name, ms in sorted(by.items(), key=lambda kv: -len(kv[1]))]
    print(table(rows, ["painting", "faint", "of its hand marks", "median px",
                       "median opacity", "also M2"]))

    heading("O3 and M2 on the Curator's own: the candle, the patron's rim, the lock")
    for name in ("curator_candle", "curator_patron", "curator_locked"):
        mine = [m for m in marks if m["painting"] == name]
        rows = []
        for m in mine:
            if not (faint(m) or m2(m) or (m["px"] < (landing_px(m["tip"]) or 0))):
                continue
            rows.append([m["line"], m["brush"], f"{m['px']:.1f}", f"{m['opacity']:.2f}",
                         m["pressure"], f"{m['colour']:.2f}", f"{m['under']:.2f}",
                         f"{m['reach']:.2f}", f"{m['moved']:.0f}",
                         "faint" if faint(m) else "", "M2" if m2(m) else ""])
        print(f"  {name}: {len(mine)} hand-laid marks")
        print(table(rows, ["line", "brush", "px", "opacity", "pressure", "colour",
                           "under it", "reach", "moved (levels, 90th)", "O3", "M2"],
                    indent="    "))


# -- the run ------------------------------------------------------------------------------

BENCHES = (
    ("claims", "the nine rebuilt at stage 99, against the PNGs they shipped"),
    ("alpha", "K: an alpha from the places, against the painter's cuts"),
    ("deposit", "M: the candle at 1x, 2x and 4x, reduced to its size, and the weave"),
    ("layer", "N: the nine checklists, under key='low' and read inside the cut"),
    ("grey", "L1: the fact at mix(), over the corpus's mixtures"),
    ("faint", "O3 and M2: faint marks and marks under their cliff, over the corpus"),
)
_NEEDS_CORPUS = {"grey", "faint"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    for flag, what in BENCHES:
        parser.add_argument(f"--{flag}", action="store_true", help=what)
    parser.add_argument("--corpus", action="store_true",
                        help="replay the corpus afresh and keep it in out/curator/corpus.pkl")
    args = parser.parse_args(argv)
    if args.corpus:
        kept = corpus(fresh=True)
        print(f"  kept {len(kept.mixes)} mixtures and {len(kept.marks)} hand-laid marks "
              f"in {CACHE}")
    chosen = {k for k, v in vars(args).items() if v and k != "corpus"}
    if args.corpus and not chosen:
        return 0
    run = {flag.replace("-", "_") for flag, _ in BENCHES} if not chosen else chosen
    print("The Curator's rows, measured. Engine "
          f"{easel.__version__} from {Path(easel.__file__).parent}", flush=True)
    if "claims" in run:
        probe_claims()
    if "alpha" in run:
        probe_alpha()
    if "deposit" in run:
        probe_deposit()
    if "layer" in run:
        probe_layer()
    kept = corpus() if run & _NEEDS_CORPUS else None
    if "grey" in run:
        probe_grey(kept)
    if "faint" in run:
        probe_faint(kept)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
