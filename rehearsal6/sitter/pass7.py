p = s.palette
def at_value(base, target, other="titanium_white"):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a+b)/2
        if p.value_of(p.mix(base, other, m)) < target: a = m
        else: b = m
    return (a+b)/2
def V(base, v): return p.mix(base,"titanium_white", at_value(base,v))
sk = p.mix("burnt_sienna","cadmium_red",0.22)
sh = p.mix("burnt_sienna","burnt_umber",0.35)
p["skin_lit"] = V(sk, 0.52)
p["skin_hi"]  = V(sk, 0.62)
p["skin_shd"] = V(sh, 0.33)
p["skin_dp"]  = V(sh, 0.20)
p["beard"]    = p.mix("burnt_umber","ultramarine",0.32)
p["beard_lt"] = V(p.mix("burnt_umber","yellow_ochre",0.30), 0.24)
for n in ("skin_lit","skin_hi","skin_shd","skin_dp","beard","beard_lt"):
    print(f"{n:9s} {p.hex(p[n])} {p.value_of(p[n]):.2f}")
s.dry()

face = polygon([(0.418,0.262),(0.406,0.294),(0.412,0.316),(0.400,0.357),(0.420,0.382),(0.432,0.412),
                (0.480,0.430),(0.540,0.418),(0.568,0.372),(0.570,0.316),(0.548,0.268),(0.498,0.242),
                (0.452,0.246)])
s.block_in(face.inset(0.022), "flat", "skin_lit", direction=(74,), density=0.95, size=0.045, load=1.0)
s.dry(0.5)
# the plane of the cheek, which is the lightest thing on him
s.stroke([(0.500,0.300),(0.534,0.366)], "round_hard", "skin_hi", size=0.036, pressure="even")
s.stroke([(0.528,0.288),(0.556,0.348)], "round_hard", "skin_hi", size=0.028, pressure="swell")
s.stroke([(0.470,0.262),(0.508,0.256)], "flat", "skin_hi", size=0.024, pressure="even")
# brow ridge and the socket under it; the shadow down the side of the nose
s.stroke([(0.424,0.282),(0.478,0.292)], "bristle", "skin_shd", size=0.020, load=0.8, pressure="swell")
s.stroke([(0.438,0.318),(0.472,0.328)], "bristle", "skin_shd", size=0.016, load=0.7, pressure="taper")
s.stroke([(0.414,0.330),(0.424,0.372)], "bristle", "skin_shd", size=0.017, load=0.8, pressure="press_in")
s.dab(0.424, 0.384, "round_hard", "skin_dp", size=0.020, press=2)
s.dry()

beard = polygon([(0.410,0.412),(0.436,0.400),(0.472,0.404),(0.526,0.412),(0.570,0.398),(0.578,0.440),
                 (0.556,0.494),(0.498,0.528),(0.450,0.518),(0.422,0.484),(0.410,0.446)])
s.block_in(beard.inset(0.018), "bristle", "beard", direction=(-16,), density=0.95, size=0.038, load=1.0)
s.dry(0.6)
s.stroke([(0.470,0.510),(0.532,0.492)], "bristle", "beard_lt", size=0.014, load=0.6, pressure="swell")
s.stroke([(0.552,0.412),(0.566,0.462)], "bristle", "beard_lt", size=0.012, load=0.5, pressure="taper")
print("strokes:", s.stroke_count)
