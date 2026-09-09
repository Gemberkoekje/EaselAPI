"""The ``easel`` command line: a thin wrapper over :class:`easel.session.Session`.

The CLI exists so a painter can work in small increments from a shell without
holding a Python process open. Session state lives in a single ``.easel`` file, so
each command loads it, does one thing, and saves it back::

    easel new painting.easel --size 1024x768 --texture linen --ground toned_grey
    easel run painting.easel first_pass.py
    easel look painting.easel --grid
    easel export painting.easel painting.png

A script given to ``easel run`` is executed with the session already bound to the
name ``s`` (and ``session``), plus the whole public API in scope. It does not need
imports of its own.
"""

from __future__ import annotations

import argparse
import sys
import traceback
from pathlib import Path

from easel.brush import BRUSHES
from easel.canvas import GROUNDS
from easel.palette import PIGMENTS
from easel.prepare import LEVELS
from easel.regions import REGION_NAMES
from easel.session import Session
from easel.texture import TEXTURES

__all__ = ["main"]

_REGION_HELP = (
    "a named region (" + ", ".join(REGION_NAMES) + "), a grid cell like D4, "
    "or a span like C3:F6"
)


def _parse_size(text: str) -> tuple[int, int]:
    parts = str(text).lower().replace("*", "x").split("x")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(f"Size must look like 1024x768, got {text!r}")
    try:
        w, h = int(parts[0]), int(parts[1])
    except ValueError:
        raise argparse.ArgumentTypeError(f"Size must be two integers, got {text!r}") from None
    if w < 8 or h < 8:
        raise argparse.ArgumentTypeError(f"Size must be at least 8x8, got {text!r}")
    return w, h


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="easel",
        description="A headless painting engine. Paint, look, repeat.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_new = sub.add_parser("new", help="create a new session file")
    p_new.add_argument("session", type=Path)
    p_new.add_argument("--size", type=_parse_size, default="1024x768", help="WIDTHxHEIGHT")
    p_new.add_argument("--texture", choices=TEXTURES, default="linen")
    p_new.add_argument("--ground", default="white", help=f"one of: {', '.join(sorted(GROUNDS))}")
    p_new.add_argument("--seed", type=int, default=0)
    p_new.add_argument("--out-dir", type=Path, default=Path("out"))
    p_new.add_argument("--no-timelapse", action="store_true")
    p_new.add_argument("--force", action="store_true",
                       help="overwrite an existing session file")

    p_run = sub.add_parser("run", help="run a painting script against a session")
    p_run.add_argument("session", type=Path)
    p_run.add_argument("script", type=Path)

    p_look = sub.add_parser("look", help="render a view of the canvas")
    p_look.add_argument("session", type=Path)
    p_look.add_argument("--grid", action="store_true", help="overlay the labelled A-H/1-8 grid")
    p_look.add_argument("--fine", action="store_true",
                        help="label tenths of what is on screen instead of the A-H/1-8 grid")
    p_look.add_argument("--values", action="store_true", help="greyscale, to judge values")
    p_look.add_argument("--region", default=None, help=_REGION_HELP)
    p_look.add_argument("--reference", type=Path, default=None, help="show a reference alongside")
    p_look.add_argument("--diff", action="store_true", help="tint what changed since last look")
    p_look.add_argument("--scale", type=int, default=None, help="long-side pixels (0 for full)")
    p_look.add_argument("--no-sketch", action="store_true", help="hide the pencil underdrawing")
    p_look.add_argument("-o", "--output", type=Path, default=None)

    p_cmp = sub.add_parser("compare", help="per-cell value of the reference, canvas and difference")
    p_cmp.add_argument("session", type=Path)
    p_cmp.add_argument("reference", type=Path)
    p_cmp.add_argument("--region", default=None,
                       help=f"measure inside a region, in its own tenths. {_REGION_HELP}")
    p_cmp.add_argument("--threshold", type=float, default=0.10, help="what counts as out")
    p_cmp.add_argument("-o", "--output", type=Path, default=None)

    p_prep = sub.add_parser("prepare", help="cut a reference into numbered masses")
    p_prep.add_argument("session", type=Path)
    p_prep.add_argument("reference", type=Path)
    p_prep.add_argument("--level", choices=sorted(LEVELS), default="coarse")
    p_prep.add_argument("--merge", action="append", default=[], metavar="A,B",
                        help="join areas, e.g. --merge 3,7. Repeatable.")
    p_prep.add_argument("--sketch", action="store_true",
                        help="also lay the outlines as pencil. ASSISTED MODE -- see PAINTER.md")
    p_prep.add_argument("-o", "--output", type=Path, default=None)

    p_mark = sub.add_parser("mark", help="record, list or forget named landmarks")
    p_mark.add_argument("session", type=Path)
    p_mark.add_argument("name", nargs="?", default=None)
    p_mark.add_argument("x", type=float, nargs="?", default=None)
    p_mark.add_argument("y", type=float, nargs="?", default=None)
    p_mark.add_argument("--forget", action="store_true", help="remove the named landmark")

    p_undo = sub.add_parser("undo", help="scrape back N strokes")
    p_undo.add_argument("session", type=Path)
    p_undo.add_argument("n", type=int, nargs="?", default=1)

    p_export = sub.add_parser("export", help="write the painting as a PNG")
    p_export.add_argument("session", type=Path)
    p_export.add_argument("output", type=Path)
    p_export.add_argument("--no-impasto", action="store_true")
    p_export.add_argument("--no-sketch", action="store_true",
                          help="the paint alone, without whatever pencil it has not covered")

    p_tl = sub.add_parser("timelapse", help="write the time-lapse")
    p_tl.add_argument("session", type=Path)
    p_tl.add_argument("output", type=Path, help=".gif for animation, .png for a contact sheet")
    p_tl.add_argument("--fps", type=float, default=8.0)

    p_log = sub.add_parser("log", help="show recent marks")
    p_log.add_argument("session", type=Path)
    p_log.add_argument("-n", type=int, default=20)

    sub.add_parser("brushes", help="list brushes, pigments, grounds and regions")

    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point for the ``easel`` command. Returns a process exit code."""
    args = build_parser().parse_args(argv)

    try:
        return _dispatch(args)
    except (OSError, ValueError, KeyError, SyntaxError) as exc:
        print(f"easel: {exc}", file=sys.stderr)
        return 1


def _dispatch(args) -> int:
    if args.command == "brushes":
        return _cmd_reference()

    if args.command == "new":
        if args.session.exists() and not args.force:
            raise FileExistsError(
                f"{args.session} already exists. Use --force to overwrite it, "
                f"or `easel undo` / paint into it directly if you meant to keep it."
            )
        w, h = args.size if isinstance(args.size, tuple) else _parse_size(args.size)
        s = Session(
            w, h,
            texture=args.texture,
            ground=args.ground,
            seed=args.seed,
            timelapse=not args.no_timelapse,
            out_dir=args.out_dir,
        )
        s.save(args.session)
        print(f"Created {args.session} ({w}x{h}, {args.texture}, ground {args.ground}, "
              f"seed {args.seed})")
        return 0

    session = Session.load(args.session)

    if args.command == "run":
        return _cmd_run(session, args)

    if args.command == "look":
        scale = None if args.scale == 0 else args.scale
        path = session.look(
            grid="fine" if args.fine else args.grid,
            values=args.values,
            region=args.region,
            reference=args.reference,
            diff=args.diff,
            path=args.output,
            sketch=not args.no_sketch,
            **({} if scale is None and args.scale is None else {"scale": scale}),
        )
        session.save(args.session)
        print(path)
        return 0

    if args.command == "compare":
        result = session.compare(args.reference, region=args.region, path=args.output,
                                 threshold=args.threshold)
        session.save(args.session)
        print(result)
        return 0

    if args.command == "prepare":
        return _cmd_prepare(session, args)

    if args.command == "mark":
        return _cmd_mark(session, args)

    if args.command == "undo":
        n = session.undo(args.n)
        session.save(args.session)
        print(f"Undid {n} stroke(s). {session.stroke_count} remain.")
        return 0

    if args.command == "export":
        path = session.export(args.output, impasto=not args.no_impasto,
                              sketch=not args.no_sketch)
        print(path)
        return 0

    if args.command == "timelapse":
        out = Path(args.output)
        path = (session.contact_sheet(out) if out.suffix.lower() == ".png"
                else session.timelapse_gif(out, fps=args.fps))
        print(path)
        return 0

    if args.command == "log":
        print(f"{session.stroke_count} strokes, seed {session.seed}, "
              f"{session.size[0]}x{session.size[1]}")
        print(session.log(args.n))
        return 0

    return 1


def _cmd_prepare(session: Session, args) -> int:
    """Cut the reference into numbered masses and print the table."""
    prep = session.prepare(args.reference, level=args.level, path=args.output)
    for pair in args.merge:
        numbers = [int(n) for n in str(pair).replace(" ", "").split(",") if n]
        if len(numbers) < 2:
            raise ValueError(f"--merge takes two or more area numbers, got {pair!r}. "
                             f"For example: --merge 3,7")
        prep.merge(*numbers)
    if args.merge:
        # The overlay has to show the map the table describes.
        session.look_areas(args.reference, path=args.output)
    if args.sketch:
        drawn = session.sketch()
        print(f"ASSISTED: laid {len(drawn)} outlines as pencil. The definition of done "
              f"reports a run that starts from this separately -- see PAINTER.md.")
    session.save(args.session)
    print(prep)
    return 0


def _cmd_mark(session: Session, args) -> int:
    """Record, list or forget a landmark."""
    if args.name is None:
        if not session.marks:
            print("No landmarks yet. easel mark painting.easel top_l 0.42 0.31")
            return 0
        for name, (x, y) in sorted(session.marks.items()):
            print(f"{name:16s} {x:.3f} {y:.3f}")
        return 0
    if args.forget:
        session.unmark(args.name)
    else:
        if args.x is None or args.y is None:
            raise ValueError(
                f"Marking {args.name!r} needs a position: "
                f"easel mark {args.session} {args.name} 0.42 0.31"
            )
        session.mark(args.name, args.x, args.y)
    session.save(args.session)
    print(f"{len(session.marks)} landmark(s): {', '.join(sorted(session.marks)) or '(none)'}")
    return 0


def _cmd_run(session: Session, args) -> int:
    """Execute a painting script with the session and the public API in scope."""
    script = Path(args.script)
    if not script.exists():
        raise FileNotFoundError(f"Script not found: {script}")

    import easel

    namespace = {name: getattr(easel, name) for name in easel.__all__}
    namespace.update(
        {"s": session, "session": session, "palette": session.palette,
         "__name__": "__easel_script__", "__file__": str(script)}
    )
    try:
        code = compile(script.read_text(encoding="utf-8"), str(script), "exec")
    except SyntaxError:
        print(f"easel: {script} does not parse\n", file=sys.stderr)
        traceback.print_exc()
        return 1

    try:
        exec(code, namespace)  # noqa: S102 - running the painter's own script is the point
    except Exception:
        # Save what was painted before the error: a half-finished pass is still work.
        session.save(args.session)
        print(f"easel: script raised, session saved with {session.stroke_count} strokes\n",
              file=sys.stderr)
        traceback.print_exc()
        return 1

    session.save(args.session)
    print(f"Ran {script.name}: {session.stroke_count} strokes total.")
    return 0


def _cmd_reference() -> int:
    print("Brushes (session.stroke(points, brush=...)):")
    for name, b in BRUSHES.items():
        print(f"  {name:12s} tip={b.tip:11s} size={b.size:<5} {_brush_blurb(name)}")
    print("\nPigments (colours; mix them on the palette):")
    for name in sorted(set(PIGMENTS)):
        print(f"  {name:16s} {PIGMENTS[name]}")
    print("\nGrounds (Session(ground=...)):")
    for name, hexv in sorted(GROUNDS.items()):
        print(f"  {name:16s} {hexv}")
    print("\nCanvas textures:", ", ".join(TEXTURES))
    print("\nRegions (region(...)):")
    print("  " + ", ".join(REGION_NAMES))
    print("\nGrid cells: A1 through H8, via cell('D6').")
    return 0


_BLURBS = {
    "round_soft": "blending and soft edges; the least painterly, use sparingly",
    "round_hard": "deliberate marks, accents, small deliberate shapes",
    "liner": "fine lines at feature scale; holds its load, no jitter",
    "flat": "block-in, chisel edges, planes; follows the stroke direction",
    "bristle": "the workhorse: broken, streaky, alive. Reach for this first",
    "knife": "thick slabs with a hard edge; drags what it crosses",
    "smudge": "carries no paint; moves what is already on the canvas",
}


def _brush_blurb(name: str) -> str:
    return _BLURBS.get(name, "")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
