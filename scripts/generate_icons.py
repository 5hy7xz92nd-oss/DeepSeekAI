#!/usr/bin/env python3
"""
Generate original FloatAI icons (floating-window + chat-bubble motif).
Replaces the previous whale icon to resolve the Chrome Web Store
impersonation rejection (Violation ref: Red Nickel).

Design:
  - Rounded square background with a purple -> teal gradient (distinct from
    DeepSeek's brand blue).
  - A white floating-window card in the center with a title-bar dot row.
  - A speech bubble overlapping the card, conveying "chat".

Outputs: icon16/24/32/48/128.png and app-logo.png (256) in src/icons/.
"""
import math
import os
from PIL import Image, ImageDraw

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "src", "icons")


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient_bg(size):
    """Diagonal purple -> teal gradient."""
    top_left = (124, 77, 255)   # vivid violet
    bot_right = (13, 148, 136)  # teal-600
    img = Image.new("RGB", (size, size), top_left)
    px = img.load()
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * (size - 1))
            px[x, y] = lerp(top_left, bot_right, t)
    return img


def rounded_rect_mask(size, radius):
    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    return mask


def draw_icon(size):
    """Render the FloatAI icon at the given pixel size."""
    s = size
    img = gradient_bg(s).convert("RGBA")
    # round the corners of the background for a squircle look
    bg_mask = rounded_rect_mask(s, int(s * 0.22))
    transparent = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    img = Image.composite(img, transparent, bg_mask)

    d = ImageDraw.Draw(img)

    # Floating window card (centered, slightly upper area)
    pad = s * 0.24
    card_x0, card_y0 = pad, s * 0.26
    card_x1, card_y1 = s - pad, s * 0.66
    card_r = int(s * 0.08)
    # card shadow (subtle)
    sh_off = max(1, int(s * 0.03))
    d.rounded_rectangle(
        [card_x0 + sh_off, card_y0 + sh_off, card_x1 + sh_off, card_y1 + sh_off],
        radius=card_r, fill=(0, 0, 0, 70),
    )
    d.rounded_rectangle(
        [card_x0, card_y0, card_x1, card_y1],
        radius=card_r, fill=(255, 255, 255, 255),
    )
    # title bar dots on the card
    dot_r = max(1, int(s * 0.018))
    dot_y = card_y0 + (card_y1 - card_y0) * 0.18
    for i, frac in enumerate([0.33, 0.46, 0.59]):
        cx = card_x0 + (card_x1 - card_x0) * frac
        color = [(255, 184, 77), (124, 77, 255), (13, 148, 136)][i]
        d.ellipse([cx - dot_r, dot_y - dot_r, cx + dot_r, dot_y + dot_r], fill=color)

    # Speech bubble overlapping the lower-right of the card
    bub_x0, bub_y0 = s * 0.40, s * 0.50
    bub_x1, bub_y1 = s * 0.82, s * 0.80
    bub_r = int(s * 0.10)
    d.rounded_rectangle(
        [bub_x0, bub_y0, bub_x1, bub_y1],
        radius=bub_r, fill=(124, 77, 255, 255),
    )
    # bubble tail
    tail = [
        (bub_x0 + (bub_x1 - bub_x0) * 0.18, bub_y1 - 1),
        (bub_x0 + (bub_x1 - bub_x0) * 0.10, bub_y1 + s * 0.10),
        (bub_x0 + (bub_x1 - bub_x0) * 0.38, bub_y1 - 1),
    ]
    d.polygon(tail, fill=(124, 77, 255, 255))
    # three dots inside bubble
    br = max(1, int(s * 0.022))
    by = (bub_y0 + bub_y1) / 2
    for frac in [0.30, 0.50, 0.70]:
        bx = bub_x0 + (bub_x1 - bub_x0) * frac
        d.ellipse([bx - br, by - br, bx + br, by + br], fill=(255, 255, 255, 255))

    return img


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    sizes = {
        "icon16.png": 16,
        "icon24.png": 24,
        "icon32.png": 32,
        "icon48.png": 48,
        "icon128.png": 128,
        "app-logo.png": 256,
    }
    for name, size in sizes.items():
        img = draw_icon(size)
        path = os.path.join(OUT_DIR, name)
        img.save(path, "PNG")
        print(f"wrote {path} ({size}x{size})")


if __name__ == "__main__":
    main()
