# The brush was the weakest passage in the finished picture, and there were 115 strokes
# in hand. Measured across it, the committed canvas read 0.53 0.59 0.58 0.51 0.56 0.60
# at the top and the same flat noise in the middle: light and dark distributed as
# stripes, with no form at all. That is why it read as a curtain rather than a cylinder.
#
# Two things were tried and thrown away first. A scumble across the whole mass buried
# the strip-gaps into a smooth wash, and the strips are the best thing here. A ramp at
# low opacity and a starved load laid almost nothing -- 0.62 to 0.56 across the whole
# width. What works is a bristle pushed hard: a comb cannot bury, it leaves the old
# paint showing between its streaks however high the opacity goes, so form can go on
# over texture without replacing it.
import numpy as np
def prof(tag):
    v = s.canvas.rgb @ np.array([0.2126, 0.7152, 0.0722])
    v = np.where(v <= 0.0031308, v*12.92, 1.055*np.power(np.maximum(v,1e-9),1/2.4)-0.055)
    h, w = v.shape
    for y0, y1, ytag in [(0.05, 0.25, "top"), (0.30, 0.50, "middle"), (0.52, 0.72, "low")]:
        print(f"  {tag:6s} {ytag:6s} " + " ".join(
            f"{x:.2f}:{v[int(y0*h):int(y1*h), int(x*w)-12:int(x*w)+12].mean():.2f}"
            for x in (0.74, 0.78, 0.82, 0.86, 0.90, 0.94)))
prof("before")

# The turning side. lift_off so each pass is heaviest at the top, where the arch light
# makes the form read, and trails away at the bottom where the mass is meant to dissolve
# into the dash -- the low band already ramped the other way and that merge is right.
for x, op, size in [(0.848, 0.35, 0.046), (0.888, 0.55, 0.046),
                    (0.926, 0.68, 0.044), (0.966, 0.78, 0.042)]:
    s.stroke([(x + 0.016, -0.04), (x - 0.018, 0.38), (x + 0.012, 0.74)],
             "bristle", "brush_sh", size=size, opacity=op, load=0.85, pressure="lift_off")

# The leading edge, the side facing the bloom.
s.stroke([(0.757, 0.04), (0.737, 0.38), (0.763, 0.68)], "bristle", "foam",
         size=0.044, opacity=0.52, load=0.85, pressure="swell")
s.stroke([(0.797, 0.16), (0.783, 0.52)], "bristle", "foam",
         size=0.030, opacity=0.32, load=0.80, pressure="taper")
prof("after")

# The outer pass runs to x 0.987 and the right pillar's edge sits at 0.951, so paint has
# been laid across the pillar. It goes back on top because it is nearer: this is the
# "keep each mass in its own function and re-run the stack in depth order" repair, and
# it is why the masses are functions in prelude.py at all.
s.paint({"shape": pillar_r(), "brush": "flat", "color": "frame", "size": 0.024,
         "direction": "axis", "density": 1.0, "load": 1.0, "load_falloff": 0.0,
         "edge": "clean"})
print(s.look())
