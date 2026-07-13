# Long Reach Marlins website

This repository contains the static website source for Long Reach Marlins, Inc. All site files are under `src/`.

Shared page markup lives in `templates/base.html`, while page-specific content lives in `templates/pages/`.
Run `py -3 scripts/build_pages.py` after editing a template to regenerate the deployable HTML files under `src/`.
The local server and GitHub Pages workflow run this build automatically.
