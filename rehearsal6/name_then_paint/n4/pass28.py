exec(open("_pal.py").read())
exec(open("_geom.py").read())
exec(open("_pot.py").read())
exec(open("_bg.py").read())
import random
rng = random.Random(1279)
_t2 = p.mix(p.mix("burnt_sienna", "cadmium_red", 0.18), "yellow_ochre", 0.22)
p["arris2"]  = at(p.desaturate(p.mix(_warmgrey, "cadmium_yellow", 0.34), 0.34), 0.790)
p["contact2"]= at(p.desaturate(p.mix(_warmgrey, "ultramarine", 0.35), 0.15), 0.235)
p["sill_ck"] = at(p.desaturate(p.mix(_warmgrey, "ultramarine", 0.25), 0.25), 0.405)
p["bloom"]   = at(p.desaturate(p.mix(_t2, "cerulean", 0.30), 0.55), 0.560)
p["crackw"]  = at(p.mix(_t2, "burnt_umber", 0.55), 0.190)
s.dry()

# 1. the sill top, its shadow and its edge, all together
rebuild_sill()
for x0,y0,x1,y1,sz,col in [(0.048,0.664,0.112,0.652,0.006,"sill_ck"),
                           (0.112,0.652,0.146,0.668,0.005,"sill_ck"),
                           (0.030,0.722,0.084,0.732,0.005,"sill_ck"),
                           (0.062,0.700,0.130,0.694,0.006,"sill_hot"),
                           (0.140,0.716,0.192,0.722,0.005,"sill_hot")]:
    s.stroke([(x0,y0),(x1,y1)], "liner", col, size=sz,
             pressure=[0.2,0.9,0.4,0.7,0.15], load=1.0)
s.dry()

# 2. the pot meets the sill
s.stroke(arc(CX, 0.7535, 0.0730, 0.0170, 166, 14, 20), "flat", "contact2",
         size=0.010, pressure="even", load=1.0)
for x, y, sz in [(0.5240,0.7565,0.011),(0.4820,0.7545,0.009),(0.7180,0.7615,0.009),
                 (0.7480,0.7625,0.007)]:
    s.dab(x, y, "round_hard", "contact2", size=sz, press=1)
s.dry()

# 3. the pot's foot, back on top of it
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
for i in range(25):
    u = -1.01 + 2.02*i/24.0 + rng.uniform(-0.016, 0.016)
    k = (1.0 - min(0.999, u*u)) ** 0.5
    ya = 0.6560
    yb = 0.7455 + 0.0140*k - rng.uniform(0.0, 0.014)
    n = 5
    pts = [(CX + u*hw(max(0.5545, ya+(yb-ya)*j/(n-1.0))), ya+(yb-ya)*j/(n-1.0))
           for j in range(n)]
    s.stroke(pts, "flat", pc(u, rng.uniform(-0.016, 0.016)),
             size=rng.uniform(0.014, 0.020), pressure="even", load=1.0)
s.stroke(ring(0.7020, 0.018,  0.86, -0.10), "bristle", pc( 0.30, 0.026), size=0.011,
         pressure="taper", load=0.70)
s.stroke(ring(0.7300, 0.020, -0.86,  0.86), "bristle", pc(-0.12,-0.085), size=0.013,
         pressure=[0.5,1.0,0.8,0.4], load=0.90)
s.stroke(ring(0.6820, 0.017, -0.20, -0.90), "bristle", pc(-0.50, 0.030), size=0.010,
         pressure="lift_off", load=0.60)
s.stroke([(0.5945,0.6720),(0.5905,0.7010),(0.5940,0.7250)], "liner", "crackw",
         size=0.0040, pressure=[0.9,0.6,0.05], load=1.0)
s.stroke([(0.5460,0.6820),(0.5610,0.6740)], "bristle", "bloom", size=0.006,
         pressure="taper", load=0.40)
s.stroke([(0.6440,0.6920),(0.6680,0.6840)], "bristle", "bloom", size=0.006,
         pressure="taper", load=0.45)
s.dry()

# 4. the face, with a top edge that cannot reach the pot
FACE2 = polygon([(0.0,0.7620),(1.0,0.8020),(1.0,0.8720),(0.0,0.8220)])
s.block_in(FACE2, "flat", "sill_face", direction=(3, 168), density=1.0, size=0.022,
           pressure="even", load=1.0, load_falloff=0.0, overhang=0)
for x0, x1, y, v, sz in [(0.66,0.99,0.826,0.336,0.020),(0.74,0.99,0.852,0.320,0.016),
                         (0.06,0.32,0.812,0.280,0.018),(0.12,0.38,0.844,0.288,0.015),
                         (0.42,0.70,0.832,0.298,0.014)]:
    s.stroke([(x0, y + 0.040*x0), (x1, y + 0.040*x1)], "flat",
             at(p.desaturate(p.mix(_warmgrey, "ultramarine", 0.30), 0.32), v),
             size=sz, pressure="even", load=1.0, load_falloff=0.0)
s.dry()
for a, b, sz, pr in [((0.030,0.7528),(0.176,0.7588),0.0035,[0.1,0.45,0.2]),
                     ((0.248,0.7616),(0.390,0.7674),0.0035,[0.2,0.6,0.15,0.35]),
                     ((0.735,0.7818),(0.868,0.7872),0.0050,[0.3,1.0,0.45,0.9,0.2]),
                     ((0.888,0.7882),(0.994,0.7920),0.0045,[0.5,0.85,0.2])]:
    s.stroke([a, b], "liner", "arris2", size=sz, pressure=pr, load=1.0)
print(s.stroke_count)
print(s.look())
