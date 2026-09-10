# Pass 9 - the terracotta pot. Body in steps, then far lip / inside / near lip.
p = s.palette
terra = p.mix("burnt_sienna", "cadmium_red", 0.28)
p["terra_mid"]  = p.tint(terra, 0.20)
p["terra_lit"]  = p.tint(p.mix(terra, "yellow_ochre", 0.28), 0.42)
p["terra_hi"]   = p.tint(p.mix(terra, "yellow_ochre", 0.40), 0.56)
p["terra_sh"]   = p.mix(terra, "ultramarine", 0.42)
p["terra_refl"] = p.mix(p.mix(terra, "ultramarine", 0.42), "burnt_sienna", 0.50)
p["pot_in"]     = p.mix(p.mix("burnt_umber", "ultramarine", 0.40), "burnt_sienna", 0.12)
p["cast"]       = p.mix(p["tbl"], p.mix("ultramarine","burnt_umber",0.5), 0.60)
for k in ("terra_mid","terra_lit","terra_hi","terra_sh","terra_refl","pot_in","cast"):
    print(f"{k:11s} {p.hex(p[k])}  v={p.value_of(p[k]):.3f}")

# --- redraw the guide lines ----------------------------------------------------
s.erase()
s.pencil([s.pt("rim_l"), (0.360, 0.652), (0.420, 0.648), (0.478, 0.656), s.pt("rim_r")])
s.pencil([(0.324, 0.686), (0.366, 0.712), (0.417, 0.718), (0.472, 0.712), (0.512, 0.694)])
s.pencil([(0.324, 0.686), (0.336, 0.780), s.pt("base_l")])
s.pencil([(0.512, 0.694), (0.498, 0.782), s.pt("base_r")])
s.pencil([s.pt("base_l"), (0.400, 0.878), (0.446, 0.877), s.pt("base_r")])

s.dry()
# --- cast shadow first: it is on the table, behind the pot in depth ------------
s.block_in(blob(Region(0.44, 0.792, 0.78, 0.902), wobble=0.30, seed=6), "flat", "cast",
           direction=(13, 158), density=1.0, size=0.055, load=1.0, pressure="even")
s.block_in(ellipse(Region(0.36, 0.848, 0.58, 0.894)), "flat", "cast",
           direction=(6, 170), density=1.0, size=0.038, load=1.0, pressure="even")

# --- the body, as steps across the form ---------------------------------------
body = polygon([(0.324,0.678),(0.418,0.690),(0.512,0.686),(0.498,0.782),(0.482,0.866),
                (0.440,0.880),(0.396,0.879),(0.352,0.860),(0.336,0.780)])
s.block_in(body.inset(0.026), "flat", "terra_mid", direction=(13, 167), density=1.0,
           size=0.052, load=1.0, pressure="even")
s.block_in(polygon([(0.326,0.684),(0.386,0.692),(0.376,0.800),(0.372,0.868),
                    (0.352,0.858),(0.336,0.778)]).inset(0.016),
           "flat", "terra_lit", direction=(9, 172), density=1.0, size=0.032,
           load=1.0, pressure="even")
s.block_in(polygon([(0.452,0.692),(0.512,0.686),(0.498,0.782),(0.482,0.866),
                    (0.446,0.878),(0.448,0.790)]).inset(0.016),
           "flat", "terra_sh", direction=(15, 163), density=1.0, size=0.032,
           load=1.0, pressure="even")
s.stroke([(0.506,0.706),(0.496,0.790),(0.484,0.856)], "round_hard", "terra_refl",
         size=0.012, pressure=[0.4,1.0,0.7])
# lose the joins between the steps while they are wet
for pts in ([(0.384,0.740),(0.392,0.796)], [(0.452,0.744),(0.458,0.804)],
            [(0.398,0.856),(0.436,0.862)]):
    s.smudge(pts, size=0.022)

# --- the rim: far lip, then the inside, then the near lip ---------------------
s.dry()
s.block_in(ellipse(Region(0.316, 0.640, 0.518, 0.700)).inset(0.012), "flat", "terra_lit",
           direction=(4, 176), density=1.0, size=0.026, load=1.0, pressure="even")
s.block_in(ellipse(Region(0.334, 0.652, 0.502, 0.692)).inset(0.010), "flat", "pot_in",
           direction=(7, 173), density=1.0, size=0.020, load=1.0, pressure="even")
s.stroke([(0.330,0.670),(0.372,0.694),(0.418,0.702),(0.468,0.694),(0.510,0.676)],
         "flat", "terra_lit", size=0.020, pressure="even")
s.stroke([(0.336,0.668),(0.376,0.690),(0.418,0.697)], "round_hard", "terra_hi",
         size=0.009, pressure=[0.5,1.0,0.35])
s.stroke([(0.330,0.662),(0.368,0.650),(0.418,0.646),(0.470,0.650)], "round_hard",
         "terra_hi", size=0.008, pressure=[0.3,1.0,0.8,0.3])

print("strokes:", s.stroke_count)
print(s.look(region=span("C5","F8")))
print(s.look())
