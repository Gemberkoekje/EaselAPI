p = s.palette
p["far2"]   = p.tint(p.mix("ultramarine", "alizarin", 0.35), 0.48)
p["far3"]   = p.tint(p["far2"], 0.25)
p["water2"] = p.mix(p["sky"], p["water"], 0.35)
p["path"]   = p.mix(p["water2"], p["glow"], 0.65)
p["shine"]  = p.mix(p["mud_lt"], p["sky_warm"], 0.55)
p["spit"]   = p.mix("ultramarine", "burnt_umber", 0.55)
for n in ("far2", "far3", "water2", "path", "shine", "spit"):
    print(f"{n:8s} {p.hex(p[n])} {p.value_of(p[n]):.2f}")

# --- (a) sky again, from the right so the run-out lands where it is already solid
for y, col in ((0.05, "sky_hi"), (0.16, "sky"), (0.28, "sky"), (0.38, "sky")):
    s.stroke([(1.02, y), (0.5, y + 0.01), (-0.02, y)], "flat", col, size=0.17, load=1.0, load_falloff=0.25, pressure="even")
for y in (0.44, 0.50):
    s.stroke([(1.02, y), (0.5, y - 0.005), (-0.02, y)], "bristle", "sky_warm", size=0.11, load=1.0, load_falloff=0.25, pressure="even")
s.stroke([(0.15, 0.545), (0.5, 0.53), (0.85, 0.545)], "round_soft", "glow", size=0.07, opacity=0.85, pressure="swell")
s.stroke([(0.35, 0.56), (0.62, 0.555)], "round_soft", "glow", size=0.04, opacity=0.9, pressure="swell")
s.dry()

# --- (b) the far headland, lighter and bluer, laid along the ridge rather than across it
ridge = [(-0.02, 0.415), (0.12, 0.375), (0.24, 0.405), (0.38, 0.465), (0.52, 0.525), (0.60, 0.565)]
s.stroke(ridge, "round_soft", "far2", size=0.09, load=1.0, load_falloff=0.2, pressure="even")
s.stroke([(-0.02, 0.47), (0.15, 0.44), (0.30, 0.48), (0.45, 0.54), (0.58, 0.58)], "round_soft", "far2", size=0.10, load=1.0, load_falloff=0.2, pressure="even")
s.stroke([(-0.02, 0.53), (0.20, 0.52), (0.40, 0.56), (0.55, 0.59)], "round_soft", "far2", size=0.09, load=1.0, load_falloff=0.2, pressure="even")
s.stroke([(0.02, 0.40), (0.12, 0.385), (0.22, 0.41)], "round_soft", "far3", size=0.04, opacity=0.6, pressure="taper")
s.smudge([(0.24, 0.40), (0.40, 0.47)], size=0.05)
s.smudge([(0.48, 0.50), (0.60, 0.56)], size=0.05)
s.dry()

# --- (c) water as a reflection of the sky; the near spit; the path of light
s.block_in(Region(0.0, 0.60, 1.0, 0.71), "flat", "water2", direction="horizontal", density=1.0, size=0.06, load_falloff=0.3)
s.stroke([(0.60, 0.575), (0.72, 0.555), (0.84, 0.545), (0.94, 0.555), (1.02, 0.57)], "round_hard", "spit", size=0.03, pressure="even")
s.stroke([(0.62, 0.59), (0.80, 0.58), (1.02, 0.59)], "flat", "spit", size=0.035, pressure="even")
s.dry(0.6)
s.stroke([(0.52, 0.59), (0.50, 0.65), (0.47, 0.72)], "round_soft", "path", size=0.08, pressure="press_in")
s.stroke([(0.555, 0.59), (0.545, 0.66), (0.53, 0.72)], "round_soft", "path", size=0.05, opacity=0.8, pressure="press_in")
s.stroke([(0.40, 0.625), (0.62, 0.62)], "bristle", "path", size=0.015, load=0.6, pressure="taper")
s.stroke([(0.10, 0.655), (0.30, 0.65)], "bristle", "sky_warm", size=0.012, load=0.5, pressure="taper")
s.stroke([(0.70, 0.66), (0.92, 0.665)], "bristle", "sky_warm", size=0.012, load=0.5, pressure="taper")
s.dry()

# --- (d) the wet shine where the water meets the mud; darker mud low down
s.stroke([(-0.02, 0.735), (0.5, 0.725), (1.02, 0.735)], "flat", "shine", size=0.05, load=1.0, load_falloff=0.3, pressure="even")
s.stroke([(0.30, 0.755), (0.70, 0.75)], "bristle", "shine", size=0.03, load=0.6, pressure="taper")
s.stroke([(-0.02, 0.86), (0.4, 0.88), (0.7, 0.85)], "bristle", "mud", size=0.10, load=0.9, load_falloff=0.3, pressure="even")
s.stroke([(0.0, 0.95), (0.5, 0.97), (1.02, 0.94)], "bristle", "mud_dk", size=0.11, load=0.9, load_falloff=0.3, pressure="even")
s.stroke([(0.55, 0.80), (0.95, 0.79)], "bristle", "mud_lt", size=0.04, load=0.5, pressure="taper")

# --- (e) posts, at different heights, and their broken reflections
for x, y0, y1, size in ((0.30, 0.655, 0.775, 0.014), (0.345, 0.672, 0.78, 0.011),
                        (0.63, 0.66, 0.79, 0.016), (0.71, 0.685, 0.80, 0.012)):
    s.stroke([(x, y0), (x, y1)], "round_hard", "post", size=size, pressure="even")
    s.stroke([(x, y1 + 0.005), (x + 0.004, y1 + 0.05)], "round_soft", "post", size=size * 0.9, opacity=0.35, pressure="lift_off")

print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
