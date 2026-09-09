# Pass 3: looking only. Hair silhouette, forehead/hairline, chin/beard.
REF = "C:/temp/Level3.jpg"
print("hair mass  :", s.look(region=span("D1", "G4"), reference=REF, grid=True))
print("D2 forehead:", s.look(region=cell("D2"), reference=REF, grid="fine"))
print("D5 chin    :", s.look(region=cell("D5"), reference=REF, grid="fine"))
print("E5 jaw/neck:", s.look(region=cell("E5"), reference=REF, grid="fine"))
print("strokes:", s.stroke_count)
