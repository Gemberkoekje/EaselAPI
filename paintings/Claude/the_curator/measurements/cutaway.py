import numpy as np
from PIL import Image
from easel import Session
A = "/home/user/projects/the-curator/game/art/easel/"
s = Session(16, 16, ground="toned_grey", seed=1, out_dir=".")
p = s.palette
for name, rgb_path, cut_path, cells in (("candle", "candle/candle_rgb.png", A + "candle.png", ("D", "E", 1, 2)),
                                         ("patron", "../cand/patron_rgb.png", A + "patron_default.png", ("D", "E", 1, 3))):
    rgb = np.asarray(Image.open(rgb_path).convert("RGB"))
    a = np.asarray(Image.open(cut_path).convert("RGBA"))[:, :, 3]
    H, W = a.shape
    out = a == 0
    med = np.median(rgb[out], axis=0).astype(int)
    hx = "#%02x%02x%02x" % tuple(med)
    c0, c1, r0, r1 = cells
    x0, x1 = int((ord(c0) - 65) * W / 8), int((ord(c1) - 64) * W / 8)
    y0, y1 = int((r0 - 1) * H / 8), int(r1 * H / 8)
    share = out[y0:y1, x0:x1].mean()
    print(f"{name}: cut-away {out.mean():.1%} of the canvas, its median colour {hx} value {p.value_of(hx):.2f}; "
          f"planned light {c0}{r0}:{c1}{r1} = x {x0}-{x1}, y {y0}-{y1}: {share:.0%} of it is cut away")
