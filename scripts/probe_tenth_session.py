"""The measurements behind the tenth session's list and the winter greenhouse's.

Two rounds, filed as one because they raised the same two items from opposite
directions: what ``direction=`` names, and a check that fires on a row of separate
things. This script re-measures every claim the rounds were built on, on the engine as
it now is, and prints the numbers quoted in ``CALIBRATION.md``, ``SUGGESTIONS.md``,
``CHANGELOG.md`` and the docstrings the round changed.

Two of the claims did not survive it, and both probes below print the *before* beside
the *after*:

* ``cost_line`` and the picture describing different geometries -- they do not; both
  are in normalised units, which is the half nobody had written down;
* the asymmetric pull doing something extra to a smudge on a long boundary -- it does
  not; the strip is the calibrated reach at every join length.

    python scripts/probe_tenth_session.py
"""

from __future__ import annotations

import math
import time
import warnings

import numpy as np

from easel import Region, Session, hull, polygon
from easel.color import luminance

OUT = "out"


def new(width: int = 1024, height: int = 768, ground: str = "toned_grey",
        seed: int = 7) -> Session:
    return Session(width, height, texture="linen", ground=ground, seed=seed,
                   timelapse=False, out_dir=OUT)


# -- 1. the check that fired on every rehearsal ------------------------------------------
def probe_rehearsed_check() -> None:
    print("\n== the first-sixty rule on the --rehearse path ==")
    s = new(320, 240)
    for i in range(70):
        s.stroke([(0.05 + 0.012 * i, 0.20), (0.05 + 0.012 * i, 0.30)], "flat",
                 "burnt_umber", size=0.05)

    def detail(session, prior):
        session._prior = prior
        before = len(session.history.records)
        for i in range(9):
            session.dab(0.2 + 0.03 * i, 0.8, "round_hard", "titanium_white", size=0.01)
        said = session.report(since=before)
        return "FIRES" if "detail before the masses" in said else "silent"

    print(f"  the painting itself, {s.spent} strokes spent:   {detail(s.scratch(), s.history.records):>6}")
    print(f"  the same pass on a copy, before 0.4.0:        "
          f"{detail(s.scratch(), []):>6}   <- spent {s.spent}, records held 0")
    print("  read: the rule's `earlier` term came off the copy's own log, which is empty.")


# -- 2. what a jitter override buys ------------------------------------------------------
def probe_jitter() -> None:
    print("\n== jitter=, as the width of the band it lays ==")
    print("  one straight stroke, liner at size=0.005, pressure='even', 1024x768")
    print(f"  {'jitter':>8} {'x default':>10} {'band, in brushes':>18}")
    for j in (0.0, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5):
        s = new(ground="white")
        before = s.canvas.rgb.copy()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            s.stroke([(0.1, 0.5), (0.9, 0.5)], "liner", "burnt_umber", size=0.005,
                     jitter=j, pressure="even")
        rows = np.nonzero((np.abs(s.canvas.rgb - before).sum(axis=2) > 1e-3).any(axis=1))[0]
        band = (rows.max() - rows.min() + 1) / (0.005 * 1024)
        print(f"  {j:8.3f} {j / 0.02:10.1f} {band:18.2f}")
    print("  read: the wall is five times the default, where a line stops being one brush wide.")


# -- 3. cover(), and how much canvas it buries -------------------------------------------
def probe_cover() -> None:
    print("\n== cover(), against the area it was handed ==")
    patch = Region(0.905, 0.380, 0.985, 0.478)     # the painter's own mis-made leaf
    print("  Region(0.905, 0.380, 0.985, 0.478), flat at size=0.06, 1024x768")
    for edge in ("ragged", "clean", "hard"):
        s = new()
        s.block_in(Region(0.0, 0.0, 1.0, 1.0), "flat", "burnt_umber", size=0.12, solid=True)
        s.dry()
        before = s.canvas.rgb.copy()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            s.cover(patch, "titanium_white", size=0.06, edge=edge)
        painted = (np.abs(s.canvas.rgb - before).sum(axis=2) > 1e-3).sum()
        asked = (patch.x1 - patch.x0) * 1024 * (patch.y1 - patch.y0) * 768
        print(f"  edge={edge:<7} {painted / asked:5.2f}x the area asked for")
    print("  read: the overrun is the recipe; on a worked passage clean or hard is the answer.")


# -- 4. inset() at the canvas frame ------------------------------------------------------
def probe_inset() -> None:
    print("\n== inset() on a boundary that lies on the frame ==")
    glass = polygon([(0.55, 0.05), (1.05, 0.02), (1.05, 0.98), (0.55, 0.95)], name="glass")
    rows = slice(int(0.15 * 768), int(0.85 * 768))
    for label, place in (("inset(0.024)", glass.inset(0.024)),
                         ("frame=False", glass.inset(0.024, frame=False))):
        s = new()
        ground = s.canvas.values()[rows, -1] / 255.0
        s.block_in(place, "flat", "burnt_umber", size=0.06, solid=True)
        now = s.canvas.values()[rows, -1] / 255.0
        bare = float(np.mean(np.abs(now - ground) < 0.02))
        print(f"  {label:<13} right column still bare: {bare:6.1%}")
    print("  read: a mass that meets the frame should run off it, and now does.")


# -- 5. the ground still showing through -------------------------------------------------
def probe_ground() -> None:
    print("\n== how much ground is still showing ==")
    s = new(400, 300, ground="umber_wash")
    print(f"  bare canvas                       {s.canvas.ground_showing():7.2%}")
    s.block_in(Region(0.0, 0.0, 1.0, 1.0), "bristle", "ultramarine", size=0.09, density=0.7)
    print(f"  one pass at density=0.7           {s.canvas.ground_showing():7.2%}")
    s.block_in(Region(0.0, 0.0, 1.0, 1.0), "flat", "ultramarine", size=0.09, solid=True)
    print(f"  a solid mass over it              {s.canvas.ground_showing():7.2%}")
    print(f"  ...at the looser 16/255           {s.canvas.ground_showing(16 / 255):7.2%}")
    print("  read: the painting that raised this finished at 0.07%. The floor is 0.5%.")


# -- 6. a round tip on a small shape -----------------------------------------------------
def probe_round_tip() -> None:
    print("\n== a round tip blocking in a small shape ==")
    leaf = hull([(0.918, 0.405), (0.949, 0.393), (0.968, 0.424),
                 (0.951, 0.462), (0.921, 0.448)], name="leaf")
    w, h = 1200, 800
    short = min(leaf.box.width * w / max(w, h), leaf.box.height * h / max(w, h))
    print(f"  the painter's pressed leaf: {short:.3f} across at its narrowest, {w}x{h}")
    print(f"  {'size':>7} {'share':>6} {'round_hard':>11} {'flat':>7}   (painted area / the shape's)")
    for size in (0.005, 0.009, 0.0115, 0.013, 0.023):
        got = []
        for brush in ("round_hard", "flat"):
            s = new(w, h)
            before = s.canvas.rgb.copy()
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                s.block_in(leaf, brush, "titanium_white", size=size, density=1.0,
                           solid=True, direction=34, pressure="even", opacity=1.0)
            painted = (np.abs(s.canvas.rgb - before).max(axis=2) > 0.01).sum()
            got.append(painted / leaf.mask(w, h).sum())
        print(f"  {size:7.4f} {size / short:6.2f} {got[0]:11.2f} {got[1]:7.2f}")
    print("  read: the fringe is the silhouette past a quarter, which is where clean already warns.")


# -- 7. the graded-passage rule on a row of separate things ------------------------------
def probe_graded_band() -> None:
    print("\n== the graded-passage rule, narrowed ==")

    def ramped():
        s = new()
        p = s.palette
        for i, v in enumerate((0.30, 0.38, 0.46, 0.54, 0.62, 0.70, 0.78, 0.86)):
            p[f"v{i}"] = p.at_value(p.mix("cadmium_red", "cerulean", 0.3), v)
        return s

    def band(s):
        line = next((ln for ln in s.report().splitlines() if "stepping colours" in ln), "")
        return "FIRES" if line else "silent"

    def lay(s, y, col, size):
        s.stroke([(0.05, y), (0.95, y)], "flat", col, size=size, load=1.0, load_falloff=0.0)

    one = ramped()
    for i in range(8):
        lay(one, 0.18 + i * 0.028, f"v{i}", 0.03)
    print(f"  one ramp of eight, too narrow for its own step   {band(one):>6}")

    two = ramped()
    for i in range(8):
        lay(two, 0.18 + i * 0.028, f"v{i % 4}", 0.03)
    print(f"  two ramps of four laid end to end                {band(two):>6}")

    pots = ramped()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for i in range(10):
            x = 0.10 + i * 0.075
            for j, col in enumerate(("v1", "v3", "v5")):
                pots.stroke([(x + j * 0.004, 0.52), (x + j * 0.004, 0.58)], "flat", col,
                            size=0.005)
    print(f"  ten pots, three body strokes each                {band(pots):>6}")

    smudged = ramped()
    for i in range(5):
        lay(smudged, 0.20 + i * 0.028, f"v{i}", 0.06)
    smudged.smudge([(0.05, 0.34), (0.95, 0.34)], size=0.02)
    print(f"  five wide marks and a smudge among them          {band(smudged):>6}")
    print("  read: a passage steps one way, in one run, in colours something laid.")


# -- 8. the chisel staircase, and the hard clip ------------------------------------------
def horizontal_edge_share(s: Session, box, pad: float = 0.01) -> float:
    """Share of the strong edges in a region running within 10 degrees of horizontal."""
    img = np.asarray(s.canvas.to_srgb8(impasto=True), dtype=np.float32) / 255.0
    h, w, _ = img.shape
    grey = luminance(img.reshape(-1, 3) ** 2.2).reshape(h, w)
    x0, y0 = int((box.x0 - pad) * w), int((box.y0 - pad) * h)
    x1, y1 = int((box.x1 + pad) * w), int((box.y1 + pad) * h)
    g = grey[max(y0, 1):min(y1, h - 1), max(x0, 1):min(x1, w - 1)]
    gy, gx = np.gradient(g)
    mag = np.hypot(gx, gy)
    strong = mag > max(np.percentile(mag, 90), 1e-4)
    ang = np.degrees(np.arctan2(np.abs(gx[strong]), np.abs(gy[strong])))
    return float((ang < 10.0).mean())


def probe_hard_clip() -> None:
    print("\n== edge='hard': a pass that ends where the outline is ==")
    face = polygon([(0.303, 0.268), (0.307, 0.400), (0.311, 0.540), (0.318, 0.680),
                    (0.330, 0.820), (0.344, 0.905), (0.398, 0.940), (0.384, 0.820),
                    (0.368, 0.680), (0.357, 0.540), (0.348, 0.400), (0.340, 0.258)]
                   ).smooth(3)
    print("  the winter greenhouse's lit face, 1120x860, vertical passes, laid solid")
    print(f"  {'tip':11s} {'size':>6} {'edge':>7} {'horizontal edges':>17} {'past the outline':>17}")
    for brush, size in (("flat", 0.020), ("knife", 0.020), ("bristle", 0.022),
                        ("round_hard", 0.020)):
        for edge in ("ragged", "hard"):
            s = Session(1120, 860, texture="linen", ground="toned_warm_grey", seed=41,
                        timelapse=False, out_dir=OUT)
            s.palette["v"] = s.palette.at_value(
                s.palette.mix("yellow_ochre", "viridian", 0.30), 0.25)
            before = s.canvas.rgb.copy()
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                s.block_in(face, brush, "v", size=size, density=1.0, solid=True,
                           opacity=1.0, pressure="even", direction=90, edge=edge)
            painted = np.abs(s.canvas.rgb - before).max(axis=2) > 0.01
            ys, xs = np.nonzero(painted)
            x0, y0, x1, y1 = face.bounds
            past = max(x0 * 1120 - xs.min(), xs.max() - x1 * 1120,
                       y0 * 860 - ys.min(), ys.max() - y1 * 860, 0.0)
            print(f"  {brush:11s} {size:6.3f} {edge:>7} "
                  f"{horizontal_edge_share(s, face.box):16.0%} {past:14.1f}px")
    print("  read: the chisels put horizontal edges into a mass that has none; the clip removes them.")


# -- 9. pricing a compound recipe --------------------------------------------------------
def probe_count_only() -> None:
    print("\n== a count-only rehearsal ==")

    def pots(s):
        for i in range(13):
            x = 0.08 + i * 0.068
            body = polygon([(x, 0.60), (x + 0.048, 0.60), (x + 0.040, 0.70), (x + 0.008, 0.70)])
            s.block_in(body, "flat", "burnt_sienna", size=0.012, density=1.0, solid=True,
                       direction="axis")
            s.stroke([(x - 0.002, 0.602), (x + 0.050, 0.602)], "round_hard", "burnt_umber",
                     size=0.008)
            s.stroke([(x + 0.004, 0.612), (x + 0.044, 0.612)], "flat", "titanium_white",
                     size=0.006)

    base = new()
    out = {}
    for count in (False, True):
        trial = base.scratch(count_only=count)
        t0 = time.perf_counter()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            pots(trial)
        out[count] = (trial, time.perf_counter() - t0)
    painted, counted = out[False], out[True]
    print("  thirteen pots, three verbs each, 1024x768")
    print(f"  rendered {painted[0].history.stroke_count:4d} strokes in {painted[1]:6.2f}s")
    print(f"  counted  {counted[0].history.stroke_count:4d} strokes in {counted[1]:6.2f}s"
          f"   ({painted[1] / max(counted[1], 1e-9):.0f}x)")
    same = all(a.points == b.points for a, b in
               zip(painted[0].history.records, counted[0].history.records, strict=True))
    print(f"  same paths: {same}")
    print("  read: pass geometry is settled before anything is stamped, so the count is exact.")


# -- 10. what direction= is measured in --------------------------------------------------
def probe_direction_units() -> None:
    print("\n== direction=, in normalised units and as a line ==")
    band = Region(0.1, 0.3, 0.9, 0.7)

    def screen(s):
        w, h = s.size
        out = []
        for r in s.history.records:
            (ax, ay), (bx, by) = r.points[0], r.points[-1]
            out.append(math.degrees(math.atan2((by - ay) * h, (bx - ax) * w)) % 180.0)
        return float(np.median(out))

    print(f"  {'canvas':>10} {'asked':>7} {'as an angle':>13} {'as a line':>11}")
    for (w, h), asked in (((1000, 500), -23), ((1024, 768), 45), ((1024, 768), -23)):
        angled = new(w, h, ground="white")
        angled.block_in(band, "flat", "burnt_umber", size=0.05, density=0.9, direction=asked)
        long = max(w, h)
        run = 0.4
        line = ((0.30, 0.50),
                (0.30 + run * math.cos(math.radians(asked)) / (w / long),
                 0.50 + run * math.sin(math.radians(asked)) / (h / long)))
        lined = new(w, h, ground="white")
        lined.block_in(band, "flat", "burnt_umber", size=0.05, density=0.9, direction=line)
        print(f"  {w}x{h:<5} {asked:6}d {screen(angled) - 180.0 if screen(angled) > 90 else screen(angled):12.1f}d "
              f"{screen(lined) - 180.0 if screen(lined) > 90 else screen(lined):10.1f}d")
    print("  read: the angle is in the 0..1 coordinates; the line is on the screen.")


# -- 11. a smudge on a long boundary -----------------------------------------------------
def probe_smudge_strip() -> None:
    print("\n== a smudge's reach, against the length of the join ==")
    w, h, bound = 1024, 768, 0.50
    row = int(bound * h)

    def stepped():
        s = new(w, h)
        p = s.palette
        p["dark"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.5), 0.17)
        p["lit"] = p.at_value(p.mix("yellow_ochre", "titanium_white", 0.5), 0.78)
        for place, colour in ((Region(0.0, 0.0, 1.0, bound), "dark"),
                              (Region(0.0, bound, 1.0, 1.0), "lit")):
            s.block_in(place, "flat", colour, size=0.06, solid=True, opacity=1.0,
                       pressure="even", direction="horizontal", edge="hard")
        s.dry()
        return s

    print("  one pass at the default size, a hard step from 0.19 to 0.78, 1024x768")
    print(f"  {'join':>6} {'strip height':>14} {'strip value':>12}")
    for length in (0.05, 0.10, 0.20, 0.40, 0.80):
        s = stepped()
        before = s.canvas.values(sketch=False).astype(np.float32) / 255.0
        x0 = 0.5 - length / 2.0
        s.smudge([(x0, bound), (x0 + length, bound)], size=0.02)
        after = s.canvas.values(sketch=False).astype(np.float32) / 255.0
        c0, c1 = int((x0 + length * 0.2) * w), int((x0 + length * 0.8) * w)
        lift = (after[:, c0:c1].mean(axis=1) - before[:, c0:c1].mean(axis=1))[:row]
        tall = 100.0 * int((lift > 0.01).sum()) / h
        value = float(after[:, c0:c1].mean(axis=1)[:row][int(np.argmax(lift))])
        print(f"  {length:6.2f} {tall:13.2f}% {value:12.2f}")
    print("  read: the reach is flat and the value is halfway. A long join gets a second edge.")


def main() -> None:
    print("The tenth session and the winter greenhouse: every claim, re-measured.")
    probe_rehearsed_check()
    probe_jitter()
    probe_cover()
    probe_inset()
    probe_ground()
    probe_round_tip()
    probe_graded_band()
    probe_hard_clip()
    probe_count_only()
    probe_direction_units()
    probe_smudge_strip()


if __name__ == "__main__":
    main()
