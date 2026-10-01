"""The card game: the candle, the cards, the coins.

Their laps first, so nothing ends on a ruled line above the floor. Then the candle: a
holder, the wax, the flame, and a film of its light in the air. The cards are chisel marks,
the one place a flat's own shape stands for the thing: a fan in Uktarl's hand at his chest,
one in hers, two in the doppelganger's long fingers, three lying on the table along its
slant. Each stack of coins is a body and a lit rim; a few loose coins, each one different.
"""

s.block_in(a_lower, "flat", "plum", size=0.05, solid=True, edge="hard", direction=95)
s.block_in(d_lower, "flat", "black", size=0.05, solid=True, edge="hard", direction=95)

cx, cy = candle_base
s.stroke(px_pts([(cx - 15, cy + 2), (cx, cy + 4), (cx + 15, cy + 2)]), "round_hard",
         p.at_value(p.mix("black", "copper", 0.3), 0.18), size=0.012, opacity=0.95,
         pressure=[0.3, 1.0, 0.3])
s.stroke(px_pts([(cx, cy), (cx, cy - 22), (cx + 1, cy - 40)]), "flat", "wax", size=0.011,
         solid=True, pressure="even")
s.stroke(px_pts([(cx - 4, cy - 30), (cx - 4, cy - 6)]), "flat",
         p.at_value(p.mix("wax", "wood", 0.4), 0.55), size=0.004, opacity=0.8,
         pressure="even")
s.stroke(px_pts([(cx + 1, cy - 42), (cx + 1, cy - 50), (cx + 2, cy - 60)]), "round_hard",
         "flame", size=0.010, opacity=1.0, pressure=[1.0, 0.8, 0.15])
s.dry()
s.glaze(px_pts([(cx, cy - 34), (cx + 1, cy - 50), (cx + 2, cy - 66)]),
        p.at_value(p.mix("glow", "wood_lit", 0.5), 0.50), opacity=0.14, size=0.07,
        pressure=[0.6, 1.0, 0.4])


def fan(hand, cards, mix, size):
    """Each card a chisel mark from the hand; every other one a step darker, so the
    edge where one card lies over the next can be found."""
    hx, hy = hand
    for i, (ang, length) in enumerate(cards):
        a = math.radians(ang - 90)
        tip = (hx + length * math.cos(a), hy + length * math.sin(a))
        colour = mix if i % 2 == 0 else p.at_value(mix, p.value_of(mix) - 0.13)
        s.stroke(px_pts([(hx, hy), tip]), "flat", colour, size=size, solid=True,
                 pressure="even", note="cards")


fan(uk_fan_hand, UK_FAN, "card", 0.017)
s.stroke(px_pts([(uk_fan_hand[0] - 9, uk_fan_hand[1] + 4), (uk_fan_hand[0] + 6,
                  uk_fan_hand[1] + 2)]), "round_hard", "face_mid", size=0.011,
         opacity=0.95, pressure="even", note="subject")
fan(a_fan_hand, A_FAN, p.at_value("card", 0.70), 0.014)
s.stroke(px_pts(d_hand), "round_hard", p.at_value(p.mix("d_skin", "face_lit", 0.3), 0.58),
         size=0.006, opacity=0.9, pressure=[0.6, 1.0, 0.4])
fan(d_hand[0], D_FAN, p.at_value("card", 0.66), 0.013)
for a, b in TABLE_CARDS:
    s.stroke(px_pts([a, b]), "flat", p.at_value("card", 0.62), size=0.011, solid=True,
             pressure="even", note="cards")

for (x, y), h, metal in COIN_STACKS:
    s.stroke(px_pts([(x, y), (x, y - h)]), "flat", p.at_value(p.mix(metal, "wood", 0.45), 0.30),
             size=0.012, solid=True, pressure="even")
    s.stroke(px_pts([(x - 6, y - h - 1), (x + 6, y - h - 1)]), "flat", metal, size=0.006,
             solid=True, pressure="even")
for i, ((x, y), size, metal) in enumerate(LOOSE_COINS):
    s.stroke(px_pts([(x - 3 - i, y + 1), (x + 3 + i, y - 1)]), "round_hard", metal,
             size=size, opacity=0.95, pressure=[0.6, 1.0], tip_wobble=0.4)
rx, ry = silver_ring
s.stroke(px_pts([(rx - 6, ry + 1), (rx, ry - 3), (rx + 6, ry + 1), (rx, ry + 3)]),
         "round_hard", "silver", size=0.004, opacity=0.95, pressure=[0.3, 1.0, 1.0, 0.3])
