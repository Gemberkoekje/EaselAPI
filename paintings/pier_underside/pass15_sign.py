p = s.palette
p["sig"] = p.at_value(p.mix("viridian", "burnt_umber", 0.45), 0.255)
# a thing, and the light thrown back up at it: the whole logic of the picture, small.
s.stroke([(0.038, 0.9425), (0.082, 0.9438)], "liner", "sig", size=0.0038,
         pressure=[0.2, 1.0, 0.35], load=0.9, opacity=0.62, note="signature")
s.stroke([(0.046, 0.9565), (0.071, 0.9572)], "liner", "sig", size=0.0030,
         pressure=[0.0, 0.8, 0.0], load=0.6, load_falloff=0.9, opacity=0.38,
         note="signature")
s.look(path="out/19_signed.png")
s.export("pier_underside.png")
print("exported")
