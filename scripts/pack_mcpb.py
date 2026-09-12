"""Build ``dist/easel.mcpb``, the one-click desktop bundle, out of ``mcpb/``.

    python scripts/pack_mcpb.py

The bundle is a zip of four small files, and it does not contain the engine. The
manifest declares ``server.type = "uv"``, so the installing host resolves
``easel-paint[mcp]`` from PyPI and builds the environment itself. That is not a
convenience, it is the only route available: easel depends on numpy and pillow,
the mcp extra pulls in pydantic, and the MCPB spec says in as many words that
compiled dependencies cannot be vendored portably. Bundling them would mean one
file per platform per CPython ABI. This way one file covers darwin, linux and
win32, and the engine a painter installs is the same one PyPI serves everybody.

The consequence to keep in mind is that the bundle pins an exact version, so it is
only *installable* once that version is on PyPI. It packs fine before then --
which is why the release workflow builds it early, to find a broken manifest
during a rehearsal, and publishes it only after the PyPI upload has succeeded.

No version is written by hand here. pyproject.toml is the source of truth, as it
is for the tag, and this copies it into both the manifest and the dependency pin.
The 0.0.0 placeholders in ``mcpb/`` exist to be overwritten: if a substitution
finds nothing to substitute, something has been renamed without telling this
script, and it stops rather than shipping a bundle pinned to 0.0.0.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "mcpb"
PLACEHOLDER = "0.0.0"

# Pinned rather than `latest`, for the reason publish.yml pins its actions by
# digest: this runs in the release path, and a surprise major version there is a
# surprise in the one build that cannot be taken back.
MCPB_CLI = "@anthropic-ai/mcpb@2.1.2"

# Every file the substitution has to touch. Named rather than globbed so that a
# new file carrying a version is a deliberate edit here.
VERSIONED = ("manifest.json", "pyproject.toml")


def project_version() -> str:
    """The version in the root ``pyproject.toml`` -- the same line the tag is checked against."""
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    return pyproject["project"]["version"]


def substitute(path: Path, version: str) -> None:
    """Write *version* over every ``0.0.0`` in *path*, refusing if there are none."""
    text = path.read_text(encoding="utf-8")
    if PLACEHOLDER not in text:
        raise SystemExit(
            f"{path.name} has no {PLACEHOLDER} left to fill in. Either a version is "
            "being written by hand now, which is the thing this script exists to "
            "prevent, or the file changed and VERSIONED did not."
        )
    path.write_text(text.replace(PLACEHOLDER, version), encoding="utf-8")


def run_cli(*args: str) -> None:
    """Run the mcpb CLI through npx, which is where it lives -- it is a node package."""
    npx = shutil.which("npx")
    if npx is None:
        raise SystemExit("npx is not on PATH, and the mcpb CLI is a node package.")
    subprocess.run([npx, "--yes", MCPB_CLI, *args], check=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pack_mcpb.py",
        description="Build the MCPB desktop bundle from mcpb/.",
    )
    parser.add_argument("--out-dir", type=Path, default=ROOT / "dist",
                        help="where to write easel.mcpb (default: dist/)")
    args = parser.parse_args(argv)

    version = project_version()
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # Substitution happens on a copy. The checked-in mcpb/ keeps its placeholders,
    # so a second pack from a dirty tree cannot pin the version twice or pin the
    # wrong one, and `git status` after a release is still clean.
    staged = out_dir / "mcpb-staged"
    if staged.exists():
        shutil.rmtree(staged)
    # Ignore what a local `uv run` leaves behind in mcpb/. .mcpbignore already keeps
    # it out of the bundle; this keeps it out of the copy, so packing after a local
    # test does not drag a virtualenv through dist/.
    shutil.copytree(SOURCE, staged,
                    ignore=shutil.ignore_patterns(".venv", "__pycache__", "uv.lock"))
    for name in VERSIONED:
        substitute(staged / name, version)

    run_cli("validate", str(staged / "manifest.json"))

    bundle = out_dir / "easel.mcpb"
    bundle.unlink(missing_ok=True)
    run_cli("pack", str(staged), str(bundle))

    # Read back rather than trust: the point of the whole exercise is that the
    # version in the shipped manifest is the released one.
    packed = json.loads((staged / "manifest.json").read_text(encoding="utf-8"))
    if packed["version"] != version:
        raise SystemExit(f"packed manifest says {packed['version']}, pyproject says {version}.")

    size = bundle.stat().st_size
    print(f"{bundle} -- easel {version}, {size:,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
