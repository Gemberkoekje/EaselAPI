# The surroundings get the last third. The fall of light is laid as overlapping
# passes that lose their ends rather than as a shape, because a shape leaves its
# own boundary across the picture. Each stops short of the hands: a pale pass laid
# late is still in front of whatever it crosses, and that is how fingers get lost.
s.dry()

RAMP = [
    ([(-0.08, 0.20), (0.34, -0.02), (0.72, -0.14)], 0.00),
    ([(-0.08, 0.31), (0.36, 0.07), (0.74, -0.08)], 0.20),
    ([(-0.08, 0.42), (0.34, 0.17), (0.70, 0.01)], 0.40),
    ([(-0.08, 0.53), (0.27, 0.30), (0.56, 0.14)], 0.60),
    ([(-0.08, 0.63), (0.10, 0.50), (0.21, 0.43)], 0.80),
    ([(-0.08, 0.73), (0.05, 0.62), (0.13, 0.56)], 1.00),
]
for pts, t in RAMP:
    long_enough = abs(pts[-1][0] - pts[0][0]) > 0.45
    s.stroke(pts, "bristle", p.mix(p["glow"], p["table"], t), size=0.145,
             opacity=0.52, load=1.0, load_falloff=0.0,
             pressure=([1.0, 0.65, 0.0] if long_enough else "lift_off"),
             note="table")

# grain: four marks that describe it, none parallel to another, each breaking
s.stroke([(-0.06, 0.148), (0.28, 0.212), (0.63, 0.238), (1.06, 0.222)], "bristle",
         "grain", size=0.030, load=0.46, load_falloff=0.55, opacity=0.34,
         pressure="swell", note="table")
s.stroke([(1.06, 0.470), (0.78, 0.436), (0.56, 0.398)], "bristle", "grain",
         size=0.024, load=0.40, load_falloff=0.60, opacity=0.28,
         pressure="swell", note="table")
s.stroke([(0.04, 0.688), (0.16, 0.648), (0.26, 0.632)], "bristle", "tbl_lit",
         size=0.020, load=0.38, load_falloff=0.60, opacity=0.24,
         pressure="swell", note="table")
s.stroke([(0.88, 0.086), (0.97, 0.306), (1.02, 0.552)], "bristle", "grain",
         size=0.026, load=0.42, load_falloff=0.55, opacity=0.26,
         pressure="swell", note="table")

for pts, sz, op in [([(1.06, 0.10), (0.98, 0.32), (0.95, 0.54)], 0.17, 0.30),
                    ([(0.60, 1.06), (0.34, 1.03), (0.10, 1.05)], 0.16, 0.28),
                    ([(0.34, -0.06), (0.58, 0.01), (0.78, 0.01)], 0.13, 0.20)]:
    s.glaze(pts, "corner", opacity=op, size=sz, note="table")
print(s.look())
