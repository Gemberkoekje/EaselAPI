# Ripples. The starved bristle's speckle is what reads as water; a round tip at this
# size lays a tidy capsule, so only three of those survive, as accents by the lamps.
# Tilts deliberately spread, and two whole passages left with nothing in them.
s.dry()
rip = [
  ([(0.276, 0.706), (0.352, 0.716), (0.418, 0.704)], "bristle", "watlit",  0.034, 0.42, 0.85, "swell"),
  ([(0.432, 0.742), (0.505, 0.722), (0.560, 0.726)], "bristle", "glow2",   0.030, 0.34, 0.75, "taper"),
  ([(0.470, 0.658), (0.556, 0.670), (0.618, 0.657)], "bristle", "glow2",   0.027, 0.38, 0.70, "lift_off"),
  ([(0.612, 0.628), (0.699, 0.645), (0.760, 0.634)], "bristle", "glow1",   0.029, 0.30, 0.60, "swell"),
  ([(0.236, 0.790), (0.312, 0.822), (0.372, 0.828)], "bristle", "water",   0.044, 0.32, 0.55, "taper"),
  ([(0.398, 0.906), (0.474, 0.938)],                 "bristle", "water",   0.052, 0.26, 0.42, "swell"),
  ([(0.586, 0.536), (0.658, 0.527)],                 "bristle", "glow1",   0.026, 0.20, 0.42, "taper"),
  ([(0.498, 0.606), (0.566, 0.617), (0.614, 0.609)], "bristle", "glow1",   0.026, 0.26, 0.50, "swell"),
  ([(0.318, 0.646), (0.379, 0.652)], "round_hard", "glow3", 0.011, 1.0, 0.90, "lift_off"),
  ([(0.398, 0.688), (0.446, 0.697)], "round_hard", "glow2", 0.008, 1.0, 0.75, "taper"),
  ([(0.684, 0.572), (0.730, 0.581)], "round_hard", "glow2", 0.007, 1.0, 0.60, "taper"),
  ([(0.452, 0.694), (0.532, 0.706)], "bristle", "watrefl", 0.030, 0.45, 0.55, "taper"),
  ([(0.300, 0.766), (0.368, 0.776)], "bristle", "watrefl", 0.027, 0.40, 0.50, "lift_off"),
]
for pts, brush, col, size, load, op, press in rip:
    kw = dict(tip_wobble=0.55) if brush == "round_hard" else {}
    s.stroke(pts, brush, col, size=size, load=load, opacity=op, pressure=press,
             load_falloff=0.30, note="subject", **kw)
print(s.look(region="B4:H8"))
