import math
p = s.palette
def at_value(base, target):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        m=(lo+hi)/2
        if p.value_of(p.tint(base, m)) < target: lo=m
        else: hi=m
    return p.tint(base, (lo+hi)/2)
G  = p.desaturate(p.mix("ultramarine", "burnt_sienna", 0.40), 0.45)
Gw = p.desaturate(p.mix("burnt_umber", "yellow_ochre", 0.45), 0.60)
CH_C = p.desaturate(p.mix("ultramarine", "burnt_sienna", 0.42), 0.40)
CH_W = p.desaturate(p.mix("burnt_umber", "yellow_ochre", 0.50), 0.55)
def china(v, w): return at_value(p.mix(CH_C, CH_W, max(0., min(1., w))), v)
p["twig1"] = at_value(G, 0.630)
p["twig2"] = at_value(G, 0.685)
p["twig3"] = at_value(G, 0.736)
p["twig4"] = at_value(p.mix(G, Gw, 0.4), 0.772)
def bez3(p0,c0,c1,p1,n=22):
    o=[]
    for i in range(n):
        t=i/(n-1.0); u=1-t
        o.append((u**3*p0[0]+3*u*u*t*c0[0]+3*u*t*t*c1[0]+t**3*p1[0],
                  u**3*p0[1]+3*u*u*t*c0[1]+3*u*t*t*c1[1]+t**3*p1[1]))
    return o
s.dry()
limb = [
 (bez3((1.04,0.045),(0.94,0.088),(0.86,0.152),(0.735,0.196)), "twig1", 0.0092, [1.0,0.8,0.45]),
 (bez3((0.735,0.196),(0.688,0.212),(0.652,0.204),(0.604,0.226)), "twig2", 0.0062, [0.7,0.5,0.15]),
 (bez3((0.902,0.118),(0.888,0.196),(0.876,0.256),(0.858,0.330)), "twig2", 0.0060, [0.9,0.6,0.2]),
 (bez3((0.858,0.330),(0.872,0.372),(0.894,0.392),(0.908,0.428)), "twig3", 0.0042, [0.6,0.3,0.1]),
 (bez3((0.806,0.166),(0.782,0.106),(0.766,0.070),(0.752,0.020)), "twig2", 0.0052, [0.8,0.4,0.1]),
 (bez3((0.876,0.256),(0.828,0.286),(0.800,0.318),(0.766,0.362)), "twig3", 0.0044, [0.7,0.35,0.1]),
 (bez3((0.664,0.208),(0.640,0.164),(0.628,0.140),(0.616,0.108)), "twig3", 0.0038, [0.6,0.3,0.1]),
 (bez3((1.04,0.284),(0.966,0.336),(0.918,0.372),(0.856,0.410)), "twig4", 0.0072, [0.8,0.5,0.2]),
 (bez3((0.940,0.352),(0.930,0.406),(0.926,0.436),(0.920,0.472)), "twig4", 0.0040, [0.6,0.3,0.1]),
 (bez3((0.612,0.176),(0.586,0.148),(0.566,0.140),(0.534,0.120)), "twig4", 0.0034, [0.5,0.25,0.1]),
]
for pts, col, sz, pr in limb:
    s.stroke(pts, "liner", col, size=sz, pressure=pr, load=1.0, load_falloff=0.05)

# the handle, once more, and nothing goes over it after this
p["h_dk"]   = china(0.355, 0.60)
p["h_lit"]  = china(0.620, 0.35)
p["h_join"] = china(0.295, 0.55)
hp = bez3((0.524, 0.652), (0.626, 0.658), (0.646, 0.740), (0.506, 0.766), 26)
s.stroke(hp, "round_hard", "h_dk", size=0.019, pressure="even", load=1.0, load_falloff=0.06)
s.stroke(bez3((0.537, 0.647), (0.624, 0.651), (0.641, 0.716), (0.598, 0.747), 18)[:14],
         "round_hard", "h_lit", size=0.0075, pressure=[0.35, 1.0, 0.5], load=1.0)
s.stroke([(0.522, 0.657), (0.518, 0.679)], "round_hard", "h_join", size=0.010,
         pressure=[0.9, 0.3], load=1.0)
s.stroke([(0.505, 0.752), (0.501, 0.768)], "round_hard", "h_join", size=0.009,
         pressure=[0.85, 0.3], load=1.0)
print("strokes:", s.stroke_count)
print(s.look(sketch=False))
