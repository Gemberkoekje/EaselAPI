p = s.palette
dk = p.mix("ultramarine", "burnt_umber", 0.55)

p["glow_hi"]  = p.mix("titanium_white", "yellow_ochre", 0.07)      # 0.93
p["glow_mid"] = p.mix("titanium_white", "cerulean", 0.10)          # 0.88
p["glow_lo"]  = p.mix(p.mix("titanium_white","cerulean",0.14), "yellow_ochre", 0.06)  # 0.82
p["out_far"]  = p.mix(p.mix("titanium_white","cerulean",0.20), "burnt_umber", 0.05)   # 0.72
p["out_tree"] = p.mix(p.mix("titanium_white","cerulean",0.22), "viridian", 0.14)
p["wall"]     = p.mix(dk, "burnt_sienna", 0.26)
p["wall_hi"]  = p.mix(p.mix(dk,"burnt_sienna",0.26), "titanium_white", 0.13)
p["dk"]       = dk
print("out_tree", p.hex(p["out_tree"]), round(p.value_of(p["out_tree"]),2))
print("wall", p.hex(p["wall"]), round(p.value_of(p["wall"]),2),
      " wall_hi", round(p.value_of(p["wall_hi"]),2))

# --- landmarks ---
s.mark("win_tr", 0.497, 0.098)
s.mark("win_br", 0.487, 0.652)
s.mark("sill_bk", 0.030, 0.638)
s.mark("sill_lip", 0.030, 0.800)
s.mark("pot_rl", 0.497, 0.574)
s.mark("pot_rr", 0.673, 0.568)
s.mark("pot_base", 0.585, 0.760)
s.mark("plant_top", 0.618, 0.322)

# --- 1. the light outside, furthest of all ---
bandA = polygon([(-0.09, -0.03), (0.585, -0.05), (0.578, 0.300), (-0.09, 0.272)])
bandB = polygon([(-0.09, 0.264), (0.578, 0.293), (0.572, 0.500), (-0.09, 0.486)])
bandC = polygon([(-0.09, 0.482), (0.572, 0.498), (0.567, 0.705), (-0.09, 0.725)])

s.block_in(bandA, "flat", "glow_hi",  density=0.85, size=0.09, direction=(14, 101), load=1.0)
s.block_in(bandB, "flat", "glow_mid", density=0.85, size=0.09, direction=(-9, 84), load=1.0)
s.block_in(bandC, "flat", "glow_lo",  density=0.85, size=0.085, direction=(19, 106), load=1.0)
# lose the two joins while the paint is fresh
s.smudge([(0.06, 0.268), (0.30, 0.281)], size=0.040)
s.smudge([(0.30, 0.281), (0.53, 0.292)], size=0.038)
s.smudge([(0.05, 0.487), (0.31, 0.492)], size=0.042)
s.smudge([(0.31, 0.492), (0.54, 0.498)], size=0.036)

# something out there, soft and without detail
far  = blob((0.24, 0.578), 0.33, 0.095, wobble=0.45, seed=4)
tree = blob((0.145, 0.515), 0.105, 0.070, wobble=0.5, seed=9)
s.block_in(far,  "flat", "out_far",  density=0.8, size=0.05, direction=(8, 96))
s.block_in(tree, "flat", "out_tree", density=0.8, size=0.04, direction=(-22, 70))
s.smudge([(0.05, 0.510), (0.26, 0.498)], size=0.045)
s.smudge([(0.26, 0.498), (0.46, 0.520)], size=0.040)
s.smudge([(0.10, 0.560), (0.22, 0.545)], size=0.040)

print("strokes:", s.stroke_count)
