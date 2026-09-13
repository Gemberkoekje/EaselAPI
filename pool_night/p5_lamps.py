LAMP_A = blob((0.360, 0.690), 0.105, 0.075, wobble=0.25, seed=4)
p["glow1"] = p.at_value(p.mix("watdeep", "watlit", 0.30), 0.665)
p["glow2"] = p.at_value(p.mix("watdeep", "watlit", 0.55), 0.735)
p["glow3"] = p.at_value(p.mix("watdeep", "watlit", 0.75), 0.805)

# A: the bloom body, over a narrow value span so 8 rings do not read as contours
s.scumble(LAMP_A, "watdeep", "glow1", 8, direction="inward", note="subject")
# the core, stacked soft and offset toward the wall the lamp is set in
s.dab(0.340, 0.662, "round_soft", "glow2", size=0.090, opacity=0.55, note="subject")
s.dab(0.331, 0.650, "round_soft", "glow3", size=0.050, opacity=0.60, note="subject")

# the light fanning away from it -- light *in* the water, so glazes close to the field
p["fan_wide"] = p.at_value(p.mix("watdeep", "watlit", 0.35), 0.60)
p["fan_core"] = p.at_value(p.mix("watdeep", "watlit", 0.50), 0.66)
s.dry()
s.glaze([(0.375, 0.700), (0.56, 0.762), (0.76, 0.818)], "fan_wide", opacity=0.20,
        size=0.14, pressure=[1.0, 0.65, 0.20], note="subject")
s.glaze([(0.385, 0.676), (0.54, 0.658), (0.72, 0.648)], "fan_core", opacity=0.16,
        size=0.080, pressure=[1.0, 0.55, 0.12], note="subject")

# B: a halo laid as film, not as paint, and one core -- a different method entirely
s.glaze([(0.632, 0.566), (0.678, 0.554)], "glow1", opacity=0.30, size=0.105,
        pressure="swell", note="subject")
s.dab(0.649, 0.557, "round_hard", "glow3", size=0.026, press=3, tip_wobble=0.6,
      note="subject")
print(s.look(region="B4:H8"))
