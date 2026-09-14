from easel import Session, cell
s = Session(900, 600, ground="toned_grey", seed=7)
s.mark("a", *cell("C3").point(0.5, 0.5))
s.mark("b", *cell("F3").point(0.5, 0.5))
s.mark("c", *cell("D6").point(0.5, 0.5))
s.pencil([s.pt("a"), s.pt("b"), s.pt("c"), s.pt("a")], pressure=0.7)
print("drawing:", s.look())
plan = [{"points": [s.pt("a"), s.pt("c")], "brush": "bristle", "size": 0.09,
         "color": "titanium_white"}]
print("rehearse A:", s.rehearse(plan, region="C3:F6"))
print("rehearse B:", s.rehearse([dict(plan[0], size=0.03, brush="liner")], region="C3:F6"))
s.stroke(**plan[0])
print("painted:", s.look(region="C3:F6"))
print("strokes:", s.stroke_count, "log entries:", len(s.log()))
