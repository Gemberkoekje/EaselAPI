exec(open("helpers.py").read())
exec(open("pears.py").read())
p = s.palette
# under the pears: the pane smear, and the mug's ribs
s.stroke([(0.49, 0.512), (0.24, 0.512)], "flat", "window", size=0.035, pressure="even",
         load=1.0, load_falloff=0.0, note="pane smear covered")
s.stroke([(0.556, 0.44), (0.552, 0.665)], "round_hard", "mug", size=0.04, pressure="even",
         load=1.0, note="mug face, ribs quietened")
s.dry()
paint_pear("pear1")
top = TOPS["pear1"]
s.stroke([top, (top[0] + 0.006, top[1] - 0.02), (top[0] + 0.004, top[1] - 0.04)], "liner", "dark",
         size=0.006, pressure=[1.0, 0.8, 0.5], load=1.0, note="pear1 stem")
print("strokes:", s.stroke_count)
print(s.look(region="B3:F7"))
