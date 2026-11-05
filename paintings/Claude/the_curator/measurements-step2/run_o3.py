"""Replays one painting script and measures every hand-laid stroke, as the bench's two candidates read them.

    python -I run_o3.py OUT.jsonl SCRIPT [script args...]

For each s.stroke() the script itself calls (not strokes laid inside block_in and the like):
  M2 (at the call): a round tip under its one-touch width (6.5 px round_hard or liner, 7.5 round_soft,
     4 px for an oriented tip) laid with a pressure list or opacity under 1.
  O3 (after): the mark's colour value lies 0.15 or more from the median value under its path, and the
     90th percentile, over the path, of how far each pixel moved toward that value is under 0.25.
The path is the stroke's points (Catmull-Rom through three or more, as smooth=True draws them) at the
brush's width. Values are the canvas's own value view (Canvas.values), read before and after the mark.
"""
import inspect, json, os, runpy, sys
import numpy as np
from PIL import Image, ImageDraw
import easel
from easel import Session

out_path, script, args = sys.argv[1], os.path.abspath(sys.argv[2]), sys.argv[3:]
WIDTH_OF = {"round_hard": 6.5, "liner": 6.5, "round_soft": 7.5}
CHISEL = 4.0
rows = []
orig = Session.stroke

def path_mask(canvas, pts, width, smooth):
    W, H = canvas.width, canvas.height
    p = np.array([[x * W, y * H] for x, y in pts], dtype=float)
    if smooth and len(p) >= 3:
        p = np.asarray(easel.catmull_rom(p, 24), dtype=float)
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    w = max(1, int(round(width)))
    d.line([tuple(q) for q in p], fill=255, width=w, joint="curve")
    r = width / 2
    for q in (p[0], p[-1]):
        d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=255)
    return np.asarray(m) > 0

def wrapped(self, points, *a, **kw):
    caller = inspect.stack()[1]
    direct = os.path.abspath(caller.filename) == script
    before = self.canvas.values(sketch=False).astype(np.float32) / 255 if direct else None
    rec = orig(self, points, *a, **kw)
    if not direct:
        return rec
    after = self.canvas.values(sketch=False).astype(np.float32) / 255
    c = self.canvas
    prm = rec.params
    width = prm["size"] * c.long_side
    tip = prm.get("tip", rec.brush)
    pressure = rec.pressure
    is_list = isinstance(pressure, (list, tuple))
    limit = WIDTH_OF.get(tip, CHISEL if tip in ("flat", "bristle", "knife") else None)
    m2 = limit is not None and width < limit and (is_list or prm["opacity"] < 1)
    mask = path_mask(c, rec.points, width, prm.get("smooth", True))
    vb, va = before[mask], after[mask]
    vc = float(self.palette.value_of(rec.color_hex))
    med = float(np.median(vb))
    gap = vc - vb
    ok = np.abs(gap) >= 0.02
    f90 = float(np.percentile((va[ok] - vb[ok]) / gap[ok], 90)) if ok.any() else float("nan")
    moved = np.abs(va - vb) * 255
    o3 = abs(vc - med) >= 0.15 and f90 < 0.25
    rows.append(dict(script=os.path.basename(script), args=" ".join(args), line=caller.lineno, note=rec.note,
                     tip=tip, width_px=round(width, 2), opacity=prm["opacity"], pressure=pressure if is_list else str(pressure),
                     colour=round(vc, 3), median_under=round(med, 3), distance=round(vc - med, 3), reach90=round(f90, 3),
                     levels_mean=round(float(moved.mean()), 1), levels_p90=round(float(np.percentile(moved, 90)), 1),
                     path_px=int(mask.sum()), M2=bool(m2), O3=bool(o3), points=[[round(x, 4), round(y, 4)] for x, y in rec.points]))
    return rec

Session.stroke = wrapped
sys.argv = [script] + args
try:
    runpy.run_path(script, run_name="__main__")
finally:
    with open(out_path, "a") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    print(f"{os.path.basename(script)} {' '.join(args)}: {len(rows)} hand-laid strokes", file=sys.stderr)
