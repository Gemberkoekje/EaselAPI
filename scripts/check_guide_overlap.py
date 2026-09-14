"""Report any sentence stated in more than one of the guide's five files.

The documentation is arranged so that every rule is stated once, in the file it
belongs to, and linked from the others. Before the tenth round the same six rules
were each stated in four to six places, because five files split by kind of content
each restated their neighbours to stand alone; a rule nothing enforces is a
preference, so this script is the enforcement. It prints every run of words that
appears in two files and exits non-zero if there are any.

Code blocks are excluded, because a call is meant to appear wherever it is used, and
so are table rows, because a fact in `REFERENCE.md` and the same fact in a
`CALIBRATION.md` table are the same fact on purpose. What is left is prose, and prose
that matches for `WINDOW` words running is a copy.

    python scripts/check_guide_overlap.py
    python scripts/check_guide_overlap.py --window 10       # stricter
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = ("PAINTER.md", "PAINTING.md", "RECIPES.md", "REFERENCE.md")
#: The measurements file heads each measurement with the claim it measures, in the
#: guide's own words, and that is not a copy -- a number without its claim is a table
#: of figures. So it is checked only on request.
CALIBRATION = "CALIBRATION.md"
WINDOW = 12


def prose_words(text: str) -> list[str]:
    """The document as a list of words, with code, tables and markup taken out."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    lines = [ln for ln in text.splitlines() if not ln.lstrip().startswith("|")]
    text = re.sub(r"[`*_\[\]()#>|]", " ", "\n".join(lines))
    return [w.casefold() for w in re.findall(r"[A-Za-z0-9][A-Za-z0-9'.,%/=-]*", text)]


def runs(words: list[str], window: int) -> dict[str, int]:
    """Every `window`-word run in the document, keyed to where it starts."""
    return {" ".join(words[i:i + window]): i for i in range(len(words) - window + 1)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--window", type=int, default=WINDOW,
                        help=f"words that have to run together to count as a copy (default {WINDOW})")
    parser.add_argument("--include-calibration", action="store_true",
                        help="also check CALIBRATION.md, whose claim lines restate the guide on purpose")
    args = parser.parse_args(argv)

    documents = DOCUMENTS + ((CALIBRATION,) if args.include_calibration else ())
    where: dict[str, dict[str, int]] = defaultdict(dict)
    words = {name: prose_words((ROOT / name).read_text(encoding="utf-8")) for name in documents}
    for name, ws in words.items():
        for run, start in runs(ws, args.window).items():
            where[run][name] = start

    shared = {run: docs for run, docs in where.items() if len(docs) > 1}
    # Collapse overlapping windows into one report per passage: keep a run only if the
    # run one word earlier is not also shared between the same documents.
    passages = []
    for run, docs in shared.items():
        name = next(iter(docs))
        start = docs[name]
        earlier = " ".join(words[name][start - 1:start - 1 + args.window]) if start else None
        if earlier in shared and set(shared[earlier]) == set(docs):
            continue
        passages.append((sorted(docs), run))
    passages.sort()

    for docs, run in passages:
        print(f"{' + '.join(docs)}:\n    {run} ...")
    print(f"\n{len(passages)} passage(s) stated in more than one file "
          f"(window {args.window} words)")
    return 1 if passages else 0


if __name__ == "__main__":
    sys.exit(main())
