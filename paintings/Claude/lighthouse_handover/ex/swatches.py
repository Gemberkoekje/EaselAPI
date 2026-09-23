import os
from easel import Session, Region
W = os.path.dirname(os.path.abspath(__file__)); os.chdir(W)
s = Session(1200, 260, ground="burnt_sienna", seed=9, out_dir=W)
p = s.palette
plan = {
 "zenith":  p.at_value(p.mix("ultramarine", "alizarin", 0.25), 0.34),
 "high":    p.at_value(p.mix("ultramarine", "cerulean", 0.5), 0.45),
 "pale":    p.at_value(p.mix("cerulean", "titanium_white", 0.7), 0.58),
 "low":     p.at_value(p.mix("yellow_ochre", "alizarin", 0.15), 0.66),
 "glow":    p.at_value(p.mix("cadmium_yellow", "cadmium_red", 0.35), 0.72),
 "core":    p.at_value(p.mix("cadmium_yellow", "titanium_white", 0.5), 0.82),
 "sea_far": p.at_value(p.mix("ultramarine", "burnt_umber", 0.3), 0.44),
 "sea_near":p.at_value(p.mix("ultramarine", "burnt_umber", 0.4), 0.26),
 "land":    p.at_value(p.mix("burnt_umber", "ultramarine", 0.5), 0.15),
 "grass":   p.at_value(p.mix("burnt_umber", "viridian", 0.3), 0.20),
 "lit":     p.at_value(p.mix("burnt_sienna", "yellow_ochre", 0.4), 0.30),
 "tower":   p.at_value(p.mix("ultramarine", "burnt_umber", 0.4), 0.28),
 "rim":     p.at_value(p.mix("cadmium_red", "yellow_ochre", 0.5), 0.52),
 "lamp":    p.at_value(p.mix("titanium_white", "cadmium_yellow", 0.12), 0.93),
}
n = len(plan); w = 1.0 / n
for i, (name, c) in enumerate(plan.items()):
    s.block_in(Region(i * w + 0.004, 0.10, (i + 1) * w - 0.004, 0.90), "flat", c, size=0.012, solid=True)
    print(f"{name:9s} value {p.value_of(c):.2f}  chroma {p.chroma_of(c):.3f}  {p.hex(c)}")
s.look(path=f"{W}/ex9_swatches.png")
s.look(values=True, path=f"{W}/ex9_swatches_values.png")
