# Pass 27 — the last thirteen marks. Break the stripes the G1:H8 block_in left,
# strengthen the cast shadow, carry the spoon across the rim so it stops being a
# floating stub, lose three edges, and put on three highlights.
# Run: python -m easel run painting.easel c27_final.py
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
p["scum"] = at_value(WOOD, 0.44)
p["deep"] = S(M("ultramarine", "burnt_umber", 0.45), 1.0)
p["black"] = S(M("ultramarine", "burnt_umber", 0.55), 1.0)
p["hi"] = at_value(NEUT, 0.90)

s.dry()
n0 = s.stroke_count

# 1. three crossing scumbles over the striped right third
s.stroke([(0.735, 0.02), (1.005, 0.30)], "bristle", "scum", size=0.10,
         load=0.55, load_falloff=0.2, pressure="taper", opacity=0.45)
s.stroke([(1.005, 0.52), (0.730, 0.30)], "bristle", "scum", size=0.13,
         load=0.6, load_falloff=0.2, pressure="taper", opacity=0.40)
s.stroke([(0.740, 0.74), (1.005, 0.99)], "bristle", "scum", size=0.11,
         load=0.5, load_falloff=0.2, pressure="taper", opacity=0.45)

# 2. the cast shadow, stronger and reaching further
s.stroke([(0.300, 0.700), (0.420, 0.735), (0.520, 0.712)], "flat", "deep",
         size=0.070, load=1.0, load_falloff=0.1, pressure="even", opacity=0.75)
s.stroke([(0.500, 0.775), (0.380, 0.795), (0.310, 0.760)], "flat", "deep",
         size=0.048, load=1.0, load_falloff=0.1, pressure="even", opacity=0.6)
s.stroke([(0.560, 0.628), (0.470, 0.672), (0.350, 0.668)], "flat", "deep",
         size=0.040, load=1.0, load_falloff=0.1, pressure="even", opacity=0.7)

# 3. the spoon across the rim
s.stroke([(0.519, 0.070), (0.510, 0.130), (0.506, 0.180)], "flat", "black",
         size=0.021, load=1.0, pressure="even")

print("paint so far:", s.stroke_count - n0)

# 4. three lost edges
s.smudge([(0.300, 0.760), (0.330, 0.800)], size=0.07)
s.smudge([(0.336, 0.430), (0.342, 0.520)], size=0.045)
s.smudge([(0.545, 0.795), (0.500, 0.815)], size=0.06)

# 5. three highlights
s.dab(0.418, 0.310, "round_hard", "hi", size=0.012)
s.dab(0.352, 0.262, "round_hard", "hi", size=0.010)
s.dab(0.700, 0.318, "round_hard", "hi", size=0.009)

print(s.look(reference=REF))
print("total strokes:", s.stroke_count)
