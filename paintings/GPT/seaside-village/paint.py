"""An original seaside painting, made exclusively with Easel paint marks.

Run ``python paint.py sketch`` once, then each numbered pass with --rehearse
before running it without that flag. ``python paint.py export`` finishes the files.
"""

import argparse
from pathlib import Path

from easel import Region, Session, polygon


ROOT = Path(__file__).resolve().parent
PROCESS = ROOT / "process"
SESSION = PROCESS / "painting.easel"
WIDTH, HEIGHT = 1440, 960
BUDGET = 420


def palette(s):
    """Mix the limited, related colours used throughout the picture."""
    p = s.palette
    p["dark"] = p.mix("ultramarine", "burnt_umber", 0.36)
    p["violet"] = p.mix("ultramarine", "alizarin", 0.32)
    p["sky_top"] = p.at_value(p.mix("ultramarine", "alizarin", 0.18), 0.53)
    p["sky_mauve"] = p.at_value(p.mix("ultramarine", "alizarin", 0.47), 0.66)
    p["sky_rose"] = p.at_value(p.mix("burnt_sienna", "alizarin", 0.30), 0.73)
    p["horizon"] = p.at_value(p.mix("yellow_ochre", "cadmium_red", 0.65), 0.80)
    p["cloud"] = p.at_value(p.mix("ultramarine", "alizarin", 0.40), 0.58)
    p["cloud_light"] = p.at_value(p.mix("burnt_sienna", "alizarin", 0.19), 0.72)
    p["cloud_cool"] = p.at_value(p.mix("ultramarine", "cerulean", 0.25), 0.60)
    p["water_far"] = p.at_value(p.mix("cerulean", "alizarin", 0.21), 0.51)
    p["water_mid"] = p.at_value(p.mix("cerulean", "burnt_umber", 0.18), 0.39)
    p["water_deep"] = p.at_value(p.mix("ultramarine", "cerulean", 0.45), 0.27)
    p["water_lilac"] = p.at_value(p.mix("ultramarine", "alizarin", 0.29), 0.46)
    p["water_peach"] = p.at_value(p.mix("burnt_sienna", "alizarin", 0.24), 0.57)
    p["water_silver"] = p.at_value(p.mix("cerulean", "burnt_umber", 0.10), 0.57)
    p["headland"] = p.at_value(p.mix("ultramarine", "alizarin", 0.15), 0.42)
    p["distant"] = p.at_value(p.mix("ultramarine", "burnt_sienna", 0.34), 0.35)
    p["quay_dark"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.40), 0.21)
    p["quay_mid"] = p.at_value(p.mix("ultramarine", "burnt_sienna", 0.48), 0.31)
    p["quay_warm"] = p.at_value(p.mix("burnt_umber", "yellow_ochre", 0.40), 0.43)
    p["quay_top"] = p.at_value(p.mix("burnt_sienna", "yellow_ochre", 0.35), 0.55)
    p["wall_ochre"] = p.at_value(p.mix("yellow_ochre", "burnt_sienna", 0.20), 0.62)
    p["wall_cream"] = p.at_value(p.mix("yellow_ochre", "burnt_umber", 0.15), 0.73)
    p["wall_rose"] = p.at_value(p.mix("burnt_sienna", "alizarin", 0.22), 0.60)
    p["wall_cool"] = p.at_value(p.mix("ultramarine", "burnt_sienna", 0.37), 0.48)
    p["wall_shadow"] = p.at_value(p.mix("ultramarine", "burnt_sienna", 0.44), 0.37)
    p["roof_red"] = p.at_value(p.mix("burnt_sienna", "alizarin", 0.22), 0.32)
    p["roof_slate"] = p.at_value(p.mix("ultramarine", "burnt_sienna", 0.27), 0.26)
    p["roof_light"] = p.at_value(p.mix("burnt_sienna", "yellow_ochre", 0.16), 0.44)
    p["window"] = p.at_value(p.mix("cadmium_yellow", "cadmium_red", 0.14), 0.75)
    p["window_dim"] = p.at_value(p.mix("yellow_ochre", "cadmium_red", 0.12), 0.62)
    p["window_core"] = p.at_value(p.mix("cadmium_yellow", "titanium_white", 0.70), 0.91)
    p["reflection"] = p.at_value(p.mix("yellow_ochre", "cadmium_red", 0.19), 0.57)
    p["reflection_red"] = p.at_value(p.mix("cadmium_red", "alizarin", 0.29), 0.35)
    p["boat_red"] = p.mix("cadmium_red", "alizarin", 0.09)
    p["boat_light"] = p.at_value(p.mix("cadmium_red", "yellow_ochre", 0.12), 0.51)
    p["boat_shadow"] = p.at_value(p.mix("cadmium_red", "ultramarine", 0.40), 0.25)
    p["wood"] = p.at_value(p.mix("burnt_sienna", "yellow_ochre", 0.32), 0.49)
    p["rim"] = p.at_value(p.mix("yellow_ochre", "burnt_sienna", 0.28), 0.72)


def P(x, height, distance):
    """One projection for the village: eye 3 m high, looking along the quay."""
    return 0.22 + x * 0.85 / distance, 0.46 - (height - 3.0) * 1.275 / distance


HOUSE_SPECS = [
    ("far", 8.8, 39.0, 2.5, 3.2, 4.6, 4.3, "wall_cool", "roof_slate"),
    ("ochre", 10.6, 34.5, 3.1, 3.9, 5.5, 4.8, "wall_ochre", "roof_red"),
    ("rose", 13.5, 31.8, 3.0, 3.5, 4.8, 4.4, "wall_rose", "roof_slate"),
    ("cream", 16.0, 29.8, 3.4, 4.3, 6.0, 4.9, "wall_cream", "roof_red"),
    ("blue", 18.4, 27.5, 2.8, 3.7, 5.1, 2.0, "wall_cool", "roof_slate"),
    ("near", 20.7, 25.7, 4.0, 4.6, 6.6, 2.6, "wall_ochre", "roof_slate"),
]


def house(spec):
    name, x, z, width, eave, ridge, depth, wall, roof = spec
    front = polygon(
        [
            P(x, 0, z),
            P(x + width, 0, z),
            P(x + width, eave, z),
            P(x + width / 2, ridge, z),
            P(x, eave, z),
        ],
        name=name + " front",
    )
    side = polygon(
        [
            P(x, 0, z + depth),
            P(x, 0, z),
            P(x, eave, z),
            P(x, eave, z + depth),
        ],
        name=name + " side",
    )
    roof_shape = polygon(
        [
            P(x - 0.18, eave, z + depth + 0.25),
            P(x - 0.18, eave, z - 0.28),
            P(x + width / 2, ridge, z - 0.28),
            P(x + width / 2, ridge, z + depth + 0.25),
        ],
        name=name + " roof",
    )
    return {
        "front": front,
        "side": side,
        "roof": roof_shape,
        "wall_color": wall,
        "roof_color": roof,
        "spec": spec,
    }


HOUSES = {spec[0]: house(spec) for spec in HOUSE_SPECS}
CAPE = polygon(
    [
        (-0.04, 0.465),
        (0.045, 0.445),
        (0.095, 0.463),
        (0.15, 0.468),
        (0.19, 0.487),
        (0.245, 0.485),
        (0.285, 0.502),
        (0.375, 0.518),
        (0.20, 0.536),
        (-0.04, 0.553),
    ],
    name="distant headland",
)
QUAY = polygon(
    [
        (0.345, 0.557),
        (0.415, 0.552),
        (0.50, 0.573),
        (0.61, 0.590),
        (0.725, 0.609),
        (0.87, 0.629),
        (1.04, 0.651),
        (1.04, 0.830),
        (0.91, 0.782),
        (0.77, 0.729),
        (0.635, 0.677),
        (0.51, 0.631),
        (0.414, 0.599),
        (0.352, 0.586),
    ],
    name="curving harbour wall",
)
BOAT = polygon(
    [
        (0.417, 0.766),
        (0.445, 0.749),
        (0.492, 0.744),
        (0.566, 0.718),
        (0.625, 0.699),
        (0.640, 0.706),
        (0.619, 0.744),
        (0.572, 0.784),
        (0.497, 0.818),
        (0.449, 0.813),
        (0.426, 0.791),
    ],
    name="red dinghy",
)
BOAT_INSIDE = polygon(
    [
        (0.435, 0.767),
        (0.489, 0.760),
        (0.565, 0.734),
        (0.625, 0.711),
        (0.601, 0.740),
        (0.553, 0.769),
        (0.487, 0.795),
        (0.451, 0.791),
    ],
    name="dinghy interior",
)


def mass(s, shape, color, size, *, direction="axis", brush="flat", note="", **kw):
    opts = dict(
        density=0.94,
        solid=True,
        edge="hard",
        pressure="even",
        opacity=0.96,
        jitter=0.012,
        size_jitter=0.035,
    )
    opts.update(kw)
    return s.block_in(
        shape, brush, color, size=size, direction=direction, note=note, **opts
    )


def stroke(s, points, color, size, *, brush="bristle", note="", **kw):
    opts = dict(load=0.82, opacity=0.82, pressure="swell")
    opts.update(kw)
    return s.stroke(points, brush, color, size=size, note=note, **opts)


def sketch(s):
    s.pencil(CAPE.closed, pressure=0.32, smooth=False)
    s.pencil(QUAY.closed, pressure=0.50, smooth=False)
    for h in HOUSES.values():
        for shape in (h["side"], h["front"], h["roof"]):
            s.pencil(shape.closed, pressure=0.48, smooth=False)
    s.pencil(
        [
            (0.697, 0.443),
            (0.697, 0.276),
            (0.720, 0.242),
            (0.742, 0.275),
            (0.742, 0.491),
        ],
        pressure=0.48,
        smooth=False,
    )
    s.pencil(BOAT.closed, pressure=0.65, smooth=False)
    s.pencil(BOAT_INSIDE.closed, pressure=0.48, smooth=False)
    s.pencil([(0.474, 0.760), (0.496, 0.790)], pressure=0.4)
    s.pencil([(0.550, 0.741), (0.568, 0.760)], pressure=0.4)
    s.pencil([(0.635, 0.708), (0.675, 0.681), (0.713, 0.659)], pressure=0.3)
    s.mark("bow", 0.635, 0.705)
    s.mark("warm house", *P(17.7, 2.0, 29.8))


def underpainting(s):
    s.block_in(
        polygon([(-0.06, -0.06), (1.06, -0.06), (1.06, 0.60), (-0.06, 0.56)]),
        "bristle",
        "sky_mauve",
        size=0.23,
        density=0.73,
        direction=3,
        load=0.85,
        note="atmosphere: sky mass",
    )
    s.block_in(
        polygon([(-0.06, 0.49), (1.06, 0.48), (1.06, 1.06), (-0.06, 1.06)]),
        "flat",
        "water_mid",
        size=0.21,
        density=0.76,
        direction=-3,
        load=0.92,
        note="water: large mass",
    )
    s.block_in(
        QUAY,
        "bristle",
        "quay_dark",
        size=0.13,
        density=0.75,
        direction=19,
        note="quay: first dark",
    )


def upper_sky(s):
    s.scumble(
        polygon([(-0.08, -0.06), (1.08, -0.06), (1.08, 0.34), (-0.08, 0.41)]),
        "sky_top",
        "sky_mauve",
        9,
        brush="flat",
        direction=-3,
        load=1.0,
        load_falloff=0.0,
        opacity=0.95,
        jitter=0.006,
        size_jitter=0.022,
        note="atmosphere: lavender dusk",
    )


def horizon_sky(s):
    s.scumble(
        polygon(
            [(-0.08, 0.23), (0.45, 0.25), (1.08, 0.22), (1.08, 0.57), (-0.08, 0.59)]
        ),
        "sky_mauve",
        "horizon",
        11,
        brush="flat",
        direction=-2,
        load=1.0,
        load_falloff=0.0,
        opacity=0.94,
        jitter=0.004,
        size_jitter=0.018,
        note="atmosphere: last peach light",
    )
    stroke(
        s,
        [(-0.05, 0.388), (0.15, 0.392), (0.37, 0.368)],
        "sky_rose",
        0.048,
        load=0.45,
        opacity=0.52,
        note="atmosphere: light crossing",
    )


def clouds(s):
    # The first two rehearsals made speckles and ribbons. Redraw the passage as
    # broad, tapering volumes of air; close-valued glazes lose their boundaries.
    s.dry()
    paths = [
        (
            [(-0.04, 0.17), (0.09, 0.214), (0.23, 0.198), (0.39, 0.147)],
            "cloud",
            0.100,
            0.26,
        ),
        ([(-0.01, 0.18), (0.12, 0.217), (0.27, 0.191)], "sky_top", 0.045, 0.22),
        ([(0.03, 0.244), (0.16, 0.246), (0.32, 0.192)], "cloud_light", 0.025, 0.24),
        (
            [(1.06, 0.065), (0.91, 0.12), (0.76, 0.124), (0.64, 0.102)],
            "sky_top",
            0.095,
            0.25,
        ),
        ([(1.05, 0.12), (0.91, 0.154), (0.80, 0.15)], "cloud_light", 0.022, 0.16),
        ([(0.64, 0.309), (0.81, 0.297), (1.05, 0.33)], "cloud", 0.055, 0.26),
        ([(0.70, 0.334), (0.84, 0.328), (1.04, 0.354)], "sky_rose", 0.028, 0.20),
        ([(-0.03, 0.323), (0.14, 0.341), (0.28, 0.315)], "sky_rose", 0.065, 0.15),
        ([(0.13, 0.43), (0.30, 0.415), (0.51, 0.449)], "horizon", 0.10, 0.19),
    ]
    for points, color, size, opacity in paths:
        s.glaze(
            points,
            color,
            size=size,
            opacity=opacity,
            pressure=[0.12, 0.85, 1.0, 0.10],
            note="atmosphere: cloud veil",
        )


def far_water(s):
    sea = polygon(
        [(-0.06, 0.495), (1.06, 0.486), (1.06, 0.79), (-0.06, 0.76)],
        name="sea below horizon",
    )
    mass(s, sea, "water_far", 0.16, direction=0, note="water: horizon plane")
    s.scumble(
        Region(-0.06, 0.59, 1.06, 0.82),
        "water_far",
        "water_mid",
        9,
        brush="flat",
        direction=0,
        load=1.0,
        load_falloff=0.0,
        opacity=0.94,
        jitter=0.007,
        size_jitter=0.025,
        note="water: distant luminous plane",
    )


def near_water(s):
    s.scumble(
        polygon([(-0.07, 0.68), (1.07, 0.71), (1.07, 1.07), (-0.07, 1.07)]),
        "water_mid",
        "water_deep",
        10,
        brush="flat",
        direction=-2,
        load=1.0,
        load_falloff=0.0,
        opacity=0.92,
        jitter=0.008,
        size_jitter=0.024,
        note="water: deep foreground",
    )
    stroke(
        s,
        [(-0.05, 0.80), (0.14, 0.767), (0.32, 0.786)],
        "water_lilac",
        0.047,
        load=0.43,
        opacity=0.52,
        note="water: crossing current",
    )
    stroke(
        s,
        [(0.72, 0.90), (0.87, 0.91), (1.05, 0.951)],
        "water_mid",
        0.062,
        load=0.38,
        opacity=0.55,
        note="water: foreground turn",
    )


def distant_coast(s):
    s.dry()
    mass(
        s,
        CAPE.smooth(2),
        "headland",
        0.037,
        direction=4,
        brush="bristle",
        density=0.78,
        note="distance: headland",
    )
    little = polygon(
        [
            (0.294, 0.513),
            (0.326, 0.500),
            (0.357, 0.499),
            (0.389, 0.516),
            (0.43, 0.527),
            (0.291, 0.533),
        ]
    )
    mass(
        s,
        little.smooth(1),
        "distant",
        0.022,
        direction=4,
        brush="flat",
        note="distance: low island",
    )
    s.dry()
    s.glaze(
        [(-0.035, 0.526), (0.105, 0.535), (0.245, 0.526), (0.354, 0.530)],
        "water_far",
        size=0.034,
        opacity=0.26,
        pressure=[0.5, 1.0, 0.8, 0.05],
        note="distance: sea mist loses the shore",
    )
    stroke(
        s,
        [(0.19, 0.505), (0.244, 0.512), (0.291, 0.514)],
        "water_far",
        0.012,
        brush="round_hard",
        pressure=[0.0, 0.65, 0.0],
        opacity=0.45,
        tip_wobble=0.55,
        note="distance: headland dissolves",
    )


def village_foundation(s):
    s.dry()
    mass(
        s,
        QUAY,
        "quay_dark",
        0.061,
        direction=19,
        note="quay: wall in its own direction",
    )
    vegetation = polygon(
        [
            (0.344, 0.562),
            (0.367, 0.514),
            (0.389, 0.501),
            (0.409, 0.475),
            (0.433, 0.490),
            (0.478, 0.463),
            (0.505, 0.481),
            (0.562, 0.444),
            (0.603, 0.461),
            (0.663, 0.437),
            (0.726, 0.463),
            (0.771, 0.470),
            (0.864, 0.503),
            (0.923, 0.517),
            (1.035, 0.560),
            (1.035, 0.658),
            (0.735, 0.628),
            (0.515, 0.594),
        ],
        name="gardens behind the quay",
    )
    mass(
        s,
        vegetation,
        "roof_slate",
        0.080,
        brush="bristle",
        direction=12,
        density=0.78,
        note="surroundings: garden shadow",
    )


def bell_tower(s):
    s.dry()
    body = polygon([(0.696, 0.487), (0.698, 0.283), (0.742, 0.276), (0.744, 0.491)])
    front = polygon([(0.714, 0.486), (0.716, 0.284), (0.741, 0.277), (0.743, 0.490)])
    cap = polygon([(0.691, 0.287), (0.718, 0.237), (0.748, 0.280), (0.716, 0.289)])
    mass(s, body, "wall_shadow", 0.024, direction=90, note="subject: tower shadow")
    mass(s, front, "wall_ochre", 0.018, direction=90, note="subject: tower light")
    mass(s, cap, "roof_slate", 0.022, direction=0, note="subject: tower cap")
    stroke(
        s,
        [(0.726, 0.309), (0.727, 0.340)],
        "dark",
        0.011,
        brush="round_hard",
        pressure=[0.60, 1.0, 0.9],
        tip_wobble=0.15,
        load_falloff=0,
        note="subject: belfry opening",
    )
    stroke(
        s,
        [(0.702, 0.317), (0.702, 0.339)],
        "quay_dark",
        0.006,
        brush="flat",
        pressure="even",
        note="subject: far belfry slit",
    )


def paint_house(s, name):
    s.dry()
    h = HOUSES[name]
    front_size = {
        "far": 0.024,
        "ochre": 0.031,
        "rose": 0.029,
        "cream": 0.034,
        "blue": 0.030,
        "near": 0.042,
    }[name]
    mass(
        s,
        h["side"],
        "wall_shadow",
        front_size * 0.75,
        direction=90,
        note=f"subject: {name} cottage side",
    )
    mass(
        s,
        h["front"],
        h["wall_color"],
        front_size,
        direction=90,
        note=f"subject: {name} cottage face",
    )
    mass(
        s,
        h["roof"],
        h["roof_color"],
        front_size * 0.8,
        direction=h["roof"].axis,
        note=f"subject: {name} cottage roof",
    )


def roof_incidents(s):
    for name in ("ochre", "cream", "near"):
        h = HOUSES[name]
        _, x, z, width, eave, ridge, depth, _, _ = h["spec"]
        roof_line = [
            P(x + width * 0.10, eave + 0.3, z + depth * 0.80),
            P(x + width * 0.26, eave + 0.9, z + depth * 0.48),
            P(x + width * 0.43, ridge - 0.18, z + depth * 0.13),
        ]
        roof_light = s.palette.at_value(
            h["roof_color"], s.palette.value_of(h["roof_color"]) + 0.06
        )
        stroke(
            s,
            roof_line,
            roof_light,
            0.026 if name != "near" else 0.034,
            load=0.72,
            load_falloff=0.30,
            texture_sensitivity=0.45,
            opacity=0.55,
            clip=h["roof"],
            note=f"subject: {name} broken roof light",
        )
        chimney_x, chimney_y = P(x + width * 0.30, ridge - 0.35, z + depth * 0.6)
        stroke(
            s,
            [(chimney_x, chimney_y + 0.008), (chimney_x, chimney_y - 0.030)],
            "quay_mid",
            0.009 if name != "near" else 0.013,
            brush="flat",
            pressure="even",
            load=1,
            load_falloff=0,
            note="subject: chimney",
        )
        stroke(
            s,
            [
                (chimney_x - 0.004, chimney_y - 0.029),
                (chimney_x + 0.008, chimney_y - 0.029),
            ],
            "roof_slate",
            0.0045,
            brush="liner",
            pressure="even",
            tip_wobble=0.2,
            note="subject: chimney cap",
        )
    h = HOUSES["rose"]
    stroke(
        s,
        [P(13.55, 3.7, 34.8), P(14.3, 4.6, 33.3)],
        "quay_mid",
        0.026,
        clip=h["roof"],
        load=0.58,
        opacity=0.55,
        note="subject: blue slate glancing light",
    )


def solid_joins(s):
    # Shaped block-ins wander independently of the brush's jitter setting. These
    # three thin holes need actual paint before windows are placed on the walls.
    s.dry()
    for points, color, size in (
        ([(0.552, 0.456), (0.552, 0.561)], "wall_shadow", 0.014),
        ([(0.694, 0.414), (0.694, 0.576)], "wall_cream", 0.019),
        ([(0.904, 0.387), (0.905, 0.608)], "wall_ochre", 0.014),
    ):
        stroke(
            s,
            points,
            color,
            size,
            brush="flat",
            pressure="even",
            load=1,
            load_falloff=0,
            opacity=1,
            jitter=0.003,
            note="subject: bury an open join with wall paint",
        )


def walls_weathering(s):
    names = ("far", "ochre", "rose", "cream", "blue", "near")
    for i, name in enumerate(names):
        h = HOUSES[name]
        _, x, z, width, eave, _, _, wall, _ = h["spec"]
        left, bottom = P(x, 0, z)
        right = P(x + width, 0, z)[0]
        if i + 1 < len(names):
            right = min(right, HOUSES[names[i + 1]]["side"].box.x0)
        top = P(x, eave - 0.1, z)[1]
        visible = Region(left + 0.002, top, right - 0.002, bottom - 0.003)
        pale = s.palette.mix(wall, "wall_cream", 0.17)
        cool = s.palette.mix(wall, "wall_shadow", 0.19)
        stroke(
            s,
            [
                visible.point(0.18, 0.04),
                visible.point(0.29, 0.47),
                visible.point(0.43, 0.92),
            ],
            pale,
            0.027 + i * 0.002,
            load=0.75,
            load_falloff=0.25,
            opacity=0.57,
            texture_sensitivity=0.35,
            clip=visible,
            note=f"subject: {name} worn plaster light",
        )
        stroke(
            s,
            [visible.point(0.82, 0.48), visible.point(0.67, 0.99)],
            cool,
            0.025 + i * 0.001,
            load=0.69,
            load_falloff=0.20,
            opacity=0.50,
            texture_sensitivity=0.35,
            clip=visible,
            note=f"subject: {name} plaster shadow",
        )


OPENINGS = [
    (0.434, 0.493, 0.514, 0.010, "dim"),
    (0.508, 0.471, 0.500, 0.012, "warm"),
    (0.491, 0.523, 0.566, 0.015, "door"),
    (0.524, 0.532, 0.552, 0.010, "cool"),
    (0.596, 0.500, 0.524, 0.011, "dim"),
    (0.647, 0.493, 0.520, 0.009, "warm"),
    (0.701, 0.458, 0.489, 0.014, "warm"),
    (0.733, 0.464, 0.496, 0.012, "warm"),
    (0.716, 0.535, 0.584, 0.020, "door-warm"),
    (0.817, 0.480, 0.513, 0.014, "cool"),
    (0.805, 0.556, 0.601, 0.016, "door"),
    (0.875, 0.494, 0.526, 0.012, "dim"),
    (0.933, 0.438, 0.480, 0.018, "warm"),
    (0.982, 0.444, 0.489, 0.016, "warm"),
    (0.963, 0.547, 0.611, 0.023, "door"),
    (0.923, 0.535, 0.565, 0.014, "dim"),
]


def window_darks(s, start, end):
    s.dry()
    for x, top, bottom, width, kind in OPENINGS[start:end]:
        s.pencil(
            [
                (x - width / 2, top),
                (x + width / 2, top),
                (x + width / 2, bottom),
                (x - width / 2, bottom),
                (x - width / 2, top),
            ],
            pressure=0.35,
            smooth=False,
        )
        stroke(
            s,
            [(x, top), (x, bottom)],
            "dark" if "door" in kind else "quay_dark",
            width,
            brush="flat",
            pressure="even",
            load=1,
            load_falloff=0,
            opacity=0.97,
            jitter=0.004,
            size_jitter=0.022,
            note="subject: door or recessed window",
        )


def window_light(s):
    s.dry()
    for x, top, bottom, width, kind in OPENINGS:
        if kind == "door":
            continue
        colour = {
            "warm": "window",
            "dim": "window_dim",
            "cool": "water_lilac",
            "door-warm": "reflection",
        }[kind]
        inset = 0.004 if width < 0.013 else 0.0055
        stroke(
            s,
            [(x - width * 0.08, top + inset), (x + width * 0.03, bottom - inset)],
            colour,
            width * (0.58 if kind == "dim" else 0.64),
            brush="flat",
            pressure="even",
            load=1,
            load_falloff=0,
            opacity=0.93,
            jitter=0.009,
            size_jitter=0.05,
            note="subject: warm interior" if kind != "cool" else "subject: unlit glass",
        )


def quay_walkway(s):
    s.dry()
    walk = polygon(
        [
            (0.350, 0.557),
            (0.420, 0.559),
            (0.519, 0.575),
            (0.666, 0.589),
            (0.802, 0.603),
            (1.04, 0.627),
            (1.04, 0.678),
            (0.886, 0.648),
            (0.720, 0.620),
            (0.568, 0.596),
            (0.438, 0.576),
            (0.350, 0.578),
        ],
        name="quay walkway in perspective",
    )
    mass(s, walk, "quay_warm", 0.028, direction=9, note="quay: stone walkway")
    stroke(
        s,
        [
            (0.355, 0.578),
            (0.435, 0.580),
            (0.568, 0.602),
            (0.720, 0.627),
            (0.889, 0.657),
            (1.04, 0.686),
        ],
        "quay_top",
        0.012,
        brush="round_hard",
        pressure=[0.18, 0.32, 0.55, 0.7, 1.0],
        load=0.86,
        load_falloff=0.18,
        tip_wobble=0.25,
        note="quay: receding capstones",
    )
    for x, y, height, width in (
        (0.401, 0.577, 0.022, 0.007),
        (0.565, 0.604, 0.026, 0.009),
        (0.711, 0.635, 0.031, 0.011),
        (0.881, 0.666, 0.040, 0.014),
    ):
        stroke(
            s,
            [(x, y), (x - 0.001, y - height)],
            "dark",
            width,
            brush="flat",
            pressure="even",
            load=1,
            load_falloff=0,
            note="quay: iron mooring bollard",
        )


def boat_shadow(s):
    s.dry()
    stroke(
        s,
        [(0.419, 0.797), (0.471, 0.827), (0.522, 0.820), (0.611, 0.772)],
        "water_deep",
        0.038,
        brush="round_hard",
        pressure=[0.08, 0.85, 1.0, 0.06],
        load=1,
        load_falloff=0,
        tip_wobble=0.30,
        opacity=0.86,
        note="water: dinghy's soft shadow",
    )
    for points, color, size in (
        ([(0.443, 0.827), (0.470, 0.832), (0.499, 0.827)], "reflection_red", 0.018),
        ([(0.495, 0.843), (0.533, 0.834), (0.550, 0.825)], "boat_shadow", 0.012),
        ([(0.452, 0.853), (0.483, 0.858)], "reflection_red", 0.009),
        ([(0.540, 0.808), (0.578, 0.794)], "boat_shadow", 0.016),
    ):
        stroke(
            s,
            points,
            color,
            size,
            brush="round_hard",
            load=0.73,
            pressure=[0.05, 1.0, 0.1],
            tip_wobble=0.65,
            note="water: red broken below the hull",
        )


def boat_far_hull(s):
    s.dry()
    s.pencil(BOAT.closed, pressure=0.52, smooth=False)
    s.pencil(BOAT_INSIDE.closed, pressure=0.40, smooth=False)
    mass(
        s,
        BOAT.smooth(1),
        "boat_shadow",
        0.032,
        direction=((0.438, 0.801), (0.621, 0.720)),
        note="subject: dinghy mass",
    )
    stroke(
        s,
        [(0.423, 0.768), (0.491, 0.752), (0.563, 0.725), (0.632, 0.706)],
        "boat_red",
        0.014,
        brush="round_hard",
        pressure=[0.40, 0.80, 1.0, 0.18],
        tip_wobble=0.20,
        load=1,
        load_falloff=0,
        note="subject: far gunwale behind the interior",
    )


def boat_interior(s):
    mass(
        s,
        BOAT_INSIDE.smooth(1),
        "dark",
        0.027,
        direction=((0.447, 0.785), (0.619, 0.715)),
        note="subject: hollow dinghy interior",
    )
    stroke(
        s,
        [(0.452, 0.777), (0.505, 0.769), (0.568, 0.741), (0.607, 0.723)],
        "wood",
        0.008,
        brush="flat",
        pressure="even",
        load=1,
        load_falloff=0,
        clip=BOAT_INSIDE,
        opacity=0.87,
        note="subject: worn floorboard",
    )
    stroke(
        s,
        [(0.458, 0.786), (0.507, 0.777), (0.555, 0.757)],
        "quay_mid",
        0.006,
        brush="flat",
        pressure="even",
        load=1,
        load_falloff=0,
        clip=BOAT_INSIDE,
        note="subject: floor in shadow",
    )
    for points, size in (
        ([(0.472, 0.756), (0.491, 0.789)], 0.009),
        ([(0.549, 0.738), (0.568, 0.760)], 0.008),
    ):
        stroke(
            s,
            points,
            "wood",
            size,
            brush="flat",
            pressure="even",
            load=1,
            load_falloff=0,
            clip=BOAT_INSIDE,
            note="subject: wooden thwart across the interior",
        )


NEAR_HULL = polygon(
    [
        (0.428, 0.782),
        (0.454, 0.791),
        (0.484, 0.796),
        (0.520, 0.786),
        (0.559, 0.767),
        (0.603, 0.741),
        (0.634, 0.712),
        (0.617, 0.750),
        (0.573, 0.787),
        (0.500, 0.818),
        (0.451, 0.811),
    ],
    name="near red hull",
)


def boat_near_hull(s):
    s.dry()
    mass(
        s,
        NEAR_HULL.smooth(1),
        "boat_red",
        0.027,
        direction=((0.446, 0.805), (0.615, 0.737)),
        note="subject: near red hull",
    )
    stroke(
        s,
        [(0.444, 0.794), (0.483, 0.806), (0.528, 0.791), (0.586, 0.760)],
        "boat_light",
        0.018,
        brush="round_hard",
        load=0.92,
        load_falloff=0.15,
        pressure=[0.05, 0.9, 1.0, 0.04],
        clip=NEAR_HULL,
        tip_wobble=0.22,
        note="subject: red hull turning into light",
    )
    stroke(
        s,
        [(0.450, 0.812), (0.499, 0.816), (0.543, 0.800), (0.584, 0.777)],
        "boat_shadow",
        0.009,
        brush="round_hard",
        pressure=[0.2, 1.0, 0.6, 0.0],
        tip_wobble=0.35,
        clip=NEAR_HULL,
        note="subject: lower plank in shadow",
    )


def boat_rim_and_rope(s):
    s.dry()
    stroke(
        s,
        [(0.434, 0.781), (0.459, 0.796), (0.489, 0.799), (0.531, 0.785)],
        "rim",
        0.006,
        brush="round_hard",
        pressure=[0.1, 0.65, 1.0, 0.05],
        load=1,
        load_falloff=0,
        tip_wobble=0.23,
        note="subject: near gunwale catching the evening",
    )
    stroke(
        s,
        [(0.554, 0.770), (0.595, 0.748), (0.628, 0.716)],
        "boat_light",
        0.005,
        brush="liner",
        pressure=[0.2, 0.8, 0.05],
        tip_wobble=0.35,
        note="subject: bow edge interrupted by shade",
    )
    stroke(
        s,
        [(0.472, 0.759), (0.489, 0.786)],
        "rim",
        0.003,
        brush="liner",
        pressure=[0.05, 0.65, 0.1],
        tip_wobble=0.35,
        note="subject: glint on the nearer seat",
    )
    stroke(
        s,
        [(0.634, 0.711), (0.664, 0.704), (0.691, 0.676), (0.710, 0.636)],
        "quay_top",
        0.0022,
        brush="liner",
        pressure=[0.4, 0.5, 0.7, 0.8],
        load=1,
        load_falloff=0,
        opacity=0.83,
        note="subject: slack mooring rope",
    )
    stroke(
        s,
        [(0.456, 0.776), (0.488, 0.755), (0.536, 0.717)],
        "wood",
        0.0036,
        brush="liner",
        pressure="even",
        load=1,
        load_falloff=0,
        note="subject: a single resting oar",
    )
    stroke(
        s,
        [(0.535, 0.718), (0.550, 0.699)],
        "quay_top",
        0.009,
        brush="round_hard",
        pressure=[0.3, 1.0, 0.1],
        tip_wobble=0.35,
        note="subject: oar blade",
    )


WATER = polygon(
    [
        (-0.03, 0.496),
        (0.29, 0.496),
        (0.34, 0.542),
        (0.343, 0.593),
        (0.413, 0.603),
        (0.511, 0.635),
        (0.635, 0.681),
        (0.77, 0.734),
        (0.91, 0.787),
        (1.03, 0.834),
        (1.03, 1.03),
        (-0.03, 1.03),
    ],
    name="open harbour water",
)


def water_sheen(s):
    s.dry()
    p = s.palette
    p["water_dusk"] = p.at_value(p.mix("water_far", "sky_mauve", 0.34), 0.54)
    p["reflection_veil"] = p.at_value(p.mix("ultramarine", "alizarin", 0.40), 0.41)
    for points, color, size, opacity in (
        ([(-0.03, 0.56), (0.14, 0.59), (0.34, 0.575)], "water_dusk", 0.12, 0.21),
        ([(0.04, 0.582), (0.19, 0.607), (0.36, 0.595)], "water_peach", 0.053, 0.16),
        ([(0.03, 0.614), (0.17, 0.627), (0.30, 0.625)], "water_dusk", 0.040, 0.19),
        (
            [(0.704, 0.740), (0.717, 0.797), (0.732, 0.890)],
            "reflection_veil",
            0.049,
            0.11,
        ),
        (
            [(0.943, 0.831), (0.957, 0.898), (0.949, 1.025)],
            "reflection_veil",
            0.069,
            0.11,
        ),
        (
            [(0.505, 0.646), (0.504, 0.674), (0.518, 0.695)],
            "reflection_veil",
            0.024,
            0.11,
        ),
    ):
        s.glaze(
            points,
            color,
            size=size,
            opacity=opacity,
            pressure=[0.2, 1.0, 0.08],
            clip=WATER,
            note="water: veiled sky and interior light",
        )


def reflected_shadows(s):
    p = s.palette
    p["reflected_dark"] = p.mix("quay_dark", "water_mid", 0.35)
    # A first rehearsal left seven spoon-shaped islands. Treat the reflection as
    # one connected mass instead, with a broken lower edge and room for the bow.
    reflected = polygon(
        [
            (0.349, 0.590),
            (0.413, 0.603),
            (0.511, 0.635),
            (0.635, 0.681),
            (0.770, 0.734),
            (0.910, 0.787),
            (1.030, 0.834),
            (1.030, 0.955),
            (0.975, 0.936),
            (0.906, 0.915),
            (0.823, 0.863),
            (0.752, 0.828),
            (0.689, 0.774),
            (0.667, 0.731),
            (0.648, 0.699),
            (0.611, 0.691),
            (0.573, 0.696),
            (0.520, 0.686),
            (0.470, 0.651),
            (0.416, 0.651),
            (0.369, 0.618),
        ],
        name="broken reflection of the quay",
    )
    mass(
        s,
        reflected,
        "reflected_dark",
        0.055,
        direction=23,
        brush="bristle",
        solid=False,
        load=0.81,
        load_falloff=0.33,
        texture_sensitivity=0.40,
        opacity=0.68,
        note="water: connected village shadow",
    )
    ripple(
        s,
        [(0.673, 0.766), (0.704, 0.761), (0.746, 0.767)],
        "water_mid",
        0.014,
        note="water: current opens the reflected dark",
    )
    ripple(
        s,
        [(0.802, 0.851), (0.859, 0.847), (0.913, 0.860)],
        "water_mid",
        0.014,
        note="water: shadow broken by open water",
    )


def water_currents(s):
    p = s.palette
    p["water_join"] = p.mix("water_far", "water_mid", 0.46)
    marks = [
        ([(-0.04, 0.665), (0.095, 0.645), (0.244, 0.666)], "water_mid", 0.044),
        ([(0.25, 0.604), (0.313, 0.621), (0.381, 0.619)], "water_join", 0.041),
        ([(0.047, 0.705), (0.159, 0.694), (0.277, 0.716)], "water_lilac", 0.029),
        ([(0.232, 0.648), (0.332, 0.654), (0.438, 0.668)], "water_join", 0.035),
        ([(0.294, 0.709), (0.344, 0.696), (0.435, 0.713)], "water_mid", 0.039),
        ([(-0.045, 0.800), (0.102, 0.777), (0.25, 0.793)], "water_mid", 0.052),
        ([(0.107, 0.852), (0.245, 0.837), (0.369, 0.859)], "water_mid", 0.048),
        ([(0.317, 0.878), (0.438, 0.878), (0.579, 0.905)], "water_mid", 0.031),
        ([(0.65, 0.859), (0.732, 0.850), (0.815, 0.864)], "water_mid", 0.039),
        ([(0.718, 0.929), (0.828, 0.917), (0.934, 0.936)], "water_deep", 0.050),
        ([(0.803, 0.819), (0.876, 0.826), (0.941, 0.844)], "water_mid", 0.038),
        ([(0.423, 0.982), (0.553, 0.959), (0.680, 0.966)], "water_mid", 0.053),
    ]
    for points, color, size in marks:
        if color == "water_lilac":
            color = p.mix("water_lilac", "water_mid", 0.50)
        stroke(
            s,
            points,
            color,
            size * 0.48,
            brush="round_hard",
            load=1.0,
            load_falloff=0.0,
            pressure=[0.03, 0.8, 1.0, 0.12, 0.02],
            hardness=0.5,
            tip_wobble=0.38,
            opacity=0.60,
            clip=WATER,
            note="water: a current crossing the graded field",
        )


def ripple(s, points, color, size, note="water: broken reflection", **kw):
    opts = dict(
        brush="round_hard",
        pressure=[0.04, 1.0, 0.55, 0.04],
        load=0.93,
        load_falloff=0.25,
        tip_wobble=0.65,
        opacity=0.82,
        clip=WATER,
    )
    opts.update(kw)
    stroke(s, points, color, size, note=note, **opts)


def warm_reflections(s):
    s.dry()
    for points, size, color in (
        ([(0.486, 0.652), (0.505, 0.649), (0.528, 0.653)], 0.005, "reflection"),
        ([(0.502, 0.667), (0.519, 0.669), (0.539, 0.665)], 0.004, "window_dim"),
        ([(0.485, 0.689), (0.501, 0.687), (0.516, 0.690)], 0.005, "reflection"),
        ([(0.578, 0.684), (0.594, 0.680), (0.614, 0.682)], 0.005, "reflection"),
        ([(0.683, 0.726), (0.701, 0.722), (0.721, 0.724)], 0.006, "reflection"),
        ([(0.709, 0.745), (0.729, 0.741), (0.754, 0.745)], 0.007, "window_dim"),
        ([(0.690, 0.764), (0.706, 0.761), (0.726, 0.763)], 0.0045, "reflection"),
        ([(0.724, 0.783), (0.745, 0.779), (0.769, 0.784)], 0.006, "reflection"),
        ([(0.682, 0.808), (0.703, 0.804), (0.727, 0.806)], 0.005, "reflection"),
        ([(0.913, 0.830), (0.938, 0.825), (0.964, 0.829)], 0.008, "window_dim"),
        ([(0.955, 0.852), (0.980, 0.848), (1.008, 0.854)], 0.007, "reflection"),
        ([(0.899, 0.882), (0.925, 0.878), (0.951, 0.882)], 0.008, "reflection"),
    ):
        ripple(s, points, color, size)


def silver_water(s):
    for points, size, color in (
        ([(-0.03, 0.554), (0.045, 0.556), (0.101, 0.549)], 0.005, "water_silver"),
        ([(0.137, 0.566), (0.192, 0.567), (0.230, 0.563)], 0.003, "water_dusk"),
        ([(0.079, 0.621), (0.144, 0.624), (0.187, 0.618)], 0.0055, "water_silver"),
        ([(0.211, 0.592), (0.264, 0.590), (0.292, 0.594)], 0.004, "water_peach"),
        ([(0.254, 0.668), (0.285, 0.666), (0.328, 0.672)], 0.007, "water_lilac"),
        ([(0.132, 0.734), (0.184, 0.729), (0.228, 0.733)], 0.006, "water_lilac"),
        ([(0.325, 0.757), (0.368, 0.751), (0.402, 0.752)], 0.007, "water_lilac"),
        ([(0.018, 0.823), (0.084, 0.818), (0.149, 0.825)], 0.006, "water_mid"),
        ([(0.221, 0.892), (0.279, 0.886), (0.345, 0.891)], 0.010, "water_mid"),
        ([(0.431, 0.873), (0.489, 0.877), (0.557, 0.870)], 0.006, "water_lilac"),
        ([(0.615, 0.823), (0.655, 0.818), (0.686, 0.822)], 0.005, "water_mid"),
        ([(0.703, 0.982), (0.765, 0.977), (0.842, 0.983)], 0.008, "water_mid"),
    ):
        ripple(s, points, color, size, note="water: a broken catch of sky")


def reflected_light(s):
    p = s.palette
    p["soft_gold"] = p.at_value(p.mix("window", "horizon", 0.48), 0.70)
    for points, size, color in (
        ([(0.498, 0.654), (0.511, 0.653), (0.522, 0.655)], 0.003, "soft_gold"),
        ([(0.510, 0.678), (0.522, 0.677), (0.534, 0.679)], 0.003, "reflection"),
        ([(0.693, 0.729), (0.702, 0.727), (0.713, 0.729)], 0.004, "soft_gold"),
        ([(0.725, 0.749), (0.738, 0.747), (0.752, 0.750)], 0.0045, "window"),
        ([(0.705, 0.776), (0.714, 0.774), (0.725, 0.776)], 0.0035, "soft_gold"),
        ([(0.719, 0.831), (0.737, 0.828), (0.761, 0.833)], 0.005, "reflection"),
        ([(0.697, 0.862), (0.711, 0.859), (0.733, 0.864)], 0.004, "reflection"),
        ([(0.924, 0.835), (0.944, 0.832), (0.963, 0.835)], 0.005, "soft_gold"),
        ([(0.957, 0.873), (0.977, 0.869), (1.003, 0.875)], 0.004, "window_dim"),
        ([(0.922, 0.923), (0.945, 0.918), (0.976, 0.924)], 0.006, "reflection"),
    ):
        ripple(
            s, points, color, size, note="water: light travelling out from the windows"
        )


def quay_planes(s):
    s.dry()
    p = s.palette
    p["stone_cool"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.31), 0.28)
    planes = [
        (
            [
                (0.351, 0.585),
                (0.435, 0.590),
                (0.503, 0.603),
                (0.510, 0.631),
                (0.414, 0.599),
                (0.352, 0.586),
            ],
            "stone_cool",
            0.024,
        ),
        (
            [(0.503, 0.603), (0.646, 0.627), (0.650, 0.682), (0.510, 0.631)],
            "quay_mid",
            0.032,
        ),
        (
            [(0.646, 0.627), (0.797, 0.654), (0.798, 0.739), (0.650, 0.682)],
            "stone_cool",
            0.035,
        ),
        (
            [
                (0.797, 0.654),
                (1.040, 0.696),
                (1.040, 0.830),
                (0.910, 0.782),
                (0.798, 0.739),
            ],
            "quay_mid",
            0.042,
        ),
    ]
    for points, color, size in planes:
        mass(
            s,
            polygon(points),
            color,
            size,
            direction=19,
            note="quay: broad reflected stone planes",
        )
    stroke(
        s,
        [(0.634, 0.711), (0.664, 0.704), (0.691, 0.676), (0.710, 0.636)],
        "quay_top",
        0.0022,
        brush="liner",
        pressure=[0.4, 0.5, 0.7, 0.8],
        load=1,
        load_falloff=0,
        opacity=0.83,
        note="subject: restore the rope in front of the stone planes",
    )


def stone_incidents(s):
    p = s.palette
    p["stone_lit"] = p.at_value(p.mix("burnt_sienna", "ultramarine", 0.47), 0.37)
    p["stone_muted"] = p.at_value(p.mix("burnt_umber", "ultramarine", 0.38), 0.33)
    for points, size, color in (
        ([(0.442, 0.602), (0.471, 0.609)], 0.008, "stone_muted"),
        ([(0.523, 0.618), (0.557, 0.625)], 0.009, "stone_lit"),
        ([(0.565, 0.638), (0.607, 0.650)], 0.009, "stone_muted"),
        ([(0.610, 0.633), (0.638, 0.639)], 0.009, "stone_lit"),
        ([(0.718, 0.652), (0.748, 0.660)], 0.012, "stone_lit"),
        ([(0.754, 0.684), (0.784, 0.695)], 0.013, "stone_muted"),
        ([(0.815, 0.678), (0.855, 0.689)], 0.015, "stone_lit"),
        ([(0.862, 0.699), (0.897, 0.709)], 0.014, "stone_muted"),
        ([(0.918, 0.705), (0.965, 0.718)], 0.016, "stone_lit"),
        ([(0.836, 0.722), (0.872, 0.734)], 0.013, "stone_lit"),
        ([(0.902, 0.748), (0.944, 0.762)], 0.020, "stone_muted"),
        ([(0.970, 0.771), (1.033, 0.791)], 0.021, "stone_lit"),
    ):
        stroke(
            s,
            points,
            color,
            size,
            brush="flat",
            pressure="even",
            load=0.87,
            load_falloff=0.2,
            opacity=0.68,
            texture_sensitivity=0.34,
            clip=QUAY,
            note="quay: an uneven face of old stone",
        )


def mortar_and_tide(s):
    for points, size in (
        ([(0.570, 0.626), (0.568, 0.638), (0.581, 0.642)], 0.0018),
        ([(0.736, 0.666), (0.734, 0.680), (0.714, 0.675)], 0.0024),
        ([(0.826, 0.696), (0.850, 0.703), (0.849, 0.717)], 0.0020),
        ([(0.913, 0.722), (0.910, 0.740), (0.890, 0.734)], 0.0028),
        ([(0.972, 0.742), (0.996, 0.749), (0.994, 0.766)], 0.0030),
    ):
        stroke(
            s,
            points,
            "quay_dark",
            size,
            brush="liner",
            pressure=[0.2, 0.8, 0.2],
            load=0.85,
            tip_wobble=0.42,
            note="quay: a few open mortar joints",
        )
    p = s.palette
    p["lost_stone"] = p.mix("stone_cool", "reflected_dark", 0.45)
    for points, size in (
        ([(0.377, 0.593), (0.399, 0.598), (0.426, 0.608)], 0.015),
        ([(0.748, 0.724), (0.774, 0.735), (0.796, 0.745)], 0.022),
    ):
        stroke(
            s,
            points,
            "lost_stone",
            size,
            brush="round_hard",
            pressure=[0.05, 1.0, 0.02],
            tip_wobble=0.38,
            load=1,
            load_falloff=0,
            opacity=0.91,
            note="quay: the wall loses its edge in its reflection",
        )
    ripple(
        s,
        [(0.628, 0.795), (0.669, 0.790), (0.712, 0.798)],
        "water_deep",
        0.012,
        note="water: a tide line cuts the shadow",
    )
    ripple(
        s,
        [(0.807, 0.868), (0.855, 0.864), (0.904, 0.875)],
        "water_deep",
        0.015,
        note="water: lost lower reflection edge",
    )
    ripple(
        s,
        [(0.944, 0.945), (0.975, 0.949), (1.04, 0.953)],
        "water_deep",
        0.017,
        note="water: shadow disappears at the frame",
    )


def dwelling_details(s):
    s.dry()
    for points in (
        [(0.694, 0.477), (0.706, 0.477)],
        [(0.728, 0.482), (0.738, 0.482)],
        [(0.934, 0.446), (0.934, 0.473)],
        [(0.977, 0.468), (0.987, 0.468)],
    ):
        stroke(
            s,
            points,
            "quay_mid",
            0.0017,
            brush="liner",
            pressure="even",
            load=1,
            load_falloff=0,
            tip_wobble=0.2,
            note="subject: just four window divisions",
        )
    for points, size in (
        ([(0.702, 0.585), (0.729, 0.587)], 0.004),
        ([(0.793, 0.602), (0.815, 0.604)], 0.005),
        ([(0.947, 0.613), (0.979, 0.617)], 0.006),
    ):
        stroke(
            s,
            points,
            "quay_top",
            size,
            brush="flat",
            pressure="even",
            load=0.88,
            note="subject: worn doorstep",
        )
    p = s.palette
    p["garden"] = p.at_value(p.mix("viridian", "ultramarine", 0.27), 0.29)
    p["geranium"] = p.mix("boat_red", "alizarin", 0.16)
    for x, y, direction in ((0.686, 0.583, -1), (0.841, 0.605, 1)):
        stroke(
            s,
            [(x - 0.004, y), (x + 0.005, y)],
            "roof_light",
            0.010,
            brush="flat",
            pressure="even",
            load=1,
            load_falloff=0,
            note="subject: a terracotta pot",
        )
        stroke(
            s,
            [
                (x, y - 0.006),
                (x + direction * 0.005, y - 0.020),
                (x + direction * 0.011, y - 0.024),
            ],
            "garden",
            0.017,
            brush="round_hard",
            pressure=[0.4, 1.0, 0.03],
            tip_wobble=0.77,
            note="subject: a little garden at the door",
        )
        s.dab(
            x + direction * 0.009,
            y - 0.025,
            "round_hard",
            "geranium",
            size=0.0045,
            press=3,
            tip_wobble=0.8,
            note="subject: one muted geranium head",
        )


def evening_air(s):
    s.dry()
    p = s.palette
    p["smoke"] = p.at_value("cloud", 0.66)
    p["air_rose"] = p.at_value(p.mix("sky_mauve", "sky_rose", 0.25), 0.67)
    s.glaze(
        [(0.663, 0.318), (0.648, 0.282), (0.614, 0.267), (0.587, 0.239)],
        "smoke",
        size=0.024,
        opacity=0.10,
        pressure=[0.2, 0.4, 0.8, 0.01],
        note="atmosphere: a trace of chimney smoke",
    )
    s.glaze(
        [(0.484, 0.353), (0.475, 0.326), (0.449, 0.313)],
        "sky_mauve",
        size=0.014,
        opacity=0.10,
        pressure=[0.1, 0.7, 0.01],
        note="atmosphere: the far chimney's breath",
    )
    for points, color, size in (
        ([(-0.025, 0.283), (0.110, 0.265), (0.265, 0.288)], "air_rose", 0.077),
        ([(0.235, 0.201), (0.338, 0.193), (0.444, 0.157)], "sky_mauve", 0.060),
        ([(0.055, 0.382), (0.164, 0.369), (0.268, 0.385)], "sky_rose", 0.065),
    ):
        s.glaze(
            points,
            color,
            size=size,
            opacity=0.10,
            pressure=[0.05, 0.8, 0.1],
            note="atmosphere: a close-valued veil",
        )
    s.glaze(
        [(0.236, 0.513), (0.276, 0.525), (0.321, 0.530)],
        "water_far",
        size=0.025,
        opacity=0.15,
        pressure=[0.05, 0.7, 0.02],
        note="distance: lose the low edge without dragging light from the sky",
    )
    s.glaze(
        [(0.179, 0.519), (0.236, 0.528), (0.291, 0.524)],
        "water_far",
        size=0.025,
        opacity=0.17,
        pressure=[0.1, 1.0, 0.05],
        note="distance: the headland's end is mist",
    )
    for points, size, color in (
        (
            [(0.274, 0.352), (0.281, 0.348), (0.289, 0.354), (0.298, 0.349)],
            0.0024,
            "cloud",
        ),
        (
            [(0.319, 0.330), (0.325, 0.327), (0.331, 0.331), (0.337, 0.329)],
            0.0018,
            "cloud",
        ),
        ([(0.248, 0.369), (0.252, 0.367), (0.258, 0.370)], 0.0015, "sky_mauve"),
    ):
        stroke(
            s,
            points,
            color,
            size,
            brush="liner",
            pressure=[0.05, 0.8, 0.4, 0.1],
            tip_wobble=0.2,
            load=1,
            note="atmosphere: a gull far out over the harbour",
        )


def tide_fragments(s):
    # Dark water through the coloured marks is as important as more light on them.
    for points, size, color in (
        ([(0.427, 0.827), (0.454, 0.828), (0.487, 0.829)], 0.004, "water_deep"),
        ([(0.457, 0.837), (0.491, 0.837), (0.520, 0.832)], 0.005, "water_deep"),
        ([(0.476, 0.853), (0.506, 0.850), (0.537, 0.847)], 0.005, "water_deep"),
        ([(0.493, 0.695), (0.519, 0.692), (0.544, 0.695)], 0.005, "water_mid"),
        ([(0.684, 0.748), (0.709, 0.749), (0.730, 0.747)], 0.004, "reflected_dark"),
        ([(0.716, 0.780), (0.743, 0.783), (0.772, 0.779)], 0.004, "reflected_dark"),
        ([(0.669, 0.806), (0.692, 0.810), (0.716, 0.809)], 0.004, "water_deep"),
        ([(0.731, 0.829), (0.754, 0.831), (0.778, 0.828)], 0.004, "water_deep"),
        ([(0.898, 0.830), (0.921, 0.832), (0.945, 0.831)], 0.0035, "reflected_dark"),
        ([(0.948, 0.857), (0.981, 0.856), (1.01, 0.858)], 0.0045, "reflected_dark"),
        ([(0.909, 0.885), (0.934, 0.885), (0.963, 0.883)], 0.004, "water_deep"),
        ([(0.926, 0.922), (0.950, 0.925), (0.988, 0.922)], 0.0045, "water_deep"),
    ):
        ripple(
            s,
            points,
            color,
            size,
            note="water: interrupt the reflections with the tide",
        )


def last_water(s):
    for points, size, color in (
        ([(0.025, 0.589), (0.066, 0.591), (0.091, 0.587)], 0.0026, "water_dusk"),
        ([(0.183, 0.645), (0.224, 0.642), (0.250, 0.646)], 0.0034, "water_silver"),
        ([(0.033, 0.718), (0.074, 0.715), (0.102, 0.719)], 0.0045, "water_mid"),
        ([(0.277, 0.784), (0.309, 0.781), (0.344, 0.785)], 0.0035, "water_lilac"),
        ([(0.370, 0.813), (0.398, 0.809), (0.421, 0.812)], 0.003, "water_lilac"),
        ([(0.422, 0.851), (0.455, 0.848), (0.478, 0.851)], 0.0032, "reflection_red"),
        ([(0.588, 0.846), (0.618, 0.842), (0.654, 0.846)], 0.0043, "water_lilac"),
        ([(0.760, 0.887), (0.795, 0.884), (0.827, 0.890)], 0.0035, "water_mid"),
        ([(0.684, 0.855), (0.700, 0.853), (0.718, 0.855)], 0.0025, "window_dim"),
        ([(0.943, 0.954), (0.967, 0.952), (0.992, 0.957)], 0.0035, "reflection"),
    ):
        ripple(s, points, color, size, note="water: the last small stirrings")


def quiet_sky_joins(s):
    # The weakest remaining passage is the broad sky's stepped joins. These are
    # all close-valued films in open air, placed clear of the village silhouettes.
    s.dry()
    p = s.palette
    p["sky_mid_veil"] = p.mix("sky_top", "sky_mauve", 0.50)
    p["sky_warm_veil"] = p.mix("sky_mauve", "sky_rose", 0.45)
    p["sky_low_veil"] = p.mix("sky_rose", "horizon", 0.32)
    for points, color, size, opacity in (
        (
            [(-0.05, 0.155), (0.18, 0.172), (0.44, 0.205), (0.64, 0.190)],
            "sky_mid_veil",
            0.118,
            0.25,
        ),
        (
            [(-0.04, 0.265), (0.16, 0.285), (0.36, 0.310), (0.59, 0.290)],
            "sky_warm_veil",
            0.075,
            0.23,
        ),
        ([(1.05, 0.126), (0.93, 0.165), (0.77, 0.148)], "sky_mid_veil", 0.10, 0.22),
        ([(0.775, 0.211), (0.89, 0.217), (1.04, 0.221)], "sky_warm_veil", 0.050, 0.20),
        ([(0.03, 0.389), (0.17, 0.406), (0.33, 0.387)], "sky_low_veil", 0.065, 0.21),
        ([(-0.01, 0.174), (0.12, 0.216), (0.27, 0.190)], "cloud", 0.057, 0.13),
        ([(0.98, 0.087), (0.84, 0.126), (0.76, 0.119)], "sky_top", 0.075, 0.17),
        ([(0.08, 0.324), (0.18, 0.337), (0.305, 0.308)], "sky_rose", 0.050, 0.09),
    ):
        s.glaze(
            points,
            color,
            size=size,
            opacity=opacity,
            pressure=[0.04, 0.8, 1.0, 0.08],
            note="atmosphere: soften a stepped sky join",
        )


def final_lights(s):
    s.dry()
    for points, size in (
        ([(0.506, 0.478), (0.507, 0.488)], 0.0030),
        ([(0.699, 0.465), (0.700, 0.472)], 0.0037),
        ([(0.731, 0.472), (0.731, 0.479)], 0.0033),
        ([(0.929, 0.447), (0.929, 0.465)], 0.0046),
        ([(0.979, 0.454), (0.980, 0.462)], 0.0040),
    ):
        stroke(
            s,
            points,
            "window_core",
            size,
            brush="round_hard",
            pressure=[0.2, 1.0, 0.45],
            tip_wobble=0.45,
            load=1,
            load_falloff=0,
            opacity=0.98,
            note="subject: the brightest interior light",
        )
    s.palette["reflected_core"] = s.palette.at_value(
        s.palette.mix("window_core", "horizon", 0.25), 0.82
    )
    for points, size in (
        ([(0.701, 0.732), (0.709, 0.731)], 0.0020),
        ([(0.735, 0.747), (0.746, 0.748)], 0.0025),
        ([(0.935, 0.836), (0.947, 0.835)], 0.0030),
    ):
        ripple(s, points, "reflected_core", size, note="water: three sharp gold glints")
    stroke(
        s,
        [(0.459, 0.794), (0.475, 0.798)],
        "wall_cream",
        0.0019,
        brush="liner",
        pressure=[0.0, 0.9, 0.0],
        tip_wobble=0.35,
        note="subject: the smallest catch on the boat",
    )
    stroke(
        s,
        [(0.708, 0.604), (0.714, 0.604)],
        "water_silver",
        0.0020,
        brush="liner",
        pressure=[0.1, 0.8, 0.05],
        tip_wobble=0.55,
        note="quay: one cool glint on the bollard",
    )


def signature(s):
    s.erase()
    p = s.palette
    p["signature_blue"] = p.at_value("water_deep", 0.35)
    for points in (
        [(0.040, 0.953), (0.050, 0.956), (0.064, 0.951)],
        [(0.042, 0.962), (0.053, 0.965), (0.069, 0.960)],
        [(0.052, 0.954), (0.054, 0.936), (0.062, 0.947)],
    ):
        stroke(
            s,
            points,
            "signature_blue",
            0.0018,
            brush="liner",
            pressure=[0.1, 0.8, 0.2],
            load=1,
            tip_wobble=0.30,
            note="signature",
        )


STAGES = {
    "01-underpainting": underpainting,
    "02-upper-sky": upper_sky,
    "03-horizon-sky": horizon_sky,
    "04-clouds": clouds,
    "05-far-water": far_water,
    "06-near-water": near_water,
    "07-distant-coast": distant_coast,
    "08-village-foundation": village_foundation,
    "09-bell-tower": bell_tower,
    "10-far-cottage": lambda s: paint_house(s, "far"),
    "11-ochre-cottage": lambda s: paint_house(s, "ochre"),
    "12-rose-cottage": lambda s: paint_house(s, "rose"),
    "13-cream-cottage": lambda s: paint_house(s, "cream"),
    "14-blue-cottage": lambda s: paint_house(s, "blue"),
    "15-near-cottage": lambda s: paint_house(s, "near"),
    "15b-solid-joins": solid_joins,
    "16-roof-incidents": roof_incidents,
    "17-plaster": walls_weathering,
    "18-far-window-darks": lambda s: window_darks(s, 0, 8),
    "19-near-window-darks": lambda s: window_darks(s, 8, 16),
    "20-window-light": window_light,
    "21-quay-walkway": quay_walkway,
    "22-boat-shadow": boat_shadow,
    "23-boat-far-hull": boat_far_hull,
    "24-boat-interior": boat_interior,
    "25-boat-near-hull": boat_near_hull,
    "26-boat-rim-and-rope": boat_rim_and_rope,
    "27-water-sheen": water_sheen,
    "28-reflected-shadows": reflected_shadows,
    "29-water-currents": water_currents,
    "30-warm-reflections": warm_reflections,
    "31-silver-water": silver_water,
    "32-reflected-light": reflected_light,
    "33-quay-planes": quay_planes,
    "34-stone-incidents": stone_incidents,
    "35-mortar-and-tide": mortar_and_tide,
    "36-dwelling-details": dwelling_details,
    "37-evening-air": evening_air,
    "38-tide-fragments": tide_fragments,
    "39-last-water": last_water,
    "39b-quiet-sky-joins": quiet_sky_joins,
    "40-final-lights": final_lights,
    "41-signature": signature,
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["sketch", *STAGES, "export", "report"])
    parser.add_argument("--rehearse", action="store_true")
    parser.add_argument("--count", action="store_true")
    args = parser.parse_args()

    if args.stage == "sketch":
        if SESSION.exists():
            raise FileExistsError(
                "The painting already exists; keep its brush history."
            )
        s = Session(
            WIDTH,
            HEIGHT,
            texture="linen",
            ground="#746d78",
            seed=61,
            texture_strength=0.72,
            budget=BUDGET,
            out_dir=PROCESS,
        )
        palette(s)
        sketch(s)
        s.save(SESSION)
        print(s.look(path=PROCESS / "00-drawing.png", grid=True, marks=False))
        print(s.look(path=PROCESS / "00-drawing-plain.png", marks=False))
        return

    s = Session.load(SESSION)
    palette(s)
    if args.stage == "report":
        print(s.budget_line())
        print(s.report(subject_share=0.40))
        print(s.log(last=12))
        return
    if args.stage == "export":
        print(s.export(ROOT / "painting.png", sketch=False))
        print(s.timelapse_gif(ROOT / "painting.gif", fps=9, every=2))
        print(s.history.save_log(PROCESS / "strokes.json"))
        print(s.contact_sheet(PROCESS / "timelapse-contact-sheet.png"))
        print(
            s.look(
                path=PROCESS / "final-values.png",
                values=True,
                sketch=False,
                marks=False,
            )
        )
        print(s.budget_line())
        return

    if args.rehearse or args.count:
        s = s.scratch(count_only=args.count)
    start = len(s.history.records)
    before = s.spent
    STAGES[args.stage](s)
    print(f"Pass {args.stage}: {s.spent - before} marks")
    print(s.budget_line())
    if args.count:
        return
    suffix = "rehearsal" if args.rehearse else "painted"
    print(
        s.look(
            path=PROCESS / f"{args.stage}-{suffix}.png",
            sketch=False,
            marks=False,
            scale=1000,
        )
    )
    print(
        s.look(
            path=PROCESS / f"{args.stage}-{suffix}-values.png",
            values=True,
            sketch=False,
            marks=False,
            scale=800,
        )
    )
    print(s.report(since=start, subject_share=0.40))
    if not args.rehearse:
        s.save(SESSION)


if __name__ == "__main__":
    main()
