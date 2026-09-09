# Pass 21 — darken the crewmate (still landing near 0.35 against the reference's
# 0.15) and lay the cast shadow. The shadow is driven row by row so it keeps its
# silhouette and does not paint over the mug; block_in would have given a box.
# Run: python -m easel run painting.easel c21_shadow.py
REF = r"C:\temp\Level1.jpg"
p = s.palette
M, T, D, S = p.mix, p.tint, p.desaturate, p.shade

p["fig_dk"] = S(M("burnt_umber", "ultramarine", 0.14), 1.0)
p["shad_core"] = S(M("ultramarine", "burnt_umber", 0.50), 1.0)
p["shad_mid"] = T(D(M("ultramarine", "burnt_umber", 0.55), 0.30), 0.16)
p["shad_out"] = T(D(M("ultramarine", "burnt_sienna", 0.50), 0.38), 0.26)
p["wood_lit"] = T(D(M("yellow_ochre", "burnt_umber", 0.32), 0.28), 0.40)
for k in ("fig_dk", "shad_core", "shad_mid", "shad_out"):
    print(f"{k:10s} {p.hex(p[k])} {p.value_of(p[k]):.3f}")

s.dry()

# --- the crewmate, one more crossing pass at full opacity ------------------
n0 = s.stroke_count
rows = [(0.410, 0.376, 0.458), (0.432, 0.364, 0.468), (0.462, 0.360, 0.470),
        (0.492, 0.359, 0.521), (0.522, 0.359, 0.521), (0.552, 0.359, 0.470),
        (0.582, 0.359, 0.470), (0.610, 0.360, 0.470), (0.634, 0.362, 0.403),
        (0.634, 0.433, 0.469)]
for i, (y, lx, rx) in enumerate(rows):
    pts = [(lx, y), (rx, y)]
    s.stroke(pts if i % 2 == 0 else pts[::-1], "flat", "fig_dk", size=0.017,
             load=1.0, load_falloff=0.05, pressure="even", opacity=1.0)
print("figure darken:", s.stroke_count - n0)

# --- the cast shadow ------------------------------------------------------
n0 = s.stroke_count
SH = [(0.602, [(0.332, 0.354), (0.562, 0.602)], "shad_core"),
      (0.626, [(0.318, 0.358), (0.556, 0.606)], "shad_core"),
      (0.652, [(0.306, 0.380), (0.524, 0.606)], "shad_core"),
      (0.676, [(0.296, 0.586)], "shad_core"),
      (0.700, [(0.290, 0.574)], "shad_mid"),
      (0.726, [(0.288, 0.558)], "shad_mid"),
      (0.752, [(0.290, 0.536)], "shad_mid"),
      (0.778, [(0.298, 0.512)], "shad_out"),
      (0.802, [(0.318, 0.482)], "shad_out"),
      (0.824, [(0.352, 0.442)], "shad_out")]
i = 0
for y, segs, col in SH:
    for lx, rx in segs:
        pts = [(lx, y), (rx, y)]
        s.stroke(pts if i % 2 == 0 else pts[::-1], "flat", col, size=0.028,
                 load=1.0, load_falloff=0.12, pressure="even")
        i += 1
print("shadow body:", s.stroke_count - n0)

# the handle's own cast shadow, a ring with lit wood inside it
n0 = s.stroke_count
LOBE = [(0.514, 0.598, 0.676), (0.536, 0.578, 0.700), (0.560, 0.574, 0.704),
        (0.582, 0.576, 0.700), (0.604, 0.584, 0.682), (0.624, 0.596, 0.658)]
for i, (y, lx, rx) in enumerate(LOBE):
    pts = [(lx, y), (rx, y)]
    s.stroke(pts if i % 2 == 0 else pts[::-1], "flat", "shad_mid", size=0.024,
             load=1.0, load_falloff=0.1, pressure="even")
s.dry()
s.stroke([(0.600, 0.538), (0.658, 0.540)], "flat", "wood_lit", size=0.020,
         load=1.0, pressure="even")
s.stroke([(0.660, 0.562), (0.598, 0.560)], "flat", "wood_lit", size=0.020,
         load=1.0, pressure="even")
print("handle shadow:", s.stroke_count - n0)

print(s.look(reference=REF))
print("total strokes:", s.stroke_count)
