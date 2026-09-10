p = s.palette
s.dry()
# bury both gold pillars - read off the grid this time, not guessed
s.stroke([(0.464,-0.04),(0.454,0.30),(0.439,0.62),(0.424,0.885)], "round_hard",
         "wall", size=0.078, load=1.0, pressure="even")
s.stroke([(0.566,-0.04),(0.578,0.30),(0.590,0.62),(0.601,0.885)], "round_hard",
         "wall", size=0.074, load=1.0, pressure="even")
print("buried", s.stroke_count)
# halation: one wide film centred on the slot, so it bleeds both ways at once
s.stroke([(0.518,-0.04),(0.522,0.30),(0.523,0.62),(0.527,0.885)], "round_hard",
         "spill", size=0.150, load=1.0, opacity=0.16, pressure="even")
s.stroke([(0.518,-0.04),(0.522,0.30),(0.523,0.62),(0.527,0.885)], "round_hard",
         "spill2", size=0.098, load=1.0, opacity=0.14, pressure="even")
print("halation", s.stroke_count)
# the wall is darker away from the light
s.stroke([(-0.05,0.10),(0.04,0.46),(-0.02,0.82)], "bristle", "wall_d", size=0.14,
         load=1.0, opacity=0.55, pressure="swell")
s.stroke([(1.05,0.10),(0.96,0.46),(1.02,0.82)], "bristle", "wall_d", size=0.14,
         load=1.0, opacity=0.55, pressure="swell")
s.stroke([(0.10,0.20),(0.16,0.58)], "bristle", "wall_d", size=0.10, load=1.0,
         opacity=0.35, pressure="taper")
s.stroke([(0.90,0.26),(0.84,0.62)], "bristle", "wall_d", size=0.10, load=1.0,
         opacity=0.35, pressure="taper")
# and it is plaster, which is not a stack of vertical bands
s.stroke([(0.06,0.34),(0.26,0.30),(0.36,0.33)], "bristle", "wall_l", size=0.030,
         load=0.8, opacity=0.28, pressure="swell")
s.stroke([(0.70,0.56),(0.86,0.60)], "bristle", "wall_l", size=0.024, load=0.8,
         opacity=0.22, pressure="taper")
s.stroke([(0.24,0.72),(0.34,0.66)], "bristle", "wall_l", size=0.038, load=0.9,
         opacity=0.20, pressure="lift_off")
s.stroke([(0.76,0.16),(0.92,0.13)], "bristle", "wall_l", size=0.020, load=0.7,
         opacity=0.25, pressure="taper")
print("total", s.stroke_count)
print(s.look())
