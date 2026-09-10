p = s.palette
def at_value(base, target, other="titanium_white"):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a+b)/2
        if p.value_of(p.mix(base, other, m)) < target: a = m
        else: b = m
    return (a+b)/2
def V(base, v): return p.mix(base,"titanium_white", at_value(base,v))
p["coat"]     = "#100d0b"
p["coat_lift"]= p.mix("burnt_umber","ultramarine",0.30)
p["coat_cool"]= p.mix("ultramarine","burnt_umber",0.35)
p["tee"]      = p.mix("ultramarine","burnt_umber",0.45)
# folds; the light running along the top of the back
s.stroke([(0.560,0.560),(0.706,0.498)], "bristle", "coat_lift", size=0.022, load=0.6, pressure="swell")
s.stroke([(0.776,0.532),(0.850,0.624)], "bristle", "coat_lift", size=0.016, load=0.5, pressure="taper")
s.stroke([(0.596,0.700),(0.658,0.905)], "bristle", "coat_cool", size=0.028, load=0.45, pressure="swell")
s.dry()
s.block_in(polygon([(0.492,0.600),(0.560,0.616),(0.578,0.760),(0.492,0.775),(0.478,0.680)]),
           "flat", "tee", direction=(78,), density=0.85, size=0.040, load=1.0)
s.stroke([(0.498,0.632),(0.556,0.648)], "liner", p.tint("cerulean",0.25), size=0.007, pressure=[0.9,0.3])
print("strokes:", s.stroke_count)
