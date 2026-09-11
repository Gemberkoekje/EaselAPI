# Edges. The bloom had gone rectangular, so its top and left boundaries are walked
# along -- along, in short passes, never across, and one pass each: a second undoes
# most of the first and leaves a thumbprint. Where one pass is not enough the answer
# is paint, which is the last three marks.
s.smudge([(0.205, 0.346), (0.268, 0.338)], size=0.040)
s.smudge([(0.331, 0.331), (0.406, 0.336)], size=0.038)
s.smudge([(0.181, 0.402), (0.187, 0.478)], size=0.038)

# Two smudges along the cowl were tried here and taken out: the cowl slopes, my
# passes ran flat, and across a boundary a smudge drags a finger-shaped lobe of the
# lighter mass into the darker one. That edge is lost with paint instead, in p8.

# Paint across the bloom's boundary rather than smudging it again.
s.stroke([(0.148, 0.318), (0.232, 0.356), (0.286, 0.332)], "bristle", "haze",
         size=0.036, load=0.55, opacity=0.50, pressure="swell")
s.stroke([(0.424, 0.298), (0.468, 0.352), (0.452, 0.428)], "bristle", "cyan_md",
         size=0.028, load=0.60, opacity=0.55, pressure="taper")
s.stroke([(0.196, 0.556), (0.238, 0.632)], "bristle", "cyan_lo",
         size=0.032, load=0.50, opacity=0.45, pressure="lift_off")
print(s.look())
