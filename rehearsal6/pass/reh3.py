R = "/home/user/refs/Level1.jpg"
lipA = [(0.294,0.272),(0.340,0.306),(0.404,0.325),(0.470,0.331),(0.532,0.316),(0.585,0.282),(0.620,0.243)]
lipB = [(0.300,0.262),(0.352,0.298),(0.420,0.318),(0.486,0.322),(0.545,0.305),(0.598,0.268),(0.626,0.230)]
s.preview([{"points":lipA,"brush":"flat","size":0.028,"color":"mug_hi","label":"lipA"},
           {"points":lipB,"brush":"flat","size":0.028,"color":"mug_wt","label":"lipB"}],
          reference=R, region=span("C2","F4"), grid="fine")
print(s.rehearse([{"points":lipA,"brush":"flat","size":0.030,"color":"mug_hi",
                   "pressure":"even","load":1.0}], reference=R, region=span("C2","F4")))
