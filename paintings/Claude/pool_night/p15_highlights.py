s.dry()
p["hi"]   = p.at_value(p.mix("cerulean", "titanium_white", 0.85), 0.93)
p["hi2"]  = p.at_value(p.mix("cerulean", "titanium_white", 0.70), 0.86)
p["hi3"]  = p.at_value(p.mix("cerulean", "titanium_white", 0.55), 0.79)

# the two lamps, which are the lightest things in the picture and are meant to be
s.dab(0.352, 0.672, "round_soft", "hi3", size=0.086, opacity=0.32, note="subject")
s.dab(0.343, 0.664, "round_soft", "hi3", size=0.058, opacity=0.60, note="subject")
s.dab(0.337, 0.659, "round_hard", "hi",  size=0.030, press=3, tip_wobble=0.50, note="subject")
s.glaze([(0.636, 0.564), (0.672, 0.552)], "hi3", opacity=0.35, size=0.052,
        pressure="swell", note="subject")
s.dab(0.650, 0.557, "round_hard", "hi",  size=0.019, press=3, tip_wobble=0.65, note="subject")

# four catches on the surface, where the light is and nowhere else
s.stroke([(0.284, 0.704), (0.352, 0.714), (0.410, 0.703)], "bristle", "hi2",
         size=0.030, load=0.38, opacity=0.85, load_falloff=0.35, pressure="swell", note="subject")
s.stroke([(0.430, 0.740), (0.500, 0.722)], "bristle", "hi3",
         size=0.027, load=0.45, opacity=0.80, load_falloff=0.40, pressure="taper", note="subject")
s.stroke([(0.486, 0.664), (0.556, 0.673)], "bristle", "hi3",
         size=0.026, load=0.40, opacity=0.70, load_falloff=0.42, pressure="lift_off", note="subject")
s.stroke([(0.612, 0.548), (0.664, 0.540)], "bristle", "hi3",
         size=0.026, load=0.36, opacity=0.60, load_falloff=0.45, pressure="taper", note="subject")

# one broken catch-light along the near edge -- the mark that makes a hollow thing
# read as hollow. Partial and off-centre, and the only mark on it.
s.stroke([(0.706, 0.892), (0.782, 0.808), (0.856, 0.728)], "liner",
         p.at_value("deck", 0.70), size=0.0060, opacity=0.95, load=0.75,
         load_falloff=0.75, pressure=[0.15, 1.0, 0.2])
# and one glint where the rail leaves the water
s.dab(0.741, 0.806, "round_hard", p.at_value("deck", 0.72), size=0.0075, press=2,
      tip_wobble=0.7)
print(s.look())
