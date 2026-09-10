"""The reflectance floor, measured where it is not wanted.

Both halves of `REVIEW.md`'s open entry after finding 32, as numbers rather than
as an argument:

1. **A pixel nothing is being painted onto still moves.** `blend_wet()` floors
   *both* colours before weighting them by how much paint is landing, so a canvas
   pixel below the floor is rounded up to it by the K/S round trip even where the
   incoming alpha is a thousandth. The soft edge of every dab covers its whole
   square bounding box, so this is ordinary painting, not a contrived input.

2. **A colour below the floor cannot be laid as written.** The same clip caps the
   *incoming* colour, so `cadmium_yellow`'s blue channel and a literal black land
   lighter than they were asked for, at any opacity.

Run it before and after the fix; `--label` names the run in the output.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO / "src") not in sys.path:
    sys.path.insert(0, str(_REPO / "src"))

from easel.brush import BRUSHES  # noqa: E402
from easel.canvas import Canvas  # noqa: E402
from easel.color import blend_wet, linear_to_srgb, mix, parse_color  # noqa: E402


def srgb8(linear) -> np.ndarray:
    """Linear -> the 0..255 numbers that actually reach the PNG."""
    return np.round(linear_to_srgb(np.asarray(linear, dtype=np.float32)) * 255.0).astype(int)


def rgbstr(linear) -> str:
    """One colour as the triple a painter would read off the PNG."""
    return "(" + ", ".join(f"{v:3d}" for v in srgb8(linear).tolist()) + ")"


# -- 1. the pixel that is not being painted on ----------------------------------------
def untouched_pixel() -> None:
    print("1. A pixel at the soft edge of a dab, with nothing landing on it")
    print("   blend_wet(dst, src, amount) for a dst below the floor:")
    print(f"   {'amount':>10}  {'linear out':>12}  {'sRGB':>6}   lift from dst")
    dst = np.zeros((1, 1, 3), dtype=np.float32)          # true black
    src = parse_color("#C08A2E")                          # an unrelated ochre
    for amount in (0.0, 1e-6, 1e-4, 1e-3, 1e-2, 0.05):
        a = np.full((1, 1), amount, dtype=np.float32)
        out = blend_wet(dst, src, a)[0, 0]
        print(f"   {amount:>10.6f}  {out[0]:>12.6f}  {int(srgb8(out)[0]):>6d}   "
              f"{int(srgb8(out)[0]):+d} of 255")

    print()
    print("   The same thing through the engine, which is how it is reached:")
    print("   a round_soft dab landing a brush-width away from a black patch.")
    c = Canvas(64, 64, texture="smooth", ground="#FFFFFF", seed=0)
    c.rgb[:] = 0.0                                        # a canvas of true black
    before = c.rgb[8, 8].copy()
    brush = BRUSHES["round_soft"]
    mask = brush.mask(radius_px=12.0, angle_rad=0.0)
    # Centre the dab so that (8, 8) sits inside its bounding box but outside the
    # tip's own footprint -- the corner of the square, where the mask is ~0.
    c.stamp(20.0, 20.0, mask, parse_color("#C08A2E"), strength=1.0, load=1.0,
            wetness_gain=0.9, thickness_gain=0.0, texture_sensitivity=0.0)
    after = c.rgb[8, 8]
    off = 8 - (20 - mask.shape[0] // 2)
    reach = float(mask[off, off]) if 0 <= off < mask.shape[0] else 0.0
    print(f"   mask value at that pixel: {reach:.8f}")
    print(f"   before the dab: linear {before[0]:.6f}  sRGB {rgbstr(before)}")
    print(f"   after  the dab: linear {after[0]:.6f}  sRGB {rgbstr(after)}")

    print()
    print("   And how far the lift reaches across a whole black canvas under one dab:")
    c2 = Canvas(64, 64, texture="smooth", ground="#FFFFFF", seed=0)
    c2.rgb[:] = 0.0
    c2.stamp(32.0, 32.0, mask, parse_color("#C08A2E"), strength=1.0, load=1.0,
             wetness_gain=0.9, thickness_gain=0.0, texture_sensitivity=0.0)
    moved = int((srgb8(c2.rgb).max(axis=2) > 0).sum())
    inside = int((mask > 1e-3).sum())
    print(f"   pixels the tip actually reaches (mask > 0.001): {inside}")
    print(f"   pixels whose sRGB moved off 0:                  {moved}")


# -- 2. the colour that cannot be laid ------------------------------------------------
def unlayable_colour() -> None:
    print()
    print("2. A colour below the floor, laid at full strength")
    print(f"   {'colour':>16}  {'asked for':>22}  {'lands as':>22}   worst channel")
    cases = [
        ("cadmium_yellow", "#FFC012"),
        ("black", "#000000"),
        ("near-black", "#010101"),
        ("burnt_umber", "#2A1E1A"),          # a control: written above the floor
    ]
    for name, hexv in cases:
        want = parse_color(hexv)
        dst = np.tile(parse_color("#F3EDE1"), (1, 1, 1))  # any ground
        a = np.ones((1, 1), dtype=np.float32)             # nothing held back
        got = blend_wet(dst, want, a)[0, 0]
        worst = int(np.abs(srgb8(got) - srgb8(want)).max())
        print(f"   {name:>16}  {rgbstr(want):>22}  {rgbstr(got):>22}   {worst:>3d} of 255")


# -- 3. the mixtures the floor exists to protect --------------------------------------
def tuned_mixtures() -> None:
    print()
    print("3. The mixtures findings 5, 6 and 33 tuned the floor and the exponent against")
    print(f"   {'mixture':>52}  {'sRGB':>17}")
    cases = [
        ("cadmium_red + ultramarine 0.5 (violet, not green)", ("cadmium_red", "ultramarine", 0.5)),
        ("cadmium_yellow + ultramarine 0.5 (olive, not brown)", ("cadmium_yellow", "ultramarine", 0.5)),
        ("cerulean + white 0.7 (a pale sky)", ("cerulean", "titanium_white", 0.7)),
        ("ultramarine + burnt_umber 0.5 (near the model floor)", ("ultramarine", "burnt_umber", 0.5)),
        ("ultramarine + burnt_sienna 0.5 (the cool grey)", ("ultramarine", "burnt_sienna", 0.5)),
        ("cadmium_yellow + white 0.5", ("cadmium_yellow", "titanium_white", 0.5)),
        ("cadmium_yellow + cadmium_red 0.5", ("cadmium_yellow", "cadmium_red", 0.5)),
        ("cadmium_yellow, mixed with nothing (ratio 0.0)", ("cadmium_yellow", "titanium_white", 0.0)),
    ]
    from easel.color import luminance
    for label, (a, b, r) in cases:
        m = mix(a, b, r)
        print(f"   {label:>52}  {rgbstr(m):>17}  value {float(luminance(m)):.4f}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--label", default="", help="name for this run, e.g. before / after")
    args = ap.parse_args()
    if args.label:
        print(f"===== {args.label} =====")
        print()
    untouched_pixel()
    unlayable_colour()
    tuned_mixtures()


if __name__ == "__main__":
    main()
