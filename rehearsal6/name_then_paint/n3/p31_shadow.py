p = s.palette
def at_value(base, target):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        m=(lo+hi)/2
        if p.value_of(p.tint(base, m)) < target: lo=m
        else: hi=m
    return p.tint(base, (lo+hi)/2)
E = p.desaturate(p.mix("burnt_umber", "ultramarine", 0.42), 0.45)
p["umb2"] = at_value(E, 0.300)
p["umb3"] = at_value(p.desaturate(E, 0.2), 0.372)
s.dry()
s.block_in(polygon([(0.470,0.796),(0.562,0.793),(0.640,0.800),(0.666,0.818),
                    (0.620,0.840),(0.524,0.843),(0.468,0.834)]).inset(0.007),
           "bristle", "umb2", direction=(4, -12), density=1.0, size=0.012, load=1.0)
s.block_in(polygon([(0.636,0.800),(0.790,0.808),(0.868,0.815),(0.860,0.858),
                    (0.760,0.855),(0.634,0.843)]).inset(0.008),
           "bristle", "umb3", direction=(3, -10), density=1.0, size=0.014, load=0.95)
s.stroke([(0.322, 0.824), (0.400, 0.847), (0.478, 0.827)], "round_hard", "contact",
         size=0.013, pressure=[0.45, 1.0, 0.8], load=1.0)
print("strokes:", s.stroke_count)
print(s.look(sketch=False))
print(s.look(values=True))
