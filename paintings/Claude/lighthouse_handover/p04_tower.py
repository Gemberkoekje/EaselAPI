# The subject. A tapered cylinder lit from the left by the glow: the whole tower in its
# shadow colour, the lit side laid on it, the join at half strength -- each one long
# flat stroke up the axis, clipped to its own outline, so the clip does the tapering.
# Then the gallery, the cap, and (dry) the lantern glass and the lamp.
FLAT = dict(opacity=1.0, load=1.0, load_falloff=0.0, pressure="even", jitter=0.0,
            size_jitter=0.0, note="subject")
s.stroke([(TX, 0.548), (TX, 0.203)], "flat", "tower", size=0.043, clip=tower, **FLAT)
s.stroke([(TX - 0.0115, 0.548), (TX - 0.0078, 0.205)], "flat", "tower_lit", size=0.016,
         clip=tower_lit_side, **FLAT)
s.stroke([(TX - 0.0062, 0.536), (TX - 0.0050, 0.380), (TX - 0.0037, 0.211)], "flat",
         p.mix("tower", "tower_lit", 0.5), size=0.005, opacity=0.6, load=1.0,
         load_falloff=0.0, pressure="even", clip=tower, note="subject")      # the join
s.stroke([(TX - 0.0200, 0.2035), (TX + 0.0200, 0.2035)], "flat", "land", size=0.009,
         opacity=0.95, load=1.0, load_falloff=0.0, pressure="even", note="subject")  # gallery
s.block_in(cap, "flat", "land", size=0.006, density=1.0, solid=True, edge="hard",
           direction="horizontal", note="subject")
s.stroke([(TX, 0.1398), (TX, 0.1285)], "liner", "land", size=0.004, note="subject")  # finial
s.dry()
s.stroke([(TX, 0.1968), (TX, 0.1598)], "flat", "lantern", size=0.019, clip=lantern, **FLAT)
s.dab(TX, 0.178, "round_hard", "lamp", size=0.012, press=3, tip_wobble=0.35, note="subject")
