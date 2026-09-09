"""Rendered width of a round_hard line against its nominal size, measured on the
fresh first part of the stroke (columns 130-250 of a stroke starting at x=120),
and the same with run-out disabled. White smooth ground, 1200 px long side."""
import numpy as np
from PIL import Image
from easel import Session

W = 1200
sizes = (0.03, 0.02, 0.012, 0.008, 0.006, 0.005, 0.004, 0.003, 0.002)
for ff in (None, 0.0):
    s = Session(W, 800, texture="smooth", ground="white", seed=1, out_dir="out/small", timelapse=False)
    kw = {} if ff is None else {"load_falloff": ff}
    for i, sz in enumerate(sizes):
        y = 0.08 + i * 0.1
        s.stroke([(0.1, y), (0.9, y)], "round_hard", "ultramarine", size=sz, pressure="even", load=1.0, **kw)
    s.export("out/small/lines.png")
    im = np.asarray(Image.open("out/small/lines.png").convert("L")).astype(float)
    ground = im[5, 5]
    print(f"== round_hard lines, load_falloff={'default' if ff is None else ff} ==")
    for i, sz in enumerate(sizes):
        y = int((0.08 + i * 0.1) * 800)
        fresh = ground - im[y - 40:y + 40, 130:250]
        tail = ground - im[y - 40:y + 40, 900:1020]
        wf = (fresh > 8).sum(axis=0).mean()
        wt = (tail > 8).sum(axis=0).mean()
        nominal = sz * W
        print(f"  size {sz:.3f} = {nominal:5.1f} px: fresh width {wf:4.1f} px ({wf / nominal:.2f}x), peak {fresh.max() / ground:.2f}"
              f" | tail width {wt:4.1f} px, peak {tail.max() / ground:.2f}")
