# pass 6 -- highlights last: smallest brush, fewest strokes
# the hottest point of the bounce, right of the keyboard
s.dab(0.685, 0.676, "round_hard", p.at_value(p["pool_b"], 0.40), size=0.012,
      press=3, tip_wobble=0.7)
# one bright core on the prompt -- the second-lightest mark in the picture, on the subject
s.stroke([(0.347, 0.4325), (0.367, 0.4318)], "liner", p.at_value(p["phos"], 0.80),
         size=0.006, load=1.0, opacity=0.95, note="subject")

# sign it: a mark, not a name -- bottom right, close in value to what it sits on
s.stroke([(0.885, 0.955), (0.905, 0.950), (0.925, 0.953)], "liner", p.at_value(p["pool_b"], 0.22),
         size=0.005, load=0.6, opacity=0.8, note="signature")
s.look()
