# Pass 7: the dark figure. A silhouette walked with strokes, not a block_in box.
REF = "C:/temp/Level3.jpg"
p = s.palette
p["coat"]     = p.shade(p.mix("ultramarine", "burnt_umber", 0.62), 0.55)
p["coat_lit"] = p.mix(p.mix("ultramarine", "burnt_umber", 0.55), "titanium_white", 0.13)
p["bg_dark"]  = p.mix(p.mix("burnt_umber", "ultramarine", 0.25), "titanium_white", 0.12)
p["bg_mid2"]  = p.desaturate(p.mix(p.mix("burnt_umber", "yellow_ochre", 0.40),
                                   "titanium_white", 0.18), 0.30)


def edge(knots):
    def at(x):
        for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return knots[-1][1]
    return at


top = edge([(0.26, 1.05), (0.34, 0.90), (0.40, 0.80), (0.46, 0.70), (0.50, 0.63),
            (0.545, 0.585), (0.60, 0.560), (0.635, 0.490), (0.68, 0.442),
            (0.74, 0.430), (0.78, 0.452), (0.82, 0.505), (0.86, 0.575),
            (0.89, 0.660), (0.92, 0.800), (0.95, 1.05)])

n0 = s.stroke_count
x = 0.275
i = 0
while x < 0.945:
    s.stroke([(x, top(x)), (x, 1.03)], "flat", "coat",
             size=0.13 + 0.02 * (i % 3), load=1.0, pressure="lift_off")
    x += 0.042
    i += 1
print("silhouette walk:", s.stroke_count - n0)

# second pass ALONG the edge so the boundary is not stringy
n0 = s.stroke_count
xs = [0.28, 0.38, 0.48, 0.57, 0.66, 0.75, 0.84]
for a, b in zip(xs, xs[1:]):
    s.stroke([(a, top(a) + 0.035), (b, top(b) + 0.035)], "bristle", "coat",
             size=0.10, load=0.95, pressure="swell")
print("edge pass:", s.stroke_count - n0)

# background darks the first pass left far too light
n0 = s.stroke_count
s.block_in(span("A1", "B2"), "flat", "bg_dark", density=1.0, size=0.11, overhang=0)
s.block_in(span("B3", "C6"), "flat", "bg_dark", density=0.95, size=0.11, overhang=0,
           direction="vertical")
s.block_in(span("E1", "F2"), "flat", "bg_dark", density=0.9, size=0.10, overhang=0,
           direction="horizontal")
s.block_in(span("G3", "H5"), "flat", "bg_mid2", density=0.9, size=0.11, overhang=0,
           direction="diagonal")
s.block_in(span("H8", "H8"), "flat", "bg_dark", density=0.9, size=0.09, overhang=0)
s.block_in(span("A6", "B8"), "flat", "bg_dark", density=0.85, size=0.11, overhang=0,
           direction="horizontal")
print("bg darks:", s.stroke_count - n0)

s.dry()
print("look:", s.look(reference=REF, grid=True))
print("vals:", s.look(reference=REF, values=True))
print(s.compare(REF))
print("TOTAL strokes:", s.stroke_count)
