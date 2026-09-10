"""own1, pass 4 - the sun path still has two perfectly straight vertical edges.
Break the silhouette from OUTSIDE it: strokes that start in the water, cross,
and come out the other side, plus bright ones that overshoot."""
p = s.palette
s.dry()

cross = [(0.36, 0.505, 0.52, "wat_far", 0.013), (0.50, 0.535, 0.39, "wat_far", 0.011),
         (0.41, 0.562, 0.28, "wat_far", 0.014), (0.60, 0.590, 0.30, "wat_far", 0.012),
         (0.33, 0.622, 0.46, "wat_near", 0.016), (0.55, 0.652, 0.36, "wat_near", 0.013),
         (0.38, 0.688, 0.31, "wat_near", 0.018), (0.58, 0.726, 0.33, "wat_near", 0.014),
         (0.30, 0.758, 0.42, "wat_near", 0.020), (0.61, 0.796, 0.30, "wat_near", 0.016),
         (0.34, 0.836, 0.36, "wat_near", 0.022), (0.63, 0.880, 0.32, "wat_near", 0.018),
         (0.28, 0.912, 0.40, "wat_near", 0.024), (0.66, 0.955, 0.34, "wat_near", 0.020)]
for x, y, w, col, sz in cross:
    s.stroke([(x, y), (x + w * 0.45, y + 0.006), (x + w, y - 0.005)], "bristle",
             col, size=sz, opacity=0.9, load=0.95, load_falloff=0.35,
             note="cross the path")

over = [(0.47, 0.528, 0.26, 0.010), (0.53, 0.608, 0.25, 0.012),
        (0.44, 0.700, 0.33, 0.013), (0.57, 0.772, 0.27, 0.011),
        (0.41, 0.860, 0.36, 0.015), (0.53, 0.935, 0.31, 0.013),
        (0.62, 0.572, 0.17, 0.009), (0.49, 0.982, 0.34, 0.014)]
for x, y, w, sz in over:
    s.stroke([(x, y), (x + w, y + 0.004)], "bristle", "wat_lit", size=sz,
             opacity=0.85, load=1.0, load_falloff=0.45, note="glint")
print("path broken:", s.stroke_count)

# the haze's blocky top
warm = p.mix(p["sky_lo"], p["glow"], 0.30)
for a, b, sz in [((0.42, 0.030), (0.54, 0.072), 0.075),
                 ((0.60, 0.020), (0.72, 0.062), 0.075),
                 ((0.76, 0.052), (0.86, 0.100), 0.065),
                 ((0.36, 0.088), (0.46, 0.130), 0.060),
                 ((0.86, 0.130), (0.92, 0.180), 0.055)]:
    s.stroke([a, b], "bristle", warm, size=sz, opacity=0.55, load=0.85,
             note="soften the haze")
for a, b in [((0.50, 0.055), (0.62, 0.048)), ((0.80, 0.095), (0.88, 0.130))]:
    s.smudge([a, b], size=0.040)

# tie the tree to its own reflection
s.stroke([(0.246, 0.600), (0.240, 0.622)], "flat", "tree", size=0.010,
         pressure="even", load=1.0, note="waterline")
s.stroke([(0.222, 0.612), (0.268, 0.616)], "bristle", "wat_lit", size=0.007,
         opacity=0.8, load=1.0, note="light at the waterline")
s.stroke([(0.236, 0.690), (0.252, 0.694)], "bristle", "tree", size=0.007,
         opacity=0.55, load=1.0, note="reflection")

# a last few darks in the near water so the foreground is not all one value
for x, y, w, sz in [(0.02, 0.700, 0.18, 0.016), (0.80, 0.742, 0.20, 0.018),
                    (0.86, 0.880, 0.16, 0.022)]:
    s.stroke([(x, y), (x + w, y + 0.004)], "bristle", "mud", size=sz,
             opacity=0.5, load=0.9, note="dark ripple")
print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
