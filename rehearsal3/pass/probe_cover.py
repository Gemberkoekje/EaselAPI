"""Probe: how many passes does a mass need to actually reach value_of(colour)?
Rehearsals R2/R3 asked for value 0.235 and put down something near 0.47.
Measures the exported PNG directly (my own code; nothing here touches the painting)."""
import os
from PIL import Image
from easel import Session, region

TMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_probe.png")


def canvas_value(s):
    s.export(TMP)
    im = Image.open(TMP).convert("RGB")
    w, h = im.size
    im = im.crop((int(w * .3), int(h * .3), int(w * .7), int(h * .7)))
    px = list(im.getdata())
    return sum(0.2126 * r + 0.7152 * g + 0.0722 * b for r, g, b in px) / (255 * len(px))


def fresh():
    s = Session(600, 450, texture="linen", ground="white", seed=5)
    p = s.palette
    p["dk"] = p.desaturate(p.mix("burnt_umber", "ultramarine", 0.35), 0.35)
    return s, p


for brush, kw in [("flat", dict(pressure="even", load=1.0)),
                  ("bristle", dict(pressure="even", load=1.0)),
                  ("round_hard", dict(pressure="even", load=1.0)),
                  ("flat", dict(pressure="even", load=1.0, opacity=1.0)),
                  ("flat", dict(pressure="taper", load=1.0))]:
    s, p = fresh()
    target = p.value_of(p["dk"])
    out = [f"{brush:10s} target {target:.3f} |"]
    for n in range(1, 6):
        y = 0.02
        while y < 1.0:
            s.stroke([(-0.02, y), (1.02, y)], brush, "dk", size=0.06,
                     load_falloff=0.0, **kw)
            y += 0.030
        s.dry()
        out.append(f"x{n} {canvas_value(s):.3f}")
    print(" ".join(out), " ", {k: v for k, v in kw.items() if k != "load"})

s, p = fresh()
for n in range(1, 5):
    s.block_in(region("all"), "flat", "dk", density=1.0, size=0.08)
    s.dry()
    print(f"block_in density=1.0 x{n}: {canvas_value(s):.3f} "
          f"(target {p.value_of(p['dk']):.3f}) strokes={s.stroke_count}")

s, p = fresh()
for n in range(1, 4):
    s.block_in(region("all"), "flat", "dk", density=1.0, size=0.08,
               direction="cross" if n % 2 else "horizontal")
    s.dry()
    print(f"block_in cross      x{n}: {canvas_value(s):.3f} strokes={s.stroke_count}")
os.remove(TMP)
