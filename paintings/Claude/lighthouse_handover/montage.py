import sys
from PIL import Image, ImageDraw
out, width, files = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
ims = []
for f in files:
    im = Image.open(f).convert("RGB")
    h = int(im.height * width / im.width)
    ims.append((f.rsplit("/", 1)[-1], im.resize((width, h))))
H = sum(im.height + 18 for _, im in ims)
sheet = Image.new("RGB", (width, H), (20, 20, 20))
y = 0
d = ImageDraw.Draw(sheet)
for name, im in ims:
    d.text((4, y + 3), name, fill=(230, 230, 230))
    sheet.paste(im, (0, y + 18)); y += im.height + 18
sheet.save(out)
