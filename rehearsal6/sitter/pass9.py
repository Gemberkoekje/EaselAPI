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
p["coat"]="#100d0b"
p["phone_lt"]=p.desaturate(V(p.mix("yellow_ochre","ultramarine",0.30),0.44),0.55)
p["phone_dk"]=p.desaturate(V(p.mix("burnt_umber","yellow_ochre",0.35),0.24),0.40)
p["wall_lit"]=p.desaturate(V(warm,0.60),0.35)
p["wall_mid"]=p.desaturate(V(warm,0.48),0.35)
p["hand_dk"] =V(p.mix("burnt_sienna","burnt_umber",0.55),0.20)
p["hand_shd"]=V(p.mix("burnt_sienna","burnt_umber",0.35),0.28)
p["carton_d"]=V(p.mix("burnt_sienna","cadmium_red",0.35),0.31)
p["hair_md"] =p.desaturate(V(p.mix("burnt_umber","yellow_ochre",0.45),0.30),0.25)
p["beard_lt"]=V(p.mix("burnt_umber","yellow_ochre",0.30),0.26)
s.dry()
# the bottom of the coat never got covered
s.block_in(polygon([(0.556,0.878),(0.700,0.856),(0.848,0.866),(0.872,0.94),(0.862,1.0),(0.552,1.0)]),
           "bristle","coat", direction=(-6,), density=0.9, size=0.075, load=1.0)
s.dry()
# the tablet lying on the table in front of him
s.stroke([(0.628,0.902),(0.788,0.884)], "flat","phone_lt", size=0.044, pressure="even")
s.stroke([(0.638,0.954),(0.792,0.938)], "flat","phone_dk", size=0.048, pressure="even")
s.dry()
# the lit wall behind, on the right
s.stroke([(0.898,0.298),(0.996,0.322)], "bristle","wall_lit", size=0.058, load=0.9, pressure="swell")
s.stroke([(0.916,0.398),(0.996,0.424)], "bristle","wall_mid", size=0.048, load=0.85, pressure="taper")
# the hands are far too light against the dark behind them
s.stroke([(0.252,0.398),(0.372,0.418)], "bristle","hand_dk", size=0.044, load=0.9, pressure="swell")
s.stroke([(0.258,0.456),(0.370,0.470)], "bristle","hand_shd", size=0.038, load=0.85, pressure="taper")
s.stroke([(0.148,0.930),(0.232,0.924)], "bristle","carton_d", size=0.052, load=0.9, pressure="swell")
# the jaw and the hair falling behind it
s.stroke([(0.572,0.386),(0.614,0.472)], "bristle","hair_md", size=0.038, load=0.9, pressure="swell")
s.stroke([(0.516,0.400),(0.556,0.428)], "bristle","beard_lt", size=0.022, load=0.8, pressure="taper")
print("strokes:", s.stroke_count)
