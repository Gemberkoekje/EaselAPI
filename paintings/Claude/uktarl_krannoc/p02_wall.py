"""The wall, then the carved rays on it.

The wall goes down in a bristle, a few degrees off the frame so its passes are not a stack
of bands. Each ray is one wide flat stroke held to its own wedge, laid from the sun
outward and lifting off as it goes: a chisel's pressure changes its paint and not its
width, so the gilding thins away from the lamp without a second mark.
"""

s.block_in(wall, "bristle", "wall", size=0.12, density=0.85, direction=-4)

RAY_MIX = ["ray", "ray_hi", "ray", "ray_lo", "ray_hi", "ray", "ray_hi", "ray_lo", "ray",
           "ray_hi", "ray_lo", "ray", "ray_lo"]
for (ang, half), shape, mix in zip(RAYS, rays, RAY_MIX):
    a = math.radians(ang)
    reach = 1250
    pts = [(SUN[0] + r * math.cos(a), SUN[1] - r * math.sin(a)) for r in (46, 420, reach)]
    width = 2 * reach * math.tan(math.radians(half)) / CW + 0.01
    s.stroke(px_pts(pts), "flat", mix, size=min(width, 0.16), clip=shape, solid=True,
             pressure=[1.0, 0.8, 0.4], note="ray")
