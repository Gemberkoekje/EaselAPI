import math, random
rng = random.Random(191)
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
def china(v, w): return at_value(p.mix(CH_C, CH_W, max(0., min(1., w))), v)
p["h_dk"]   = china(0.360, 0.60)
p["h_lit"]  = china(0.610, 0.35)
p["h_join"] = china(0.300, 0.55)
p["in_top"] = at_value(p.desaturate(p.mix("ultramarine","burnt_sienna",0.40), 0.45), 0.258)
p["in_low"] = at_value(p.desaturate(p.mix("ultramarine","burnt_sienna",0.46), 0.50), 0.405)
p["refl"]   = at_value(p.desaturate(p.mix("ultramarine","burnt_sienna",0.44), 0.30), 0.505)
p["glint"]  = at_value(p.desaturate(p.mix("ultramarine","burnt_sienna",0.50), 0.25), 0.720)
p["crack"]  = at_value(p.mix("burnt_umber", "ultramarine", 0.25), 0.330)
p["bounce"] = china(0.560, 0.90)

CX, RIM_Y, RX, RY = 0.393, 0.630, 0.142, 0.074
IRX, IRY = 0.118, 0.056
BX, BASE_Y, BRX, BRY = 0.398, 0.796, 0.084, 0.044
def bez3(p0, c0, c1, p1, n=24):
    o=[]
    for i in range(n):
        t=i/(n-1.0); u=1-t
        o.append((u**3*p0[0]+3*u*u*t*c0[0]+3*u*t*t*c1[0]+t**3*p1[0],
                  u**3*p0[1]+3*u*u*t*c0[1]+3*u*t*t*c1[1]+t**3*p1[1]))
    return o
def earc(cx, cy, rx, ry, a0, a1, n=16):
    return [(cx+rx*math.cos(a0+(a1-a0)*i/(n-1.0)),
             cy+ry*math.sin(a0+(a1-a0)*i/(n-1.0))) for i in range(n)]

s.dry()
# --- handle: dark first, then the edge that catches the light -------------
hp = bez3((0.524, 0.652), (0.626, 0.658), (0.646, 0.740), (0.506, 0.766))
s.stroke(hp, "round_hard", "h_dk", size=0.019, pressure="even", load=1.0, load_falloff=0.1)
s.stroke(bez3((0.536, 0.648), (0.624, 0.652), (0.640, 0.718), (0.596, 0.748))[:16],
         "round_hard", "h_lit", size=0.007, pressure=[0.35, 1.0, 0.55], load=1.0)
s.stroke([(0.520, 0.660), (0.516, 0.678)], "round_hard", "h_join", size=0.010,
         pressure=[0.9, 0.3], load=1.0)
s.stroke([(0.503, 0.756), (0.500, 0.768)], "round_hard", "h_join", size=0.009,
         pressure=[0.8, 0.3], load=1.0)

# --- inside: darkest under the far rim, lifting toward the tea ------------
s.stroke(earc(CX, RIM_Y, IRX-0.006, IRY-0.005, 1.06*math.pi, 1.94*math.pi),
         "round_hard", "in_top", size=0.013, pressure="even", load=1.0, load_falloff=0.15)
s.stroke(earc(CX, RIM_Y-0.006, IRX-0.022, IRY-0.020, 1.12*math.pi, 1.88*math.pi),
         "round_hard", "in_low", size=0.010, pressure=[0.3, 1.0, 0.4], load=0.85)

# --- the window lying on the cold tea -------------------------------------
s.stroke([(0.328, 0.6555), (0.372, 0.6515), (0.418, 0.6525), (0.452, 0.6575)],
         "round_hard", "refl", size=0.008, pressure=[0.4, 1.0, 0.7, 0.2], load=1.0)
s.stroke([(0.344, 0.664), (0.386, 0.6615)], "round_hard", "refl", size=0.005,
         pressure=[0.2, 0.8], load=0.7)
s.dab(0.3625, 0.6535, "round_hard", "glint", size=0.010, press=3)

# --- warm bounce off the board, along the foot ----------------------------
s.stroke(earc(BX, BASE_Y-0.004, BRX-0.008, BRY-0.010, 0.10*math.pi, 0.92*math.pi),
         "round_hard", "bounce", size=0.010, pressure=[0.25, 1.0, 0.35], load=0.9)

# --- the crack ------------------------------------------------------------
s.stroke([(0.3405, 0.6985), (0.3455, 0.722), (0.3495, 0.7455), (0.3585, 0.771)],
         "liner", "crack", size=0.0055, pressure=[1.0, 0.85, 0.6, 0.25], load=1.0)
s.stroke([(0.3485, 0.7405), (0.3625, 0.7565)], "liner", "crack", size=0.004,
         pressure=[0.7, 0.15], load=1.0)
s.dab(0.3395, 0.6955, "round_hard", "crack", size=0.009, press=2)

print("strokes:", s.stroke_count)
print(s.look(region="C4:G8", sketch=False))
