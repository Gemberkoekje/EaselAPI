s.dry()
# widen the column back to what it is below: two passes, full length
s.stroke([(0.512,-0.03),(0.513,0.22),(0.514,0.46)], "flat", "blaze", size=0.030,
         load=1.0, pressure="even")
s.stroke([(0.544,-0.03),(0.545,0.22),(0.546,0.46)], "flat", "blaze", size=0.030,
         load=1.0, pressure="even")
s.stroke([(0.494,-0.03),(0.495,0.46)], "bristle", "lit", size=0.016, load=1.0,
         opacity=0.85, pressure="even")
s.stroke([(0.562,-0.03),(0.563,0.46)], "bristle", "lit", size=0.015, load=1.0,
         opacity=0.85, pressure="even")
s.stroke([(0.478,-0.03),(0.479,0.48)], "bristle", "spill2", size=0.022, load=1.0,
         opacity=0.6, pressure="swell")
s.stroke([(0.578,-0.03),(0.579,0.48)], "bristle", "spill2", size=0.020, load=1.0,
         opacity=0.55, pressure="swell")
s.stroke([(0.462,-0.03),(0.463,0.50)], "bristle", "spill", size=0.026, load=1.0,
         opacity=0.35, pressure="swell")
s.stroke([(0.594,-0.03),(0.595,0.50)], "bristle", "spill", size=0.024, load=1.0,
         opacity=0.30, pressure="swell")
print("total", s.stroke_count)
print(s.look())
