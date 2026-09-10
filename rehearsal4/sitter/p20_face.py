p = s.palette
s.dry()
n = s.stroke_count

# the background painted back up to the profile: the edge is where two masses meet
s.stroke([(0.396, 0.242), (0.391, 0.312), (0.388, 0.376)], "flat", "deep",
         size=0.028, pressure="even")
s.stroke([(0.390, 0.372), (0.401, 0.414), (0.408, 0.452)], "flat", "deep",
         size=0.026, pressure="even")
s.stroke([(0.405, 0.448), (0.415, 0.492), (0.431, 0.532)], "flat", "bgL",
         size=0.028, pressure="even")
print("profile", s.stroke_count - n); n = s.stroke_count

# the eye: dark, light, and the edge between them
s.stroke([(0.4475, 0.3045), (0.4665, 0.3025)], "round_hard", "skin_d", size=0.014)
s.stroke([(0.4585, 0.3025), (0.4655, 0.3035)], "round_hard", "eyew2", size=0.006)
s.stroke([(0.4520, 0.3055), (0.4535, 0.3055)], "round_hard", "iris", size=0.0085)
s.stroke([(0.4435, 0.2955), (0.4665, 0.2985)], "liner", "hair_d", size=0.0045)
s.dab(0.4502, 0.3028, "round_hard", "titanium_white", size=0.0026, press=3)
print("eye", s.stroke_count - n); n = s.stroke_count

s.stroke([(0.4135, 0.3505), (0.4085, 0.3705)], "round_hard", "skin_l", size=0.005)
s.stroke([(0.4295, 0.3995), (0.4335, 0.4025)], "round_hard", "beard", size=0.006)
s.stroke([(0.4185, 0.4135), (0.4435, 0.4065), (0.4635, 0.4165)], "bristle",
         "beard", size=0.012)
s.stroke([(0.4385, 0.4475), (0.4555, 0.4495)], "round_hard", "iris", size=0.007)
s.dab(0.4465, 0.4372, "round_hard", "teeth2", size=0.0055, press=2)
s.stroke([(0.4425, 0.4595), (0.4585, 0.4615)], "round_hard", "lip", size=0.005)
s.stroke([(0.4305, 0.4765), (0.4445, 0.5165), (0.4685, 0.5445)], "bristle",
         "beard", size=0.018)
print("nose/mouth/beard", s.stroke_count - n)

print("total:", s.stroke_count)
print(s.look(region=span("D3", "E4"), reference="ref.jpg"))
