import math, random
rng = random.Random(281)
p = s.palette
def at_value(base, target):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        m=(lo+hi)/2
        if p.value_of(p.tint(base, m)) < target: lo=m
        else: hi=m
    return p.tint(base, (lo+hi)/2)
G = p.desaturate(p.mix("ultramarine", "burnt_sienna", 0.44), 0.30)
Gw = p.desaturate(p.mix("burnt_umber", "yellow_ochre", 0.45), 0.55)
for nm, v, w in [("g1", 0.812, 0.10), ("g2", 0.834, 0.25), ("g3", 0.852, 0.40),
                 ("g4", 0.868, 0.20), ("g5", 0.798, 0.30)]:
    p[nm] = at_value(p.mix(G, Gw, w), v)
s.dry()

CX, RIM_Y, RX, RY = 0.393, 0.630, 0.142, 0.074
def on_cup(x, y):
    if y < RIM_Y - RY - 0.018: return False
    if y > 0.86: return True
    t = (x - CX) / (RX + 0.028)
    return abs(t) < 1.0 and y > 0.545

# break the two pasted glass rectangles with overlapping marks at many angles
placed = 0
while placed < 44:
    x = rng.uniform(-0.10, 1.12); y = rng.uniform(0.455, 0.638)
    L = rng.uniform(0.05, 0.20); a = rng.uniform(-0.85, 0.85)
    dx, dy = L/2*math.cos(a), L/2*math.sin(a)*0.55
    if on_cup(x-dx, y-dy) or on_cup(x+dx, y+dy) or on_cup(x, y): continue
    col = rng.choice(["g1","g2","g3","g2","g4","g3","g5"])
    s.stroke([(x-dx, y-dy), (x+dx, y+dy)], "flat", col,
             size=rng.choice([0.026, 0.038, 0.050, 0.018]), pressure="even",
             load=1.0, load_falloff=0.10)
    placed += 1

# bury the dark bars on the board under short marks of its own colour
for cx, cy, w in [(0.115, 0.882, 0.10), (0.255, 0.892, 0.06), (0.720, 0.878, 0.11),
                  (0.880, 0.874, 0.10)]:
    for _ in range(9):
        x = cx + rng.gauss(0, w*0.55); y = cy + rng.gauss(0, 0.011)
        L = rng.uniform(0.028, 0.070); a = rng.uniform(-0.45, 0.45)
        s.stroke([(x-L/2*math.cos(a), y-L/2*math.sin(a)*0.5),
                  (x+L/2*math.cos(a), y+L/2*math.sin(a)*0.5)], "flat",
                 rng.choice(["sill", "sill_b", "sill_a", "sill"]),
                 size=rng.choice([0.016, 0.022, 0.028]), pressure="even",
                 load=1.0, load_falloff=0.15)
print("strokes:", s.stroke_count)
print(s.look())
