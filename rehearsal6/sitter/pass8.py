p = s.palette
def at_value(base, target, other="titanium_white"):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a+b)/2
        if p.value_of(p.mix(base, other, m)) < target: a = m
        else: b = m
    return (a+b)/2
def V(base, v): return p.mix(base,"titanium_white", at_value(base,v))
sk = p.mix("burnt_sienna","cadmium_red",0.22); sh = p.mix("burnt_sienna","burnt_umber",0.35)
p["skin_lit"]=V(sk,0.52); p["skin_hi"]=V(sk,0.63); p["skin_shd"]=V(sh,0.34); p["skin_dp"]=V(sh,0.20)
p["ink"]="#171114"
p["tooth"]=p.desaturate(V(p.mix("yellow_ochre","burnt_sienna",0.2),0.74),0.55)
p["sclera"]=p.desaturate(V(p.mix("ultramarine","burnt_sienna",0.5),0.58),0.40)
p["lip"]=p.desaturate(V(p.mix("cadmium_red","burnt_sienna",0.40),0.40),0.25)
p["beard"]=p.mix("burnt_umber","ultramarine",0.32)
p["hair_md"]=p.desaturate(V(p.mix("burnt_umber","yellow_ochre",0.45),0.27),0.25)
s.dry()
# --- the plane of the face, broken across the slab and turned at the far cheek
s.stroke([(0.478,0.254),(0.470,0.336),(0.480,0.406)], "bristle","skin_lit", size=0.030, load=0.9, pressure="swell")
s.stroke([(0.462,0.256),(0.532,0.252)], "bristle","skin_shd", size=0.018, load=0.8, pressure="taper")
s.stroke([(0.548,0.276),(0.558,0.352),(0.544,0.402)], "bristle","skin_shd", size=0.026, load=0.9, pressure="swell")
s.stroke([(0.500,0.312),(0.524,0.354)], "bristle","skin_hi", size=0.016, load=0.8, pressure="swell")
s.stroke([(0.424,0.398),(0.468,0.404)], "bristle","skin_lit", size=0.014, load=0.85, pressure="swell")
s.smudge([(0.470,0.248),(0.524,0.244)], size=0.030)      # lose the hairline into the hair
s.dry()
# --- eye
s.stroke([(0.436,0.298),(0.474,0.306)], "bristle","skin_dp", size=0.012, load=0.9, pressure="swell")
s.stroke([(0.419,0.277),(0.458,0.292)], "liner","ink", size=0.005, pressure=[0.4,1.0,0.3])
s.stroke([(0.449,0.309),(0.457,0.310)], "round_hard","sclera", size=0.007, pressure="even")
s.dab(0.4625,0.309, "round_hard","ink", size=0.010, press=2)
s.dab(0.4645,0.3062,"round_hard","titanium_white", size=0.0035, press=3)
# --- nose and mouth
s.stroke([(0.430,0.390),(0.441,0.394)], "round_hard","ink", size=0.009, pressure="swell")
s.stroke([(0.409,0.412),(0.440,0.424),(0.462,0.419)], "bristle","beard", size=0.014, load=0.9, pressure="swell")
s.stroke([(0.455,0.444),(0.470,0.452)], "round_hard","ink", size=0.010, pressure="swell")
s.dab(0.4455,0.4405,"round_hard","tooth", size=0.007, press=2)
s.stroke([(0.442,0.464),(0.466,0.467)], "round_hard","lip", size=0.009, pressure="swell")
s.dry()
# --- take the sprinkle out of the hair at the back
s.stroke([(0.640,0.196),(0.686,0.286)], "bristle","hair_md", size=0.030, load=0.85, pressure="swell")
s.stroke([(0.596,0.140),(0.646,0.190)], "bristle","hair_md", size=0.024, load=0.8, pressure="taper")
s.smudge([(0.556,0.470),(0.598,0.498)], size=0.036)      # lose the hair into the coat
print("strokes:", s.stroke_count)
