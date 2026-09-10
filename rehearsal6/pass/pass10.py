R = "/home/user/refs/Level1.jpg"
p = s.palette
p["fig"]  = p.mix("burnt_umber","alizarin",0.18)
p["fig2"] = p.mix(p["fig"], p["wood_lo"], 0.13)
p["visor"] = p.mix(p.mix("ultramarine","burnt_umber",0.28), "titanium_white", 0.60)
print("fig", p.hex(p["fig"]), round(p.value_of(p["fig"]),3),
      "visor", p.hex(p["visor"]), round(p.value_of(p["visor"]),3))

body = polygon([(0.360,0.455),(0.368,0.420),(0.400,0.400),(0.442,0.400),(0.480,0.424),
                (0.496,0.470),(0.498,0.560),(0.500,0.616),(0.470,0.634),(0.392,0.636),
                (0.364,0.610),(0.358,0.530)])
s.preview(body, reference=R, region=span("C4","F6"))
s.block_in(body.inset(0.013), "flat", "fig", direction=88, density=1.0, size=0.026,
           load=1.0, pressure="even")
print("body", s.stroke_count)
pack = polygon([(0.494,0.486),(0.536,0.494),(0.554,0.522),(0.552,0.570),(0.526,0.588),
                (0.496,0.580)])
s.block_in(pack.inset(0.010), "flat", "fig2", direction=76, density=1.0, size=0.020,
           load=1.0, pressure="even")
print("pack", s.stroke_count)
# the two legs, dark against the foot
s.stroke([(0.400,0.630),(0.402,0.652)], "round_hard", "fig", size=0.024, load=1.0,
         pressure="even")
s.stroke([(0.452,0.630),(0.455,0.654)], "round_hard", "fig", size=0.030, load=1.0,
         pressure="even")
# the visor: dark first, then the light, then the edge (three marks)
s.stroke([(0.374,0.452),(0.420,0.470),(0.446,0.486)], "round_hard", "visor",
         size=0.026, load=1.0, pressure="swell")
s.stroke([(0.382,0.456),(0.416,0.471)], "round_hard", "mug_hi", size=0.014,
         load=1.0, pressure="taper")
print("figure done", s.stroke_count)

# the spoon: in front of the tea
spoon = polygon([(0.509,-0.03),(0.546,-0.03),(0.531,0.140),(0.514,0.240),(0.489,0.234),
                 (0.500,0.118)])
s.block_in(spoon.inset(0.008), "flat", "dk", direction=83, density=1.0, size=0.016,
           load=1.0, pressure="even")
print("spoon", s.stroke_count)
s.stroke([(0.508,0.246),(0.524,0.268),(0.545,0.281)], "round_hard", "mug_shd",
         size=0.017, load=1.0, pressure="swell")
s.dab(0.536, 0.276, "round_hard", "mug_wt", size=0.011, press=3)
print("total", s.stroke_count)
print(s.look(reference=R, region=span("C1","G7")))
