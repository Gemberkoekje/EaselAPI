p = s.palette; dk = p["dk"]
tc   = p.mix("burnt_sienna", "cadmium_red", 0.30)
warm = p.mix("yellow_ochre", "titanium_white", 0.40)
def T(v):
    lo, hi = 0.0, 1.0
    if v >= p.value_of(tc):
        for _ in range(24):
            m=(lo+hi)/2
            if p.value_of(p.mix(tc, warm, m)) < v: lo=m
            else: hi=m
        c = p.mix(tc, warm, (lo+hi)/2)
        return p.mix(c, "titanium_white", 0.14) if v > 0.56 else c
    for _ in range(24):
        m=(lo+hi)/2
        if p.value_of(p.mix(tc, dk, m)) > v: lo=m
        else: hi=m
    return p.mix(tc, dk, (lo+hi)/2)

crack = [(0.5455,0.5800),(0.5525,0.6120),(0.5450,0.6480),(0.5535,0.6840),
         (0.5475,0.7080),(0.5565,0.7275)]
def shift(pts, d): return [(x+d, y) for x, y in pts]
dark = {"points": crack, "brush": "liner", "color": T(0.125), "size": 0.0038,
        "pressure": [1.0,0.9,1.0,0.8,0.9,0.6]}
lite_r = {"points": shift(crack[:4], 0.0042), "brush": "liner", "color": T(0.615),
          "size": 0.0022, "load": 0.55, "pressure": [0.9,1.0,0.6,0.3]}
lite_l = {"points": shift(crack[:4], -0.0042), "brush": "liner", "color": T(0.615),
          "size": 0.0022, "load": 0.55, "pressure": [0.9,1.0,0.6,0.3]}
s.rehearse([dark, lite_r], region="D5:G7")
s.rehearse([dark, lite_l], region="D5:G7")
s.rehearse([dark], region="D5:G7")
