p = s.palette
def at(base, target):
    a,b=0.0,1.0
    for _ in range(24):
        m=(a+b)/2
        a,b=(m,b) if p.value_of(p.mix(base,"titanium_white",m))<target else (a,m)
    return (a+b)/2
cold = p.mix("ultramarine","burnt_umber",0.42)
warm = p.mix("yellow_ochre","cadmium_red",0.16)
for n,base,v in (("wall_d",cold,0.150),("wall",cold,0.225),("wall_l",cold,0.310),
                 ("floor",cold,0.190),("spill",warm,0.520),("spill2",warm,0.680),
                 ("lit",warm,0.820),("blaze",warm,0.930)):
    p[n]=p.mix(base,"titanium_white",at(base,v))
    print(f"{n:7s} {p.hex(p[n])} v={p.value_of(p[n]):.3f}")
p["glare"] = p.tint(p.mix("yellow_ochre","titanium_white",0.80), 0.55)
print("glare", p.hex(p["glare"]), round(p.value_of(p["glare"]),3))
print(s.look(grid=True))
