"""Why do these pictures come out as horizontal bands? Two hypotheses, one probe.

REHEARSAL6's owner asked where the seascape bias comes from. `THE_BOAT_AGAIN.md`
proposes that it is not a subject preference at all -- twenty-four bare sessions have
named a subject and none named a seascape -- but something the engine makes cheap. Two
candidate mechanisms, and they predict different things about the stroke log:

**H1, the vocabulary.** The named regions that span the canvas are all full-width
horizontal bands and `horizon(y)` is a primitive, so a painter naming a big place gets
a band. This predicts banding concentrated in `block_in` passes over named regions.

**H2, the brush geometry.** Proposed by N3's painter, unprompted, about its own
picture:

    oriented tips end in a chisel, so any stroke that terminates inside the picture
    leaves a visible square end -- which forced me to run every stroke off both canvas
    edges, which at a shallow angle means horizontal. Repeat that eight times and you
    have bands. [...] Nobody chose that; the brush's geometry chose it.

This predicts something H1 does not: **strokes deliberately ending outside the canvas**,
and the effect concentrated in the oriented tips (`flat`, `bristle`, `knife`) rather
than the round ones, which have no chisel to hide.

So this measures, per session and weighted by paint actually laid:

- **off-canvas termination** -- a stroke whose first or last point is at or past an edge
- **angle** -- share of paint within 10 degrees of horizontal against within 10 of
  vertical
- both split by **oriented tip against round tip**, which is the split that separates
  the two hypotheses

Nothing here is a verdict. It says which mechanism the pictures are consistent with.

Run from the repo root:  python rehearsal6/name_then_paint/probe_stroke_geometry.py
"""
from __future__ import annotations

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SESSIONS = f"{ROOT}/rehearsal6/sessions"

#: Tips held square to their travel. The guide's own words: "an oriented tip is held
#: square to its travel, so a horizontal stroke necessarily ends on a vertical edge".
ORIENTED = ("flat", "bristle", "knife")
#: How close to an edge counts as running off it.
EDGE = 0.005
#: Degrees from an axis that count as aligned to it, matching probe_axis_alignment.
TOLERANCE = 10.0


def _paint_strokes(log: list) -> list:
    return [r for r in log
            if r["kind"] in ("stroke", "glaze", "smudge") and (r.get("points") or [])]


def _angle(points: list) -> float | None:
    """The stroke's overall direction, in degrees from horizontal, 0-90."""
    (x0, y0), (x1, y1) = points[0], points[-1]
    dx, dy = x1 - x0, y1 - y0
    if abs(dx) < 1e-9 and abs(dy) < 1e-9:
        return None
    return abs(math.degrees(math.atan2(dy, dx))) % 180.0


def measure(path: str, label: str) -> None:
    if not os.path.exists(path):
        print(f"  {label:<32} (missing)")
        return
    with open(path, encoding="utf-8") as handle:
        log = json.load(handle)["log"]

    rows = {"oriented": [0.0, 0.0, 0.0, 0.0], "round": [0.0, 0.0, 0.0, 0.0]}
    for record in _paint_strokes(log):
        points = record["points"]
        tip = str(record.get("params", {}).get("tip", record.get("brush", "")))
        key = "oriented" if any(t in tip for t in ORIENTED) else "round"
        # Weight by paint laid: the structure of a picture is made by its big masses,
        # and counting marks equally would let a hundred accents outvote six block-ins.
        weight = float(record.get("paint", 0.0)) or 1.0
        rows[key][0] += weight

        off = any(c <= EDGE or c >= 1.0 - EDGE
                  for c in (points[0][0], points[0][1], points[-1][0], points[-1][1]))
        if off:
            rows[key][1] += weight
        angle = _angle(points)
        if angle is None:
            continue
        if angle <= TOLERANCE or angle >= 180.0 - TOLERANCE:
            rows[key][2] += weight
        elif abs(angle - 90.0) <= TOLERANCE:
            rows[key][3] += weight

    total = rows["oriented"][0] + rows["round"][0]
    print(f"  {label}")
    for key in ("oriented", "round"):
        paint, off, horiz, vert = rows[key]
        if paint <= 0:
            print(f"    {key:<9} (no paint)")
            continue
        print(f"    {key:<9} {100 * paint / max(total, 1):5.1f} % of paint   "
              f"ends off-canvas {100 * off / paint:5.1f} %   "
              f"horizontal {100 * horiz / paint:5.1f} %   "
              f"vertical {100 * vert / paint:5.1f} %")


if __name__ == "__main__":
    print("Stroke geometry, from the saved session logs. Weighted by paint laid.\n")
    print("H1 (vocabulary) predicts banding without off-canvas termination.")
    print("H2 (chisel ends) predicts strokes run off the edges, oriented tips most.\n")

    for name, label in [
        ("name_then_paint-n1", "N1  pot of peonies, bare table (the clean test)"),
        ("name_then_paint-n2", "N2  geraniums on a windowsill"),
        ("name_then_paint-n3", "N3  teacup on a windowsill  (+23.78 dB)"),
        ("name_then_paint-n4", "N4  rosemary on a windowsill"),
        ("pass-own1", "R6 unprompted 1, the seascape  (+8.12 dB)"),
        ("pass-own2", "R6 unprompted 2, structure broken  (-9.52 dB)"),
        ("pass-copy", "R6 the mug copy, from a photograph"),
        ("sitter-copy", "R6 the sitter copy, from a photograph"),
    ]:
        measure(f"{SESSIONS}/{name}.json", label)
        print()
