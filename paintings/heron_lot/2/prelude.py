# Heron in a flooded lot, dawn - second attempt.
# A steep downward view: no horizon in the frame, so the picture has no
# horizontal bands to fight. Everything is the lot's own perspective.
import math
p = s.palette
A = s.aspect

p["far_dark"] = p.at_value(p.mix(p.mix("ultramarine","burnt_umber",0.5),"viridian",0.16), 0.200)
p["far_lt"]   = p.at_value(p.mix(p.mix("ultramarine","burnt_umber",0.5),"viridian",0.16), 0.285)
p["glow_hi"]  = p.at_value(p.mix(p.mix("yellow_ochre","cadmium_red",0.34),
                                 "titanium_white", 0.58), 0.790)
p["glow"]     = p.at_value(p.mix(p.mix("yellow_ochre","cadmium_red",0.34),
                                 "titanium_white", 0.55), 0.745)
p["w_mid"]    = p.at_value(p.mix(p.mix("cerulean","burnt_umber",0.40),
                                 "titanium_white", 0.34), 0.555)
p["w_near"]   = p.at_value(p.mix(p.mix("burnt_umber","ultramarine",0.42),
                                 "yellow_ochre", 0.20), 0.355)
p["w_deep"]   = p.at_value(p.mix(p.mix("burnt_umber","ultramarine",0.45),
                                 "yellow_ochre", 0.14), 0.290)
p["sheen"]    = p.at_value(p.mix(p.mix("cerulean","ultramarine",0.35),
                                 "burnt_umber", 0.30), 0.485)
p["grit"]     = p.at_value(p.mix("burnt_umber","ultramarine",0.34), 0.235)
p["lane_f"]   = p.at_value(p.mix(p.mix("titanium_white","burnt_umber",0.26),
                                 "ultramarine", 0.08), 0.625)
p["lane_n"]   = p.at_value(p.mix(p.mix("titanium_white","burnt_umber",0.26),
                                 "ultramarine", 0.08), 0.620)
p["lamp_w"]   = p.at_value(p.mix(p.mix("cerulean","burnt_umber",0.35),
                                 p.mix("cadmium_red","yellow_ochre",0.5), 0.42), 0.700)
p["lamp_c"]   = p.at_value(p.mix(p.mix("cerulean","burnt_umber",0.35),
                                 p.mix("cadmium_red","yellow_ochre",0.5), 0.55), 0.790)
p["h_lt"]     = p.at_value(p.mix(p.mix("titanium_white","ultramarine",0.10),
                                 "cadmium_red", 0.06), 0.865)
p["h_wh"]     = p.at_value(p.mix(p.mix("titanium_white","ultramarine",0.12),
                                 "cadmium_red", 0.07), 0.740)
p["h_md"]     = p.at_value(p.mix(p.mix("ultramarine","burnt_umber",0.45),
                                 "titanium_white", 0.40), 0.460)
p["h_dk"]     = p.at_value(p.mix("ultramarine","burnt_umber",0.40), 0.275)
p["h_bk"]     = p.at_value(p.mix("ultramarine","burnt_umber",0.44), 0.195)
p["beak"]     = p.at_value(p.mix(p.mix("yellow_ochre","burnt_umber",0.50),
                                 "ultramarine", 0.24), 0.300)
p["refl"]     = p.at_value(p.mix(p.mix("ultramarine","burnt_umber",0.45),
                                 "cerulean", 0.18), 0.320)

# --- the far edge: lumpy, and it DIPS where the bird's head will stand -------
FAR = union(
    polygon([(-0.06,-0.06),(1.06,-0.06),(1.06,0.086),(0.62,0.124),
             (0.34,0.166),(-0.06,0.118)]),
    blob((0.404, 0.152), 0.044, wobble=0.46, points=15, seed=7,  aspect=A),
    blob((0.272, 0.126), 0.034, wobble=0.48, points=13, seed=2,  aspect=A),
    blob((0.558, 0.120), 0.036, wobble=0.40, points=13, seed=11, aspect=A),
    blob((0.770, 0.100), 0.030, wobble=0.46, points=13, seed=5,  aspect=A),
    blob((0.958, 0.086), 0.028, wobble=0.42, points=13, seed=9,  aspect=A)).smooth(1)

WATER = polygon([(-0.06, 0.128), (0.34, 0.190), (0.62, 0.146), (1.06, 0.098),
                 (1.06, 1.06), (-0.06, 1.06)])

# --- the near dark: a wedge off two edges, deeper on the right --------------
NEAR = polygon([(-0.06, 0.855), (0.28, 0.812), (0.60, 0.748), (1.06, 0.638),
                (1.06, 1.06), (-0.06, 1.06)]).smooth(1)

# --- stall lines radiating from a vanishing point off the top left ----------
VP = (-0.55, -0.10)
def lane(x_bottom, t0=0.0, t1=1.0, n=3):
    """the stretch of the line through VP that crosses y=1.06 at x_bottom"""
    x2, y2 = x_bottom, 1.06
    return [(VP[0] + (x2 - VP[0]) * t, VP[1] + (y2 - VP[1]) * t)
            for t in [t0 + (t1 - t0) * i / (n - 1) for i in range(n)]]

# --- the bird: facing right, head down, about to strike ----------------------
# Drawn small and legible, then placed: the bird is 1.22x and moved in, because
# at its first size it was a smaller share of the canvas than painting 1's was.
def T(pts, k=1.22, ox=0.065, cx=0.32, cy=0.10):
    return [(cx + (x - cx) * k + ox, cy + (y - cy) * k) for x, y in pts]

HEAD  = polygon(T([(0.2740,0.1120),(0.2880,0.0975),(0.3080,0.0960),(0.3250,0.1080),
                   (0.3330,0.1420),(0.3180,0.1560),(0.2930,0.1520),(0.2745,0.1350)])).smooth(1)
# the crown covers the top and front only: the nape and the throat keep the
# dark, which is what stops a head reading as a ball
CROWN = polygon([(0.3452, 0.1245), (0.3506, 0.1032), (0.3684, 0.0962),
                 (0.3866, 0.1026), (0.3974, 0.1236), (0.3902, 0.1402),
                 (0.3700, 0.1392), (0.3522, 0.1348)]).smooth(1)
BILL  = T([(0.3300,0.1440),(0.3630,0.1930),(0.3955,0.2420)])
CREST = T([(0.3030,0.0965),(0.2790,0.0885),(0.2540,0.0870)])
NECK  = T([(0.3125,0.1430),(0.3290,0.2000),(0.3175,0.2560),(0.3410,0.3140)])
NECK_L= T([(0.3055,0.1445),(0.3215,0.2005),(0.3100,0.2565),(0.3330,0.3150)])
BODY  = polygon(T([(0.3520,0.3155),(0.3160,0.3255),(0.2760,0.3320),(0.2440,0.3430),
                   (0.2270,0.3560),(0.2480,0.3800),(0.2820,0.4060),(0.3220,0.4290),
                   (0.3620,0.4090),(0.3760,0.3700),(0.3700,0.3340)])).smooth(1)
WING  = polygon(T([(0.3400,0.3350),(0.3020,0.3430),(0.2660,0.3530),(0.2830,0.3830),
                   (0.3180,0.4030),(0.3520,0.3880),(0.3610,0.3600)])).smooth(1)
BACK  = T([(0.2330,0.3520),(0.2820,0.3300),(0.3350,0.3200),(0.3660,0.3290)])
BREAST= T([(0.3700,0.3400),(0.3745,0.3740),(0.3600,0.4060)])
LEG_F = T([(0.3320,0.4270),(0.3355,0.4520),(0.3380,0.4720)])
LEG_B = T([(0.2900,0.4110),(0.2850,0.4390),(0.2810,0.4640)])
WATERLINE = 0.554

def m_field():
    """The whole picture is one graded field, and the light is in it from the
    first pass. Brush left off: the verb takes it from its own step, which is
    the thing painting 1's hand-laid band did not do and ribboned for."""
    # two ramps, not one: warm at the top where it reflects the horizon, cool
    # in the middle where it reflects the sky overhead, warm-dark near where
    # you look through it to asphalt. One scumble makes the whole field warm.
    upper = polygon([(-0.06, 0.128), (0.34, 0.190), (0.62, 0.146), (1.06, 0.098),
                     (1.06, 0.585), (-0.06, 0.615)])
    lower = polygon([(-0.06, 0.500), (1.06, 0.470), (1.06, 1.06), (-0.06, 1.06)])
    s.scumble(upper, "glow", "w_mid", 7, direction=4)
    s.scumble(lower, "w_mid", "w_near", 8, direction=3)

def m_far():
    """The far dark. A comb at one direction - a chisel prints battlements on a
    lumpy silhouette, which is what painting 1 got and had to repaint."""
    s.block_in(FAR, "bristle", "far_dark", size=0.040, density=1.0, solid=True,
               direction=6, opacity=0.96)
    # single parallel comb passes rib a mass. CALIBRATION's repair: lay it with
    # the comb, then put the core back with solid strokes down the middle -
    # which leaves the top edge combed, where the ribbing is what you want.
    for x0, x1, y0, y1, sz in ((-0.08, 0.44, 0.042, 0.062, 0.055),
                               (0.30, 1.08, 0.036, 0.028, 0.048),
                               (0.10, 0.62, 0.092, 0.104, 0.034)):
        s.stroke([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 + 0.006), (x1, y1)],
                 "flat", "far_dark", size=sz, opacity=1.0, load=1.0,
                 load_falloff=0.0, pressure="even")
    # the far side of it is further away and hazier, not one flat black
    s.stroke([(-0.08, 0.012), (0.46, 0.004), (1.08, -0.006)], "bristle", "far_lt",
             size=0.030, load=0.45, load_falloff=0.8, opacity=0.45, pressure="swell")
    for pts, col, sz, ld in (
            ([(0.456,0.196),(0.470,0.156),(0.462,0.130)], "far_dark", 0.030, 0.75),
            ([(0.596,0.168),(0.612,0.124),(0.628,0.100)], "far_lt",   0.036, 0.55),
            ([(0.300,0.182),(0.286,0.146)],               "far_dark", 0.026, 0.85),
            ([(0.806,0.146),(0.822,0.108)],               "far_lt",   0.028, 0.50)):
        s.stroke(pts, "bristle", col, size=sz, load=ld, opacity=0.85,
                 pressure="lift_off")
    # light coming through the branches, worked in from the silhouette
    s.stroke([(0.540,0.124),(0.556,0.142)], "round_hard", "glow", size=0.009,
             load=0.30, opacity=0.6)
    s.stroke([(0.714,0.112),(0.730,0.128),(0.736,0.142)], "round_hard", "glow",
             size=0.007, load=0.25, opacity=0.5)

def m_near():
    """No wedge mass: the ramp simply carries on down, and the near character is
    passages laid on the lot's own diagonal. A swept mass here was a wall of mud."""
    s.scumble(polygon([(-0.06, 0.680), (1.06, 0.640), (1.06, 1.06), (-0.06, 1.06)]),
              "w_near", "w_deep", 6, direction=3)
    # thin water over dark asphalt, on the perspective, no two alike
    for pts, col, sz, ld, op, pr in (
            ([(0.92, 1.05), (0.52, 0.880), (0.20, 0.760)], "w_deep", 0.072, 0.8, 0.46, "swell"),
            ([(1.06, 0.900), (0.70, 0.780), (0.38, 0.700)], "w_deep", 0.050, 0.7, 0.34, "taper"),
            ([(0.46, 1.06), (0.14, 0.892), (-0.06, 0.820)], "w_deep", 0.056, 0.75, 0.40, "lift_off")):
        s.stroke(pts, "bristle", col, size=sz, load=ld, load_falloff=0.72,
                 opacity=op, pressure=pr)
    for pts, col, sz, ld, op in (
            ([(0.04, 0.900), (0.36, 0.862), (0.66, 0.822)], "grit", 0.040, 0.30, 0.50),
            ([(0.18, 0.980), (0.52, 0.940)], "grit", 0.034, 0.26, 0.44),
            ([(0.60, 0.912), (0.92, 0.862)], "grit", 0.030, 0.28, 0.40),
            ([(0.34, 1.030), (0.74, 0.995)], "grit", 0.046, 0.22, 0.46)):
        s.stroke(pts, "bristle", col, size=sz, load=ld, load_falloff=0.90,
                 opacity=op, pressure="swell")

def _lift(box, d):
    """a colour that is what is already there, d of value above it"""
    f = s.sample(box)
    return p.at_value(p.mix(f, "titanium_white", min(0.5, abs(d) * 3)),
                      p.value_of(f) + d)

def m_lanes():
    """Stall lines under the flood: invisible at the top where the reflection
    owns the surface, emerging as the view steepens. Each is mixed off the water
    it lies under - opacity cannot quieten a stroke, only its colour can."""
    p["ln_far"] = _lift((0.30, 0.560, 0.70, 0.620), 0.075)
    p["ln_mid"] = _lift((0.20, 0.720, 0.70, 0.790), 0.130)
    p["ln_nr"]  = _lift((0.10, 0.900, 0.70, 0.990), 0.215)
    for xb, t0, t1, col, sz, ld in (
            (0.46, 0.54, 1.05, "ln_mid", 0.019, 0.85),
            (0.02, 0.60, 1.05, "ln_mid", 0.017, 0.75),
            (0.92, 0.58, 1.05, "ln_mid", 0.016, 0.70),
            (1.34, 0.64, 1.05, "ln_far", 0.014, 0.60)):
        s.stroke(lane(xb, t0, t1, 5), "flat", col, size=sz, opacity=0.9, load=ld,
                 load_falloff=0.45, pressure=[0.0, 0.35, 0.7, 0.95, 1.0], note="lane")
    # the near ends, where you look straight down and the paint is simply there
    for xb, t0, t1, sz in ((0.46, 0.88, 1.06, 0.026), (0.02, 0.94, 1.06, 0.028),
                           (0.92, 0.92, 1.06, 0.023)):
        s.stroke(lane(xb, t0, t1, 3), "flat", "ln_nr", size=sz, opacity=0.9,
                 load=0.95, load_falloff=0.2, pressure=[0.5, 0.9, 1.0], note="lane")
    # one bay-end line across them, and the water moving over another
    s.stroke([(-0.05, 0.905), (0.34, 0.845), (0.70, 0.800)], "flat", "ln_far",
             size=0.013, opacity=0.8, load=0.6, load_falloff=0.6,
             pressure=[0.0, 0.9, 0.15], note="lane")
    s.stroke(lane(0.46, 0.78, 0.90, 3), "bristle", "ln_far", size=0.022,
             load=0.35, load_falloff=0.85, opacity=0.5, pressure="swell", note="lane")

def m_lamp():
    """A sodium lamp out of frame, drawn toward the viewer as a broken path.
    Mixed close to the water in hue AND value: a glint is the field one step up,
    not a different colour laid on it."""
    warm = p.mix("cadmium_red", "yellow_ochre", 0.5)
    def hot(box, d):
        f = s.sample(box)
        return p.at_value(p.mix(f, warm, 0.30), p.value_of(f) + d)
    p["lp1"] = hot((0.72, 0.190, 0.83, 0.300), 0.055)
    p["lp2"] = hot((0.72, 0.360, 0.83, 0.470), 0.095)
    p["lp3"] = hot((0.72, 0.540, 0.83, 0.660), 0.130)
    for x, y, w, sz, col, ld, op, br in (
            (0.766, 0.214, 0.022, 0.026, "lp1", 0.35, 0.40, "bristle"),
            (0.774, 0.272, 0.034, 0.008, "lp1", 0.8,  0.50, "round_hard"),
            (0.760, 0.322, 0.018, 0.028, "lp2", 0.40, 0.45, "bristle"),
            (0.780, 0.388, 0.044, 0.007, "lp2", 0.9,  0.55, "round_hard"),
            (0.766, 0.446, 0.026, 0.030, "lp2", 0.45, 0.50, "bristle"),
            (0.786, 0.512, 0.052, 0.009, "lp3", 0.85, 0.60, "round_hard"),
            (0.770, 0.570, 0.032, 0.032, "lp3", 0.40, 0.48, "bristle"),
            (0.792, 0.638, 0.058, 0.008, "lp3", 0.8,  0.50, "round_hard"),
            (0.776, 0.700, 0.036, 0.028, "lp3", 0.30, 0.36, "bristle")):
        s.stroke([(x - w, y + 0.005), (x + w * 0.25, y - 0.002), (x + w * 0.8, y + 0.002)],
                 br, col, size=sz, opacity=op, load=ld, load_falloff=0.6,
                 pressure="swell")

def m_bird_dark():
    """The bird, dark first: the light is a shape laid ON this. edge="clean" from
    the start - a chisel staircases a sloping silhouette and painting 1 spent two
    rehearsals finding that out."""
    s.dry()
    s.block_in(BODY, "flat", "h_dk", size=0.018, density=1.0, solid=True,
               direction="axis", opacity=1.0, pressure="even", edge="clean",
               note="subject")
    # a neck is a stroke, not a mass
    s.stroke(NECK, "flat", "h_dk", size=0.030, opacity=1.0, load=1.0,
             load_falloff=0.0, jitter=0.006, size_jitter=0.04, pressure="even",
             note="subject")
    s.stroke(NECK[1:], "flat", "h_dk", size=0.023, opacity=1.0, load=1.0,
             load_falloff=0.0, jitter=0.006, size_jitter=0.04, pressure="even",
             note="subject")
    # round_hard, not flat: measured, a chisel under about 4px lands the ground
    # and never reaches its mixture at any size. A round tip holds its colour.
    s.block_in(HEAD, "round_hard", "h_dk", size=0.011, density=1.0, solid=True,
               direction="axis", opacity=1.0, pressure="even", edge="clean",
               note="subject")
    # the bill: a dagger, and a stroke - as a mass it is thinner than the brush
    # and blooms pale, which is what painting 1 got
    s.stroke(BILL, "round_hard", "beak", size=0.0145, opacity=1.0, load=1.0,
             load_falloff=0.0, pressure=[1.0, 0.55, 0.04], note="subject")
    s.stroke([BILL[0], ((BILL[0][0]+BILL[1][0])/2 + 0.004,
                        (BILL[0][1]+BILL[1][1])/2 + 0.003)], "round_hard", "h_bk",
             size=0.0050, opacity=0.65, load=1.0, load_falloff=0.15,
             pressure=[0.9, 0.1], note="subject")
    # two crest plumes trailing back off the crown
    s.stroke(CREST, "liner", "h_bk", size=0.0042, opacity=1.0, load=1.0,
             load_falloff=0.0, pressure=[1.0, 0.45, 0.0], note="subject")
    s.stroke([(CREST[0][0]+0.006, CREST[0][1]+0.011), (CREST[1][0]+0.006, CREST[1][1]+0.016),
              (CREST[2][0]+0.016, CREST[2][1]+0.018)], "liner", "h_bk", size=0.0030,
             opacity=0.85, load=1.0, load_falloff=0.0, pressure=[0.8, 0.35, 0.0],
             note="subject")

def m_bird_light():
    """At this scale a plane is a stroke: a chisel stepping across a cell-sized
    shape shows every step, which is what painting 1's shoulder slabs were."""
    g = lambda t: p.mix("h_dk", "h_md", t)
    # the grey back and the folded wing
    # inset, so the dark the body was laid in rims it and the form turns
    s.block_in(WING.inset(0.012), "flat", "h_md", size=0.016, density=1.0,
               solid=True, direction="axis", opacity=0.95, pressure="even",
               note="subject")
    s.stroke(BACK, "flat", "h_md", size=0.015, opacity=1.0, load=1.0,
             load_falloff=0.0, pressure="even", note="subject")
    s.stroke([(0.2900, 0.4010), (0.3480, 0.3880), (0.4090, 0.3810)], "flat",
             g(0.45), size=0.0095, opacity=0.5, load=1.0, load_falloff=0.0,
             pressure="even", note="subject")
    # feather groups over the shoulder - marks, never one slab
    for pts, col, sz, op, ld, fo in (
            ([(0.3080, 0.4080), (0.3560, 0.3990), (0.3980, 0.3940)], g(0.85), 0.0120, 0.95, 1.0, 0.15),
            ([(0.3240, 0.4390), (0.3700, 0.4290)], g(0.25), 0.0105, 0.85, 0.9, 0.35),
            ([(0.2960, 0.4260), (0.3300, 0.4170)], "h_bk", 0.0095, 0.7, 0.8, 0.45)):
        s.stroke(pts, "flat", col, size=sz, opacity=op, load=ld,
                 load_falloff=fo, pressure="even", note="subject")
    # the belly and the shoulder keep the dark, so the body turns under
    s.stroke([(0.2900, 0.4480), (0.3500, 0.4740), (0.4120, 0.4720)], "flat",
             "h_dk", size=0.0200, opacity=0.9, load=1.0, load_falloff=0.35,
             pressure="even", note="subject")
    s.stroke([(0.3060, 0.4030), (0.3420, 0.3960)], "flat", "h_bk", size=0.0130,
             opacity=0.75, load=0.9, load_falloff=0.45, pressure="even",
             note="subject")
    s.stroke([(0.2820, 0.4340), (0.3160, 0.4440)], "bristle", "h_dk",
             size=0.0150, load=0.55, load_falloff=0.7, opacity=0.6,
             pressure="taper", note="subject")
    s.stroke([(0.3160, 0.4240), (0.3640, 0.4160), (0.4020, 0.4120)], "bristle",
             g(0.70), size=0.0150, load=0.30, load_falloff=0.88, opacity=0.35,
             pressure="swell", note="subject")
    # break the inner plane's boundary, or it reads as an oval laid on an oval
    for pts, col, sz, ld, op, pr in (
            ([(0.3260, 0.4020), (0.3480, 0.4180)], g(0.35), 0.0120, 0.45, 0.45, "taper"),
            ([(0.3880, 0.4260), (0.4060, 0.4420)], g(0.90), 0.0100, 0.40, 0.40, "swell"),
            ([(0.3400, 0.4560), (0.3720, 0.4480)], g(0.55), 0.0130, 0.35, 0.38, "lift_off")):
        s.stroke(pts, "bristle", col, size=sz, load=ld, load_falloff=0.85,
                 opacity=op, pressure=pr, note="subject")
    # a tail point at the back, which a rounded blob does not have
    s.stroke([(0.2900, 0.4180), (0.2680, 0.4150), (0.2560, 0.4180)], "flat",
             g(0.40), size=0.0115, opacity=0.9, load=1.0, load_falloff=0.25,
             pressure="even", note="subject")
    # the lit rim at the front of the breast, ON the silhouette not inboard
    s.stroke([(0.4440, 0.3900), (0.4510, 0.4260)], "flat", "h_wh", size=0.0105,
             opacity=0.95, load=1.0, load_falloff=0.15, pressure="even", note="subject")
    s.stroke([(0.4480, 0.4390), (0.4340, 0.4720)], "flat", p.mix("h_wh","h_md",0.35),
             size=0.0090, opacity=0.8, load=0.9, load_falloff=0.4, pressure="even",
             note="subject")
    s.stroke([(0.4330, 0.3920), (0.4400, 0.4310), (0.4260, 0.4680)], "flat",
             p.mix("h_wh", "h_dk", 0.55), size=0.0085, opacity=0.5, load=1.0,
             load_falloff=0.0, pressure="even", note="subject")
    # the neck in three values: white, mid, and the dark it was laid in
    s.stroke(NECK_L, "flat", "h_lt", size=0.0105, opacity=1.0, load=1.0,
             load_falloff=0.0, jitter=0.004, size_jitter=0.03, pressure="even",
             note="subject")
    s.stroke([(x + 0.0075, y) for x, y in NECK_L], "flat",
             p.mix("h_lt", "h_dk", 0.42), size=0.0080, opacity=0.7, load=1.0,
             load_falloff=0.0, pressure="even", note="subject")
    s.smudge([(x + 0.004, y) for x, y in NECK_L])
    # the head: the white, the black stripe, the eye. Three marks and stop.
    s.block_in(CROWN, "round_hard", "h_lt", size=0.0095, density=1.0, solid=True,
               direction="axis", opacity=1.0, pressure="even", edge="clean",
               note="subject")
    s.stroke([(0.3455, 0.1145), (0.3690, 0.1055), (0.3900, 0.1095)], "liner",
             "h_bk", size=0.0042, opacity=1.0, load=1.0, load_falloff=0.0,
             pressure=[0.4, 1.0, 0.85], note="subject")
    s.dab(0.3820, 0.1275, "round_hard", "h_bk", size=0.0052, press=3,
          tip_wobble=0.4, note="subject")
    # the legs, and one difference between them
    s.stroke(LEG_F, "liner", "h_bk", size=0.0060, opacity=1.0, load=1.0,
             load_falloff=0.0, pressure=[1.0, 0.85, 0.7], note="subject")
    s.stroke(LEG_B, "liner", p.mix("h_bk", "w_mid", 0.45), size=0.0050,
             opacity=0.7, load=0.85, load_falloff=0.35,
             pressure=[0.9, 0.55, 0.3], note="subject")

def m_reflection():
    """A white bird in dark water reflects PALE, not dark - the plan had this
    wrong and the pairs check caught it. Broken across, never a mirror."""
    def lift(y0, y1, d):
        f = s.sample((0.26, y0, 0.46, y1))
        return p.at_value(p.mix(f, "h_wh", min(0.55, d * 3.2)), p.value_of(f) + d)
    p["rf1"] = lift(0.565, 0.625, 0.150)
    p["rf2"] = lift(0.640, 0.710, 0.175)
    p["rf3"] = lift(0.725, 0.800, 0.150)
    p["rf4"] = lift(0.810, 0.870, 0.085)
    p["rd"]  = p.at_value(p.mix(s.sample((0.26, 0.58, 0.46, 0.66)), "h_dk", 0.55),
                          p.value_of(s.sample((0.26, 0.58, 0.46, 0.66))) - 0.095)
    # the dark of the body, only where the water is still light enough to hold it
    for x0, x1, y, sz, op, ld in ((0.326, 0.428, 0.566, 0.018, 0.78, 0.9),
                                  (0.312, 0.436, 0.596, 0.016, 0.60, 0.75),
                                  (0.330, 0.418, 0.630, 0.013, 0.42, 0.6)):
        s.stroke([(x0, y + 0.004), (x1, y - 0.003)], "bristle", "rd", size=sz,
                 load=ld, load_falloff=0.72, opacity=op, pressure="swell",
                 note="subject")
    # the white of it, broken wider and further apart as it comes toward you
    for x0, x1, y, sz, col, op, ld in (
            (0.345, 0.407, 0.578, 0.0090, "rf1", 0.82, 0.9),
            (0.334, 0.416, 0.610, 0.0105, "rf1", 0.66, 0.85),
            (0.352, 0.404, 0.642, 0.0080, "rf2", 0.52, 0.7),
            (0.324, 0.428, 0.678, 0.0125, "rf2", 0.72, 0.85),
            (0.340, 0.398, 0.714, 0.0085, "rf2", 0.46, 0.65),
            (0.312, 0.438, 0.756, 0.0140, "rf3", 0.60, 0.8),
            (0.348, 0.410, 0.794, 0.0095, "rf3", 0.38, 0.6),
            (0.306, 0.444, 0.834, 0.0150, "rf4", 0.32, 0.55)):
        s.stroke([(x0, y + 0.005), (x0 * 0.4 + x1 * 0.6, y - 0.004), (x1, y + 0.002)],
                 "round_hard", col, size=sz, opacity=op, load=ld,
                 load_falloff=0.35, pressure=[0.25, 1.0, 0.3], note="subject")

def m_waterline():
    """Where the bird meets the surface: the one place its edge is interrupted."""
    s.dab(0.4066, 0.5556, "round_hard", "h_bk", size=0.0080, press=3,
          tip_wobble=0.6, note="subject")
    s.dab(0.3372, 0.5462, "round_hard", p.mix("h_bk", "w_mid", 0.4), size=0.0062,
          press=3, tip_wobble=0.6, note="subject")
    glint = p.at_value(s.sample((0.28, 0.53, 0.48, 0.58)),
                       p.value_of(s.sample((0.28, 0.53, 0.48, 0.58))) + 0.17)
    s.stroke([(0.352, 0.5620), (0.408, 0.5680), (0.468, 0.5600)], "round_hard",
             glint, size=0.0085, opacity=0.75, load=0.85, load_falloff=0.4,
             pressure=[0.15, 1.0, 0.25], note="subject")
    s.stroke([(0.276, 0.5530), (0.336, 0.5580), (0.392, 0.5520)], "round_hard",
             glint, size=0.0065, opacity=0.5, load=0.7, load_falloff=0.5,
             pressure=[0.2, 0.9, 0.15], note="subject")
    s.stroke([(0.248, 0.5860), (0.340, 0.5950), (0.452, 0.5870)], "round_hard",
             glint, size=0.0055, opacity=0.36, load=0.6, load_falloff=0.55,
             pressure=[0.1, 0.8, 0.12], note="subject")
    # the legs again, stronger, now they have water to stand in
    s.stroke(LEG_F, "liner", "h_bk", size=0.0068, opacity=1.0, load=1.0,
             load_falloff=0.0, pressure=[1.0, 0.9, 0.75], note="subject")

def m_nearfield():
    """The sheet-flood: cool sky lying ON the water, warm asphalt showing
    THROUGH it, in the same passage - and laid on the lot's own diagonal."""
    f1 = s.sample((0.05, 0.700, 0.45, 0.800))
    f2 = s.sample((0.45, 0.880, 0.95, 0.990))
    cool = p.mix("cerulean", "ultramarine", 0.35)
    p["sh1"] = p.at_value(p.mix(f1, cool, 0.30), p.value_of(f1) + 0.105)
    p["sh2"] = p.at_value(p.mix(f2, cool, 0.24), p.value_of(f2) + 0.085)
    p["dp"]  = p.at_value(p.mix(f2, p.mix("burnt_umber","ultramarine",0.30), 0.45),
                          p.value_of(f2) - 0.070)
    s.dry()
    # two smooth patches that mirror the sky: a chisel, not a comb
    s.stroke([(0.96, 1.05), (0.52, 0.855), (0.06, 0.735)], "flat", "sh1",
             size=0.090, opacity=0.34, load=1.0, load_falloff=0.35,
             pressure=[0.85, 1.0, 0.25])
    s.stroke([(1.06, 0.930), (0.66, 0.812), (0.28, 0.742)], "flat", "sh2",
             size=0.052, opacity=0.26, load=1.0, load_falloff=0.45,
             pressure=[0.15, 1.0, 0.5])
    s.stroke([(0.60, 1.05), (0.24, 0.892), (-0.06, 0.800)], "bristle", "sh1",
             size=0.042, load=0.5, load_falloff=0.8, opacity=0.32, pressure="swell")
    for pts, sz, ld, op, pr in (
            ([(0.84, 1.05), (0.50, 0.928), (0.24, 0.856)], 0.046, 0.6, 0.40, "swell"),
            ([(1.05, 1.02), (0.78, 0.940)], 0.036, 0.5, 0.32, "taper"),
            ([(0.38, 1.06), (0.10, 0.930)], 0.034, 0.55, 0.34, "lift_off")):
        s.stroke(pts, "bristle", "dp", size=sz, load=ld, load_falloff=0.78,
                 opacity=op, pressure=pr)
    # the lines again, over the sheen, where you look straight down at them
    for xb, t0, t1, sz, op in ((0.46, 0.80, 1.06, 0.024, 0.85),
                               (0.02, 0.86, 1.06, 0.026, 0.80),
                               (0.92, 0.84, 1.06, 0.021, 0.75),
                               (1.34, 0.90, 1.06, 0.018, 0.6)):
        s.stroke(lane(xb, t0, t1, 4), "flat", "ln_nr", size=sz, opacity=op,
                 load=0.95, load_falloff=0.3, pressure=[0.3, 0.7, 0.95, 1.0],
                 note="lane")
    for pts, sz, ld, op in (([(0.06, 0.905), (0.38, 0.868), (0.68, 0.828)], 0.038, 0.28, 0.48),
                            ([(0.24, 0.995), (0.58, 0.952)], 0.032, 0.24, 0.42),
                            ([(0.66, 0.918), (0.96, 0.870)], 0.028, 0.26, 0.38)):
        s.stroke(pts, "bristle", "grit", size=sz, load=ld, load_falloff=0.92,
                 opacity=op, pressure="swell")

def m_lamp2():
    """The lamp's path had gone too quiet - painting 1's mistake, made twice.
    It is the only warm note below the glow and the right side is empty without it."""
    warm = p.mix("cadmium_red", "yellow_ochre", 0.5)
    def hot(box, d):
        f = s.sample(box)
        return p.at_value(p.mix(f, warm, 0.40), p.value_of(f) + d)
    p["h1"] = hot((0.72, 0.300, 0.84, 0.400), 0.055)
    p["h2"] = hot((0.72, 0.470, 0.84, 0.570), 0.080)
    p["h3"] = hot((0.72, 0.640, 0.84, 0.740), 0.075)
    # length and a bend, not a lozenge: a round tip prints one silhouette
    for x, y, w, sz, col, ld, op, br in (
            (0.766, 0.316, 0.030, 0.022, "h1", 0.35, 0.45, "bristle"),
            (0.780, 0.376, 0.052, 0.026, "h1", 0.30, 0.40, "bristle"),
            (0.762, 0.444, 0.034, 0.009, "h2", 0.8,  0.55, "round_hard"),
            (0.788, 0.508, 0.062, 0.028, "h2", 0.38, 0.48, "bristle"),
            (0.768, 0.566, 0.040, 0.026, "h2", 0.32, 0.44, "bristle"),
            (0.794, 0.634, 0.070, 0.030, "h3", 0.35, 0.46, "bristle"),
            (0.774, 0.698, 0.044, 0.010, "h3", 0.75, 0.48, "round_hard"),
            (0.802, 0.768, 0.076, 0.028, "h3", 0.28, 0.36, "bristle"),
            (0.782, 0.834, 0.048, 0.026, "h3", 0.24, 0.30, "bristle")):
        s.stroke([(x - w, y + 0.006), (x - w * 0.1, y - 0.004),
                  (x + w * 0.5, y + 0.001), (x + w * 0.95, y + 0.005)],
                 br, col, size=sz, opacity=op, load=ld, load_falloff=0.70,
                 pressure="swell")

def m_finish_bird():
    """The head measured 0.75 against a planned 0.865 - the oriented tips never
    reach their mixture, so the fix is to mix lighter than the target, not to
    lay the same colour again."""
    s.stroke([(0.3520, 0.1120), (0.3700, 0.1055), (0.3880, 0.1130)], "round_hard",
             "titanium_white", size=0.0145, opacity=1.0, load=1.0,
             load_falloff=0.0, pressure=[0.7, 1.0, 0.6], note="subject")
    s.stroke([(0.3560, 0.1300), (0.3760, 0.1330)], "round_hard",
             p.at_value("titanium_white", 0.905), size=0.0105, opacity=0.9,
             load=1.0, load_falloff=0.1, pressure=[0.9, 0.5], note="subject")
    # the light falls off down the neck: an even bright stripe reads as tape
    s.stroke(NECK_L[:2], "flat", p.at_value("titanium_white", 0.900),
             size=0.0090, opacity=1.0, load=1.0, load_falloff=0.0, jitter=0.004,
             pressure="even", note="subject")
    s.stroke(NECK_L[1:], "flat", p.mix("h_lt", "h_md", 0.38), size=0.0085,
             opacity=0.75, load=1.0, load_falloff=0.0, jitter=0.005,
             pressure="even", note="subject")
    s.stroke([(x + 0.0025, y) for x, y in NECK_L[1:]], "bristle",
             p.mix("h_lt", "h_dk", 0.5), size=0.0105, load=0.35,
             load_falloff=0.85, opacity=0.45, pressure="swell", note="subject")
    s.smudge([(x + 0.002, y) for x, y in NECK_L])
    # the eye and its catchlight, and the bill's under-edge
    s.dab(0.3818, 0.1268, "round_hard", "h_bk", size=0.0050, press=3,
          tip_wobble=0.4, note="subject")
    s.dab(0.3800, 0.1246, "round_hard", "titanium_white", size=0.0019, press=3,
          note="subject")
    s.stroke([(0.3980, 0.1600), (0.4360, 0.2150), (0.4700, 0.2660)], "liner",
             "h_bk", size=0.0042, opacity=0.65, load=1.0, load_falloff=0.25,
             pressure=[0.9, 0.5, 0.05], note="subject")
    # the body: feather groups at varied angles, and a tail that ends in a point
    g = lambda t: p.mix("h_dk", "h_md", t)
    for pts, col, sz, op, ld, fo in (
            ([(0.3120, 0.4150), (0.3560, 0.4060), (0.3940, 0.4030)], g(0.95), 0.0105, 0.85, 1.0, 0.2),
            ([(0.3300, 0.4460), (0.3740, 0.4380)], g(0.20), 0.0095, 0.8, 0.9, 0.4),
            ([(0.3480, 0.3980), (0.3900, 0.3940)], g(0.65), 0.0080, 0.7, 0.85, 0.35),
            ([(0.2860, 0.4300), (0.3140, 0.4230)], "h_bk", 0.0085, 0.65, 0.8, 0.5)):
        s.stroke(pts, "flat", col, size=sz, opacity=op, load=ld, load_falloff=fo,
                 pressure="even", note="subject")
    s.stroke([(0.2820, 0.4200), (0.2620, 0.4165), (0.2470, 0.4200)], "round_hard",
             g(0.30), size=0.0130, opacity=0.9, load=1.0, load_falloff=0.2,
             pressure=[1.0, 0.6, 0.08], note="subject")
    s.stroke([(0.3060, 0.4600), (0.3540, 0.4780), (0.4020, 0.4740)], "bristle",
             "h_dk", size=0.0135, load=0.45, load_falloff=0.8, opacity=0.5,
             pressure="swell", note="subject")
    # one edge lost: the bird's back into the light water behind it
    behind = s.sample((0.300, 0.375, 0.400, 0.400))
    p["lose"] = p.at_value(p.mix(behind, "h_md", 0.55),
                           (p.value_of(behind) + p.value_of(p["h_md"])) / 2)
    s.stroke([(0.2980, 0.3960), (0.3480, 0.3870), (0.3980, 0.3830)], "bristle",
             "lose", size=0.0130, load=0.40, load_falloff=0.85, opacity=0.45,
             pressure="swell", note="subject")

def m_finish_water():
    """The far band was flat and the upper right blank. What is actually there
    is the trees coming down into the water they stand at the edge of."""
    # haze along the top of the far mass, and crowns breaking its lower edge
    s.stroke([(-0.08, 0.022), (0.44, 0.012), (1.08, 0.000)], "bristle", "far_lt",
             size=0.040, load=0.75, load_falloff=0.55, opacity=0.75, pressure="swell")
    s.stroke([(0.24, 0.046), (0.70, 0.034), (1.08, 0.026)], "bristle",
             p.mix("far_lt", "far_dark", 0.45), size=0.028, load=0.55,
             load_falloff=0.7, opacity=0.55, pressure="taper")
    for pts, col, sz, ld, op in (
            ([(0.148, 0.104), (0.160, 0.138)], "far_dark", 0.026, 0.8, 0.85),
            ([(0.648, 0.108), (0.664, 0.142), (0.658, 0.160)], "far_dark", 0.030, 0.7, 0.8),
            ([(0.878, 0.092), (0.890, 0.126)], "far_lt", 0.024, 0.5, 0.6),
            ([(0.492, 0.118), (0.506, 0.152)], "far_dark", 0.022, 0.75, 0.8)):
        s.stroke(pts, "bristle", col, size=sz, load=ld, load_falloff=0.7,
                 opacity=op, pressure="lift_off")
    # two gaps worked in from the silhouette, never a dot in the interior
    s.stroke([(0.226, 0.118), (0.244, 0.100)], "round_hard", "glow", size=0.010,
             load=0.30, opacity=0.55)
    s.stroke([(0.712, 0.106), (0.728, 0.090), (0.736, 0.076)], "round_hard",
             "glow", size=0.008, load=0.25, opacity=0.45)
    # the trees reflected into the bright water, soft and broken
    def dim(box, d):
        f = s.sample(box)
        return p.at_value(p.mix(f, "far_dark", 0.35), p.value_of(f) - d)
    p["tr1"] = dim((0.50, 0.170, 0.95, 0.230), 0.170)
    p["tr2"] = dim((0.50, 0.240, 0.95, 0.300), 0.125)
    for x0, x1, y, col, sz, ld, op, pr in (
            (0.560, 0.880, 0.184, "tr1", 0.034, 0.9, 0.80, "swell"),
            (0.640, 0.960, 0.216, "tr1", 0.026, 0.75, 0.62, "taper"),
            (0.520, 0.764, 0.246, "tr2", 0.020, 0.6, 0.48, "lift_off"),
            (0.828, 1.060, 0.266, "tr2", 0.018, 0.55, 0.40, "swell"),
            (0.086, 0.292, 0.190, "tr1", 0.028, 0.85, 0.68, "taper"),
            (0.036, 0.200, 0.228, "tr2", 0.019, 0.6, 0.44, "swell")):
        s.stroke([(x0, y + 0.005), (x0 * 0.5 + x1 * 0.5, y - 0.004), (x1, y + 0.002)],
                 "bristle", col, size=sz, load=ld, load_falloff=0.75,
                 opacity=op, pressure=pr)
    # drift on the open water, mixed off the field: a glint is the field one step up
    for box, d, x0, x1, y, sz, ld, op in (
            ((0.60, 0.300, 0.90, 0.340), 0.085, 0.600, 0.880, 0.322, 0.028, 0.45, 0.55),
            ((0.45, 0.380, 0.75, 0.420), 0.080, 0.470, 0.720, 0.402, 0.026, 0.40, 0.48),
            ((0.80, 0.420, 1.05, 0.460), 0.075, 0.840, 1.060, 0.442, 0.030, 0.42, 0.46),
            ((0.08, 0.330, 0.30, 0.370), 0.078, 0.070, 0.290, 0.352, 0.026, 0.40, 0.50),
            ((0.50, 0.500, 0.78, 0.540), 0.048, 0.520, 0.760, 0.522, 0.020, 0.28, 0.30),
            ((0.10, 0.470, 0.34, 0.510), 0.045, 0.110, 0.330, 0.494, 0.022, 0.26, 0.30)):
        f = s.sample(box)
        c = p.at_value(f, p.value_of(f) + d)
        s.stroke([(x0, y + 0.004), (x1, y - 0.003)], "bristle", c, size=sz,
                 load=ld, load_falloff=0.88, opacity=op, pressure="swell")
    # and two ripple lines the bird has set going, crossing its own reflection
    g = p.at_value(s.sample((0.20, 0.600, 0.56, 0.650)),
                   p.value_of(s.sample((0.20, 0.600, 0.56, 0.650))) + 0.115)
    s.stroke([(0.196, 0.624), (0.372, 0.646), (0.556, 0.620)], "round_hard", g,
             size=0.0060, opacity=0.42, load=0.65, load_falloff=0.5,
             pressure=[0.1, 0.9, 0.12])
    s.stroke([(0.150, 0.690), (0.376, 0.716), (0.606, 0.684)], "round_hard", g,
             size=0.0070, opacity=0.32, load=0.6, load_falloff=0.55,
             pressure=[0.08, 0.8, 0.1])

def m_last():
    """The deadest passage is the lower left, and the thing that says which kind
    of place this is has not been painted yet."""
    def off(box, d, toward=None):
        f = s.sample(box)
        c = f if toward is None else p.mix(f, toward, min(0.5, abs(d) * 3))
        return p.at_value(c, p.value_of(f) + d)
    cool = p.mix("cerulean", "ultramarine", 0.35)
    # sheen sweeping into the dead corner on the lot's own diagonal
    s.stroke([(0.42, 1.06), (0.14, 0.902), (-0.06, 0.820)], "flat",
             off((0.02, 0.85, 0.36, 0.98), 0.095, cool), size=0.072,
             opacity=0.32, load=1.0, load_falloff=0.4, pressure=[0.9, 1.0, 0.3])
    s.stroke([(0.20, 1.05), (0.02, 0.948)], "bristle",
             off((0.00, 0.93, 0.24, 1.04), 0.080, cool), size=0.040, load=0.5,
             load_falloff=0.8, opacity=0.34, pressure="swell")
    for pts, d, sz, ld, op in (
            ([(-0.05, 0.938), (0.22, 0.902), (0.44, 0.872)], -0.065, 0.042, 0.6, 0.42),
            ([(0.06, 1.030), (0.34, 0.996)], -0.055, 0.036, 0.5, 0.36),
            ([(0.12, 0.860), (0.38, 0.828)], 0.055, 0.026, 0.28, 0.34)):
        s.stroke(pts, "bristle", off((0.05, 0.88, 0.40, 0.98), d), size=sz,
                 load=ld, load_falloff=0.86, opacity=op, pressure="swell")
    # a storm drain, half under the sheet. It is ground furniture, not a second
    # subject: small, low in contrast, and lying in the corner.
    dk = off((0.62, 0.90, 0.78, 0.98), -0.105)
    s.stroke([(0.620, 0.944), (0.762, 0.918)], "flat", dk, size=0.030,
             opacity=0.85, load=1.0, load_falloff=0.3, pressure="even")
    for i, (x0, x1, y) in enumerate(((0.634, 0.744, 0.9330), (0.638, 0.748, 0.9420),
                                     (0.642, 0.752, 0.9515), (0.646, 0.740, 0.9605))):
        s.stroke([(x0, y), (x1, y - 0.002)], "liner",
                 off((0.62, 0.90, 0.78, 0.98), -0.17), size=0.0045,
                 opacity=0.75 - i * 0.08, load=0.9, load_falloff=0.35,
                 pressure=[0.8, 0.3])
    s.stroke([(0.616, 0.9260), (0.768, 0.9010)], "round_hard",
             off((0.62, 0.88, 0.78, 0.94), 0.115), size=0.0055, opacity=0.6,
             load=0.8, load_falloff=0.45, pressure=[0.2, 1.0, 0.2])
    # incident on the quiet left water
    for box, d, x0, x1, y, sz, ld, op in (
            ((0.02, 0.400, 0.24, 0.440), 0.070, 0.010, 0.230, 0.424, 0.026, 0.32, 0.42),
            ((0.04, 0.540, 0.26, 0.580), 0.060, 0.030, 0.250, 0.564, 0.022, 0.28, 0.36),
            ((0.10, 0.640, 0.32, 0.680), -0.055, 0.090, 0.300, 0.664, 0.028, 0.45, 0.34),
            ((0.02, 0.290, 0.22, 0.330), 0.055, 0.015, 0.215, 0.312, 0.020, 0.26, 0.32)):
        f = s.sample(box)
        s.stroke([(x0, y + 0.004), (x1, y - 0.003)], "bristle",
                 p.at_value(f, p.value_of(f) + d), size=sz, load=ld,
                 load_falloff=0.88, opacity=op, pressure="swell")
    # soften the two hardest stall lines, and lose one edge of the reflection
    s.stroke(lane(0.02, 0.90, 0.99, 3), "bristle",
             off((0.02, 0.92, 0.20, 1.04), 0.075), size=0.026, load=0.35,
             load_falloff=0.85, opacity=0.40, pressure="swell", note="lane")
    s.smudge([(0.296, 0.742), (0.372, 0.756), (0.446, 0.744)])
    # the last marks: two accents, and they are on the bird
    s.dab(0.3796, 0.1242, "round_hard", "titanium_white", size=0.0020, press=3,
          note="subject")
    s.stroke([(0.3960, 0.1520), (0.4120, 0.1750)], "round_hard",
             p.at_value("titanium_white", 0.88), size=0.0045, opacity=0.8,
             load=1.0, load_falloff=0.2, pressure=[0.9, 0.1], note="subject")

def m_last2():
    """The last of it: the body wants structure, the drain wants the water over
    it, and the middle distance is the quietest thing left."""
    def off(box, d):
        f = s.sample(box)
        return p.at_value(f, p.value_of(f) + d)
    # water running over the drain, so it is under the sheet and not on it
    s.stroke([(0.598, 0.9360), (0.700, 0.9200), (0.788, 0.9080)], "bristle",
             off((0.60, 0.90, 0.79, 0.96), 0.075), size=0.020, load=0.35,
             load_falloff=0.85, opacity=0.42, pressure="swell")
    s.stroke([(0.642, 0.9640), (0.744, 0.9470)], "bristle",
             off((0.62, 0.94, 0.78, 0.99), -0.045), size=0.016, load=0.4,
             load_falloff=0.88, opacity=0.34, pressure="taper")
    # the body: closely spaced greys at different angles, and the wing's edge
    g = lambda t: p.mix("h_dk", "h_md", t)
    for pts, col, sz, op, ld, fo in (
            ([(0.3020, 0.4230), (0.3380, 0.4120), (0.3700, 0.4080)], g(0.55), 0.0090, 0.7, 0.85, 0.4),
            ([(0.3540, 0.4300), (0.3920, 0.4230)], g(1.0), 0.0075, 0.65, 0.8, 0.45),
            ([(0.2960, 0.4460), (0.3260, 0.4560)], g(0.15), 0.0085, 0.6, 0.75, 0.5),
            ([(0.3700, 0.4520), (0.4020, 0.4600)], g(0.35), 0.0070, 0.55, 0.7, 0.5)):
        s.stroke(pts, "flat", col, size=sz, opacity=op, load=ld,
                 load_falloff=fo, pressure="even", note="subject")
    s.stroke([(0.2880, 0.4090), (0.3300, 0.3990), (0.3760, 0.3950)], "bristle",
             g(0.85), size=0.0125, load=0.30, load_falloff=0.88, opacity=0.35,
             pressure="swell", note="subject")
    # the wing's lower edge, found once
    s.stroke([(0.3180, 0.4560), (0.3620, 0.4620), (0.3980, 0.4520)], "round_hard",
             g(0.05), size=0.0055, opacity=0.55, load=0.85, load_falloff=0.4,
             pressure=[0.15, 0.9, 0.15], note="subject")
    # the middle distance: ripple bands mixed off the field, no two alike
    for box, d, x0, x1, y, sz, ld, op, pr in (
            ((0.46, 0.360, 0.72, 0.400), 0.075, 0.470, 0.716, 0.384, 0.024, 0.35, 0.45, "swell"),
            ((0.50, 0.450, 0.76, 0.490), -0.060, 0.516, 0.748, 0.472, 0.030, 0.5, 0.36, "taper"),
            ((0.46, 0.520, 0.70, 0.560), 0.065, 0.472, 0.690, 0.544, 0.020, 0.30, 0.38, "lift_off"),
            ((0.54, 0.600, 0.80, 0.640), 0.070, 0.556, 0.792, 0.622, 0.026, 0.32, 0.40, "swell"),
            ((0.86, 0.520, 1.05, 0.560), 0.060, 0.868, 1.060, 0.542, 0.022, 0.28, 0.34, "taper")):
        f = s.sample(box)
        s.stroke([(x0, y + 0.005), ((x0 + x1) / 2, y - 0.004), (x1, y + 0.002)],
                 "bristle", p.at_value(f, p.value_of(f) + d), size=sz, load=ld,
                 load_falloff=0.88, opacity=op, pressure=pr)
    # and the far edge broken in two more places on the right
    s.stroke([(0.918, 0.098), (0.932, 0.132)], "bristle", "far_dark", size=0.026,
             load=0.75, load_falloff=0.7, opacity=0.8, pressure="lift_off")
    s.stroke([(0.556, 0.112), (0.572, 0.084)], "round_hard", "glow", size=0.008,
             load=0.28, opacity=0.5)

def m_close():
    """Soften the one hard thing left on the bird, and stop."""
    g = lambda t: p.mix("h_dk", "h_md", t)
    s.stroke([(0.4490, 0.3960), (0.4540, 0.4260), (0.4420, 0.4600)], "bristle",
             p.mix("h_wh", "h_md", 0.40), size=0.0125, load=0.35,
             load_falloff=0.85, opacity=0.45, pressure="swell", note="subject")
    s.stroke([(0.4380, 0.4120), (0.4480, 0.4400)], "bristle", "h_wh",
             size=0.0090, load=0.30, load_falloff=0.88, opacity=0.40,
             pressure="taper", note="subject")
    s.stroke([(0.4320, 0.3880), (0.4460, 0.3930)], "round_hard",
             p.mix("h_wh", "h_lt", 0.5), size=0.0048, opacity=0.7, load=0.9,
             load_falloff=0.35, pressure=[0.2, 0.9, 0.15], note="subject")
    s.stroke([(0.3260, 0.4320), (0.3700, 0.4250), (0.4060, 0.4300)], "bristle",
             g(0.45), size=0.0105, load=0.30, load_falloff=0.88, opacity=0.34,
             pressure="swell", note="subject")
    # one glint on the surface beside the bird, where the dawn catches a ripple
    f = s.sample((0.44, 0.560, 0.60, 0.600))
    s.stroke([(0.452, 0.5760), (0.520, 0.5840), (0.584, 0.5760)], "round_hard",
             p.at_value(f, p.value_of(f) + 0.185), size=0.0065, opacity=0.7,
             load=0.8, load_falloff=0.45, pressure=[0.12, 1.0, 0.18])
