p = s.palette
def at_value(base, target, other="titanium_white"):
    a, b = 0.0, 1.0
    for _ in range(24):
        m=(a+b)/2
        if p.value_of(p.mix(base,other,m))<target: a=m
        else: b=m
    return (a+b)/2
def V(base,v): return p.mix(base,"titanium_white", at_value(base,v))
sk=p.mix("burnt_sienna","cadmium_red",0.22); sh=p.mix("burnt_sienna","burnt_umber",0.35)
p["skin_lit"]=V(sk,0.50); p["skin_shd"]=V(sh,0.41); p["skin_ear"]=V(sh,0.38)
p["dark"]=p.mix("ultramarine","burnt_umber",0.55)
p["hair_dk"]=p.mix("burnt_umber","ultramarine",0.22); p["ink"]="#171114"
p["tooth"]=p.desaturate(V(p.mix("yellow_ochre","burnt_sienna",0.2),0.74),0.55)
s.dry()
n0 = s.stroke_count
# 1 the lit plane of the cheek and jaw, which the beard shape had swallowed
s.stroke([(0.500,0.396),(0.542,0.412),(0.576,0.408)], "bristle","skin_lit", size=0.040, load=0.9, pressure="swell", note="cheek plane")
# 2 the stubbled underside of the jaw
s.stroke([(0.504,0.442),(0.546,0.452),(0.574,0.438)], "bristle","skin_shd", size=0.034, load=0.85, pressure="taper", note="jaw stubble")
# 3 the profile: the dark behind it, brought up to where the face stops
s.stroke([(0.398,0.266),(0.389,0.320),(0.395,0.368),(0.409,0.400)], "bristle","dark", size=0.028, load=0.9, pressure="swell", note="profile edge")
# 4 loose hair falling across the forehead
s.stroke([(0.424,0.256),(0.468,0.240),(0.516,0.234)], "liner","hair_dk", size=0.005, pressure=[0.3,1.0,0.25], note="forehead wisp")
# 5 the hair in front of the ear
s.stroke([(0.559,0.296),(0.567,0.362)], "bristle","hair_dk", size=0.013, load=0.8, pressure="swell", note="sideburn")
# 6 the ear
s.dab(0.5775, 0.3495, "round_hard","skin_ear", size=0.019, press=2)
# 7 the dark of the open mouth
s.stroke([(0.452,0.444),(0.470,0.452)], "round_hard","ink", size=0.009, pressure="swell", note="open mouth")
# 8 the tooth catching the light
s.dab(0.4452, 0.4402, "round_hard","tooth", size=0.006, press=3)
# 9 the eye
s.dab(0.4622, 0.3085, "round_hard","ink", size=0.009, press=3)
# 10 the mole on his neck
s.dab(0.5880, 0.4340, "round_hard","ink", size=0.006, press=2)
print("last ten:", s.stroke_count - n0, "total:", s.stroke_count)
