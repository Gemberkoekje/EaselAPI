# Pass 3 - scrap the bullseye. One dark field with an asymmetric warm drift.
p = s.palette
s.dry()

# cover everything above the table, ripples and lobes and all
s.block_in(polygon([(0.0,0.0),(1.0,0.0),(1.0,0.79),(0.0,0.76)]), "bristle", "bg",
           direction=(58, 142), density=1.0, size=0.15, load=1.0, load_falloff=0.16)

# an off-centre warm drift, laid along its own axis, no closed oval anywhere
s.block_in(ribbon([(0.02, 0.16), (0.30, 0.27), (0.60, 0.41)], 0.34), "bristle", "bg_1",
           direction="axis", density=0.85, size=0.12, load=1.0)
s.block_in(ribbon([(0.10, 0.13), (0.34, 0.24), (0.55, 0.34)], 0.20), "bristle", "bg_2",
           direction="axis", density=0.80, size=0.10, load=1.0)
s.block_in(ribbon([(0.16, 0.15), (0.38, 0.26)], 0.11), "bristle", "bg_3",
           direction="axis", density=0.70, size=0.075, load=0.95)
# a cooler counter-note top right so the field is not one temperature
s.block_in(ribbon([(0.72, 0.02), (0.99, 0.20)], 0.26), "bristle", "bg_cool",
           direction="axis", density=0.7, size=0.11, load=0.9)

# --- the table again, on top of that ------------------------------------------
s.dry()
tbl_mass = polygon([(0.0, 0.700), (0.40, 0.712), (1.0, 0.729), (1.0, 1.0), (0.0, 1.0)])
s.block_in(tbl_mass, "flat", "tbl", direction=(6, 168), density=1.0, size=0.10,
           load=1.0, pressure="even")
s.block_in(blob(Region(0.02, 0.83, 0.50, 1.00), wobble=0.32, seed=4), "bristle",
           "tbl_lit", direction=(9, 163), density=0.9, size=0.085, load=1.0)
s.block_in(polygon([(0.68, 0.723), (1.0, 0.729), (1.0, 1.0), (0.84, 1.0)]), "flat",
           "tbl_dk", direction=(24, 140), density=1.0, size=0.09, load=1.0, pressure="even")

print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
