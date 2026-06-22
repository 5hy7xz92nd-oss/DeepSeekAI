#!/usr/bin/env python3
"""
Process the user-supplied icon1.png into the full set of extension icons.
Replaces the temporary script-generated icons.

Input:  src/icons/icon1.png  (1254x1254, full-bleed gradient square)
Output: src/icons/icon{16,24,32,48,128}.png and app-logo.png (256)

Notes:
  - Uses LANCZOS for high-quality downscaling.
  - The source has a thin blue outline on the speech bubble; at 16/24px it
    may blur. We do NOT draw extra shapes — we preserve the user's artwork.
"""
import os
from PIL import Image

SRC = os.path.join(os.path.dirname(__file__), "..", "src", "icons", "icon1.png")
OUT_DIR = os.path.dirname(SRC)

SIZES = {
    "icon16.png": 16,
    "icon24.png": 24,
    "icon32.png": 32,
    "icon48.png": 48,
    "icon128.png": 128,
    "app-logo.png": 256,
}


def main():
    src = Image.open(SRC).convert("RGBA")
    assert src.size[0] == src.size[1], f"source must be square, got {src.size}"
    print(f"source: {src.size[0]}x{src.size[1]}")

    for name, size in SIZES.items():
        # For very small sizes, scale down in two steps for sharper result.
        img = src
        if size < 64 and src.size[0] > 4 * size:
            mid = src.resize((size * 2, size * 2), Image.LANCZOS)
            img = mid.resize((size, size), Image.LANCZOS)
        else:
            img = src.resize((size, size), Image.LANCZOS)
        path = os.path.join(OUT_DIR, name)
        img.save(path, "PNG", optimize=True)
        print(f"wrote {path} ({size}x{size})")


if __name__ == "__main__":
    main()
