import colorsys, math
from easel import Session
s = Session(64, 64, ground="toned_grey", seed=1, out_dir=".")
p = s.palette

def lab(hx):
    r, g, b = (int(hx[i:i+2], 16) / 255 for i in (1, 3, 5))
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
    X = 0.4124 * lin[0] + 0.3576 * lin[1] + 0.1805 * lin[2]
    Y = 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
    Z = 0.0193 * lin[0] + 0.1192 * lin[1] + 0.9505 * lin[2]
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(X / 0.95047), f(Y), f(Z / 1.08883)
    L, a, bb = 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)
    return L, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360

def row(name, c):
    hx = p.hex(c)
    r, g, b = (int(hx[i:i+2], 16) / 255 for i in (1, 3, 5))
    h, _, _ = colorsys.rgb_to_hsv(r, g, b)
    L, C, H = lab(hx)
    print(f"{name:44s} {hx}  value {p.value_of(c):.2f}  chroma {p.chroma_of(c):.3f}  HSV hue {h*360:5.0f}  LCh C {C:5.1f} h {H:5.0f}")

row("burnt_umber", "burnt_umber")
row("ultramarine", "ultramarine")
print("-- umber + ultramarine share, at value 0.44")
for t in (0.10, 0.12, 0.15, 0.18, 0.20, 0.22, 0.25, 0.30, 0.35):
    row(f"umber+ultra {t:.2f} @0.44", p.at_value(p.mix("burnt_umber", "ultramarine", t), 0.44))
print("-- white before at_value (doorway_wall stone)")
row("(umber+ultra .18)+white .2 @0.40", p.at_value(p.mix(p.mix("burnt_umber", "ultramarine", 0.18), "titanium_white", 0.2), 0.40))
row("umber+ultra .18 @0.40 (no white)", p.at_value(p.mix("burnt_umber", "ultramarine", 0.18), 0.40))
row("(umber+ultra .25)+white .5 @0.44", p.at_value(p.mix(p.mix("burnt_umber", "ultramarine", 0.25), "titanium_white", 0.5), 0.44))
print("-- shipped mixtures")
row("beyond stone: ultra .25 @0.44", p.at_value(p.mix("burnt_umber", "ultramarine", 0.25), 0.44))
row("beyond stone_shade: ultra .30 @0.34", p.at_value(p.mix("burnt_umber", "ultramarine", 0.3), 0.34))
row("beyond floor: ultra .20 @0.20", p.at_value(p.mix("burnt_umber", "ultramarine", 0.2), 0.20))
row("wall plaster: umber+sienna .25 @0.27", p.at_value(p.mix("burnt_umber", "burnt_sienna", 0.25), 0.27))
row("wall plaster_dark: ultra .25 @0.17", p.at_value(p.mix("burnt_umber", "ultramarine", 0.25), 0.17))
for u in (0.04, 0.09):
    row(f"wall voussoir: ochre .3, ultra {u}, white @0.40", p.at_value(p.mix(p.mix(p.mix("burnt_umber", "yellow_ochre", 0.3), "ultramarine", u), "titanium_white", 0.22), 0.40))
print("-- p0.py (first beyond drawing)")
row("p0 stone: white+umber .35 @0.46", p.at_value(p.mix("titanium_white", "burnt_umber", 0.35), 0.46))
print("-- swatch.py candidates")
row("umber+white", p.at_value(p.mix("burnt_umber", "titanium_white", 0.5), 0.47))
row("umber+ochre", p.at_value(p.mix("burnt_umber", "yellow_ochre", 0.25), 0.47))
row("umber+ultra(0.25)", p.at_value(p.mix("burnt_umber", "ultramarine", 0.25), 0.47))
row("umber+viridian", p.at_value(p.mix("burnt_umber", "viridian", 0.3), 0.47))
row("sienna+ultra", p.at_value(p.mix("burnt_sienna", "ultramarine", 0.5), 0.47))
row("wall joint: ultra .35 @0.18", p.at_value(p.mix("burnt_umber", "ultramarine", 0.35), 0.18))
row("beyond joint: ultra+umber .5 @0.26", p.at_value(p.mix("ultramarine", "burnt_umber", 0.5), 0.26))
row("counter seam / shelves shadow: ultra .30 @0.14", p.at_value(p.mix("burnt_umber", "ultramarine", 0.3), 0.14))
print("-- the arch stones' 22% white (doorway_wall.py:61, :69), with and without")
base = p.mix(p.mix("burnt_umber", "yellow_ochre", 0.3), "ultramarine", 0.06)
for v in (0.36, 0.40, 0.44):
    row(f"arch stone with white @{v}", p.at_value(p.mix(base, "titanium_white", 0.22), v))
    row(f"arch stone without white @{v}", p.at_value(base, v))
