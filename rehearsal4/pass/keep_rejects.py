"""Copy the looks that caught a rejected mark into rejected/ under real names,
and recover own1's lost frames from its own timelapse (the shared out/ dir
renumbers per session, so own1's looks were overwritten by own2's)."""
import os
import shutil
from PIL import Image, ImageSequence

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
REJ = os.path.join(HERE, "rejected")
os.makedirs(REJ, exist_ok=True)

PAIRS = [
    ("look_024.png", "copy_01_jagged_polygon_lit_band.png"),
    ("look_028.png", "copy_02_smudge_size010_pulled_lobes.png"),
    ("look_029.png", "copy_03_grain_opacity008_shouting.png"),
    ("look_034.png", "copy_04_mug_flat_size012_spilled_off_silhouette.png"),
    ("look_035.png", "copy_05_after_undo_spiky_black_shadow.png"),
    ("look_038.png", "copy_06_crewmate_milk_chocolate.png"),
    ("look_042.png", "copy_07_white_bar_at_the_base.png"),
    ("look_001.png", "own2_01_leaf_veins_overshot_the_leaves.png"),
    ("look_003.png", "own2_02_flat_ridges_as_stickynote_bars.png"),
    ("look_004.png", "own2_03_dark_gaps_as_black_slugs.png"),
]
for src, dst in PAIRS:
    p = os.path.join(OUT, src)
    if os.path.exists(p):
        shutil.copy2(p, os.path.join(REJ, dst))
        print("kept", dst)
    else:
        print("MISSING", src)

gif = os.path.join(HERE, "own1_timelapse.gif")
im = Image.open(gif)
frames = [f.convert("RGB") for f in ImageSequence.Iterator(im)]
print("own1 timelapse frames:", len(frames))
for frac, name in ((0.46, "own1_01_sun_path_solid_trapezoid.png"),
                   (0.52, "own1_02_water_buried_the_far_bank.png")):
    i = min(len(frames) - 1, int(len(frames) * frac))
    frames[i].save(os.path.join(REJ, name))
    print("recovered frame", i, "->", name)
