"""Build the package step 2's questions were put to the Bell-Warden's painter in.

The painter answers from a zip: `README.md`, `QUESTIONS.md` and `KEY.md` beside this file,
a form (`answers-template.md`), and pictures -- its arrangements drawn flat at four sizes,
the guide candidates over its own canvas, its subject's pass laid seven ways, and its
painting with the darks re-laid under the box's floor, each under letters in a fixed
shuffled order -- and every labelled sheet. The pictures are not committed; the probe's
benches make them, and this lays them out under their letters, checking that the
shuffles still give the letters `KEY.md` records.

    python scripts/probe_bell_session.py --thumbnail --guides --terminator --floor
    python paintings/Claude/bell_warden/questions-step2/make_package.py

The probe takes about half an hour for those four; this, a few seconds. It writes
`out/painter-questions-bell-step2/` and a zip beside it. `numbers/` is the repository's
as it stands when this runs.
"""

from __future__ import annotations

import random
import re
import shutil
import sys
import zipfile
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

import probe_bell_session as probe  # noqa: E402

from easel.look import label_sheet  # noqa: E402

PKG = ROOT / "out" / "painter-questions-bell-step2"
ZIP = ROOT / "out" / "painter-questions-bell-step2.zip"
OUT = probe.OUT

SIZES = [str(s) for s in probe.THUMB_SIZES]
GUIDES = list(probe.GUIDE_KINDS)
TERMINATORS = [name for name, _ in probe.TERMINATOR_KINDS]
DARKS = ["as painted", "to 0.07"]

#: What the painter was shown, as `KEY.md` records it. The builder refuses to write a
#: package whose letters say something else.
SIZE_KEY = {"W": "96", "X": "192", "Y": "256", "Z": "128"}
GUIDE_KEY = {"E": "casing 150", "F": "today", "G": "ink", "H": "casing"}
TERMINATOR_KEY = {"A": "feather 0.012", "B": "soft copies", "C": "as painted", "D": "smudge",
                  "E": "feather 0.03", "F": "join", "G": "copies ragged"}
DARK_KEY = {"P": "to 0.07", "Q": "as painted"}


def shuffled(items: list[str], seed: int) -> list[str]:
    out = list(items)
    random.Random(seed).shuffle(out)
    return out


def lettered(items: list[str], letters: str, seed: int) -> dict[str, str]:
    return dict(zip(letters, shuffled(items, seed), strict=True))


def check(made: dict[str, str], key: dict[str, str], what: str) -> None:
    if made != key:
        raise SystemExit(f"the {what} letters no longer match KEY.md: {made} against {key}")


def blind_sheets() -> None:
    blind = PKG / "blind"
    blind.mkdir(parents=True, exist_ok=True)
    sizes = lettered(SIZES, "WXYZ", 8)
    check(sizes, SIZE_KEY, "thumbnail size")
    for name in ("cat", "piebald", "arch", "final"):
        panels = [(letter, Image.open(OUT / "thumbnails" / f"{name}_{size}.png").convert("RGB"))
                  for letter, size in sorted(sizes.items())]
        label_sheet(panels, columns=4).save(blind / f"q4_{name}.png")
    guides = lettered(GUIDES, "EFGH", 4)
    check(guides, GUIDE_KEY, "guide")
    for ground in ("bell_after_room", "mid_grey"):
        panels = [(letter, Image.open(OUT / "guides" / f"{probe._slug(kind)}_{ground}.png"))
                  for letter, kind in sorted(guides.items())]
        label_sheet(panels, columns=4).save(blind / f"q4_guides_{ground}.png")
    terms = lettered(TERMINATORS, "ABCDEFG", 9)
    check(terms, TERMINATOR_KEY, "terminator")
    for size in ("1024x768", "1440x960"):
        for key in ("whole", "chest"):
            panels = [(letter, Image.open(OUT / "terminator"
                                          / f"{probe._slug(kind)}_{size}_{key}.png"))
                      for letter, kind in sorted(terms.items())]
            label_sheet(panels, columns=4).save(blind / f"q9_{key}_{size}.png")
    darks = lettered(DARKS, "PQ", 10)
    check(darks, DARK_KEY, "dark")
    for letter, kind in sorted(darks.items()):
        shutil.copy2(OUT / "floor" / f"bell_{probe._slug(kind)}.png", blind / f"q10_{letter}.png")


def labelled_sheets() -> None:
    labelled = PKG / "labelled"
    labelled.mkdir(parents=True, exist_ok=True)
    for pattern in ("thumbnail_*.png", "guides_*.png", "terminator_*.png", "form_*.png",
                    "face_structures.png", "floor_bell.png", "rings_*.png"):
        for path in sorted(OUT.glob(pattern)):
            shutil.copy2(path, labelled / path.name)
    for name in ("plan_128.png", "final_256_guides.png"):
        shutil.copy2(OUT / "thumbnails" / name, labelled / f"thumbnail_{name}")


def numbers() -> None:
    folder = PKG / "numbers"
    folder.mkdir(parents=True, exist_ok=True)
    calibration = (ROOT / "CALIBRATION.md").read_text(encoding="utf-8")
    start = calibration.index("## The bell-warden's round")
    (folder / "CALIBRATION-the-bell-wardens-round.md").write_text(
        calibration[start:], encoding="utf-8")
    for name in ("NOTES-step2.md",):
        if (ROOT / name).exists():
            shutil.copy2(ROOT / name, folder / name)
    plan = ROOT / "PLAN-0.8.0.md"
    if plan.exists():
        text = plan.read_text(encoding="utf-8")
        found = re.search(r"^## 6\. Questions.*?(?=^## 7\.)", text, flags=re.S | re.M)
        if found:
            (folder / "PLAN-0.8.0-section-6.md").write_text(found.group(0), encoding="utf-8")
    scripts = PKG / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "scripts" / "probe_bell_session.py", scripts / "probe_bell_session.py")


def main() -> int:
    if PKG.exists():
        shutil.rmtree(PKG)
    PKG.mkdir(parents=True)
    for name in ("README.md", "QUESTIONS.md", "KEY.md"):
        shutil.copy2(HERE / name, PKG / name)
    shutil.copy2(HERE / "answers-template.md", PKG / "answers-step2.md")
    blind_sheets()
    labelled_sheets()
    numbers()
    if ZIP.exists():
        ZIP.unlink()
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(PKG.rglob("*")):
            if path.is_file():
                z.write(path, path.relative_to(PKG.parent))
    print(f"wrote {PKG} and {ZIP}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
