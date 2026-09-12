# Pass 8: the foot of the tower and the vines that have got out. Two boulders
# in front of the base, so the tower stands in the rock rather than on it --
# the bigger one on the right with its top taking the fog's light, the smaller
# one on the left lit from the other side; the door, one dark mark between
# them; two pots waiting on the rock by it, one standing in the other. Then
# the vine that has escaped the lamp room: a stem trailing down the lit face
# from the gallery with three leaves on it, and a shorter tendril over the
# rail on the shadow side.
def boulders():
    big = blob((TX + 0.035, 0.918), 0.046, wobble=0.45, points=9, seed=5, aspect=s.aspect)
    s.block_in(big, "flat", "rock", size=0.022, density=1.0, solid=True, direction="axis",
               edge="clean", note="boulder")
    s.stroke([(TX + 0.005, 0.895), (TX + 0.04, 0.885), (TX + 0.07, 0.898)], "flat", "rock_top",
             size=0.014, opacity=1.0, load=1.0, load_falloff=0.0, pressure="even", note="boulder top")
    s.stroke([(TX - 0.005, 0.955), (TX + 0.04, 0.965), (TX + 0.08, 0.958)], "round_hard", "rock_deep",
             size=0.010, opacity=0.85, pressure="swell", note="under the boulder")
    small = blob((TX - 0.058, 0.928), 0.028, wobble=0.4, points=8, seed=3, aspect=s.aspect)
    s.block_in(small, "flat", "rock", size=0.014, density=1.0, solid=True, direction="axis",
               edge="clean", note="second boulder")
    s.stroke([(TX - 0.085, 0.905), (TX - 0.062, 0.90), (TX - 0.04, 0.91)], "flat", "rock_warm",
             size=0.010, opacity=1.0, load=1.0, load_falloff=0.0, pressure="even", note="second boulder, lit")

def door_and_pots():
    s.stroke([(TX - 0.022, 0.85), (TX - 0.022, 0.905)], "flat", "iron", size=0.017, opacity=0.9,
             load=1.0, load_falloff=0.0, pressure="even", note="the door")
    pot(TX - 0.046, 0.905, 0.021, 0.028, "empty")
    s.stroke([(TX - 0.046, 0.877), (TX - 0.046, 0.866)], "flat", "terra", size=0.017, opacity=1.0,
             load=1.0, load_falloff=0.0, pressure="even", note="subject pot, stacked")
    s.stroke([(TX - 0.058, 0.866), (TX - 0.034, 0.866)], "flat", "terra_lit", size=0.005, opacity=0.95,
             load=1.0, load_falloff=0.0, pressure="even", note="subject pot rim, stacked")
    pot(TX + 0.095, 0.882, 0.024, 0.03, "bushy")

def escaped_vines():
    s.stroke([(TX - 0.052, 0.302), (TX - 0.06, 0.33), (TX - 0.056, 0.37), (TX - 0.064, 0.41),
              (TX - 0.058, 0.44)], "liner", "leaf_dark", size=0.0035, opacity=0.9, pressure="even",
             note="subject escaped vine")
    for (x, y, sz, ang) in ((TX - 0.064, 0.325, 0.011, 1), (TX - 0.050, 0.372, 0.012, -1),
                            (TX - 0.068, 0.428, 0.010, 1)):
        s.stroke([(x, y), (x + 0.005 * ang, y + 0.008)], "round_hard", "leaf", size=sz, opacity=0.9,
                 pressure="swell", tip_wobble=0.5, note="subject escaped leaf")
    s.stroke([(TX + 0.042, 0.268), (TX + 0.056, 0.29), (TX + 0.062, 0.322)], "liner", "leaf_dark",
             size=0.003, opacity=0.85, pressure="even", note="subject tendril over the rail")
    s.stroke([(TX + 0.06, 0.312), (TX + 0.068, 0.322)], "round_hard", p.mix("leaf", "leaf_dark", 0.4),
             size=0.009, opacity=0.9, pressure="swell", tip_wobble=0.5, note="subject tendril leaf")

for layer in (boulders, door_and_pots, escaped_vines):
    layer()
print(s.look(values=True))
print(s.look())
print(s.look(region="E6:G8"))
print(s.look(region="E2:G4"))
