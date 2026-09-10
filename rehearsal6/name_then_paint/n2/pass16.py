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
        return p.mix(c, "titanium_white", 0.14) if v > 0.56 else c
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
# the pot needs its own light, half and dark, not just its colour
s.block_in(band(0.07,0.27), "bristle", T(0.565), density=0.85, size=0.014,
           direction="axis", load=0.9)
s.block_in(band(0.68,0.93), "bristle", T(0.162), density=0.85, size=0.016,
           direction="axis", load=0.9)
s.block_in(band(0.26,0.44), "round_hard", T(0.430), density=0.45, size=0.014,
           pressure="even", load=0.55)

# --- the near edge of the rim, restated over the leaves that fell across it ---
def arc(a0, a1, n=12):
    out = [(0.5855 + 0.0895*math.cos(a0+(a1-a0)*i/n),
            0.5520 + 0.0300*math.sin(a0+(a1-a0)*i/n)) for i in range(n+1)]
    inn = [(0.5865 + 0.0700*math.cos(a0+(a1-a0)*i/n),
            0.5555 + 0.0145*math.sin(a0+(a1-a0)*i/n)) for i in range(n+1)]
    return polygon(out + list(reversed(inn)))
PI = math.pi
for a0, a1, v, sz in [(PI, PI*0.76, 0.585, 0.011), (PI*0.78, PI*0.55, 0.480, 0.010),
                      (PI*0.56, PI*0.32, 0.375, 0.010), (PI*0.33, PI*0.10, 0.255, 0.010),
                      (PI*0.12, 0.0, 0.205, 0.009)]:
    s.block_in(arc(a0, a1), "flat", T(v), density=1.0, size=sz, direction="axis", load=1.0)
# the shadow the lip throws onto the body is what makes a lip read
for a0, a1, v in [(PI, PI*0.70, 0.205), (PI*0.72, PI*0.36, 0.180), (PI*0.38, 0.0, 0.150)]:
    n = 10
    o = [(0.5855 + 0.0880*math.cos(a0+(a1-a0)*i/n),
          0.5570 + 0.0290*math.sin(a0+(a1-a0)*i/n)) for i in range(n+1)]
    q = [(0.5855 + 0.0855*math.cos(a0+(a1-a0)*i/n),
          0.5680 + 0.0290*math.sin(a0+(a1-a0)*i/n)) for i in range(n+1)]
    s.block_in(polygon(o + list(reversed(q))), "flat", T(v), density=1.0, size=0.008,
               direction="axis", load=1.0)
print("strokes:", s.stroke_count)
