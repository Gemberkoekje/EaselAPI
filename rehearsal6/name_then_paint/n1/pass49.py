p = s.palette
sig = p.mix(p["tbl_dk"], p["tbl_lit"], 0.55)
print("signature value", round(p.value_of(sig), 3))
s.stroke([(0.9180, 0.9250), (0.9480, 0.9490)], "liner", sig, size=0.0050,
         pressure=[0.35, 1.0, 0.45], note="signature")
s.stroke([(0.9060, 0.9520), (0.9200, 0.9632)], "liner", sig, size=0.0042,
         pressure=[0.4, 1.0, 0.3], note="signature")
print("strokes:", s.stroke_count)
print(s.look(region=span("G7","H8")))
s.export("final.png")
print("exported")
