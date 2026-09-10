import math, random
rng = random.Random(401)
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
def bez3(p0,c0,c1,p1,n=24):
    o=[]
    for i in range(n):
        t=i/(n-1.0); u=1-t
        o.append((u**3*p0[0]+3*u*u*t*c0[0]+3*u*t*t*c1[0]+t**3*p1[0],
                  u**3*p0[1]+3*u*u*t*c0[1]+3*u*t*t*c1[1]+t**3*p1[1]))
    return o
s.dry()

# board back where the smudge dragged the cup over it
s.block_in(polygon([(0.548, 0.640), (0.706, 0.634), (0.706, 0.804), (0.498, 0.810),
                    (0.506, 0.760), (0.522, 0.706), (0.538, 0.664)]).inset(0.010),
           "flat", "sill", direction=(-3, 27), density=1.0, size=0.026, load=1.0)
# board's back edge on the left, washed out by the burn strokes
s.block_in(polygon([(-0.06, 0.646), (0.236, 0.638), (0.238, 0.700), (-0.06, 0.712)]).inset(0.008),
           "flat", "sill", direction=(-2, 24), density=1.0, size=0.022, load=1.0)
for i in range(7):
    x = -0.02 + i * 0.040 + rng.uniform(-0.010, 0.010)
    y = 0.648 + rng.uniform(-0.008, 0.007)
    L = rng.uniform(0.048, 0.090)
    s.stroke([(x - L/2, y + 0.006), (x + L/2, y - 0.006)], "bristle",
             rng.choice(["sill", "sill_b", "sill_a"]), size=rng.choice([0.013, 0.019, 0.025]),
             pressure="taper", load=rng.uniform(0.7, 1.0), load_falloff=0.25)

# the cup's two silhouettes, re-laid crisply
for t in [-0.995, -0.975, -0.945, -0.905, -0.86, 0.86, 0.905, 0.945, 0.975, 0.995]:
    k = math.sqrt(max(0., 1-t*t))
    x0, y0 = CX + t*RX, RIM_Y + RY*k
    x1, y1 = BX + t*BRX, BASE_Y + BRY*k
    s.stroke([(x0, y0 + 0.003), (x0*0.45 + x1*0.55, y0*0.45 + y1*0.55), (x1, y1 - 0.003)],
             "flat", china(val(t), max(0., min(1., (t+0.35)/1.35))),
             size=0.009 if abs(t) > 0.94 else 0.013, pressure="even",
             load=1.0, load_falloff=0.12)

# the handle again
hp = bez3((0.524, 0.652), (0.626, 0.658), (0.646, 0.740), (0.506, 0.766))
p["h_dk"]   = china(0.360, 0.60)
p["h_lit"]  = china(0.615, 0.35)
p["h_join"] = china(0.300, 0.55)
s.stroke(hp, "round_hard", "h_dk", size=0.019, pressure="even", load=1.0, load_falloff=0.08)
s.stroke(bez3((0.536, 0.648), (0.624, 0.652), (0.640, 0.718), (0.596, 0.748))[:16],
         "round_hard", "h_lit", size=0.007, pressure=[0.35, 1.0, 0.55], load=1.0)
s.stroke([(0.522, 0.658), (0.518, 0.678)], "round_hard", "h_join", size=0.010,
         pressure=[0.9, 0.3], load=1.0)
s.stroke([(0.504, 0.754), (0.501, 0.768)], "round_hard", "h_join", size=0.009,
         pressure=[0.8, 0.3], load=1.0)

# the shadow's near end, buried by the board patch
s.block_in(polygon([(0.452, 0.794), (0.560, 0.791), (0.648, 0.799), (0.668, 0.818),
                    (0.622, 0.842), (0.520, 0.844), (0.446, 0.834)]).inset(0.008),
           "bristle", "umbra", direction=(4, -12), density=1.0, size=0.014, load=1.0)
s.stroke([(0.464, 0.812), (0.524, 0.818)], "round_hard", "contact",
         size=0.009, pressure=[0.9, 0.15], load=1.0)
# the stray pale flake by the cup's shoulder
s.stroke([(0.190, 0.552), (0.232, 0.556), (0.268, 0.549)], "round_hard", "burn",
         size=0.022, pressure=[0.8, 1.0, 0.15], load=1.0)
print("strokes:", s.stroke_count)
print(s.look(region="B4:G8", sketch=False))
