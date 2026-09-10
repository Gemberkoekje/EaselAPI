# Pass 11 - the pot again, keeping the chroma: broken bristle over a solid mid.
p = s.palette
t = p.mix("burnt_sienna", "cadmium_red", 0.32)
p["terra_mid"]  = p.mix(t, "yellow_ochre", 0.20)
p["terra_lit"]  = p.tint(p.mix(t, "yellow_ochre", 0.65), 0.18)
p["terra_hi"]   = p.tint(p.mix(t, "cadmium_yellow", 0.45), 0.30)
p["terra_sh"]   = p.mix(t, "ultramarine", 0.42)
p["terra_refl"] = p.mix(p.mix(t, "ultramarine", 0.45), "burnt_sienna", 0.55)
p["crack"]      = p.mix(p.mix(t, "ultramarine", 0.5), "burnt_umber", 0.55)
s.dry()

body = polygon([(0.324,0.676),(0.418,0.690),(0.512,0.684),(0.498,0.782),(0.482,0.866),
                (0.440,0.880),(0.396,0.879),(0.352,0.860),(0.336,0.780)])
s.block_in(body.inset(0.020), "flat", "terra_mid", direction=(11, 169), density=1.0,
           size=0.040, load=1.0, pressure="even")

lit = polygon([(0.330,0.684),(0.404,0.696),(0.398,0.790),(0.392,0.868),(0.352,0.856),
               (0.338,0.774)])
s.block_in(lit.inset(0.013), "bristle", "terra_lit", direction=(78, 14), density=0.75,
           size=0.026, load=0.75)
sh = polygon([(0.442,0.694),(0.512,0.684),(0.498,0.782),(0.482,0.864),(0.440,0.876),
              (0.442,0.786)])
s.block_in(sh.inset(0.013), "bristle", "terra_sh", direction=(84, 20), density=0.8,
           size=0.026, load=0.8)

# reflected light up the shadow edge, and marks that run round the form
s.stroke([(0.504,0.706),(0.496,0.782),(0.484,0.850)], "bristle", "terra_refl",
         size=0.011, pressure=[0.35,1.0,0.75], load=0.9)
s.stroke([(0.342,0.720),(0.404,0.734),(0.462,0.730)], "bristle", "terra_mid",
         size=0.014, pressure="taper", load=0.65)
s.stroke([(0.348,0.828),(0.412,0.848),(0.470,0.840)], "bristle",
         p.mix(p["terra_mid"], p["terra_lit"], 0.45), size=0.017, pressure="taper", load=0.7)
s.stroke([(0.368,0.770),(0.430,0.782)], "bristle", p.mix(p["terra_mid"],"yellow_ochre",0.3),
         size=0.010, pressure="taper", load=0.55)

# --- the rim: far lip, the inside, the near lip -------------------------------
s.stroke([(0.320,0.668),(0.362,0.648),(0.418,0.642),(0.474,0.648),(0.516,0.668)],
         "flat", "terra_lit", size=0.017, pressure="even", load=1.0)
s.block_in(ellipse(Region(0.332, 0.650, 0.502, 0.690)).inset(0.008), "flat", "pot_in",
           direction=(6, 174), density=1.0, size=0.016, load=1.0, pressure="even")
s.stroke([(0.344,0.658),(0.400,0.652),(0.462,0.656)], "round_hard",
         p.mix(p["pot_in"], "burnt_sienna", 0.30), size=0.008, pressure=[0.4,0.9,0.4])
s.stroke([(0.320,0.672),(0.366,0.694),(0.418,0.700),(0.470,0.694),(0.514,0.674)],
         "flat", "terra_lit", size=0.019, pressure="even", load=1.0)
s.stroke([(0.328,0.670),(0.372,0.690),(0.420,0.696)], "round_hard", "terra_hi",
         size=0.007, pressure=[0.5,1.0,0.3])
s.stroke([(0.334,0.688),(0.386,0.710),(0.440,0.714),(0.492,0.704)], "round_hard",
         "terra_sh", size=0.007, pressure=[0.3,0.9,0.9,0.4])

# --- the crack ----------------------------------------------------------------
s.stroke([(0.366,0.702),(0.379,0.744),(0.370,0.788),(0.383,0.828),(0.380,0.860)],
         "round_hard", "crack", size=0.0055, pressure=[1.0,0.9,1.0,0.7,0.35])
s.stroke([(0.361,0.706),(0.374,0.746),(0.365,0.786)], "round_hard", "terra_hi",
         size=0.0035, pressure=[0.7,0.5,0.25])
s.stroke([(0.372,0.760),(0.390,0.784)], "round_hard", "crack",
         size=0.004, pressure=[0.8,0.2])

# --- cut the silhouette back ---------------------------------------------------
s.stroke([(0.310,0.694),(0.318,0.772),(0.334,0.856)], "flat", "bg", size=0.026,
         pressure="even", load=1.0)
s.stroke([(0.526,0.688),(0.516,0.762),(0.500,0.842)], "flat", "cast", size=0.026,
         pressure="even", load=1.0)
s.stroke([(0.350,0.890),(0.420,0.900),(0.490,0.886)], "flat", "cast", size=0.024,
         pressure="even", load=1.0)
s.stroke([(0.356,0.874),(0.418,0.884),(0.478,0.874)], "round_hard",
         p.mix(p["cast"], "burnt_umber", 0.5), size=0.012, pressure=[0.6,1.0,0.5])

print("strokes:", s.stroke_count)
print(s.look(region=span("C5","F8"), sketch=False))
