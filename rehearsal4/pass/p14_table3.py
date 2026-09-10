"""Pass A5 - cover the shouting grain and lay the table one more time.
Lesson: low `opacity` on a LONG stroke still saturates to near full colour."""
p = s.palette
s.dry()

s.block_in("all", "flat", "table_base", direction=(8,), density=1.0,
           size=0.26, load=1.0, load_falloff=0.2)
print("base:", s.stroke_count)
s.block_in(ellipse(Region(0.55, 0.02, 0.95, 0.86), rotate=-12), "flat",
           "table_lit", direction=(-72,), density=0.95, size=0.20, load=1.0)
s.block_in(ellipse(Region(0.30, 0.74, 0.84, 1.08)), "flat", "table_lit",
           direction=(-8,), density=0.95, size=0.18, load=1.0)
s.block_in(ellipse(Region(0.62, 0.28, 0.86, 0.76), rotate=-10), "flat",
           "table_glow", direction=(-78,), density=0.9, size=0.16, load=1.0)
print("lit:", s.stroke_count)
s.block_in(ellipse(Region(-0.24, -0.10, 0.20, 1.10)), "flat", "table_dark",
           direction=(86,), density=0.95, size=0.16, load=1.0)
s.block_in(polygon([(0.855, -0.02), (1.02, -0.02), (1.02, 0.06), (0.88, 0.018)]),
           "flat", p.mix("ultramarine", "burnt_umber", 0.55), direction="axis",
           density=1.0, size=0.05, load=1.0)
print("dark:", s.stroke_count)

# grain, third attempt: short marks, not edge to edge, and genuinely thin
s.glaze([(0.02, 0.30), (0.30, 0.25), (0.48, 0.20)], "grain_d", opacity=0.10)
s.glaze([(0.62, 0.46), (0.86, 0.42), (1.00, 0.40)], "grain_d", opacity=0.10)
s.stroke([(0.04, 0.60), (0.26, 0.575)], "bristle", "grain_l", size=0.022,
         opacity=0.04, load=1.0, note="grain thin")
s.stroke([(0.70, 0.68), (0.94, 0.645)], "bristle", "grain_d", size=0.026,
         opacity=0.04, load=1.0, note="grain thin")
print("strokes:", s.stroke_count)
print(s.look())
