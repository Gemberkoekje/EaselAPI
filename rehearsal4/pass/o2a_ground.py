"""own2, pass 1 - sunflower head, face on, filling a square.
Structure deliberately opposed to own1: one centre, everything radiating from
it, no horizon, no depth layering, no horizontals. Marks run outward, not across."""
import math
import random

p = s.palette
p["bg_dk"] = p.mix("viridian", "burnt_umber", 0.55)
p["bg_md"] = p.mix(p.mix("viridian", "burnt_umber", 0.30), "titanium_white", 0.16)
p["leaf"] = p.desaturate(p.mix(p.mix("viridian", "cadmium_yellow", 0.30),
                               "titanium_white", 0.14), 0.25)
p["leaf_l"] = p.mix(p["leaf"], "cadmium_yellow", 0.45)
for n in ("bg_dk", "bg_md", "leaf", "leaf_l"):
    print(f"{n:7s} {p.hex(p[n])} v={p.value_of(p[n]):.2f}")

CX, CY = 0.470, 0.450
rng = random.Random(9)

# the ground behind everything: dark, and turned off the canvas axes
s.block_in("all", "flat", "bg_dk", direction=(34, 124), density=1.0,
           size=0.20, load=1.0, load_falloff=0.2)
s.block_in(ellipse(Region(0.06, 0.02, 0.94, 0.90)).inset(0.09), "flat",
           "bg_md", direction=(38,), density=0.85, size=0.18, load=1.0)
print("ground:", s.stroke_count)

# leaves: four masses pushing in from the corners, each along its own axis
leaves = [([(0.02, 0.86), (0.20, 0.74), (0.36, 0.70)], 0.13),
          ([(0.98, 0.70), (0.82, 0.62), (0.68, 0.62)], 0.11),
          ([(0.14, 0.10), (0.26, 0.22), (0.34, 0.30)], 0.09),
          ([(0.92, 0.96), (0.74, 0.88), (0.62, 0.82)], 0.10)]
for pts, w in leaves:
    lf = ribbon(pts, w, end_width=w * 0.35)
    s.block_in(lf.inset(0.022), "flat", "leaf", direction="axis",
               density=1.0, size=0.045, load=1.0)
print("leaves:", s.stroke_count)
for pts, w in leaves:
    s.stroke(pts, "liner", "leaf_l", size=0.005, pressure=[0.9, 0.6, 0.15],
             note="leaf vein")
print("strokes:", s.stroke_count)
print(s.look())
