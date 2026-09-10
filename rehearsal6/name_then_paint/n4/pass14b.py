exec(open("_pal.py").read())
exec(open("_geom.py").read())
exec(open("_pot.py").read())
_t2 = p.mix(p.mix("burnt_sienna", "cadmium_red", 0.18), "yellow_ochre", 0.22)
p["pot_lit"] = at(p.desaturate(p.mix(_t2, "cadmium_yellow", 0.12), 0.20), 0.555)
for x, y in [(0.556,0.4965),(0.590,0.4930),(0.628,0.4950),(0.664,0.4915),
             (0.694,0.4975),(0.610,0.5005),(0.650,0.4890)]:
    s.dab(x, y, "round_hard", "leaf_dk", size=0.013, press=2)
s.block_in(NEARLIP.inset(0.006), "flat", "pot_lit", direction=(2,), density=1.0,
           size=0.013, pressure="even", load=1.0)
print(s.stroke_count)
print(s.look(region="E4:G7"))
