import math
# Light falling off the pool's rim onto the wet deck. This is also how the pool's
# silhouette gets sharpened -- the deck's own colour laid up to where the water
# stops, brush centre outside the shape. Never a line drawn along it.
def band(a, b, out, t, value, brush, size, op, press, run=0.05, load=1.0):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    pts = [(a[0] - ux * run + out[0] * t, a[1] - uy * run + out[1] * t),
           ((a[0] + b[0]) / 2 + out[0] * t * 1.12, (a[1] + b[1]) / 2 + out[1] * t * 1.12),
           (b[0] + ux * run + out[0] * t, b[1] + uy * run + out[1] * t)]
    s.stroke(pts, brush, p.at_value("deck", value), size=size, opacity=op,
             load=load, load_falloff=0.0 if brush == "flat" else 0.35, pressure=press)

s.dry()
OUT_NEAR = ( 0.743,  0.671)
OUT_FAR  = (-0.578, -0.816)
OUT_END  = ( 0.349, -0.937)
OUT_HEAD = (-0.492,  0.870)

# nearest the viewer and opposite the bright water: the strongest of the four
for t, v, br, sz, op, pr in [(0.020, 0.50, "flat",    0.034, 0.85, [0.30, 1.0, 0.75]),
                             (0.056, 0.42, "bristle", 0.058, 0.60, [0.20, 0.9, 0.60]),
                             (0.108, 0.34, "bristle", 0.078, 0.42, [0.10, 0.6, 0.35])]:
    band(pb, pc, OUT_NEAR, t, v, br, sz, op, pr, load=0.9)
# the near end, by lamp A: bright where the lamp is, gone at the far end of it
for t, v, br, sz, op, pr in [(0.026, 0.47, "flat",    0.032, 0.80, [1.0, 0.65, 0.20]),
                             (0.066, 0.38, "bristle", 0.055, 0.55, [0.9, 0.45, 0.10]),
                             (0.115, 0.31, "bristle", 0.072, 0.35, [0.7, 0.25, 0.0])]:
    band(pa, pb, OUT_HEAD, t, v, br, sz, op, pr, load=0.8)
# the far side, furthest from the light: two, dim, and mostly lost
for t, v, br, sz, op, pr in [(0.022, 0.38, "flat",    0.030, 0.60, [0.15, 0.7, 1.0]),
                             (0.062, 0.32, "bristle", 0.058, 0.35, [0.05, 0.4, 0.8])]:
    band(pa, pd, OUT_FAR, t, v, br, sz, op, pr, run=0.02, load=0.7)
# the far end, by lamp B
for t, v, br, sz, op, pr in [(0.028, 0.42, "flat",    0.030, 0.65, [0.2, 0.8, 0.9]),
                             (0.070, 0.33, "bristle", 0.056, 0.38, [0.1, 0.55, 0.7])]:
    band(pd, pc, OUT_END, t, v, br, sz, op, pr, run=0.02, load=0.7)
print(s.look())
