s.dry()
# The lower-right deck came back blotchy -- the coping bands' starved bristle reading
# as grit over a large quiet area. Films along the deck's own direction, so nothing
# new runs across it.
for pts, size, op, val in [([(0.660, 1.050), (0.820, 0.905), (0.990, 0.760)], 0.130, 0.50, 0.280),
                           ([(0.830, 1.050), (0.970, 0.905), (1.060, 0.815)], 0.110, 0.44, 0.272),
                           ([(0.900, 0.762), (1.020, 0.655)],                 0.085, 0.38, 0.292)]:
    s.glaze(pts, p.at_value("deck", val), opacity=op, size=size, pressure="swell")
print(s.look(region="F6:H8"))
