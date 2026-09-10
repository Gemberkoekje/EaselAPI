# --- 1. the sky, furthest, laid on a slope so the canvas doesn't choose the angle
s.block_in(span("A1","H5"), "bristle", "sky", direction=(9,-14), density=0.75,
           size=0.155, load=1.0)
print("sky", s.stroke_count)
# --- 2. the gap of light sitting on the horizon, low and to the right
s.block_in(ellipse(span("D5","H6")).shifted(0.02,0.02), "round_hard", "glow",
           direction=-6, density=0.85, size=0.085, load=1.0, pressure="even")
s.block_in(ellipse(span("F5","H6")).inset(0.02), "round_hard", "glow2",
           direction=-8, density=0.9, size=0.055, load=1.0, pressure="even")
s.stroke([(0.735,0.660),(0.815,0.652),(0.880,0.660)], "round_hard", "blaze",
         size=0.045, load=1.0, pressure="swell")
print("glow", s.stroke_count)
# --- 3. the water: one field, then the dark end and the light end
s.block_in(span("A6","H8"), "bristle", "water_m", direction=(-3,6), density=0.8,
           size=0.13, load=1.0)
s.block_in(polygon([(-0.02,0.700),(0.42,0.700),(0.30,1.02),(-0.02,1.02)]), "bristle",
           "water_d", direction=(-6), density=0.85, size=0.085, load=1.0)
print("water", s.stroke_count)
print(s.look())
