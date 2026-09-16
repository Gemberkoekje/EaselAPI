# The tree in the yard: the only event on the left, and it must stay quiet. A bare
# tree at twelve metres in flat light is mostly a soft haze of twigs with a few
# darker lines in it -- so the mass goes down first and the sticks are few.
p["twig"]   = p.at_value(p.mix(p["neutral"], "burnt_umber", 0.32), 0.53)
p["twigdk"] = p.at_value(p.mix(p["neutral"], "burnt_umber", 0.40), 0.45)
p["bough"]  = p.at_value(p.mix(p.mix("burnt_umber", "ultramarine", 0.40),
                               "yellow_ochre", 0.10), 0.38)
p["trunk"]  = p.at_value(p.mix("burnt_umber", "ultramarine", 0.44), 0.31)

# --- the twig mass. A starved brush gave chunks, which read as lichen; twigs at
# twelve metres are a veil, so it is glazes, laid along the way the boughs run.
for pts, sz, op in [
    # one broad wandering veil over the whole crown, to make it one mass
    ([(0.052, 0.244), (0.118, 0.160), (0.196, 0.196), (0.242, 0.290),
      (0.176, 0.388), (0.096, 0.404), (0.058, 0.318)], 0.090, 0.10),
    # then shorter ones that cross it, none starting where another does
    ([(0.068, 0.372), (0.134, 0.300), (0.212, 0.252)], 0.062, 0.11),
    ([(0.226, 0.178), (0.158, 0.244), (0.104, 0.336)], 0.054, 0.10),
    ([(0.088, 0.146), (0.146, 0.218), (0.180, 0.320)], 0.046, 0.09),
    ([(0.198, 0.372), (0.152, 0.286), (0.126, 0.178)], 0.040, 0.08),
    ([(0.036, 0.284), (0.102, 0.252), (0.166, 0.288)], 0.034, 0.08),
    ([(0.152, 0.438), (0.184, 0.354), (0.148, 0.262)], 0.030, 0.07),
    ([(0.114, 0.108), (0.166, 0.128), (0.208, 0.180)], 0.026, 0.06)]:
    s.glaze(pts, "twigdk", opacity=op, size=sz, note="dist")

# --- the trunk: one stroke, not straight, and lost where the twigs take over
s.stroke([(0.126, 0.642), (0.130, 0.552), (0.137, 0.462), (0.141, 0.386), (0.146, 0.318)],
         "round_hard", "trunk", size=0.013, pressure=[1.0, 0.88, 0.70, 0.44, 0.0],
         load=1.0, opacity=0.92, jitter=0.016, note="dist")
s.dab(0.124, 0.648, "round_hard", p.at_value(p["trunk"], 0.24), size=0.015,
      press=2, tip_wobble=0.7, note="dist")          # where it meets the ground

# --- three boughs only, at three weights, none matching another across the trunk
s.stroke([(0.140, 0.388), (0.092, 0.300), (0.056, 0.224)], "round_hard", "bough",
         size=0.0075, pressure=[0.9, 0.45, 0.0], load=0.9, opacity=0.82,
         jitter=0.016, note="dist")
s.stroke([(0.144, 0.330), (0.198, 0.268), (0.238, 0.196)], "round_hard", "bough",
         size=0.0055, pressure=[0.8, 0.35, 0.0], load=0.9, opacity=0.70,
         jitter=0.016, note="dist")
s.stroke([(0.148, 0.268), (0.126, 0.182), (0.116, 0.118)], "round_hard", "bough",
         size=0.004, pressure=[0.6, 0.28, 0.0], load=0.9, opacity=0.58,
         jitter=0.016, note="dist")

# --- the one bough that crosses the sky, tying the left of the picture to the
#     right, and lost for a stretch where it passes the brightest haze
s.stroke([(0.150, 0.150), (0.276, 0.116), (0.386, 0.094)], "liner", "bough",
         size=0.0042, pressure=[0.75, 0.42, 0.0], load=1.0, opacity=0.62, note="dist")
s.stroke([(0.530, 0.062), (0.656, 0.046), (0.800, 0.031)], "liner", "bough",
         size=0.0032, pressure=[0.0, 0.42, 0.20], load=1.0, opacity=0.48, note="dist")
