p = s.palette
s.dry()
# the pool is a floor with light on it, not a firework
s.stroke([(0.10,0.985),(0.34,0.955),(0.50,0.940)], "bristle", "spill", size=0.055,
         load=1.0, opacity=0.45, pressure="swell")
s.stroke([(0.92,0.985),(0.70,0.955),(0.56,0.940)], "bristle", "spill", size=0.050,
         load=1.0, opacity=0.40, pressure="swell")
s.stroke([(0.20,0.905),(0.44,0.892)], "bristle", "spill", size=0.030, load=1.0,
         opacity=0.30, pressure="taper")
# the two accidental bars on the wall
s.stroke([(0.44,0.244),(0.70,0.252),(0.90,0.262)], "bristle", "wall", size=0.055,
         load=1.0, opacity=0.75, pressure="even")
s.stroke([(-0.04,0.268),(0.16,0.278),(0.32,0.286)], "bristle", "wall", size=0.050,
         load=1.0, opacity=0.70, pressure="even")
# light bouncing off the floor back onto the wall, low down
s.stroke([(0.18,0.836),(0.34,0.832)], "bristle", "wall_l", size=0.030, load=1.0,
         opacity=0.40, pressure="swell")
s.stroke([(0.82,0.836),(0.66,0.832)], "bristle", "wall_l", size=0.026, load=1.0,
         opacity=0.32, pressure="swell")
# the door is ajar: the two sides are not the same
s.stroke([(-0.05,0.06),(0.06,0.42),(-0.02,0.78)], "bristle", "wall_d", size=0.16,
         load=1.0, opacity=0.45, pressure="swell")
s.stroke([(0.20,0.10),(0.26,0.40)], "bristle", "wall_d", size=0.09, load=1.0,
         opacity=0.28, pressure="taper")
print("total", s.stroke_count)
s.stroke([(0.040,0.966),(0.056,0.984),(0.086,0.952)], "liner", "spill", size=0.006,
         load=1.0, pressure=[0.9,1.0,0.4], note="signature")
print(s.look())
