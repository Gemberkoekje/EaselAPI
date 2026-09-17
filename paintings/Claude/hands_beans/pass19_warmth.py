# The hands were one olive-tan all over, and skin is not: warm and red at the
# knuckles where the skin is thin over bone, cooler and paler across the planes
# between. Laid as glazes, because that is a film shifting the colour underneath
# rather than a stripe of a different colour laid on top of it. PAINTING.md's own
# table puts the window at 0.10-0.12; past 0.14 it stops being warmth and becomes
# pink paint, which is exactly what the first two attempts gave.
s.dry()

for pts, sz, col, op in [
    ([(0.476, 0.428), (0.516, 0.444)], 0.028, "joint",    0.13),
    ([(0.470, 0.474), (0.512, 0.492)], 0.032, "joint",    0.15),
    ([(0.416, 0.408), (0.460, 0.418)], 0.022, "joint_lo", 0.10),
    ([(0.394, 0.450), (0.440, 0.462)], 0.024, "joint_lo", 0.11),
    ([(0.590, 0.694), (0.528, 0.674)], 0.032, "joint_lo", 0.11),
    ([(0.624, 0.294), (0.666, 0.270), (0.706, 0.260)], 0.030, "joint", 0.12),
    ([(0.590, 0.314), (0.556, 0.362), (0.528, 0.406)], 0.026, "joint_lo", 0.10),
]:
    s.glaze(pts, col, opacity=op, size=sz, note="subject")

for pts, sz, op in [([(0.458, 0.423), (0.400, 0.409), (0.352, 0.409)], 0.020, 0.10),
                    ([(0.454, 0.465), (0.390, 0.453), (0.334, 0.455)], 0.023, 0.11),
                    ([(0.512, 0.654), (0.462, 0.632), (0.422, 0.610)], 0.018, 0.09),
                    ([(0.692, 0.230), (0.748, 0.212), (0.802, 0.214)], 0.032, 0.10)]:
    s.glaze(pts, "fl_cool", opacity=op, size=sz, note="subject")
print(s.look(region="C3:G5"))
