from easel import Region
print(s.compare(PLAN))
for nm, r in (("sidewalk", Region(0.30, 0.730, 0.55, 0.775)),
              ("road top", Region(0.30, 0.800, 0.55, 0.840)),
              ("road bot", Region(0.30, 0.960, 0.55, 1.000)),
              ("facade  ", Region(0.02, 0.400, 0.14, 0.520))):
    print(f"  {nm} pigment {p.value_of(s.sample(r)):.3f}")
print(s.look(values=True))
