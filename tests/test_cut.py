"""Step 11 of 0.9.0: a piece cut out of its canvas -- K, N and M1, as The Curator's painter chose.

Its answers (``paintings/Claude/the_curator/answers.md`` and ``answers-step2.md``): **one
declaration, ``s.plan(cut=place)``**, which the checklist reads inside and the export takes
its alpha from; **the cut's edge as a held paint edge falls**, the places' coverage at four
samples a side softened to 0.85 px, ``soften=`` in pixels; **``export(size=)``** for a small
piece painted large; and **inside a cut, every line measured inside it** -- the ground as
canvas with nothing laid on it and its fringe along the edge, with no floor, and a line for
the cut's own edge.
"""

from __future__ import annotations

import math
import warnings

import numpy as np
import pytest
from PIL import Image

from easel import Region, Session, difference, ellipse, polygon
from easel.plan import Plan
from easel.session import _soft_edge, _soften_sigma


def make(tmp_path, w: int = 320, h: int = 400) -> Session:
    return Session(w, h, ground="toned_grey", seed=4, out_dir=tmp_path, timelapse=False)


FIGURE = ellipse((0.5, 0.5), 0.3, 0.32, name="figure")


def painted(tmp_path, w: int = 320, h: int = 400) -> Session:
    """A figure laid solid past its outline, the canvas round it left bare."""
    s = make(tmp_path, w, h)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.block_in(FIGURE.scaled(1.06), "flat", "burnt_umber", size=0.05, solid=True,
                   direction="axis")
    return s


# -- the declaration -----------------------------------------------------------------------
def test_the_plan_holds_the_cut_and_says_it(tmp_path):
    s = make(tmp_path)
    plan = s.plan(cut=FIGURE)
    assert [one.name for one in plan.cut] == ["figure"]
    assert "cut: figure" in str(plan)
    hood = ellipse((0.5, 0.2), 0.1, 0.08, name="hood")
    assert [one.name for one in s.plan(cut=[FIGURE, hood]).cut] == ["figure", "hood"]
    assert s.plan(values={FIGURE: 0.2}).cut == s.plan().cut      # left off, kept
    assert s.plan(cut=[]).cut == ()                               # [] takes it back


def test_a_cut_round_a_hole_is_a_difference(tmp_path):
    s = make(tmp_path)
    arch = ellipse((0.5, 0.45), 0.2, 0.25, name="arch")
    plan = s.plan(cut=difference(Region(0.0, 0.0, 1.0, 1.0), arch, name="the wall"))
    inside = plan.inside_cut(*s.size)
    assert not inside[int(0.45 * 400), int(0.5 * 320)]          # the arch is cut away
    assert inside[5, 5]                                          # the wall ships


def test_a_cut_off_the_canvas_is_refused(tmp_path):
    sliver = polygon([(0.0001, 0.0001), (0.0012, 0.0001), (0.0001, 0.0011)])
    with pytest.raises(ValueError, match="covers no pixels"):
        make(tmp_path).plan(cut=sliver)


def test_the_cut_survives_the_file(tmp_path):
    s = make(tmp_path)
    s.plan(cut=difference(Region(0.0, 0.0, 1.0, 1.0), FIGURE, name="the wall"))
    s.save(tmp_path / "p.easel")
    back = Session.load(tmp_path / "p.easel")
    assert back.plan() == s.plan()
    # A plan written before 0.9.0 has no cut, and opens as it did.
    assert Plan.from_json({"why": "a wall"}).cut == ()


# -- the alpha -------------------------------------------------------------------------------
def test_an_export_with_a_cut_carries_its_alpha(tmp_path):
    s = painted(tmp_path)
    s.plan(cut=FIGURE)
    img = np.asarray(Image.open(s.export(tmp_path / "cut.png")))
    assert img.shape == (400, 320, 4)
    assert img[200, 160, 3] == 255 and img[5, 5, 3] == 0
    whole = Image.open(s.export(tmp_path / "whole.png", alpha=False))
    assert whole.mode == "RGB"
    assert np.array_equal(np.asarray(whole), img[..., :3])


def test_an_export_without_a_cut_is_whole_unless_it_names_one(tmp_path):
    s = painted(tmp_path)
    assert Image.open(s.export(tmp_path / "a.png")).mode == "RGB"
    named = np.asarray(Image.open(s.export(tmp_path / "b.png", alpha=FIGURE)))
    assert named.shape[2] == 4 and named[5, 5, 3] == 0
    with pytest.raises(ValueError, match="declares none"):
        s.export(tmp_path / "c.png", alpha=True)
    with pytest.raises(ValueError, match="writes no alpha"):
        s.export(tmp_path / "d.png", soften=2.5)


def test_soften_is_a_width_in_pixels_and_never_negative(tmp_path):
    s = painted(tmp_path)
    s.plan(cut=FIGURE)
    with pytest.raises(ValueError, match="0 or more"):
        s.export(tmp_path / "e.png", soften=-1)
    raw = np.asarray(Image.open(s.export(tmp_path / "raw.png", soften=0)))[..., 3]
    soft = np.asarray(Image.open(s.export(tmp_path / "soft.png", soften=2.5)))[..., 3]
    band = lambda a: int(((a >= 0.1 * 255) & (a <= 0.9 * 255)).sum())  # noqa: E731
    assert band(soft) > 2 * band(raw)


def _slant_band(sigma_soften: float) -> float:
    """The band between 10% and 90% over a straight edge's length, at a slant."""
    n, k, slant = 96, 4, math.radians(60.0)
    sub = (np.arange(n * k) + 0.5) / k
    xs, ys = np.meshgrid(sub, sub)
    cover = (ys > math.tan(slant) * (xs - n / 2) + n / 2).reshape(n, k, n, k).mean(axis=(1, 3))
    alpha = _soft_edge(cover.astype(np.float32), sigma_soften)[16:80, :]
    return float(((alpha >= 0.1) & (alpha <= 0.9)).sum()) / ((n - 32) / math.sin(slant))


@pytest.mark.parametrize("width", [1.5, 2.5, 3.0])
def test_soften_is_the_width_a_slanted_edge_reads(width):
    assert _slant_band(width) == pytest.approx(width, abs=0.06)


def test_the_default_is_the_painters_held_edge():
    """0.85 px sits on the measure's first step: the softening at a sigma of 0.38, the
    patron's own 0.39."""
    assert _soften_sigma(0.85) == pytest.approx(0.383, abs=0.01)
    assert 0.77 < _slant_band(0.85) <= 1.01
    assert _soften_sigma(0.0) == 0.0


# -- painted large, exported small ----------------------------------------------------------
def test_size_reduces_and_keeps_the_proportions(tmp_path):
    s = painted(tmp_path, 480, 600)
    assert Image.open(s.export(tmp_path / "a.png", size=300)).size == (240, 300)
    assert Image.open(s.export(tmp_path / "b.png", size=(160, 200))).size == (160, 200)
    with pytest.raises(ValueError, match="proportions"):
        s.export(tmp_path / "c.png", size=(200, 200))
    with pytest.raises(ValueError, match="smaller than the painting and not larger"):
        s.export(tmp_path / "d.png", size=1200)


def test_the_alpha_is_built_at_the_size_that_ships(tmp_path):
    big = painted(tmp_path, 640, 800)
    small = painted(tmp_path, 320, 400)
    for s in (big, small):
        s.plan(cut=FIGURE)
    reduced = np.asarray(Image.open(big.export(tmp_path / "big.png", size=(320, 400))))
    own = np.asarray(Image.open(small.export(tmp_path / "small.png")))
    assert np.array_equal(reduced[..., 3], own[..., 3])


# -- the check, inside the cut --------------------------------------------------------------
def test_the_checklist_reads_inside_the_cut(tmp_path):
    s = painted(tmp_path)
    whole = s.checklist()
    assert "of the canvas is still bare ground" in whole
    assert "check the background hardest" in whole
    s.plan(cut=FIGURE)
    cut = s.checklist()
    assert "ground: 0.00% of the cut has nothing laid on it, 0.00% of the 2 px along its edge" \
        in cut
    assert "bare ground" not in cut and "check the background hardest" not in cut
    assert "cut: its edge is " in cut
    values = next(line for line in cut.splitlines() if line.strip().startswith("values:"))
    assert values.split()[1].startswith("0.1")        # the umber alone, not the bare canvas


def test_a_planned_place_outside_the_cut_is_named_and_not_counted(tmp_path):
    s = painted(tmp_path)
    corner = Region(0.0, 0.0, 0.15, 0.12, name="corner")
    s.plan(cut=FIGURE, values={FIGURE: 0.15, corner: 0.6})
    line = next(ln for ln in s.checklist().splitlines() if ln.strip().startswith("plan:"))
    assert line.strip() == "plan: 1 of 1 places inside 0.10; outside the cut: corner"


def test_bare_canvas_along_the_edge_is_the_fringe(tmp_path):
    """Painted short of its outline, a piece shows the ground's colour round it."""
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.block_in(FIGURE.scaled(0.9), "flat", "burnt_umber", size=0.05, solid=True,
                   direction="axis")
    s.plan(cut=FIGURE)
    line = next(ln for ln in s.checklist().splitlines() if ln.strip().startswith("ground:"))
    share, fringe = (float(part.split("%")[0].split()[-1]) for part in line.split(","))
    assert fringe > 50.0 and share > 1.0


def test_a_pass_reads_inside_the_cut_too(tmp_path):
    s = painted(tmp_path)
    s.plan(cut=FIGURE)
    report = s.report()
    assert "of the cut has nothing laid on it" in report and "cut: its edge is" in report
