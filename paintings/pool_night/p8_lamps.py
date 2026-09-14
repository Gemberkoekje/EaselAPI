p["glow1"] = p.at_value(p.mix("watdeep", "watlit", 0.30), 0.670)
p["glow2"] = p.at_value(p.mix("watdeep", "watlit", 0.55), 0.745)
p["glow3"] = p.at_value(p.mix("watdeep", "watlit", 0.78), 0.815)

# A: the near lamp. A halo of two crossed films so it is not a capsule, a core, and
# a satellite -- a light seen through moving water breaks in two.
s.glaze([(0.315, 0.672), (0.395, 0.702)], "glow1", opacity=0.40, size=0.155,
        pressure="swell", note="subject")
s.glaze([(0.345, 0.645), (0.378, 0.722)], "glow1", opacity=0.28, size=0.105,
        pressure="swell", note="subject")
s.glaze([(0.328, 0.660), (0.364, 0.677)], "glow2", opacity=0.50, size=0.060,
        pressure="swell", note="subject")
s.dab(0.336, 0.661, "round_hard", "glow3", size=0.040, press=3, tip_wobble=0.55,
      note="subject")
s.dab(0.373, 0.682, "round_hard", "glow2", size=0.017, press=2, tip_wobble=0.7,
      note="subject")

# and the light fanning away from A: light *in* the water, glazed close to the field
p["fan_wide"] = p.at_value(p.mix("watdeep", "watlit", 0.35), 0.625)
p["fan_core"] = p.at_value(p.mix("watdeep", "watlit", 0.50), 0.680)
s.dry()
s.glaze([(0.385, 0.702), (0.56, 0.762), (0.76, 0.818)], "fan_wide", opacity=0.30,
        size=0.135, pressure=[1.0, 0.65, 0.20], note="subject")
s.glaze([(0.392, 0.678), (0.54, 0.658), (0.72, 0.648)], "fan_core", opacity=0.24,
        size=0.078, pressure=[1.0, 0.55, 0.12], note="subject")

# B: the far lamp, compact, no fan -- one difference per object on purpose
s.glaze([(0.630, 0.568), (0.680, 0.552)], "glow1", opacity=0.40, size=0.100,
        pressure="swell", note="subject")
s.dab(0.649, 0.557, "round_hard", "glow3", size=0.026, press=3, tip_wobble=0.6,
      note="subject")
print(s.look(region="B4:H8"))
