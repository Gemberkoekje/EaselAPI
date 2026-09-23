# The signature: not a name -- a small light over a short horizon, the picture's own
# subject in two marks. Lower-left corner, on the dark water, close to it in value.
p["sig_line"] = p.at_value(p.mix("sea_near", "pale", 0.3), 0.33)
p["sig_light"] = p.at_value(p.mix("sea_near", "glow", 0.35), 0.37)
s.stroke([(0.029, 0.960), (0.043, 0.9585), (0.058, 0.9595)], "liner", "sig_line",
         size=0.0028, opacity=0.9, pressure=[0.3, 1.0, 0.4], note="signature")
s.dab(0.0435, 0.9455, "round_hard", "sig_light", size=0.0045, press=2, tip_wobble=0.3,
      note="signature")
