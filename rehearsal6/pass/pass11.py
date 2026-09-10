R = "/home/user/refs/Level1.jpg"
p = s.palette
s.dry()
# --- value corrections: the figure has to actually cover -------------------
s.stroke([(0.382,0.430),(0.378,0.560),(0.382,0.624)], "round_hard", "fig",
         size=0.048, load=1.0, pressure="even")
s.stroke([(0.424,0.412),(0.424,0.560),(0.426,0.626)], "round_hard", "fig",
         size=0.050, load=1.0, pressure="even")
s.stroke([(0.466,0.432),(0.470,0.560),(0.468,0.620)], "round_hard", "fig",
         size=0.046, load=1.0, pressure="even")
s.stroke([(0.396,0.408),(0.452,0.410)], "round_hard", "fig", size=0.030,
         load=1.0, pressure="even")
s.stroke([(0.512,0.508),(0.534,0.560)], "round_hard", "fig2", size=0.040,
         load=1.0, pressure="even")
# --- the inside of the vessel runs further right than I had it -------------
s.stroke([(0.560,0.172),(0.596,0.196),(0.606,0.232)], "round_hard", "tea",
         size=0.036, load=1.0, pressure="even")
s.stroke([(0.540,0.150),(0.580,0.172)], "round_hard", "tea", size=0.028,
         load=1.0, pressure="even")
s.stroke([(0.586,0.244),(0.560,0.268)], "round_hard", "tea2", size=0.026,
         load=1.0, pressure="even")
# --- the lit table beside the handle's shadow, and the far corner ----------
s.stroke([(0.660,0.700),(0.730,0.672),(0.760,0.646)], "round_hard", "wood_lit",
         size=0.060, load=1.0, opacity=0.7, pressure="even")
s.stroke([(0.700,0.740),(0.748,0.706)], "round_hard", "wood_hi", size=0.045,
         load=1.0, opacity=0.5, pressure="even")
s.stroke([(0.882,0.012),(0.960,0.040),(1.01,0.062)], "flat", "dk", size=0.030,
         load=1.0, pressure="even")
print("corrections", s.stroke_count)
# --- the handle ------------------------------------------------------------
mid = [(0.640,0.234),(0.692,0.258),(0.717,0.302),(0.712,0.362),(0.683,0.419),
       (0.639,0.452),(0.610,0.462)]
s.stroke(mid, "flat", "mug_shd", size=0.046, load=1.0, pressure="even")
s.stroke([(0.646,0.226),(0.700,0.252),(0.728,0.300),(0.724,0.364),(0.694,0.424),
          (0.648,0.458)], "bristle", "mug_lit", size=0.024, load=1.0, pressure="swell")
s.stroke([(0.652,0.220),(0.706,0.248),(0.734,0.300),(0.730,0.362)], "bristle",
         "mug_hi", size=0.013, load=1.0, pressure="taper")
s.stroke([(0.632,0.246),(0.628,0.300)], "round_hard", "mug_mid", size=0.026,
         load=1.0, pressure="even")
s.stroke([(0.614,0.450),(0.628,0.464),(0.604,0.478)], "round_hard", "mug_lit",
         size=0.030, load=1.0, pressure="even")
# the hole is table, and the table is behind the handle
s.stroke([(0.640,0.318),(0.652,0.360),(0.648,0.404)], "round_hard", "wood_lit",
         size=0.034, load=1.0, opacity=0.9, pressure="even")
s.stroke([(0.662,0.330),(0.664,0.386)], "round_hard", "wood_mid", size=0.024,
         load=1.0, opacity=0.8, pressure="even")
print("total", s.stroke_count)
print(s.look(reference=R, region=span("C1","G7")))
