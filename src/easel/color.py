"""Colour handling: sRGB <-> linear conversion and pigment-style subtractive mixing.

All pixel work inside Easel happens in **linear-light float32 RGB** in the range
0..1. Conversion to sRGB happens once, at export.

Mixing naive RGB averages turns every mixture grey-brown, which is the single
fastest way to make a painting look like clip-art. Easel therefore mixes in
Kubelka-Munk absorption/scattering space (single-constant approximation), which
keeps blue + yellow leaning green instead of sliding to grey.

Known limit of the single-constant model: white is a weaker lightener here than
real titanium white, which is a strong scatterer. Mixing 50/50 with white lightens
less than you would expect on a real palette -- reach for a higher white ratio, or
use :meth:`easel.palette.Palette.tint`.

If the optional ``pymixbox`` package is installed *and* its licence suits your
project, Easel will use it instead -- it is a better model. See the note in
:func:`mix` about why it is not a hard dependency.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "srgb_to_linear",
    "linear_to_srgb",
    "parse_color",
    "mix",
    "mix_many",
    "luminance",
    "linear_to_oklab",
    "MIXBOX_AVAILABLE",
]

# --------------------------------------------------------------------------------------
# Optional Mixbox backend
# --------------------------------------------------------------------------------------
# NOTE ON LICENCE: the reference Mixbox implementation is distributed under a
# CC BY-NC licence (non-commercial). Easel is MIT, so Mixbox is an *opt-in extra*
# rather than a dependency: `pip install easel-paint[mixbox]`. Without it, the
# built-in Kubelka-Munk approximation below is used, which is cruder but free of
# licence entanglement. Set EASEL_DISABLE_MIXBOX=1 to force the built-in model.
try:  # pragma: no cover - depends on optional install
    import os

    if os.environ.get("EASEL_DISABLE_MIXBOX"):
        raise ImportError
    import mixbox as _mixbox

    MIXBOX_AVAILABLE = True
except Exception:  # pragma: no cover
    _mixbox = None
    MIXBOX_AVAILABLE = False


# --------------------------------------------------------------------------------------
# Transfer functions
# --------------------------------------------------------------------------------------
def srgb_to_linear(x: np.ndarray) -> np.ndarray:
    """Convert sRGB-encoded values in 0..1 to linear light."""
    x = np.asarray(x, dtype=np.float32)
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4).astype(np.float32)


def linear_to_srgb(x: np.ndarray) -> np.ndarray:
    """Convert linear-light values in 0..1 to sRGB encoding."""
    x = np.clip(np.asarray(x, dtype=np.float32), 0.0, 1.0)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055).astype(np.float32)


def luminance(linear_rgb: np.ndarray) -> np.ndarray:
    """Rec. 709 relative luminance of linear RGB. Accepts (...,3)."""
    rgb = np.asarray(linear_rgb, dtype=np.float32)
    return (0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]).astype(np.float32)


#: Linear sRGB to the LMS cone space Oklab is built on, and the cube-root stage
#: after it. Constants from Bjorn Ottosson's derivation.
_OKLAB_M1 = np.array(
    [[0.4122214708, 0.5363325363, 0.0514459929],
     [0.2119034982, 0.6806995451, 0.1073969566],
     [0.0883024619, 0.2817188376, 0.6299787005]], dtype=np.float32)
_OKLAB_M2 = np.array(
    [[0.2104542553, 0.7936177850, -0.0040720468],
     [1.9779984951, -2.4285922050, 0.4505937099],
     [0.0259040371, 0.7827717662, -0.8086757660]], dtype=np.float32)


def linear_to_oklab(linear_rgb: np.ndarray) -> np.ndarray:
    """Linear RGB to Oklab. Accepts (..., 3).

    A perceptual space, so that "these two areas are the same colour" means what a
    painter means by it. Euclidean distance in sRGB does not: it puts two dark
    browns further apart than a dark brown and a mid grey, which is how an
    automatic segmentation ends up cutting a coat along its folds.
    """
    rgb = np.asarray(linear_rgb, dtype=np.float32)
    lms = rgb @ _OKLAB_M1.T
    lms = np.cbrt(np.maximum(lms, 0.0), dtype=np.float32)
    return (lms @ _OKLAB_M2.T).astype(np.float32)


# --------------------------------------------------------------------------------------
# Colour parsing
# --------------------------------------------------------------------------------------
def parse_color(value) -> np.ndarray:
    """Coerce a colour into linear-light float32 RGB.

    Accepts:

    * ``"#rrggbb"`` / ``"#rgb"`` hex strings (interpreted as sRGB),
    * a named pigment from :mod:`easel.palette` (e.g. ``"ultramarine"``),
    * a 3-tuple/list/ndarray of 0..1 floats (interpreted as sRGB), or
    * an existing linear ndarray of shape (3,) produced by Easel itself.
    """
    if isinstance(value, np.ndarray) and value.dtype == np.float32 and value.shape == (3,):
        return value
    if isinstance(value, str):
        s = value.strip()
        if s.startswith("#"):
            return srgb_to_linear(_hex_to_rgb(s))
        from easel.palette import PIGMENTS  # local import avoids a cycle

        key = s.lower().replace(" ", "_")
        if key in PIGMENTS:
            return srgb_to_linear(_hex_to_rgb(PIGMENTS[key]))
        raise ValueError(
            f"Unknown colour {value!r}. Use a hex string like '#3355aa', an (r, g, b) "
            f"tuple, or one of the pigment names: {', '.join(sorted(PIGMENTS))}"
        )
    arr = np.asarray(value, dtype=np.float32)
    if arr.shape != (3,):
        raise ValueError(f"Colour must have 3 components, got shape {arr.shape}")
    return srgb_to_linear(np.clip(arr, 0.0, 1.0))


def _hex_to_rgb(s: str) -> np.ndarray:
    s = s.lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        raise ValueError(f"Bad hex colour: #{s}")
    return np.array([int(s[i : i + 2], 16) / 255.0 for i in (0, 2, 4)], dtype=np.float32)


# --------------------------------------------------------------------------------------
# Pigment mixing
# --------------------------------------------------------------------------------------
# Reflectance floor. This is not just a divide-by-zero guard: real pigments never
# absorb a channel completely, and a hard zero makes that channel's K/S explode and
# swamp every mixture (cadmium red + ultramarine comes out dark green instead of
# violet). 0.01 is the smallest floor that keeps mixtures behaving like paint.
_FLOOR = np.float32(0.01)
_EPS = np.float32(1e-4)

# Mixtures are combined as a power mean of K/S with this exponent, rather than a
# plain (p=1) arithmetic mean.
#
# Why: single-constant Kubelka-Munk treats white as just another reflectance, but
# real titanium white is a powerful scatterer that dominates a mixture well beyond
# its volume share. At p=1 a 50/50 white mix barely lightens, which is wrong and
# actively misleading to paint with. p=0.5 gives white its real tinting strength
# while leaving the mixtures that matter behaving like paint: yellow + blue stays
# olive, red + blue stays violet, and nothing collapses toward grey.
_MIX_EXPONENT = np.float32(0.5)


def _to_ks(reflectance: np.ndarray) -> np.ndarray:
    """Kubelka-Munk K/S from reflectance (single-constant approximation)."""
    r = np.clip(reflectance, _FLOOR, 1.0 - _EPS)
    return ((1.0 - r) ** 2) / (2.0 * r)


def _from_ks(ks: np.ndarray) -> np.ndarray:
    """Invert K/S back to reflectance."""
    ks = np.maximum(ks, 0.0)
    return np.clip(1.0 + ks - np.sqrt(ks * ks + 2.0 * ks), 0.0, 1.0).astype(np.float32)


def mix(a, b, ratio: float = 0.5) -> np.ndarray:
    """Mix two colours like paint. ``ratio`` is the proportion of ``b``.

    ``mix(x, y, 0.0)`` is ``x``; ``mix(x, y, 1.0)`` is ``y``.
    """
    ca, cb = parse_color(a), parse_color(b)
    t = float(np.clip(ratio, 0.0, 1.0))
    return mix_many([ca, cb], [1.0 - t, t])


def mix_many(colors, weights=None) -> np.ndarray:
    """Mix N linear-RGB colours with optional weights, in pigment space."""
    cols = np.stack([parse_color(c) for c in colors]).astype(np.float32)
    if weights is None:
        w = np.full(len(cols), 1.0 / len(cols), dtype=np.float32)
    else:
        w = np.asarray(weights, dtype=np.float32)
        total = float(w.sum())
        w = w / total if total > 0 else np.full(len(cols), 1.0 / len(cols), dtype=np.float32)

    if MIXBOX_AVAILABLE:  # pragma: no cover - optional path
        srgb = [linear_to_srgb(c) * 255.0 for c in cols]
        latents = [np.asarray(_mixbox.rgb_to_latent(tuple(s)), dtype=np.float32) for s in srgb]
        blended = np.sum(np.stack(latents) * w[:, None], axis=0)
        out = np.asarray(_mixbox.latent_to_rgb(tuple(blended.tolist())), dtype=np.float32) / 255.0
        return srgb_to_linear(out)

    # Power mean with exponent _MIX_EXPONENT (0.5 -> sqrt and square, which are
    # cheap enough to run per pixel in the wet-blend path).
    ks = np.sqrt(_to_ks(cols))
    return _from_ks(np.sum(ks * w[:, None], axis=0) ** 2)


def blend_wet(dst: np.ndarray, src: np.ndarray, amount: np.ndarray) -> np.ndarray:
    """Per-pixel pigment blend used by wet-into-wet painting.

    ``dst`` is (h, w, 3) linear RGB already on the canvas, ``src`` is the incoming
    colour (3,) or (h, w, 3), and ``amount`` is (h, w) in 0..1 giving how much of
    the incoming paint displaces what is there.
    """
    a = amount[..., None].astype(np.float32)
    src_b = np.broadcast_to(np.asarray(src, dtype=np.float32), dst.shape)
    ks_dst = np.sqrt(_to_ks(dst))
    ks_src = np.sqrt(_to_ks(src_b))
    return _from_ks((ks_dst * (1.0 - a) + ks_src * a) ** 2)
