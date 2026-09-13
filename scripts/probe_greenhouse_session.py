"""The measurements behind the greenhouse sessions' list in SUGGESTIONS.md.

Three painters were handed one subject -- a lighthouse half way through becoming a
greenhouse -- and left three request lists beside their paintings under
``paintings/lighthouse_greenhouse/``. Two of the three carried probes of their own;
this script re-measures every claim the round was built on, on the engine as it now
is, and prints the numbers quoted in ``CALIBRATION.md``, ``SUGGESTIONS.md`` and the
docstrings the round changed.

Where a probe below repeats a painter's own, it says whose, and the painter's file
stays where it is: this is the version that runs against the fixed engine and prints
the *before* beside the *after* wherever the before can still be reproduced.

    python scripts/probe_greenhouse_session.py          # writes out/probe_greenhouse_*.png
"""

from __future__ import annotations

import hashlib
import tempfile
import warnings
from pathlib import Path

import numpy as np

import easel.session as session_module
from easel import Session, cell, polygon, span
from easel.color import luminance

OUT = Path("out")


def new(width: int = 1024, height: int = 768, ground: str = "toned_warm_grey",
        seed: int = 47) -> Session:
    return Session(width, height, texture="linen", ground=ground, seed=seed,
                   timelapse=False, out_dir=OUT)


def painted(s: Session) -> np.ndarray:
    """Where paint has landed: a pixel more than a little off the ground it started on."""
    ground = s.canvas.rgb[:4].reshape(-1, 3).mean(axis=0)
    return np.abs(s.canvas.rgb - ground).sum(axis=2) > 0.03


# -- 1. the clean contour, before and after ---------------------------------------------
def _spline_spine(edge, closed, spacing, smooth=True):
    """The contour as it was swept until 0.2.0: through a spline, whatever was asked."""
    return _raw_spine(edge, closed, spacing, True)


_raw_spine = session_module._sweep_spine


def top_above(shape, top_edge: float, ground: str, spline: bool, **block_kw) -> float:
    """How many pixels of paint stand above the shape's top edge, in its own x-band.

    Fable's ``probe_clean_contour.py`` measurement, with the old contour available
    on request: ``spline=True`` puts the spline back for one call.
    """
    s = new(ground=ground, seed=3)
    session_module._sweep_spine = _spline_spine if spline else _raw_spine
    try:
        s.block_in(shape, "flat", "burnt_umber", size=0.02, density=1.0, solid=True,
                   direction=90, **block_kw)
    finally:
        session_module._sweep_spine = _raw_spine
    band = painted(s)[:, int(shape.box.x0 * 1024):int(shape.box.x1 * 1024)]
    rows = np.nonzero(band.any(axis=1))[0]
    return (top_edge - rows.min() / 768) * 768


def probe_clean_contour() -> None:
    print("\n== the contour of edge='clean', through a spline and along the edges ==")
    print("  1024x768 linen, flat at size=0.02, solid, vertical passes. Pixels of paint")
    print("  standing above the shape's top edge; the ragged fill's half-brush is ~3px.")
    cases = [
        ("a fresh four-cornered tower (Fable)", "toned_grey", 0.20,
         [(0.30, 0.90), (0.40, 0.90), (0.38, 0.20), (0.32, 0.20)]),
        ("lighthouse_dusk's own tower()", "burnt_sienna", 0.165,
         [(0.228, 0.630), (0.312, 0.630), (0.297, 0.165), (0.243, 0.165)]),
        ("a tower tapering 0.20 to 0.07 (Sonnet)", "cool_grey", 0.18,
         [(0.30, 0.92), (0.50, 0.92), (0.435, 0.18), (0.365, 0.18)]),
    ]
    print(f"  {'shape':40s} {'ragged':>7} {'clean, spline':>14} {'clean, edges':>13}")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for name, ground, top, pts in cases:
            shape = polygon(pts)
            ragged = top_above(shape, top, ground, False, edge="ragged")
            before = top_above(shape, top, ground, True, edge="clean")
            after = top_above(shape, top, ground, False, edge="clean")
            print(f"  {name:40s} {ragged:6.0f}px {before:13.0f}px {after:12.0f}px")
    print("  read: the arch was the spline bowing through two sparse corners; along the")
    print("        polygon's own edges the contour stops where the fill does.")


# -- 2. what a clean edge takes off a narrow mass -----------------------------------------
def probe_clean_narrow() -> None:
    print("\n== edge='clean' on a mass narrow relative to its brush ==")
    print("  Opus's lantern cap, 0.214 x 0.036, 1120x860 linen, flat, solid, direction='axis'.")
    print("  'share' is the brush over the cap's shorter extent in the brush's own unit;")
    print("  'kept' is the area the half-brush inset leaves to fill; 'covered' is the")
    print("  share of the cap's pixels that got paint, ragged and clean; 'corners' the")
    print("  same over the outer 8% of its width at either end.")
    cap = polygon([(0.148, 0.114), (0.362, 0.114), (0.302, 0.078), (0.208, 0.078)],
                  name="cap")
    w, h = 1120, 860
    mask = cap.mask(w, h)
    ys, xs = np.nonzero(mask)
    x0, x1 = xs.min(), xs.max()
    span_px = x1 - x0
    corner = mask & ((xs.min() + 0.08 * span_px > np.arange(w))[None, :]
                     | (xs.max() - 0.08 * span_px < np.arange(w))[None, :])
    short = min(cap.width * w / max(w, h), cap.height * h / max(w, h))
    print(f"  {'size':>6} {'share':>6} {'kept':>6} {'covered ragged':>15} {'clean':>6} "
          f"{'corners ragged':>15} {'clean':>6} {'spill ragged':>13} {'clean':>6}")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for size in (0.004, 0.006, 0.008, 0.010, 0.012, 0.016, 0.020):
            row = [size, size / short, cap.inset(size / 2).area / cap.area]
            got = {}
            for edge in ("ragged", "clean"):
                s = Session(w, h, texture="linen", ground="toned_warm_grey", seed=41,
                            timelapse=False, out_dir=OUT)
                s.block_in(cap, "flat", "burnt_umber", size=size, density=1.0,
                           solid=True, direction="axis", edge=edge)
                on = painted(s)
                got[edge] = (float(on[mask].mean()), float(on[corner].mean()),
                             float((on & ~mask).sum() / mask.sum()))
            print(f"  {row[0]:6.3f} {row[1]:6.0%} {row[2]:6.0%} {got['ragged'][0]:15.0%} "
                  f"{got['clean'][0]:6.0%} {got['ragged'][1]:15.0%} {got['clean'][1]:6.0%} "
                  f"{got['ragged'][2]:13.0%} {got['clean'][2]:6.0%}")
    print("  read: the warning fires past a quarter of the shorter extent.")


# -- 3. the chisel staircase (Opus, probe 1) ------------------------------------------------
def horizontal_edge_share(s: Session, box, pad: float = 0.01) -> tuple[float, int]:
    """Share of the strong edges in a region that run within 10 degrees of horizontal.

    Opus's own measure: the Sobel measure ``CALIBRATION.md``'s *Laying a mass along
    its own axis* table is built on. Higher is squarer; a staircase is a run of
    horizontal edges where the mass has no horizontal feature.
    """
    img = np.asarray(s.canvas.to_srgb8(impasto=True), dtype=np.float32) / 255.0
    h, w, _ = img.shape
    grey = luminance(img.reshape(-1, 3) ** 2.2).reshape(h, w)
    x0, y0, x1, y1 = (int((box.x0 - pad) * w), int((box.y0 - pad) * h),
                      int((box.x1 + pad) * w), int((box.y1 + pad) * h))
    g = grey[max(y0, 1):min(y1, h - 1), max(x0, 1):min(x1, w - 1)]
    gy, gx = np.gradient(g)
    mag = np.hypot(gx, gy)
    strong = mag > max(np.percentile(mag, 90), 1e-4)
    ang = np.degrees(np.arctan2(np.abs(gx[strong]), np.abs(gy[strong])))
    return float((ang < 10.0).mean()), int(strong.sum())


def lit_face():
    return polygon([(0.303, 0.268), (0.307, 0.400), (0.311, 0.540), (0.318, 0.680),
                    (0.330, 0.820), (0.344, 0.905), (0.398, 0.940), (0.384, 0.820),
                    (0.368, 0.680), (0.357, 0.540), (0.348, 0.400), (0.340, 0.258)]
                   ).smooth(3)


def probe_staircase() -> None:
    print("\n== the chisel staircase: a solid tip's pass ends on a sloping boundary ==")
    print("  Opus's lit band: 0.06 x 0.64, boundaries ~3 degrees off vertical, 1120x860")
    print("  linen on toned_warm_grey, vertical passes, laid solid. Share of strong edges")
    print("  within 10 degrees of horizontal -- the mass has none, so all of it is the tool's.")
    face = lit_face()
    print(f"  {'tip':11s} {'size':>6} {'horizontal edges':>17} {'strong px':>10}")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for brush, size in (("flat", 0.020), ("flat", 0.010), ("knife", 0.020),
                            ("bristle", 0.022), ("bristle", 0.012), ("round_hard", 0.020)):
            s = Session(1120, 860, texture="linen", ground="toned_warm_grey", seed=41,
                        timelapse=False, out_dir=OUT)
            s.palette["v"] = s.palette.at_value(
                s.palette.mix("yellow_ochre", "viridian", 0.30), 0.25)
            s.block_in(face, brush, "v", size=size, density=1.0, solid=True,
                       opacity=1.0, pressure="even", direction=90)
            share, n = horizontal_edge_share(s, face.box)
            print(f"  {brush:11s} {size:6.3f} {share:16.0%} {n:10d}")
    print("  read: the chisel tips put horizontal edges into a mass that has none; the")
    print("        comb does not, and neither does a round tip. Same shape, same passes.")


# -- 4. direction left off (Opus, probe 3) -------------------------------------------------
def probe_direction() -> None:
    print("\n== a shaped block_in with direction left off ==")
    mid = polygon([(0.222, 0.266), (0.216, 0.400), (0.208, 0.540), (0.198, 0.680),
                   (0.186, 0.820), (0.176, 0.905), (0.354, 0.905), (0.340, 0.820),
                   (0.328, 0.680), (0.321, 0.540), (0.317, 0.400), (0.313, 0.268)]
                  ).smooth(3)
    vine = polygon([(0.19, 0.13), (0.32, 0.13), (0.32, 0.22), (0.19, 0.22)])
    s = Session(1120, 860, texture="linen", ground="toned_warm_grey", seed=41,
                timelapse=False, out_dir=OUT)
    print(f"  {'mass':24s} {'axis':>6} {'90':>6} {'left off':>9} {'ratio':>7}  warns")
    for name, shape, size in (("the tower's mid plane", mid, 0.027),
                              ("the tower's lit band", lit_face(), 0.022),
                              ("the vine mass (wider)", vine, 0.030)):
        base = {"shape": shape, "brush": "flat", "size": size, "density": 1.0}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            axis = s.cost(dict(base, direction="axis"), share=0)
            vert = s.cost(dict(base, direction=90), share=0)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            dflt = s.cost(base, share=0)
        fired = any("direction= left off" in str(c.message) for c in caught)
        print(f"  {name:24s} {axis:6d} {vert:6d} {dflt:9d} {dflt / max(axis, 1):6.1f}x  "
              f"{'yes' if fired else 'no'}")
    print("  read: the warning at 2.5x fires on the two masses that were nearly paid for")
    print("        at 3.9x and 11x, and not on the one that is wider than it is tall.")


# -- 5. a banded scumble across a wedge (Sonnet) -------------------------------------------
def probe_wedge() -> None:
    print("\n== scumble's auto-sized brush on a wedge ==")
    print("  Sonnet's beam: a wedge 0.045 across at the mouth and 0.42 at the far edge,")
    print("  1024x768 linen on cool_grey, n=8, direction='vertical' -- the passes run")
    print("  across the wedge and step along it. Paint outside the outline, as a share")
    print("  of the wedge's own area, by which half of the wedge it fell beside.")
    wedge = polygon([(0.64, 0.28), (0.64, 0.325), (0.0, 0.62), (0.0, 0.20)], name="beam")
    w, h = 1024, 768
    mask = wedge.mask(w, h)
    xs = np.arange(w)[None, :]
    mouth_half = (xs >= 0.32 * w)
    print(f"  {'size':>8} {'steps':>6} {'bloom, mouth half':>18} {'far half':>9}  warns")
    for size in (None, 0.10, 0.05):
        s = new(ground="cool_grey", seed=74)
        s.palette["a"] = s.palette.at_value("burnt_umber", 0.45)
        s.palette["b"] = s.palette.at_value("titanium_white", 0.75)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            recs = s.scumble(wedge, "a", "b", 8, direction="vertical", size=size)
        laid = recs[0].params["size"]
        step = wedge.width / 8
        on = painted(s)
        outside = on & ~mask
        area = mask.sum()
        fired = any("width varies" in str(c.message) for c in caught)
        print(f"  {laid:8.3f} {laid / step:6.1f} {(outside & mouth_half).sum() / area:18.0%} "
              f"{(outside & ~mouth_half).sum() / area:9.0%}  {'yes' if fired else 'no'}")
    first, last = session_module._pass_lengths(wedge, 90.0, 8)
    print(f"  the passes run {first:.3f} long at one end and {last:.3f} at the other:")
    print("  read: picked for the step, the brush is wider than the whole mouth, and the")
    print("        bloom is all at that end. The warning names both lengths.")


# -- 6. the chroma the engine lays ---------------------------------------------------------
def probe_chroma() -> None:
    print("\n== does the engine lay the chroma it was given? ==")
    print("  512x384 linen on toned_warm_grey, a mass 0.60x0.30 laid solid, flat at 0.03.")
    print("  Oklab chroma of the mixture, of the paint sampled over the mass, and of the")
    print("  rendered view of it; and the ground's, for the contrast the eye sees.")
    print(f"  {'mixture':28s} {'mixed':>6} {'paint':>6} {'view':>6} {'ground':>7}")
    for name, mix in (("yellow_ochre + viridian 0.3", ("yellow_ochre", "viridian", 0.30)),
                      ("cadmium_red + white 0.4", ("cadmium_red", "titanium_white", 0.40)),
                      ("cerulean + umber 0.5", ("cerulean", "burnt_umber", 0.50)),
                      ("ultramarine + white 0.6", ("ultramarine", "titanium_white", 0.60))):
        s = Session(512, 384, texture="linen", ground="toned_warm_grey", seed=5,
                    timelapse=False, out_dir=OUT)
        p = s.palette
        p["m"] = p.mix(*mix)
        ground = p.chroma_of(s.sample())
        s.block_in((0.20, 0.35, 0.80, 0.65), "flat", "m", size=0.03, solid=True)
        inner = (0.23, 0.38, 0.77, 0.62)
        print(f"  {name:28s} {p.chroma_of('m'):6.3f} {p.chroma_of(s.sample(inner)):6.3f} "
              f"{p.chroma_of(s.sample(inner, rendered=True)):6.3f} {ground:7.3f}")
    print("  read: the paint and the view carry the mixture's own chroma; what reads")
    print("        more vivid than the number is the eye, judging it against the field.")


# -- 7. the pairs a value plan puts within 0.10 (Opus, probe 4) -----------------------------
def probe_pairs() -> None:
    print("\n== the pairs inside a written value plan ==")
    plan = {span("A1", "H2").__class__(0.0, 0.0, 1.0, 0.25, "fog high"): 0.58,
            span("A1", "H2").__class__(0.0, 0.25, 1.0, 0.40, "fog low"): 0.68,
            cell("B4").__class__(0.10, 0.30, 0.30, 0.40, "beam"): 0.75,
            span("A1", "H2").__class__(0.0, 0.40, 1.0, 0.55, "sea far"): 0.54,
            span("A1", "H2").__class__(0.0, 0.55, 1.0, 0.75, "sea near"): 0.40,
            cell("B4").__class__(0.0, 0.75, 0.5, 1.0, "rock"): 0.21,
            cell("B4").__class__(0.25, 0.30, 0.35, 0.90, "tower"): 0.40,
            cell("B4").__class__(0.20, 0.15, 0.32, 0.25, "vines"): 0.26}
    s = new()
    table = str(s.compare(plan))
    lines = table.splitlines()
    start = next(i for i, ln in enumerate(lines) if "planned within" in ln)
    for ln in lines[start:start + 5]:
        print("  " + ln)
    print("  read: four pairs of twenty-eight, on the empty canvas, before a stroke.")


# -- 8. undo, and where the generator stands afterwards ------------------------------------
def probe_undo() -> None:
    print("\n== undo, in-process and through the session file ==")
    print("  320x240, seed 5: a mass, then a mark or a second mass, undone, then a third")
    print("  mass -- against the same third mass laid straight after the first.")

    def h(s):
        return hashlib.sha256(s.canvas.rgb.tobytes()).hexdigest()[:12]

    def base():
        s = Session(320, 240, seed=5, timelapse=False, out_dir=OUT)
        s.palette["c"] = s.palette.mix("ultramarine", "burnt_umber", 0.4)
        return s

    shape = polygon([(0.1, 0.1), (0.6, 0.15), (0.5, 0.7), (0.15, 0.6)])

    def third(s):
        s.block_in(shape, "bristle", "c", size=0.04, direction="axis")

    clean = base()
    clean.block_in(shape, "flat", "c", size=0.05)
    third(clean)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s = base()
        s.block_in(shape, "flat", "c", size=0.05)
        s.stroke([(0.2, 0.2), (0.8, 0.8)], "bristle", "c")
        s.undo(1)
        third(s)
        print(f"  in-process, a mark undone:        {'identical' if h(s) == h(clean) else 'DRIFTS'}")
        s = base()
        s.block_in(shape, "flat", "c", size=0.05)
        n = len(s.block_in(shape, "knife", "c", size=0.05))
        s.undo(n)
        third(s)
        print(f"  in-process, a whole mass undone:  {'identical' if h(s) == h(clean) else 'DRIFTS'}")
        d = tempfile.mkdtemp()
        s = base()
        s.block_in(shape, "flat", "c", size=0.05)
        s.stroke([(0.2, 0.2), (0.8, 0.8)], "bristle", "c")
        s.save(f"{d}/a.easel")
        t = Session.load(f"{d}/a.easel")
        t.undo(1)
        t.save(f"{d}/a.easel")
        u = Session.load(f"{d}/a.easel")
        third(u)
        print(f"  through the file, as `easel undo`: {'identical' if h(u) == h(clean) else 'DRIFTS'}")
    print("  read: every mark carries the generator's state at the start of its call,")
    print("        and the log keeps its points exactly, so both paths put the painting")
    print("        back where a clean rebuild has it.")


# -- 9. which free verbs touch the stream (Fable, probe_rng) ------------------------------
def probe_free_verbs() -> None:
    print("\n== which free verbs change the marks laid after them ==")
    print("  400x300, seed 9: one bristle stroke, laid after each verb, hashed.")

    def build(pre):
        s = Session(400, 300, texture="linen", ground="toned_grey", seed=9,
                    timelapse=False, out_dir=OUT)
        s.palette["c"] = s.palette.mix("ultramarine", "burnt_umber", 0.4)
        plan = [{"points": [(0.1, 0.5), (0.9, 0.5)], "brush": "bristle", "color": "c",
                 "size": 0.08}]
        {"none": lambda: None, "look": lambda: s.look(),
         "values": lambda: s.look(values=True), "preview": lambda: s.preview(plan),
         "rehearse": lambda: s.rehearse(plan), "cost": lambda: s.cost(plan),
         "compare": lambda: s.compare({"all": 0.3}),
         "pencil": lambda: s.pencil([(0.1, 0.1), (0.9, 0.9)]),
         "dry": lambda: s.dry(), "erase": lambda: s.erase()}[pre]()
        s.stroke([(0.1, 0.5), (0.9, 0.5)], "bristle", "c", size=0.08)
        return hashlib.sha256(s.canvas.rgb.tobytes()).hexdigest()[:12]

    base_hash = build("none")
    for pre in ("look", "values", "preview", "rehearse", "cost", "compare",
                "pencil", "dry", "erase"):
        same = build(pre) == base_hash
        print(f"  {pre:9s} {'leaves it' if same else 'CHANGES it'}")
    print("  read: the planning verbs are free of side effects. pencil, dry and erase")
    print("        are logged, and a mark's texture is seeded from its place in the")
    print("        log -- so adding or removing one shifts every later mark. It is the")
    print("        log index, not the stream; deterministic, and worth knowing.")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    probe_clean_contour()
    probe_clean_narrow()
    probe_staircase()
    probe_direction()
    probe_wedge()
    probe_chroma()
    probe_pairs()
    probe_undo()
    probe_free_verbs()
    print()


if __name__ == "__main__":
    main()
