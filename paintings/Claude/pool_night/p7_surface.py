# Most of this surface reflects the dark room; the lamps come up through the gaps.
# A reflection has no grain, so these are films, not brushwork -- the bristle's comb
# laid four of these as one rake dragged across the water.
s.dry()
refl = [([(0.560, 0.540), (0.70, 0.578), (0.89, 0.655)], 0.130, 0.45, "even"),
        ([(0.200, 0.790), (0.36, 0.860), (0.55, 0.965)], 0.155, 0.38, [1.0, 0.85, 0.5]),
        ([(0.660, 0.740), (0.82, 0.706)],                0.075, 0.28, "taper"),
        ([(0.330, 0.870), (0.52, 0.800), (0.68, 0.742)], 0.060, 0.22, "swell")]
for pts, size, op, press in refl:
    s.glaze(pts, "watrefl", opacity=op, size=size, pressure=press, note="subject")
print(s.look(region="B4:H8"))
