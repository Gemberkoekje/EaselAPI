"""own2, last three. The striped ladder on the top petal survived two passes
because every cover stroke ran radially past it rather than over it."""
p = s.palette
s.dry()
s.stroke([(0.432, 0.290), (0.424, 0.210), (0.418, 0.148)], "round_hard",
         p.mix(p["pet_mid"], p["pet_lit"], 0.55), size=0.052,
         pressure=[0.9, 1.0, 0.15], load=1.0, note="bury the ladder")
s.stroke([(0.408, 0.278), (0.397, 0.212), (0.392, 0.166)], "round_hard",
         p.mix(p["pet_mid"], p["pet_sh"], 0.30), size=0.030,
         pressure=[0.8, 1.0, 0.15], load=1.0, note="fold in that petal")
s.stroke([(0.452, 0.268), (0.448, 0.208)], "round_hard",
         p.mix(p["pet_sh"], p["pet_dk"], 0.30), size=0.011, opacity=0.5,
         pressure=[0.8, 0.15], load=1.0, note="its shadowed edge")
print("strokes:", s.stroke_count)
print(s.look())
print(s.export("own2_final.png"))
print(s.timelapse_gif("own2_timelapse.gif"))
