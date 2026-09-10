import random
p = s.palette; dk = p["dk"]; rnd = random.Random(1111)
pale = p.mix("titanium_white", "yellow_ochre", 0.28)
def SV(t, b="burnt_umber"):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        m=(lo+hi)/2
        if p.value_of(p.mix(pale, b, m)) > t: lo=m
        else: hi=m
    return p.mix(pale, b, (lo+hi)/2)

s.dry()
# --- knit the repaired patch back into the window ---
for i in range(11):
    y0 = rnd.uniform(0.150, 0.372)
    x0 = rnd.uniform(0.340, 0.408)
    ln = rnd.uniform(0.075, 0.150)
    s.stroke([(x0,y0),(x0+ln, y0+ln*rnd.uniform(-0.75,-0.15))], "bristle",
             rnd.choice(["glow_p","glow_p","haze","glow_w","glow_g"]),
             size=rnd.uniform(0.032,0.058), load=rnd.uniform(0.35,0.55),
             pressure=rnd.choice(["taper","lift_off"]))
for i in range(5):
    y0 = rnd.uniform(0.165, 0.250)
    s.stroke([(rnd.uniform(0.395,0.425), y0), (rnd.uniform(0.465,0.492), y0-rnd.uniform(0.01,0.04))],
             "bristle", "glow_p", size=rnd.uniform(0.030,0.048),
             load=rnd.uniform(0.35,0.50), pressure="taper")
s.stroke([(0.384,0.318),(0.474,0.300)], "round_soft", "haze", size=0.030,
         load=0.45, opacity=0.40, pressure="even")

# --- the shadowed sill on the right is a slab: give it a plane and a little wear ---
for a, b, v, w, ld in [((0.700,0.6820),(0.905,0.6900),0.325,0.014,0.40),
                       ((0.760,0.7220),(0.985,0.7300),0.265,0.012,0.35),
                       ((0.820,0.6620),(0.990,0.6680),0.230,0.013,0.35),
                       ((0.690,0.8460),(0.900,0.8380),0.215,0.012,0.35),
                       ((0.560,0.8180),(0.720,0.8140),0.300,0.011,0.30)]:
    s.stroke([a,b], "bristle", SV(v, dk), size=w, load=ld, pressure="lift_off")
s.stroke([(0.9420,0.6560),(0.9160,0.7480)], "bristle", SV(0.245, dk), size=0.010, load=0.35)
s.stroke([(0.6300,0.6980),(0.6560,0.7620)], "bristle", SV(0.275, dk), size=0.009, load=0.30)
# the room deepens toward the right edge
s.block_in(blob((1.020,0.760), 0.16, 0.20, wobble=0.5, seed=71), "bristle",
           p.mix(dk, "ultramarine", 0.15), density=0.30, size=0.050,
           direction=(58,142), load=0.35)
print("strokes:", s.stroke_count)
