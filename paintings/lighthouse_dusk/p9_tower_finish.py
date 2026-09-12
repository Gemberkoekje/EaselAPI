# Pass 9: the tower, last touches. The gallery casts a shadow onto the top of the
# tower under it, which is what gives the plate its weight; the lit face gets one
# warmer touch low down where the glow reaches it most; and the glass gets its
# brightest point once more, since everything else in the picture is quieter now.
p["tower_deep"] = p.at_value("tower_sh", 0.30)
s.stroke([(0.244, 0.173), (0.297, 0.173)], "flat", "tower_deep", size=0.009, opacity=0.75,
         load=1.0, load_falloff=0.0, jitter=0.0, pressure="even", note="shadow under the gallery")
s.stroke([(0.296, 0.60), (0.292, 0.50)], "flat", p.mix("tower_lit", "glow", 0.3), size=0.014,
         opacity=0.5, load=1.0, load_falloff=0.0, pressure="lift_off", note="warmth low on the lit face")
s.dab(0.2705, 0.126, "round_hard", p.mix("lamp", "titanium_white", 0.7), size=0.010, press=3,
      note="the lamp, once more")
print(s.look())
print(s.look(region="B1:D3"))
print(s.look(region="D5:H8"))
