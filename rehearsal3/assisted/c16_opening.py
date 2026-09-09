# Pass 16 — the opening. Rejected in 16a:
#   * the tea went on over still-wet mug paint and mixed to a milky mid-brown
#     (planned value 0.23, rehearsed at roughly 0.45). dry() first.
#   * the pale rim painted as a RING around the hole read as a rope laid on the
#     mug -- an outline, exactly what PAINTER.md says not to do. Instead: fill
#     the whole opening with the inner-wall tone so it is continuous with the
#     body, dry, then lay the tea on top and let the crescent be what is left.
#   * the tea's left edge was at 0.352; re-read off the crop it is 0.391, so the
#     lit inner wall is a much wider crescent than I had it.
# Run: python -m easel run painting.easel c16_opening.py
REF = r"C:\temp\Level1.jpg"
p = s.palette
M, T, D, S = p.mix, p.tint, p.desaturate, p.shade

BLUEGREY = D(M("cerulean", "burnt_umber", 0.32), 0.22)
p["wall"] = T(BLUEGREY, 0.62)
p["wall_lit"] = T(BLUEGREY, 0.80)
p["tea"] = S(M("ultramarine", "burnt_umber", 0.55), 1.0)
p["bag"] = T(M("yellow_ochre", "burnt_umber", 0.45), 0.30)
for k in ("wall", "wall_lit", "tea", "bag"):
    print(f"{k:9s} {p.hex(p[k])} {p.value_of(p[k]):.3f}")

s.dry()

# 1. the inside of the mug, all of it, in the inner-wall tone
OPEN = [(0.110, 0.415, 0.545), (0.130, 0.368, 0.590), (0.155, 0.340, 0.612),
        (0.180, 0.318, 0.630), (0.205, 0.312, 0.636), (0.230, 0.314, 0.632),
        (0.255, 0.326, 0.616), (0.280, 0.352, 0.588), (0.305, 0.396, 0.540),
        (0.320, 0.440, 0.500)]
n0 = s.stroke_count
for i, (y, lx, rx) in enumerate(OPEN):
    a, b = (lx, y), (rx, y)
    if i % 2:
        a, b = b, a
    col = "wall_lit" if y < 0.17 else "wall"
    s.stroke([a, b], "flat", col, size=0.026, load=1.0, load_falloff=0.1,
             pressure="even")
print("opening fill:", s.stroke_count - n0)

s.dry()

# 2. the tea, on dry paint so it reads as itself
TEA = [(0.135, 0.470, 0.545), (0.150, 0.428, 0.590), (0.170, 0.406, 0.606),
       (0.190, 0.396, 0.618), (0.210, 0.391, 0.625), (0.230, 0.390, 0.622),
       (0.250, 0.391, 0.616), (0.270, 0.398, 0.605), (0.290, 0.412, 0.585),
       (0.310, 0.440, 0.545), (0.324, 0.470, 0.512)]
n0 = s.stroke_count
for i, (y, lx, rx) in enumerate(TEA):
    a, b = (lx, y), (rx, y)
    if i % 2:
        a, b = b, a
    s.stroke([a, b], "flat", "tea", size=0.023, load=1.0, load_falloff=0.05,
             pressure="even")
print("tea:", s.stroke_count - n0)

# 3. the teabag showing at the right of the surface, two dabs not one
s.dab(0.582, 0.205, "round_hard", "bag", size=0.020)
s.dab(0.590, 0.214, "round_hard", "bag", size=0.016)

print(s.look(region=span("C1", "F4"), reference=REF))
print("total strokes:", s.stroke_count)
