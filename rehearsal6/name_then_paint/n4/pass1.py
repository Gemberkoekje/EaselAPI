exec(open("_pal.py").read())
exec(open("_geom.py").read())

# 1. the furthest thing: the light in the glass
s.block_in(GLASS, "flat", "glass", direction=(100, 14), density=0.9,
           size=0.16, pressure="even", load=1.0, load_falloff=0.2)
s.block_in(HOT.inset(0.03), "flat", "glass_hot", direction=(112,), density=0.85,
           size=0.11, pressure="even", load=1.0)
s.block_in(LOW.inset(0.03), "flat", "glass_low", direction=(84,), density=0.85,
           size=0.10, pressure="even", load=1.0)
# lose the joins while the paint is still moving
for a, b in [((0.255, 0.055), (0.215, 0.245)), ((0.235, 0.300), (0.320, 0.355)),
             ((0.300, 0.395), (0.155, 0.330)), ((0.105, 0.345), (0.075, 0.290)),
             ((0.470, 0.330), (0.420, 0.400))]:
    s.smudge([a, b], size=0.042)

# 2. the wall to the right of it
s.block_in(WALL, "flat", "wall", direction=(104, 16), density=0.9,
           size=0.15, pressure="even", load=1.0, load_falloff=0.2)
s.block_in(polygon([(0.552,0.02),(0.700,0.0),(0.712,0.62),(0.556,0.615)]),
           "bristle", "wall_lit", direction=(97,), density=0.75, size=0.09, load=0.85)
s.block_in(polygon([(0.855,0.0),(1.0,0.0),(1.0,0.30),(0.870,0.42)]),
           "bristle", "wall_dk", direction=(108,), density=0.7, size=0.10, load=0.85)
for a, b in [((0.706, 0.120), (0.742, 0.200)), ((0.716, 0.330), (0.680, 0.420)),
             ((0.700, 0.520), (0.735, 0.580)), ((0.862, 0.180), (0.830, 0.260)),
             ((0.876, 0.360), (0.905, 0.415))]:
    s.smudge([a, b], size=0.040)

print(s.stroke_count)
print(s.look())
