# The distance: hedge on the horizon, then the frozen ground running toward me.
# round_hard for the field -- bristle combed it, flat terraced it, and a round tip
# declares no axis. Frost lying in the hollows is what crosses it.
from easel import Region, ellipse

p["hedge"]   = p.at_value(p.mix(p["neutral"], "burnt_umber", 0.28), 0.59)
p["hedgedk"] = p.at_value(p.mix(p["neutral"], "burnt_umber", 0.42), 0.43)
p["yardfar"] = p.at_value(p.mix(p["neutral"], "yellow_ochre", 0.15), 0.55)
p["yardmid"] = p.at_value(p.mix(p["neutral"], "yellow_ochre", 0.22), 0.46)
p["yardnr"]  = p.at_value(p.mix(p["neutral"], "burnt_umber", 0.26), 0.38)
p["frost"]   = p.at_value(p.mix(p["neutral"], "titanium_white", 0.40), 0.66)

s.scumble(Region(-0.04, 0.452, 1.04, 0.70), "yardfar", "yardmid", 7, brush="round_hard",
          direction=-6, size=0.078, load=1.0, load_falloff=0.0, opacity=0.95,
          pressure="even", note="dist")
s.scumble(Region(-0.04, 0.64, 1.04, 1.04), "yardmid", "yardnr", 8, brush="round_hard",
          direction=5, size=0.092, load=1.0, load_falloff=0.0, opacity=0.95,
          pressure="even", note="dist")

# the hedge: long and thin, so it is strokes, not a mass -- and its top is lost
s.stroke([(-0.06, 0.470), (0.075, 0.462), (0.185, 0.468), (0.266, 0.461)],
         "bristle", "hedge", size=0.030, load=0.55, opacity=0.70,
         pressure=[0.9, 1.0, 0.7, 0.35], note="dist")
s.stroke([(0.244, 0.472), (0.140, 0.480), (0.020, 0.474), (-0.06, 0.481)],
         "bristle", "hedge", size=0.022, load=0.40, opacity=0.50,
         pressure=[0.5, 1.0, 0.8, 0.4], note="dist")
s.dab(0.050, 0.462, "round_hard", "hedgedk", size=0.013, press=3, tip_wobble=0.7, note="dist")
s.dab(0.166, 0.467, "round_hard", "hedgedk", size=0.009, press=2, tip_wobble=0.7, note="dist")

# frost in the hollows: a starved brush on rough canvas is speckle, which is the
# thing itself -- and a patch of it is a broken stroke, not an eleven-stroke mass
s.stroke([(-0.06, 0.870), (0.085, 0.836), (0.225, 0.858)], "bristle", "frost",
         size=0.052, load=0.28, load_falloff=0.12, opacity=0.80,
         pressure=[0.6, 1.0, 0.4], note="dist")
s.stroke([(0.235, 0.905), (0.105, 0.930), (-0.04, 0.912)], "bristle", "frost",
         size=0.038, load=0.22, load_falloff=0.10, opacity=0.75,
         pressure=[0.4, 0.9, 0.5], note="dist")
s.stroke([(0.205, 0.694), (0.320, 0.706), (0.408, 0.690)], "bristle", "frost",
         size=0.030, load=0.22, load_falloff=0.10, opacity=0.72,
         pressure=[0.8, 1.0, 0.3], note="dist")
s.stroke([(0.095, 0.606), (0.196, 0.617), (0.262, 0.605)], "bristle", "frost",
         size=0.022, load=0.18, load_falloff=0.08, opacity=0.65,
         pressure=[0.5, 1.0, 0.2], note="dist")

# frozen ruts toward the vanishing point -- crossers, none parallel
s.stroke([(-0.06, 0.96), (0.15, 0.760), (0.256, 0.588)], "bristle", "yardnr",
         size=0.036, load=0.42, opacity=0.45, pressure="swell", note="dist")
s.stroke([(0.29, 1.03), (0.352, 0.850), (0.392, 0.730)], "bristle", "yardnr",
         size=0.042, load=0.38, opacity=0.42, pressure="swell", note="dist")
s.stroke([(-0.06, 0.660), (0.120, 0.612), (0.252, 0.566)], "bristle", "yardfar",
         size=0.026, load=0.35, opacity=0.36, pressure="lift_off", note="dist")
