"""`easel demo` and the demo blocks in `RECIPES.md`: finding 19, and G3 of the 0.6.0 plan.

The whole-guide run -- every demo painted and held to what it names -- is
`scripts/check_guide_blocks.py`'s, and takes minutes. These are the parts that are
cheap enough to run on every commit: that every block parses and names things that
exist, that the rule in `easel.demo.faults` catches a failure block that has stopped
failing, and that the command and the sheet do what they say on the fastest demo.
"""

from __future__ import annotations

import pytest
from PIL import Image

from easel import demo
from easel.cli import main
from easel.notices import NOTICES

#: A draft of the recipes file, small enough to paint in a test: one recipe, and a
#: failure block whose *goes wrong* line is filled in per test.
DRAFT = """# Recipes

## A line across the middle

```python
s.stroke([(0.2, 0.5), (0.8, 0.5)], "flat", "mid", size=0.03)
```

**Goes wrong as:** a chain of beads.

```python
{demo}
```
"""

#: The fastest demo in the file, for the tests that have to paint one.
QUICK = "a-small-container-with-something-spilling-from-it"


def draft(block: str) -> str:
    return DRAFT.replace("{demo}", block)


# -- the blocks ------------------------------------------------------------------------
def test_every_demo_in_the_recipes_parses_and_names_what_exists():
    """A misspelt code is refused at parse time, so this is also the check that every
    code a *goes wrong* line names is one the engine can say."""
    every = demo.demos()
    assert len(every) >= 19
    for d in every:
        assert d.recipe, f"{d.heading} has a demo and no recipe block to lay beside it"
        assert d.failure.strip(), f"{d.heading}'s demo has nothing that goes wrong"
        assert set(d.codes) <= set(NOTICES)


def test_a_demo_is_one_per_recipe_and_under_its_own_heading():
    slugs = [d.slug for d in demo.demos()]
    assert len(slugs) == len(set(slugs))
    headings = {r.slug for r in demo.recipes()}
    assert set(slugs) <= headings


def test_what_goes_wrong_is_a_code_a_report_line_or_nothing():
    d, = demo.demos(draft('# goes wrong: jitter-beads; report() says "one disc"\n'
                          's.dab(0.5, 0.5)'))
    assert d.codes == ("jitter-beads",) and d.words == ("one disc",)
    nothing, = demo.demos(draft("# goes wrong: nothing says so\ns.dab(0.5, 0.5)"))
    assert nothing.silent


@pytest.mark.parametrize("block, complaint", [
    ("# goes wrong: jiter-beads\ns.dab(0.5, 0.5)", "neither a notice code"),
    ("s.dab(0.5, 0.5)\n# goes wrong: jitter-beads\ns.dab(0.5, 0.5)", "code before"),
    ("# the smallest fix: first\ns.dab(0.5, 0.5)\n# goes wrong: jitter-beads", "out of order"),
    ("# goes wrong: jitter-beads\ns.dab(0.5, 0.5)\n# goes wrong: jitter-beads", "two"),
])
def test_a_malformed_demo_is_refused_naming_its_recipe(block, complaint):
    with pytest.raises(ValueError, match=complaint) as caught:
        demo.demos(draft(block))
    assert "A line across the middle" in str(caught.value)


def test_a_demo_block_is_not_a_recipe_block():
    """What keeps the failure out of the recommended run, and the recipe out of the demo."""
    recipe, = demo.recipes(draft("# goes wrong: jitter-beads\ns.dab(0.5, 0.5)"))
    assert not demo.is_demo(recipe.recipe)
    assert recipe.recipe.startswith("s.stroke(")
    assert demo.is_demo(recipe.blocks[1])


# -- the rule ----------------------------------------------------------------------------
def test_a_failure_that_fails_the_way_it_says_has_no_faults(tmp_path):
    d, = demo.demos(draft(
        "# goes wrong: jitter-beads\n"
        's.stroke([(0.2, 0.5), (0.8, 0.5)], "flat", "mid", size=0.03, jitter=0.5)\n'
        "# the smallest fix: the default wander\n"
        's.stroke([(0.2, 0.5), (0.8, 0.5)], "flat", "mid", size=0.03, jitter=0.02)'))
    drawn = demo.panels(d, tmp_path)
    assert [p.label for p in drawn] == ["the recipe", "goes wrong", "the smallest fix"]
    assert drawn[1].codes == ["jitter-beads"]
    assert demo.faults(d, drawn) == []


def test_a_failure_block_that_stopped_failing_is_a_fault(tmp_path):
    """The half of the invariant that is new: a block kept under *Goes wrong as* after
    the engine stopped saying what it names is a picture of a fault the tool no longer
    makes, with a line claiming the tool catches it."""
    d, = demo.demos(draft('# goes wrong: jitter-beads\n'
                          's.stroke([(0.2, 0.5), (0.8, 0.5)], "flat", "mid", size=0.03)'))
    faults = demo.faults(d, demo.panels(d, tmp_path))
    assert any("names 'jitter-beads', and the calls said nothing" in f for f in faults)


def test_a_fix_that_still_says_what_went_wrong_is_a_fault(tmp_path):
    d, = demo.demos(draft(
        "# goes wrong: jitter-beads\n"
        's.stroke([(0.2, 0.5), (0.8, 0.5)], "flat", "mid", size=0.03, jitter=0.5)\n'
        "# the smallest fix: not one\n"
        's.stroke([(0.2, 0.5), (0.8, 0.5)], "flat", "mid", size=0.03, jitter=0.4)'))
    faults = demo.faults(d, demo.panels(d, tmp_path))
    assert faults == ["the smallest fix says jitter-beads at the call"]


def test_the_six_mistakes_are_recipes_with_demos():
    """`easel demo mistakes` is the entry path's own sheet, and it is six recipes'
    failures rather than six blocks of its own: a heading renamed or a demo taken out
    has to break here, where the message says which."""
    every = {r.slug: r for r in demo.recipes()}
    assert len(demo.MISTAKES) == 6
    for slug, looks in demo.MISTAKES:
        recipe = every.get(slug)
        assert recipe is not None, f"{slug} is not a recipe in RECIPES.md"
        assert recipe.demo is not None, f"{slug} has no demo for the mistakes sheet"
        assert looks and looks == looks.lower()


def test_the_mistakes_sheet_is_one_panel_each(tmp_path, monkeypatch):
    """Painted on one of them, because the sheet paints a passage per panel and the
    suite is not where six of those belong -- `easel demo mistakes` is."""
    monkeypatch.setattr(demo, "MISTAKES", ((QUICK, "a rim that reads as damage"),))
    written, drawn = demo.mistakes(tmp_path)
    assert written.name == "demo-mistakes.png"
    assert [looks for looks, _, _ in drawn] == ["a rim that reads as damage"]
    assert drawn[0][2].codes == ["round-fringe"]
    width, height = Image.open(written).size
    assert width < 2 * height                       # one panel, not a recipe's row of them


def test_a_burial_is_a_failure_a_demo_can_show(tmp_path):
    """A demo's body is opened as a pass, the way `easel run` opens one. The rule that
    names a burial needs the canvas as the pass began, and without it a repair that
    buries what stands on it was a failure no demo could name."""
    d, = demo.demos(draft(
        "# the passage: a mass, and three things standing on it\n"
        's.block_in(Region(0.1, 0.6, 0.9, 0.9), "flat", "dark", size=0.1, solid=True)\n'
        "for x in (0.3, 0.5, 0.7):\n"
        '    s.stroke([(x, 0.8), (x + 0.02, 0.65)], "round_hard", "light", size=0.012)\n'
        '# goes wrong: report() says "earlier details out of sight"\n'
        's.block_in(Region(0.1, 0.6, 0.9, 0.9), "flat", "dark", size=0.1, solid=True)'))
    drawn = demo.panels(d, tmp_path)
    assert demo.faults(d, drawn) == []


def test_a_block_that_raises_is_a_fault_and_not_a_crash(tmp_path):
    d, = demo.demos(draft("# goes wrong: nothing says so\ns.no_such_verb()"))
    drawn = demo.panels(d, tmp_path)
    assert drawn[1].error.startswith("AttributeError")
    assert any("raised AttributeError" in f for f in demo.faults(d, drawn))


# -- the sheet ---------------------------------------------------------------------------
def test_a_small_failure_is_enlarged_and_a_large_one_is_not():
    """Five dabs of a 5 px brush on a whole canvas are five dots nobody can compare."""
    small = [demo.Panel("the recipe", box=(200, 100, 210, 108)),
             demo.Panel("goes wrong", box=(190, 96, 230, 112))]
    x0, y0, x1, y1 = demo.focus(small, 400, 300)
    assert (x1 - x0) * 3 == (y1 - y0) * 4                # the canvas's own shape
    assert x1 - x0 >= 100                                 # enlarged at most four times
    assert x0 <= 190 and x1 >= 230 and y0 <= 96 and y1 >= 112
    large = [demo.Panel("goes wrong", box=(0, 0, 360, 280))]
    assert demo.focus(large, 400, 300) is None


# -- the command -------------------------------------------------------------------------
def test_the_command_with_no_words_lists_every_recipe(capsys):
    main(["demo"])
    out = capsys.readouterr().out
    for recipe in demo.recipes():
        assert recipe.slug in out
    assert "(no demo yet)" in out


def test_the_command_paints_a_demo_and_says_what_each_panel_was_told(tmp_path, capsys):
    assert main(["demo", "--out-dir", str(tmp_path), "container"]) == 0
    out = capsys.readouterr().out
    sheet = tmp_path / f"demo-{QUICK}.png"
    assert str(sheet) in out
    assert "the call says round-fringe" in out
    assert "round-fringe: " in out                        # the notice itself, quoted
    assert "`easel explain <code>`" in out
    # The recipe and what goes wrong, side by side: two panels of the canvas's shape.
    width, height = Image.open(sheet).size
    assert width > 2 * height


@pytest.mark.parametrize("words, said", [
    ("teapot", "No recipe's heading has all of"),
    ("passage", "names 2 recipes"),
    ("form that turns", "has no demo yet"),
])
def test_the_command_says_why_it_drew_nothing(words, said, capsys, tmp_path):
    main(["demo", "--out-dir", str(tmp_path), *words.split()])
    assert said in capsys.readouterr().out
    assert not list(tmp_path.glob("*.png"))


def test_a_recipe_is_found_by_its_anchor_as_well_as_its_words():
    assert [r.slug for r in demo.find(QUICK)] == [QUICK]
    assert [r.slug for r in demo.find("something spilling")] == [QUICK]
