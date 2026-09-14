"""Fogged glass: a greenhouse wall in late winter, seen from outside.

The projection is written first, per RECIPES 'A scene with straight edges'.
Everything in the scene is placed in metres and P() says where it lands.
"""

# ---------------------------------------------------------------- projection
VX, VY = 0.22, 0.46          # vanishing point == horizon == eye level
F      = 0.80                # focal length
E      = 1.70                # eye height, metres

def P(xm, hm, dm):
    """Screen point: xm metres right of the axis, hm above the ground, dm away."""
    return (VX + xm * F / dm, VY - (hm - E) * F * s.aspect / dm)

# the greenhouse, in metres
WALL   = 1.40                # the glass wall is this far to my right
SILL   = 0.60                # top of the brick base
EAVE   = 2.10
RIDGE_X, RIDGE_H = 3.60, 2.95
FAR    = 22.0                # the far gable
NEAR   = 1.15                # nearer than the right edge of the canvas

BAR_DM = [1.92, 2.54, 3.16, 3.78, 4.40, 5.02, 5.64, 6.26]   # glazing bars
def bar_w(dm):               # a 45 mm bar, at that distance
    return max(0.8 * 0.045 / dm, 0.0045)

# ------------------------------------------------------------------ palette
p = s.palette
p["neutral"] = p.mix("ultramarine", "burnt_umber", 0.5)
p["sky"]      = p.at_value(p.mix(p["neutral"], "cerulean", 0.11), 0.61)
p["skymid"]   = p.at_value(p.mix(p["neutral"], "cerulean", 0.05), 0.67)
p["skylow"]   = p.at_value(p.mix(p["neutral"], "yellow_ochre", 0.12), 0.73)
p["lip"]      = p.at_value(p.mix(p["neutral"], "cerulean", 0.06), 0.86)
p["fogcool"]  = p.at_value(p.desaturate(p.mix("cerulean", "titanium_white", 0.72), 0.30), 0.60)
p["fog"]      = p.at_value(p.desaturate(p.mix(p.mix("yellow_ochre", "cerulean", 0.42),
                                              "titanium_white", 0.70), 0.35), 0.55)
p["fogwarm"]  = p.at_value(p.desaturate(p.mix(p.mix("yellow_ochre", "titanium_white", 0.62),
                                              "burnt_sienna", 0.14), 0.52), 0.52)
p["leafhaze"] = p.at_value(p.desaturate(p.mix(p.mix("viridian", "yellow_ochre", 0.45),
                                              "burnt_umber", 0.20), 0.55), 0.44)
p["leafmid"]  = p.at_value(p.mix(p.mix("viridian", "yellow_ochre", 0.34), "burnt_umber", 0.14), 0.34)
p["leaf"]     = p.at_value(p.mix(p.mix("viridian", "yellow_ochre", 0.28), "burnt_umber", 0.12), 0.26)
p["bar"]      = p.at_value(p.mix("burnt_umber", "ultramarine", 0.32), 0.36)
p["barlit"]   = p.at_value(p.mix("burnt_umber", "ultramarine", 0.22), 0.56)
p["brick"]    = p.at_value(p.mix(p.mix("burnt_sienna", "burnt_umber", 0.45), "ultramarine", 0.18), 0.30)
p["trees"]    = p.at_value(p.desaturate(p.mix("burnt_umber", "ultramarine", 0.45), 0.25), 0.50)
p["yard"]     = p.at_value(p.desaturate(p.mix("yellow_ochre", "ultramarine", 0.34), 0.40), 0.42)
p["warm"]     = p.at_value(p.mix(p.mix("burnt_sienna", "cadmium_red", 0.42), "burnt_umber", 0.12), 0.38)
p["dark"]     = p.at_value(p.mix("ultramarine", "burnt_umber", 0.48), 0.20)

# ------------------------------------------------- the masses, clipped at the frame
from easel import polygon, blob, ellipse, ribbon

def _edge_x(y_target, hm):
    """dm at which the line at height hm crosses screen y = y_target."""
    return 1.2 * (E - hm) / (y_target - VY)

R_EDGE_DM = F * WALL / (1.0 - VX)          # where the wall meets the right frame

EAVE_R  = P(WALL, EAVE, R_EDGE_DM)         # (1.00, 0.126)
EAVE_F  = P(WALL, EAVE, FAR)
SILL_F  = P(WALL, SILL, FAR)
GRND_F  = P(WALL, 0.0,  FAR)
SILL_B  = P(WALL, SILL, _edge_x(1.0, SILL))    # sill leaves the bottom frame
GRND_B  = P(WALL, 0.0,  _edge_x(1.0, 0.0))     # ground line leaves the bottom frame
RIDGE_R = P(RIDGE_X, RIDGE_H, F * RIDGE_X / (1.0 - VX))

GLASS = polygon([EAVE_F, EAVE_R, (1.04, 1.04), SILL_B, SILL_F])
BASE  = polygon([SILL_F, SILL_B, GRND_B, GRND_F])
LIP   = polygon([EAVE_F, EAVE_R, RIDGE_R, (RIDGE_X * 0 + VX + 0.004, VY - 0.010)])
SKY   = polygon([(-0.04, -0.04), (1.04, -0.04), RIDGE_R, EAVE_F, (VX, VY), (-0.04, VY + 0.01)])
YARD  = polygon([(-0.04, VY), (VX, VY), GRND_F, GRND_B, (-0.04, 1.04)])

# what stands inside the glass
TALL  = blob((0.865, 0.525), 0.135, 0.295, wobble=0.42, seed=4)
BANK  = blob((0.632, 0.648), 0.158, 0.096, wobble=0.38, seed=7)
HANG  = blob((0.762, 0.330), 0.112, 0.068, wobble=0.45, seed=2)
DIM   = blob((0.420, 0.452), 0.095, 0.050, wobble=0.35, seed=9)

# the runnels: no two alike -- different lengths, starts, wander and weight
RUNNELS = [
  ([(0.907, 0.09), (0.898, 0.31), (0.914, 0.49), (0.899, 0.67), (0.911, 0.87), (0.904, 1.02)], 1.00),
  ([(0.843, 0.19), (0.855, 0.37), (0.840, 0.58), (0.851, 0.81), (0.844, 1.02)], 0.85),
  ([(0.975, 0.05), (0.964, 0.27), (0.978, 0.53), (0.967, 0.82)], 0.75),
  ([(0.932, 0.42), (0.941, 0.63), (0.930, 0.86)], 0.55),
  ([(0.869, 0.62), (0.877, 0.84), (0.870, 1.02)], 0.45),
  ([(0.757, 0.24), (0.749, 0.43), (0.760, 0.64), (0.751, 0.88)], 0.80),
  ([(0.722, 0.51), (0.729, 0.72), (0.721, 0.95)], 0.50),
  ([(0.700, 0.31), (0.706, 0.49), (0.698, 0.70)], 0.40),
  ([(0.646, 0.37), (0.641, 0.55), (0.648, 0.77)], 0.35),
  ([(0.616, 0.42), (0.620, 0.62)], 0.25),
]

# the tree in the yard, twelve metres off
TRUNK  = [(0.128, 0.622), (0.133, 0.49), (0.139, 0.37), (0.144, 0.255), (0.148, 0.135)]
BOUGHS = [
  ([(0.140, 0.345), (0.078, 0.255), (0.030, 0.150)], 0.55),
  ([(0.137, 0.420), (0.205, 0.330), (0.258, 0.198)], 0.55),
  ([(0.146, 0.215), (0.092, 0.120), (0.058, 0.048)], 0.40),
  ([(0.145, 0.240), (0.214, 0.150), (0.268, 0.072)], 0.40),
  ([(0.148, 0.135), (0.300, 0.093), (0.520, 0.052), (0.790, 0.028)], 0.45),
  ([(0.300, 0.093), (0.366, 0.028)], 0.30),
  ([(0.520, 0.052), (0.602, 0.010)], 0.30),
]
CROWN = ellipse((0.142, 0.300), 0.135, 0.230)
PATH  = polygon([(-0.04, 0.86), (0.36, 0.60), GRND_F, (-0.04, 0.66)])

HEDGE = blob((0.10, 0.470), 0.185, 0.030, wobble=0.55, seed=12)
