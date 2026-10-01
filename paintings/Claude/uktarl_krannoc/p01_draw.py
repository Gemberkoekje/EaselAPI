"""The drawing, as guides: free, and still on the view after the paint goes on."""

s.unguide()
for shape, note in ((mountain, "mountain"), (uk_collar, "collar"), (uk_head, "Uktarl"),
                    (uk_body, "body"), (uk_wing, "wing"), (uk_arm, "arm"), (uk_hand, "hand"),
                    (uk_cards_hand, "cards"), (table_top, "table"),
                    (a_head, "A"), (a_hair, ""), (a_body, "A body"), (d_head, "D"),
                    (d_ears[0], ""), (d_ears[1], ""), (d_body, "D body"),
                    (b_hood, "B"), (b_body, "B body"), (tub, "tub")):
    s.guide(shape, note=note)
for i, r in enumerate(rays):
    s.guide(r, note="")
s.guide([s.px(0, wall_base_y), s.px(CW, wall_base_y)], note="floor line")
s.mark("candle", *s.px(*candle_at))
s.mark("lantern", *s.px(*lantern_at))
