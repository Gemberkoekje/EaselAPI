# Pass 4: looking only. Ear cell, and the hand passage.
REF = "C:/temp/Level3.jpg"
print("E3 ear     :", s.look(region=cell("E3"), reference=REF, grid="fine"))
print("hand       :", s.look(region=span("B4", "D7"), reference=REF, grid=True))
print("strokes:", s.stroke_count)
