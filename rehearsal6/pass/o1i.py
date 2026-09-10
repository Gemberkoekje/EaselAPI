p = s.palette
s.dry()
# 1. the light must not end at a wall, and must not have a lid
s.stroke([(0.395,0.605),(0.435,0.648),(0.470,0.686)], "bristle", "rain", size=0.055,
         load=1.0, opacity=0.55, pressure="swell")
s.stroke([(0.44,0.578),(0.60,0.566),(0.76,0.560)], "bristle", "rain", size=0.030,
         load=1.0, opacity=0.35, pressure="swell")
s.stroke([(0.62,0.548),(0.84,0.540),(1.02,0.544)], "bristle", "mid1", size=0.026,
         load=1.0, opacity=0.30, pressure="taper")
s.stroke([(0.50,0.640),(0.66,0.628)], "bristle", "mid2", size=0.020, load=1.0,
         opacity=0.40, pressure="taper")
# light getting up under the cloud's base
s.stroke([(0.66,0.402),(0.86,0.352),(1.02,0.318)], "bristle", "mid1", size=0.024,
         load=1.0, opacity=0.30, pressure="swell")
s.stroke([(0.78,0.330),(0.98,0.290)], "bristle", "mid2", size=0.012, load=1.0,
         opacity=0.35, pressure="taper")
print("light", s.stroke_count)
# 2. take out the pale sticks and lay the reflection as broken dashes
s.stroke([(0.70,0.760),(0.84,0.772)], "bristle", "water_m", size=0.075, load=1.0,
         opacity=0.85, pressure="even")
s.stroke([(0.86,0.740),(0.99,0.766)], "bristle", "water_m", size=0.055, load=1.0,
         opacity=0.75, pressure="even")
for x, y, sz, op, col in [(0.795,0.716,0.030,0.75,"glow2"),(0.770,0.744,0.024,0.55,"glow"),
                          (0.806,0.762,0.018,0.45,"glow2"),(0.760,0.792,0.030,0.40,"water_l"),
                          (0.812,0.824,0.022,0.35,"water_l"),(0.742,0.856,0.040,0.30,"water_l"),
                          (0.800,0.902,0.028,0.22,"water_l"),(0.716,0.948,0.048,0.20,"water_l")]:
    s.stroke([(x-sz*0.9, y), (x+sz*0.9, y+0.006)], "bristle", col, size=sz*0.5,
             load=1.0, opacity=op, pressure="swell")
print("reflection", s.stroke_count)
# 3. cross the sea's ribbing
s.stroke([(0.02,0.760),(0.30,0.800),(0.58,0.836)], "bristle", "water_m", size=0.045,
         load=1.0, opacity=0.30, pressure="taper")
s.stroke([(0.40,0.960),(0.72,0.906)], "bristle", "water_d", size=0.038, load=1.0,
         opacity=0.30, pressure="swell")
s.stroke([(0.86,0.980),(1.02,0.940)], "bristle", "water_d", size=0.055, load=1.0,
         opacity=0.35, pressure="taper")
print("total", s.stroke_count)
print(s.look())
