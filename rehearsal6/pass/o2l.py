s.dry()
# short marks with a round tip are blobs. Only long strokes from here.
s.stroke([(0.470,0.100),(0.468,0.240),(0.466,0.360)], "bristle", "wall", size=0.052,
         load=1.0, pressure="even")
s.stroke([(0.586,0.100),(0.588,0.240),(0.590,0.360)], "bristle", "wall", size=0.048,
         load=1.0, pressure="even")
# run the column through the patch instead of letting the patch sit on it
s.stroke([(0.518,0.060),(0.520,0.230),(0.522,0.400)], "bristle", "blaze", size=0.044,
         load=1.0, pressure="even")
s.stroke([(0.502,0.070),(0.500,0.400)], "bristle", "lit", size=0.014, load=1.0,
         opacity=0.8, pressure="swell")
s.stroke([(0.552,0.070),(0.554,0.400)], "bristle", "lit", size=0.013, load=1.0,
         opacity=0.8, pressure="swell")
s.stroke([(0.484,0.050),(0.482,0.420)], "bristle", "spill2", size=0.020, load=1.0,
         opacity=0.55, pressure="swell")
s.stroke([(0.572,0.050),(0.574,0.420)], "bristle", "spill2", size=0.018, load=1.0,
         opacity=0.50, pressure="swell")
# the orange sausage in the corner
s.stroke([(-0.06,0.930),(0.10,0.952),(0.22,0.985)], "bristle", "floor", size=0.090,
         load=1.0, opacity=0.95, pressure="even")
s.stroke([(-0.06,1.01),(0.14,1.03)], "bristle", "floor", size=0.070, load=1.0,
         opacity=0.9, pressure="even")
print("total", s.stroke_count)
print(s.look())
