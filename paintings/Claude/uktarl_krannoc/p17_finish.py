"""The last marks: two edges lost into the dark at the sides, and the signature.

Her far side and the doppelganger's far side are the edges furthest from the light and
from Uktarl; losing a stretch of each lets the dark close round the table, and leaves the
crisp edges in the middle, where the eye is meant to be.

The signature is a small carved sunrise, the room's own sign: an arc and three short rays,
in the floor's dark at the bottom right, close in value to what it sits on.
"""

s.smudge(px_pts([(118, 612), (113, 652), (110, 692)]))
s.smudge(px_pts([(824, 640), (829, 690), (833, 738)]))

sig = p.at_value(p.mix("floor", "rim", 0.25), 0.21)
x, y = 990, 748
arc = [(x + 9 * math.cos(math.radians(a)), y - 9 * math.sin(math.radians(a)))
       for a in (0, 45, 90, 135, 180)]
s.stroke(px_pts(arc), "round_hard", sig, size=0.003, opacity=0.9, pressure="even",
         note="signature")
for a in (45, 90, 135):
    r0, r1 = 12, 19
    s.stroke(px_pts([(x + r0 * math.cos(math.radians(a)), y - r0 * math.sin(math.radians(a))),
                     (x + r1 * math.cos(math.radians(a)), y - r1 * math.sin(math.radians(a)))]),
             "round_hard", sig, size=0.003, opacity=0.9, pressure=[1.0, 0.4],
             note="signature")
