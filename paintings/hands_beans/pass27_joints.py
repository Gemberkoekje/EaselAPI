# The two lit fingers were the last mechanical thing in the picture: two clean
# parallel arcs of cream in a painting where every other passage had been broken.
# Fingers have joints, and the light dips at each one. Six small marks take the
# bars out -- across the run, not along it, which is what breaks a parallel.
s.dry()

for pts, sz, col, op in [
    ([(0.4045, 0.3880), (0.4005, 0.4180)], 0.0105, "fl_mid",  0.58),
    ([(0.3480, 0.3930), (0.3455, 0.4150)], 0.0085, "fl_mid",  0.42),
    ([(0.3960, 0.4350), (0.3905, 0.4680)], 0.0115, "fl_mid",  0.62),
    ([(0.3325, 0.4400), (0.3290, 0.4720)], 0.0095, "fl_body", 0.48),
]:
    s.stroke(pts, "round_hard", col, size=sz, opacity=op, load=1.0,
             load_falloff=0.30, tip_wobble=0.50, pressure=[0.35, 0.95],
             note="subject")

# one starved warm pass across both, where the light turns over the knuckles:
# it crosses the two arcs at an angle and is the mark that stops them pairing
s.stroke([(0.4620, 0.3860), (0.4405, 0.4340), (0.4230, 0.4820)], "bristle",
         "joint_lo", size=0.026, opacity=0.34, load=0.52, load_falloff=0.50,
         pressure="swell", note="subject")
s.stroke([(0.3720, 0.3900), (0.3595, 0.4290), (0.3510, 0.4680)], "bristle",
         "fl_cool", size=0.020, opacity=0.26, load=0.48, load_falloff=0.55,
         pressure="swell", note="subject")
print(s.look())
