# The last marks. The flattest passage left is the gap between the tree and the
# building: a puddle skinned with ice explains the ground plane there, and being a
# reflection of the sky it is lighter than the earth around it, which is the one
# thing in the foreground that is.
p["ice"]    = p.at_value(p.mix(p["neutral"], "cerulean", 0.10), 0.54)
p["icerim"] = p.at_value(p.mix(p["neutral"], "burnt_umber", 0.30), 0.34)

s.stroke([(0.276, 0.664), (0.330, 0.656), (0.386, 0.667)], "bristle", "ice",
         size=0.019, load=0.9, load_falloff=0.10, opacity=0.78,
         pressure=[0.4, 1.0, 0.5], note="ground")
s.stroke([(0.292, 0.676), (0.352, 0.672)], "bristle", "ice", size=0.011,
         load=0.7, load_falloff=0.15, opacity=0.60, pressure=[0.8, 0.2], note="ground")
s.stroke([(0.272, 0.671), (0.322, 0.679), (0.382, 0.673)], "liner", "icerim",
         size=0.0030, pressure=[0.0, 0.8, 0.3], load=1.0, opacity=0.62, note="ground")

# a second, much smaller, further off -- so the first reads as weather and not as an
# incident placed there
s.stroke([(0.436, 0.612), (0.474, 0.608), (0.508, 0.614)], "bristle", "ice",
         size=0.010, load=0.6, load_falloff=0.15, opacity=0.52,
         pressure=[0.3, 0.9, 0.4], note="ground")

# and two clods between them, to carry the eye across
for pts, sz in [([(0.352, 0.726), (0.372, 0.720)], 0.010),
                ([(0.246, 0.702), (0.232, 0.697)], 0.008)]:
    s.stroke(pts, "round_hard", "stone", size=sz, pressure=[1.0, 0.35],
             load=1.0, opacity=0.78, tip_wobble=0.7, note="ground")
