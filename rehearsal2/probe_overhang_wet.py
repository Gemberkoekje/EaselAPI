import numpy as np
from PIL import Image
from easel import Session, Region

def mask(s, path, ref=(2, 2)):
    s.export(path)
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    g = im[ref[0], ref[1]]
    return np.abs(im - g).sum(axis=2) > 40

print("== block_in overhang: region 0.3-0.7, bristle size 0.10, white ground ==")
for oh in (0.35, 0.0, 0.5):
    s = Session(1000, 1000, ground="white", seed=1)
    s.block_in(Region(0.3, 0.3, 0.7, 0.7), "bristle", "ultramarine", density=1.0, size=0.10, overhang=oh)
    m = mask(s, "out/probe_overhang.png")
    ys, xs = np.where(m)
    print(f"  overhang={oh}: painted x {xs.min()/1000:.3f}-{xs.max()/1000:.3f}, y {ys.min()/1000:.3f}-{ys.max()/1000:.3f}; "
          f"coverage inside region {m[300:700, 300:700].mean():.3f}")

print("== run-out of a full-width flat stroke, size 0.14, over a fresh block_in: wet vs dried ==")
for dry in (False, True):
    s = Session(1200, 800, texture="rough", ground="toned_warm_grey", seed=23)
    p = s.palette
    p["sky"] = p.tint(p.mix("alizarin", "cerulean", 0.55), 0.80)
    p["sky_hi"] = p.tint(p.mix("alizarin", "cerulean", 0.6), 0.9)
    s.block_in(Region(0.0, 0.0, 1.0, 0.57), "flat", "sky", direction="horizontal", density=1.0, size=0.2)
    if dry:
        s.dry()
    s.export("out/probe_before.png")
    before = np.asarray(Image.open("out/probe_before.png").convert("RGB")).astype(int)
    s.stroke([(0.0, 0.06), (0.5, 0.04), (1.0, 0.07)], "flat", "sky_hi", size=0.14, pressure="even")
    s.export("out/probe_after.png")
    after = np.asarray(Image.open("out/probe_after.png").convert("RGB")).astype(int)
    changed = (np.abs(after - before).sum(axis=2) > 12)[0:110, :]
    print(f"  {'dried' if dry else 'wet  '}: changed-pixel fraction by x-quarter "
          + "  ".join(f"{changed[:, int(a*1200):int(b*1200)].mean():.2f}" for a, b in ((0, .25), (.25, .5), (.5, .75), (.75, 1))))
    print("   ", s.log().splitlines()[-1])
