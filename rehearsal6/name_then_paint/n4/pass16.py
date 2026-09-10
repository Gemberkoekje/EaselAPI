exec(open("_pal.py").read())
exec(open("_geom.py").read())
exec(open("_pot.py").read())
import random
rng = random.Random(77)
_t2 = p.mix(p.mix("burnt_sienna", "cadmium_red", 0.18), "yellow_ochre", 0.22)
s.dry()

VK = [(-1.00,0.360),(-0.75,0.262),(-0.50,0.280),(-0.25,0.338),(0.00,0.408),
      ( 0.25,0.478),( 0.50,0.548),( 0.75,0.600),(0.90,0.560),(1.00,0.482)]
def vof(u):
    u = max(-1.0, min(1.0, u))
    for i in range(len(VK) - 1):
        if VK[i][0] <= u <= VK[i+1][0]:
            (a, va), (b, vb) = VK[i], VK[i+1]
            t = (u - a) / (b - a)
            return va + (vb - va) * t
    return VK[-1][1]

CACHE = {}
def pot_color(u, dv=0.0):
    key = (round(u, 2), round(dv, 3))
    if key not in CACHE:
        base = (p.mix(_t2, "ultramarine", 0.09 + 0.17 * min(1.0, -u)) if u < -0.08
                else p.mix(_t2, "cadmium_yellow", 0.05 + 0.16 * u))
        CACHE[key] = at(p.desaturate(base, 0.20), max(0.14, vof(u) + dv))
    return CACHE[key]

def body_stroke(u, ya, yb):
    n = 7
    pts = []
    for i in range(n):
        y = ya + (yb - ya) * i / (n - 1.0)
        pts.append((CX + u * hw(max(0.5545, y)), y))
    return pts

# --- the body, modelled across the form ------------------------------------
for i in range(19):
    u = -1.02 + 2.04 * i / 18.0 + rng.uniform(-0.030, 0.030)
    k = (1.0 - min(0.999, u * u)) ** 0.5
    ya = max(0.5555, 0.5460 + 0.0325 * k + 0.0030) + rng.uniform(0.0, 0.010)
    yb = 0.7455 + 0.0140 * k - rng.uniform(0.0, 0.018)
    s.stroke(body_stroke(u, ya, yb), "flat", pot_color(u, rng.uniform(-0.018, 0.018)),
             size=rng.uniform(0.016, 0.023), pressure="even", load=1.0)

# --- arcs across them, so the marks are not all one way --------------------
s.stroke(ring(0.5900, 0.012, -0.94, -0.25), "bristle", pot_color(-0.62, -0.030),
         size=0.013, pressure=[0.8,1.0,0.5], load=0.9)
s.stroke(ring(0.6350, 0.015,  0.82,  0.12), "bristle", pot_color(0.50, 0.028),
         size=0.012, pressure="lift_off", load=0.7)
s.stroke(ring(0.6900, 0.017, -0.88,  0.30), "bristle", pot_color(-0.30, -0.020),
         size=0.014, pressure="taper", load=0.75)
s.stroke(ring(0.7180, 0.019,  0.86, -0.20), "bristle", pot_color(0.45, 0.020),
         size=0.011, pressure="taper", load=0.65)
s.stroke(ring(0.5730, 0.011, -0.96,  0.96), "bristle", pot_color(-0.20, -0.075),
         size=0.011, pressure=[0.95,1.0,0.85,0.5], load=0.95, note="under the collar")
s.stroke(ring(0.7400, 0.020, -0.80,  0.80), "bristle", pot_color(-0.10, -0.085),
         size=0.013, pressure=[0.5,1.0,0.8,0.4], load=0.9, note="the foot turns under")

# --- the crack: the dark, the lit edge, and one branch ---------------------
CRACK = [(0.5905,0.5620),(0.5865,0.5980),(0.5960,0.6360),(0.5880,0.6710),
         (0.5945,0.7010),(0.5905,0.7240)]
s.stroke(CRACK, "liner", "crack", size=0.0042, pressure=[0.9,1.0,0.7,1.0,0.6,0.3], load=1.0)
s.stroke([(0.5945,0.5690),(0.5910,0.5990),(0.6000,0.6330)], "liner",
         pot_color(0.10, 0.150), size=0.0032, pressure=[0.2,0.9,0.4], load=1.0)
s.stroke([(0.5940,0.6420),(0.6120,0.6610),(0.6230,0.6720)], "liner", "crack",
         size=0.0034, pressure=[0.8,0.5,0.15], load=1.0)
s.stroke([(0.5905,0.5620),(0.5880,0.5480)], "liner", "crack",
         size=0.0038, pressure=[0.9,0.35], load=1.0)
# a chip out of the lip
s.dab(0.5480, 0.5140, "round_hard", "pot_dark", size=0.011, press=2)
s.dab(0.5455, 0.5085, "round_hard", "lip_lit", size=0.006, press=2)
print(s.stroke_count)
print(s.look(region="E4:G7"))
