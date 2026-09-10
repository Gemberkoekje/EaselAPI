p = s.palette
# rain, as the comb of a bristle brush: it is the right tool for it
for pts, col, sz, op, pr in [
        ([(0.02,0.43),(0.085,0.97)], "rain",    0.150, 0.24, "lift_off"),
        ([(0.16,0.46),(0.235,0.93)], "rain",    0.115, 0.21, "lift_off"),
        ([(0.29,0.49),(0.355,0.86)], "squall2", 0.090, 0.19, "lift_off"),
        ([(0.41,0.48),(0.455,0.78)], "rain",    0.065, 0.15, "lift_off"),
        ([(0.09,0.52),(0.14,0.84)],  "squall2", 0.048, 0.16, "taper"),
        ([(0.235,0.55),(0.28,0.74)], "rain",    0.036, 0.14, "taper"),
        ([(0.50,0.50),(0.525,0.71)], "rain",    0.040, 0.10, "lift_off")]:
    s.stroke(pts, "bristle", col, size=sz, load=1.0, opacity=op, pressure=pr)
print("rain", s.stroke_count)
# the sea in front of the rain, on its own slope
s.stroke([(-0.03,0.905),(0.32,0.938),(0.66,0.972)], "bristle", "water_d", size=0.075,
         load=1.0, opacity=0.65, pressure="even")
s.stroke([(-0.03,0.985),(0.40,1.01)], "bristle", "water_d", size=0.060, load=1.0,
         opacity=0.55, pressure="taper")
s.stroke([(0.18,0.828),(0.52,0.852)], "bristle", "water_d", size=0.040, load=1.0,
         opacity=0.35, pressure="swell")
s.stroke([(0.60,0.905),(0.95,0.930)], "bristle", "water_d", size=0.055, load=1.0,
         opacity=0.40, pressure="taper")
# the light running out of the gap toward the viewer, broken by the swell
s.stroke([(0.80,0.712),(0.755,0.792)], "bristle", "glow2", size=0.024, load=1.0,
         opacity=0.55, pressure="lift_off")
s.stroke([(0.775,0.800),(0.735,0.856)], "bristle", "water_l", size=0.038, load=1.0,
         opacity=0.45, pressure="swell")
s.stroke([(0.725,0.884),(0.688,0.960)], "bristle", "water_l", size=0.050, load=1.0,
         opacity=0.30, pressure="taper")
s.stroke([(0.88,0.746),(0.955,0.782)], "bristle", "water_l", size=0.022, load=1.0,
         opacity=0.40, pressure="taper")
print("total", s.stroke_count)
print(s.look())
