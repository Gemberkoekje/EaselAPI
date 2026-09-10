R = "/home/user/refs/Level1.jpg"
p = s.palette
s.dry()
# the foot: dark under the body, then the lit rim of the base on top of it
s.stroke([(0.372,0.628),(0.440,0.648),(0.510,0.646),(0.546,0.632)], "bristle",
         "sh_mid", size=0.030, load=1.0, pressure="even")
s.stroke([(0.384,0.610),(0.450,0.626)], "round_hard", "mug_dk", size=0.022,
         load=1.0, opacity=0.8, pressure="even")
s.stroke([(0.374,0.654),(0.424,0.670),(0.474,0.672),(0.520,0.662),(0.548,0.648)],
         "bristle", "mug_lit", size=0.016, load=1.0, pressure="swell")
s.stroke([(0.452,0.668),(0.508,0.660),(0.540,0.648)], "round_hard", "mug_hi",
         size=0.010, load=1.0, pressure="taper")
print("foot", s.stroke_count)
# the two bright smears left on the table beside the handle's shadow
s.stroke([(0.660,0.690),(0.720,0.664),(0.772,0.640)], "bristle", "wood_lit",
         size=0.055, load=1.0, opacity=0.55, pressure="even")
s.stroke([(0.690,0.752),(0.760,0.716),(0.800,0.700)], "bristle", "wood_mid",
         size=0.048, load=1.0, opacity=0.45, pressure="taper")
# the handle: kill the speckle, and the pale lump where it meets the body
s.stroke([(0.650,0.224),(0.702,0.250),(0.730,0.300),(0.726,0.362),(0.696,0.420)],
         "round_hard", "mug_lit", size=0.020, load=1.0, opacity=0.85, pressure="even")
s.stroke([(0.612,0.446),(0.634,0.458),(0.612,0.472)], "round_hard", "mug_shd",
         size=0.024, load=1.0, opacity=0.8, pressure="even")
s.stroke([(0.678,0.430),(0.646,0.454),(0.616,0.464)], "bristle", "mug_mid",
         size=0.020, load=1.0, pressure="taper")
# the left silhouette: table laid up to where the vessel stops
s.stroke([(0.278,0.300),(0.290,0.420),(0.308,0.540),(0.330,0.640)], "bristle",
         "wood_l2", size=0.032, load=1.0, pressure="even")
s.stroke([(0.292,0.268),(0.302,0.360),(0.316,0.470)], "bristle", "mug_lit",
         size=0.016, load=1.0, pressure="swell")
# the spoon runs down into the tea
s.stroke([(0.520,0.130),(0.508,0.196),(0.500,0.238)], "flat", "dk", size=0.028,
         load=1.0, pressure="even")
s.stroke([(0.512,0.014),(0.524,0.070)], "flat", "dk", size=0.030, load=1.0,
         pressure="even")
print("total", s.stroke_count)
print(s.look())
