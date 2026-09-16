"""
Misty Pine Forest at Dawn
A fine art oil painting rendered with Easel (easel-paint).
Depicting a misty pine forest at dawn, with golden sunlight breaking
through the fog onto a still, glassy lake.
"""

import math
import random
import time
from pathlib import Path
import easel
from easel import Region, polygon, span

def paint():
    t_start = time.time()
    print("Beginning creation of 'Misty Pine Forest at Dawn'...")

    # Session: 1024x768 on fine linen with toned warm grey ground
    s = easel.Session(
        width=1024,
        height=768,
        texture="linen",
        ground="toned_warm_grey",
        seed=42,
        timelapse=True
    )
    p = s.palette

    # -------------------------------------------------------------
    # 1. PALETTE DEFINITIONS (harmonized tonal values)
    # -------------------------------------------------------------
    print("Mixing pigments and harmonizing values...")
    # Deepest tonal anchor
    p["dark"] = p.mix("ultramarine", "burnt_umber", 0.50)

    # Dawn Sky
    p["sky_zenith"]  = p.at_value(p.mix(p.mix("cerulean", "ultramarine", 0.4), "burnt_umber", 0.35), 0.28)
    p["sky_slate"]   = p.at_value(p.mix("cerulean", "burnt_umber", 0.30), 0.42)
    p["sky_rose"]    = p.at_value(p.mix(p.mix("alizarin", "yellow_ochre", 0.35), "titanium_white", 0.45), 0.56)
    p["sky_apricot"] = p.at_value(p.mix("cadmium_red", "cadmium_yellow", 0.65), 0.70)
    p["sky_amber"]   = p.at_value(p.mix("cadmium_yellow", "yellow_ochre", 0.35), 0.80)
    p["sun_gold"]    = p.at_value(p.mix("cadmium_yellow", "titanium_white", 0.45), 0.90)
    p["sun_core"]    = "titanium_white"

    # Morning Mist & Glow
    p["mist_warm"]   = p.at_value(p.mix("yellow_ochre", "titanium_white", 0.85), 0.82)
    p["mist_cool"]   = p.at_value(p.mix("cerulean", "titanium_white", 0.75), 0.72)
    p["mist_pale"]   = p.at_value("titanium_white", 0.91)

    # Distant Mountains & Ridge
    p["ridge_far"]   = p.at_value(p.mix("ultramarine", "burnt_umber", 0.45), 0.46)
    p["ridge_mid"]   = p.at_value(p.mix("viridian", "burnt_umber", 0.55), 0.34)
    p["ridge_pines"] = p.at_value(p.mix("viridian", "burnt_umber", 0.65), 0.25)

    # Lake Water
    p["lake_horizon"]= p.at_value(p.mix("yellow_ochre", "burnt_umber", 0.32), 0.62)
    p["lake_mid"]    = p.at_value(p.mix("cerulean", "burnt_umber", 0.55), 0.26)
    p["lake_deep"]   = p.at_value(p.mix("ultramarine", "burnt_umber", 0.65), 0.14)
    p["lake_sky"]    = p.at_value(p.mix("cerulean", "titanium_white", 0.45), 0.45)

    # Pine Trees
    p["pine_deep"]   = p.mix("viridian", "burnt_umber", 0.70)
    p["pine_dark"]   = p.at_value(p.mix("viridian", "burnt_umber", 0.55), 0.18)
    p["pine_body"]   = p.at_value(p.mix("viridian", "yellow_ochre", 0.35), 0.24)
    p["pine_rim"]    = p.at_value(p.mix("yellow_ochre", "cadmium_yellow", 0.60), 0.68)
    p["pine_spark"]  = p.at_value("cadmium_yellow", 0.88)
    p["bark_dark"]   = p.at_value(p.mix("burnt_sienna", "burnt_umber", 0.65), 0.18)
    p["bark_lit"]    = p.at_value(p.mix("burnt_sienna", "yellow_ochre", 0.45), 0.42)

    # Shoreline & Rocks
    p["rock_dark"]   = p.mix("burnt_umber", "dark", 0.4)
    p["rock_plane"]  = p.at_value(p.mix("dark", "titanium_white", 0.30), 0.28)
    p["moss"]        = p.at_value(p.mix("viridian", "yellow_ochre", 0.55), 0.22)

    # Landmarks
    s.mark("sun", 0.66, 0.42)
    s.mark("horizon", 0.0, 0.52)

    # -------------------------------------------------------------
    # 2. GRAPHITE UNDERDRAWING
    # -------------------------------------------------------------
    print("Pass 1: Graphite underdrawing...")
    s.pencil([(0.0, 0.52), (1.0, 0.52)], pressure=0.35)
    s.pencil([(0.30, 0.52), (0.48, 0.47), (0.65, 0.44), (0.82, 0.45), (1.0, 0.48)], pressure=0.25)
    s.pencil([(0.0, 0.68), (0.14, 0.71), (0.24, 0.76), (0.32, 0.84), (0.28, 0.95), (0.0, 1.0)], pressure=0.40)
    # Tree trunks guides
    s.pencil([(0.11, 0.74), (0.10, 0.07)], pressure=0.35)
    s.pencil([(0.20, 0.73), (0.21, 0.13)], pressure=0.30)
    s.pencil([(0.04, 0.78), (0.02, 0.18)], pressure=0.30)

    # -------------------------------------------------------------
    # 3. UNDER-MASSES (Value Foundation)
    # -------------------------------------------------------------
    print("Pass 2: Foundational under-masses...")
    s.block_in(easel.region("upper-half"), "bristle", "sky_rose", density=0.75, size=0.20, direction="axis")
    s.block_in(easel.region("lower-half"), "bristle", "lake_mid", density=0.75, size=0.20, direction="axis")

    # -------------------------------------------------------------
    # 4. GRADED FIELDS (Sky & Lake)
    # -------------------------------------------------------------
    print("Pass 3: Graded atmospheric fields...")
    # Sky: zenith to rose
    s.scumble(
        polygon([(-0.06, -0.06), (1.06, -0.06), (1.06, 0.32), (-0.06, 0.32)]),
        "sky_zenith", "sky_rose",
        n=8, direction=3, load=1.0, load_falloff=0.0, opacity=0.95
    )
    # Sky: rose to radiant sunrise amber
    s.scumble(
        polygon([(-0.06, 0.26), (1.06, 0.26), (1.06, 0.545), (-0.06, 0.545)]),
        "sky_rose", "sky_amber",
        n=8, direction=4, load=1.0, load_falloff=0.0, opacity=0.95
    )

    # Lake: horizon to mid-lake
    s.scumble(
        polygon([(-0.06, 0.505), (1.06, 0.505), (1.06, 0.78), (-0.06, 0.78)]),
        "lake_horizon", "lake_mid",
        n=8, direction=2, load=1.0, load_falloff=0.0, opacity=0.95
    )
    # Lake: mid-lake to deep foreground
    s.scumble(
        polygon([(-0.06, 0.74), (1.06, 0.74), (1.06, 1.06), (-0.06, 1.06)]),
        "lake_mid", "lake_deep",
        n=7, direction=3, load=1.0, load_falloff=0.0, opacity=0.95
    )

    # Soft high morning clouds
    s.stroke([(0.10, 0.15), (0.32, 0.17), (0.50, 0.14)], "bristle", "mist_pale",
             size=0.022, load=0.30, opacity=0.35, pressure="swell")
    s.stroke([(0.52, 0.21), (0.74, 0.18), (0.92, 0.21)], "bristle", "mist_pale",
             size=0.018, load=0.25, opacity=0.30, pressure="swell")

    # -------------------------------------------------------------
    # 5. DISTANT MOUNTAINS & VALLEY FOG
    # -------------------------------------------------------------
    print("Pass 4: Distant ridges and valley fog...")
    # Far mountain ridge
    mtn_far = polygon([
        (0.28, 0.52), (0.40, 0.485), (0.52, 0.455), (0.66, 0.435),
        (0.80, 0.460), (0.92, 0.445), (1.05, 0.470), (1.05, 0.52), (0.28, 0.52)
    ])
    s.block_in(mtn_far, brush="flat", color="ridge_far", size=0.040, density=1.0, opacity=0.75)

    # Valley mist between ridges
    s.stroke([(0.30, 0.505), (1.05, 0.505)], "round_soft", "mist_warm", size=0.055, opacity=0.50)

    # Mid-ground ridge on the far right shore
    mtn_mid = polygon([
        (0.44, 0.52), (0.56, 0.490), (0.70, 0.470), (0.84, 0.475),
        (1.05, 0.495), (1.05, 0.52), (0.44, 0.52)
    ])
    s.block_in(mtn_mid, brush="flat", color="ridge_mid", size=0.035, density=1.0, opacity=0.80)

    # Distant pine forest silhouette along the mid-ridge crest (continuous organic mass)
    s.stroke([(0.46, 0.495), (0.60, 0.485), (0.75, 0.472), (0.90, 0.480), (1.05, 0.495)],
             brush="bristle", color="ridge_pines", size=0.022, opacity=0.85)

    # Distant forest reflection in the water
    s.stroke([(0.48, 0.525), (0.65, 0.528), (0.82, 0.526), (1.02, 0.527)],
             brush="flat", color="ridge_pines", size=0.016, opacity=0.35)

    # Soft rolling mist bank along the shoreline and valley
    s.dry()
    s.stroke([(0.25, 0.518), (1.05, 0.518)], "round_soft", "mist_warm", size=0.038, opacity=0.55)
    s.stroke([(0.38, 0.523), (0.95, 0.523)], "round_soft", "mist_pale", size=0.024, opacity=0.50)

    # -------------------------------------------------------------
    # 6. SUN HALO, MORNING GLOW & VOLUMETRIC LIGHT
    # -------------------------------------------------------------
    print("Pass 5: Sun halo, morning glow and atmospheric light shafts...")
    sun_pt = s.pt("sun")

    # Atmosphere around the sun
    s.dry()
    # Broad circular warmth
    s.dab(sun_pt[0], sun_pt[1], "round_soft", "sun_gold", size=0.18, press=2, opacity=0.25)
    s.dab(sun_pt[0], sun_pt[1], "round_soft", "sun_gold", size=0.10, press=2, opacity=0.40)

    # Soft diagonal light shafts through misty atmosphere
    for target_pt, sz, op in [
        ((0.20, 0.62), 0.10, 0.12),
        ((0.32, 0.68), 0.12, 0.14),
        ((0.46, 0.74), 0.11, 0.14),
        ((0.58, 0.66), 0.09, 0.12),
    ]:
        s.glaze([sun_pt, target_pt], "mist_warm", opacity=op, size=sz, pressure=[0.8, 0.4])

    # Dawn light spilling into the water across the horizon
    s.glaze([sun_pt, (sun_pt[0], 0.52), (sun_pt[0], 0.60)], "sun_gold", opacity=0.18, size=0.10,
            pressure=[1.0, 0.8, 0.3])

    # The rising Sun Disc
    s.dry()
    s.dab(*sun_pt, brush="round_hard", color="sun_gold", size=0.068, press=3, tip_wobble=0.15)
    s.dab(*sun_pt, brush="round_soft", color="sun_core", size=0.040, press=2)

    # Soft wisp of morning mist crossing the lower edge of the sun
    s.stroke([(sun_pt[0] - 0.07, sun_pt[1] + 0.016), (sun_pt[0] + 0.07, sun_pt[1] + 0.012)],
             "round_soft", "mist_warm", size=0.020, opacity=0.45, glaze=True)

    # -------------------------------------------------------------
    # 7. GLASSY LAKE: SHIMMERING GLITTER PATH & REFLECTIONS
    # -------------------------------------------------------------
    print("Pass 6: Shimmering water reflections and broken flashes...")
    s.dry()

    # Broken horizontal flashes for the sun's reflection (the glitter path)
    # Using brush sizes >= 0.006 to ensure optimal paint deposition
    rng = random.Random(555)
    glitter_rows = [
        (0.528, 0.045, 0.88, 0.007, 6),
        (0.542, 0.055, 0.82, 0.007, 7),
        (0.560, 0.070, 0.75, 0.007, 7),
        (0.582, 0.085, 0.68, 0.008, 8),
        (0.610, 0.105, 0.60, 0.008, 8),
        (0.645, 0.125, 0.52, 0.008, 7),
        (0.690, 0.145, 0.44, 0.009, 6),
        (0.745, 0.170, 0.35, 0.009, 5),
        (0.810, 0.195, 0.28, 0.010, 4),
        (0.885, 0.225, 0.20, 0.010, 4),
    ]

    for y, total_w, base_op, stroke_sz, num_flashes in glitter_rows:
        # Subtle warm background glow under the ripples
        s.stroke(
            [(sun_pt[0] - total_w * 0.7, y), (sun_pt[0] + total_w * 0.7, y)],
            "round_soft", "sun_gold", size=stroke_sz * 3, opacity=base_op * 0.30, glaze=True
        )
        # Broken discrete flashes across this row
        for _ in range(num_flashes):
            fx = sun_pt[0] + rng.gauss(0, total_w * 0.38)
            flen = rng.uniform(0.018, 0.048)
            f_op = base_op * rng.uniform(0.80, 1.15)
            # Golden ripple
            s.stroke(
                [(fx - flen/2, y), (fx + flen/2, y)],
                "liner", "sun_gold", size=stroke_sz, opacity=min(1.0, f_op)
            )
            # High-intensity white-gold glint in upper half
            if y < 0.66 and abs(fx - sun_pt[0]) < total_w * 0.28:
                s.stroke(
                    [(fx - flen * 0.25, y), (fx + flen * 0.25, y)],
                    "liner", "sun_core", size=stroke_sz * 0.8, opacity=min(1.0, f_op * 0.95)
                )

    # Ultra-fine horizontal surface ripples in the open flanks of the lake
    for ry in [0.55, 0.60, 0.67, 0.75, 0.83, 0.92]:
        for x0, x1 in [(-0.02, 0.35), (0.78, 1.02)]:
            s.stroke([(x0, ry), (x1, ry)], "liner", "lake_sky", size=0.005, opacity=0.35)

    # Low wisps of lake steam / morning vapour skimming the cold water
    for my, mx0, mx1 in [
        (0.535, 0.15, 0.82),
        (0.565, 0.35, 0.95),
        (0.625, 0.08, 0.60),
        (0.705, 0.38, 0.82),
    ]:
        s.stroke([(mx0, my), (mx1, my)], "round_soft", "mist_pale", size=0.022, opacity=0.30, glaze=True)

    # -------------------------------------------------------------
    # 8. FOREGROUND ROCKY HEADLAND (Left)
    # -------------------------------------------------------------
    print("Pass 7: Foreground rocky shoreline promontory...")
    s.dry()
    shore_poly = polygon([
        (0.0, 0.68), (0.13, 0.70), (0.24, 0.75), (0.33, 0.82),
        (0.36, 0.88), (0.28, 0.96), (0.0, 1.0), (0.0, 0.68)
    ])
    # Massive dark bedrock
    s.block_in(shore_poly, brush="knife", color="rock_dark", size=0.055, solid=True)

    # Granite facet planes catching ambient dawn light
    s.stroke([(0.02, 0.71), (0.18, 0.74)], "knife", "rock_plane", size=0.030, opacity=0.85)
    s.stroke([(0.14, 0.79), (0.28, 0.83)], "knife", "rock_plane", size=0.025, opacity=0.80)
    s.stroke([(0.05, 0.75), (0.22, 0.78)], "bristle", "moss", size=0.030, opacity=0.75)

    # Wet boulders at the water's edge
    for rx, ry, sz in [
        (0.25, 0.77, 0.028),
        (0.32, 0.83, 0.025),
        (0.35, 0.87, 0.022),
        (0.29, 0.93, 0.026)
    ]:
        s.dab(rx, ry, brush="knife", color="rock_dark", size=sz)
        # Warm golden rim catching the morning sun
        s.stroke([(rx, ry - sz * 0.3), (rx + sz * 0.35, ry)], "liner", "pine_rim", size=0.005, opacity=0.85)

    # Mirror reflection of the rock bank in the water
    s.stroke([(0.0, 0.71), (0.22, 0.78)], "flat", "dark", size=0.05, opacity=0.65)
    s.stroke([(0.15, 0.81), (0.32, 0.89)], "flat", "lake_deep", size=0.05, opacity=0.65)
    # Bright water surface contact line
    s.stroke([(0.12, 0.71), (0.24, 0.76), (0.33, 0.83), (0.36, 0.88)],
             "liner", "sun_gold", size=0.005, opacity=0.80)

    # -------------------------------------------------------------
    # 9. MAJESTIC CONIFERS (Realistic Full Conifer Foliage)
    # -------------------------------------------------------------
    print("Pass 8: Painting authentic majestic conifer trees...")
    s.dry()

    def paint_conifer(x_base, y_base, x_top, y_top, trunk_w, max_reach, steps, seed_val):
        prng = random.Random(seed_val)

        # 1. Base trunk
        s.stroke([(x_base, y_base), (x_top, y_top)], brush="bristle", color="dark",
                 size=trunk_w, pressure="taper", load=1.0, load_falloff=0.0)
        # Sunward warm bark rim
        s.stroke([(x_base + trunk_w * 0.3, y_base), (x_top + trunk_w * 0.15, y_top + 0.1)],
                 brush="liner", color="bark_lit", size=trunk_w * 0.35, opacity=0.85)

        # 2. Dense overlapping conifer boughs from crown down to base
        # Foliage occupies the top 85% of the tree height
        foliage_span = (y_base - y_top) * 0.85

        for i in range(steps):
            t = (i + 1) / (steps + 1) # 0 at top, 1 at bottom of foliage
            # Non-linear reach: slender at top, full body in mid-lower section
            reach = max_reach * (0.12 + 0.88 * (t ** 0.65)) * prng.uniform(0.85, 1.15)
            y = y_top + t * foliage_span
            x = x_top + t * (x_base - x_top)

            droop = reach * prng.uniform(0.12, 0.22)
            brush_sz = 0.012 + t * 0.016

            # A. Dense center body covering trunk
            s.stroke([(x - reach * 0.45, y), (x + reach * 0.45, y)],
                     "bristle", "pine_dark", size=brush_sz * 1.2, opacity=0.92)

            # B. Left bough (shadowed / cool evergreen)
            l_tip = (x - reach, y + droop)
            s.stroke([(x, y - 0.003), (x - reach * 0.5, y + droop * 0.3), l_tip],
                     "bristle", "pine_deep", size=brush_sz, opacity=0.90)

            # C. Right bough (sunward / rich green with dawn rim light)
            r_tip = (x + reach, y + droop)
            s.stroke([(x, y - 0.003), (x + reach * 0.5, y + droop * 0.3), r_tip],
                     "bristle", "pine_body", size=brush_sz, opacity=0.90)

            # D. Golden dawn rim highlights on right-side branch tips
            if t > 0.15 and prng.random() > 0.30:
                rim_start = (x + reach * 0.45, y + droop * 0.35)
                s.stroke([rim_start, r_tip], "liner", "pine_rim", size=0.005, opacity=0.92)
                # Delicate dew/sun sparkle on needle tip
                if prng.random() > 0.45:
                    s.dab(r_tip[0], r_tip[1], "liner", "pine_spark", size=0.005, press=2)

        # Lower bare weathered twigs near tree base
        for _ in range(4):
            by = y_top + foliage_span + prng.uniform(0.01, 0.05)
            bx = x_top + (x_base - x_top) * (foliage_span / (y_base - y_top))
            bw = max_reach * prng.uniform(0.3, 0.6)
            s.stroke([(bx, by), (bx - bw, by + 0.01)], "liner", "bark_dark", size=0.004, opacity=0.8)
            s.stroke([(bx, by), (bx + bw * 0.8, by + 0.01)], "liner", "bark_lit", size=0.004, opacity=0.7)

        # Crown peak
        s.stroke([(x_top, y_top + 0.02), (x_top, y_top - 0.012)], "liner", "pine_dark", size=0.004)

        # 3. Water reflection of the tree plunging into the lake
        ref_h = foliage_span * 0.70
        s.stroke([(x_base, y_base), (x_base, y_base + ref_h)],
                 "flat", "pine_deep", size=max_reach * 0.85, opacity=0.55)
        # Soft horizontal breaks across the reflection
        for dy in [0.06, 0.12, 0.19, 0.28, 0.38]:
            ry = y_base + dy
            if ry < 0.98:
                s.stroke([(x_base - max_reach * 0.5, ry), (x_base + max_reach * 0.5, ry)],
                         "knife", "lake_deep", size=0.006, opacity=0.50)

    # Tree 1: Tall Elder Hero Pine (Left)
    print("  -> Elder Hero Pine (Left)...")
    paint_conifer(x_base=0.11, y_base=0.74, x_top=0.10, y_top=0.06,
                  trunk_w=0.016, max_reach=0.110, steps=36, seed_val=111)

    # Tree 2: Stately Companion Pine
    print("  -> Stately Companion Pine...")
    paint_conifer(x_base=0.20, y_base=0.73, x_top=0.21, y_top=0.12,
                  trunk_w=0.013, max_reach=0.095, steps=32, seed_val=222)

    # Tree 3: Weathered Leaning Pine (Frame Edge)
    print("  -> Weathered Leaning Pine (Edge)...")
    paint_conifer(x_base=0.03, y_base=0.78, x_top=0.01, y_top=0.17,
                  trunk_w=0.017, max_reach=0.080, steps=28, seed_val=333)

    # Tree 4: Younger Slender Pine (Promontory Point)
    print("  -> Slender Pine (Point)...")
    paint_conifer(x_base=0.27, y_base=0.77, x_top=0.28, y_top=0.28,
                  trunk_w=0.009, max_reach=0.060, steps=22, seed_val=444)

    # -------------------------------------------------------------
    # 10. ATMOSPHERIC SOFTENING, LAKE MIST & FINISH
    # -------------------------------------------------------------
    print("Pass 9: Atmospheric softening and final touches...")
    # Drifting mist weaving behind and through the lower trunks
    s.stroke([(0.00, 0.71), (0.22, 0.73)], "round_soft", "mist_warm", size=0.035, opacity=0.35, glaze=True)
    s.stroke([(0.14, 0.75), (0.33, 0.76)], "round_soft", "mist_pale", size=0.030, opacity=0.30, glaze=True)

    # Soften parts of the far horizon into the dawn mist
    s.smudge([(0.76, 0.518), (0.94, 0.512)])
    s.stroke([(0.75, 0.517), (0.95, 0.511)], "round_soft", "mist_warm", size=0.025, opacity=0.40)

    # Final sparkling glints of dawn sunlight on the water
    s.dab(0.662, 0.536, "round_hard", "sun_core", size=0.007, press=3, tip_wobble=0.5)
    s.dab(0.658, 0.562, "round_hard", "sun_core", size=0.005, press=3, tip_wobble=0.5)

    # Artist signature in lower right corner
    s.stroke([(0.88, 0.95), (0.92, 0.935)], "liner", "dark", size=0.005, note="signature")

    # -------------------------------------------------------------
    # EXPORT & TIMELAPSE
    # -------------------------------------------------------------
    print("Exporting completed fine art painting...")
    out_file = Path("misty_pine_forest_at_dawn.png")
    s.export(out_file, impasto=True, sketch=True)

    print("Generating time-lapse GIF...")
    gif_file = Path("misty_pine_forest_at_dawn.gif")
    s.timelapse_gif(gif_file, fps=10.0, every=3)

    print("Saving Easel session file...")
    easel_file = Path("misty_pine_forest.easel")
    s.save(easel_file)

    print(s.report())
    elapsed = time.time() - t_start
    print(f"Masterpiece complete in {elapsed:.1f}s! Total marks: {s.spent}")
    return out_file

if __name__ == "__main__":
    paint()
