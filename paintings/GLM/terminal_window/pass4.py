# pass 4 -- near things: keyboard rim, key flecks, mug, desk front edge
# keyboard: its back edge faces the screen and catches the light
s.stroke([(0.372, 0.668), (0.50, 0.664), (0.640, 0.662)], "liner", p["key_rim"],
         size=0.006, load=0.55, opacity=0.8, note="subject")
s.stroke([(0.375, 0.678), (0.44, 0.676)], "liner", p["key_rim"],
         size=0.005, load=0.30, opacity=0.5)            # first key row, broken
s.stroke([(0.52, 0.674), (0.62, 0.672)], "liner", p["key_rim"],
         size=0.005, load=0.28, opacity=0.4)
s.stroke([(0.40, 0.692), (0.58, 0.689)], "liner", p.at_value(p["key_rim"], 0.30),
         size=0.005, load=0.25, opacity=0.35)           # second row, dimmer still

# mug: silhouette in the dim, one lit left edge, one dark opening -- all off mug_c
mx, my = s.pt("mug_c")
s.block_in(s.circle((mx, my), 0.030, wobble=0.15, seed=2),
           "round_hard", p["key"], size=0.014, solid=True, pressure="even", edge="clean")
s.stroke([(mx - 0.023, my - 0.012), (mx - 0.029, my + 0.006), (mx - 0.014, my + 0.024)],
         "round_hard", p.at_value(p["mug_rim"], 0.38),
         size=0.007, opacity=0.75, pressure=[0.4, 1.0, 0.5], tip_wobble=0.7)
s.stroke([(mx - 0.016, my + 0.031), (mx + 0.013, my + 0.032)], "liner", p["shadow"],
         size=0.005, load=0.6, opacity=0.7)                     # contact shadow
s.stroke([(mx - 0.015, my - 0.024), (mx + 0.013, my - 0.023)], "round_hard", p["shadow"],
         size=0.008, opacity=0.9, pressure=[0.6, 1.0, 0.6], tip_wobble=0.7)
s.stroke([(mx - 0.011, my - 0.021), (mx + 0.009, my - 0.0205)], "liner", p.at_value(p["mug_rim"], 0.34),
         size=0.004, load=0.5, opacity=0.7)                   # far rim catching light

# the pool spills over the desk front edge in two broken runs
s.stroke([(0.30, 0.866), (0.42, 0.868), (0.55, 0.867)], "flat", p.at_value(p["pool_b"], 0.30),
         size=0.014, load=0.7, opacity=0.7, pressure=[0.2, 1.0, 0.3])
s.stroke([(0.60, 0.867), (0.72, 0.869)], "flat", p.at_value(p["pool_b"], 0.27),
         size=0.013, load=0.6, opacity=0.6, pressure=[0.3, 1.0, 0.2])
s.look()
s.look(region=span("F5", "H7"))
