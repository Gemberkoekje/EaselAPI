import math
p = s.palette; dk = p["dk"]
tc   = p.mix("burnt_sienna", "cadmium_red", 0.30)
warm = p.mix("yellow_ochre", "titanium_white", 0.40)
pale = p.mix("titanium_white", "yellow_ochre", 0.28)
def T(v):
    lo, hi = 0.0, 1.0
    if v >= p.value_of(tc):
        for _ in range(24):
            m=(lo+hi)/2
            if p.value_of(p.mix(tc, warm, m)) < v: lo=m
            else: hi=m
        c = p.mix(tc, warm, (lo+hi)/2)
        return p.mix(c, "titanium_white", 0.16) if v > 0.56 else c
    for _ in range(24):
        m=(lo+hi)/2
        if p.value_of(p.mix(tc, dk, m)) > v: lo=m
        else: hi=m
    return p.mix(tc, dk, (lo+hi)/2)
def SV(t, b="burnt_umber"):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        m=(lo+hi)/2
        if p.value_of(p.mix(pale, b, m)) > t: lo=m
        else: hi=m
    return p.mix(pale, b, (lo+hi)/2)

s.dry()
crack = [(0.5455,0.5800),(0.5525,0.6120),(0.5450,0.6480),(0.5535,0.6840),
         (0.5475,0.7080),(0.5565,0.7275)]
s.stroke(crack, "liner", T(0.125), size=0.0038, pressure=[1.0,0.9,1.0,0.8,0.9,0.55])
s.stroke([(x+0.0044, y) for x, y in crack[:4]], "liner", T(0.720),
         size=0.0028, load=0.6, pressure=[0.85,1.0,0.55,0.2])
# the chip the crack starts from: a bite out of the lip
s.block_in(polygon([(0.5385,0.5695),(0.5510,0.5710),(0.5495,0.5815),(0.5375,0.5790)]),
           "flat", T(0.185), density=1.0, size=0.006, direction=(72,160), load=1.0)
s.stroke([(0.5380,0.5700),(0.5500,0.5716)], "liner", T(0.660), size=0.0026, load=0.7)
# old clay: a few dry marks, close in value to what they land on
for a, b, v, w, ld in [((0.5220,0.6180),(0.5300,0.6960),0.470,0.006,0.35),
                       ((0.6180,0.5960),(0.6080,0.6900),0.300,0.007,0.35),
                       ((0.5720,0.6420),(0.5680,0.7080),0.400,0.005,0.30),
                       ((0.6420,0.6040),(0.6360,0.6720),0.215,0.006,0.35)]:
    s.stroke([a,b], "bristle", T(v), size=w, load=ld, pressure="lift_off")

# --- the mullion's shadow has to be darker than everything it lies on ---
def sx(t): return 0.2790 + 0.098*t
for y0, y1, v in [(0.650,0.700,0.455),(0.698,0.752,0.400),(0.750,0.800,0.352)]:
    t0=(y0-0.648)/0.152; t1=(y1-0.648)/0.152
    s.block_in(polygon([(sx(t0)+0.002,y0),(sx(t0)+0.021,y0),
                        (sx(t1)+0.021,y1),(sx(t1)+0.002,y1)]),
               "flat", SV(v), density=1.0, size=0.010, direction="axis", load=1.0)
s.smudge([(sx(0.10)+0.001,0.665),(sx(0.55)+0.003,0.732)], size=0.024)
s.smudge([(sx(0.55)+0.022,0.732),(sx(0.95)+0.021,0.792)], size=0.022)

# --- the pot bounces a little warmth back onto the sill ---
s.block_in(blob((0.4880,0.7330), 0.034, 0.015, wobble=0.5, seed=59), "bristle",
           p.mix(SV(0.620), "burnt_sienna", 0.22), density=0.4, size=0.012, load=0.45,
           direction=(-8, 84))
# --- the fallen petals were shouting: quiet them down ---
for x, y, w, t, c in [(0.4180,0.7420,0.0140,28,p.mix("cadmium_red","burnt_sienna",0.45)),
                      (0.3660,0.7660,0.0120,-52,p.mix("cadmium_red",dk,0.30))]:
    dx = math.cos(math.radians(t))*w*0.45; dy = math.sin(math.radians(t))*w*0.45
    s.stroke([(x-dx,y-dy),(x+dx,y+dy)], "round_hard", c, size=w, pressure="even", load=1.0)
s.stroke([(0.3612,0.7648),(0.3700,0.7672)], "round_hard", p.mix("cadmium_red","alizarin",0.3),
         size=0.0075, pressure="even")

# --- a little life in the empty stretch of sill ---
for a, b, v, w, ld in [((0.0800,0.6980),(0.2300,0.7020),0.690,0.011,0.35),
                       ((0.1400,0.7560),(0.2450,0.7500),0.640,0.009,0.30),
                       ((0.4400,0.6900),(0.5050,0.6960),0.560,0.010,0.35),
                       ((0.0500,0.8340),(0.1900,0.8300),0.365,0.010,0.35),
                       ((0.2600,0.8480),(0.3900,0.8420),0.395,0.009,0.30)]:
    s.stroke([a,b], "bristle", SV(v), size=w, load=ld, pressure="lift_off")
s.stroke([(0.1980,0.6720),(0.2080,0.7620)], "bristle", SV(0.660), size=0.008, load=0.30)
print("strokes:", s.stroke_count)
