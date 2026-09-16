# The runnels: tracks where water has gathered and run down the inside of the pane,
# clearing the film, so the green comes through. This is the subject. They stay
# between the glazing bars, because the condensation is inside and the bars are not,
# and they start and stop at the pane laps, because that is where the water does.
p["runnel"]   = p.at_value(p.desaturate(p.mix(p.mix("viridian", "yellow_ochre", 0.34),
                                 "burnt_umber", 0.16), 0.38), 0.32)
p["runnelup"] = p.at_value(p.desaturate(p.mix(p["neutral"], "viridian", 0.16), 0.34), 0.34)
p["bead"]     = p.at_value(p.mix(p["neutral"], "titanium_white", 0.55), 0.76)

def lap_y(x, hm):
    dm = F * WALL / (x - VX)
    return VY - (hm - E) * F * s.aspect / dm

def track(x, hm_top, hm_bot, wob, n=7):
    """A runnel down one pane, wandering the way water does."""
    y0, y1 = lap_y(x, hm_top), lap_y(x, hm_bot)
    return [(x + wob[i % len(wob)], y0 + (y1 - y0) * i / (n - 1.0)) for i in range(n)]

W1 = (0.0, 0.004, -0.003, 0.005, -0.002, 0.003, -0.004)
W2 = (0.0, -0.005, 0.003, -0.002, 0.004, -0.003, 0.002)

# --- the near pane: the big ones, full weight
for x, ht, hb, wob, sz, col, pr in [
        (0.899, 2.01, 1.48, W1, 0.012, "runnelup", [0.15, 0.9, 0.4, 1.0, 0.7, 0.5, 0.0]),
        (0.905, 1.46, 0.52, W2, 0.013, "runnel",   [0.0, 0.8, 1.0, 0.45, 0.9, 0.6, 0.0]),
        (0.976, 2.02, 0.74, W2, 0.009, "runnelup", [0.4, 1.0, 0.3, 0.8, 0.6, 0.2, 0.0]),
        (0.845, 1.03, 0.46, W1, 0.008, "runnel",   [0.0, 0.7, 1.0, 0.4, 0.8, 0.3, 0.0])]:
    s.stroke(track(x, ht, hb, wob), "round_hard", col, size=sz, pressure=pr,
             load=0.62, load_falloff=0.45, opacity=0.80, jitter=0.014,
             tip_wobble=0.35, note="subject")

# --- the second pane: smaller, and one of them barely there
for x, ht, hb, wob, sz, col, pr in [
        (0.760, 2.00, 0.70, W2, 0.010, "runnel",   [0.2, 0.9, 1.0, 0.6, 0.8, 0.4, 0.0]),
        (0.722, 1.52, 0.72, W1, 0.007, "runnelup", [0.0, 0.8, 0.5, 0.9, 0.4, 0.0, 0.0]),
        (0.692, 2.01, 1.05, W1, 0.006, "runnel",   [0.0, 0.6, 1.0, 0.4, 0.7, 0.2, 0.0])]:
    s.stroke(track(x, ht, hb, wob), "round_hard", col, size=sz, pressure=pr,
             load=0.55, load_falloff=0.45, opacity=0.70, jitter=0.012,
             tip_wobble=0.35, note="subject")

# --- the third, nearly lost in the haze
for x, ht, hb, sz in [(0.628, 1.98, 1.06, 0.005), (0.601, 1.50, 0.95, 0.004)]:
    s.stroke(track(x, ht, hb, W2, n=5), "round_hard", "runnelup", size=sz,
             pressure=[0.0, 0.8, 0.5, 0.3, 0.0], load=0.7, load_falloff=0.35,
             opacity=0.55, jitter=0.008, tip_wobble=0.35, note="subject")
