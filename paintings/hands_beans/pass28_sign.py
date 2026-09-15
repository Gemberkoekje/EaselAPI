# Signed. Not a name -- two small bean-shaped marks along the bottom edge, one set
# a little apart from the other: the gesture the whole painting is about, made once
# more at the smallest size it will survive. Value 0.25 on a 0.17 ground, so it is
# there if you look and does the picture no harm if you do not.
p["sig"] = p.at_value(p.mix("burnt_sienna", "burnt_umber", 0.40), 0.252)
s.stroke([(0.4980, 0.9655), (0.5115, 0.9690)], "round_hard", "sig", size=0.0090,
         opacity=0.85, load=1.0, tip_wobble=0.65, pressure=[0.8, 0.3],
         note="signature")
s.stroke([(0.5330, 0.9725), (0.5445, 0.9700)], "round_hard", "sig", size=0.0078,
         opacity=0.72, load=1.0, tip_wobble=0.70, pressure=[0.35, 0.85],
         note="signature")
print(s.look(region="D7:F8"))
