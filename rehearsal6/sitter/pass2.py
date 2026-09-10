p = s.palette
def at_value(base, target, other="titanium_white"):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a+b)/2
        if p.value_of(p.mix(base, other, m)) < target: a = m
        else: b = m
    return (a+b)/2
warm  = p.mix("yellow_ochre","burnt_sienna",0.30)
def V(base, v): return p.mix(base,"titanium_white", at_value(base,v))
p["wall_cool"] = p.desaturate(V(warm,0.53), 0.42)
p["wall_hic"]  = p.desaturate(V(warm,0.70), 0.35)
p["dark"]      = p.mix("ultramarine","burnt_umber",0.55)
p["dark_warm"] = p.mix("burnt_umber","ultramarine",0.28)
p["skin_far"]  = p.desaturate(V(p.mix("burnt_sienna","cadmium_red",0.2),0.58), 0.15)
p["red_sh"]    = V(p.mix("cadmium_red","burnt_sienna",0.45), 0.40)
p["yellow_sp"] = V(p.mix("cadmium_yellow","yellow_ochre",0.4), 0.62)
p["table_lit"] = p.desaturate(V(warm,0.46), 0.25)
p["mid_dim"]   = p.desaturate(V(warm,0.30), 0.35)
p["bag_red"]   = V(p.mix("alizarin","burnt_umber",0.35), 0.17)
for n in ("wall_cool","wall_hic","skin_far","red_sh","yellow_sp","table_lit","mid_dim","bag_red"):
    print(f"{n:10s} {p.hex(p[n])} {p.value_of(p[n]):.2f}")

wall = polygon([(0.735,0.0),(1.0,0.0),(1.0,0.46),(0.925,0.48),(0.855,0.40),(0.795,0.33),(0.757,0.19)])
s.block_in(wall, "flat", "wall_cool", direction=(11,), density=0.55, size=0.105, load=1.0)
s.block_in(polygon([(0.885,0.0),(1.0,0.0),(1.0,0.26),(0.912,0.235)]), "flat", "wall_hic",
           direction=(14,), density=0.6, size=0.075, load=1.0)
s.stroke([(0.752,0.02),(0.762,0.30)], "bristle", "mid_dim", size=0.022, load=0.7, pressure="lift_off")
s.dry()

# dark plaque on the wall
s.dab(0.886, 0.300, "round_hard", "dark_warm", size=0.038, press=2)
s.stroke([(0.872,0.276),(0.900,0.318)], "round_hard", "dark_warm", size=0.020)
s.dry()

# --- the man seated behind, right: cap, then face, then beard
s.block_in(blob((0.793,0.310), 0.040, 0.030, wobble=0.30, seed=6), "flat", "dark", size=0.026, density=1.0)
s.block_in(ellipse(polygon([(0.766,0.325),(0.822,0.325),(0.822,0.402),(0.766,0.402)])),
           "round_hard", "skin_far", pressure="even", size=0.024, density=0.9)
s.stroke([(0.775,0.378),(0.812,0.386)], "bristle", "dark_warm", size=0.020, load=0.8)
s.stroke([(0.762,0.412),(0.812,0.428)], "flat", "mid_dim", size=0.030, pressure="even")
s.dry()

# --- red patterned shirt
sh = polygon([(0.812,0.392),(0.878,0.386),(0.906,0.452),(0.898,0.534),(0.842,0.548),(0.816,0.470)])
s.block_in(sh, "bristle", "red_sh", direction="axis", density=0.95, size=0.038, load=1.0)
for (x,y,r) in [(0.836,0.418,0.014),(0.868,0.440,0.012),(0.848,0.478,0.013),(0.884,0.492,0.011),(0.860,0.520,0.010)]:
    s.dab(x, y, "round_hard", "yellow_sp", size=r, press=2)
s.dry()

# --- the dark figure at the right edge
s.block_in(polygon([(0.930,0.330),(1.0,0.318),(1.0,0.60),(0.946,0.575),(0.926,0.46)]),
           "flat", "dark", direction=(80,), density=0.95, size=0.045, load=1.0)
s.dry()

# --- table and the clutter on it, then the dark under it
s.block_in(polygon([(0.862,0.648),(0.945,0.632),(0.952,0.706),(0.868,0.752)]),
           "flat", "table_lit", direction=(-9,), density=0.9, size=0.042, load=1.0)
s.stroke([(0.874,0.578),(0.930,0.566)], "bristle", "mid_dim", size=0.045, load=0.7, pressure="swell")
s.block_in(polygon([(0.936,0.735),(1.0,0.720),(1.0,1.0),(0.928,1.0)]), "flat", "dark",
           direction=(84,), density=0.95, size=0.04, load=1.0)
s.block_in(blob((0.950,0.848), 0.055, 0.080, wobble=0.30, seed=9), "bristle", "bag_red",
           direction="axis", density=0.95, size=0.036, load=1.0)
print("strokes:", s.stroke_count)
