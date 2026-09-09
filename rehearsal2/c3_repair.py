R = r"C:\temp\AntonConspiracy.jpg"
p = s.palette
p["door2"]     = p.desaturate(p.tint(p.mix("yellow_ochre", "burnt_umber", 0.35), 0.5), 0.45)
p["flesh_mid"] = p.mix(p["flesh"], p["flesh_sh"], 0.5)
p["cheek"]     = p.mix(p["flesh_lt"], "cadmium_red", 0.08)
for n in ("door2", "flesh_mid", "cheek"):
    print(f"{n:9s} {p.hex(p[n])} {p.value_of(p[n]):.2f}")

# --- (a) the doorway, no longer green; the post beside it
s.block_in(Region(0.262, 0.0, 0.40, 0.24), "flat", "door2", direction="vertical", density=1.0, size=0.06)
s.stroke([(0.252, 0.0), (0.254, 0.25)], "round_hard", "ceiling", size=0.018, pressure="even")
s.dry()

# --- (b) the hair: back to its mass value, following its direction; few lights, at the crown only
for pts, size, col in (
    ([(0.44, 0.22), (0.46, 0.12), (0.52, 0.05), (0.60, 0.03), (0.67, 0.07), (0.72, 0.16)], 0.07, "hair"),
    ([(0.46, 0.20), (0.52, 0.12), (0.60, 0.10), (0.68, 0.15), (0.73, 0.26)], 0.07, "hair"),
    ([(0.50, 0.25), (0.57, 0.19), (0.65, 0.22), (0.71, 0.33), (0.70, 0.42)], 0.07, "hair"),
    ([(0.53, 0.30), (0.60, 0.28), (0.66, 0.34), (0.68, 0.44)], 0.06, "hair"),
    ([(0.55, 0.38), (0.62, 0.40), (0.66, 0.47)], 0.05, "hair"),
    ([(0.49, 0.14), (0.55, 0.08), (0.62, 0.07), (0.68, 0.11)], 0.035, "hair_lt"),
    ([(0.53, 0.20), (0.60, 0.16), (0.67, 0.20)], 0.03, "hair_lt"),
    ([(0.64, 0.28), (0.69, 0.36)], 0.025, "hair_lt"),
    ([(0.54, 0.09), (0.60, 0.06)], 0.015, "hair_hi"),
):
    s.stroke(pts, "bristle", col, size=size, load=1.0, pressure="taper")
s.dry()

# --- (c) the face: cover the false eye, carve the profile from outside, nose, cheek, beard
s.stroke([(0.445, 0.40), (0.45, 0.47)], "bristle", "flesh", size=0.04, load=1.0, pressure="even")
s.stroke([(0.38, 0.40), (0.415, 0.415), (0.42, 0.44), (0.425, 0.47), (0.42, 0.50)], "round_hard", "wall_mid2", size=0.025, pressure="even")
s.stroke([(0.38, 0.52), (0.44, 0.54), (0.45, 0.58)], "round_hard", "wall_mid2", size=0.03, pressure="even")
s.stroke([(0.39, 0.26), (0.415, 0.27), (0.412, 0.31), (0.405, 0.34)], "round_hard", "wall_mid2", size=0.02, pressure="even")
s.stroke([(0.415, 0.355), (0.408, 0.385), (0.425, 0.395)], "round_hard", "flesh", size=0.022, pressure="even")
s.dab(0.412, 0.375, "round_soft", "cheek", size=0.018)
s.stroke([(0.47, 0.30), (0.485, 0.36), (0.48, 0.41)], "round_soft", "cheek", size=0.035, opacity=0.6)
s.stroke([(0.435, 0.435), (0.455, 0.44)], "round_hard", "beard", size=0.012, pressure="even")
s.stroke([(0.44, 0.48), (0.46, 0.545), (0.50, 0.565), (0.53, 0.55)], "bristle", "beard", size=0.035, load=1.0, pressure="even")
s.stroke([(0.505, 0.48), (0.52, 0.52)], "bristle", "beard", size=0.03, load=1.0, pressure="even")
s.dry()

# --- (d) the fingers again, with variety; the beret's curve; the left man's head
s.block_in(Region(0.185, 0.36, 0.34, 0.49), "bristle", "wall_mid2", direction="vertical", density=1.0, size=0.05)
s.block_in(Region(0.30, 0.40, 0.375, 0.50), "bristle", "red_hair", direction="vertical", density=1.0, size=0.04)
for x0, y0, x1, y1, size, col in ((0.205, 0.475, 0.19, 0.405, 0.024, "flesh"),
                                  (0.232, 0.47, 0.222, 0.372, 0.027, "flesh_lt"),
                                  (0.262, 0.465, 0.255, 0.36, 0.028, "flesh"),
                                  (0.291, 0.47, 0.287, 0.37, 0.025, "flesh_lt"),
                                  (0.318, 0.48, 0.316, 0.40, 0.022, "flesh"),
                                  (0.345, 0.50, 0.342, 0.435, 0.02, "flesh_mid")):
    s.stroke([(x0, y0), (x1, y1)], "round_hard", col, size=size, pressure="lift_off")
s.stroke([(0.20, 0.49), (0.34, 0.50)], "bristle", "flesh_mid", size=0.035, pressure="even")
s.stroke([(0.23, 0.33), (0.27, 0.265), (0.33, 0.25), (0.385, 0.28), (0.40, 0.36)], "bristle", "dark", size=0.045, load=1.0, pressure="even")
s.block_in(Region(0.24, 0.29, 0.39, 0.385), "bristle", "dark", direction="horizontal", density=1.0, size=0.05)
s.stroke([(0.12, 0.30), (0.25, 0.29)], "bristle", "dark", size=0.06, pressure="even")
s.stroke([(0.145, 0.35), (0.15, 0.46)], "bristle", "flesh_mid", size=0.05, load=1.0, pressure="even")
s.stroke([(0.20, 0.35), (0.215, 0.46)], "bristle", "flesh_sh", size=0.05, load=1.0, pressure="even")
s.stroke([(0.15, 0.46), (0.23, 0.47)], "bristle", "beard", size=0.035, pressure="even")

print("strokes:", s.stroke_count)
print(s.look(reference=R, grid=True))
print(s.look(reference=R, values=True))
