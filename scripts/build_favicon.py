#!/usr/bin/env python3
"""Generate the favicon set from scripts/favicon-source.jpg (a detail of one of
Cecile's paintings). Run: PYTHONPATH=scripts python3 scripts/build_favicon.py"""
import os
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, "favicon-source.jpg")
META = os.path.join(ROOT, "assets", "img", "meta")
os.makedirs(META, exist_ok=True)

im = ImageOps.exif_transpose(Image.open(SRC)).convert("RGB")
w, h = im.size
if w != h:  # center-crop to square if needed
    s = min(w, h)
    im = im.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))

im.save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
im.resize((32, 32), Image.LANCZOS).save(os.path.join(META, "favicon-32.png"))
im.resize((180, 180), Image.LANCZOS).save(os.path.join(META, "apple-touch-icon.png"))
print("Wrote favicon.ico, assets/img/meta/favicon-32.png, assets/img/meta/apple-touch-icon.png")
