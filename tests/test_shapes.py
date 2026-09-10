"""M8: masses that are not rectangles.

Every named place in this engine used to be an axis-aligned rectangle, and that
turned out not to be cosmetic: told only what the tool was mechanically good at,
six fresh sessions in eight justified their choice of subject by horizontal bands
and rectangles in as many words (``rehearsal3/unprompted/``). A band was the only
mass ``block_in`` filled honestly, so bands were what got painted.

So the assertions here are mostly about the silhouette: that a shaped block-in
stops at its own boundary, that a pass across a concave shape comes back in pieces
instead of painting over the bite, and that a rectangle still paints exactly what it
always did. And, because the outline can come off the photograph instead of out of
the painter, that a traced one says so where the write-up cannot miss it.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from easel import Session
from easel.regions import (
    Polygon,
    Region,
    as_place,
    as_region,
    blob,
    cell,
    ellipse,
    hull,
    polygon,
    ribbon,
)


def make(tmp_path, **kw):
    kw.setdefault("timelapse", False)
    return Session(300, 240, texture="linen", ground="white", seed=4, out_dir=tmp_path,
                   **kw)


def painted(s: Session) -> np.ndarray:
    """Where paint actually landed, as a boolean mask of the canvas."""
    return s.canvas.rgb.mean(axis=2) < 0.86


#: A shape with a bite out of it: the left half runs to the bottom, the middle is
#: cut away, the right half runs to the bottom again.
NOTCHED = polygon([(0.10, 0.10), (0.90, 0.10), (0.90, 0.90), (0.62, 0.90),
                   (0.62, 0.45), (0.38, 0.45), (0.38, 0.90), (0.10, 0.90)],
                  name="notched")


# --------------------------------------------------------------------------------------
# The shape itself
# --------------------------------------------------------------------------------------
def test_a_shape_knows_its_bounds_its_area_and_its_middle():
    square = polygon([(0.2, 0.2), (0.6, 0.2), (0.6, 0.8), (0.2, 0.8)])
    assert square.bounds == pytest.approx((0.2, 0.2, 0.6, 0.8))
    assert square.area == pytest.approx(0.4 * 0.6)
    assert square.center == pytest.approx((0.4, 0.5))
    assert square.axis == pytest.approx(90.0, abs=1.0)      # taller than it is wide
    assert square.point(0.5, 0.5) == pytest.approx((0.4, 0.5))


def test_two_points_are_not_a_shape_and_the_error_says_what_to_do():
    with pytest.raises(ValueError) as exc:
        polygon([(0.2, 0.2), (0.6, 0.6)])
    assert "ribbon" in str(exc.value), "the error did not point at the way to do this"


def test_points_on_one_line_are_not_a_shape():
    with pytest.raises(ValueError):
        polygon([(0.1, 0.5), (0.4, 0.5), (0.9, 0.5)])


def test_a_shape_is_kept_on_the_canvas():
    """A mass that runs off the edge is normal. Points off the canvas are not."""
    big = polygon([(-0.5, -0.5), (1.6, -0.2), (1.4, 1.7), (-0.3, 1.2)])
    assert big.bounds == pytest.approx((0.0, 0.0, 1.0, 1.0))


def test_a_closed_outline_and_an_open_one_are_the_same_shape():
    pts = [(0.2, 0.2), (0.7, 0.3), (0.5, 0.8)]
    assert polygon(pts).points == polygon([*pts, pts[0]]).points


def test_what_the_shape_contains_is_what_its_mask_covers():
    shape = blob((0.5, 0.5), 0.3, 0.22, seed=7)
    mask = shape.mask(400, 300)
    assert mask.sum() / mask.size == pytest.approx(shape.area, abs=0.005)
    assert shape.contains(*shape.center)
    assert not shape.contains(0.02, 0.02)


def test_inset_stays_inside_the_shape_and_a_negative_one_grows_it():
    """Two masses meeting at the same depth want the near one held off the seam by
    half a brush -- the same reason ``Region.inset`` exists."""
    shape = blob((0.5, 0.5), 0.3, 0.25, seed=2)
    smaller = shape.inset(0.04)
    bigger = shape.inset(-0.04)
    assert smaller.area < shape.area < bigger.area
    assert all(shape.contains(x, y) for x, y in smaller.points), \
        "the inset shape left the original"


def test_insetting_past_the_middle_leaves_a_sliver_rather_than_raising():
    """A painter mid-painting should not get an exception for asking for too much
    margin. Region.inset has always behaved this way; so does a shape."""
    tiny = ellipse((0.5, 0.5), 0.05).inset(0.4)
    assert tiny.area < 0.001
    assert tiny.center == pytest.approx((0.5, 0.5), abs=0.02)


def test_a_shape_carries_its_name_and_where_it_came_from_through_a_reshape():
    traced = Polygon(((0.2, 0.2), (0.8, 0.3), (0.5, 0.9)), name="area 3", traced=True)
    for made in (traced.inset(0.01), traced.scaled(0.8), traced.shifted(0.01, 0.0)):
        assert made.traced and made.name == "area 3"


# --------------------------------------------------------------------------------------
# Building one without doing arithmetic
# --------------------------------------------------------------------------------------
def test_an_ellipse_fills_the_place_it_is_given():
    """``ellipse(cell("D5"))`` is the point: a place the painter read off a look,
    not four numbers it made up."""
    c = cell("D5")
    e = ellipse(c)
    assert e.bounds == pytest.approx(c.bounds, abs=0.005)
    assert e.contains(*c.center)
    assert not e.contains(c.x0 + 0.001, c.y0 + 0.001), "an ellipse filled its corner"


def test_a_blob_is_the_same_silhouette_for_the_same_seed_and_a_different_one_otherwise():
    a = blob((0.5, 0.5), 0.3, seed=5)
    assert a.points == blob((0.5, 0.5), 0.3, seed=5).points
    assert a.points != blob((0.5, 0.5), 0.3, seed=6).points


def test_a_blob_wanders_from_the_ellipse_it_started_as():
    steady = ellipse((0.5, 0.5), 0.3, 0.3, steps=15)
    wandered = blob((0.5, 0.5), 0.3, wobble=0.3, points=15, seed=1)
    radii = [math.hypot(x - 0.5, y - 0.5) for x, y in wandered.points]
    assert max(radii) - min(radii) > 0.05, "the blob came out as round as an ellipse"
    assert wandered.area == pytest.approx(steady.area, rel=0.35)


def test_a_hull_is_the_mass_around_the_landmarks_and_drops_the_ones_inside_it():
    corners = [(0.1, 0.9), (0.5, 0.1), (0.9, 0.85)]
    made = hull([*corners, (0.5, 0.5)])
    assert len(made.points) == 3
    assert set(made.points) == set(corners)
    assert made.contains(0.5, 0.5)


def test_a_hull_can_join_two_shapes():
    a, b = ellipse((0.25, 0.3), 0.1), ellipse((0.75, 0.7), 0.1)
    both = hull([a, b])
    assert both.contains(*a.center) and both.contains(*b.center)
    assert both.area > a.area + b.area


def test_a_ribbon_is_a_mass_of_the_width_asked_for_running_along_the_line():
    line = [(0.1, 0.5), (0.9, 0.5)]
    r = ribbon(line, 0.2)
    assert r.height == pytest.approx(0.2, abs=0.01)
    assert r.contains(0.5, 0.55) and not r.contains(0.5, 0.75)
    tapered = ribbon(line, 0.2, end_width=0.02)
    assert tapered.contains(0.15, 0.55) and not tapered.contains(0.85, 0.55)


def test_a_ribbon_bends_where_its_line_bends():
    r = ribbon([(0.1, 0.8), (0.5, 0.2), (0.9, 0.8)], 0.12)
    assert r.contains(0.5, 0.25), "the ribbon did not follow its middle point"
    assert not r.contains(0.5, 0.7), "the ribbon filled in the bend"


def test_a_region_can_be_used_as_a_shape_and_a_shape_as_a_region():
    r = cell("C3")
    assert polygon(r).bounds == pytest.approx(r.bounds)
    shape = blob((0.4, 0.4), 0.2, seed=3)
    assert as_region(shape).bounds == pytest.approx(shape.bounds)
    assert isinstance(as_place(shape), Polygon)
    assert isinstance(as_place("C3"), Region)


# --------------------------------------------------------------------------------------
# Blocking one in
# --------------------------------------------------------------------------------------
def test_a_shaped_block_in_stops_at_its_silhouette(tmp_path):
    """The whole milestone in one assertion: paint inside the shape, and outside it
    no more than the brush's own spill past the last pass."""
    s = make(tmp_path)
    shape = blob((0.5, 0.5), 0.28, 0.24, seed=2)
    s.block_in(shape, "bristle", "burnt_umber", size=0.09, density=1.0)

    inside = shape.mask(*s.size)
    outside_far = ~shape.inset(-0.06).mask(*s.size)      # further than a brush away
    marks = painted(s)
    assert (marks & inside).sum() > 0.9 * inside.sum(), "the shape did not get filled"
    assert (marks & outside_far).sum() < 0.01 * outside_far.sum(), \
        "paint landed well outside the silhouette"


def test_a_shape_is_not_its_bounding_box(tmp_path):
    """If a shaped mass painted its box there would be nothing here to build."""
    shape = ellipse((0.5, 0.5), 0.35, 0.3)

    def paint(place):
        s = make(tmp_path)
        s.block_in(place, "bristle", "burnt_umber", size=0.09)
        return painted(s)

    # A window just inside the top-left corner of the box, and well clear of the
    # ellipse -- further from it than the brush can spill.
    corner = np.zeros((240, 300), dtype=bool)
    corner[int(0.21 * 240):int(0.26 * 240), int(0.16 * 300):int(0.23 * 300)] = True
    assert (paint(shape.box) & corner).sum() > 0.3 * corner.sum(), \
        "the box left its own corner bare"
    assert (paint(shape) & corner).sum() < 0.01 * corner.sum(), \
        "the shape painted its box's corner"


def test_a_pass_across_a_concave_shape_comes_back_in_pieces(tmp_path):
    """A mass with a bite out of it keeps the bite. One sweep across this shape
    crosses it, leaves it, and crosses it again -- that is two strokes, not one."""
    s = make(tmp_path)
    records = s.block_in(NOTCHED, "flat", "ultramarine", direction="vertical",
                         size=0.07)
    assert len(records) > 12, "a concave sweep laid one stroke per pass"

    notch = np.zeros(s.size[::-1], dtype=bool)
    notch[int(0.52 * 240):int(0.86 * 240), int(0.42 * 300):int(0.58 * 300)] = True
    marks = painted(s)
    assert (marks & notch).sum() < 0.15 * notch.sum(), "the bite got painted over"
    assert (marks & NOTCHED.mask(*s.size)).sum() > 0.9 * NOTCHED.mask(*s.size).sum()


def test_shaped_passes_alternate_direction(tmp_path):
    """Paint runs out along a stroke. Passes that all start at the same edge stack
    their run-out and leave the mass lighter on one side (REVIEW.md finding 12) --
    true of a shaped sweep as much as of a rectangular one."""
    s = make(tmp_path)
    records = s.block_in(ellipse((0.5, 0.5), 0.4, 0.3), "bristle", "burnt_umber",
                         direction="horizontal", size=0.08)
    lefts = [r.points[0][0] < r.points[-1][0] for r in records]
    assert True in lefts and False in lefts, "every pass started at the same edge"


def test_the_axis_direction_sweeps_along_the_mass_and_not_along_the_canvas(tmp_path):
    """A mass laid along the canvas's axes is the loudest tell that nobody chose the
    direction (``rehearsal3/HUMAN_NOTES.md``). ``direction="axis"`` is the shape
    answering that question itself."""
    r = ribbon([(0.15, 0.8), (0.85, 0.25)], 0.16)
    assert r.axis == pytest.approx(-38.0, abs=8.0)

    s = make(tmp_path)
    records = s.block_in(r, "flat", "burnt_umber", direction="axis", size=0.05)
    angles = [math.degrees(math.atan2(rec.points[-1][1] - rec.points[0][1],
                                      rec.points[-1][0] - rec.points[0][0]))
              for rec in records]
    folded = [abs((a + 90) % 180 - 90) for a in angles]
    assert np.median(folded) == pytest.approx(abs(r.axis), abs=10.0), \
        "the passes did not follow the mass's own axis"


def test_a_shape_holds_its_passes_back_to_the_edge_and_a_rectangle_does_not(tmp_path):
    """A rectangle's block-in runs a third of a brush past its edge so the mass does
    not look cropped; a shape's edge is the drawing, so its passes stop. The M6
    assisted run lost the right edge of its subject to that overhang
    (``rehearsal3/assisted/GOTCHAS.md``, gotcha 10)."""
    s = make(tmp_path)
    box = Region(0.3, 0.3, 0.7, 0.7)
    rect = s.block_in(box, "flat", "burnt_umber", direction="horizontal", size=0.08)
    shape = s.block_in(polygon(box), "flat", "burnt_umber", direction="horizontal",
                       size=0.08)
    assert min(p[0] for r in rect for p in r.points) < box.x0 - 0.01
    assert min(p[0] for r in shape for p in r.points) == pytest.approx(box.x0, abs=0.02)


def test_a_shaped_block_in_is_ordinary_strokes_so_undo_and_replay_are_right(tmp_path):
    s = make(tmp_path)
    s.stroke([(0.1, 0.1), (0.9, 0.2)], "bristle", "ultramarine")
    before = s.canvas.rgb.copy()
    records = s.block_in(blob((0.5, 0.6), 0.25, seed=4), "bristle", "burnt_umber",
                         size=0.08)
    assert all(r.kind == "stroke" for r in records)

    assert np.array_equal(s.replay().canvas.to_srgb8(), s.canvas.to_srgb8())
    s.undo(len(records))
    assert np.allclose(s.canvas.rgb, before), "undo did not scrape the mass back off"


def test_the_same_shape_and_seed_paint_the_same_mass(tmp_path):
    def paint():
        s = make(tmp_path)
        s.block_in(blob(cell("D4"), seed=9), "bristle", "burnt_umber", size=0.06)
        return s.canvas.to_srgb8()

    assert np.array_equal(paint(), paint())


def test_an_unknown_direction_still_explains_itself(tmp_path):
    s = make(tmp_path)
    with pytest.raises(ValueError) as exc:
        s.block_in(ellipse((0.5, 0.5), 0.2), direction="sideways")
    assert "axis" in str(exc.value) and "degrees" in str(exc.value)


# --------------------------------------------------------------------------------------
# The rest of the API takes a shape
# --------------------------------------------------------------------------------------
def test_drying_a_shape_leaves_the_paint_around_it_wet(tmp_path):
    s = make(tmp_path)
    s.block_in("all", "bristle", "burnt_umber", size=0.2)
    shape = ellipse((0.3, 0.5), 0.15)
    s.dry(1.0, region=shape)
    mask = shape.mask(*s.size)
    assert float(s.canvas.wetness[mask].max()) == pytest.approx(0.0, abs=1e-6)
    assert float(s.canvas.wetness[~mask].max()) > 0.1, "drying a shape dried its box"


def test_erasing_a_shape_takes_out_only_the_part_of_the_line_inside_it(tmp_path):
    s = make(tmp_path)
    s.pencil([(0.05, 0.5), (0.95, 0.5)], smooth=False)
    s.erase(ellipse((0.5, 0.5), 0.2, 0.2))
    pieces = s.sketch_lines()
    assert len(pieces) == 2, f"expected the line either side of the shape, got {pieces}"
    assert pieces[0][0][0] == pytest.approx(0.05, abs=0.01)
    assert pieces[0][-1][0] == pytest.approx(0.30, abs=0.03)
    assert pieces[1][0][0] == pytest.approx(0.70, abs=0.03)


def test_a_shaped_dry_and_a_shaped_erase_come_back_out_of_the_log(tmp_path):
    """The log is the painting. A shape that only lived in the call would replay as
    a rectangle, or as the whole canvas."""
    s = make(tmp_path)
    s.pencil([(0.05, 0.5), (0.95, 0.5)], smooth=False)
    s.block_in("all", "bristle", "burnt_umber", size=0.2)
    s.dry(1.0, region=ellipse((0.3, 0.5), 0.15))
    s.erase(ellipse((0.5, 0.5), 0.2, 0.2))
    s.stroke([(0.1, 0.8), (0.9, 0.75)], "bristle", "ultramarine")

    again = s.replay()
    assert np.array_equal(again.canvas.to_srgb8(), s.canvas.to_srgb8())
    assert np.allclose(again.canvas.wetness, s.canvas.wetness)
    assert again.sketch_lines() == s.sketch_lines()


def test_a_shape_can_be_looked_at_and_measured_like_any_other_place(tmp_path):
    s = make(tmp_path)
    shape = blob((0.5, 0.5), 0.25, seed=1)
    assert s.look(region=shape, path=tmp_path / "look.png").exists()
    result = s.compare(tmp_path / "look.png", region=shape,
                       path=tmp_path / "cmp.png")
    assert result.cells, "compare had nothing to say about a shape"


def test_preview_draws_the_shape_and_paints_nothing(tmp_path):
    s = make(tmp_path)
    before = s.canvas.rgb.copy()
    shape = blob((0.5, 0.5), 0.25, seed=1)
    path = s.preview([shape, {"points": [(0.1, 0.1), (0.4, 0.3)], "brush": "liner"}],
                     path=tmp_path / "pv.png")
    assert path.exists()
    assert np.array_equal(before, s.canvas.rgb), "preview painted something"
    assert not s.history.records, "preview logged something"


def test_rehearsing_a_mass_shows_the_paint_without_spending_it(tmp_path):
    s = make(tmp_path)
    before = s.canvas.rgb.copy()
    plan = [{"shape": blob((0.5, 0.5), 0.25, seed=1), "brush": "bristle",
             "color": "burnt_umber", "size": 0.08}]
    assert s.rehearse(plan, path=tmp_path / "rh.png").exists()
    assert np.array_equal(before, s.canvas.rgb), "the rehearsal was committed"
    assert not s.history.records

    # What was rehearsed is what lands -- the same mass in the same place. Not the
    # same pixels: a block-in's wander comes from the session's own generator, and
    # the rehearsal deliberately has its own so that trying something does not
    # change the painting that follows it.
    trial = s._trial_session()
    trial.block_in(plan[0]["shape"], "bristle", "burnt_umber", size=0.08)
    s.block_in(plan[0]["shape"], "bristle", "burnt_umber", size=0.08)
    rehearsed, real = painted(trial), painted(s)
    overlap = (rehearsed & real).sum() / max((rehearsed | real).sum(), 1)
    assert overlap > 0.9, f"the rehearsed mass landed somewhere else ({overlap:.2f})"


# --------------------------------------------------------------------------------------
# A shape and a sweep
# --------------------------------------------------------------------------------------
def test_a_shape_can_be_swept_along_its_own_outline(tmp_path):
    """M6c sweeps a boundary; M8 builds shapes. A shape *is* a boundary, and one
    that comes back on itself -- so it goes straight into ``sweep``, and the painter
    does not have to choose between the two milestones."""
    s = make(tmp_path)
    shape = blob((0.5, 0.5), 0.28, 0.24, seed=2)
    records = s.sweep(shape, "bristle", "burnt_umber", depth=0.14, size=0.07)
    assert records and all(r.kind == "stroke" for r in records)

    marks = painted(s)
    inside = shape.mask(*s.size)
    far_out = ~shape.inset(-0.07).mask(*s.size)
    assert (marks & inside).sum() > 0.5 * inside.sum(), "the sweep missed the mass"
    assert (marks & far_out).sum() < 0.01 * far_out.sum(), \
        "the sweep ran outside the shape it was given"
    assert np.array_equal(s.replay().canvas.to_srgb8(), s.canvas.to_srgb8())


def test_sweeping_a_traced_shape_records_it_the_way_blocking_one_in_does(tmp_path):
    s = make(tmp_path)
    traced = Polygon(ellipse((0.5, 0.5), 0.3, 0.25).points, name="area 7", traced=True)
    s.sweep(traced, "bristle", "burnt_umber", depth=0.08, size=0.06)
    assert s.assisted and "area 7" in s.assisted[0]


# --------------------------------------------------------------------------------------
# The traced-copy question
# --------------------------------------------------------------------------------------
def test_the_painters_own_shape_is_not_an_assisted_mode(tmp_path):
    s = make(tmp_path)
    s.block_in(hull([(0.2, 0.2), (0.8, 0.3), (0.5, 0.8)]), "bristle", "burnt_umber",
               size=0.1)
    assert s.assisted == []


def test_a_mass_blocked_in_on_a_traced_outline_says_so(tmp_path):
    """The brief reserves the traced-copy question for the human. A run that answers
    it one way has to say so in the write-up -- so the painting keeps the record."""
    s = make(tmp_path)
    traced = Polygon(((0.2, 0.2), (0.8, 0.3), (0.5, 0.8)), name="area 4", traced=True)
    records = s.block_in(traced, "bristle", "burnt_umber", size=0.1)
    assert s.assisted and "area 4" in s.assisted[0]
    assert "(traced)" in records[0].note
    assert "Assisted" in s.log()


def test_an_area_of_the_prepared_reference_arrives_traced(tmp_path, monkeypatch):
    from easel.prepare import Area, Preparation

    prep = Preparation.__new__(Preparation)
    area = Area(number=1, bounds=(0.2, 0.2, 0.8, 0.8), share=0.2, cells=["D4"],
                value=0.5, hex="#808080",
                outline=[(0.2, 0.2), (0.8, 0.25), (0.6, 0.8)])
    prep._areas = {1: area}
    s = make(tmp_path)
    s._preparation = prep

    assert s.ref_outline(1) == area.outline, "the plain outline changed shape"
    shape = s.ref_shape(1)
    assert shape.traced and shape.name == "area 1"
    assert prep.shape(1).traced


def test_which_assisted_modes_were_used_survives_a_round_trip_through_disk(tmp_path):
    s = make(tmp_path)
    s.block_in(Polygon(((0.2, 0.2), (0.8, 0.3), (0.5, 0.8)), name="area 2", traced=True),
               "bristle", "burnt_umber", size=0.12)
    s.save(tmp_path / "p.easel")
    assert Session.load(tmp_path / "p.easel").assisted == s.assisted
