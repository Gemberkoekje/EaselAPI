"""own1, pass 1 - flooded field, low sun through haze.
Structure: horizontal bands stacked in depth. Sky, far bank, water, near bank.
Everything recedes; the only verticals are accents."""
p = s.palette
p["sky_hi"] = p.desaturate(p.mix(p.mix("ultramarine", "burnt_sienna", 0.45),
                                 "titanium_white", 0.60), 0.15)
p["sky_lo"] = p.desaturate(p.mix(p.mix("cadmium_red", "yellow_ochre", 0.45),
                                 "titanium_white", 0.62), 0.30)
p["glow"] = p.mix(p.mix("cadmium_yellow", "cadmium_red", 0.22),
                  "titanium_white", 0.58)
p["sun"] = p.mix("lemon_yellow", "titanium_white", 0.80)
p["bank"] = p.desaturate(p.mix(p.mix("ultramarine", "burnt_umber", 0.5),
                               "titanium_white", 0.16), 0.2)
for n in ("sky_hi", "sky_lo", "glow", "sun", "bank"):
    print(f"{n:7s} {p.hex(p[n])} v={p.value_of(p[n]):.2f}")

# sky: one quiet mass, flat, laid on a slight tilt so it is not the canvas axis
s.block_in(Region(-0.03, -0.03, 1.03, 0.50), "flat", "sky_hi",
           direction=(6, 96), density=1.0, size=0.19, load=1.0, load_falloff=0.2)
print("sky:", s.stroke_count)

# the warm half of the sky, low down, wet into the cool
s.block_in(Region(-0.03, 0.24, 1.03, 0.50), "flat", "sky_lo",
           direction=(4,), density=1.0, size=0.13, load=1.0)
print("warm sky:", s.stroke_count)

# the haze round the sun - three ellipses, each smaller and hotter
s.block_in(ellipse(Region(0.30, 0.10, 0.92, 0.62)).inset(0.09), "flat",
           p.mix(p["sky_lo"], p["glow"], 0.45), direction=(-4,), density=1.0,
           size=0.18, load=1.0)
s.block_in(ellipse(Region(0.44, 0.20, 0.82, 0.56)).inset(0.06), "flat",
           p.mix(p["sky_lo"], p["glow"], 0.80), direction=(-4,), density=1.0,
           size=0.12, load=1.0)
s.block_in(ellipse(Region(0.53, 0.28, 0.73, 0.50)).inset(0.035), "flat",
           "glow", direction=(-4,), density=1.0, size=0.07, load=1.0)
print("haze:", s.stroke_count)

s.dab(0.630, 0.392, "round_hard", "sun", size=0.055, press=3)
s.dab(0.630, 0.392, "round_hard", "sun", size=0.030, press=3)

# the far bank: a low dark band, swept along its own ragged top edge
s.sweep([(-0.03, 0.470), (0.18, 0.462), (0.38, 0.468), (0.52, 0.458),
         (0.66, 0.464), (0.84, 0.455), (1.03, 0.462)], "bristle", "bank",
        into="down", depth=0.045, size=0.030, cross=20, load=1.0)
print("bank:", s.stroke_count)
print(s.look())
