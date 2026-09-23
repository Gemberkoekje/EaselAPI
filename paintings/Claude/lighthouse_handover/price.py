import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import load
s, ns = load()
headland, cliff_face, lit_slope, grass_cap, TOP_EDGE = (ns[k] for k in ("headland", "cliff_face", "lit_slope", "grass_cap", "TOP_EDGE"))
plans = {
 "mass 0.05 TOP_EDGE": {"shape": headland, "brush": "flat", "color": "land", "size": 0.05, "solid": True, "direction": TOP_EDGE, "edge": "clean"},
 "mass 0.07 TOP_EDGE": {"shape": headland, "brush": "flat", "color": "land", "size": 0.07, "solid": True, "direction": TOP_EDGE, "edge": "clean"},
 "mass 0.07 axis":     {"shape": headland, "brush": "flat", "color": "land", "size": 0.07, "solid": True, "direction": "axis", "edge": "clean"},
 "cliff 0.022":        {"shape": cliff_face, "brush": "flat", "color": "cliff", "size": 0.022, "solid": True, "direction": ((0.97, 0.70), (0.90, 0.79)), "edge": "clean"},
 "cliff 0.03 axis":    {"shape": cliff_face, "brush": "flat", "color": "cliff", "size": 0.03, "solid": True, "direction": "axis", "edge": "clean"},
 "lit 0.014":          {"shape": lit_slope, "brush": "flat", "color": "lit", "size": 0.014, "solid": True, "direction": ((0.412, 0.628), (0.635, 0.544)), "edge": "clean"},
}
for k, plan in plans.items():
    print(f"{k:22s}", s.cost_line(plan).replace("\n", " | "))
