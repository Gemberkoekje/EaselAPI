# The bowl, which had gone dead. One grazed arc along the far rim -- the only
# long curve in a picture otherwise made of straight runs -- and beans catching
# light where the light actually falls, clustered rather than sprinkled.
s.dry()

# the lit stripe down the cupped forearm was the loudest thing outside the hands:
# two starved marks laid ACROSS it break it rather than merely darkening it
s.stroke([(0.596, 0.700), (0.664, 0.716), (0.722, 0.712)], "bristle", "fl_body3",
         size=0.040, opacity=0.62, load=0.50, load_falloff=0.45,
         pressure="swell", note="subject")
s.stroke([(0.652, 0.792), (0.714, 0.778), (0.768, 0.786)], "bristle", "fl_shad",
         size=0.034, opacity=0.55, load=0.45, load_falloff=0.50,
         pressure="swell", note="subject")

# the far rim, grazed from the upper left and losing its far end
s.stroke([(-0.060, 0.802), (0.020, 0.760), (0.104, 0.734), (0.186, 0.744),
          (0.258, 0.772)], "round_hard", "rim_lit", size=0.012, opacity=0.88,
         load=1.0, load_falloff=0.22, pressure=[0.75, 1.0, 0.62, 0.30, 0.0],
         note="bowl")
# and a second, broken, a little inside it: the rim has thickness
s.stroke([(0.012, 0.784), (0.086, 0.762), (0.148, 0.768)], "bristle", "crock",
         size=0.018, opacity=0.60, load=0.45, load_falloff=0.50,
         pressure="swell", note="bowl")

# the contents: a granular pass, then beans, clustered toward the light
s.stroke([(-0.020, 0.868), (0.090, 0.842), (0.210, 0.856)], "bristle", "bean_warm",
         size=0.058, opacity=0.38, load=0.42, load_falloff=0.35,
         pressure="swell", note="bowl")
s.stroke([(0.000, 0.930), (0.110, 0.910)], "bristle", "bean",
         size=0.046, opacity=0.50, load=0.38, load_falloff=0.40,
         pressure="swell", note="bowl")
for pts, sz, col, op, pr in [
        ([(0.030, 0.846), (0.058, 0.854)], 0.015, "bean_warm", 0.85, [0.8, 0.3]),
        ([(0.062, 0.836), (0.090, 0.832)], 0.013, "bean_warm", 0.70, [0.4, 0.9]),
        ([(0.104, 0.858), (0.128, 0.866)], 0.011, "bean_warm", 0.55, [0.7, 0.25])]:
    s.stroke(pts, "round_hard", col, size=sz, opacity=op, load=1.0,
             tip_wobble=0.60, pressure=pr, note="bowl")
s.dab(0.048, 0.874, "round_hard", "bean_warm", size=0.009, press=3,
      tip_wobble=0.75, opacity=0.80, note="bowl")
s.dab(0.150, 0.842, "round_hard", "bean", size=0.012, press=2,
      tip_wobble=0.70, opacity=0.75, note="bowl")

# where the bowl sets down on the table, on its shadow side
s.stroke([(0.318, 0.836), (0.372, 0.884), (0.400, 0.940)], "bristle", "tbl_deep",
         size=0.042, opacity=0.70, load=0.85, load_falloff=0.40,
         pressure="swell", note="bowl")
print(s.look())
