p = s.palette
def at_value(base, target, other="titanium_white"):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a+b)/2
        if p.value_of(p.mix(base, other, m)) < target: a = m
        else: b = m
    return (a+b)/2
def V(base, v): return p.mix(base,"titanium_white", at_value(base,v))
p["coat"]     = "#100d0b"                                   # supplied: ref coat is 0.04-0.06
p["coat_lift"]= p.mix("burnt_umber","ultramarine",0.30)
p["coat_cool"]= p.mix("ultramarine","burnt_umber",0.35)
p["neck"]     = V(p.mix("burnt_sienna","burnt_umber",0.35), 0.26)
p["neck_d"]   = V(p.mix("burnt_sienna","burnt_umber",0.60), 0.16)
p["tee"]      = p.mix("ultramarine","burnt_umber",0.45)
for n in ("coat","coat_lift","coat_cool","neck","neck_d","tee"):
    print(f"{n:10s} {p.hex(p[n])} {p.value_of(p[n]):.2f}")

# --- neck first: it sits behind the collar
nk = polygon([(0.462,0.502),(0.518,0.510),(0.548,0.586),(0.556,0.628),(0.480,0.620),(0.454,0.556)])
s.block_in(nk, "flat", "neck", direction=(72,), density=0.95, size=0.032, load=1.0)
s.stroke([(0.470,0.516),(0.500,0.556)], "bristle", "neck_d", size=0.026, load=0.8, pressure="lift_off")
s.dry()

# --- the coat: core first, inset so the brush does not eat the silhouette
coat = polygon([(0.418,0.548),(0.462,0.522),(0.522,0.550),(0.588,0.514),(0.658,0.484),(0.724,0.474),
                (0.786,0.508),(0.842,0.568),(0.874,0.642),(0.886,0.734),(0.878,0.850),(0.862,1.0),
                (0.378,1.0),(0.370,0.762),(0.392,0.640)])
s.block_in(coat.inset(0.052), "bristle", "coat", direction=(63,), density=0.9, size=0.105, load=1.0)
s.dry(0.5)
# then the true edge, swept along the boundary so the passes follow the back
top = [(0.522,0.550),(0.588,0.514),(0.658,0.484),(0.724,0.474),(0.786,0.508),(0.842,0.568),
       (0.874,0.642),(0.886,0.734),(0.878,0.850)]
s.sweep(top, "bristle", "coat", into=(0.66,0.78), depth=0.085, size=0.052, cross=26, load=1.0)
s.dry(0.5)
left = [(0.418,0.548),(0.398,0.660),(0.376,0.790),(0.380,1.0)]
s.sweep(left, "bristle", "coat", into=(0.55,0.85), depth=0.06, size=0.05, cross=0, load=1.0)
s.dry()
# folds and the light running along the top of the shoulder
s.stroke([(0.560,0.560),(0.700,0.500)], "bristle", "coat_lift", size=0.022, load=0.6, pressure="swell")
s.stroke([(0.772,0.530),(0.848,0.620)], "bristle", "coat_lift", size=0.018, load=0.5, pressure="taper")
s.stroke([(0.600,0.700),(0.660,0.900)], "bristle", "coat_cool", size=0.030, load=0.45, pressure="swell")
s.stroke([(0.455,0.700),(0.470,0.900)], "bristle", "coat_lift", size=0.024, load=0.45, pressure="taper")
s.dry()
# the fleece under the coat, and its zip
s.block_in(polygon([(0.492,0.600),(0.560,0.616),(0.578,0.760),(0.492,0.775),(0.478,0.680)]),
           "flat", "tee", direction=(78,), density=0.9, size=0.034, load=1.0)
s.stroke([(0.498,0.632),(0.556,0.648)], "liner", p.tint("cerulean",0.25), size=0.007, pressure=[0.9,0.3])
s.stroke([(0.516,0.672),(0.524,0.756)], "liner", "coat_lift", size=0.006, pressure=[0.4,1.0,0.3])
print("strokes:", s.stroke_count)
