R = "/home/user/refs/Level1.jpg"
p = s.palette

# ---- palette -------------------------------------------------------------
wood      = p.mix(p.mix("yellow_ochre", "burnt_sienna", 0.3), "ultramarine", 0.12)
p["wood_dk"]  = p.desaturate(wood, 0.30)
p["wood_mid"] = p.desaturate(p.mix(wood, "titanium_white", 0.255), 0.35)
p["wood_lit"] = p.desaturate(p.mix(wood, "titanium_white", 0.486), 0.32)
p["wood_hi"]  = p.desaturate(p.mix(wood, "titanium_white", 0.585), 0.32)
p["dk"]       = p.mix("ultramarine", "burnt_umber", 0.5)
p["dk_warm"]  = p.mix("ultramarine", "burnt_umber", 0.72)
p["shad"]     = p.mix(p["dk"], p["wood_mid"], 0.52)
p["shad_lo"]  = p.mix(p["dk"], p["wood_mid"], 0.20)
for n in ("wood_dk","wood_mid","wood_lit","wood_hi","dk","dk_warm","shad","shad_lo"):
    print(f"{n:9s} {p.hex(p[n])} v={p.value_of(p[n]):.3f}")

# ---- landmarks (free) ----------------------------------------------------
s.mark("rim_l", 0.288, 0.250)
s.mark("rim_t", 0.485, 0.111)
s.mark("rim_r", 0.632, 0.215)
s.mark("lip_f", 0.469, 0.333)
s.mark("base_l", 0.366, 0.662)
s.mark("base_f", 0.450, 0.676)
s.mark("base_r", 0.550, 0.650)
s.mark("hand_o", 0.731, 0.262)

# ---- 1. furthest of all: the dark beyond the table's far edge -------------
corner = polygon([(0.838, -0.02), (1.02, -0.02), (1.02, 0.090), (0.874, 0.019)])
s.block_in(corner, "flat", "dk", direction=19, density=1.0, size=0.030,
           load=1.0, pressure="even")
print("after corner", s.stroke_count)

# ---- 2. the table: light swathe, right field, dark left edge --------------
lit = ribbon([(0.705, -0.06), (0.700, 0.30), (0.675, 0.56), (0.595, 0.82), (0.44, 1.06)], 0.20)
s.block_in(lit, "bristle", "wood_lit", direction="axis", density=0.85, size=0.085, load=1.0)
print("after lit swathe", s.stroke_count)

rightfield = polygon([(0.755, 0.06), (1.02, 0.10), (1.02, 0.74), (0.80, 0.70), (0.775, 0.36)])
s.block_in(rightfield, "flat", "wood_mid", direction=74, density=0.8, size=0.09, load=0.95)
print("after right field", s.stroke_count)

topband = ribbon([(0.26, 0.035), (0.55, 0.062), (0.78, 0.03)], 0.115)
s.block_in(topband, "bristle", "wood_lit", direction="axis", density=0.8, size=0.055, load=0.9)
print("after top band", s.stroke_count)

leftband = ribbon([(-0.02, 0.06), (0.035, 0.52), (0.125, 1.05)], 0.19)
s.block_in(leftband, "bristle", "wood_dk", direction="axis", density=0.8, size=0.075, load=0.9)
print("after left band", s.stroke_count)

# foreground light, bottom centre (D8/E8 are the lightest cells down there)
fore = ribbon([(0.30, 1.05), (0.52, 0.93), (0.78, 0.86), (1.0, 0.83)], 0.17)
s.block_in(fore, "bristle", "wood_lit", direction="axis", density=0.8, size=0.075, load=1.0)
print("after foreground", s.stroke_count)

# ---- 3. cut the table back up to the dark corner (edge from the near side)
s.stroke([(0.845, 0.008), (0.94, 0.043), (1.01, 0.078)], "flat", "wood_mid",
         size=0.045, pressure="even", load=1.0)
print("total", s.stroke_count)
print(s.look())
print(s.look(reference=R, grid=True))
