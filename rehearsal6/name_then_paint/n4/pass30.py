exec(open("_pal.py").read())
exec(open("_geom.py").read())
exec(open("_pot.py").read())
exec(open("_plant.py").read())
rng = random.Random(1487)
_t2 = p.mix(p.mix("burnt_sienna", "cadmium_red", 0.18), "yellow_ochre", 0.22)
p["contact2"] = at(p.desaturate(p.mix(_warmgrey, "ultramarine", 0.35), 0.15), 0.235)
s.dry()

VK = [(-1.00,0.335),(-0.88,0.262),(-0.72,0.228),(-0.56,0.248),(-0.40,0.278),
      (-0.24,0.318),(-0.10,0.368),( 0.05,0.415),( 0.25,0.478),( 0.50,0.548),
      ( 0.72,0.596),( 0.88,0.558),( 1.00,0.468)]
def vof(u):
    u = max(-1.0, min(1.0, u))
    for i in range(len(VK)-1):
        if VK[i][0] <= u <= VK[i+1][0]:
            (a,va),(b,vb) = VK[i], VK[i+1]
            return va + (vb-va)*(u-a)/(b-a)
    return VK[-1][1]
CC = {}
def pc(u, dv=0.0):
    k = (round(u,3), round(dv,3))
    if k not in CC:
        base = (p.mix(_t2, "ultramarine", 0.08+0.18*min(1.0,-u)) if u < -0.06
                else p.mix(_t2, "cadmium_yellow", 0.05+0.16*u))
        CC[k] = at(p.desaturate(base, 0.19), max(0.145, vof(u)+dv))
    return CC[k]

# the foot: carry the paint down to the silhouette and darken where it sits
for i in range(21):
    u = -1.00 + 2.00*i/20.0 + rng.uniform(-0.018, 0.018)
    k = (1.0 - min(0.999, u*u)) ** 0.5
    ya = 0.7180 + rng.uniform(0.0, 0.006)
    yb = 0.7480 + 0.0158*k - rng.uniform(0.0, 0.004)
    s.stroke([(CX + u*hw(max(0.5545, ya)), ya),
              (CX + u*hw(0.7480), (ya+yb)/2.0),
              (CX + u*hw(0.7480), yb)], "flat",
             pc(u, -0.055 + rng.uniform(-0.014, 0.014)),
             size=rng.uniform(0.013, 0.018), pressure="even", load=1.0)
s.stroke(ring(0.7420, 0.0195, -0.84, 0.84), "bristle", pc(-0.20, -0.105), size=0.012,
         pressure=[0.5,1.0,0.85,0.4], load=0.9)
s.stroke(arc(CX, 0.7548, 0.0672, 0.0150, 168, 12, 18), "flat", "contact2",
         size=0.0075, pressure="even", load=1.0)
for x, y, sz in [(0.5320,0.7560,0.010),(0.4900,0.7540,0.008),(0.7220,0.7605,0.008)]:
    s.dab(x, y, "round_hard", "contact2", size=sz, press=1)

# lose part of the pot's left edge under a drooping sprig
for o, ang, ln, sz in [((0.5480,0.5480),214,0.075,0.010),((0.5300,0.5180),206,0.062,0.009),
                       ((0.5560,0.5960),222,0.048,0.007)]:
    s.stroke(stem(ang, ln, origin=o, bow=rng.uniform(-0.3,0.3), rng=rng), "bristle",
             "leaf_dk", size=sz, pressure="taper", load=0.85)
print(s.stroke_count)
print(s.look(region="D4:H8"))
