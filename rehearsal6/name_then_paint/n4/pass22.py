exec(open("_pal.py").read())
exec(open("_geom.py").read())
exec(open("_plant.py").read())
rng = random.Random(509)
p["dust_l"] = at(p.desaturate(p.mix(_neutral, "cadmium_yellow", 0.22), 0.35), 0.868)
s.dry()

# --- one clean field for the lower pane, then the bars, then the plant ----
s.block_in(polygon([(0.010,0.286),(0.552,0.282),(0.550,0.610),(0.014,0.604)]),
           "flat", "glass", direction=(97, 13), density=1.0, size=0.060,
           pressure="even", load=1.0, overhang=0)
s.dry()
for a, b in [((0.500,0.320),(0.140,0.560)), ((0.300,0.300),(0.060,0.470))]:
    s.glaze([a, b], "dust_l", opacity=0.06)
s.stroke([(0.016,0.2985),(0.290,0.2925)], "flat", "bar", size=0.022,
         pressure="even", load=1.0)
s.stroke([(0.560,0.2795),(0.300,0.2855)], "flat", "bar", size=0.022,
         pressure="even", load=1.0)
s.stroke([(0.028,0.2905),(0.300,0.2845)], "liner", "bar_lit", size=0.005,
         pressure=[0.2,0.9,0.5,0.9,0.3], load=1.0)
s.stroke([(0.310,0.2775),(0.556,0.2725)], "liner", "bar_lit", size=0.005,
         pressure=[0.4,0.9,0.25], load=1.0)
s.stroke([(0.292,0.276),(0.286,0.612)], "flat", "bar", size=0.026,
         pressure="even", load=1.0)
s.stroke([(0.300,0.290),(0.295,0.600)], "liner", "bar_lit", size=0.006,
         pressure=[0.3,1.0,0.7,0.2], load=1.0)
s.dry()

def along(path, t):
    a, b, c = path
    if t < 0.5:
        u = t*2.0;  return (a[0]+(b[0]-a[0])*u, a[1]+(b[1]-a[1])*u)
    u = (t-0.5)*2.0; return (b[0]+(c[0]-b[0])*u, b[1]+(c[1]-b[1])*u)

def twig(o, ang, ln, col, depth=2, szf=1.0):
    path = stem(ang + rng.uniform(-8,8), ln, origin=o, bow=rng.uniform(-0.34,0.34),
                sag=0.36*ln*abs(math.cos(math.radians(ang))), rng=rng)
    s.stroke(path, "bristle", col, size=max(0.006, rng.uniform(0.009, 0.021)*szf),
             pressure=rng.choice(["taper","lift_off",[1.0,0.85,0.2]]), load=rng.uniform(0.6,1.0))
    if depth > 0:
        for t in (0.44, 0.70, 0.90):
            if rng.random() < 0.36: continue
            for side in (1, -1):
                if rng.random() < 0.42: continue
                twig(along(path, t), ang + side*rng.uniform(16,50) + rng.uniform(-10,10),
                     ln*rng.uniform(0.34,0.58), col, depth-1, szf*0.78)

# --- the branch that sweeps left over the window and droops --------------
LEFT = [((0.5150,0.4260),172,0.185),((0.5000,0.3960),163,0.215),((0.4880,0.4550),182,0.150),
        ((0.5300,0.3720),156,0.170),((0.4760,0.4180),176,0.135),((0.5050,0.4700),190,0.120),
        ((0.5350,0.4450),168,0.130),((0.4640,0.3860),160,0.115)]
for o, ang, ln in LEFT:
    twig(o, ang, ln * rng.uniform(0.88, 1.15), "leaf_dk", depth=2, szf=1.0)
for _ in range(22):
    x = rng.uniform(0.300, 0.520); y = rng.uniform(0.360, 0.520)
    a = math.degrees(math.atan2(0.430 - y, x - 0.540)) + rng.uniform(-45, 45)
    s.stroke(stem(a, rng.uniform(0.022, 0.062), origin=(x, y),
                  bow=rng.uniform(-0.4,0.4), sag=0.0, rng=rng), "bristle",
             "leaf_dk" if rng.random() < 0.82 else "leaf_mid",
             size=rng.uniform(0.008, 0.022), pressure="taper", load=rng.uniform(0.55,0.95))
print(s.stroke_count)
print(s.look())
