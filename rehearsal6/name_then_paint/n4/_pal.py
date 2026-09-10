p = s.palette

def at(c, target):
    """Mix c toward white or toward ink until it reads `target` in the value view."""
    up = p.value_of(c) < target
    other = "titanium_white" if up else p["ink"]
    lo, hi = 0.0, 1.0
    for _ in range(26):
        mid = (lo + hi) / 2.0
        v = p.value_of(p.mix(c, other, mid))
        if (v < target) == up:
            lo = mid
        else:
            hi = mid
    return p.mix(c, other, (lo + hi) / 2.0)

p["ink"] = p.mix("ultramarine", "burnt_umber", 0.45)

_neutral = p.mix("ultramarine", "burnt_sienna", 0.55)      # complements -> grey
_warmgrey = p.mix("burnt_umber", "yellow_ochre", 0.40)
_terra   = p.mix("burnt_sienna", "cadmium_red", 0.28)
_leaf    = p.mix("viridian", "burnt_umber", 0.35)
_sage    = p.mix(p.mix("viridian", "yellow_ochre", 0.42), "ultramarine", 0.12)

# --- the window: palest mass, dusty, cool at the bottom, hot at the top right
p["glass"]      = at(p.mix(_neutral, "yellow_ochre", 0.18), 0.82)
p["glass_hot"]  = at(p.mix(_neutral, "cadmium_yellow", 0.30), 0.90)
p["glass_low"]  = at(p.desaturate(p.mix(_neutral, "cerulean", 0.20), 0.60), 0.755)
p["glass_far"]  = at(p.desaturate(p.mix(_neutral, "yellow_ochre", 0.25), 0.45), 0.66)
p["bar"]        = at(p.desaturate(_warmgrey, 0.25), 0.38)
p["bar_lit"]    = at(_warmgrey, 0.60)

# --- the wall on the right
p["wall_lit"]   = at(p.desaturate(_warmgrey, 0.30), 0.47)
p["wall"]       = at(p.desaturate(p.mix(_warmgrey, "ultramarine", 0.18), 0.25), 0.40)
p["wall_dk"]    = at(p.mix(_warmgrey, "ultramarine", 0.30), 0.325)

# --- the sill
p["sill_hot"]   = at(p.mix(_warmgrey, "cadmium_yellow", 0.35), 0.74)
p["sill_lit"]   = at(p.mix(_warmgrey, "yellow_ochre", 0.45), 0.63)
p["sill_shad"]  = at(p.mix(_warmgrey, "ultramarine", 0.30), 0.42)
p["sill_face"]  = at(p.mix(_warmgrey, "ultramarine", 0.35), 0.31)
p["under"]      = at(p.mix("burnt_umber", "ultramarine", 0.35), 0.17)

# --- the pot
p["pot_lit"]    = at(_terra, 0.54)
p["pot_mid"]    = at(_terra, 0.39)
p["pot_shad"]   = at(p.mix(_terra, "ultramarine", 0.30), 0.25)
p["pot_rim"]    = at(p.mix(_terra, "cadmium_yellow", 0.25), 0.64)
p["crack"]      = at(p.mix(_terra, "ultramarine", 0.55), 0.16)
p["soil"]       = at(p.mix("burnt_umber", "ultramarine", 0.20), 0.20)

# --- the rosemary
p["leaf_dk"]    = at(p.desaturate(p.mix(_leaf, "ultramarine", 0.25), 0.45), 0.175)
p["leaf_mid"]   = at(p.desaturate(_leaf, 0.50), 0.265)
p["leaf_lit"]   = at(p.desaturate(_sage, 0.62), 0.395)
p["leaf_hot"]   = at(p.desaturate(p.mix(_sage, "cadmium_yellow", 0.20), 0.58), 0.520)

p["wall_edge"] = at(p.mix(_warmgrey, "ultramarine", 0.30), 0.355)
p["sill_lit"]  = at(p.desaturate(p.mix(_warmgrey, "yellow_ochre", 0.40), 0.55), 0.620)
p["sill_hot"]  = at(p.desaturate(p.mix(_warmgrey, "cadmium_yellow", 0.30), 0.42), 0.735)
p["sill_mid"]  = at(p.desaturate(p.mix(_warmgrey, "yellow_ochre", 0.35), 0.60), 0.500)
p["sill_shad"] = at(p.desaturate(p.mix(_warmgrey, "ultramarine", 0.22), 0.30), 0.450)
p["sill_face"] = at(p.desaturate(p.mix(_warmgrey, "ultramarine", 0.30), 0.35), 0.300)
p["under"]     = at(p.desaturate(p.mix("burnt_umber", "ultramarine", 0.22), 0.18), 0.175)
p["arris"]     = at(p.desaturate(p.mix(_warmgrey, "cadmium_yellow", 0.32), 0.38), 0.715)
p["stem"]      = at(p.desaturate(p.mix("burnt_umber", "viridian", 0.30), 0.35), 0.220)
