import math
p = s.palette; dk = p["dk"]
pale = p.mix("titanium_white", "yellow_ochre", 0.28)
def SV(t, b="burnt_umber"):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        m=(lo+hi)/2
        if p.value_of(p.mix(pale, b, m)) > t: lo=m
        else: hi=m
    return p.mix(pale, b, (lo+hi)/2)
def leaf(x, y, w, col, tilt, ln=0.55):
    dx = math.cos(math.radians(tilt))*w*ln/2; dy = math.sin(math.radians(tilt))*w*ln/2
    s.stroke([(x-dx,y-dy),(x+dx,y+dy)], "round_hard", col, size=w, pressure="even", load=1.0)

s.dry()
# --- wipe the corridor back to plain sill ---
s.block_in(polygon([(0.2500,0.6440),(0.3300,0.6460),(0.4180,0.7500),(0.3300,0.7480)]),
           "flat", SV(0.712), density=1.0, size=0.020, direction=(-52,38), load=1.0)
s.block_in(polygon([(0.3300,0.7480),(0.4180,0.7500),(0.4660,0.8060),(0.3760,0.8050)]),
           "flat", SV(0.668), density=1.0, size=0.018, direction=(-50,40), load=1.0)
# --- one shadow, clearly darker, widening and fading as it goes ---
def sx(t): return 0.2800 + 0.1000*t
def wd(t): return 0.0215 + 0.0110*t
for t0, t1, v in [(0.00,0.34,0.472),(0.32,0.68,0.428),(0.66,1.00,0.392)]:
    y0 = 0.6480 + 0.1530*t0; y1 = 0.6480 + 0.1530*t1
    s.block_in(polygon([(sx(t0),y0),(sx(t0)+wd(t0),y0),(sx(t1)+wd(t1),y1),(sx(t1),y1)]),
               "flat", SV(v), density=1.0, size=0.010, direction="axis", load=1.0)
# transition strips instead of smudging: the join is lost by paint, not by dragging
for side in (0, 1):
    for t0, t1, v in [(0.02,0.40,0.585),(0.38,0.74,0.545),(0.72,1.00,0.520)]:
        y0 = 0.6480 + 0.1530*t0; y1 = 0.6480 + 0.1530*t1
        o0 = -0.0075 if side == 0 else wd(t0)
        o1 = -0.0075 if side == 0 else wd(t1)
        s.block_in(polygon([(sx(t0)+o0,y0),(sx(t0)+o0+0.0080,y0),
                            (sx(t1)+o1+0.0080,y1),(sx(t1)+o1,y1)]),
                   "bristle", SV(v), density=0.55, size=0.008, direction="axis", load=0.6)

# --- the petals lie inside that shadow, so they cannot be bright ---
leaf(0.4180,0.7420,0.0140, p.mix(p.mix("cadmium_red","burnt_sienna",0.45), dk, 0.32), 28, ln=0.9)
leaf(0.3660,0.7660,0.0118, p.mix(p.mix("cadmium_red",dk,0.30), "burnt_umber", 0.25), -52, ln=0.9)
leaf(0.3648,0.7628,0.0060, p.mix("cadmium_red","burnt_sienna",0.35), -46, ln=0.8)

# --- the plant's backlit edge: leaves, not stubs ---
for x, y, w, c, t in [(0.4320,0.4300,0.030,"lf_dk2",-34),(0.4180,0.4680,0.026,"lf_dk2",42),
                      (0.4460,0.4060,0.024,"lf_dk", 18),(0.4080,0.5060,0.022,"lf_dk2",-56),
                      (0.4680,0.3860,0.026,"lf_dk", 64)]:
    leaf(x, y, w, c, t, ln=0.75)
for a, b, w, col, ld in [((0.4020,0.4180),(0.4480,0.4020),0.014,"glow_b",0.5),
                         ((0.3980,0.4880),(0.4380,0.4760),0.013,"glow_c",0.45),
                         ((0.4140,0.5260),(0.4560,0.5180),0.012,"glow_c",0.45),
                         ((0.4420,0.3760),(0.4820,0.3660),0.013,"glow_b",0.45)]:
    s.stroke([a,b], "bristle", col, size=w, load=ld, pressure="taper")
print("strokes:", s.stroke_count)
