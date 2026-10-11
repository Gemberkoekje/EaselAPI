# The shell side of the measurements in answers.md, as run on 2026-10-11 (easel-paint 0.8.0, Linux).
# Paths are this session's: TOOLS is the-curator/tools/easel, Q a scratch folder.
TOOLS=/home/user/projects/the-curator/tools/easel
Q=/tmp/claude-0/-home-user-projects/effc84d7-d7e9-5d60-848f-887f6f888335/scratchpad/q2
PY="/opt/tools/easel/venv/bin/python -I"; E=/opt/tools/easel/venv/bin/easel

# The candle's checklist, re-run (its log was not kept); candle_rgb.png is identical to the shipped run.
cd $Q/candle && $PY $TOOLS/candle.py 99

# The candle at four times its size: only the Session line changes, so the geometry, sizes and seed are the same.
cd $Q/candle4x && sed 's/^s = Session(W, H, /s = Session(W * 4, H * 4, /' $TOOLS/candle.py > candle4x.py && $PY candle4x.py 99
$PY $Q/../easel-answers/measurements/compare4x.py

# s.report() at the end of the candle and the patron.
cd $Q/report && for f in candle patron_default; do
  sed 's/^    print(s.checklist())$/    print(s.checklist())\n    print("=== report ===")\n    print(s.report())/' $TOOLS/$f.py > $f.py
  $PY $f.py 99 | sed -n '/=== report ===/,$p'; done

# The candle through easel run --rehearse: two lines changed (STAGE fixed, the Session line removed).
cd $Q/run && $E new candle.easel --size 120x300 --texture linen --ground toned_warm_grey --seed 61 --budget 110 --no-prelude --force
sed -e '/^s = Session(/d' -e 's/^STAGE = .*/STAGE = 99/' $TOOLS/candle.py > pass.py && $E run candle.easel pass.py --rehearse

# What the guide prints with no flags: PAINTER.md lines 28-146 exactly (no output means identical).
$E guide > short.txt; $E guide --full > full.txt; sed -n '28,146p' full.txt | diff - short.txt
$E guide --help     # the only help text that names --reference

# The Python measurements: run each with the Easel venv's python. cutaway.py reads paths relative to $Q, so run it from there.
# candle_1x_vs_4x.png is compare4x.py's pair.png: left as shipped, right painted at 4x and reduced, both cut out on one grey.
# patron_rim.png: the shipped patron's hood and shoulders over a doorway-like colour, enlarged 2x (nearest).
