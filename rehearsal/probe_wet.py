from easel import Region, Session
import numpy as np

# 1) single stroke of blue, then yellow straight over it -- maximally wet
s = Session(800, 300, ground="white", seed=21)
s.stroke([(0.1, 0.5), (0.9, 0.5)], "flat", "ultramarine", size=0.25, pressure="even")
w_after_one = float(s.canvas.wetness.max())
s.stroke([(0.15, 0.5), (0.85, 0.5)], "flat", "cadmium_yellow", size=0.12, pressure="even")
mid = s.canvas.rgb[150, 400]
print("one blue stroke -> max wetness", round(w_after_one, 3))
print("  yellow-over-wet hex:", s.palette.hex(tuple(mid)))

# 2) what the exercise actually does: block_in the halves, then measure wetness
s2 = Session(800, 400, ground="white", seed=4)
top, bottom = Region(0, 0, 1, 0.5), Region(0, 0.5, 1, 1)
n0 = s2.stroke_count
s2.block_in(top, "flat", "ultramarine", density=1.0, size=0.12)
s2.block_in(bottom, "flat", "ultramarine", density=1.0, size=0.12)
print("block_in strokes used:", s2.stroke_count - n0)
print("  wetness top  (supposedly wet):", round(float(s2.canvas.wetness[:200].max()), 3),
      " mean", round(float(s2.canvas.wetness[:200].mean()), 3))
s2.dry(1.0, region=bottom)
print("  wetness bottom (dried):      ", round(float(s2.canvas.wetness[200:].max()), 3))
