p = s.palette
print("palette survived:", p.hex(p["wall_l"]))

# --- far background, back to front -------------------------------------
s.block_in(span("G1", "H3"), "flat", "wall_l", direction=97, size=0.15,
           density=1.0, load=1.0)                      # lit wall behind him
s.block_in(span("H1", "H2"), "flat", "wall_h", direction=104, size=0.10,
           density=1.0, load=1.0)                      # its brightest corner
s.block_in(span("A1", "C1"), "flat", "wall_m", direction=5, size=0.12,
           density=0.9, load=1.0)                      # warm ceiling band
s.block_in(span("C2", "E3"), "flat", "bg_dark", direction=18, size=0.14,
           density=1.0, load=1.0)                      # dark shelf, upper left
s.block_in(cell("A2"), "flat", "bg_dark", direction=-14, size=0.12,
           density=1.0, load=1.0)
s.block_in(span("A3", "B5"), "flat", "greyblur", direction=95, size=0.13,
           density=0.95, load=1.0)                     # pale blur, left edge
s.block_in(span("G3", "H4"), "flat", "rightbg", direction=14, size=0.14,
           density=0.95, load=1.0)                     # the other man's group
s.block_in(cell("H6"), "flat", "table", direction=-9, size=0.10,
           density=1.0, load=1.0)                      # lit table, right
s.block_in(span("A7", "C8"), "flat", "lowleft", direction=-7, size=0.16,
           density=0.95, load=1.0)                     # foreground table, left
print("strokes:", s.stroke_count)
print(s.look(reference="ref.jpg", grid=True, values=True))
print(s.look(reference="ref.jpg"))
