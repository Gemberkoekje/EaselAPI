"""Execute every python block in PAINTER.md, the way a fresh reader would."""
import io, re, sys, traceback
from pathlib import Path

text = io.open("PAINTER.md", encoding="utf-8").read()
blocks = re.findall(r"```python\n(.*?)```", text, re.S)
print(f"{len(blocks)} python blocks\n")

PREAMBLE = (
    "from easel import Session, Region, region, cell, horizon, below, above\n"
    "s = Session(400, 300, ground='toned_grey', seed=1, timelapse=False, out_dir='out/_check')\n"
    "p = s.palette\n"
    "s.palette['dark'] = s.palette.mix('ultramarine','burnt_umber',0.45)\n"
    "s.palette['corrected_colour'] = s.palette['dark']\n"
    "s.palette['light'] = s.palette.tint('yellow_ochre', 0.5)\n"
    "s.palette['shadow'] = s.palette['dark']\n"
    "s.palette['mid'] = s.palette['light']\n"
    "s.palette['pale'] = s.palette['light']\n"
    "s.palette['cool'] = s.palette['dark']\n"
    "path = [(0.2,0.3),(0.5,0.4),(0.8,0.3)]\n"
)
ok = bad = skipped = 0
for i, b in enumerate(blocks, 1):
    head = b.strip().splitlines()[0][:60]
    if re.search(r"^\s*s\.\w+\(.*[=,]\s*(brush|color|points|region)\b", b, re.M) or \
       re.search(r"\.\.\.", b):
        # signature listings and elided pseudo-code
        skipped += 1
        print(f"  {i:>2} SKIP (pseudo-code)  {head}")
        continue
    src = b.replace('"ref.jpg"', repr(r"C:\temp\AntonConspiracy.jpg"))
    try:
        exec(compile(PREAMBLE + src, f"<block {i}>", "exec"), {})
        ok += 1
        print(f"  {i:>2} ok               {head}")
    except Exception as e:
        bad += 1
        print(f"  {i:>2} FAIL             {head}\n       {type(e).__name__}: {e}")
print(f"\nok {ok}  failed {bad}  skipped {skipped}")
sys.exit(1 if bad else 0)
