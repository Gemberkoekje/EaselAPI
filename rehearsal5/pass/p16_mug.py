REF = "C:/temp/Level1.jpg"
p = s.palette

WARM_DARK = p.mix("ultramarine", "burnt_umber", 0.72)
CERAMIC = p.mix(p.mix("ultramarine", "burnt_umber", 0.42), "cerulean", 0.22)

def val(target, base=CERAMIC):
    other = "titanium_white" if p.value_of(base) < target else WARM_DARK
    up = p.value_of(base) < target
    lo, hi = 0.0, 1.0
    for _ in range(26):
        mid = (lo + hi) / 2
        if (p.value_of(p.mix(base, other, mid)) < target) == up:
            lo = mid
        else:
            hi = mid
    c = p.mix(base, other, (lo + hi) / 2)
    if abs(p.value_of(c) - target) > 0.01:
        print(f"   !! wanted {target} got {p.value_of(c):.3f}")
    return c

p["mug_mid"]  = val(0.500)
p["mug_dark"] = val(0.435)
p["mug_lit"]  = val(0.585)
p["mug_hi"]   = val(0.660)
p["mug_spec"] = val(0.745)
p["tea"]      = val(0.140, base=p.mix("burnt_umber", "ultramarine", 0.28))
p["tea_lit"]  = val(0.255, base=p.mix("burnt_umber", "ultramarine", 0.28))
for n in ("mug_dark", "mug_mid", "mug_lit", "mug_hi", "mug_spec", "tea", "tea_lit"):
    print(f"{n:<9} {p.hex(p[n])} v={p.value_of(p[n]):.3f}")

rim  = ellipse((0.474, 0.226), 0.167, 0.110, rotate=5)
tea  = ellipse((0.470, 0.244), 0.132, 0.077, rotate=5)
body = polygon([(0.307, 0.224), (0.352, 0.292), (0.412, 0.327), (0.474, 0.337),
                (0.545, 0.324), (0.605, 0.289), (0.641, 0.230),
                (0.596, 0.440), (0.548, 0.630), (0.510, 0.652), (0.456, 0.663),
                (0.400, 0.652), (0.364, 0.624), (0.334, 0.425)])
handle = ribbon([(0.641, 0.276), (0.682, 0.300), (0.706, 0.352), (0.708, 0.412),
                 (0.682, 0.468), (0.630, 0.502), (0.598, 0.508)], 0.033)
figure = polygon([(0.360, 0.470), (0.374, 0.432), (0.402, 0.412), (0.448, 0.406),
                  (0.492, 0.418), (0.508, 0.452), (0.512, 0.560), (0.504, 0.598),
                  (0.362, 0.598)])
pack = polygon([(0.508, 0.462), (0.556, 0.472), (0.560, 0.548), (0.506, 0.562)])

# the drawing was wrong about the handle, the figure and the spoon: erase, redraw
s.erase()
for shape in (rim, tea, body, handle, figure, pack):
    s.pencil(shape.closed, pressure=0.6)
s.pencil([(0.533, 0.000), (0.512, 0.140), (0.496, 0.268)], pressure=0.7)
s.pencil([(0.560, 0.000), (0.535, 0.140), (0.520, 0.268)], pressure=0.7)
s.pencil([(0.492, 0.272), (0.516, 0.318), (0.534, 0.352)], pressure=0.5)

# ---- the hollow thing, in its three depths ------------------------------
s.block_in(rim.inset(0.027), "flat", "mug_lit", direction="axis", density=0.9,
           size=0.055, load=1.0, note="far rim")
print("rim", s.stroke_count)
s.block_in(tea.inset(0.024), "flat", "tea", direction=5, density=1.0,
           size=0.048, load=1.0, note="the inside")
print("tea", s.stroke_count)
s.block_in(body.inset(0.032), "flat", "mug_mid", direction="axis", density=0.9,
           size=0.065, load=1.0, note="near wall")
print("body", s.stroke_count)

print(s.look(reference=REF))
print(s.look(region=span("C2", "F5"), reference=REF))
