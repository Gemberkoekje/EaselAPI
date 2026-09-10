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
def yf(x): return 0.8010 - 0.038 * x
def sx(t): return 0.2800 + 0.1000*t
def wd(t): return 0.0215 + 0.0110*t
def yy(t): return 0.6480 + 0.1530*t

s.dry()
# --- wipe the woven strap out; a bristle that small is a comb, not a brush ---
for t0, t1, v in [(-0.02,0.55,0.705),(0.53,1.03,0.672)]:
    s.block_in(polygon([(sx(t0)-0.016,yy(t0)),(sx(t0)+wd(t0)+0.016,yy(t0)),
                        (sx(t1)+wd(t1)+0.016,yy(t1)),(sx(t1)-0.016,yy(t1))]),
               "flat", SV(v), density=1.0, size=0.018, pressure="even",
               direction="axis", load=1.0)
# --- the shadow again: solid, softer, a little less insistent ---
for t0, t1, v in [(0.00,0.36,0.500),(0.34,0.70,0.458),(0.68,1.00,0.420)]:
    s.block_in(polygon([(sx(t0),yy(t0)),(sx(t0)+wd(t0),yy(t0)),
                        (sx(t1)+wd(t1),yy(t1)),(sx(t1),yy(t1))]),
               "flat", SV(v), density=1.0, size=0.011, pressure="even",
               direction="axis", load=1.0)
for side in (0, 1):
    for t0, t1, v in [(0.00,0.50,0.600),(0.48,1.00,0.565)]:
        o0 = -0.0085 if side == 0 else wd(t0) - 0.0015
        o1 = -0.0085 if side == 0 else wd(t1) - 0.0015
        s.block_in(polygon([(sx(t0)+o0,yy(t0)),(sx(t0)+o0+0.0105,yy(t0)),
                            (sx(t1)+o1+0.0105,yy(t1)),(sx(t1)+o1,yy(t1))]),
                   "round_hard", SV(v), density=0.45, size=0.013,
                   pressure="even", load=0.55)

# --- the lip was a dashed line; a lip is a change of plane ---
for x0, x1, va, vb in [(-0.06,0.180,0.700,0.452),(0.160,0.360,0.672,0.478),
                       (0.340,0.530,0.612,0.442)]:
    s.block_in(polygon([(x0,yf(x0)-0.0140),(x1,yf(x1)-0.0140),(x1,yf(x1)+0.0010),(x0,yf(x0)+0.0010)]),
               "flat", SV(va), density=1.0, size=0.009, pressure="even", direction="axis", load=1.0)
    s.block_in(polygon([(x0,yf(x0)+0.0010),(x1,yf(x1)+0.0010),(x1,yf(x1)+0.0165),(x0,yf(x0)+0.0165)]),
               "flat", SV(vb), density=1.0, size=0.009, pressure="even", direction="axis", load=1.0)
s.stroke([(0.0850,yf(0.085)-0.0030),(0.1980,yf(0.198)-0.0035)], "flat", SV(0.800),
         size=0.0055, pressure="lift_off", load=1.0)
s.stroke([(0.4140,yf(0.414)-0.0025),(0.4720,yf(0.472)-0.0030)], "flat", SV(0.665),
         size=0.0045, pressure="taper", load=1.0)

# --- seat the petals with a touch of dark under each ---
s.stroke([(0.4130,0.7472),(0.4240,0.7462)], "round_hard", SV(0.470), size=0.0055,
         pressure="even", load=0.9)
s.stroke([(0.3618,0.7712),(0.3706,0.7700)], "round_hard", SV(0.430), size=0.0048,
         pressure="even", load=0.9)
print("strokes:", s.stroke_count)
