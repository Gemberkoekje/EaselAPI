REF = "C:/temp/Level1.jpg"
p = s.palette
WARM_DARK = p.mix("ultramarine", "burnt_umber", 0.72)

def val(target, base):
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
    if abs(p.value_of(c) - target) > 0.012:
        print(f"   !! wanted {target} got {p.value_of(c):.3f}")
    return c

BROWN = p.mix("burnt_umber", "ultramarine", 0.20)
p["fig_dark"] = val(0.140, BROWN)
p["fig_pack"] = val(0.180, BROWN)
p["spoon_d"]  = val(0.135, p.mix("ultramarine", "burnt_umber", 0.55))
for n in ("fig_dark", "fig_pack", "spoon_d"):
    print(f"{n:<9} {p.hex(p[n])} v={p.value_of(p[n]):.3f}")

# the crewmate: five columns, round tip so the head comes out round
for x, y0 in [(0.375, 0.441), (0.407, 0.418), (0.438, 0.407),
              (0.470, 0.412), (0.500, 0.433)]:
    s.stroke([(x, y0), (x + 0.004, 0.598)], "round_hard", "fig_dark",
             size=0.033, pressure="even", load=1.0, note="crewmate")
for x in (0.521, 0.546):
    s.stroke([(x, 0.450), (x, 0.534)], "round_hard", "fig_pack",
             size=0.030, pressure="even", load=1.0, note="backpack")
for x in (0.398, 0.452):
    s.stroke([(x, 0.594), (x, 0.626)], "round_hard", "fig_dark",
             size=0.029, pressure="even", load=1.0, note="leg")
print("figure", s.stroke_count)

s.stroke([(0.380, 0.456), (0.404, 0.448), (0.427, 0.444)], "round_hard",
         "mug_mid", size=0.017, pressure="swell", load=1.0, note="visor")
print("visor", s.stroke_count)

# the spoon
s.stroke([(0.535, 0.000), (0.514, 0.135), (0.498, 0.258)], "round_hard",
         "spoon_d", size=0.026, pressure="even", load=1.0, note="spoon handle")
s.stroke([(0.495, 0.264), (0.516, 0.308), (0.538, 0.348)], "round_hard",
         "mug_dark", size=0.022, pressure="swell", load=1.0, note="spoon bowl")
s.stroke([(0.528, 0.030), (0.512, 0.140)], "liner", "mug_dark",
         size=0.005, pressure="taper", load=1.0, note="spoon edge light")
print("spoon", s.stroke_count)

print(s.look(reference=REF))
print(s.look(region=span("C3", "F6"), reference=REF))
