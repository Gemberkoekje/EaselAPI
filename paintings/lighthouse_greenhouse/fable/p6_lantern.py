# Pass 6: the lamp room, in front of the halo. It is a hollow thing seen from
# outside with the light inside it, so the order is: the glass drum as one
# solid green mass (the vines are what fills it); the lamp's light where it
# gets between the leaves, as a few bright irregular smears; the leaves that
# press flat against the glass, back-lit, as yellow-green smears with a bend
# in them; the stems and the leaves in shadow, dark; the tomatoes; and then
# the things in front of all of it -- the mullions, one sheen on the glass,
# the gallery rail, the dome and its finial. No two leaves the same brush,
# size or direction.
def lamp_room_mass():
    s.block_in(lantern(), "flat", "leaf", size=0.02, density=1.0, solid=True, direction=90,
               opacity=1.0, pressure="even", note="subject lamp room, green mass")

def light_between_leaves():
    s.stroke([(0.648, 0.218), (0.662, 0.211), (0.675, 0.222)], "bristle", "glow", size=0.022,
             load=0.8, opacity=0.9, pressure="swell", note="subject the lamp, between leaves")
    s.stroke([(0.631, 0.247), (0.642, 0.238)], "bristle", "glow", size=0.012, load=0.7,
             opacity=0.8, pressure="swell", note="subject light between leaves")
    s.stroke([(0.682, 0.258), (0.692, 0.267), (0.697, 0.281)], "bristle", "glow", size=0.011,
             load=0.7, opacity=0.75, pressure="swell", note="subject light between leaves")
    s.dab(0.671, 0.195, "round_hard", "glow", size=0.009, press=3, tip_wobble=0.7,
          note="subject light between leaves")
    s.stroke([(0.620, 0.201), (0.631, 0.190)], "round_hard", p.mix("glow", "leaf_lit", 0.5),
             size=0.008, opacity=0.8, pressure="swell", tip_wobble=0.5, note="subject light between leaves")

def leaves_on_the_glass():
    s.stroke([(0.636, 0.212), (0.647, 0.204), (0.655, 0.211)], "bristle", "leaf_lit", size=0.016,
             load=0.8, opacity=0.9, pressure="swell", note="subject leaf, back-lit")
    s.stroke([(0.660, 0.241), (0.672, 0.236), (0.681, 0.245)], "bristle", "leaf_lit", size=0.018,
             load=0.8, opacity=0.9, pressure="swell", note="subject leaf, back-lit")
    s.stroke([(0.688, 0.205), (0.697, 0.216)], "round_hard", "leaf_lit", size=0.011, opacity=0.9,
             pressure="swell", tip_wobble=0.5, note="subject leaf, back-lit")
    s.stroke([(0.622, 0.262), (0.634, 0.271), (0.645, 0.266)], "bristle", "leaf_lit", size=0.014,
             load=0.75, opacity=0.85, pressure="swell", note="subject leaf, back-lit")
    s.stroke([(0.655, 0.285), (0.668, 0.278)], "round_hard", "leaf_lit", size=0.010, opacity=0.85,
             pressure="swell", tip_wobble=0.5, note="subject leaf, back-lit")

def stems_and_shadow_leaves():
    s.stroke([(0.628, 0.293), (0.636, 0.262), (0.650, 0.236), (0.658, 0.212)], "liner", "leaf_dark",
             size=0.0035, opacity=0.85, pressure="even", note="subject stem")
    s.stroke([(0.690, 0.291), (0.684, 0.262), (0.674, 0.245)], "liner", "leaf_dark", size=0.003,
             opacity=0.8, pressure="even", note="subject stem")
    s.dab(0.643, 0.252, "round_hard", "leaf_dark", size=0.014, press=3, tip_wobble=0.7,
          note="subject leaf, in shadow")
    s.stroke([(0.676, 0.222), (0.686, 0.232)], "round_hard", "leaf_dark", size=0.012, opacity=0.85,
             pressure="swell", tip_wobble=0.6, note="subject leaf, in shadow")
    s.stroke([(0.619, 0.229), (0.630, 0.222)], "round_hard", "leaf_dark", size=0.011, opacity=0.8,
             pressure="swell", tip_wobble=0.6, note="subject leaf, in shadow")

def tomatoes():
    for x, y, sz in ((0.639, 0.279, 0.012), (0.651, 0.283, 0.009), (0.684, 0.246, 0.011),
                     (0.627, 0.242, 0.008), (0.697, 0.284, 0.010)):
        s.dab(x, y, "round_hard", "tomato", size=sz, press=3, tip_wobble=0.4, note="subject tomato")
    s.dab(0.636, 0.276, "round_hard", "tomato_lit", size=0.005, press=2, note="subject tomato, lit")
    s.dab(0.681, 0.243, "round_hard", "tomato_lit", size=0.005, press=2, note="subject tomato, lit")

def glazing_bars():
    for x, sz in ((TX - 0.045, 0.005), (TX - 0.024, 0.0035), (TX - 0.003, 0.004),
                  (TX + 0.020, 0.0035), (TX + 0.045, 0.005)):
        s.stroke([(x, 0.173), (x, 0.298)], "liner", "iron", size=sz, opacity=0.92,
                 pressure="even", note="subject mullion")
    s.stroke([(TX - 0.038, 0.19), (TX - 0.03, 0.222), (TX - 0.026, 0.25)], "round_soft",
             p.at_value("fog", 0.80), size=0.009, opacity=0.35, load=1.0, load_falloff=0.0,
             pressure=[0.3, 1.0, 0.2], note="subject sheen on the glass")

def gallery_rail():
    s.stroke([(TX - 0.070, 0.268), (TX + 0.070, 0.268)], "liner", "iron", size=0.004, opacity=0.9,
             jitter=0.0, pressure="even", note="gallery rail")
    for x in (TX - 0.066, TX - 0.02, TX + 0.066):
        s.stroke([(x, 0.268), (x, 0.301)], "liner", "iron", size=0.0035, opacity=0.9,
                 pressure="even", note="rail post")

def dome():
    s.block_in(roof(), "flat", "iron", size=0.010, density=1.0, solid=True, direction="axis",
               opacity=1.0, pressure="even", edge="clean", note="dome")   # ragged, the passes serrated the curve
    rim = [(TX - 0.05 * math.cos(math.radians(a)), 0.178 - 0.047 * math.sin(math.radians(a)))
           for a in (168, 140, 110, 80, 55)]
    s.stroke(rim, "round_hard", p.at_value("tower_sh", 0.46), size=0.006, opacity=0.7,
             load=1.0, load_falloff=0.0, pressure=[0.05, 0.7, 1.0, 0.6, 0.05], note="dome, lit rim")
    s.dab(TX, 0.122, "round_hard", "iron", size=0.011, press=3, note="finial")

for layer in (lamp_room_mass, light_between_leaves, leaves_on_the_glass, stems_and_shadow_leaves,
              tomatoes, glazing_bars, gallery_rail, dome):
    layer()
print(s.look(values=True))
print(s.look())
print(s.look(region="E1:G3"))
