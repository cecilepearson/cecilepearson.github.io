#!/usr/bin/env python3
"""Download the latin Poppins woff2 faces so fonts are self-hosted (no runtime
request to Google Fonts). Writes assets/fonts/poppins/poppins-<weight>.woff2."""
import os, re, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets", "fonts", "poppins")
os.makedirs(OUT, exist_ok=True)

CSS_URL = "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap"
# A modern-browser UA makes Google return woff2 (vs older ttf).
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


css = get(CSS_URL).decode("utf-8")
# Split into @font-face blocks, keep only the latin subset of each weight.
blocks = re.findall(r"/\*\s*(\S+)\s*\*/\s*@font-face\s*{([^}]*)}", css)
saved = {}
for subset, body in blocks:
    if subset != "latin":
        continue
    weight = re.search(r"font-weight:\s*(\d+)", body)
    url = re.search(r"url\((https://[^)]+\.woff2)\)", body)
    if not (weight and url):
        continue
    w = weight.group(1)
    dest = os.path.join(OUT, f"poppins-{w}.woff2")
    with open(dest, "wb") as f:
        f.write(get(url.group(1)))
    saved[w] = os.path.getsize(dest)

for w in ("300", "400", "500", "600"):
    if w in saved:
        print(f"poppins-{w}.woff2  {saved[w]/1024:.0f} KB")
    else:
        print(f"poppins-{w}.woff2  MISSING")
print(f"-> {OUT}")
