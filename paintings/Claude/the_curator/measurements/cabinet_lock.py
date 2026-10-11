"""How bright the cabinet's lock came out: the plan's light, D4:E5, planned at 0.6."""
import numpy as np
from PIL import Image
V = (np.asarray(Image.open("/home/user/projects/the-curator/game/art/easel/locked_shelf.png").convert("RGB")).astype(float) / 255) @ [0.2126, 0.7152, 0.0722]
H, W = V.shape
c = V[int(3 * H / 8):int(5 * H / 8), int(3 * W / 8):int(5 * W / 8)]
print(f"D4:E5 max {c.max():.2f}, brightest twentieth {np.sort(c.ravel())[-max(1, c.size // 20):].mean():.2f}, pixels over 0.55: {(c > 0.55).sum()}")
