R = "/home/user/refs/Level1.jpg"
p = s.palette
s.dry()
# a round tip declares no axis - the right brush for a mass that keeps coming out square
soft = blob((0.455, 0.706), 0.172, 0.112, wobble=0.30, seed=12)
s.block_in(soft, "round_hard", "sh_soft", direction="axis", density=0.85,
           size=0.075, load=1.0, pressure="even")
print("penumbra", s.stroke_count)
mid = blob((0.437, 0.712), 0.125, 0.082, wobble=0.33, seed=5)
s.block_in(mid, "round_hard", "sh_mid", direction=(-14), density=0.9,
           size=0.052, load=1.0, pressure="even")
print("mid", s.stroke_count)
core = blob((0.415, 0.712), 0.082, 0.050, wobble=0.35, seed=8)
s.block_in(core, "round_hard", "sh_core", direction=(-18), density=1.0,
           size=0.034, load=1.0, pressure="even")
print("core", s.stroke_count)

# the handle's shadow: lighter and thinner than the first try
s.stroke([(0.601,0.607),(0.624,0.556),(0.664,0.523),(0.699,0.548)], "round_hard",
         "sh_mid", size=0.022, load=1.0, opacity=0.55, pressure="swell")
s.stroke([(0.700,0.552),(0.703,0.592),(0.667,0.624),(0.618,0.628)], "round_hard",
         "sh_soft", size=0.020, load=1.0, opacity=0.5, pressure="taper")

# the lit table comes back up to the shadow from below and from the left
s.stroke([(0.30,0.885),(0.50,0.855),(0.70,0.845)], "bristle", "wood_lit", size=0.075,
         load=1.0, opacity=0.55, pressure="even")
s.stroke([(0.26,0.955),(0.52,0.915),(0.76,0.895)], "bristle", "wood_hi", size=0.065,
         load=1.0, opacity=0.40, pressure="taper")
s.stroke([(0.245,0.700),(0.262,0.640)], "round_hard", "wood_lit", size=0.055,
         load=1.0, opacity=0.45, pressure="even")
s.stroke([(0.50,0.822),(0.60,0.795)], "round_hard", "wood_lit", size=0.045,
         load=1.0, opacity=0.40, pressure="taper")
print("total", s.stroke_count)
print(s.look())
print(s.look(reference=R, region=span("C5","G8")))
