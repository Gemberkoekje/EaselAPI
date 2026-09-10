R = "/home/user/refs/Level1.jpg"
# --- five strokes to take the scallops off the shadow and carry the core right
s.stroke([(0.310,0.690),(0.352,0.772),(0.430,0.808)], "round_hard", "sh_soft",
         size=0.055, load=1.0, opacity=0.45, pressure="even")
s.stroke([(0.470,0.800),(0.550,0.762),(0.600,0.700)], "round_hard", "sh_soft",
         size=0.050, load=1.0, opacity=0.40, pressure="even")
s.stroke([(0.430,0.700),(0.505,0.690),(0.545,0.700)], "round_hard", "sh_core",
         size=0.045, load=1.0, opacity=0.75, pressure="even")
s.stroke([(0.390,0.745),(0.480,0.740)], "round_hard", "sh_mid", size=0.040,
         load=1.0, opacity=0.60, pressure="even")
s.stroke([(0.34,0.90),(0.58,0.955)], "round_hard", "wood_lit", size=0.07,
         load=1.0, opacity=0.30, pressure="even")
print("shadow fixed", s.stroke_count)

# --- the drawing. graphite, free, and it goes under the near masses --------
rim = [s.pt("rim_l"), (0.303,0.198), (0.352,0.152), (0.418,0.120), s.pt("rim_t"),
       (0.556,0.122), (0.607,0.156), s.pt("rim_r"), (0.622,0.262), (0.578,0.305),
       (0.502,0.331), s.pt("lip_f"), (0.404,0.325), (0.330,0.294), s.pt("rim_l")]
s.pencil(rim, pressure=0.65)
s.pencil([s.pt("rim_l"), (0.300,0.350), (0.318,0.455), (0.340,0.570), s.pt("base_l")])
s.pencil([s.pt("base_l"), (0.400,0.674), s.pt("base_f"), (0.505,0.670), s.pt("base_r")])
s.pencil([s.pt("base_r"), (0.578,0.598), (0.598,0.520), (0.613,0.437), (0.625,0.320),
          s.pt("rim_r")])
# the tea: the inside, which has a far edge above it and a near edge below it
s.pencil([(0.318,0.240),(0.372,0.185),(0.452,0.157),(0.535,0.160),(0.594,0.196),
          (0.575,0.258),(0.492,0.296),(0.400,0.288),(0.340,0.262),(0.318,0.240)])
# the handle, and its hole
s.pencil([s.pt("rim_r"), (0.686,0.222), s.pt("hand_o"), (0.740,0.320), (0.706,0.404),
          (0.650,0.458), (0.606,0.474)])
s.pencil([(0.628,0.300),(0.668,0.296),(0.692,0.344),(0.672,0.408),(0.630,0.428),
          (0.624,0.352),(0.628,0.300)])
# the printed figure
s.pencil([(0.360,0.446),(0.372,0.406),(0.408,0.389),(0.452,0.396),(0.487,0.424),
          (0.497,0.472),(0.514,0.480),(0.556,0.506),(0.560,0.584),(0.518,0.600),
          (0.512,0.622),(0.432,0.630),(0.376,0.626),(0.363,0.548),(0.360,0.446)])
s.pencil([(0.362,0.448),(0.396,0.442),(0.446,0.462),(0.466,0.486),(0.412,0.486),
          (0.372,0.470),(0.362,0.448)])
# the spoon
s.pencil([(0.509,0.0),(0.543,0.004),(0.528,0.145),(0.512,0.236),(0.489,0.232),
          (0.500,0.120),(0.509,0.0)])
print(s.look(reference=R, region=span("C1","G7")))
print("total", s.stroke_count)
