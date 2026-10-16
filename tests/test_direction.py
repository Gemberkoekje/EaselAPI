"""Step 7 of 0.9.0, workstream G: what a mass is charged for its direction, said at the call.

As the painter of Uktarl's Room chose after the bench
(``paintings/Claude/uktarl_krannoc/answers-step2.md``, 5a and 5b):

- **G1, a direction given that costs far more than the shape's own axis**, a notice with
  both prices. The mountain's ten facets, laid along the line from each peak to its dip,
  cost 88 strokes against 31 along their own axes; ``direction-default`` speaks only when
  ``direction=`` is left off, so nothing said so.
- **G2 (a), a shape whose passes come back in pieces**, a notice with its counts and no
  price: *14 passes in 22 pieces: lay each part along its own length*. The collar was a
  V laid as one mass, 22 strokes, against 3 and 4 as its two flaps.

Both are facts, off the geometry the price is counted from, and neither draws from the
stream.
"""

from __future__ import annotations

import warnings

import pytest

from easel import Session, polygon
from easel.session import _pass_pieces


def make(tmp_path) -> Session:
    return Session(480, 320, texture="linen", ground="toned_grey", seed=7, out_dir=tmp_path,
                   timelapse=False)


#: A tall thin facet leaning off the vertical: dear across its length, cheap along it.
FACET = [(0.40, 0.20), (0.47, 0.20), (0.55, 0.80), (0.48, 0.80)]
#: A V with its notch at the top, and the same V as its two flaps.
V = [(0.30, 0.20), (0.40, 0.20), (0.50, 0.55), (0.60, 0.20), (0.70, 0.20), (0.55, 0.75),
     (0.45, 0.75)]
FLAPS = ([(0.30, 0.20), (0.40, 0.20), (0.53, 0.65), (0.45, 0.75)],
         [(0.60, 0.20), (0.70, 0.20), (0.55, 0.75), (0.47, 0.65)])


def said(s: Session, *args, **kw) -> tuple[list, dict[str, str]]:
    """Lay one mass; its records and what it said, by code."""
    told = len(s.notices())
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        records = s.block_in(*args, **kw)
    return records, {n.code: n.text for n in s.notices(since=told)}


# -- G1: one direction given ---------------------------------------------------------------
def test_a_direction_given_that_costs_far_more_than_the_axis_says_both_prices(tmp_path):
    s = make(tmp_path)
    facet = polygon(FACET, name="facet")
    records, codes = said(s, facet, "flat", "burnt_umber", size=0.02, direction=0)
    _, along, _ = _pass_pieces(facet, 0.02, "axis", 1.0)
    assert codes["direction-given"] == (
        f"block_in of facet at direction=0 costs {len(records)} strokes; along the "
        f"mass's own axis it costs {along} (direction=\"axis\", or {facet.axis:.0f} "
        f"degrees). That is {len(records) / along:.1f}x the price.")
    assert len(records) > 2.5 * along
    assert "direction-default" not in codes


def test_the_price_it_quotes_is_what_the_mass_is_charged(tmp_path):
    """One walk: the strokes the notice says are the strokes the call lays, at the
    direction given and at the axis, so the two numbers cannot drift from the bill."""
    facet = polygon(FACET, name="facet")
    for direction in (0, "axis", 30, ((0.40, 0.20), (0.55, 0.80))):
        s = make(tmp_path)
        records, _ = said(s, facet, "flat", "burnt_umber", size=0.02, direction=direction)
        assert _pass_pieces(facet, 0.02, direction, 1.0)[1] == len(records), direction


@pytest.mark.parametrize("direction", ["axis", 80, ("axis", 172), (0, 90, 45)])
def test_the_axis_a_near_angle_and_a_sequence_say_nothing_of_it(tmp_path, direction):
    """The axis is the cheap way round; an angle within 2.5x of it is the painter's to
    choose; a sequence has its own notice, which prices every angle in it."""
    s = make(tmp_path)
    _, codes = said(s, polygon(FACET, name="facet"), "flat", "burnt_umber", size=0.02,
                    direction=direction)
    assert "direction-given" not in codes


def test_a_named_direction_and_a_line_are_directions_given(tmp_path):
    s = make(tmp_path)
    _, codes = said(s, polygon(FACET, name="facet"), "flat", "burnt_umber", size=0.02,
                    direction="horizontal")
    assert "at direction='horizontal' costs" in codes["direction-given"]
    # The painter's own form: the line from a peak to its dip, which crosses the facet.
    _, codes = said(s, polygon(FACET, name="facet"), "flat", "burnt_umber", size=0.02,
                    direction=[(0.40, 0.50), (0.55, 0.52)])
    assert "at the line given, 8 degrees costs" in codes["direction-given"]


def test_left_off_it_is_direction_default_that_speaks(tmp_path):
    s = make(tmp_path)
    _, codes = said(s, polygon(FACET, name="facet"), "flat", "burnt_umber", size=0.02)
    assert "direction-default" in codes and "direction-given" not in codes


def test_a_rectangle_is_not_asked(tmp_path):
    s = make(tmp_path)
    _, codes = said(s, (0.40, 0.10, 0.47, 0.90), "flat", "burnt_umber", size=0.02,
                    direction=0)
    assert "direction-given" not in codes and "pieces" not in codes


# -- G2 (a): passes in pieces ----------------------------------------------------------------
def test_a_shape_whose_passes_come_back_in_pieces_says_so_with_its_counts(tmp_path):
    s = make(tmp_path)
    collar = polygon(V, name="collar")
    records, codes = said(s, collar, "flat", "burnt_umber", size=0.02, direction=0)
    passes, pieces, cut = _pass_pieces(collar, 0.02, 0, 1.0)
    assert pieces == len(records) and pieces - passes >= passes / 3
    assert codes["pieces"] == (
        f"block_in of collar lays {passes} passes in {pieces} pieces: {cut} of them cross "
        f"the shape more than once and come back cut. Lay each part along its own "
        f"length, as a mass of its own.")


def test_each_part_along_its_own_length_is_silent_and_cheaper(tmp_path):
    """The remedy the notice names, laid: the two flaps say nothing, and cost less than
    the V at any of the directions it was tried at."""
    s = make(tmp_path)
    flaps = 0
    for i, points in enumerate(FLAPS):
        records, codes = said(s, polygon(points, name=f"flap {i}"), "flat", "burnt_umber",
                              size=0.02, direction="axis")
        assert "pieces" not in codes
        flaps += len(records)
    collar = polygon(V, name="collar")
    assert all(flaps < _pass_pieces(collar, 0.02, d, 1.0)[1] for d in (0, 45, 90, "axis"))


def test_a_convex_shape_never_comes_back_in_pieces(tmp_path):
    s = make(tmp_path)
    for direction in (None, 0, 45, "axis"):
        _, codes = said(s, polygon(FACET, name="facet"), "flat", "burnt_umber", size=0.02,
                        direction=direction)
        assert "pieces" not in codes


def test_a_plan_priced_says_both(tmp_path):
    """`cost()` walks the same passes before a mark is laid, and says what the call
    would: a rehearsal that comes back dear should say why."""
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.cost([{"shape": polygon(FACET, name="facet"), "brush": "flat",
                 "color": "burnt_umber", "size": 0.02, "direction": 0},
                {"shape": polygon(V, name="collar"), "brush": "flat",
                 "color": "burnt_umber", "size": 0.02, "direction": 0}])
    codes = [n.code for n in s.notices()]
    assert "direction-given" in codes and "pieces" in codes
    assert not s.history.records


def test_neither_draws_from_the_stream(tmp_path):
    """Both count off the geometry, so a mass laid with them speaking lays what it laid
    before they existed, and so does every mark after it."""
    from easel import session as session_module

    s = make(tmp_path)
    state = s.rng.bit_generator.state
    b = s._resolve_brush("flat", 0.02, None, {})
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        session_module._check_direction_given(s, polygon(FACET, name="facet"), b, 0, 1.0)
        session_module._check_pieces(s, polygon(V, name="collar"), b, 0, 1.0)
    assert [n.code for n in s.notices()] == ["direction-given", "pieces"]
    assert s.rng.bit_generator.state == state
