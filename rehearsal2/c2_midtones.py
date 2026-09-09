R = r"C:\temp\AntonConspiracy.jpg"
p = s.palette
p["door"]     = p.tint(p.mix("yellow_ochre", "cerulean", 0.3), 0.5)
p["wall_lt2"] = p.mix(p["wall_lt"], p["wall_pale"], 0.5)
p["wall_mid2"]= p.mix(p["wall_mid"], p["ceiling"], 0.35)
p["beard"]    = p.mix("burnt_umber", p["hair"], 0.4)
p["hair_hi"]  = p.tint(p["hair"], 0.55)
p["red_hair"] = p.mix("burnt_sienna", "cadmium_red", 0.3)
p["phone"]    = p.desaturate(p.tint(p["dark"], 0.35), 0.5)
p["label"]    = p.tint(p["orange"], 0.6)
p["panel"]    = p.desaturate(p.tint(p["wall_mid"], 0.25), 0.4)
for n in ("door", "wall_lt2", "wall_mid2", "beard", "hair_hi", "red_hair", "phone", "label", "panel"):
    print(f"{n:9s} {p.hex(p[n])} {p.value_of(p[n]):.2f}")

# --- (a) break the corduroy: a crossing pass on both walls, then the corrections
s.block_in(Region(0.55, 0.0, 1.0, 0.32), "flat", "wall_lt2", direction="diagonal", density=0.6, size=0.14)
s.block_in(Region(0.0, 0.0, 0.42, 0.33), "flat", "wall_mid2", direction="diagonal", density=0.6, size=0.14)
s.block_in(Region(0.255, 0.0, 0.405, 0.24), "flat", "door", direction="vertical", density=1.0, size=0.07)
s.stroke([(0.248, 0.0), (0.25, 0.25)], "round_hard", "ceiling", size=0.02, pressure="even")
s.stroke([(0.0, 0.04), (0.24, 0.05)], "bristle", "dark", size=0.07, pressure="even", load=0.8)
s.block_in(Region(0.0, 0.30, 0.09, 0.55), "flat", "panel", direction="vertical", density=1.0, size=0.05)
s.dab(0.67, 0.03, "round_soft", "wall_pale", size=0.06)
s.dry()

# --- (b) the head: hair lights sweeping back, then the profile, beard, moustache
for pts, size, col in (
    ([(0.45, 0.11), (0.55, 0.07), (0.66, 0.13), (0.72, 0.24)], 0.05, "hair_lt"),
    ([(0.46, 0.17), (0.56, 0.14), (0.67, 0.20), (0.71, 0.32)], 0.045, "hair_hi"),
    ([(0.50, 0.24), (0.58, 0.22), (0.66, 0.28), (0.69, 0.40)], 0.04, "hair_lt"),
    ([(0.54, 0.31), (0.62, 0.33), (0.67, 0.44)], 0.035, "hair_hi"),
    ([(0.44, 0.13), (0.47, 0.22)], 0.03, "hair"),
    ([(0.60, 0.42), (0.66, 0.46), (0.70, 0.44)], 0.04, "hair"),
):
    s.stroke(pts, "bristle", col, size=size, load=1.0, pressure="taper")
# the face, cut in against the profile
s.stroke([(0.455, 0.25), (0.44, 0.30), (0.432, 0.36), (0.435, 0.41)], "bristle", "flesh", size=0.045, load=1.0, pressure="even")
s.stroke([(0.49, 0.24), (0.48, 0.32), (0.475, 0.40), (0.47, 0.46)], "bristle", "flesh", size=0.06, load=1.0, pressure="even")
s.stroke([(0.52, 0.30), (0.515, 0.40), (0.51, 0.46)], "bristle", "flesh_sh", size=0.035, load=1.0, pressure="even")
s.dab(0.418, 0.38, "round_soft", "flesh_lt", size=0.03)
s.stroke([(0.44, 0.44), (0.46, 0.44)], "round_hard", "beard", size=0.02, pressure="even")
s.stroke([(0.445, 0.48), (0.465, 0.55), (0.49, 0.57)], "bristle", "beard", size=0.04, load=1.0, pressure="even")
s.stroke([(0.50, 0.47), (0.52, 0.53), (0.535, 0.56)], "bristle", "beard", size=0.035, load=1.0, pressure="even")
s.stroke([(0.40, 0.30), (0.405, 0.36)], "round_hard", "wall_mid", size=0.02, pressure="even")   # the space in front of the nose
s.dry()

# --- (c) the hand: background between the fingers, red hair behind, then five fingers, glove, wrist
s.block_in(Region(0.29, 0.40, 0.38, 0.50), "bristle", "red_hair", direction="vertical", density=1.0, size=0.04)
for x0, y0, x1, y1, size in ((0.205, 0.47, 0.20, 0.40, 0.025), (0.235, 0.47, 0.232, 0.37, 0.025),
                             (0.262, 0.47, 0.258, 0.36, 0.026), (0.292, 0.48, 0.29, 0.37, 0.025),
                             (0.322, 0.49, 0.32, 0.40, 0.024), (0.35, 0.50, 0.345, 0.43, 0.022)):
    s.stroke([(x0, y0), (x1, y1)], "round_hard", "flesh", size=size, pressure="lift_off")
for x in (0.22, 0.248, 0.276, 0.306):
    s.stroke([(x, 0.47), (x, 0.395)], "round_hard", "wall_mid2", size=0.008, pressure="even")
s.block_in(Region(0.20, 0.49, 0.375, 0.63), "bristle", "dark", direction="horizontal", density=1.0, size=0.06)
s.stroke([(0.30, 0.61), (0.375, 0.66)], "bristle", "dark", size=0.06, pressure="even")
s.dry()

# --- (d) carton label and cap, the phone, the glasses, the red bag's dark top
s.block_in(Region(0.22, 0.84, 0.305, 1.0), "flat", "label", direction="vertical", density=1.0, size=0.05)
s.stroke([(0.225, 0.76), (0.26, 0.76)], "round_hard", "titanium_white", size=0.03, pressure="even")
s.stroke([(0.60, 0.94), (0.78, 0.90)], "flat", "phone", size=0.08, pressure="even")
s.stroke([(0.68, 0.98), (0.79, 0.94)], "flat", "phone", size=0.05, pressure="even")
for x in (0.05, 0.105):
    s.stroke([(x, 0.88), (x, 1.0)], "flat", "glass", size=0.045, pressure="even", load=0.8)
s.block_in(Region(0.90, 0.76, 1.0, 0.86), "bristle", "dark", direction="horizontal", density=1.0, size=0.06)
s.stroke([(0.77, 0.46), (0.76, 0.62)], "bristle", "dark", size=0.06, pressure="even")   # dark between man and shirt

print("strokes:", s.stroke_count)
print(s.look(reference=R, grid=True))
print(s.look(reference=R, values=True))
