"""Step 3 of 0.9.0: paint held out of a shape, a place with a hole to read, and a
rehearsal's look shaped as ``easel look`` shapes one.

``clip_out=`` is the painter's answer P1 (``paintings/Claude/uktarl_krannoc/answers.md``):
the paint lands where ``clip=`` allows and none of ``clip_out=`` reaches, and the
exclusion's edge is cut on the line. ``difference()`` is for places that are read, and
every verb that lays paint refuses one.
"""

from __future__ import annotations

import numpy as np
import pytest
from PIL import Image

from easel import Session, difference, ellipse, polygon, span
from easel.cli import main
from easel.regions import Difference, _looks_like_point
from easel.session import _clips_from_params


def make(tmp_path):
    return Session(320, 240, texture="linen", ground="toned_grey", seed=7,
                   out_dir=tmp_path, timelapse=False)


FIGURE = ellipse((0.5, 0.5), 0.12, 0.25, name="figure")
WALL = polygon([(0.08, 0.1), (0.92, 0.1), (0.92, 0.9), (0.08, 0.9)], name="wall")


def _moved(s, before) -> np.ndarray:
    return np.abs(s.canvas.rgb - before).sum(axis=2) > 1e-4


def _wholly(shape, s) -> np.ndarray:
    return shape.coverage(s.canvas.width, s.canvas.height) >= 1.0


@pytest.mark.parametrize("verb", ["stroke", "dab", "smudge", "glaze", "block_in", "sweep",
                                  "cover", "scumble"])
def test_every_verb_that_takes_clip_takes_clip_out(tmp_path, verb):
    s = make(tmp_path)
    s.palette["c"] = s.palette.mix("cadmium_yellow", "titanium_white", 0.5)
    s.block_in(span("A1", "H8"), "flat", "burnt_umber", size=0.08)   # something to drag
    before = s.canvas.rgb.copy()
    lay = {
        "stroke": lambda: s.stroke([(0.1, 0.5), (0.9, 0.5)], "round_soft", "c",
                                   size=0.3, clip_out=FIGURE),
        "dab": lambda: s.dab(0.5, 0.5, "round_hard", "c", size=0.3, press=3,
                             clip_out=FIGURE),
        "smudge": lambda: s.smudge([(0.3, 0.5), (0.7, 0.5)], size=0.02, clip_out=FIGURE),
        "glaze": lambda: s.glaze([(0.1, 0.5), (0.9, 0.5)], "c", size=0.3, clip_out=FIGURE),
        "block_in": lambda: s.block_in(WALL, "flat", "c", size=0.05, edge="hard",
                                       clip_out=FIGURE),
        "sweep": lambda: s.sweep([(0.1, 0.3), (0.9, 0.3)], "flat", "c", into="down",
                                 depth=0.5, size=0.05, clip_out=FIGURE),
        "cover": lambda: s.cover(WALL, "c", size=0.05, clip_out=FIGURE),
        "scumble": lambda: s.scumble(WALL, "c", "burnt_umber", 4, size=0.05,
                                     clip_out=FIGURE),
    }[verb]
    lay()
    moved = _moved(s, before)
    assert moved.any(), "the call lays paint"
    assert not (moved & _wholly(FIGURE, s)).any(), "and none of it inside the figure"


def _rings(shape, w: int, h: int, reach: int) -> np.ndarray:
    """How many pixels out from ``shape`` each pixel lies, counted in 4-steps."""
    cur = shape.coverage(w, h) > 0.0
    out = np.full((h, w), reach + 1)
    for k in range(1, reach + 1):
        grown = cur.copy()
        grown[1:] |= cur[:-1]
        grown[:-1] |= cur[1:]
        grown[:, 1:] |= cur[:, :-1]
        grown[:, :-1] |= cur[:, 1:]
        out[grown & ~cur] = k
        cur = grown
    return out


def test_the_exclusion_is_cut_on_the_line_and_leaves_no_seam(tmp_path):
    """Broken into the light, the exclusion's edge is the seam the painter found: a few
    pixels of the darker ground between the light and the figure. Cut on the line, the
    paint just outside the figure reads as the wall further out does, and the call
    costs what the hold alone costs."""
    held = make(tmp_path)
    out = make(tmp_path)
    for s in (held, out):
        s.palette["c"] = s.palette.mix("cadmium_yellow", "titanium_white", 0.5)
    held.block_in(WALL, "flat", "c", size=0.05, edge="hard")
    out.block_in(WALL, "flat", "c", size=0.05, edge="hard", clip_out=FIGURE)
    assert held.stroke_count == out.stroke_count
    rings = _rings(FIGURE, 320, 240, 24)
    rim = out.palette.value_of(out.canvas.rgb[rings <= 3].mean(axis=0))
    wall = out.palette.value_of(out.canvas.rgb[(rings > 6) & (rings <= 24)].mean(axis=0))
    ground = out.palette.value_of(make(tmp_path).canvas.rgb.mean(axis=(0, 1)))
    assert wall - ground > 0.2
    assert rim > wall - 0.02


def test_a_held_out_mark_is_logged_so_that_0_8_0_refuses_it(tmp_path):
    """A new key would be dropped by 0.8.0's replay, which would lay the mark through
    the figure. The clip becomes a mapping, which 0.8.0 fails to read as an outline."""
    s = make(tmp_path)
    s.palette["c"] = s.palette.mix("cadmium_yellow", "titanium_white", 0.5)
    rec = s.block_in(WALL, "flat", "c", size=0.05, edge="hard", clip_out=FIGURE)[0]
    held = rec.params["clip"]
    assert set(held) == {"in", "out"} and len(held["in"]) == 1 and len(held["out"]) == 1
    # One hold without an exclusion is logged as it always was.
    plain = s.stroke([(0.1, 0.5), (0.9, 0.5)], "flat", "c", size=0.05, clip=WALL)
    assert isinstance(plain.params["clip"][0][0], float)

    def read_as_0_8_0(held):                 # v0.8.0's _clips_from_params, verbatim
        many = bool(held) and not _looks_like_point(held[0])
        return tuple(polygon([(float(x), float(y)) for x, y in one])
                     for one in (held if many else [held]))

    with pytest.raises(KeyError):
        read_as_0_8_0(held)
    assert len(_clips_from_params(held)) == 1

    path = s.save(tmp_path / "p.easel")
    again = Session.load(path)
    assert np.array_equal(again.replay().canvas.rgb, s.canvas.rgb)


def test_clip_out_alone_holds_nothing_in_so_a_feather_is_refused(tmp_path):
    s = make(tmp_path)
    with pytest.raises(ValueError, match="holds it to none"):
        s.stroke([(0.1, 0.5), (0.9, 0.5)], "flat", "burnt_umber", size=0.05,
                 clip_out=FIGURE, feather=0.002)
    with pytest.raises(ValueError, match="clip_out="):
        s.stroke([(0.1, 0.5), (0.9, 0.5)], "flat", "burnt_umber", clip_out=object())


def test_a_difference_is_read_and_never_painted(tmp_path):
    s = make(tmp_path)
    seen = difference(WALL, FIGURE, name="wall seen")
    assert isinstance(seen, Difference)
    assert not seen.contains(0.5, 0.5) and seen.contains(0.15, 0.15)
    assert seen.area == pytest.approx(WALL.area - FIGURE.area, abs=0.005)
    assert seen.shifted(0.01, 0.0).holes[0].center[0] == pytest.approx(
        FIGURE.center[0] + 0.01)
    for paint in (lambda: s.block_in(seen, "flat", "burnt_umber"),
                  lambda: s.cover(seen, "burnt_umber"),
                  lambda: s.scumble(seen, "burnt_umber", "titanium_white", 4),
                  lambda: s.sweep(seen, "flat", "burnt_umber"),
                  lambda: s.stroke([(0.1, 0.5), (0.9, 0.5)], clip=seen),
                  lambda: s.stroke([(0.1, 0.5), (0.9, 0.5)], clip_out=seen),
                  lambda: s.block_in(WALL, clip=[WALL, seen])):
        with pytest.raises(ValueError, match="clip_out="):
            paint()
    assert s.stroke_count == 0
    with pytest.raises(ValueError, match="took everything"):
        difference(FIGURE, WALL)


def test_a_difference_reads_only_what_is_left_and_survives_the_file(tmp_path):
    s = make(tmp_path)
    s.palette["light"] = s.palette.mix("cadmium_yellow", "titanium_white", 0.8)
    s.palette["dark"] = s.palette.mix("burnt_umber", "ultramarine", 0.4)
    s.block_in(FIGURE, "flat", "dark", size=0.04, edge="hard", solid=True)
    s.block_in(WALL, "flat", "light", size=0.05, edge="hard", clip_out=FIGURE,
               solid=True)
    seen = difference(WALL, FIGURE, name="wall")
    wall_value = s.palette.value_of(s.sample(seen))
    assert wall_value > s.palette.value_of(s.sample(WALL))
    s.plan(values={seen: 0.8})
    again = Session.load(s.save(tmp_path / "p.easel"))
    assert again._plan == s._plan
    assert isinstance(again._plan.values[0].outline, Difference)
    # The thumbnail of the masses laid fills the wall round the figure, as it was laid.
    thumb = Image.open(s.thumbnail(size=160)).convert("L")
    w, h = thumb.size
    assert thumb.getpixel((w // 2, h // 2)) < thumb.getpixel((w // 8, h // 8)) - 60


def test_a_rehearsals_look_takes_easel_looks_flags(tmp_path, capsys):
    session = tmp_path / "p.easel"
    assert main(["new", str(session), "--size", "320x240", "--out-dir",
                 str(tmp_path / "out")]) == 0
    script = tmp_path / "pass.py"
    script.write_text('s.mark("sun", 0.5, 0.5)\n'
                      's.block_in("D5", "flat", "burnt_umber", size=0.06)\n')
    capsys.readouterr()
    flags = ["--region", "C3:F6", "--no-marks", "--no-sketch", "--scale", "100"]
    assert main(["run", str(session), str(script), "--rehearse", *flags]) == 0
    rehearsed = capsys.readouterr().out.strip().splitlines()[-1]
    assert main(["look", str(session), *flags]) == 0
    looked = capsys.readouterr().out.strip().splitlines()[-1]
    assert Image.open(rehearsed).size == Image.open(looked).size
    assert main(["run", str(session), str(script), "--rehearse"]) == 0
    plain = capsys.readouterr().out.strip().splitlines()[-1]
    assert Image.open(plain).size != Image.open(rehearsed).size
    other = tmp_path / "other.py"
    other.write_text(script.read_text())
    assert main(["run", str(session), str(script), str(other), "--alternatives",
                 "--region", "C3:F6", "--scale", "80"]) == 0
    capsys.readouterr()
    # A run that writes no look refuses the flags rather than ignoring them.
    for extra in ([], ["--count"], ["--alternatives", "--count"]):
        assert main(["run", str(session), str(script), "--region", "C3:F6",
                     *extra]) != 0
        assert "writes none" in capsys.readouterr().err
    assert Session.load(session).stroke_count == 0
