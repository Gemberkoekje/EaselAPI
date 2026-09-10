REF = "C:/temp/Level1.jpg"

pts = {
    "rim_l":   (0.3125, 0.221),
    "rim_t":   (0.465, 0.112),
    "rim_r":   (0.643, 0.250),
    "rim_f":   (0.456, 0.328),
    "base_l":  (0.364, 0.624),
    "base_f":  (0.456, 0.663),
    "base_r":  (0.548, 0.630),
    "hand_r":  (0.733, 0.358),
    "hand_b":  (0.575, 0.545),
    "fig_t":   (0.453, 0.397),
    "fig_b":   (0.430, 0.622),
    "spoon_t": (0.520, 0.005),
    "shad_b":  (0.440, 0.845),
}
for k, (x, y) in pts.items():
    s.mark(k, x, y)

print(s.look(reference=REF))
print(s.look(region=span("D1", "F2"), reference=REF))
print(s.look(region=span("C5", "F7"), reference=REF))
