# pass 5, take two -- corners yes, foreground band only, pool untouched
tl = polygon([(-0.02, -0.02), (0.30, -0.02), (0.30, 0.14), (0.10, 0.30), (-0.02, 0.30)])
tr = polygon([(1.02, -0.02), (0.72, -0.02), (0.72, 0.16), (0.92, 0.32), (1.02, 0.32)])
s.block_in(tl, "flat", p["room"], size=0.12, density=0.6, opacity=0.8, direction=-30)
s.block_in(tr, "flat", p["room"], size=0.12, density=0.6, opacity=0.8, direction=-28)
s.block_in(fore, "flat", p["fore"], size=0.10, density=0.7, opacity=0.7,
           direction=2)                                     # the floor, not the pool

# a whisper more light pooled behind the text block
s.glaze([(0.40, 0.35), (0.51, 0.34), (0.61, 0.35)], p["glow_mid"], opacity=0.16,
        size=0.12, pressure=[0.3, 1.0, 0.3], brush="round_soft")

# the stand catches one dim bounce on its left edge
s.stroke([(0.481, 0.60), (0.484, 0.64)], "liner", p.at_value(p["key_rim"], 0.30),
         size=0.004, load=0.4, opacity=0.6)

# break the keyboard's bottom edge in one stretch: paint across it, starved
s.stroke([(0.46, 0.733), (0.55, 0.736), (0.63, 0.734)], "bristle", p.at_value(p["pool_b"], 0.30),
         size=0.028, load=0.55, opacity=0.5, pressure="swell")
s.look()
