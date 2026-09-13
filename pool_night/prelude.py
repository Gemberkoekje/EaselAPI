# ---- mixtures -------------------------------------------------------------
p = s.palette
grey = p.mix("cerulean", "burnt_umber", 0.50)

p["night"]   = p.at_value(p.mix("cerulean", "burnt_umber", 0.55), 0.16)
p["truss"]   = p.at_value(p.mix("ultramarine", "burnt_umber", 0.55), 0.142)
p["wall"]    = p.at_value(p.mix(grey, "viridian", 0.22), 0.34)
p["deckfar"] = p.at_value(p.mix(grey, "titanium_white", 0.35), 0.30)
p["deck"]    = p.at_value(p.mix(p.mix(grey, "titanium_white", 0.45), "alizarin", 0.07), 0.44)
p["water"]   = p.at_value(p.mix("cerulean", "viridian", 0.28), 0.66)
p["watdeep"] = p.at_value(p.mix("cerulean", "viridian", 0.35), 0.57)
p["watrefl"] = p.at_value(p.mix(p.mix("cerulean", "viridian", 0.40), "night", 0.45), 0.40)
p["watlit"]  = p.at_value(p.mix(p.mix("cerulean", "viridian", 0.22), "titanium_white", 0.5), 0.82)
p["core"]    = p.at_value(p.mix("cerulean", "titanium_white", 0.85), 0.93)
p["warm"]    = p.at_value(p.mix("cadmium_red", "yellow_ochre", 0.40), 0.50)

# ---- the drawing ----------------------------------------------------------
# wall base: a slope, never a horizontal, and it is meant to get lost mid-way
WALLBASE = [(-0.05, 0.245), (0.38, 0.29), (0.72, 0.335), (1.05, 0.365)]

ROOM  = polygon([(-0.05, -0.05), (1.05, -0.05)] + WALLBASE[::-1])
GLOW  = polygon([(-0.05, 0.10), (1.05, 0.205), (1.05, 0.37)] + WALLBASE[::-1][1:])
# dropped below the wall base, so the block-in's half-brush bleed feathers up to the
# junction instead of chewing a sawtooth out of the glow above it
FLOOR = polygon([(x, y + 0.055) for x, y in WALLBASE] + [(1.05, 1.05), (-0.05, 1.05)])

# the pool: a diamond crossing every band in the picture
pa, pb = (0.02, 0.780), (0.55, 1.08)      # near-left, near-right (off the bottom)
pc, pd = (0.97, 0.615), (0.50, 0.440)     # far-right, far-left
POOL = polygon([pa, pb, pc, pd])

FARWALL  = [pa, pd]          # the pool's far long side — the lamps are in it
FAREND   = [pd, pc]          # the far end wall
NEARSIDE = [pb, pc]          # the near long side — the coping we look over
NEAREND  = [pa, pb]

# ---- the stack, in depth order, so a repair can re-run it ------------------
def room():
    # a sequence of angles, so the roof dark is not a comb of horizontal bars
    s.block_in(ROOM, "bristle", "night", density=0.9, size=0.16,
               direction="cross")

def wallglow():
    # light coming up off the water: passes along the wall base, stepping up and
    # wandering off the line, heavy at the right where the water is brightest and
    # dying to nothing at the left where the pool is far away
    s.sweep(WALLBASE, "bristle", "wall", into=(0.5, 0.05), depth=0.17, size=0.055,
            pressure=[0.05, 0.35, 1.0], opacity=0.5, load=0.85)

def floor():
    s.block_in(FLOOR, "bristle", "deckfar", density=1.0, size=0.15, solid=True,
               opacity=1.0, pressure="even", direction=24)

def water():
    # the deep value first; the light is built on it, not ramped inside it.
    # edge="clean" draws the contour along the pool's own straight edges -- a flat
    # at this size steps them into a staircase otherwise.
    s.block_in(POOL, "flat", "watdeep", size=0.10, solid=True, direction="axis",
               edge="clean", opacity=1.0, pressure="even", note="subject")
