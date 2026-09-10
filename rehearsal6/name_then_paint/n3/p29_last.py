import math, random
rng = random.Random(457)
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
BX, BASE_Y, BRX, BRY = 0.398, 0.796, 0.084, 0.044
KEYS = [(-1.00,0.815),(-0.93,0.700),(-0.82,0.628),(-0.60,0.590),(-0.25,0.552),
        (0.12,0.512),(0.48,0.474),(0.76,0.452),(0.92,0.482),(1.00,0.512)]
def val(t):
    for i in range(len(KEYS)-1):
        a,b = KEYS[i], KEYS[i+1]
        if a[0] <= t <= b[0]:
            f=(t-a[0])/(b[0]-a[0]); return a[1]+(b[1]-a[1])*f
    return KEYS[-1][1]
s.dry()

# lay the speckled band of glass down solid, ends off the canvas
for i, y in enumerate([0.428, 0.456, 0.484, 0.510]):
    a, b = (-0.22, y + 0.008), (1.22, y - 0.010)
    if i % 2: a, b = b, a
    s.stroke([a, b], "flat", ["sky_h", "sky_w", "sky_h", "sky_w"][i],
             size=[0.062, 0.048, 0.070, 0.044][i], pressure="even",
             load=1.0, load_falloff=0.06)

# a little more life in the wall, following the form, barely there
for t, f0, f1 in [(-0.66, 0.10, 0.62), (-0.42, 0.34, 0.88), (-0.12, 0.06, 0.48),
                  (0.20, 0.40, 0.92), (0.44, 0.12, 0.56), (0.62, 0.44, 0.90),
                  (-0.78, 0.30, 0.72), (0.06, 0.55, 0.95)]:
    k = math.sqrt(max(0., 1-t*t))
    xr, yr = CX + t*RX, RIM_Y + RY*k
    xb, yb = BX + t*BRX, BASE_Y + BRY*k
    pa = (xr*(1-f0) + xb*f0, yr*(1-f0) + yb*f0)
    pb = (xr*(1-f1) + xb*f1, yr*(1-f1) + yb*f1)
    v = val(t) * rng.uniform(0.965, 1.035)
    s.stroke([pa, pb], "bristle", china(v, max(0., min(1., (t+0.35)/1.35))),
             size=rng.choice([0.008, 0.011, 0.014]),
             pressure=rng.choice(["taper", "lift_off"]),
             load=rng.uniform(0.45, 0.7), load_falloff=0.35)

# sign it
s.stroke([(0.031, 0.9665), (0.0385, 0.9525), (0.0475, 0.9490), (0.0565, 0.9545),
          (0.0625, 0.9670)], "liner", "sig", size=0.0055,
         pressure=[0.25, 0.9, 1.0, 0.85, 0.25], note="signature")
print("strokes:", s.stroke_count)
print(s.look(sketch=False))
