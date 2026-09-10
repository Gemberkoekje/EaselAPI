import math, random
rng = random.Random(173)
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
def china(v, warm):
    return at_value(p.mix(CH_C, CH_W, max(0.0, min(1.0, warm))), v)

CX, RIM_Y, RX, RY = 0.393, 0.630, 0.142, 0.074
IRX, IRY = 0.118, 0.056
BX, BASE_Y, BRX, BRY = 0.398, 0.796, 0.084, 0.044

# a hand-drawn value curve across the front wall: rim-light left, bounce right
KEYS = [(-1.00, 0.815), (-0.93, 0.700), (-0.82, 0.628), (-0.60, 0.590),
        (-0.25, 0.552), (0.12, 0.512), (0.48, 0.474), (0.76, 0.452),
        (0.92, 0.482), (1.00, 0.512)]
def val(t):
    for i in range(len(KEYS)-1):
        a, b = KEYS[i], KEYS[i+1]
        if a[0] <= t <= b[0]:
            f = (t - a[0]) / (b[0] - a[0])
            return a[1] + (b[1] - a[1]) * f
    return KEYS[-1][1]

s.dry()
# tidy the pale slabs still on the back of the sill
for x0, x1, y in [(-0.06, 0.245, 0.649), (0.575, 0.735, 0.645), (0.760, 0.905, 0.641)]:
    s.block_in(polygon([(x0, y), (x1, y-0.006), (x1, y+0.052), (x0, y+0.058)]).inset(0.006),
               "flat", "sill", direction=(-2, 22), density=1.0, size=0.016, load=1.0)

# the front wall, in strokes that run down the form
n = 30
for i in range(n):
    t = -0.985 + 1.97 * i / (n - 1.0)
    k = math.sqrt(max(0.0, 1 - t*t))
    x0, y0 = CX + t*RX, RIM_Y + RY*k
    x1, y1 = BX + t*BRX, BASE_Y + BRY*k
    v = val(t) * (1.0 - 0.035*rng.random())
    warm = max(0.0, min(1.0, (t + 0.35) / 1.35))
    col = china(v, warm)
    sz = 0.010 if abs(t) > 0.90 else rng.choice([0.014, 0.019, 0.024])
    s.stroke([(x0, y0 + 0.004), (x0*0.45 + x1*0.55, y0*0.45 + y1*0.55), (x1, y1 - 0.004)],
             "flat", col, size=sz, pressure=rng.choice(["even", "taper", "swell"]),
             load=1.0, load_falloff=0.15)

# scumble the joins: half-value marks laid dry across the steps
for i in range(11):
    t = -0.80 + 1.60 * i / 10.0 + rng.uniform(-0.05, 0.05)
    k = math.sqrt(max(0.0, 1 - t*t))
    f = rng.uniform(0.18, 0.80)
    x = (CX + t*RX)*(1-f) + (BX + t*BRX)*f
    y = (RIM_Y + RY*k)*(1-f) + (BASE_Y + BRY*k)*f
    v = (val(t) + val(t + 0.10)) / 2
    s.stroke([(x - 0.020, y - 0.012), (x + 0.022, y + 0.014)], "bristle",
             china(v, max(0.0, min(1.0, (t+0.35)/1.35))), size=rng.choice([0.012, 0.017]),
             pressure="taper", load=rng.uniform(0.45, 0.7), load_falloff=0.35)

# the rim: the top surface of the china, brightest where it faces the light
MRX, MRY = (RX+IRX)/2, (RY+IRY)/2
def marc(a0, a1, n=14):
    return [(CX + MRX*math.cos(a0+(a1-a0)*i/(n-1.0)),
             RIM_Y + MRY*math.sin(a0+(a1-a0)*i/(n-1.0))) for i in range(n)]
for a0, a1, v, w in [(math.pi, 1.30*math.pi, 0.845, 0.15), (1.28*math.pi, 1.56*math.pi, 0.895, 0.20),
                     (1.54*math.pi, 1.78*math.pi, 0.830, 0.45), (1.76*math.pi, 2.0*math.pi, 0.735, 0.70)]:
    s.stroke(marc(a0, a1), "round_hard", china(v, w), size=0.013,
             pressure="even", load=1.0, load_falloff=0.1)
# the near lip
for a0, a1, v, w in [(0.0, 0.26*math.pi, 0.640, 0.75), (0.24*math.pi, 0.62*math.pi, 0.735, 0.55),
                     (0.60*math.pi, 1.0*math.pi, 0.700, 0.30)]:
    s.stroke(marc(a0, a1), "round_hard", china(v, w), size=0.011,
             pressure="even", load=1.0, load_falloff=0.1)
print("strokes:", s.stroke_count)
print(s.look(region="B4:G8", sketch=False))
