"""Abstract warm-up exercises, straight from PAINTER.md.

Deliberately not pictures of anything. These calibrate your sense of what the
palette reaches, what the pressure profiles do, and how wet paint behaves, without
suggesting a subject.

    python examples/exercises.py            # writes out/ex_*.png
"""

from __future__ import annotations

from pathlib import Path

from easel import Region, Session, blob, cell, region

OUT = Path("out")


def value_scale() -> None:
    """Nine steps, dark to light. Check them in greyscale, not in colour."""
    s = Session(900, 200, ground="toned_grey", seed=1, out_dir=OUT)
    for i in range(9):
        band = Region(i / 9.0, 0.15, (i + 1) / 9.0, 0.85)
        s.block_in(
            band, "flat",
            s.palette.mix("burnt_umber", "titanium_white", i / 8.0),
            density=1.0, size=0.06,
        )
    s.export(OUT / "ex_value_scale.png")
    s.look(values=True, path=OUT / "ex_value_scale_values.png")


def pressure_profiles() -> None:
    """The same gesture under each pressure profile.

    The low opacity and the flat load are what make this legible. Pressure scales
    how heavily paint lands, not how wide the mark is, so at full strength the
    overlapping dabs saturate and all six profiles come out identical -- and paint
    running out along the stroke hides the profile behind its own fade.
    """
    s = Session(900, 500, ground="toned_grey", seed=2, out_dir=OUT)
    for i, p in enumerate(["taper", "press_in", "lift_off", "even", "swell", "dab"]):
        y = 0.12 + i * 0.15
        s.stroke([(0.10, y), (0.50, y)], "round_soft", "titanium_white", pressure=p,
                 size=0.05, opacity=0.35, load=1.0, load_falloff=0.0, note=p)
        s.stroke([(0.55, y), (0.92, y)], "bristle", "titanium_white", pressure=p,
                 size=0.05, opacity=0.35, load=1.0, load_falloff=0.0, note=p)
    s.export(OUT / "ex_pressure.png")


def paint_running_out() -> None:
    """Four loads on rough canvas. Dry brush is not an effect, it is running out."""
    s = Session(900, 400, texture="rough", ground="toned_grey", seed=3, out_dir=OUT)
    for i, load in enumerate([1.0, 0.6, 0.35, 0.2]):
        y = 0.15 + i * 0.22
        s.stroke([(0.06, y), (0.94, y)], "bristle", "titanium_white",
                 size=0.07, load=load, load_falloff=0.0, pressure="even",
                 note=f"load={load}")
    s.export(OUT / "ex_load.png")


def wet_versus_dry() -> None:
    """The same yellow over blue: into wet paint above, onto dry paint below.

    One stroke per band, deliberately. A block-in is ten to thirty strokes and
    wetness fades with every mark made anywhere, so blocking these bands in leaves
    the "wet" one already dry by the time the yellow lands -- and the exercise then
    demonstrates the exact opposite of what it is for.
    """
    s = Session(800, 400, ground="white", seed=4, out_dir=OUT)
    s.stroke([(0.10, 0.27), (0.90, 0.27)], "flat", "ultramarine",
             size=0.22, pressure="even")
    s.stroke([(0.15, 0.27), (0.85, 0.27)], "flat", "cadmium_yellow",
             size=0.10, pressure="even", note="into wet blue")
    s.stroke([(0.10, 0.73), (0.90, 0.73)], "flat", "ultramarine",
             size=0.22, pressure="even")
    s.dry()
    s.stroke([(0.15, 0.73), (0.85, 0.73)], "flat", "cadmium_yellow",
             size=0.10, pressure="even", note="onto dry blue")
    s.export(OUT / "ex_wet_dry.png")


def edge_study() -> None:
    """One hard edge, one soft, one lost. Notice where your eye goes."""
    s = Session(900, 300, ground="toned_grey", seed=5, out_dir=OUT)
    thirds = region("all").split_h(3)
    for r in thirds:
        s.block_in(r, "bristle", "burnt_umber", density=1.0, size=0.1)
    s.dry()
    light = s.palette.tint("burnt_umber", 0.6)
    s.block_in(thirds[0], "bristle", light, density=1.0, size=0.1)
    s.stroke([(0.02, 0.5), (0.31, 0.5)], "round_hard", light, size=0.03)  # hard
    s.smudge([(0.35, 0.3), (0.35, 0.7)], size=0.09)                       # soft
    s.export(OUT / "ex_edges.png")


def mixing() -> None:
    """What the pigments actually do together."""
    p = Session(600, 200, seed=6, timelapse=False).palette
    pairs = [
        ("cadmium_yellow", "ultramarine"),
        ("cadmium_red", "ultramarine"),
        ("cadmium_yellow", "cadmium_red"),
        ("cerulean", "titanium_white"),
        ("burnt_umber", "titanium_white"),
    ]
    for a, b in pairs:
        print(f"  {a:16s} + {b:16s} -> {p.hex(p.mix(a, b, 0.5))}")


def draw_try_paint() -> None:
    """The precision loop, on a shape that is not a picture of anything.

    Three verified points, a drawing hung on them, two rehearsals that cost nothing,
    and one stroke spent on the better of them. Afterwards the graphite is gone
    exactly where the paint landed and still there beside it, which is what an
    underdrawing is for.
    """
    s = Session(900, 600, ground="toned_grey", seed=7, timelapse=False, out_dir=OUT)
    s.mark("a", *cell("C3").point(0.5, 0.5))
    s.mark("b", *cell("F3").point(0.5, 0.5))
    s.mark("c", *cell("D6").point(0.5, 0.5))
    s.pencil([s.pt("a"), s.pt("b"), s.pt("c"), s.pt("a")], pressure=0.7)
    s.look(path=OUT / "ex7_drawing.png")

    plan = [{"points": [s.pt("a"), s.pt("c")], "brush": "bristle", "size": 0.09,
             "color": "titanium_white"}]
    s.rehearse(plan, region="C3:F6", path=OUT / "ex7_rehearse_wide.png")
    s.rehearse([dict(plan[0], size=0.03, brush="liner")], region="C3:F6",
               path=OUT / "ex7_rehearse_fine.png")

    strokes_before, records_before = s.stroke_count, len(s.history.records)
    s.stroke(**plan[0])
    print(f"  drawing + two rehearsals cost {strokes_before} strokes and "
          f"{records_before - 1} log entries beyond the pencil line")
    s.look(region="C3:F6", path=OUT / "ex7_painted.png")


def a_box_and_a_shape() -> None:
    """8. The same mass as a rectangle and as a shape, side by side."""
    s = Session(900, 400, ground="toned_grey", seed=3, out_dir=OUT)
    s.palette["dark"] = s.palette.mix("ultramarine", "burnt_umber", 0.45)

    mass = blob(cell("B4").point(0.5, 0.5), 0.16, 0.30, wobble=0.3, seed=1)
    boxed = s.block_in(mass.box, "bristle", "dark", size=0.10, direction="axis")
    shaped = s.block_in(mass.shifted(0.5, 0.0), "bristle", "dark", size=0.10,
                        direction="axis")
    print(f"  the box took {len(boxed)} passes, the shape {len(shaped)}")
    s.look(path=OUT / "ex8_box_and_shape.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for fn in (value_scale, pressure_profiles, paint_running_out,
               wet_versus_dry, edge_study, draw_try_paint, a_box_and_a_shape):
        print(f"{fn.__name__} ...")
        fn()
    print("mixing:")
    mixing()
    print(f"\nWrote exercises to {OUT.resolve()}")


if __name__ == "__main__":
    main()
