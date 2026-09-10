R = "/home/user/refs/Level1.jpg"
s.dry()
n0 = s.stroke_count
# 1-2  the visor: the one mark that makes the motif read
s.stroke([(0.377,0.451),(0.409,0.464),(0.440,0.481)], "round_hard", "visor",
         size=0.022, load=1.0, pressure="swell", note="visor")
s.stroke([(0.384,0.455),(0.412,0.467)], "round_hard", "mug_hi", size=0.011,
         load=1.0, pressure="taper", note="visor light")
# 3  the light running along the top-left rim
s.stroke([(0.294,0.240),(0.316,0.186),(0.362,0.150),(0.420,0.128)], "liner",
         "mug_wt", size=0.008, load=1.0, pressure=[0.3,1.0,0.9,0.2], note="rim light")
# 4  where the light catches the near lip
s.stroke([(0.436,0.328),(0.494,0.328)], "round_hard", "mug_wt", size=0.009,
         load=1.0, pressure="swell", note="lip accent")
# 5-6  the tea bag's tag, lying on the table
s.stroke([(0.828,0.548),(0.876,0.578),(0.918,0.612)], "flat", "dk", size=0.052,
         load=1.0, pressure="even", angle_follow=False, angle=62, note="tag")
s.dab(0.836, 0.552, "round_hard", "mug_hi", size=0.014, press=3, note="tag label")
# 7-8  the string, and a hair on the table
s.stroke([(0.636,0.214),(0.690,0.300),(0.726,0.404),(0.772,0.482),(0.822,0.540)],
         "liner", "mug_lit", size=0.005, load=1.0, pressure=[0.8,0.5,0.9,0.6,0.9],
         note="string")
s.stroke([(0.560,0.640),(0.660,0.672),(0.756,0.652)], "liner", "sh_mid",
         size=0.004, load=0.8, pressure=[0.2,1.0,0.3], note="hair")
# 9-10  two edges given away
s.smudge([(0.332,0.766),(0.362,0.796)], size=0.036, note="lose shadow edge")
s.smudge([(0.300,0.470),(0.296,0.516)], size=0.032, note="lose mug edge")
print("last ten:", n0, "->", s.stroke_count)
# --- signature: not part of the painting, and it costs nothing -------------
s.stroke([(0.038,0.944),(0.052,0.968),(0.078,0.930)], "liner", "sh_soft",
         size=0.006, load=1.0, pressure=[0.9,1.0,0.4], note="signature")
print("total", s.stroke_count)
print(s.look())
print(s.look(reference=R))
print(s.look(reference=R, values=True))
