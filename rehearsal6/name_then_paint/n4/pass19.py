exec(open("_pal.py").read())
exec(open("_geom.py").read())
exec(open("_pot.py").read())
exec(open("_plant.py").read())
rng = random.Random(211)
p["woody_l"] = at(p.desaturate(p.mix("burnt_umber", "yellow_ochre", 0.35), 0.35), 0.420)
p["woody"]   = at(p.desaturate(p.mix("burnt_umber", "viridian", 0.22), 0.30), 0.245)
s.dry()

def along(path, t):
    a, b, c = path
    if t < 0.5:
        u = t * 2.0
        return (a[0]+(b[0]-a[0])*u, a[1]+(b[1]-a[1])*u)
    u = (t-0.5)*2.0
    return (b[0]+(c[0]-b[0])*u, b[1]+(c[1]-b[1])*u)

def twig(o, ang, ln, col, depth=1, szf=1.0):
    path = stem(ang + rng.uniform(-8, 8), ln, origin=o,
                bow=rng.uniform(-0.34, 0.34), rng=rng)
    s.stroke(path, "bristle", col, size=max(0.006, rng.uniform(0.008, 0.019)*szf),
             pressure=rng.choice(["taper", "lift_off", [1.0, 0.85, 0.2]]),
             load=rng.uniform(0.6, 1.0))
    if depth > 0:
        for t in (0.48, 0.76):
            if rng.random() < 0.42:
                continue
            for side in (1, -1):
                if rng.random() < 0.45:
                    continue
                twig(along(path, t), ang + side*rng.uniform(18, 52) + rng.uniform(-10, 10),
                     ln*rng.uniform(0.34, 0.58), col, depth-1, szf*0.8)

# 1. close the gap between the bush's left fringe and the pot
for _ in range(26):
    x = rng.uniform(0.430, 0.600); y = rng.uniform(0.360, 0.512)
    a = math.degrees(math.atan2(0.500 - y, x - 0.600)) + rng.uniform(-40, 40)
    s.stroke(stem(a, rng.uniform(0.030, 0.075), origin=(x, y),
                  bow=rng.uniform(-0.4, 0.4), sag=0.0, rng=rng), "bristle",
             "leaf_dk" if rng.random() < 0.78 else "leaf_mid",
             size=rng.uniform(0.012, 0.030), pressure="taper", load=rng.uniform(0.55, 0.95))
# and the right shoulder down to the rim
for _ in range(18):
    x = rng.uniform(0.690, 0.870); y = rng.uniform(0.400, 0.512)
    a = math.degrees(math.atan2(0.500 - y, x - 0.660)) + rng.uniform(-40, 40)
    s.stroke(stem(a, rng.uniform(0.028, 0.070), origin=(x, y),
                  bow=rng.uniform(-0.4, 0.4), sag=0.0, rng=rng), "bristle",
             rng.choice(["leaf_dk","leaf_mid","leaf_mid","leaf_lit"]),
             size=rng.uniform(0.011, 0.028), pressure="taper", load=rng.uniform(0.55, 0.95))

# 2. woody stems, taller and light enough to read
for a, ln, o, col, sz in [(94,0.115,(0.6000,0.4915),"woody_l",0.0085),
                          (76,0.130,(0.6210,0.4890),"woody",0.0090),
                          (108,0.100,(0.5800,0.4940),"woody",0.0075),
                          (64,0.118,(0.6480,0.4880),"woody_l",0.0080),
                          (86,0.092,(0.6680,0.4915),"woody",0.0070),
                          (122,0.078,(0.5620,0.4960),"woody_l",0.0065)]:
    s.stroke(stem(a + rng.uniform(-5,5), ln, origin=o, bow=rng.uniform(-0.26,0.26),
                  sag=0.0, rng=rng), "bristle", col, size=sz,
             pressure=[1.0, 0.9, 0.35], load=0.9)

# 3. sprigs spilling over the rim, in front of the pot
FRONT = [((0.5300,0.5010),196,0.105),((0.5480,0.4980),208,0.090),((0.5700,0.4960),222,0.075),
         ((0.5250,0.5060),186,0.120),((0.6900,0.4970),330,0.085),((0.7080,0.5000),318,0.105),
         ((0.7180,0.5060),342,0.070),((0.6600,0.4930),256,0.062),((0.6100,0.4950),244,0.058),
         ((0.5900,0.4940),232,0.068),((0.7000,0.4930),300,0.075),((0.5400,0.5030),200,0.068)]
for o, ang, ln in FRONT:
    twig(o, ang, ln * rng.uniform(0.85, 1.15),
         "leaf_dk" if rng.random() < 0.66 else "leaf_mid", depth=1, szf=0.95)
# a few needles caught by the light on the near sprigs
for _ in range(9):
    x = rng.uniform(0.700, 0.760); y = rng.uniform(0.510, 0.585)
    s.stroke(stem(rng.uniform(300, 350), rng.uniform(0.016, 0.034), origin=(x, y),
                  bow=rng.uniform(-0.3, 0.3), sag=0.0, rng=rng), "bristle", "leaf_lit",
             size=rng.uniform(0.006, 0.011), pressure="taper", load=0.8)
print(s.stroke_count)
print(s.look())
