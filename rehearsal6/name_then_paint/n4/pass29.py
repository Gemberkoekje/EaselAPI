exec(open("_pal.py").read())
exec(open("_geom.py").read())
exec(open("_pot.py").read())
import random
rng = random.Random(1381)
_t2 = p.mix(p.mix("burnt_sienna", "cadmium_red", 0.18), "yellow_ochre", 0.22)
p["bloom"]    = at(p.desaturate(p.mix(_t2, "cerulean", 0.30), 0.55), 0.560)
p["crackw"]   = at(p.mix(_t2, "burnt_umber", 0.55), 0.190)
p["potcatch"] = at(p.desaturate(p.mix(_t2, "cadmium_yellow", 0.36), 0.24), 0.775)
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

# bridge the band the sill cut through the pot - nothing below y=0.575 is buried
for i in range(25):
    u = -1.01 + 2.02*i/24.0 + rng.uniform(-0.016, 0.016)
    ya, yb = 0.5700 + rng.uniform(0.0, 0.006), 0.6880 - rng.uniform(0.0, 0.012)
    n = 5
    pts = [(CX + u*hw(max(0.5545, ya+(yb-ya)*j/(n-1.0))), ya+(yb-ya)*j/(n-1.0))
           for j in range(n)]
    s.stroke(pts, "flat", pc(u, rng.uniform(-0.016, 0.016)),
             size=rng.uniform(0.014, 0.020), pressure="even", load=1.0)
s.stroke(ring(0.5780, 0.011, -0.96, 0.96), "bristle", pc(-0.30, -0.075), size=0.011,
         pressure=[0.95,1.0,0.85,0.5], load=0.95, note="under the collar")
s.stroke(ring(0.6100, 0.013, -0.94, -0.16), "bristle", pc(-0.62, -0.028), size=0.011,
         pressure="taper", load=0.80)
s.stroke(ring(0.6400, 0.015,  0.82,  0.12), "bristle", pc( 0.50,  0.028), size=0.012,
         pressure="lift_off", load=0.70)
s.stroke(ring(0.6700, 0.016, -0.30, -0.88), "bristle", pc(-0.46,  0.026), size=0.010,
         pressure="taper", load=0.65)
for x0,y0,x1,y1,sz,ld in [(0.5540,0.6320,0.5700,0.6200,0.007,0.45),
                          (0.6440,0.6720,0.6680,0.6640,0.006,0.45),
                          (0.6980,0.6100,0.7090,0.5990,0.005,0.40)]:
    s.stroke([(x0,y0),(x1,y1)], "bristle", "bloom", size=sz, pressure="taper", load=ld)
s.stroke([(0.5895,0.5495),(0.5905,0.5620),(0.5865,0.5980),(0.5960,0.6360),
          (0.5885,0.6700)], "liner", "crackw", size=0.0044,
         pressure=[0.05,0.55,1.0,0.75,0.9], load=1.0)
s.stroke([(0.5952,0.5700),(0.5920,0.5990),(0.6008,0.6320)], "liner",
         at(p.desaturate(p.mix(_t2,"cadmium_yellow",0.20),0.22), 0.680),
         size=0.0030, pressure=[0.1,0.9,0.3], load=1.0)
s.stroke([(0.5950,0.6420),(0.6135,0.6620),(0.6255,0.6730)], "liner", "crackw",
         size=0.0034, pressure=[0.85,0.5,0.05], load=1.0)
s.dab(0.7085, 0.5960, "round_hard", "potcatch", size=0.008, press=3)
print(s.stroke_count)
print(s.look())
