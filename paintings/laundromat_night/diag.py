from easel import Region
print("planned facade_lt v=%.3f   facade v=%.3f" % (p.value_of(p["facade_lt"]), p.value_of(p["facade"])))
print("wall before:      %.3f" % p.value_of(s.sample(Region(0.30, 0.40, 0.45, 0.50))))
s.block_in(fascia(), "flat", "facade_lt", density=1.0, solid=True, size=0.022,
           direction="axis")
print("fascia pigment:   %.3f" % p.value_of(s.sample(Region(0.30, 0.275, 0.45, 0.305))))
s.block_in(base_course(), "flat", p.at_value("facade", 0.215), density=1.0,
           solid=True, size=0.024, direction="axis")
print("base   pigment:   %.3f" % p.value_of(s.sample(Region(0.30, 0.685, 0.45, 0.700))))
# and a glaze-height-free version of the same colour, for comparison
s.block_in(Region(0.55, 0.275, 0.70, 0.305), "flat", "facade_lt", density=1.0,
           solid=True, size=0.022, glaze=True)
print("fascia no-height: %.3f" % p.value_of(s.sample(Region(0.57, 0.280, 0.68, 0.300))))
print(s.look())
