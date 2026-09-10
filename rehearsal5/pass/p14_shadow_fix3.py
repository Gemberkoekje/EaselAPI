REF = "C:/temp/Level1.jpg"
p = s.palette

WARM_DARK = p.mix("ultramarine", "burnt_umber", 0.72)
WOOD = p.desaturate(p.mix("burnt_umber", "yellow_ochre", 0.38), 0.22)

def val(target, base=None, warm=True):
    """A mixture that really reads `target` - white above the base, umber-blue
    below it.  Prints and asserts, because both searches clamped silently."""
    base = WOOD if base is None else base
    other = "titanium_white" if p.value_of(base) < target else WARM_DARK
    lo, hi = 0.0, 1.0
    up = p.value_of(base) < target
    for _ in range(26):
        mid = (lo + hi) / 2
        v = p.value_of(p.mix(base, other, mid))
        if (v < target) == up:
            lo = mid
        else:
            hi = mid
    c = p.mix(base, other, (lo + hi) / 2)
    got = p.value_of(c)
    if abs(got - target) > 0.01:
        print(f"   !! wanted {target} got {got:.3f} ({p.hex(c)})")
    return c

p["shad_pen"]  = val(0.335)
p["shad_core"] = val(0.175)
p["shad_pool"] = val(0.140)
p["shad_ring"] = val(0.350)
for n in ("shad_pen", "shad_core", "shad_pool", "shad_ring"):
    print(f"{n:<11} {p.hex(p[n])} v={p.value_of(p[n]):.3f}")

s.dry()
pen = ellipse((0.462, 0.700), 0.178, 0.176)
s.block_in(pen.inset(0.035), "flat", "shad_pen", direction=-16, density=0.85,
           size=0.070, load=1.0, note="penumbra 3")
print("pen", s.stroke_count)

core = blob((0.462, 0.700), 0.152, 0.150, wobble=0.20, seed=6)
s.block_in(core.inset(0.036), "flat", "shad_core", direction=34, density=1.0,
           size=0.075, load=1.0, note="core 3")
print("core", s.stroke_count)

for pts, size in [([(0.360, 0.646), (0.448, 0.678), (0.528, 0.662)], 0.055),
                  ([(0.528, 0.700), (0.436, 0.716), (0.366, 0.696)], 0.048),
                  ([(0.396, 0.740), (0.476, 0.744), (0.528, 0.724)], 0.038)]:
    s.stroke(pts, "round_hard", "shad_pool", size=size, pressure="swell",
             load=1.0, note="deeper under the mug")
print("pool", s.stroke_count)

for pts, size in [([(0.598, 0.556), (0.618, 0.542), (0.645, 0.539), (0.668, 0.549)], 0.015),
                  ([(0.668, 0.549), (0.679, 0.566), (0.674, 0.586)], 0.013),
                  ([(0.672, 0.589), (0.650, 0.601), (0.622, 0.600), (0.603, 0.588)], 0.015)]:
    s.stroke(pts, "round_hard", "shad_ring", size=size, pressure="swell",
             load=1.0, note="handle shadow 2")
print("ring", s.stroke_count)

print(s.look(region=span("C5", "G7"), reference=REF))
print(s.look(reference=REF))
