"""Measure two things the guide does not state: how far block_in paints beyond its
region, and how far a loaded brush travels before it runs dry. Public API + PNG only."""
import numpy as np
from PIL import Image
from easel import Session, Region

def painted_mask(s, path):
    s.export(path)
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    ground = np.asarray(Image.open(path).convert("RGB"))[2, 2].astype(int)
    return (np.abs(im - ground).sum(axis=2) > 40)

print("== block_in overshoot (region 0.3-0.7 both axes, white ground) ==")
for brush, size in (("bristle", 0.10), ("flat", 0.10), ("bristle", 0.05), ("round_hard", 0.08)):
    s = Session(1000, 1000, ground="white", seed=1)
    s.block_in(Region(0.3, 0.3, 0.7, 0.7), brush, "ultramarine", density=1.0, size=size)
    m = painted_mask(s, "out/probe_overshoot.png")
    ys, xs = np.where(m)
    x0, x1, y0, y1 = xs.min() / 1000, xs.max() / 1000, ys.min() / 1000, ys.max() / 1000
    over = max(0.3 - x0, x1 - 0.7, 0.3 - y0, y1 - 0.7)
    print(f"  {brush:10s} size={size:.2f}: painted x {x0:.3f}-{x1:.3f}, y {y0:.3f}-{y1:.3f}; "
          f"overshoot {over:.3f} = {over / size:.2f} brush sizes, {s.stroke_count} strokes")

print("== run-out: one horizontal stroke, size 0.10, from x=0.02 to 0.98 ==")
for brush in ("bristle", "flat", "round_hard"):
    for ff in (None, 0.5, 0.25, 0.0):
        s = Session(1000, 500, ground="white", seed=1)
        kw = {} if ff is None else {"load_falloff": ff}
        s.stroke([(0.02, 0.5), (0.98, 0.5)], brush, "ultramarine", size=0.10, load=1.0, pressure="even", **kw)
        m = painted_mask(s, "out/probe_runout.png")
        band = m[200:300, :]                       # the stroke's own height
        cov = band.mean(axis=0)                     # coverage per column
        full = cov[40:120].mean()
        # first column (after the start) where coverage drops below half of the initial coverage
        idx = np.where(cov[120:] < 0.5 * full)[0]
        half = (120 + idx[0]) / 1000 if len(idx) else None
        end_cov = cov[880:960].mean()
        label = "default" if ff is None else f"falloff={ff}"
        print(f"  {brush:10s} {label:12s}: start coverage {full:.2f}, end coverage {end_cov:.2f}, "
              f"half-coverage at x={half if half is None else round(half, 2)} "
              f"({'never' if half is None else f'{(half - 0.02) / 0.10:.1f} brush sizes'})")
