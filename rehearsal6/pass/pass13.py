R = "/home/user/refs/Level1.jpg"
s.dry()
# value: D5 and D6 drifted light when the foot went in
s.stroke([(0.420,0.516),(0.424,0.600)], "round_hard", "fig", size=0.070,
         load=1.0, pressure="even")
s.stroke([(0.392,0.700),(0.452,0.710),(0.494,0.700)], "round_hard", "sh_core",
         size=0.040, load=1.0, opacity=0.85, pressure="even")
# two pale lumps left on the table
s.stroke([(0.232,0.690),(0.258,0.630)], "bristle", "wood_l2", size=0.055,
         load=1.0, opacity=0.8, pressure="even")
s.stroke([(0.614,0.716),(0.664,0.694)], "bristle", "sh_soft", size=0.045,
         load=1.0, opacity=0.7, pressure="taper")
# the foot is a curved base, not a bar: break its two square ends
s.stroke([(0.362,0.648),(0.382,0.664)], "round_hard", "sh_mid", size=0.020,
         load=1.0, opacity=0.85, pressure="even")
s.stroke([(0.524,0.660),(0.548,0.644),(0.556,0.622)], "round_hard", "mug_shd",
         size=0.018, load=1.0, opacity=0.9, pressure="taper")
# the scar where the handle meets the body
s.stroke([(0.596,0.400),(0.606,0.460),(0.596,0.500)], "bristle", "mug_shd",
         size=0.026, load=1.0, opacity=0.9, pressure="swell")
# the light halo down the left silhouette
s.stroke([(0.286,0.330),(0.296,0.450),(0.312,0.560)], "bristle", "wood_l2",
         size=0.022, load=1.0, opacity=0.75, pressure="even")
print("total", s.stroke_count)
