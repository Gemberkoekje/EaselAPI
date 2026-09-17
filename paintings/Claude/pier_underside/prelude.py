# ---- values, planned as numbers before anything is mixed -------------------
p = s.palette
p["deck"]      = p.at_value(p.mix("burnt_umber", "viridian", 0.30), 0.22)
p["beam"]      = p.at_value(p.mix("burnt_umber", "viridian", 0.34), 0.14)
p["deck_warm"] = p.at_value(p.mix("burnt_umber", "yellow_ochre", 0.35), 0.24)
p["pile"]      = p.at_value(p.mix("burnt_umber", "viridian", 0.50), 0.19)
p["pile_lit"]  = p.at_value(p.mix("yellow_ochre", "viridian", 0.45), 0.44)
p["water"]     = p.at_value(p.mix("viridian", "burnt_umber", 0.45), 0.28)
p["water_lit"] = p.at_value(p.desaturate(p.mix("viridian", "titanium_white", 0.42), 0.30), 0.52)
p["opening"]   = p.at_value(p.mix("yellow_ochre", "titanium_white", 0.62), 0.80)
p["caustic"]   = p.at_value(p.mix("lemon_yellow", "titanium_white", 0.45), 0.90)
p["barnacle"]  = p.at_value(p.mix("titanium_white", "yellow_ochre", 0.30), 0.64)

VP = (0.72, 0.625)          # the far end, where the deck meets the light

# ---- masses, each its own function so the stack can be re-run --------------
def deck():                 # the underside -- the subject, and most of the frame
    return polygon([(0.0, 0.0), (1.0, 0.0), (1.0, 0.540), (0.84, 0.558),
                    (0.72, 0.577), (0.56, 0.600), (0.38, 0.626),
                    (0.20, 0.670), (0.0, 0.718)])

def water():                # a strip at the foot, catching the slot
    return polygon([(0.0, 1.0), (1.0, 1.0), (1.0, 0.676), (0.78, 0.686),
                    (0.55, 0.700), (0.32, 0.716), (0.0, 0.748)])

def slot():                 # the wedge of daylight between them, right side only
    return polygon([(0.26, 0.726), (0.50, 0.610), (0.72, 0.584),
                    (1.0, 0.545), (1.0, 0.684), (0.72, 0.692),
                    (0.50, 0.706), (0.27, 0.734)])

def piles():                # near to far; each a ribbon, none of them straight
    return [
        ribbon([(0.145, 0.0), (0.135, 0.30), (0.155, 0.60), (0.142, 0.88)], 0.105, 0.088),
        ribbon([(0.885, 0.0), (0.897, 0.32), (0.875, 0.60), (0.889, 0.80)], 0.078, 0.062),
        ribbon([(0.425, 0.315), (0.417, 0.50), (0.428, 0.700)], 0.042, 0.032),
        ribbon([(0.622, 0.435), (0.627, 0.545), (0.620, 0.672)], 0.024, 0.018),
    ]

def beams():                # the grain of the underside, converging on VP
    return [[(0.0, y), VP] for y in (0.04, 0.155, 0.275, 0.40, 0.525)] +            [[(1.0, y), VP] for y in (0.10, 0.245, 0.395)]
