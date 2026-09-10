exec(open("_pal.py").read())
exec(open("_geom.py").read())
exec(open("_plant.py").read())
rng = random.Random(613)
s.dry()

# --- the pane's field spilled over the jamb: give the jamb its edge back --
s.block_in(polygon([(0.5525,0.448),(0.6070,0.448),(0.6010,0.634),(0.5460,0.630)]),
           "flat", "bar", direction=(90,), density=1.0, size=0.026,
           pressure="even", load=1.0, overhang=0)
s.stroke([(0.5555,0.452),(0.5510,0.626)], "liner", "bar_lit", size=0.007,
         pressure=[0.85,0.5,1.0,0.55], load=1.0)
s.stroke([(0.6035,0.455),(0.5985,0.630)], "liner", "wall_dk", size=0.005,
         pressure=[0.4,1.0,0.6], load=1.0)
s.dry()

def along(path, t):
    a, b, c = path
    if t < 0.5:
        u = t*2.0;  return (a[0]+(b[0]-a[0])*u, a[1]+(b[1]-a[1])*u)
    u = (t-0.5)*2.0; return (b[0]+(c[0]-b[0])*u, b[1]+(c[1]-b[1])*u)

def twig(o, ang, ln, col, depth=1, szf=1.0, sagf=0.36):
    path = stem(ang + rng.uniform(-8,8), ln, origin=o, bow=rng.uniform(-0.32,0.32),
                sag=sagf*ln*abs(math.cos(math.radians(ang))), rng=rng)
    s.stroke(path, "bristle", col, size=max(0.006, rng.uniform(0.009,0.020)*szf),
             pressure=rng.choice(["taper","lift_off",[1.0,0.85,0.2]]), load=rng.uniform(0.6,1.0))
    if depth > 0:
        for t in (0.46, 0.74):
            if rng.random() < 0.38: continue
            for side in (1,-1):
                if rng.random() < 0.44: continue
                twig(along(path,t), ang + side*rng.uniform(16,48) + rng.uniform(-10,10),
                     ln*rng.uniform(0.34,0.58), col, depth-1, szf*0.78, sagf)

# --- long branches running from the crown out into the left lobe ---------
for o, ang, ln in [((0.5980,0.4880),158,0.235),((0.5820,0.4700),165,0.255),
                   ((0.6060,0.4600),150,0.210),((0.5700,0.4880),172,0.200),
                   ((0.6140,0.4400),143,0.195)]:
    twig(o, ang, ln * rng.uniform(0.9,1.1), "leaf_dk", depth=2, szf=0.95, sagf=0.28)
# --- fill the gap that made the left lobe read as a separate plant -------
for _ in range(30):
    x = rng.uniform(0.500, 0.615); y = rng.uniform(0.300, 0.500)
    a = math.degrees(math.atan2(0.470 - y, x - 0.630)) + rng.uniform(-50, 50)
    s.stroke(stem(a, rng.uniform(0.024, 0.068), origin=(x,y), bow=rng.uniform(-0.4,0.4),
                  sag=0.0, rng=rng), "bristle",
             "leaf_dk" if rng.random() < 0.80 else "leaf_mid",
             size=rng.uniform(0.009, 0.024), pressure="taper", load=rng.uniform(0.55,0.95))
# --- a few long tips reaching further left and drooping -----------------
for o, ang, ln in [((0.3900,0.3400),178,0.115),((0.3500,0.3900),192,0.095),
                   ((0.4200,0.4400),196,0.105),((0.3300,0.3200),168,0.080),
                   ((0.4600,0.4700),204,0.090),((0.3750,0.4300),200,0.075)]:
    twig(o, ang, ln, "leaf_dk", depth=1, szf=0.72, sagf=0.55)
print(s.stroke_count)
print(s.look())
