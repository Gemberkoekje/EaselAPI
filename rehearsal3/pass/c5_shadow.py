# c5 - the cast shadow, driven stroke by stroke (it has a silhouette, so no
# block_in), plus wood grain to break up the block-in rectangles from c4.
# Shadow values read off the C5:G8 compare (ref = 0.42 - delta):
#   deep core  x 0.375-0.56, y 0.68-0.78   ref 0.11-0.20  -> floor 0.23
#   left lobe  x 0.31-0.375, y 0.65-0.75   ref 0.16-0.19
#   outer edge y 0.80-0.85                 ref 0.41-0.46
#   handle's own shadow ring, x 0.60-0.71  ref 0.42-0.46
REF = r"C:\temp\Level1.jpg"
p = s.palette


def at_value(base, target):
    lo, hi = 0.0, 1.0
    if p.value_of(base) > target:
        for _ in range(26):
            mid = (lo + hi) / 2
            if p.value_of(p.shade(base, mid)) > target:
                lo = mid
            else:
                hi = mid
        return p.shade(base, (lo + hi) / 2)
    for _ in range(26):
        mid = (lo + hi) / 2
        if p.value_of(p.tint(base, mid)) < target:
            lo = mid
        else:
            hi = mid
    return p.tint(base, (lo + hi) / 2)


def edge(knots):
    def at(x):
        if x <= knots[0][0]:
            return knots[0][1]
        for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return knots[-1][1]
    return at


sh_base = p.desaturate(p.mix("burnt_umber", "ultramarine", 0.32), 0.42)
p["sh_core"] = at_value(sh_base, 0.225)
p["sh_mid"] = at_value(sh_base, 0.30)
p["sh_out"] = at_value(sh_base, 0.40)
p["grain_d"] = at_value(p.desaturate(p.mix("yellow_ochre", "burnt_umber", 0.6), 0.3), 0.36)
p["grain_l"] = at_value(p.desaturate(p.mix("yellow_ochre", "burnt_umber", 0.3), 0.3), 0.60)
for n in ("sh_core", "sh_mid", "sh_out", "grain_d", "grain_l"):
    print(f"{n:8s} {p.hex(p[n])} {p.value_of(p[n]):.3f}")

top = edge([(0.305, 0.662), (0.322, 0.596), (0.342, 0.572), (0.356, 0.640),
            (0.420, 0.658), (0.500, 0.664), (0.578, 0.641), (0.620, 0.621),
            (0.664, 0.610), (0.700, 0.612)])
bot = edge([(0.305, 0.720), (0.316, 0.762), (0.336, 0.793), (0.400, 0.828),
            (0.455, 0.845), (0.545, 0.831), (0.616, 0.764), (0.668, 0.690),
            (0.700, 0.616)])

n0 = s.stroke_count
x = 0.310
while x < 0.700:
    t, b = top(x), bot(x)
    if b - t > 0.012:
        # darkest in the middle of the blob, opening out to the fringe
        f = min(1.0, abs(x - 0.44) / 0.26)
        col = "sh_mid" if f < 0.55 else "sh_out"
        s.stroke([(x, t - 0.008), (x, b + 0.010)], "bristle", col,
                 size=0.085 + 0.03 * (1 - f), load=1.0, pressure="swell")
    x += 0.029
print("shadow pass A:", s.stroke_count - n0)

# the deep core, a second pass running the other way so the dry ends do not line up
y = 0.672
while y < 0.792:
    s.stroke([(0.575, y), (0.340, y + 0.012)], "bristle", "sh_core",
             size=0.055, load=1.0, pressure="lift_off", load_falloff=0.3)
    y += 0.024
# a little of the core up against the mug's foot on the left
s.stroke([(0.352, 0.590), (0.336, 0.700)], "bristle", "sh_core", size=0.05,
         load=1.0, pressure="even")
print("shadow core:", s.stroke_count - n0)

# handle's own shadow - a faint ring, only two values off the table
s.stroke([(0.600, 0.548), (0.650, 0.534), (0.702, 0.558)], "bristle", "sh_out",
         size=0.035, load=0.85, pressure="swell", opacity=0.7)
s.stroke([(0.604, 0.586), (0.652, 0.600), (0.700, 0.576)], "bristle", "sh_out",
         size=0.032, load=0.8, pressure="swell", opacity=0.6)

# lose the shadow's outer edge in two places, keep it found near the mug's foot
s.smudge([(0.350, 0.812), (0.470, 0.856), (0.560, 0.840)], size=0.055)
s.smudge([(0.612, 0.776), (0.672, 0.700)], size=0.05)

# wood grain: several short overlapping passes, different loads and sizes,
# leaving places untouched (NOT one pass edge to edge)
grain = [((0.02, 0.58), (0.38, 0.30), 0.012, 0.45, "grain_d"),
         ((0.00, 0.86), (0.30, 0.62), 0.010, 0.40, "grain_d"),
         ((0.10, 0.20), (0.44, -0.02), 0.014, 0.5, "grain_l"),
         ((0.52, 0.10), (0.90, -0.10), 0.011, 0.45, "grain_l"),
         ((0.62, 0.30), (1.00, 0.06), 0.009, 0.40, "grain_d"),
         ((0.58, 0.98), (1.00, 0.70), 0.013, 0.5, "grain_l"),
         ((0.70, 0.86), (1.02, 0.62), 0.008, 0.42, "grain_d"),
         ((0.24, 0.99), (0.56, 0.80), 0.010, 0.45, "grain_l"),
         ((0.76, 0.46), (1.02, 0.30), 0.009, 0.38, "grain_d")]
for a, b_, sz, ld, col in grain:
    s.stroke([a, b_], "bristle", col, size=sz, load=ld, pressure="taper",
             opacity=0.55, load_falloff=0.2)

# break the two worst block-in steps
s.smudge([(0.625, 0.06), (0.625, 0.40)], size=0.07)
s.smudge([(0.625, 0.72), (0.625, 0.98)], size=0.07)
s.smudge([(0.752, 0.10), (0.752, 0.55)], size=0.06)
s.smudge([(0.33, 0.876), (0.62, 0.876)], size=0.06)

print("strokes:", s.stroke_count)
print(s.look(reference=REF))
