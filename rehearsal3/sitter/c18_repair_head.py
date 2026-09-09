# Pass 18: repair the eye (a dark crescent, not an eye), the mouth (a cream bar),
# the moustache, the beard direction, the nose form and the ear.
REF = "C:/temp/Level3.jpg"
p = s.palette
p["sk_hi"]   = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.38), "titanium_white", 0.76)
p["sk_lit"]  = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.44), "titanium_white", 0.62)
p["sk_mid"]  = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.40), "titanium_white", 0.46)
p["sk_shad"] = p.desaturate(
    p.mix(p.mix("burnt_sienna", "burnt_umber", 0.45), "titanium_white", 0.32), 0.22)
p["brow2"]   = p.mix(p.mix("burnt_umber", "burnt_sienna", 0.25), "titanium_white", 0.11)
p["iris"]    = p.mix("burnt_umber", "ultramarine", 0.30)
p["eyew"]    = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.25), "titanium_white", 0.78)
p["catch"]   = p.mix("titanium_white", "yellow_ochre", 0.06)
p["mouth_dk"] = p.mix("burnt_umber", "alizarin", 0.22)
p["teeth"]   = p.mix(p.mix("yellow_ochre", "burnt_sienna", 0.14), "titanium_white", 0.74)
p["lip2"]    = p.desaturate(
    p.mix(p.mix("cadmium_red", "burnt_sienna", 0.55), "titanium_white", 0.44), 0.35)
p["beard"]   = p.mix(p.mix("burnt_umber", "burnt_sienna", 0.32), "titanium_white", 0.09)
p["must"]    = p.mix("burnt_umber", "ultramarine", 0.10)
p["ear_c"]   = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.42), "titanium_white", 0.40)
s.dry()

# ---- 1. wipe the eye area back to skin and rebuild it small ----
n0 = s.stroke_count
s.stroke([(0.4270, 0.2950), (0.4520, 0.2985), (0.4790, 0.3020)], "flat", "sk_lit",
         size=0.026, load=1.0, pressure="even")
s.stroke([(0.4290, 0.3130), (0.4530, 0.3150), (0.4760, 0.3120)], "flat", "sk_lit",
         size=0.020, load=1.0, pressure="even")
s.stroke([(0.4330, 0.3040), (0.4530, 0.3062), (0.4720, 0.3040)], "round_soft",
         "sk_shad", size=0.017, opacity=0.30, pressure="even")
print("reset:", s.stroke_count - n0)

n0 = s.stroke_count
s.stroke([(0.4255, 0.2920), (0.4460, 0.2872), (0.4640, 0.2896)], "liner", "brow2",
         size=0.0050, load=1.0, pressure="swell")
s.stroke([(0.4640, 0.2896), (0.4730, 0.2942), (0.4800, 0.2998)], "liner", "brow2",
         size=0.0032, load=1.0, pressure="lift_off")
# eye whites first, then the iris on top of them
s.stroke([(0.4486, 0.3116), (0.4522, 0.3096)], "round_hard", "eyew",
         size=0.0060, load=1.0, pressure="even")
s.stroke([(0.4614, 0.3058), (0.4672, 0.3040)], "round_hard", "eyew",
         size=0.0050, load=1.0, pressure="even")
s.dab(0.4562, 0.3074, "round_hard", "iris", size=0.0072)
s.dab(0.4562, 0.3074, "round_hard", "iris", size=0.0060)
s.stroke([(0.4478, 0.3120), (0.4548, 0.3024), (0.4640, 0.3018), (0.4680, 0.3044)],
         "liner", "brow2", size=0.0034, load=1.0, pressure="even")
s.stroke([(0.4484, 0.3142), (0.4562, 0.3160), (0.4668, 0.3098)], "liner", "sk_shad",
         size=0.0032, load=1.0, pressure="taper")
s.dab(0.4546, 0.3058, "round_hard", "catch", size=0.0032)
s.dab(0.4546, 0.3058, "round_hard", "catch", size=0.0028)
print("eye:", s.stroke_count - n0)

# ---- 2. mouth: cut the cream bar back, leave a short tooth ----
n0 = s.stroke_count
s.stroke([(0.4420, 0.4400), (0.4530, 0.4488), (0.4640, 0.4600)], "round_hard",
         "mouth_dk", size=0.0110, load=1.0, pressure="even")
s.stroke([(0.4300, 0.4338), (0.4392, 0.4382)], "liner", "teeth",
         size=0.0055, load=1.0, pressure="even")
s.stroke([(0.4288, 0.4318), (0.4400, 0.4372), (0.4520, 0.4436)], "liner", "sk_mid",
         size=0.0040, load=1.0, pressure="taper")          # upper lip edge
s.stroke([(0.4406, 0.4664), (0.4510, 0.4696), (0.4608, 0.4694)], "liner", "lip2",
         size=0.0060, load=1.0, pressure="swell")
print("mouth:", s.stroke_count - n0)

# ---- 3. moustache, dark and definite ----
n0 = s.stroke_count
s.stroke([(0.4140, 0.4008), (0.4310, 0.4090), (0.4490, 0.4168), (0.4700, 0.4246)],
         "bristle", "must", size=0.016, load=1.0, pressure="swell")
s.stroke([(0.4190, 0.4058), (0.4380, 0.4142), (0.4600, 0.4230)], "bristle", "must",
         size=0.011, load=1.0, pressure="taper")
print("moustache:", s.stroke_count - n0)

# ---- 4. beard: cross the vertical combing, solidify the chin ----
n0 = s.stroke_count
s.stroke([(0.4420, 0.4820), (0.4700, 0.5060), (0.4980, 0.5220)], "bristle", "beard",
         size=0.030, load=1.0, pressure="swell")
s.stroke([(0.4520, 0.5060), (0.4820, 0.5280), (0.5120, 0.5320)], "bristle", "beard",
         size=0.024, load=1.0, pressure="taper")
s.stroke([(0.4680, 0.4560), (0.5020, 0.4820), (0.5320, 0.5020)], "bristle", "beard",
         size=0.026, load=0.9, pressure="taper")
s.stroke([(0.5000, 0.4360), (0.5280, 0.4620), (0.5480, 0.4900)], "bristle", "beard",
         size=0.020, load=0.75, pressure="lift_off")
print("beard:", s.stroke_count - n0)

# ---- 5. nose form and ear ----
n0 = s.stroke_count
s.stroke([(0.4232, 0.3300), (0.4280, 0.3560), (0.4300, 0.3800)], "bristle", "sk_mid",
         size=0.013, load=0.9, pressure="taper")          # far plane of the nose
s.stroke([(0.4128, 0.3260), (0.4118, 0.3520), (0.4108, 0.3740)], "liner", "sk_hi",
         size=0.0060, load=1.0, pressure="swell")          # lit ridge
s.stroke([(0.5880, 0.3060), (0.6010, 0.3180), (0.6000, 0.3400),
          (0.5890, 0.3560)], "round_hard", "ear_c", size=0.0110,
         load=1.0, pressure="even")
s.stroke([(0.5920, 0.3160), (0.5950, 0.3320), (0.5900, 0.3460)], "liner", "sk_shad",
         size=0.0065, load=1.0, pressure="taper")
print("nose/ear:", s.stroke_count - n0)

print("D3:", s.look(region=cell("D3"), reference=REF))
print("D4:", s.look(region=cell("D4"), reference=REF))
print("head:", s.look(region=span("D2", "F5"), reference=REF))
print("TOTAL strokes:", s.stroke_count)
