import math, random
rng = random.Random(233)
p = s.palette
def at_value(base, target):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        m=(lo+hi)/2
        if p.value_of(p.tint(base, m)) < target: lo=m
        else: hi=m
    return p.tint(base, (lo+hi)/2)
G = p.desaturate(p.mix("ultramarine", "burnt_sienna", 0.40), 0.45)
Gw = p.desaturate(p.mix("burnt_umber", "yellow_ochre", 0.45), 0.60)
p["twig1"] = at_value(G, 0.655)
p["twig2"] = at_value(G, 0.705)
p["twig3"] = at_value(G, 0.752)
p["twig4"] = at_value(p.mix(G, Gw, 0.4), 0.782)
p["grime"] = at_value(p.mix(G, Gw, 0.55), 0.790)
p["grime2"]= at_value(p.mix(G, Gw, 0.35), 0.828)
p["umbra"] = at_value(p.desaturate(p.mix("burnt_umber","ultramarine",0.42), 0.45), 0.335)
for n in ("twig1","twig2","twig3","twig4","grime","grime2","umbra"):
    print(f"{n:7s} {p.hex(p[n])} v={p.value_of(p[n]):.3f}")
s.dry()

def bez3(p0,c0,c1,p1,n=20):
    o=[]
    for i in range(n):
        t=i/(n-1.0); u=1-t
        o.append((u**3*p0[0]+3*u*u*t*c0[0]+3*u*t*t*c1[0]+t**3*p1[0],
                  u**3*p0[1]+3*u*u*t*c0[1]+3*u*t*t*c1[1]+t**3*p1[1]))
    return o

# a bare limb outside the glass, upper right - low contrast, seen through light
limb = [
 (bez3((1.04,0.045),(0.94,0.088),(0.86,0.152),(0.735,0.196)), "twig1", 0.0090, [1.0,0.8,0.45]),
 (bez3((0.735,0.196),(0.688,0.212),(0.652,0.204),(0.604,0.226)), "twig2", 0.0060, [0.7,0.5,0.15]),
 (bez3((0.902,0.118),(0.888,0.196),(0.876,0.256),(0.858,0.330)), "twig2", 0.0058, [0.9,0.6,0.2]),
 (bez3((0.858,0.330),(0.872,0.372),(0.894,0.392),(0.908,0.428)), "twig3", 0.0040, [0.6,0.3,0.1]),
 (bez3((0.806,0.166),(0.782,0.106),(0.766,0.070),(0.752,0.020)), "twig2", 0.0050, [0.8,0.4,0.1]),
 (bez3((0.876,0.256),(0.828,0.286),(0.800,0.318),(0.766,0.362)), "twig3", 0.0042, [0.7,0.35,0.1]),
 (bez3((0.664,0.208),(0.640,0.164),(0.628,0.140),(0.616,0.108)), "twig3", 0.0036, [0.6,0.3,0.1]),
 (bez3((1.04,0.284),(0.966,0.336),(0.918,0.372),(0.856,0.410)), "twig4", 0.0070, [0.8,0.5,0.2]),
 (bez3((0.940,0.352),(0.930,0.406),(0.926,0.436),(0.920,0.472)), "twig4", 0.0038, [0.6,0.3,0.1]),
]
for pts, col, sz, pr in limb:
    s.stroke(pts, "liner", col, size=sz, pressure=pr, load=1.0, load_falloff=0.05)

# grime and old condensation on the glass, strongest at the sides
def haze(cx, cy, n, sx, sy, cols):
    for _ in range(n):
        x = cx + rng.gauss(0, sx); y = cy + rng.gauss(0, sy)
        L = rng.uniform(0.03, 0.12); a = rng.uniform(-0.7, 0.7)
        s.stroke([(x-L/2*math.cos(a), y-L/2*math.sin(a)*0.5),
                  (x+L/2*math.cos(a), y+L/2*math.sin(a)*0.5)], "bristle",
                 rng.choice(cols), size=rng.choice([0.012, 0.020, 0.030]),
                 pressure=rng.choice(["taper","lift_off"]),
                 load=rng.uniform(0.35, 0.6), load_falloff=0.4)
haze(0.075, 0.594, 7, 0.075, 0.030, ["grime", "grime2"])
haze(0.885, 0.578, 7, 0.080, 0.032, ["grime", "grime2"])
haze(0.640, 0.600, 4, 0.060, 0.022, ["grime2"])
haze(0.24, 0.556, 3, 0.050, 0.020, ["grime2"])

# the shadow wants more weight where it leaves the cup
s.block_in(polygon([(0.452, 0.796), (0.560, 0.792), (0.646, 0.800), (0.664, 0.818),
                    (0.620, 0.840), (0.520, 0.842), (0.446, 0.832)]).inset(0.008),
           "bristle", "umbra", direction=(4, -13), density=1.0, size=0.014, load=1.0)

# break the mechanical sawtooth at the top of the bottom dark band
for x, y, sz, col in [(0.16, 0.878, 0.024, "ledge"), (0.46, 0.884, 0.018, "sill_b"),
                      (0.68, 0.874, 0.026, "ledge"), (0.90, 0.868, 0.020, "sill_d"),
                      (0.30, 0.892, 0.016, "sill"), (0.80, 0.892, 0.022, "sill_b")]:
    s.stroke([(x-0.07, y+0.008), (x+0.075, y-0.007)], "bristle", col, size=sz,
             pressure="taper", load=rng.uniform(0.6, 1.0), load_falloff=0.3)
print("strokes:", s.stroke_count)
print(s.look())
