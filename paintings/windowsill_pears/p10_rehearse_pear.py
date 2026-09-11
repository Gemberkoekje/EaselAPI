exec(open("helpers.py").read())
exec(open("pears.py").read())
p = s.palette
p["pear_rim"] = to_value(p.mix(p["pear_lit"], p["pear_body"], 0.22), 0.63)
print("pear_rim", p.hex(p["pear_rim"]), round(p.value_of(p["pear_rim"]), 2))
plan = pear_plan("pear1") + [stem_plan("pear1")]
for item in plan:
    print(item["label"], s.cost(item))
print("cost", s.cost(plan))
print(s.rehearse(plan, region="B3:E7"))
