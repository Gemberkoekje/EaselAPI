# Pass 20: the hand, the glove, the carton, the glasses, the background figures.
REF = "C:/temp/Level3.jpg"
p = s.palette
p["hand_lit"] = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.42), "titanium_white", 0.70)
p["hand_mid"] = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.44), "titanium_white", 0.50)
p["hand_shd"] = p.mix(p.mix("burnt_umber", "burnt_sienna", 0.40), "titanium_white", 0.16)
p["glove"]  = p.mix("burnt_umber", "ultramarine", 0.30)
p["coat"]   = p.shade(p.mix("ultramarine", "burnt_umber", 0.62), 0.55)
p["carton"] = p.mix(p.mix("cadmium_red", "cadmium_yellow", 0.58), "titanium_white", 0.08)
p["cart_l"] = p.mix(p.mix("cadmium_red", "cadmium_yellow", 0.70), "titanium_white", 0.30)
p["paper"]  = p.mix(p.mix("yellow_ochre", "burnt_sienna", 0.10), "titanium_white", 0.84)
p["glass"]  = p.mix(p.mix("yellow_ochre", "viridian", 0.20), "titanium_white", 0.72)
p["bgfig"]  = p.mix(p.mix("burnt_umber", "ultramarine", 0.30), "titanium_white", 0.07)
p["bgface"] = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.40), "titanium_white", 0.40)
p["bghair"] = p.mix(p.mix("burnt_sienna", "cadmium_red", 0.30), "titanium_white", 0.14)
p["h_d"]    = p.mix(p.mix("burnt_umber", "yellow_ochre", 0.18), "titanium_white", 0.04)
p["sk_mid"] = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.40), "titanium_white", 0.46)
s.dry()

# ---- the ear again: bristle would not cover it, use a flat ----
n0 = s.stroke_count
s.stroke([(0.5960, 0.2960), (0.6080, 0.3200), (0.6040, 0.3560)], "flat", "h_d",
         size=0.026, load=1.0, pressure="even")
s.stroke([(0.5800, 0.3160), (0.5880, 0.3300), (0.5840, 0.3460)], "round_hard",
         "sk_mid", size=0.009, load=1.0, pressure="even")
print("ear:", s.stroke_count - n0)

# ---- the glove first, the fingers over it ----
n0 = s.stroke_count
for pts, sz in [([(0.2200, 0.5900), (0.2900, 0.6300), (0.3560, 0.6800)], 0.058),
                ([(0.2300, 0.6600), (0.3000, 0.6950), (0.3620, 0.7350)], 0.052),
                ([(0.2600, 0.7250), (0.3300, 0.7550), (0.3900, 0.7900)], 0.046),
                ([(0.3400, 0.6300), (0.3800, 0.7000), (0.4100, 0.7900)], 0.044)]:
    s.stroke(pts, "flat", "glove", size=sz, load=1.0, pressure="even")
print("glove:", s.stroke_count - n0)

n0 = s.stroke_count
FINGERS = [
    ([(0.2410, 0.3970), (0.2360, 0.4700), (0.2310, 0.5480)], 0.017, "hand_lit"),
    ([(0.2760, 0.3910), (0.2700, 0.4700), (0.2630, 0.5520)], 0.018, "hand_lit"),
    ([(0.3080, 0.4070), (0.3000, 0.4800), (0.2930, 0.5620)], 0.017, "hand_mid"),
    ([(0.3360, 0.4380), (0.3290, 0.5000), (0.3220, 0.5720)], 0.015, "hand_mid"),
    ([(0.1900, 0.5080), (0.2070, 0.5520), (0.2280, 0.5920)], 0.020, "hand_lit"),
]
for pts, sz, col in FINGERS:
    s.stroke(pts, "flat", col, size=sz, load=1.0, pressure="even")
s.stroke([(0.2570, 0.4200), (0.2540, 0.4900), (0.2500, 0.5500)], "liner", "hand_shd",
         size=0.006, load=1.0, pressure="taper")
s.stroke([(0.2910, 0.4300), (0.2860, 0.4950), (0.2810, 0.5560)], "liner", "hand_shd",
         size=0.005, load=1.0, pressure="taper")
print("fingers:", s.stroke_count - n0)

# ---- the carton ----
n0 = s.stroke_count
s.stroke([(0.1720, 0.8100), (0.1740, 0.9000), (0.1700, 0.9900)], "flat", "cart_l",
         size=0.036, load=1.0, pressure="even")
s.stroke([(0.2300, 0.8100), (0.2320, 0.9000), (0.2300, 0.9900)], "flat", "carton",
         size=0.052, load=1.0, pressure="even")
s.stroke([(0.2860, 0.8200), (0.2880, 0.9000), (0.2860, 0.9900)], "flat", "carton",
         size=0.040, load=1.0, pressure="even")
s.stroke([(0.1600, 0.7960), (0.2300, 0.7620), (0.3020, 0.7960)], "flat", "cart_l",
         size=0.020, load=1.0, pressure="even")
s.stroke([(0.2380, 0.7560), (0.2380, 0.8000)], "flat", "paper",
         size=0.026, load=1.0, pressure="even")
s.stroke([(0.1780, 0.9200), (0.2600, 0.9280)], "liner", "paper",
         size=0.010, load=1.0, pressure="taper")
print("carton:", s.stroke_count - n0)

# ---- glasses bottom left, phone bottom right ----
n0 = s.stroke_count
s.stroke([(0.0700, 0.9500), (0.0740, 1.0000)], "flat", "glass",
         size=0.030, load=0.9, pressure="even")
s.stroke([(0.1180, 0.9700), (0.1200, 1.0000)], "flat", "glass",
         size=0.022, load=0.9, pressure="even")
s.stroke([(0.6300, 0.9950), (0.6900, 0.9400), (0.7500, 0.9000)], "flat", "glass",
         size=0.034, load=1.0, pressure="even")
print("glass/phone:", s.stroke_count - n0)

# ---- the two background figures on the left ----
n0 = s.stroke_count
s.stroke([(0.2900, 0.3900), (0.3500, 0.3800), (0.4000, 0.4100)], "flat", "bgfig",
         size=0.048, load=1.0, pressure="even")          # the beret
s.stroke([(0.3000, 0.4700), (0.3300, 0.5100), (0.3500, 0.5600)], "bristle", "bghair",
         size=0.034, load=1.0, pressure="taper")         # her red hair
s.stroke([(0.1000, 0.4900), (0.1300, 0.5600), (0.1600, 0.6300)], "flat", "bgfig",
         size=0.056, load=1.0, pressure="even")          # the man at the left
s.stroke([(0.1450, 0.4600), (0.1620, 0.4900)], "flat", "bgface",
         size=0.028, load=1.0, pressure="even")
print("bg figures:", s.stroke_count - n0)

print("whole:", s.look(reference=REF))
print("TOTAL strokes:", s.stroke_count)
