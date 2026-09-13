# Pass 4: the tower, on the fog and the rock, before the stairs and the lamp
# room. One solid cool mass with a clean silhouette, its lit face -- the side
# toward the glow and the beam -- as a second shape on top, and one
# half-strength stroke down the join so the terminator turns instead of
# stepping (PAINTING.md, "A form that turns"; rehearsed as a pass ramp first
# and it came back nearly flat). A little weathering low down, where a
# lighthouse mid-conversion would actually be damp, hints at the change
# before the stairs and the vines make it explicit. Then the near boulders,
# after the tower, so it stands *in* the rock rather than on it.
def lit_face_bottom():   # a touch more weathering right at the waterline
    return polygon([(TOWER_BL, TOWER_BASE_Y), (0.395, TOWER_BASE_Y),
                    (0.392, 0.635), (TOWER_BL + 0.010, 0.635)])

s.block_in(tower(), "flat", "tower_sh", size=0.035, density=1.0, solid=True,
           direction=90, note="tower mass")
s.block_in(lit_face(), "flat", "tower_lit", size=0.016, density=1.0, solid=True,
           direction=90, opacity=1.0, pressure="even", note="lit face")
s.stroke([(0.4625, TOWER_BASE_Y - 0.01), (0.4575, 0.42), (0.4525, TOWER_TOP_Y + 0.01)],
         "flat", p.mix("tower_sh", "tower_lit", 0.5), size=0.012, opacity=0.6, load=1.0,
         load_falloff=0.0, pressure="even", note="the terminator, softened")
s.block_in(lit_face_bottom(), "flat", "moss", size=0.012, density=1.0, solid=True,
           direction=90, opacity=0.6, pressure="even", note="damp, near the waterline")
s.stroke([(0.345, 0.70), (0.355, 0.655), (0.362, 0.62)], "bristle", "moss", size=0.02,
         load=0.35, opacity=0.5, pressure="taper", note="moss creeping up the shadow side")
s.block_in(boulders(), "flat", "rock", size=0.024, density=1.0, solid=True,
           direction="axis", edge="clean", note="boulders, near the tower's foot")
s.stroke([(0.45, 0.700), (0.485, 0.693), (0.515, 0.705)], "flat", "rock_cool", size=0.013,
         opacity=1.0, load=1.0, load_falloff=0.0, pressure="even", note="boulder top")
s.stroke([(0.455, 0.735), (0.49, 0.745)], "round_hard", "rock_deep", size=0.009,
         opacity=0.85, pressure="swell", note="under the boulder")
s.block_in(boulders2(), "flat", "rock", size=0.018, density=1.0, solid=True,
           direction="axis", edge="clean", note="second boulder, left")
s.stroke([(0.285, 0.720), (0.315, 0.716)], "flat", "rock_warm", size=0.010,
         opacity=1.0, load=1.0, load_falloff=0.0, pressure="even", note="second boulder, lit edge")
print(s.look(values=True))
print(s.look())
print(s.look(region="C1:F7"))
