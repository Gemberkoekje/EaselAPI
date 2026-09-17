# What makes the pane wet: beading, one leaf pressed flat against the glass where
# the film is clear, and one warm thing glowing through where it is not.
from easel import hull

p["leafpress"] = p.at_value(p.mix(p.mix("viridian", "yellow_ochre", 0.30),
                                  "burnt_umber", 0.08), 0.25)
p["leafedge"]  = p.at_value(p.mix(p.mix("viridian", "yellow_ochre", 0.52),
                                  "titanium_white", 0.22), 0.44)
p["glow"]      = p.at_value(p.mix(p.mix("burnt_sienna", "cadmium_red", 0.40),
                                  "titanium_white", 0.30), 0.42)

# --- beading: a starved brush on rough canvas is the thing itself, not a stipple
for pts, sz, ld, op in [
        ([(0.828, 0.235), (0.905, 0.205), (0.995, 0.188)], 0.030, 0.22, 0.75),
        ([(0.992, 0.330), (0.900, 0.362), (0.822, 0.352)], 0.024, 0.18, 0.70),
        ([(0.836, 0.560), (0.918, 0.585), (0.998, 0.566)], 0.034, 0.26, 0.72),
        ([(0.985, 0.742), (0.902, 0.775), (0.824, 0.756)], 0.028, 0.20, 0.66),
        ([(0.700, 0.300), (0.760, 0.286), (0.790, 0.300)], 0.018, 0.16, 0.55)]:
    s.stroke(pts, "bristle", "bead", size=sz, load=ld, load_falloff=0.10,
             opacity=op, pressure="swell", note="subject")

# --- one leaf pressed flat on the glass: dark, then light, then the edge between
leaf = hull([(0.918, 0.405), (0.949, 0.393), (0.968, 0.424),
             (0.951, 0.462), (0.921, 0.448)])
s.block_in(leaf, "round_hard", "leafpress", direction=34, density=1.0,
           size=0.013, pressure="even", note="subject")
s.stroke([(0.925, 0.438), (0.946, 0.421), (0.962, 0.421)], "round_hard", "leafedge",
         size=0.006, pressure=[0.3, 1.0, 0.0], load=0.8, opacity=0.85, note="subject")
s.stroke([(0.919, 0.409), (0.944, 0.398), (0.966, 0.421)], "liner", "leafpress",
         size=0.004, pressure=[0.0, 0.9, 0.4], load=1.0, opacity=0.9, note="subject")

# --- the one warm thing in the picture, seen through the film and so not sharp
s.dab(0.782, 0.886, "round_soft", "glow", size=0.030, press=2, note="subject")
s.dab(0.775, 0.879, "round_hard", p.at_value(p["glow"], 0.36), size=0.013,
      press=2, tip_wobble=0.7, note="subject")
