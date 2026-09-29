"""Letters as paths: a single-stroke font, placed, slanted and varied.

Nothing in the engine lays a letter, and a painter who needs a word types one path a
letter by hand -- which is where the letters go wrong: one painter's own ``G`` came
out as another letter, the arc run the wrong way round. So the font is the part that
ships. :func:`letter_paths` returns each letter's strokes as paths, placed where the
text goes, and a painter lays them with :meth:`~easel.session.Session.stroke` or
:meth:`~easel.session.Session.pencil` like any other path -- the way :func:`ribbon`
returns a shape and paints nothing. A path is one stroke, and a letter is one to
three of them.

The font is data: :data:`GLYPHS`, one entry a character, each an advance and its
paths, in a box one capital high with ``y`` running down -- ``0`` the top of a
capital, ``1`` the baseline, lower-case bodies from ``0.4`` and descenders to
``1.3``. An arc is kept as the points along it, so a glyph is only points.
"""

from __future__ import annotations

import math

import numpy as np

__all__ = ["GLYPHS", "LETTERS", "letter_paths"]

#: The gap between two letters, and the drop from one line to the next, in capitals.
_GAP = 0.18
_LEADING = 1.6

#: How much a hand varies, as a fraction of a capital: a letter's size, its baseline's
#: drift from letter to letter (and the most it drifts), a letter's lean in degrees,
#: and how far a point of a letter wanders off the font's.
_HAND_SIZE = 0.04
_HAND_DRIFT = 0.015
_HAND_DRIFT_MOST = 0.06
_HAND_LEAN = 2.0
_HAND_POINT = 0.012

#: The longest straight step a returned path takes, in capitals: long enough to keep a
#: path short, short enough that a stroke's spline through it stays on the line.
_STEP = 0.12


def _arc(cx: float, cy: float, rx: float, ry: float, a0: float, a1: float,
         every: float = 15.0) -> list[tuple[float, float]]:
    """Points along an arc, from ``a0`` to ``a1`` degrees; ``0`` is right, ``90`` down."""
    n = max(2, int(math.ceil(abs(a1 - a0) / every)))
    return [(round(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), 4),
             round(cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)), 4))
            for i in range(n + 1)]


def _ring(cx: float, cy: float, rx: float, ry: float, start: float = -90.0):
    return _arc(cx, cy, rx, ry, start, start + 360.0)


def _dot(x: float, y: float) -> list[tuple[float, float]]:
    return [(x, y), (x, y + 0.06)]


#: Every character the font draws: ``{character: (advance, [path, ...])}``, a path a
#: list of ``(u, v)`` in capitals, ``v`` running down from the top of a capital.
GLYPHS: dict[str, tuple[float, list[list[tuple[float, float]]]]] = {
    " ": (0.40, []),
    # capitals
    "A": (0.70, [[(0.0, 1.0), (0.35, 0.0), (0.70, 1.0)], [(0.14, 0.62), (0.56, 0.62)]]),
    "B": (0.66, [[(0.0, 1.0), (0.0, 0.0), (0.34, 0.0)] + _arc(0.34, 0.24, 0.24, 0.24, -90, 90)
                 + [(0.0, 0.48)],
                 [(0.0, 0.48), (0.38, 0.48)] + _arc(0.38, 0.74, 0.28, 0.26, -90, 90)
                 + [(0.0, 1.0)]]),
    "C": (0.76, [_arc(0.40, 0.50, 0.40, 0.50, -40, -320)]),
    "D": (0.72, [[(0.0, 0.0), (0.0, 1.0)],
                 [(0.0, 0.0), (0.30, 0.0)] + _arc(0.30, 0.50, 0.42, 0.50, -90, 90)
                 + [(0.0, 1.0)]]),
    "E": (0.60, [[(0.60, 0.0), (0.0, 0.0), (0.0, 1.0), (0.60, 1.0)],
                 [(0.0, 0.50), (0.46, 0.50)]]),
    "F": (0.58, [[(0.58, 0.0), (0.0, 0.0), (0.0, 1.0)], [(0.0, 0.50), (0.44, 0.50)]]),
    "G": (0.80, [_arc(0.40, 0.50, 0.40, 0.50, -40, -330)
                 + [(0.80, 0.56), (0.50, 0.56)]]),
    "H": (0.66, [[(0.0, 0.0), (0.0, 1.0)], [(0.66, 0.0), (0.66, 1.0)],
                 [(0.0, 0.50), (0.66, 0.50)]]),
    "I": (0.10, [[(0.05, 0.0), (0.05, 1.0)]]),
    "J": (0.52, [[(0.50, 0.0), (0.50, 0.72)] + _arc(0.26, 0.72, 0.24, 0.28, 0, 165)]),
    "K": (0.62, [[(0.0, 0.0), (0.0, 1.0)], [(0.60, 0.0), (0.0, 0.62)],
                 [(0.20, 0.46), (0.62, 1.0)]]),
    "L": (0.54, [[(0.0, 0.0), (0.0, 1.0), (0.54, 1.0)]]),
    "M": (0.82, [[(0.0, 1.0), (0.0, 0.0), (0.41, 0.75), (0.82, 0.0), (0.82, 1.0)]]),
    "N": (0.66, [[(0.0, 1.0), (0.0, 0.0), (0.66, 1.0), (0.66, 0.0)]]),
    "O": (0.84, [_ring(0.42, 0.50, 0.42, 0.50)]),
    "P": (0.62, [[(0.0, 1.0), (0.0, 0.0), (0.34, 0.0)] + _arc(0.34, 0.26, 0.28, 0.26, -90, 90)
                 + [(0.0, 0.52)]]),
    "Q": (0.86, [_ring(0.42, 0.50, 0.42, 0.50), [(0.52, 0.72), (0.88, 1.05)]]),
    "R": (0.64, [[(0.0, 1.0), (0.0, 0.0), (0.34, 0.0)] + _arc(0.34, 0.26, 0.28, 0.26, -90, 90)
                 + [(0.0, 0.52)], [(0.30, 0.52), (0.64, 1.0)]]),
    "S": (0.64, [_arc(0.32, 0.25, 0.30, 0.25, -20, -270)
                 + _arc(0.32, 0.75, 0.32, 0.25, -90, 160)[1:]]),
    "T": (0.66, [[(0.0, 0.0), (0.66, 0.0)], [(0.33, 0.0), (0.33, 1.0)]]),
    "U": (0.66, [[(0.0, 0.0), (0.0, 0.66)] + _arc(0.33, 0.66, 0.33, 0.34, 180, 0)
                 + [(0.66, 0.0)]]),
    "V": (0.66, [[(0.0, 0.0), (0.33, 1.0), (0.66, 0.0)]]),
    "W": (0.86, [[(0.0, 0.0), (0.20, 1.0), (0.43, 0.30), (0.66, 1.0), (0.86, 0.0)]]),
    "X": (0.62, [[(0.0, 0.0), (0.62, 1.0)], [(0.62, 0.0), (0.0, 1.0)]]),
    "Y": (0.64, [[(0.0, 0.0), (0.32, 0.50), (0.64, 0.0)], [(0.32, 0.50), (0.32, 1.0)]]),
    "Z": (0.62, [[(0.0, 0.0), (0.60, 0.0), (0.0, 1.0), (0.62, 1.0)]]),
    # lower case: bodies from 0.4 to the baseline, ascenders from 0, descenders to 1.3
    "a": (0.54, [_ring(0.26, 0.70, 0.26, 0.30, 0), [(0.54, 0.40), (0.54, 1.0)]]),
    "b": (0.56, [[(0.0, 0.0), (0.0, 1.0)], _ring(0.28, 0.70, 0.28, 0.30, 180)]),
    "c": (0.50, [_arc(0.27, 0.70, 0.27, 0.30, -45, -315)]),
    "d": (0.56, [_ring(0.27, 0.70, 0.27, 0.30, 0), [(0.56, 0.0), (0.56, 1.0)]]),
    "e": (0.54, [[(0.02, 0.70), (0.54, 0.70)] + _arc(0.27, 0.70, 0.27, 0.30, 0, -320)[1:]]),
    "f": (0.40, [_arc(0.32, 0.20, 0.16, 0.18, -30, -180) + [(0.16, 1.0)],
                 [(0.0, 0.42), (0.36, 0.42)]]),
    "g": (0.54, [_ring(0.26, 0.70, 0.26, 0.30, 0),
                 [(0.54, 0.40), (0.54, 1.10)] + _arc(0.28, 1.10, 0.26, 0.20, 0, 160)]),
    "h": (0.52, [[(0.0, 0.0), (0.0, 1.0)],
                 _arc(0.26, 0.62, 0.26, 0.22, 180, 360) + [(0.52, 1.0)]]),
    "i": (0.10, [[(0.05, 0.40), (0.05, 1.0)], _dot(0.05, 0.16)]),
    "j": (0.32, [[(0.28, 0.40), (0.28, 1.10)] + _arc(0.10, 1.10, 0.18, 0.18, 0, 160),
                 _dot(0.28, 0.16)]),
    "k": (0.46, [[(0.0, 0.0), (0.0, 1.0)], [(0.42, 0.40), (0.0, 0.74)],
                 [(0.14, 0.64), (0.46, 1.0)]]),
    "l": (0.10, [[(0.05, 0.0), (0.05, 1.0)]]),
    "m": (0.80, [[(0.0, 0.40), (0.0, 1.0)],
                 _arc(0.20, 0.62, 0.20, 0.22, 180, 360) + [(0.40, 1.0)],
                 _arc(0.60, 0.62, 0.20, 0.22, 180, 360) + [(0.80, 1.0)]]),
    "n": (0.52, [[(0.0, 0.40), (0.0, 1.0)],
                 _arc(0.26, 0.62, 0.26, 0.22, 180, 360) + [(0.52, 1.0)]]),
    "o": (0.56, [_ring(0.28, 0.70, 0.28, 0.30)]),
    "p": (0.56, [[(0.0, 0.40), (0.0, 1.30)], _ring(0.28, 0.70, 0.28, 0.30, 180)]),
    "q": (0.56, [_ring(0.27, 0.70, 0.27, 0.30, 0), [(0.56, 0.40), (0.56, 1.30)]]),
    "r": (0.38, [[(0.0, 0.40), (0.0, 1.0)], _arc(0.26, 0.64, 0.26, 0.24, 180, 300)]),
    "s": (0.46, [_arc(0.23, 0.55, 0.21, 0.15, -20, -270)
                 + _arc(0.23, 0.85, 0.23, 0.15, -90, 160)[1:]]),
    "t": (0.40, [[(0.16, 0.10), (0.16, 0.88)] + _arc(0.30, 0.88, 0.14, 0.12, 180, 60)[1:],
                 [(0.0, 0.42), (0.36, 0.42)]]),
    "u": (0.52, [[(0.0, 0.40), (0.0, 0.78)] + _arc(0.26, 0.78, 0.26, 0.22, 180, 0)[1:]
                 + [(0.52, 0.40)], [(0.52, 0.40), (0.52, 1.0)]]),
    "v": (0.52, [[(0.0, 0.40), (0.26, 1.0), (0.52, 0.40)]]),
    "w": (0.72, [[(0.0, 0.40), (0.18, 1.0), (0.36, 0.55), (0.54, 1.0), (0.72, 0.40)]]),
    "x": (0.48, [[(0.0, 0.40), (0.48, 1.0)], [(0.48, 0.40), (0.0, 1.0)]]),
    "y": (0.52, [[(0.0, 0.40), (0.26, 1.0)], [(0.52, 0.40), (0.26, 1.0), (0.12, 1.30)]]),
    "z": (0.50, [[(0.0, 0.40), (0.48, 0.40), (0.0, 1.0), (0.50, 1.0)]]),
    # figures
    "0": (0.60, [_ring(0.30, 0.50, 0.30, 0.50)]),
    "1": (0.34, [[(0.04, 0.20), (0.26, 0.0), (0.26, 1.0)]]),
    "2": (0.62, [_arc(0.30, 0.28, 0.28, 0.28, -160, 20) + [(0.0, 1.0), (0.62, 1.0)]]),
    "3": (0.60, [_arc(0.28, 0.26, 0.27, 0.24, -160, 90)
                 + _arc(0.28, 0.75, 0.30, 0.25, -90, 160)[1:]]),
    "4": (0.62, [[(0.46, 1.0), (0.46, 0.0), (0.0, 0.70), (0.62, 0.70)]]),
    "5": (0.62, [[(0.56, 0.0), (0.08, 0.0), (0.04, 0.46)]
                 + _arc(0.30, 0.70, 0.30, 0.30, -150, 150)]),
    "6": (0.60, [[(0.48, 0.02), (0.22, 0.25), (0.04, 0.62)]
                 + _arc(0.31, 0.70, 0.28, 0.30, 180, 540)[1:]]),
    "7": (0.60, [[(0.0, 0.0), (0.60, 0.0), (0.20, 1.0)]]),
    "8": (0.60, [_ring(0.30, 0.25, 0.24, 0.25, 90), _ring(0.30, 0.74, 0.29, 0.26)]),
    "9": (0.60, [_arc(0.30, 0.30, 0.28, 0.30, 0, -360)
                 + [(0.56, 0.62), (0.46, 0.85), (0.28, 1.0)]]),
    # marks
    ".": (0.10, [_dot(0.05, 0.94)]),
    ",": (0.12, [[(0.07, 0.94), (0.02, 1.14)]]),
    "'": (0.10, [[(0.05, 0.0), (0.05, 0.22)]]),
    '"': (0.26, [[(0.05, 0.0), (0.05, 0.22)], [(0.21, 0.0), (0.21, 0.22)]]),
    "-": (0.36, [[(0.0, 0.60), (0.36, 0.60)]]),
    ":": (0.10, [_dot(0.05, 0.43), _dot(0.05, 0.94)]),
    ";": (0.12, [_dot(0.07, 0.43), [(0.07, 0.94), (0.02, 1.14)]]),
    "!": (0.10, [[(0.05, 0.0), (0.05, 0.72)], _dot(0.05, 0.94)]),
    "?": (0.54, [_arc(0.27, 0.25, 0.26, 0.24, -160, 60) + [(0.27, 0.72)],
                 _dot(0.27, 0.94)]),
    "(": (0.30, [_arc(0.36, 0.50, 0.32, 0.62, -125, -235)]),
    ")": (0.30, [_arc(-0.06, 0.50, 0.32, 0.62, -55, 55)]),
    "/": (0.40, [[(0.40, 0.0), (0.0, 1.0)]]),
}

#: The characters :data:`GLYPHS` draws, as one string, for an error to name.
LETTERS = "".join(GLYPHS)


def letter_paths(text: str, place, cap: float = 0.04, slant: float = 0.0,
                 seed: int | None = None, aspect: float | None = None
                 ) -> list[list[tuple[float, float]]]:
    """The strokes of ``text`` in a single-stroke hand, as paths placed on the canvas.

    Nothing is laid: each path is one stroke, laid the way any path is::

        for path in letter_paths("North gate", (0.12, 0.20), cap=0.04, slant=10,
                                 seed=3, aspect=s.aspect):
            s.stroke(path, "round_hard", "ink", size=0.003, opacity=0.9, load=1.0,
                     load_falloff=0.0, pressure="taper", smooth=False)

    With ``seed`` left off, every copy of a letter is the font's own, on one level
    baseline, and a line of them reads as type. **A hand is a seed**: each letter a
    little larger or smaller than the next, leaning a degree or two its own way, its
    points off the font's by about a hundredth of a capital, and the baseline drifting
    from letter to letter -- so no two copies of a letter are alike, and the same seed
    is the same hand again. Give it a ``slant`` as well, and ``pressure=`` on the
    stroke, which is where a hand's weight goes.

    A letter is one to three paths, about one and a half on average, so fifty letters
    are about seventy-five strokes; the returned list's length is the price. Capitals
    about 32 pixels tall read at the size a picture is shown small on a screen.

    Args:
        text: what to write. ``\\n`` starts a line below. Every character has to be
            in :data:`LETTERS` -- capitals, lower case, figures, a space and
            ``.,'"-:;!?()/``.
        place: where the first line's baseline starts, ``(x, y)``; or a region,
            whose bottom left it starts at, with ``cap`` its height when ``cap`` is
            left at its default.
        cap: the height of a capital, as a fraction of the canvas's **height**, as a
            point's ``y`` is: ``0.04`` is about 31 pixels on a canvas 768 high.
        slant: how far the letters lean forward, in degrees; ``0`` is upright.
        seed: the hand. ``None`` is the font as drawn.
        aspect: the canvas's width over its height -- ``s.aspect`` -- so a letter is
            as wide in pixels as the font draws it. Left off, the canvas is taken as
            square, and on a 4:3 canvas every letter is a quarter too narrow.

    Returns:
        A list of paths, each a list of ``(x, y)`` points.
    """
    text = str(text)
    missing = sorted({c for c in text if c not in GLYPHS and c != "\n"})
    if missing:
        raise ValueError(f"letter_paths() has no letter for {''.join(missing)!r}. The "
                         f"font draws {LETTERS!r}; spell it with those, or lay the "
                         f"mark yourself with s.stroke.")
    from easel.regions import Region, _looks_like_bounds, as_region

    if isinstance(place, (Region, str)) or _looks_like_bounds(place):
        box = as_region(place)
        x0, y0 = box.x0, box.y1
        if cap == 0.04:
            cap = box.y1 - box.y0
    else:
        x0, y0 = float(place[0]), float(place[1])
    cap = float(cap)
    if not (math.isfinite(cap) and cap > 0.0):
        raise ValueError(f"letter_paths(cap={cap!r}) is a capital's height, a fraction "
                         f"of the canvas's height: 0.04 is about 31 pixels at 768.")
    across = 1.0 / (1.0 if aspect is None else float(aspect))   # a capital's width unit
    lean = math.tan(math.radians(float(slant)))
    rng = None if seed is None else np.random.default_rng(int(seed))

    out: list[list[tuple[float, float]]] = []
    for row, line in enumerate(text.split("\n")):
        pen, drift = 0.0, 0.0
        base = y0 + row * _LEADING * cap
        for char in line:
            advance, paths = GLYPHS[char]
            size, turn = 1.0, 0.0
            if rng is not None:
                size = 1.0 + _HAND_SIZE * float(rng.standard_normal())
                turn = math.radians(_HAND_LEAN * float(rng.standard_normal()))
                drift = float(np.clip(drift + _HAND_DRIFT * rng.standard_normal(),
                                      -_HAND_DRIFT_MOST, _HAND_DRIFT_MOST))
            middle = advance / 2.0
            for path in paths:
                pts = np.asarray(_dense(path), dtype=np.float64)
                if rng is not None:
                    pts = pts + _HAND_POINT * _smooth_noise(rng, len(pts))
                u = (pts[:, 0] - middle) * size
                v = (pts[:, 1] - 1.0) * size                     # up from the baseline
                u, v = (u * math.cos(turn) - v * math.sin(turn),
                        u * math.sin(turn) + v * math.cos(turn))
                u = u + middle - v * lean                         # v is negative going up
                xs = x0 + (pen + u) * cap * across
                ys = base + (v + drift) * cap
                out.append([(float(x), float(y)) for x, y in zip(xs, ys, strict=True)])
            pen += (advance * size if rng is not None else advance) + _GAP
    return out


def _dense(path: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """A path with its long straight steps cut, so a spline through it keeps to it."""
    out = [path[0]]
    for (ax, ay), (bx, by) in zip(path[:-1], path[1:], strict=True):
        n = max(1, int(math.ceil(math.hypot(bx - ax, by - ay) / _STEP)))
        out.extend((ax + (bx - ax) * i / n, ay + (by - ay) * i / n) for i in range(1, n + 1))
    return out


def _smooth_noise(rng: np.random.Generator, n: int) -> np.ndarray:
    """``n`` points of wander, in two dimensions, that turn rather than fizz."""
    kick = rng.standard_normal((n, 2))
    walk = np.zeros((n, 2))
    w = np.zeros(2)
    for i in range(n):
        w = 0.6 * w + 0.8 * kick[i]
        walk[i] = w
    return walk
