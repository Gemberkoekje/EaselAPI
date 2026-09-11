exec(open("helpers.py").read())
exec(open("pears.py").read())
p = s.palette
p["pear_body"] = to_value(p.mix(p.mix("yellow_ochre", "viridian", 0.30), "burnt_umber", 0.30), 0.34)
p["pear_reflect"] = to_value(p.mix(p.mix("yellow_ochre", "viridian", 0.18), "burnt_sienna", 0.25), 0.44)
for k in ("pear_body", "pear_reflect", "pear_lit"):
    print(k, p.hex(p[k]), round(p.value_of(p[k]), 2))
plan = pear_plan("pear1") + [stem_plan("pear1")]
print("cost", s.cost(plan))
print(s.rehearse(plan, region="B3:E7"))
