"""Run-out measured strictly: fraction of pixels within the stroke's band that are
close to the stroke's own colour, per x-quarter. Replicates the pass-1 strokes."""
import numpy as np
from PIL import Image
from easel import Session, Region

def near(path, hexcol, y0, y1, tol=28):
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)[y0:y1]
    c = np.array([int(hexcol[i:i + 2], 16) for i in (1, 3, 5)])
    return (np.abs(im - c).max(axis=2) <= tol)

for texture in ("smooth", "linen", "rough"):
    for brush, size, ff in (("flat", 0.14, None), ("bristle", 0.12, None), ("bristle", 0.12, 0.25), ("bristle", 0.12, 0.0)):
        s = Session(1200, 800, texture=texture, ground="toned_warm_grey", seed=23)
        p = s.palette
        p["sky"] = p.tint(p.mix("alizarin", "cerulean", 0.55), 0.80)
        p["warm"] = p.tint(p.mix("yellow_ochre", "cadmium_red", 0.15), 0.72)
        s.block_in(Region(0.0, 0.0, 1.0, 0.57), "flat", "sky", direction="horizontal", density=1.0, size=0.2)
        kw = {} if ff is None else {"load_falloff": ff}
        s.stroke([(0.0, 0.40), (0.5, 0.39), (1.0, 0.41)], brush, "warm", size=size, load=1.0, pressure="even", **kw)
        s.export("out/probe_strict.png")
        h = int(size * 1200 * 0.3)
        m = near("out/probe_strict.png", p.hex(p["warm"]), 320 - h, 320 + h)
        label = "default" if ff is None else f"falloff={ff}"
        print(f"  {texture:6s} {brush:8s} size={size:.2f} {label:12s}: solid fraction by quarter "
              + "  ".join(f"{m[:, int(a*1200):int(b*1200)].mean():.2f}" for a, b in ((0, .25), (.25, .5), (.5, .75), (.75, 1))))
