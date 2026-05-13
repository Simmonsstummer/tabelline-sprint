"""Generate app icons: x with lightning bolt on gradient background."""
from PIL import Image, ImageDraw
import numpy as np
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent

PINK = np.array([255, 61, 138], dtype=np.float32)
PURPLE = np.array([139, 92, 246], dtype=np.float32)
BLUE = np.array([58, 163, 255], dtype=np.float32)

DARK = (26, 26, 46, 255)
WHITE = (255, 255, 255, 255)
YELLOW = (255, 200, 69, 255)


def make_gradient(size):
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    t = (xx + yy) / (2 * (size - 1))

    arr = np.zeros((size, size, 3), dtype=np.float32)
    m1 = t < 0.5
    m2 = ~m1
    t1 = (t[m1] * 2)[:, None]
    arr[m1] = PINK * (1 - t1) + PURPLE * t1
    t2 = ((t[m2] - 0.5) * 2)[:, None]
    arr[m2] = PURPLE * (1 - t2) + BLUE * t2

    arr = np.clip(arr, 0, 255).astype(np.uint8)
    rgba = np.dstack([arr, np.full((size, size), 255, dtype=np.uint8)])
    return Image.fromarray(rgba, "RGBA")


def draw_x(draw, cx, cy, half, color, w):
    p1 = (cx - half, cy - half)
    p2 = (cx + half, cy + half)
    p3 = (cx - half, cy + half)
    p4 = (cx + half, cy - half)
    draw.line([p1, p2], fill=color, width=w)
    draw.line([p3, p4], fill=color, width=w)
    r = w // 2
    for (px, py) in [p1, p2, p3, p4]:
        draw.ellipse([px - r, py - r, px + r, py + r], fill=color)


def make_icon(size, with_bolt=True):
    img = make_gradient(size)
    draw = ImageDraw.Draw(img)

    cx, cy = size // 2, int(size * 0.54)
    half = int(size * 0.27)
    stroke = max(4, int(size * 0.13))
    outline_extra = max(2, int(size * 0.025))

    draw_x(draw, cx, cy, half, DARK, stroke + outline_extra)
    draw_x(draw, cx, cy, half, WHITE, stroke)

    if with_bolt:
        bolt_cx = int(size * 0.78)
        bolt_cy = int(size * 0.22)
        bw = int(size * 0.16)
        bh = int(size * 0.22)

        pts = [
            (bolt_cx + bw * 0.10, bolt_cy - bh * 0.50),
            (bolt_cx - bw * 0.55, bolt_cy + bh * 0.10),
            (bolt_cx - bw * 0.10, bolt_cy + bh * 0.10),
            (bolt_cx - bw * 0.30, bolt_cy + bh * 0.50),
            (bolt_cx + bw * 0.55, bolt_cy - bh * 0.10),
            (bolt_cx + bw * 0.10, bolt_cy - bh * 0.10),
        ]
        pts = [(int(x), int(y)) for x, y in pts]

        outline_w = max(3, int(size * 0.025))

        edges = list(zip(pts, pts[1:] + [pts[0]]))
        for (p1, p2) in edges:
            draw.line([p1, p2], fill=DARK, width=outline_w * 2)
        for (px, py) in pts:
            r = outline_w
            draw.ellipse([px - r, py - r, px + r, py + r], fill=DARK)

        draw.polygon(pts, fill=YELLOW)

    return img


def main():
    for name, sz in [("icon-512.png", 512), ("icon-192.png", 192), ("icon-180.png", 180)]:
        img = make_icon(sz)
        img.save(OUT_DIR / name, optimize=True)
        print(f"Wrote {name} ({sz}x{sz})")

    # Favicon: render at 48 native, save as multi-res ICO
    fav = make_icon(48)
    fav.save(OUT_DIR / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    print("Wrote favicon.ico (16/32/48)")


if __name__ == "__main__":
    main()
