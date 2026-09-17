exec(open("helpers.py").read())
exec(open("pears.py").read())
p = s.palette
p["mug_hi"] = to_value(p.mix(p["mug_lit"], "titanium_white", 0.5), 0.82)
pp1 = lambda d, f, lobe="big": pear_point(PEARS["pear1"], d, f, lobe)
pp3 = lambda d, f, lobe="big": pear_point(PEARS["pear3"], d, f, lobe)
s.dry()
# repairs: the notch in pear 1's shoulder, the two-tone left wall
s.stroke([pp1(-30, 0.85, "small"), pp1(10, 0.8, "small"), pp1(-60, 0.9), pp1(-35, 0.93)],
         "round_hard", "pear_body", size=0.016, pressure=[0.5, 1.0, 1.0, 0.6], load=1.0,
         jitter=0.0, note="pear 1 shoulder, notch filled")
s.stroke([(0.03, -0.02), (0.03, 0.25)], "round_soft", "wall", size=0.04, opacity=0.5,
         pressure="even", load=1.0, note="left wall, band merged")
# edges: lose two quiet ones, along them, once
s.smudge([(0.36, 0.766), (0.48, 0.771)], size=0.025, note="lying pear into its shadow")
s.smudge([(0.76, 0.578), (0.98, 0.578)], size=0.03, note="curtain into the sill")
# highlights: few, small, last
s.dab(*pp1(215, 0.72), "round_hard", "pear_hi", size=0.012, press=3, note="pear 1 catchlight")
s.dab(*pp3(20, 0.70), "round_hard", "pear_hi", size=0.010, press=3, note="lying pear catchlight")
s.stroke([(0.507, 0.414), (0.535, 0.428), (0.562, 0.433)], "liner", "mug_hi", size=0.006,
         pressure=[0.3, 1.0, 0.5], load=1.0, note="mug near lip")
s.dab(0.655, 0.497, "round_hard", "mug_hi", size=0.008, press=3, note="handle glint")
s.stroke([(0.0, 0.775), (0.20, 0.777)], "liner", "sill_lit", size=0.005, opacity=0.7,
         pressure="lift_off", load=1.0, note="sun on the sill edge")
print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
print(s.look(region="B3:F7"))
