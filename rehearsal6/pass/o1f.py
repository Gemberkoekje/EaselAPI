p = s.palette
p["rain"] = p.mix(p["squall2"], p["sky"], 0.55)
print("rain", p.hex(p["rain"]), round(p.value_of(p["rain"]),3))
# rain: it varies, it breaks, and it disappears for a whole passage
s.stroke([(0.02,0.560),(0.06,0.720)], "bristle", "rain", size=0.055, load=0.55,
         opacity=0.75, pressure="lift_off")
s.stroke([(0.11,0.588),(0.16,0.735)], "bristle", "rain", size=0.038, load=0.45,
         opacity=0.60, pressure="taper")
s.stroke([(0.19,0.566),(0.25,0.700)], "bristle", "squall2", size=0.070, load=0.6,
         opacity=0.55, pressure="lift_off")
s.stroke([(0.28,0.540),(0.33,0.690)], "bristle", "rain", size=0.030, load=0.40,
         opacity=0.55, pressure="swell")
s.stroke([(0.36,0.515),(0.42,0.680)], "bristle", "rain", size=0.048, load=0.50,
         opacity=0.45, pressure="lift_off")
s.stroke([(0.47,0.474),(0.52,0.606)], "bristle", "rain", size=0.026, load=0.35,
         opacity=0.40, pressure="taper")
s.stroke([(0.05,0.640),(0.30,0.700)], "bristle", "rain", size=0.030, load=0.5,
         opacity=0.40, pressure="swell")
s.stroke([(0.60,0.420),(0.63,0.490)], "bristle", "rain", size=0.020, load=0.35,
         opacity=0.30, pressure="taper")
print("rain", s.stroke_count)
# where the rain meets the sea there is no edge at all
s.smudge([(0.10,0.700),(0.14,0.716)], size=0.040)
s.smudge([(0.30,0.688),(0.34,0.702)], size=0.036)
s.smudge([(0.42,0.672),(0.46,0.688)], size=0.032)
# the light does not stop at a wall
s.stroke([(0.40,0.596),(0.46,0.640),(0.50,0.672)], "round_hard", "sky", size=0.040,
         load=1.0, opacity=0.55, pressure="even")
s.smudge([(0.44,0.618),(0.48,0.652)], size=0.038)
print("total", s.stroke_count)
print(s.look())
