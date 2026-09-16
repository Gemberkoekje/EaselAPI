"""``easel.__version__`` against the version pyproject.toml declares.

The version is written by hand in pyproject.toml and copied by hand into
``easel/__init__.py``, and the copy has already fallen behind once: 0.1.1 shipped
with ``__version__`` still reading 0.1.0. That is not cosmetic. ``build_server``
passes it to the MCP server as its advertised version, so for the whole of 0.1.1
every client that asked was told it was talking to 0.1.0 -- and nothing failed,
which is exactly why it went unnoticed.

The repository's habit is to write a version once and check every other copy
against it: the release workflow refuses a tag that disagrees with pyproject,
``scripts/pack_mcpb.py`` refuses to pack a bundle it cannot stamp, and
``test_server_json.py`` holds server.json to the same line. This is the copy that
had no such check.

Deriving ``__version__`` from ``importlib.metadata`` instead would remove the
second copy altogether, and is the obvious thing to reach for. It is not done
because the scripts in ``scripts/`` import easel straight off ``src/`` without
installing it, where there is no distribution metadata to read -- so it would
need a hardcoded fallback, which is the drifting copy again wearing a hat.
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

import pytest

import easel

ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]


def test_version_agrees_with_pyproject() -> None:
    """pyproject.toml decides; ``__init__.py`` follows."""
    assert easel.__version__ == PYPROJECT["version"]


def test_version_is_exported() -> None:
    """It is part of the public surface, and the MCP server reads it off the
    package rather than importing it by name."""
    assert "__version__" in easel.__all__


# -- a release claim against the tag that would make it true --------------------------
#
# `CHANGELOG.md` said *0.5.0 is released, so the next change to land here needs a
# version bump before it can ship* for a day, and 0.5.0 was not released: the newest
# tag was `v0.4.0` and the newest file on PyPI was 0.4.0. The line was written when
# that round was cut, in anticipation of a tag push that never happened, and the round
# filed after it was nearly cut as 0.6.0 over a version number that was still free --
# which would have left a hole in the changelog and on PyPI for a release nobody made.
#
# *Released* and *shipped* are claims about the world. The only thing that makes them
# true is a pushed tag: `publish.yml` runs on `v*` and on nothing else, so until the
# tag exists no wheel has been built and no file has been uploaded. So the rule is
# written in `CHANGELOG.md` where a person writing that line will read it, and this is
# the check that keeps it from being a preference.

#: How this file spots a section claiming its version is out in the world. Each has
#: been written in `CHANGELOG.md` at least once. It reads the words and cannot tell a
#: claim from a quotation of one, so a passage *about* this rule has to paraphrase --
#: which is a fair price for a check that needs nothing but the file and the tags.
RELEASED_CLAIM = re.compile(
    r"\*\*Released[.*]|Shipped as\s+`?v?(?P<v1>\d+\.\d+\.\d+)|"
    r"(?P<v2>\d+\.\d+\.\d+)\s+(?:is|was|has been)\s+released"
)

CHANGELOG = ROOT / "CHANGELOG.md"


def _tags() -> set[str]:
    """Every tag this checkout can see, or an empty set if it cannot see any.

    A shallow clone has no tags and cannot answer the question, so the test below
    skips rather than failing on it. CI asks for them explicitly (`fetch-tags` on the
    checkout step) so that the one place the answer matters is not the one place the
    check is silent.
    """
    import subprocess

    try:
        done = subprocess.run(["git", "tag", "--list"], cwd=ROOT, check=False,
                              capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):  # pragma: no cover - no git
        return set()
    return {line.strip() for line in done.stdout.splitlines() if line.strip()}


def _claimed_released() -> set[str]:
    """Every version `CHANGELOG.md` says is out, whichever way it says it.

    A section's own heading supplies the version for a bare ``**Released.**``; the
    other two spellings name it inline, wherever in the file they are written -- the
    line that started this was in the *Unreleased* section, about a version below it.
    """
    text = CHANGELOG.read_text(encoding="utf-8")
    claimed: set[str] = set()
    sections = re.split(r"^## \[([^\]]+)\]", text, flags=re.M)
    # [preamble, heading, body, heading, body, ...]
    for heading, body in zip(sections[1::2], sections[2::2], strict=True):
        for found in RELEASED_CLAIM.finditer(body):
            named = found.group("v1") or found.group("v2")
            if named:
                claimed.add(named)
            elif re.fullmatch(r"\d+\.\d+\.\d+", heading):
                claimed.add(heading)
    return claimed


def test_nothing_claims_to_have_shipped_without_a_tag() -> None:
    """The tag is what makes it true, so the tag is what the claim is checked against."""
    tags = _tags()
    if not tags:  # pragma: no cover - a shallow clone, which cannot answer
        pytest.skip("this checkout has no tags, so it cannot tell what shipped")
    missing = sorted(v for v in _claimed_released() if f"v{v}" not in tags)
    assert not missing, (
        f"CHANGELOG.md says {', '.join(missing)} shipped, and there is no tag for it. "
        f"Nothing is released until `git tag v<version> && git push origin v<version>`: "
        f"publish.yml runs on the tag and on nothing else. Write the entry without the "
        f"claim, tag it, then add the claim."
    )


def test_only_one_version_is_ever_being_prepared() -> None:
    """The other half of the same mistake, and the one that would have caught it.

    A version that was never tagged is a version still being prepared, and there can
    only be one of those -- the one ``pyproject.toml`` names. Two of them means a
    version was bumped past a release nobody made, which leaves a number that reads as
    used and is not, and a hole in this file that nothing will ever fill. That is what
    a 0.6.0 section over an untagged 0.5.0 was, for about an hour.
    """
    tags = _tags()
    if not tags:  # pragma: no cover - a shallow clone, which cannot answer
        pytest.skip("this checkout has no tags, so it cannot tell what shipped")
    versions = [h for h in re.findall(r"^## \[([^\]]+)\]", CHANGELOG.read_text(
        encoding="utf-8"), flags=re.M) if re.fullmatch(r"\d+\.\d+\.\d+", h)]
    assert versions, "CHANGELOG.md has no version sections"
    untagged = [v for v in versions if f"v{v}" not in tags]
    assert len(untagged) <= 1, (
        f"CHANGELOG.md has sections for {', '.join(untagged)} and none of them is "
        f"tagged. Only the version being prepared may be untagged; the rest were "
        f"skipped. Fold them together, or tag what was actually released."
    )
    if untagged:
        assert untagged[0] == PYPROJECT["version"], (
            f"CHANGELOG.md is preparing {untagged[0]} and pyproject.toml says "
            f"{PYPROJECT['version']}."
        )
