# Stage 1 -- the big masses, biggest brush, no detail.
# Values planned against value_of(): the palette bottoms out at 0.23, so the range
# to work in is 0.23 (coat) .. 0.96 (white), not 0..1.
p = s.palette
p["bg_warm"] = p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.35), 0.40)   # ~0.58
p["bg_dim"]  = p.tint(p.mix("burnt_umber", "yellow_ochre", 0.40), 0.15)    # ~0.35
p["coat"]    = p.mix("ultramarine", "burnt_umber", 0.55)                   # ~0.23
p["hair"]    = p.tint(p.mix("burnt_umber", "yellow_ochre", 0.50), 0.20)    # ~0.40
p["flesh"]   = p.tint(p.mix("burnt_sienna", "cadmium_red", 0.25), 0.80)    # ~0.71


def sweep(pairs):
    """Interpolate a boundary given as (x, y) knots -- y at any x between them."""
    def at(x):
        for (x0, y0), (x1, y1) in zip(pairs, pairs[1:]):
            if x0 <= x <= x1:
                t = (x - x0) / (x1 - x0)
                return y0 + t * (y1 - y0)
        return pairs[-1][1]
    return at


# 1. the whole field, warm and mid.  Ground still breathes through at 0.7.
s.block_in(Region(0.0, 0.0, 1.0, 1.0), "bristle", "bg_warm",
           density=0.7, size=0.22, direction="horizontal")
s.dry()

# 2. the dim half behind the figures, left and low
s.block_in(Region(0.0, 0.24, 0.44, 0.78), "bristle", "bg_dim",
           density=0.65, size=0.18, direction="diagonal")
s.dry()

# 3. THE COAT.  A silhouette, not a box: one long stroke per brush-width, each
#    starting where the shoulder actually is and running off the bottom edge.
coat_top = sweep([(0.33, 1.02), (0.40, 0.82), (0.46, 0.66), (0.52, 0.52),
                  (0.58, 0.43), (0.66, 0.44), (0.74, 0.50), (0.84, 0.57),
                  (0.94, 0.63), (1.02, 0.68)])
x = 0.345
i = 0
while x < 1.0:
    top = coat_top(x)
    if top < 1.0:
        wob = 0.012 * ((i % 3) - 1)
        s.stroke([(x + wob, top), (x + wob * 0.5, (top + 1.0) * 0.5), (x, 1.02)],
                 "bristle", "coat", size=0.13, pressure="press_in",
                 load=0.9, note="coat")
    x += 0.033
    i += 1
s.dry()

# 4. the head: hair mass, strokes following the way the hair falls
for i, (x0, y0, x1, y1) in enumerate([
        (0.455, 0.10, 0.53, 0.20), (0.44, 0.14, 0.52, 0.28),
        (0.47, 0.09, 0.60, 0.19), (0.52, 0.08, 0.64, 0.22),
        (0.57, 0.10, 0.67, 0.30), (0.60, 0.14, 0.68, 0.40),
        (0.56, 0.20, 0.66, 0.46), (0.50, 0.13, 0.58, 0.24)]):
    s.stroke([(x0, y0), ((x0 + x1) * 0.5 + 0.01, (y0 + y1) * 0.5), (x1, y1)],
             "bristle", "hair", size=0.10, pressure="taper", note="hair")
s.dry()

# 5. the light of the face -- the mass whose left edge is the profile
face_left = sweep([(0.22, 0.437), (0.28, 0.420), (0.33, 0.414), (0.36, 0.408),
                   (0.39, 0.425), (0.42, 0.432), (0.46, 0.443), (0.52, 0.462),
                   (0.57, 0.500)])
y = 0.235
while y < 0.56:
    lx = face_left(y)
    s.stroke([(lx, y), (lx + 0.07, y + 0.005), (lx + 0.135, y - 0.004)],
             "bristle", "flesh", size=0.055, pressure="lift_off",
             load=0.8, note="face")
    y += 0.035

print("strokes:", s.stroke_count)
print(s.look())
