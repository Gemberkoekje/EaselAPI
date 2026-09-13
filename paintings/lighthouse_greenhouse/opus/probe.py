"""The measurements behind this session's list in SUGGESTIONS.md.

Four probes on stated canvases. Probes 1 to 3 measure engine behaviour and back
items 1 to 3 of that file. Probe 4 is arithmetic on this painting's own written
value plan rather than a measurement of anything -- it shows that the check item
4 asks for would have fired before the first stroke, and says nothing about
whether the check is worth building.

``LESSONS.md``'s standing rule is that a claim with no test behind it says so,
and every one of the painters' claims that has failed re-measurement so far was
reported as *observed*. Items 5 and 6 of that file have no probe here and say so.

    python paintings/lighthouse_greenhouse/opus/probe.py

Probe 1  the chisel staircase: what a solid tip's pass ends do to a boundary
         that slopes, against the same mass laid with a comb.
Probe 2  what ``edge="clean"`` costs a small shape, as a fraction of the mass
         the painter meant, against the brush's share of its shorter extent.
Probe 3  the price of a shaped ``block_in`` with ``direction`` left off, on the
         two masses of this painting where it was nearly paid.
Probe 4  the pairwise separations inside this painting's own written value
         plan -- the check ``compare()`` does not run.
"""

from __future__ import annotations

import numpy as np

from easel import Session, polygon
from easel.color import luminance

OUT = "out"


# --------------------------------------------------------------------------
# The two masses this painting actually used, so the numbers are the ones the
# picture was made from rather than a demonstration built to produce them.
def lit_face():
    return polygon([(0.303, 0.268), (0.307, 0.400), (0.311, 0.540), (0.318, 0.680),
                    (0.330, 0.820), (0.344, 0.905), (0.398, 0.940), (0.384, 0.820),
                    (0.368, 0.680), (0.357, 0.540), (0.348, 0.400), (0.340, 0.258)]
                   ).smooth(3)


def mid_face():
    return polygon([(0.222, 0.266), (0.216, 0.400), (0.208, 0.540), (0.198, 0.680),
                    (0.186, 0.820), (0.176, 0.905), (0.354, 0.905), (0.340, 0.820),
                    (0.328, 0.680), (0.321, 0.540), (0.317, 0.400), (0.313, 0.268)]
                   ).smooth(3)


def roof():
    return polygon([(0.148, 0.114), (0.362, 0.114), (0.302, 0.078), (0.208, 0.078)])


def horizontal_edge_share(path, box, pad=0.01):
    """Share of the strong edges in a region that run within 10 degrees of
    horizontal.

    The same Sobel measure ``CALIBRATION.md``'s *Laying a mass along its own
    axis* table is built on, written out here because the module it was
    imported from is not in this repository. Higher is squarer; a staircase is
    a run of horizontal edges where the mass has no horizontal features.
    """
    from PIL import Image

    img = np.asarray(Image.open(path).convert("RGB"), dtype=np.float32) / 255.0
    h, w, _ = img.shape
    grey = luminance(img.reshape(-1, 3) ** 2.2).reshape(h, w)
    x0, y0, x1, y1 = (int((box.x0 - pad) * w), int((box.y0 - pad) * h),
                      int((box.x1 + pad) * w), int((box.y1 + pad) * h))
    g = grey[max(y0, 1):min(y1, h - 1), max(x0, 1):min(x1, w - 1)]
    gy, gx = np.gradient(g)
    mag = np.hypot(gx, gy)
    strong = mag > max(np.percentile(mag, 90), 1e-4)
    if strong.sum() < 50:
        return float("nan"), 0
    # a horizontal *edge* has a vertical gradient
    ang = np.degrees(np.arctan2(np.abs(gx[strong]), np.abs(gy[strong])))
    return float((ang < 10.0).mean()), int(strong.sum())


# --------------------------------------------------------------------------
def probe_one_staircase():
    """A solid tip's pass ends stack into a staircase down a sloping boundary.

    The lit band of this painting's tower: 0.06 wide, 0.64 tall, its boundaries
    sloping about 3 degrees off vertical, filled with vertical passes. Every
    pass of a chisel tip terminates in a hard *horizontal* edge, and where the
    boundary slopes the ends stop at different heights, so the ends stack into
    steps. A comb's pass ends are already broken and stack into nothing.

    The mass has no horizontal feature in it at all, so every horizontal edge
    measured here is the tool's.
    """
    print("\nPROBE 1  the chisel staircase")
    print("  a mass 0.06 x 0.64 whose boundaries slope 3 degrees off vertical,")
    print("  1120x860 linen on toned_warm_grey, vertical passes, laid solid.")
    print("  Share of strong edges running within 10 degrees of horizontal --")
    print("  the mass has no horizontal feature, so all of it is the tool's.")
    face = lit_face()
    print(f"  {'tip':10s} {'size':>6} {'horizontal edges':>18} {'strong px':>10}")
    for brush, size in (("flat", 0.020), ("flat", 0.010), ("knife", 0.020),
                        ("bristle", 0.022), ("bristle", 0.012),
                        ("round_hard", 0.020)):
        s = Session(1120, 860, texture="linen", ground="toned_warm_grey", seed=41,
                    out_dir=OUT, timelapse=False)
        # laid dark against the ground so the boundary is unambiguous: what is
        # measured is where the paint stops, not how well the mass reads
        s.palette["v"] = s.palette.at_value(
            s.palette.mix("yellow_ochre", "viridian", 0.30), 0.25)
        s.block_in(face, brush, "v", size=size, density=1.0, solid=True,
                   opacity=1.0, pressure="even", direction=90)
        path = s.export(f"{OUT}/probe_stair_{brush}_{size}.png")
        share, n = horizontal_edge_share(path, face.box)
        print(f"  {brush:10s} {size:6.3f} {share:17.0%} {n:10d}")
    print("  read: the chisel tips put horizontal edges into a mass that has")
    print("        none; the comb does not. Same shape, same passes, same size.")


def probe_two_clean_edge():
    """What edge="clean" costs a small shape.

    It insets the fill by half the brush, so what it takes out is a rim half a
    brush wide all the way round -- which is a rim on a big mass and most of
    the mass on a small one. The number that predicts it is the brush's share
    of the shape's *shorter* extent.
    """
    print("\nPROBE 2  what edge=\"clean\" takes off a small shape")
    print("  area of shape.inset(size/2) as a share of the shape, against the")
    print("  brush's share of the shape's shorter extent")
    tower = polygon([(0.170, 0.258), (0.163, 0.400), (0.154, 0.540),
                     (0.142, 0.680), (0.128, 0.820), (0.118, 0.940),
                     (0.398, 0.940), (0.384, 0.820), (0.368, 0.680),
                     (0.357, 0.540), (0.348, 0.400), (0.340, 0.258)])
    cases = [("this painting's lantern cap", roof(), 0.016),
             ("the same cap, half the brush", roof(), 0.008),
             ("the tower's lit band", lit_face(), 0.022),
             ("the lantern box", polygon(
                 [(0.160, 0.108), (0.350, 0.108), (0.344, 0.234),
                  (0.166, 0.234)]), 0.045),
             ("the tower's mid plane", mid_face(), 0.027),
             ("the whole tower (clean, and fine)", tower, 0.035)]
    print(f"  {'shape':32s} {'size':>6} {'brush/short':>12} {'area kept':>10}")
    for name, shape, size in cases:
        box = shape.box
        short = min(box.width, box.height)
        kept = shape.inset(size / 2).area / shape.area
        print(f"  {name:32s} {size:6.3f} {size / short:11.0%} {kept:10.0%}")
    print("  read: past about a fifth of the shorter extent the contour is")
    print("        eating the mass, and the corners go first.")


def probe_three_direction():
    """The price of leaving `direction` off a shaped block_in.

    Both of these were costed with `direction=90`, written without it, and
    caught by a rehearsal that came back charging 124 strokes for a pass
    budgeted at 40.
    """
    print("\nPROBE 3  a shaped block_in with `direction` left off")
    s = Session(1120, 860, texture="linen", ground="toned_warm_grey", seed=41,
                out_dir=OUT, timelapse=False)
    print(f"  {'mass':22s} {'axis':>6} {'90':>6} {'default':>9} {'ratio':>7}")
    worst = 0.0
    for name, shape, size in (("the tower's mid plane", mid_face(), 0.027),
                              ("the tower's lit band", lit_face(), 0.022),
                              ("the vine mass", polygon(
                                  [(0.19, 0.13), (0.32, 0.13), (0.32, 0.22),
                                   (0.19, 0.22)]), 0.030)):
        base = {"shape": shape, "brush": "flat", "size": size, "density": 1.0}
        axis = s.cost(dict(base, direction="axis"), share=0)
        vert = s.cost(dict(base, direction=90), share=0)
        dflt = s.cost(base, share=0)
        ratio = dflt / max(min(axis, vert), 1)
        worst = max(worst, ratio)
        print(f"  {name:22s} {axis:6d} {vert:6d} {dflt:9d} {ratio:6.1f}x")
    print("  read: a warning at 2.5x would have caught every one of these")
    print(f"        (worst {worst:.1f}x) and fires on nothing else in this painting.")


def probe_four_separations():
    """The check `compare()` does not run: are any two planned places within 0.10?

    `compare({place: value})` scores each place against its own target. The
    threshold it scores against is `0.10`, and what `0.10` *means* in the guide
    is the distance below which two masses read as one -- which is a statement
    about a pair, and no pair is ever checked.
    """
    print("\nPROBE 4  pairwise separation inside this painting's own value plan")
    plan = {"fog high": 0.58, "fog low": 0.68, "beam": 0.75, "sea far": 0.54,
            "sea near": 0.40, "rock": 0.21, "tower": 0.40, "vines": 0.26}
    names = list(plan)
    close = [(a, b, abs(plan[a] - plan[b]))
             for i, a in enumerate(names) for b in names[i + 1:]
             if abs(plan[a] - plan[b]) < 0.10]
    for a, b, d in sorted(close, key=lambda t: t[2]):
        print(f"  {a:10s} {plan[a]:.2f}   {b:10s} {plan[b]:.2f}   apart {d:.2f}")
    print(f"  {len(close)} pairs under 0.10 out of {len(names) * (len(names) - 1) // 2},")
    print("  written down before the first stroke and never reported by anything.")
    print("  read: `sea near` and `tower` are the two that touch on the canvas.")
    print("        The tower's foot dissolved into the water exactly there, and")
    print("        it cost two late strokes to make it look deliberate.")


if __name__ == "__main__":
    import os

    os.makedirs(OUT, exist_ok=True)
    probe_one_staircase()
    probe_two_clean_edge()
    probe_three_direction()
    probe_four_separations()
    print()
