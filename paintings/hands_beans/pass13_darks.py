# Two things at once. The hands had no core shadow -- every dark sat at 0.34, so
# nothing turned. And four fingers described equally were four parallel bars that
# no brushwork was going to rescue. So: warm core darks under the two fingers that
# stay, and the lower two lost into the palm's shadow. Two fingers is not a grille.
s.dry()

# the two that stay, given real undersides
for pts, sz, op, col in [
    ([(0.508, 0.468), (0.434, 0.434), (0.360, 0.430)], 0.013, 0.78, "fl_under"),
    ([(0.500, 0.514), (0.420, 0.484), (0.340, 0.484), (0.292, 0.510)], 0.015, 0.88, "fl_core"),
]:
    s.stroke(pts, "round_hard", col, size=sz, opacity=op, load=1.0,
             load_falloff=0.35, tip_wobble=0.45,
             pressure=[0.25, 1.0, 0.7, 0.2][:len(pts)], note="subject")

# the two that go: knocked back into the hollow with marks laid ACROSS their run,
# which takes their linearity out as well as their light
s.stroke([(0.482, 0.528), (0.420, 0.556), (0.350, 0.572)], "bristle", "fl_under",
         size=0.046, opacity=0.72, load=0.85, load_falloff=0.35,
         pressure="swell", note="subject")
s.stroke([(0.318, 0.596), (0.382, 0.566), (0.448, 0.572)], "bristle", "palm_dk",
         size=0.038, opacity=0.60, load=0.60, load_falloff=0.45,
         pressure="swell", note="subject")
s.stroke([(0.364, 0.520), (0.396, 0.572), (0.416, 0.616)], "bristle", "fl_under",
         size=0.030, opacity=0.55, load=0.55, load_falloff=0.50,
         pressure="swell", note="subject")

# the bottom of the cup, where a cupped palm is darkest
s.stroke([(0.382, 0.598), (0.442, 0.614), (0.496, 0.602)], "bristle", "fl_core",
         size=0.030, opacity=0.78, load=1.0, load_falloff=0.35,
         pressure="swell", note="subject")
s.stroke([(0.564, 0.706), (0.500, 0.692), (0.446, 0.666)], "bristle", "fl_under",
         size=0.020, opacity=0.70, load=0.55, load_falloff=0.40,
         pressure="swell", note="subject")
# the wrist: the break that stops hand and forearm reading as one bar
s.stroke([(0.624, 0.628), (0.652, 0.666), (0.664, 0.706)], "bristle", "fl_under",
         size=0.026, opacity=0.72, load=0.58, load_falloff=0.40,
         pressure="swell", note="subject")

# the picking hand: its shadow side, under its knuckles, and its own wrist
s.stroke([(0.800, 0.286), (0.766, 0.334), (0.724, 0.366)], "bristle", "fl_under",
         size=0.024, opacity=0.78, load=0.58, load_falloff=0.35,
         pressure="swell", note="subject")
s.stroke([(0.688, 0.442), (0.744, 0.452), (0.790, 0.432)], "bristle", "fl_core",
         size=0.022, opacity=0.70, load=0.58, load_falloff=0.40,
         pressure="swell", note="subject")
s.stroke([(0.622, 0.310), (0.600, 0.340)], "round_hard", "fl_core",
         size=0.011, opacity=0.75, load=1.0, tip_wobble=0.50,
         pressure=[0.9, 0.3], note="subject")
s.stroke([(0.756, 0.232), (0.790, 0.202), (0.812, 0.176)], "bristle", "fl_under",
         size=0.020, opacity=0.58, load=0.55, load_falloff=0.45,
         pressure="swell", note="subject")
print(s.look())
