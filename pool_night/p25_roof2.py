s.dry()
# The upper left is the last thin passage: a big empty dark with only the two main
# members crossing it. Secondary structure, at the floor of the box like the rest of
# the roof, so it adds depth without adding light. One of them catches the water.
for pts, size, op in [([(0.115, 0.008), (0.119, 0.052), (0.122, 0.094)], 0.0050, 0.85),
                      ([(0.048, 0.114), (0.100, 0.084), (0.150, 0.055)], 0.0065, 0.90),
                      ([(0.142, 0.120), (0.272, 0.150), (0.402, 0.179)], 0.0070, 0.85)]:
    s.stroke(pts, "flat", "truss", size=size, opacity=op, load=1.0,
             load_falloff=0.0, pressure="even")
s.stroke([(0.156, 0.126), (0.268, 0.156)], "liner",
         p.at_value(p.mix("wall", "watlit", 0.25), 0.36), size=0.0030,
         opacity=0.70, load=0.5, load_falloff=0.85, pressure=[0.2, 1.0])

# and one more ripple band on the wall, higher and further left than the others
s.glaze([(0.048, 0.196), (0.158, 0.185), (0.268, 0.199)], p.at_value("wall", 0.22),
        opacity=0.32, size=0.010, pressure="swell")
print(s.look(region="A1:E3"))
