p = s.palette
def at_value(base, target, other="titanium_white"):
    a, b = 0.0, 1.0
    for _ in range(24):
        m=(a+b)/2
        if p.value_of(p.mix(base,other,m))<target: a=m
        else: b=m
    return (a+b)/2
def V(base,v): return p.mix(base,"titanium_white", at_value(base,v))
print("before:", s.stroke_count)
s.undo(3)                                  # signature, the erase, and the mole dab
print("after undo:", s.stroke_count)
s.erase(region=span("E5","H8"))            # free; puts the stray coat line back out
s.erase(region=span("A6","D8"))
p["sig"] = V(p.mix("burnt_umber","ultramarine",0.30), 0.30)
s.stroke([(0.020,0.980),(0.020,0.944),(0.049,0.944)], "liner", "sig", size=0.005,
         pressure=[0.9,0.55,0.25], note="signature")
print("total:", s.stroke_count)
s.export("copy_final.png")
s.timelapse_gif("copy_timelapse.gif")
