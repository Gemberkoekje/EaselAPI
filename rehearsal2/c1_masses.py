R = r"C:\temp\AntonConspiracy.jpg"
p = s.palette
p["dark"]     = p.mix("ultramarine", "burnt_umber", 0.55)
p["coat_wm"]  = p.mix(p["dark"], "burnt_sienna", 0.12)
p["ceiling"]  = p.mix("burnt_umber", "yellow_ochre", 0.3)
p["wall_mid"] = p.tint(p.mix("yellow_ochre", "burnt_umber", 0.5), 0.3)
p["wall_lt"]  = p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.2), 0.6)
p["wall_pale"]= p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.2), 0.78)
p["hair"]     = p.mix("burnt_umber", "yellow_ochre", 0.45)
p["hair_lt"]  = p.tint(p["hair"], 0.35)
p["flesh"]    = p.tint(p.mix("burnt_sienna", "yellow_ochre", 0.5), 0.55)
p["flesh_sh"] = p.tint(p.mix("burnt_sienna", "burnt_umber", 0.4), 0.2)
p["flesh_lt"] = p.tint(p.mix("burnt_sienna", "yellow_ochre", 0.5), 0.75)
p["orange"]   = p.mix("cadmium_yellow", "cadmium_red", 0.35)
p["table"]    = p.tint("yellow_ochre", 0.55)
p["red"]      = p.mix("cadmium_red", "alizarin", 0.4)
p["glass"]    = p.desaturate(p.tint("cerulean", 0.6), 0.5)

def cells(a, b=None):
    """Bounding box of a span of grid cells, e.g. cells('E5', 'H8')."""
    b = b or a
    return Region((ord(a[0]) - 65) / 8, (int(a[1:]) - 1) / 8,
                  (ord(b[0]) - 64) / 8, int(b[1:]) / 8)

def edge(knots):
    def at(x):
        for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return knots[-1][1]
    return at

# --- 1. background: mid on the left, light on the right, dark ceiling top-left
s.block_in(cells("A1", "D3"), "bristle", "wall_mid", direction="horizontal", density=1.0, size=0.18)
s.block_in(cells("E1", "H3"), "bristle", "wall_lt", direction="horizontal", density=1.0, size=0.18)
s.block_in(cells("A1", "B2"), "bristle", "ceiling", direction="horizontal", density=0.9, size=0.14)
s.block_in(cells("A4", "C4"), "bristle", "wall_mid", direction="horizontal", density=1.0, size=0.12)
s.block_in(cells("F4", "H5"), "bristle", "wall_mid", direction="horizontal", density=1.0, size=0.14)
s.dry()

# --- 2. the coat, as a silhouette: sweep down from where its top edge actually is
top = edge([(0.28, 0.63), (0.34, 0.66), (0.40, 0.62), (0.47, 0.57), (0.52, 0.60),
            (0.57, 0.57), (0.63, 0.48), (0.72, 0.44), (0.80, 0.50), (0.86, 0.60),
            (0.90, 0.72), (0.93, 1.02)])
x = 0.305
while x < 0.93:
    s.stroke([(x, top(x)), (x, 1.02)], "bristle", "coat_wm", size=0.13, load=1.0,
             pressure="lift_off")
    x += 0.033
# cross it: one stroke along the top edge itself, and a few across the mass
s.stroke([(0.30, 0.64), (0.40, 0.62), (0.47, 0.575), (0.57, 0.575), (0.63, 0.49),
          (0.72, 0.45), (0.80, 0.505), (0.86, 0.60), (0.90, 0.73)],
         "bristle", "coat_wm", size=0.09, load=1.0, pressure="even")
for y in (0.72, 0.82, 0.92):
    s.stroke([(0.31, y), (0.60, y + 0.02), (0.91, y)], "bristle", "coat_wm", size=0.14,
             load=1.0, pressure="even")

# --- 3. the figures on the left: dark body A5-B8, cap B3, beret C3, face B3-B4 in shadow
s.block_in(cells("A5", "B8"), "bristle", "dark", direction="vertical", density=1.0, size=0.14)
s.stroke([(0.13, 0.31), (0.25, 0.30)], "bristle", "dark", size=0.08, pressure="even")
s.stroke([(0.22, 0.32), (0.40, 0.31)], "bristle", "dark", size=0.12, pressure="even")
s.stroke([(0.24, 0.38), (0.38, 0.37)], "bristle", "dark", size=0.06, pressure="even")
s.stroke([(0.15, 0.36), (0.16, 0.48)], "bristle", "flesh_sh", size=0.07, pressure="even")
s.stroke([(0.21, 0.36), (0.22, 0.47)], "bristle", "flesh_sh", size=0.06, pressure="even")
s.dry()

# --- 4. the head: face first, then the hair over its back edge
s.stroke([(0.445, 0.26), (0.44, 0.40), (0.455, 0.52)], "bristle", "flesh", size=0.06, load=1.0, pressure="even")
s.stroke([(0.475, 0.24), (0.47, 0.40), (0.475, 0.57)], "bristle", "flesh", size=0.06, load=1.0, pressure="even")
s.stroke([(0.505, 0.30), (0.50, 0.44), (0.50, 0.56)], "bristle", "flesh", size=0.06, load=1.0, pressure="even")
for y, x0, x1 in ((0.06, 0.47, 0.62), (0.12, 0.44, 0.68), (0.20, 0.43, 0.71),
                  (0.28, 0.46, 0.73), (0.36, 0.53, 0.72), (0.42, 0.59, 0.70)):
    s.stroke([(x0, y), (x1, y)], "bristle", "hair", size=0.10, load=1.0, pressure="even")

# --- 5. the hand and glove, the carton, the table, the red shirt and bag
s.block_in(Region(0.19, 0.37, 0.37, 0.52), "bristle", "flesh", direction="vertical", density=1.0, size=0.06)
s.block_in(Region(0.20, 0.50, 0.375, 0.64), "bristle", "dark", direction="horizontal", density=1.0, size=0.07)
s.block_in(Region(0.155, 0.745, 0.305, 1.0), "flat", "orange", direction="vertical", density=1.0, size=0.08)
s.block_in(Region(0.77, 0.62, 1.0, 0.75), "bristle", "table", direction="horizontal", density=1.0, size=0.08)
s.block_in(Region(0.83, 0.44, 1.0, 0.62), "bristle", "red", direction="horizontal", density=0.9, size=0.08)
s.block_in(Region(0.90, 0.80, 1.0, 1.0), "bristle", "red", direction="vertical", density=0.9, size=0.08)
s.stroke([(0.79, 0.36), (0.79, 0.46)], "bristle", "flesh_sh", size=0.06, pressure="even")
s.stroke([(0.77, 0.34), (0.85, 0.33)], "bristle", "dark", size=0.05, pressure="even")

print("strokes:", s.stroke_count)
print(s.look(reference=R, grid=True))
print(s.look(reference=R, values=True))
