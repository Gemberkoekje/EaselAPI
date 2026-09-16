# Pass 1, the furthest things. The sky grades down toward the rooflines, so it is a
# scumble rather than a block-in: same cost, and it arrives already graded. A wide
# brush and solid=True, because the first rehearsal came back as horizontal streaks
# of bare ground -- the pass structure, which is the one thing to hide here.
s.scumble(sky(), "sky", "sky_lo", 7, size=0.13, load=1.0, load_falloff=0.0,
           opacity=0.95, note="sky")

# Two starved passes across it at an angle, so a graded field is not a stack of
# bands. Ends run off the canvas.
s.stroke([(-0.06, 0.052), (0.42, 0.112), (1.06, 0.082)], "bristle", "sky_lo",
         size=0.075, load=0.40, opacity=0.45, pressure="swell", note="sky haze")
s.stroke([(1.06, 0.218), (0.55, 0.178), (-0.06, 0.228)], "bristle", "sky",
         size=0.065, load=0.35, opacity=0.40, pressure="swell", note="sky haze")

# The facade: the anchoring dark. A brush small enough that its overhang does not
# eat the parapet, and ragged rather than clean -- edge="clean" on a comb left a
# pale stringy fringe along the whole roofline, which the engine warned it would.
# The roofline is simply where this mass's paint stops and the sky still shows.
s.block_in(facade(), "bristle", "facade", density=1.0, size=0.07,
           direction=(8, 96), note="facade")
# the roof stack: slim, vertical, and run well down into the mass so it belongs to
# the building rather than floating at the line
s.block_in(vent(), "flat", "facade_dk", density=1.0, solid=True, size=0.014,
           direction="axis", note="facade vent")
print(s.budget_line())
