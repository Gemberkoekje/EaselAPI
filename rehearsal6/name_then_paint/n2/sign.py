p = s.palette
pale = p.mix("titanium_white", "yellow_ochre", 0.28)
def SV(t, b="burnt_umber"):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        m=(lo+hi)/2
        if p.value_of(p.mix(pale, b, m)) > t: lo=m
        else: hi=m
    return p.mix(pale, b, (lo+hi)/2)
ink = SV(0.295)
s.stroke([(0.0470,0.8330),(0.0545,0.8560),(0.0505,0.8620)], "liner", ink,
         size=0.0040, pressure=[1.0,0.8,0.35], note="signature")
s.stroke([(0.0390,0.8480),(0.0640,0.8430)], "liner", ink,
         size=0.0032, pressure=[0.5,1.0,0.4], note="signature")
print("strokes:", s.stroke_count)
