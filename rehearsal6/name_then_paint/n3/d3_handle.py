import math
p = s.palette
def at_value(base, target):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        m = (lo+hi)/2
        if p.value_of(p.tint(base, m)) < target: lo = m
        else: hi = m
    return p.tint(base, (lo+hi)/2)
CH_C = p.desaturate(p.mix("ultramarine", "burnt_sienna", 0.42), 0.40)
CH_W = p.desaturate(p.mix("burnt_umber", "yellow_ochre", 0.50), 0.55)
p["h_lit"] = at_value(p.mix(CH_C, CH_W, 0.45), 0.600)
p["h_dk"]  = at_value(p.mix(CH_C, CH_W, 0.60), 0.360)

def bez3(p0, c0, c1, p1, n=22):
    out = []
    for i in range(n):
        t = i/(n-1.0); u = 1-t
        out.append((u**3*p0[0]+3*u*u*t*c0[0]+3*u*t*t*c1[0]+t**3*p1[0],
                    u**3*p0[1]+3*u*u*t*c0[1]+3*u*t*t*c1[1]+t**3*p1[1]))
    return out
path = bez3((0.524, 0.652), (0.626, 0.658), (0.646, 0.740), (0.506, 0.766))
A = [{"points": path, "brush": "round_hard", "color": "h_dk", "size": 0.020,
      "pressure": "even", "load": 1.0}]
B = [{"points": path, "brush": "round_hard", "color": "h_dk", "size": 0.014,
      "pressure": "even", "load": 1.0}]
print(s.rehearse(A, region="D5:G7"))
print(s.rehearse(B, region="D5:G7"))
