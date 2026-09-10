p = s.palette
def at_value(base, target, other="titanium_white"):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a+b)/2
        if p.value_of(p.mix(base, other, m)) < target: a = m
        else: b = m
    return (a+b)/2
def V(base, v): return p.mix(base,"titanium_white", at_value(base,v))
warm = p.mix("yellow_ochre","burnt_sienna",0.30)
p["dark"]      = p.mix("ultramarine","burnt_umber",0.55)
p["dark_warm"] = p.mix("burnt_umber","ultramarine",0.28)
p["cloth"]     = p.desaturate(p.mix("burnt_umber","viridian",0.35), 0.30)
p["skin_far"]  = p.desaturate(V(p.mix("burnt_sienna","cadmium_red",0.2),0.50), 0.18)
p["skin_hand"] = V(p.mix("burnt_sienna","cadmium_red",0.28), 0.47)
p["hand_shad"] = V(p.mix("burnt_sienna","burnt_umber",0.4), 0.27)
p["red_hair"]  = V(p.mix("burnt_sienna","cadmium_red",0.4), 0.30)
p["teal"]      = p.desaturate(p.mix("viridian","ultramarine",0.45), 0.30)
p["blur_warm"] = p.desaturate(V(warm,0.44), 0.30)
p["carton"]    = V(p.mix("cadmium_red","yellow_ochre",0.45), 0.47)
p["carton_d"]  = V(p.mix("burnt_sienna","cadmium_red",0.35), 0.33)
p["cream"]     = p.desaturate(V(warm,0.72), 0.45)
for n in ("cloth","skin_hand","hand_shad","red_hair","teal","blur_warm","carton","carton_d","cream"):
    print(f"{n:10s} {p.hex(p[n])} {p.value_of(p[n]):.2f}")

# --- far: the dark clothing mass both figures share, behind the hands
s.block_in(polygon([(0.075,0.60),(0.20,0.55),(0.30,0.56),(0.375,0.62),(0.375,0.92),
                    (0.245,0.95),(0.115,0.88),(0.070,0.75)]),
           "bristle", "dark", direction=(-58,), density=0.95, size=0.072, load=1.0)
s.dry()
# left man: flat cap, face, beard
s.block_in(blob((0.146,0.366), 0.052, 0.034, wobble=0.35, seed=3), "flat", "dark_warm",
           direction=(-8,), density=0.95, size=0.030, load=1.0)
s.block_in(ellipse(polygon([(0.118,0.392),(0.182,0.392),(0.182,0.500),(0.118,0.500)])),
           "round_hard", "skin_far", pressure="even", size=0.028, density=0.9)
s.stroke([(0.126,0.502),(0.176,0.520)], "bristle", "dark_warm", size=0.030, load=0.85)
s.stroke([(0.108,0.575),(0.204,0.612)], "bristle", "cloth", size=0.055, load=0.9, pressure="swell")
s.dry()
# beret and the head under it
s.block_in(polygon([(0.176,0.300),(0.245,0.272),(0.318,0.288),(0.332,0.352),(0.286,0.412),
                    (0.208,0.408),(0.174,0.352)]),
           "bristle", "dark_warm", direction="axis", density=0.95, size=0.050, load=1.0)
s.stroke([(0.196,0.286),(0.300,0.276)], "bristle", "cloth", size=0.018, load=0.5, pressure="lift_off")
s.dry()
# red hair
s.block_in(blob((0.293,0.492), 0.048, 0.096, wobble=0.35, seed=11), "bristle", "red_hair",
           direction="axis", density=0.9, size=0.036, load=0.95)
s.stroke([(0.268,0.430),(0.302,0.560)], "bristle", "dark_warm", size=0.022, load=0.6, pressure="taper")
s.dry()
# --- nearer: the two raised hands, lit
h1 = hull([(0.140,0.470),(0.156,0.398),(0.214,0.400),(0.238,0.520),(0.196,0.640),(0.140,0.596)])
h2 = hull([(0.244,0.446),(0.268,0.382),(0.330,0.386),(0.362,0.470),(0.352,0.612),(0.262,0.620)])
s.block_in(h1, "round_hard", "skin_hand", pressure="even", direction="axis", density=0.95, size=0.030)
s.block_in(h2, "round_hard", "skin_hand", pressure="even", direction="axis", density=0.95, size=0.030)
s.dry(0.6)
for a,b_ in [((0.170,0.406),(0.166,0.520)), ((0.199,0.408),(0.205,0.540)),
             ((0.287,0.392),(0.286,0.520)), ((0.317,0.398),(0.323,0.530)), ((0.345,0.470),(0.348,0.560))]:
    s.stroke([a,b_], "liner", "hand_shad", size=0.008, pressure=[0.3,1.0,0.4])
s.stroke([(0.150,0.560),(0.230,0.600)], "bristle", "hand_shad", size=0.030, load=0.7)
s.dry()
# gloves over the wrists
s.block_in(polygon([(0.176,0.612),(0.272,0.588),(0.366,0.628),(0.370,0.836),(0.240,0.868),(0.172,0.760)]),
           "bristle", "dark", direction=(-70,), density=0.95, size=0.058, load=1.0)
s.dry()
# --- left edge: teal chair, warm blur, dark below
s.block_in(polygon([(0.0,0.600),(0.048,0.592),(0.052,0.760),(0.0,0.772)]), "flat", "teal",
           direction=(86,), density=0.9, size=0.036, load=1.0)
s.stroke([(0.020,0.660),(0.098,0.690)], "bristle", "blur_warm", size=0.052, load=0.8, pressure="swell")
s.stroke([(0.008,0.790),(0.090,0.812)], "flat", "dark_warm", size=0.055, pressure="even")
s.dry()
# --- foreground: the juice carton and the glass
cart = polygon([(0.140,0.790),(0.232,0.748),(0.300,0.766),(0.302,1.0),(0.142,1.0)])
s.block_in(cart, "flat", "carton", direction=(84,), density=0.95, size=0.044, load=1.0)
s.block_in(polygon([(0.238,0.762),(0.300,0.772),(0.302,1.0),(0.240,1.0)]), "flat", "carton_d",
           direction=(88,), density=0.9, size=0.034, load=1.0)
s.stroke([(0.186,0.760),(0.196,0.960)], "bristle", "cream", size=0.026, load=0.9, pressure="even")
s.stroke([(0.238,0.752),(0.244,0.800)], "flat", "cream", size=0.020, pressure="even")
s.stroke([(0.062,0.905),(0.130,0.900)], "bristle", "cream", size=0.030, load=0.55, pressure="swell")
print("strokes:", s.stroke_count)
