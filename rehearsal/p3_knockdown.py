# Stage 3 -- the whole thing is too light and too orange next to the reference.
# Knock the picture down into a dim interior, then find the lights again.
p = s.palette
p["gloom"]     = p.tint(p.mix("burnt_umber", "ultramarine", 0.35), 0.10)
p["gloom_wrm"] = p.tint(p.mix("burnt_umber", "burnt_sienna", 0.30), 0.16)
print("gloom", p.hex(p["gloom"]), p.value_of(p["gloom"]),
      "| warm", p.hex(p["gloom_wrm"]), p.value_of(p["gloom_wrm"]))

s.dry()
# A broken scumble, not a coat of paint: low load so the warm underneath sparkles
# through it and the surface stays worked.
s.block_in(Region(0.0, 0.0, 1.0, 1.0), "bristle", "gloom", density=0.55,
           size=0.22, direction="horizontal", load=0.55, note="knock down")
s.block_in(Region(0.0, 0.0, 1.0, 0.72), "bristle", "gloom_wrm", density=0.45,
           size=0.20, direction="diagonal", load=0.45, note="knock down warm")
print("strokes:", s.stroke_count)
print(s.look())
