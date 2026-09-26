"""Question E: what each candidate reading says about the lantern, its panes and the face.

Reads the finished canvas through Easel's own values view, so a number here is what
look(values=True) shows. Places are the painting's own polygons, in its pixels.
"""
import numpy as np
from PIL import Image, ImageDraw
from easel import Session

# Run from this folder: the painting's session file sits one level up.
s = Session.load("../wenna.easel")
path = s.look(values=True, sketch=False, path="values.png")
v = np.asarray(Image.open(path).convert("L"), dtype=np.float64) / 255.0
H, W = v.shape


def mask(points):
    img = Image.new("L", (W, H), 0)
    ImageDraw.Draw(img).polygon([(x, y) for x, y in points], fill=1)
    return np.asarray(img, dtype=bool)


def T(x, y):
    return (300 + (x - 300) * 1.3, 146 + (y - 146) * 1.3 - 36)


face_pts = [T(x, y) for x, y in [
    (372, 205), (384, 212), (393, 228), (398, 245), (404, 258), (400, 268), (408, 282),
    (417, 298), (426, 314), (425, 320), (416, 326), (411, 331), (414, 340), (410, 346),
    (407, 350), (411, 356), (409, 364), (402, 370), (404, 380), (400, 392), (390, 400),
    (372, 398), (348, 392), (322, 380), (300, 362), (290, 350), (306, 318), (324, 285),
    (340, 255), (352, 232), (362, 216)]]
places = {
    "lantern (planned place)": [(560, 240), (636, 240), (634, 360), (562, 360)],
    "panes (inside the edge straps)": [(567, 243), (630, 243), (629, 357), (568, 357)],
    "panes' middle third": [(588, 270), (612, 270), (612, 340), (588, 340)],
    "face (whole)": face_pts,
    "fist (redrawn)": [(358, 482), (366, 466), (386, 458), (414, 455), (444, 454),
                       (470, 458), (486, 470), (490, 492), (486, 516), (474, 536),
                       (450, 548), (420, 552), (390, 548), (368, 536), (358, 514)],
}
print(f"{'place':32s} {'px':>6s} {'mean':>6s} {'median':>6s} {'p90':>6s} {'p95':>6s} {'p99':>6s} {'max':>6s}")
for name, pts in places.items():
    vals = v[mask(pts)]
    q = np.percentile(vals, [50, 90, 95, 99])
    print(f"{name:32s} {vals.size:6d} {vals.mean():6.3f} {q[0]:6.3f} {q[1]:6.3f} {q[2]:6.3f} {q[3]:6.3f} {vals.max():6.3f}")
print(f"\ncanvas: p95 {np.percentile(v, 95):.3f}; share above 0.60: {100 * (v > 0.60).mean():.2f}%; "
      f"above 0.66: {100 * (v > 0.66).mean():.2f}%")
