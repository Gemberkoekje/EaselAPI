# Pass 22: compare says everything below row 5 is 0.15-0.20 too light. The first
# coat pass was long vertical strokes that ran dry; relay it in short bands with
# load_falloff=0. Also lighten the four cells that came out too DARK.
REF = "C:/temp/Level3.jpg"
p = s.palette
p["coat"]     = p.shade(p.mix("ultramarine", "burnt_umber", 0.62), 0.55)
p["coat_lit"] = p.mix(p.mix("ultramarine", "burnt_umber", 0.55), "titanium_white", 0.11)
p["zip"]      = p.desaturate(p.mix("cerulean", "burnt_umber", 0.35), 0.25)
p["bg_lit"]   = p.mix(p.mix("yellow_ochre", "burnt_sienna", 0.30), "titanium_white", 0.46)
p["bg_hi"]    = p.mix(p.mix("yellow_ochre", "burnt_sienna", 0.20), "titanium_white", 0.62)
p["hand_mid"] = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.44), "titanium_white", 0.50)
p["hand_shd"] = p.mix(p.mix("burnt_umber", "burnt_sienna", 0.40), "titanium_white", 0.16)
p["bghair2"]  = p.desaturate(
    p.mix(p.mix("burnt_sienna", "cadmium_red", 0.22), "titanium_white", 0.16), 0.40)
s.dry()

BANDS = [
    (0.470, 0.660, 0.790, "coat_lit", 0.075),
    (0.530, 0.630, 0.840, "coat",     0.085),
    (0.590, 0.575, 0.865, "coat",     0.085),
    (0.655, 0.490, 0.885, "coat_lit", 0.090),
    (0.720, 0.420, 0.900, "coat",     0.090),
    (0.790, 0.365, 0.910, "coat",     0.090),
    (0.860, 0.325, 0.920, "coat_lit", 0.090),
    (0.930, 0.305, 0.930, "coat",     0.090),
    (0.995, 0.295, 0.935, "coat",     0.090),
    (0.660, 0.225, 0.430, "coat",     0.075),
    (0.735, 0.265, 0.460, "coat",     0.070),
]
n0 = s.stroke_count
for i, (y, x0, x1, col, sz) in enumerate(BANDS):
    a, b = (x0, x1) if i % 2 == 0 else (x1, x0)
    s.stroke([(a, y), ((a + b) / 2.0, y + 0.004), (b, y)], "flat", col,
             size=sz, load=1.0, load_falloff=0.0, pressure="even")
print("coat bands:", s.stroke_count - n0)

n0 = s.stroke_count
s.stroke([(0.500, 0.605), (0.575, 0.590), (0.640, 0.548)], "bristle", "coat_lit",
         size=0.018, load=1.0, pressure="taper")               # collar
s.stroke([(0.600, 0.630), (0.640, 0.720), (0.660, 0.830)], "bristle", "coat_lit",
         size=0.016, load=0.9, pressure="lift_off")            # lapel
s.stroke([(0.520, 0.545), (0.560, 0.552)], "liner", "zip",
         size=0.009, load=1.0, pressure="even")                # the blue flash
s.stroke([(0.700, 0.480), (0.780, 0.512), (0.845, 0.575)], "bristle", "coat_lit",
         size=0.022, load=0.75, pressure="swell")              # shoulder
print("coat detail:", s.stroke_count - n0)

n0 = s.stroke_count
s.stroke([(0.030, 0.045), (0.160, 0.038), (0.290, 0.052)], "flat", "bg_lit",
         size=0.048, load=1.0, load_falloff=0.0, pressure="even")
s.stroke([(0.040, 0.130), (0.150, 0.122)], "bristle", "bg_lit",
         size=0.036, load=0.75, pressure="taper")
s.stroke([(0.150, 0.185), (0.235, 0.178)], "flat", "bg_lit",
         size=0.030, load=1.0, pressure="even")
s.stroke([(0.885, 0.300), (0.960, 0.312), (1.000, 0.330)], "flat", "bg_hi",
         size=0.048, load=1.0, load_falloff=0.0, pressure="even")
s.stroke([(0.640, 0.045), (0.720, 0.040)], "flat", "bg_lit",
         size=0.040, load=1.0, pressure="even")
print("bg lighten:", s.stroke_count - n0)

n0 = s.stroke_count
s.stroke([(0.228, 0.570), (0.288, 0.588), (0.345, 0.606)], "flat", "hand_mid",
         size=0.030, load=1.0, pressure="even")                # the palm
s.stroke([(0.232, 0.612), (0.300, 0.630), (0.352, 0.648)], "bristle", "hand_shd",
         size=0.018, load=0.9, pressure="taper")               # knuckle shadow
s.stroke([(0.300, 0.480), (0.328, 0.520), (0.352, 0.562)], "bristle", "bghair2",
         size=0.030, load=1.0, pressure="taper")               # kill the red slash
print("hand/bg:", s.stroke_count - n0)

print("whole:", s.look(reference=REF))
print("vals :", s.look(reference=REF, values=True))
print("TOTAL strokes:", s.stroke_count)
