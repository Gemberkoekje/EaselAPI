import random
p = s.palette; dk = p["dk"]; rnd = random.Random(909)
pale = p.mix("titanium_white", "yellow_ochre", 0.28)
tc   = p.mix("burnt_sienna", "cadmium_red", 0.30)
warmy= p.mix("yellow_ochre", "titanium_white", 0.40)
def T(v):
    lo, hi = 0.0, 1.0
    if v >= p.value_of(tc):
        for _ in range(24):
            m=(lo+hi)/2
            if p.value_of(p.mix(tc, warmy, m)) < v: lo=m
            else: hi=m
        c = p.mix(tc, warmy, (lo+hi)/2)
        return p.mix(c, "titanium_white", 0.18) if v > 0.56 else c
    for _ in range(24):
        m=(lo+hi)/2
        if p.value_of(p.mix(tc, dk, m)) > v: lo=m
        else: hi=m
    return p.mix(tc, dk, (lo+hi)/2)

s.dry()
# --- the dark tongue in the window was a botched repair: put the light back ---
up = polygon([(0.400,0.156),(0.492,0.162),(0.491,0.262),(0.399,0.256)])
lo = polygon([(0.399,0.256),(0.491,0.262),(0.490,0.358),(0.397,0.352)])
s.block_in(up.inset(0.009), "flat", "glow_p", density=1.0, size=0.019, direction=(9,97), load=1.0)
s.block_in(lo.inset(0.009), "flat", "haze",   density=1.0, size=0.019, direction=(-7,85), load=1.0)
for i in range(7):
    x0 = rnd.uniform(0.352, 0.430); y0 = rnd.uniform(0.150, 0.360)
    ln = rnd.uniform(0.06, 0.13)
    s.stroke([(x0,y0),(x0+ln, y0+ln*rnd.uniform(-0.8,-0.2))], "bristle",
             rnd.choice(["glow_p","haze","glow_w"]), size=rnd.uniform(0.030,0.052),
             load=rnd.uniform(0.35,0.55), pressure="taper")

# --- the reveal, clean, from the head of the window down to where the leaves take over ---
rv = polygon([(0.4850,0.106),(0.5090,0.110),(0.5125,0.408),(0.4840,0.404)])
s.block_in(rv.inset(0.007), "flat", "reveal", density=1.0, size=0.014, direction=88, load=1.0)
s.block_in(polygon([(0.4855,0.300),(0.5105,0.304),(0.5125,0.408),(0.4845,0.404)]).inset(0.006),
           "flat", "reveal_d", density=1.0, size=0.012, direction=87, load=1.0)
s.stroke([(0.4880,0.130),(0.4865,0.290)], "flat", p.mix(p["reveal"], "titanium_white", 0.22),
         size=0.005, pressure="lift_off", load=0.9)

# --- break the ladder of ticks on the casement edge ---
for y0, y1 in [(0.1620,0.1880),(0.3320,0.3560),(0.5540,0.5760)]:
    s.stroke([(0.1075,y0),(0.1055,y1)], "flat", "case", size=0.010, pressure="even", load=1.0)

# --- the highlights: four, and no more ---
s.dab(0.5148, 0.5406, "round_hard", T(0.735), size=0.011, press=3)
s.dab(0.6875, 0.3392, "round_hard", p.tint(p.mix("cadmium_red","cadmium_yellow",0.32), 0.44),
      size=0.009, press=3)
s.dab(0.7228, 0.4028, "round_hard", p["lf_hot"], size=0.008, press=3)
s.dab(0.1268, 0.7952, "round_hard", p.mix(pale, "titanium_white", 0.35), size=0.007, press=2)
print("strokes:", s.stroke_count)
