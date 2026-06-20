"""Compose the OG/rich-embed image: captured relic backdrop + centered 444 wordmark."""
from PIL import Image, ImageFilter

BG = r"C:\Users\Chris\444-linksite\tools\bg-frame.png"
WM = r"C:\Users\Chris\444-linksite\wordmark.png"
OUT = r"C:\Users\Chris\444-linksite\og-image.png"

W, H = 1200, 630
bg = Image.open(BG).convert("RGBA")
if bg.size != (W, H):
    bg = bg.resize((W, H), Image.LANCZOS)

# Center scrim — radial darkening so the white wordmark reads over bright chrome.
scrim = Image.new("L", (W, H), 0)
import math
cx, cy = W / 2, H / 2
maxd = math.hypot(cx, cy)
px = scrim.load()
for y in range(H):
    for x in range(W):
        d = math.hypot(x - cx, y - cy) / maxd
        # darkest at center, fading out
        v = int(150 * max(0.0, 1.0 - d * 1.15))
        px[x, y] = v
black = Image.new("RGBA", (W, H), (4, 7, 12, 0))
black.putalpha(scrim)
bg = Image.alpha_composite(bg, black)

# Wordmark, ~60% width, centered.
wm = Image.open(WM).convert("RGBA")
tw = int(W * 0.60)
th = int(tw * wm.size[1] / wm.size[0])
wm = wm.resize((tw, th), Image.LANCZOS)
ox, oy = (W - tw) // 2, (H - th) // 2

# Soft dark glow behind the mark for separation.
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
glow.paste(wm, (ox, oy), wm)
glow = glow.filter(ImageFilter.GaussianBlur(14))
# darken the glow to a shadow
r, g, b, a = glow.split()
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
shadow.putalpha(a.point(lambda v: int(v * 0.9)))
bg = Image.alpha_composite(bg, shadow)

# The wordmark itself.
layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
layer.paste(wm, (ox, oy), wm)
bg = Image.alpha_composite(bg, layer)

bg.convert("RGB").save(OUT, quality=92)
print("wrote", OUT, bg.size)
