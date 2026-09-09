# Pass 2: looking only. No paint. Enlarged crops of the head to place landmarks.
REF = "C:/temp/Level3.jpg"
print("head passage :", s.look(region=span("D2", "F5"), reference=REF, grid=True))
print("D3 brow/eye  :", s.look(region=cell("D3"), reference=REF, grid="fine"))
print("D4 nose/mouth:", s.look(region=cell("D4"), reference=REF, grid="fine"))
print("strokes:", s.stroke_count)
