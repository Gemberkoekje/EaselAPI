REF = "C:/temp/Level1.jpg"

pts = {
    "rim_l":   (0.295, 0.208),
    "rim_t":   (0.465, 0.112),
    "rim_r":   (0.643, 0.233),
    "rim_f":   (0.456, 0.347),
    "base_l":  (0.347, 0.646),
    "base_f":  (0.438, 0.672),
    "base_r":  (0.545, 0.637),
    "hand_r":  (0.735, 0.360),
    "hand_b":  (0.590, 0.512),
    "fig_t":   (0.427, 0.385),
    "fig_b":   (0.420, 0.655),
    "spoon_t": (0.520, 0.005),
    "shad_b":  (0.456, 0.854),
}
for k, (x, y) in pts.items():
    s.mark(k, x, y)

print(s.look(reference=REF))
print(s.look(region=span("C2", "F4"), reference=REF))
print(s.look(region=span("C5", "F7"), reference=REF))
