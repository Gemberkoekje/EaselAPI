R = "/home/user/refs/Level1.jpg"
p = s.palette
def at(base, target):
    a,b = 0.0,1.0
    for _ in range(24):
        m=(a+b)/2
        a,b = (m,b) if p.value_of(p.mix(base,"titanium_white",m)) < target else (a,m)
    return (a+b)/2
cool = p.mix("ultramarine","burnt_umber",0.28)
for n,v in (("mug_dk",0.30),("mug_shd",0.44),("mug_mid",0.525),("mug_lit",0.62),
            ("mug_hi",0.72),("mug_wt",0.86)):
    p[n] = p.mix(cool, "titanium_white", at(cool, v))
    print(f"{n:8s} {p.hex(p[n])} v={p.value_of(p[n]):.3f}")
p["tea"]  = p.mix("burnt_umber","ultramarine",0.42)
p["tea2"] = p.mix(p["tea"], p["wood_lo"], 0.16)
print("tea", p.hex(p["tea"]), round(p.value_of(p["tea"]),3),
      "tea2", p.hex(p["tea2"]), round(p.value_of(p["tea2"]),3))

mug = polygon([(0.288,0.250),(0.303,0.198),(0.352,0.152),(0.418,0.120),(0.485,0.111),
               (0.556,0.122),(0.607,0.156),(0.632,0.215),(0.625,0.320),(0.613,0.437),
               (0.598,0.520),(0.578,0.598),(0.550,0.650),(0.505,0.670),(0.450,0.676),
               (0.400,0.674),(0.366,0.662),(0.340,0.570),(0.318,0.455),(0.300,0.350)])
s.preview(mug, reference=R, region=span("C1","G7"))
# a) the whole vessel, one mass, along its own axis
s.block_in(mug.inset(0.033), "flat", "mug_mid", direction=87, density=0.9,
           size=0.065, load=1.0, pressure="even")
print("body", s.stroke_count)
# b) the far edge of the rim - what stands behind the inside
back = ribbon([(0.300,0.225),(0.345,0.160),(0.430,0.125),(0.520,0.118),(0.592,0.152),
               (0.628,0.208)], 0.052)
s.block_in(back, "flat", "mug_lit", direction="axis", density=0.95, size=0.026,
           load=1.0, pressure="even")
print("back rim", s.stroke_count)
# c) the inside
tea = polygon([(0.318,0.240),(0.372,0.185),(0.452,0.157),(0.535,0.160),(0.594,0.196),
               (0.575,0.258),(0.492,0.296),(0.400,0.288),(0.340,0.262)])
s.block_in(tea.inset(0.020), "flat", "tea", direction=-6, density=1.0, size=0.040,
           load=1.0, pressure="even")
s.block_in(tea, "round_hard", "tea", direction=-6, density=1.0, size=0.026,
           load=1.0, pressure="even")
print("tea", s.stroke_count)
print(s.look(reference=R, region=span("C1","G7")))
