REF = "C:/temp/Level1.jpg"

# --- paint out the two smudge lobes --------------------------------------
for a, b, size, col in [((0.215, 0.183), (0.375, 0.158), 0.046, "wood_mid"),
                        ((0.205, 0.216), (0.360, 0.190), 0.038, "wood_field"),
                        ((0.215, 0.543), (0.365, 0.518), 0.046, "wood_mid"),
                        ((0.200, 0.578), (0.355, 0.553), 0.038, "wood_field")]:
    s.stroke([a, b], "bristle", col, size=size, load=1.0, load_falloff=0.0,
             pressure="even", note="kill smudge lobe")

# --- break up the ruled grain lines --------------------------------------
for a, b, brush, size, col in [((0.80, 0.245), (0.99, 0.212), "bristle", 0.018, "wood_light"),
                               ((0.87, 0.445), (1.00, 0.423), "bristle", 0.015, "wood_mid"),
                               ((0.62, 0.082), (0.79, 0.056), "liner", 0.004, "wood_light")]:
    s.stroke([a, b], brush, col, size=size, load=1.0, load_falloff=0.0, note="grain")
print("repairs+grain", s.stroke_count)

# --- the shadow, previewed but not painted -------------------------------
core = polygon([(0.400, 0.545), (0.345, 0.600), (0.316, 0.668), (0.336, 0.755),
                (0.388, 0.815), (0.443, 0.843), (0.505, 0.826), (0.560, 0.766),
                (0.594, 0.690), (0.614, 0.600), (0.600, 0.545)])
pen = core.scaled(1.10)
ring = ribbon([(0.607, 0.548), (0.655, 0.520), (0.702, 0.545),
               (0.714, 0.580), (0.678, 0.602), (0.632, 0.592)], 0.030)
print("core  ", s.preview(core, reference=REF, region=span("C5", "G7")))
print("pen   ", s.preview(pen, reference=REF, region=span("C5", "G7")))
print("ring  ", s.preview(ring, reference=REF, region=span("E5", "G6")))

print(s.look(region=span("A1", "C4"), reference=REF))
