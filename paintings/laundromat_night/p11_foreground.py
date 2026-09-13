# Pass 11. Fifty-one strokes were left, which is too many to leave in hand, and the
# weakest passage has moved: the left third got its pass, so what is thinnest now is
# the near foreground. The road's scumble still bands faintly across the bottom
# where no reflection streak reaches it, the sidewalk is one uniform strip the whole
# width of the canvas, and the bottom-right corner has nothing in it at all.
s.dry()

# Four marks across the bands at four angles, two lighter and two darker, in the
# stretches the reflection never reached. A surface's grain varies -- it breaks, it
# crosses, it disappears for a whole passage.
for pts, sz, val, ld, op in (
        ([(0.775, 0.842), (0.860, 0.930), (0.900, 1.055)], 0.036, 0.290, 0.85, 0.45),
        ([(1.055, 0.880), (0.965, 0.952), (0.930, 1.055)], 0.028, 0.180, 0.80, 0.45),
        ([(0.245, 1.055), (0.205, 0.960), (0.225, 0.905)], 0.024, 0.185, 0.80, 0.40),
        ([(0.505, 1.055), (0.545, 0.968), (0.530, 0.908)], 0.030, 0.275, 0.85, 0.40)):
    s.stroke(pts, "bristle", p.at_value("kerb", val), size=sz, load=ld,
             opacity=op, pressure="swell", note="foreground")

# A second wet patch, on the right to answer the puddle on the left. Varied rather
# than repeated: it is smaller, it has no crisp near edge, it reflects the shop
# instead of the sky, and it is three strokes rather than a mass -- so it reads as
# the same street, not as the same object twice.
for pts, sz, val, op in (
        ([(0.782, 0.9210), (0.846, 0.9165), (0.906, 0.9245)], 0.030, 0.300, 0.40),
        ([(0.800, 0.9385), (0.862, 0.9340)], 0.022, 0.345, 0.35),
        ([(0.828, 0.9105), (0.884, 0.9155)], 0.016, 0.275, 0.30)):
    s.stroke(pts, "bristle", p.at_value("refl_hi", val), size=sz, load=0.85,
             opacity=op, pressure="swell", note="foreground")

# A gutter drain set into the kerb. Rehearsed once at 0.165 against a 0.40 band
# with a bright lip over it, and it came back a black domino stuck on the pavement
# -- an object in the picture rather than a hole in the street. Seen from across a
# road at night this is a quiet dark slot and nothing else, so the contrast comes
# down by half, the lip goes, and its ends are allowed to taper away.
s.stroke([(0.2680, 0.7888), (0.3065, 0.7870)], "flat",
         p.at_value("kerb", 0.250), size=0.013, load=1.0, load_falloff=0.0,
         opacity=0.85, pressure=[0.35, 1.0, 0.30], note="foreground drain")
s.stroke([(0.2730, 0.7948), (0.3010, 0.7930)], "bristle",
         p.at_value("kerb", 0.285), size=0.012, load=0.8, opacity=0.45,
         pressure="swell", note="foreground drain")

# The sidewalk: a slab joint running back at an angle, a stain, and a second crack,
# so a strip the full width of the canvas has something in it besides the pool.
s.stroke([(0.470, 0.7060), (0.508, 0.7480), (0.530, 0.7880)], "round_hard",
         p.at_value("asphalt", 0.245), size=0.0050, load=0.9, opacity=0.60,
         jitter=0.04, pressure=[0.25, 1.0, 0.35], note="foreground")
s.stroke([(0.640, 0.7220), (0.700, 0.7340), (0.742, 0.7280)], "bristle",
         p.at_value("kerb", 0.300), size=0.026, load=0.80, opacity=0.40,
         pressure="swell", note="foreground")
s.stroke([(0.148, 0.7480), (0.196, 0.7280), (0.232, 0.7120)], "round_hard",
         p.at_value("asphalt", 0.230), size=0.0040, load=0.9, opacity=0.50,
         jitter=0.04, pressure="taper", note="foreground")

# Three marks across the pool's own horizontal passes, which are the last banding
# left in the picture.
for pts, sz, val, op in (
        ([(0.300, 0.7025), (0.336, 0.7420), (0.352, 0.7860)], 0.024, 0.415, 0.35),
        ([(0.588, 0.7080), (0.560, 0.7440), (0.572, 0.7840)], 0.020, 0.380, 0.30),
        ([(0.408, 0.7860), (0.440, 0.7460), (0.428, 0.7060)], 0.016, 0.450, 0.30)):
    s.stroke(pts, "bristle", p.at_value("spill_cool", val), size=sz, load=0.85,
             opacity=op, pressure="swell", note="foreground")

# The kerb, continued either side of the stretch that was found in pass 8 -- broken,
# and dimmer as it goes away from the light, so it is one kerb and not three marks.
s.stroke([(0.700, 0.7762), (0.800, 0.7720), (0.884, 0.7672)], "bristle",
         p.at_value("kerb", 0.355), size=0.010, load=0.85, load_falloff=0.15,
         opacity=0.70, pressure=[1.0, 0.6, 0.15], note="foreground")
s.stroke([(0.196, 0.7905), (0.290, 0.7880)], "bristle",
         p.at_value("kerb", 0.300), size=0.009, load=0.75, opacity=0.55,
         pressure="swell", note="foreground")

# And the two bottom corners weighted down, so the eye stays up at the window.
s.stroke([(-0.05, 1.055), (0.070, 1.010), (0.130, 1.055)], "bristle",
         p.at_value("asphalt", 0.155), size=0.055, load=0.9, opacity=0.45,
         pressure="swell", note="foreground")
s.stroke([(1.055, 1.010), (0.960, 1.030), (0.880, 1.055)], "bristle",
         p.at_value("asphalt", 0.165), size=0.048, load=0.9, opacity=0.40,
         pressure="swell", note="foreground")
print(s.budget_line())
