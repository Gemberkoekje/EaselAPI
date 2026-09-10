"""Pass A3 - lose the block-in's shoulders, put the grain in the wood."""
p = s.palette
p["grain_d"] = p.desaturate(p.mix(p.mix("cadmium_yellow", "burnt_umber", 0.75),
                                  "titanium_white", 0.30), 0.35)
p["grain_l"] = p.desaturate(p.mix(p.mix("lemon_yellow", "burnt_umber", 0.62),
                                  "titanium_white", 0.70), 0.20)
print("grain_d", p.hex(p["grain_d"]), round(p.value_of(p["grain_d"]), 2))
print("grain_l", p.hex(p["grain_l"]), round(p.value_of(p["grain_l"]), 2))

# lose the shoulders the ellipses left
for a, b, sz in [((0.55, 0.06), (0.60, 0.34), 0.11),
                 ((0.60, 0.34), (0.585, 0.62), 0.11),
                 ((0.30, 0.74), (0.55, 0.70), 0.10),
                 ((0.16, 0.10), (0.13, 0.52), 0.10),
                 ((0.13, 0.52), (0.17, 0.96), 0.10),
                 ((0.80, 0.86), (0.95, 0.70), 0.10),
                 ((0.86, 0.10), (0.93, 0.34), 0.09)]:
    s.smudge([a, b], size=sz)
print("after smudge:", s.stroke_count)

grain = [
    ([(0.00, 0.09), (0.30, 0.05), (0.62, 0.02)], "grain_d", 0.018, 0.30),
    ([(0.00, 0.30), (0.34, 0.24), (0.66, 0.17)], "grain_d", 0.012, 0.22),
    ([(0.02, 0.47), (0.30, 0.43), (0.55, 0.38)], "grain_l", 0.010, 0.18),
    ([(0.00, 0.62), (0.22, 0.60), (0.40, 0.57)], "grain_d", 0.014, 0.22),
    ([(0.00, 0.80), (0.26, 0.78), (0.50, 0.75)], "grain_d", 0.020, 0.20),
    ([(0.04, 0.95), (0.34, 0.93), (0.62, 0.90)], "grain_l", 0.012, 0.20),
    ([(0.66, 0.13), (0.84, 0.09), (1.00, 0.06)], "grain_d", 0.014, 0.24),
    ([(0.70, 0.30), (0.88, 0.25), (1.00, 0.21)], "grain_l", 0.010, 0.20),
    ([(0.66, 0.46), (0.86, 0.42), (1.00, 0.39)], "grain_d", 0.011, 0.18),
    ([(0.72, 0.64), (0.90, 0.60), (1.00, 0.58)], "grain_l", 0.013, 0.22),
    ([(0.62, 0.86), (0.84, 0.81), (1.00, 0.78)], "grain_d", 0.016, 0.20),
    ([(0.52, 1.00), (0.78, 0.96), (1.00, 0.93)], "grain_l", 0.011, 0.18),
    ([(0.10, 0.20), (0.26, 0.34), (0.34, 0.52)], "grain_d", 0.008, 0.14),
    ([(0.78, 0.02), (0.88, 0.16), (0.94, 0.32)], "grain_d", 0.008, 0.13),
]
for pts, col, sz, op in grain:
    s.stroke(pts, "bristle", col, size=sz, opacity=op, load=0.5,
             load_falloff=0.1, pressure="taper", note="grain")

print("strokes:", s.stroke_count)
print(s.look())
