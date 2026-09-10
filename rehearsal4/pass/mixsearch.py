"""Find palette mixtures that land on the reference's mass colours."""
from easel import Session

s = Session(400, 200, seed=1)
p = s.palette

NAMES = ["titanium_white", "cadmium_yellow", "lemon_yellow", "cadmium_red",
         "alizarin", "ultramarine", "cerulean", "burnt_umber", "yellow_ochre",
         "burnt_sienna", "viridian"]

TARGETS = {
    "table_lit":  "#9F8D79",
    "table_mid":  "#8C765D",
    "table_warm": "#7D6B53",
    "table_dark": "#6F583D",
    "table_cool": "#685848",
    "shadow_lo":  "#25201A",
    "shadow_hi":  "#4A3E33",
    "mug_lit":    "#B8C0CC",
    "mug_face":   "#6E7080",
    "mug_shade":  "#505464",
    "tea":        "#0D0908",
    "crew":       "#1A120F",
    "tag":        "#211B29",
    "spoon_lit":  "#9AA0A8",
    "visor":      "#8A9098",
}


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def dist(h1, h2):
    a, b = rgb(h1), rgb(h2)
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


for name, target in TARGETS.items():
    best = None
    for i, a in enumerate(NAMES):
        for b in NAMES[i:]:
            for r in [x / 10 for x in range(0, 11)]:
                base = p.mix(a, b, r)
                for w in [x / 20 for x in range(0, 21)]:
                    c = p.mix(base, "titanium_white", w) if w else base
                    for d in (0.0, 0.25, 0.5):
                        cc = p.desaturate(c, d) if d else c
                        h = p.hex(cc)
                        e = dist(h, target)
                        if best is None or e < best[0]:
                            best = (e, a, b, r, w, d, h, p.value_of(cc))
    e, a, b, r, w, d, h, v = best
    tv = p.value_of(target) if hasattr(p, "value_of") else 0
    print(f"{name:10s} target {target} -> {h} err {e:5.1f} v={v:.2f}"
          f"   mix({a},{b},{r}) white {w} desat {d}")
