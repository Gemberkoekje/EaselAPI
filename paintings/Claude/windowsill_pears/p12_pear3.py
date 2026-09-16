exec(open("helpers.py").read())
exec(open("pears.py").read())
s.dry()
plan3 = pear_plan("pear3") + [stem_plan("pear3")]
plan3[3]["size"] = 0.011
plan3[3]["pressure"] = [0.15, 0.5, 0.9, 1.0, 0.7, 0.35, 0.1]
print("pear3 cost", s.cost(plan3))
run_plan(plan3)
print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
