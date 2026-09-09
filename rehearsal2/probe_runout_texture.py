"""Run-out again, this time on each texture, with a pale colour on a toned ground
(the case that speckled in the rehearsal), for two brush sizes."""
import numpy as np
from PIL import Image
from easel import Session

def coverage(s, path, y0, y1):
    s.export(path)
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    ground = im[2, 2]
    m = (np.abs(im - ground).sum(axis=2) > 40)[y0:y1, :]
    return m.mean(axis=0)

for texture in ("smooth", "linen", "rough"):
    for size in (0.10, 0.20):
        for ff in (None, 0.25):
            s = Session(1000, 500, texture=texture, ground="toned_grey", seed=1)
            kw = {} if ff is None else {"load_falloff": ff}
            s.stroke([(0.02, 0.5), (0.98, 0.5)], "bristle", s.palette.tint("yellow_ochre", 0.6),
                     size=size, load=1.0, pressure="even", **kw)
            h = int(size * 1000 * 0.4)
            cov = coverage(s, "out/probe_runout_tex.png", 250 - h, 250 + h)
            segs = [cov[int(a * 1000):int(b * 1000)].mean() for a, b in ((0.05, 0.2), (0.3, 0.45), (0.55, 0.7), (0.8, 0.95))]
            label = "default" if ff is None else f"falloff={ff}"
            print(f"  {texture:6s} size={size:.2f} {label:12s}: coverage by quarter "
                  + "  ".join(f"{c:.2f}" for c in segs))
