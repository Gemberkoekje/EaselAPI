sig = p.at_value("deck", 0.34)
s.stroke([(0.038, 0.946), (0.073, 0.949)], "liner", sig, size=0.0045,
         opacity=0.85, load=0.7, load_falloff=0.5, pressure=[0.3, 1.0],
         note="signature")
s.dab(0.056, 0.963, "round_hard", sig, size=0.0055, press=2, tip_wobble=0.6,
      note="signature")
print(s.look(region="A7:C8"))
print(s.budget_line())
