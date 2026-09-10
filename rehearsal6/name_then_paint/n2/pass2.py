p = s.palette
p["haze"]    = p.mix("titanium_white", "cerulean", 0.13)                 # ~0.85
p["haze_lo"] = p.mix(p.mix("titanium_white","cerulean",0.17), "viridian", 0.07)
p["glow_top"]= p.mix("titanium_white", "yellow_ochre", 0.06)
print("haze", p.hex(p["haze"]), round(p.value_of(p["haze"]),2),
      "haze_lo", p.hex(p["haze_lo"]), round(p.value_of(p["haze_lo"]),2))

s.dry()
# knock the outside back into haze - broken, so some of it still shows
outside = polygon([(-0.09, 0.430), (0.575, 0.452), (0.570, 0.700), (-0.09, 0.720)])
s.block_in(outside, "flat", "haze",    density=0.55, size=0.062, direction=(11, 99), load=1.0)
s.block_in(blob((0.22,0.585), 0.30, 0.075, wobble=0.5, seed=6), "flat", "haze_lo",
           density=0.5, size=0.05, direction=(-14, 78), load=0.85)
s.smudge([(0.04, 0.470), (0.27, 0.462)], size=0.042)
s.smudge([(0.27, 0.462), (0.52, 0.478)], size=0.038)
s.smudge([(0.12, 0.640), (0.34, 0.628)], size=0.040)
# light strongest where it enters, upper left
s.block_in(blob((0.16,0.145), 0.26, 0.14, wobble=0.4, seed=3), "flat", "glow_top",
           density=0.6, size=0.07, direction=(24, 112), load=0.9)
s.smudge([(0.07, 0.280), (0.33, 0.292)], size=0.040)

# --- 2. the interior wall: nearer than the window, so it cuts the aperture ---
right_wall = polygon([(0.484,-0.09), (1.12,-0.09), (1.12,0.80), (0.468,0.74)])
top_band   = polygon([(-0.10,-0.09), (1.12,-0.09), (1.12,0.148), (0.50,0.118),
                      (0.05,0.094), (-0.10,0.120)])
left_jamb  = polygon([(-0.10,0.00), (0.056,0.055), (0.048,0.75), (-0.10,0.75)])

s.block_in(right_wall.inset(0.058), "bristle", "wall", density=0.9, size=0.11,
           direction=(68, 152), load=1.0)
s.block_in(top_band.inset(0.032), "bristle", "wall", density=0.9, size=0.062,
           direction=(-7, 82), load=1.0)
s.block_in(left_jamb.inset(0.022), "flat", "wall", density=0.95, size=0.042,
           direction=82, load=1.0)
print("strokes:", s.stroke_count)
