# The weakest passage: the crown is an oval smudge. Break the silhouette with sky
# worked IN FROM THE EDGE with a starved brush -- sky dabbed into the middle gives
# a floating hole -- then put the finer branches back through it.
from easel import Region

sky_here = s.sample(Region(0.26, 0.14, 0.40, 0.30))
p["gap"]  = sky_here
p["fine"] = p.at_value(p.mix(p.mix("burnt_umber", "ultramarine", 0.42),
                             "yellow_ochre", 0.12), 0.43)

# --- slivers of sky in from the outline, no two the same length
for pts, sz, ld, op in [
        ([(0.028, 0.196), (0.076, 0.238), (0.104, 0.268)], 0.026, 0.30, 0.70),
        ([(0.268, 0.286), (0.212, 0.268), (0.176, 0.276)], 0.022, 0.26, 0.64),
        ([(0.124, 0.076), (0.140, 0.126), (0.146, 0.164)], 0.020, 0.24, 0.62),
        ([(0.056, 0.396), (0.096, 0.362), (0.118, 0.344)], 0.018, 0.22, 0.58),
        ([(0.244, 0.402), (0.204, 0.372)], 0.016, 0.20, 0.52),
        ([(0.198, 0.132), (0.172, 0.176)], 0.014, 0.18, 0.48)]:
    s.stroke(pts, "bristle", "gap", size=sz, load=ld, load_falloff=0.30,
             opacity=op, pressure="lift_off", note="dist")

# --- and the crown is densest where the boughs are, not evenly all over
s.glaze([(0.118, 0.386), (0.148, 0.288), (0.158, 0.196)], "twigdk",
        opacity=0.13, size=0.040, note="dist")
s.glaze([(0.098, 0.316), (0.152, 0.262), (0.202, 0.248)], "twigdk",
        opacity=0.10, size=0.032, note="dist")

# --- finer branches, breaking the outline from inside it
for pts, sz, pr, op in [
        ([(0.106, 0.286), (0.062, 0.232), (0.030, 0.206)], 0.0035, [0.8, 0.4, 0.0], 0.62),
        ([(0.170, 0.252), (0.216, 0.216), (0.252, 0.208)], 0.0030, [0.7, 0.35, 0.0], 0.56),
        ([(0.148, 0.196), (0.132, 0.126), (0.126, 0.082)], 0.0028, [0.7, 0.3, 0.0], 0.52),
        ([(0.160, 0.310), (0.206, 0.336), (0.238, 0.372)], 0.0026, [0.6, 0.3, 0.0], 0.46),
        ([(0.128, 0.418), (0.086, 0.400), (0.052, 0.408)], 0.0024, [0.6, 0.25, 0.0], 0.42)]:
    s.stroke(pts, "liner", "fine", size=sz, pressure=pr, load=1.0,
             opacity=op, note="dist")
