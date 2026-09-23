"""10a's measurement: the steep left edge of each mass on blind/q10_ground.png (enlarged x2),
per row, in canvas pixels. Run from the package root: python measure_ground_edges.py"""
import numpy as np
from PIL import Image

a = np.asarray(Image.open("blind/q10_ground.png").convert("RGB")).astype(float) / 255
L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
bg = a.sum(axis=2) < 3 * 40 / 255                      # the sheet's own dark background
cols, rows = np.where(~bg.all(axis=0))[0], np.where(~bg.all(axis=1))[0]
panels, start = [], cols[0]
for i, j in zip(cols, cols[1:]):
    if j != i + 1: panels.append((start, i)); start = j
panels.append((start, cols[-1]))
y0, y1, ENL = rows[0], rows[-1], 2.0
print("letter  wander sd  largest bite  in-between px (median)")
for letter, (x0, x1) in zip("ABCD", panels):
    P = L[y0:y1, x0:x1]
    lo, hi = np.percentile(P, 5), np.percentile(P, 95)       # the mass, the ground
    N = (P - lo) / (hi - lo)
    band = range(int(0.55 * P.shape[0]), int(0.92 * P.shape[0]))  # the steep left side
    pos, ys = [], []
    for y in band:
        k = np.where(N[y] < 0.5)[0]
        if len(k) == 0 or k[0] < 2: continue
        e = k[0]
        pos.append(e - 1 + (N[y, e - 1] - 0.5) / max(N[y, e - 1] - N[y, e], 1e-6)); ys.append(y)
    ys, pos = np.array(ys), np.array(pos)
    r = pos - np.polyval(np.polyfit(ys, pos, 1), ys)
    mid = ((N[band.start:band.stop, : P.shape[1] // 2] > 0.15) &
           (N[band.start:band.stop, : P.shape[1] // 2] < 0.85)).sum(axis=1)
    print(f"  {letter}     {r.std() / ENL:5.2f}      {np.abs(r).max() / ENL:5.2f}         {np.median(mid) / ENL:4.2f}")
