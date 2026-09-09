p = s.palette
p["far4"] = p.tint(p.desaturate(p.mix("ultramarine", "alizarin", 0.35), 0.55), 0.40)
p["far5"] = p.tint(p["far4"], 0.3)
for n in ("far4", "far5"):
    print(f"{n:6s} {p.hex(p[n])} {p.value_of(p[n]):.2f}")

# --- (a) the far headland, painted along the ridge with flat and bristle, greyed for distance
for pts, size in (([(-0.02, 0.415), (0.12, 0.375), (0.24, 0.405), (0.38, 0.465), (0.52, 0.525), (0.60, 0.565)], 0.085),
                  ([(-0.02, 0.475), (0.15, 0.445), (0.30, 0.485), (0.45, 0.545), (0.58, 0.585)], 0.10),
                  ([(-0.02, 0.535), (0.20, 0.525), (0.40, 0.565), (0.56, 0.595)], 0.09)):
    s.stroke(pts, "flat", "far4", size=size, load=1.0, load_falloff=0.3, pressure="even")
s.stroke([(0.60, 0.585), (0.35, 0.49), (0.10, 0.40)], "bristle", "far4", size=0.06, load=0.9, load_falloff=0.3, pressure="even")
s.stroke([(0.0, 0.40), (0.12, 0.372), (0.26, 0.41), (0.40, 0.47)], "bristle", "far5", size=0.03, load=0.55, pressure="taper")
s.smudge([(0.20, 0.395), (0.34, 0.44)], size=0.045)
s.smudge([(0.44, 0.49), (0.56, 0.545)], size=0.045)
s.smudge([(0.58, 0.57), (0.63, 0.59)], size=0.04)
s.dry()

# --- (b) the spit: a ragged top, a reflection under it, its bottom edge lost
s.stroke([(0.60, 0.578), (0.66, 0.562), (0.72, 0.553), (0.79, 0.549), (0.86, 0.545), (0.93, 0.552), (1.02, 0.565)],
         "bristle", "spit", size=0.025, load=0.9, pressure="even")
s.stroke([(0.63, 0.605), (0.80, 0.60), (1.02, 0.61)], "bristle", "spit", size=0.02, load=0.5, pressure="taper")
s.stroke([(0.66, 0.625), (0.85, 0.622), (1.0, 0.63)], "bristle", "spit", size=0.015, load=0.4, pressure="taper")
s.smudge([(0.62, 0.60), (0.80, 0.60), (1.0, 0.605)], size=0.03)

# --- (c) water: ripples across the light, the shine knocked back to glints
s.stroke([(-0.02, 0.715), (0.5, 0.71), (1.02, 0.715)], "flat", "water2", size=0.035, load=1.0, load_falloff=0.3, pressure="even", opacity=0.8)
s.stroke([(0.02, 0.735), (0.5, 0.735), (0.98, 0.74)], "bristle", "water2", size=0.03, load=0.6, pressure="taper", opacity=0.7)
for y, x0, x1, col in ((0.605, 0.40, 0.66, "path"), (0.63, 0.36, 0.68, "water2"), (0.65, 0.42, 0.62, "path"),
                       (0.675, 0.30, 0.70, "water2"), (0.69, 0.44, 0.58, "path")):
    s.stroke([(x0, y), (x1, y)], "bristle", col, size=0.014, load=0.55, pressure="taper")
s.stroke([(0.15, 0.745), (0.45, 0.742)], "bristle", "shine", size=0.012, load=0.5, pressure="taper")
s.stroke([(0.58, 0.75), (0.86, 0.748)], "bristle", "shine", size=0.012, load=0.45, pressure="taper")

# --- (d) mud: quieten the loudest speckle, one tide channel leading in
s.stroke([(0.55, 0.83), (0.80, 0.84)], "bristle", "mud", size=0.07, load=0.85, load_falloff=0.3, pressure="even")
s.stroke([(0.60, 0.93), (0.98, 0.91)], "bristle", "mud", size=0.07, load=0.85, load_falloff=0.3, pressure="even")
s.stroke([(0.53, 0.77), (0.62, 0.83), (0.76, 0.90), (0.96, 1.0)], "round_hard", "mud_dk", size=0.03, load=0.8, pressure="press_in")
s.stroke([(0.57, 0.80), (0.68, 0.86), (0.80, 0.93)], "round_hard", "shine", size=0.008, load=0.5, pressure="taper")

# --- (e) sky softened where the striations show; the brightest glow last
s.smudge([(0.20, 0.43), (0.80, 0.43)], size=0.05)
s.dab(0.50, 0.553, "round_soft", "glow", size=0.04)
s.dab(0.485, 0.60, "round_hard", "glow", size=0.008)
s.dab(0.53, 0.635, "round_hard", "glow", size=0.007)

print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
