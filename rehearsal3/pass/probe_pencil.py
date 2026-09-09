"""Probe: PAINTER.md line 220-221 says paint covers graphite "in proportion to
how much actually lands: it survives under a scumble and in the ground". In c4 a
single `block_in(region("all"), "flat", c, density=0.78, size=0.22)` erased the
whole drawing outright. This measures how much graphite is left at four densities.
Scratch sessions; nothing here touches either painting."""
import os
from PIL import Image
from easel import Session, region

TMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_pen.png")


def contrast_on_the_line(s):
    """std-dev of luma in a band ON the pencil line minus a band well off it.
    ~0 means the graphite has gone."""
    s.export(TMP)
    im = Image.open(TMP).convert("L")
    w, h = im.size

    def band(y0, y1):
        px = list(im.crop((int(w * .1), int(h * y0), int(w * .9), int(h * y1)))
                  .getdata())
        m = sum(px) / len(px)
        return (sum((v - m) ** 2 for v in px) / len(px)) ** 0.5

    return band(0.28, 0.38), band(0.62, 0.72)


for dens in (0.30, 0.50, 0.78, 1.00):
    s = Session(800, 600, texture="linen", ground="umber_wash", seed=11)
    for i in range(9):
        y = 0.30 + i * 0.011
        s.pencil([(0.05, y), (0.95, y + 0.004)], pressure=0.85)
    on0, off0 = contrast_on_the_line(s)
    s.block_in(region("all"), "flat",
               s.palette.mix("yellow_ochre", "burnt_umber", 0.4),
               density=dens, size=0.22, direction="diagonal")
    on1, off1 = contrast_on_the_line(s)
    print(f"density {dens:.2f}: graphite band sd {on0:6.2f} -> {on1:5.2f} "
          f"| bare canvas sd {off0:6.2f} -> {off1:5.2f} "
          f"| signal left {max(0.0, on1 - off1):5.2f} of {on0 - off0:5.2f} "
          f"({s.stroke_count} strokes)")
os.remove(TMP)
