# pass 1b, take three -- halo as ONE tight low-contrast inward scumble, pool as before
s.dry()
halo2 = blob(span("C2", "F4"), wobble=0.22, seed=4)
s.scumble(halo2, p["halo_a"], p["halo_b"], 10, direction="inward")

pool_strokes = []
for i in range(9):
    t = i / 8.0
    y = 0.672 + t * 0.19
    half = 0.215 + t * 0.11
    val = 0.365 - t * 0.12
    col = p.at_value(p.mix("cerulean", "lemon_yellow", 0.55), val)
    pool_strokes.append({"points": [(0.515 - half, y + 0.004), (0.515, y), (0.515 + half, y - 0.004)],
                         "brush": "flat", "color": col, "size": 0.11,
                         "opacity": 0.5, "load": 1.0, "load_falloff": 0.0,
                         "pressure": [0.1, 0.9, 0.1]})
s.paint(pool_strokes)
s.look()
