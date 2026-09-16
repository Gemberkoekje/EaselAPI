# Pass 8: the galvanised watering can on the aisle floor. A cool grey thing
# among warm ones: two chisel strokes for the body, the right side turning into
# shadow, the top lit by the sky, spout, rose and handle, a lit edge on the sun
# side, and the one sharp highlight in the picture on its rim.
s.dry()
body, (tx, ty), hw, sy = can_geo()
bx, by = P(CAN["xm"], 0, CAN["dm"])
p["zinc_lit"] = p.at_value("zinc", 0.60)
p["zinc_mid"] = p.at_value("zinc", 0.50)
for c in (-0.45, 0.45):
    s.stroke([(tx + c * hw * 0.92, ty + 0.004), (bx + c * hw, by - 0.002)], "flat", "zinc_mid",
             size=hw * 1.15, opacity=1.0, load=1.0, load_falloff=0.0, pressure="even", note="subject can")
s.stroke([(tx + hw * 0.55, ty + 0.01), (bx + hw * 0.6, by - 0.004)], "round_soft", "zinc_dk",
         size=hw * 0.9, opacity=0.55, pressure=[0.6, 1.0, 0.8], note="subject can")
s.stroke([(tx - hw * 0.6, ty), (tx + hw * 0.6, ty)], "round_hard", "zinc_lit", size=0.02,
         opacity=0.95, pressure="even", note="subject can")
s.stroke([(tx + hw * 0.8, ty + 0.03), (tx + hw * 1.6, ty + 0.002), (tx + hw * 2.3, ty - 0.02)],
         "round_hard", "zinc_mid", size=0.006, opacity=0.95, pressure=[0.7, 1.0, 0.8], note="subject can")
s.dab(tx + hw * 2.35, ty - 0.022, "round_hard", "zinc_dk", size=0.013, press=3, tip_wobble=0.4,
      note="subject can")
s.stroke([(tx - hw * 0.7, ty + 0.002), (tx - hw * 0.2, ty - 0.03), (tx + hw * 0.5, ty - 0.03),
          (tx + hw * 0.9, ty + 0.004)], "round_hard", "zinc_dk", size=0.005, opacity=0.95,
         pressure=[0.3, 1.0, 1.0, 0.3], note="subject can")
s.stroke([(tx - hw * 0.88, ty + 0.006), (bx - hw * 0.95, by - 0.006)], "round_hard", "zinc_lit",
         size=0.005, opacity=0.85, pressure=[1.0, 0.5, 0.15], note="subject can")
s.dab(tx - hw * 0.55, ty + 0.001, "round_hard", "zinc_hi", size=0.009, press=3, note="subject can highlight")
# its shadow on the floor, away from the sun, losing its far end
dx, dy = shadow_dir((bx, by))
p["floor_sh"] = p.at_value("floor", 0.24)
s.stroke([(bx, by - 0.004), (bx + dx * 0.05, by + dy * 0.05), (bx + dx * 0.11, by + dy * 0.11)],
         "round_hard", "floor_sh", size=hw * 1.6, opacity=0.6, pressure=[1.0, 0.7, 0.1],
         note="subject can shadow")
print(s.budget_line())
print(s.look(region="B6:D8"))
