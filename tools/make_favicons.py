"""Generate theme-aware favicon assets from single-four.png (white-on-transparent).

Outputs:
  single-four-dark.png  -> dark glyph for LIGHT browser chrome (recolored, alpha kept)
  apple-touch-icon.png  -> 180x180, solid void bg + white glyph (iOS has no transparency)
"""
from PIL import Image

SRC = r"C:\Users\Chris\444-linksite\single-four.png"
OUT_DARK = r"C:\Users\Chris\444-linksite\single-four-dark.png"
OUT_APPLE = r"C:\Users\Chris\444-linksite\apple-touch-icon.png"

MIDNIGHT = (26, 35, 50)   # #1A2332  — dark glyph for light UI
VOID = (12, 17, 24)       # #0c1118  — apple-touch background

src = Image.open(SRC).convert("RGBA")
alpha = src.getchannel("A")

# --- dark variant: solid midnight fill, original alpha ---
dark = Image.new("RGBA", src.size, MIDNIGHT + (0,))
dark.putalpha(alpha)
dark.save(OUT_DARK)

# --- apple-touch-icon: white glyph on solid void, padded, square 180 ---
white = Image.new("RGBA", src.size, (255, 255, 255, 0))
white.putalpha(alpha)

side = max(src.size)
pad = int(side * 0.18)
canvas = Image.new("RGBA", (side, side), VOID + (255,))
# center the (possibly non-square) glyph
ox = (side - src.size[0]) // 2
oy = (side - src.size[1]) // 2
canvas.alpha_composite(white, (ox, oy))
# pad by shrinking glyph: redo with padding for breathing room
canvas = Image.new("RGBA", (side, side), VOID + (255,))
target = side - 2 * pad
gw, gh = src.size
scale = min(target / gw, target / gh)
nw, nh = int(gw * scale), int(gh * scale)
glyph = white.resize((nw, nh), Image.LANCZOS)
canvas.alpha_composite(glyph, ((side - nw) // 2, (side - nh) // 2))
canvas.resize((180, 180), Image.LANCZOS).save(OUT_APPLE)

print("wrote", OUT_DARK)
print("wrote", OUT_APPLE)
