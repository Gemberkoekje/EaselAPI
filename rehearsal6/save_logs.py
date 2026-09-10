"""Write each painter's session log out as JSON, so the checks survive the run.

A `.easel` file is a canvas plus its history, and the canvas makes it about 15 MB --
too big to commit, and `*.easel` is ignored repository-wide for that reason. But
three of the checks in `verify_done.py` read the *history* and not the canvas: the
stroke count, the last ten charged marks, and the signature. In REHEARSAL4 those
numbers went into the write-up and could not afterwards be re-derived from anything
in the repository.

The history is a few hundred kilobytes of JSON. Writing it out beside the paintings
costs almost nothing and makes those three checks reproducible from a clone, which is
the same argument the exports and time-lapses are committed under.

Run from the repo root, after a run:  python rehearsal6/save_logs.py
"""
from __future__ import annotations

import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SESSIONS = f"{HERE}/sessions"


def save(run: str, name: str) -> str | None:
    src = f"{HERE}/{run}/{name}.easel"
    if not os.path.exists(src):
        return None
    with np.load(src, allow_pickle=False) as z:
        payload = {"meta": json.loads(str(z["meta"])), "log": json.loads(str(z["log"]))}
    os.makedirs(SESSIONS, exist_ok=True)
    dst = f"{SESSIONS}/{run}-{name}.json"
    with open(dst, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=1)
    return dst


if __name__ == "__main__":
    for run in ("pass", "sitter"):
        for name in ("copy", "own1", "own2"):
            dst = save(run, name)
            if dst is None:
                continue
            print(f"  {os.path.relpath(dst, HERE):<28} "
                  f"{os.path.getsize(dst) / 1024:8.0f} KB")
