# A warm veil to unify the subject, mixed close to what it lands on. Eight narrow
# films read as stains; three broad ones read as a wash, which is the point.
s.dry()
for pts, sz, col, op in [
    ([(0.380, 0.548), (0.478, 0.576), (0.572, 0.552), (0.646, 0.594)], 0.115,
     "veil_lo", 0.10),
    ([(0.624, 0.660), (0.716, 0.762), (0.808, 0.876)], 0.135, "veil_lo", 0.09),
    ([(0.668, 0.372), (0.744, 0.352), (0.804, 0.310)], 0.098, "veil", 0.08),
]:
    s.glaze(pts, col, opacity=op, size=sz, note="subject")
print(s.look())
