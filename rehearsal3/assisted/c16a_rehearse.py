# Pass 16a — rehearse the opening: dark tea in the hole, pale rim ring around it.
# Run: python -m easel run painting.easel c16a_rehearse.py
REF = r"C:\temp\Level1.jpg"
p = s.palette
M, T, D, S = p.mix, p.tint, p.desaturate, p.shade

p["tea"] = S(M("ultramarine", "burnt_umber", 0.55), 1.0)
p["tea_warm"] = S(M("burnt_umber", "burnt_sienna", 0.30), 0.7)
p["rim_lit"] = T(D(M("cerulean", "burnt_umber", 0.30), 0.20), 0.82)
p["rim_top"] = T(D(M("cerulean", "burnt_umber", 0.34), 0.20), 0.62)
for k in ("tea", "tea_warm", "rim_lit", "rim_top"):
    print(f"{k:9s} {p.hex(p[k])} {p.value_of(p[k]):.3f}")

SPAN = [(0.130, 0.435, 0.520), (0.150, 0.395, 0.565), (0.170, 0.372, 0.590),
        (0.190, 0.358, 0.605), (0.210, 0.352, 0.610), (0.230, 0.357, 0.600),
        (0.250, 0.368, 0.585), (0.270, 0.390, 0.556), (0.288, 0.428, 0.494)]

plan = []
for i, (y, lx, rx) in enumerate(SPAN):
    a, b = (lx, y), (rx, y)
    if i % 2:
        a, b = b, a
    plan.append({"points": [a, b], "brush": "flat", "color": "tea",
                 "size": 0.024, "load": 1.0, "load_falloff": 0.1,
                 "pressure": "even"})

RING = [(0.332, 0.198), (0.352, 0.155), (0.400, 0.126), (0.462, 0.113),
        (0.522, 0.115), (0.572, 0.132), (0.605, 0.160), (0.620, 0.196),
        (0.608, 0.232), (0.575, 0.264), (0.520, 0.290), (0.462, 0.303),
        (0.404, 0.298), (0.362, 0.278), (0.336, 0.248), (0.330, 0.216),
        (0.332, 0.198)]
plan += [
    {"points": RING[0:5], "brush": "flat", "color": "rim_top", "size": 0.017,
     "load": 1.0, "pressure": "even"},
    {"points": RING[4:9], "brush": "flat", "color": "rim_top", "size": 0.020,
     "load": 1.0, "pressure": "even"},
    {"points": RING[8:13], "brush": "flat", "color": "rim_lit", "size": 0.024,
     "load": 1.0, "pressure": "even"},
    {"points": RING[12:17], "brush": "flat", "color": "rim_lit", "size": 0.026,
     "load": 1.0, "pressure": "even"},
]
print("planned:", len(plan))
print(s.rehearse(plan, reference=REF, region=span("C1", "F4")))
print("strokes (unchanged):", s.stroke_count)
