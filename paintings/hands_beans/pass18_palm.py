# The weakest passage, and it is the heart of the subject: the cup read as a hard
# elliptical hole cut in a board. A palm's hollow has no edge like that. Marks laid
# ACROSS the boundary take it out -- that is what loses an edge, not another smudge
# -- and then the beans it is holding get enough description to be beans.
s.dry()

# break the ellipse: three marks across it, at values between the two masses
for pts, sz, col, op in [
    ([(0.358, 0.516), (0.402, 0.498), (0.442, 0.504)], 0.026, "fl_body3", 0.58),
    ([(0.526, 0.544), (0.550, 0.582), (0.538, 0.616)], 0.022, "fl_under", 0.52),
    ([(0.408, 0.628), (0.456, 0.646), (0.502, 0.638)], 0.024, "fl_body3", 0.48),
    ([(0.372, 0.558), (0.362, 0.594)], 0.018, "fl_under", 0.45),
]:
    s.stroke(pts, "bristle", col, size=sz, opacity=op, load=0.55,
             load_falloff=0.50, pressure="swell", note="subject")

# the beans it is holding: a granular bed, then four described, no two alike
s.stroke([(0.376, 0.590), (0.440, 0.604), (0.500, 0.592)], "bristle", "bean_palm",
         size=0.040, opacity=0.68, load=0.52, load_falloff=0.35,
         pressure="swell", note="subject")
s.stroke([(0.392, 0.566), (0.452, 0.576), (0.494, 0.566)], "bristle", "bean_warm",
         size=0.028, opacity=0.55, load=0.46, load_falloff=0.40,
         pressure="swell", note="subject")
for pts, sz, col, op, pr in [
    ([(0.404, 0.582), (0.428, 0.590)], 0.013, "bean_lit",  0.88, [0.8, 0.3]),
    ([(0.448, 0.598), (0.474, 0.592)], 0.011, "bean_warm", 0.78, [0.35, 0.9]),
    ([(0.478, 0.572), (0.498, 0.580)], 0.010, "bean_warm", 0.62, [0.7, 0.2])]:
    s.stroke(pts, "round_hard", col, size=sz, opacity=op, load=1.0,
             tip_wobble=0.65, pressure=pr, note="subject")
s.dab(0.4235, 0.6055, "round_hard", "bean_dk", size=0.0105, press=3,
      tip_wobble=0.75, opacity=0.80, note="subject")

# the near wall of the cup, rising toward the thumb: reflected light, kept low
s.stroke([(0.396, 0.648), (0.466, 0.666), (0.540, 0.654)], "bristle", "fl_body2",
         size=0.030, opacity=0.62, load=0.58, load_falloff=0.45,
         pressure="swell", note="subject")
print(s.look(region="C4:F6"))
