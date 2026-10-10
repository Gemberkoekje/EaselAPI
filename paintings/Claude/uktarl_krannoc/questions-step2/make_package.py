"""Build the package step 2's questions are put to the painter of Uktarl's Room in.

The painter answers from a zip: `README.md`, `QUESTIONS.md` and `KEY.md` beside this file,
a form (`answers-template.md`), the blind sheets the soft-hold bench lays under letters,
the rules' labelled sheets, the round's numbers and the bench. The pictures are not
committed; the probe makes them, and this lays them out, checking first that the letters
the probe wrote are the ones `KEY.md` records.

    python scripts/probe_uktarl_session.py --soft --rules
    python paintings/Claude/uktarl_krannoc/questions-step2/make_package.py

It writes `out/painter-questions-uktarl-step2/` and a zip beside it. `numbers/` is the
repository's as it stands when this runs.
"""

from __future__ import annotations

import re
import shutil
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BENCH = ROOT / "out" / "uktarl"
PACKAGE = ROOT / "out" / "painter-questions-uktarl-step2"

BLIND = ("soft_her_terminator.png", "soft_its_terminator.png",
         "soft_uktarl_s_far_cheek.png", "soft_her_far_side.png", "soft_her_wig.png",
         "soft_its_far_side.png", "soft_the_near_bandit.png", "soft_the_blanket_heap.png",
         "soft_whole_256.png", "soft_whole.png")
LABELLED = ("rules_disc.png", "rules_bars.png", "rules_graded.png")
#: What each letter is, as `KEY.md` names it and as the probe's `soft_key.txt` writes it.
LETTERS = {"A": "B3", "B": "as painted", "C": "B2", "D": "B1"}


def _check_letters() -> None:
    written = dict(re.findall(r"^([A-D]) = (.+)$",
                              (BENCH / "soft_key.txt").read_text(encoding="utf-8"),
                              flags=re.M))
    if written != LETTERS:
        raise SystemExit(f"the probe's letters {written} are not KEY.md's {LETTERS}")


def _calibration_section() -> str:
    text = (ROOT / "CALIBRATION.md").read_text(encoding="utf-8")
    start = text.index("## Uktarl's Room's round")
    end = text.find("\n## ", start + 1)
    return text[start:] if end < 0 else text[start:end]


def _plan_section() -> str:
    text = (ROOT / "PLAN-0.9.0.md").read_text(encoding="utf-8")
    start = text.index("## 6. Questions")
    return text[start:text.index("\n## 7.", start)]


def main() -> int:
    _check_letters()
    missing = [name for name in BLIND + LABELLED if not (BENCH / name).exists()]
    if missing:
        raise SystemExit(f"run the probe's --soft and --rules first; missing: {missing}")
    if PACKAGE.exists():
        shutil.rmtree(PACKAGE)
    for folder in ("blind", "labelled", "numbers", "scripts"):
        (PACKAGE / folder).mkdir(parents=True)
    for name in ("README.md", "QUESTIONS.md", "KEY.md"):
        shutil.copy2(HERE / name, PACKAGE / name)
    shutil.copy2(HERE / "answers-template.md", PACKAGE / "answers-step2.md")
    for name in BLIND:
        shutil.copy2(BENCH / name, PACKAGE / "blind" / name)
    for name in LABELLED:
        shutil.copy2(BENCH / name, PACKAGE / "labelled" / name)
    (PACKAGE / "numbers" / "CALIBRATION-uktarl.md").write_text(_calibration_section(),
                                                               encoding="utf-8")
    (PACKAGE / "numbers" / "PLAN-0.9.0-questions.md").write_text(_plan_section(),
                                                                 encoding="utf-8")
    shutil.copy2(ROOT / "NOTES-step2.md", PACKAGE / "numbers" / "NOTES-step2.md")
    for name in ("probe_uktarl_session.py", "probe_bell_session.py"):
        shutil.copy2(ROOT / "scripts" / name, PACKAGE / "scripts" / name)
    archive = PACKAGE.with_suffix(".zip")
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zipped:
        for path in sorted(PACKAGE.rglob("*")):
            if path.is_file():
                zipped.write(path, path.relative_to(PACKAGE.parent))
    print(f"wrote {PACKAGE} and {archive}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
