# Pass 11 — the block-ins left hard vertical stair-steps where the light band met
# the mid one. Cross them, and give the table its grain direction.
# Run: python -m easel run painting.easel c11_woodfix.py
REF = r"C:\temp\Level1.jpg"
p = s.palette
n0 = s.stroke_count

# one broad horizontal pass over the seams, half density, bigger brush
s.block_in(span("B1", "G8"), "flat", "wood_mid", density=0.45, size=0.22,
           direction="horizontal", opacity=0.55)
print("seam pass:", s.stroke_count - n0)

# grain: long shallow diagonals, varied size and load, both tones, alternating
# direction so the dry ends do not all land on the same side
grain = [
    ((0.02, 0.10), (0.62, 0.44), "wood_lit", 0.030, 0.55),
    ((0.98, 0.62), (0.30, 0.22), "wood_dim", 0.022, 0.50),
    ((0.02, 0.42), (0.55, 0.72), "wood_dim", 0.018, 0.45),
    ((0.99, 0.88), (0.36, 0.55), "wood_lit", 0.026, 0.60),
    ((0.05, 0.72), (0.70, 0.99), "wood_lit", 0.020, 0.50),
    ((0.96, 0.30), (0.52, 0.12), "wood_lit", 0.016, 0.55),
    ((0.10, 0.94), (0.92, 0.99), "wood_dim", 0.014, 0.45),
    ((0.99, 0.20), (0.60, 0.05), "wood_dim", 0.012, 0.40),
]
for a, b, col, sz, ld in grain:
    s.stroke([a, b], "bristle", col, size=sz, load=ld, load_falloff=0.2,
             pressure="taper", opacity=0.6)

# the dark corner beyond the table, top right
s.stroke([(0.86, 0.005), (1.005, 0.03)], "flat", "dark_bg", size=0.05,
         pressure="even", load=1.0)
s.stroke([(0.90, 0.0), (1.005, 0.005)], "flat", "dark_bg", size=0.05,
         pressure="even", load=1.0)
# the lit far edge of the table just under it
s.stroke([(0.855, 0.045), (1.005, 0.070)], "flat", "wood_lit", size=0.018,
         pressure="even", load=1.0)

print(s.look(reference=REF))
print("total strokes:", s.stroke_count)
