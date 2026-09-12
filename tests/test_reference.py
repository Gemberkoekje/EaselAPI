"""`REFERENCE.md` against the engine it describes.

A reference is a promise that a number in it is the number in the code. The guide can
be a little out of date and still teach the right habit; a reference that is out of
date is worse than no reference, because it is read *instead of* looking. Nothing here
judges the prose -- it checks the facts that can drift on their own: the brush table,
the defaults, every name a painter can say, and every flag the shell takes.

The one measurement in the repo that a test can make is this one. Everything else worth
knowing about the engine was found by looking at a picture.
"""

from __future__ import annotations

import re
from dataclasses import fields
from pathlib import Path

import pytest

from easel.brush import BRUSHES, Brush
from easel.canvas import GROUNDS
from easel.cli import build_parser
from easel.history import History
from easel.palette import PIGMENTS
from easel.prepare import LEVELS
from easel.regions import REGION_NAMES
from easel.stroke import PRESSURE_PROFILES
from easel.texture import TEXTURES

REFERENCE = Path(__file__).resolve().parents[1] / "REFERENCE.md"
TEXT = REFERENCE.read_text(encoding="utf-8")

#: Pigment names that are short forms of another entry rather than paint of their own.
ALIASES = ("white", "yellow", "ochre", "red", "blue", "umber", "sienna")


def _number(cell: str) -> float:
    return float(cell.strip().strip("`"))


@pytest.mark.parametrize("name", sorted(BRUSHES))
def test_the_brush_table_is_the_brush(name):
    """Every row of it, against the preset it names."""
    rows = [ln for ln in TEXT.splitlines() if ln.startswith(f"| `{name}` |")]
    assert len(rows) == 1, f"REFERENCE.md has {len(rows)} rows for {name}"
    cells = rows[0].split("|")
    b = BRUSHES[name]
    got = [_number(c) for c in cells[3:8]]
    assert got == [b.size, b.opacity, b.hardness, b.load, b.load_falloff]


@pytest.mark.parametrize(
    "field",
    ["spacing", "jitter", "size_jitter", "angle", "aspect", "wetness",
     "thickness_gain", "smudge", "texture_sensitivity", "bristle_count",
     "bristle_pitch", "bristle_seed", "tip_wobble"],
)
def test_every_other_brush_default_is_listed_as_it_stands(field):
    """Read back as a number, not as a string: `0` and `0.0` are the same default, and
    a test that says otherwise is a test about typography."""
    default = {f.name: f.default for f in fields(Brush)}[field]
    found = re.search(rf"`{field} ([\d.]+)`", TEXT)
    assert found, f"REFERENCE.md does not list a default for {field}"
    assert float(found.group(1)) == pytest.approx(float(default))


@pytest.mark.parametrize("name", REGION_NAMES)
def test_every_region_a_painter_can_say_is_named(name):
    assert re.search(rf"\b{re.escape(name)}\b", TEXT)


@pytest.mark.parametrize("name", sorted(GROUNDS))
def test_every_ground_is_named(name):
    assert name in TEXT


@pytest.mark.parametrize("name", TEXTURES)
def test_every_texture_is_named(name):
    assert name in TEXT


@pytest.mark.parametrize("name", PRESSURE_PROFILES)
def test_every_pressure_profile_is_named(name):
    assert f'"{name}"' in TEXT


@pytest.mark.parametrize("name", sorted(set(PIGMENTS) - set(ALIASES)))
def test_every_pigment_is_named(name):
    assert name in TEXT


def test_the_short_names_are_named_as_short_names():
    """Seven of the eighteen entries are the same paint under another name, and a
    painter counting the box off this page should not come out with eighteen."""
    for alias in ALIASES:
        assert f"`{alias}`" in TEXT
    assert len(set(PIGMENTS) - set(ALIASES)) == 11
    assert "Eleven pigments" in TEXT


@pytest.mark.parametrize("level", sorted(LEVELS))
def test_every_prepare_level_is_named(level):
    assert f'"{level}"' in TEXT or f"`{level}`" in TEXT
    assert str(LEVELS[level]) in TEXT


def test_the_signature_allowance_is_the_one_the_log_grants():
    assert f"first {History.SIGNATURE_ALLOWANCE}" in TEXT or "first five" in TEXT
    assert History.SIGNATURE_ALLOWANCE == 5, "the reference says five in words"


def _budget_columns() -> tuple[str, str]:
    """The free column and the charged column of the budget table, as two strings."""
    table = TEXT.split("## What counts against the budget")[1].split("\n\n")[1]
    free, charged = [], []
    for row in table.splitlines()[2:]:                      # past the header and rule
        cells = row.split("|")
        free.append(cells[1])
        charged.append(cells[2])
    return " ".join(free), " ".join(charged)


@pytest.mark.parametrize("kind", [k for k in History.UNPAINTED_KINDS if k != "look"])
def test_what_the_log_does_not_charge_for_is_in_the_free_column(kind):
    """`look` is the exception: it is a record kind, not a call a painter makes."""
    free, charged = _budget_columns()
    assert f"`{kind}" in free and f"`{kind}" not in charged


@pytest.mark.parametrize(
    "verb", ["stroke", "dab", "smudge", "glaze", "block_in", "sweep", "scumble", "cover"])
def test_every_verb_that_lays_paint_is_in_the_charged_column(verb):
    """Including `smudge` and `glaze`, which a painter reaches for believing otherwise."""
    free, charged = _budget_columns()
    assert f"`{verb}" in charged and f"`{verb}" not in free


def _cli_options() -> set[str]:
    """Every long option the shell takes, whichever subcommand takes it."""
    out: set[str] = set()
    parser = build_parser()
    for action in parser._actions:
        for choice in getattr(action, "choices", None) or {}:
            sub = action.choices[choice]
            out.update(o for a in sub._actions for o in a.option_strings)
    return out


@pytest.mark.parametrize("flag", sorted(set(re.findall(r"--[a-z][a-z-]+", TEXT))))
def test_every_flag_the_reference_prints_is_a_flag(flag):
    assert flag in _cli_options()
