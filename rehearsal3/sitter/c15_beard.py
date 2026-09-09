# Pass 15: cut the profile with the background's own colour, then the beard.
REF = "C:/temp/Level3.jpg"
p = s.palette
p["bg_dark"] = p.mix(p.mix("burnt_umber", "ultramarine", 0.25), "titanium_white", 0.10)
p["bg_blur"] = p.desaturate(
    p.mix(p.mix("burnt_umber", "yellow_ochre", 0.35), "titanium_white", 0.24), 0.35)
p["beard"]   = p.mix(p.mix("burnt_umber", "burnt_sienna", 0.32), "titanium_white", 0.09)
p["beard_l"] = p.mix(p.mix("burnt_umber", "burnt_sienna", 0.40), "titanium_white", 0.24)
p["must"]    = p.mix("burnt_umber", "ultramarine", 0.12)
for n in ("bg_dark", "bg_blur", "beard", "beard_l", "must"):
    print(n, p.hex(p[n]), round(p.value_of(p[n]), 2))
s.dry()

# --- the edge is where two masses meet: lay the background UP TO the profile ---
n0 = s.stroke_count
OUTSIDE = [(0.401, 0.200), (0.398, 0.245), (0.395, 0.288), (0.397, 0.308),
           (0.392, 0.348), (0.390, 0.386), (0.400, 0.398), (0.406, 0.410),
           (0.412, 0.422), (0.419, 0.444)]
s.stroke(OUTSIDE, "flat", "bg_dark", size=0.034, load=1.0, pressure="even")
s.stroke([(0.372, 0.180), (0.368, 0.300), (0.372, 0.420)], "flat", "bg_dark",
         size=0.046, load=1.0, pressure="swell")
s.stroke([(0.386, 0.170), (0.382, 0.270), (0.386, 0.360)], "bristle", "bg_dark",
         size=0.038, load=0.9, pressure="taper")
s.stroke([(0.400, 0.452), (0.412, 0.478), (0.424, 0.500)], "flat", "bg_blur",
         size=0.030, load=1.0, pressure="even")
print("profile cut:", s.stroke_count - n0)

# --- the beard, strokes running the way it grows ---
n0 = s.stroke_count
BEARD = [
    ([(0.4180, 0.4020), (0.4300, 0.4400), (0.4400, 0.4780)], "beard",   0.030, "taper"),
    ([(0.4400, 0.4130), (0.4520, 0.4560), (0.4620, 0.5060)], "beard",   0.032, "swell"),
    ([(0.4650, 0.4230), (0.4750, 0.4700), (0.4820, 0.5260)], "beard",   0.034, "taper"),
    ([(0.4900, 0.4350), (0.4980, 0.4810), (0.5020, 0.5300)], "beard",   0.034, "lift_off"),
    ([(0.5150, 0.4520), (0.5220, 0.4950), (0.5230, 0.5290)], "beard_l", 0.032, "taper"),
    ([(0.5380, 0.4700), (0.5400, 0.5050), (0.5330, 0.5290)], "beard_l", 0.028, "swell"),
    ([(0.5560, 0.4000), (0.5570, 0.4460), (0.5490, 0.4900)], "beard_l", 0.030, "taper"),
    ([(0.5680, 0.3600), (0.5700, 0.3960), (0.5640, 0.4300)], "beard",   0.022, "lift_off"),
]
for pts, col, sz, pr in BEARD:
    s.stroke(pts, "bristle", col, size=sz, load=1.0, pressure=pr)
print("beard:", s.stroke_count - n0)

# stubble on the cheek — dry brush, not a mass
n0 = s.stroke_count
s.stroke([(0.462, 0.398), (0.502, 0.424), (0.540, 0.456)], "bristle", "beard_l",
         size=0.022, load=0.42, pressure="taper")
s.stroke([(0.486, 0.386), (0.522, 0.414), (0.552, 0.444)], "bristle", "beard_l",
         size=0.016, load=0.38, pressure="lift_off")
print("stubble:", s.stroke_count - n0)

# the moustache: dark, thick, one mark
n0 = s.stroke_count
s.stroke([(0.4144, 0.4016), (0.4300, 0.4095), (0.4480, 0.4175), (0.4706, 0.4250)],
         "bristle", "must", size=0.019, load=1.0, pressure="swell")
print("moustache:", s.stroke_count - n0)

print("head:", s.look(region=span("D2", "F5"), reference=REF))
print("TOTAL strokes:", s.stroke_count)
