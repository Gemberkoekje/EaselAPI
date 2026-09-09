"""Replicate the pass-1 sky exactly: block_in on rough, toned_warm_grey, size 0.2,
flat vs bristle, and measure coverage per pass-band by horizontal quarter."""
import numpy as np
from PIL import Image
from easel import Session, Region

for brush in ("flat", "bristle"):
    for ff in (None, 0.25):
        s = Session(1200, 800, texture="rough", ground="toned_warm_grey", seed=23)
        s.palette["sky"] = s.palette.tint(s.palette.mix("alizarin", "cerulean", 0.55), 0.80)
        kw = {} if ff is None else {"load_falloff": ff}
        s.block_in(Region(0.0, 0.0, 1.0, 0.57), brush, "sky", direction="horizontal", density=1.0, size=0.2, **kw)
        s.export("out/probe_blockin.png")
        im = np.asarray(Image.open("out/probe_blockin.png").convert("RGB")).astype(int)
        ground = np.asarray(Image.open("out/probe_blockin.png").convert("RGB"))[790, 600].astype(int)
        m = (np.abs(im - ground).sum(axis=2) > 40)
        label = "default" if ff is None else f"falloff={ff}"
        print(f"{brush:8s} {label:12s} {s.stroke_count} strokes; coverage of y 0.02-0.50 by x-quarter: "
              + "  ".join(f"{m[16:400, int(a * 1200):int(b * 1200)].mean():.2f}" for a, b in ((0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.0))))
        for rec in s.log().splitlines()[-4:] if isinstance(s.log(), str) else []:
            print("   ", rec)
