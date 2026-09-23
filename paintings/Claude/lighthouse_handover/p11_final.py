# The weakest passage: the cliff face, one smooth plane with marks on it. Turn it with
# films rather than more paint -- warmer on the left where it faces the glow, darker on
# the right where it turns away. Calm the wavy dark line near the top of the sky. And
# the tower's shadow side takes a little cool light back from the sky.
s.dry()
face_l = s.sample(polygon([(0.48, 0.62), (0.60, 0.59), (0.62, 0.68), (0.52, 0.68)]))
face_r = s.sample(polygon([(0.84, 0.58), (1.0, 0.57), (1.0, 0.70), (0.86, 0.72)]))
p["face_warm"] = p.at_value(p.mix(face_l, "lit_dim", 0.6), p.value_of(face_l) + 0.03)
p["face_dark"] = p.at_value(p.mix(face_r, "land", 0.6), p.value_of(face_r) - 0.025)
s.glaze([(0.47, 0.650), (0.53, 0.640), (0.60, 0.625)], "face_warm", opacity=0.5, size=0.09,
        pressure=[0.6, 1.0, 0.4], clip=headland)
s.glaze([(0.84, 0.640), (0.94, 0.625), (1.06, 0.615)], "face_dark", opacity=0.5, size=0.12,
        pressure=[0.4, 0.9, 1.0], clip=headland)
top = s.sample(Region(0.0, 0.06, 1.0, 0.12))
p["top_calm"] = top
s.glaze([(-0.06, 0.092), (0.40, 0.088), (1.06, 0.094)], "top_calm", opacity=0.35, size=0.05,
        pressure=[0.8, 1.0, 0.8])
shade = s.sample(polygon([(TX + 0.004, 0.25), (TX + 0.012, 0.25), (TX + 0.017, 0.50), (TX + 0.006, 0.50)]))
p["tower_cool"] = p.at_value(p.mix(shade, "pale", 0.4), p.value_of(shade) + 0.04)
s.glaze([(TX + 0.0120, 0.215), (TX + 0.0150, 0.380), (TX + 0.0175, 0.530)], "tower_cool",
        opacity=0.35, size=0.008, pressure=[0.6, 1.0, 0.7], clip=tower, note="subject")
s.dry()
