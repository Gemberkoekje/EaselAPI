# Tidal Sky -- golden-hour coastal scene
# Why this subject: the whole picture is one light -- a low sun's amber/coral reflection
# running unbroken from sky to water -- and the boat is the one dark thing standing in it.

p = s.palette

# -- golden-hour mixtures (mixed to values, not ratios) --
p["peach"]      = p.at_value(p.mix("cadmium_yellow", "cadmium_red", 0.25), 0.80)
p["coral"]      = p.at_value(p.mix("cadmium_red", "alizarin", 0.35), 0.62)
p["amber"]      = p.at_value(p.mix("yellow_ochre", "cadmium_red", 0.30), 0.52)
p["gold"]       = p.at_value(p.mix("cadmium_yellow", "titanium_white", 0.60), 0.88)
p["water_amber"]= p.at_value(p.mix("yellow_ochre", "burnt_umber", 0.35), 0.48)
p["water_coral"]= p.at_value(p.mix("cadmium_red", "burnt_umber", 0.40), 0.44)
p["teal"]       = p.at_value(p.mix("cerulean", "burnt_umber", 0.45), 0.33)
p["teal_deep"]  = p.at_value(p.mix("cerulean", "burnt_umber", 0.60), 0.23)
p["boat_dark"]  = p.mix("ultramarine", "burnt_umber", 0.45)     # the darkest thing in the box
p["cloud_pale"] = p.at_value(p.mix("titanium_white", "cadmium_yellow", 0.12), 0.90)

# -- landmarks, verified points --
s.mark("sun",   0.30, 0.43)
s.mark("bow",   0.51, 0.575)
s.mark("stern", 0.755, 0.555)

# -- the masses, each in its own function so a repair is one re-run --
HORIZON = 0.52

def boat_shape():
    return polygon([s.pt("bow"), (0.63, 0.567), s.pt("stern"),
                    (0.745, 0.578), (0.63, 0.594), (0.535, 0.596)])

def sky_mass():
    s.scumble(polygon([(-0.06, -0.06), (1.06, -0.06), (1.06, 0.30), (-0.06, 0.30)]),
              "peach", "coral", 7, direction=4, load=1.0, load_falloff=0.0, opacity=0.95)

def sky_low_mass():
    s.scumble(polygon([(-0.06, 0.26), (1.06, 0.26), (1.06, 0.545), (-0.06, 0.545)]),
              "coral", "amber", 7, direction=3, load=1.0, load_falloff=0.0, opacity=0.95)

def water_mass():
    s.scumble(polygon([(-0.06, 0.50), (1.06, 0.50), (1.06, 0.80), (-0.06, 0.80)]),
              "water_coral", "teal", 8, direction=2, load=1.0, load_falloff=0.0, opacity=0.95)

def water_near_mass():
    s.scumble(polygon([(-0.06, 0.76), (1.06, 0.76), (1.06, 1.06), (-0.06, 1.06)]),
              "teal", "teal_deep", 6, direction=3, load=1.0, load_falloff=0.0, opacity=0.95)
