p = s.palette
def at_value(base, target, other="titanium_white"):
    a, b = 0.0, 1.0
    for _ in range(24):
        m=(a+b)/2
        if p.value_of(p.mix(base,other,m))<target: a=m
        else: b=m
    return (a+b)/2
def V(base,v): return p.mix(base,"titanium_white", at_value(base,v))
# the pencil left a stray line across the coat where no paint buried it
s.erase(region=span("E5","H8"))
s.erase(region=span("A6","D8"))
p["sig"] = V(p.mix("burnt_umber","ultramarine",0.30), 0.30)
n0 = s.stroke_count
s.stroke([(0.022,0.982),(0.022,0.944)], "liner", "sig", size=0.005, pressure=[0.9,0.4], note="signature")
s.stroke([(0.022,0.982),(0.052,0.982)], "liner", "sig", size=0.005, pressure=[0.9,0.4], note="signature")
print("signature cost:", s.stroke_count - n0, " total:", s.stroke_count)
s.export("copy_final.png")
s.timelapse_gif("copy_timelapse.gif")
