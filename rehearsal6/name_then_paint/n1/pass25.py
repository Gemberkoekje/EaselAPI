exec(open("lib2.py").read())
pc, warm, cool, arc, at, clean, head, edges, ruffle = build(s)
p = s.palette
s.dry()
# repair B, then rebuild A
head(0.640, 0.520, 0.112, 0.100, 5, 0.645, 0.215, 0.020)
clean(0.640, 0.520, 0.112, 0.100, [(238, 424, "bg"), (52, 128, "bg")], sz=0.024, rr=1.16)
head(0.442, 0.436, 0.100, 0.092, 17, 0.700, 0.200, 0.019)
clean(0.442, 0.436, 0.100, 0.092, [(150, 340, "bg")], sz=0.022, rr=1.17)
print("strokes:", s.stroke_count)
print(s.look(region=span("C3","G6"), sketch=False))
