p = s.palette
pale = p.mix("titanium_white", "yellow_ochre", 0.28)
def SV(t, b="burnt_umber"):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        m=(lo+hi)/2
        if p.value_of(p.mix(pale, b, m)) > t: lo=m
        else: hi=m
    return p.mix(pale, b, (lo+hi)/2)
def sx(t): return 0.2800 + 0.1000*t
def yy(t): return 0.6480 + 0.1530*t

wipe = [{"points": [(sx(-0.05)+d, yy(-0.05)), (sx(1.05)+d, yy(1.05))], "brush": "flat",
         "color": SV(0.700), "size": 0.030, "pressure": "even", "load": 1.0}
        for d in (-0.012, 0.012, 0.034)]
shad = [{"points": [(sx(0.0)+0.010, yy(0.0)), (sx(1.0)+0.014, yy(1.0))], "brush": "flat",
         "color": SV(0.470), "size": 0.024, "pressure": "even", "load": 1.0},
        {"points": [(sx(0.0)+0.010, yy(0.0)), (sx(1.0)+0.014, yy(1.0))], "brush": "round_soft",
         "color": SV(0.545), "size": 0.030, "pressure": "even", "load": 0.45, "opacity": 0.5}]
s.rehearse(wipe + shad, region="B6:D7")
s.rehearse(wipe, region="B6:D7")
