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
hb = p.mix("burnt_umber","yellow_ochre",0.45)
p["hair_dk"]  = p.mix("burnt_umber","ultramarine",0.22)
p["hair_md"]  = p.desaturate(V(hb, 0.27), 0.25)
p["hair_lt"]  = p.desaturate(V(hb, 0.44), 0.30)
p["hair_hi"]  = p.desaturate(V(hb, 0.58), 0.35)
for n in ("hair_dk","hair_md","hair_lt","hair_hi"):
    print(f"{n:8s} {p.hex(p[n])} {p.value_of(p[n]):.2f}")

# --- the arm and the near side of the coat, which the first pass left bare
s.block_in(polygon([(0.398,0.556),(0.500,0.552),(0.566,0.646),(0.572,1.0),(0.368,1.0),(0.362,0.706)]),
           "bristle", "coat", direction=(76,), density=0.85, size=0.115, load=1.0)
s.stroke([(0.430,0.640),(0.452,0.860)], "bristle", "coat_lift", size=0.020, load=0.45, pressure="swell")
s.dry()

# --- the whole head, laid as hair; the face will be cut into it next
head = polygon([(0.416,0.268),(0.430,0.220),(0.452,0.176),(0.482,0.138),(0.514,0.112),(0.546,0.103),
                (0.583,0.112),(0.617,0.141),(0.653,0.185),(0.683,0.242),(0.701,0.303),(0.701,0.377),
                (0.687,0.434),(0.656,0.482),(0.618,0.506),(0.578,0.470),(0.548,0.400),(0.516,0.328),
                (0.468,0.288)])
s.block_in(head, "bristle", "hair_dk", direction=(-26,), density=0.9, size=0.086, load=1.0)
s.dry(0.55)
# the light coming over the top and the back of the hair, following its sweep
s.stroke([(0.470,0.200),(0.520,0.136),(0.580,0.122)], "bristle", "hair_lt", size=0.038, load=0.85, pressure="swell")
s.stroke([(0.578,0.124),(0.640,0.176),(0.678,0.256)], "bristle", "hair_lt", size=0.042, load=0.8, pressure="taper")
s.stroke([(0.668,0.248),(0.692,0.330),(0.684,0.412)], "bristle", "hair_md", size=0.046, load=0.9, pressure="swell")
s.stroke([(0.612,0.310),(0.648,0.400),(0.638,0.470)], "bristle", "hair_md", size=0.040, load=0.7, pressure="taper")
s.stroke([(0.440,0.238),(0.492,0.180),(0.548,0.152)], "bristle", "hair_hi", size=0.016, load=0.6, pressure="taper")
s.stroke([(0.600,0.148),(0.652,0.212)], "bristle", "hair_hi", size=0.013, load=0.5, pressure="lift_off")
s.stroke([(0.560,0.430),(0.610,0.486)], "bristle", "hair_dk", size=0.034, load=0.8, pressure="press_in")
print("strokes:", s.stroke_count)
