# The knife marks read as foreign objects: too light, too hard, too rectangular
# against the dark. Knock them into the mass rather than undoing them.
p = s.palette
p["knock"] = p.mix(p.mix("ultramarine", "burnt_umber", 0.55), "burnt_sienna", 0.22)
s.dry()
for x0, y0, x1, y1 in [(0.06, 0.545, 0.30, 0.615), (0.46, 0.585, 0.68, 0.640),
                       (0.76, 0.680, 0.99, 0.740), (0.40, 0.462, 0.55, 0.492)]:
    s.stroke([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 + 0.008), (x1, y1)],
             "bristle", "knock", size=0.05, load=0.8, pressure="taper")
for x0, y0, x1, y1 in [(0.08, 0.556, 0.28, 0.606), (0.48, 0.596, 0.66, 0.632),
                       (0.78, 0.690, 0.97, 0.734)]:
    s.smudge([(x0, y0), (x1, y1)], size=0.045)
# put back one small warm note, softer and closer in value
s.stroke([(0.52, 0.606), (0.60, 0.618)], "bristle",
         p.tint(p.mix("burnt_sienna", "yellow_ochre", 0.5), 0.18),
         size=0.016, load=0.6, pressure="taper")
print("strokes:", s.stroke_count)
print(s.look())
