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
import warnings
from dataclasses import dataclass
from pathlib import Path

from PIL import Image as _PILImage

from easel import demo, diagnosis, docs, notices
from easel.brush import BRUSHES
from easel.canvas import GROUNDS
from easel.look import DEFAULT_LOOK_SIZE, label_sheet, save_look
from easel.notices import NOTICES, EaselWarning
from easel.palette import PIGMENTS
from easel.prepare import LEVELS
from easel.regions import REGION_NAMES
from easel.session import _MAX_PANELS, Session, _panel_label, _panel_scale
from easel.texture import TEXTURES

__all__ = ["main", "build_parser", "parse_size", "reference_text", "run_script",
           "run_scripts", "run_alternatives", "ScriptResult", "Alternative",
           "Alternatives"]

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


def _example_codes() -> str:
    """One code of each kind, for `easel explain --help` to show what one looks like.

    Read off the registry rather than typed, because a typed one went stale: the help
    offered `spill` as an example for a while, which was a code this round had planned
    and not built, so the one place the tool demonstrates its own vocabulary was
    advertising a word it answers *unknown notice* to. A list that cannot be wrong is
    better than a list somebody has to remember to update -- and one fact beside one
    habit says more about the vocabulary than three facts would.
    """
    first = [next((code for code, spec in sorted(NOTICES.items()) if spec.kind == kind),
                  None)
             for kind in notices.KINDS]
    return ", ".join(f"`{code}`" for code in first if code)


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
    p_new.add_argument("--no-timelapse", action="store_true",
                       help="no time-lapse: `easel timelapse` then needs --from-log")
    p_new.add_argument("--frame-px", type=int, default=None,
                       help="the long side of each time-lapse frame, in pixels "
                            "(default 360): the size `easel timelapse` rebuilds the "
                            "film at, since the session file keeps no frames")
    p_new.add_argument("--force", action="store_true",
                       help="overwrite an existing session file")
    p_new.add_argument("--no-prelude", action="store_true",
                       help="do not write a prelude.py beside the session. The "
                            "scaffold holds the s.plan(...) call every pass then runs "
                            "before it, which is where what the painting is for gets "
                            "written down")

    p_run = sub.add_parser("run", help="run one or more painting scripts against a session")
    p_run.add_argument("session", type=Path)
    p_run.add_argument("script", type=Path, nargs="+",
                       help="one or more scripts, run in the order given against the "
                            "same session -- with --rehearse, against one copy, so a "
                            "pass that goes on top of another is judged on it; with "
                            "--alternatives, each against a copy of its own")
    p_run.add_argument("--rehearse", action="store_true",
                       help="run the pass against a copy: write the look, print the "
                            "cost, commit nothing")
    p_run.add_argument("--count", action="store_true",
                       help="price the pass without painting it: a rehearsal with "
                            "the pixel work skipped, so a helper that calls a dozen "
                            "verbs has a price in a second. No look, nothing "
                            "committed. Implies --rehearse")
    p_run.add_argument("--alternatives", action="store_true",
                       help="the scripts are versions of one pass, not passes on top "
                            "of each other: rehearse each on a copy of its own, print "
                            "each one's check, and lay their looks side by side in one "
                            "sheet. Implies --rehearse; with --count, prices each and "
                            "lays no sheet")
    p_run.add_argument("--prelude", type=Path, default=None,
                       help="run this file first, in the same scope (helpers, "
                            "mixtures, landmarks)")
    p_run.add_argument("--no-prelude", action="store_true",
                       help="do not auto-load prelude.py from beside the session")
    p_run.add_argument("--check", action="store_true",
                       help="run the post-pass check over the whole painting rather "
                            "than over this pass alone")

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
    p_look.add_argument("--no-sketch", action="store_true",
                        help="hide the drawing: the pencil the paint has not covered, "
                             "and the guides s.guide() drew on the view")
    p_look.add_argument("--no-marks", action="store_true",
                        help="hide the landmarks, whose labels sit over the details "
                             "they name")
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

    p_undo = sub.add_parser("undo", help="scrape back N log records")
    p_undo.add_argument("session", type=Path)
    p_undo.add_argument("n", type=int, nargs="?", default=1)

    p_export = sub.add_parser("export", help="write the painting as a PNG")
    p_export.add_argument("session", type=Path)
    p_export.add_argument("output", type=Path)
    p_export.add_argument("--no-impasto", action="store_true")
    p_export.add_argument("--no-sketch", action="store_true",
                          help="the paint alone, without whatever pencil it has not covered")

    p_tl = sub.add_parser(
        "timelapse", help="write the time-lapse",
        description="The session file keeps no frames, so the film is rebuilt from "
                    "the log at the session's frame size: a full repaint, about half "
                    "a minute for a painting of a couple of hundred marks. A file "
                    "saved before 0.7.0 that kept its frames uses them.")
    p_tl.add_argument("session", type=Path)
    p_tl.add_argument("output", type=Path, help=".gif for animation, .png for a contact sheet")
    p_tl.add_argument("--fps", type=float, default=8.0)
    p_tl.add_argument("--every", type=int, default=1,
                      help="keep every nth frame (GIF only); the last frame is always kept")
    p_tl.add_argument("--scale", type=int, default=None,
                      help="long side in pixels (GIF only); shrinks the frames, which "
                           "are made at the session's frame size")
    p_tl.add_argument("--from-log", action="store_true",
                      help="build the frames at --scale rather than at the session's "
                           "frame size, the canvas's own when --scale is left off. "
                           "Also a full repaint, and works on a painting made with "
                           "--no-timelapse")

    p_plan = sub.add_parser(
        "plan",
        help="declare what this painting is for, and what the check should hold it to",
        description="What a painter is told to write down before the first mark, "
                    "written where the engine can see it. With no arguments it prints "
                    "the plan the session is holding. Each argument changes one thing "
                    "and keeps the rest, so the values can be declared once and the "
                    "lightest place added later.",
    )
    p_plan.add_argument("session", type=Path)
    p_plan.add_argument("--why", default=None,
                        help="what the picture is for, in a sentence. Nothing measures "
                             "it; the closing check quotes it back")
    p_plan.add_argument("--value", action="append", default=None, metavar="PLACE=VALUE",
                        help="a place and the value you mean to paint it: "
                             "--value 'A1:H3=0.70'. Repeatable, and the whole set "
                             "replaces any declared before. The check then says how "
                             "many places are painted as promised")
    p_plan.add_argument("--lightest", default=None, metavar="PLACE",
                        help="the place meant to be the lightest thing in the picture")
    p_plan.add_argument("--subject-share", type=float, default=None, metavar="SHARE",
                        help="the share of the budget the subject gets, 0..1")
    p_plan.add_argument("--bands", choices=["subject", ""], default=None,
                        help="'subject' declares that this picture's subject really "
                             "does run in one direction, so the stack-of-bars line "
                             "counts what crosses the bars instead of warning")
    p_plan.add_argument("--ground", choices=["showing", "buried", ""], default=None,
                        help="'buried' says this picture covers its ground on purpose, "
                             "so the ground line stops asking for some back. 'showing' "
                             "is the default expectation, and '' takes the declaration "
                             "back, as it does for --bands")
    p_plan.add_argument("--clear", action="store_true",
                        help="forget the plan entirely and start again")

    p_check = sub.add_parser(
        "check",
        help="the closing checklist, answered: every measured line with its number",
        description="What to run when the painting looks finished. Every line of "
                    "PAINTER.md's closing checklist that has a number behind it, "
                    "answered -- the values, the edges, the ground, the boxes, the "
                    "subject's share, what is left of the budget -- and then the "
                    "three questions nothing can measure, with the plan's own `why` "
                    "quoted back. `easel log --check` is the same measurements after "
                    "a pass; this one is the end of the painting.",
    )
    p_check.add_argument("session", type=Path)
    p_check.add_argument("--subject-share", type=float, default=None, metavar="SHARE",
                         help="the share of the budget the subject was to get, 0..1. "
                              "The plan's own is used when this is left off")

    p_log = sub.add_parser("log", help="show recent marks")
    p_log.add_argument("session", type=Path)
    p_log.add_argument("-n", type=int, default=20,
                       help="how many marks to show -- or with --reports, how many "
                            "reports")
    g_log = p_log.add_mutually_exclusive_group()
    g_log.add_argument("--check", action="store_true",
                       help="run the post-pass check over the whole painting instead")
    g_log.add_argument("--reports", action="store_true",
                       help="what each `easel run` printed after its pass, as the "
                            "session file kept it -- rehearsed and counted passes "
                            "included, each saying which it was")

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
    g_which.add_argument("--painting", action="store_true",
                         help="PAINTING.md instead: how the paint and the brushes behave, read once")
    g_which.add_argument("--recipes", action="store_true",
                         help="RECIPES.md instead: one situation at a time, the calls in order")
    g_which.add_argument("--reference", action="store_true",
                         help="REFERENCE.md instead: units, defaults, every argument")
    g_which.add_argument("--calibration", action="store_true",
                         help="CALIBRATION.md instead: the measured numbers behind the rules")
    g_which.add_argument("--diagnosis", action="store_true",
                         help="DIAGNOSIS.md instead: the symptom index, which `easel "
                              "diagnose` is the way to use")
    p_guide.add_argument("--path", action="store_true",
                         help="print where the document is, rather than what it says")

    p_diagnose = sub.add_parser(
        "diagnose",
        help="you have looked, it is wrong: the passage that says why",
        description="Describe what you can see on the canvas, in your own words, and "
                    "this prints the passage of the guide that measured it. It is "
                    "DIAGNOSIS.md's symptom index with the pointer already followed -- "
                    "so say what is in front of you (`concentric rings`, `a stringy "
                    "edge`, `the ground shows through`) rather than what you think "
                    "caused it. With no words: every symptom it covers.",
    )
    p_diagnose.add_argument("words", nargs="*",
                            help="what you are looking at, in your own words")
    p_diagnose.add_argument("--list", action="store_true", dest="list_only",
                            help="the symptoms that match, without their passages")

    p_explain = sub.add_parser(
        "explain",
        help="print the measurement behind one of the notices the engine gives",
        description=f"Every notice the engine gives at a call carries a code -- "
                    f"{_example_codes()}. This prints the passage of the guide that "
                    f"holds its measurement, which is where the reason for the rule "
                    f"lives. With no code: every code there is.",
    )
    p_explain.add_argument("code", nargs="?", default="",
                           help="the notice's code, as the pass printed it")

    p_demo = sub.add_parser(
        "demo",
        help="a recipe painted beside what it looks like when it goes wrong",
        description="Paints one recipe of RECIPES.md beside its commonest failure, side "
                    "by side -- the recipe, the call that goes wrong with what the tool "
                    "says about it, and the smallest fix where it is not the recipe "
                    "itself -- and prints what each panel was told. Name the recipe by "
                    "the words of its heading: `easel demo crosses a boundary`. "
                    "`easel demo mistakes` paints the six a painter meets most, one "
                    "sheet, before the exercises. With no words: every recipe, and "
                    "which of them have a demo.",
    )
    p_demo.add_argument("words", nargs="*",
                        help="the recipe, by the words of its heading, or `mistakes`")
    p_demo.add_argument("--out-dir", type=Path, default=Path("out"),
                        help="where the sheet is written, as demo-<recipe>.png")
    p_demo.add_argument("-o", "--output", type=Path, default=None,
                        help="write the sheet here instead")

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
    name = ("painting" if args.painting
            else "recipes" if args.recipes
            else "reference" if args.reference
            else "calibration" if args.calibration
            else "diagnosis" if args.diagnosis
            else "guide")

    if args.path:
        print(docs.document_path(name))
        return 0

    text = docs.read(name) if (args.full or name != "guide") else docs.front_page()
    docs.write(text)
    return 0


def _cmd_explain(args) -> int:
    """`easel explain <code>`: the reason, at the moment it applies.

    A rule whose paragraph leaves the reading path has not lost its reason -- the
    reason stops being read in advance and starts being handed over when the call
    that trips it is made. The pass prints the code; this turns the code back into
    the passage that measured it.

    With no code, the table of them, which is the same list `REFERENCE.md` carries
    and is short enough to read in a shell.
    """
    if not args.code:
        print("The engine says these at a call. `easel explain <code>` for any one.\n")
        for kind in notices.KINDS:
            print(f"  {kind}s")
            for code, spec in sorted(NOTICES.items()):
                if spec.kind == kind:
                    print(f"    {code:20s} {spec.about}")
        return 0

    docs.write(notices.explain(args.code) + "\n")
    return 0


def _cmd_diagnose(args) -> int:
    """`easel diagnose <words>`: the symptom index with the pointer already followed.

    `DIAGNOSIS.md` was built to be grepped, and the one session that had it followed
    none of its pointers -- it worked from the rows it remembered, and a remembered
    row has no measurement attached. The row is not the thing; the passage it names
    is. So this does the following, and what comes back is the passage.

    It also puts the index in the hands of a painter who installed the wheel, who
    until now had no file to grep at all.
    """
    words = " ".join(args.words)
    docs.write(diagnosis.listing(words) if args.list_only else diagnosis.answer(words))
    return 0


def _cmd_demo(args) -> int:
    """`easel demo <recipe>`: the failure a recipe describes, painted beside the recipe.

    Finding 19 asked for this in so many words -- the recommended call, what it looks
    like, the common failure, the smallest fix -- because a failure described in prose
    is one more rule to carry, and a picture of it is something to hold a rehearsal
    against. It needs no session: every panel is a fresh canvas with the guide's own
    context under it, the one `scripts/check_guide_blocks.py` holds each demo to.
    """
    text, _ = demo.answer(" ".join(args.words), out_dir=args.out_dir, path=args.output)
    docs.write(text)
    return 0


def _load(path: Path) -> Session:
    """Open a session file, and say what opening it said -- once, before anything else.

    What a file says as it opens -- an ``out_dir`` somewhere foreign, an engine older
    than this one -- used to reach the shell as a raw Python warning, file name and
    line number first, and the server not at all. It goes to stderr under its own
    heading now, because stdout is where ``easel look`` prints the path a painter's
    script reads back.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=EaselWarning)
        session = Session.load(path)
    if session._load_notices:
        print(notices.block(session._load_notices, when="at load") + "\n", file=sys.stderr)
    return session


def _dispatch(args) -> int:
    if args.command == "brushes":
        return _cmd_reference()

    if args.command == "guide":
        return _cmd_guide(args)

    if args.command == "explain":
        return _cmd_explain(args)

    if args.command == "diagnose":
        return _cmd_diagnose(args)

    if args.command == "demo":
        return _cmd_demo(args)

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
            timelapse=(False if args.no_timelapse
                       else (True if args.frame_px is None else args.frame_px)),
            out_dir=args.out_dir,
            budget=args.budget,
        )
        s.save(args.session)
        print(f"Created {args.session} ({w}x{h}, {args.texture}, ground {args.ground}, "
              f"seed {args.seed})")
        if not args.no_prelude:
            written = _write_prelude(args.session)
            if written is not None:
                print(f"Wrote {written} -- fill in s.plan(...) before the first pass")
        return 0

    session = _load(args.session)

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
            marks=not args.no_marks,
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

    if args.command == "plan":
        return _cmd_plan(session, args)

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
        sheet = out.suffix.lower() == ".png"
        if (session._film_from_log and session.timelapse) or (args.from_log and not sheet):
            # Said before the wait rather than after it: this used to be a read, and
            # a command that has gone quiet for half a minute looks like one that hung.
            print(f"Rebuilding the film from the log, {len(session.history.records)} "
                  f"records: a full repaint.", file=sys.stderr)
        path = (session.contact_sheet(out) if sheet
                else session.timelapse_gif(out, fps=args.fps, every=args.every,
                                           scale=args.scale,
                                           from_log=args.from_log))
        print(path)
        return 0

    if args.command == "check":
        # Read-only, and the one command here that does not save: a checklist asks
        # the painting questions and changes nothing about it, so writing the file
        # back would only move its timestamp.
        print(session.checklist(subject_share=args.subject_share))
        return 0

    if args.command == "log":
        print(f"{session.stroke_count} strokes, seed {session.seed}, "
              f"{session.size[0]}x{session.size[1]}")
        if args.reports:
            print(notices.saved(session.reports(), last=args.n))
        else:
            print(session.report() if args.check else session.log(args.n))
        return 0

    return 1


#: The `prelude.py` `easel new` writes beside a new session. `_resolve_prelude` already
#: runs a file of this name before every pass, and this is what goes in it.
#:
#: **A worked example is an instruction**, which is `LESSONS.md`'s own rule and the
#: reason this file exists at all. The decision taken on a painter who never declares a
#: plan was *say it where it costs*: no message at the first stroke, no nag. So the one
#: place the call is put in front of a painter is here, in the file they are about to
#: edit anyway -- commented out, because a plan filled in with somebody else's numbers
#: is worse than no plan.
PRELUDE_STUB = '''"""Run before every pass, in the same scope: helpers, mixtures, and the plan.

`easel run` executes this first and then the pass, so anything defined here is in
scope for every script -- and `s.plan(...)` declared here is declared once for the
whole painting rather than once per pass.
"""

# What the painting is for, and what the post-pass check should hold it to. Fill in
# what you have decided and leave out what you have not; `easel explain` has the
# reason behind every line the check prints.
#
# s.plan(
#     why="one sentence: what this picture is for",
#     # The places and the values you mean to paint them. Declaring them prices the
#     # pairs -- two places closer than 0.10 read as one where they meet -- and the
#     # check then says how many are painted as promised.
#     values={span("A1", "H3"): 0.70, span("A4", "H6"): 0.39},
#     lightest=span("A1", "H3"),   # the place meant to be the lightest thing in it
#     subject_share=0.40,          # the share of the budget the subject gets
#     # bands="subject",           # this picture's subject really does run one way
#     # ground="buried",           # and it covers its ground on purpose
# )
'''


def _write_prelude(session: Path) -> Path | None:
    """The `prelude.py` scaffold, beside a new session file. Returns where it went.

    ``None`` when one is already there: a prelude is the painter's own file and the
    one place their mixtures live, and `easel new --force` is about the session.
    Overwriting a prelude would throw away work that is not the session's to throw.
    """
    path = Path(session).resolve().parent / "prelude.py"
    if path.exists():
        return None
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(PRELUDE_STUB, encoding="utf-8")
    return path


def _parse_value(text: str) -> tuple[str, float]:
    """``--value 'A1:H3=0.70'`` as the place and the value it promises.

    A place is a name here rather than a shape, because a shell has no ``blob()``.
    Everything ``region()`` accepts is a name -- cells, spans, the bands and halves --
    and a plan whose places are shapes is a plan written in a ``prelude.py``, which is
    where the shapes already live.
    """
    place, sep, value = str(text).rpartition("=")
    if not sep or not place.strip():
        raise ValueError(
            f"--value {text!r} is a place and the value you mean to paint it, joined "
            f"by '=': --value 'A1:H3=0.70'. `easel brushes` lists every place name."
        )
    try:
        number = float(value)
    except ValueError:
        raise ValueError(
            f"--value {text!r} gives {value!r} as a value, and a value is a number "
            f"0..1 -- the way palette.value_of() reports it. 0.70, not '70%'."
        ) from None
    return place.strip(), number


def _cmd_plan(session: Session, args) -> int:
    """`easel plan`: the declarations, from a shell, saved in the session file.

    The plan is the shell's half of `Session.plan`. A painter working from a prelude
    writes shapes; a painter working from a shell writes place names, and both end up
    in the same `.easel` file, which is what the post-pass check reads after every
    pass. Printed rather than merely stored, because a plan the painter cannot read
    back is a plan nobody trusts.
    """
    values = (dict(_parse_value(one) for one in args.value)
              if args.value is not None else None)
    # The pairs notice is filtered here and printed below as the table it came from:
    # this command's whole output is the plan, the stderr copy would arrive above it
    # pointing at a line of this file, and the table says the same thing in full. It is
    # still kept on the session and saved, as every notice is.
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=EaselWarning)
        plan = session.plan(why=args.why, values=values, lightest=args.lightest,
                            subject_share=args.subject_share, bands=args.bands,
                            ground=args.ground, clear=args.clear)
    # Always, as every other command here does. `easel plan p.easel` with nothing to
    # declare is a read and writes the file back unchanged; a declaration that was not
    # saved is the thing this whole command exists to stop.
    session.save(args.session)
    print(plan)
    if plan.values:
        print(plan.pairs_text(session.plan_pairs()))
    return 0


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

    **A pass run against a scratch copy says so when it fails.** Read off the session
    rather than taken as an argument, because the session is the thing that knows:
    a caller that handed over a copy and then said ``rehearsing=False`` would print
    the same wrong line this exists to stop. A script that raised under ``--rehearse``
    used to report *session saved with N strokes*, with ``N`` continuing the
    painting's own count -- which is right for a script asking how far along it is,
    and reads exactly like a commit in a message about what was saved. Nothing was
    committed: the rehearsing branch returns above the save.
    """
    import easel

    short = Path(name).name
    # `stroke_count` on a copy continues the painting's numbers; `history` is the
    # copy's own log, which is what this pass laid. See `Session.scratch`.
    on_copy = bool(getattr(session, "_is_trial", False))

    def laid() -> str:
        if on_copy:
            return (f"nothing committed, the copy had laid "
                    f"{session.history.stroke_count} of this pass's marks")
        return f"session saved with {session.stroke_count} strokes"

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
            f"easel: {short} called exit(); {laid()}",
        )
    except Exception:
        # Save what was painted before the error: a half-finished pass is still work.
        return ScriptResult(1, f"easel: script raised, {laid()}",
                            traceback.format_exc())

    if session.budget is None:
        return ScriptResult(0, f"Ran {short}: {session.stroke_count} strokes total.")
    return ScriptResult(0, f"Ran {short}: {session.budget_line()}.")


def run_scripts(session: Session, scripts, prelude: str = "",
                prelude_name: str = "prelude.py") -> ScriptResult:
    """Run several painting scripts in order against one session.

    ``scripts`` is a sequence of ``(source, name)`` pairs. Each is run by
    :func:`run_script` in a **fresh** scope with the prelude re-executed in front
    of it, so that running two passes together is the same thing as running them
    one after the other -- it is the canvas that carries over between passes, not
    the namespace, and a pass that quietly depended on the last one's leftover
    variables would paint differently depending on how it was invoked.

    A pass that goes on top of another pass has to be judged on it, and a rehearsal
    of one pass alone cannot show that. ``easel run p.easel p2.py p3.py --rehearse``
    lays them on one copy in order, which is what the alternative -- a wrapper that
    ``exec()``s each file -- was doing in nobody's log.

    Stops at the first script that fails, and reports which one. What the scripts
    before it painted is still work: the result says to save it.
    """
    pairs = list(scripts)
    if not pairs:  # pragma: no cover - argparse requires at least one
        raise ValueError("run_scripts needs at least one script.")

    done: list[str] = []
    for source, name in pairs:
        result = run_script(session, source, name, prelude=prelude,
                            prelude_name=prelude_name)
        if result.code != 0:
            # Anything an earlier script painted is committed even though this one
            # failed -- the same rule run_script applies within a single pass.
            report = result.report
            if done:
                report = f"{report} (after {', '.join(done)})"
            return ScriptResult(result.code, report, result.trace,
                                save=result.save or bool(done))
        done.append(Path(name).name)

    if len(done) == 1:
        return result
    ran = ", ".join(done)
    if session.budget is None:
        return ScriptResult(0, f"Ran {ran}: {session.stroke_count} strokes total.")
    return ScriptResult(0, f"Ran {ran}: {session.budget_line()}.")


@dataclass(frozen=True)
class Alternative:
    """One version of a pass, rehearsed on a copy of its own.

    ``text`` is what it came to -- the line saying what it cost and the block after it,
    or what it raised -- and ``code`` its exit code, ``0`` when it ran. ``laid`` is the
    strokes its copy laid, and ``panel`` its look at the sheet's panel size: ``None``
    for a counted version, which lays no paint, and for one that raised.
    """

    name: str
    code: int
    text: str
    laid: int = 0
    panel: _PILImage.Image | None = None


@dataclass(frozen=True)
class Alternatives:
    """Every version :func:`run_alternatives` rehearsed, and the sheet it laid them in."""

    tried: tuple[Alternative, ...]
    sheet: Path | None = None

    @property
    def code(self) -> int:
        """The first code that is not ``0``, or ``0`` when every version ran."""
        return next((one.code for one in self.tried if one.code), 0)

    @property
    def sheet_line(self) -> str:
        """Which versions the sheet holds, and where it is -- ``""`` with no sheet."""
        if self.sheet is None:
            return ""
        shown = [one.name for one in self.tried if one.panel is not None]
        if len(shown) == 1:
            return f"{shown[0]}, on a copy of its own: {self.sheet}"
        return f"{', '.join(shown[:-1])} and {shown[-1]} side by side: {self.sheet}"

    @property
    def text(self) -> str:
        """Everything, in order, as one answer: what the MCP server hands back."""
        return "\n\n".join([one.text for one in self.tried]
                           + ([self.sheet_line] if self.sheet else []))


def run_alternatives(session: Session, scripts, prelude: str = "",
                     prelude_name: str = "prelude.py", count_only: bool = False,
                     whole: bool = False) -> Alternatives:
    """Rehearse versions of one pass, each on a copy of its own, and lay them side by side.

    ``scripts`` is a sequence of ``(source, name)`` pairs, as :func:`run_scripts` takes
    them. That lays them on **one** copy in order, so a pass is judged on the pass under
    it; this gives each its own, because what is being compared is **versions of one
    pass**. The lighthouse painter compared whole passes that way through a harness of
    its own, a file per version opened one after another, and said what would have
    replaced it: *rehearsing scripts as side-by-side alternatives*.

    Each version runs in a fresh scope with the prelude in front of it, is checked over
    what it laid -- over the whole painting under it with ``whole``, as ``--check`` --
    and keeps its report on ``session`` as a rehearsal does. Their looks are laid in one
    sheet, each panel labelled with the version and the strokes it laid; a counted run
    lays no paint, and so no sheet. **One that raises is said and left off the sheet,
    and the rest are still rehearsed**, since none of them stands on another. Every copy
    is seeded as the next marks of the painting, so whichever is then run for real
    lands as its panel shows it.

    Nothing is written but the sheet: the caller saves ``session``, whose reports have
    grown by one for every version that ran.
    """
    pairs = list(scripts)
    if not pairs:  # pragma: no cover - argparse requires at least one
        raise ValueError("run_alternatives needs at least one script.")
    if not count_only and len(pairs) > _MAX_PANELS:
        raise ValueError(
            f"{len(pairs)} alternatives would be {len(pairs)} panels, past the "
            f"{_MAX_PANELS} a sheet can be compared at a glance. Rehearse them as two "
            f"sheets -- or count them, which lays no sheet."
        )
    shorts = [Path(name).name for _, name in pairs]
    # A version is called by its file's name, as a rehearsal is -- unless two share one,
    # when the path it was given by is what tells them apart on the sheet.
    names = [short if shorts.count(short) == 1 else name
             for short, (_, name) in zip(shorts, pairs, strict=True)]
    px = _panel_scale(DEFAULT_LOOK_SIZE, len(pairs))
    left = session.remaining
    tried: list[Alternative] = []
    for i, ((source, name), label) in enumerate(zip(pairs, names, strict=True), 1):
        target = session.scratch(count_only=count_only)
        before = target._open_pass()
        told = len(target.notices())
        result = run_script(target, source, name, prelude=prelude,
                            prelude_name=prelude_name)
        said = target.notices(since=told)
        which = f"{label} ({i} of {len(pairs)})"
        if result.code != 0:
            # Said the way a rehearsal that raised is said -- what the calls that ran
            # said, then what went wrong and where -- with which version it was.
            tried.append(Alternative(label, result.code, "\n".join(
                part for part in (notices.block(said),
                                  f"{result.report} ({label}, {i} of {len(pairs)})",
                                  result.trace.rstrip()) if part)))
            continue
        check = target.report() if whole else target.report(since=before)
        block = notices.block(said, check)
        laid = target.history.stroke_count
        cost = f"{laid} strokes" if left is None else f"{laid} strokes of the {left} left"
        if count_only:
            head = f"Counted {which}: {cost}. Nothing painted, nothing committed."
            panel = None
        else:
            head = f"Rehearsed {which}: {cost}. Nothing committed."
            # The view a rehearsal's own look is, at the size one panel of the sheet has.
            panel = target.look_image(scale=px)
        session._keep_report(target, label, before, block)
        tried.append(Alternative(label, 0, "\n".join(p for p in (head, block) if p),
                                 laid, panel))
    shown = [(_panel_label(one.name, one.laid), one.panel)
             for one in tried if one.panel is not None]
    sheet = (save_look(label_sheet(shown), session._look_path(None, "rehearse"))
             if shown else None)
    return Alternatives(tuple(tried), sheet)


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
    """Execute one or more painting scripts with the session and API in scope."""
    scripts = [Path(s) for s in args.script]
    missing = [s for s in scripts if not s.exists()]
    if missing:
        # All of them up front: finding the third one missing after the first two
        # have already been painted into the session is a worse place to find out.
        raise FileNotFoundError(
            "Script not found: " + ", ".join(str(s) for s in missing))

    prelude, prelude_name = _resolve_prelude(args)
    if prelude and args.prelude is None:
        print(f"Prelude: {prelude_name}")

    if args.alternatives:
        # Versions of one pass: each on a copy of its own, each with its own check, and
        # their looks in one sheet. Warnings are said in each version's block, as below.
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=EaselWarning)
            tried = run_alternatives(
                session, [(s.read_text(encoding="utf-8"), str(s)) for s in scripts],
                prelude=prelude, prelude_name=prelude_name or "prelude.py",
                count_only=args.count, whole=args.check,
            )
        for one in tried.tried:
            # Flushed, so a version that raised is said in its place among the others.
            print(f"{one.text}\n", file=sys.stderr if one.code else sys.stdout, flush=True)
        if tried.sheet is not None:
            print(tried.sheet_line)
        # What each version's check said is kept, as a rehearsal's is, and written after
        # the printing for the same reason. A run in which none ran has nothing to keep.
        if any(one.code == 0 for one in tried.tried):
            session.save(args.session)
        return tried.code

    # A rehearsal runs the pass against a copy of the session. The strokes are
    # seeded as if they were the next marks of the real painting, so what is
    # rehearsed is what lands when the same pass is run for real -- and because
    # nothing it lays reaches the session file, it costs nothing but the look. The
    # one thing it writes there is what its check said (`Session.reports`). Several
    # scripts share the one copy, in order, so a pass is judged on the pass under it.
    # `--count` is the same copy with the pixel work skipped: the price and the check
    # in a fraction of the time, and nothing to look at. See `Session.scratch`.
    rehearsing = args.rehearse or args.count
    names = ", ".join(s.name for s in scripts)
    target = session.scratch(count_only=args.count) if rehearsing else session
    before = target._open_pass()
    told = len(target.notices())

    # Every notice the pass gives is kept on the session by `Session._notify` before
    # it is warned, so the stderr copy is the one that can go: unfiltered it arrives
    # interleaved with whatever else is on the stream, in the middle of the pass,
    # apart from the check it belongs beside, and once per source line rather than
    # once per thing said. Filtered here and printed below, it is said once, in
    # order, on stdout, under one heading with the check. Only `EaselWarning`: a
    # painter's own script, and every library under it, warns exactly as before.
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=EaselWarning)
        result = run_scripts(
            target,
            [(s.read_text(encoding="utf-8"), str(s)) for s in scripts],
            prelude=prelude, prelude_name=prelude_name or "prelude.py",
        )
    # The post-pass check, beside the budget line: what the pass just laid would be
    # warned about, read off the log. Over the pass alone unless asked for the whole
    # painting -- and a rehearsal is checked too, because that is where a pass gets
    # changed for free.
    check = target.report() if args.check else target.report(since=before)
    said = target.notices(since=told)
    block = notices.block(said, check)

    def failed() -> None:
        """A pass that raised still laid marks and still said things.

        The notices go out with the error rather than with the check, because there
        is no check: they are what the engine said about the calls that did run, and
        dropping them here would make a failing pass say *less* than it did before
        there was a channel to collect them.
        """
        if said:
            print(f"{notices.block(said)}\n", file=sys.stderr)
        print(f"{result.report}\n", file=sys.stderr)
        if result.trace:
            print(result.trace, file=sys.stderr, end="")

    if rehearsing:
        if result.code == 0:
            # What the pass itself laid: the copy's own log. Its `stroke_count`
            # continues the painting's, which is what a script inside it wants.
            spent = target.history.stroke_count
            left = session.remaining
            cost = (f"{spent} strokes" if left is None
                    else f"{spent} strokes of the {left} left")
            if args.count:
                # No look: a counted pass lays no paint, and a picture of the canvas
                # it borrowed is a picture of the last pass, which is worse than none.
                print(f"Counted {names}: {cost}. Nothing painted, nothing committed.")
                print(block)
            else:
                print(f"Rehearsed {names}: {cost}. Nothing committed.")
                print(block)
                print(target.look(path=None))
            # What the check said is the one thing a rehearsal keeps, and it is kept
            # on the painting: the copy's canvas, log, palette, landmarks and guides
            # are thrown away with it, so writing the file back changes nothing else.
            # After the printing, so a file that cannot be written costs the record
            # and not the rehearsal the painter is waiting for.
            session._keep_report(target, names, before, block)
            session.save(args.session)
        else:
            failed()
        return result.code

    if result.code == 0:
        session._keep_report(target, names, before, block)
    if result.save:
        session.save(args.session)
    if result.code == 0:
        print(result.report)
        print(block)
    else:
        failed()
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
