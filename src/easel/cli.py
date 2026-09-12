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
from dataclasses import dataclass
from pathlib import Path

from PIL import Image as _PILImage

from easel import guide
from easel.brush import BRUSHES
from easel.canvas import GROUNDS
from easel.palette import PIGMENTS
from easel.prepare import LEVELS
from easel.regions import REGION_NAMES
from easel.session import Session
from easel.texture import TEXTURES

__all__ = ["main", "build_parser", "parse_size", "reference_text", "run_script",
           "ScriptResult"]

_REGION_HELP = (
    "a named region (" + ", ".join(REGION_NAMES) + "), a grid cell like D4, "
    "or a span like C3:F6"
)


def parse_size(text: str) -> tuple[int, int]:
    """``"1024x768"`` as a (width, height) pair. Raises ``ValueError`` on anything else.

    Shared with the MCP server, which takes the same string for the same reason:
    one spelling of a canvas size, and one set of complaints about a bad one.
    """
    parts = str(text).lower().replace("*", "x").split("x")
    if len(parts) != 2:
        raise ValueError(f"Size must look like 1024x768, got {text!r}")
    try:
        w, h = int(parts[0]), int(parts[1])
    except ValueError:
        raise ValueError(f"Size must be two integers, got {text!r}") from None
    if w < 8 or h < 8:
        raise ValueError(f"Size must be at least 8x8, got {text!r}")
    return w, h


def _parse_size(text: str) -> tuple[int, int]:
    """``parse_size`` as an argparse type, so a bad --size prints usage rather than a trace."""
    try:
        return parse_size(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from None


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
    p_new.add_argument("--budget", type=int, default=None,
                       help="how many strokes this painting is allowed; "
                            "`run` then prints spent and remaining")
    p_new.add_argument("--no-timelapse", action="store_true")
    p_new.add_argument("--force", action="store_true",
                       help="overwrite an existing session file")

    p_run = sub.add_parser("run", help="run a painting script against a session")
    p_run.add_argument("session", type=Path)
    p_run.add_argument("script", type=Path)
    p_run.add_argument("--rehearse", action="store_true",
                       help="run the pass against a copy: write the look, print the "
                            "cost, commit nothing")
    p_run.add_argument("--prelude", type=Path, default=None,
                       help="run this file first, in the same scope (helpers, "
                            "mixtures, landmarks)")
    p_run.add_argument("--no-prelude", action="store_true",
                       help="do not auto-load prelude.py from beside the session")

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
    p_tl.add_argument("--every", type=int, default=1,
                      help="keep every nth frame (GIF only); the last frame is always kept")
    p_tl.add_argument("--scale", type=int, default=None,
                      help="long side in pixels (GIF only)")

    p_log = sub.add_parser("log", help="show recent marks")
    p_log.add_argument("session", type=Path)
    p_log.add_argument("-n", type=int, default=20)

    sub.add_parser("brushes", help="list brushes, pigments, grounds and regions")

    p_guide = sub.add_parser(
        "guide",
        help="print the painting guide that ships with the engine",
        description="Print PAINTER.md, the guide this engine is written around. "
                    "With no arguments: `The first hour`, which is the whole "
                    "method in under a thousand words and enough to start.",
    )
    g_which = p_guide.add_mutually_exclusive_group()
    g_which.add_argument("--full", action="store_true",
                         help="the whole guide, not just its first page")
    g_which.add_argument("--reference", action="store_true",
                         help="REFERENCE.md instead: units, defaults, every argument")
    g_which.add_argument("--calibration", action="store_true",
                         help="CALIBRATION.md instead: the measured numbers behind the rules")
    p_guide.add_argument("--path", action="store_true",
                         help="print where the document is, rather than what it says")

    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point for the ``easel`` command. Returns a process exit code."""
    args = build_parser().parse_args(argv)

    try:
        return _dispatch(args)
    except (OSError, ValueError, KeyError, SyntaxError,
            _PILImage.DecompressionBombError) as exc:
        # DecompressionBombError is Pillow's guard against a crafted or merely
        # huge reference image decoding into an enormous array; it subclasses
        # plain Exception rather than OSError, so without naming it here it
        # escaped this handler as a raw traceback instead of the same clean
        # "easel: ..." message every other bad-input case gets.
        print(f"easel: {exc}", file=sys.stderr)
        return 1


def _cmd_guide(args) -> int:
    """`easel guide`: hand the painter the method, not just the brush.

    A session that installed from PyPI has no repository to read, and the guide
    is the half of this project that the measured runs say matters. So it is in
    the package, and this is how it is read without leaving the shell.
    """
    name = ("reference" if args.reference
            else "calibration" if args.calibration
            else "guide")

    if args.path:
        print(guide.document_path(name))
        return 0

    text = guide.read(name) if (args.full or name != "guide") else guide.front_page()
    guide.write(text)
    return 0


def _dispatch(args) -> int:
    if args.command == "brushes":
        return _cmd_reference()

    if args.command == "guide":
        return _cmd_guide(args)

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
            budget=args.budget,
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
                else session.timelapse_gif(out, fps=args.fps, every=args.every,
                                           scale=args.scale))
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
    if args.forget and args.name is None:
        raise ValueError(
            f"easel mark {args.session} --forget needs a name: "
            f"easel mark {args.session} top_l --forget"
        )
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


@dataclass(frozen=True)
class ScriptResult:
    """What running a painting script came to, before anyone decides how to say it.

    ``code`` is the process exit code the CLI returns; ``report`` is the one line
    about what happened; ``trace`` is the traceback, or ``""``; ``save`` says whether
    there is anything to write back. Split out from the printing because the MCP
    server runs the same scripts and has to hand the same words back as a tool
    result rather than print them -- and a second copy of the save-what-was-painted
    rules is a second place for them to go wrong.
    """

    code: int
    report: str
    trace: str = ""
    save: bool = True

    @property
    def text(self) -> str:
        return f"{self.report}\n\n{self.trace}".rstrip() if self.trace else self.report


def run_script(session: Session, source: str, name: str,
               prelude: str = "", prelude_name: str = "prelude.py") -> ScriptResult:
    """Execute a painting script with the session and the public API in scope.

    ``name`` is what the script is called: a path from the CLI, a plain label from
    the server, where the script arrives as text. Tracebacks name it in full and the
    report names its last part, which is what the CLI has always printed.

    ``prelude`` is source run first, in the *same* scope, so a painter working from a
    shell can keep helpers, mixtures and landmarks in one file instead of opening
    every pass with ``exec(open("helpers.py").read())``. It is the painter's own
    file either way -- named with ``--prelude``, or found beside the session.

    Nothing is written here: the caller saves when :attr:`ScriptResult.save` says to,
    because it is the caller that knows where the session file lives.
    """
    import easel

    short = Path(name).name

    namespace = {n: getattr(easel, n) for n in easel.__all__}
    namespace.update(
        {"s": session, "session": session, "palette": session.palette,
         "__name__": "__easel_script__", "__file__": name}
    )
    if prelude:
        try:
            exec(compile(prelude, prelude_name, "exec"), namespace)  # noqa: S102
        except SyntaxError:
            return ScriptResult(1, f"easel: {prelude_name} does not parse",
                                traceback.format_exc(), save=False)
        except Exception:
            # The prelude is meant to be helpers and mixtures. If it raised, the
            # pass has not started, so there is nothing new to save -- and running
            # the script on top of a half-built scope would fail somewhere less
            # informative than here.
            return ScriptResult(1, f"easel: {prelude_name} raised before "
                                   f"{short} ran", traceback.format_exc(), save=False)

    try:
        code = compile(source, name, "exec")
    except SyntaxError:
        # Nothing ran, so there is nothing new to save.
        return ScriptResult(1, f"easel: {name} does not parse",
                            traceback.format_exc(), save=False)

    try:
        exec(code, namespace)  # noqa: S102 - running the painter's own script is the point
    except SystemExit as exc:
        # sys.exit()/exit()/quit() raise this, not Exception, so it is not caught
        # by the except below -- left unhandled it propagates straight out of
        # main() and skips the save entirely. A script that exits early
        # (deliberately, or a stray exit()/quit() copied from an interactive
        # example) would then silently discard everything painted so far, and
        # with code 0 the CLI would look like it had succeeded with nothing saved
        # and no message printed at all.
        return ScriptResult(
            exc.code if isinstance(exc.code, int) else (1 if exc.code else 0),
            f"easel: {short} called exit(); session saved with "
            f"{session.stroke_count} strokes",
        )
    except Exception:
        # Save what was painted before the error: a half-finished pass is still work.
        return ScriptResult(1, f"easel: script raised, session saved with "
                               f"{session.stroke_count} strokes", traceback.format_exc())

    if session.budget is None:
        return ScriptResult(0, f"Ran {short}: {session.stroke_count} strokes total.")
    return ScriptResult(0, f"Ran {short}: {session.budget_line()}.")


def _resolve_prelude(args) -> tuple[str, str]:
    """The prelude source to run before a pass, and what to call it.

    Named with ``--prelude``, or a ``prelude.py`` sitting beside the session file --
    which is the painter's own working directory, not anywhere this went looking.
    Auto-loading is announced rather than silent, and ``--no-prelude`` turns it off.
    """
    if args.prelude is not None:
        path = Path(args.prelude)
        if not path.exists():
            raise FileNotFoundError(f"Prelude not found: {path}")
        return path.read_text(encoding="utf-8"), str(path)
    if args.no_prelude:
        return "", ""
    beside = Path(args.session).resolve().parent / "prelude.py"
    if beside.exists():
        return beside.read_text(encoding="utf-8"), str(beside)
    return "", ""


def _cmd_run(session: Session, args) -> int:
    """Execute a painting script with the session and the public API in scope."""
    script = Path(args.script)
    if not script.exists():
        raise FileNotFoundError(f"Script not found: {script}")

    prelude, prelude_name = _resolve_prelude(args)
    if prelude and args.prelude is None:
        print(f"Prelude: {prelude_name}")

    # A rehearsal runs the pass against a copy of the session. The strokes are
    # seeded as if they were the next marks of the real painting, so what is
    # rehearsed is what lands when the same pass is run for real -- and because the
    # session file is never written, it costs nothing but the look.
    target = session.scratch() if args.rehearse else session

    result = run_script(target, script.read_text(encoding="utf-8"), str(script),
                        prelude=prelude, prelude_name=prelude_name or "prelude.py")

    if args.rehearse:
        if result.code == 0:
            path = target.look(path=None)
            spent = target.stroke_count
            left = session.remaining
            cost = (f"{spent} strokes" if left is None
                    else f"{spent} strokes of the {left} left")
            print(f"Rehearsed {Path(args.script).name}: {cost}. Nothing committed.")
            print(path)
        else:
            print(f"{result.report}\n", file=sys.stderr)
            if result.trace:
                print(result.trace, file=sys.stderr, end="")
        return result.code

    if result.save:
        session.save(args.session)
    if result.code == 0:
        print(result.report)
    else:
        print(f"{result.report}\n", file=sys.stderr)
        if result.trace:
            print(result.trace, file=sys.stderr, end="")
    return result.code


def reference_text() -> str:
    """What ``easel brushes`` prints: every name the painter can say, in one place.

    A string rather than a print, because the MCP server answers the same question
    and two copies of this list would drift the first time a pigment was added.
    """
    lines = ["Brushes (session.stroke(points, brush=...)):"]
    for name, b in BRUSHES.items():
        lines.append(f"  {name:12s} tip={b.tip:11s} size={b.size:<5} {_brush_blurb(name)}")
    lines.append("  " + "-" * 62)
    lines.append("  Any brush field can be overridden per mark: size, opacity, load,")
    lines.append("  load_falloff, spacing, jitter... and on the round tips,")
    lines.append("  tip_wobble=0..1 -- an irregular silhouette, redrawn per mark, for")
    lines.append("  a small mark that should not read as the brush's own disc.")
    lines.append("\nPigments (colours; mix them on the palette):")
    for name in sorted(set(PIGMENTS)):
        lines.append(f"  {name:16s} {PIGMENTS[name]}")
    lines.append("\nGrounds (Session(ground=...)):")
    for name, hexv in sorted(GROUNDS.items()):
        lines.append(f"  {name:16s} {hexv}")
    lines.append("\nCanvas textures: " + ", ".join(TEXTURES))
    lines.append("\nRegions (region(...)):")
    lines.append("  " + ", ".join(REGION_NAMES))
    lines.append("\nGrid cells: A1 through H8, via cell('D6').")
    lines.append("\nShapes -- a mass that is not a rectangle, for block_in(...):")
    lines.append("  polygon(points)                 an outline you already have")
    lines.append("  ellipse(place, rx, ry, rotate)  a round mass, or one filling a cell")
    lines.append("  blob(place, radius, seed=)      an irregular silhouette")
    lines.append("  hull([points])                  the mass around three or four landmarks")
    lines.append("  ribbon(points, width)           a mass running along a line")
    return "\n".join(lines)


def _cmd_reference() -> int:
    print(reference_text())
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
