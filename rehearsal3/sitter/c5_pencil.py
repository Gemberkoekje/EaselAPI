# Pass 5: landmarks + pencil drawing. No paint spent (pencil is free).
REF = "C:/temp/Level3.jpg"
p = s.palette

# ---------------- palette, planned as numbers ----------------
p["coat"]      = p.shade(p.mix("ultramarine", "burnt_umber", 0.62), 0.55)
p["coat_lit"]  = p.mix(p.mix("ultramarine", "burnt_umber", 0.55), "titanium_white", 0.13)
p["bg_dark"]   = p.mix(p.mix("burnt_umber", "ultramarine", 0.25), "titanium_white", 0.12)
p["bg_mid"]    = p.mix(p.mix("burnt_umber", "yellow_ochre", 0.45), "titanium_white", 0.22)
p["bg_lit"]    = p.mix(p.mix("yellow_ochre", "burnt_sienna", 0.30), "titanium_white", 0.48)
p["bg_hi"]     = p.mix(p.mix("yellow_ochre", "burnt_sienna", 0.20), "titanium_white", 0.68)
p["hair_dk"]   = p.mix(p.mix("burnt_umber", "ultramarine", 0.14), "titanium_white", 0.10)
p["hair_mid"]  = p.mix(p.mix("burnt_umber", "yellow_ochre", 0.42), "titanium_white", 0.16)
p["hair_lit"]  = p.mix(p.mix("yellow_ochre", "burnt_umber", 0.38), "titanium_white", 0.36)
p["hair_hi"]   = p.mix(p.mix("yellow_ochre", "burnt_umber", 0.22), "titanium_white", 0.55)
p["beard"]     = p.mix(p.mix("burnt_umber", "burnt_sienna", 0.30), "titanium_white", 0.11)
p["skin_shad"] = p.desaturate(p.mix(p.mix("burnt_sienna", "burnt_umber", 0.40),
                                    "titanium_white", 0.26), 0.18)
p["skin_mid"]  = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.48), "titanium_white", 0.42)
p["skin_lit"]  = p.mix(p.mix("yellow_ochre", "cadmium_red", 0.20), "titanium_white", 0.58)
p["skin_hi"]   = p.mix(p.mix("yellow_ochre", "cadmium_red", 0.14), "titanium_white", 0.76)
p["lip"]       = p.mix(p.mix("cadmium_red", "burnt_sienna", 0.45), "titanium_white", 0.45)
p["carton"]    = p.mix(p.mix("cadmium_red", "cadmium_yellow", 0.60), "titanium_white", 0.10)
p["white_hi"]  = p.mix(p.mix("yellow_ochre", "titanium_white", 0.86), "titanium_white", 0.4)

for n in ("coat", "coat_lit", "bg_dark", "bg_mid", "bg_lit", "bg_hi", "hair_dk",
          "hair_mid", "hair_lit", "hair_hi", "beard", "skin_shad", "skin_mid",
          "skin_lit", "skin_hi", "lip", "carton", "white_hi"):
    print("%-10s %-8s %.2f" % (n, p.hex(p[n]), p.value_of(p[n])))

# ---------------- landmarks, each read off a fine single-cell crop -------------
s.mark("eye",     0.4563, 0.3075)   # pupil          <- cell D3 point(0.65,0.46)
s.mark("brow_a",  0.4250, 0.2913)   # brow front end <- cell D3 point(0.40,0.33)
s.mark("brow_b",  0.4800, 0.2990)   # brow outer end <- cell D3 point(0.84,0.39)
s.mark("nose",    0.4075, 0.3855)   # nose tip       <- cell D4 point(0.28,0.08)
s.mark("mouth",   0.4563, 0.4538)   # mouth cavity   <- cell D4 point(0.65,0.63)
s.mark("chin",    0.4780, 0.5370)   # bottom of beard<- cell D5 top-right
s.mark("ear",     0.5950, 0.3310)   # ear centre     <- cell E3 point(0.76,0.65)
s.mark("temple",  0.4290, 0.2280)   # hairline front
s.mark("hairtop", 0.5300, 0.0790)   # crown
s.mark("hairbk",  0.6784, 0.2780)   # widest point of the hair at the back

# ---------------- the drawing ----------------
PROFILE = [(0.4190, 0.2060), (0.4155, 0.2450), (0.4125, 0.2880), (0.4150, 0.3080),
           (0.4100, 0.3480), s.pt("nose"), (0.4180, 0.3960), (0.4230, 0.4080),
           (0.4290, 0.4200), (0.4360, 0.4433), (0.4414, 0.4688), (0.4475, 0.4930),
           (0.4620, 0.5180), s.pt("chin")]

HAIR_SIL = [(0.4250, 0.2100), (0.4230, 0.1700), (0.4330, 0.1300), (0.4600, 0.1000),
            (0.4950, 0.0830), s.pt("hairtop"), (0.5750, 0.0950), (0.6150, 0.1350),
            (0.6474, 0.2130), s.pt("hairbk"), (0.6700, 0.3300), (0.6659, 0.3704),
            (0.6567, 0.4444), (0.6350, 0.4700)]

HAIRLINE = [(0.4180, 0.2000), s.pt("temple"), (0.4370, 0.2500), (0.4550, 0.2680),
            (0.4815, 0.2860), (0.5100, 0.3050), (0.5400, 0.3250)]

BROW = [s.pt("brow_a"), (0.4400, 0.2870), (0.4600, 0.2900), s.pt("brow_b")]
EYE = [(0.4475, 0.3125), (0.4530, 0.3020), (0.4610, 0.3010), (0.4675, 0.3038),
       (0.4620, 0.3180), (0.4530, 0.3190), (0.4475, 0.3125)]
NOSE_UNDER = [s.pt("nose"), (0.4213, 0.3900), (0.4330, 0.3900), (0.4399, 0.3889)]
MOUSTACHE = [(0.4144, 0.4016), (0.4300, 0.4090), (0.4480, 0.4170), (0.4706, 0.4248)]
MOUTH_DK = [(0.4340, 0.4380), (0.4475, 0.4445), (0.4600, 0.4520), (0.4653, 0.4641),
            (0.4520, 0.4660), (0.4400, 0.4600), (0.4340, 0.4380)]
TEETH = [(0.4290, 0.4329), (0.4420, 0.4390), (0.4568, 0.4456)]
BEARD_OUT = [(0.4475, 0.4930), (0.4620, 0.5180), s.pt("chin"), (0.5100, 0.5330),
             (0.5350, 0.5150), (0.5500, 0.4850), (0.5560, 0.4400), (0.5600, 0.3950),
             (0.5700, 0.3550)]
BEARD_TOP = [(0.4300, 0.4090), (0.4600, 0.4250), (0.4900, 0.4450), (0.5200, 0.4750),
             (0.5400, 0.5050)]
EAR = [(0.5810, 0.2950), (0.6050, 0.3050), (0.6134, 0.3310), (0.6003, 0.3611),
       (0.5864, 0.3657), (0.5760, 0.3450)]
COLLAR = [(0.4800, 0.5450), (0.5200, 0.5750), (0.5650, 0.5900), (0.6000, 0.5750),
          (0.6250, 0.5350)]
COAT_R = [(0.6350, 0.4700), (0.6800, 0.4380), (0.7400, 0.4300), (0.7800, 0.4500),
          (0.8200, 0.5000), (0.8600, 0.5700), (0.8900, 0.6500), (0.9050, 0.7600)]
COAT_L = [(0.3000, 1.0000), (0.3400, 0.9000), (0.3900, 0.8200), (0.4400, 0.7400),
          (0.4800, 0.6800), (0.5100, 0.6200)]
HAND = [(0.2410, 0.3960), (0.2200, 0.4600), (0.1900, 0.5100), (0.1760, 0.5600),
        (0.1900, 0.6300), (0.2200, 0.6900), (0.2600, 0.7300), (0.3200, 0.7500),
        (0.3600, 0.7200)]
F1 = [(0.2410, 0.3960), (0.2350, 0.4700), (0.2300, 0.5400)]
F2 = [(0.2760, 0.3900), (0.2700, 0.4700), (0.2600, 0.5500)]
F3 = [(0.3080, 0.4060), (0.3000, 0.4800), (0.2900, 0.5600)]
THUMB = [(0.1880, 0.5070), (0.2050, 0.5500), (0.2250, 0.5900)]
GLOVE = [(0.2200, 0.5600), (0.2700, 0.5900), (0.3200, 0.6200), (0.3600, 0.6600)]
CARTON = [(0.1500, 0.9900), (0.1550, 0.7900), (0.2300, 0.7530), (0.3060, 0.7900),
          (0.3060, 0.9900)]

for line, pr in [(PROFILE, 0.75), (HAIR_SIL, 0.6), (HAIRLINE, 0.5), (BROW, 0.8),
                 (EYE, 0.8), (NOSE_UNDER, 0.7), (MOUSTACHE, 0.7), (MOUTH_DK, 0.8),
                 (TEETH, 0.6), (BEARD_OUT, 0.6), (BEARD_TOP, 0.5), (EAR, 0.6),
                 (COLLAR, 0.5), (COAT_R, 0.5), (COAT_L, 0.5), (HAND, 0.55),
                 (F1, 0.5), (F2, 0.5), (F3, 0.5), (THUMB, 0.5), (GLOVE, 0.5),
                 (CARTON, 0.5)]:
    s.pencil(line, pressure=pr)

print("drawing whole:", s.look(reference=REF))
print("drawing head :", s.look(region=span("D2", "F5"), reference=REF))
print("strokes:", s.stroke_count)
