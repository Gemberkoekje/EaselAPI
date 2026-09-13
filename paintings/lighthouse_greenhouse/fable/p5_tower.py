# Pass 5: the tower, in front of the fog and the rock. First the lamp's light
# in the air, which is on the fog and so goes down before the tower: two glazes
# with the soft round tip, one wide and faint in the green-gold of light
# through leaves, one small and paler. Then the tower as one solid cool mass
# with a clean silhouette, and its lit face -- the side that looks left, toward
# the open sea -- as a second shape on top of it, with one half-strength stroke
# down the join so the cylinder turns instead of stepping. Then the gallery
# plate, wider than the tower, and the shadow it casts on the tower below it.
# The first version was laid with a 0.02 flat and showed every pass as a
# stripe, and its clean contour, splined through four corners, rose off the
# top of the mass as an arch: the sides are subdivided now, and the brushes wider.
p["tower_deep"] = p.at_value("tower_sh", 0.29)
s.dry()
s.glaze([(0.55, 0.232), (0.66, 0.226), (0.77, 0.236)], "halo", opacity=0.20, size=0.13,
        pressure="swell", note="subject halo, wide")
s.glaze([(0.625, 0.233), (0.695, 0.237)], "glow", opacity=0.24, size=0.07,
        pressure="swell", note="subject halo, close")
s.block_in(tower(), "flat", "tower_sh", size=0.032, density=1.0, solid=True, direction=90,
           edge="clean", note="tower mass")
s.block_in(lit_face(), "flat", "tower_lit", size=0.022, density=1.0, solid=True, direction=90,
           opacity=1.0, pressure="even", note="lit face")
s.stroke([(TX - 0.017, 0.925), (TX - 0.012, 0.62), (TX - 0.007, 0.315)], "flat",
         p.mix("tower_sh", "tower_lit", 0.5), size=0.012, opacity=0.6, load=1.0,
         load_falloff=0.0, pressure="even", note="the terminator, softened")
s.stroke(gallery(), "flat", "iron", size=0.014, opacity=0.95, load=1.0, load_falloff=0.0,
         jitter=0.0, pressure="even", note="gallery plate")
s.stroke([(TX - 0.047, 0.318), (TX + 0.047, 0.318)], "flat", "tower_deep", size=0.010,
         opacity=0.75, load=1.0, load_falloff=0.0, jitter=0.0, pressure="even",
         note="shadow under the gallery")
print(s.look(values=True))
print(s.look())
print(s.look(region="E2:G5"))
