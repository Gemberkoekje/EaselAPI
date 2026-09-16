# --- heron in a flooded lot, dawn -------------------------------------------
# Every mass is a named function so a repair can re-run the stack in depth order.
import math

p = s.palette
A = s.aspect

def _mix(*a):  # readability only
    return p.mix(*a)

# --- the mixtures, all planned to a value and swatched before the first mass --
p["sky_hi"]   = p.at_value(p.mix("cerulean", "ultramarine", 0.45), 0.50)
p["sky_lo"]   = p.at_value(p.mix(p.mix("yellow_ochre", "cadmium_red", 0.40),
                                 "cerulean", 0.22), 0.67)
# the dawn band itself: the picture's light. Without it the greyscale has a
# dark and a mid and nothing else.
_warm = p.mix(p.mix("yellow_ochre", "cadmium_red", 0.32), "titanium_white", 0.50)
_warm2 = p.mix(_warm, "titanium_white", 0.35)
p["dawn1"]    = p.at_value(p.mix(_warm2, "cerulean", 0.16), 0.672)
p["dawn2"]    = p.at_value(p.mix(_warm2, "cerulean", 0.10), 0.712)
p["dawn3"]    = p.at_value(_warm2, 0.742)
p["dawn_w"]   = p.at_value(p.mix(_warm2, "cerulean", 0.34), 0.655)
p["trees"]    = p.at_value(p.mix(p.mix("ultramarine", "burnt_umber", 0.50),
                                 "viridian", 0.18), 0.20)
p["trees_lt"] = p.at_value(p.mix(p.mix("ultramarine", "burnt_umber", 0.50),
                                 "viridian", 0.18), 0.27)
p["scrub"]    = p.at_value(p.mix(p.mix("ultramarine", "burnt_umber", 0.52),
                                 "cerulean", 0.30), 0.52)
p["water_far"]= p.at_value(p.mix(p.mix("cerulean", "titanium_white", 0.55),
                                 "cadmium_red", 0.10), 0.60)
p["water_mid"]= p.at_value(p.mix(p.mix("cerulean", "burnt_umber", 0.35),
                                 "titanium_white", 0.30), 0.50)
p["water_nr"] = p.at_value(p.mix(p.mix("burnt_umber", "ultramarine", 0.40),
                                 "yellow_ochre", 0.22), 0.42)
p["refl_tree"]= p.at_value(p.mix(p.mix("ultramarine", "burnt_umber", 0.48),
                                 "cerulean", 0.20), 0.34)
p["tarmac"]   = p.at_value(p.desaturate(p.mix("burnt_umber", "ultramarine", 0.45), 0.35), 0.345)
p["tarmac_d"] = p.at_value(p.desaturate(p.mix("burnt_umber", "ultramarine", 0.45), 0.30), 0.27)
p["wet_asph"] = p.at_value(p.mix(p.mix("burnt_umber", "ultramarine", 0.42),
                                 "yellow_ochre", 0.16), 0.32)
p["grit"]     = p.at_value(p.mix("burnt_umber", "ultramarine", 0.30), 0.22)
p["lane"]     = p.at_value(p.mix(p.mix("titanium_white", "burnt_umber", 0.22),
                                 "ultramarine", 0.07), 0.68)
p["lane_wet"] = p.at_value(p.mix(p.mix("burnt_umber", "ultramarine", 0.40),
                                 "titanium_white", 0.52), 0.56)
p["lane_dim"] = p.at_value(p.mix(p.mix("burnt_umber", "ultramarine", 0.40),
                                 "titanium_white", 0.52), 0.49)
p["lamp"]     = p.at_value(p.mix(p.mix("cadmium_red", "yellow_ochre", 0.58),
                                 "titanium_white", 0.55), 0.80)
# the light on the water is mixed close to the water, in hue as well as value:
# mixed to its own colour it is a searchlight that owns the picture
p["lamp_wtr"] = p.at_value(p.mix(p.mix("cerulean", "burnt_umber", 0.35),
                                 p.mix("cadmium_red", "yellow_ochre", 0.5), 0.34), 0.63)
p["lamp_w2"]  = p.at_value(p.mix(p.mix("cerulean", "burnt_umber", 0.35),
                                 p.mix("cadmium_red", "yellow_ochre", 0.5), 0.46), 0.71)
p["pole"]     = p.at_value(p.mix("ultramarine", "burnt_umber", 0.42), 0.26)
p["heron_lt"] = p.at_value(p.mix(p.mix("titanium_white", "ultramarine", 0.10),
                                 "cadmium_red", 0.06), 0.80)
p["heron_md"] = p.at_value(p.mix(p.mix("ultramarine", "burnt_umber", 0.45),
                                 "titanium_white", 0.40), 0.46)
p["heron_wh"] = p.at_value(p.mix(p.mix("titanium_white", "ultramarine", 0.12),
                                 "cadmium_red", 0.07), 0.71)
p["heron_bk"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.44), 0.215)
p["heron_dk"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.38), 0.30)
# the bill runs off the trees into the sky, so it has to be dark to read there
p["beak"]     = p.at_value(p.mix(p.mix("yellow_ochre", "burnt_umber", 0.55),
                                 "ultramarine", 0.26), 0.285)
p["beak_lit"] = p.at_value(p.mix(p.mix("yellow_ochre", "burnt_umber", 0.35),
                                 "titanium_white", 0.30), 0.62)

# --- the drawing -------------------------------------------------------------
# the far edge of the lot: tilted, and it is never a ruled line
WATER_TOP = [(-0.06, 0.412), (0.18, 0.408), (0.40, 0.402), (0.62, 0.398),
             (0.84, 0.392), (1.06, 0.386)]

# the far edge: a pale atmospheric wedge on the left, a lumpy dark clump right
# the far side of the lot in dawn haze - two pieces, and the middle simply lost
SCRUB_A = polygon([(-0.06, 0.378), (0.05, 0.374), (0.13, 0.379), (0.19, 0.372),
                   (0.19, 0.402), (0.05, 0.406), (-0.06, 0.408)])
SCRUB_B = polygon([(0.27, 0.370), (0.36, 0.362), (0.45, 0.366), (0.54, 0.357),
                   (0.62, 0.359), (0.62, 0.400), (0.45, 0.403), (0.27, 0.401)])

CLUMP = union(
    polygon([(0.50, 0.372), (1.06, 0.356), (1.06, 0.398), (0.50, 0.404)]),
    blob((0.556, 0.368), 0.030, wobble=0.42, points=13, seed=11, aspect=A),
    blob((0.636, 0.348), 0.040, wobble=0.40, points=13, seed=4,  aspect=A),
    blob((0.742, 0.330), 0.048, wobble=0.38, points=15, seed=9,  aspect=A),
    blob((0.864, 0.318), 0.054, wobble=0.44, points=15, seed=2,  aspect=A),
    blob((0.986, 0.336), 0.042, wobble=0.36, points=13, seed=6,  aspect=A))

FOLIAGE = [348, 24, 4, 336, 62, 352, 16, 330, 8, 44, 356, 20, 340, 0, 30, 350]

WATER = polygon([(-0.06, 0.428), (0.30, 0.424), (0.62, 0.420), (1.06, 0.412),
                 (1.06, 1.06), (-0.06, 1.06)])

# the near water: you look through it onto asphalt. A wedge, not a band.
NEARWATER = polygon([(-0.06, 0.728), (0.28, 0.778), (0.58, 0.842), (0.86, 0.918),
                     (1.06, 0.972), (1.06, 1.06), (-0.06, 1.06)])

# the flood's edge: dry asphalt comes in from the bottom-right corner as a wedge
# where the sheet gives out: the crown of the lot's camber coming dry. The
# edge wanders - nothing about a flood is ruled.
TARMAC = polygon([(-0.06, 0.762), (0.022, 0.784), (0.056, 0.771), (0.094, 0.802),
                  (0.126, 0.824), (0.152, 0.810), (0.186, 0.846), (0.216, 0.880),
                  (0.246, 0.866), (0.270, 0.902), (0.296, 0.940), (0.312, 0.976),
                  (0.332, 1.022), (0.338, 1.06), (-0.06, 1.06)]).smooth(1)
ISLAND = blob((0.452, 0.972), 0.050, wobble=0.55, points=15, seed=8, aspect=A)

# stall lines converging on a vanishing point off the left, at the far edge
VP = (-0.17, 0.400)
def _lane(x0, y0, t_far, t_near=0.0):
    dx, dy = VP[0] - x0, VP[1] - y0
    return [(x0 + dx * t, y0 + dy * t)
            for t in (t_near, t_near + (t_far - t_near) * 0.45, t_far)]
LANE1 = _lane(0.56, 1.03, 0.74)
LANE2 = _lane(0.99, 1.03, 0.62)
LANE3 = _lane(0.22, 1.03, 0.52)
LANE4 = _lane(-0.04, 1.03, 0.40)

# the light: a pole in the lot, its lamp losing to the dawn
POLE_TOP, POLE_FOOT = (0.206, -0.03), (0.228, 0.588)
LAMP = (0.264, 0.126)

# --- the heron ---------------------------------------------------------------
# Lit from the upper left: the dawn is low and the lamp is over that shoulder.
# The pale neck stands against the dark trees; the dark body against lit water.
HERON_BODY = polygon([(0.5760, 0.5220), (0.5880, 0.4960), (0.6140, 0.4855),
                      (0.6500, 0.4845), (0.6860, 0.4925), (0.7180, 0.5050),
                      (0.7365, 0.5135), (0.7150, 0.5265), (0.6880, 0.5410),
                      (0.6560, 0.5620), (0.6180, 0.5745), (0.5930, 0.5700),
                      (0.5755, 0.5510)])
BACK_LIT  = polygon([(0.5920, 0.5015), (0.6200, 0.4885), (0.6560, 0.4875),
                     (0.6920, 0.4950), (0.7240, 0.5075), (0.7000, 0.5140),
                     (0.6600, 0.5015), (0.6200, 0.5020), (0.5985, 0.5125)])
BREAST    = polygon([(0.5768, 0.5235), (0.5900, 0.4990), (0.6065, 0.4945),
                     (0.6050, 0.5290), (0.5985, 0.5570), (0.5900, 0.5690),
                     (0.5778, 0.5520)])
WING      = polygon([(0.6070, 0.5120), (0.6470, 0.5030), (0.6900, 0.5120),
                     (0.7090, 0.5255), (0.6830, 0.5400), (0.6480, 0.5510),
                     (0.6190, 0.5410)])
NECK      = ribbon([(0.6060, 0.4980), (0.5920, 0.4560), (0.6000, 0.4130),
                    (0.5870, 0.3720), (0.5650, 0.3440)], 0.030, end_width=0.022)
NECK_LIT  = ribbon([(0.5985, 0.4985), (0.5845, 0.4565), (0.5925, 0.4135),
                    (0.5795, 0.3725), (0.5590, 0.3455)], 0.014, end_width=0.010)
HEAD      = polygon([(0.5400, 0.3382), (0.5482, 0.3268), (0.5622, 0.3228),
                     (0.5782, 0.3250), (0.5892, 0.3346), (0.5862, 0.3470),
                     (0.5702, 0.3534), (0.5522, 0.3514), (0.5405, 0.3450)])
CROWN     = polygon([(0.5435, 0.3370), (0.5500, 0.3282), (0.5628, 0.3244),
                     (0.5772, 0.3266), (0.5852, 0.3352), (0.5700, 0.3372),
                     (0.5540, 0.3400), (0.5425, 0.3418)])
BEAK      = polygon([(0.5452, 0.3332), (0.4700, 0.3548), (0.4692, 0.3622),
                     (0.5440, 0.3492)])
CREST     = [(0.5808, 0.3300), (0.5960, 0.3352), (0.6110, 0.3448)]
LEG_F = [(0.6120, 0.5700), (0.6075, 0.6120), (0.6020, 0.6600)]
LEG_B = [(0.6580, 0.5600), (0.6650, 0.6000), (0.6720, 0.6460)]

# --- masses, in depth order ---------------------------------------------------
def m_sky():
    s.scumble(span("A1", "H4"), "sky_hi", "sky_lo", 11, direction=356)

def m_trees():
    s.block_in(CLUMP, "bristle", "trees", size=0.036, density=1.0, solid=True,
               direction=8, opacity=0.95)
    # three crowns breaking the top contour, no two alike
    s.stroke([(0.712, 0.322), (0.726, 0.286), (0.738, 0.266)], "bristle",
             "trees", size=0.030, load=0.7, opacity=0.85, pressure="lift_off")
    s.stroke([(0.836, 0.310), (0.846, 0.272), (0.838, 0.248)], "bristle",
             "trees_lt", size=0.036, load=0.55, opacity=0.7, pressure="lift_off")
    s.stroke([(0.906, 0.316), (0.930, 0.282)], "bristle", "trees",
             size=0.026, load=0.85, opacity=0.9, pressure="taper")
    # sky coming in through the branches: slivers in from the silhouette
    s.stroke([(0.780, 0.300), (0.794, 0.316)], "round_hard", "sky_lo",
             size=0.009, load=0.30, opacity=0.6)
    s.stroke([(0.888, 0.290), (0.902, 0.304), (0.908, 0.318)], "round_hard",
             "sky_lo", size=0.007, load=0.25, opacity=0.5)

def m_water():
    s.scumble(WATER, "water_far", "water_nr", 12, direction=356)

def m_nearwater():
    s.scumble(NEARWATER, "water_nr", "wet_asph", 7, direction=10)

def _seg(line, a, b):
    """the stretch of a stall line between two fractions of its length"""
    (x0, y0), (x2, y2) = line[0], line[-1]
    return [(x0 + (x2 - x0) * t, y0 + (y2 - y0) * t)
            for t in (a, a + (b - a) * 0.5, b)]

def m_lanes():
    # stall lines through the flood: broken by grit and ripple, never one rule
    for line, a, b, col, sz, op, ld in (
            (LANE2, 0.00, 0.34, "lane_wet", 0.026, 0.60, 0.9),
            (LANE2, 0.42, 0.70, "lane_wet", 0.021, 0.48, 0.7),
            (LANE2, 0.79, 1.00, "lane_dim", 0.015, 0.34, 0.5),
            (LANE1, 0.04, 0.41, "lane_wet", 0.021, 0.50, 0.8),
            (LANE1, 0.55, 0.88, "lane_dim", 0.015, 0.33, 0.55),
            (LANE3, 0.10, 0.62, "lane_dim", 0.017, 0.36, 0.6),
            (LANE4, 0.22, 0.86, "lane_dim", 0.013, 0.26, 0.45)):
        s.stroke(_seg(line, a, b), "flat", col, size=sz, opacity=op, load=ld,
                 load_falloff=0.55, pressure=[0.95, 0.7, 0.15], note="lane")
    # one of them wavers where the water moves over it
    s.stroke(_seg(LANE2, 0.34, 0.44), "bristle", "lane_dim", size=0.020,
             load=0.4, opacity=0.4, pressure="swell", note="lane")

def m_grit():
    for pts, col, sz, ld, op in (
            ([(0.05, 0.905), (0.34, 0.935), (0.62, 0.975)], "grit", 0.040, 0.30, 0.55),
            ([(0.12, 0.845), (0.40, 0.880)], "wet_asph", 0.032, 0.25, 0.5),
            ([(0.02, 0.975), (0.30, 1.005)], "grit", 0.048, 0.22, 0.6),
            ([(0.46, 0.902), (0.68, 0.945)], "grit", 0.028, 0.28, 0.45),
            ([(0.20, 0.790), (0.44, 0.812)], "wet_asph", 0.024, 0.20, 0.4)):
        s.stroke(pts, "bristle", col, size=sz, load=ld, load_falloff=0.9,
                 opacity=op, pressure="swell")

def m_nearfield():
    """The near water, looked at more steeply: reflection on top of grit."""
    # thin sheet over dark asphalt - broad soft patches, no two alike
    for pts, col, sz, ld, op, pr in (
            ([(-0.05, 0.845), (0.11, 0.902), (0.255, 0.972)], "wet_asph", 0.072, 0.75, 0.50, "swell"),
            ([(0.06, 1.015), (0.24, 1.045)], "tarmac_d", 0.060, 0.70, 0.42, "taper"),
            ([(0.33, 0.958), (0.50, 1.002), (0.66, 1.030)], "wet_asph", 0.055, 0.60, 0.38, "lift_off"),
            ([(0.60, 0.890), (0.78, 0.938)], "tarmac_d", 0.044, 0.55, 0.30, "swell"),
            ([(0.84, 0.965), (1.02, 1.005)], "wet_asph", 0.050, 0.50, 0.34, "press_in")):
        s.stroke(pts, "bristle", col, size=sz, load=ld, load_falloff=0.7,
                 opacity=op, pressure=pr)
    # and the dawn still lying on the surface over the top of them
    s.dry()
    s.glaze([(-0.05, 0.805), (0.30, 0.862), (0.68, 0.918), (1.05, 0.968)],
            "lane_dim", opacity=0.10, size=0.085, pressure=[0.3, 0.9, 0.7, 0.25])

def m_grit2():
    for pts, col, sz, ld, op in (
            ([(0.04, 0.912), (0.30, 0.948), (0.55, 0.988)], "grit", 0.038, 0.30, 0.50),
            ([(0.14, 0.852), (0.40, 0.886)], "wet_asph", 0.030, 0.26, 0.42),
            ([(0.46, 0.905), (0.70, 0.952)], "grit", 0.027, 0.28, 0.40),
            ([(0.72, 1.012), (0.96, 1.038)], "grit", 0.044, 0.22, 0.48)):
        s.stroke(pts, "bristle", col, size=sz, load=ld, load_falloff=0.92,
                 opacity=op, pressure="swell")

def m_near_lane():
    # the one stall line you are looking straight down at: found, and the only
    # crisp line in the water. Its far end goes to nothing.
    s.stroke([(0.196, 1.045), (0.118, 0.978), (0.052, 0.918), (0.004, 0.874)],
             "flat", "lane", size=0.017, opacity=0.85, load=1.0, load_falloff=0.18,
             jitter=0.012, size_jitter=0.05, pressure=[1.0, 0.9, 0.5, 0.05], note="lane")
    s.stroke([(0.168, 1.020), (0.104, 0.966)], "bristle", "lane", size=0.014,
             load=0.35, opacity=0.5, pressure="swell", note="lane")

def m_lose_wedge():
    # the near-water scumble left a step along its top edge on the left
    s.smudge([(-0.04, 0.733), (0.10, 0.749), (0.24, 0.772), (0.38, 0.800)])
    s.stroke([(0.02, 0.718), (0.14, 0.745), (0.27, 0.768)], "bristle", "water_nr",
             size=0.034, load=0.45, opacity=0.35, pressure="swell")

GLOW = blob(LAMP, 0.080, wobble=0.35, points=15, seed=5, aspect=A)
POOL = blob((0.234, 0.624), 0.050, wobble=0.50, points=15, seed=12, aspect=A)

def m_pole():
    # a thin member wants the ruled setting, or it beads into a chain of blocks
    ruled = dict(opacity=0.95, load=1.0, load_falloff=0.0, jitter=0.0,
                 size_jitter=0.0, pressure="even")
    s.stroke([POLE_TOP, (0.216, 0.30), POLE_FOOT], "flat", "pole", size=0.0072, **ruled)
    s.stroke([(0.2285, 0.462), (0.2305, 0.594)], "flat", "pole", size=0.0102, **ruled)
    s.stroke([(0.2055, 0.1075), (0.234, 0.1135), (0.258, 0.1225)], "flat", "pole",
             size=0.0062, **ruled)
    s.stroke([(0.2495, 0.1275), (0.2775, 0.1305)], "flat", "pole", size=0.013,
             opacity=1.0, load=1.0, load_falloff=0.0, jitter=0.0,
             size_jitter=0.0, pressure="even")

def m_glow():
    # a halo is light IN the air: glazes crossing at the source, mixed a step
    # above the sky and toward its own colour. An inward scumble draws a moon.
    field = s.sample(GLOW)
    v = p.value_of(field)
    p["air_wide"] = p.at_value(p.mix(field, "lamp", 0.34), v + 0.045)
    p["air_core"] = p.at_value(p.mix(field, "lamp", 0.55), v + 0.10)
    s.dry()
    for ang, sz, op, col in ((6, 0.105, 0.075, "air_wide"),
                             (64, 0.098, 0.070, "air_wide"),
                             (124, 0.092, 0.065, "air_wide"),
                             (38, 0.048, 0.11, "air_core"),
                             (100, 0.044, 0.10, "air_core")):
        r = 0.058 if col == "air_wide" else 0.030
        dx = r * math.cos(math.radians(ang))
        dy = r * A * math.sin(math.radians(ang))
        s.glaze([(LAMP[0] - dx, LAMP[1] - dy), LAMP, (LAMP[0] + dx, LAMP[1] + dy)],
                col, opacity=op, size=sz, pressure=[0.25, 1.0, 0.25])
    # and one small hot point on the dark luminaire: the lamp itself
    s.dab(0.2655, 0.1295, "round_hard", "lamp", size=0.0080, press=3, tip_wobble=0.6)

def m_lamp_water():
    # light on shallow water draws toward the viewer as a broken path
    p["pool_edge"] = s.sample(POOL)
    p["pool_core"] = p.at_value(p.mix(s.sample(POOL), "lamp_wtr", 0.6),
                                p.value_of(s.sample(POOL)) + 0.09)
    s.scumble(POOL, "pool_edge", "pool_core", 7, direction="inward")
    for x, y, w, sz, col, op in (
            (0.230, 0.610, 0.014, 0.0090, "lamp_w2",  0.80),
            (0.234, 0.645, 0.023, 0.0070, "lamp_wtr", 0.60),
            (0.226, 0.674, 0.010, 0.0105, "lamp_w2",  0.66),
            (0.239, 0.712, 0.031, 0.0060, "lamp_wtr", 0.44),
            (0.231, 0.750, 0.018, 0.0090, "lamp_wtr", 0.48),
            (0.245, 0.800, 0.040, 0.0055, "lamp_wtr", 0.30),
            (0.236, 0.849, 0.025, 0.0075, "lamp_wtr", 0.26)):
        s.stroke([(x - w, y + 0.003), (x + w * 0.7, y - 0.002)], "round_hard",
                 col, size=sz, opacity=op, load=1.0, load_falloff=0.15,
                 pressure=[0.35, 1.0, 0.2])
    # the pole's own dark, broken into the same water
    for x, y, w, sz, op in ((0.2295, 0.630, 0.011, 0.0085, 0.55),
                            (0.2345, 0.692, 0.017, 0.0065, 0.42),
                            (0.2285, 0.774, 0.008, 0.0095, 0.32)):
        s.stroke([(x - w, y), (x + w * 0.6, y - 0.0015)], "round_hard", "pole",
                 size=sz, opacity=op, load=1.0, load_falloff=0.25,
                 pressure=[0.9, 0.25])

def m_tree_refl():
    """The trees in the water - weighted right, and gone where the bird stands."""
    for pts, col, sz, ld, op, pr in (
            ([(0.735, 0.436), (0.860, 0.442), (0.990, 0.434)], "refl_tree", 0.034, 0.85, 0.72, "swell"),
            ([(0.800, 0.468), (0.930, 0.462), (1.045, 0.470)], "refl_tree", 0.026, 0.70, 0.55, "taper"),
            ([(0.880, 0.494), (1.010, 0.488)], "refl_tree", 0.020, 0.55, 0.40, "lift_off"),
            ([(0.700, 0.458), (0.775, 0.452)], "refl_tree", 0.022, 0.45, 0.38, "swell"),
            ([(0.500, 0.436), (0.556, 0.441)], "refl_tree", 0.018, 0.35, 0.30, "taper"),
            ([(0.938, 0.520), (1.030, 0.528)], "refl_tree", 0.016, 0.40, 0.26, "swell")):
        s.stroke(pts, "bristle", col, size=sz, load=ld, load_falloff=0.7,
                 opacity=op, pressure=pr)
    # the surface breaking it up again
    s.stroke([(0.820, 0.452), (0.905, 0.448)], "round_hard", "water_far",
             size=0.0085, load=0.5, opacity=0.45, pressure="swell")
    s.stroke([(0.952, 0.478), (1.020, 0.474)], "round_hard", "water_far",
             size=0.007, load=0.4, opacity=0.35, pressure="taper")

def m_surface():
    """Incident on the open water. Glints mixed from the water itself - a glint
    is the field one step up, not a different colour laid on it."""
    hi = s.sample(span("C5", "F5"))
    lo = s.sample(span("B7", "E7"))
    p["glint_hi"] = p.at_value(hi, p.value_of(hi) + 0.085)
    p["glint_lo"] = p.at_value(lo, p.value_of(lo) + 0.075)
    p["ripple"]   = p.at_value(lo, p.value_of(lo) - 0.075)
    for pts, col, sz, ld, op, pr in (
            ([(0.058, 0.527), (0.180, 0.5195)], "glint_hi", 0.028, 0.40, 0.50, "swell"),
            ([(0.348, 0.5695), (0.472, 0.5745)], "glint_hi", 0.026, 0.32, 0.42, "taper"),
            ([(0.762, 0.6055), (0.902, 0.6115)], "glint_lo", 0.030, 0.35, 0.38, "lift_off"),
            ([(0.084, 0.6475), (0.218, 0.6555)], "glint_lo", 0.027, 0.30, 0.34, "swell"),
            ([(0.468, 0.6935), (0.642, 0.7025)], "glint_lo", 0.032, 0.28, 0.30, "taper"),
            ([(0.300, 0.4855), (0.396, 0.4805)], "glint_hi", 0.026, 0.25, 0.32, "swell")):
        s.stroke(pts, "bristle", col, size=sz, load=ld, load_falloff=0.88,
                 opacity=op, pressure=pr)
    for pts, sz, op in (([(0.556, 0.6375), (0.702, 0.6485)], 0.018, 0.32),
                        ([(0.126, 0.7095), (0.302, 0.7235)], 0.022, 0.28),
                        ([(0.796, 0.6875), (0.964, 0.7045)], 0.016, 0.24)):
        s.stroke(pts, "bristle", "ripple", size=sz, load=0.45,
                 load_falloff=0.8, opacity=op, pressure="swell")

def m_heron_dark():
    """The whole bird in the shadow colour. The light is a shape laid ON this,
    never a value change inside it. Dry first, or it sinks into the water."""
    s.dry()
    s.block_in(HERON_BODY, "flat", "heron_dk", size=0.012, density=1.0,
               solid=True, direction="axis", opacity=1.0, pressure="even",
               edge="clean", note="subject")
    # a neck is a stroke, not a mass: one member of even width
    s.stroke([(0.6080, 0.5000), (0.5930, 0.4570), (0.6005, 0.4150),
              (0.5910, 0.3790), (0.5808, 0.3520)], "flat", "heron_dk",
             size=0.0245, opacity=1.0, load=1.0, load_falloff=0.0,
             jitter=0.006, size_jitter=0.04, pressure="even", note="subject")
    s.stroke([(0.5972, 0.4090), (0.5900, 0.3800), (0.5812, 0.3535)], "flat",
             "heron_dk", size=0.0185, opacity=1.0, load=1.0, load_falloff=0.0,
             jitter=0.006, size_jitter=0.04, pressure="even", note="subject")
    s.block_in(HEAD, "flat", "heron_dk", size=0.0045, density=1.0, solid=True,
               direction="axis", opacity=1.0, pressure="even", note="subject")
    # the bill: a dagger. Thinner than the brush, a mass blooms pale - so it is
    # a stroke, tapering by pressure on a round tip.
    s.stroke([(0.5418, 0.3412), (0.5030, 0.3478), (0.4642, 0.3548)],
             "round_hard", "beak", size=0.0128, opacity=1.0, load=1.0,
             load_falloff=0.0, pressure=[1.0, 0.52, 0.03], note="subject")
    s.stroke([(0.5410, 0.3462), (0.5070, 0.3522)], "round_hard", "heron_dk",
             size=0.0045, opacity=0.65, load=1.0, load_falloff=0.15,
             pressure=[0.9, 0.12], note="subject")
    # two crest plumes off the crown, dark against the sky behind them
    s.stroke([(0.5830, 0.3268), (0.6030, 0.3318), (0.6230, 0.3402)], "liner",
             "heron_dk", size=0.0055, opacity=1.0, load=1.0, load_falloff=0.0,
             pressure=[1.0, 0.55, 0.0], note="subject")
    s.stroke([(0.5845, 0.3330), (0.6015, 0.3412), (0.6150, 0.3512)], "liner",
             "heron_dk", size=0.0038, opacity=0.9, load=1.0, load_falloff=0.0,
             pressure=[0.9, 0.4, 0.0], note="subject")

# the light on the bird: a grey heron is a white head and neck, a grey back and
# a dark shoulder - which is also the counterchange the picture needs.
NECK_LIT_PATH = [(0.5985, 0.4960), (0.5845, 0.4570), (0.5920, 0.4150),
                 (0.5828, 0.3790), (0.5735, 0.3540)]
SHOULDER = polygon([(0.6080, 0.5210), (0.6420, 0.5140), (0.6560, 0.5230),
                    (0.6360, 0.5390), (0.6120, 0.5390)])

def m_heron_light():
    """At this scale a plane is a stroke, not a block-in: a chisel stepping
    across a cell-sized shape shows every step."""
    # the grey back, and the flank turning under it
    s.block_in(WING, "flat", "heron_md", size=0.010, density=1.0, solid=True,
               direction="axis", opacity=0.92, pressure="even", note="subject")
    s.stroke([(0.5985, 0.5035), (0.6480, 0.4925), (0.6950, 0.5015),
              (0.7240, 0.5120)], "flat", "heron_md", size=0.0135, opacity=1.0,
             load=1.0, load_falloff=0.0, pressure="even", note="subject")
    s.stroke([(0.6120, 0.5150), (0.6520, 0.5085), (0.6930, 0.5195)], "flat",
             p.mix("heron_md", "heron_dk", 0.45), size=0.0085, opacity=0.5,
             load=1.0, load_falloff=0.0, pressure="even", note="subject")
    # the dark shoulder: three marks, not one slab, or it reads as a hole
    s.stroke([(0.6135, 0.5270), (0.6370, 0.5215)], "flat", "heron_bk",
             size=0.0140, opacity=0.85, load=1.0, load_falloff=0.3,
             pressure="even", note="subject")
    s.stroke([(0.6300, 0.5330), (0.6555, 0.5285)], "flat",
             p.mix("heron_bk", "heron_dk", 0.4), size=0.0100, opacity=0.6,
             load=0.8, load_falloff=0.5, pressure="even", note="subject")
    # the breast is a lit RIM at the front of the silhouette, not a patch in
    # the middle of it: laid inboard it reads as an egg stuck on the bird.
    s.stroke([(0.5822, 0.5100), (0.5862, 0.5340), (0.5902, 0.5570)],
             "flat", "heron_wh", size=0.0125, opacity=0.95, load=1.0,
             load_falloff=0.0, pressure="even", note="subject")
    s.stroke([(0.5928, 0.5150), (0.5962, 0.5360), (0.5980, 0.5530)],
             "flat", p.mix("heron_wh", "heron_dk", 0.55), size=0.0080,
             opacity=0.5, load=1.0, load_falloff=0.0, pressure="even",
             note="subject")
    # the dark streaking down the front of a grey heron - three, no two alike
    s.stroke([(0.5905, 0.5060), (0.5935, 0.5210)], "liner", "heron_dk",
             size=0.0042, opacity=0.6, load=0.9, load_falloff=0.3,
             pressure=[0.9, 0.1], note="subject")
    s.stroke([(0.5872, 0.5290), (0.5898, 0.5420)], "liner", "heron_dk",
             size=0.0032, opacity=0.45, load=0.8, load_falloff=0.4,
             pressure=[0.7, 0.15], note="subject")
    # and a few feathers across the flat of the back
    s.stroke([(0.6320, 0.5015), (0.6720, 0.5065)], "bristle",
             p.mix("heron_md", "heron_wh", 0.35), size=0.0092, load=0.4,
             opacity=0.45, pressure="swell", note="subject")
    s.stroke([(0.6620, 0.5150), (0.7020, 0.5230)], "bristle", "heron_dk",
             size=0.0115, load=0.45, opacity=0.4, pressure="taper", note="subject")
    # the neck in three values, left to right: white, mid, and the dark it
    # was laid in. The mid is what turns it; without it it is two stripes.
    s.stroke(NECK_LIT_PATH, "flat", "heron_lt", size=0.0092, opacity=1.0,
             load=1.0, load_falloff=0.0, jitter=0.004, size_jitter=0.03,
             pressure="even", note="subject")
    s.stroke([(0.6045, 0.4940), (0.5905, 0.4565), (0.5982, 0.4155),
              (0.5888, 0.3800), (0.5790, 0.3550)],
             "flat", p.mix("heron_lt", "heron_dk", 0.42), size=0.0078,
             opacity=0.7, load=1.0, load_falloff=0.0, pressure="even",
             note="subject")
    s.smudge([(0.6040, 0.4960), (0.5900, 0.4580), (0.5978, 0.4170),
              (0.5884, 0.3810), (0.5788, 0.3560)])
    # the head: the white, the black stripe, the eye. Three marks and stop.
    s.stroke([(0.5430, 0.3392), (0.5620, 0.3330), (0.5800, 0.3358)], "flat",
             "heron_lt", size=0.0180, opacity=1.0, load=1.0, load_falloff=0.0,
             pressure="even", note="subject")
    s.stroke([(0.5512, 0.3282), (0.5690, 0.3258), (0.5848, 0.3296)], "liner",
             "heron_bk", size=0.0068, opacity=1.0, load=1.0, load_falloff=0.0,
             pressure=[0.5, 1.0, 0.95], note="subject")
    s.dab(0.5528, 0.3368, "round_hard", "heron_bk", size=0.0060, press=3,
          tip_wobble=0.4, note="subject")

def m_heron_legs():
    """Long and thin, and the thing that puts the bird IN the water."""
    s.stroke([(0.6122, 0.5665), (0.6082, 0.6080), (0.6032, 0.6560)], "liner",
             "heron_bk", size=0.0058, opacity=1.0, load=1.0, load_falloff=0.0,
             pressure=[1.0, 0.85, 0.7], note="subject")
    # the far leg is softer and half lost - one difference per object
    s.stroke([(0.6582, 0.5580), (0.6648, 0.5960), (0.6712, 0.6430)], "liner",
             p.mix("heron_bk", "water_mid", 0.45), size=0.0048, opacity=0.7,
             load=0.85, load_falloff=0.35, pressure=[0.9, 0.55, 0.3],
             note="subject")
    # thigh feathers over the top of each
    s.stroke([(0.6090, 0.5620), (0.6180, 0.5700)], "bristle", "heron_dk",
             size=0.0110, load=0.5, opacity=0.6, pressure="taper", note="subject")

def m_heron_water():
    """Where the bird meets the surface, and what the surface gives back."""
    # the reflection: smeared and broken, never a mirror
    for pts, col, sz, ld, op, pr in (
            ([(0.5960, 0.6720), (0.6480, 0.6760), (0.6880, 0.6720)], "heron_dk", 0.030, 0.8, 0.62, "swell"),
            ([(0.6080, 0.7010), (0.6620, 0.7060)], "heron_dk", 0.022, 0.6, 0.44, "taper"),
            ([(0.5900, 0.7320), (0.6380, 0.7370)], "refl_tree", 0.017, 0.45, 0.30, "lift_off"),
            ([(0.6180, 0.7640), (0.6540, 0.7690)], "refl_tree", 0.013, 0.35, 0.22, "swell")):
        s.stroke(pts, "bristle", col, size=sz, load=ld, load_falloff=0.75,
                 opacity=op, pressure=pr, note="subject")
    # the white of it, broken into two glints
    s.stroke([(0.5985, 0.6830), (0.6160, 0.6855)], "round_hard", "heron_wh",
             size=0.0080, opacity=0.55, load=0.7, load_falloff=0.4,
             pressure=[0.9, 0.2], note="subject")
    s.stroke([(0.6040, 0.7140), (0.6165, 0.7160)], "round_hard",
             p.mix("heron_wh", "water_mid", 0.5), size=0.0060, opacity=0.4,
             load=0.6, load_falloff=0.5, pressure=[0.8, 0.15], note="subject")
    # the dark where each leg enters, and the ripple it sets going
    s.dab(0.6032, 0.6588, "round_hard", "heron_bk", size=0.0075, press=3,
          tip_wobble=0.6, note="subject")
    s.stroke([(0.5820, 0.6620), (0.6060, 0.6668), (0.6330, 0.6626)],
             "round_hard", "glint_hi", size=0.0072, opacity=0.7, load=0.8,
             load_falloff=0.4, pressure=[0.15, 1.0, 0.3], note="subject")
    s.stroke([(0.5680, 0.6790), (0.6100, 0.6858), (0.6520, 0.6800)],
             "round_hard", "glint_hi", size=0.0055, opacity=0.42, load=0.65,
             load_falloff=0.5, pressure=[0.1, 0.85, 0.2], note="subject")
    s.stroke([(0.6520, 0.6480), (0.6740, 0.6512)], "round_hard", "glint_hi",
             size=0.0050, opacity=0.5, load=0.7, load_falloff=0.45,
             pressure=[0.8, 0.15], note="subject")

def m_dawn():
    """A passage light in the middle. Laid with a comb, not a chisel - a flat
    scallops a wide band and prints its passes as stripes. The bright part
    stops before the trees: the sky is behind them, and this goes on last."""
    for y0, y1, y2, x_end, col, sz, op in (
            (0.2340, 0.2280, 0.2250, 1.07, "dawn_w", 0.058, 0.26),
            (0.2530, 0.2455, 0.2420, 1.07, "dawn1",  0.052, 0.28),
            (0.2715, 0.2635, 0.2600, 0.86, "dawn2",  0.046, 0.32),
            (0.2900, 0.2810, 0.2775, 0.72, "dawn3",  0.040, 0.34),
            (0.3080, 0.2985, 0.2950, 0.62, "dawn3",  0.034, 0.32),
            (0.3260, 0.3155, 0.3120, 0.56, "dawn2",  0.028, 0.30),
            (0.3440, 0.3330, 0.3290, 0.50, "dawn1",  0.024, 0.26)):
        s.stroke([(-0.07, y0 + 0.012), (x_end * 0.28, y0),
                  (x_end * 0.60, y1), (x_end, y2)], "bristle", col,
                 size=sz, opacity=op, load=1.0, load_falloff=0.0,
                 pressure=[0.0, 0.85, 1.0, 0.0])

def m_dawn_restore():
    """The veil went over the far trees and the bird's head. They are in front
    of the sky, so they go back on top of it."""
    s.stroke([(0.712, 0.322), (0.726, 0.286), (0.738, 0.266)], "bristle",
             "trees", size=0.030, load=0.7, opacity=0.9, pressure="lift_off")
    s.stroke([(0.836, 0.310), (0.846, 0.272), (0.838, 0.248)], "bristle",
             "trees_lt", size=0.036, load=0.6, opacity=0.8, pressure="lift_off")
    s.stroke([(0.906, 0.316), (0.930, 0.282)], "bristle", "trees",
             size=0.026, load=0.85, opacity=0.9, pressure="taper")
    s.stroke([(0.560, 0.352), (0.600, 0.340), (0.650, 0.348)], "bristle",
             "trees", size=0.028, load=0.75, opacity=0.85, pressure="swell")
    # the head, its stripe and its crest, back in front of the light
    s.stroke([(0.5430, 0.3392), (0.5620, 0.3330), (0.5800, 0.3358)], "flat",
             "heron_lt", size=0.0180, opacity=1.0, load=1.0, load_falloff=0.0,
             pressure="even", note="subject")
    s.stroke([(0.5512, 0.3282), (0.5690, 0.3258), (0.5848, 0.3296)], "liner",
             "heron_bk", size=0.0068, opacity=1.0, load=1.0, load_falloff=0.0,
             pressure=[0.5, 1.0, 0.95], note="subject")
    s.stroke([(0.5830, 0.3268), (0.6030, 0.3318), (0.6230, 0.3402)], "liner",
             "heron_bk", size=0.0052, opacity=1.0, load=1.0, load_falloff=0.0,
             pressure=[1.0, 0.55, 0.0], note="subject")
    s.dab(0.5528, 0.3368, "round_hard", "heron_bk", size=0.0060, press=3,
          tip_wobble=0.4, note="subject")

def m_dawn_water():
    """and the same light lying on the water below it"""
    for pts, col, sz, op, pr in (
            ([(-0.07, 0.452), (0.20, 0.446), (0.44, 0.442)], "dawn1", 0.026, 0.34, [0.0, 1.0, 0.35]),
            ([(0.04, 0.478), (0.28, 0.474), (0.50, 0.472)], "dawn_w", 0.018, 0.26, [0.0, 0.85, 0.2]),
            ([(0.30, 0.436), (0.52, 0.433)], "dawn2", 0.014, 0.30, [0.1, 0.9, 0.0])):
        s.stroke(pts, "flat", col, size=sz, opacity=op, load=1.0,
                 load_falloff=0.25, pressure=pr)

def m_bill_fix():
    """The bill had become the brightest thing in the picture. Against the dawn
    it wants to be dark - and the eye should go to the head, not the beak."""
    s.stroke([(0.5418, 0.3412), (0.5030, 0.3478), (0.4642, 0.3548)],
             "round_hard", p.at_value(p.mix("beak", "ultramarine", 0.30), 0.255),
             size=0.0125, opacity=0.9, load=1.0, load_falloff=0.0,
             pressure=[1.0, 0.52, 0.03], note="subject")
    s.stroke([(0.5400, 0.3368), (0.5120, 0.3418)], "liner", "beak_lit",
             size=0.0032, opacity=0.55, load=0.9, load_falloff=0.3,
             pressure=[0.85, 0.1], note="subject")

def m_nearfield_sheen():
    """The sheet-flood: cool sky lying ON the water, warm asphalt showing
    THROUGH it, in the same passage. The near water reflects the sky overhead,
    which is the cool half - not the warm horizon. Laid on the stall lines'
    own diagonal, so the foreground is not another stack of horizontals."""
    f1 = s.sample((0.05, 0.760, 0.45, 0.860))
    f2 = s.sample((0.45, 0.880, 0.95, 0.990))
    cool = p.mix("cerulean", "ultramarine", 0.35)
    p["sheen1"] = p.at_value(p.mix(f1, cool, 0.26), p.value_of(f1) + 0.062)
    p["sheen2"] = p.at_value(p.mix(f2, cool, 0.21), p.value_of(f2) + 0.050)
    p["deep"]   = p.at_value(p.mix(f2, p.mix("burnt_umber", "ultramarine", 0.30), 0.45),
                             p.value_of(f2) - 0.080)
    p["nf_dark"] = p["deep"]
    p["nf_glint"] = p.at_value(p.mix(f1, _warm2, 0.60), p.value_of(f1) + 0.155)
    s.dry()
    # two smooth patches that mirror the sky: a chisel, not a comb - a comb
    # here reads as a woven blue mat rather than as water lying still
    s.stroke([(0.92, 1.05), (0.48, 0.862), (0.04, 0.746)], "flat", "sheen1",
             size=0.086, opacity=0.30, load=1.0, load_falloff=0.35,
             pressure=[0.85, 1.0, 0.2])
    s.stroke([(1.06, 0.968), (0.66, 0.846), (0.30, 0.766)], "flat", "sheen2",
             size=0.050, opacity=0.24, load=1.0, load_falloff=0.45,
             pressure=[0.15, 1.0, 0.45])
    # one broken edge where the smooth patch gives out
    s.stroke([(0.58, 1.04), (0.26, 0.888), (-0.04, 0.796)], "bristle", "sheen1",
             size=0.040, load=0.5, load_falloff=0.8, opacity=0.30,
             pressure="swell")
    # and the asphalt coming through between them
    for pts, sz, ld, op, pr in (
            ([(0.80, 1.05), (0.50, 0.930), (0.28, 0.864)], 0.044, 0.6, 0.40, "swell"),
            ([(1.05, 1.03), (0.82, 0.950)], 0.034, 0.5, 0.32, "taper"),
            ([(0.36, 1.06), (0.10, 0.938)], 0.032, 0.55, 0.34, "lift_off")):
        s.stroke(pts, "bristle", "deep", size=sz, load=ld,
                 load_falloff=0.78, opacity=op, pressure=pr)

def m_nearfield_lines():
    """The stall lines back on top of the glaze, and the grit in the water."""
    for line, a, b, col, sz, op, ld in (
            (LANE2, 0.00, 0.30, "lane", 0.024, 0.62, 0.95),
            (LANE2, 0.40, 0.66, "lane_wet", 0.019, 0.44, 0.7),
            (LANE1, 0.02, 0.36, "lane_wet", 0.020, 0.52, 0.85),
            (LANE1, 0.52, 0.80, "lane_dim", 0.014, 0.30, 0.5),
            (LANE3, 0.06, 0.50, "lane_wet", 0.016, 0.38, 0.65)):
        s.stroke(_seg(line, a, b), "flat", col, size=sz, opacity=op, load=ld,
                 load_falloff=0.5, pressure=[0.95, 0.7, 0.12], note="lane")
    for pts, col, sz, ld, op in (
            ([(0.10, 0.935), (0.38, 0.972), (0.62, 1.008)], "grit", 0.036, 0.30, 0.52),
            ([(0.52, 0.898), (0.78, 0.942)], "nf_dark", 0.028, 0.25, 0.40),
            ([(0.80, 1.005), (1.02, 1.032)], "grit", 0.042, 0.22, 0.46),
            ([(0.20, 0.826), (0.44, 0.856)], "nf_dark", 0.026, 0.24, 0.36)):
        s.stroke(pts, "bristle", col, size=sz, load=ld, load_falloff=0.9,
                 opacity=op, pressure="swell")
    # three places where the dawn catches a ripple, and only three
    s.stroke([(0.36, 0.846), (0.50, 0.862)], "round_hard", "nf_glint",
             size=0.0075, opacity=0.65, load=0.7, load_falloff=0.45,
             pressure=[0.2, 1.0, 0.15])
    s.stroke([(0.70, 0.918), (0.84, 0.940)], "round_hard", "nf_glint",
             size=0.0060, opacity=0.48, load=0.6, load_falloff=0.5,
             pressure=[0.85, 0.1])
    s.stroke([(0.06, 0.884), (0.17, 0.898)], "round_hard", "nf_glint",
             size=0.0050, opacity=0.40, load=0.55, load_falloff=0.55,
             pressure=[0.1, 0.8, 0.1])

def m_heron_feathers():
    """The shoulder had become two rectangles - the tool's own shape standing
    for the thing. Feather groups bury them: closely spaced greys, overlapping,
    no two at the same angle."""
    g = lambda t: p.mix("heron_dk", "heron_md", t)
    for pts, col, sz, op, ld, fo in (
            # scapulars over the shoulder, burying the slabs
            ([(0.6095, 0.5195), (0.6390, 0.5140), (0.6600, 0.5175)], g(0.75), 0.0130, 1.0, 1.0, 0.10),
            ([(0.6150, 0.5300), (0.6430, 0.5245), (0.6640, 0.5290)], g(0.30), 0.0115, 0.95, 1.0, 0.20),
            ([(0.6120, 0.5390), (0.6380, 0.5350)], g(0.55), 0.0095, 0.85, 0.9, 0.35),
            ([(0.6280, 0.5155), (0.6560, 0.5125), (0.6820, 0.5185)], g(0.95), 0.0105, 0.9, 1.0, 0.25),
            # the dark shoulder, back as a broken group rather than a block
            ([(0.6180, 0.5255), (0.6395, 0.5215)], "heron_bk", 0.0090, 0.75, 0.8, 0.45),
            ([(0.6330, 0.5335), (0.6520, 0.5300)], "heron_bk", 0.0068, 0.55, 0.7, 0.55),
            # coverts and primaries running back to the tail
            ([(0.6560, 0.5260), (0.6900, 0.5290), (0.7140, 0.5230)], g(0.45), 0.0120, 0.8, 0.9, 0.30),
            ([(0.6700, 0.5140), (0.7020, 0.5175), (0.7260, 0.5135)], g(0.85), 0.0090, 0.75, 0.85, 0.40),
            ([(0.6820, 0.5380), (0.7120, 0.5330)], g(0.20), 0.0080, 0.65, 0.7, 0.5)):
        s.stroke(pts, "flat", col, size=sz, opacity=op, load=ld,
                 load_falloff=fo, pressure="even", note="subject")
    # dry-brush across it so the groups are not nine separate marks
    s.stroke([(0.6220, 0.5210), (0.6580, 0.5175), (0.6960, 0.5235)], "bristle",
             g(0.70), size=0.0165, load=0.35, load_falloff=0.85, opacity=0.40,
             pressure="swell", note="subject")
    s.stroke([(0.6400, 0.5420), (0.6760, 0.5400)], "bristle", g(0.35),
             size=0.0130, load=0.30, load_falloff=0.9, opacity=0.35,
             pressure="taper", note="subject")

def m_heron_edges():
    """Warmth in the light, softness in the belly, and one edge properly lost."""
    warm_lt = p.mix("heron_lt", _warm2, 0.22)
    # the dawn is warm: the light on the bird has to carry some of it
    s.stroke([(0.5826, 0.5130), (0.5866, 0.5330)], "flat", warm_lt,
             size=0.0085, opacity=0.45, load=1.0, load_falloff=0.2,
             pressure="even", note="subject")
    s.stroke([(0.5866, 0.4560), (0.5938, 0.4180)], "flat",
             p.mix("heron_lt", _warm2, 0.16), size=0.0058, opacity=0.40,
             load=1.0, load_falloff=0.2, pressure="even", note="subject")
    s.stroke([(0.5470, 0.3345), (0.5640, 0.3310)], "round_hard", warm_lt,
             size=0.0075, opacity=0.5, load=1.0, load_falloff=0.3,
             pressure=[0.9, 0.2], note="subject")
    # the belly was a drawn line; break it with paint across it
    s.stroke([(0.6050, 0.5640), (0.6300, 0.5735), (0.6560, 0.5640)], "bristle",
             p.mix("heron_dk", "water_mid", 0.35), size=0.0125, load=0.4,
             load_falloff=0.85, opacity=0.45, pressure="swell", note="subject")
    # and lose the tail into the water behind it - one edge, completely. The
    # value has to come off the water that is actually there, or the lost edge
    # arrives as a highlight stuck on the tail.
    behind = s.sample((0.716, 0.498, 0.766, 0.534))
    p["lose"] = p.at_value(p.mix(behind, "heron_md", 0.5),
                           (p.value_of(behind) + p.value_of(p["heron_md"])) / 2)
    s.stroke([(0.6960, 0.5095), (0.7180, 0.5125), (0.7420, 0.5180)], "bristle",
             "lose", size=0.0135, load=0.4, load_falloff=0.85, opacity=0.45,
             pressure="swell", note="subject")
    s.stroke([(0.7080, 0.5235), (0.7330, 0.5270)], "bristle",
             p.at_value(p["lose"], p.value_of(p["lose"]) - 0.06), size=0.0100,
             load=0.35, load_falloff=0.88, opacity=0.38, pressure="taper",
             note="subject")
    # the shoulder's dark had gone under the feather groups; put a little back
    s.stroke([(0.6205, 0.5270), (0.6420, 0.5232)], "flat", "heron_bk",
             size=0.0080, opacity=0.60, load=0.85, load_falloff=0.45,
             pressure="even", note="subject")

def m_waterline():
    """The trees' foot was a rule across half the canvas. Break it where the
    reflection runs straight down out of them, and keep it found twice."""
    for x, y0, y1, sz, col, op, ld in (
            (0.586, 0.398, 0.446, 0.022, "refl_tree", 0.55, 0.7),
            (0.664, 0.402, 0.438, 0.016, "refl_tree", 0.42, 0.55),
            (0.772, 0.396, 0.452, 0.026, "refl_tree", 0.50, 0.65),
            (0.902, 0.394, 0.444, 0.019, "refl_tree", 0.38, 0.5),
            (0.994, 0.392, 0.436, 0.015, "refl_tree", 0.32, 0.45)):
        s.stroke([(x, y0), (x + 0.006, (y0 + y1) / 2), (x - 0.004, y1)],
                 "bristle", col, size=sz, load=ld, load_falloff=0.8,
                 opacity=op, pressure="swell")
    # and found, twice, where the light catches the far kerb
    s.stroke([(0.700, 0.4045), (0.746, 0.4030)], "round_hard", "dawn2",
             size=0.0055, opacity=0.7, load=0.9, load_falloff=0.3,
             pressure=[0.2, 1.0, 0.15])
    s.stroke([(0.936, 0.3985), (0.982, 0.3975)], "round_hard", "dawn1",
             size=0.0045, opacity=0.5, load=0.8, load_falloff=0.4,
             pressure=[0.8, 0.1])

def m_last():
    """The subject's own footprint, the light reaching the far water, and the
    two accents the picture is allowed."""
    # the bird in the water, a little more resolved
    s.stroke([(0.5940, 0.6745), (0.6420, 0.6785), (0.6840, 0.6740)], "bristle",
             p.mix("heron_dk", "water_mid", 0.25), size=0.0245, load=0.7,
             load_falloff=0.72, opacity=0.48, pressure="swell", note="subject")
    s.stroke([(0.6060, 0.6960), (0.6520, 0.7005)], "bristle",
             p.mix("heron_bk", "water_mid", 0.45), size=0.0160, load=0.5,
             load_falloff=0.8, opacity=0.34, pressure="taper", note="subject")
    s.stroke([(0.5950, 0.6845), (0.6180, 0.6870)], "round_hard", "heron_wh",
             size=0.0072, opacity=0.5, load=0.65, load_falloff=0.5,
             pressure=[0.85, 0.15], note="subject")
    # one more ring going out from the near leg
    s.stroke([(0.5560, 0.6950), (0.6120, 0.7035), (0.6700, 0.6960)],
             "round_hard", "glint_hi", size=0.0048, opacity=0.36, load=0.6,
             load_falloff=0.55, pressure=[0.1, 0.8, 0.12], note="subject")
    # the dawn reaching the far water: the empty side gets the light, not a thing
    far = s.sample((0.86, 0.560, 1.00, 0.640))
    p["far_lt"] = p.at_value(p.mix(far, "dawn1", 0.45), p.value_of(far) + 0.055)
    s.dry()
    s.glaze([(0.82, 0.578), (0.94, 0.586), (1.07, 0.596)], "far_lt",
            opacity=0.13, size=0.075, pressure=[0.3, 0.9, 0.6])
    s.glaze([(0.86, 0.640), (0.98, 0.650), (1.07, 0.656)], "far_lt",
            opacity=0.10, size=0.042, pressure=[0.8, 0.5, 0.2])
    # a drift of cloud in the plain upper sky, on the same slight tilt
    s.stroke([(-0.06, 0.108), (0.30, 0.094), (0.66, 0.086)], "bristle",
             p.at_value(p.mix(s.sample((0.3, 0.06, 0.6, 0.13)), _warm2, 0.35), 0.575),
             size=0.038, load=0.4, load_falloff=0.88, opacity=0.30,
             pressure="swell")
    s.stroke([(0.44, 0.052), (0.82, 0.044), (1.06, 0.050)], "bristle",
             p.at_value(p.mix(s.sample((0.5, 0.02, 0.9, 0.08)), _warm2, 0.28), 0.545),
             size=0.028, load=0.35, load_falloff=0.9, opacity=0.24,
             pressure="taper")
    # and the two accents the picture is allowed: the eye, and the bill's tip
    s.dab(0.5522, 0.3362, "round_hard", "heron_bk", size=0.0048, press=3,
          tip_wobble=0.5, note="subject")
    s.dab(0.5498, 0.3338, "round_hard", "titanium_white", size=0.0022, press=3,
          note="subject")

def m_midwater():
    """The weakest passage: a wide empty mid-blue between the lamp and the bird.
    What is actually there is more of the lot - the stall lines running on to
    the far end, fainter and closer together as they go."""
    f = s.sample((0.34, 0.560, 0.74, 0.680))
    v = p.value_of(f)
    p["far_lane"]  = p.at_value(p.mix(f, "lane", 0.55), v + 0.075)
    p["far_lane2"] = p.at_value(p.mix(f, "lane", 0.40), v + 0.050)
    p["far_dark"]  = p.at_value(p.mix(f, "wet_asph", 0.50), v - 0.065)
    # unevenly spaced and barely there: a fan of equal bars is a diagram
    for x0, y0, x1, col, sz, op, ld in (
            (0.905, 0.716, 0.575, "far_lane",  0.016, 0.28, 0.7),
            (1.000, 0.652, 0.760, "far_lane2", 0.012, 0.20, 0.55),
            (0.790, 0.792, 0.430, "far_lane",  0.019, 0.24, 0.6),
            (0.455, 0.706, 0.205, "far_lane2", 0.013, 0.17, 0.5)):
        y1 = y0 - 0.2913 * (x0 - x1)
        s.stroke([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 + 0.002), (x1, y1)],
                 "flat", col, size=sz, opacity=op, load=ld, load_falloff=0.55,
                 pressure=[0.9, 0.65, 0.08], note="lane")
    # asphalt showing through between them, on the same diagonal
    for x0, y0, x1, sz, ld, op in ((0.840, 0.752, 0.480, 0.030, 0.55, 0.32),
                                   (0.600, 0.660, 0.330, 0.024, 0.45, 0.26),
                                   (1.020, 0.700, 0.780, 0.026, 0.40, 0.24)):
        y1 = y0 - 0.2913 * (x0 - x1)
        s.stroke([(x0, y0), (x1, y1)], "bristle", "far_dark", size=sz,
                 load=ld, load_falloff=0.85, opacity=op, pressure="swell")
    # the lamp's path carried on to the bottom edge rather than stopping short
    s.stroke([(0.2340, 0.8960), (0.2520, 0.8935)], "round_hard", "lamp_wtr",
             size=0.0068, opacity=0.24, load=0.6, load_falloff=0.5,
             pressure=[0.7, 0.15])
    s.stroke([(0.2410, 0.9420), (0.2680, 0.9390)], "round_hard", "lamp_wtr",
             size=0.0055, opacity=0.18, load=0.5, load_falloff=0.6,
             pressure=[0.15, 0.7, 0.1])
    # one slack cable off the pole: the upper half had nothing crossing it
    sky_here = s.sample((0.40, 0.130, 0.80, 0.190))
    s.stroke([(0.2420, 0.1125), (0.4400, 0.1530), (0.6400, 0.1735),
              (0.8200, 0.1740)], "liner",
             p.at_value(p.mix(sky_here, "pole", 0.30),
                        p.value_of(sky_here) - 0.115),
             size=0.0030, opacity=0.35, load=1.0, load_falloff=0.30,
             pressure=[1.0, 0.7, 0.35, 0.0])

def m_final():
    """Repairs, and the last quiet passage."""
    # the dawn band went over the pole as well: it is in front of the sky
    ruled = dict(opacity=0.92, load=1.0, load_falloff=0.0, jitter=0.0,
                 size_jitter=0.0, pressure="even")
    s.stroke([(0.2125, 0.2280), (0.2200, 0.3320), (0.2262, 0.4280)], "flat",
             "pole", size=0.0072, **ruled)
    s.stroke([(0.2155, 0.2620), (0.2205, 0.3480)], "flat",
             p.at_value(p["pole"], 0.315), size=0.0042, opacity=0.6,
             load=1.0, load_falloff=0.0, jitter=0.0, size_jitter=0.0,
             pressure="even")
    # the neck's lit edge was a taped strip. Soften it BELOW the head only -
    # the focal edge stays hard and the ones away from it give way.
    s.stroke([(0.5890, 0.4780), (0.5838, 0.4530), (0.5880, 0.4280)], "bristle",
             p.mix("heron_lt", "water_mid", 0.42), size=0.0105, load=0.35,
             load_falloff=0.85, opacity=0.42, pressure="swell", note="subject")
    s.stroke([(0.5806, 0.4620), (0.5960, 0.4675)], "bristle",
             p.mix("heron_lt", "heron_md", 0.55), size=0.0080, load=0.30,
             load_falloff=0.9, opacity=0.34, pressure="taper", note="subject")
    # and the breast rim had chisel ends: break them with paint across
    s.stroke([(0.5760, 0.5560), (0.5900, 0.5620), (0.6020, 0.5580)], "bristle",
             p.mix("heron_wh", "heron_dk", 0.45), size=0.0105, load=0.35,
             load_falloff=0.88, opacity=0.45, pressure="swell", note="subject")
    s.stroke([(0.5800, 0.5060), (0.5920, 0.5010)], "bristle",
             p.mix("heron_wh", "heron_md", 0.4), size=0.0085, load=0.3,
             load_falloff=0.9, opacity=0.38, pressure="taper", note="subject")
    # the left water was the last plain passage: incident, off the field itself
    fl = s.sample((0.02, 0.520, 0.20, 0.640))
    p["lw_hi"] = p.at_value(fl, p.value_of(fl) + 0.075)
    p["lw_lo"] = p.at_value(p.mix(fl, "wet_asph", 0.45), p.value_of(fl) - 0.070)
    for pts, col, sz, ld, op, pr in (
            ([(-0.04, 0.5580), (0.112, 0.5525)], "lw_hi", 0.026, 0.35, 0.42, "swell"),
            ([(0.040, 0.6120), (0.176, 0.6185)], "lw_lo", 0.030, 0.45, 0.34, "taper"),
            ([(-0.03, 0.6720), (0.128, 0.6790)], "lw_hi", 0.022, 0.30, 0.36, "lift_off"),
            ([(0.088, 0.4880), (0.196, 0.4845)], "lw_hi", 0.019, 0.28, 0.30, "swell"),
            ([(0.012, 0.7180), (0.180, 0.7285)], "lw_lo", 0.034, 0.40, 0.28, "swell")):
        s.stroke(pts, "bristle", col, size=sz, load=ld, load_falloff=0.88,
                 opacity=op, pressure=pr)
    # and two pieces of aggregate in the dark corner
    s.stroke([(0.030, 0.902), (0.148, 0.946)], "bristle", "grit", size=0.030,
             load=0.28, load_falloff=0.92, opacity=0.42, pressure="swell")
    s.stroke([(0.062, 1.010), (0.196, 1.038)], "bristle", "wet_asph",
             size=0.036, load=0.24, load_falloff=0.92, opacity=0.34,
             pressure="taper")
