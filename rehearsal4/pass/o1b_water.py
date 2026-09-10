"""own1, pass 2 - the flood. Water is the sky lying down: same values, softer,
broken by horizontals. Also break up the blocky steps the haze ellipses left."""
p = s.palette
p["wat_far"] = p.desaturate(p.mix(p.mix("ultramarine", "burnt_sienna", 0.4),
                                  "titanium_white", 0.50), 0.2)
p["wat_lit"] = p.mix(p["sky_lo"], p["glow"], 0.55)
p["wat_near"] = p.desaturate(p.mix(p.mix("ultramarine", "burnt_umber", 0.4),
                                   "titanium_white", 0.36), 0.15)
p["mud"] = p.mix(p["bank"], "burnt_umber", 0.45)
for n in ("wat_far", "wat_lit", "wat_near", "mud"):
    print(f"{n:8s} {p.hex(p[n])} v={p.value_of(p[n]):.2f}")

# soften the haze's stepped edges while the sky is still the top layer
for a, b, sz, op in [((0.34, 0.14), (0.44, 0.30), 0.09, 0.45),
                     ((0.86, 0.16), (0.78, 0.32), 0.09, 0.45),
                     ((0.42, 0.48), (0.52, 0.34), 0.08, 0.40),
                     ((0.80, 0.50), (0.72, 0.36), 0.08, 0.40),
                     ((0.48, 0.10), (0.66, 0.08), 0.10, 0.35)]:
    s.stroke([a, b], "bristle", p.mix(p["sky_lo"], p["glow"], 0.35), size=sz,
             opacity=op, load=0.85, note="break the haze step")
for a, b in [((0.40, 0.22), (0.47, 0.30)), ((0.84, 0.24), (0.77, 0.32)),
             ((0.55, 0.09), (0.68, 0.10))]:
    s.smudge([a, b], size=0.045)
print("haze softened:", s.stroke_count)

# the water, laid flat and horizontal - the opposite of the bank's rag
s.block_in(Region(-0.03, 0.478, 1.03, 1.03), "flat", "wat_far",
           direction=(1,), density=1.0, size=0.14, load=1.0, load_falloff=0.25)
s.block_in(Region(-0.03, 0.72, 1.03, 1.03), "flat", "wat_near",
           direction=(-1,), density=1.0, size=0.13, load=1.0)
print("water:", s.stroke_count)

# the path of light, straight down from the sun, widening as it nears
s.block_in(ribbon([(0.632, 0.482), (0.628, 0.72), (0.618, 1.02)], 0.10,
                  end_width=0.30), "flat", "wat_lit", direction=(2,),
           density=0.9, size=0.075, load=1.0)
print("light path:", s.stroke_count)

# ripples: short horizontals, never the same length or value twice
rip = [(0.10, 0.560, 0.20, "wat_lit", 0.020, 0.5), (0.34, 0.545, 0.12, "wat_lit", 0.014, 0.4),
       (0.78, 0.552, 0.17, "wat_lit", 0.018, 0.45), (0.48, 0.600, 0.26, "sky_lo", 0.016, 0.6),
       (0.06, 0.640, 0.15, "wat_near", 0.022, 0.7), (0.72, 0.628, 0.22, "sky_lo", 0.020, 0.55),
       (0.24, 0.700, 0.30, "wat_lit", 0.024, 0.5), (0.60, 0.735, 0.18, "glow", 0.018, 0.5),
       (0.02, 0.790, 0.26, "wat_far", 0.030, 0.7), (0.70, 0.812, 0.28, "sky_lo", 0.026, 0.5),
       (0.32, 0.870, 0.34, "wat_far", 0.032, 0.6), (0.76, 0.920, 0.22, "wat_far", 0.028, 0.55),
       (0.08, 0.955, 0.30, "bank", 0.030, 0.45), (0.44, 0.990, 0.36, "bank", 0.034, 0.4)]
for x, y, w, col, sz, op in rip:
    s.stroke([(x, y), (x + w * 0.55, y - 0.006), (x + w, y + 0.004)], "bristle",
             col, size=sz, opacity=op, load=0.9, load_falloff=0.3, note="ripple")
print("strokes:", s.stroke_count)
print(s.look())
