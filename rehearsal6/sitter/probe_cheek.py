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
p["skin_lit"] = V(sk, 0.52); p["skin_hi"] = V(sk, 0.62); p["skin_mid"] = V(sk, 0.45)

# A: bristle passes running down the form, cheek carried right to the ear
A = [dict(points=[(0.478,0.256),(0.470,0.330),(0.478,0.404)], brush="bristle", color="skin_lit", size=0.030, load=0.95, pressure="swell"),
     dict(points=[(0.512,0.252),(0.506,0.336),(0.516,0.410)], brush="bristle", color="skin_lit", size=0.030, load=0.95, pressure="swell"),
     dict(points=[(0.546,0.268),(0.544,0.344),(0.552,0.404)], brush="bristle", color="skin_mid", size=0.030, load=0.9, pressure="swell"),
     dict(points=[(0.498,0.296),(0.522,0.356)], brush="bristle", color="skin_hi", size=0.019, load=0.8, pressure="swell")]
# B: round_hard, no axis at all
B = [dict(points=[(0.474,0.258),(0.470,0.336),(0.480,0.406)], brush="round_hard", color="skin_lit", size=0.032, pressure="even"),
     dict(points=[(0.514,0.254),(0.508,0.340),(0.518,0.408)], brush="round_hard", color="skin_lit", size=0.032, pressure="even"),
     dict(points=[(0.548,0.270),(0.546,0.348),(0.554,0.404)], brush="round_hard", color="skin_mid", size=0.030, pressure="even"),
     dict(points=[(0.500,0.298),(0.524,0.358)], brush="round_hard", color="skin_hi", size=0.020, pressure="taper")]
print(s.rehearse(A, region="D2:F5"))
print(s.rehearse(B, region="D2:F5"))
