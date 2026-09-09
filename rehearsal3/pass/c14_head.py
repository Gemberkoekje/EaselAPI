# c14 - one self-inflicted error, repaired.
# c12's "shelf band" stroke, meant to soften a light band on the mug's upper
# body, ran (0.345,0.372)->(0.600,0.366) at size 0.040 and therefore straight
# across the crewmate's HEAD. compare D4 went +0.14 -> +0.23 for that reason
# alone. Repaint the head; nothing else.
REF = r"C:\temp\Level1.jpg"
p = s.palette


def at_value(base, target):
    lo, hi = 0.0, 1.0
    if p.value_of(base) > target:
        for _ in range(26):
            mid = (lo + hi) / 2
            if p.value_of(p.shade(base, mid)) > target:
                lo = mid
            else:
                hi = mid
        return p.shade(base, (lo + hi) / 2)
    for _ in range(26):
        mid = (lo + hi) / 2
        if p.value_of(p.tint(base, mid)) < target:
            lo = mid
        else:
            hi = mid
    return p.tint(base, (lo + hi) / 2)


p["crew3"] = at_value(p.desaturate(p.mix("alizarin", "burnt_umber", 0.62), 0.5), 0.222)
s.dry()
n0 = s.stroke_count

head = [(0.388, 0.436), (0.398, 0.412), (0.412, 0.402), (0.430, 0.398),
        (0.448, 0.396), (0.466, 0.398), (0.482, 0.404), (0.496, 0.416),
        (0.506, 0.436)]
for i, (xx, t) in enumerate(head):
    a, z = ((xx, t + 0.006), (xx, 0.474)) if i % 2 else ((xx, 0.474), (xx, t + 0.006))
    s.stroke([a, z], "flat", "crew3", size=0.024, load=1.0, pressure="even",
             load_falloff=0.05)
# the visor goes back on top of it - it is the mark that names the figure
p["visor2"] = at_value(p.desaturate(p.mix("cerulean", "burnt_umber", 0.30), 0.45), 0.560)
p["glint2"] = at_value(p.desaturate("cerulean", 0.25), 0.860)
s.stroke([(0.373, 0.462), (0.400, 0.470), (0.427, 0.474)], "round_hard",
         "visor2", size=0.026, load=1.0, pressure="swell")
s.dab(0.382, 0.460, "round_hard", "glint2", size=0.009)

print("head repaint:", s.stroke_count - n0, "| strokes:", s.stroke_count)
print(s.look(reference=REF))
