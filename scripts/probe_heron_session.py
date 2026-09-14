"""The measurements behind the ninth session's two lists in SUGGESTIONS.md.

A grey heron in a flooded parking lot at dawn, painted against ``PAINTER.md`` and its
nine exercises, ``RECIPES.md``, ``REFERENCE.md`` and ``DIAGNOSIS.md`` -- the restricted
arm again, with the symptom index added. It painted the subject twice, and the two
paintings together left four engine items and ten documentation items.

The session's own probes sit beside its paintings
(``paintings/heron_lot/1/probe_seq.py``, ``probe_seq2.py``, ``probe_band.py`` and
``paintings/heron_lot/2/probe_cover.py``); ``probe_band.py`` needs a session file that
is not committed, and the rest run. This script re-measures every claim the round was
built on, on the engine as it now is, and prints the numbers quoted in
``CALIBRATION.md``, ``SUGGESTIONS.md`` and the docstrings the round changed.

**Two of the round's claims did not survive it**, and both probes below print what was
claimed beside what is there:

* *a warning when an oriented tip is handed a ``size`` under about 0.008* -- the
  finding is real and the unit is wrong. The cliff is at four **pixels**, which is a
  different ``size`` on every canvas;
* *the across-band ripple counts canvas texture on a rough ground* -- it does not. The
  metric is insensitive to texture and sensitive to how wide a window it is read
  through.

    python scripts/probe_heron_session.py          # writes nothing
"""

from __future__ import annotations

import ast
import warnings
from pathlib import Path

import numpy as np

from easel import Palette, Region, Session, polygon, span

ROOT = Path(__file__).resolve().parents[1]
MIX, GROUND = 0.865, "#6d635a"


def new(width: int = 1024, height: int = 768, ground: str = "toned_warm_grey",
        seed: int = 17) -> Session:
    return Session(width, height, texture="linen", ground=ground, seed=seed,
                   timelapse=False)


# -- 1. a sequence of directions lays a complete stack per angle ---------------------------
def probe_sequence_stacks() -> None:
    print("\n== direction= given a sequence: the eighth session's guess, measured ==")
    s = new(640, 480, seed=3)
    s.palette["d"] = s.palette.mix("ultramarine", "burnt_umber", 0.45)
    shapes = {
        "wide": polygon([(0.20, 0.42), (0.80, 0.40), (0.80, 0.52), (0.20, 0.54)]),
        "tall": polygon([(0.44, 0.18), (0.56, 0.18), (0.56, 0.78), (0.44, 0.78)]),
    }
    kw = dict(brush="bristle", color="d", size=0.036, density=1.0, solid=True)

    def cost(shape, direction) -> int:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return s.cost([dict(kw, shape=shape, direction=direction)], share=0)

    print(f"  {'mass':>6} {'sequence':>22} {'cost':>6} {'sum of singles':>15} "
          f"{'dearest single':>15}")
    for name, shape in shapes.items():
        singles = {a: cost(shape, a) for a in (0, 30, 60, 90, 120, 150)}
        for seq in ([0, 90], [0, 30, 60, 90], [0, 30, 60, 90, 120, 150]):
            total = cost(shape, seq)
            print(f"  {name:>6} {str(seq):>22} {total:6d} "
                  f"{sum(singles[a] for a in seq):15d} {max(singles.values()):15d}")
    print("  read: the cost is the sum, to the stroke, on every shape and every list.")
    print("        'the stack is sized for the steepest angle in it' was offered as a")
    print("        guess by the eighth session and is wrong.")

    # ...and in paint: whole stacks, one after the other.
    def angles(direction):
        t = s.scratch()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            recs = t.block_in(shapes["wide"], direction=direction, **kw)
        out = []
        for r in recs:
            p = np.asarray(r.points)
            dx = (p[-1, 0] - p[0, 0]) * t.canvas.width
            dy = (p[-1, 1] - p[0, 1]) * t.canvas.height
            out.append(round(float(np.degrees(np.arctan2(dy, dx))) % 180 / 15) * 15 % 180)
        return out

    from collections import Counter
    for direction in (0, 90, [0, 90]):
        got = angles(direction)
        print(f"  direction={str(direction):10s} {len(got):3d} passes, angles "
              f"{dict(sorted(Counter(got).items()))}")
    print("  read: `[0, 90]` is the 0-degree stack whole, then the 90-degree stack whole.")


# -- 2. the bristle floor, against the two paintings that ignored it ----------------------
def probe_bristle_floor() -> None:
    print("\n== the check's bristle floor, and every call site that tripped it ==")

    def scan(root: Path):
        rows = []
        for path in sorted(root.rglob("*.py")):
            for node in ast.walk(ast.parse(path.read_text())):
                if not isinstance(node, ast.Call):
                    continue
                if getattr(node.func, "attr", None) not in ("stroke", "dab"):
                    continue
                kw = {}
                for k in node.keywords:
                    try:
                        kw[k.arg] = ast.literal_eval(k.value)
                    except Exception:
                        pass
                brush = kw.get("brush")
                if brush is None and len(node.args) > 1:
                    try:
                        brush = ast.literal_eval(node.args[1])
                    except Exception:
                        brush = None
                size = kw.get("size")
                if brush == "bristle" and isinstance(size, (int, float)) and size < 0.025:
                    rows.append(kw.get("load"))
        return rows

    for name in ("1", "2"):
        loads = scan(ROOT / "paintings" / "heron_lot" / name)
        named = [v for v in loads if isinstance(v, (int, float))]
        starved = [v for v in named if v <= 0.6]
        print(f"  heron_lot/{name}: {len(loads)} small-bristle call sites, "
              f"{len(named)} naming a load, {len(starved)} of them at or under 0.6, "
              f"{len(loads) - len(named)} at the preset's own 0.9")
    print("  read: not one used the preset's load. The rule now skips a comb starved")
    print("        into the run-out window CALIBRATION.md already publishes, and still")
    print("        fires on a small *loaded* comb -- what it was written for.")

    s = new(400, 300, ground="toned_grey", seed=3)
    s.palette["c"] = s.palette.mix("ultramarine", "burnt_umber", 0.4)
    for load in (0.9, 0.6, 0.35):
        t = s.scratch()
        for i in range(4):
            t.stroke([(0.2, 0.3 + i * 0.1), (0.8, 0.32 + i * 0.1)], "bristle", "c",
                     size=0.012, load=load)
        fired = "fires" if "bristle under" in t.report() else "silent"
        print(f"  four bristle marks at size=0.012, load={load}: {fired}")


# -- 3. a graded passage laid by hand ------------------------------------------------------
def probe_graded_band() -> None:
    print("\n== a hand-laid graded passage, and what the rule does not fire on ==")
    s = new(1024, 768, seed=11)
    p = s.palette
    warm = p.mix("cadmium_red", "yellow_ochre", 0.45)
    for name, v in (("dawn_w", 0.655), ("dawn1", 0.672), ("dawn2", 0.712),
                    ("dawn3", 0.742)):
        p[name] = p.at_value(p.mix(warm, "cerulean", 0.16), v)
    p["dark"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.5), 0.25)
    p["lit"] = p.at_value(p.mix("cerulean", "titanium_white", 0.7), 0.70)

    def fired(build) -> str:
        t = s.scratch()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            build(t)
        line = next((ln for ln in t.report().splitlines() if "stepping colours" in ln), "")
        return line.strip()[2:] if line else ""

    def dawn(t):
        """The session's own dawn band: seven strokes, brushes chosen by hand."""
        for y0, x_end, col, sz, op in (
                (0.2340, 1.07, "dawn_w", 0.058, 0.26), (0.2530, 1.07, "dawn1", 0.052, 0.28),
                (0.2715, 0.86, "dawn2", 0.046, 0.32), (0.2900, 0.72, "dawn3", 0.040, 0.34),
                (0.3080, 0.62, "dawn3", 0.034, 0.32), (0.3260, 0.56, "dawn2", 0.028, 0.30),
                (0.3440, 0.50, "dawn1", 0.024, 0.26)):
            t.stroke([(-0.07, y0 + 0.012), (x_end * 0.28, y0), (x_end, y0 - 0.009)],
                     "bristle", col, size=sz, opacity=op, load=1.0, load_falloff=0.0,
                     pressure=[0.0, 0.85, 1.0])

    cases = {
        "the dawn band (7 hand strokes)": dawn,
        "a scumble, brush left to the verb":
            lambda t: t.scumble(span("A1", "H4"), "dark", "lit", 11),
        "a scumble handed a narrow brush":
            lambda t: t.scumble(span("A1", "H4"), "dark", "lit", 11, size=0.02),
        "a solid block_in at density=1.0":
            lambda t: t.block_in(span("A5", "H8"), "flat", "dark", size=0.06,
                                 density=1.0, solid=True, direction="horizontal"),
        "a sweep":
            lambda t: t.sweep([(0.05, 0.55), (0.5, 0.52), (0.95, 0.58)], "bristle",
                              "dark", into=(0.5, 1.0), depth=0.2, size=0.05),
    }
    for label, build in cases.items():
        said = fired(build)
        print(f"  {label:38} {said[:78] if said else '(silent)'}")
    print("  read: a mass is one colour however its passes are spaced, which is what")
    print("        keeps every block_in out of it; the discriminator is the verb.")


# -- 4. what a solid mass lands at, and in what unit ---------------------------------------
def _solid(side: int, brush: str, px: float, ground: str = GROUND,
           mixture: float = MIX) -> float:
    t = Session(side, side, texture="linen", ground=ground, seed=5, timelapse=False)
    q = t.palette
    c = q.at_value(q.mix(q.mix("titanium_white", "ultramarine", 0.10),
                         "cadmium_red", 0.06), mixture)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        t.block_in(Region(0.30, 0.30, 0.70, 0.70), brush, c, size=px / side,
                   density=1.0, solid=True, opacity=1.0, pressure="even")
    return q.value_of(t.sample((0.40, 0.40, 0.60, 0.60)))


def probe_solid_mass() -> None:
    p = Palette()
    print("\n== what a solid mass actually lands at ==")
    print(f"  600x600 linen, ground {p.value_of(GROUND):.3f}, mixture {MIX}, every "
          f"clause of *a plane that is a plane*")
    sizes = (1.8, 2.7, 3.6, 4.8, 7.2, 12.0, 18.0)
    print(f"  {'brush':>11} " + " ".join(f"{px:7.1f}px" for px in sizes))
    for brush in ("flat", "bristle", "round_hard"):
        row = [_solid(600, brush, px) for px in sizes]
        print(f"  {brush:>11} " + " ".join(f"{v:9.3f}" for v in row))
    print("  read: the session's own table, to the thousandth.")

    print("\n  and it is a pull toward the ground, not a fixed shortfall:")
    for ground, mixture in (("#F6F4F0", 0.865), ("#241F1C", 0.865), ("#F6F4F0", 0.20)):
        got = [_solid(600, b, 18.0, ground, mixture) for b in ("flat", "bristle")]
        print(f"  ground {p.value_of(ground):.3f}, mixture {mixture}: "
              f"flat {got[0]:.3f}, bristle {got[1]:.3f}")
    print("  read: over a lighter ground the same mixture lands ABOVE itself. The")
    print("        session measured one ground and could not see this half.")

    print("\n  the cliff is at four PIXELS, not at a size:")
    print(f"  {'canvas':>8} " + " ".join(f"{px:6.1f}px" for px in (2.7, 3.6, 4.8, 7.2)))
    for side in (300, 600, 1200):
        row = [_solid(side, "flat", px) for px in (2.7, 3.6, 4.8, 7.2)]
        print(f"  {side:8d} " + " ".join(f"{v:8.3f}" for v in row))
    print("  read: the same size= is 2.4px on a 300px canvas and 9.6px on a 1200px one,")
    print("        so the proposed `size < 0.008` would be silent on the failing case")
    print("        and noisy on a working one. The warning counts pixels.")


# -- 5. the across-band ripple, and what it is actually sensitive to -----------------------
def probe_ripple_metric() -> None:
    print("\n== the across-band ripple metric, tried on a painting and discarded ==")

    def band(texture: str, load: float, falloff: float) -> Session:
        t = Session(1024, 768, texture=texture, ground="toned_grey", seed=21,
                    timelapse=False)
        q = t.palette
        q["hi"] = q.at_value(q.mix("cerulean", "titanium_white", 0.55), 0.62)
        q["lo"] = q.at_value(q.mix("cerulean", "burnt_umber", 0.35), 0.38)
        t.scumble(span("A1", "H4"), "hi", "lo", 11, load=load, load_falloff=falloff)
        return t

    def ripple(t: Session, x0: float, x1: float) -> float:
        box = t.canvas.rgb[20:380, int(x0 * 1024):int(x1 * 1024)]
        rows = np.asarray([t.palette.value_of(r.mean(axis=0)) for r in box])
        return float(np.std(np.diff(rows)))

    solid = {tex: band(tex, 1.0, 0.0) for tex in ("smooth", "linen", "rough")}
    print(f"  {'window':>11} {'width':>7} " + " ".join(f"{t:>8}" for t in solid))
    for x0, x1 in ((0.02, 0.98), (0.30, 0.70), (0.045, 0.175), (0.46, 0.50)):
        row = [ripple(solid[t], x0, x1) for t in solid]
        print(f"  {f'{x0}-{x1}':>11} {x1 - x0:7.3f} " + " ".join(f"{v:8.4f}" for v in row))
    starved = {tex: ripple(band(tex, 0.45, 0.6), 0.02, 0.98) for tex in solid}
    print(f"  {'starved 0.45':>11} {0.96:7.3f} "
          + " ".join(f"{starved[t]:8.4f}" for t in solid))
    print("  read: identical across textures at every window width, and on a starved")
    print("        pass `rough` reads LOWER than linen. It is not the texture -- it is")
    print("        the window: narrower means fewer pixels averaged per row, and the")
    print("        number grows two and a half times for the same paint.")


# -- 6. sample() over a cell, and over the mass ---------------------------------------------
def probe_sample_place() -> None:
    print("\n== sample() averages the place it is given ==")
    s = new(1024, 768, ground="toned_grey", seed=9)
    p = s.palette
    p["water"] = p.at_value(p.mix("cerulean", "burnt_umber", 0.45), 0.50)
    p["bird"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.55), 0.30)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.block_in(Region(0.0, 0.0, 1.0, 1.0), "flat", "water", size=0.09, solid=True,
                   direction="horizontal", pressure="even", opacity=1.0)
        bird = polygon([(0.53, 0.44), (0.60, 0.42), (0.63, 0.50), (0.57, 0.56)],
                       name="bird")
        s.block_in(bird, "flat", "bird", size=0.03, solid=True, direction="axis",
                   pressure="even", opacity=1.0)
    from easel import cell
    for label, place in (("the cell it stands in (F5)", cell("F5")),
                         ("its own shape", bird),
                         ("a region cut inside it", Region(0.565, 0.465, 0.600, 0.510))):
        print(f"  a bird planned at 0.300, sampled by {label:28} "
              f"{p.value_of(s.sample(place)):.3f}")
    print("  read: the cell is mostly the water the bird is standing in. A painter read")
    print("        two masses this way and concluded the engine lays everything 0.14")
    print("        light; both were at_value doing what it was asked.")


# -- 7. the pencil, across every painting in the repository ---------------------------------
def probe_pencil_use() -> None:
    print("\n== how many paintings drew, and how many placed a landmark ==")
    paintings = ROOT / "paintings"
    marks = ("painting.png", "painting.gif", "NOTES.md", "prelude.py")
    found = []
    for d in sorted(p for p in paintings.iterdir() if p.is_dir()):
        if any((d / m).exists() for m in marks):
            found.append(d)
        else:
            found.extend(sorted(c for c in d.iterdir() if c.is_dir()))
    print(f"  {'painting':>34} {'pencil':>7} {'landmarks':>10}")
    drew = landmarked = 0
    for d in found:
        text = "".join(f.read_text() for f in sorted(d.glob("*.py")))
        pencils, landmarks = text.count("s.pencil("), text.count("s.mark(")
        drew += pencils > 0
        landmarked += landmarks > 0
        print(f"  {d.relative_to(paintings).as_posix():>34} {pencils:7d} {landmarks:10d}")
    print(f"  read: {len(found) - drew} of {len(found)} paintings drew no line at all, "
          f"and {len(found) - landmarked}")
    print("        placed no landmark. Only the pass scripts are counted -- a probe or")
    print("        an exercise beside a painting is not the painting.")


def main() -> None:
    probe_sequence_stacks()
    probe_bristle_floor()
    probe_graded_band()
    probe_solid_mass()
    probe_ripple_metric()
    probe_sample_place()
    probe_pencil_use()
    print()


if __name__ == "__main__":
    main()
