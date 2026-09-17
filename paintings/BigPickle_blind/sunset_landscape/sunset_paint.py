"""Landscape with mountains at sunset."""
from easel import Session, polygon, blob, span, cell, region

s = Session(1200, 800, texture="linen", ground="toned_grey", seed=42, budget=120)

# Mix palette colours
s.palette["sky_top"] = s.palette.mix("ultramarine", "cerulean", 0.4)
s.palette["sky_mid"] = s.palette.mix("yellow_ochre", "cadmium_red", 0.35)
s.palette["sky_low"] = s.palette.mix("cadmium_red", "yellow_ochre", 0.3)
s.palette["sun"] = s.palette.tint("cadmium_yellow", 0.7)
s.palette["mountain_dark"] = s.palette.mix("ultramarine", "burnt_umber", 0.55)
s.palette["mountain_mid"] = s.palette.mix("ultramarine", "burnt_umber", 0.4)
s.palette["mountain_light"] = s.palette.mix("yellow_ochre", "burnt_sienna", 0.4)
s.palette["ground"] = s.palette.mix("burnt_umber", "ultramarine", 0.3)
s.palette["ground_light"] = s.palette.mix("yellow_ochre", "burnt_sienna", 0.5)
s.palette["highlight"] = s.palette.tint("cadmium_yellow", 0.6)

# 1. Graphite drawing - outline the main shapes
horizon_y = 0.55

# Far mountains (background)
far_mtn = polygon([
    (-0.05, horizon_y), (0.12, 0.32), (0.25, 0.28), (0.38, 0.35),
    (0.50, 0.22), (0.62, 0.30), (0.75, 0.25), (0.88, 0.33),
    (1.05, horizon_y)
])

# Near mountains (midground)
near_mtn = polygon([
    (-0.05, horizon_y), (0.08, 0.40), (0.22, 0.36), (0.35, 0.42),
    (0.48, 0.34), (0.58, 0.38), (0.72, 0.35), (0.85, 0.41),
    (1.05, horizon_y)
])

# Foreground hills
fg_hill = polygon([
    (-0.05, horizon_y), (0.10, 0.50), (0.25, 0.48), (0.40, 0.52),
    (0.55, 0.46), (0.70, 0.50), (0.85, 0.47), (1.05, horizon_y)
])

# Draw outlines
s.pencil(far_mtn.closed, pressure=0.5, smooth=False, note="far mountain outline")
s.pencil(near_mtn.closed, pressure=0.5, smooth=False, note="near mountain outline")
s.pencil(fg_hill.closed, pressure=0.5, smooth=False, note="foreground hill outline")
s.look(grid=True)

# 2. Sky - graded field (back to front: sky first)
# Upper sky: deep blue
upper_sky = polygon([(-0.05, -0.05), (1.05, -0.05), (1.05, 0.35), (-0.05, 0.35)])
s.scumble(upper_sky, "sky_top", "sky_mid", 6, direction=4,
          load=1.0, load_falloff=0.0, opacity=0.95)

# Lower sky: warm sunset glow
lower_sky = polygon([(-0.05, 0.25), (1.05, 0.22), (1.05, 0.55), (-0.05, 0.58)])
s.scumble(lower_sky, "sky_mid", "sky_low", 7, direction=3,
          load=1.0, load_falloff=0.0, opacity=0.95)

# Horizon glow
horizon_glow = polygon([(-0.05, 0.45), (1.05, 0.42), (1.05, 0.58), (-0.05, 0.60)])
s.scumble(horizon_glow, "sky_low", "sun", 5, direction=2,
          load=1.0, load_falloff=0.0, opacity=0.90)

# Cross strokes for sky texture
s.stroke([(-0.05, 0.18), (0.40, 0.22), (1.05, 0.15)], "bristle", "sky_top",
         size=0.065, load=0.40, opacity=0.35, pressure="swell")
s.stroke([(1.05, 0.35), (0.55, 0.38), (-0.05, 0.32)], "bristle", "sky_mid",
         size=0.055, load=0.35, opacity=0.30, pressure="swell")

s.look(values=True)

# 3. Far mountains (background)
s.block_in(far_mtn, "bristle", "mountain_dark", density=0.85, size=0.12,
           direction="axis", note="far mountain mass")
s.look(values=True)

# 4. Near mountains (midground)
s.block_in(near_mtn, "bristle", "mountain_mid", density=0.80, size=0.10,
           direction=-15, note="near mountain mass")

# Add some warmth to sun-facing slopes
sun_face = polygon([
    (0.45, horizon_y), (0.50, 0.22), (0.60, 0.30), (0.72, 0.25),
    (0.80, 0.30), (0.85, horizon_y)
])
s.block_in(sun_face, "bristle", "mountain_light", density=0.5, size=0.08,
           direction=20, edge="hard", note="sun-lit mountain slope")

s.look(values=True)

# 5. Foreground
s.block_in(fg_hill, "bristle", "ground", density=0.85, size=0.10,
           direction="axis", note="foreground mass")

# Light on foreground
fg_light = polygon([
    (0.30, horizon_y), (0.45, 0.48), (0.60, 0.46), (0.75, 0.50),
    (0.80, horizon_y)
])
s.block_in(fg_light, "bristle", "ground_light", density=0.5, size=0.07,
           direction=10, edge="hard", note="foreground light")

s.look(values=True)

# 6. Sun - bright accent
s.dab(0.50, 0.38, brush="round_hard", color="sun", size=0.04, press=3,
      note="sun")

# Sun glow
s.stroke([(0.42, 0.40), (0.50, 0.38), (0.58, 0.40)], "round_soft", "sun",
         size=0.06, opacity=0.4, pressure="taper", note="sun glow")

s.look(values=True)

# 7. Edge work - soften mountain ridgelines
s.smudge([(0.48, 0.22), (0.55, 0.26)], size=0.025, note="soften far ridge")
s.smudge([(0.46, 0.34), (0.52, 0.36)], size=0.020, note="soften near ridge")

# 8. Highlights - small, deliberate marks
# Catch light on water (implied) or ground
s.dab(0.35, 0.52, brush="round_hard", color="highlight", size=0.008, press=2,
      note="ground highlight")
s.dab(0.65, 0.50, brush="round_hard", color="highlight", size=0.006, press=2,
      note="ground highlight 2")

# Warm edge light on foreground
s.stroke([(0.20, 0.53), (0.40, 0.50), (0.60, 0.52)], "bristle", "highlight",
         size=0.03, load=0.3, opacity=0.3, pressure="taper",
         note="warm edge light")

s.look(values=True)

# 9. Final look and export
s.look(grid=True)
s.export("sunset_landscape.png")
print(f"Painting complete: {s.budget_line()}")
