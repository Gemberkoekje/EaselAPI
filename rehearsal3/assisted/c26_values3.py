# Pass 26 — down the compare list again. G/H are now +0.11..+0.21 (I over-lifted
# the right of the table); D2-D6 and E2-E5 are still +0.13..+0.26 too light.
# Arithmetic on the cell means says D3 must be about three-quarters dark, i.e.
# the tea's front edge belongs at y=0.345, not 0.325.
# Run: python -m easel run painting.easel c26_values3.py
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
WOOD = D(M("yellow_ochre", "burnt_umber", 0.42), 0.32)
p["g_wood"] = at_value(WOOD, 0.45)
p["h_wood"] = at_value(WOOD, 0.36)
p["tea"] = S(M("ultramarine", "burnt_umber", 0.55), 1.0)
p["deep"] = S(M("ultramarine", "burnt_umber", 0.45), 1.0)
p["mid_pale"] = at_value(NEUT, 0.68)
p["navy"] = at_value(M("ultramarine", "burnt_umber", 0.28), 0.26)
print("navy", p.hex(p["navy"]), round(p.value_of(p["navy"]), 3))

s.dry()

# --- 1. the right third of the table, back down ---------------------------
n0 = s.stroke_count
s.block_in(span("G1", "H8"), "flat", "g_wood", density=0.7, size=0.11,
           direction="diagonal", overhang=0.0, opacity=0.75)
for i, (a, b) in enumerate([((0.90, 0.02), (0.90, 0.98)),
                            ((0.965, 0.98), (0.965, 0.02)),
                            ((0.885, 0.06), (1.005, 0.10))]):
    s.stroke([a, b], "flat", "h_wood", size=0.075, load=1.0, load_falloff=0.12,
             pressure="even", opacity=0.65)
print("right third:", s.stroke_count - n0)

# --- 2. the tea, down to its real front edge, at the floor ----------------
n0 = s.stroke_count
for i, (y, lx, rx, sz) in enumerate([(0.180, 0.412, 0.600, 0.048),
                                     (0.235, 0.398, 0.614, 0.052),
                                     (0.290, 0.392, 0.584, 0.046),
                                     (0.330, 0.398, 0.548, 0.030)]):
    pts = [(lx, y), (rx, y)]
    s.stroke(pts if i % 2 == 0 else pts[::-1], "flat", "tea", size=sz,
             load=1.0, load_falloff=0.05, pressure="even", opacity=1.0)
# the shadow the lip throws, down to y=0.345
s.stroke([(0.362, 0.336), (0.440, 0.348), (0.520, 0.346), (0.566, 0.334)],
         "flat", "deep", size=0.020, load=1.0, pressure="even")
print("tea deeper:", s.stroke_count - n0)

# --- 3. the deep shadow immediately right of the mug ----------------------
n0 = s.stroke_count
for i, (x, ty, by) in enumerate([(0.590, 0.470, 0.650), (0.606, 0.490, 0.646),
                                 (0.578, 0.500, 0.646)]):
    pts = [(x, ty), (x, by)]
    s.stroke(pts if i % 2 == 0 else pts[::-1], "flat", "deep", size=0.022,
             load=1.0, load_falloff=0.08, pressure="even", opacity=0.9)
# and the shadow's core under the base
s.stroke([(0.330, 0.678), (0.430, 0.700), (0.520, 0.690)], "flat", "deep",
         size=0.048, load=1.0, load_falloff=0.08, pressure="even", opacity=0.9)
s.stroke([(0.500, 0.650), (0.400, 0.664), (0.330, 0.652)], "flat", "deep",
         size=0.030, load=1.0, load_falloff=0.08, pressure="even", opacity=0.8)
print("deep right + core:", s.stroke_count - n0)

# --- 4. knock the two over-bright slabs on the mug back -------------------
n0 = s.stroke_count
s.stroke([(0.360, 0.368), (0.470, 0.372), (0.566, 0.366)], "flat", "mid_pale",
         size=0.026, load=1.0, load_falloff=0.15, pressure="even", opacity=0.75)
s.stroke([(0.548, 0.420), (0.544, 0.610)], "flat", "mid_pale", size=0.040,
         load=1.0, load_falloff=0.15, pressure="even", opacity=0.7)
print("knock back:", s.stroke_count - n0)

# --- 5. the tag is meant to be navy, not brown ----------------------------
for i, (y, lx, rx) in enumerate([(0.568, 0.824, 0.910), (0.600, 0.820, 0.912),
                                 (0.628, 0.834, 0.898)]):
    pts = [(lx, y), (rx, y)]
    s.stroke(pts if i % 2 == 0 else pts[::-1], "flat", "navy", size=0.022,
             load=1.0, pressure="even")

print(s.look(reference=REF))
print("total strokes:", s.stroke_count)
