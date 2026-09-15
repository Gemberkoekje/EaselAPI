# The weakest passage in the picture: where the picking hand's thumb crosses the
# side of the cupped hand, half a dozen marks in three directions had made a patch
# of camouflage with a green cast. Bury it in one quiet warm plane, then state the
# two things that are actually there -- the thumb, and the hand it passes in front
# of -- with a dark between them so they separate.
s.dry()

# the side of the cupped hand, turning away from the light: one unified plane
s.stroke([(0.546, 0.512), (0.624, 0.558), (0.702, 0.606)], "bristle", "fl_side",
         size=0.072, opacity=0.95, load=1.0, load_falloff=0.25,
         pressure="swell", note="subject")
s.stroke([(0.556, 0.572), (0.636, 0.608), (0.708, 0.634)], "bristle", "fl_side2",
         size=0.055, opacity=0.88, load=1.0, load_falloff=0.30,
         pressure="swell", note="subject")
s.stroke([(0.560, 0.486), (0.630, 0.520), (0.694, 0.556)], "bristle", "fl_side",
         size=0.044, opacity=0.70, load=0.85, load_falloff=0.40,
         pressure="swell", note="subject")

# the dark that puts the thumb in front of it
s.stroke([(0.652, 0.396), (0.588, 0.448), (0.534, 0.486)], "bristle", "fl_under",
         size=0.022, opacity=0.85, load=1.0, load_falloff=0.30,
         pressure="swell", note="subject")

# the thumb itself, restated: body, then its lit upper edge
s.stroke([(0.642, 0.356), (0.578, 0.412), (0.518, 0.456), (0.486, 0.484)],
         "bristle", "fl_body2", size=0.050, opacity=0.92, load=1.0,
         load_falloff=0.30, pressure="lift_off", note="subject")
s.stroke([(0.628, 0.344), (0.566, 0.398), (0.510, 0.440)], "round_hard", "fl_lit",
         size=0.017, opacity=0.78, load=1.0, load_falloff=0.30, tip_wobble=0.40,
         pressure=[0.35, 1.0, 0.55], note="subject")
print(s.look(region="D3:G6"))
