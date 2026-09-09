"""Two things that cost me strokes, each shown with a measurement.

Run with plain python:  python defect_demo.py
Nothing here reads the engine's source; it paints, exports a PNG, and measures
the PNG with Pillow.

A. `block_in` overhang is ASYMMETRIC, and the vertical figure in the guide is
   right for the top edge and 2x low for the bottom.
   PAINTER.md: "a region blocked in at size=0.1 comes out roughly 0.05 wider
   than you asked on the sides and 0.025 taller." Measured on 1200x810: sides
   0.050 / 0.042 (accurate), top 0.032, bottom 0.058. So a mass blocked in above
   something else drops more than twice as far onto it as the guide says, and
   you cannot inset symmetrically to compensate.

B. A `bristle` stroke at `load=1.0` does not cover dry opaque paint.
   PAINTER.md: "anything that has to read as a *solid mass* ... wants to stay up
   there. Pass `load=1.0` explicitly when you are covering." It also says a
   bristle covers "about three-quarters of its width" - but the two sentences
   are 40 lines apart and the first one is the one you remember when a mark you
   meant as a correction leaves the old colour showing through. It cost me three
   passes on the ear.
"""
from PIL import Image
from easel import Session, cell, region

W, H = 1200, 810


def bbox_of_dark(path, thresh=110):
    im = Image.open(path).convert("L")
    px = im.load()
    xs, ys = [], []
    for y in range(0, im.height, 2):
        for x in range(0, im.width, 2):
            if px[x, y] < thresh:
                xs.append(x)
                ys.append(y)
    return min(xs), min(ys), max(xs), max(ys)


print("=" * 68)
print("A. block_in overhang, 1200x810 canvas, one cell, size=0.10")
print("=" * 68)
s = Session(W, H, ground="white", texture="smooth", seed=1)
s.palette["k"] = s.palette.mix("ultramarine", "burnt_umber", 0.5)
s.block_in(cell("D4"), "flat", "k", density=1.0, size=0.10)
s.export("demo_a.png")
x0, y0, x1, y1 = bbox_of_dark("demo_a.png")
ax0, ay0, ax1, ay1 = 0.375 * W, 0.375 * H, 0.500 * W, 0.500 * H
print("cell D4 asked for : x %.0f..%.0f  y %.0f..%.0f  (px)" % (ax0, ax1, ay0, ay1))
print("paint actually at : x %d..%d  y %d..%d  (px)" % (x0, x1, y0, y1))
print("spill left/right  : %.0f / %.0f px  = %.3f / %.3f of canvas width"
      % (ax0 - x0, x1 - ax1, (ax0 - x0) / W, (x1 - ax1) / W))
print("spill top/bottom  : %.0f / %.0f px  = %.3f / %.3f of canvas height"
      % (ay0 - y0, y1 - ay1, (ay0 - y0) / H, (y1 - ay1) / H))
print("-> guide says 'roughly 0.05 wider on the sides and 0.025 taller'.")
print("   Sides check out. Top is 0.032; the BOTTOM is 0.058, over twice the")
print("   quoted figure, and the spill is not symmetric top-to-bottom.")
print()

print("=" * 68)
print("B. bristle at load=1.0 over dry opaque paint")
print("=" * 68)
s2 = Session(600, 400, ground="white", texture="linen", seed=2)
p = s2.palette
p["under"] = p.mix("cadmium_yellow", "titanium_white", 0.10)      # bright
p["over"] = p.mix("ultramarine", "burnt_umber", 0.50)             # dark
s2.block_in(region("all"), "flat", "under", density=1.0, size=0.20)
s2.dry()
s2.stroke([(0.10, 0.30), (0.90, 0.30)], "bristle", "over",
          size=0.16, load=1.0, load_falloff=0.0, pressure="even")
s2.stroke([(0.10, 0.72), (0.90, 0.72)], "flat", "over",
          size=0.16, load=1.0, load_falloff=0.0, pressure="even")
s2.export("demo_b.png")
im = Image.open("demo_b.png").convert("RGB")
pw, ph = im.size


def mean_band(y_lo, y_hi):
    px = im.load()
    tot = n = 0
    for y in range(int(ph * y_lo), int(ph * y_hi)):
        for x in range(int(pw * 0.25), int(pw * 0.75)):
            r, g, b = px[x, y]
            tot += 0.2126 * r + 0.7152 * g + 0.0722 * b
            n += 1
    return tot / n / 255.0


print("under-colour  %s value %.2f" % (p.hex(p["under"]), p.value_of(p["under"])))
print("over-colour   %s value %.2f" % (p.hex(p["over"]), p.value_of(p["over"])))
print("bristle band  measured value %.2f" % mean_band(0.26, 0.34))
print("flat band     measured value %.2f" % mean_band(0.68, 0.76))
print("-> same colour, same load, same size: the bristle band sits well above")
print("   the paint's own value because a quarter of the bright under-colour is")
print("   still showing. Use `flat` when the point of the stroke is to cover.")
