"""Build the package step 2's five questions were put to the painter in, again.

The painter answered from a zip: `README.md`, `QUESTIONS.md` and `KEY.md` beside this
file, a form (`answers-template.md`), and pictures -- the edge and dry-brush candidates
laid out again under letters in a fixed shuffled order, the corpus's graded crops under
numbers, and every labelled sheet. The pictures are not committed; this rebuilds them
from the benches that made them, and checks that the shuffles still give the letters the
painter's answers use.

    python scripts/probe_cohort_session.py --graded     # first: the crops, about 25 min
    python paintings/Claude/lighthouse_handover/questions-step2/make_package.py

About ten minutes; it writes `out/painter-questions-step2/` and a zip beside it. The
painter's one measurement, `../verify/measure_ground_edges.py`, runs from the package's
root against `blind/q10_ground.png`. `numbers/` is the repository's as it stands when
this runs, so it is not what the painter read if the round has moved on since -- and
`PLAN-0.7.0.md` and `NOTES-step2.md` left the repository with 0.7.0's claim, so after it
`numbers/` carries neither.

**To rebuild the package as the painter read it, check out `427901a`** (#76, the step
that made it). The crops are laid by the engine installed, and from step 5 on that engine
breaks a held edge and drags a dry brush, so a later `crop_01` is not the crop that was
read. `out/graded/` is gitignored and rewritten by every `--graded` run: copy a crop out
before re-running the probe if it is evidence for a reading.
"""

from __future__ import annotations

import random
import shutil
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

import probe_handover_session as probe  # noqa: E402

from easel.look import label_sheet  # noqa: E402

PKG = ROOT / "out" / "painter-questions-step2"
ZIP = ROOT / "out" / "painter-questions-step2.zip"

EDGE = ["today", "A1 0.002", "A2 0.002", "A2 0.003"]
GATE = ["today", "B1", "B2", "B1+B2", "B3"]

#: What the painter was shown, as `KEY.md` records it. The builder refuses to write a
#: package whose letters say something else.
EDGE_KEY = {"A": "A2 0.003", "B": "A2 0.002", "C": "A1 0.002", "D": "today"}
GATE_KEY = {"P": "today", "Q": "B1", "R": "B3", "S": "B2", "T": "B1+B2"}
CROP_KEY = {
    "crop_01.png": "hands_pass08_pickmass.py.png",
    "crop_02.png": "car_wash_p13_form.py.png",
    "crop_03.png": "pier_pass2_masses.py.png",
    "crop_04.png": "pier_pass4_water.py.png",
    "crop_05.png": "opus_p3_beam.py.png",
    "crop_06.png": "fable_p8_base.py.png",
    "crop_07.png": "heron2_pass11_last.py.png",
    "crop_08.png": "gpt_25-boat-near-hull.png",
    "crop_09.png": "sonnet_p3_beam.py.png",
    "crop_10.png": "hands_pass22_bowl3.py.png",
}


def shuffled(items: list[str], seed: int) -> list[str]:
    out = list(items)
    random.Random(seed).shuffle(out)
    return out


def capture_benches() -> dict[str, list]:
    """Run the benches the blind sheets are cut from, keeping every panel by name."""
    captured: dict[str, list] = {}
    save = probe.save_sheet

    def keep(panels, name, columns=None):
        captured[name] = list(panels)
        return save(panels, name, columns)

    probe.save_sheet = keep
    try:
        rb = probe.rebuild()
        rb1440 = probe.rebuild(1440, 960, upto="p03_headland.py")
        probe.bench_edge_sheets(rb, rb1440)
        probe.bench_crosser()
        probe.bench_exercise_three()
        probe.bench_water(rb)
    finally:
        probe.save_sheet = save
    return captured


def blind(panels: list, mapping: dict[str, str], name: str, columns: int,
          rows: list[tuple[str, str]] | None = None) -> None:
    """One blind sheet: the captured panels laid out again under their letters."""
    by_label = dict(panels)
    laid = [(f"{letter}{caption}", by_label[f"{prefix}{candidate}"])
            for prefix, caption in rows or [("", "")]
            for letter, candidate in mapping.items()]
    target = PKG / "blind" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    label_sheet(laid, columns=columns).save(target)


def main() -> None:
    crops_dir = ROOT / "out" / "graded"
    crops = sorted(crops_dir.glob("*.png"))
    if not crops:
        raise SystemExit("no crops under out/graded/: run "
                         "`python scripts/probe_cohort_session.py --graded` first")
    edges = dict(zip("ABCD", shuffled(EDGE, 10), strict=True))
    gates = dict(zip("PQRST", shuffled(GATE, 12), strict=True))
    order = shuffled([c.name for c in crops], 13)
    crop_map = {f"crop_{i:02d}.png": name for i, name in enumerate(order, start=1)}
    if (edges, gates, crop_map) != (EDGE_KEY, GATE_KEY, CROP_KEY):
        raise SystemExit("the shuffles no longer give the letters in KEY.md -- the "
                         "painter's answers would not read against this package")

    if PKG.exists():
        shutil.rmtree(PKG)
    PKG.mkdir(parents=True)
    captured = capture_benches()

    blind(captured["edges_tower_1024x768.png"], edges, "q10_tower_1x.png", 4)
    blind(captured["edges_tower_1024x768_x3.png"], edges, "q10_tower_x3.png", 4)
    blind(captured["edges_tower_1440x960.png"], edges, "q10_tower_1440.png", 4)
    blind(captured["edges_headland.png"], edges, "q10_headland.png", 4,
          rows=[("roughened, ", ", your roughened outline"),
                ("plain, ", ", the plain outline")])
    blind(captured["edges_ground.png"], edges, "q10_ground.png", 4)
    blind(captured["edges_burial.png"], edges, "q10_burial.png", 4)
    by_label = dict(captured["flecks_crosser.png"])     # "<gate> load <load>"
    label_sheet([(f"{letter}, load {load}", by_label[f"{gate} load {load}"])
                 for letter, gate in gates.items() for load in ("0.3", "0.45", "0.6")],
                columns=3).save(PKG / "blind" / "q12_crosser.png")
    blind(captured["flecks_exercise3.png"], gates, "q12_exercise3.png", 1)
    blind(captured["flecks_water.png"], gates, "q12_water.png", 2)
    (PKG / "blind" / "q13").mkdir(parents=True, exist_ok=True)
    for target, source in crop_map.items():
        shutil.copy2(crops_dir / source, PKG / "blind" / "q13" / target)

    labelled = PKG / "labelled"
    (labelled / "graded").mkdir(parents=True)
    for sheet in sorted((ROOT / "out" / "handover").glob("*.png")):
        shutil.copy2(sheet, labelled / sheet.name)
    for crop in crops:
        shutil.copy2(crop, labelled / "graded" / crop.name)

    numbers = PKG / "numbers"
    numbers.mkdir()
    calibration = (ROOT / "CALIBRATION.md").read_text(encoding="utf-8")
    (numbers / "CALIBRATION-the-lighthouse-handovers-round.md").write_text(
        calibration[calibration.index("## The lighthouse handover's round"):],
        encoding="utf-8", newline="\n")
    plan = ROOT / "PLAN-0.7.0.md"
    if plan.exists():
        text = plan.read_text(encoding="utf-8")
        section = text[text.index("## 5. Decisions taken"):text.index("## 6. Order of work")]
        section = section.rstrip().removesuffix("---").rstrip()
        (numbers / "PLAN-0.7.0-section-5.md").write_text(section + "\n", encoding="utf-8",
                                                         newline="\n")
    notes = ROOT / "NOTES-step2.md"
    if notes.exists():
        shutil.copy2(notes, numbers / "NOTES-step2.md")

    scripts = PKG / "scripts"
    scripts.mkdir()
    for name in ("probe_handover_session.py", "probe_cohort_session.py"):
        shutil.copy2(ROOT / "scripts" / name, scripts / name)
    shutil.copy2(Path(__file__), scripts / "make_package.py")
    for name in ("README.md", "QUESTIONS.md", "KEY.md"):
        shutil.copy2(HERE / name, PKG / name)
    shutil.copy2(HERE / "answers-template.md", PKG / "answers-step2.md")

    if ZIP.exists():
        ZIP.unlink()
    with zipfile.ZipFile(ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(PKG.rglob("*")):
            if path.is_file():
                zf.write(path, Path(PKG.name) / path.relative_to(PKG))
    print(f"wrote {ZIP} ({ZIP.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
