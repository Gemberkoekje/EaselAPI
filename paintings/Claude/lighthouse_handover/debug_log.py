import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import load
from easel import polygon
s, ns = load(); c = s.scratch(); p = c.palette
mid = polygon([(-0.06, 0.17), (1.06, 0.15), (1.06, 0.45), (-0.06, 0.47)])
recs = c.scumble(mid, "high", "pale", 8, direction=-2, brush="flat", opacity=0.95, jitter=0.01, size_jitter=0.03)
for r in recs:
    pts = getattr(r, "points", None)
    d = {k: getattr(r, k) for k in ("brush", "size", "opacity", "load", "note") if hasattr(r, k)}
    print(type(r).__name__, [tuple(round(v, 3) for v in pt) for pt in (pts[:1] + pts[-1:] if pts else [])], len(pts or []), d)
print([a for a in dir(recs[0]) if not a.startswith("_")])
