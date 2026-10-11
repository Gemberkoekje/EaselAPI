import numpy as np
from PIL import Image
from easel import Session, polygon

def width_profile(path, x_edge, y0, y1, outside, inside):
    im = np.asarray(Image.open(path).convert("L")).astype(float)
    ws = []
    for y in range(y0, y1):
        row = im[y, x_edge - 8:x_edge + 9]
        lo, hi = row[:3].mean(), row[-3:].mean()
        if hi - lo < 40:
            continue
        t = (row - lo) / (hi - lo)
        def cross(level):
            for i in range(len(t) - 1):
                if t[i] < level <= t[i + 1]:
                    return i + (level - t[i]) / (t[i + 1] - t[i])
            return None
        a, b = cross(0.1), cross(0.9)
        if a is not None and b is not None:
            ws.append(b - a)
    ws = np.array(ws)
    return len(ws), np.median(ws), np.percentile(ws, 10), np.percentile(ws, 90)

for W, H, brush, size, edge, label in ((400, 620, "flat", 0.03, "hard", "patron size, flat 0.03, edge=hard"),
                                       (400, 620, "bristle", 0.06, None, "patron size, bristle 0.06, default edge, solid"),
                                       (120, 300, "flat", 0.03, "hard", "candle size, flat 0.03, edge=hard")):
    s = Session(W, H, texture="linen", ground="umber_wash", seed=5, budget=50, out_dir=".")
    p = s.palette
    light = p.at_value(p.mix("titanium_white", "yellow_ochre", 0.14), 0.82)
    place = polygon([(0.3, 0.2), (0.7, 0.2), (0.7, 0.8), (0.3, 0.8)])
    kw = dict(density=1.0, size=size, solid=True, direction="vertical")
    if edge:
        kw["edge"] = edge
    s.block_in(place, brush, light, **kw)
    s.export("held.png")
    n, med, p10, p90 = width_profile("held.png", int(0.3 * W), int(0.3 * H), int(0.7 * H), 0, 0)
    print(f"{label:48s} rows {n:3d}  10-90% width median {med:4.2f} px  (10th-90th pct {p10:4.2f}-{p90:4.2f})")
