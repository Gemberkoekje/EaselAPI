# Pass 9: the surroundings again, and the edges. Three broken strokes of fog
# drift across the beam at different angles, so the beam is in the fog rather
# than painted on it. The tower gets three dry-brush streaks --
# down the lit face, down the shadow side, and a green damp stain running from
# under the gallery where the watering has got out -- so its pass structure
# reads as weathering. Two foam marks where the sea meets the spur, on the
# water side of the boundary. Two darker rays in the beam near the lamp (the
# shadows of leaves in the light) and a pale streak across the far sea were
# rehearsed with these and dropped: both read as marks drawn on the picture.
p["fog_wisp"]  = p.at_value("fog", 0.69)
p["foam"]      = p.at_value(p.mix("sea_far", "titanium_white", 0.5), 0.68)
p["stain"]     = p.at_value(p.mix("leaf", "tower_lit", 0.5), 0.45)
# fog drifting across the beam
s.stroke([(0.10, 0.31), (0.28, 0.345), (0.46, 0.335)], "bristle", "fog_wisp", size=0.05, load=0.4,
         opacity=0.45, pressure="swell", note="fog drift")
s.stroke([(0.24, 0.425), (0.40, 0.405)], "bristle", "fog_wisp", size=0.04, load=0.35,
         opacity=0.4, pressure="taper", note="fog drift")
s.stroke([(-0.02, 0.485), (0.14, 0.50), (0.24, 0.49)], "bristle", "fog_wisp", size=0.06, load=0.4,
         opacity=0.4, pressure="swell", note="fog drift, low")
# weathering on the tower
s.stroke([(TX - 0.033, 0.36), (TX - 0.036, 0.50), (TX - 0.040, 0.64)], "bristle",
         p.at_value("tower_sh", 0.46), size=0.018, load=0.35, opacity=0.5, pressure="taper",
         note="weathering, lit face")
s.stroke([(TX + 0.038, 0.42), (TX + 0.044, 0.60), (TX + 0.05, 0.78)], "bristle",
         p.at_value("tower_lit", 0.42), size=0.016, load=0.3, opacity=0.45, pressure="taper",
         note="weathering, shadow side")
s.stroke([(TX - 0.012, 0.325), (TX - 0.010, 0.42), (TX - 0.013, 0.52)], "bristle", "stain",
         size=0.012, load=0.3, opacity=0.5, pressure="lift_off", note="subject damp stain from the watering")
# foam at the spur, on the water side
s.stroke([(0.435, 0.958), (0.465, 0.936)], "round_hard", "foam", size=0.008, load=0.45,
         opacity=0.75, pressure="taper", note="water's edge")
s.stroke([(0.395, 1.005), (0.43, 0.982)], "round_hard", "foam", size=0.010, load=0.4,
         opacity=0.7, pressure="swell", note="water's edge, lower")
print(s.look(values=True))
print(s.look())
