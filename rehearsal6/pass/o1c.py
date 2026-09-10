p = s.palette
s.dry()
for n in ("water_d","water_m","water_l"):
    p[n] = p.desaturate(p[n], 0.42)
    print(n, p.hex(p[n]), round(p.value_of(p[n]),3))
# reset the band the water spilled into
s.block_in(span("A5","H6"), "bristle", "sky", direction=(11,-9), density=0.85,
           size=0.12, load=1.0)
print("sky reset", s.stroke_count)
# the light, lower and smaller, sitting right on the horizon
s.block_in(ellipse(span("E6","H6")).shifted(0.0,-0.03), "round_hard", "glow",
           direction=-5, density=0.9, size=0.06, load=1.0, pressure="even")
s.block_in(ellipse(span("F6","H6")).inset(0.015).shifted(0.0,-0.02), "round_hard",
           "glow2", direction=-6, density=0.9, size=0.038, load=1.0, pressure="even")
s.stroke([(0.700,0.688),(0.800,0.680),(0.900,0.686)], "round_hard", "blaze",
         size=0.030, load=1.0, pressure="swell")
print("glow", s.stroke_count)
# the sea, with its top edge kept where I put it
sea = polygon([(-0.04,0.735),(1.04,0.722),(1.04,1.04),(-0.04,1.04)])
s.block_in(sea, "bristle", "water_m", direction=(-4,7), density=0.8, size=0.10,
           load=1.0, overhang=0)
s.block_in(polygon([(-0.04,0.740),(0.40,0.735),(0.28,1.04),(-0.04,1.04)]), "bristle",
           "water_d", direction=-9, density=0.85, size=0.07, load=1.0, overhang=0)
print("sea", s.stroke_count)
# the horizon is where two masses meet, cut from the near side
s.stroke([(-0.02,0.706),(0.35,0.703),(0.70,0.700),(1.02,0.699)], "flat", "water_d",
         size=0.016, load=1.0, pressure="even")
print("total", s.stroke_count)
print(s.look())
