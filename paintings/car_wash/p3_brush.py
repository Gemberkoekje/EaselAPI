# The side brush swinging in. It is smothered in foam, so it is a pale churning mass,
# not a dark one -- which also leaves a dark wedge of tunnel running between it and
# the bloom, with the stop light sitting in that wedge.
body = {"shape": brushmass(), "brush": "bristle", "color": "brush_lt",
        "size": 0.085, "density": 0.80, "direction": (82, 103)}
print("brush body:", s.cost(body), "strokes")
s.paint(body)

# The gaps between the strips: raked down through it, unevenly, at four widths.
s.stroke([(0.905, -0.03), (0.845, 0.42), (0.878, 0.74)], "bristle", "brush_dk",
         size=0.038, opacity=0.75, pressure="taper")
s.stroke([(0.995, 0.02), (0.955, 0.51)], "bristle", "brush_dk",
         size=0.022, opacity=0.65, pressure="lift_off")
s.stroke([(0.793, 0.145), (0.762, 0.385), (0.815, 0.60)], "bristle", "brush_dk",
         size=0.030, opacity=0.70, pressure="swell")
s.stroke([(0.862, 0.30), (0.838, 0.66)], "bristle", "brush_dk",
         size=0.016, opacity=0.55, pressure="taper")

# Strips flung off the leading edge, breaking the silhouette into the tunnel.
s.stroke([(0.742, 0.225), (0.668, 0.196)], "bristle", "brush_lt",
         size=0.020, opacity=0.60, load=0.35, pressure="lift_off")
s.stroke([(0.728, 0.455), (0.655, 0.505)], "bristle", "brush_lt",
         size=0.017, opacity=0.55, load=0.30, pressure="lift_off")
s.stroke([(0.800, 0.700), (0.735, 0.775)], "bristle", "brush_dk",
         size=0.022, opacity=0.60, load=0.40, pressure="taper")
print(s.look())
