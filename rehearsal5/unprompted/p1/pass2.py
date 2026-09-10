p = s.palette
p["sky_mid"] = p.tint(p.mix("cerulean", "cadmium_red", 0.30), 0.52)
p["sky_low"] = p.tint(p.mix("yellow_ochre", "cadmium_red", 0.30), 0.60)
for n in ("sky_high", "sky_mid", "sky_low"):
    print(f"{n:9s} {p.hex(p[n])}  {p.value_of(p[n]):.2f}")

s.dry()

# three steps of sky, top to horizon, each a ribbon on a line of its own
top = ribbon([(0.00, 0.085), (0.42, 0.055), (1.00, 0.095)], 0.155)
mid = ribbon([(0.00, 0.215), (0.46, 0.245), (1.00, 0.225)], 0.100)
low = ribbon([(0.00, 0.330), (0.50, 0.312), (1.00, 0.322)], 0.062)

s.block_in(top, "flat", "sky_high", direction="axis", density=0.95,
           size=0.10, load=1.0, load_falloff=0.25, pressure="even")
s.block_in(mid, "flat", "sky_mid", direction="axis", density=0.95,
           size=0.07, load=1.0, load_falloff=0.25, pressure="even")
s.block_in(low, "flat", "sky_low", direction="axis", density=0.95,
           size=0.05, load=1.0, load_falloff=0.25, pressure="even")

# lose the two joins while the paint is still wet
s.smudge([(0.14, 0.168), (0.30, 0.158)], size=0.04)
s.smudge([(0.62, 0.172), (0.80, 0.166)], size=0.04)
s.smudge([(0.20, 0.283), (0.38, 0.290)], size=0.04)
s.smudge([(0.66, 0.286), (0.86, 0.281)], size=0.04)

print("strokes", s.stroke_count)
print(s.look(grid=True))
