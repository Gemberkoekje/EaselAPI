# The foreground. A quarter of the picture doing nothing: frozen ground two to five
# metres off, which should be the coarsest thing in the painting and the quietest.
# Marks scale off distance, so the ground comes toward you.

p["clod"]   = p.at_value(p.mix(p["neutral"], "burnt_umber", 0.30), 0.33)
p["clodlt"] = p.at_value(p.mix(p["neutral"], "yellow_ochre", 0.20), 0.47)
p["grass"]  = p.at_value(p.desaturate(p.mix("yellow_ochre", "burnt_umber", 0.42), 0.74), 0.50)
p["stone"]  = p.at_value(p.mix(p["neutral"], "burnt_umber", 0.36), 0.27)

# --- broken frozen ground, coarsest nearest, none of the passes parallel
for pts, sz, ld, col, op in [
        ([(-0.05, 0.965), (0.19, 0.930), (0.42, 0.975)], 0.085, 0.50, "clod",   0.55),
        ([(0.40, 0.880), (0.16, 0.845), (-0.05, 0.878)], 0.070, 0.44, "clodlt", 0.42),
        ([(-0.05, 0.775), (0.14, 0.752), (0.33, 0.786)], 0.052, 0.40, "clod",   0.44),
        ([(0.31, 0.690), (0.15, 0.676), (-0.05, 0.694)], 0.038, 0.34, "clodlt", 0.36),
        ([(-0.05, 0.615), (0.12, 0.605), (0.26, 0.618)], 0.026, 0.28, "clod",   0.30)]:
    s.stroke(pts, "bristle", col, size=sz, load=ld, load_falloff=0.30,
             opacity=op, pressure="swell", note="ground")

# --- frost in the hollows, and it is bigger near me than it was far off
for pts, sz, ld, op in [([(0.055, 1.010), (0.225, 0.972), (0.385, 1.005)], 0.070, 0.22, 0.85),
                        ([(0.310, 0.842), (0.160, 0.868), (0.020, 0.848)], 0.046, 0.18, 0.72),
                        ([(-0.04, 0.712), (0.105, 0.728), (0.235, 0.710)], 0.030, 0.15, 0.58)]:
    s.stroke(pts, "bristle", "frost", size=sz, load=ld, load_falloff=0.10,
             opacity=op, pressure="swell", note="ground")

# --- dead grass: vertical, which crosses the ground's own bands. No two tufts get
#     the same number of blades or the same fan, or they read as one thing repeated.
TUFTS = [(0.064, 0.930, 0.072, 0.0060, 0.78, (-0.42, -0.05, 0.28, 0.55)),
         (0.176, 0.998, 0.086, 0.0066, 0.80, (-0.22, 0.34)),
         (0.256, 0.874, 0.050, 0.0046, 0.66, (-0.50, 0.02, 0.40)),
         (0.096, 0.806, 0.040, 0.0038, 0.58, (0.18, -0.34)),
         (0.320, 0.752, 0.030, 0.0030, 0.48, (-0.28, 0.15, 0.48))]
for x, y, h, w, op, leans in TUFTS:
    for k, lean in enumerate(leans):
        hk = h * (1.0 - 0.13 * k)
        s.stroke([(x + k * w * 0.7, y), (x + k * w * 0.7 + lean * hk * 0.45, y - hk * 0.60),
                  (x + k * w * 0.7 + lean * hk, y - hk)],
                 "liner", "grass", size=w * (1.0 - 0.15 * k),
                 pressure=[0.95, 0.45, 0.0], load=1.0,
                 opacity=op * (1.0 - 0.12 * k), note="ground")

# --- a few frozen clods, dark, to give the left half something below the tree
for pts, sz in [([(0.120, 0.960), (0.142, 0.952)], 0.017),
                ([(0.292, 0.921), (0.276, 0.915)], 0.012),
                ([(0.054, 0.866), (0.068, 0.860)], 0.009)]:
    s.stroke(pts, "round_hard", "stone", size=sz, pressure=[1.0, 0.35],
             load=1.0, opacity=0.85, tip_wobble=0.7, note="ground")

# --- and the base meets the ground: lose that edge where the haze takes it
s.smudge([(0.290, 0.575), (0.352, 0.660), (0.418, 0.760)])
s.stroke([(0.268, 0.548), (0.330, 0.632), (0.396, 0.730)], "bristle", "yardfar",
         size=0.030, load=0.38, opacity=0.40, pressure="swell", note="ground")
