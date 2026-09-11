# Pass 6: the last cleanups above the sill, then the mug (behind the pears).
exec(open("helpers.py").read())
p = s.palette
# run the pane stroke the other way with a brush that does not run dry
s.stroke([(0.67, 0.55), (0.155, 0.55)], "flat", "window", size=0.04, pressure="even",
         load=1.0, load_falloff=0.0, note="pane, right to left")
s.stroke([(0.705, -0.02), (0.705, 0.575)], "flat", "wall", size=0.05, pressure="even",
         load=1.0, load_falloff=0.0, note="right jamb, unified")
s.stroke([(1.03, 0.60), (-0.03, 0.60)], "flat", "sill", size=0.045, pressure="even",
         load=1.0, load_falloff=0.0, note="sill far edge, straight")
s.stroke([(1.03, 0.825), (-0.03, 0.825)], "flat", "wall_low", size=0.04, pressure="even",
         load=1.0, load_falloff=0.0, note="wall below sill, top edge")
s.stroke([(-0.03, 0.665), (0.27, 0.665)], "flat", "sill", size=0.08, pressure="lift_off",
         load=1.0, note="sill left end")

# the mug: body, then the opening back to front, then handle
p["mug_shade"] = to_value(p["mug"], 0.28)
s.dry()
body = polygon([(0.505, 0.415), (0.625, 0.415), (0.62, 0.675), (0.51, 0.675)])
print("mug body cost", s.cost({"shape": body, "brush": "flat", "size": 0.028, "direction": 90}))
s.block_in(body, "flat", "mug", density=1.0, size=0.028, direction=90, load=1.0, note="mug body")
s.stroke([(0.60, 0.43), (0.605, 0.55), (0.60, 0.665)], "flat", "mug_shade", size=0.03,
         pressure=[0.7, 1.0, 0.9], load=1.0, note="mug, shadow side")
s.stroke([(0.515, 0.43), (0.513, 0.55), (0.517, 0.66)], "flat", "mug_lit", size=0.014,
         pressure=[0.9, 0.6, 0.4], load=1.0, note="mug, light on the window side")
# the opening: far lip, the inside, the near lip
s.stroke([(0.505, 0.413), (0.535, 0.395), (0.565, 0.391), (0.595, 0.395), (0.625, 0.413)],
         "round_hard", "mug_lit", size=0.012, pressure="even", load=1.0, note="far lip")
s.stroke([(0.512, 0.413), (0.565, 0.402), (0.618, 0.413)], "round_hard", "mug_in",
         size=0.018, pressure=[0.6, 1.0, 0.6], load=1.0, note="inside of the mug")
s.stroke([(0.505, 0.414), (0.535, 0.430), (0.565, 0.434), (0.595, 0.430), (0.625, 0.414)],
         "round_hard", "mug", size=0.012, pressure="even", load=1.0, note="near lip")
s.stroke([(0.622, 0.47), (0.668, 0.50), (0.678, 0.545), (0.66, 0.59), (0.618, 0.605)],
         "round_hard", "mug", size=0.02, pressure=[0.9, 1.0, 1.0, 0.9], load=1.0, note="handle")
print("strokes:", s.stroke_count)
print(s.look(grid=True))
print(s.look(region="D3:F6"))
