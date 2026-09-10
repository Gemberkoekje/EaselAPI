p = s.palette
def at_value(base, target, other="titanium_white"):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a+b)/2
        if p.value_of(p.mix(base, other, m)) < target: a = m
        else: b = m
    return (a+b)/2
def V(base, v): return p.mix(base,"titanium_white", at_value(base,v))
p["dark"]=p.mix("ultramarine","burnt_umber",0.55)
p["hair_lt"]=p.desaturate(V(p.mix("burnt_umber","yellow_ochre",0.45),0.47),0.30)
A=[dict(points=[(0.398,0.266),(0.389,0.320),(0.395,0.368),(0.409,0.400)], brush="bristle",
        color="dark", size=0.030, load=0.9, pressure="swell"),
   dict(points=[(0.552,0.382),(0.586,0.436),(0.610,0.494)], brush="bristle",
        color="hair_lt", size=0.050, load=0.9, pressure="swell")]
B=[dict(points=[(0.393,0.262),(0.384,0.322),(0.390,0.370),(0.404,0.402)], brush="flat",
        color="dark", size=0.024, pressure="even"),
   dict(points=[(0.552,0.382),(0.586,0.436),(0.610,0.494)], brush="bristle",
        color="hair_lt", size=0.050, load=0.9, pressure="swell")]
print(s.rehearse(A, region="D2:F5", reference="ref.jpg"))
print(s.rehearse(B, region="D2:F5"))
