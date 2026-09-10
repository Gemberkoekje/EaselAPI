"""Pass B2/E2 - tame the shadow (it was a black starburst), then the mug with
the shape inset by half a brush so the spill lands ON the silhouette."""
p = s.palette
s.dry()

# --- the table, back over the shadow's overreach -------------------------
s.block_in(ellipse(Region(0.24, 0.775, 0.76, 1.06)), "flat", "table_lit",
           direction=(-6,), density=1.0, size=0.10, load=1.0)
s.block_in(ellipse(Region(0.16, 0.72, 0.40, 0.98)), "flat",
           p.mix(p["table_base"], p["table_lit"], 0.4), direction=(-72,),
           density=1.0, size=0.09, load=1.0)
print("table back:", s.stroke_count)

# --- the shadow again, quieter and with a round edge --------------------
p["shad_pen"] = p.mix(p["shad_core"], p["table_base"], 0.52)
print("shad_pen", p.hex(p["shad_pen"]), round(p.value_of(p["shad_pen"]), 2))
s.block_in(ellipse(Region(0.275, 0.560, 0.660, 0.830), rotate=-7), "flat",
           "shad_pen", direction=(-16,), density=1.0, size=0.085, load=1.0)
s.block_in(ellipse(Region(0.315, 0.592, 0.618, 0.782), rotate=-7), "flat",
           "shad_core", direction=(-12,), density=1.0, size=0.070, load=1.0)
print("shadow:", s.stroke_count)

# --- the mug ------------------------------------------------------------
p["mug_face"] = p.desaturate(p.mix(p.mix("cadmium_red", "ultramarine", 0.7),
                                   "titanium_white", 0.55), 0.5)
p["mug_shade"] = p.desaturate(p.mix(p.mix("ultramarine", "burnt_sienna", 0.3),
                                    "titanium_white", 0.45), 0.25)
p["mug_rim"] = p.desaturate(p.mix(p.mix("ultramarine", "burnt_sienna", 0.1),
                                  "titanium_white", 0.85), 0.25)
p["mug_lit"] = p.mix(p["mug_face"], p["mug_rim"], 0.55)
p["mug_hi"] = p.mix(p["mug_rim"], "titanium_white", 0.55)
p["tea"] = "#0d0a09"

# handle first: it is behind the body where the two meet
s.stroke([(0.632, 0.298), (0.676, 0.322), (0.699, 0.366)], "flat", "mug_face",
         size=0.030, pressure="even", load=1.0, note="handle upper")
s.stroke([(0.699, 0.366), (0.696, 0.416), (0.666, 0.455), (0.620, 0.480)],
         "flat", "mug_face", size=0.030, pressure="even", load=1.0,
         note="handle lower")

mug = polygon([(0.304, 0.247), (0.322, 0.180), (0.358, 0.138), (0.412, 0.114),
               (0.470, 0.107), (0.528, 0.120), (0.578, 0.148), (0.612, 0.196),
               (0.628, 0.268), (0.622, 0.372), (0.608, 0.498), (0.591, 0.624),
               (0.5625, 0.670), (0.500, 0.706), (0.430, 0.712), (0.372, 0.666),
               (0.352, 0.625), (0.334, 0.500), (0.3206, 0.375)])
s.block_in(mug.inset(0.045), "flat", "mug_face", direction="axis",
           density=1.0, size=0.09, load=1.0)
print("body:", s.stroke_count)

s.sweep([(0.308, 0.254), (0.3206, 0.375), (0.334, 0.500), (0.352, 0.625),
         (0.372, 0.664)], "flat", "mug_shade", into=(0.47, 0.45),
        depth=0.055, size=0.045, cross=22, load=1.0)
s.sweep([(0.625, 0.288), (0.622, 0.372), (0.608, 0.498), (0.591, 0.624),
         (0.562, 0.668)], "flat", "mug_lit", into=(0.47, 0.45),
        depth=0.055, size=0.042, cross=22, load=1.0)
print("sides:", s.stroke_count)

s.stroke([(0.311, 0.247), (0.328, 0.187), (0.363, 0.147), (0.414, 0.124),
          (0.470, 0.117), (0.526, 0.130), (0.574, 0.157), (0.606, 0.203),
          (0.620, 0.266)], "flat", "mug_rim", size=0.024, pressure="even",
         load=1.0, note="rim band")
s.stroke([(0.340, 0.268), (0.362, 0.294), (0.412, 0.314), (0.470, 0.324),
          (0.530, 0.312), (0.575, 0.286), (0.596, 0.262)], "flat", "mug_rim",
         size=0.030, pressure="even", load=1.0, note="front lip")

inside = polygon([(0.336, 0.258), (0.352, 0.200), (0.395, 0.160), (0.450, 0.140),
                  (0.515, 0.145), (0.565, 0.175), (0.594, 0.225), (0.590, 0.268),
                  (0.545, 0.297), (0.470, 0.313), (0.400, 0.300), (0.355, 0.280)])
s.block_in(inside.inset(0.026), "flat", "tea", direction="axis", density=1.0,
           size=0.052, load=1.0)
print("strokes:", s.stroke_count)
print(s.look())
print(s.look(region=span("C2", "F6"), reference="ref.jpg"))
