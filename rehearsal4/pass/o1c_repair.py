"""own1, pass 3 - the water's overhang buried the far bank, and the sun's path
came out a solid trapezoid. A real sun path is broken horizontals with water
between them, so cut the column apart with the water's own colour."""
p = s.palette
s.dry()

# the far bank, back on the horizon
s.sweep([(-0.03, 0.468), (0.16, 0.460), (0.34, 0.466), (0.50, 0.456),
         (0.64, 0.462), (0.82, 0.453), (1.03, 0.460)], "bristle", "bank",
        into="down", depth=0.032, size=0.026, cross=18, load=1.0)
print("bank:", s.stroke_count)

# cut the light column apart
cuts = [(0.44, 0.520, 0.30, "wat_far", 0.016), (0.52, 0.575, 0.26, "wat_far", 0.013),
        (0.40, 0.618, 0.34, "wat_far", 0.020), (0.56, 0.668, 0.22, "wat_near", 0.015),
        (0.42, 0.712, 0.30, "wat_near", 0.022), (0.50, 0.762, 0.34, "wat_near", 0.017),
        (0.38, 0.815, 0.26, "wat_near", 0.024), (0.52, 0.862, 0.32, "wat_near", 0.019),
        (0.40, 0.918, 0.30, "wat_near", 0.026), (0.46, 0.968, 0.36, "wat_near", 0.022)]
for x, y, w, col, sz in cuts:
    s.stroke([(x, y), (x + w * 0.5, y + 0.005), (x + w, y - 0.004)], "bristle",
             col, size=sz, opacity=0.85, load=0.95, load_falloff=0.3,
             note="cut the sun path")
for x, y, w, sz in [(0.585, 0.545, 0.11, 0.011), (0.560, 0.645, 0.15, 0.013),
                    (0.545, 0.788, 0.18, 0.015), (0.520, 0.905, 0.21, 0.016)]:
    s.stroke([(x, y), (x + w, y + 0.003)], "bristle", "wat_lit", size=sz,
             opacity=0.9, load=1.0, note="sun on the water")
print("path:", s.stroke_count)

# the near bank, bottom left: the one thing in front of the water
p["reed"] = p.mix(p["mud"], "burnt_umber", 0.35)
s.sweep([(-0.03, 0.955), (0.10, 0.930), (0.22, 0.945), (0.34, 0.918),
         (0.46, 0.948), (0.56, 0.985)], "bristle", "mud", into="down",
        depth=0.075, size=0.042, cross=22, load=1.0)
print("near bank:", s.stroke_count)

# reeds off it - the only near verticals, and they lean
for x, y0, h, lean, sz in [(0.04, 0.945, 0.115, 0.014, 0.005),
                           (0.09, 0.936, 0.155, -0.020, 0.005),
                           (0.13, 0.940, 0.090, 0.010, 0.004),
                           (0.20, 0.944, 0.170, 0.026, 0.006),
                           (0.235, 0.938, 0.110, -0.012, 0.004),
                           (0.30, 0.928, 0.190, 0.018, 0.006),
                           (0.345, 0.930, 0.125, -0.016, 0.004),
                           (0.41, 0.945, 0.150, 0.022, 0.005),
                           (0.47, 0.952, 0.098, -0.010, 0.004)]:
    s.stroke([(x, y0), (x + lean * 0.4, y0 - h * 0.6), (x + lean, y0 - h)],
             "liner", "reed", size=sz, pressure=[1.0, 0.6, 0.15], note="reed")
print("reeds:", s.stroke_count)

# the standing dead tree, left of centre, and its broken reflection
p["tree"] = "#191720"
s.stroke([(0.247, 0.605), (0.243, 0.400), (0.238, 0.215)], "flat", "tree",
         size=0.011, pressure=[1.0, 0.8, 0.35], note="trunk")
for a, b, c, sz in [((0.240, 0.330), (0.205, 0.290), (0.178, 0.252), 0.005),
                    ((0.241, 0.302), (0.276, 0.268), (0.305, 0.246), 0.005),
                    ((0.239, 0.256), (0.214, 0.222), (0.196, 0.196), 0.004),
                    ((0.238, 0.240), (0.262, 0.208), (0.279, 0.185), 0.004),
                    ((0.244, 0.392), (0.281, 0.362), (0.300, 0.350), 0.004)]:
    s.stroke([a, b, c], "liner", "tree", size=sz, pressure=[1.0, 0.5, 0.1],
             note="branch")
for x, y, w, sz, op in [(0.232, 0.628, 0.030, 0.008, 0.8),
                        (0.238, 0.665, 0.022, 0.007, 0.6),
                        (0.228, 0.712, 0.034, 0.009, 0.5),
                        (0.240, 0.768, 0.026, 0.008, 0.4)]:
    s.stroke([(x, y), (x + w, y + 0.002)], "bristle", "tree", size=sz,
             opacity=op, load=1.0, note="reflection")
print("tree:", s.stroke_count)

for x, y, sz in [(0.795, 0.212, 0.008), (0.838, 0.190, 0.006), (0.760, 0.168, 0.005)]:
    s.stroke([(x - sz * 1.6, y + sz * 0.5), (x, y - sz * 0.4),
              (x + sz * 1.6, y + sz * 0.6)], "liner", "bank", size=sz * 0.55,
             pressure=[0.6, 1.0, 0.6], note="bird")
print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
