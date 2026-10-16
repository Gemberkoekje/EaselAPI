"""Step 6 of 0.9.0, workstream E: a thing drawn in its own frame, and shapes turned in pixels.

As the painter of Uktarl's Room asked (``paintings/Claude/uktarl_krannoc/answers.md``, D):

- **``s.frame(centre, rx, ry, tilt=)``** with ``.at()``, ``.polygon()`` and ``.arc()``,
  which replaces its ``hp()``, ``dp()`` and ``ah()`` point for point -- each was a centre,
  two radii and a tilt -- and its outlines, with its own warps kept its own;
- **``.rotated()`` on shapes and groups**, clockwise as ``rotate=`` is on ``ellipse()``,
  and **turned in pixels whatever unit they are handed**: turned in fractions on its 4:3
  canvas, a square came back at 23.4 degrees with a 104-degree corner. A shape does not
  know its canvas, so ``aspect=`` is required, and its absence raises and names the fix.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from easel import (
    Frame,
    Region,
    Session,
    cell,
    difference,
    ellipse,
    group,
    polygon,
)

W, H = 1024, 768


def make(tmp_path, w: int = W, h: int = H) -> Session:
    return Session(w, h, texture="linen", ground="toned_grey", seed=7, out_dir=tmp_path,
                   timelapse=False)


# -- the painter's three heads, as its prelude.py wrote them, in pixels -------------------
def _head(centre, rx, ry, tilt_deg):
    """``hp()``, ``dp()`` and ``ah()`` are this, with other constants."""
    cx, cy = centre
    t = math.radians(tilt_deg)

    def at(u, v):
        return (cx + u * rx * math.cos(t) - v * ry * math.sin(t),
                cy + u * rx * math.sin(t) + v * ry * math.cos(t))
    return at


HEADS = {
    "hp": ((512, 344), 24, 34, -6),     # Uktarl's head
    "dp": ((752, 482), 22, 33, -8),     # the doppelganger's
    "ah": ((188, 496), 22, 31, 7),      # the left bandit's
}

#: Every local point the prelude hands its three helpers, a head's features and planes.
LOCAL = [(0.96, -0.46), (0.50, -0.33), (0.0, -0.28), (-0.50, -0.25), (-0.97, -0.20),
         (-0.42, -0.10), (0.42, -0.15), (-0.34, 0.52), (0.18, 0.55), (-0.74, -0.24),
         (-1.62, -0.66), (1.58, -0.70), (0.30, -0.98), (0.20, 0.86), (-0.12, -0.98),
         (0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]


def _head_arc(at, t0, t1, n):
    """``head_arc()``: Uktarl's outline, narrowing toward a pointed chin."""
    pts = []
    for i in range(n + 1):
        t = math.radians(t0 + (t1 - t0) * i / n)
        below = max(0.0, math.sin(t))
        pts.append(at(math.cos(t) * (1 - 0.30 * below ** 1.5),
                      math.sin(t) * (1 + 0.06 * below)))
    return pts


@pytest.mark.parametrize("helper", sorted(HEADS))
def test_the_frame_is_the_painters_helper_point_for_point(tmp_path, helper):
    """In pixels through ``s.px``, which is how the painter would write it, and in
    fractions typed as fractions: the same places either way."""
    s = make(tmp_path)
    centre, rx, ry, tilt = HEADS[helper]
    at = _head(centre, rx, ry, tilt)
    in_pixels = s.frame(s.px(*centre), *s.px(rx, ry), tilt=tilt)
    in_fractions = s.frame((centre[0] / W, centre[1] / H), rx / W, ry / H, tilt=tilt)
    for frame in (in_pixels, in_fractions):
        for u, v in LOCAL:
            assert frame.at(u, v) == pytest.approx(s.px(*at(u, v)), abs=1e-12)
            assert frame.at((u, v)) == frame.at(u, v), "a pair is taken too"


def test_an_outline_and_a_plane_share_their_edge_without_retyping(tmp_path):
    """The prelude's ``uk_head_poly`` and ``uk_face_lit``: an arc of the head's outline,
    warped by the painter's own taper, and the terminator's points, so the lit plane's
    edge lies on the head's. ``arc()`` gives the outline's points in the frame's units,
    and the warp stays the painter's, as it asked."""
    s = make(tmp_path)
    at = _head(*HEADS["hp"])
    head = s.frame(s.px(512, 344), *s.px(24, 34), tilt=-6)

    def chin(points):
        return [(u * (1 - 0.30 * max(0.0, v) ** 1.5), v * (1 + 0.06 * max(0.0, v)))
                for u, v in points]

    shape = head.polygon(chin(head.arc(0, 360, 40))[:-1], name="Uktarl's head")
    painted = polygon([s.px(*p) for p in _head_arc(at, 0, 360, 40)[:-1]])
    assert np.allclose(shape.points, painted.points, atol=1e-12)
    assert shape.name == "Uktarl's head"

    term = [(0.96, -0.46), (0.50, -0.33), (0.0, -0.28), (-0.50, -0.25), (-0.97, -0.20)]
    lit = head.polygon(chin(head.arc(-26, 168, 20)) + term[::-1][1:-1])
    painted_lit = polygon([s.px(*p) for p in
                           _head_arc(at, -26, 168, 20) + [at(*q) for q in term][::-1][1:-1]])
    assert np.allclose(lit.points, painted_lit.points, atol=1e-12)


def test_an_arc_is_its_ends_and_its_steps_clockwise_from_the_right(tmp_path):
    head = make(tmp_path).frame((0.5, 0.5), 0.1, 0.1)
    arc = head.arc(0, 90, 3)
    assert len(arc) == 4, "n steps, both ends included"
    assert arc[0] == pytest.approx((1.0, 0.0)) and arc[-1] == pytest.approx((0.0, 1.0))
    assert head.at(*arc[-1])[1] > 0.5, "90 degrees is the bottom: v runs downward"
    with pytest.raises(ValueError, match="one step"):
        head.arc(0, 90, 0)


# -- turning in pixels ---------------------------------------------------------------------
def _angles(points, w, h):
    """The top edge's angle, the first corner, and two sides, all in pixels."""
    p = np.asarray(points) * [w, h]
    top, side = p[1] - p[0], p[-1] - p[0]
    angle = math.degrees(math.atan2(top[1], top[0]))
    corner = math.degrees(math.acos(np.dot(top, side)
                                    / np.linalg.norm(top) / np.linalg.norm(side)))
    return angle, corner, float(np.linalg.norm(top)), float(np.linalg.norm(side))


@pytest.mark.parametrize("degrees", [6, 30, -45, 90])
def test_a_square_turned_on_a_canvas_that_is_not_square_stays_square(tmp_path, degrees):
    """The painter's measurement: a 100 px square turned 30 degrees in fractions on
    1024x768 came back at 23.4 degrees, with a 104-degree corner and sides of 94 and
    109 px. Turned in pixels it comes back at 30, square, 100 by 100."""
    s = make(tmp_path)
    square = polygon([s.px(462, 334), s.px(562, 334), s.px(562, 434), s.px(462, 434)])
    angle, corner, top, side = _angles(square.rotated(degrees, aspect=s.aspect).points, W, H)
    assert angle == pytest.approx(degrees, abs=1e-9)
    assert corner == pytest.approx(90.0, abs=1e-9)
    assert top == pytest.approx(100.0) and side == pytest.approx(100.0)


def test_a_frame_tilted_on_a_canvas_standing_up_keeps_its_right_angles(tmp_path):
    s = make(tmp_path, 768, 1024)
    head = s.frame(s.px(300, 400), *s.px(40, 60), tilt=30)
    o, right, down = (np.asarray(head.at(*p)) * [768, 1024]
                      for p in ((0, 0), (1, 0), (0, 1)))
    assert np.dot(right - o, down - o) == pytest.approx(0.0, abs=1e-9)
    assert np.linalg.norm(right - o) == pytest.approx(40.0)
    assert np.linalg.norm(down - o) == pytest.approx(60.0)
    assert math.degrees(math.atan2(*(right - o)[::-1])) == pytest.approx(30.0)


def test_a_shape_does_not_know_its_canvas_so_the_turn_asks_for_it():
    """Required, not defaulted: a default would turn in fractions, which is the skew."""
    shape = polygon(cell("D4"))
    for turned in (shape, cell("D4"), group(shape, (0.5, 0.5)),
                   difference(cell("D4"), ellipse((0.45, 0.45), 0.01, 0.01))):
        with pytest.raises(TypeError, match=r"aspect=s\.aspect"):
            turned.rotated(30)
    with pytest.raises(ValueError, match="above zero"):
        shape.rotated(30, aspect=0)


def test_clockwise_as_rotate_is_on_ellipse(tmp_path):
    """On a square canvas fractions are pixels, and the two turns agree."""
    turned = ellipse((0.5, 0.5), 0.2, 0.1).rotated(30, aspect=1.0)
    assert np.allclose(turned.points, ellipse((0.5, 0.5), 0.2, 0.1, rotate=30).points)


def test_the_point_named_stays_put_and_a_full_turn_comes_back(tmp_path):
    s = make(tmp_path)
    shape = polygon([s.px(400, 300), s.px(520, 310), s.px(470, 420)], name="lid")
    hinge = s.px(400, 300)
    turned = shape.rotated(-12, about=hinge, aspect=s.aspect)
    assert turned.points[0] == pytest.approx(hinge)
    assert turned.name == "lid"
    assert np.allclose(shape.rotated(360, aspect=s.aspect).points, shape.points)
    about_middle = shape.rotated(40, aspect=s.aspect)
    assert about_middle.center == pytest.approx(shape.center, abs=1e-12)
    assert shape.rotated(40, about=cell("A1"), aspect=s.aspect).points == \
        shape.rotated(40, about=cell("A1").center, aspect=s.aspect).points


def test_a_region_turns_into_a_shape_and_a_difference_keeps_its_holes(tmp_path):
    s = make(tmp_path)
    box = Region(*s.px(400, 300), *s.px(500, 360))
    turned = box.rotated(20, aspect=s.aspect)
    assert turned.points == polygon(box).rotated(20, aspect=s.aspect).points
    angle, corner, _, _ = _angles(turned.points, W, H)
    assert angle == pytest.approx(20.0) and corner == pytest.approx(90.0)

    hole = ellipse(s.px(450, 330), *s.px(10, 10))
    seen = difference(box, hole, name="wall")
    turned = seen.rotated(20, about=s.px(450, 330), aspect=s.aspect)
    assert turned.name == "wall" and len(turned.holes) == 1
    assert np.allclose(turned.holes[0].points,
                       polygon(hole).rotated(20, about=s.px(450, 330),
                                             aspect=s.aspect).points)


def test_a_group_turns_about_one_point_and_its_points_turn_with_it(tmp_path):
    """Every part about the same point, so the parts keep their places relative to each
    other -- as ``scaled()`` does -- and a point among them comes back a point."""
    s = make(tmp_path)
    head = polygon([s.px(480, 300), s.px(540, 300), s.px(540, 380), s.px(480, 380)])
    brow = Region(*s.px(490, 320), *s.px(530, 330))
    eye = s.px(500, 340)
    pivot = s.px(510, 400)
    t_head, t_brow, t_eye = group(head, brow, eye).rotated(15, about=pivot,
                                                           aspect=s.aspect)
    assert np.allclose(t_head.points, head.rotated(15, about=pivot, aspect=s.aspect).points)
    assert np.allclose(t_brow.points, brow.rotated(15, about=pivot, aspect=s.aspect).points)
    assert isinstance(t_eye, tuple) and len(t_eye) == 2
    eye_frame = s.frame(pivot, *s.px(1, 1), tilt=15)
    du, dv = (eye[0] - pivot[0]) * W, (eye[1] - pivot[1]) * H
    assert t_eye == pytest.approx(eye_frame.at(du, dv), abs=1e-12)
    # About the group's middle when no point is named, as `scaled()` is.
    g = group(head, eye)
    assert np.allclose(g.rotated(15, aspect=s.aspect)[0].points,
                       head.rotated(15, about=g.center, aspect=s.aspect).points)


# -- the frame's own checks ----------------------------------------------------------------
def test_radii_typed_in_pixels_are_told_to_go_through_px(tmp_path):
    """The painter's own sketch of the call was ``s.frame(s.px(512, 344), 24, 34,
    tilt=-6)``: radii in pixels, which as fractions are 24 canvases wide."""
    s = make(tmp_path)
    with pytest.raises(ValueError, match=r"\*s\.px\(24, 34\)"):
        s.frame(s.px(512, 344), 24, 34, tilt=-6)
    with pytest.raises(ValueError, match="above zero"):
        s.frame((0.5, 0.5), 0.0, 0.1)
    with pytest.raises(TypeError, match="aspect"):
        Frame((0.5, 0.5), 0.1, 0.1)


def test_one_radius_is_round_in_pixels_and_a_place_names_the_centre(tmp_path):
    s = make(tmp_path)
    wheel = s.frame(cell("D4"), s.px(30, 0)[0])
    assert wheel.centre == pytest.approx(cell("D4").center)
    o = np.asarray(wheel.at(0, 0)) * [W, H]
    assert np.linalg.norm(np.asarray(wheel.at(1, 0)) * [W, H] - o) == pytest.approx(30.0)
    assert np.linalg.norm(np.asarray(wheel.at(0, 1)) * [W, H] - o) == pytest.approx(30.0)


def test_a_frame_lays_nothing_and_takes_no_place_in_the_log(tmp_path):
    """Drawing helpers: a frame and a turn touch neither the log nor the random stream."""
    s = make(tmp_path)
    state = s.rng.bit_generator.state
    head = s.frame(s.px(512, 344), *s.px(24, 34), tilt=-6)
    head.polygon(head.arc(0, 360, 12)[:-1]).rotated(10, aspect=s.aspect)
    assert not s.history.records
    assert s.rng.bit_generator.state == state
