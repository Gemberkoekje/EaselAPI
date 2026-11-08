"""Step 10 of 0.9.0: a shape cut at its notch, and the notice that prices its parts.

As the painter of Uktarl's Room chose when the pieces notice came back to it
(``paintings/Claude/uktarl_krannoc/answers-step7.md``): **(a), hold the notice until the
parts can be priced**, and speak when the parts cost under the mass by far, with both
prices, where the cut runs and which way each part runs, and the parts handed back as
shapes. A count of pieces could not tell its collar's V from the guide's own recipes,
which join parts on purpose; a price can. ``Polygon.split()`` is the cut, and
``parts-cheaper`` is the notice, at twice the parts and five strokes saved.
"""

from __future__ import annotations

import warnings

import pytest

import easel.session as session_module
from easel import Session, difference, ellipse, polygon, ribbon, roughen, union
from easel.session import _cheapest_way, _clean_fill

#: Uktarl's Room's collar as its prelude typed it, on its 1024x768 canvas.
COLLAR = [(0.4765625, 0.5182291666666666), (0.45703125, 0.4817708333333333),
          (0.435546875, 0.4296875), (0.458984375, 0.4401041666666667),
          (0.478515625, 0.46875), (0.5, 0.4947916666666667), (0.51953125, 0.46875),
          (0.54296875, 0.4348958333333333), (0.57421875, 0.4166666666666667),
          (0.55859375, 0.4713541666666667), (0.541015625, 0.5026041666666666),
          (0.5234375, 0.5182291666666666)]
#: ``PAINTING.md``'s ribbon round a bend.
BENT = [(0.20, 0.30), (0.45, 0.62), (0.78, 0.34)]


def make(tmp_path) -> Session:
    return Session(1024, 768, ground="toned_grey", seed=3, out_dir=tmp_path, timelapse=False)


def said(s: Session, *args, **kw) -> tuple[list, dict[str, str]]:
    """Lay one mass; its records and what it said, by code."""
    told = len(s.notices())
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        records = s.block_in(*args, **kw)
    return records, {n.code: n.text for n in s.notices(since=told)}


# -- the cut --------------------------------------------------------------------------------
def test_a_v_is_cut_down_its_notch_into_two_parts_that_tile_it():
    collar = polygon(COLLAR, name="collar")
    left, right = collar.split()
    assert left.area + right.area == pytest.approx(collar.area, abs=1e-12)
    assert (left.name, right.name) == ("collar, part 1", "collar, part 2")
    # The cut runs from the notch straight down to the base, where the painter put it.
    shared = set(left.points) & set(right.points)
    assert {(round(x, 3), round(y, 3)) for x, y in shared} == {(0.5, 0.495), (0.5, 0.518)}


def test_a_long_v_is_cut_down_its_middle_not_across_an_arm():
    """The shortest cut from a notch can run across one arm; the narrowest parts do not."""
    v = polygon([(0.30, 0.20), (0.40, 0.20), (0.50, 0.55), (0.60, 0.20), (0.70, 0.20),
                 (0.55, 0.75), (0.45, 0.75)])
    one, two = v.split()
    assert sorted(round(p.box.x0, 2) for p in (one, two)) == [0.3, 0.5]
    assert one.area == pytest.approx(two.area, rel=1e-9)


def test_a_bend_is_cut_at_the_bend():
    a, b = ribbon(BENT, 0.029).split()
    for part in (a, b):
        assert part.box.x0 < 0.46 or part.box.x1 > 0.44     # each part is one arm
    assert {round(a.box.x0, 2), round(b.box.x1, 2)} == {0.19, 0.79}


@pytest.mark.parametrize("shape", [
    ellipse((0.5, 0.5), 0.2, 0.1),
    polygon([(0.2, 0.2), (0.8, 0.25), (0.7, 0.8), (0.25, 0.7)]),
    roughen(ellipse((0.5, 0.5), 0.25, 0.15), seed=4),
], ids=["ellipse", "quadrilateral", "roughened"])
def test_a_shape_with_no_notch_is_not_cut(shape):
    with pytest.raises(ValueError, match="no notch to cut at"):
        shape.split()


def test_a_difference_is_not_cut():
    held = difference(polygon(COLLAR), ellipse((0.5, 0.47), 0.005))
    with pytest.raises(ValueError, match="has holes"):
        held.split()


def test_the_cut_depends_on_the_outline_alone():
    first = [p.points for p in polygon(COLLAR).split()]
    assert [p.points for p in polygon(COLLAR, name="x").split()] == first
    assert [p.points for p in polygon(COLLAR).split()] == first


# -- the notice ---------------------------------------------------------------------------
def test_the_collar_says_both_prices_and_where_it_is_cut(tmp_path):
    s = make(tmp_path)
    records, codes = said(s, polygon(COLLAR, name="collar"), "flat", "burnt_umber",
                          size=0.014, direction="axis")
    assert len(records) == 22
    assert codes["parts-cheaper"] == (
        "block_in of collar costs 22 strokes; cut at its notch, (0.500, 0.495) to (0.500, "
        "0.518), its two parts cost 5 and 4, laid along -57 and 59 degrees: lay each part "
        "along its own length. The shape's .split() hands the two parts back.")


def test_the_parts_cost_what_the_notice_said(tmp_path):
    s = make(tmp_path)
    collar = polygon(COLLAR, name="collar")
    laid = []
    for part in collar.split():
        strokes, degrees = _cheapest_way(part, 0.014, 1.0)
        records, codes = said(s, part, "flat", "burnt_umber", size=0.014, direction=degrees)
        laid.append(len(records))
        assert len(records) == strokes and "parts-cheaper" not in codes
    assert laid == [5, 4]


def test_the_bend_says_it_when_it_is_priced(tmp_path):
    s = make(tmp_path)
    told = len(s.notices())
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assert s.cost({"shape": ribbon(BENT, 0.029, name="bent"), "size": 0.015}) == 75
    said_ = {n.code: n.text for n in s.notices(since=told)}
    assert said_["parts-cheaper"].startswith(
        "block_in of bent costs 75 strokes; cut at its notch, ")
    assert "its two parts cost 10 and 10" in said_["parts-cheaper"]


def test_a_clean_edge_prices_each_part_inset_as_it_would_be_laid(tmp_path):
    s = make(tmp_path)
    bent = ribbon(BENT, 0.029, name="bent")
    _, codes = said(s, bent, "flat", "burnt_umber", size=0.015, edge="clean")
    parts = [_cheapest_way(_clean_fill(p, 0.0075), 0.015, 1.0)[0] for p in bent.split()]
    assert f"its two parts cost {parts[0]} and {parts[1]}" in codes["parts-cheaper"]


#: The guide's own joined shapes, as their recipes lay them: a grip's lobes, a
#: silhouette's shade at its 20 degrees, and a figure with an arm held out.
GRIP = union(ellipse((0.50, 0.56), 0.10, 0.09, rotate=-10),
             ellipse((0.40, 0.60), 0.06, 0.07), ellipse((0.60, 0.52), 0.05, 0.06))
BODY = union(ellipse((0.50, 0.56), 0.17, 0.21), ellipse((0.33, 0.36), 0.075, 0.09),
             ribbon([(0.58, 0.66), (0.66, 0.80), (0.70, 0.95)], 0.05, end_width=0.025),
             ribbon([(0.40, 0.70), (0.36, 0.82), (0.37, 0.95)], 0.045, end_width=0.03))


def _px(x: float, y: float) -> tuple[float, float]:
    return x / 1024, y / 768


STANDING = union(ellipse(_px(512, 300), *_px(24, 32)),
                 polygon([_px(478, 324), _px(546, 324), _px(596, 640), _px(432, 640)]),
                 polygon([_px(548, 350), _px(640, 300), _px(652, 316), _px(560, 384)]))


@pytest.mark.parametrize(("shape", "size", "kw"), [
    (GRIP, 0.03, {"direction": "axis", "edge": "clean", "solid": True}),
    (BODY.shifted(0.028, 0.038), 0.035, {"direction": 20}),
    (STANDING, 0.02, {"direction": "axis", "edge": "clean", "solid": True}),
], ids=["grip", "shade", "standing figure"])
def test_the_recipes_joined_shapes_are_not_told_to_cut(tmp_path, shape, size, kw):
    s = make(tmp_path)
    _, codes = said(s, shape, "flat", "burnt_umber", size=size, **kw)
    assert "parts-cheaper" not in codes


def test_it_speaks_for_the_cut_and_not_for_a_direction(tmp_path):
    """A convex shape laid the dear way is direction-given's, and a bent shape laid a
    dearer way than its own axis is measured against the axis, and says both."""
    s = make(tmp_path)
    facet = polygon([(0.40, 0.20), (0.47, 0.20), (0.55, 0.80), (0.48, 0.80)], name="facet")
    _, codes = said(s, facet, "flat", "burnt_umber", size=0.02, direction=0)
    assert "direction-given" in codes and "parts-cheaper" not in codes
    elbow = ribbon([(0.30, 0.20), (0.30, 0.70), (0.70, 0.70)], 0.04, name="elbow")
    records, codes = said(s, elbow, "flat", "burnt_umber", size=0.015, direction=45)
    assert len(records) == 80
    assert codes["parts-cheaper"].startswith(
        "block_in of elbow costs 80 strokes, 76 along its own axis; cut at its notch")


def test_a_sequence_of_directions_is_left_to_its_own_notice(tmp_path):
    s = make(tmp_path)
    _, codes = said(s, polygon(COLLAR, name="collar"), "flat", "burnt_umber", size=0.014,
                    direction="cross")
    assert "parts-cheaper" not in codes


def test_a_small_mass_is_not_told(tmp_path):
    """Five strokes saved is the floor: halving a mass of six saves three."""
    s = make(tmp_path)
    _, codes = said(s, polygon(COLLAR, name="collar"), "flat", "burnt_umber", size=0.05,
                    direction="axis")
    assert "parts-cheaper" not in codes


def test_the_notice_draws_nothing_from_the_stream(tmp_path):
    s = make(tmp_path)
    state = s.rng.bit_generator.state
    told = len(s.notices())
    collar = polygon(COLLAR, name="collar")
    b = s._resolve_brush("flat", 0.014, None, {})
    session_module._check_parts(s, collar, collar, b, "axis", 1.0, "ragged")
    assert s.rng.bit_generator.state == state
    assert [n.code for n in s.notices(since=told)] == ["parts-cheaper"]
    assert len(s.history.records) == 0
