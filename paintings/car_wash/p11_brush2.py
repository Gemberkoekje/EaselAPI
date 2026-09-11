# The brush was reading as a vertical curtain. What it is missing is rotation: the
# strips on a spinning cylinder splay, and they flare hardest at the bottom where it
# throws. Four marks, none of them vertical.
s.stroke([(0.912, 0.572), (0.846, 0.692), (0.808, 0.752)], "bristle", "brush_dk",
         size=0.026, load=0.60, opacity=0.62, pressure="taper")
s.stroke([(0.972, 0.616), (0.898, 0.742)], "bristle", "foam",
         size=0.019, load=0.55, opacity=0.55, pressure="lift_off")
s.stroke([(0.772, 0.352), (0.828, 0.226), (0.862, 0.148)], "bristle", "brush_lt",
         size=0.022, load=0.50, opacity=0.50, pressure="swell")
s.stroke([(0.884, 0.226), (0.918, 0.398), (0.902, 0.548)], "bristle", "brush_dk",
         size=0.015, load=0.45, opacity=0.48, pressure="taper")
print(s.look())
