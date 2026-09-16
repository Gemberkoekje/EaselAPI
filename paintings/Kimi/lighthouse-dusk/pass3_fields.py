# Pass 3: graded fields, the beam as lit air, and the first broken reflection.
sky_mass()
sky_glow_mass()

# A far dark edge interrupts the horizon without becoming a second subject.
s.block_in(headland(), "flat", "tower_dark", size=0.018, density=1.0,
           solid=True, direction="axis", edge="hard", opacity=1.0,
           pressure="even")

sea_mass()

# Clouds: three starved marks, no two alike, crossing the sky bands.
s.stroke([(0.10, 0.145), (0.28, 0.175), (0.46, 0.150)], "bristle", "sky_mid",
         size=0.030, load=0.35, opacity=0.38, pressure="swell")
s.stroke([(0.54, 0.120), (0.72, 0.155), (0.94, 0.135)], "bristle", "horizon_gold",
         size=0.022, load=0.28, opacity=0.26, pressure="swell")
s.stroke([(0.06, 0.330), (0.24, 0.305), (0.39, 0.325)], "bristle", "sky_high",
         size=0.020, load=0.30, opacity=0.32, pressure="taper")

# The beam is air, not a surface: dry first, then three films close to the field.
field = s.sample(sky_low())
v = p.value_of(field)
p["beam_far"] = p.at_value(p.mix(field, "horizon_gold", 0.45), min(v + 0.06, 0.74))
p["beam_body"] = p.at_value(p.mix(field, "gold_core", 0.35), min(v + 0.12, 0.80))
p["beam_core"] = p.at_value(p.mix(field, "lamp_glass", 0.32), min(v + 0.18, 0.86))
s.dry()
s.glaze([s.pt("lamp"), (0.46, 0.325), s.pt("beam_far")], "beam_far",
        opacity=0.09, size=0.20, pressure=[0.4, 0.8, 1.0])
s.glaze([s.pt("lamp"), (0.46, 0.320), (-0.06, 0.365)], "beam_body",
        opacity=0.14, size=0.11, pressure=[1.0, 0.75, 0.35])
s.glaze([s.pt("lamp"), (0.55, 0.300), (0.25, 0.345)], "beam_core",
        opacity=0.16, size=0.055, pressure=[1.0, 0.65, 0.10])
# A faint return on the right keeps the lamp from becoming a one-way searchlight.
s.glaze([s.pt("lamp"), (0.78, 0.285), (1.06, 0.305)], "beam_far",
        opacity=0.07, size=0.10, pressure=[0.8, 0.6, 0.3])

# Warm path on the water: broken, slightly bent flashes. The tower and rock
# will interrupt the middle, so the marks are built as visible pieces rather
# than as a ruled column of rectangles.
s.dry()
for points, size, op in [
    ([(0.585, 0.546), (0.635, 0.540), (0.724, 0.548)], 0.012, 0.40),
    ([(0.600, 0.575), (0.648, 0.569), (0.712, 0.576)], 0.009, 0.34),
    ([(0.620, 0.608), (0.658, 0.602), (0.700, 0.609)], 0.007, 0.27),
    ([(0.595, 0.650), (0.630, 0.644), (0.672, 0.651)], 0.006, 0.22),
    ([(0.700, 0.646), (0.735, 0.642), (0.770, 0.648)], 0.005, 0.18),
]:
    s.stroke(points, "bristle", "horizon_gold", size=size, load=0.42,
             opacity=op, pressure="swell", note="subject")

s.look(values=True, path="pass3_values.png")
s.look(path="pass3_colour.png")
