# One mark, in the quiet dark of the cowl at the bottom right, a step lighter than
# what it sits on. It starts inside the picture and runs off the edge of it.
before = s.stroke_count
s.stroke([(0.936, 0.940), (1.048, 0.921)], "liner", "frame_lt",
         size=0.0050, opacity=0.85, pressure=[0.15, 1.0], note="signature")
print("stroke_count", before, "->", s.stroke_count)
print(s.look())
