exec(open("_pal.py").read())
exec(open("_geom.py").read())
exec(open("_pot.py").read())
exec(open("_plant.py").read())
exec(open("_paintpot.py").read())
_t2 = p.mix(p.mix("burnt_sienna", "cadmium_red", 0.18), "yellow_ochre", 0.22)
p["pot_dark"] = at(p.mix(_t2, "ultramarine", 0.55), 0.165)
p["bloom"]    = at(p.desaturate(p.mix(_t2, "cerulean", 0.30), 0.55), 0.560)
p["crackw"]   = at(p.mix(_t2, "burnt_umber", 0.55), 0.190)
p["woody"]    = at(p.desaturate(p.mix("burnt_umber", "viridian", 0.22), 0.30), 0.245)
p["woody_l"]  = at(p.desaturate(p.mix("burnt_umber", "yellow_ochre", 0.35), 0.35), 0.420)
paint_pot(727)
rng = random.Random(829)

def along(path, t):
    a, b, c = path
    if t < 0.5:
        u = t*2.0;  return (a[0]+(b[0]-a[0])*u, a[1]+(b[1]-a[1])*u)
    u = (t-0.5)*2.0; return (b[0]+(c[0]-b[0])*u, b[1]+(c[1]-b[1])*u)
def twig(o, ang, ln, col, depth=1, szf=1.0):
    path = stem(ang + rng.uniform(-8,8), ln, origin=o, bow=rng.uniform(-0.34,0.34), rng=rng)
    s.stroke(path, "bristle", col, size=max(0.006, rng.uniform(0.009,0.020)*szf),
             pressure=rng.choice(["taper","lift_off",[1.0,0.85,0.2]]), load=rng.uniform(0.6,1.0))
    if depth > 0:
        for t in (0.48, 0.76):
            if rng.random() < 0.40: continue
            for side in (1,-1):
                if rng.random() < 0.44: continue
                twig(along(path,t), ang + side*rng.uniform(18,50) + rng.uniform(-10,10),
                     ln*rng.uniform(0.34,0.56), col, depth-1, szf*0.78)

# woody stems out of the soil, then sprigs spilling over the rim
for a, ln, o, col, sz in [(94,0.115,(0.6000,0.4915),"woody_l",0.0085),
                          (76,0.130,(0.6210,0.4890),"woody",0.0090),
                          (108,0.100,(0.5800,0.4940),"woody",0.0075),
                          (64,0.118,(0.6480,0.4880),"woody_l",0.0080),
                          (86,0.092,(0.6680,0.4915),"woody",0.0070),
                          (122,0.078,(0.5620,0.4960),"woody_l",0.0065)]:
    s.stroke(stem(a + rng.uniform(-5,5), ln, origin=o, bow=rng.uniform(-0.26,0.26),
                  sag=0.0, rng=rng), "bristle", col, size=sz,
             pressure=[1.0,0.9,0.35], load=0.9)
for o, ang, ln in [((0.5290,0.5015),196,0.100),((0.5470,0.4985),208,0.086),
                   ((0.5690,0.4965),222,0.072),((0.5240,0.5065),186,0.115),
                   ((0.6910,0.4975),330,0.082),((0.7090,0.5005),318,0.100),
                   ((0.7185,0.5065),342,0.068),((0.6610,0.4935),256,0.060),
                   ((0.6110,0.4955),244,0.056),((0.5910,0.4945),232,0.066),
                   ((0.7010,0.4935),300,0.072),((0.5410,0.5035),200,0.066)]:
    twig(o, ang, ln * rng.uniform(0.85,1.15),
         "leaf_dk" if rng.random() < 0.66 else "leaf_mid", depth=1, szf=0.95)
for _ in range(9):
    x = rng.uniform(0.700, 0.762); y = rng.uniform(0.510, 0.588)
    s.stroke(stem(rng.uniform(300,350), rng.uniform(0.016,0.034), origin=(x,y),
                  bow=rng.uniform(-0.3,0.3), sag=0.0, rng=rng), "bristle", "leaf_lit",
             size=rng.uniform(0.006,0.011), pressure="taper", load=0.8)
print(s.stroke_count)
print(s.look(region="D3:H7"))
