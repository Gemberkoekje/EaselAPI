R = "/home/user/refs/Level1.jpg"
# break the vertical ribbing on the left band with marks that run across it
s.stroke([(-0.02,0.18),(0.09,0.13),(0.19,0.115)], "flat", "wood_mid", size=0.13,
         opacity=0.30, load=1.0, pressure="even")
s.stroke([(-0.02,0.47),(0.10,0.42)], "flat", "wood_dk", size=0.16, opacity=0.25,
         load=1.0, pressure="even")
s.stroke([(0.0,0.72),(0.14,0.66),(0.24,0.645)], "flat", "wood_mid", size=0.12,
         opacity=0.22, load=1.0, pressure="even")
s.stroke([(-0.02,0.98),(0.12,0.92)], "flat", "wood_dk", size=0.15, opacity=0.30,
         load=1.0, pressure="even")
s.stroke([(0.03,0.36),(0.16,0.315),(0.27,0.31)], "round_hard", "wood_mid", size=0.09,
         opacity=0.18, load=1.0, pressure="even")

# broad diffuse light over the right field, several angles, no two alike
s.stroke([(0.66,0.02),(0.78,0.30),(0.83,0.58)], "flat", "wood_lit", size=0.18,
         opacity=0.22, load=1.0, pressure="even")
s.stroke([(0.55,0.28),(0.80,0.40),(1.0,0.44)], "flat", "wood_lit", size=0.11,
         opacity=0.18, load=1.0, pressure="even")
s.stroke([(0.62,0.72),(0.88,0.60),(1.0,0.50)], "round_hard", "wood_lit", size=0.13,
         opacity=0.16, load=1.0, pressure="even")
s.stroke([(0.58,0.62),(0.70,0.36),(0.72,0.10)], "flat", "wood_mid", size=0.10,
         opacity=0.20, load=1.0, pressure="even")

# take the hard ends off the dark corner, and cover the smudge lobes
s.stroke([(0.66,1.02),(0.88,0.86),(1.02,0.72)], "round_hard", "wood_lo", size=0.15,
         opacity=0.22, load=1.0, pressure="even")
s.stroke([(0.56,0.90),(0.70,0.83)], "round_hard", "wood_mid", size=0.10,
         opacity=0.30, load=1.0, pressure="even")
s.stroke([(0.55,0.52),(0.66,0.46)], "round_hard", "wood_mid", size=0.09,
         opacity=0.30, load=1.0, pressure="even")
s.stroke([(0.56,0.18),(0.66,0.11)], "round_hard", "wood_mid", size=0.08,
         opacity=0.30, load=1.0, pressure="even")
print("total", s.stroke_count)
print(s.look())
