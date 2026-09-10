p = s.palette
s.dry()
p["mid1"] = p.mix(p["sky"], p["glow"], 0.42)
p["mid2"] = p.mix(p["sky"], p["glow"], 0.72)
print("mid1", p.hex(p["mid1"]), round(p.value_of(p["mid1"]),3),
      " mid2", p.hex(p["mid2"]), round(p.value_of(p["mid2"]),3))
# knock the yellow sausage back into the sky
s.stroke([(0.44,0.470),(0.72,0.455),(1.02,0.462)], "round_hard", "sky", size=0.075,
         load=1.0, opacity=0.85, pressure="even")
s.stroke([(0.44,0.530),(0.74,0.518),(1.02,0.524)], "round_hard", "sky", size=0.050,
         load=1.0, opacity=0.70, pressure="even")
s.stroke([(0.435,0.590),(0.60,0.585)], "round_hard", "sky", size=0.045, load=1.0,
         opacity=0.60, pressure="lift_off")
# the light as steps, laid low and wide, then the joins lost while wet
s.stroke([(0.42,0.585),(0.72,0.575),(1.03,0.580)], "round_hard", "mid1", size=0.040,
         load=1.0, pressure="press_in")
s.stroke([(0.46,0.628),(0.75,0.620),(1.03,0.624)], "round_hard", "mid2", size=0.036,
         load=1.0, pressure="press_in")
s.stroke([(0.50,0.662),(0.78,0.655),(1.03,0.658)], "round_hard", "glow", size=0.030,
         load=1.0, pressure="press_in")
s.stroke([(0.56,0.686),(0.82,0.680),(1.03,0.682)], "round_hard", "glow2", size=0.022,
         load=1.0, pressure="press_in")
s.stroke([(0.68,0.697),(0.84,0.693),(0.98,0.695)], "round_hard", "blaze", size=0.013,
         load=1.0, pressure="swell")
s.smudge([(0.62,0.600),(0.66,0.612)], size=0.032)
s.smudge([(0.80,0.596),(0.84,0.610)], size=0.032)
s.smudge([(0.72,0.640),(0.76,0.650)], size=0.028)
# the confetti the wet paint threw across the sea
s.stroke([(0.44,0.735),(0.62,0.742),(0.80,0.736)], "bristle", "water_m", size=0.055,
         load=1.0, opacity=0.9, pressure="even")
s.stroke([(0.50,0.790),(0.70,0.798)], "bristle", "water_m", size=0.045, load=1.0,
         opacity=0.8, pressure="taper")
print("total", s.stroke_count)
print(s.look())
