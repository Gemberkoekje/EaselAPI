p = s.palette
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
def yy(t): return 0.6480 + 0.1530*t

s.dry()
# --- wipe the corridor with long strokes; block_in kept combing it ---
for d, v in [(-0.014, 0.706), (0.012, 0.698), (0.036, 0.686)]:
    s.stroke([(sx(-0.07)+d, yy(-0.07)), (sx(1.07)+d, yy(1.07))], "flat", SV(v),
             size=0.030, pressure="even", load=1.0)

# --- the sill lip, as two planes meeting, laid the same way ---
for x0, x1, v, sz, dy in [(-0.06,0.205,0.702,0.016,-0.0070),(0.185,0.385,0.672,0.015,-0.0070),
                          (0.365,0.560,0.616,0.015,-0.0068)]:
    s.stroke([(x0, yf(x0)+dy), (x1, yf(x1)+dy)], "flat", SV(v), size=sz,
             pressure="even", load=1.0)
for x0, x1, v, sz in [(-0.06,0.205,0.452,0.018),(0.185,0.405,0.478,0.017),
                      (0.385,0.560,0.440,0.017)]:
    s.stroke([(x0, yf(x0)+0.0100), (x1, yf(x1)+0.0100)], "flat", SV(v), size=sz,
             pressure="even", load=1.0)
s.stroke([(0.0850,yf(0.085)-0.0032),(0.1980,yf(0.198)-0.0038)], "flat", SV(0.805),
         size=0.0050, pressure="lift_off", load=1.0)
s.stroke([(0.4180,yf(0.418)-0.0028),(0.4760,yf(0.476)-0.0032)], "flat", SV(0.660),
         size=0.0042, pressure="taper", load=1.0)

# --- and now one shadow, solid, soft-edged, sharper where it leaves the bar ---
s.stroke([(sx(0.00)+0.011, yy(0.00)), (sx(0.96)+0.015, yy(0.96))], "flat", SV(0.472),
         size=0.023, pressure="even", load=1.0)
s.stroke([(sx(0.00)+0.010, yy(0.00)), (sx(0.46)+0.012, yy(0.46))], "flat", SV(0.432),
         size=0.015, pressure="even", load=1.0)
s.stroke([(sx(0.02)+0.011, yy(0.02)), (sx(0.98)+0.015, yy(0.98))], "round_soft", SV(0.552),
         size=0.030, pressure="even", load=0.45, opacity=0.5)
print("strokes:", s.stroke_count)
