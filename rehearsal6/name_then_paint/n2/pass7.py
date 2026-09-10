import math
p = s.palette; dk = p["dk"]
tc = p.mix("burnt_sienna", "cadmium_red", 0.35)
def T(v):
    lo, hi = 0.0, 1.0
    if v >= p.value_of(tc):
        for _ in range(24):
            m = (lo+hi)/2
            if p.value_of(p.tint(tc, m)) < v: lo = m
            else: hi = m
        return p.tint(tc, (lo+hi)/2)
    for _ in range(24):
        m = (lo+hi)/2
        if p.value_of(p.mix(tc, dk, m)) > v: lo = m
        else: hi = m
    return p.mix(tc, dk, (lo+hi)/2)
print("tc", p.hex(tc), round(p.value_of(tc),2), "| lit", p.hex(T(0.55)), "| core", p.hex(T(0.17)))

def xl(t): return 0.4995 + 0.0295 * t**1.25
def xr(t): return 0.6705 - 0.0290 * t**1.25
def X(t,u): return (1-u)*xl(t) + u*xr(t)
def Y(t,u): return ((1-u)*(0.5660 + t*0.1595) + u*(0.5600 + t*0.1645)
                    + (0.013 - 0.003*t) * math.sin(math.pi*u))
def band(u0, u1, t0=0.0, t1=1.0, n=7):
    ts = [t0 + (t1-t0)*i/n for i in range(n+1)]
    return polygon([(X(t,u0), Y(t,u0)) for t in ts]
                   + [(X(t,u1), Y(t,u1)) for t in reversed(ts)])
body = band(0.0, 1.0)

s.dry()
# the reveal behind the pot's lit edge, darkened while nothing stands on it
s.block_in(polygon([(0.487,0.500),(0.516,0.504),(0.521,0.652),(0.485,0.650)]), "flat",
           p.mix(p["reveal_d"], dk, 0.42), density=1.0, size=0.016, direction=88, load=1.0)
# contact shadow: on the sill, under the pot, so it goes first
s.block_in(polygon([(0.520,0.716),(0.585,0.7305),(0.652,0.7175),(0.700,0.733),
                    (0.610,0.752),(0.524,0.736)]), "flat", T(0.15),
           density=1.0, size=0.016, direction=6, load=1.0)

# --- the pot: one mass, then the light side and the shadow side ---
s.block_in(body.inset(0.016), "flat", T(0.40), density=1.0, size=0.032, direction="axis", load=1.0)
s.block_in(band(0.02, 0.34), "flat", T(0.52), density=1.0, size=0.018, direction="axis", load=1.0)
s.block_in(band(0.10, 0.24), "flat", T(0.585), density=1.0, size=0.013, direction="axis", load=1.0)
s.block_in(band(0.52, 0.94), "flat", T(0.225), density=1.0, size=0.020, direction="axis", load=1.0)
s.block_in(band(0.66, 0.87), "flat", T(0.170), density=1.0, size=0.015, direction="axis", load=1.0)
s.block_in(band(0.925, 1.00), "flat",
           p.mix(T(0.245), "cadmium_red", 0.30), density=1.0, size=0.009, direction="axis", load=1.0)
# lose the turns of the form
for u0, u1, v, sz in [(0.30,0.42,0.455,0.012),(0.44,0.56,0.335,0.012),(0.86,0.94,0.205,0.008)]:
    s.block_in(band(u0,u1), "bristle", T(v), density=0.5, size=sz, direction="axis", load=0.6)
s.smudge([(X(0.15,0.40), Y(0.15,0.40)), (X(0.80,0.42), Y(0.80,0.42))], size=0.026)
s.smudge([(X(0.20,0.54), Y(0.20,0.54)), (X(0.85,0.56), Y(0.85,0.56))], size=0.024)

# --- the rim: far edge, then the inside, then the near edge (that one comes later) ---
rim = ellipse((0.5855, 0.5525), 0.0895, 0.0300)
s.block_in(rim, "flat", T(0.44), density=1.0, size=0.016, direction="axis", load=1.0)
s.block_in(polygon([(0.500,0.550),(0.530,0.531),(0.585,0.5245),(0.640,0.529),
                    (0.628,0.545),(0.585,0.5395),(0.534,0.545)]), "flat", T(0.63),
           density=1.0, size=0.011, direction=(-6, 84), load=1.0)
s.block_in(polygon([(0.640,0.529),(0.672,0.546),(0.669,0.566),(0.640,0.552)]), "flat",
           T(0.28), density=1.0, size=0.010, direction=(52,140), load=1.0)
inside = ellipse((0.5865, 0.5565), 0.0710, 0.0205)
s.block_in(inside, "flat", p.mix(dk, "burnt_sienna", 0.10), density=1.0, size=0.012,
           direction="axis", load=1.0)
s.block_in(polygon([(0.526,0.5495),(0.586,0.5405),(0.648,0.5495),(0.632,0.5555),
                    (0.586,0.5485),(0.542,0.5555)]), "flat", T(0.235),
           density=1.0, size=0.008, direction=(-4,88), load=1.0)
print("strokes:", s.stroke_count)
