#!/usr/bin/env python3
"""Download full-resolution originals (35 works + ABOUT portrait) from the Wix CDN
into scripts/_originals/ (gitignored). The committed site never touches Wix; this
folder is the local master backup. Re-running is safe (skips already-downloaded)."""
import json, os, sys, urllib.request
from _works import SLUGS, PORTRAIT_MEDIA_ID

HERE = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(HERE, "_originals")
os.makedirs(ORIG, exist_ok=True)

manifest = json.load(open(os.path.join(HERE, "gallery_manifest.json")))
by_order = {e["order"]: e for e in manifest}


def download(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return os.path.getsize(dest), "cached"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    with open(dest, "wb") as f:
        f.write(data)
    return len(data), "downloaded"


def ext_for(url):
    u = url.lower()
    if u.endswith("jpeg"):
        return ".jpeg"
    if u.endswith("png"):
        return ".png"
    return ".jpg"


total = 0
errors = 0
for i, slug in enumerate(SLUGS, start=1):
    entry = by_order.get(i)
    if not entry:
        print(f"!! no manifest entry for order {i} ({slug})")
        errors += 1
        continue
    url = entry["original_url"]
    dest = os.path.join(ORIG, f"{i:02d}-{slug}{ext_for(url)}")
    try:
        size, status = download(url, dest)
        total += size
        print(f"{i:02d}  {slug:34}  {status:10}  {size/1024:8.0f} KB")
    except Exception as e:
        print(f"{i:02d}  {slug:34}  ERROR  {e}")
        errors += 1

# ABOUT portrait
purl = f"https://static.wixstatic.com/media/{PORTRAIT_MEDIA_ID}"
try:
    psize, pstatus = download(purl, os.path.join(ORIG, "portrait.jpg"))
    total += psize
    print(f"--  portrait{'':28}  {pstatus:10}  {psize/1024:8.0f} KB")
except Exception as e:
    print(f"--  portrait  ERROR  {e}  (supply scripts/_originals/portrait.jpg manually)")
    errors += 1

print(f"\nTOTAL: {total/1024/1024:.1f} MB  ->  {ORIG}")
if errors:
    print(f"WARNING: {errors} item(s) failed.")
    sys.exit(1)
