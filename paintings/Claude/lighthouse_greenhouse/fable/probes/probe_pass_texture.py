"""Peak-to-peak of the pass structure, measured on the committed painting.

Re-measures a claim this session first got wrong. The tower's solid flat block-in reads
at ~0.03 peak-to-peak -- exactly what the docs promise for solid block_in, so the docs
are right. What actually stripes is the far sea, a scumble laid with a flat over a wide
band, at ~0.11 -- the flat brush's wander scalloping the band, a texture cost the
"quiet gradient" recipe does not mention.

Run: .venv/bin/python probes/probe_pass_texture.py
"""
import os

import numpy as np
from PIL import Image

from easel import Session

HERE = os.path.dirname(os.path.abspath(__file__))
PNG = os.path.join(HERE, "..", "painting.png")


def profile(img, x0, x1, y0, y1, axis, value_of):
    band = img[int(y0 * 768):int(y1 * 768), int(x0 * 1024):int(x1 * 1024), :]
    line = band.mean(axis=axis)                       # mean colour per column or per row
    v = np.array([value_of(c) for c in line])
    t = np.arange(len(v))
    resid = v - np.polyval(np.polyfit(t, v, 1), t)    # detrend, so the ramp is not counted
    return v.mean(), resid.std(), resid.max() - resid.min()


if __name__ == "__main__":
    img = np.asarray(Image.open(PNG).convert("RGB")).astype(float) / 255.0
    pal = Session(64, 48, seed=1).palette
    def value_of(c):
        return pal.value_of("#" + "".join(f"{int(round(x * 255)):02x}" for x in c))
    cases = [
        ("tower lit face  (solid flat block-in), across", 0.617, 0.647, 0.645, 0.685, 0),
        ("tower shadow side (solid flat block-in), across", 0.668, 0.695, 0.645, 0.685, 0),
        ("far sea  (scumble with flat, wide band), down", 0.25, 0.35, 0.66, 0.80, 1),
        ("fog  (scumble, wide band), down", 0.25, 0.35, 0.06, 0.20, 1),
    ]
    for name, *args in cases:
        m, sd, p2p = profile(img, *args, value_of)
        print(f"{name:48s} mean {m:.3f}  sd {sd:.3f}  peak-to-peak {p2p:.3f}")
    print("\nExpected: tower faces ~0.01-0.03 (as documented); far sea ~0.11 (the real stripes).")
