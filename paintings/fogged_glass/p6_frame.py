# The frame: brick base, bottom rail, glazing bars, eave, and the lit sliver of
# roof glass above it. These carry the dark the picture has not got yet.
# Each member is ONE stroke -- laid as several it beads into a chain of blocks --
# and its width is solved off the projection, so it thins correctly with distance.
p["bar"]    = p.at_value(p.mix("burnt_umber", "ultramarine", 0.34), 0.31)
p["barlit"] = p.at_value(p.mix("burnt_umber", "ultramarine", 0.20), 0.58)
p["brick"]  = p.at_value(p.desaturate(p.mix(p.mix("burnt_sienna", "burnt_umber", 0.55),
                               "ultramarine", 0.26), 0.45), 0.29)
p["lip"]    = p.at_value(p.mix(p["neutral"], "cerulean", 0.06), 0.86)

# half the default wander (jitter 0.02 / size_jitter 0.06): a member is
# straighter than a brush is, and zero would be a ruled line
QUIET = dict(jitter=0.01, size_jitter=0.03, load=1.0, load_falloff=0.0)

def member(hm, d_far, d_near, width_m, n=14, xm=WALL):
    """Points along a horizontal member, with the pressure list that makes a round
    tip thin exactly as perspective thins it."""
    ds = [d_far * (d_near / d_far) ** (i / (n - 1.0)) for i in range(n)]
    w_near = F * width_m / d_near
    press = [min(1.0, (F * width_m / d) / w_near) for d in ds]
    press[0] = 0.0                      # the far end goes to nothing in the haze
    return [P(xm, hm, d) for d in ds], w_near, press

# --- the brick base, below the sill: a long wedge, so strokes, not a mass
pts, w, pr = member(0.30, 26.0, 2.60, 0.62)
s.stroke(pts, "round_hard", "brick", size=w, pressure=pr, opacity=0.95,
         **QUIET, note="frame")
pts, w, pr = member(0.55, 21.0, 2.42, 0.16)
s.stroke(pts, "round_hard", p.at_value(p["brick"], 0.20), size=w, pressure=pr,
         opacity=0.9, **QUIET, note="frame")     # the shadow the sill casts on it

# --- the bottom rail, and the light on its upper face
pts, w, pr = member(0.635, 21.0, 2.30, 0.10)
s.stroke(pts, "round_hard", "bar", size=w, pressure=pr, opacity=0.95,
         **QUIET, note="frame")
pts, w, pr = member(0.678, 21.0, 2.55, 0.045)
s.stroke(pts, "round_hard", "barlit", size=w, pressure=pr, opacity=0.8,
         **QUIET, note="frame")

# --- the glazing bars, far to near, thinning to nothing in the bright haze
for dm, op in zip(BAR_DM[::-1], [0.35, 0.50, 0.68, 0.82, 0.92, 0.97, 1.0, 1.0]):
    s.stroke([P(WALL, EAVE + 0.02, dm), P(WALL, -0.10, dm)], "round_hard", "bar",
             size=max(F * 0.045 / dm, 0.0040), pressure="even", opacity=op,
             **QUIET, note="frame")

# --- the eave, the heaviest line in the picture, and the roof glass above it
pts, w, pr = member(EAVE + 0.045, 26.0, 1.30, 0.115)
s.stroke(pts, "round_hard", "bar", size=w, pressure=pr, opacity=0.97,
         **QUIET, note="frame")
pts, w, pr = member(2.44, 21.0, 2.10, 0.085, xm=2.28)
s.stroke(pts, "round_hard", "lip", size=w, pressure=pr, opacity=0.9,
         **QUIET, note="frame")

# --- the horizontal laps where one pane overlaps the next. This is what says
# glazing rather than balustrade, and it crosses the comb the bars make.
for hm, wm, op, lit in [(1.03, 0.022, 0.62, 0.30), (1.54, 0.020, 0.55, 0.26),
                        (2.02, 0.018, 0.48, 0.22)]:
    pts, w, pr = member(hm, 18.0, 1.45, wm)
    s.stroke(pts, "round_hard", "bar", size=w, pressure=pr, opacity=op,
             **QUIET, note="frame")
    pts, w, pr = member(hm + 0.012, 18.0, 1.45, wm * 0.55)
    s.stroke(pts, "round_hard", "barlit", size=w, pressure=pr, opacity=lit,
             **QUIET, note="frame")
