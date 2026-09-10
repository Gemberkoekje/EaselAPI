p = s.palette
s.dry()
# opacity does not thin a long stroke. It buried the light. Put it back.
s.block_in(polygon([(0.508,-0.05),(0.546,-0.05),(0.553,0.885),(0.500,0.885)]),
           "flat", "blaze", direction=90, density=0.95, size=0.030, load=1.0,
           pressure="even")
print("core", s.stroke_count)
s.stroke([(0.503,-0.04),(0.499,0.40),(0.496,0.880)], "liner", "lit", size=0.010,
         load=1.0, pressure=[0.6,1.0,0.9])
s.stroke([(0.551,-0.04),(0.554,0.40),(0.557,0.880)], "liner", "lit", size=0.009,
         load=1.0, pressure=[0.5,0.9,1.0])
print("edges", s.stroke_count)
# the teeth and hard trapezoids along the floor line
s.stroke([(0.14,0.856),(0.30,0.876),(0.40,0.902)], "round_hard", "floor", size=0.060,
         load=1.0, opacity=0.9, pressure="even")
s.stroke([(0.86,0.856),(0.70,0.876),(0.60,0.902)], "round_hard", "floor", size=0.060,
         load=1.0, opacity=0.9, pressure="even")
s.stroke([(-0.05,0.848),(0.20,0.856)], "round_hard", "wall", size=0.050, load=1.0,
         opacity=0.9, pressure="even")
s.stroke([(1.05,0.848),(0.80,0.856)], "round_hard", "wall", size=0.050, load=1.0,
         opacity=0.9, pressure="even")
print("floor line", s.stroke_count)
# where the light strikes the floor it is hottest
s.stroke([(0.470,0.884),(0.512,0.878),(0.556,0.884)], "round_hard", "blaze",
         size=0.030, load=1.0, pressure="swell")
s.stroke([(0.430,0.916),(0.512,0.906),(0.594,0.918)], "round_hard", "lit",
         size=0.026, load=1.0, opacity=0.75, pressure="swell")
print("total", s.stroke_count)
print(s.look())
