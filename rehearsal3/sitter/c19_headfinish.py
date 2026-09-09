# Pass 19: the ear was an orange horseshoe; the beard was smeared not massed;
# the forehead was a white block. Fix all three, then strands over the forehead.
REF = "C:/temp/Level3.jpg"
p = s.palette
p["h_a"] = p.mix(p.mix("burnt_umber", "yellow_ochre", 0.30), "titanium_white", 0.06)
p["h_d"] = p.mix(p.mix("burnt_umber", "yellow_ochre", 0.18), "titanium_white", 0.04)
p["h_c"] = p.mix(p.mix("yellow_ochre", "burnt_umber", 0.55), "titanium_white", 0.12)
p["beard"]  = p.mix(p.mix("burnt_umber", "burnt_sienna", 0.30), "titanium_white", 0.07)
p["beard2"] = p.mix(p.mix("burnt_umber", "burnt_sienna", 0.42), "titanium_white", 0.18)
p["sk_mid"] = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.40), "titanium_white", 0.46)
p["sk_lit"] = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.44), "titanium_white", 0.62)
p["sk_shad"] = p.desaturate(
    p.mix(p.mix("burnt_sienna", "burnt_umber", 0.45), "titanium_white", 0.32), 0.22)
p["brow2"] = p.mix(p.mix("burnt_umber", "burnt_sienna", 0.25), "titanium_white", 0.11)
p["eyew"]  = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.25), "titanium_white", 0.78)
s.dry()

# ---- the ear: bury the horseshoe in hair, leave a small quiet one ----
n0 = s.stroke_count
s.stroke([(0.5920, 0.2980), (0.6080, 0.3160), (0.6060, 0.3520), (0.5960, 0.3680)],
         "bristle", "h_d", size=0.024, load=1.0, pressure="even")
s.stroke([(0.5790, 0.3140), (0.5900, 0.3220), (0.5910, 0.3400), (0.5830, 0.3500)],
         "round_hard", "sk_mid", size=0.010, load=1.0, pressure="even")
s.stroke([(0.5830, 0.3230), (0.5860, 0.3350)], "liner", "sk_shad",
         size=0.0055, load=1.0, pressure="taper")
print("ear:", s.stroke_count - n0)

# ---- the beard as a mass, strokes running the way it grows ----
n0 = s.stroke_count
BEARD = [
    ([(0.4450, 0.4200), (0.4640, 0.4640), (0.4760, 0.5100)], 0.030, "swell"),
    ([(0.4700, 0.4300), (0.4880, 0.4780), (0.4960, 0.5300)], 0.032, "taper"),
    ([(0.4980, 0.4400), (0.5120, 0.4880), (0.5140, 0.5280)], 0.030, "lift_off"),
    ([(0.5260, 0.4530), (0.5340, 0.4900), (0.5280, 0.5180)], 0.028, "swell"),
    ([(0.5480, 0.4520), (0.5480, 0.4820), (0.5380, 0.5060)], 0.024, "taper"),
    ([(0.4520, 0.4900), (0.4760, 0.5320), (0.5060, 0.5430)], 0.024, "swell"),
]
for pts, sz, pr in BEARD:
    s.stroke(pts, "bristle", "beard", size=sz, load=1.0, pressure=pr)
# the lit right edge of the beard along the jaw
s.stroke([(0.5340, 0.4700), (0.5480, 0.4980), (0.5420, 0.5220)], "bristle", "beard2",
         size=0.013, load=0.8, pressure="taper")
print("beard:", s.stroke_count - n0)

# ---- knock the white forehead back with a warm glaze, and blend the band ----
n0 = s.stroke_count
s.glaze([(0.4180, 0.2320), (0.4600, 0.2660), (0.4980, 0.2960)], "sk_mid", opacity=0.28)
s.smudge([(0.4200, 0.3560), (0.4700, 0.3620), (0.5200, 0.3680)], size=0.030)
s.smudge([(0.4300, 0.2760), (0.4800, 0.2960), (0.5200, 0.3160)], size=0.024)
print("forehead/blend:", s.stroke_count - n0)

# ---- hair falling over the forehead and temple ----
n0 = s.stroke_count
s.stroke([(0.4620, 0.1900), (0.4380, 0.2200), (0.4260, 0.2520)], "bristle", "h_a",
         size=0.013, load=1.0, pressure="lift_off")
s.stroke([(0.4820, 0.1980), (0.4560, 0.2340), (0.4400, 0.2660)], "bristle", "h_d",
         size=0.009, load=1.0, pressure="taper")
s.stroke([(0.5060, 0.2200), (0.4840, 0.2560), (0.4700, 0.2820)], "bristle", "h_c",
         size=0.007, load=1.0, pressure="lift_off")
print("strands:", s.stroke_count - n0)

# ---- brow down a touch, and white on the far side of the iris ----
n0 = s.stroke_count
s.stroke([(0.4280, 0.2968), (0.4470, 0.2932), (0.4640, 0.2952)], "liner", "brow2",
         size=0.0038, load=1.0, pressure="swell")
s.stroke([(0.4602, 0.3050), (0.4652, 0.3038)], "round_hard", "eyew",
         size=0.0042, load=1.0, pressure="even")
print("eye tweak:", s.stroke_count - n0)

print("head:", s.look(region=span("D2", "F5"), reference=REF))
print("whole:", s.look(reference=REF))
print("TOTAL strokes:", s.stroke_count)
