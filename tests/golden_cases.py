"""The fixed painting scripts behind the golden-image tests.

The brief has asked for visual regression since M2 and it never existed, which is
why every defect in the M1/M2 and M4 reviews was found by a human looking at a PNG.
These cases are the automated half of that: a fixed script of marks on each
texture, plus the sampler sheet, hashed. Any change to *what a mark looks like*
fails loudly, in the test suite, on the change that caused it.

They are not a substitute for looking. A hash says something moved; it cannot say
whether what moved got better. When a case fails, the test writes the new image
next to the expected one -- look at both, decide, and only then regenerate::

    python scripts/make_golden.py

The script is one place so that the test and the regenerator paint the *same*
strokes. Editing the marks below invalidates every stored hash on purpose.
"""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path

import numpy as np
from PIL import Image

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO / "src") not in sys.path:  # pragma: no cover - import plumbing
    sys.path.insert(0, str(_REPO / "src"))

from easel.regions import blob, hull, polygon, ribbon  # noqa: E402
from easel.session import Session  # noqa: E402
from easel.texture import TEXTURES  # noqa: E402

#: Small on purpose: big enough that a broken stroke still reads as broken, small
#: enough that the whole suite stays quick and the stored PNGs stay in the repo.
GOLDEN_SIZE = (420, 300)

GOLDEN_DIR = Path(__file__).resolve().parent / "golden"
HASH_FILE = GOLDEN_DIR / "hashes.json"


def paint_marks(s: Session) -> None:
    """A fixed script covering every way this engine puts paint on a surface.

    One of each brush; a stroke starved of load, which is where dry brush comes
    from; two strokes crossing while wet, which is where mixing comes from; a glaze
    over dry paint; a smudge dragging what is already there; a block-in below full
    density; and a single dab. If any of those change, a case here changes with it.

    Nothing in this script may depend on the wall clock, the filesystem, or on
    anything but the session's own seed.
    """
    p = s.palette
    p["dark"] = p.mix("ultramarine", "burnt_umber", 0.45)
    p["light"] = p.tint("yellow_ochre", 0.65)

    # A block-in below full density: the ground has to keep showing through.
    s.block_in("upper-band", brush="bristle", color="dark", density=0.7, size=0.16)

    # One stroke per brush, across the middle, each with a different pressure.
    s.stroke([(0.06, 0.46), (0.34, 0.40), (0.62, 0.50), (0.94, 0.44)],
             "bristle", "light", pressure="taper", size=0.09)
    s.stroke([(0.06, 0.56), (0.40, 0.60), (0.94, 0.54)],
             "flat", "cadmium_red", pressure="press_in", size=0.075)
    s.stroke([(0.08, 0.66), (0.50, 0.70), (0.92, 0.64)],
             "round_soft", "ultramarine", pressure="lift_off", size=0.06)
    s.stroke([(0.10, 0.76), (0.52, 0.79), (0.90, 0.74)],
             "round_hard", "titanium_white", pressure="even", size=0.035)
    s.stroke([(0.12, 0.88), (0.55, 0.90), (0.88, 0.86)],
             "knife", "dark", pressure="swell", size=0.06)

    # Starved: the load runs out along the stroke and the tooth takes over. This is
    # the mark that caught the deposit-nothing bug in REVIEW.md finding 11.
    s.stroke([(0.05, 0.32), (0.5, 0.30), (0.95, 0.33)],
             "bristle", "titanium_white", pressure="even", size=0.10,
             load=0.30, load_falloff=1.1)

    # Wet into wet: the second crosses the first before anything has dried.
    s.stroke([(0.20, 0.14), (0.30, 0.36)], "flat", "cadmium_red", size=0.07)
    s.stroke([(0.14, 0.28), (0.38, 0.20)], "flat", "titanium_white", size=0.07)

    # Dry, then a glaze over it -- colour without height.
    s.dry()
    s.glaze([(0.55, 0.12), (0.90, 0.26)], "ultramarine", opacity=0.22)

    # Smudge drags what is on the canvas rather than adding paint.
    s.smudge([(0.62, 0.50), (0.78, 0.62)], size=0.06)

    # A single dab, the smallest thing the engine makes.
    s.dab(0.5, 0.5, brush="round_hard", color="titanium_white", size=0.03)

    # The liner at the size it is actually for. The sampler drives every brush at
    # its own three sizes, so it shows the liner's dynamics and never its point:
    # a line three pixels wide is what this preset exists for, and it belongs under
    # regression at that width or it is not covered at all.
    s.stroke([(0.16, 0.20), (0.42, 0.24), (0.68, 0.18)], "liner", "titanium_white")


def build_marks(texture: str) -> np.ndarray:
    """Render the fixed script on one texture. Returns 8-bit sRGB."""
    w, h = GOLDEN_SIZE
    s = Session(w, h, texture=texture, ground="toned_grey", seed=11, timelapse=False)
    paint_marks(s)
    return s.canvas.to_srgb8()


def draw_drawing(s: Session) -> None:
    """The graphite channel: pressure, tooth, burial under paint, and the eraser.

    On rough paper, where the tooth bites hardest and a light line is a chain of
    grains rather than a line. Everything about the pencil that could silently
    change -- how dark it is, how broken, how much of it survives an opaque mass and
    a scumble -- is visible in one image here.
    """
    for i, press in enumerate((0.25, 0.5, 0.75, 1.0)):
        y = 0.10 + i * 0.09
        s.pencil([(0.06, y), (0.35, y - 0.03), (0.65, y + 0.03), (0.94, y)], pressure=press)

    # A drawn contour, the way a feature gets set down before any paint.
    theta = np.linspace(0.0, 2.0 * np.pi, 20, endpoint=True)
    s.pencil(list(zip(0.30 + 0.11 * np.cos(theta), 0.66 + 0.16 * np.sin(theta),
                      strict=True)), pressure=0.7, smooth=False)
    s.pencil(list(zip(0.70 + 0.11 * np.cos(theta), 0.66 + 0.16 * np.sin(theta),
                      strict=True)), pressure=0.7, smooth=False)

    # Paint over both contours: an opaque mass buries the left one, and a starved
    # glaze over the right one leaves it showing straight through. Those two are
    # the whole contract of the channel, side by side in one image.
    s.stroke([(0.20, 0.60), (0.40, 0.72)], "flat", "cadmium_red", size=0.10)
    # At this opacity a little over half the graphite survives the pass -- measured,
    # not guessed. See NOTES.md for the table.
    s.glaze([(0.60, 0.56), (0.82, 0.76)], "ultramarine", opacity=0.10, size=0.10)

    # And the eraser: the drawing goes where the painter disagrees with it.
    s.erase((0.02, 0.14, 0.30, 0.22))


def draw_shapes(s: Session) -> None:
    """M8: masses that are not rectangles, and every way of laying one out.

    A shape swept along its own axis, a concave one whose passes have to come back
    in pieces, a mass hung on landmarks, and one following a line. Between them they
    cover the clip against the outline, the multi-span pass, the angle resolution and
    the default of no overhang -- the four things that could change what a shaped
    mass looks like without anything else in this file noticing.
    """
    p = s.palette
    p["dark"] = p.mix("ultramarine", "burnt_umber", 0.45)
    p["mid"] = p.tint("burnt_sienna", 0.35)

    s.block_in(blob((0.30, 0.34), 0.24, 0.20, seed=4, name="blob"), brush="bristle",
               color="dark", direction="axis", density=0.9, size=0.10)
    s.block_in(polygon([(0.58, 0.10), (0.96, 0.10), (0.96, 0.62), (0.80, 0.62),
                        (0.80, 0.30), (0.70, 0.30), (0.70, 0.62), (0.58, 0.62)],
                       name="notch"),
               brush="flat", color="mid", direction="vertical", size=0.07)
    s.block_in(hull([(0.08, 0.98), (0.34, 0.66), (0.52, 0.98)], name="hull"),
               brush="bristle", color="mid", direction=28, density=1.0, size=0.08)
    s.block_in(ribbon([(0.56, 0.96), (0.76, 0.80), (0.98, 0.78)], 0.12, end_width=0.05,
                      name="ribbon"),
               brush="flat", color="dark", direction="axis", size=0.05)


def build_shapes() -> np.ndarray:
    """The shaped block-ins, on linen. Returns 8-bit sRGB."""
    w, h = GOLDEN_SIZE
    s = Session(w, h, texture="linen", ground="toned_grey", seed=17, timelapse=False)
    draw_shapes(s)
    return s.canvas.to_srgb8()


def build_drawing() -> np.ndarray:
    """The pencil, on rough paper. Returns 8-bit sRGB."""
    w, h = GOLDEN_SIZE
    s = Session(w, h, texture="rough", ground="warm_white", seed=5, timelapse=False)
    draw_drawing(s)
    return s.canvas.to_srgb8()


def build_sampler() -> np.ndarray:
    """Every painted cell of ``samples/brushes.png``, stacked, as one array.

    The cells and not the sheet: the sheet's labels come from Pillow's default
    bitmap font, and a golden that fails because a font shifted by a pixel teaches
    the next session to regenerate goldens without looking, which is the one habit
    that makes them worthless.
    """
    sampler = _load_sampler_module()
    rows = []
    for i, texture in enumerate(TEXTURES):
        seed = 100 + i * 1000
        for r, name in enumerate(sampler.BRUSHES):
            for c, (_label, size, pressure) in enumerate(
                [(sl, sv, pr) for sl, sv in sampler.SIZES for pr in sampler.PRESSURES]
            ):
                cell = sampler.render_cell(name, size, pressure, texture,
                                           seed + r * 31 + c * 7)
                rows.append(np.asarray(cell, dtype=np.uint8))
    return np.concatenate(rows, axis=0)


def _load_sampler_module():
    """Import ``scripts/make_brush_sampler.py`` as a module, without running main()."""
    path = _REPO / "scripts" / "make_brush_sampler.py"
    spec = importlib.util.spec_from_file_location("_easel_sampler", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


#: name -> builder. Every entry gets a stored hash.
CASES: dict[str, object] = {f"marks_{t}": (lambda t=t: build_marks(t)) for t in TEXTURES}
CASES["drawing"] = build_drawing
CASES["shapes"] = build_shapes
CASES["sampler"] = build_sampler

#: Cases stored as a hash only. The sampler is 190x19440 as one strip and a
#: near-duplicate of ``samples/brushes.png``, which is already committed and is
#: the sheet a human is meant to look at.
HASH_ONLY = frozenset({"sampler"})

#: What to open when a case fails, per case.
LOOK_AT = {"sampler": _REPO / "samples" / "brushes.png"}


def build(name: str) -> np.ndarray:
    """Render one case by name."""
    if name not in CASES:
        raise KeyError(f"Unknown golden case {name!r}. Have: {', '.join(CASES)}")
    return CASES[name]()


def digest(arr: np.ndarray) -> str:
    """A hash of the pixels themselves, not of an encoded PNG.

    PNG bytes depend on the encoder's version and settings; the pixels do not.
    """
    a = np.ascontiguousarray(arr, dtype=np.uint8)
    h = hashlib.sha256()
    h.update(f"{a.shape}".encode())
    h.update(a.tobytes())
    return h.hexdigest()


# --------------------------------------------------------------------------------------
# Numeric tolerance fallback
# --------------------------------------------------------------------------------------
# A same-source numpy release can still round a pixel +-1 of 255 differently: the
# cp312 and cp313 wheels of numpy==2.5.3 vectorise `**` (used in the sRGB gamma
# curve, color.py) through different compiled SIMD paths, which disagree in the
# last bit on a handful of values straddling a rounding boundary. Observed first
# when CI's Python 3.13 jobs failed every golden case at "max channel delta 1" on
# well under 0.1% of pixels while the 3.12 jobs on the same commit, same package
# versions, passed exactly. That is not a repaint changing -- finding 19 (this
# file's docstring) moved 20% of pixels by up to 49 levels, and is exactly the
# kind of thing these bounds must still catch.
TOLERANCE = 1
TOLERANCE_FRACTION = 0.02

#: Block size (rows, cols) to average-pool before comparing, for a case too big to
#: keep a second full-resolution reference image in the repo for. Averaging a
#: block dilutes an isolated +-1 pixel into a fraction of a level, so it survives
#: the same noise a raw per-pixel comparison does not.
POOL_BLOCK: dict[str, tuple[int, int]] = {"sampler": (12, 5)}


def pool_average(arr: np.ndarray, block: tuple[int, int]) -> np.ndarray:
    """Block-average ``arr`` by (rows, cols). Dimensions must divide evenly."""
    bh, bw = block
    h, w = arr.shape[:2]
    pooled = (
        arr[: (h // bh) * bh, : (w // bw) * bw]
        .astype(np.float64)
        .reshape(h // bh, bh, w // bw, bw, -1)
        .mean(axis=(1, 3))
    )
    return np.round(pooled).astype(np.uint8)


def tolerance_reference_path(name: str) -> Path:
    """Where the reference image for :func:`close_enough` lives, for ``name``."""
    if name in POOL_BLOCK:
        return GOLDEN_DIR / f"{name}.pooled.png"
    return GOLDEN_DIR / f"{name}.png"


def close_enough(arr: np.ndarray, name: str) -> bool:
    """True if ``arr`` is within :data:`TOLERANCE` of the stored reference.

    Call this only after an exact :func:`digest` comparison has already failed --
    it exists to absorb build noise (see :data:`TOLERANCE`'s docstring), not to
    replace the exact check as the primary signal.
    """
    ref_path = tolerance_reference_path(name)
    if not ref_path.exists():
        return False
    candidate = pool_average(arr, POOL_BLOCK[name]) if name in POOL_BLOCK else arr
    ref = np.asarray(Image.open(ref_path).convert("RGB"), dtype=np.int16)
    if ref.shape != candidate.shape:
        return False
    delta = np.abs(ref - candidate.astype(np.int16))
    if delta.max() > TOLERANCE:
        return False
    return bool((delta.max(axis=2) > 0).mean() <= TOLERANCE_FRACTION)
