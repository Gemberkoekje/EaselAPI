"""Repaint a real painting, stroke for stroke, with whatever engine is installed.

M7 changes every mark, so the brief says to judge it on the sampler *and* on a real
painting. This replays the M6 headline run's own scripts -- `rehearsal3/pass/`, the
295-stroke mug -- against the current source tree, so the same 295 marks can be
looked at before and after the change.

    python m7/repaint.py out.png            # the copy
    python m7/repaint.py out.png --own      # the unprompted painting
    python m7/repaint.py --compare before.png after.png sheet.png

The reference photograph is not in the repo (it was a file on the painter's own
machine), so every `look`/`compare`/`preview`/`rehearse` call that wants one is
served without it. Nothing about the strokes depends on the reference: those calls
only draw pictures for the painter to read.
"""

from __future__ import annotations

import sys
from pathlib import Path

import easel
from easel.session import Session

REPO = Path(__file__).resolve().parents[1]
PASS = REPO / "rehearsal3" / "pass"

#: The session the `pass` run painted on. Its `.easel` state file was not kept, so
#: the size and ground come from its LOG.md (1200x900; `umber_wash`, chosen after
#: the first canvas was thrown away -- gap 2) and the texture and seed are the pair
#: that reproduce `copy_final.png` most closely of the eighteen tried, at an RMS of
#: 3.4 levels out of 255. Every combination was within 3.4-4.7, so this is the best
#: guess and not a certainty; what matters here is that the same 295 marks are
#: painted on the same surface by both engines.
CANVAS = dict(width=1200, height=900, texture="linen", ground="umber_wash", seed=11)

#: Its scripts, in the order they were run. `c9_probe2` and `probe_*` are probes,
#: not passes, and are left out -- they painted on a copy or on their own canvas.
COPY_SCRIPTS = ["c1_draw", "c2_fixdraw", "c3_draw", "c4_table", "c5_shadow", "c6_mug",
                "c7_mugfix", "c8_rehearse", "c9_cup", "c10_fix", "c11_repair",
                "c12_finish", "c13_last", "c14_head"]
OWN_SCRIPTS = ["o1_draw", "o2_sky", "o3_land", "o4_finish", "o5_last"]


def _without_reference(method):
    """Serve a look/compare/preview/rehearse that asks for a photograph we do not have."""
    def wrapper(self, *args, **kwargs):
        kwargs.pop("reference", None)
        args = tuple(a for a in args if not (isinstance(a, str) and a.endswith(".jpg")))
        try:
            return method(self, *args, **kwargs)
        except TypeError:
            return None
    wrapper.__wrapped__ = method
    return wrapper


def _serve_the_missing_reference() -> None:
    """Once per process: none of these calls paints anything, they only draw looks."""
    for name in ("look", "preview", "rehearse"):
        method = getattr(Session, name)
        if not hasattr(method, "__wrapped__"):
            setattr(Session, name, _without_reference(method))
    Session.compare = lambda self, *a, **k: None


def run(scripts: list[str], out: Path) -> Session:
    _serve_the_missing_reference()
    s = Session(**CANVAS, timelapse=False, out_dir=REPO / "out" / "m7_looks")
    namespace = {name: getattr(easel, name) for name in easel.__all__}
    namespace.update({"s": s, "session": s, "palette": s.palette,
                      "__name__": "__easel_script__"})
    for name in scripts:
        path = PASS / f"{name}.py"
        code = compile(path.read_text(encoding="utf-8"), str(path), "exec")
        namespace["__file__"] = str(path)
        exec(code, namespace)  # noqa: S102 - replaying the painter's own script is the point
        print(f"  {name:14s} {s.stroke_count:4d} strokes")
    s.export(out)
    print(f"Wrote {out} ({s.stroke_count} strokes)")
    return s


#: What to enlarge underneath the two paintings. The handle, the string and the tag
#: are the round-tip marks in this painting, so they are where pressure now changes
#: the width of what was painted; the rim and the crewmate are its bristle masses.
DETAILS = {"the handle, the string and the tag": (690, 150, 1130, 570),
           "the rim, the tea and the spoon": (330, 40, 770, 460)}
PANEL_H = 520
PAD, LABEL_H, BG, FG = 16, 22, (28, 28, 30), (232, 232, 236)


def compare(before: Path, after: Path, out: Path) -> Path:
    """The two paintings side by side, with the marks that changed enlarged below."""
    from PIL import Image, ImageDraw  # noqa: PLC0415 - only this mode needs it

    pair = [(Image.open(before).convert("RGB"), "BEFORE  (main, before M7)"),
            (Image.open(after).convert("RGB"), "AFTER  (main + M7)")]
    rows = [[(im.resize((round(im.width * PANEL_H / im.height), PANEL_H), Image.LANCZOS),
              f"{label} -- 295 strokes") for im, label in pair]]
    for title, box in DETAILS.items():
        crop_h = PANEL_H - 60
        rows.append([(im.crop(box).resize(
            (round((box[2] - box[0]) * crop_h / (box[3] - box[1])), crop_h), Image.LANCZOS),
            f"{label.split()[0].lower()}: {title}") for im, label in pair])

    width = max(sum(i.width for i, _ in row) + PAD * (len(row) + 1) for row in rows)
    height = sum(row[0][0].height + LABEL_H + PAD for row in rows) + PAD
    sheet = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(sheet)
    y = PAD
    for row in rows:
        x = PAD
        for img, label in row:
            draw.text((x, y), label, fill=FG)
            sheet.paste(img, (x, y + LABEL_H))
            x += img.width + PAD
        y += row[0][0].height + LABEL_H + PAD
    sheet.save(out)
    return out


def main(argv: list[str]) -> int:
    if argv and argv[0] == "--compare":
        print(f"Wrote {compare(Path(argv[1]), Path(argv[2]), Path(argv[3]))}")
        return 0
    out = Path(argv[0]) if argv else REPO / "m7" / "repaint.png"
    scripts = OWN_SCRIPTS if "--own" in argv else COPY_SCRIPTS
    out.parent.mkdir(parents=True, exist_ok=True)
    run(scripts, out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
