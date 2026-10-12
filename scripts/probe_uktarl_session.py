"""The measurements behind Uktarl's Room's round -- step 2 of ``PLAN-0.9.0.md``.

One painter painted against 0.8.0 the day it shipped: four bandits in vampire costume at
a card table, their leader standing inside a carved sunburst, in 410 of 450 strokes. Its
verdict is filed as the open round at the top of ``SUGGESTIONS.md``, and the plan built on
it proposes paint held outside a shape, a held edge that is soft, three rules narrowed and
a habit declared, a rehearsal's look cropped, a local frame, a share of the budget for
each part, the direction a mass is charged for, the low key said, and a shorter reading
path. **Every one of those is a candidate until this script has measured it** --
``LESSONS.md``'s first rule.

It reuses ``probe_bell_session.py``'s rebuild, which lays each committed pass through the
CLI's own ``run_script`` and keeps a copy of the canvas after each, and
``probe_cohort_session.py``'s corpus harness, with a pass hook of its own. Every candidate
is patched in for the length of one bench and never into the engine.

    python scripts/probe_uktarl_session.py              # every flag below
    python scripts/probe_uktarl_session.py --claims     # the rebuild, against the export
    python scripts/probe_uktarl_session.py --clip-out   # 4A: the backlight, held outside him;
                                                        # from step 3, as built beside it
    python scripts/probe_uktarl_session.py --answers    # the painter's answers, re-measured
    python scripts/probe_uktarl_session.py --soft       # 4B: the soft hold; blind sheets
    python scripts/probe_uktarl_session.py --join       # P9: the step across the terminators
    python scripts/probe_uktarl_session.py --shares     # 4F: the shares line, pass by pass
    python scripts/probe_uktarl_session.py --rules      # 4C: three rules' candidates, and C5
    python scripts/probe_uktarl_session.py --direction  # 4G: what a direction costs
    python scripts/probe_uktarl_session.py --key        # 4H: the line beside a named light
    python scripts/probe_uktarl_session.py --reading    # 4I: the reading path's inventory
    python scripts/probe_uktarl_session.py --answers2   # the second answers, re-measured
    python scripts/probe_uktarl_session.py --corpus     # the corpus replay alone, kept

``--rules``, ``--direction`` and ``--key`` read one replay of every committed painting,
about twenty-five minutes, kept in ``out/uktarl/corpus.pkl`` until ``--corpus`` asks for
another or the engine is a release other than the one that replayed it. ``--soft``
re-lays five passes under each candidate and rebuilds the painting three times, about
eight minutes. Pictures go to ``out/uktarl/``; the soft sheets carry letters, and their
key is ``out/uktarl/soft_key.txt``, kept from the painter.
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import math
import pickle
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_bell_session as bell  # noqa: E402
import probe_cohort_session as cohort  # noqa: E402

import easel  # noqa: E402
import easel.session as session_module  # noqa: E402
from easel import Session, checklist  # noqa: E402
from easel.plan import read_place  # noqa: E402
from easel.regions import Polygon  # noqa: E402

UKTARL = ROOT / "paintings" / "Claude" / "uktarl_krannoc"
OUT = ROOT / "out" / "uktarl"

#: The painting, registered with the bell probe's rebuild under the corpus probe's own
#: entry, so the two cannot disagree about its canvas or its order. Its passes rebuild in
#: their numbering: the drawing ran three times, but a drawing of guides lays no record.
_ENTRY = {entry.name: entry for entry in cohort.CORPUS}["uktarl"]
bell.ORDERS["uktarl"] = _ENTRY.passes
bell.CANVASES["uktarl"] = dict(_ENTRY.session)
bell.FOLDERS["uktarl"] = UKTARL

BACKLIGHT = "p08_backlight.py"
heading = bell.heading
table = bell.table


def save_sheet(panels: list[tuple[str, Image.Image]], name: str,
               columns: int | None = None) -> Path:
    """Panels side by side, each labelled, into ``out/uktarl/``."""
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    bell.label_sheet(panels, columns=columns or len(panels)).save(path)
    return path


# -- the rebuild ------------------------------------------------------------------------

def probe_claims(rb: bell.Rebuilt) -> None:
    """The rebuild against the painter's own export, and the counts section 3 quotes."""
    bell.probe_rebuild(rb)
    s = rb.session
    print(f"  {len(s.history.records)} records against 429 filed, "
          f"{s.stroke_count} spent against 410")
    landmarks = sorted(getattr(s, "marks", {}) or {})
    print(f"  landmarks left at the end: {', '.join(landmarks) or 'none'}")


# -- 4A: paint held outside a shape ----------------------------------------------------

@contextlib.contextmanager
def excluding(shapes: list[Polygon], side: str = "line", feather: float = 0.002):
    """Every held mark laid while this is open also stays off ``shapes``.

    The candidate ``clip_out=`` as a patch on :meth:`Session._clip_cover`: the held mask
    is multiplied by one minus the excluded shapes' coverage. ``side`` is where the
    exclusion's edge breaks against the tooth, over ``feather`` of the long side:

    - ``"line"``: nowhere; cut on the outline, as ``feather=0`` cuts a hold.
    - ``"light"``: outward from the outline, into the paint being held -- what a hold's
      default does on its own side, and what the painter's answer A says opens a dark
      seam between a backlight and the figure.
    - ``"figure"``: inward, onto the excluded shape -- the paint reaches past the line
      and breaks there, which is the painter's other form.

    ``_edge_depth`` is positive inside and negative outside, so both ramps are the one
    ``Session._clip_cover`` uses, read from one side or the other.
    """
    original = Session._clip_cover

    def patched(self, holds, feather_=0.0, outs=()):
        cover = original(self, holds, feather_, outs).copy()
        w, h = self.canvas.width, self.canvas.height
        px = float(feather) * self.canvas.long_side
        for one in shapes:
            inside = one.coverage(w, h)
            keep = 1.0 - inside
            if side != "line" and px > 0.0:
                rows, cols, depth, _ = one._edge_depth(w, h, px, inside)
                near = depth < 0.0 if side == "light" else depth > 0.0
                rows, cols, depth = rows[near], cols[near], np.abs(depth[near])
                if len(rows):
                    full = np.full(len(rows), px, dtype=np.float32)
                    broken = self.canvas.broken_edge(rows, cols, depth, full)
                    keep[rows, cols] = (np.minimum(keep[rows, cols], broken)
                                        if side == "light"
                                        else np.maximum(keep[rows, cols], 1.0 - broken))
            cover *= keep
        return cover

    Session._clip_cover = patched
    try:
        yield
    finally:
        Session._clip_cover = original


#: The painter's backlight with its three regions replaced by one place and the figure
#: excluded: ``clip=wall, clip_out=uktarl`` in the candidate's words. Every path, brush,
#: size, colour and pressure is the committed pass's, line for line.
BACKLIGHT_OUT = '''
base = s.sample(ell_px(380, 500, 26, 40))
p["backglow"] = p.at_value(p.mix("glow", base, 0.55), 0.38)
p["backglow_hot"] = p.at_value(p.mix("glow", base, 0.35), 0.48)
s.dry()
p["backglow_wide"] = p.at_value(p.mix("glow", base, 0.75), 0.29)
for path in ([(420, 400), (380, 470), (360, 540), (370, 620)],
             [(730, 380), (760, 450), (770, 520), (750, 610)]):
    s.stroke(px_pts(path), "round_soft", "backglow_wide", size=0.24, opacity=0.40,
             pressure=[0.3, 1.0, 0.8, 0.3], clip=wall)
for path in ([(446, 390), (424, 460), (414, 540), (404, 630)],
             [(694, 360), (712, 440), (716, 520), (706, 610)]):
    s.stroke(px_pts(path), "round_soft", "backglow", size=0.11, opacity=0.55,
             pressure=[0.5, 1.0, 0.9, 0.4], clip=wall)
    s.stroke(px_pts(path), "round_soft", "backglow_hot", size=0.045, opacity=0.6,
             pressure=[0.6, 1.0, 0.8, 0.3], clip=wall)
s.stroke(px_pts([(470, 316), (512, 300), (556, 312)]), "round_soft",
         p.at_value(p.mix("ray_lit", "glow", 0.5), 0.56), size=0.075, opacity=0.5,
         pressure="swell", clip=wall)
'''

#: Uktarl as the exclusion names him: every part the three regions were typed round.
UKTARL_PARTS = ("uk_head_poly", "uk_hair", "uk_collar", "uk_body", "uk_arm", "uk_hand",
                "uk_wing")


def _step_across(view: np.ndarray, x: int, rows: slice) -> float:
    """How far the value jumps between two neighbouring columns: a seam, if large."""
    return float(np.abs(view[rows, x] - view[rows, x - 1]).mean())


def _seam(view: np.ndarray) -> str:
    """The painter's measure in answer A: the wall left unlit between light and figure."""
    counts = [int(((view[y, 404:440] > 0.17) & (view[y, 404:440] < 0.40)).sum())
              for y in (460, 490, 520, 550)]
    return "/".join(str(c) for c in counts)


def probe_clip_out(rb: bell.Rebuilt) -> None:
    """4A: the backlight laid once with an exclusion, against the three typed regions."""
    heading("4A: the backlight held outside Uktarl, against the three regions")
    scope = bell.scope_of("uktarl")
    shapes = [scope[name] for name in UKTARL_PARTS]
    regions = [scope[name] for name in ("glow_left", "glow_right", "glow_above")]
    typed = sum(len(one.points) for one in regions)
    print(f"  the three regions: {typed} points; the exclusion: one argument naming "
          f"{len(shapes)} shapes the prelude already has")
    prelude = (UKTARL / "prelude.py").read_text(encoding="utf-8-sig")

    laid = {}
    committed = rb.opened(BACKLIGHT)
    bell.run_pass(committed, UKTARL / BACKLIGHT, UKTARL / "prelude.py")
    laid["committed: three regions"] = committed
    seam = rb.opened(BACKLIGHT)
    bell.run_pass(seam, UKTARL / "versions" / "p08_v2_seam.py", UKTARL / "prelude.py")
    laid["rehearsed: the seam"] = seam
    for label, side in (("clip_out, cut on the line", "line"),
                        ("clip_out, broken into the light", "light"),
                        ("clip_out, broken onto him", "figure")):
        out = rb.opened(BACKLIGHT)
        started = time.time()
        with excluding(shapes, side):
            bell.run_source(out, BACKLIGHT_OUT, BACKLIGHT, prelude=prelude)
        laid[label] = out
        print(f"  {label}: laid in {time.time() - started:.1f} s")
    # Step 3: the same pass through the engine's own clip_out=, no patch. It has to lay
    # what the bench's cut-on-the-line candidate laid, pixel for pixel.
    if "clip_out" in Session.stroke.__code__.co_varnames:
        built = rb.opened(BACKLIGHT)
        started = time.time()
        bell.run_source(built, BACKLIGHT_OUT.replace(
            "clip=wall)", f"clip=wall, clip_out=[{', '.join(UKTARL_PARTS)}])"),
            BACKLIGHT, prelude=prelude)
        laid["clip_out, as built (step 3)"] = built
        same = np.array_equal(built.canvas.rgb, laid["clip_out, cut on the line"].canvas.rgb)
        print(f"  clip_out, as built: laid in {time.time() - started:.1f} s; "
              f"{'the same pixels as' if same else 'NOT the same pixels as'} the bench's "
              f"cut on the line")

    base = bell.values(committed)
    h, w = base.shape
    cover = np.zeros((h, w), dtype=np.float32)
    for one in shapes:
        cover = np.maximum(cover, one.coverage(w, h))
    figure = cover > 0.5
    whole = cover >= 0.999
    rows = slice(int(0.42 * h), int(0.83 * h))
    before = bell.values(rb.opened(BACKLIGHT))
    out_rows = []
    for label, s in laid.items():
        v = bell.values(s)
        diff = np.abs(v - base)
        moved = diff > 2 / 255
        touched = (np.abs(v - before) > 2 / 255) & figure
        records = len(s.history.records) - len(rb.opened(BACKLIGHT).history.records)
        out_rows.append([label, records, f"{int(moved.sum())}", f"{diff.max() * 255:.0f}",
                         f"{int(touched.sum())}", f"{int((touched & whole).sum())}",
                         _seam(v),
                         f"{_step_across(v, 290, rows) * 255:.1f}",
                         f"{_step_across(v, 812, rows) * 255:.1f}"])
    print(table(out_rows, ["laid", "records", "px off committed", "most, levels",
                           "px on him", "wholly him", "seam px", "step x=290", "step x=812"]))
    print("  (px on him: pixels at least half his that the pass changed by more than two "
          "levels; wholly him: those his outline covers entirely, not its antialiased rim)")
    print("  (seam px: at the painter's four rows, y=460, 490, 520 and 550, the pixels "
          "between the light and his left edge that read 0.17 to 0.40, neither")
    print("  (a step is the mean jump in value, in 8-bit levels, between two neighbouring "
          "columns over the figure's height; the seam's columns are 290 and 812)")

    box = (0.25, 0.22, 0.85, 0.86)
    panels = [(label, bell.crop(s, box)) for label, s in laid.items()]
    print(f"  sheet: {save_sheet(panels, 'clip_out.png', columns=2)}")


# -- the corpus, replayed once for every bench that reads it ---------------------------

CACHE = OUT / "corpus.pkl"


@dataclass
class Kept:
    """What one replay of the corpus kept: every committed pass, and every shaped mass."""

    passes: list[dict] = field(default_factory=list)
    masses: list[dict] = field(default_factory=list)
    errors: dict[str, list[str]] = field(default_factory=dict)
    engine: str = ""


_KEEPING: list[Kept] = []
_PAINTING: list[str] = [""]
_CURRENT_PASS: list = [None]


def _keep_pass(done, session: Session) -> None:
    """A ``PASS_HOOKS`` entry: the pass's records, its report, and its light, read once."""
    if not _KEEPING:
        return
    records = session.history.records
    marks = [r for r in records[done.start:done.end] if r.kind not in bell.UNPAINTED]
    earlier = sum(1 for r in records[:done.start] if r.kind not in bell.UNPAINTED)
    w, h = session.canvas.width, session.canvas.height
    entry = {"painting": _PAINTING[0], "pass": done.name, "start": done.start,
             "end": done.end, "marks": marks, "earlier": earlier, "canvas": (w, h),
             "findings": list(done.findings), "error": done.error,
             "report": session.report(since=done.start).splitlines(),
             "spent": session.stroke_count, "key": session._plan.key,
             "light": None, "values": None}
    paid = [r for r in records if r.kind not in bell.UNPAINTED]
    if paid:
        view = session.canvas.values(sketch=False).astype(np.float32) / 255.0
        flat = view.reshape(-1)[::17]
        reach = (session.palette.darkest_value, session.palette.lightest_value)
        entry["values"] = {"low": float(np.percentile(flat, 5)),
                           "high": float(np.percentile(flat, 95)),
                           "middle": (reach[0] + reach[1]) / 2.0}
        plan = session._plan
        if plan.lightest is not None:
            pv = session._value_view()
            mask = plan.lightest.outline.mask(w, h)
            if mask.any() and (~mask).any():
                entry["light"] = {
                    "name": plan.lightest.name,
                    "bright": float(read_place(pv[mask]).brightest),
                    "rest": float(np.percentile(pv[~mask], 95))}
    _KEEPING[0].passes.append(entry)


def _spans(poly: Polygon, degrees: float, band: float) -> tuple[int, int]:
    """``(lines, pieces)``: how many passes a shaped mass lays at ``degrees``, and in how
    many pieces -- ``Session._shape_paths``' own arithmetic, without the wander."""
    theta = math.radians(session_module._angle_of(degrees))
    dx, dy = math.cos(theta), math.sin(theta)
    nx, ny = -dy, dx
    pts = np.asarray(poly.points, dtype=np.float64)
    cx, cy = poly.box.center
    offs = (pts[:, 0] - cx) * nx + (pts[:, 1] - cy) * ny
    lo, hi = float(offs.min()), float(offs.max())
    n = max(1, int(round((hi - lo) / band)))
    lines = pieces = 0
    for i in range(n):
        off = lo + (i + 0.5) * (hi - lo) / n
        origin = (cx + nx * off, cy + ny * off)
        kept = [1 for t0, t1 in session_module._spans_inside(poly, origin, (dx, dy))
                if t1 - t0 >= band * 0.35]
        if kept:
            lines += 1
            pieces += len(kept)
    return lines, pieces


@contextlib.contextmanager
def pricing():
    """Every shaped ``block_in`` priced as it is called: at its direction, along its axis.

    Patched where the engine already prices a mass -- the two direction checks, which
    are handed the resolved brush, density and overhang -- so nothing about the call
    changes: the walk runs on a trial copy, as the checks' own does.
    """
    saved = (session_module._check_default_direction,
             session_module._check_direction_sequence)

    def record(session, place, b, direction, density, overhang):
        if not _KEEPING or not isinstance(place, Polygon):
            return
        dirs = session_module._pass_directions(
            "horizontal" if direction is None else direction)
        trial = session._trial_session()

        def price(d) -> int:
            return sum(1 for _ in trial._block_in_paths(place, b, d, density, overhang))

        band = session_module._pass_step(b.size, density)
        lines = pieces = 0
        for d in dirs:
            angle = place.axis if d == "axis" else d
            one, many = _spans(place, angle, band)
            lines += one
            pieces += many
        current = _CURRENT_PASS[0]
        _KEEPING[0].masses.append({
            "painting": _PAINTING[0], "pass": current.name if current else "",
            "place": place.name, "direction": direction,
            "given": price(direction), "axis": price("axis"),
            "lines": lines, "pieces": pieces,
            "single": len(dirs) == 1 and direction not in (None, "axis")})

    def default(session, place, b, density, overhang, stacklevel=2):
        record(session, place, b, None, density, overhang)
        return saved[0](session, place, b, density, overhang, stacklevel=stacklevel + 1)

    def sequence(session, place, b, direction, density, overhang, stacklevel=2):
        record(session, place, b, direction, density, overhang)
        return saved[1](session, place, b, direction, density, overhang,
                        stacklevel=stacklevel + 1)

    session_module._check_default_direction = default
    session_module._check_direction_sequence = sequence
    try:
        yield
    finally:
        (session_module._check_default_direction,
         session_module._check_direction_sequence) = saved


def replay_corpus(names: tuple[str, ...] = ()) -> Kept:
    """Every committed painting rebuilt through the corpus probe's harness; what it kept."""
    kept = Kept(engine=easel.__version__)
    _KEEPING[:] = [kept]
    cohort.PASS_HOOKS.append(_keep_pass)
    opened = cohort.Watcher.open

    def tracking(self, name, session):
        made = opened(self, name, session)
        _CURRENT_PASS[0] = made
        return made

    cohort.Watcher.open = tracking
    try:
        with pricing():
            for entry in cohort.CORPUS:
                if names and entry.name not in names:
                    continue
                _PAINTING[0] = entry.name
                started = time.time()
                rep = cohort.replay(entry, keep_canvas=False)
                kept.errors[entry.name] = rep.errors
                print(f"  {entry.name:<12} {len(rep.passes):3d} passes, {rep.spent:4d} "
                      f"strokes, {time.time() - started:5.0f} s"
                      + (f"  [{'; '.join(rep.errors)[:80]}]" if rep.errors else ""),
                      flush=True)
    finally:
        cohort.PASS_HOOKS.remove(_keep_pass)
        cohort.Watcher.open = opened
        _KEEPING.clear()
    return kept


def corpus(fresh: bool = False) -> Kept:
    """The corpus replay, from ``out/uktarl/corpus.pkl`` unless stale or asked afresh."""
    if CACHE.exists() and not fresh:
        with CACHE.open("rb") as handle:
            kept = Kept(**pickle.load(handle))
        if kept.engine == easel.__version__:
            return kept
    heading("the corpus, replayed (about twenty minutes)")
    kept = replay_corpus()
    OUT.mkdir(parents=True, exist_ok=True)
    with CACHE.open("wb") as handle:
        pickle.dump(vars(kept), handle, protocol=pickle.HIGHEST_PROTOCOL)
    return kept


def committed(kept: Kept) -> list[dict]:
    """The passes that laid paint and ran clean."""
    return [p for p in kept.passes if p["marks"] and not p["error"]]


def canvas_of(entry: dict) -> SimpleNamespace:
    """What the check's rules read of a canvas: its proportions."""
    w, h = entry["canvas"]
    return SimpleNamespace(width=w, height=h, long_side=max(w, h))


# -- the painter's answers, re-measured ------------------------------------------------

REPORTS = UKTARL / "reports.txt"

#: The standing lines a report prints under its check, by the word that opens each.
STANDING = ("plan:", "lightest:", "subject:", "values:", "edges:", "ground:", "unspent:",
            "boxes:", "pencil:", "key:")


def saved_reports() -> list[tuple[str, list[str]]]:
    """``reports.txt`` as ``(heading, lines)`` per report, oldest first."""
    reports: list[tuple[str, list[str]]] = []
    for line in REPORTS.read_text(encoding="utf-8").splitlines():
        if line.startswith(("painted ", "rehearsed ")):
            reports.append((line, []))
        elif reports and line.strip():
            reports[-1][1].append(line)
    return reports


def probe_reports() -> None:
    """C: what the 46 reports printed, and how much of it repeated the report before."""
    heading("C: the 46 saved reports, as printed")
    reports = saved_reports()
    standing = repeated = 0
    last: dict[str, str] = {}
    no_light = 0
    findings: dict[str, int] = {}
    for _, lines in reports:
        said = False
        for line in lines:
            body = line.strip()
            word = body.split(" ", 1)[0]
            if line.startswith("    ") and word in STANDING:
                standing += 1
                repeated += last.get(word) == body
                last[word] = body
                said |= word == "values:" and "no clear light" in body
            elif body.startswith("- "):
                kind = ("disc" if "one disc printed" in body else
                        "bars" if "stack of bars" in body else
                        "graded" if "graded passage" in body else body[2:40])
                findings[kind] = findings.get(kind, 0) + 1
        no_light += said
    print(f"  {len(reports)} reports; {standing} standing lines, {repeated} "
          f"({repeated / standing:.0%}) word for word the same line in the report before")
    print(f"  'no clear light' in {no_light} of {len(reports)}")
    print(f"  {sum(findings.values())} finding lines: " + ", ".join(
        f"{k} {v}" for k, v in sorted(findings.items(), key=lambda kv: -kv[1])))


def probe_cape_edge(rb: bell.Rebuilt) -> None:
    """A: across the figure's left edge at four rows, after the backlight and at the end."""
    heading("A: the backlight against Uktarl's left edge, value by pixel")
    for label, s in (("after the backlight", rb.after[BACKLIGHT]),
                     ("the finished painting", rb.session)):
        v = bell.values(s)
        print(f"  {label}:")
        for y in (460, 490, 520, 550):
            row = v[y, 404:440]
            print(f"    y={y} x=404..439: " + " ".join(f"{x:.2f}" for x in row))


def _turned(points: np.ndarray, degrees: float) -> np.ndarray:
    """Points in fractions turned about their centre in fractions, as if square."""
    t = np.radians(degrees)
    c = points.mean(axis=0)
    d = points - c
    return c + d @ np.array([[np.cos(t), np.sin(t)], [-np.sin(t), np.cos(t)]])


def probe_rotation() -> None:
    """D: a 100 px square turned in fractions on a 4:3 canvas, read back in pixels."""
    heading("D: turning in fractions on a 1024x768 canvas, read in pixels")
    w, h = 1024, 768
    square = np.array([[462, 334], [562, 334], [562, 434], [462, 434]], dtype=float)
    rows = []
    for degrees in (6, 30):
        frac = square / [w, h]
        back = _turned(frac, degrees) * [w, h]
        top = back[1] - back[0]
        side = back[3] - back[0]
        angle = np.degrees(np.arctan2(top[1], top[0]))
        corner = np.degrees(np.arccos(np.dot(top, side)
                                      / np.linalg.norm(top) / np.linalg.norm(side)))
        rows.append([f"{degrees} deg", f"{angle:.1f} deg", f"{corner:.1f} deg",
                     f"{np.linalg.norm(top):.0f}", f"{np.linalg.norm(side):.0f}"])
    print(table(rows, ["asked", "top edge comes back at", "corner", "top px", "side px"]))


def probe_spent(rb: bell.Rebuilt) -> None:
    """E: what each pass spent, against the painter's split by part."""
    heading("E: strokes spent per pass")
    s = rb.session
    records = s.history.records
    starts = [rb.starts[k] for k in rb.labels] + [len(records)]
    rows = []
    for k, label in enumerate(rb.labels):
        laid = records[starts[k]:starts[k + 1]]
        spent = sum(1 for r in laid if r.kind not in bell.UNPAINTED)
        rows.append([label, spent])
    print(table(rows, ["pass", "spent"]))
    print(f"  total {sum(r[1] for r in rows)} of {s.budget}")


# -- 4B: a held edge that is soft -------------------------------------------------------

#: The candidates, each a softness on one hold, over ``px`` pixels from its outline:
#: B1 a smooth ramp inward; B2 that ramp broken against the canvas's tooth, the way
#: the default feather breaks an edge, only deeper; B3 a smooth ramp centred on the
#: outline, half outside it. B4, a ``lose()`` verb, was declined by the painter (P2).
SOFT_KINDS = ("B1", "B2", "B3")


def _smooth(t: np.ndarray) -> np.ndarray:
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


@contextlib.contextmanager
def softening(soft: dict[tuple, float], kind: str):
    """Every hold whose outline is a key of ``soft`` is softened over that many pixels.

    Per hold, as the painter's answer B asks: a call held by its own outline and by a
    second shape softens the one and keeps the other as it was, since the masks
    multiply. Every other hold is built as ``Session._clip_cover`` builds it.
    """
    original = Session._clip_cover

    def patched(self, holds, feather=0.0):
        if not any(tuple(one.points) in soft for one in holds):
            return original(self, holds, feather)
        w, h = self.canvas.width, self.canvas.height
        cover = None
        for one in holds:
            mask = one.coverage(w, h)
            px = soft.get(tuple(one.points))
            reach = px if px else float(feather) * self.canvas.long_side
            if reach > 0.0:
                rows, cols, depth, full = one._edge_depth(w, h, reach, mask)
                if px and kind == "B3":
                    mask[rows, cols] = _smooth(0.5 + depth / px)
                elif px and len(rows):
                    # Every pixel within reach, the outline's own antialiased rim
                    # outside it too: the ramp is nothing at the line, so a pixel
                    # past it takes nothing, or a faded edge keeps a dotted ring.
                    d = np.maximum(depth, 0.0).astype(np.float32)
                    f = np.minimum(full, reach).astype(np.float32)
                    ramp = (_smooth(d / np.maximum(f, 1e-6)) if kind == "B1"
                            else self.canvas.broken_edge(rows, cols, d, f))
                    mask[rows, cols] = np.minimum(mask[rows, cols], ramp)
                elif len(rows):
                    inside = depth > 0.0
                    r, c, d = rows[inside], cols[inside], depth[inside]
                    f = np.minimum(full[inside], reach).astype(np.float32)
                    mask[r, c] = np.minimum(mask[r, c], self.canvas.broken_edge(r, c, d, f))
            cover = mask if cover is None else cover * mask
        return cover

    Session._clip_cover = patched
    try:
        yield
    finally:
        Session._clip_cover = original


#: The painter's answer B, row by row: the pass, the hold to soften, and how far. The
#: terminators are measured along the prelude's own terminator; the rest along the
#: whole outline. The mountain's far ends and the crags' ends are left out: the first
#: is one shape lit in the middle, which a hold cannot soften at its ends only, and
#: the second are strokes, which have no hold to soften.
SOFT_CASES = (
    ("her terminator", "p11_left_bandit.py", "a_lit", 8, "A_TERM"),
    ("its terminator", "p09_doppelganger.py", "dp_lit", 8, "DP_TERM"),
    ("Uktarl's far cheek", "p07_uktarl_head.py", "uk_face_lit", 8, "UK_TERM"),
    ("her far side", "p11_left_bandit.py", "a_body", 11, ""),
    ("her wig", "p11_left_bandit.py", "a_hair", 3, ""),
    ("its far side", "p09_doppelganger.py", "dp_body", 9, ""),
    ("the near bandit", "p13_near_bandit.py", "b_body", 7, ""),
    ("the blanket heap", "p05_floor_tub.py", "tub_heap", 2.5, ""),
)


def step_widths(view: np.ndarray, runs, reach: float = 4.0, every: float = 2.0,
                least: float = 0.08) -> list[float]:
    """How wide the step across a line is, in pixels, every few pixels along it.

    The ``edges:`` line's own measure, taken along a line given rather than wherever a
    ridge is found: the value range within ``reach`` pixels either side, over the
    steepest gradient across it. A 10-to-90% rise reads the plateaus at its ends, and on
    a face 44 px across the terminator is 9 px from the face's edge, so a long profile
    reads the wig. A place whose range is under ``least`` has no step and is skipped.
    """
    h, w = view.shape
    out = []
    ts = np.arange(-reach, reach + 0.25, 0.5)
    for run in runs:
        pts = np.asarray(run, dtype=np.float64) * [w, h]
        for a, b in zip(pts[:-1], pts[1:], strict=True):
            length = float(np.hypot(*(b - a)))
            if length < 1e-6:
                continue
            along = (b - a) / length
            n = np.array([-along[1], along[0]])
            for d in np.arange(every / 2.0, length, every):
                p = a + along * d
                prof = np.mean([bell._bilinear(view, p[0] + ts * n[0] + k * along[0],
                                               p[1] + ts * n[1] + k * along[1])
                                for k in (-1, 0, 1)], axis=0)
                span = float(prof.max() - prof.min())
                slope = float(np.abs(np.diff(prof)).max()) / 0.5
                if span >= least and slope > 0.0:
                    out.append(span / slope)
    return out


def _runs_of(scope: dict, shape: Polygon, term: str) -> list:
    """Where a case's edge is measured: the terminator, or the shape's outline."""
    if term:
        return [scope["px_pts"](scope[term])]
    return [[(float(x), float(y)) for x, y in shape.closed]]


def _box_round(shape: Polygon, w: int, h: int, margin: int = 24) -> tuple:
    pts = np.asarray(shape.points) * [w, h]
    x0, y0 = pts.min(axis=0) - margin
    x1, y1 = pts.max(axis=0) + margin
    return (max(x0, 0) / w, max(y0, 0) / h, min(x1, w) / w, min(y1, h) / h)


def _edges_numbers(view: np.ndarray) -> str:
    """The ``edges:`` line's two numbers: the share under 2.5 px, and the median."""
    line = checklist.edges_line(view)
    found = re.findall(r"(\d+)% of edges.*median ([\d.]+) px", line)
    return f"{found[0][0]}%, {found[0][1]} px" if found else line


def _blind(labels: list[str], seed: int) -> list[str]:
    """Letters for ``labels`` in a fixed shuffled order, so a sheet can be read blind."""
    order = np.random.default_rng(seed).permutation(len(labels))
    letters = "ABCDEFGH"
    return [letters[int(np.nonzero(order == i)[0][0])] for i in range(len(labels))]


def probe_soft(rb: bell.Rebuilt) -> None:
    """4B: each edge of the painter's answer B, softened by each candidate, per hold."""
    heading("4B: the soft hold, on the edges the painter would soften")
    scope = bell.scope_of("uktarl")
    w, h = rb.session.canvas.width, rb.session.canvas.height
    labels = ["as painted", *SOFT_KINDS]
    letters = _blind(labels, seed=9)
    key = [f"{letter} = {label}" for letter, label in sorted(zip(letters, labels, strict=True))]
    rows = []
    sheets = []
    for name, label, shape_name, px, term in SOFT_CASES:
        shape = scope[shape_name]
        runs = _runs_of(scope, shape, term)
        laid = {}
        for kind in labels:
            s = rb.opened(label)
            started = time.time()
            soft = {} if kind == "as painted" else {tuple(shape.points): float(px)}
            with softening(soft, kind):
                bell.run_pass(s, UKTARL / label, UKTARL / "prelude.py")
            laid[kind] = (s, time.time() - started)
        base = laid["as painted"][1]
        for kind, (s, seconds) in laid.items():
            widths = step_widths(bell.values(s), runs, reach=max(4.0, float(px)))
            rows.append([name, f"{px:g}", kind, len(widths),
                         f"{bell.pct(widths, 50):.1f}", f"{bell.pct(widths, 90):.1f}",
                         f"{seconds - base:+.1f}"])
        box = _box_round(shape, w, h)
        panels = [(letter, bell.crop(laid[kind][0], box, zoom=2))
                  for letter, kind in sorted(zip(letters, labels, strict=True))]
        sheets.append(save_sheet(panels, f"soft_{_slug(name)}.png", columns=4))
    print(table(rows, ["edge", "asked px", "laid", "samples", "step, median px",
                       "p90 px", "seconds over"]))
    print("  (step: the range within the asked px (4 at least) either side over the steepest gradient across "
          "it, every 2 px -- along the prelude's terminator for the three faces, along "
          "the whole outline otherwise)")

    # The whole picture with every edge of the table softened, one candidate at a time.
    whole = {"as painted": rb.session}
    by_pass: dict[str, dict] = {}
    for _, label, shape_name, px, _ in SOFT_CASES:
        by_pass.setdefault(label, {})[tuple(scope[shape_name].points)] = float(px)
    for kind in SOFT_KINDS:
        s = bell.new_session("uktarl")
        prelude = UKTARL / "prelude.py"
        for label in bell.ORDERS["uktarl"]:
            with softening(by_pass.get(label, {}), kind):
                bell.run_pass(s, UKTARL / label, prelude)
        whole[kind] = s
    print("  the whole picture, every edge of answer B softened:")
    for kind, s in whole.items():
        print(f"    {kind:<11} edges: {_edges_numbers(bell.values(s))}")
    small = [(letter, Image.fromarray(whole[kind].canvas.to_srgb8(impasto=True, sketch=False))
              .resize((256, 192), Image.LANCZOS))
             for letter, kind in sorted(zip(letters, labels, strict=True))]
    sheets.append(save_sheet(small, "soft_whole_256.png", columns=4))
    full = [(letter, Image.fromarray(whole[kind].canvas.to_srgb8(impasto=True, sketch=False)))
            for letter, kind in sorted(zip(letters, labels, strict=True))]
    sheets.append(save_sheet(full, "soft_whole.png", columns=2))
    (OUT / "soft_key.txt").write_text("\n".join(key) + "\n", encoding="utf-8")
    for path in sheets:
        print(f"  sheet: {path}")
    print(f"  the letters' key, kept from the painter: {OUT / 'soft_key.txt'}")


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.casefold()).strip("_")


def probe_answers2(rb: bell.Rebuilt) -> None:
    """The second answers' measured claims: Uktarl's lit plane under B1, and the laps."""
    heading("answers-step2, 8: Uktarl's lit plane, softened by B1")
    scope = bell.scope_of("uktarl")
    label = "p07_uktarl_head.py"
    lit = scope["uk_face_lit"]
    laid = {}
    for kind in ("as painted", "B1"):
        s = rb.opened(label)
        soft = {} if kind == "as painted" else {tuple(lit.points): 8.0}
        with softening(soft, kind):
            bell.run_pass(s, UKTARL / label, UKTARL / "prelude.py")
        laid[kind] = bell.values(s)
    w, h = rb.session.canvas.width, rb.session.canvas.height
    inside = lit.coverage(w, h) > 0.5
    darker = (laid["as painted"] - laid["B1"])[inside]
    moved = darker[darker > 0.05]
    print(f"  {int(inside.sum())} pixels of the lit plane; B1 darkens {moved.size} of them "
          f"({moved.size / inside.sum():.0%}) by more than 0.05, median "
          f"{float(np.median(moved)) if moved.size else 0.0:.2f}")
    outline = [[(float(x), float(y)) for x, y in lit.closed]]
    for kind, view in laid.items():
        widths = step_widths(view, outline, reach=8.0)
        print(f"  {kind:<11} the step across the lit plane's whole outline: median "
              f"{bell.pct(widths, 50):.1f} px over {len(widths)} samples")

    heading("answers-step2, 4a: the value across the laps' passes, as painted")
    view = bell.values(rb.session)
    for name in ("a_lower", "d_lower"):
        shape = scope[name]
        mask = shape.coverage(w, h) > 0.99
        ripples = []
        for y in np.nonzero(mask.any(axis=1))[0]:
            row = view[y, mask[y]]
            if row.size > 12:
                core = row[3:-3]
                trend = np.polyval(np.polyfit(np.arange(core.size), core, 1),
                                   np.arange(core.size))
                ripples.append(float(np.abs(core - trend).max()))
        print(f"  {shape.name}: across each row inside it, the largest departure from the "
              f"row's own slope -- median {bell.pct(ripples, 50):.3f}, "
              f"p90 {bell.pct(ripples, 90):.3f}, over {len(ripples)} rows")


def probe_join(rb: bell.Rebuilt) -> None:
    """P9: how wide the step across each face's terminator is, as painted."""
    heading("P9: the join across each face's terminator, as painted")
    scope = bell.scope_of("uktarl")
    view = bell.values(rb.session)
    rows = []
    for name, term, face in (("the lady", "A_TERM", "a_face"),
                             ("the doppelganger", "DP_TERM", "dp_head"),
                             ("Uktarl", "UK_TERM", "uk_head_poly")):
        widths = step_widths(view, [scope["px_pts"](scope[term])])
        pts = np.asarray(scope[face].points) * [rb.session.canvas.width,
                                                 rb.session.canvas.height]
        across = float(pts[:, 0].max() - pts[:, 0].min())
        rows.append([name, f"{across:.0f}", len(widths), f"{bell.pct(widths, 50):.1f}",
                     f"{bell.pct(widths, 90):.1f}", f"{across / 6:.0f}"])
    print(table(rows, ["face", "across px", "samples", "step, median px", "p90 px",
                       "a sixth of it, px"]))
    print(f"  a join at size=0.006 is {0.006 * rb.session.canvas.long_side:.1f} px wide "
          "on this canvas")


# -- 4F: a share of the budget for each part --------------------------------------------

#: The painter's split (answer E), as shares of the 450.
SHARES = {"uktarl": 0.25, "doppelganger": 0.11, "lady": 0.11, "near bandit": 0.10,
          "relief": 0.25, "table": 0.08, "floor": 0.05}
_PASS_PART = {"p02": "relief", "p03": "relief", "p04": "relief", "p14": "relief",
              "p05": "floor", "p06": "uktarl", "p07": "uktarl", "p08": "uktarl",
              "p09": "doppelganger", "p10": "table", "p11": "lady", "p13": "near bandit"}
#: The passes that lay several parts, call by call, by the line each call is made at.
_LINE_PART = {("p12", 10): "lady", ("p12", 11): "doppelganger", ("p12", 43): "uktarl",
              ("p12", 47): "doppelganger", ("p15", 9): "relief", ("p15", 13): "uktarl",
              ("p15", 20): "uktarl", ("p15", 23): "uktarl", ("p15", 25): "lady",
              ("p15", 28): "doppelganger", ("p15", 38): "uktarl", ("p16", 55): "uktarl",
              ("p16", 58): "uktarl", ("p16", 61): "uktarl", ("p16", 70): "relief",
              ("p17", 82): "lady", ("p17", 83): "doppelganger"}


def parts_of(calls: list) -> list[tuple[str, str, int]]:
    """``(pass, part, strokes)`` per call, the signature left out as the budget leaves it.

    ``fan()`` in the card game is one function called for three hands, so its calls go
    to the hand they follow: Uktarl's, then hers after line 43, the doppelganger's
    after line 47. Every other call of the card game, and of the light's pass, not
    listed is the table's.
    """
    out = []
    after = "uktarl"
    for c in calls:
        if str(c.args.get("note", "")) == "signature" or not c.paid:
            continue
        prefix = c.run[:3]
        part = _PASS_PART.get(prefix)
        if part is None:
            if c.func == "fan":
                part = after
            else:
                part = _LINE_PART.get((prefix, c.line), "table")
                if (prefix, c.line) == ("p12", 43):
                    after = "lady"
                elif (prefix, c.line) == ("p12", 47):
                    after = "doppelganger"
        out.append((c.run, part, c.paid))
    return out


def shares_line(spent: dict[str, int], budget: int) -> str:
    """The candidate standing line: each part against its share of the budget."""
    said = []
    for part, share in SHARES.items():
        planned = int(round(share * budget))
        mark = " (over)" if spent.get(part, 0) > planned else ""
        said.append(f"{part} {spent.get(part, 0)} of {planned}{mark}")
    return "shares: " + ", ".join(said)


def probe_shares(rb: bell.Rebuilt) -> None:
    """4F: the shares line, pass by pass, under the split the painter says it would plan."""
    heading("4F: shares of the budget, under the painter's split")
    budget = rb.session.budget
    spent: dict[str, int] = {}
    by_pass: dict[str, list] = {}
    for run, part, paid in parts_of(rb.calls):
        by_pass.setdefault(run, []).append((part, paid))
    head = 0
    for label in rb.labels:
        for part, paid in by_pass.get(label, []):
            spent[part] = spent.get(part, 0) + paid
        if label == "p07_uktarl_head.py":
            head = spent.get("uktarl", 0)
        if label in by_pass:
            print(f"  {label:<22} {shares_line(spent, budget)}")
    total = sum(spent.values())
    print("  spent by part: " + ", ".join(f"{k} {v}" for k, v in spent.items())
          + f"; {total} in all, {budget - total} left in hand")
    marks = rb.after["p07_uktarl_head.py"].stroke_count
    print(f"  after the head's pass: uktarl {head} strokes -- {head / marks:.0%} of the "
          f"{marks} laid so far, {head / budget:.0%} of the budget of {budget}")


# -- 4C: the rules, over the corpus -----------------------------------------------------

def _width_px(r, canvas) -> float:
    pressure = r.pressure
    peak = max(pressure) if isinstance(pressure, (list, tuple)) and pressure else 1.0
    return float(r.params.get("size", 0.0)) * canvas.long_side * float(peak)


def _value_of_hex(hexcode: str) -> float:
    code = (hexcode or "#000000").lstrip("#")
    rgb = np.array([[[int(code[i:i + 2], 16) for i in (0, 2, 4)]]], dtype=np.uint8)
    return float(session_module._values_of(rgb)[0, 0])


def near_copies(discs: list, canvas, tol=(0.08, 0.12, 8.0, 0.04), least: int = 3) -> list:
    """The painter's candidate C1: groups of ``least`` or more near-copies, linked pairwise.

    Two marks are near-copies when their widths, lengths, directions and values are all
    within ``tol`` -- relative, relative, degrees, value -- read off the record: the
    width at the pressure's peak, the chord, its angle, the colour's value. A direction
    is not compared between two marks shorter than they are wide: a dab has none.
    """
    props = []
    for r in discs:
        length, angle = session_module._mark_length_and_angle(r, canvas)
        props.append((_width_px(r, canvas), length * canvas.long_side, angle,
                      _value_of_hex(r.color_hex)))
    n = len(props)
    root = list(range(n))

    def find(i):
        while root[i] != i:
            root[i] = root[root[i]]
            i = root[i]
        return i

    for i in range(n):
        for j in range(i + 1, n):
            (wi, li, ai, vi), (wj, lj, aj, vj) = props[i], props[j]
            if abs(wi - wj) > tol[0] * max(wi, wj):
                continue
            if abs(li - lj) > tol[1] * max(li, lj, 1e-9) and max(li, lj) > 0.5:
                continue
            if min(li, lj) >= max(wi, wj):
                off = abs(ai - aj) % 180.0
                if min(off, 180.0 - off) > tol[2]:
                    continue
            if abs(vi - vj) > tol[3]:
                continue
            root[find(i)] = find(j)
    groups: dict[int, list] = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(discs[i])
    return [g for g in groups.values() if len(g) >= least]


def _shaped(r) -> bool:
    return isinstance(r.pressure, (list, tuple)) or len(r.points) >= 3


def disc_fires(marks, canvas) -> dict[str, list]:
    """What each disc candidate counts on one pass: the marks it would name."""
    discs = session_module._discs(marks, canvas)
    out = {"engine": discs if len(discs) >= 3 else []}
    plain = [r for r in discs if not _shaped(r)]
    out["exempt shaped"] = plain if len(plain) >= 3 else []
    out["near-copies"] = [r for g in near_copies(discs, canvas) for r in g]
    out["near-copies, loose"] = [r for g in near_copies(discs, canvas,
                                                        (0.12, 0.20, 12.0, 0.06))
                                 for r in g]
    return out


def _path_px(r, canvas, every: float = 2.0) -> np.ndarray:
    pts = np.asarray(r.points, dtype=np.float64).reshape(-1, 2) * [canvas.width,
                                                                     canvas.height]
    if len(pts) < 2:
        return pts
    out = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:], strict=True):
        n = max(1, int(np.hypot(*(b - a)) / every))
        out.extend(a + (b - a) * (k / n) for k in range(1, n + 1))
    return np.asarray(out)


def _touching(group: list, canvas) -> list:
    """The largest set of ``group``'s marks joined footprint to footprint."""
    paths = [_path_px(r, canvas) for r in group]
    half = [float(r.params.get("size", 0.0)) * canvas.long_side / 2.0 for r in group]
    n = len(group)
    root = list(range(n))

    def find(i):
        while root[i] != i:
            root[i] = root[root[i]]
            i = root[i]
        return i

    for i in range(n):
        for j in range(i + 1, n):
            d = np.hypot(*(paths[i][:, None, :] - paths[j][None, :, :]).transpose(2, 0, 1))
            if float(d.min()) <= half[i] + half[j]:
                root[find(i)] = find(j)
    sets: dict[int, list] = {}
    for i in range(n):
        sets.setdefault(find(i), []).append(group[i])
    return max(sets.values(), key=len) if sets else []


def bars_fires(marks, canvas) -> dict[str, list]:
    """The stack-of-bars rule as the engine asks it (without its decay), and touching."""
    long_marks = []
    for r in marks:
        length, angle = session_module._mark_length_and_angle(r, canvas)
        if length >= 2.0 * float(r.params.get("size", 0.0)) and length > 0.0:
            long_marks.append((r, angle))
    bars = session_module._one_per_scumble(long_marks)
    best: list = []
    for _, centre in bars:
        near = [(r, a) for r, a in bars
                if min(abs(a - centre), 180.0 - abs(a - centre)) <= 6.0]
        if len(near) > len(best):
            best = near

    def fires(group) -> bool:
        return (len(group) >= 12 and len(group) >= 0.6 * len(bars)
                and len({session_module._call_of(r) for r in group}) >= 2)

    stack = [r for r, _ in best]
    out = {"engine": stack if fires(stack) else []}
    joined = _touching(stack, canvas) if out["engine"] else []
    out["touching"] = joined if fires(joined) else []
    return out


def graded_fires(marks, canvas) -> dict[str, list]:
    """The graded-passage rule as the engine asks it, and with a mass's passes as one."""
    long_marks = []
    for r in marks:
        length, angle = session_module._mark_length_and_angle(r, canvas)
        if length >= 2.0 * float(r.params.get("size", 0.0)) and length > 0.0:
            long_marks.append((r, angle))
    band = session_module._graded_band(long_marks, canvas)
    laid = band[4] if band else []
    units = {session_module._call_of(r): r for r in laid}
    colours = {r.color_hex for r in units.values()}
    hand = [r for r in laid if not r.params.get("via")]
    keep = len(units) >= 5 and len(colours) >= 3 and len({r.color_hex for r in hand}) >= 3
    return {"engine": laid, "a mass as one": laid if keep else []}


def probe_rules(kept: Kept) -> None:
    """4C: the three rules and their candidates, pass by pass over the corpus."""
    heading("4C: the disc, bars and graded rules, over every committed pass")
    passes = committed(kept)
    tally: dict[tuple[str, str], int] = {}
    named: dict[tuple[str, str], list[str]] = {}
    for p in passes:
        canvas = canvas_of(p)
        for rule, fires in (("disc", disc_fires(p["marks"], canvas)),
                            ("bars", bars_fires(p["marks"], canvas)),
                            ("graded", graded_fires(p["marks"], canvas))):
            for cand, marks in fires.items():
                if marks:
                    tally[(rule, cand)] = tally.get((rule, cand), 0) + 1
                    named.setdefault((rule, cand), {})[
                        f"{p['painting']}/{p['pass']}"] = len(marks)
    print(f"  {len(passes)} committed passes over {len({p['painting'] for p in passes})} "
          f"paintings")
    rows = [[rule, cand, n] for (rule, cand), n in sorted(tally.items())]
    print(table(rows, ["rule", "candidate", "passes it fires on"]))
    for rule in ("disc", "bars", "graded"):
        base = named.get((rule, "engine"), {})
        for (r, cand), where in sorted(named.items()):
            if r != rule or cand == "engine":
                continue
            kept_ = [x for x in where if x in base]
            lost = sorted(set(base) - set(where))
            print(f"  {rule}, {cand}: keeps {len(kept_)} of {len(base)}; drops "
                  f"{len(lost)}: " + (", ".join(f"{x} ({base[x]})" for x in lost) or "none"))
            fewer = [f"{x} ({base[x]} to {where[x]})" for x in kept_ if where[x] < base[x]]
            if fewer:
                print(f"    and names fewer marks on {len(fewer)}: {', '.join(fewer)}")
    engine_said = sum(1 for p in passes for f in p["findings"] if "one disc printed" in f)
    print(f"  (the engine's own findings, with the bars rule's decay: disc on "
          f"{engine_said} passes, bars on "
          f"{sum(1 for p in passes for f in p['findings'] if 'stack of bars' in f)}, "
          f"graded on "
          f"{sum(1 for p in passes for f in p['findings'] if 'graded passage' in f)})")
    uk = [p for p in passes if p["painting"] == "uktarl"]
    print("  on Uktarl's Room, pass by pass (marks named by each candidate):")
    for p in uk:
        canvas = canvas_of(p)
        d = disc_fires(p["marks"], canvas)
        b = bars_fires(p["marks"], canvas)
        g = graded_fires(p["marks"], canvas)
        said = [f"{k} {len(v)}" for k, v in d.items() if v]
        said += [f"bars/{k} {len(v)}" for k, v in b.items() if v]
        said += [f"graded/{k} {len(v)}" for k, v in g.items() if v]
        if said:
            print(f"    {p['pass']:<22} disc/" + ", ".join(said))
    for path in disagreement_sheets(kept):
        print(f"  sheet: {path}")


_FOLDERS = {entry.name: entry.folder for entry in cohort.CORPUS}


def _marks_crop(painting: str, marks: list, size: int = 220) -> Image.Image:
    """The finished painting round a set of marks, at 1:1 or larger, ``size`` across."""
    rgb = Image.open(_FOLDERS[painting] / "painting.png").convert("RGB")
    w, h = rgb.size
    pts = np.concatenate([np.asarray(r.points, dtype=np.float64).reshape(-1, 2)
                          for r in marks]) * [w, h]
    (x0, y0), (x1, y1) = pts.min(axis=0) - 16, pts.max(axis=0) + 16
    side = max(x1 - x0, y1 - y0, 48.0)
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    box = (int(max(cx - side / 2, 0)), int(max(cy - side / 2, 0)),
           int(min(cx + side / 2, w)), int(min(cy + side / 2, h)))
    crop = rgb.crop(box)
    scale = size / max(crop.size)
    return crop.resize((max(1, int(crop.width * scale)), max(1, int(crop.height * scale))),
                       Image.NEAREST if scale >= 1 else Image.LANCZOS)


def disagreement_sheets(kept: Kept) -> list[Path]:
    """Where a candidate and the engine disagree, cropped from the finished paintings.

    For the painter's batch 2: each pass the engine's disc rule fires on, round the marks
    it names, labelled by whether the near-copies candidate keeps it; and the same for the
    bars and graded rules' candidates. The finished picture, not the canvas as the pass
    left it -- a later pass may cover a mark, which the label does not say.
    """
    sheets = []
    for rule, fires, cand in (("disc", disc_fires, "near-copies"),
                              ("bars", bars_fires, "touching"),
                              ("graded", graded_fires, "a mass as one")):
        panels = []
        for p in committed(kept):
            said = fires(p["marks"], canvas_of(p))
            if not said["engine"]:
                continue
            verdict = "kept" if said[cand] else "dropped"
            label = f"{p['painting']}/{p['pass'][:18]}: {verdict}"
            panels.append((label, _marks_crop(p["painting"], said["engine"])))
        if panels:
            sheets.append(save_sheet(panels, f"rules_{rule}.png", columns=6))
    return sheets


def probe_versions(rb: bell.Rebuilt) -> None:
    """G1 and G2 on the two recovered versions the verdict priced: the facets, the V."""
    heading("G1 and G2 on the recovered versions")
    prelude = UKTARL / "prelude.py"
    for label, version in (("p03_mountain.py", "p03_v1_facets.py"),
                           ("p06_uktarl_body.py", "p06_v1_collar.py")):
        kept = Kept(engine=easel.__version__)
        _KEEPING[:] = [kept]
        _PAINTING[0] = "uktarl"
        try:
            with pricing():
                bell.run_pass(rb.opened(label), UKTARL / "versions" / version, prelude)
        finally:
            _KEEPING.clear()
        rows = [[m["place"] or "-", str(m["direction"])[:24], m["given"], m["axis"],
                 f"{m['given'] / max(m['axis'], 1):.1f}",
                 "G1" if m["single"] and m["given"] > 2.5 * max(m["axis"], 1) else "",
                 m["lines"], m["pieces"],
                 "G2" if m["lines"] and m["pieces"] - m["lines"] >= m["lines"] / 3 else ""]
                for m in kept.masses]
        print(f"  {version}: {sum(m['given'] for m in kept.masses)} strokes in "
              f"{len(kept.masses)} shaped masses")
        print(table(rows, ["place", "direction", "given", "axis", "ratio", "G1", "passes",
                           "pieces", "G2"], indent="    "))


def probe_standing(kept: Kept) -> None:
    """C5: the standing lines a pass prints word for word as the pass before printed them."""
    heading("C5: standing lines repeated from the pass before, over the corpus")
    by_painting: dict[str, list[dict]] = {}
    for p in committed(kept):
        by_painting.setdefault(p["painting"], []).append(p)
    rows = []
    total = same = 0
    for painting, passes in by_painting.items():
        last: dict[str, str] = {}
        n = k = 0
        for p in passes:
            for line in p["report"]:
                body = line.strip()
                word = body.split(" ", 1)[0]
                if word in STANDING:
                    n += 1
                    k += last.get(word) == body
                    last[word] = body
        rows.append([painting, len(passes), n, k, f"{k / max(n, 1):.0%}"])
        total += n
        same += k
    print(table(rows, ["painting", "passes", "standing lines", "same as before", "share"]))
    print(f"  over the corpus: {same} of {total} ({same / max(total, 1):.0%}) word for word "
          "the line before; printed only on change, those lines go")


# -- 4G: what a mass is charged for its direction ----------------------------------------

def probe_direction(kept: Kept) -> None:
    """G1, G2 and G3 over the corpus."""
    heading("G1: a single direction given, priced against the mass's own axis")
    single = [m for m in kept.masses if m["single"]]
    over = [m for m in single if m["given"] > 2.5 * max(m["axis"], 1)]
    print(f"  {len(kept.masses)} shaped masses; {len(single)} with one direction given; "
          f"{len(over)} of those over 2.5x their axis price")
    rows = [[m["painting"], m["pass"], m["place"] or "-", m["direction"], m["given"],
             m["axis"], f"{m['given'] / max(m['axis'], 1):.1f}"]
            for m in sorted(over, key=lambda m: -m["given"] / max(m["axis"], 1))]
    print(table(rows, ["painting", "pass", "place", "direction", "given", "axis", "ratio"]))
    ratios = [m["given"] / max(m["axis"], 1) for m in single]
    print(f"  ratio over the {len(single)}: median {bell.pct(ratios, 50):.2f}, "
          f"p90 {bell.pct(ratios, 90):.2f}, max {max(ratios):.1f}")

    heading("G2: masses whose passes come back in pieces")
    pieced = [m for m in kept.masses
              if m["lines"] and (m["pieces"] - m["lines"]) >= m["lines"] / 3.0]
    print(f"  {len(pieced)} of {len(kept.masses)} shaped masses have a third or more of "
          f"their passes in two or more pieces")
    rows = [[m["painting"], m["pass"], m["place"] or "-", m["direction"], m["lines"],
             m["pieces"], m["given"]]
            for m in sorted(pieced, key=lambda m: -(m["pieces"] - m["lines"]))[:25]]
    print(table(rows, ["painting", "pass", "place", "direction", "passes", "pieces",
                       "strokes"]))
    print(f"  {len({m['painting'] for m in pieced})} paintings; strokes in those masses: "
          f"{sum(m['given'] for m in pieced)}")

    heading("G3: mass passes that land nothing because they fall outside a clip")
    rows = []
    for painting in sorted({p["painting"] for p in kept.passes}):
        outside = [r for p in committed(kept) if p["painting"] == painting
                   for r in p["marks"]
                   if r.params.get("via") and r.params.get("clip") is not None
                   and float(r.paint) == 0.0]
        if outside:
            passes = {p["pass"] for p in committed(kept) if p["painting"] == painting
                      for r in p["marks"] if r in outside}
            rows.append([painting, len(outside), len(passes)])
    print(table(rows, ["painting", "mass passes laying no paint, held", "in committed passes"]))
    print(f"  {sum(r[1] for r in rows)} strokes over {len(rows)} paintings. A skip keeps "
          "every later mark only if it keeps the index (a record still logged, uncharged) "
          "and draws the pass's wander from the stream: a stroke's texture is seeded from "
          "its log index (Session._stroke_rng) and a mass's wander from self.rng between "
          "passes (_shape_paths)")


# -- 4H: a light in a picture that is dark on purpose ----------------------------------

def probe_key(kept: Kept) -> None:
    """H2: what the line would say, pass by pass, where it says *no clear light*."""
    heading("H2: 'no clear light' beside a light named in the plan, over the corpus")
    rows = []
    for painting in sorted({p["painting"] for p in kept.passes}):
        passes = [p for p in committed(kept) if p["painting"] == painting and p["values"]]
        unlit = [p for p in passes if not p["key"]
                 and p["values"]["high"] < p["values"]["middle"]]
        named = [p for p in unlit if p["light"]]
        clear = [p for p in named if p["light"]["bright"] - p["light"]["rest"] >= 0.10]
        if unlit:
            first = clear[0]["pass"] if clear else "-"
            last = clear[-1]["light"] if clear else None
            rows.append([painting, len(passes), len(unlit), len(named), len(clear), first,
                         f"{last['bright']:.2f} vs {last['rest']:.2f}" if last else "-"])
    print(table(rows, ["painting", "passes", "no clear light", "with a light named",
                       "H2 names it", "first", "last reading"]))
    keyed = sorted({p["painting"] for p in committed(kept) if p["key"]})
    print(f"  paintings that declared a key: {', '.join(keyed) or 'none'}")


# -- 4I: the reading path -----------------------------------------------------------------

READING = ("PAINTER.md", "RECIPES.md", "REFERENCE.md")


def _sections(text: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    title, body = "(top)", []
    for line in text.splitlines():
        if line.startswith("## "):
            out.append((title, "\n".join(body)))
            title, body = line[3:].strip(), []
        else:
            body.append(line)
    out.append((title, "\n".join(body)))
    return out


def _words(text: str) -> int:
    return len(re.findall(r"\S+", text))


def _engine_shingles(n: int = 6) -> set[tuple[str, ...]]:
    """Every run of ``n`` words in a string the engine can print: what a notice says."""
    said = set()
    for path in (ROOT / "src" / "easel").glob("*.py"):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                words = re.findall(r"[a-z0-9']+", node.value.casefold())
                said.update(tuple(words[i:i + n]) for i in range(len(words) - n + 1))
    return said


def probe_reading() -> None:
    """4I: the three files the painter read, section by section, against the notices."""
    heading("4I: the reading path, section by section")
    said = _engine_shingles()
    total = 0
    for name in READING:
        text = (ROOT / name).read_text(encoding="utf-8")
        words = _words(text)
        total += words
        rows = []
        for title, body in _sections(text):
            w = re.findall(r"[a-z0-9']+", body.casefold())
            shingles = [tuple(w[i:i + 6]) for i in range(len(w) - 5)]
            echoed = sum(1 for s in shingles if s in said) / max(len(shingles), 1)
            rows.append([title[:52], _words(body), f"{echoed:.0%}"])
        print(f"  {name}: {words} words")
        print(table(sorted(rows, key=lambda r: -r[1]),
                    ["section", "words", "said by the engine too"], indent="    "))
    print(f"  the three files: {total} words (the painter read 28,538 of them on 2026-10-01)")
    painter = (ROOT / "PAINTER.md").read_text(encoding="utf-8")
    cuts = ("And six failures, painted", "When you think it is finished")
    for _title, body in _sections(painter):
        for line in body.splitlines():
            if line.startswith("### ") and any(c.casefold() in line.casefold() for c in cuts):
                print(f"  answer H's cut: {line[4:].strip()}")
    for sentence in ("Say a place; do not compute a coordinate", "You cannot reason in pixels"):
        print(f"  '{sentence}': {'present' if sentence in painter else 'absent'} in PAINTER.md")


# -- the run ----------------------------------------------------------------------------

BENCHES = (
    ("claims", "the rebuild, against the painter's export"),
    ("clip-out", "4A: the backlight laid with an exclusion, against the three regions"),
    ("answers", "the painter's measured answers, re-measured"),
    ("soft", "4B: the soft hold on the edges of answer B, per hold; blind sheets"),
    ("join", "P9: the step across each face's terminator, as painted"),
    ("shares", "4F: the shares line, pass by pass, under the painter's split"),
    ("rules", "4C: the disc, bars and graded candidates, and C5, over the corpus"),
    ("direction", "4G: G1, G2 and G3 over the corpus"),
    ("key", "4H: H2 over the corpus's plans with a named light"),
    ("reading", "4I: the reading path's inventory"),
    ("answers2", "the second answers' measured claims, re-measured"),
)
_NEEDS_REBUILD = {"claims", "clip_out", "answers", "soft", "join", "shares", "answers2"}
_NEEDS_CORPUS = {"rules", "direction", "key"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    for flag, what in BENCHES:
        parser.add_argument(f"--{flag}", action="store_true", help=what)
    parser.add_argument("--corpus", action="store_true",
                        help="replay the corpus afresh and keep it in out/uktarl/corpus.pkl")
    args = parser.parse_args(argv)
    if args.corpus:
        kept = corpus(fresh=True)
        print(f"  kept {len(kept.passes)} passes and {len(kept.masses)} masses in {CACHE}")
    chosen = {k for k, v in vars(args).items() if v and k != "corpus"}
    if args.corpus and not chosen:
        return 0
    run = {flag.replace("-", "_") for flag, _ in BENCHES} if not chosen else chosen
    print("Uktarl's Room's round, measured. Engine "
          f"{easel.__version__} from {Path(easel.__file__).parent}", flush=True)
    rb = bell.rebuild("uktarl") if run & _NEEDS_REBUILD else None
    if "claims" in run:
        probe_claims(rb)
    if "clip_out" in run:
        probe_clip_out(rb)
    if "answers" in run:
        probe_reports()
        probe_cape_edge(rb)
        probe_rotation()
        probe_spent(rb)
    if "soft" in run:
        probe_soft(rb)
    if "join" in run:
        probe_join(rb)
    if "answers2" in run:
        probe_answers2(rb)
    if "shares" in run:
        probe_shares(rb)
    kept = corpus() if run & _NEEDS_CORPUS else None
    if "rules" in run:
        probe_rules(kept)
        probe_standing(kept)
    if "direction" in run:
        probe_direction(kept)
        probe_versions(rb or bell.rebuild("uktarl"))
    if "key" in run:
        probe_key(kept)
    if "reading" in run:
        probe_reading()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
