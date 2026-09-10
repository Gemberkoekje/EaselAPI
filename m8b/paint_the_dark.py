"""M8b's evidence: one composition laid twice, by the engine before and after.

The brief says a change to the wet blend is judged on the sampler *and* a real
painting, looked at. The sampler half and two real paintings are the *first*
measurement here and they all come back byte for byte identical (`m8b/README.md`),
because nothing in the existing corpus is painted with a colour outside the K/S
band. That settles what this change breaks -- nothing -- and says nothing about
what it buys.

So this is the other half: a controlled pair in the range the fix opens up. Same
masses, same colours, same seed, same brushes, same order of work. The only
difference is which `blend_wet` is installed. The palette is chosen to sit where the
old floor bit: a painter-supplied near-black for the dark mass, and cadmium yellow,
the one shipped pigment whose blue channel is written under the floor.

    python m8b/paint_the_dark.py

Writes ``m8b/before.png``, ``m8b/after.png`` and ``m8b/compared.png``, and prints
the darkest value each engine reached and how far apart the two pictures are.

There is no subject here on purpose, the same as `m8/paint_two_ways.py`: the guide
must not carry one and neither should the evidence.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import easel.canvas as canvas_mod  # noqa: E402
import easel.color as color_mod  # noqa: E402
from easel import Session, blob, hull, ribbon  # noqa: E402
from easel.color import (  # noqa: E402
    _INV_MIX_EXPONENT,
    _from_ks,
    _ks_pow,
    _to_ks,
    linear_to_srgb,
    parse_color,
)

OUT = Path(__file__).resolve().parent
SIZE = (900, 675)
SEED = 21

#: A near-black the painter supplies rather than mixes. The box has no black on
#: purpose (`palette.py`), but a painter who reaches for one has to get it: this is
#: sRGB 6, linear 0.002, comfortably under the 0.01 reflectance floor.
DEEP = "#060606"


# --------------------------------------------------------------------------------------
# The engine as it was
# --------------------------------------------------------------------------------------
def _blend_wet_before(dst, src, amount):
    """`blend_wet` before M8b: the K/S clip applied to both colours and left there."""
    a = amount[..., None].astype(np.float32)
    src_b = np.broadcast_to(np.asarray(src, dtype=np.float32), dst.shape)
    ks_dst = _ks_pow(_to_ks(dst))
    ks_src = _ks_pow(_to_ks(src_b))
    return _from_ks((ks_dst * (1.0 - a) + ks_src * a) ** _INV_MIX_EXPONENT)


def _mix_many_before(colors, weights=None):
    """`mix_many` before M8b, so the palette and the canvas stay the same mixture."""
    cols = np.stack([parse_color(c) for c in colors]).astype(np.float32)
    if weights is None:
        w = np.full(len(cols), 1.0 / len(cols), dtype=np.float32)
    else:
        w = np.asarray(weights, dtype=np.float32)
        total = float(w.sum())
        w = w / total if total > 0 else np.full(len(cols), 1.0 / len(cols), dtype=np.float32)
    ks = _ks_pow(_to_ks(cols))
    return _from_ks(np.sum(ks * w[:, None], axis=0) ** _INV_MIX_EXPONENT)


class old_engine:  # noqa: N801 - a context manager reads better lowercase here
    """Install the pre-M8b blend for the duration of a painting."""

    def __enter__(self):
        import easel.palette as palette_mod
        import easel.stroke as stroke_mod

        self._saved = [
            (canvas_mod, "blend_wet", canvas_mod.blend_wet),
            (color_mod, "blend_wet", color_mod.blend_wet),
            (color_mod, "mix_many", color_mod.mix_many),
            (palette_mod, "mix_many", palette_mod.mix_many),
            (stroke_mod, "mix_many", stroke_mod.mix_many),
        ]
        for mod, name, _old in self._saved:
            setattr(mod, name, _blend_wet_before if name == "blend_wet" else _mix_many_before)
        # `mix` is a thin wrapper over `mix_many` and looks it up at call time, so
        # patching the module attribute is enough for the palette's own `mix` too.
        return self

    def __exit__(self, *exc):
        for mod, name, old in self._saved:
            setattr(mod, name, old)
        return False


# --------------------------------------------------------------------------------------
# The painting
# --------------------------------------------------------------------------------------
def masses():
    """The same five masses as `m8/paint_two_ways.py`, so the pair is comparable."""
    return [
        ("ground", ribbon([(-0.05, 0.74), (0.45, 0.62), (1.05, 0.70)], 0.62), "far", 0.17,
         "axis", 0.85),
        ("rise", hull([(0.02, 0.62), (0.30, 0.30), (0.62, 0.40), (0.74, 0.66),
                       (0.10, 0.72)]), "mid", 0.13, "axis", 1.0),
        ("mass", blob((0.66, 0.45), 0.26, 0.30, wobble=0.30, seed=4), "deep", 0.11,
         ("axis", 118.0), 1.0),
        ("arm", ribbon([(0.16, 0.86), (0.42, 0.66), (0.63, 0.58)], 0.20, end_width=0.07),
         "deep", 0.075, "axis", 1.0),
        ("light", blob((0.30, 0.26), 0.17, 0.11, wobble=0.35, seed=9), "lit", 0.06,
         "axis", 1.0),
    ]


def paint() -> Session:
    """One painting. Whichever `blend_wet` is installed is the one it is painted with."""
    s = Session(*SIZE, texture="linen", ground="toned_grey", seed=SEED, timelapse=False,
                out_dir=OUT)
    p = s.palette
    p["far"] = p.mix("cerulean", "titanium_white", 0.55)
    p["mid"] = p.mix("yellow_ochre", "burnt_umber", 0.45)
    p["deep"] = parse_color(DEEP)
    p["lit"] = p.mix("cadmium_yellow", "titanium_white", 0.25)

    for name, shape, color, size, direction, density in masses():
        s.block_in(shape, "bristle", color, direction=direction, density=density,
                   size=size, note=name)

    # Accents over the dark, with soft tips: this is where a dab's bounding box
    # crosses paint that is under the floor, which is the half of the defect that
    # was unreachable before because the dark could not be laid in the first place.
    s.dry()
    s.stroke([(0.24, 0.30), (0.33, 0.24), (0.40, 0.27)], "flat", "lit", size=0.035)
    s.stroke([(0.60, 0.36), (0.70, 0.30), (0.80, 0.34)], "round_soft", "lit", size=0.03,
             opacity=0.6)
    s.stroke([(0.58, 0.52), (0.68, 0.48), (0.78, 0.53)], "round_soft", "lit", size=0.026,
             opacity=0.45)
    s.dab(0.31, 0.25, brush="round_hard", color="lit", size=0.022)
    s.dab(0.70, 0.44, brush="round_soft", color="lit", size=0.02, press=2)
    return s


# --------------------------------------------------------------------------------------
# Reading the pair
# --------------------------------------------------------------------------------------
def srgb8(linear) -> np.ndarray:
    return np.round(linear_to_srgb(np.asarray(linear, dtype=np.float32)) * 255.0).astype(int)


def report(label: str, marks: int, px: np.ndarray) -> np.ndarray:
    dark = px.reshape(-1, 3).max(axis=1)
    print(f"  {label:7s} {marks:3d} marks   darkest pixel sRGB {int(dark.min()):3d}   "
          f"pixels at or under sRGB 16: {100.0 * float((dark <= 16).mean()):5.2f}%   "
          f"mean value {float(px.mean()):6.2f}")
    return px


#: The window local contrast is measured over, in pixels. Wide enough to hold a few
#: bristle streaks, narrow enough that it does not average the whole mass away.
_WINDOW = 9


def _box_mean(g: np.ndarray) -> np.ndarray:
    """Mean of ``g`` over every ``_WINDOW``-square, by summed-area table."""
    k = _WINDOW
    c = np.cumsum(np.cumsum(np.pad(g, ((1, 0), (1, 0))), 0), 1)
    return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]) / (k * k)


def inside_the_dark(before: np.ndarray, after: np.ndarray) -> None:
    """What the dark mass is made of, in each engine.

    The headline number -- "the darkest pixel went from 26 to 6" -- is the least
    interesting thing here, because a mass can be darker and still be a hole. What a
    painter needs from a dark is that it keeps a *surface*: the comb's streaks and the
    canvas tooth have to survive in it. Pinning 40% of the mass to one value is what
    takes those away, so this counts the levels the mass is built from and measures
    the texture left inside it.
    """
    mass = (before.max(axis=2) <= 40) & (after.max(axis=2) <= 40)
    print()
    print(f"  Inside the dark mass ({int(mass.sum())} px, {100.0 * float(mass.mean()):.1f}% "
          f"of the picture, taken as dark in both so the pixels compared are the same):")
    for label, im in (("before", before), ("after", after)):
        v = im[mass].max(axis=1)
        pinned = 100.0 * float(((v >= 25) & (v <= 26)).mean())
        # Local contrast: the standard deviation in a 9x9 window, averaged over the
        # mass. This is the comb and the tooth; a flat fill drives it to zero.
        g = im.max(axis=2).astype(np.float32)
        m1 = _box_mean(g)
        local = np.sqrt(np.maximum(_box_mean(g * g) - m1 * m1, 0.0))
        edge = (_WINDOW // 2, _WINDOW // 2 + local.shape[0])
        inner = mass[edge[0] : edge[1], edge[0] : _WINDOW // 2 + local.shape[1]]
        print(f"    {label:7s} range {int(v.min()):3d}-{int(v.max()):3d}   "
              f"{len(np.unique(v)):3d} distinct levels   "
              f"at the old floor's value (25-26): {pinned:5.1f}%   "
              f"local contrast {float(local[inner].mean()):5.2f}")


#: What to enlarge underneath the pair: the dark mass, where the painter's near-black
#: had to squeeze through the floor, and the lit blob, which is cadmium yellow.
DETAILS = {"the dark mass, and the soft accents over it": (480, 210, 900, 525),
           "the lit mass: cadmium yellow, whose blue is under the floor": (140, 90, 500, 360)}
PANEL_H = 430
PAD, LABEL_H, BG, FG = 16, 22, (28, 28, 30), (232, 232, 236)


def compare(before: Path, after: Path, out: Path) -> Path:
    """The two paintings side by side, with the places that changed enlarged below."""
    from PIL import Image, ImageDraw  # noqa: PLC0415 - only this mode needs it

    pair = [(Image.open(before).convert("RGB"), "BEFORE  (the floor on the result)"),
            (Image.open(after).convert("RGB"), "AFTER  (the floor on the arithmetic only)")]
    rows = [[(im.resize((round(im.width * PANEL_H / im.height), PANEL_H), Image.LANCZOS), label)
             for im, label in pair]]
    for title, box in DETAILS.items():
        crop_h = PANEL_H - 40
        rows.append([(im.crop(box).resize(
            (round((box[2] - box[0]) * crop_h / (box[3] - box[1])), crop_h), Image.LANCZOS),
            f"{label.split()[0].lower()}: {title}") for im, label in pair])

    width = max(sum(i.width for i, _ in row) + PAD * (len(row) + 1) for row in rows)
    height = sum(row[0][0].height + LABEL_H + PAD for row in rows) + PAD
    sheet = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(sheet)
    y = PAD
    for row in rows:
        x = PAD
        for img, label in row:
            draw.text((x, y), label, fill=FG)
            sheet.paste(img, (x, y + LABEL_H))
            x += img.width + PAD
        y += row[0][0].height + LABEL_H + PAD
    sheet.save(out)
    return out


def exported(path: Path) -> np.ndarray:
    """The PNG as it was written, so the numbers describe the picture being looked at.

    Not ``canvas.rgb``: the export composites the impasto relief over the paint, and
    that is part of what a dark mass looks like.
    """
    from PIL import Image  # noqa: PLC0415

    return np.asarray(Image.open(path).convert("RGB")).astype(int)


def main() -> int:
    print("One composition, two engines:")
    with old_engine():
        before = paint()
    before.export(OUT / "before.png")
    px_before = report("before", before.stroke_count, exported(OUT / "before.png"))

    after = paint()
    after.export(OUT / "after.png")
    px_after = report("after", after.stroke_count, exported(OUT / "after.png"))

    inside_the_dark(px_before, px_after)

    diff = np.abs(px_before - px_after)
    moved = diff.max(axis=2) > 0
    print()
    print(f"  pixels that differ: {100.0 * float(moved.mean()):5.2f}%   "
          f"largest difference {int(diff.max()):3d} of 255   "
          f"mean over the pixels that moved {float(diff.max(axis=2)[moved].mean()):.2f}")
    print(f"  Wrote {compare(OUT / 'before.png', OUT / 'after.png', OUT / 'compared.png')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
