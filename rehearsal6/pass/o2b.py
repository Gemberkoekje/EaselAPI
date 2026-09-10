# 1. the furthest thing: the lit room beyond, and the light it throws on the floor
s.block_in(polygon([(0.33,-0.04),(0.70,-0.04),(0.72,0.865),(0.30,0.865)]),
           "flat", "lit", direction=90, density=0.9, size=0.085, load=1.0,
           pressure="even")
print("light", s.stroke_count)
s.block_in(polygon([(0.30,0.845),(0.72,0.845),(1.00,1.04),(0.02,1.04)]),
           "flat", "spill2", direction=4, density=0.85, size=0.075, load=1.0,
           pressure="even")
print("spill", s.stroke_count)
s.block_in(polygon([(0.42,-0.04),(0.60,-0.04),(0.61,0.845),(0.41,0.845)]),
           "flat", "blaze", direction=90, density=0.95, size=0.045, load=1.0,
           pressure="even")
print("core", s.stroke_count)
print(s.look())
