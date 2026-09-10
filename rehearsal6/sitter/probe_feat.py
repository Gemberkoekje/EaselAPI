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
p["ink"]="#171114"; p["tooth"]=p.desaturate(V(p.mix("yellow_ochre","burnt_sienna",0.2),0.74),0.55)
p["sclera"]=p.desaturate(V(p.mix("ultramarine","burnt_sienna",0.5),0.60),0.40)
p["lip"]=V(p.mix("cadmium_red","burnt_sienna",0.40),0.40)
p["beard"]=p.mix("burnt_umber","ultramarine",0.32)
C = [
 dict(points=[(0.478,0.254),(0.470,0.336),(0.480,0.406)], brush="bristle", color="skin_lit", size=0.032, load=0.9, pressure="swell"),
 dict(points=[(0.462,0.256),(0.532,0.252)], brush="bristle", color="skin_shd", size=0.020, load=0.8, pressure="taper"),
 dict(points=[(0.548,0.276),(0.558,0.352),(0.544,0.402)], brush="bristle", color="skin_shd", size=0.026, load=0.9, pressure="swell"),
 dict(points=[(0.500,0.312),(0.524,0.354)], brush="bristle", color="skin_hi", size=0.016, load=0.8, pressure="swell"),
 dict(points=[(0.510,0.400),(0.542,0.348)], brush="bristle", color="skin_lit", size=0.024, load=0.8, pressure="taper"),
 # features
 dict(points=[(0.434,0.298),(0.476,0.307)], brush="bristle", color="skin_dp", size=0.014, load=0.9, pressure="swell"),
 dict(points=[(0.427,0.285),(0.478,0.297)], brush="liner", color="ink", size=0.009, pressure=[0.4,1.0,0.3]),
 dict(points=[(0.444,0.310),(0.452,0.311)], brush="round_hard", color="sclera", size=0.010, pressure="even"),
 dict(points=[(0.457,0.309),(0.462,0.310)], brush="round_hard", color="ink", size=0.013, pressure="even"),
 dict(points=[(0.418,0.379),(0.427,0.383)], brush="round_hard", color="skin_dp", size=0.014, pressure="even"),
 dict(points=[(0.404,0.358),(0.412,0.364)], brush="round_hard", color="skin_hi", size=0.011, pressure="taper"),
 dict(points=[(0.410,0.418),(0.446,0.426),(0.472,0.417)], brush="bristle", color="beard", size=0.018, load=0.9, pressure="swell"),
 dict(points=[(0.444,0.448),(0.472,0.453)], brush="round_hard", color="ink", size=0.013, pressure="swell"),
 dict(points=[(0.436,0.441),(0.446,0.443)], brush="round_hard", color="tooth", size=0.009, pressure="even"),
 dict(points=[(0.434,0.463),(0.464,0.466)], brush="round_hard", color="lip", size=0.011, pressure="swell"),
]
print(s.rehearse(C, region="D3:E4", reference="ref.jpg"))
