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
p["dark"]=p.mix("ultramarine","burnt_umber",0.55)
p["hand_shd"]=V(p.mix("burnt_sienna","burnt_umber",0.45),0.24)
p["hair_lt"]=p.desaturate(V(p.mix("burnt_umber","yellow_ochre",0.45),0.46),0.30)
p["wall_lit"]=p.desaturate(V(warm,0.60),0.35)
s.dry()
s.block_in(polygon([(0.870,0.868),(1.0,0.858),(1.0,1.0),(0.862,1.0)]), "bristle","dark",
           direction=(-8,), density=0.9, size=0.072, load=1.0)
s.stroke([(0.252,0.530),(0.372,0.548)], "bristle","hand_shd", size=0.052, load=0.9, pressure="swell")
s.stroke([(0.582,0.392),(0.616,0.464)], "bristle","hair_lt", size=0.032, load=0.85, pressure="swell")
s.stroke([(0.902,0.340),(0.996,0.396)], "bristle","wall_lit", size=0.066, load=0.9, pressure="swell")
print("strokes:", s.stroke_count)
