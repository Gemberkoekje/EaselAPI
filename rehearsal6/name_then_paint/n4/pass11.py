exec(open("_pal.py").read())
exec(open("_geom.py").read())
exec(open("_plant.py").read())
p["wall_edge"] = at(p.mix(_warmgrey, "ultramarine", 0.30), 0.355)
exec(open("_bg.py").read())
rebuild_background()
rng = random.Random(31)

def lit_at(x, y):
    """light rakes in from the upper right"""
    return max(0.0, min(1.0, 0.62 * (x - 0.44) / 0.46 + 0.38 * (0.52 - y) / 0.42))

def pick(x, y, bias=0.0):
    f = lit_at(x, y) + bias + rng.uniform(-0.14, 0.14)
    if f < 0.34:  return "leaf_dk"
    if f < 0.62:  return "leaf_mid"
    if f < 0.90:  return "leaf_lit"
    return "leaf_hot"

def along(path, t):
    a, b, c = path
    if t < 0.5:
        u = t * 2.0
        return (a[0] + (b[0]-a[0])*u, a[1] + (b[1]-a[1])*u)
    u = (t - 0.5) * 2.0
    return (b[0] + (c[0]-b[0])*u, b[1] + (c[1]-b[1])*u)

drawn = []
def branch(origin, ang, length, depth, dark_only=False):
    path = stem(ang + rng.uniform(-7, 7), length, origin=origin,
                bow=rng.uniform(-0.32, 0.32), rng=rng)
    mid = along(path, 0.6)
    col = "leaf_dk" if dark_only else pick(*mid, bias=-0.10 + 0.10 * (2 - depth))
    sz = max(0.009, 0.020 * (0.55 + 0.45 * depth) * rng.uniform(0.75, 1.3))
    s.stroke(path, "bristle", col, size=sz,
             pressure=rng.choice(["taper", "lift_off", [1.0, 0.85, 0.2]]),
             load=rng.uniform(0.65, 1.0))
    drawn.append(path)
    if depth <= 0:
        return
    for t in (0.42, 0.66, 0.86):
        if rng.random() < 0.34:
            continue
        o = along(path, t)
        for side in (1, -1):
            if rng.random() < 0.40:
                continue
            branch(o, ang + side * rng.uniform(16, 46) + rng.uniform(-9, 9),
                   length * rng.uniform(0.36, 0.60), depth - 1, dark_only)

# --- porous core: short radial marks with gaps, not a solid block ----------
CORE = hull([(0.470,0.492),(0.492,0.300),(0.586,0.214),(0.735,0.236),
             (0.806,0.352),(0.762,0.466),(0.630,0.508)])
for _ in range(58):
    for _try in range(24):
        x = rng.uniform(0.45, 0.82); y = rng.uniform(0.20, 0.51)
        if CORE.contains(x, y):
            break
    a = math.degrees(math.atan2(CROWN[1] - y, x - CROWN[0])) + rng.uniform(-30, 30)
    ln = rng.uniform(0.035, 0.085)
    s.stroke(stem(a, ln, origin=(x, y), bow=rng.uniform(-0.4, 0.4), sag=0.0, rng=rng),
             "bristle", "leaf_dk" if rng.random() < 0.72 else "leaf_mid",
             size=rng.uniform(0.016, 0.040), pressure="taper",
             load=rng.uniform(0.55, 0.95))

# --- the armature: main branches, each subdividing -------------------------
MAIN = [(166,0.230),(152,0.275),(137,0.225),(124,0.290),(110,0.245),( 97,0.300),
        ( 85,0.250),( 72,0.295),( 60,0.235),( 47,0.275),( 34,0.230),( 21,0.255),
        (  8,0.205),( -6,0.175),(180,0.175),(191,0.140),(201,0.120)]
ORIG = [(0.560,0.500),(0.596,0.492),(0.626,0.486),(0.660,0.490),(0.694,0.498),
        (0.578,0.444),(0.674,0.440),(0.626,0.412),(0.542,0.470),(0.712,0.468)]
for i, (ang, ln) in enumerate(MAIN):
    branch(ORIG[i % len(ORIG)], ang, ln * rng.uniform(0.88, 1.14), 2,
           dark_only=(ang > 120 and rng.random() < 0.6))
print(s.stroke_count)
print(s.look())
