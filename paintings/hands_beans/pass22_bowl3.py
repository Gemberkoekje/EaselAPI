# The bowl is a big smooth brown field and a bowl of dried beans is not smooth.
# Granularity, worked in from the rim where the light reaches first, thinning as
# it goes down into the shadow. Beans described only where the light finds them;
# the rest stays a mass, because nine described beans would cost the picture.
s.dry()

for pts, sz, col, ld, op in [
    ([(-0.030, 0.812), (0.060, 0.786), (0.156, 0.782), (0.240, 0.800)], 0.044,
     "bean_warm", 0.46, 0.44),
    ([(0.250, 0.836), (0.150, 0.820), (0.040, 0.826), (-0.040, 0.848)], 0.038,
     "bean_lit",  0.40, 0.34),
    ([(-0.030, 0.900), (0.080, 0.880), (0.190, 0.888)], 0.050, "bean_warm",
     0.42, 0.30),
    ([(0.210, 0.940), (0.100, 0.958), (-0.020, 0.950)], 0.046, "bean", 0.38, 0.28),
    ([(0.052, 0.996), (0.160, 0.982), (0.268, 0.996)], 0.042, "bean_dk", 0.40, 0.26),
]:
    s.stroke(pts, "bristle", col, size=sz, opacity=op, load=ld,
             load_falloff=0.40, pressure="swell", note="bowl")

# four beans the light actually finds, near the rim, no two alike
for pts, sz, col, op, pr, tw in [
    ([(0.036, 0.802), (0.062, 0.810)], 0.014, "bean_lit",  0.82, [0.85, 0.30], 0.60),
    ([(0.108, 0.792), (0.132, 0.786)], 0.012, "bean_warm", 0.66, [0.35, 0.90], 0.70),
    ([(0.176, 0.806), (0.196, 0.816)], 0.010, "bean_warm", 0.52, [0.75, 0.20], 0.75),
    ([(0.070, 0.856), (0.094, 0.850)], 0.011, "bean_warm", 0.44, [0.45, 0.85], 0.65),
]:
    s.stroke(pts, "round_hard", col, size=sz, opacity=op, load=1.0,
             tip_wobble=tw, pressure=pr, note="bowl")

# where the rim turns down into the bowl, on the side away from the light
s.stroke([(0.226, 0.788), (0.294, 0.820), (0.340, 0.866)], "bristle", "crock",
         size=0.026, opacity=0.62, load=0.85, load_falloff=0.45,
         pressure="swell", note="bowl")
print(s.look(region="A5:D8"))
