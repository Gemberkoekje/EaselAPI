"""The candle painted at 4x (candle4x/candle_rgb.png) reduced to 120x300, against the shipped 1x run."""
import numpy as np
from PIL import Image
Q = "/tmp/claude-0/-home-user-projects/effc84d7-d7e9-5d60-848f-887f6f888335/scratchpad/q2/"
A = "/home/user/projects/the-curator/game/art/easel/"
one = Image.open(Q + "candle/candle_rgb.png").convert("RGB")
small = Image.open(Q + "candle4x/candle_rgb.png").convert("RGB").resize(one.size, Image.LANCZOS)
small.save(Q + "candle4x/candle_4x_down.png")
al = np.asarray(Image.open(A + "candle.png").convert("RGBA"))[:, :, 3] > 128
for name, im in (("1x", one), ("4x reduced", small)):
    V = (np.asarray(im).astype(float) / 255) @ [0.2126, 0.7152, 0.0722]
    top = V[30:80, 45:75][al[30:80, 45:75]]
    print(f"{name:11s} wax top (y 30-80): mean value {top.mean():.2f}, 95th pct {np.percentile(top, 95):.2f}")
bg = Image.new("RGB", one.size, (96, 92, 88))
pair = Image.new("RGB", (one.size[0] * 2 + 10, one.size[1]), (40, 40, 40))
alpha = Image.open(A + "candle.png").getchannel("A")
for i, im in enumerate((one, small)):
    pair.paste(Image.composite(im, bg, alpha), (i * (one.size[0] + 10), 0))
pair.resize((pair.size[0] * 2, pair.size[1] * 2), Image.NEAREST).save(Q + "candle4x/pair.png")
