p = s.palette
s.dry()
n = s.stroke_count

# knock the hair's lit band back — it came out a wig
for pts in [
    [(0.482, 0.168), (0.534, 0.118), (0.596, 0.140)],
    [(0.560, 0.118), (0.628, 0.180), (0.672, 0.262)],
    [(0.500, 0.146), (0.560, 0.160), (0.618, 0.212)],
]:
    s.stroke(pts, "bristle", "hair_d", size=0.045, opacity=0.42, load=0.6)
print("hair knock-back", s.stroke_count - n); n = s.stroke_count

# A2 and C2: the deepest background darks
s.block_in(cell("A2"), "flat", "deep", direction=-12, size=0.09, density=1.0, load=1.0)
s.block_in(span("C2", "C2"), "flat", "deep", direction=16, size=0.09, density=1.0, load=1.0)
s.stroke([(0.262, 0.268), (0.330, 0.290)], "bristle", "deep", size=0.055, load=1.0)
print("darks", s.stroke_count - n); n = s.stroke_count

# the foreground table, left: everything down there is a stop too light
s.block_in(span("A7", "C8"), "bristle", "lowdark", direction=-6, size=0.10,
           density=0.7, opacity=0.5, load=0.8)
print("lower left", s.stroke_count - n); n = s.stroke_count

# his sleeve, bottom middle
s.block_in(span("D8", "D8"), "flat", "coat", direction=-10, size=0.09,
           density=1.0, load=1.0)
print("sleeve", s.stroke_count - n); n = s.stroke_count

# the phone on the table
phone = polygon([(0.622, 0.930), (0.690, 0.882), (0.768, 0.876), (0.775, 1.000),
                 (0.618, 1.000)])
s.block_in(phone, "flat", "phone", direction="axis", density=1.0, size=0.055, load=1.0)
print("phone", s.stroke_count - n)

print("total:", s.stroke_count)
print(s.look(reference="ref.jpg"))
