# Pass 23: diagnosis only. The eleven "coat" bands came out LIGHTER, not darker.
REF = "C:/temp/Level3.jpg"
p = s.palette
p["coat"]     = p.shade(p.mix("ultramarine", "burnt_umber", 0.62), 0.55)
p["coat_lit"] = p.mix(p.mix("ultramarine", "burnt_umber", 0.55), "titanium_white", 0.11)
print("coat     ", p.hex(p["coat"]), round(p.value_of(p["coat"]), 3))
print("coat_lit ", p.hex(p["coat_lit"]), round(p.value_of(p["coat_lit"]), 3))
log = s.log()
print(log[-2600:] if isinstance(log, str) else log)
print("coat crop:", s.look(region=span("F5", "G7"), reference=REF))
print(s.compare(REF, region=span("F5", "G7")))
