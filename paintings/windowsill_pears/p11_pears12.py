exec(open("helpers.py").read())
exec(open("pears.py").read())
s.dry()
for name in ("pear1", "pear2"):
    plan = pear_plan(name) + [stem_plan(name)]
    print(name, "cost", s.cost(plan))
    run_plan(plan)
print("strokes:", s.stroke_count)
print(s.look(region="B3:F7"))
plan3 = pear_plan("pear3") + [stem_plan("pear3")]
print("pear3 cost", s.cost(plan3))
print(s.rehearse(plan3, region="B4:F7"))
