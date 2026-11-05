"""The cut's edge, built from the places' coverage and softened to a width, against the shipped cuts.

Coverage at k x k samples: the share of a pixel's k x k sample points, each at its sub-pixel's centre, inside the outline.
Width: the edges.py measure, pixels with alpha between 10% and 90%, over the outline's length; the
length is the sum of the alpha's gradient magnitude at 16 x 16 samples (for an edge that goes 0 to 1,
that integral is its length). soften=w: a Gaussian on the 4 x 4 coverage, its sigma solved so the
width comes out w.
"""
import json, sys
import numpy as np
from PIL import Image
A = "/home/user/projects/the-curator/game/art/easel/"
S = "/tmp/claude-0/-home-user-projects/effc84d7-d7e9-5d60-848f-887f6f888335/scratchpad/"
OUT = sys.argv[1] if len(sys.argv) > 1 else "."

def coverage(shape, w, h, k):
    """The share of k x k sample points inside the shape, each point at the centre of its sub-pixel."""
    off = (np.arange(k) + 0.5) / k
    ys = (np.arange(h)[:, None] + off[None, :]).reshape(-1)
    xs = (np.arange(w)[:, None] + off[None, :]).reshape(-1)
    X, Y = np.meshgrid(xs, ys)
    inside = shape(X, Y)
    return inside.reshape(h, k, w, k).mean(axis=(1, 3))

def polygon_test(poly):
    P = np.asarray(poly, dtype=np.float64)
    def test(X, Y):
        res = np.zeros(X.shape, dtype=bool)
        for (x0, y0), (x1, y1) in zip(P, np.roll(P, -1, axis=0)):
            if y0 == y1:
                continue
            cond = (Y >= min(y0, y1)) & (Y < max(y0, y1))
            xint = x0 + (Y - y0) * (x1 - x0) / (y1 - y0)
            res ^= cond & (X < xint)
        return res
    return test

def length(shape, w, h):
    u = coverage(shape, w, h, 16)
    gy, gx = np.gradient(u)
    return float(np.hypot(gx, gy).sum())

def width(alpha, L):
    return float(((alpha >= 0.1) & (alpha <= 0.9)).sum()) / L

def gauss(a, sigma):
    if sigma <= 1e-3:
        return a
    r = int(np.ceil(4 * sigma))
    x = np.arange(-r, r + 1)
    k = np.exp(-x * x / (2 * sigma * sigma)); k /= k.sum()
    p = np.pad(a, r, mode="edge")
    p = np.apply_along_axis(lambda v: np.convolve(v, k, mode="valid"), 1, p)
    return np.apply_along_axis(lambda v: np.convolve(v, k, mode="valid"), 0, p)

def solve(a, L, target):
    lo, hi = 0.0, 3.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if width(gauss(a, mid), L) < target: lo = mid
        else: hi = mid
    return (lo + hi) / 2

def polys(path, names=None):
    o = json.load(open(path))
    tests = [polygon_test(o[n]) for n in (names or sorted(o))]
    return lambda X, Y: np.logical_or.reduce([t(X, Y) for t in tests])

def arch_hole(X, Y):            # cut_arch.py's opening (the alpha is its complement)
    cx, cy, r, bottom = 960, 400, 260, 720
    return ((X - cx) ** 2 + (Y - cy) ** 2 <= r * r) | ((X >= cx - r) & (X <= cx + r) & (Y >= cy) & (Y <= bottom + 10))

pieces = {
    "doorway wall": (A + "doorway_wall.png", arch_hole, True, (1920, 720)),
    "patron": (A + "patron_default.png", polys(S + "art/patron/outline.json", ["cloak", "hood"]), False, (400, 620)),
    "candle": (A + "candle.png", polys(S + "cand/outline.json"), False, (120, 300)),
}
results = {}
print(f"{'piece':13s} {'outline':>8s} {'shipped':>8s} {'2x2':>6s} {'4x4':>6s} {'sigma for 0.85':>15s} {'sigma for 2.5':>14s}  share kept: shipped / 4x4 / 0.85")
for name, (png, shape, hole, (w, h)) in pieces.items():
    shipped = np.asarray(Image.open(png).convert("RGBA"))[:, :, 3].astype(np.float64) / 255
    L = length(shape, w, h)
    c2, c4 = coverage(shape, w, h, 2), coverage(shape, w, h, 4)
    if hole:
        c2, c4 = 1 - c2, 1 - c4
    s085, s25 = solve(c4, L, 0.85), solve(c4, L, 2.5)
    soft085, soft25 = gauss(c4, s085), gauss(c4, s25)
    results[name] = dict(shipped=shipped, c2=c2, c4=c4, soft085=soft085, soft25=soft25)
    print(f"{name:13s} {L:8.0f} {width(shipped, L):8.2f} {width(c2, L):6.2f} {width(c4, L):6.2f} {s085:15.2f} {s25:14.2f}  "
          f"{shipped.mean():.4f} / {c4.mean():.4f} / {soft085.mean():.4f}")
np.savez_compressed(f"{OUT}/alphas.npz", **{f"{n}|{k}": v for n, d in results.items() for k, v in d.items()})
