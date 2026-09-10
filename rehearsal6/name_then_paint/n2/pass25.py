p = s.palette; dk = p["dk"]
pale = p.mix("titanium_white", "yellow_ochre", 0.28)
tc   = p.mix("burnt_sienna", "cadmium_red", 0.30)
warmy= p.mix("yellow_ochre", "titanium_white", 0.40)
def SV(t, b="burnt_umber"):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        m=(lo+hi)/2
        if p.value_of(p.mix(pale, b, m)) > t: lo=m
        else: hi=m
    return p.mix(pale, b, (lo+hi)/2)
def T(v):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        m=(lo+hi)/2
        if p.value_of(p.mix(tc, warmy, m)) < v: lo=m
        else: hi=m
    c = p.mix(tc, warmy, (lo+hi)/2)
    return p.mix(c, "titanium_white", 0.18) if v > 0.56 else c

s.dry()
# the rim highlight had landed on a leaf; bury it and put it on the lip
s.stroke([(0.5090,0.5352),(0.5168,0.5424)], "round_hard", p["lf_dk"],
         size=0.019, pressure="even", load=1.0)
s.dab(*cell("E5").point(0.14, 0.49), "round_hard", T(0.760), size=0.0085, press=3)
print("strokes:", s.stroke_count)
