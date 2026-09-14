s.dry()
# The left half is the empty one. It does not get a thing put in it -- it gets a
# fainter instance of the water's own light, at values inside the field's own range,
# so that dropping it would have been a decision rather than a rescue.
faint = [([(0.055, 0.252), (0.150, 0.240), (0.242, 0.255), (0.340, 0.242)], 0.016, 0.48, 0.28),
         ([(0.138, 0.208), (0.240, 0.221), (0.332, 0.206), (0.430, 0.219)], 0.012, 0.38, 0.25),
         ([(0.262, 0.171), (0.360, 0.161), (0.448, 0.174)],                 0.009, 0.30, 0.23)]
for pts, size, op, val in faint:
    s.glaze(pts, p.at_value("wall", val), opacity=op, size=size, pressure="swell")

# and the sign's own light on the wet deck under it: the one warm note, said twice
s.stroke([(0.104, 0.272), (0.101, 0.320), (0.098, 0.358)], "bristle",
         p.at_value(p.desaturate("warm", 0.55), 0.34), size=0.014, load=0.52,
         opacity=0.58, load_falloff=0.6, pressure="lift_off")
print(s.look(region="A1:E5"))
