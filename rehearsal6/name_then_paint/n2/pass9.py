import math
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
        return p.mix(c, "titanium_white", 0.12) if v > 0.56 else c
    for _ in range(24):
        m=(lo+hi)/2
        if p.value_of(p.mix(tc, dk, m)) > v: lo=m
        else: hi=m
    return p.mix(tc, dk, (lo+hi)/2)
def xl(t): return 0.4995 + 0.0295 * t**1.25
def xr(t): return 0.6705 - 0.0290 * t**1.25
def X(t,u): return (1-u)*xl(t) + u*xr(t)
def Y(t,u): return ((1-u)*(0.5660+t*0.1595) + u*(0.5600+t*0.1645)
                    + (0.013-0.003*t)*math.sin(math.pi*u))
def band(u0,u1,t0=0.0,t1=1.0,n=8):
    ts=[t0+(t1-t0)*i/n for i in range(n+1)]
    return polygon([(X(t,u0),Y(t,u0)) for t in ts]+[(X(t,u1),Y(t,u1)) for t in reversed(ts)])

s.dry()
s.block_in(polygon([(0.424,0.524),(0.508,0.532),(0.506,0.566),(0.422,0.558)]), "flat",
           "wall", density=1.0, size=0.014, direction=(-6,84), load=1.0)
for u0,u1,v,sz,d in [(0.63,0.95,0.185,0.016,0.85),(0.50,0.70,0.262,0.017,0.65),
                     (0.42,0.60,0.315,0.017,0.70),(0.085,0.255,0.545,0.013,0.80),
                     (-0.02,0.075,0.435,0.010,0.85)]:
    s.block_in(band(u0,u1), "bristle", T(v), density=d, size=sz, direction="axis", load=0.9)
s.block_in(band(0.24,0.46), "round_hard", T(0.395), density=0.35, size=0.015,
           pressure="even", load=0.5)
s.block_in(band(0.60,0.74), "round_hard", T(0.225), density=0.35, size=0.013,
           pressure="even", load=0.5)
s.block_in(band(0.90,1.02), "bristle", p.mix(T(0.235),"cadmium_red",0.35), density=0.8,
           size=0.010, direction="axis", load=0.8)
print("strokes:", s.stroke_count)
