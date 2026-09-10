"""Pass E - the mug itself, over the shadow. Body first, then the two sides
swept along their own silhouettes so the passes describe the cylinder."""
p = s.palette
p["mug_face"] = p.desaturate(p.mix(p.mix("cadmium_red", "ultramarine", 0.7),
                                   "titanium_white", 0.55), 0.5)
p["mug_shade"] = p.desaturate(p.mix(p.mix("ultramarine", "burnt_sienna", 0.3),
                                    "titanium_white", 0.45), 0.25)
p["mug_rim"] = p.desaturate(p.mix(p.mix("ultramarine", "burnt_sienna", 0.1),
                                  "titanium_white", 0.85), 0.25)
p["mug_lit"] = p.mix(p["mug_face"], p["mug_rim"], 0.55)
p["mug_hi"] = p.mix(p["mug_rim"], "titanium_white", 0.55)
p["tea"] = "#0d0a09"
for n in ("mug_shade", "mug_face", "mug_lit", "mug_rim", "mug_hi"):
    print(f"{n:9s} {p.hex(p[n])} v={p.value_of(p[n]):.2f}")

mug = polygon([(0.304, 0.247), (0.322, 0.180), (0.358, 0.138), (0.412, 0.114),
               (0.470, 0.107), (0.528, 0.120), (0.578, 0.148), (0.612, 0.196),
               (0.628, 0.268), (0.622, 0.372), (0.608, 0.498), (0.591, 0.624),
               (0.5625, 0.670), (0.500, 0.706), (0.430, 0.712), (0.372, 0.666),
               (0.352, 0.625), (0.334, 0.500), (0.3206, 0.375)])

# the handle goes down first - it is behind the body where they meet
handle = ribbon([(0.632, 0.298), (0.674, 0.322), (0.698, 0.364), (0.696, 0.414),
                 (0.666, 0.454), (0.622, 0.480)], 0.034)
s.block_in(handle, "flat", "mug_face", direction="axis", density=1.0,
           size=0.034, load=1.0)
print("handle:", s.stroke_count)

s.block_in(mug, "flat", "mug_face", direction=("axis", 74), density=0.95,
           size=0.12, load=1.0)
print("body:", s.stroke_count)

# the shadowed left of the cylinder, swept along its own edge
s.sweep([(0.306, 0.252), (0.3206, 0.375), (0.334, 0.500), (0.352, 0.625),
         (0.372, 0.666)], "bristle", "mug_shade", into=(0.47, 0.45),
        depth=0.085, size=0.055, cross=24, load=1.0)
print("left shade:", s.stroke_count)

# the lit right of the cylinder
s.sweep([(0.627, 0.285), (0.622, 0.372), (0.608, 0.498), (0.591, 0.624),
         (0.562, 0.670)], "bristle", "mug_lit", into=(0.47, 0.45),
        depth=0.070, size=0.048, cross=24, load=1.0)
print("right lit:", s.stroke_count)

# the rim: the pale band round the top, swept in from the outer arc
s.sweep([(0.304, 0.247), (0.322, 0.180), (0.358, 0.138), (0.412, 0.114),
         (0.470, 0.107), (0.528, 0.120), (0.578, 0.148), (0.612, 0.196),
         (0.628, 0.268)], "bristle", "mug_rim", into=(0.47, 0.30),
        depth=0.045, size=0.030, cross=22, load=1.0)
print("rim:", s.stroke_count)

# the dark inside, laid over the rim's inner half
inside = polygon([(0.336, 0.258), (0.352, 0.200), (0.395, 0.160), (0.450, 0.140),
                  (0.515, 0.145), (0.565, 0.175), (0.594, 0.225), (0.590, 0.268),
                  (0.545, 0.297), (0.470, 0.313), (0.400, 0.300), (0.355, 0.280)])
s.block_in(inside, "flat", "tea", direction=("axis", 68), density=1.0,
           size=0.055, load=1.0)
print("inside:", s.stroke_count)

print("strokes:", s.stroke_count)
print(s.look())
print(s.look(region=span("C2", "F6"), reference="ref.jpg"))
