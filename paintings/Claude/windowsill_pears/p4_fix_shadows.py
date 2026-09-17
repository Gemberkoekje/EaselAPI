# Pass 4: sill greyer and straight, jambs cleaned, then the cast shadows (behind the pears).
p = s.palette
p["sill"] = p.desaturate(p["sill"], 0.5)
print("sill now", p.hex(p["sill"]), "value", round(p.value_of(p["sill"]), 2))
n0 = s.stroke_count
s.dry()
print("dry counted as strokes:", s.stroke_count - n0)
s.block_in(Region(-0.02, 0.585, 1.02, 0.775), "flat", "sill", density=1.0, size=0.09,
           direction=2, load=1.0, overhang=0, note="sill, greyer and straight")
# jambs: pane laid up to the line from inside, wall laid up to it from outside
s.stroke([(0.19, -0.02), (0.19, 0.58)], "flat", "window", size=0.06, pressure="even",
         load=1.0, note="left jamb, pane side")
s.stroke([(0.125, -0.02), (0.125, 0.58)], "flat", "wall", size=0.06, pressure="even",
         load=1.0, note="left jamb, wall side")
s.stroke([(0.665, -0.02), (0.665, 0.58)], "flat", "window", size=0.05, pressure="even",
         load=1.0, note="right edge of pane")
# cast shadows on the sill: light comes from the back-left, so they fall toward us and right
s.dry()
sh = "sill_shadow"
s.stroke([(0.30, 0.66), (0.40, 0.695), (0.50, 0.715)], "round_hard", sh, size=0.055,
         pressure=[1.0, 0.85, 0.25], note="shadow of pear 1")
s.stroke([(0.45, 0.68), (0.55, 0.715), (0.63, 0.735)], "round_hard", sh, size=0.05,
         pressure=[1.0, 0.8, 0.2], note="shadow of pear 2")
s.stroke([(0.56, 0.665), (0.66, 0.70), (0.76, 0.72)], "round_hard", sh, size=0.06,
         pressure=[1.0, 0.8, 0.25], note="shadow of mug")
s.stroke([(0.34, 0.755), (0.46, 0.765), (0.56, 0.77)], "round_hard", sh, size=0.035,
         pressure=[0.9, 0.9, 0.2], note="shadow of the lying pear")
print("strokes:", s.stroke_count)
print(s.look(grid=True))
