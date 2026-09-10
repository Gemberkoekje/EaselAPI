s.dry()
# a bristle is never solid: to actually bury something, use a tip that is
s.stroke([(0.545,0.268),(0.63,0.300),(0.70,0.286)], "round_hard", "squall",
         size=0.085, load=1.0, opacity=0.9, pressure="even")
s.stroke([(0.70,0.262),(0.79,0.288),(0.86,0.276)], "round_hard", "squall",
         size=0.075, load=1.0, opacity=0.85, pressure="even")
s.stroke([(0.88,0.252),(0.97,0.272),(1.03,0.262)], "round_hard", "squall",
         size=0.070, load=1.0, opacity=0.8, pressure="even")
s.stroke([(0.56,0.356),(0.74,0.336),(0.92,0.312)], "round_hard", "rain", size=0.032,
         load=1.0, opacity=0.45, pressure="swell")
s.stroke([(0.56,0.748),(0.68,0.758)], "round_hard", "water_m", size=0.040, load=1.0,
         opacity=0.95, pressure="even")
s.stroke([(0.60,0.792),(0.68,0.798)], "round_hard", "water_m", size=0.030, load=1.0,
         opacity=0.95, pressure="even")
print("total", s.stroke_count)
print(s.look())
