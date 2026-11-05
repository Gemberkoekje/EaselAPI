# How the measurements in answers-step2.md were run, 2026-11-05, easel-paint 0.8.0 on the machine that painted the pieces.
# Paths are this session's: TOOLS is the-curator/tools/easel; each run goes in a scratch folder of its own,
# because the scripts write their PNGs into the current folder.
TOOLS=/home/user/projects/the-curator/tools/easel
PY="/opt/tools/easel/venv/bin/python -I"

# Question 1 -- the cut from the places' coverage (2x2, 4x4), softened to 0.85 px and 2.5 px; then the sheets.
$PY cut_edges.py .          # prints the widths and sigmas, writes alphas.npz
$PY sheet.py                # alpha_085.png
$PY sheet_close.py          # alpha_085_close.png

# Question 2 -- the candle at 2x, and at 1x on a smooth canvas (one line of the script changed in each).
sed 's/^s = Session(W, H, /s = Session(W * 2, H * 2, /' $TOOLS/candle.py > candle2x.py && $PY candle2x.py 99
sed 's/texture="linen"/texture="smooth"/' $TOOLS/candle.py > candle_smooth.py && $PY candle_smooth.py 99
$PY texture.py              # the fine texture at 1x linen, 1x smooth, 2x and 4x reduced; texture_sheet.png
$PY plan_in_cut.py          # the planned light's median, whole cell and inside the cut

# Question 3 -- every hand-laid stroke as M2 and O3 read it, then the tally against each stroke's intent.
for job in "candle.py 99" "patron_default.py 99" "locked_shelf.py 99" "beyond_doorway.py 99" "desk.py 99" \
           "counter.py 99" "shelves.py left 99" "shelves.py right 99" "doorway_wall.py 99"; do
  set -- $job; $PY run_o3.py marks.jsonl $TOOLS/$@
done
$PY tally.py

# Question 4 -- bare ground inside each cut: the line's own measure, and canvas with nothing laid on it.
$PY ground_in_cut.py        # needs cut_edges.py's alphas.npz

# Question 5 -- umber with ultramarine beside a neutral of the same value; Oklab hue and chroma.
$PY swatches.py             # umber_ultramarine_vs_neutral.png
