s.dry()
s.stroke([(0.487,-0.03),(0.488,0.24),(0.489,0.50)], "bristle", "spill2", size=0.020,
         load=1.0, opacity=0.85, pressure="even")
s.stroke([(0.570,-0.03),(0.571,0.24),(0.572,0.50)], "bristle", "spill2", size=0.019,
         load=1.0, opacity=0.80, pressure="even")
s.stroke([(0.500,-0.03),(0.501,0.26),(0.502,0.50)], "bristle", "lit", size=0.014,
         load=1.0, opacity=0.9, pressure="even")
s.stroke([(0.557,-0.03),(0.558,0.26),(0.559,0.50)], "bristle", "lit", size=0.013,
         load=1.0, opacity=0.9, pressure="even")
print("total", s.stroke_count)
print(s.look())
print(s.look(values=True))
