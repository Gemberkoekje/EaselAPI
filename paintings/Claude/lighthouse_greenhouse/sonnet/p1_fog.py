# Pass 1: the fog, furthest of all -- sky and sea as one field, since fog is the
# whole point: there is no horizon to draw. A quiet underlayer with the ground
# still breathing through, then the gradient as two long soft passages that
# *meet* at the glow rather than three short ones stacked -- three scumbles at
# 7-8 passes each came back a stack of visible bars (rehearsed first): the
# jump per step was too big and there were two extra seams where the calls
# met. Two passages at fourteen passes each, sharing one target colour where
# they overlap, is what actually loses the joins. Ripples last, few and
# faint, because fog flattens contrast on water same as anywhere else.
s.block_in(fog(), "bristle", "fog", size=0.22, density=0.75, direction=(4, 94),
           note="fog underlayer")
s.scumble(Region(-0.06, -0.06, 1.04, 0.46), "fog_deep", "glow", 14, brush="flat",
          size=0.20, opacity=0.4, note="fog upper, brightening down to the glow")
s.scumble(Region(-0.06, 0.34, 1.04, 0.86), "glow", "sea_near", 14, brush="flat",
          size=0.22, opacity=0.4, note="the glow giving back onto the water")
ripples = [  # (points, size, colour, opacity): tapered, no two alike, all quiet
    ([(0.05, 0.66), (0.22, 0.658), (0.40, 0.663)],  0.008, "sea_far",  0.35),
    ([(0.50, 0.70), (0.66, 0.697), (0.80, 0.703)],  0.009, "sea_near", 0.35),
    ([(0.60, 0.755), (0.78, 0.752)],                0.007, "sea_far",  0.30),
    ([(0.10, 0.78), (0.28, 0.783), (0.44, 0.779)],  0.010, "sea_near", 0.35),
    ([(0.68, 0.80), (0.90, 0.803)],                 0.008, "sea_near", 0.30),
]
for pts, size, colour, op in ripples:
    s.stroke(pts, "round_hard", colour, size=size, opacity=op, pressure="swell",
             note="ripple")
print(s.look(values=True))
print(s.look())
