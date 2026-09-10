p = s.palette
s.dry()
# a. the two gold wires were a drawn line, not an edge. Bury them.
s.stroke([(0.446,-0.04),(0.430,0.30),(0.414,0.60),(0.398,0.875)], "round_hard",
         "wall", size=0.034, load=1.0, pressure="even")
s.stroke([(0.588,-0.04),(0.600,0.34),(0.612,0.72),(0.620,0.875)], "round_hard",
         "wall", size=0.030, load=1.0, pressure="even")
print("wires buried", s.stroke_count)
# b. an edge against a light like that is glare, not a line
s.stroke([(0.462,-0.03),(0.448,0.32),(0.432,0.62),(0.416,0.870)], "round_hard",
         "spill", size=0.020, load=1.0, opacity=0.45, pressure="even")
s.stroke([(0.574,-0.03),(0.586,0.32),(0.598,0.62),(0.608,0.870)], "round_hard",
         "spill", size=0.016, load=1.0, opacity=0.35, pressure="even")
s.stroke([(0.470,-0.03),(0.456,0.32),(0.440,0.62),(0.424,0.870)], "round_hard",
         "spill2", size=0.010, load=1.0, opacity=0.55, pressure="even")
print("glare", s.stroke_count)
# c. the light on the floor radiates from the foot of the door
for x1, col, sz, op in [(0.02,"spill",0.075,0.55),(0.20,"spill2",0.070,0.70),
                        (0.38,"lit",0.060,0.80),(0.62,"lit",0.060,0.80),
                        (0.80,"spill2",0.070,0.70),(0.97,"spill",0.075,0.55)]:
    s.stroke([(0.510,0.872),(x1*0.45+0.510*0.55,0.945),(x1,1.04)], "bristle", col,
             size=sz, load=1.0, opacity=op, pressure="lift_off")
print("spill", s.stroke_count)
# d. dark floor in the two far corners, with a tip that has no corners
s.stroke([(-0.06,0.900),(0.10,0.930),(0.22,0.980)], "round_hard", "floor", size=0.11,
         load=1.0, opacity=0.9, pressure="even")
s.stroke([(1.06,0.900),(0.90,0.932),(0.78,0.982)], "round_hard", "floor", size=0.11,
         load=1.0, opacity=0.9, pressure="even")
s.stroke([(-0.06,1.03),(0.08,1.04)], "round_hard", "floor", size=0.07, load=1.0,
         opacity=0.85, pressure="even")
s.stroke([(1.06,1.03),(0.92,1.04)], "round_hard", "floor", size=0.07, load=1.0,
         opacity=0.85, pressure="even")
print("total", s.stroke_count)
print(s.look())
