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
CLI's own ``run_script`` and keeps a copy of the canvas after each, and its corpus replay.
Every candidate is patched in for the length of one bench and never into the engine.

    python scripts/probe_uktarl_session.py              # every flag below
    python scripts/probe_uktarl_session.py --claims     # the rebuild, against the export
    python scripts/probe_uktarl_session.py --clip-out   # 4A: the backlight, held outside him
    python scripts/probe_uktarl_session.py --answers    # the painter's answers, re-measured

Pictures go to ``out/uktarl/``.
"""

from __future__ import annotations

import argparse
import contextlib
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_bell_session as bell  # noqa: E402
import probe_cohort_session as cohort  # noqa: E402

import easel  # noqa: E402
from easel import Session  # noqa: E402
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

    def patched(self, holds, feather_=0.0):
        cover = original(self, holds, feather_).copy()
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


# -- the run ----------------------------------------------------------------------------

BENCHES = (
    ("claims", "the rebuild, against the painter's export"),
    ("clip-out", "4A: the backlight laid with an exclusion, against the three regions"),
    ("answers", "the painter's measured answers, re-measured"),
)
_NEEDS_REBUILD = {"claims", "clip_out", "answers"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    for flag, what in BENCHES:
        parser.add_argument(f"--{flag}", action="store_true", help=what)
    args = parser.parse_args(argv)
    chosen = {k for k, v in vars(args).items() if v}
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
