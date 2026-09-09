# Pass 17: the features. Dark first, then mid, then the few lights.
REF = "C:/temp/Level3.jpg"
p = s.palette
p["brow"]  = p.mix("burnt_umber", "ultramarine", 0.16)
p["iris"]  = p.mix("burnt_umber", "ultramarine", 0.30)
p["eyew"]  = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.30), "titanium_white", 0.80)
p["mouth_dk"] = p.mix("burnt_umber", "alizarin", 0.22)
p["teeth"] = p.mix(p.mix("yellow_ochre", "burnt_sienna", 0.10), "titanium_white", 0.82)
p["lip"]   = p.mix(p.mix("cadmium_red", "burnt_sienna", 0.50), "titanium_white", 0.42)
p["sk_hi"] = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.38), "titanium_white", 0.76)
p["sk_mid"] = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.40), "titanium_white", 0.46)
p["sk_shad"] = p.desaturate(
    p.mix(p.mix("burnt_sienna", "burnt_umber", 0.45), "titanium_white", 0.32), 0.22)
s.dry()

n0 = s.stroke_count
# --- darks ---
s.stroke([(0.4408, 0.3040), (0.4530, 0.3060), (0.4660, 0.3030)], "round_soft",
         "sk_shad", size=0.018, opacity=0.5, pressure="even")          # socket
s.stroke([(0.4250, 0.2916), (0.4420, 0.2874), (0.4600, 0.2900)], "liner",
         "brow", size=0.0080, load=1.0, pressure="swell")              # brow inner
s.stroke([(0.4600, 0.2900), (0.4720, 0.2946), (0.4800, 0.3002)], "liner",
         "brow", size=0.0055, load=1.0, pressure="lift_off")           # brow outer
s.stroke([(0.4475, 0.3128), (0.4530, 0.3018), (0.4620, 0.3010), (0.4675, 0.3040)],
         "liner", "brow", size=0.0060, load=1.0, pressure="even")      # upper lid
s.dab(0.4562, 0.3075, "round_hard", "iris", size=0.0085)
s.dab(0.4562, 0.3075, "round_hard", "iris", size=0.0075)
s.dab(0.4215, 0.3905, "round_hard", "brow", size=0.0075)               # nostril
s.stroke([(0.4380, 0.4390), (0.4500, 0.4472), (0.4610, 0.4570)], "round_hard",
         "mouth_dk", size=0.014, load=1.0, pressure="even")            # mouth cavity
s.stroke([(0.4470, 0.4500), (0.4600, 0.4600), (0.4655, 0.4655)], "round_hard",
         "mouth_dk", size=0.011, load=1.0, pressure="taper")
print("darks:", s.stroke_count - n0)

n0 = s.stroke_count
# --- mids ---
s.stroke([(0.4090, 0.3934), (0.4250, 0.3950), (0.4400, 0.3924)], "liner",
         "sk_shad", size=0.0075, load=1.0, pressure="taper")           # under the nose
s.stroke([(0.4478, 0.3192), (0.4570, 0.3200), (0.4672, 0.3140)], "liner",
         "sk_shad", size=0.0065, load=1.0, pressure="taper")           # lower lid
s.stroke([(0.4400, 0.4670), (0.4500, 0.4700), (0.4610, 0.4700)], "liner",
         "lip", size=0.0085, load=1.0, pressure="swell")               # lower lip
s.stroke([(0.5870, 0.3010), (0.6060, 0.3130), (0.6060, 0.3400),
          (0.5900, 0.3620)], "round_hard", "sk_mid", size=0.013,
         load=1.0, pressure="even")                                    # ear
s.stroke([(0.5920, 0.3120), (0.5960, 0.3300), (0.5900, 0.3480)], "liner",
         "sk_shad", size=0.0080, load=1.0, pressure="taper")           # ear inside
print("mids:", s.stroke_count - n0)

n0 = s.stroke_count
# --- the few lights ---
s.stroke([(0.4292, 0.4332), (0.4430, 0.4396), (0.4560, 0.4452)], "liner",
         "teeth", size=0.0060, load=1.0, pressure="even")              # teeth
s.stroke([(0.4292, 0.4332), (0.4430, 0.4396), (0.4560, 0.4452)], "liner",
         "teeth", size=0.0045, load=1.0, pressure="even")
s.dab(0.4498, 0.3108, "round_hard", "eyew", size=0.0055)
s.dab(0.4498, 0.3108, "round_hard", "eyew", size=0.0045)
s.dab(0.4640, 0.3050, "round_hard", "eyew", size=0.0045)
s.dab(0.4090, 0.3818, "round_hard", "sk_hi", size=0.0065)              # nose tip
s.dab(0.4090, 0.3818, "round_hard", "sk_hi", size=0.0050)
print("lights:", s.stroke_count - n0)

print("D3:", s.look(region=cell("D3"), reference=REF))
print("D4:", s.look(region=cell("D4"), reference=REF))
print("head:", s.look(region=span("D2", "F5"), reference=REF))
print("TOTAL strokes:", s.stroke_count)
