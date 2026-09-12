"""Execute every python block in the guide, the way a fresh reader would.

The guide is the deliverable, and a code block in it that does not run is worse
than no code block: the fresh session copies it, gets a traceback, and spends its
first ten minutes debugging the manual instead of painting.

The guide is three files -- `PAINTER.md` is the method, `PAINTING.md` the reasons
and `RECIPES.md` the procedures -- and all three are checked here, because a block
is just as wrong in whichever of them it happens to sit.

It also reports `PAINTER.md`'s word count against its budget. That file is the one
a session is asked to hold in its head, and the guide grew from 8,600 words to
17,000 under a no-growth rule that nothing enforced. The budget is asserted in
`tests/test_guide.py`, which is what CI actually runs; it is printed here too
because this is the script somebody runs while editing the guide.

Self-contained. It writes its own reference photograph, so it runs anywhere rather
than only on the machine of whoever wrote the guide.

    python scripts/check_guide_blocks.py
"""
from __future__ import annotations

import re
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from easel.guide import FRONT_PAGE_WORDS  # noqa: E402  (after the sys.path insert)

OUT = ROOT / "out" / "_check"
OUT.mkdir(parents=True, exist_ok=True)


def make_reference(path: Path) -> Path:
    """A stand-in photograph: a few masses, real edges, a real value range."""
    w, h = 480, 360
    img = Image.new("RGB", (w, h), (176, 168, 152))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, int(h * 0.52)], fill=(120, 126, 134))
    d.rectangle([0, int(h * 0.52), w, h], fill=(158, 128, 96))
    d.ellipse([int(w * 0.33), int(h * 0.30), int(w * 0.63), int(h * 0.72)],
              fill=(226, 222, 214))
    d.ellipse([int(w * 0.33), int(h * 0.27), int(w * 0.63), int(h * 0.35)],
              fill=(198, 194, 188))
    d.ellipse([int(w * 0.60), int(h * 0.40), int(w * 0.74), int(h * 0.58)],
              fill=(226, 222, 214))
    d.ellipse([int(w * 0.31), int(h * 0.66), int(w * 0.70), int(h * 0.76)],
              fill=(112, 92, 70))
    img.save(path)
    return path


REFERENCE = make_reference(OUT / "ref.png")

DOCUMENTS = ("PAINTER.md", "PAINTING.md", "RECIPES.md")

blocks: list[tuple[str, str]] = []
for name in DOCUMENTS:
    found = re.findall(r"```python\n(.*?)```", (ROOT / name).read_text(encoding="utf-8"), re.S)
    # A fenced block nested under a list item carries the list's indentation, which
    # is valid markdown and an IndentationError to `exec`.
    blocks += [(name, textwrap.dedent(b)) for b in found]
    print(f"{len(found):>3} python blocks in {name}")
print()

PREAMBLE = (
    "from easel import Session, Region, region, cell, span, horizon, below, above\n"
    "from easel import blob, ellipse, hull, ribbon, polygon, union\n"
    f"s = Session(400, 300, ground='toned_grey', seed=1, timelapse=True, "
    f"out_dir={str(OUT)!r})\n"
    "p = s.palette\n"
    "s.palette['dark'] = s.palette.mix('ultramarine','burnt_umber',0.45)\n"
    "s.palette['corrected_colour'] = s.palette['dark']\n"
    "s.palette['light'] = s.palette.tint('yellow_ochre', 0.5)\n"
    "s.palette['shadow'] = s.palette['dark']\n"
    "s.palette['mid'] = s.palette['light']\n"
    "s.palette['pale'] = s.palette['light']\n"
    "s.palette['cool'] = s.palette['dark']\n"
    # The lit surface a cast shadow lies on, named the way the guide names it.
    "s.palette['surface'] = s.palette.at_value(s.palette['light'], 0.60)\n"
    "path = [(0.2,0.3),(0.5,0.4),(0.8,0.3)]\n"
    # The guide's landmark blocks assume marks already exist by the time a later
    # block uses s.pt(...), which is true when the guide is read in order.
    "s.mark('top_l', 0.335, 0.315)\n"
    "s.mark('top_r', 0.630, 0.315)\n"
    "s.mark('base', 0.480, 0.715)\n"
    "s.pencil([(0.30, 0.40), (0.50, 0.55)])\n"
    # ...and the same for the plan that preview, rehearse and the paint block share.
    "plan = [{'points': [(0.335, 0.315), (0.40, 0.62)], 'brush': 'liner',\n"
    "         'size': 0.006, 'color': 'light', 'label': 'edge'}]\n"
    # ...and for the masses the guide points at by name once it has built one: a
    # shape to smudge round, a patch to light from the middle, and the bent ribbon
    # the costing blocks weigh against its straight twin.
    "mass = blob(span('D4', 'F6'), 0.22, wobble=0.3, seed=2)\n"
    "patch = ellipse(span('D4', 'F5'))\n"
    "bent = ribbon([(0.20, 0.30), (0.45, 0.62), (0.78, 0.34)], 0.029)\n"
)
ok = bad = skipped = 0
for i, (doc, b) in enumerate(blocks, 1):
    head = b.strip().splitlines()[0][:60]
    where = f"{doc.removesuffix('.md').lower():<8}"
    if re.search(r"^\s*s\.\w+\(.*[=,]\s*(brush|color|points|region|reference|strokes)\b", b, re.M) \
       or re.search(r"\.\.\.", b):
        # signature listings and elided pseudo-code
        skipped += 1
        print(f"  {i:>3} {where} SKIP (pseudo-code)  {head}")
        continue
    src = b.replace('"ref.jpg"', repr(str(REFERENCE)))
    for name in ("painting.png", "painting.gif"):          # the guide's export block
        src = src.replace(f'"{name}"', repr(str(OUT / name)))
    try:
        exec(compile(PREAMBLE + src, f"<block {i}>", "exec"), {})
        ok += 1
        print(f"  {i:>3} {where} ok               {head}")
    except Exception as e:
        bad += 1
        print(f"  {i:>3} {where} FAIL             {head}\n       {type(e).__name__}: {e}")
print(f"\nok {ok}  failed {bad}  skipped {skipped}")

# The front page's word budget, the other thing that keeps the guide usable.
words = len((ROOT / "PAINTER.md").read_text(encoding="utf-8").split())
budget = FRONT_PAGE_WORDS
verdict = "over budget" if words > budget else f"{budget - words} to spare"
print(f"PAINTER.md {words} words against a budget of {budget} -- {verdict}")
sys.exit(1 if bad or words > budget else 0)
