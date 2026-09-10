exec(open("_pal.py").read())
exec(open("_geom.py").read())
exec(open("_pot.py").read())
import random
rng = random.Random(103)
_t2 = p.mix(p.mix("burnt_sienna", "cadmium_red", 0.18), "yellow_ochre", 0.22)
s.dry()

VK = [(-1.00,0.335),(-0.88,0.262),(-0.72,0.228),(-0.56,0.248),(-0.40,0.278),
      (-0.24,0.318),(-0.10,0.368),(0.00,0.405)]
def vof(u):
    for i in range(len(VK)-1):
        if VK[i][0] <= u <= VK[i+1][0]:
            (a,va),(b,vb) = VK[i], VK[i+1]
            return va + (vb-va)*(u-a)/(b-a)
    return VK[-1][1]
CC = {}
def pc(u, dv=0.0):
    k = (round(u,3), round(dv,3))
    if k not in CC:
        CC[k] = at(p.desaturate(p.mix(_t2, "ultramarine", 0.08 + 0.18*min(1.0,-u)), 0.18),
                   max(0.145, vof(u) + dv))
    return CC[k]
def bstroke(u, ya, yb, n=8):
    return [(CX + u * hw(max(0.5545, ya + (yb-ya)*i/(n-1.0))), ya + (yb-ya)*i/(n-1.0))
            for i in range(n)]

# --- grade the shadow side with overlapping strokes, no smudging ----------
for i in range(15):
    u = -1.005 + 1.005 * i / 14.0
    uu = u + rng.uniform(-0.018, 0.018)
    k = (1.0 - min(0.999, uu*uu)) ** 0.5
    ya = max(0.5555, 0.5460 + 0.0325*k + 0.003) + rng.uniform(0.0, 0.009)
    yb = 0.7455 + 0.0140*k - rng.uniform(0.0, 0.017)
    s.stroke(bstroke(uu, ya, yb), "flat", pc(max(-1.0, min(0.0, uu)),
             rng.uniform(-0.016, 0.016)), size=rng.uniform(0.014, 0.019),
             pressure="even", load=1.0)
# arcs so the marks are not all one way
s.stroke(ring(0.6050, 0.013, -0.94, -0.16), "bristle", pc(-0.62, -0.025),
         size=0.011, pressure="taper", load=0.8)
s.stroke(ring(0.6820, 0.017, -0.20, -0.90), "bristle", pc(-0.50, 0.030),
         size=0.010, pressure="lift_off", load=0.6)
s.stroke(ring(0.7280, 0.019, -0.84, -0.10), "bristle", pc(-0.72, -0.040),
         size=0.012, pressure="taper", load=0.85)
s.stroke(ring(0.5760, 0.011, -0.96, 0.30), "bristle", pc(-0.55, -0.060),
         size=0.009, pressure=[0.9,1.0,0.6,0.25], load=0.9)
for x0,y0,x1,y1,sz,ld in [(0.5540,0.6320,0.5700,0.6200,0.007,0.45),
                          (0.5460,0.6820,0.5610,0.6740,0.006,0.40),
                          (0.6440,0.6920,0.6680,0.6840,0.006,0.45)]:
    s.stroke([(x0,y0),(x1,y1)], "bristle", "bloom", size=sz, pressure="taper", load=ld)

# --- the crack goes on last, and is lost at both ends ---------------------
s.stroke([(0.5895,0.5495),(0.5905,0.5620),(0.5865,0.5980),(0.5960,0.6360),
          (0.5880,0.6710),(0.5945,0.7010),(0.5905,0.7250)], "liner", "crackw",
         size=0.0044, pressure=[0.05,0.55,1.0,0.75,1.0,0.5,0.05], load=1.0)
s.stroke([(0.5952,0.5700),(0.5920,0.5990),(0.6008,0.6320)], "liner",
         at(p.desaturate(p.mix(_t2,"cadmium_yellow",0.20),0.22), 0.680),
         size=0.0030, pressure=[0.1,0.9,0.3], load=1.0)
s.stroke([(0.5950,0.6420),(0.6135,0.6620),(0.6255,0.6730)], "liner", "crackw",
         size=0.0034, pressure=[0.85,0.5,0.05], load=1.0)
s.stroke([(0.5860,0.6050),(0.5745,0.6180)], "liner", "crackw",
         size=0.0028, pressure=[0.7,0.05], load=1.0)
print(s.stroke_count)
print(s.look(region="E4:G7"))
