# pass 3 -- the phosphor: scrollback dim above, working lines bright, one cursor accent
# lines follow the screen's tilt (top edge rises to the right)
tilt = -0.0272

def tx(x0, x1, y0):
    return [(x0, y0 - (x0 - 0.345) * tilt), (0.5 * (x0 + x1), y0 - (0.5 * (x0 + x1) - 0.345) * tilt),
            (x1, y0 - (x1 - 0.345) * tilt)]

lines = []
y = 0.245
for ln in [0.10, 0.14, 0.07, 0.16, 0.09]:          # dim scrollback, ragged lengths
    lines.append({"points": tx(0.345, 0.345 + ln, y), "brush": "liner",
                  "color": p["phos_dim"], "size": 0.006, "note": "subject"})
    y += 0.022
y += 0.014                                          # a gap: one command ran
for i, ln in enumerate([0.18, 0.11]):               # its output, brighter
    lines.append({"points": tx(0.345, 0.345 + ln, y), "brush": "liner",
                  "color": p["phos"], "size": 0.0065, "note": "subject"})
    y += 0.022
lines.append({"points": tx(0.368, 0.368 + 0.08, y), "brush": "liner",   # an indented echo
              "color": p["phos_dim"], "size": 0.0055, "note": "subject"})
y += 0.024
prompt_y = y
lines.append({"points": tx(0.345, 0.345 + 0.055, y), "brush": "liner",  # the prompt itself
              "color": p["phos"], "size": 0.0075, "note": "subject"})

s.paint(lines)
cx, cy = 0.412, prompt_y - (0.412 - 0.345) * tilt
s.dab(cx, cy, "round_hard", p["cursor"], size=0.011,
      press=3, tip_wobble=0.7, note="subject")      # the cursor, waiting
s.look(region=span("C2", "F5"))
