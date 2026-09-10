"""M8's evidence: one composition laid twice, as boxes and as shapes.

The brief says a change that alters every painting is judged on the sampler *and* a
real painting, looked at. ``samples/shapes.png`` is the sampler half. This is the
other half, and it is a controlled pair rather than one picture: the same masses, the
same colours, the same seed, the same brushes, the same order of work. The only
difference is that one version fills each mass's *bounding rectangle* -- which is
all the engine could do before this milestone -- and the other fills the mass.

    python m8/paint_two_ways.py

Writes ``m8/boxes.png`` and ``m8/shapes.png``, and prints the axis-alignment share
from ``rehearsal3/probe_axis_alignment.py`` for both. That probe is the number the
brief names for whether a painting is built out of horizontal and vertical edges.

There is no subject here on purpose: the guide must not carry one, and neither
should the evidence for a change to the guide's own vocabulary.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from easel import Session, blob, hull, ribbon  # noqa: E402

OUT = Path(__file__).resolve().parent
SIZE = (900, 675)
SEED = 21


def masses():
    """The five masses, each with the silhouette it actually has."""
    return [
        # far, then nearer: painted back to front, as the guide says.
        ("ground", ribbon([(-0.05, 0.74), (0.45, 0.62), (1.05, 0.70)], 0.62), "far", 0.17,
         "axis", 0.85),
        ("rise", hull([(0.02, 0.62), (0.30, 0.30), (0.62, 0.40), (0.74, 0.66),
                       (0.10, 0.72)]), "mid", 0.13, "axis", 1.0),
        ("mass", blob((0.66, 0.45), 0.26, 0.30, wobble=0.30, seed=4), "dark", 0.11,
         ("axis", 118.0), 1.0),
        ("arm", ribbon([(0.16, 0.86), (0.42, 0.66), (0.63, 0.58)], 0.20, end_width=0.07),
         "dark", 0.075, "axis", 1.0),
        ("light", blob((0.30, 0.26), 0.17, 0.11, wobble=0.35, seed=9), "light", 0.06,
         "axis", 1.0),
    ]


def paint(as_boxes: bool) -> Session:
    s = Session(*SIZE, texture="linen", ground="toned_grey", seed=SEED, timelapse=True,
                out_dir=OUT)
    p = s.palette
    p["far"] = p.mix("cerulean", "titanium_white", 0.55)
    p["mid"] = p.mix("yellow_ochre", "burnt_umber", 0.45)
    p["dark"] = p.mix("ultramarine", "burnt_umber", 0.5)
    p["light"] = p.tint("yellow_ochre", 0.55)

    for name, shape, color, size, direction, density in masses():
        place = shape.box if as_boxes else shape
        s.block_in(place, "bristle", color, direction=direction, density=density,
                   size=size, note=f"{name}")

    # The same finishing pass on both: a few accents, smallest brush, fewest strokes.
    s.dry()
    s.stroke([(0.24, 0.30), (0.33, 0.24), (0.40, 0.27)], "flat", "light", size=0.035)
    s.stroke([(0.60, 0.36), (0.70, 0.30), (0.80, 0.34)], "flat", "light", size=0.03,
             opacity=0.6)
    s.dab(0.31, 0.25, brush="round_hard", color="light", size=0.022)
    return s


def main() -> int:
    sys.path.insert(0, str(ROOT / "rehearsal3"))
    spec = importlib.util.spec_from_file_location(
        "probe_axis", ROOT / "rehearsal3" / "probe_axis_alignment.py")
    probe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(probe)

    for label, as_boxes in (("boxes", True), ("shapes", False)):
        s = paint(as_boxes)
        path = s.export(OUT / f"{label}.png")
        s.timelapse_gif(OUT / f"{label}.gif")
        s.look(path=OUT / f"{label}_look.png", grid=True)
        s.look(path=OUT / f"{label}_values.png", values=True)
        share = probe.axis_share(str(path))
        print(f"{label:7s} {s.stroke_count:4d} strokes  "
              f"axis-aligned edges {share:5.1f}%  -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
