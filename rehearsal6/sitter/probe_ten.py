p = s.palette
def at_value(base, target, other="titanium_white"):
    a, b = 0.0, 1.0
    for _ in range(24):
        m=(a+b)/2
        if p.value_of(p.mix(base,other,m))<target: a=m
        else: b=m
    return (a+b)/2
def V(base,v): return p.mix(base,"titanium_white", at_value(base,v))
sk=p.mix("burnt_sienna","cadmium_red",0.22); sh=p.mix("burnt_sienna","burnt_umber",0.35)
p["skin_lit"]=V(sk,0.50); p["skin_shd"]=V(sh,0.41); p["dark"]=p.mix("ultramarine","burnt_umber",0.55)
p["hair_dk"]=p.mix("burnt_umber","ultramarine",0.22); p["ink"]="#171114"
p["tooth"]=p.desaturate(V(p.mix("yellow_ochre","burnt_sienna",0.2),0.74),0.55)
TEN=[
 dict(points=[(0.500,0.396),(0.542,0.412),(0.576,0.408)], brush="bristle", color="skin_lit", size=0.040, load=0.9, pressure="swell"),
 dict(points=[(0.504,0.442),(0.546,0.452),(0.574,0.438)], brush="bristle", color="skin_shd", size=0.034, load=0.85, pressure="taper"),
 dict(points=[(0.398,0.266),(0.389,0.320),(0.395,0.368),(0.409,0.400)], brush="bristle", color="dark", size=0.028, load=0.9, pressure="swell"),
 dict(points=[(0.426,0.254),(0.470,0.240),(0.514,0.235)], brush="bristle", color="hair_dk", size=0.008, load=0.55, pressure="taper"),
 dict(points=[(0.560,0.298),(0.568,0.362)], brush="bristle", color="hair_dk", size=0.013, load=0.8, pressure="swell"),
 dict(points=[(0.452,0.444),(0.470,0.452)], brush="round_hard", color="ink", size=0.009, pressure="swell"),
]
print(s.rehearse(TEN, region="D2:F5", reference="ref.jpg"))
