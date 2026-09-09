# Pass 16: PREVIEW the feature marks against the fine grid before spending them.
REF = "C:/temp/Level3.jpg"
p = s.palette
p["brow"]  = p.mix("burnt_umber", "ultramarine", 0.16)
p["iris"]  = p.mix("burnt_umber", "ultramarine", 0.30)
p["eyew"]  = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.30), "titanium_white", 0.80)
p["mouth_dk"] = p.mix("burnt_umber", "alizarin", 0.22)
p["teeth"] = p.mix(p.mix("yellow_ochre", "burnt_sienna", 0.10), "titanium_white", 0.84)
p["lip"]   = p.mix(p.mix("cadmium_red", "burnt_sienna", 0.50), "titanium_white", 0.42)
p["sk_hi"] = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.38), "titanium_white", 0.76)
p["sk_shad"] = p.desaturate(
    p.mix(p.mix("burnt_sienna", "burnt_umber", 0.45), "titanium_white", 0.32), 0.22)
for n in ("brow", "iris", "eyew", "mouth_dk", "teeth", "lip"):
    print(n, p.hex(p[n]), round(p.value_of(p[n]), 2))

EYE_AREA = [
    {"points": [(0.4250, 0.2916), (0.4420, 0.2874), (0.4600, 0.2900)],
     "brush": "liner", "color": "brow", "size": 0.009, "label": "brow-in"},
    {"points": [(0.4600, 0.2900), (0.4720, 0.2946), (0.4800, 0.3000)],
     "brush": "liner", "color": "brow", "size": 0.006, "label": "brow-out"},
    {"points": [(0.4475, 0.3128), (0.4530, 0.3018), (0.4620, 0.3010),
                (0.4675, 0.3040)],
     "brush": "liner", "color": "brow", "size": 0.006, "label": "lid"},
    {"points": [(0.4548, 0.3072), (0.4578, 0.3078)],
     "brush": "round_hard", "color": "iris", "size": 0.009, "label": "iris"},
    {"points": [(0.4494, 0.3110), (0.4514, 0.3106)],
     "brush": "round_hard", "color": "eyew", "size": 0.006, "label": "white-in"},
    {"points": [(0.4630, 0.3052), (0.4655, 0.3046)],
     "brush": "round_hard", "color": "eyew", "size": 0.005, "label": "white-out"},
    {"points": [(0.4475, 0.3190), (0.4560, 0.3200), (0.4660, 0.3140)],
     "brush": "liner", "color": "sk_shad", "size": 0.007, "label": "lower-lid"},
]

NOSE_MOUTH = [
    {"points": [(0.4198, 0.3898), (0.4232, 0.3912)],
     "brush": "round_hard", "color": "brow", "size": 0.008, "label": "nostril"},
    {"points": [(0.4090, 0.3930), (0.4250, 0.3948), (0.4400, 0.3922)],
     "brush": "liner", "color": "sk_shad", "size": 0.008, "label": "under-nose"},
    {"points": [(0.4085, 0.3800), (0.4098, 0.3840)],
     "brush": "round_hard", "color": "sk_hi", "size": 0.007, "label": "nose-tip-lit"},
    {"points": [(0.4380, 0.4390), (0.4500, 0.4470), (0.4620, 0.4580),
                (0.4650, 0.4650)],
     "brush": "round_hard", "color": "mouth_dk", "size": 0.014, "label": "mouth-dark"},
    {"points": [(0.4292, 0.4330), (0.4430, 0.4394), (0.4568, 0.4456)],
     "brush": "liner", "color": "teeth", "size": 0.006, "label": "teeth"},
    {"points": [(0.4400, 0.4668), (0.4500, 0.4696), (0.4610, 0.4700)],
     "brush": "liner", "color": "lip", "size": 0.008, "label": "lower-lip"},
]

print("D3 preview:", s.preview(EYE_AREA, reference=REF, region=cell("D3"), grid="fine"))
print("D4 preview:", s.preview(NOSE_MOUTH, reference=REF, region=cell("D4"), grid="fine"))
print("strokes (unchanged):", s.stroke_count)
