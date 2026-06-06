# cecilepearson.github.io

The portfolio site for painter **Cecile Pearson**, served via GitHub Pages at
<https://cecilepearson.github.io>. A hand-built Jekyll site — no Wix, no theme,
no tracking. The 35 works live in one data file and the gallery is generated from it.

## How it deploys

GitHub Pages builds this site from the `main` branch and publishes it on every
push. **One-time setup:** in the repo on GitHub go to **Settings → Pages → Build
and deployment → Source** and choose **Deploy from a branch**, branch `main`,
folder `/ (root)`.

(The code is also compatible with a Jekyll 4 GitHub Actions pipeline if you ever
prefer that — it just needs a token with the `workflow` scope to commit a
workflow file.)

## Run it locally

```sh
bundle install
bundle exec jekyll serve
# open http://localhost:4000
```

## Project layout

```
_data/works.yml        # the 35 works (order, title, year, medium, dimensions, series)
_data/dimensions.yml   # AUTO-GENERATED pixel sizes/orientation — do not edit
_data/nav.yml          # top navigation
_layouts/ _includes/   # page shell, nav, footer, gallery figure
assets/css/main.scss   # all styles (one file)
assets/js/site.js      # accessible lightbox
assets/img/works/      # optimized webp + jpg derivatives (committed)
cv/                    # CV PDF
scripts/               # image pipeline (build-time only; not served)
```

## Adding or changing a painting

1. Drop the full-resolution original into `scripts/_originals/` named
   `NN-slug.jpg` (e.g. `36-new-piece.jpg`), matching the order number.
2. Add the slug to the list in `scripts/_works.py` and an entry in
   `_data/works.yml` (title, year, medium, dimensions, and `series` if it
   belongs to a group).
3. Regenerate images (needs Python 3 + Pillow):
   ```sh
   PYTHONPATH=scripts python3 scripts/build_images.py
   ```
   This writes the optimized images into `assets/img/works/` and updates
   `_data/dimensions.yml` (pixel size + portrait/landscape) automatically.
4. Commit and push to `main`.

To edit a caption, just change `_data/works.yml`. To reorder works, change their
`order` and reorder the list.

## Image sourcing & notes

- `scripts/fetch_originals.py` pulls full-resolution originals from the Wix CDN.
  The originals live only in `scripts/_originals/` (gitignored); keep a backup —
  the committed derivatives can't be re-enlarged.
- Three works were uploaded to Wix at low resolution and will look soft when
  zoomed: **Bougainvillea**, **Thorn 3**, **Pew Back**. Re-supply higher-res
  files (steps above) when available.
- Fonts (Poppins) are self-hosted in `assets/fonts/`; re-fetch with
  `scripts/fetch_fonts.py` if needed.
