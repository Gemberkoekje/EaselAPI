# My worst passage against my best one, in one painting, by CALIBRATION's own
# measure: the across-band profile's one-step wobble.
import numpy as np
from easel import Session
# The session this painting was made in. It is not committed -- a .easel is a
# regenerable intermediate and is ignored -- so run this from the working directory
# that holds it, or rebuild one from prelude.py and the passes beside this file.
s = Session.load("heron.easel")
W, H = s.size
img = s.canvas.rgb
lin = img if img.max() <= 1.0 else img / 255.0
v = 0.2126 * lin[..., 0] + 0.7152 * lin[..., 1] + 0.0722 * lin[..., 2]
v = np.where(v <= 0.0031308, v * 12.92, 1.055 * np.power(np.clip(v, 1e-8, None), 1/2.4) - 0.055)

def profile(x0, x1, y0, y1, label, step_px, sizes):
    col = v[int(y0*H):int(y1*H), int(x0*W):int(x1*W)].mean(axis=1)
    d = np.diff(col)                      # one-step wobble of the across-band profile
    ripple = float(np.std(d)) * step_px   # scaled to one pass step, as the table does
    print(f"{label}")
    print(f"   span {col.min():.3f}-{col.max():.3f}   ripple over one step {ripple:.4f}")
    print(f"   brushes in steps: {[round(sz*W/step_px, 1) for sz in sizes]}")

step_dawn = 0.0185 * H            # my hand-laid dawn strokes stepped 0.0185 of height
profile(0.045, 0.175, 0.215, 0.365, "DAWN BAND  (7 strokes, brushes chosen by hand)",
        step_dawn, [0.058, 0.052, 0.046, 0.040, 0.034, 0.028, 0.024])

step_sky = (0.5 / 11) * H         # the sky scumble: 11 passes over 0.5 of height
profile(0.045, 0.175, 0.020, 0.200, "SKY        (scumble n=11, brush picked by the verb)",
        step_sky, [3 * 0.5 / 11])
