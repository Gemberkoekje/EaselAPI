p = s.palette
WHITE = "titanium_white"


def to_value(base, target):
    """The mixture of `base` and white that reads `target`."""
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["sky_a"] = to_value(p.mix("ultramarine", "cerulean", 0.55), 0.48)
p["sky_b"] = to_value(p.mix("cerulean", "alizarin", 0.22), 0.60)
p["sky_c"] = to_value(p.mix("cerulean", "cadmium_red", 0.50), 0.71)
p["sky_d"] = to_value(p.mix("yellow_ochre", "cadmium_red", 0.28), 0.82)
for n in ("sky_a", "sky_b", "sky_c", "sky_d"):
    print(f"{n}  {p.hex(p[n])}  {p.value_of(p[n]):.2f}")

s.dry()

bands = [
    (ribbon([(0.00, 0.075), (0.38, 0.055), (1.00, 0.090)], 0.175), "sky_a", 0.11),
    (ribbon([(0.00, 0.208), (0.44, 0.228), (1.00, 0.203)], 0.115), "sky_b", 0.08),
    (ribbon([(0.00, 0.288), (0.52, 0.276), (1.00, 0.293)], 0.085), "sky_c", 0.06),
    (ribbon([(0.00, 0.341), (0.46, 0.334), (1.00, 0.346)], 0.062), "sky_d", 0.045),
]
for sh, col, sz in bands:
    s.block_in(sh, "flat", col, direction="axis", density=0.95,
               size=sz, load=1.0, load_falloff=0.25, pressure="even")

# lose the joins - small, few, and not evenly spaced
s.smudge([(0.09, 0.150), (0.27, 0.163)], size=0.038)
s.smudge([(0.55, 0.158), (0.71, 0.150)], size=0.038)
s.smudge([(0.31, 0.263), (0.47, 0.256)], size=0.035)
s.smudge([(0.74, 0.259), (0.93, 0.266)], size=0.035)
s.smudge([(0.17, 0.313), (0.36, 0.318)], size=0.032)
s.smudge([(0.63, 0.316), (0.85, 0.310)], size=0.032)

print("strokes", s.stroke_count)
print(s.look())
print(s.look(values=True))
