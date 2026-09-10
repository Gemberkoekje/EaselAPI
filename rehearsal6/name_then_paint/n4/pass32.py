exec(open("_pal.py").read())
exec(open("_geom.py").read())
exec(open("_pot.py").read())
import random
rng = random.Random(1721)
_t2 = p.mix(p.mix("burnt_sienna", "cadmium_red", 0.18), "yellow_ochre", 0.22)
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
def pc(u, dv=0.0):
    base = (p.mix(_t2, "ultramarine", 0.08+0.18*min(1.0,-u)) if u < -0.06
            else p.mix(_t2, "cadmium_yellow", 0.05+0.16*u))
    return at(p.desaturate(base, 0.19), max(0.145, vof(u)+dv))
s.dry()
for i in range(21):
    u = -1.00 + 2.00*i/20.0 + rng.uniform(-0.018, 0.018)
    ya, yb = 0.6180 + rng.uniform(0.0, 0.005), 0.6620 - rng.uniform(0.0, 0.006)
    s.stroke([(CX + u*hw(ya), ya), (CX + u*hw((ya+yb)/2), (ya+yb)/2), (CX + u*hw(yb), yb)],
             "flat", pc(u, rng.uniform(-0.015, 0.015)),
             size=rng.uniform(0.013, 0.018), pressure="even", load=1.0)
s.stroke(ring(0.6400, 0.015,  0.82,  0.12), "bristle", pc( 0.50, 0.028), size=0.012,
         pressure="lift_off", load=0.70)
s.stroke(ring(0.6300, 0.014, -0.92, -0.20), "bristle", pc(-0.58, -0.026), size=0.011,
         pressure="taper", load=0.75)
s.stroke([(0.5915,0.6180),(0.5960,0.6360),(0.5900,0.6620)], "liner",
         at(p.mix(_t2, "burnt_umber", 0.55), 0.190), size=0.0042,
         pressure=[0.7,1.0,0.85], load=1.0)
s.stroke([(0.5950,0.6420),(0.6135,0.6620),(0.6255,0.6730)], "liner",
         at(p.mix(_t2, "burnt_umber", 0.55), 0.190), size=0.0034,
         pressure=[0.85,0.5,0.05], load=1.0)
s.stroke([(0.6440,0.6720),(0.6680,0.6640)], "bristle", "bloom", size=0.006,
         pressure="taper", load=0.45)
print(s.stroke_count)
print(s.look(region="E4:G7"))
