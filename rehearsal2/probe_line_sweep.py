import numpy as np
from PIL import Image
from easel import Session
W = 1200
sizes = [round(0.0015 + 0.0005 * i, 4) for i in range(24)]      # 0.0015 .. 0.013
s = Session(W, 1600, texture="smooth", ground="white", seed=1, out_dir="out/small", timelapse=False)
for i, sz in enumerate(sizes):
    y = 0.03 + i * 0.04
    s.stroke([(0.1, y), (0.9, y)], "round_hard", "ultramarine", size=sz, pressure="even", load=1.0)
s.export("out/small/sweep.png")
im = np.asarray(Image.open("out/small/sweep.png").convert("L")).astype(float)
ground = im[5, 5]
logs = s.log().splitlines()
for i, sz in enumerate(sizes):
    y = int((0.03 + i * 0.04) * 1600)
    band = ground - im[y - 25:y + 25, 200:1000]           # the whole stroke, not one column
    widths = (band > 8).sum(axis=0)                         # per column
    print(f"size {sz:.4f} = {sz * W:5.1f} px  width min/mean/max {widths.min():2d}/{widths.mean():4.1f}/{widths.max():2d}"
          f"  peak {band.max() / ground:.2f}  {logs[i].split(' ', 4)[-1]}")
