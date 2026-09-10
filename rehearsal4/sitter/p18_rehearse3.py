p = s.palette

def to_value(base, target):
    other = "titanium_white" if p.value_of(base) < target else "burnt_umber"
    lo, hi = 0.0, 1.0
    for _ in range(28):
        mid = (lo + hi) / 2.0
        v = p.value_of(p.mix(base, other, mid))
        if (v < target) == (other == "titanium_white"):
            lo = mid
        else:
            hi = mid
    return p.mix(base, other, (lo + hi) / 2.0)

p["bgL"] = to_value(p.mix("burnt_umber", "yellow_ochre", 0.35), 0.22)

plan = [
    # 1. the background painted back UP TO the profile — the edge is where two
    #    masses meet, not a line drawn round one
    dict(points=[(0.396, 0.244), (0.390, 0.312), (0.386, 0.376)], brush="bristle",
         color="deep", size=0.036),
    dict(points=[(0.388, 0.372), (0.400, 0.412), (0.408, 0.452)], brush="bristle",
         color="deep", size=0.030),
    dict(points=[(0.404, 0.446), (0.414, 0.492), (0.430, 0.532)], brush="bristle",
         color="bgL", size=0.030),
    # 2. the eye
    dict(points=[(0.428, 0.288), (0.452, 0.284), (0.468, 0.288)], brush="liner",
         color="hair_d", size=0.006),
    dict(points=[(0.4605, 0.3035), (0.4655, 0.3035)], brush="round_hard",
         color="eyew", size=0.007),
    dict(points=[(0.4515, 0.3055), (0.4535, 0.3065)], brush="round_hard",
         color="iris", size=0.009),
    # 3. nose and moustache
    dict(points=[(0.412, 0.352), (0.406, 0.374)], brush="round_hard",
         color="skin_v", size=0.006),
    dict(points=[(0.428, 0.399), (0.434, 0.403)], brush="round_hard",
         color="beard", size=0.007),
    dict(points=[(0.418, 0.413), (0.444, 0.406), (0.464, 0.416)], brush="bristle",
         color="beard", size=0.013),
    # 4. mouth
    dict(points=[(0.437, 0.448), (0.456, 0.450)], brush="round_hard",
         color="iris", size=0.008),
    dict(points=[(0.441, 0.459), (0.458, 0.461)], brush="round_hard",
         color="lip", size=0.006),
    # 5. chin beard, down and to the left
    dict(points=[(0.430, 0.476), (0.444, 0.516), (0.468, 0.545)], brush="bristle",
         color="beard", size=0.020),
]
print(s.rehearse(plan, reference="ref.jpg", region=span("D3", "D4")))
