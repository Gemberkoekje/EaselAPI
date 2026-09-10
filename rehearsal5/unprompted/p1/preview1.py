chan_far = ribbon([(0.815, 0.379), (0.775, 0.404), (0.717, 0.437)], 0.028, 0.055)
chan_mid = ribbon([(0.723, 0.432), (0.665, 0.494), (0.643, 0.560)], 0.050, 0.085)
chan_near = ribbon([(0.648, 0.552), (0.700, 0.680), (0.760, 0.810), (0.845, 1.005)],
                   0.080, 0.180)

s.mark("bow", 0.255, 0.607)
s.mark("stern", 0.545, 0.641)
s.mark("keel_b", 0.262, 0.636)
s.mark("keel_s", 0.548, 0.702)

hull = polygon([
    (0.255, 0.607), (0.330, 0.594), (0.430, 0.602), (0.545, 0.628),
    (0.552, 0.672), (0.500, 0.702), (0.410, 0.710), (0.330, 0.692),
    (0.268, 0.652), (0.255, 0.622),
])
inside = polygon([
    (0.262, 0.612), (0.335, 0.599), (0.432, 0.607), (0.540, 0.632),
    (0.522, 0.652), (0.430, 0.646), (0.330, 0.634), (0.268, 0.626),
])
near = polygon([
    (0.262, 0.620), (0.332, 0.632), (0.432, 0.644), (0.543, 0.638),
    (0.552, 0.672), (0.500, 0.702), (0.410, 0.710), (0.330, 0.692),
    (0.268, 0.652),
])
for nm, sh in (("chan_far", chan_far), ("chan_mid", chan_mid), ("chan_near", chan_near),
               ("hull", hull), ("inside", inside), ("near", near)):
    print(f"{nm:9s} box={sh.box} axis={round(sh.axis,1)} area={sh.area:.4f}")

print(s.preview([chan_far, chan_mid, chan_near, hull, inside, near], grid=True))
print(s.preview([hull, inside, near], region=span("B5", "F6")))
print("strokes", s.stroke_count)
