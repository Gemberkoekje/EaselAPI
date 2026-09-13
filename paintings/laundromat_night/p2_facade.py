# Pass 2, still the facade's own depth.
#
# Rehearsal 7 taught two things. The wall above the fascia is 0.02 tall, so a wash
# aimed there ran across the night sky instead -- this is a single-storey shopfront
# and the sodium lamp is at street level, so the light belongs on the piers and the
# wall's foot, not its top. And a solid band with a hard edge reads as its own mass
# at 0.03 of value: measured, the base course was 0.211 against a 0.180 wall and
# still came back a bright bar. So everything here gets an end thrown away.

# The lamp is off-canvas right. The right pier takes it first, along its own axis.
s.stroke([(0.975, 0.180), (0.968, 0.430), (0.978, 0.730)], "bristle", "facade_lt",
         size=0.055, load=1.0, load_falloff=0.0, opacity=0.55,
         pressure=[0.15, 0.8, 1.0], note="facade lamp")
s.stroke([(0.918, 0.230), (0.912, 0.470), (0.922, 0.730)], "bristle",
         p.mix("facade", "facade_lt", 0.55), size=0.040, load=1.0, load_falloff=0.0,
         opacity=0.45, pressure=[0.0, 0.6, 0.95], note="facade lamp")
# the narrow pier between window and door gets less of it, and from the other end
s.stroke([(0.750, 0.700), (0.746, 0.500), (0.752, 0.330)], "bristle",
         p.mix("facade", "facade_lt", 0.70), size=0.032, load=1.0, load_falloff=0.0,
         opacity=0.5, pressure=[1.0, 0.55, 0.1], note="facade lamp")

# The wall's foot, brightening toward the lamp: three passes the same way, one value
# step apart, each dying to nothing on the left. This is the base course as well.
for i in range(3):
    t = i / 2
    y = 0.652 + t * 0.038
    s.stroke([(0.10, y + 0.010), (0.52, y + 0.002), (1.06, y - 0.008)], "bristle",
             p.mix("facade", "facade_lt", 0.25 + 0.55 * t), size=0.036,
             load=1.0, load_falloff=0.0, opacity=0.42,
             pressure=[0.0, 0.45, 1.0], note="facade foot")

# The fascia board. A sign legitimately is a band, so it is kept subordinate: darker
# than the lamp-struck pier, tilted, its left end lost into the wall and its lower
# edge broken where the window will light it from below.
# Not solid, and not flat. The reason written here at the time was that a solid slab
# builds paint height and the relief lifts it in the view, and #33 measured that
# and it is false -- the view and the paint agree to 0.000 over a mass. The fascia at
# 0.225 only *looked* light against a 0.17 wall, which is local contrast and the
# false alarm the guide warns about. The call is kept because a bristle at 0.196 is
# the better mark anyway: a sign board unlit from the front is barely above the wall --
# what will make it read is the window lighting its underside, two passes from now.
s.block_in(fascia(), "bristle", p.at_value("facade", 0.196), density=0.9,
           size=0.030, direction=(5, 173), note="fascia")
s.stroke([(0.150, 0.292), (0.345, 0.286)], "bristle", "facade", size=0.062,
         load=0.50, opacity=0.60, pressure="lift_off", note="fascia lost end")
s.stroke([(0.906, 0.272), (0.870, 0.296)], "bristle", "facade_lt", size=0.022,
         load=0.60, opacity=0.50, pressure="lift_off", note="fascia lamp end")

# A downpipe on the right and a stain under it: one vertical incident to answer the
# stack on the roofline. It wanders; nothing here is ruled.
s.stroke([(0.893, 0.215), (0.887, 0.430), (0.896, 0.660)], "bristle", "facade_lt",
         size=0.013, load=0.85, opacity=0.70, jitter=0.03, pressure="even",
         note="downpipe")
s.stroke([(0.884, 0.480), (0.879, 0.575)], "bristle", "facade_dk", size=0.026,
         load=0.35, opacity=0.40, pressure="swell", note="facade stain")
print(s.budget_line())
