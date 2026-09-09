# Unprompted. Planning the three values as numbers first, per the guide.
p = s.palette
p["deep"]  = p.mix("ultramarine", "burnt_umber", 0.42)                       # darkest
p["mid"]   = p.tint(p.mix("burnt_sienna", "ultramarine", 0.30), 0.34)
p["warm"]  = p.desaturate(p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.30), 0.52), 0.18)
p["pale"]  = p.tint(p.mix("yellow_ochre", "titanium_white", 0.55), 0.62)
p["cool"]  = p.desaturate(p.tint(p.mix("cerulean", "ultramarine", 0.35), 0.44), 0.35)
for n in ("deep", "mid", "warm", "pale", "cool"):
    print(f"  {n:<5} {p.hex(p[n])}  {p.value_of(p[n]):.2f}")


def edge(knots):
    def at(x):
        for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return knots[-1][1]
    return at


# 1. the light field, upper right, laid warm and solid
s.block_in(Region(0.30, 0.0, 1.0, 0.58), "bristle", "pale",
           density=0.8, size=0.20, direction="horizontal", load=1.0)
s.dry()
s.block_in(Region(0.52, 0.0, 1.0, 0.34), "bristle", "warm",
           density=0.55, size=0.16, direction="diagonal", load=0.85)
s.dry()

# 2. the dark mass: a silhouette climbing from the bottom left
ridge = edge([(-0.02, 0.44), (0.16, 0.36), (0.34, 0.52), (0.50, 0.46),
              (0.66, 0.66), (0.84, 0.60), (1.02, 0.74)])
x = -0.01
i = 0
while x < 1.01:
    s.stroke([(x, ridge(x)), (x + 0.01, (ridge(x) + 1.05) * 0.5), (x - 0.005, 1.05)],
             "bristle", "deep", size=0.115 + 0.02 * ((i % 3) - 1),
             load=0.95, pressure="lift_off")
    x += 0.030
    i += 1
# a second pass along the ridge, to close the combed edge
s.dry()
for x0, x1 in [(-0.02, 0.34), (0.30, 0.68), (0.62, 1.02)]:
    s.stroke([(x0, ridge(x0) + 0.018), ((x0 + x1) / 2, ridge((x0 + x1) / 2) + 0.022),
              (x1, ridge(x1) + 0.018)], "bristle", "deep",
             size=0.07, load=0.9, pressure="taper")

# 3. a cool mid band, cutting across, at a different width
s.dry()
for k, (y, w) in enumerate([(0.30, 0.075), (0.365, 0.045), (0.245, 0.030)]):
    s.stroke([(0.02, y + 0.05), (0.34, y - 0.02), (0.68, y + 0.015), (0.99, y - 0.04)],
             "bristle", "cool", size=w, load=0.85 - 0.15 * k, pressure="swell")

print("strokes:", s.stroke_count)
print(s.look())
