exec(open("helpers.py").read())
exec(open("pears.py").read())
p = s.palette
p["glow"] = to_value(p.mix(p["window"], p.mix("cadmium_yellow", "titanium_white", 0.75), 0.4), 0.90)
p["curtain_lit"] = to_value(p["curtain"], 0.79)
p["sill_lit"] = to_value(p.mix(p["sill"], "cadmium_yellow", 0.12), 0.72)
for k in ("glow", "curtain_lit", "sill_lit"):
    print(k, p.hex(p[k]), round(p.value_of(p[k]), 2))
s.dry()
# sun through the upper-left of the pane: a few diagonal passes, none the same length
s.stroke([(0.13, 0.02), (0.50, 0.20)], "flat", "glow", size=0.10, opacity=0.55, load=1.0, note="sun in the pane")
s.stroke([(0.30, 0.00), (0.63, 0.15)], "flat", "glow", size=0.08, opacity=0.4, load=1.0, note="sun in the pane")
s.stroke([(0.13, 0.15), (0.43, 0.29)], "flat", "glow", size=0.09, opacity=0.5, load=1.0, note="sun in the pane")
s.stroke([(0.18, 0.27), (0.35, 0.34)], "flat", "glow", size=0.06, opacity=0.45, load=1.0, note="sun in the pane")
# the curtain: three folds that do not match, and its edge catching the sun
s.stroke([(0.795, -0.01), (0.79, 0.25), (0.78, 0.575)], "bristle", "curtain_fold", size=0.032,
         opacity=0.8, pressure=[0.6, 1.0, 0.7], note="fold")
s.stroke([(0.90, 0.10), (0.91, 0.32), (0.895, 0.50)], "bristle", "curtain_fold", size=0.046,
         opacity=0.7, pressure=[0.3, 1.0, 0.4], note="fold, stops short")
s.stroke([(0.955, -0.01), (0.95, 0.30), (0.965, 0.575)], "bristle", "curtain_fold", size=0.024,
         opacity=0.85, pressure=[0.8, 0.6, 0.9], note="fold")
s.stroke([(0.737, 0.0), (0.742, 0.30), (0.733, 0.575)], "round_hard", "curtain_lit", size=0.014,
         pressure=[0.6, 1.0, 0.5], load=1.0, note="curtain edge in the sun")
# the sill where the sun lands, left of the pears
s.stroke([(-0.03, 0.62), (0.27, 0.625)], "flat", "sill_lit", size=0.05, opacity=0.6,
         pressure="lift_off", load=1.0, note="sun on the sill")
s.stroke([(-0.03, 0.705), (0.22, 0.71)], "flat", "sill_lit", size=0.04, opacity=0.5,
         pressure="lift_off", load=1.0, note="sun on the sill")
# shadows: fade the tails, lose the top edge of the mug's
s.glaze([(0.68, 0.71), (0.79, 0.725)], "sill", size=0.06, opacity=0.35, note="mug shadow tail fades")
s.glaze([(0.26, 0.64), (0.30, 0.71)], "sill", size=0.05, opacity=0.4, note="pear 1 shadow, left side lighter")
s.smudge([(0.60, 0.688), (0.72, 0.698)], size=0.03, note="mug shadow top edge, along it")
# the mug's ribs
s.stroke([(0.585, 0.44), (0.583, 0.66)], "round_soft", "mug", size=0.035, opacity=0.6,
         pressure="even", load=1.0, note="mug ribs softened")
# the spray of dots outside the pears, on the pane side
pp1 = lambda d, f, lobe="big": pear_point(PEARS["pear1"], d, f, lobe)
pp2 = lambda d, f, lobe="big": pear_point(PEARS["pear2"], d, f, lobe)
s.stroke([pp1(-70, 1.5, "small"), pp1(-30, 1.5, "small"), pp1(15, 1.5, "small"), pp1(-55, 1.2), pp1(-30, 1.2)],
         "round_hard", "window", size=0.018, pressure="even", load=1.0, jitter=0.0, note="pane up to pear 1")
s.stroke([pp2(-140, 1.5, "small"), pp2(-105, 1.5, "small"), pp2(-70, 1.5, "small")],
         "round_hard", "window", size=0.018, pressure="even", load=1.0, jitter=0.0, note="pane up to pear 2")
print("strokes:", s.stroke_count)
print(s.look())
