s.dry()
# Roof members, darker than the dark they cross -- near the floor of the box, so the
# body is nearly lost and the edge underlit from the water is what reads. One
# difference each: the near truss is lit its whole length, the far one only at its
# left end, the hanger not at all.
s.stroke([(-0.05, 0.022), (0.42, 0.136), (1.05, 0.199)], "flat", "truss",
         size=0.030, opacity=0.95, load=1.0, load_falloff=0.0, pressure="even")
s.stroke([(-0.05, 0.150), (0.32, 0.066), (0.60, 0.020)], "flat", "truss",
         size=0.014, opacity=0.85, load=1.0, load_falloff=0.0, pressure="even")
s.stroke([(0.222, -0.05), (0.252, 0.098), (0.276, 0.203)], "flat", "truss",
         size=0.009, opacity=0.80, load=1.0, load_falloff=0.0, pressure="even")

p["lit_edge"] = p.at_value(p.mix("wall", "watlit", 0.35), 0.44)
p["lit_dim"]  = p.at_value(p.mix("wall", "watlit", 0.20), 0.34)
s.stroke([(0.08, 0.055), (0.45, 0.152), (1.05, 0.214)], "liner", "lit_edge",
         size=0.005, opacity=0.90, load=0.70, load_falloff=0.75, pressure=[0.2, 1.0, 0.45])
s.stroke([(-0.05, 0.159), (0.22, 0.099)], "liner", "lit_dim",
         size=0.004, opacity=0.65, load=0.55, load_falloff=0.8, pressure=[0.1, 0.9])

# the ripple light thrown up onto the wall: films, wavy, dying as they climb
caustic = [([(0.46, 0.291), (0.56, 0.274), (0.66, 0.292), (0.77, 0.272),
             (0.90, 0.286), (1.04, 0.274)], 0.024, 0.75, 0.44),
           ([(0.57, 0.232), (0.68, 0.248), (0.79, 0.229), (0.92, 0.244),
             (1.04, 0.232)], 0.017, 0.65, 0.40),
           ([(0.66, 0.178), (0.77, 0.164), (0.88, 0.180), (1.02, 0.166)], 0.012, 0.50, 0.35),
           ([(0.33, 0.302), (0.43, 0.288), (0.52, 0.303)], 0.019, 0.52, 0.37),
           ([(0.85, 0.122), (0.96, 0.135), (1.04, 0.124)], 0.009, 0.38, 0.32)]
for pts, size, op, val in caustic:
    s.glaze(pts, p.at_value("wall", val), opacity=op, size=size, pressure="swell")
print(s.look(region="A1:H4"))
