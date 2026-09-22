"""Execute every python block in the guide, the way a fresh reader would.

The guide is the deliverable, and a code block in it that does not run is worse
than no code block: the fresh session copies it, gets a traceback, and spends its
first ten minutes debugging the manual instead of painting.

**And a block that runs is not yet a block that is right.** Every recommended block
has to come back notice-clean, because a worked example is an instruction: finding 1
of the 0.5.0 cohort is a painter who laid `RECIPES.md`'s *a mass built of planes*
character for character and got the staircase the guide warns about. Two more were
found by running this check the first time -- the three answers under *Masses that are
not rectangles* demonstrated `edge="clean"` at a brush the very next paragraph
forbids, and the graded field drew its own top boundary inside the canvas, which cut
the passes reaching it into stubs shorter than the brush. Neither was visible to a
person reading the prose, because in both cases the prose was right.

**And a failure block has to fail the way it says.** `RECIPES.md`'s demo blocks --
the call that goes wrong, cut by comment lines from the passage it is laid on and the
smallest fix -- are not recommended blocks, and are held to the other half of the
invariant instead: each trips exactly the notice codes and `report()` lines its
*goes wrong* line names, and the recipe and the fix, laid on the same passage, trip
none of it. `easel.demo` owns the rule (`faults`); this is where it is run over every
demo at once. What `report()` says about a recipe that its failure does not name is
printed as a note rather than failed on: it is `LESSONS.md`'s rule 2 asked of the
post-pass check, and the answer is sometimes the rule's to change rather than the
recipe's.

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

from easel import demo  # noqa: E402  (after the sys.path insert)
from easel.docs import CARD_WORDS, FRONT_PAGE, FRONT_PAGE_WORDS, section  # noqa: E402

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


def guide_blocks(echo: bool = True) -> list[tuple[str, str]]:
    """Every recommended python block of the guide, in order, dedented so `exec` takes it.

    A function rather than a module-level loop because this script is not the only
    thing that wants the list: `scripts/probe_cohort_session.py` runs the same blocks
    past the checks it is measuring, which is `LESSONS.md`'s rule 2 -- *ask what the
    rule says to a painter doing the right thing* -- made runnable. Two copies of the
    block list would drift the first time a recipe was added.

    Demo blocks are left out: each is a failure on purpose, and counted with the
    recommended ones it would read to the probe as the guide tripping its own checks.
    """
    blocks: list[tuple[str, str]] = []
    for name in DOCUMENTS:
        found = re.findall(r"```python\n(.*?)```",
                           (ROOT / name).read_text(encoding="utf-8"), re.S)
        # A fenced block nested under a list item carries the list's indentation,
        # which is valid markdown and an IndentationError to `exec`.
        dedented = [textwrap.dedent(b) for b in found]
        kept = [b for b in dedented if not demo.is_demo(b)]
        blocks += [(name, b) for b in kept]
        if echo:
            demos = len(dedented) - len(kept)
            print(f"{len(kept):>3} python blocks in {name}"
                  + (f", and {demos} demo blocks" if demos else ""))
    if echo:
        print()
    return blocks


def is_pseudo_code(block: str) -> bool:
    """Signature listings and elided pseudo-code, which are not meant to run."""
    return bool(
        re.search(r"^\s*s\.\w+\(.*[=,]\s*(brush|color|points|region|reference|strokes)\b",
                  block, re.M)
        or re.search(r"\.\.\.", block)
    )


def runnable(block: str) -> str:
    """One block, with the placeholders a fresh reader would replace resolved."""
    src = block.replace('"ref.jpg"', repr(str(REFERENCE)))
    for name in ("painting.png", "painting.gif"):          # the guide's export block
        src = src.replace(f'"{name}"', repr(str(OUT / name)))
    return src


# What every block assumes is already open. It lives in `easel.demo` now, because
# `easel demo` has to lay the same context under a recipe that this script checks it
# under -- a demo that passed here and painted a different picture there would be two
# guides. The name stays, since `scripts/probe_cohort_session.py` reads it from here.
PREAMBLE = demo.preamble(OUT)


def check_demos() -> tuple[int, int]:
    """Hold every demo block to what it says. Returns (demos, how many are wrong)."""
    every = demo.demos()
    print(f"\n{len(every)} demo blocks, each laid as the recipe, what goes wrong, and "
          f"the fix:")
    wrong = 0
    for d in every:
        drawn = demo.panels(d, OUT)
        faults = demo.faults(d, drawn)
        wrong += bool(faults)
        verdict = "WRONG" if faults else "ok   "
        print(f"  {verdict} {d.slug:52s} {d.names}")
        for fault in faults:
            print(f"        {fault}")
        for note in demo.notes(d, drawn):
            print(f"        note -- {note}")
    return len(every), wrong


def main() -> int:
    blocks = guide_blocks()
    ok = bad = skipped = 0
    noisy: list[tuple[int, str, str, str]] = []
    for i, (doc, b) in enumerate(blocks, 1):
        head = b.strip().splitlines()[0][:60]
        where = f"{doc.removesuffix('.md').lower():<8}"
        if is_pseudo_code(b):
            skipped += 1
            print(f"  {i:>3} {where} SKIP (pseudo-code)  {head}")
            continue
        scope: dict = {}
        try:
            exec(compile(PREAMBLE + runnable(b), f"<block {i}>", "exec"), scope)
            ok += 1
            print(f"  {i:>3} {where} ok               {head}")
        except Exception as e:
            bad += 1
            print(f"  {i:>3} {where} FAIL             {head}\n       {type(e).__name__}: {e}")
            continue
        # What the engine said at the calls the block made. The session is `s` by
        # the preamble's own construction, and a block that rebinds it answers for
        # whatever it left there -- which is the session a reader would be holding.
        for notice in getattr(scope.get("s"), "notices", list)():
            noisy.append((i, doc, notice.code, str(notice)))
            print(f"  {i:>3} {where} SAYS             {notice.code}")
    print(f"\nok {ok}  failed {bad}  skipped {skipped}")

    if noisy:
        print(f"\n{len(noisy)} notice(s) tripped by a recommended block -- fix "
              f"the block, not the check:")
        for n, doc, code, text in noisy:
            print(f"  block {n} ({doc}) {code}\n       {text}")
    else:
        print("no recommended block trips a notice")

    demos, wrong = check_demos()
    print(f"{demos - wrong} of {demos} demo blocks fail exactly the way they say"
          + ("" if not wrong else " -- fix the block, or the line naming what it trips"))

    # The front page's word budget, the other thing that keeps the guide usable.
    text = (ROOT / "PAINTER.md").read_text(encoding="utf-8")
    words = len(text.split())
    card = len(section("guide", FRONT_PAGE, text).split())
    over = words > FRONT_PAGE_WORDS or card > CARD_WORDS
    for what, count, budget in (("PAINTER.md", words, FRONT_PAGE_WORDS),
                                ("its card", card, CARD_WORDS)):
        verdict = "over budget" if count > budget else f"{budget - count} to spare"
        print(f"{what} {count} words against a budget of {budget} -- {verdict}")
    return 1 if bad or noisy or wrong or over else 0


if __name__ == "__main__":
    sys.exit(main())
