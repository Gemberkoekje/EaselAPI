from easel import Session
from PIL import Image
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

for g in ("white","warm_white","toned_grey","toned_warm_grey","burnt_sienna","umber_wash","cool_grey"):
    s = Session(200, 200, texture="linen", ground=g, seed=1)
    p = f"g_{g}.png"
    s.export(p)
    im = Image.open(p).convert("RGB")
    px = list(im.getdata())
    n = len(px)
    r = sum(q[0] for q in px)/n/255
    gg = sum(q[1] for q in px)/n/255
    b = sum(q[2] for q in px)/n/255
    lum = 0.2126*r + 0.7152*gg + 0.0722*b
    print(f"{g:18s} rgb=({r:.3f},{gg:.3f},{b:.3f})  approx-value={lum:.3f}")

s = Session(200,200,seed=1)
p = s.palette
def show(name, c):
    print(f"{name:22s} {p.hex(c)}  v={p.value_of(c):.3f}")

print()
show("bg_cool",    p.mix("ultramarine","burnt_umber",0.45))
show("bg_warm",    p.mix("ultramarine","burnt_umber",0.70))
show("bg_glow",    p.tint(p.mix("ultramarine","burnt_umber",0.72),0.22))
show("bg_glow2",   p.tint(p.mix("burnt_umber","yellow_ochre",0.30),0.18))
print()
show("terra_base", p.mix("burnt_sienna","cadmium_red",0.30))
show("terra_lit",  p.tint(p.mix("burnt_sienna","cadmium_red",0.30),0.38))
show("terra_lit2", p.tint(p.mix(p.mix("burnt_sienna","cadmium_red",0.30),"yellow_ochre",0.25),0.42))
show("terra_shad", p.mix(p.mix("burnt_sienna","cadmium_red",0.3),"ultramarine",0.35))
print()
show("wood",       p.mix("burnt_umber","burnt_sienna",0.45))
show("wood_lit",   p.tint(p.mix("burnt_umber","burnt_sienna",0.45),0.35))
show("wood_lit2",  p.tint(p.mix(p.mix("burnt_umber","burnt_sienna",0.5),"yellow_ochre",0.3),0.40))
show("wood_dark",  p.mix(p.mix("burnt_umber","burnt_sienna",0.4),"ultramarine",0.30))
print()
show("leaf_dark",  p.mix("viridian","burnt_umber",0.55))
show("leaf_mid",   p.mix(p.mix("viridian","yellow_ochre",0.40),"burnt_umber",0.25))
show("leaf_lit",   p.tint(p.mix("viridian","yellow_ochre",0.55),0.30))
print()
show("petal_shad", p.tint(p.mix("ultramarine","burnt_sienna",0.50),0.70))
show("petal_shad2",p.tint(p.mix("ultramarine","burnt_umber",0.55),0.76))
show("petal_mid",  p.tint(p.mix("yellow_ochre","cerulean",0.18),0.80))
show("petal_mid2", p.tint(p.mix("burnt_umber","yellow_ochre",0.5),0.86))
show("petal_lit",  p.tint(p.mix("titanium_white","yellow_ochre",0.06),0.0))
show("white",      "titanium_white")
show("petal_warm", p.mix("titanium_white","yellow_ochre",0.10))
show("petal_pink", p.mix("titanium_white","alizarin",0.05))
