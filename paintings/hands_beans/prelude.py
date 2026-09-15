# --- prelude: palette, landmarks and every mass as a named function -------------
# Re-run the stack in depth order to repair anything (RECIPES: a repair under
# things that are standing on it).

p = s.palette

# --- mixtures ------------------------------------------------------------------
_wood  = p.mix(p.mix("burnt_umber", "burnt_sienna", 0.30), "ultramarine", 0.12)
_flesh = p.mix("yellow_ochre", "burnt_sienna", 0.40)
_cool  = p.mix(_flesh, "ultramarine", 0.22)
_warm  = p.mix("burnt_sienna", "cadmium_red", 0.35)
_crock = p.desaturate(p.mix("burnt_umber", "ultramarine", 0.20), 0.30)
_bean  = p.mix("burnt_sienna", "burnt_umber", 0.45)

p["tbl_deep"]  = p.at_value(_wood, 0.16)
p["table"]     = p.at_value(_wood, 0.23)
p["tbl_lit"]   = p.at_value(p.mix(_wood, "yellow_ochre", 0.24), 0.35)
p["bean_dk"]   = p.at_value(_bean, 0.22)
p["bean"]      = p.at_value(_bean, 0.28)
p["bean_lit"]  = p.at_value(p.desaturate(p.mix(_bean, "yellow_ochre", 0.30), 0.20), 0.50)
p["fl_shad"]   = p.at_value(_cool, 0.34)
p["crock"]     = p.at_value(_crock, 0.25)
p["fl_mid"]    = p.at_value(p.desaturate(_flesh, 0.30), 0.53)
p["fl_warm"]   = p.at_value(p.desaturate(_warm, 0.15), 0.59)
p["crock_lit"] = p.at_value(p.mix(_crock, "titanium_white", 0.30), 0.46)
p["fl_lit"]    = p.at_value(p.desaturate(p.mix(_flesh, "titanium_white", 0.45), 0.18), 0.73)
p["fl_high"]   = p.at_value(p.mix(_flesh, "titanium_white", 0.70), 0.85)
p["fl_arm"]    = p.at_value(p.desaturate(_flesh, 0.40), 0.44)
p["palm_dk"]   = p.at_value(_cool, 0.25)
p["bean_palm"] = p.at_value(p.desaturate(p.mix(_bean, "yellow_ochre", 0.25), 0.25), 0.40)
p["fl_deep"]   = p.at_value(_cool, 0.20)   # between the fingers, and under them
p["fl_body"]   = p.at_value(p.mix(p.desaturate(_flesh, 0.35), _cool, 0.30), 0.42)
p["fl_body2"]  = p.at_value(p.mix(p.desaturate(_flesh, 0.30), _cool, 0.18), 0.46)
p["fl_body3"]  = p.at_value(p.mix(p.desaturate(_flesh, 0.40), _cool, 0.45), 0.34)
p["fl_plane"]  = p.at_value(p.mix(p.desaturate(_flesh, 0.55), _cool, 0.25), 0.52)
p["rim_lit"]   = p.at_value(p.mix(_crock, "yellow_ochre", 0.45), 0.42)
p["bean_warm"] = p.at_value(p.desaturate(p.mix(_bean, "yellow_ochre", 0.40), 0.30), 0.41)
p["fl_core"]   = p.at_value(p.mix("burnt_umber", "burnt_sienna", 0.42), 0.175)  # warm core shadow
p["fl_under"]  = p.at_value(p.mix(p.mix("burnt_umber", "burnt_sienna", 0.30), _cool, 0.25), 0.225)
p["glow"]      = p.at_value(p.mix(_wood, "yellow_ochre", 0.38), 0.385)
p["glow_mid"]  = p.at_value(p.mix(_wood, "yellow_ochre", 0.26), 0.315)
p["corner"]    = p.at_value(_wood, 0.145)
p["grain"]     = p.at_value(p.mix(_wood, "burnt_sienna", 0.30), 0.255)
p["fl_spark"]  = p.at_value(p.mix(_flesh, "titanium_white", 0.80), 0.905)
p["joint"]     = p.at_value(p.desaturate(p.mix("burnt_sienna", "cadmium_red", 0.45), 0.42), 0.505)
p["joint_lo"]  = p.at_value(p.desaturate(p.mix("burnt_sienna", "alizarin", 0.30), 0.45), 0.395)
p["fl_cool"]   = p.at_value(p.desaturate(p.mix(_flesh, "cerulean", 0.055), 0.62), 0.595)
p["fl_side"]   = p.at_value(p.desaturate(p.mix(_flesh, "burnt_umber", 0.42), 0.38), 0.365)
p["fl_side2"]  = p.at_value(p.desaturate(p.mix(_flesh, "burnt_umber", 0.52), 0.40), 0.315)
p["veil"]      = p.at_value(p.mix("burnt_sienna", "yellow_ochre", 0.32), 0.405)
p["veil_lo"]   = p.at_value(p.mix("burnt_sienna", "yellow_ochre", 0.26), 0.310)

# --- landmarks -----------------------------------------------------------------
for _stale in ("bowl_c", "back_c", "bowl_r"):
    s.unmark(_stale)
LANDMARKS = {
    "pinch":  (0.484, 0.478),   # thumb and finger closing on one bean: the focal point
    "ftip":   (0.276, 0.492),   # tip of the cupped hand's middle finger
    "palm_c": (0.448, 0.562),   # centre of the cupped palm
    "heel":   (0.648, 0.790),   # heel of the cupped hand
    "knuck":  (0.700, 0.252),   # the picking hand's knuckles
    "bowlf":  (0.100, 0.725),   # top of the bowl's far rim
}
for _n, (_x, _y) in LANDMARKS.items():
    s.mark(_n, _x, _y)

# --- the bowl: a fragment, cropped by the left and bottom edges -----------------
BOWL_OUT = ellipse(Region(-0.220, 0.725, 0.420, 1.075))
BOWL_IN  = ellipse(Region(-0.168, 0.748, 0.368, 1.024))

# --- the cupped hand: left hand, palm up, wrist to the lower right --------------
CUP_PALM = polygon([
    (0.334, 0.496), (0.410, 0.454), (0.494, 0.444), (0.558, 0.470), (0.608, 0.516),
    (0.642, 0.578), (0.652, 0.650), (0.628, 0.710), (0.570, 0.740), (0.492, 0.738),
    (0.412, 0.716), (0.352, 0.670), (0.322, 0.604), (0.318, 0.542),
]).smooth(2)
CUP_HOLLOW = ellipse(Region(0.350, 0.488, 0.546, 0.636), rotate=-8)

# index reaches furthest, the little finger is shortest and curls hardest.
CUP_FING = [
    ([(0.516, 0.444), (0.434, 0.410), (0.356, 0.406), (0.296, 0.428)], 0.046, 0.037),
    ([(0.508, 0.488), (0.418, 0.458), (0.336, 0.458), (0.274, 0.488)], 0.050, 0.040),
    ([(0.500, 0.532), (0.414, 0.512), (0.340, 0.520), (0.282, 0.552)], 0.046, 0.037),
    ([(0.492, 0.572), (0.424, 0.566), (0.366, 0.582), (0.322, 0.606)], 0.038, 0.031),
]
CUP_THUMB = ([(0.596, 0.702), (0.516, 0.682), (0.452, 0.650), (0.408, 0.612)], 0.066, 0.048)
CUP_ARM   = ([(0.616, 0.648), (0.726, 0.780), (0.830, 0.916), (0.930, 1.060)], 0.146, 0.168)

CUP = union(polygon(ribbon(*CUP_ARM).closed), CUP_PALM,
            *[polygon(ribbon(pts, w, e).closed) for pts, w, e in CUP_FING],
            polygon(ribbon(*CUP_THUMB).closed))

# --- the picking hand: right hand, palm down, in steeply from the top -----------
PICK_BACK = polygon([
    (0.596, 0.290), (0.646, 0.210), (0.716, 0.166), (0.788, 0.190), (0.818, 0.252),
    (0.796, 0.318), (0.732, 0.360), (0.656, 0.352), (0.614, 0.326),
]).smooth(2)
PICK_ARM   = ([(0.752, 0.254), (0.812, 0.128), (0.856, 0.006), (0.882, -0.080)],
              0.132, 0.118)
PICK_INDEX = ([(0.610, 0.296), (0.564, 0.360), (0.522, 0.420), (0.492, 0.464)],
              0.056, 0.038)
PICK_THUMB = ([(0.644, 0.352), (0.578, 0.416), (0.520, 0.464), (0.478, 0.498)],
              0.062, 0.040)
PICK_CURL  = polygon([
    (0.692, 0.344), (0.760, 0.336), (0.796, 0.378), (0.778, 0.430), (0.722, 0.450),
    (0.664, 0.436), (0.642, 0.394),
]).smooth(2)

PICK = union(polygon(ribbon(*PICK_ARM).closed), PICK_BACK, PICK_CURL,
             polygon(ribbon(*PICK_INDEX).closed), polygon(ribbon(*PICK_THUMB).closed))

# --- the planes, decided beside the silhouettes, not after the mass is down -----
# Light from the upper left: each finger's upper-left face is lit and its
# lower-right is left as the block-in's dark. Offsets and widths vary per finger
# on purpose -- four identical ribbons would be a comb.
CUP_FING_LIT = [
    ([(0.508, 0.436), (0.432, 0.404), (0.360, 0.401), (0.306, 0.421)], 0.026, 0.018),
    ([(0.500, 0.478), (0.418, 0.450), (0.340, 0.450), (0.284, 0.478)], 0.030, 0.021),
    ([(0.492, 0.522), (0.412, 0.503), (0.342, 0.511), (0.290, 0.540)], 0.023, 0.015),
    ([(0.486, 0.564), (0.424, 0.560), (0.372, 0.574), (0.334, 0.596)], 0.017, 0.012),
]
CUP_KNUCK = polygon([                       # the ridge the fingers rise out of
    (0.474, 0.436), (0.526, 0.446), (0.556, 0.478), (0.560, 0.530),
    (0.548, 0.578), (0.512, 0.588), (0.482, 0.556), (0.470, 0.494),
]).smooth(2)
CUP_HEEL = polygon([                        # the near rim of the cup, toward us
    (0.540, 0.646), (0.612, 0.652), (0.648, 0.684), (0.638, 0.726),
    (0.576, 0.740), (0.504, 0.730), (0.470, 0.700), (0.486, 0.664),
]).smooth(2)
CUP_THUMB_LIT = ([(0.588, 0.688), (0.512, 0.668), (0.452, 0.638), (0.412, 0.604)],
                 0.030, 0.020)
CUP_ARM_LIT = ([(0.618, 0.662), (0.712, 0.776), (0.804, 0.894), (0.890, 1.012)],
               0.070, 0.054)

PICK_BACK_LIT = polygon([                   # the lit plane on the back of the hand
    (0.610, 0.282), (0.652, 0.214), (0.718, 0.178), (0.780, 0.200), (0.800, 0.250),
    (0.762, 0.290), (0.690, 0.302), (0.634, 0.302),
]).smooth(2)
PICK_INDEX_LIT = ([(0.604, 0.298), (0.560, 0.358), (0.520, 0.416), (0.492, 0.458)],
                  0.030, 0.019)
PICK_THUMB_LIT = ([(0.638, 0.352), (0.576, 0.412), (0.522, 0.458), (0.484, 0.490)],
                  0.032, 0.020)
PICK_ARM_LIT = ([(0.744, 0.250), (0.800, 0.130), (0.842, 0.014), (0.866, -0.070)],
                0.062, 0.052)
