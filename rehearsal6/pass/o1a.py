p = s.palette
def at(base, target):
    a,b = 0.0,1.0
    for _ in range(24):
        m=(a+b)/2
        a,b=(m,b) if p.value_of(p.mix(base,"titanium_white",m))<target else (a,m)
    return (a+b)/2
storm = p.mix("ultramarine","burnt_umber",0.46)
warm  = p.mix("yellow_ochre","cadmium_red",0.22)
sea   = p.mix("viridian","ultramarine",0.35)
for n,base,v in (("squall",storm,0.175),("squall2",storm,0.245),("sky",storm,0.40),
                 ("glow",warm,0.72),("glow2",warm,0.86),("blaze",warm,0.93),
                 ("water_d",sea,0.255),("water_m",sea,0.40),("water_l",sea,0.56)):
    p[n]=p.mix(base,"titanium_white",at(base,v))
    print(f"{n:8s} {p.hex(p[n])} v={p.value_of(p[n]):.3f}")
p["ink"]=p.mix("ultramarine","burnt_umber",0.55)
print("ink", p.hex(p["ink"]), round(p.value_of(p["ink"]),3))
print(s.look(grid=True))
