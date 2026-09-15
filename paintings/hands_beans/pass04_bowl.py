# Two cast shadows: a soft darkening, not a comb.
# Then the bowl. Its wall is nearly lost into the table on purpose; the contents
# are a quiet dark pool that individual lit beans will come out of later.
surf = s.sample(span("E5", "G7"))
p["cast"] = p.at_value(surf, p.value_of(surf) - 0.045)

s.stroke([(0.585, 0.735), (0.755, 0.845), (1.010, 0.955)], "bristle", "cast",
         size=0.130, load=1.0, load_falloff=0.30, opacity=0.35, pressure="press_in",
         note="table")
s.stroke([(0.355, 0.880), (0.520, 0.972), (0.690, 1.030)], "bristle", "cast",
         size=0.090, load=1.0, load_falloff=0.35, opacity=0.30, pressure="press_in",
         note="table")

s.paint([
    {"shape": BOWL_OUT, "brush": "bristle", "color": "crock", "size": 0.078,
     "density": 0.95, "direction": ("axis", 34), "solid": True, "note": "bowl"},
    {"shape": BOWL_IN, "brush": "bristle", "color": "bean", "size": 0.062,
     "density": 1.0, "direction": (14, 74), "solid": True, "note": "bowl"},
])
print(s.look(values=True))
print(s.look())
