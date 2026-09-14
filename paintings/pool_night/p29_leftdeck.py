s.dry()
# Last passage named weak: the mid-left deck, a large flat grey field. It gets
# direction rather than texture -- broad passes along the deck's own axis, lighter
# toward the pool and darker away from it, and two broken marks on them.
for pts, size, op, val in [([(0.000, 0.702), (0.120, 0.634), (0.240, 0.566)], 0.100, 0.32, 0.335),
                           ([(0.000, 0.560), (0.100, 0.498), (0.200, 0.440)], 0.090, 0.30, 0.265),
                           ([(0.020, 0.802), (0.140, 0.732)],                 0.080, 0.26, 0.300)]:
    s.glaze(pts, p.at_value("deck", val), opacity=op, size=size, pressure="swell")
s.stroke([(0.055, 0.666), (0.158, 0.608)], "bristle", p.at_value("deck", 0.385),
         size=0.030, load=0.70, opacity=0.42, load_falloff=0.5, pressure="taper")
s.stroke([(0.028, 0.614), (0.132, 0.552)], "bristle", p.at_value("deck", 0.245),
         size=0.026, load=0.60, opacity=0.36, load_falloff=0.5, pressure="swell")
print(s.look(region="A4:D7"))
