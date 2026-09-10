R = "/home/user/refs/Level1.jpg"
p = s.palette
p["wood_l2"] = p.mix(p["wood_lo"], p["wood_mid"], 0.62)
print("wood_l2", p.hex(p["wood_l2"]), round(p.value_of(p["wood_l2"]),3))

# one mass, laid on a slope, instead of a patchwork of rectangles
s.block_in(span("A1","C8"), "bristle", "wood_l2", direction=22, density=0.7,
           size=0.14, load=1.0)
print("left third", s.stroke_count)

# the corner nearest the viewer falls away
s.block_in(polygon([(-0.03,0.70),(0.17,0.88),(0.12,1.04),(-0.03,1.04)]),
           "bristle", "wood_lo", direction="axis", density=0.8, size=0.055, load=0.9)
s.stroke([(-0.02,0.60),(0.06,0.80)], "bristle", "wood_lo", size=0.09, load=0.8,
         opacity=0.35, pressure="taper")
print("bottom left", s.stroke_count)

# three long marks through the rectangles on the right, no two the same
s.stroke([(0.52,0.30),(0.72,0.20),(0.93,0.145)], "bristle", "wood_lit", size=0.075,
         load=1.0, opacity=0.40, pressure="taper")
s.stroke([(0.62,0.60),(0.83,0.50),(1.0,0.455)], "bristle", "wood_lit", size=0.055,
         load=1.0, opacity=0.35, pressure="lift_off")
s.stroke([(0.74,0.36),(0.80,0.62),(0.79,0.80)], "bristle", "wood_lit", size=0.10,
         load=0.9, opacity=0.30, pressure="swell")
s.stroke([(0.86,0.20),(1.0,0.30)], "bristle", "wood_hi", size=0.06, load=0.9,
         opacity=0.30, pressure="taper")
print("total", s.stroke_count)
print(s.look())
