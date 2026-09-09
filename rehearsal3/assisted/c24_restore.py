# Pass 24 — the F1:G8 block_in at size 0.16 overhung about 0.05 past its region
# (PAINTER.md warns of exactly this) and ate the mug's right side and the handle's
# cast shadow. Restate the mug's light strip, its right edge (by painting the
# background up to it, not by outlining it), and neutralise the salmon band the
# burnt_sienna strokes left across the bottom right.
# Run: python -m easel run painting.easel c24_restore.py
REF = r"C:\temp\Level1.jpg"
p = s.palette
M, T, D, S = p.mix, p.tint, p.desaturate, p.shade


def at_value(base, target):
    if p.value_of(base) < target:
        lo, hi, f = 0.0, 1.0, T
    else:
        lo, hi, f = 0.0, 1.0, S
    for _ in range(24):
        mid = (lo + hi) / 2
        if (p.value_of(f(base, mid)) < target) == (f is T):
            lo = mid
        else:
            hi = mid
    return f(base, (lo + hi) / 2)


NEUT = D(M("ultramarine", "burnt_umber", 0.40), 0.30)
p["pale"] = at_value(NEUT, 0.78)
p["pale2"] = at_value(NEUT, 0.70)
p["pale3"] = at_value(NEUT, 0.58)
p["wood_n"] = at_value(D(M("yellow_ochre", "burnt_umber", 0.34), 0.34), 0.58)
p["wood_d"] = at_value(D(M("yellow_ochre", "burnt_umber", 0.50), 0.34), 0.44)
p["shad"] = at_value(D(M("ultramarine", "burnt_umber", 0.55), 0.30), 0.30)
for k in ("pale", "pale2", "pale3", "wood_n", "wood_d", "shad"):
    print(f"{k:8s} {p.hex(p[k])} {p.value_of(p[k]):.3f}")

s.dry()

# --- 1. neutralise the salmon slab, bottom right --------------------------
n0 = s.stroke_count
for i, (a, b) in enumerate([((0.55, 0.905), (1.005, 0.83)),
                            ((1.005, 0.895), (0.55, 0.965)),
                            ((0.60, 0.995), (1.005, 0.955)),
                            ((1.005, 0.775), (0.72, 0.80))]):
    s.stroke([a, b], "flat", "wood_n", size=0.075, load=1.0, load_falloff=0.15,
             pressure="even", opacity=0.9)
print("salmon fix:", s.stroke_count - n0)

# --- 2. the background/shadow up to the mug's right edge ------------------
n0 = s.stroke_count
for i, (x, ty, by, col) in enumerate([(0.596, 0.30, 0.48, "wood_d"),
                                      (0.596, 0.48, 0.66, "shad"),
                                      (0.612, 0.36, 0.50, "wood_d"),
                                      (0.612, 0.50, 0.64, "shad"),
                                      (0.584, 0.34, 0.66, "shad")]):
    pts = [(x, ty), (x, by)]
    s.stroke(pts if i % 2 == 0 else pts[::-1], "flat", col, size=0.024,
             load=1.0, load_falloff=0.1, pressure="even")
print("right edge:", s.stroke_count - n0)

# --- 3. the mug's light again --------------------------------------------
n0 = s.stroke_count
# the band between the lip's shadow and the crewmate's head
for i, (y, lx, rx, col) in enumerate([(0.348, 0.352, 0.572, "pale"),
                                      (0.372, 0.356, 0.574, "pale"),
                                      (0.392, 0.358, 0.575, "pale2")]):
    pts = [(lx, y), (rx, y)]
    s.stroke(pts if i % 2 == 0 else pts[::-1], "flat", col, size=0.022,
             load=1.0, load_falloff=0.1, pressure="even")
# the lit strip right of the crewmate, down to the base
for i, (x, ty, by, col) in enumerate([(0.536, 0.40, 0.632, "pale"),
                                      (0.552, 0.40, 0.628, "pale"),
                                      (0.566, 0.40, 0.618, "pale2"),
                                      (0.500, 0.404, 0.450, "pale2"),
                                      (0.500, 0.552, 0.632, "pale2")]):
    pts = [(x, ty), (x, by)]
    s.stroke(pts if i % 2 == 0 else pts[::-1], "flat", col, size=0.020,
             load=1.0, load_falloff=0.1, pressure="even")
# the base band, and the narrow lit sliver on the far left
s.stroke([(0.372, 0.632), (0.430, 0.650), (0.494, 0.652), (0.540, 0.636)],
         "flat", "pale3", size=0.017, load=1.0, pressure="even")
s.stroke([(0.352, 0.360), (0.356, 0.470)], "flat", "pale3", size=0.012,
         load=1.0, pressure="even")
print("mug light:", s.stroke_count - n0)

print(s.look(region=span("C1", "G7"), reference=REF))
print("total strokes:", s.stroke_count)
