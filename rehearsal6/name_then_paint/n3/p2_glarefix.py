p = s.palette
def cool(ratio, t):
    return p.tint(p.mix("ultramarine", "burnt_sienna", ratio), t)

p["sky_top"]  = p.desaturate(cool(0.40, 0.815), 0.35)   # cold corner, less blue
p["sky_step"] = cool(0.48, 0.912)                        # between mid and core
p["sky_step2"]= cool(0.38, 0.845)                        # between mid and top
p["sky_hot"]  = cool(0.56, 0.972)
for n in ("sky_top", "sky_step2", "sky_step", "sky_hot"):
    print(f"{n:9s} {p.hex(p[n])}  v={p.value_of(p[n]):.3f}")

core = ellipse(span("A4", "E7"))
wedge = polygon([(0.46, 0.0), (1.0, 0.0), (1.0, 0.40), (0.62, 0.05)])

# cold corner again, wider and greyer, over the blue
s.block_in(wedge, "flat", "sky_top", direction=(-42, 38), density=0.85, size=0.10, load=1.0)
# a band straddling each join, so the step becomes three steps
s.sweep(wedge.scaled(1.06), "flat", "sky_step2", depth=0.15, size=0.10, cross=24, load=1.0)
s.sweep(core.scaled(1.14), "flat", "sky_step", depth=0.17, size=0.10, cross=24, load=1.0)
# a hot centre so the glare has somewhere to peak
s.block_in(ellipse(span("A5", "C6")).scaled(1.15), "flat", "sky_hot",
           direction=(-14, 66), density=0.8, size=0.07, load=1.0)

# walk the remaining joins while the paint is wet
for a, b in [((0.60, 0.19), (0.72, 0.28)), ((0.86, 0.10), (0.93, 0.20)),
             ((0.05, 0.34), (0.13, 0.40)), ((0.44, 0.30), (0.52, 0.38)),
             ((0.58, 0.52), (0.66, 0.47)), ((0.30, 0.70), (0.38, 0.66))]:
    s.smudge([a, b], size=0.042)

print("strokes:", s.stroke_count)
print(s.look())
