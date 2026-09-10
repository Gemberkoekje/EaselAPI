p = s.palette

def cool(ratio, t):          # ultramarine+burnt_sienna = neutral grey; low ratio = cooler
    return p.tint(p.mix("ultramarine", "burnt_sienna", ratio), t)

p["sky_mid"]  = cool(0.44, 0.875)
p["sky_core"] = cool(0.52, 0.945)
p["sky_top"]  = cool(0.32, 0.795)

for n in ("sky_top", "sky_mid", "sky_core"):
    print(f"{n:9s} {p.hex(p[n])}  v={p.value_of(p[n]):.3f}")

# the whole window field, crossed diagonals so the canvas axes stay out of it
s.block_in(span("A1", "H6"), "flat", "sky_mid", direction=(-26, 54),
           density=0.9, size=0.18, load=1.0)

# where the low sun sits: lower left of the glass
s.block_in(ellipse(span("A4", "E7")), "flat", "sky_core", direction=(-18, 62),
           density=0.85, size=0.11, load=1.0)

# colder top right corner
s.block_in(polygon([(0.52, 0.0), (1.0, 0.0), (1.0, 0.34), (0.66, 0.05)]),
           "flat", "sky_top", direction=(-40, 40), density=0.85, size=0.09, load=1.0)

print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
