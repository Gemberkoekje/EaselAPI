"""Easel -- a headless painting engine for agents that can look at their own work.

Not a drawing library and not a rasteriser. Brushes carry a finite load of paint
and run out. Paint lands wet and mixes with what is already there. The canvas has
tooth, and a brush low on paint catches only the high points. Mistakes stay until
they are painted over.

The whole API runs through one object::

    from easel import Session, blob, cell

    s = Session(1024, 768, texture="linen", ground="toned_grey", seed=7)
    s.palette["shadow"] = s.palette.mix("ultramarine", "burnt_umber", 0.4)

    s.block_in(blob(cell("D5")), brush="bristle", color="shadow", density=0.8)
    s.look(values=True)          # check the value structure
    s.stroke([(0.2, 0.6), (0.6, 0.55), (0.9, 0.62)], "bristle", "yellow_ochre")
    s.export("painting.png")

Coordinates are always normalised 0..1 with the origin at the top-left, so nothing
here depends on the canvas size. If you are new to the engine, read ``PAINTER.md``
rather than this docstring: it teaches the workflow, which matters more than the
function list.
"""

from __future__ import annotations

from easel.brush import BRUSHES, TIPS, Brush, brush
from easel.canvas import GRAPHITE, GROUNDS, Canvas
from easel.color import (
    linear_to_oklab,
    linear_to_srgb,
    mix,
    mix_many,
    parse_color,
    srgb_to_linear,
)
from easel.history import History, StrokeRecord
from easel.look import load_reference, render_look
from easel.measure import CellCompare, Comparison, compare_images
from easel.palette import PIGMENTS, Palette
from easel.prepare import LEVELS, Area, Preparation, prepare_reference
from easel.regions import (
    GRID_COLS,
    GRID_ROWS,
    REGION_NAMES,
    Polygon,
    Region,
    above,
    below,
    between,
    blob,
    cell,
    ellipse,
    golden,
    horizon,
    hull,
    left_of,
    polygon,
    region,
    ribbon,
    right_of,
    span,
    thirds,
    union,
)
from easel.session import Session
from easel.stroke import (
    PRESSURE_PROFILES,
    catmull_rom,
    draw_pencil,
    paint_stroke,
    pressure_curve,
)
from easel.texture import TEXTURES, make_texture

#: Checked against pyproject.toml by tests/test_version.py, which is the only
#: thing keeping these two in step -- see that file for what it cost last time.
__version__ = "0.2.0"

__all__ = [
    # the main entry point
    "Session",
    # surfaces
    "Canvas",
    "GROUNDS",
    "GRAPHITE",
    "TEXTURES",
    "make_texture",
    # marks
    "Brush",
    "BRUSHES",
    "brush",
    "TIPS",
    "paint_stroke",
    "draw_pencil",
    "PRESSURE_PROFILES",
    "pressure_curve",
    "catmull_rom",
    # colour
    "Palette",
    "PIGMENTS",
    "mix",
    "mix_many",
    "parse_color",
    "linear_to_oklab",
    "srgb_to_linear",
    "linear_to_srgb",
    # composition
    "Region",
    "region",
    "REGION_NAMES",
    "cell",
    "span",
    "GRID_COLS",
    "GRID_ROWS",
    "thirds",
    "golden",
    "horizon",
    "above",
    "below",
    "left_of",
    "right_of",
    "between",
    "Polygon",
    "polygon",
    "ellipse",
    "blob",
    "hull",
    "ribbon",
    "union",
    # looking, measuring and reading the reference
    "render_look",
    "load_reference",
    "Comparison",
    "CellCompare",
    "compare_images",
    "Preparation",
    "Area",
    "prepare_reference",
    "LEVELS",
    "History",
    "StrokeRecord",
    "__version__",
]
