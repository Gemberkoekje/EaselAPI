REF = "C:/temp/Level1.jpg"

# --- the opening has to be a big dark mass, not a small one --------------
for pts, size in [([(0.558, 0.202), (0.590, 0.240), (0.586, 0.286)], 0.038),
                  ([(0.566, 0.300), (0.528, 0.314)], 0.028),
                  ([(0.392, 0.308), (0.452, 0.320), (0.492, 0.316)], 0.026),
                  ([(0.352, 0.198), (0.346, 0.240), (0.362, 0.282)], 0.030),
                  ([(0.398, 0.166), (0.468, 0.162), (0.528, 0.176)], 0.028)]:
    s.stroke(pts, "flat", "tea", size=size, pressure="even", load=1.0,
             note="the opening")
print("tea", s.stroke_count)

# --- a step under the lip so the light band is not a slab ----------------
s.stroke([(0.360, 0.372), (0.440, 0.396), (0.520, 0.392)], "flat", "mug_lit",
         size=0.030, pressure="swell", load=1.0, note="step under the lip")

# --- the visor went under the crossing strokes ---------------------------
s.stroke([(0.379, 0.458), (0.404, 0.449), (0.428, 0.445)], "round_hard",
         "mug_lit", size=0.019, pressure="swell", load=1.0, note="visor")
print("lip+visor", s.stroke_count)

# --- what is beyond the table, and the far corner falling away -----------
s.stroke([(0.928, 0.006), (0.998, 0.058)], "flat", "warm_dark", size=0.030,
         pressure="even", load=1.0, note="beyond the table")
s.stroke([(0.952, 0.004), (0.999, 0.030)], "flat", "warm_dark", size=0.022,
         pressure="even", load=1.0, note="beyond the table")
s.stroke([(0.752, 0.140), (0.878, 0.118)], "bristle", "wood_far", size=0.058,
         pressure="even", load=1.0, load_falloff=0.0, note="far table")
s.stroke([(0.874, 0.200), (0.756, 0.222)], "bristle", "wood_far", size=0.058,
         pressure="even", load=1.0, load_falloff=0.0, note="far table")
print("corner", s.stroke_count)

# --- the mug sits in its shadow, not on it -------------------------------
s.stroke([(0.386, 0.672), (0.462, 0.690), (0.536, 0.672)], "round_hard",
         "shad_pool", size=0.036, pressure="swell", load=1.0, note="under the base")
s.stroke([(0.404, 0.706), (0.500, 0.706)], "round_hard", "shad_pool",
         size=0.030, pressure="swell", load=1.0, note="under the base")
print("base", s.stroke_count)

# --- the teabag string ---------------------------------------------------
s.stroke([(0.646, 0.252), (0.700, 0.330), (0.760, 0.450), (0.806, 0.540)],
         "liner", "mug_hi", size=0.004, pressure="taper", load=1.0, note="string")
s.stroke([(0.622, 0.608), (0.690, 0.626), (0.760, 0.612)], "liner", "wood_mid",
         size=0.003, pressure="taper", load=1.0, note="string on the table")
print("string", s.stroke_count)

print(s.look(reference=REF))
print(s.look(reference=REF, values=True))
print(s.compare(REF))
