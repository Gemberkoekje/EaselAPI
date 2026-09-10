import math, random
rng = random.Random(211)
p = s.palette
def at_value(base, target):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        m=(lo+hi)/2
        if p.value_of(p.tint(base, m)) < target: lo=m
        else: hi=m
    return p.tint(base, (lo+hi)/2)
CH_C = p.desaturate(p.mix("ultramarine", "burnt_sienna", 0.42), 0.40)
CH_W = p.desaturate(p.mix("burnt_umber", "yellow_ochre", 0.50), 0.55)
def china(v, w): return at_value(p.mix(CH_C, CH_W, max(0., min(1., w))), v)
CX, RIM_Y, RX, RY = 0.393, 0.630, 0.142, 0.074
IRX, IRY = 0.118, 0.056
BX, BASE_Y, BRX, BRY = 0.398, 0.796, 0.084, 0.044
def earc(cx, cy, rx, ry, a0, a1, n=18):
    return [(cx+rx*math.cos(a0+(a1-a0)*i/(n-1.0)),
             cy+ry*math.sin(a0+(a1-a0)*i/(n-1.0))) for i in range(n)]
KEYS = [(-1.00,0.815),(-0.93,0.700),(-0.82,0.628),(-0.60,0.590),(-0.25,0.552),
        (0.12,0.512),(0.48,0.474),(0.76,0.452),(0.92,0.482),(1.00,0.512)]
def val(t):
    for i in range(len(KEYS)-1):
        a,b = KEYS[i], KEYS[i+1]
        if a[0] <= t <= b[0]:
            f=(t-a[0])/(b[0]-a[0]); return a[1]+(b[1]-a[1])*f
    return KEYS[-1][1]

s.dry()
# bury the over-bright foot band under the wall's own colour
for i in range(13):
    t = -0.86 + 1.72*i/12.0
    k = math.sqrt(max(0., 1-t*t))
    x0, y0 = CX + t*RX*0.80, BASE_Y - 0.055 + BRY*k*0.8
    x1, y1 = BX + t*BRX, BASE_Y + BRY*k
    s.stroke([(x0, y0), (x1, y1-0.003)], "flat", china(val(t)*0.985, (t+0.35)/1.35),
             size=rng.choice([0.013, 0.018]), pressure="even", load=1.0, load_falloff=0.2)
# a quieter warm bounce, broken, only under the left half where the board is lit
for a0, a1, v in [(0.62*math.pi, 0.90*math.pi, 0.520), (0.34*math.pi, 0.58*math.pi, 0.495),
                  (0.12*math.pi, 0.28*math.pi, 0.462)]:
    s.stroke(earc(BX, BASE_Y-0.006, BRX-0.012, BRY-0.012, a0, a1, 10),
             "round_hard", china(v, 0.95), size=0.008,
             pressure=[0.25, 0.9, 0.3], load=rng.uniform(0.6, 0.85))

# the inside: break the ring, darkest upper-left, warmer to the right
for a0, a1, v, w in [(1.02*math.pi, 1.32*math.pi, 0.250, 0.25),
                     (1.30*math.pi, 1.60*math.pi, 0.300, 0.35),
                     (1.58*math.pi, 1.98*math.pi, 0.345, 0.55)]:
    s.stroke(earc(CX, RIM_Y, IRX-0.007, IRY-0.006, a0, a1, 12), "round_hard",
             china(v, w), size=0.012, pressure=[0.3, 1.0, 0.45], load=0.95)
for a0, a1, v, w in [(1.16*math.pi, 1.48*math.pi, 0.360, 0.30),
                     (1.52*math.pi, 1.86*math.pi, 0.425, 0.55)]:
    s.stroke(earc(CX, RIM_Y-0.005, IRX-0.024, IRY-0.021, a0, a1, 10), "round_hard",
             china(v, w), size=0.009, pressure=[0.25, 0.85, 0.3], load=0.8)

# break the comb on the wall: short marks across the form, low contrast
for i in range(18):
    t = rng.uniform(-0.82, 0.90)
    k = math.sqrt(max(0., 1-t*t))
    f = rng.uniform(0.10, 0.90)
    x = (CX+t*RX)*(1-f) + (BX+t*BRX)*f
    y = (RIM_Y+RY*k)*(1-f) + (BASE_Y+BRY*k)*f
    v = val(t) * rng.uniform(0.955, 1.045)
    L = rng.uniform(0.018, 0.046); a = rng.uniform(-0.55, 0.55)
    s.stroke([(x-L/2*math.cos(a), y-L/2*math.sin(a)*0.6),
              (x+L/2*math.cos(a), y+L/2*math.sin(a)*0.6)],
             "bristle", china(v, (t+0.35)/1.35), size=rng.choice([0.009, 0.013, 0.017]),
             pressure=rng.choice(["taper", "lift_off"]), load=rng.uniform(0.4, 0.7),
             load_falloff=0.35)
print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
