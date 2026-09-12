# Pass 7. What the light does once it is out of the window. This is the picture --
# a lit shop is only interesting for what it does to the street in front of it.
s.dry()

# Light going UP onto the underside of the fascia, and sideways onto the piers. The
# pier marks also bury the lit paint that the interior's overhang threw past the
# jamb, which was reading as a hard bright strip rather than as glow.
s.stroke([(0.196, 0.3225), (0.450, 0.3175), (0.706, 0.3215)], "bristle",
         p.at_value("facade_lt", 0.330), size=0.020, load=0.9, opacity=0.55,
         pressure=[0.3, 1.0, 0.55], note="subject glow")
s.stroke([(0.1660, 0.352), (0.1600, 0.470), (0.1670, 0.600)], "bristle",
         p.at_value("facade_lt", 0.315), size=0.024, load=0.9, opacity=0.50,
         pressure=[0.5, 1.0, 0.4], note="subject glow")
s.stroke([(0.7330, 0.350), (0.7390, 0.470), (0.7325, 0.600)], "bristle",
         p.at_value("facade_lt", 0.295), size=0.020, load=0.9, opacity=0.45,
         pressure=[0.4, 1.0, 0.35], note="subject glow")

# The sill's top surface takes the light square on -- the brightest thing outside
# the glass. The stall riser under it is shaded by that same sill, so it gets only
# what comes back up off the pavement.
s.stroke([(0.172, 0.6040), (0.396, 0.6070)], "round_hard",
         p.at_value("spill_cool", 0.575), size=0.0055, opacity=0.9, load=1.0,
         load_falloff=0.0, pressure=[0.2, 1.0, 0.35], note="subject glow")
s.stroke([(0.205, 0.668), (0.470, 0.674), (0.700, 0.668)], "bristle",
         p.at_value("facade_lt", 0.285), size=0.026, load=0.85, opacity=0.40,
         pressure="swell", note="subject glow")

# The pool on the sidewalk: five passes the same way, one value step apart, each
# dying to nothing at both ends so the pool has no drawn outline anywhere.
for i in range(5):
    t = i / 4
    y = 0.7135 + t * 0.0700
    s.stroke([(0.120 - 0.030 * t, y - 0.003), (0.450, y + 0.004),
              (0.790 + 0.030 * t, y - 0.002)], "bristle",
             p.at_value("spill_cool", 0.520 - 0.170 * t), size=0.034,
             load=1.0, load_falloff=0.0, opacity=0.45,
             pressure=[0.0, 1.0, 0.25], note="subject spill")
# and the door's own pool, which is narrower and reaches further because its light
# gets all the way to the ground
s.stroke([(0.772, 0.716), (0.845, 0.722), (0.925, 0.714)], "bristle",
         p.at_value("spill_cool", 0.480), size=0.026, load=1.0, load_falloff=0.0,
         opacity=0.50, pressure=[0.2, 1.0, 0.3], note="subject spill")
s.stroke([(0.780, 0.762), (0.850, 0.768), (0.915, 0.758)], "bristle",
         p.at_value("spill_cool", 0.390), size=0.024, load=1.0, load_falloff=0.0,
         opacity=0.45, pressure=[0.3, 1.0, 0.25], note="subject spill")
# the sill's lit edge, broken rather than ruled across the whole opening
s.stroke([(0.470, 0.6072), (0.640, 0.6055), (0.724, 0.6038)], "round_hard",
         p.at_value("spill_cool", 0.505), size=0.0045, opacity=0.8, load=1.0,
         load_falloff=0.0, pressure=[0.4, 1.0, 0.2], note="subject glow")

# ---------------------------------------------------------------- the reflection
# A reflection in a wet road is not a lit patch, it is streaks of light on dark
# asphalt with plenty of asphalt left between them. Laid as a scumble at opacity
# 0.60 it came back a pale slab filling the whole foreground and brighter than the
# sidewalk: the dabs overlap, so a low opacity accumulates back toward full colour
# rather than thinning. So the scumble is only a faint lift now, dying to almost
# nothing at the bottom edge, and the streaks are the reflection.
# Even at opacity 0.26 the base lift took 60% of the road from 0.22 up to 0.40 and
# the sidewalk, the kerb and the road became one pale field -- which was a fault in
# the design rather than in the value. The base is now barely perceptible and the
# streaks do all of the work.
s.scumble(reflection(), p.at_value("refl_hi", 0.290), p.at_value("refl_lo", 0.215),
          4, size=0.130, load=1.0, load_falloff=0.0, opacity=0.16,
          note="subject reflection")

# The streaks: running toward the viewer, spreading a little as they come, and they
# break the scumble's horizontal passes as well as being the thing itself. No two
# the same width, length or value.
for x0, x1, y1, sz, val, op in ((0.248, 0.222, 1.05, 0.020, 0.500, 0.55),
                                (0.313, 0.298, 0.958, 0.012, 0.430, 0.45),
                                (0.404, 0.392, 1.02, 0.024, 0.535, 0.60),
                                (0.479, 0.466, 0.922, 0.011, 0.415, 0.40),
                                (0.598, 0.616, 1.05, 0.018, 0.480, 0.52),
                                (0.678, 0.704, 0.978, 0.014, 0.400, 0.40)):
    s.stroke([(x0, 0.760), (0.5 * (x0 + x1), 0.5 * (0.760 + y1)), (x1, y1)],
             "bristle", p.at_value("refl_hi", val), size=sz, load=1.0,
             load_falloff=0.30, opacity=op, pressure=[1.0, 0.55, 0.0],
             note="subject reflection")
# three broader, softer, dimmer ones give the smear some body without flooding it
for x0, x1, y1, sz, val in ((0.275, 0.250, 0.905, 0.048, 0.360),
                            (0.445, 0.432, 0.975, 0.055, 0.375),
                            (0.640, 0.664, 0.885, 0.042, 0.340)):
    s.stroke([(x0, 0.762), (0.5 * (x0 + x1), 0.5 * (0.762 + y1)), (x1, y1)],
             "bristle", p.at_value("refl_hi", val), size=sz, load=1.0,
             load_falloff=0.35, opacity=0.30, pressure=[0.9, 0.5, 0.0],
             note="subject reflection")

# two of them are the mullions' own shadows, which is what ties the smear on the
# road to the window above it
for x0, x1, y1, sz in ((0.341, 0.320, 0.995, 0.016), (0.553, 0.570, 0.945, 0.013)):
    s.stroke([(x0, 0.758), (0.5 * (x0 + x1), 0.5 * (0.758 + y1)), (x1, y1)],
             "bristle", p.at_value("refl_lo", 0.225), size=sz, load=1.0,
             load_falloff=0.30, opacity=0.45, pressure=[1.0, 0.5, 0.0],
             note="subject reflection")

# The door's reflection: three marks, not a mass. It is dimmer than the window's
# and it reaches further, because the door's light gets all the way to the ground.
for x0, x1, y1, sz, val in ((0.800, 0.788, 1.05, 0.015, 0.430),
                            (0.848, 0.862, 0.965, 0.011, 0.385),
                            (0.884, 0.906, 1.01, 0.013, 0.355)):
    s.stroke([(x0, 0.748), (0.5 * (x0 + x1), 0.5 * (0.748 + y1)), (x1, y1)],
             "bristle", p.at_value("refl_hi", val), size=sz, load=1.0,
             load_falloff=0.30, opacity=0.45, pressure=[1.0, 0.55, 0.0],
             note="subject reflection")
print(s.budget_line())
