"""Pass A4 - repair. The smudges pulled light into the dark left; paint over.
Grain again, wider and quieter, with load kept full so it is not dotted."""
p = s.palette
s.dry()

# the shadowed left, repainted over the smudge lobes
s.block_in(ellipse(Region(-0.24, -0.10, 0.20, 1.10)), "flat", "table_dark",
           direction=(86,), density=0.95, size=0.15, load=1.0)
s.block_in(ellipse(Region(0.10, -0.08, 0.34, 0.52), rotate=6), "flat",
           p.mix(p["table_dark"], p["table_base"], 0.55), direction=(80,),
           density=0.9, size=0.13, load=1.0)
print("after left:", s.stroke_count)

# the pale lobe left in the middle, knocked back toward the base tone
s.block_in(ellipse(Region(0.50, 0.02, 0.66, 0.66)), "flat",
           p.mix(p["table_base"], p["table_lit"], 0.35), direction=(84,),
           density=0.9, size=0.12, load=1.0)
print("after middle:", s.stroke_count)

# grain: wide quiet streaks, full load, low opacity
p["grain_d"] = p.desaturate(p.mix(p.mix("cadmium_yellow", "burnt_umber", 0.78),
                                  "titanium_white", 0.30), 0.35)
p["grain_l"] = p.desaturate(p.mix(p.mix("lemon_yellow", "burnt_umber", 0.60),
                                  "titanium_white", 0.72), 0.20)
grain = [
    ([(0.00, 0.11), (0.26, 0.06), (0.50, 0.02)], "grain_d", 0.040, 0.10),
    ([(0.00, 0.33), (0.30, 0.28), (0.56, 0.22)], "grain_l", 0.030, 0.09),
    ([(0.00, 0.52), (0.24, 0.49), (0.44, 0.45)], "grain_d", 0.045, 0.09),
    ([(0.00, 0.70), (0.20, 0.68), (0.38, 0.65)], "grain_l", 0.026, 0.10),
    ([(0.00, 0.88), (0.24, 0.86), (0.46, 0.83)], "grain_d", 0.050, 0.08),
    ([(0.66, 0.08), (0.86, 0.04), (1.00, 0.01)], "grain_d", 0.034, 0.10),
    ([(0.68, 0.26), (0.88, 0.21), (1.00, 0.18)], "grain_l", 0.028, 0.09),
    ([(0.66, 0.44), (0.88, 0.40), (1.00, 0.37)], "grain_d", 0.040, 0.09),
    ([(0.72, 0.62), (0.92, 0.58), (1.00, 0.56)], "grain_l", 0.030, 0.10),
    ([(0.60, 0.84), (0.84, 0.79), (1.00, 0.76)], "grain_d", 0.044, 0.08),
    ([(0.44, 1.00), (0.74, 0.95), (1.00, 0.91)], "grain_l", 0.032, 0.09),
]
for pts, col, sz, op in grain:
    s.stroke(pts, "bristle", col, size=sz, opacity=op, load=1.0,
             load_falloff=0.08, pressure="even", note="grain")

# two darker hairlines, the way a plank actually shows
s.stroke([(0.00, 0.26), (0.28, 0.21), (0.52, 0.155)], "liner", "grain_d",
         size=0.004, opacity=0.30, note="grain line")
s.stroke([(0.62, 0.52), (0.84, 0.48), (1.00, 0.455)], "liner", "grain_d",
         size=0.004, opacity=0.26, note="grain line")
s.stroke([(0.06, 0.62), (0.30, 0.59), (0.48, 0.56)], "liner", "grain_d",
         size=0.003, opacity=0.22, note="grain line")

print("strokes:", s.stroke_count)
print(s.look())
