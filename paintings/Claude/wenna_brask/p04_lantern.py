"""Pass 4: the lantern -- its bracket and ring, the horn panes lit from inside, the flame, the
iron straps, cap and base; then the light it throws into the air round it."""

p["horn_dim"] = p.at_value(p.mix("horn", "burnt_sienna", 0.3), 0.58)
p["horn_hot"] = p.at_value(p.mix("horn", "flame", 0.5), 0.86)
p["iron_lit"] = p.at_value(p.mix("iron", "horn", 0.35), 0.30)
IRON = dict(opacity=0.95, load=1.0, load_falloff=0.0, jitter=0.01, size_jitter=0.03,
            pressure="even")


def lay_bracket():
    # Iron, so nearly ruled: half the default wander, run off the canvas at the wall end.
    s.stroke(bracket, "flat", "iron", size=0.011, **IRON)
    s.stroke(brace, "flat", "iron", size=0.008, **IRON)
    s.stroke(ring, "round_hard", "iron", size=0.004, opacity=0.95, pressure="even")
    # Iron on a dark wall disappears: the lamp below lights the bar's underside, strongest
    # over the lamp and gone by the wall.
    s.stroke([P(604, 192), P(664, 192), P(744, 191)], "round_hard", "iron_lit", size=0.003,
             opacity=0.85, pressure=[1.0, 0.5, 0.05])


def lay_panes():
    s.block_in(lantern, "flat", "horn_dim", size=0.02, density=1.0, solid=True,
               direction=90, edge="hard", note="subject")
    # The glow inside the horn: brightest round the flame, dim at the corners.
    s.stroke([P(598, 262), P(598, 302), P(598, 344)], "round_soft", "horn", size=0.07,
             opacity=0.8, pressure="swell", clip=lantern, note="subject")
    s.stroke([P(598, 282), P(598, 304), P(598, 326)], "round_soft", "horn_hot", size=0.035,
             opacity=0.85, pressure="swell", clip=lantern, note="subject")


def lay_flame():
    s.stroke([P(598, 318), P(597, 305), P(599, 291)], "round_hard", "flame", size=0.011,
             opacity=1.0, pressure=[1.0, 0.8, 0.1], tip_wobble=0.35, note="subject")


def lay_iron():
    # The straps: both edges and one across the front, off centre so the flame shows. No two
    # the same weight.
    for pts, size in (([P(563, 240), P(564, 360)], 0.0065), ([P(633, 240), P(632, 360)], 0.005),
                      ([P(583, 240), P(584, 360)], 0.004)):
        s.stroke(pts, "flat", "iron", size=size, note="subject", **IRON)
    s.block_in(cap, "flat", "iron", size=0.014, density=1.0, solid=True, direction=0,
               edge="hard", note="subject")
    s.block_in(base, "flat", "iron", size=0.012, density=1.0, solid=True, direction=0,
               edge="hard", note="subject")
    # The rims catch the light from inside, brightest over the flame.
    s.stroke([P(560, 240), P(598, 242), P(636, 240)], "round_hard", "iron_lit", size=0.004,
             opacity=0.8, pressure=[0.2, 1.0, 0.3], note="subject")
    s.stroke([P(554, 360), P(598, 361), P(642, 360)], "round_hard", "iron_lit", size=0.004,
             opacity=0.8, pressure=[0.3, 1.0, 0.2], note="subject")


def lay_halo():
    # Lit air round the lamp, mixed close to the wall it sits in, kept off her face.
    field = s.sample(poly([(650, 250), (720, 250), (720, 360), (650, 360)], "beside the lamp"))
    v = p.value_of(field)
    p["halo_far"] = p.at_value(p.mix(field, "horn", 0.4), v + 0.06)
    p["halo_near"] = p.at_value(p.mix("horn", field, 0.45), v + 0.12)
    s.dry()
    s.glaze([P(574, 302), P(598, 298), P(622, 302)], "halo_far", opacity=0.10, size=0.20,
            pressure="swell")
    s.glaze([P(586, 300), P(598, 298), P(610, 300)], "halo_near", opacity=0.14, size=0.12,
            pressure="swell")
    s.dry()


lay_bracket()
lay_panes()
lay_flame()
lay_iron()
lay_halo()
print(s.look(region="F1:H4", path="looks/04-lantern-crop.png"))
print(s.look(values=True, path="looks/04-lantern-values.png"))
print(s.look(path="looks/04-lantern.png"))
