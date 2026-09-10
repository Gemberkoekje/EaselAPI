REF = "C:/temp/Level1.jpg"

grain = [
    # across the dark left field and over the join, at the angle the grain runs
    ((0.03, 0.20), (0.31, 0.152), "bristle", 0.035, "wood_mid",   "taper"),
    ((0.01, 0.43), (0.27, 0.388), "bristle", 0.024, "wood_mid",   "lift_off"),
    ((0.06, 0.63), (0.36, 0.580), "bristle", 0.030, "wood_field", "swell"),
    ((0.00, 0.87), (0.29, 0.822), "bristle", 0.021, "wood_mid",   "press_in"),
    ((0.11, 0.31), (0.42, 0.258), "bristle", 0.028, "wood_field", "taper"),
    ((0.15, 0.73), (0.44, 0.681), "bristle", 0.019, "wood_field", "lift_off"),
    # fine dark lines on the lit wood
    ((0.55, 0.15), (0.89, 0.088), "liner",   0.006, "wood_mid",   "taper"),
    ((0.63, 0.31), (0.96, 0.243), "liner",   0.005, "wood_mid",   "lift_off"),
    ((0.46, 0.93), (0.82, 0.868), "liner",   0.006, "wood_mid",   "swell"),
    ((0.71, 0.56), (0.99, 0.508), "liner",   0.005, "wood_mid",   "taper"),
    # light streaks, crossing the edges of the light band
    ((0.34, 0.97), (0.74, 0.902), "bristle", 0.030, "wood_hot",   "swell"),
    ((0.56, 0.43), (0.91, 0.368), "bristle", 0.026, "wood_hot",   "taper"),
    ((0.73, 0.13), (0.99, 0.083), "bristle", 0.023, "wood_light", "lift_off"),
    ((0.78, 0.83), (1.00, 0.788), "bristle", 0.028, "wood_light", "press_in"),
]
for a, b, brush, size, col, pr in grain:
    s.stroke([a, b], brush, col, size=size, pressure=pr, load=1.0,
             load_falloff=0.0, note="grain")
print("grain", s.stroke_count)

# lose the joins the block-ins left behind
s.smudge([(0.415, 0.985), (0.472, 0.858)], size=0.042)
s.smudge([(0.872, 0.868), (0.952, 0.802)], size=0.042)
s.smudge([(0.292, 0.205), (0.312, 0.345)], size=0.040)
s.smudge([(0.278, 0.560), (0.300, 0.700)], size=0.040)
print("joins", s.stroke_count)

print(s.look(reference=REF))
print(s.look(region=span("A1", "D4"), reference=REF))
