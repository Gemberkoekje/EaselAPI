"""Pass 7: the passage to apologise for -- the glow's rings -- softened with films mixed from itself."""

field = s.sample(blob((0.17, 0.25), 0.07, 0.11, seed=2))
p["glow_film"] = p.mix(field, "glow", 0.5)

s.dry()
for pts, size, opacity in (
        ([(0.160, 0.440), (0.118, 0.300), (0.168, 0.140), (0.280, 0.070)], 0.075, 0.16),
        ([(0.205, 0.400), (0.172, 0.280), (0.222, 0.170), (0.312, 0.118)], 0.060, 0.15),
        ([(0.318, 0.100), (0.372, 0.118), (0.408, 0.180)], 0.050, 0.13),
        ([(0.120, 0.520), (0.180, 0.560), (0.260, 0.575)], 0.065, 0.12)):
    s.glaze(pts, "glow_film", opacity=opacity, size=size, pressure="swell", note="glow")
s.dry()
print(s.look(sketch=False, path="looks/07-glow.png"))
