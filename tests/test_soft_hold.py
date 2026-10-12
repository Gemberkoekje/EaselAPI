"""Step 4 of 0.9.0: a held edge that is soft.

``soft=`` is the painter's answer P2 and, after the bench, 2a and 2b
(``paintings/Claude/uktarl_krannoc/answers.md``, ``answers-step2.md``): **B1**, a smooth
ramp inward from the outline, in the long side's fraction, **per hold** -- a number loses
the mass's own edge and ``clip=`` keeps its own -- and **per stretch**, a run of a shape's
own points that tapers back to the hold's edge over its width past each end.
"""

from __future__ import annotations

import warnings

import numpy as np
import pytest

from easel import Session, ellipse, polygon
from easel.regions import _looks_like_point
from easel.session import PLAN_ACCEPTS, _clips_from_params, _Soft, _softs_from_params


def make(tmp_path, w: int = 320, h: int = 240):
    return Session(w, h, texture="linen", ground="toned_grey", seed=7, out_dir=tmp_path,
                   timelapse=False)


FIGURE = polygon([(0.30, 0.20), (0.70, 0.20), (0.74, 0.80), (0.26, 0.80)], name="figure")
FACE = ellipse((0.5, 0.5), 0.22, 0.30, name="face")
#: A lit plane reaching past the face on three sides: its own left side is the
#: terminator, inside the face; everywhere else the face's outline is what stops it.
LIT = polygon([(0.48, 0.10), (0.90, 0.10), (0.90, 0.90), (0.48, 0.90)], name="lit")
BOX = polygon([(0.25, 0.25), (0.75, 0.25), (0.75, 0.75), (0.25, 0.75)], name="box")


def _smooth(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def _bench_b1(soft: dict):
    """``scripts/probe_uktarl_session.py``'s ``softening`` patch, kind B1, verbatim but
    for the arguments a 0.9.0 ``_clip_cover`` is handed: what the painter chose, blind."""
    def patched(self, holds, feather=0.0, *_):
        w, h = self.canvas.width, self.canvas.height
        cover = None
        for one in holds:
            mask = one.coverage(w, h)
            px = soft.get(tuple(one.points))
            reach = px if px else float(feather) * self.canvas.long_side
            if reach > 0.0:
                rows, cols, depth, full = one._edge_depth(w, h, reach, mask)
                if px and len(rows):
                    d = np.maximum(depth, 0.0).astype(np.float32)
                    f = np.minimum(full, reach).astype(np.float32)
                    ramp = _smooth(d / np.maximum(f, 1e-6))
                    mask[rows, cols] = np.minimum(mask[rows, cols], ramp)
                elif len(rows):
                    inside = depth > 0.0
                    r, c, d = rows[inside], cols[inside], depth[inside]
                    f = np.minimum(full[inside], reach).astype(np.float32)
                    mask[r, c] = np.minimum(mask[r, c], self.canvas.broken_edge(r, c, d, f))
            cover = mask if cover is None else cover * mask
        return cover
    return patched


def _lay(s: Session, verb: str, soft) -> list:
    """One call of ``verb``, held to the figure -- by ``clip=``, or as its own place."""
    if verb == "stroke":
        return [s.stroke([(0.1, 0.5), (0.9, 0.5)], "round_soft", "c", size=0.3,
                         clip=FIGURE, soft=soft)]
    if verb == "dab":
        return [s.dab(0.5, 0.5, "round_hard", "c", size=0.4, press=3, clip=FIGURE,
                      soft=soft)]
    if verb == "smudge":
        return [s.smudge([(0.2, 0.5), (0.8, 0.5)], size=0.03, clip=FIGURE, soft=soft)]
    if verb == "glaze":
        return [s.glaze([(0.1, 0.5), (0.9, 0.5)], "c", size=0.3, clip=FIGURE, soft=soft)]
    if verb == "block_in":
        return s.block_in(FIGURE, "flat", "c", size=0.05, edge="hard", soft=soft)
    if verb == "sweep":
        return s.sweep([(0.1, 0.3), (0.9, 0.3)], "flat", "c", into="down", depth=0.5,
                       size=0.05, clip=FIGURE, soft=soft)
    if verb == "cover":
        return s.cover(FIGURE, "c", size=0.05, soft=soft)
    return s.scumble(FIGURE, "c", "burnt_umber", 4, size=0.05, edge="hard", soft=soft)


@pytest.mark.parametrize("verb", ["stroke", "dab", "smudge", "glaze", "block_in", "sweep",
                                  "cover", "scumble"])
def test_every_verb_that_takes_clip_takes_soft(tmp_path, verb):
    laid = {}
    for soft in (None, 0.03):
        s = make(tmp_path)
        s.palette["c"] = s.palette.mix("cadmium_yellow", "titanium_white", 0.5)
        s.block_in(BOX, "flat", "burnt_umber", size=0.08)              # something to drag
        before = s.canvas.rgb.copy()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            records = _lay(s, verb, soft)
        assert ("soft" in records[0].params["clip"]) == (soft is not None)
        laid[soft] = (s, np.abs(s.canvas.rgb - before).sum(axis=2))
    (crisp, moved), (soft_s, soft_moved) = laid[None], laid[0.03]
    assert crisp.stroke_count == soft_s.stroke_count, "a softness costs no stroke"
    # Just inside the outline the soft hold lets less paint through, and outside it
    # lets none through: what moves there is float32's rounding, crisp or soft.
    w, h = 320, 240
    inside = FIGURE.coverage(w, h) >= 1.0
    rim = inside & ~polygon(FIGURE).inset(0.01).coverage(w, h).astype(bool)
    assert soft_moved[rim].sum() < moved[rim].sum()
    outside = FIGURE.coverage(w, h) == 0.0
    assert soft_moved[outside].max() < 1e-4 and moved[outside].max() < 1e-4


def test_a_soft_hold_is_the_ramp_the_painter_chose_blind(tmp_path, monkeypatch):
    """The bench's B1, patched in as the bench patched it, and the built ``soft=``: one
    canvas, to the pixel -- whole, alone and beside a clip cut on the line."""
    width = 8.0
    for clip, feather in ((None, None), (FACE, 0)):
        built = make(tmp_path)
        built.block_in(LIT, "flat", "titanium_white", size=0.03, edge="hard", solid=True,
                       clip=clip, feather=feather, soft=built.px_size(width))
        bench = make(tmp_path)
        with monkeypatch.context() as m:
            m.setattr(Session, "_clip_cover", _bench_b1({tuple(LIT.points): width}))
            bench.block_in(LIT, "flat", "titanium_white", size=0.03, edge="hard",
                           solid=True, clip=clip, feather=feather)
        assert np.array_equal(built.canvas.rgb, bench.canvas.rgb)


def _row(mask: np.ndarray, y: float) -> np.ndarray:
    return mask[int(y * mask.shape[0])]


def _ramp_px(profile: np.ndarray) -> int:
    """How many pixels of a profile lie strictly between no paint and all of it."""
    return int(((profile > 0.02) & (profile < 0.98)).sum())


def test_a_number_loses_the_mass_own_edge_and_clip_keeps_its_own(tmp_path):
    s = make(tmp_path, 400, 300)
    held = (LIT, FACE)
    crisp = s._clip_cover(held, 0.002)
    soft = s._clip_cover(held, 0.002, (), (_Soft(0, s.px_size(10)),))
    row = _row(soft, 0.5)
    left, right = int(0.48 * 400), int(0.72 * 400)
    # The terminator -- the lit plane's own edge, inside the face -- fades over ~10 px.
    assert _ramp_px(row[left - 2:left + 14]) >= 6
    assert _ramp_px(_row(crisp, 0.5)[left - 2:left + 14]) <= 3
    # The face's outline, where the plane runs past it, keeps the edge a hold cuts.
    assert np.array_equal(row[right - 6:right + 4], _row(crisp, 0.5)[right - 6:right + 4])


def test_a_stretch_loses_its_side_and_tapers_back_over_its_width(tmp_path):
    s = make(tmp_path, 400, 400)
    w = s.px_size(12)
    crisp = s._clip_cover((BOX,), 0.002)
    soft = s._clip_cover((BOX,), 0.002, (), (_Soft(0, w, tuple(BOX.closed[1:3])),))
    x0, x1, y0 = 100, 300, 100            # the box's left and right sides, and its top
    mid = soft[200]
    assert _ramp_px(mid[x1 - 16:x1 + 2]) >= 8, "the right side fades over its width"
    assert np.array_equal(mid[x0 - 4:x0 + 16], crisp[200][x0 - 4:x0 + 16]), "the left stays"
    # Along the top, the softness tapers back from the corner: on the line over its
    # width, and a pixel ``d`` in over the width and ``d`` more, so the corner is
    # rounded rather than creased. Past that the edge is the crisp one again.
    depth = 6
    along = [float(soft[y0 + depth, x1 - k]) for k in range(1, 20)]
    assert along[0] < 0.6 < along[13]
    assert all(b >= a - 1e-6 for a, b in zip(along, along[1:], strict=False))
    assert np.array_equal(soft[y0 - 4:y0 + 20, x0:x1 - 26], crisp[y0 - 4:y0 + 20, x0:x1 - 26])
    assert not np.array_equal(soft[y0:y0 + 3, x1 - 12:x1], crisp[y0:y0 + 3, x1 - 12:x1])
    # Deep inside, nothing is lost.
    assert np.array_equal(soft[150:250, 150:250], crisp[150:250, 150:250])


def test_a_stretch_named_all_the_way_round_is_the_whole_outline(tmp_path):
    s = make(tmp_path)
    w = s.px_size(6)
    whole = s.block_in(BOX, "flat", "burnt_umber", size=0.05, edge="hard",
                       soft=[(BOX.closed, w)])[0]
    same = s.block_in(BOX, "flat", "burnt_umber", size=0.05, edge="hard",
                      soft=[(BOX, w)])[0]
    assert whole.params["clip"]["soft"] == same.params["clip"]["soft"] == [
        {"hold": 0, "width": w}]
    backwards = s.block_in(BOX, "flat", "burnt_umber", size=0.05, edge="hard",
                           soft=(BOX.closed[3:0:-1], w))[0]
    assert backwards.params["clip"]["soft"][0]["run"] == [list(p) for p in BOX.closed[3:0:-1]]


def test_a_soft_mark_is_logged_so_that_0_8_0_refuses_it(tmp_path):
    """A new key would be dropped by 0.8.0's replay, which would lay the edge hard. The
    softness goes into the clip's mapping, which 0.8.0 fails to read as an outline."""
    s = make(tmp_path)
    s.palette["c"] = s.palette.mix("cadmium_yellow", "titanium_white", 0.5)
    rec = s.block_in(LIT, "flat", "c", size=0.05, edge="hard", clip=FACE,
                     soft=[(LIT.closed[3:5], s.px_size(9))])[0]
    held = rec.params["clip"]
    assert set(held) == {"in", "soft"} and len(held["in"]) == 2
    assert held["soft"] == [{"hold": 0, "width": s.px_size(9),
                             "run": [list(p) for p in LIT.closed[3:5]]}]
    assert _softs_from_params(held) == (_Soft(0, s.px_size(9), tuple(LIT.closed[3:5])),)

    def read_as_0_8_0(held):                 # v0.8.0's _clips_from_params, verbatim
        many = bool(held) and not _looks_like_point(held[0])
        return tuple(polygon([(float(x), float(y)) for x, y in one])
                     for one in (held if many else [held]))

    with pytest.raises(KeyError):
        read_as_0_8_0(held)
    assert len(_clips_from_params(held)) == 2
    # With an exclusion beside it, all three ride in the one mapping.
    both = s.stroke([(0.1, 0.5), (0.9, 0.5)], "flat", "c", size=0.05, clip=LIT,
                    clip_out=FIGURE, soft=s.px_size(4))
    assert set(both.params["clip"]) == {"in", "out", "soft"}
    # A softness of nothing is not logged at all, and lays what no softness lays.
    plain = s.stroke([(0.1, 0.5), (0.9, 0.5)], "flat", "c", size=0.05, clip=LIT, soft=0)
    assert isinstance(plain.params["clip"][0][0], float)

    again = Session.load(s.save(tmp_path / "p.easel"))
    assert np.array_equal(again.replay().canvas.rgb, s.canvas.rgb)
    s.thumbnail(size=120)                    # the masses laid, read back flat


def test_soft_zero_loses_nothing(tmp_path):
    a, b = make(tmp_path), make(tmp_path)
    a.block_in(FIGURE, "flat", "burnt_umber", size=0.05, edge="hard")
    b.block_in(FIGURE, "flat", "burnt_umber", size=0.05, edge="hard", soft=0)
    assert np.array_equal(a.canvas.rgb, b.canvas.rgb)
    b.stroke([(0.1, 0.5), (0.9, 0.5)], soft=0)        # a helper's zero, on a free mark


def test_a_softness_draws_nothing_from_the_stream(tmp_path):
    a, b = make(tmp_path), make(tmp_path)
    ra = a.block_in(FIGURE, "flat", "burnt_umber", size=0.05, edge="hard")
    rb = b.block_in(FIGURE, "flat", "burnt_umber", size=0.05, edge="hard",
                    soft=b.px_size(8))
    assert [r.params["rng"] for r in ra] == [r.params["rng"] for r in rb]
    assert [r.index for r in ra] == [r.index for r in rb]


@pytest.mark.parametrize("call, says", [
    (lambda s: s.stroke([(0.1, 0.5), (0.9, 0.5)], soft=0.01), "holds it to none"),
    (lambda s: s.block_in(FIGURE, soft=0.01), "holds it to none"),
    (lambda s: s.stroke([(0.1, 0.5), (0.9, 0.5)], clip=[LIT, FACE], soft=0.01),
     "none of them its own"),
    (lambda s: s.block_in(FIGURE, edge="hard", soft=[(FACE, 0.01)]), "not an outline"),
    (lambda s: s.block_in(FIGURE, edge="hard", soft=[(FIGURE.closed[1:3:-1], 0.01)]),
     "was handed"),
    (lambda s: s.block_in(FIGURE, edge="hard", soft=[([(0.31, 0.2), (0.7, 0.2)], 0.01)]),
     "not a run"),
    (lambda s: s.stroke([(0.1, 0.5), (0.9, 0.5)], clip=LIT, clip_out=FIGURE,
                        soft=[(FIGURE, 0.01)]), "cut on the line"),
    (lambda s: s.block_in(FIGURE, edge="hard", soft=8), "long side"),
    (lambda s: s.block_in(FIGURE, edge="hard", soft=-0.01), "zero or more"),
    (lambda s: s.block_in(FIGURE, edge="hard", soft="wide"), "s.px_size"),
    (lambda s: s.block_in(FIGURE, edge="hard", soft=[(FIGURE, 0.01), (FIGURE, 0.02)]),
     "twice"),
    (lambda s: s.cover(FIGURE, "burnt_umber", soft=[(FACE, 0.01)]), "not an outline"),
    (lambda s: s.scumble(FIGURE, "burnt_umber", "titanium_white", 4, soft=0.01),
     "holds it to none"),
])
def test_what_soft_refuses_it_refuses_before_any_paint(tmp_path, call, says):
    s = make(tmp_path)
    with pytest.raises(ValueError, match=says):
        call(s)
    assert s.stroke_count == 0 and not s.history.records


def test_a_plan_takes_soft_as_the_verbs_do(tmp_path):
    assert all("soft" in PLAN_ACCEPTS[kind] for kind in PLAN_ACCEPTS)
    s = make(tmp_path)
    plan = [{"shape": FIGURE, "brush": "flat", "color": "burnt_umber", "size": 0.05,
             "edge": "hard", "soft": s.px_size(6)},
            {"shape": BOX, "brush": "flat", "color": "titanium_white", "size": 0.05,
             "edge": "hard", "soft": [(BOX.closed[0:2], s.px_size(6))]}]
    price = s.cost(plan)
    s.rehearse(plan)
    laid = s.paint(plan)
    assert s.stroke_count == len(laid) == price
    assert all("soft" in r.params["clip"] for r in laid)
