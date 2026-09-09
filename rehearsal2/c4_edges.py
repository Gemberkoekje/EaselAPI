R = r"C:\temp\AntonConspiracy.jpg"
p = s.palette
p["coat_lt"]  = p.tint(p["coat_wm"], 0.14)
p["coat_lt2"] = p.tint(p["coat_wm"], 0.26)
for n in ("coat_lt", "coat_lt2"):
    print(f"{n:9s} {p.hex(p[n])} {p.value_of(p[n]):.2f}")

# --- (a) the last of the green; the fringe over the forehead
s.stroke([(0.258, 0.0), (0.27, 0.07)], "round_hard", "door2", size=0.03, pressure="even")
s.stroke([(0.405, 0.0), (0.415, 0.12)], "bristle", "wall_mid2", size=0.04, pressure="even")
s.stroke([(0.43, 0.10), (0.46, 0.07)], "bristle", "hair", size=0.035, load=1.0, pressure="even")
s.stroke([(0.415, 0.13), (0.43, 0.19), (0.445, 0.245)], "bristle", "hair", size=0.035, load=1.0, pressure="even")
s.stroke([(0.44, 0.15), (0.45, 0.22)], "bristle", "hair_lt", size=0.02, load=1.0, pressure="taper")

# --- (b) dark in front of the face, so the profile is found against it
s.block_in(Region(0.34, 0.39, 0.40, 0.60), "bristle", "dark", direction="vertical", density=1.0, size=0.035)
s.stroke([(0.40, 0.30), (0.398, 0.34), (0.39, 0.385), (0.413, 0.41), (0.42, 0.44), (0.43, 0.47),
          (0.435, 0.50), (0.445, 0.55), (0.455, 0.58)], "round_hard", "dark", size=0.02, pressure="even")
s.dab(0.408, 0.382, "round_hard", "flesh", size=0.02)
s.stroke([(0.43, 0.445), (0.45, 0.45)], "round_hard", "beard", size=0.01, pressure="even")
s.dry()

# --- (c) a little form in the coat, broken marks only
s.stroke([(0.64, 0.50), (0.74, 0.47), (0.82, 0.53)], "bristle", "coat_lt", size=0.05, load=0.6, pressure="taper")
s.stroke([(0.37, 0.70), (0.42, 0.80), (0.40, 0.92)], "bristle", "coat_lt", size=0.05, load=0.55, pressure="taper")
s.stroke([(0.84, 0.62), (0.88, 0.75), (0.90, 0.90)], "bristle", "coat_lt", size=0.05, load=0.5, pressure="taper")
s.stroke([(0.545, 0.63), (0.58, 0.55), (0.63, 0.50)], "round_hard", "coat_lt2", size=0.018, pressure="taper")
s.stroke([(0.62, 0.75), (0.70, 0.70), (0.78, 0.74)], "bristle", "coat_lt", size=0.045, load=0.5, pressure="taper")
s.stroke([(0.05, 0.55), (0.08, 0.70), (0.06, 0.85)], "bristle", "coat_lt", size=0.045, load=0.5, pressure="taper")

# --- (d) edges: lose the ones that should be lost
s.smudge([(0.70, 0.09), (0.735, 0.22), (0.73, 0.36)], size=0.05)
s.smudge([(0.02, 0.12), (0.22, 0.13)], size=0.07)
s.smudge([(0.30, 0.70), (0.30, 0.95)], size=0.06)
s.smudge([(0.10, 0.50), (0.23, 0.505)], size=0.05)
s.smudge([(0.66, 0.45), (0.70, 0.47)], size=0.035)
s.smudge([(0.76, 0.60), (0.76, 0.75)], size=0.04)

# --- (e) highlights and accents, few and deliberate
s.dab(0.67, 0.03, "round_soft", "titanium_white", size=0.035)
s.dab(0.41, 0.37, "round_hard", "flesh_lt", size=0.012)
s.dab(0.443, 0.27, "round_soft", "flesh_lt", size=0.018)
s.stroke([(0.78, 0.63), (1.0, 0.62)], "round_hard", "wall_pale", size=0.014, pressure="even")
for x in (0.05, 0.105):
    s.stroke([(x, 0.905), (x, 1.0)], "flat", "phone", size=0.028, pressure="even", opacity=0.7)
    s.stroke([(x - 0.022, 0.878), (x + 0.022, 0.878)], "round_hard", "wall_pale", size=0.006, pressure="even")
s.dab(0.452, 0.315, "round_hard", "beard", size=0.012)
s.stroke([(0.42, 0.30), (0.455, 0.295)], "round_hard", "hair", size=0.008, pressure="even")
s.stroke([(0.225, 0.755), (0.26, 0.755)], "round_hard", "titanium_white", size=0.018, pressure="even")

print("strokes:", s.stroke_count)
print(s.look(reference=R, grid=True))
print(s.look(reference=R, values=True))
