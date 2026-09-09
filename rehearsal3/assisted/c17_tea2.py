# Pass 17 — the tea went on at value 0.23 onto dry paint and still reads about
# 0.42: one pass of `flat` at load 1.0 does not cover. Cross it. Also the whole
# mug is too teal -- cerulean + burnt_umber is a green-grey, not the blue-white
# of the reference -- so re-state the visible pale with an ultramarine grey.
# Run: python -m easel run painting.easel c17_tea2.py
REF = r"C:\temp\Level1.jpg"
p = s.palette
M, T, D, S = p.mix, p.tint, p.desaturate, p.shade

for rec in s.log()[-6:]:
    print(rec)

NEUT = D(M("ultramarine", "burnt_umber", 0.45), 0.28)
p["n80"] = T(NEUT, 0.80)
p["n70"] = T(NEUT, 0.66)
p["n60"] = T(NEUT, 0.52)
p["tea"] = S(M("ultramarine", "burnt_umber", 0.55), 1.0)
for k in ("n80", "n70", "n60", "tea"):
    print(f"{k:5s} {p.hex(p[k])} {p.value_of(p[k]):.3f}")

# --- tea, crossed ---------------------------------------------------------
COL = [(0.400, 0.185, 0.285), (0.420, 0.163, 0.302), (0.440, 0.152, 0.315),
       (0.460, 0.143, 0.323), (0.480, 0.137, 0.327), (0.500, 0.134, 0.327),
       (0.520, 0.132, 0.322), (0.540, 0.133, 0.313), (0.560, 0.139, 0.300),
       (0.580, 0.148, 0.288), (0.600, 0.163, 0.268), (0.614, 0.185, 0.240)]
n0 = s.stroke_count
for i, (x, ty, by) in enumerate(COL):
    a, b = (x, ty), (x, by)
    if i % 2:
        a, b = b, a
    s.stroke([a, b], "flat", "tea", size=0.022, load=1.0, load_falloff=0.05,
             pressure="even")
print("tea cross:", s.stroke_count - n0)

# --- the mug's visible pale, re-stated in a blue grey instead of a teal one --
n0 = s.stroke_count
band = [(0.348, 0.352, 0.598, "n80", 0.030),
        (0.382, 0.356, 0.592, "n80", 0.030),
        (0.415, 0.360, 0.587, "n70", 0.026)]
for i, (y, lx, rx, col, sz) in enumerate(band):
    a, b = (lx, y), (rx, y)
    if i % 2:
        a, b = b, a
    s.stroke([a, b], "flat", col, size=sz, load=1.0, load_falloff=0.15,
             pressure="even", opacity=0.85)
# the lit right-hand strip of the body, below the handle
s.stroke([(0.566, 0.34), (0.556, 0.62)], "flat", "n70", size=0.030,
         load=1.0, load_falloff=0.15, pressure="even", opacity=0.8)
s.stroke([(0.340, 0.60), (0.336, 0.34)], "flat", "n60", size=0.022,
         load=1.0, load_falloff=0.15, pressure="even", opacity=0.7)
print("mug re-state:", s.stroke_count - n0)

s.dab(0.582, 0.205, "round_hard", T(M("yellow_ochre", "burnt_umber", 0.45), 0.30),
      size=0.020)
s.dab(0.589, 0.213, "round_hard", T(M("yellow_ochre", "burnt_umber", 0.45), 0.42),
      size=0.014)

print(s.look(region=span("C1", "F4"), reference=REF))
print("total strokes:", s.stroke_count)
