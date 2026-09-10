p = s.palette
s.dry()
# broad veils, full load, translucent - rain that actually reaches the water
s.stroke([(0.03,0.44),(0.09,0.98)], "round_hard", "rain", size=0.135, load=1.0,
         opacity=0.50, pressure="even")
s.stroke([(0.19,0.47),(0.26,0.92)], "round_hard", "rain", size=0.095, load=1.0,
         opacity=0.42, pressure="even")
s.stroke([(0.31,0.50),(0.37,0.86)], "round_hard", "rain", size=0.070, load=1.0,
         opacity=0.34, pressure="even")
s.stroke([(0.43,0.48),(0.47,0.78)], "round_hard", "rain", size=0.050, load=1.0,
         opacity=0.26, pressure="even")
s.stroke([(0.11,0.52),(0.16,0.90)], "round_hard", "squall2", size=0.045, load=1.0,
         opacity=0.30, pressure="even")
print("veils", s.stroke_count)
# the lit edge of the squall, where the light gets under it
s.stroke([(0.50,0.470),(0.56,0.640),(0.58,0.700)], "round_hard", "mid1", size=0.035,
         load=1.0, opacity=0.45, pressure="even")
s.stroke([(0.55,0.520),(0.60,0.672)], "round_hard", "mid2", size=0.018, load=1.0,
         opacity=0.40, pressure="taper")
# the sea: a dark foreground, and the light running out of the gap toward us
s.stroke([(-0.02,0.930),(0.30,0.960),(0.62,0.985)], "bristle", "water_d", size=0.085,
         load=1.0, opacity=0.75, pressure="even")
s.stroke([(0.20,0.845),(0.52,0.870)], "bristle", "water_d", size=0.050, load=1.0,
         opacity=0.45, pressure="taper")
s.stroke([(0.79,0.712),(0.76,0.800),(0.71,0.900),(0.66,1.00)], "bristle", "water_l",
         size=0.060, load=1.0, opacity=0.55, pressure="lift_off")
s.stroke([(0.81,0.716),(0.79,0.782),(0.75,0.850)], "bristle", "glow2", size=0.026,
         load=1.0, opacity=0.55, pressure="lift_off")
s.stroke([(0.86,0.740),(0.92,0.800),(0.96,0.880)], "bristle", "water_l", size=0.035,
         load=1.0, opacity=0.35, pressure="taper")
print("sea", s.stroke_count)
print(s.look())
