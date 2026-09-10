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
def Y(t,u): return ((1-u)*(0.5660 + t*0.1595) + u*(0.5600 + t*0.1645)
                    + (0.013 - 0.003*t) * math.sin(math.pi*u))
def band(u0,u1,t0=0.0,t1=1.0,n=8):
    ts=[t0+(t1-t0)*i/n for i in range(n+1)]
    return polygon([(X(t,u0),Y(t,u0)) for t in ts]+[(X(t,u1),Y(t,u1)) for t in reversed(ts)])

s.dry()
# kill the halo the rim spilled onto the wall
s.block_in(polygon([(0.474,0.494),(0.534,0.500),(0.531,0.531),(0.472,0.526)]), "flat",
           "wall", density=1.0, size=0.014, direction=(-4,86), load=1.0)
s.block_in(band(0.0,1.0).inset(0.015), "flat", T(0.36), density=1.0, size=0.030,
           direction="axis", load=1.0)
# overlapping bands, broken, laid fast so they mix on the canvas
for u0,u1,v,sz in [(-0.02,0.12,0.40,0.014),(0.06,0.28,0.505,0.018),(0.22,0.44,0.425,0.019),
                   (0.38,0.60,0.330,0.019),(0.54,0.76,0.243,0.019),(0.70,0.92,0.183,0.018),
                   (0.885,1.02,0.232,0.012)]:
    col = p.mix(T(v), "cadmium_red", 0.30) if u0 > 0.8 else T(v)
    s.block_in(band(u0,u1), "bristle", col, density=0.75, size=sz, direction="axis", load=0.85)
# a round tip declares no axis - it takes the squareness out of the turns
for u0,u1,v in [(0.20,0.36,0.465),(0.34,0.50,0.375),(0.50,0.66,0.285),(0.64,0.80,0.212)]:
    s.block_in(band(u0,u1), "round_hard", T(v), density=0.42, size=0.016,
               pressure="even", load=0.55)
# less light reaches the foot
s.block_in(band(0.04,0.92,0.72,1.0), "bristle", T(0.255), density=0.4, size=0.014,
           direction="axis", load=0.5)
s.smudge([(X(0.10,0.31),Y(0.10,0.31)),(X(0.88,0.33),Y(0.88,0.33))], size=0.034)
s.smudge([(X(0.12,0.55),Y(0.12,0.55)),(X(0.90,0.57),Y(0.90,0.57))], size=0.032)
s.smudge([(X(0.15,0.78),Y(0.15,0.78)),(X(0.86,0.79),Y(0.86,0.79))], size=0.028)

# --- the rim, restated warm; a nick out of it where the crack starts ---
rim = ellipse((0.5855, 0.5520), 0.0895, 0.0295)
s.block_in(rim, "flat", T(0.40), density=1.0, size=0.015, direction="axis", load=1.0)
s.block_in(polygon([(0.4995,0.5495),(0.528,0.5305),(0.586,0.5240),(0.641,0.5285),
                    (0.630,0.5445),(0.586,0.5390),(0.535,0.5445)]), "bristle", T(0.60),
           density=0.9, size=0.010, direction=(-7,83), load=0.9)
s.block_in(polygon([(0.641,0.5285),(0.6715,0.5455),(0.6685,0.5665),(0.6395,0.5525)]),
           "flat", T(0.245), density=1.0, size=0.009, direction=(50,138), load=1.0)
inside = ellipse((0.5865, 0.5555), 0.0700, 0.0180)
s.block_in(inside, "flat", p.mix(dk, "burnt_sienna", 0.14), density=1.0, size=0.011,
           direction="axis", load=1.0)
s.block_in(polygon([(0.528,0.5490),(0.586,0.5415),(0.646,0.5490),(0.630,0.5545),
                    (0.586,0.5485),(0.544,0.5545)]), "bristle", T(0.225),
           density=0.9, size=0.007, direction=(-4,88), load=0.9)
print("strokes:", s.stroke_count)
