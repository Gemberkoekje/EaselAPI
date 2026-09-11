# Pass 5: cover the leftover orange band above the sill; lighter, warmer cast shadows.
exec(open("helpers.py").read())
p = s.palette
# the band, each part in the colour of what is actually there
s.stroke([(0.155, 0.565), (0.67, 0.565)], "flat", "window", size=0.05, pressure="even",
         load=1.0, note="pane down to the sill")
s.stroke([(-0.03, 0.565), (0.145, 0.565)], "flat", "wall", size=0.05, pressure="even",
         load=1.0, note="wall down to the sill")
s.stroke([(0.665, 0.565), (0.745, 0.565)], "flat", "wall", size=0.05, pressure="even",
         load=1.0, note="jamb down to the sill")
s.stroke([(0.72, 0.565), (1.03, 0.565)], "flat", "curtain", size=0.05, pressure="even",
         load=1.0, note="curtain down to the sill")
# the sill's front face: a step darker than its top
p["sill_face"] = to_value(p["sill"], 0.50)
s.stroke([(-0.03, 0.787), (1.03, 0.787)], "flat", "sill_face", size=0.028, pressure="even",
         load=1.0, note="sill front edge")
# cast shadows again, two steps lighter and warmer, covering the dark ones
p["cast"] = to_value(p.mix(p["sill"], p.mix("burnt_umber", "ultramarine", 0.35), 0.5), 0.45)
print("cast", p.hex(p["cast"]), round(p.value_of(p["cast"]), 2))
s.dry()
s.stroke([(0.30, 0.66), (0.40, 0.695), (0.50, 0.715)], "round_hard", "cast", size=0.065,
         pressure=[1.0, 0.9, 0.35], load=1.0, note="shadow of pear 1")
s.stroke([(0.45, 0.68), (0.55, 0.715), (0.635, 0.735)], "round_hard", "cast", size=0.06,
         pressure=[1.0, 0.85, 0.3], load=1.0, note="shadow of pear 2")
s.stroke([(0.56, 0.665), (0.66, 0.70), (0.765, 0.72)], "round_hard", "cast", size=0.07,
         pressure=[1.0, 0.85, 0.35], load=1.0, note="shadow of mug")
s.stroke([(0.34, 0.755), (0.46, 0.765), (0.565, 0.77)], "round_hard", "cast", size=0.045,
         pressure=[1.0, 0.9, 0.3], load=1.0, note="shadow of the lying pear")
print("strokes:", s.stroke_count)
print(s.look(grid=True))
