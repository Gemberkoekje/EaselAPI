"""The palette: a small set of pigments the painter mixes on, plus named slots.

Deliberately small and deliberately without black. A limited palette forces mixed
neutrals, which is most of what makes a painting look painted. Darks are made from
umber plus a blue, not from a tube of black.

Pigment hex values are chosen so that no channel is zero -- see the note on the
reflectance floor in :mod:`easel.color`. Until M8b the darks were held to a stronger
rule, that no channel sat below that floor either, because a channel under ``0.01``
rendered *as* ``0.01`` and a darker swatch would have stated a colour no stroke could
lay. The floor is off the answer now, so that rule is gone and
``cadmium_yellow``, whose blue has always been under it, lays its own ``#FFC012``.
What the darks are held to instead is being masstones rather than colour-chart
swatches, which is a claim about paint and is the note below.
"""

from __future__ import annotations

import numpy as np

from easel.color import linear_to_srgb, luminance, mix, mix_many, parse_color

__all__ = ["PIGMENTS", "Palette"]

#: The default limited palette: a warm and a cool of each primary, white, and a dark.
#:
#: The darks are **masstones** -- the colour of the paint straight from the tube,
#: laid thick -- and a masstone is much darker than the swatch most colour charts
#: print. That matters here because mixing cannot rescue it: this engine's mix
#: never takes a channel below the darker of its two ingredients, so the darkest
#: thing the box reaches is set by the swatches and nothing else. With the old,
#: chart-bright swatches the box floored at value ``0.23`` and no mixture went
#: below it, which is not what paint does -- ultramarine and burnt umber mixed are
#: meant to go near black, and that is the whole reason a limited palette can do
#: without one.
PIGMENTS: dict[str, str] = {
    # whites
    "titanium_white": "#F7F4EF",
    # yellows: warm then cool
    "cadmium_yellow": "#FFC012",
    "lemon_yellow": "#F2E33B",
    # reds: warm then cool
    "cadmium_red": "#E03C31",
    "alizarin": "#3E1A22",
    # blues: warm then cool
    "ultramarine": "#1A2856",
    "cerulean": "#215884",
    # earths / darks (no black by default)
    "burnt_umber": "#2A1E1A",
    "yellow_ochre": "#C08A2E",
    "burnt_sienna": "#56291A",
    "viridian": "#1A4638",
}

# Convenient short aliases so the painter can type less.
_ALIASES = {
    "white": "titanium_white",
    "yellow": "cadmium_yellow",
    "red": "cadmium_red",
    "blue": "ultramarine",
    "umber": "burnt_umber",
    "ochre": "yellow_ochre",
    "sienna": "burnt_sienna",
}
PIGMENTS.update({alias: PIGMENTS[target] for alias, target in _ALIASES.items()})


class Palette:
    """A mixing surface. Mixing here uses the same pigment model as the canvas.

    Named slots let the painter mix a colour once and refer to it later::

        pal = Palette()
        pal["shadow"] = pal.mix("ultramarine", "burnt_umber", 0.4)
        session.stroke([...], color=pal["shadow"])
    """

    def __init__(self, pigments: dict[str, str] | None = None) -> None:
        self._pigments = dict(pigments) if pigments is not None else dict(PIGMENTS)
        self._slots: dict[str, np.ndarray] = {}

    # -- lookup ------------------------------------------------------------------
    def __getitem__(self, name: str) -> np.ndarray:
        key = name.lower().replace(" ", "_")
        if key in self._slots:
            return self._slots[key]
        if key in self._pigments:
            return parse_color(self._pigments[key])
        raise KeyError(
            f"No pigment or mixed slot named {name!r}. "
            f"Pigments: {', '.join(sorted(set(self._pigments)))}. "
            f"Mixed slots: {', '.join(sorted(self._slots)) or '(none yet)'}"
        )

    def __setitem__(self, name: str, color) -> None:
        self._slots[name.lower().replace(" ", "_")] = parse_color(color)

    def __contains__(self, name: str) -> bool:
        key = name.lower().replace(" ", "_")
        return key in self._slots or key in self._pigments

    @property
    def slots(self) -> dict[str, np.ndarray]:
        """The painter's own mixed colours, by name."""
        return dict(self._slots)

    @property
    def pigment_names(self) -> list[str]:
        return sorted(set(self._pigments))

    # -- mixing ------------------------------------------------------------------
    def mix(self, a, b, ratio: float = 0.5) -> np.ndarray:
        """Mix two colours; ``ratio`` is the proportion of ``b``."""
        return mix(self._resolve(a), self._resolve(b), ratio)

    def mix_many(self, colors, weights=None) -> np.ndarray:
        """Mix several colours at once, with optional weights."""
        return mix_many([self._resolve(c) for c in colors], weights)

    def tint(self, color, amount: float = 0.3) -> np.ndarray:
        """Lighten toward white by adding white paint."""
        return self.mix(color, "titanium_white", amount)

    def shade(self, color, amount: float = 0.3) -> np.ndarray:
        """Darken by adding the dark (umber), not black."""
        return self.mix(color, "burnt_umber", amount)

    def desaturate(self, color, amount: float = 0.3) -> np.ndarray:
        """Knock a colour back toward a neutral of the same value.

        Uses a grey mixed to match the colour's own luminance, so desaturating does
        not also change how light the colour reads.
        """
        c = self._resolve(color)
        lin = parse_color(c)
        grey = np.full(3, float(luminance(lin)), dtype=np.float32)
        t = float(np.clip(amount, 0.0, 1.0))
        return np.clip(lin * (1.0 - t) + grey * t, 0.0, 1.0).astype(np.float32)

    def complement_grey(self, a, b, ratio: float = 0.5) -> np.ndarray:
        """Mix a colour with its rough complement to make a lively neutral."""
        return self.mix(a, b, ratio)

    # -- inspection --------------------------------------------------------------
    def hex(self, color) -> str:
        """The sRGB hex string for a colour, for logging and for ``look()`` labels."""
        lin = parse_color(self._resolve(color))
        return "#" + "".join(f"{int(round(float(v) * 255)):02x}" for v in linear_to_srgb(lin))

    def value_of(self, color) -> float:
        """How light the colour reads, 0..1 -- the same number ``look(values=True)`` shows.

        This is the sRGB-encoded luminance, not the linear one. Linear luminance is
        the wrong instrument for planning values: it puts every pigment but white and
        the yellows below 0.31 and reports *every* mixed dark as 0.04, so a painter
        cannot tell a coat-black from a burnt sienna with it, though the greyscale
        view shows them a clear step apart. Matching the values view is the point --
        the number and the picture have to agree or neither can be trusted.
        """
        lin = float(luminance(parse_color(self._resolve(color))))
        return float(linear_to_srgb(np.float32(lin)))

    @property
    def darkest_value(self) -> float:
        """The lowest value anything in this box reaches -- about ``0.13``.

        Mixing cannot go below it: this model never takes a channel under the darker
        of its two ingredients, so the darkest pigment is the floor, and piling on
        eight dried passes or four rounds of glazing lands within a hundredth of one
        flat pass. What sets the number is therefore the swatches, and the swatches
        are masstones, so the box now stops within a few hundredths of the engine's
        own limit -- the ``0.01`` linear reflectance floor in :mod:`easel.color`, or
        value ``0.10``. The rest of the gap is hue: a dark that is still blue, or
        still brown, cannot sit on the floor in all three channels at once.

        It is no longer a number the painter has to paint around. It is here so that
        :meth:`~easel.session.Session.compare` can tell an honest miss from the few
        cells a photograph may still hold below anything a pigment reaches, rather
        than reporting both the same way and sending the painter after neither.
        """
        return min(self.value_of(name) for name in set(self.pigment_names))

    def _resolve(self, color):
        if isinstance(color, str) and not color.startswith("#"):
            return self[color]
        return color

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"Palette({len(set(self._pigments))} pigments, {len(self._slots)} mixed slots)"
