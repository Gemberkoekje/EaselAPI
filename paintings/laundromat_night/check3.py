from easel import Region
for nm, r in (("figure   ", Region(0.605, 0.520, 0.645, 0.580)),
              ("band     ", Region(0.240, 0.525, 0.290, 0.545)),
              ("door     ", Region(0.298, 0.552, 0.312, 0.564)),
              ("wall     ", Region(0.230, 0.430, 0.330, 0.470)),
              ("planned figure %.2f band %.2f" % (p.value_of(p["figure"]), p.value_of(p["machine"])), None)):
    if r is None:
        print(" ", nm); continue
    print(f"  {nm} {p.value_of(s.sample(r)):.3f}")
print(s.look(region="D4:F6"))
