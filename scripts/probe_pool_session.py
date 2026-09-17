"""The measurements behind the eighth session's list in SUGGESTIONS.md.

A municipal pool at night, painted against a deliberately restricted document set --
``PAINTER.md`` and its nine exercises, ``RECIPES.md`` and ``REFERENCE.md``, nothing
else. It is the split test's other arm, and it left three engine items and five
documentation items, each labelled *measured*, *observed*, or (once) *opinion*.

This script re-measures every claim the round was built on, on the engine as it now
is, and prints the numbers quoted in ``CALIBRATION.md``, ``SUGGESTIONS.md`` and the
docstrings the round changed. Two of the round's claims did not survive it, and both
probes below print the *before* beside the *after*:

* the mechanism behind the ``direction=`` sequence price -- the session offered *the
  stack is sized for the steepest angle in the list* as a guess, and it is wrong;
* *no ``n`` fits under about ``0.07`` deep* -- exact for the recipe's eight rings,
  and the wall is at ``0.042`` for the fewest rings that read as a fall-off at all.

    python scripts/probe_pool_session.py          # writes out/compare_NNN.png
"""

from __future__ import annotations

import warnings

import numpy as np

import easel.session as session_module
from easel import Palette, Region, Session, ellipse, polygon, span
from easel.canvas import GROUNDS


def new(width: int = 1024, height: int = 768, ground: str = "cool_grey",
        seed: int = 7) -> Session:
    return Session(width, height, texture="linen", ground=ground, seed=seed,
                   timelapse=False)


# The room mass the session priced its directions on, off its own `prelude.py`.
WALLBASE = [(-0.05, 0.245), (0.38, 0.29), (0.72, 0.335), (1.05, 0.365)]
ROOM = polygon([(-0.05, -0.05), (1.05, -0.05)] + WALLBASE[::-1], name="room")


# -- 1. a sequence of directions, and what actually prices it ------------------------------
def probe_direction_sequence() -> None:
    print("\n== direction= given a sequence ==")
    print("  the room mass, bristle at size=0.16, density=0.9 -- the session's own call.")
    s = new()
    b = s._resolve_brush("bristle", 0.16, 1.0, {})

    def price(direction) -> int:
        trial = s._trial_session()
        return sum(1 for _ in trial._block_in_paths(ROOM, b, direction, 0.9, None))

    ten = [0, 12, -17, 30, -35, 50, 62, -70, 80, 95]
    each = [price(a) for a in ten]
    for name, direction in (('"axis"', "axis"), ("-17 degrees", -17),
                            ('"cross"', "cross"), ("a ten-angle sequence", ten)):
        print(f"  {name:22s} {price(direction):4d}")
    print(f"  the ten angles, one at a time: {' + '.join(str(e) for e in each)} "
          f"= {sum(each)}")
    print(f"  the steepest of them alone:    {max(each)}")
    print("  read: the session's 4, 7 and 15 reproduce to the stroke. Its ten-angle list")
    print("        cost 51 and this one costs 85, because they are different ten angles --")
    print("        the mechanism is what matters, and it is the SUM, not the steepest.")
    print("        'the stack is sized for the steepest angle in the list' was offered as")
    print("        a guess and is wrong: a sequence is one whole pass per angle.")

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        s.scratch().block_in(ROOM, "bristle", "burnt_umber", density=0.9, size=0.16,
                             direction=ten)
    print(f"  the price walk now fires on it: {'yes' if caught else 'NO'}")
    for pair in (("cross", '"cross"'), ((4, 94), "(4, 94)"), ((5, 173), "(5, 173)")):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            s.scratch().block_in(ROOM, "bristle", "burnt_umber", density=0.9,
                                 size=0.16, direction=pair[0])
        print(f"  and on the pair idiom {pair[1]:10s} ({price(pair[0]):3d}): "
              f"{'fires' if caught else 'silent'}")
    print("  read: two angles can never be more than twice the dearer of them, so the")
    print("        pair every painting in this repository uses stays quiet.")


# -- 2. the inward scumble's other wall ----------------------------------------------------
def probe_inward_window() -> None:
    print("\n== the inward scumble's usable n ==")
    print("  the brush is 3 x depth / n and the comb floor is 0.025, so n <= 120 x depth.")
    print(f"  {'depth':>7} {'n at the floor':>15} {'120 x depth':>12}")
    for depth in (0.030, 0.042, 0.0667, 0.075, 0.100, 0.200):
        patch = ellipse((0.5, 0.5), 0.30, depth, name="patch")
        fits = session_module._INWARD_STEPS * depth / 0.025
        print(f"  {depth:7.4f} {fits:15.1f} {120 * depth:12.1f}"
              f"   (_inward_depth: {session_module._inward_depth(patch):.4f})")
    print("  read: exact. 0.0667 deep is where the recipe's eight rings stop fitting --")
    print("        the session's 'about 0.07'. The wall where NO n fits is lower: five")
    print("        rings is the fewest that read as a fall-off, and that is 0.042.")

    s = new()
    s.palette["shadow"] = s.palette.at_value(
        s.palette.mix("ultramarine", "burnt_umber", 0.5), 0.30)
    s.palette["lit"] = s.palette.at_value(
        s.palette.mix("cerulean", "titanium_white", 0.7), 0.70)

    print(f"\n  {'patch':>7} {'n':>4} {'brush':>8}  warning")
    for depth, n in ((0.075, 8), (0.075, 9), (0.075, 12), (0.030, 8)):
        patch = ellipse((0.5, 0.5), 0.30, depth, name="patch")
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            s.scratch().scumble(patch, "shadow", "lit", n, direction="inward")
        size = session_module._inward_size(patch, n)
        said = next((str(c.message) for c in caught if "comb" in str(c.message)), "")
        print(f"  {depth:7.3f} {n:4d} {size:8.4f}  "
              f"{said.split('. ', 1)[1][:64] + '...' if said else '(silent)'}")
    print("  read: the session met this at n=12 on a patch 0.075 deep and read the")
    print("        post-pass check's bristle complaint as unrelated. It is said at the")
    print("        call now, and where no n fits it names `a volume of lit air` instead.")


# -- 3. a glaze's usable opacity, and aiming at a value instead ----------------------------
def _film_field(s: Session, points, color, **kw) -> tuple[np.ndarray, float, float]:
    """The footprint of a film at full strength, and the values at both ends of it."""
    before = s.canvas.rgb
    trial = s.scratch()
    trial.glaze(points, color, opacity=1.0, **kw)
    under = np.abs(trial.canvas.rgb - before).sum(axis=2) > 1e-4
    return (under,
            s.palette.value_of(before[under].mean(axis=0)),
            s.palette.value_of(trial.canvas.rgb[under].mean(axis=0)))


def probe_glaze_window() -> None:
    print("\n== a glaze's usable opacity, and to_value= ==")
    s = Session(512, 384, texture="linen", ground="toned_grey", seed=7, timelapse=False)
    p = s.palette
    p["dark"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.5), 0.30)
    p["warm"] = p.at_value(p.mix("cadmium_red", "yellow_ochre", 0.4), 0.62)
    s.block_in(span("A1", "H8"), "flat", "dark", size=0.18, solid=True,
               pressure="even", direction="horizontal")
    s.dry()
    points = [(0.2, 0.5), (0.8, 0.5)]
    kw = dict(brush="flat", size=0.18, pressure="even")

    under, field, reach = _film_field(s, points, "warm", **kw)
    print("  a warm light film over a cool dark mass, measured over the film's own")
    print(f"  footprint: the paint reads {field:.3f}, and at opacity=1.0 it reaches "
          f"{reach:.3f}.")
    print(f"  {'opacity':>8} {'value under it':>15} {'change':>8}")
    for opacity in (0.05, 0.07, 0.10, 0.14, 0.20):
        trial = s.scratch()
        trial.glaze(points, "warm", opacity=opacity, **kw)
        got = p.value_of(trial.canvas.rgb[under].mean(axis=0))
        print(f"  {opacity:8.2f} {got:15.3f} {got - field:+8.3f}")
    print("  read: CALIBRATION.md's table, on its own canvas, sampled over the middle of")
    print("        the film rather than its whole footprint, reads +0.028 to +0.123 across")
    print("        the same five settings. The shape is what matters: the window between")
    print("        'no hue left' and 'a new mass' is a few hundredths of opacity wide,")
    print("        and where it sits is different over every passage.")

    print(f"\n  {'to_value':>9} {'opacity found':>14} {'delivered':>10} {'miss':>7}")
    for target in (0.34, 0.38, 0.42, 0.46):
        trial = s.scratch()
        trial.glaze(points, "warm", to_value=target, **kw)
        got = p.value_of(trial.canvas.rgb[under].mean(axis=0))
        opacity = trial.history.records[-1].params["opacity"]
        print(f"  {target:9.2f} {opacity:14.4f} {got:10.3f} {got - target:+7.3f}")
    print("  read: one stroke, the same as any glaze, and the search is spent on trial")
    print("        canvases. at_value does this for a mixture; this is it for a film.")

    plain = s.scratch()
    plain.glaze(points, "warm", opacity=0.18, **kw)
    solved = s.scratch()
    solved.glaze(points, "warm", to_value=0.42, **kw)
    opacity = solved.history.records[-1].params["opacity"]
    again = s.scratch()
    again.glaze(points, "warm", opacity=opacity, **kw)
    print(f"  the default is still 0.18: "
          f"{'yes' if plain.history.records[-1].params['opacity'] == 0.18 else 'NO'}")
    print(f"  solving moves no paint -- the solved film is the same film typed out: "
          f"{'yes' if np.array_equal(solved.canvas.rgb, again.canvas.rgb) else 'NO'}")


# -- 4. the grounds, and a picture that sits below all of them -----------------------------
def probe_low_key_ground() -> None:
    print("\n== no preset ground suits a low-key picture ==")
    p = Palette()
    for name, hex_value in GROUNDS.items():
        print(f"  {name:18s} {hex_value}  {p.value_of(hex_value):.3f}")
    lowest = min(GROUNDS, key=lambda k: p.value_of(GROUNDS[k]))
    print(f"  the lowest preset is {lowest} at {p.value_of(GROUNDS[lowest]):.3f}.")
    print(f"  the session took cool_grey at {p.value_of(GROUNDS['cool_grey']):.3f}, and its")
    print("  masses were planned at 0.142, 0.16, 0.30, 0.34 -- every one of them below it.")
    custom = "#5a5045"
    print(f"  a ground of its own: Session(ground={custom!r}) reads "
          f"{p.value_of(custom):.3f}.")
    s = Session(256, 192, texture="linen", ground=custom, seed=3, timelapse=False)
    print(f"  and the canvas agrees: {p.value_of(s.sample()):.3f}")
    print("  read: a ground takes any colour, so the mechanism was always there. What was")
    print("        missing is a sentence pointing at it where the presets are listed.")


# -- 5. the pairs question, on the plan this session wrote ---------------------------------
def probe_plan_pairs() -> None:
    print("\n== compare({place: value}) on the empty canvas ==")
    print("  the eighth session's own nine-value plan, off paintings/Claude/pool_night/, run")
    print("  through the question it never asked.")
    plan = {
        Region(0.0, 0.0, 1.0, 0.25, "roof dark"): 0.16,
        Region(0.0, 0.05, 1.0, 0.20, "truss"): 0.142,
        Region(0.0, 0.20, 1.0, 0.36, "wall"): 0.34,
        Region(0.0, 0.36, 0.5, 0.50, "deck far"): 0.30,
        Region(0.0, 0.75, 1.0, 1.00, "deck near"): 0.44,
        Region(0.5, 0.44, 1.0, 0.62, "water"): 0.66,
        Region(0.2, 0.62, 0.9, 0.78, "water deep"): 0.57,
        Region(0.0, 0.78, 0.6, 0.95, "water reflected"): 0.40,
        Region(0.55, 0.50, 0.75, 0.60, "water lit"): 0.82,
        Region(0.60, 0.52, 0.68, 0.56, "lamp core"): 0.93,
        Region(0.80, 0.70, 0.95, 0.80, "coping"): 0.50,
    }
    s = new()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        table = str(s.compare(plan))
    lines = table.splitlines()
    start = next((i for i, ln in enumerate(lines) if "planned within" in ln), None)
    if start is None:
        print("  no pairs reported")
        return
    print("  " + lines[start])
    for line in lines[start + 1:]:
        if not line.endswith(" apart"):
            break
        print("  " + line)
    print("  read: the coping at 0.50 against the near deck at 0.44 is the session's own")
    print("        worst structural fault, found at stroke 137 with sample(). It is here")
    print("        on the empty canvas, before a mark, in one line.")


def main() -> None:
    probe_direction_sequence()
    probe_inward_window()
    probe_glaze_window()
    probe_low_key_ground()
    probe_plan_pairs()
    print()


if __name__ == "__main__":
    main()
