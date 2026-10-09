# stundenrechnen.com

Static German time & working-hours calculator site (AdSense).

- Site files live at the repo root and deploy straight into Cloudways `public_html` via git pull.
- Generator: `_build/` (`python3 _build/build.py` writes to `dist/`; copy `dist/*` to repo root before committing).
- `/_build/` is blocked from public access in `.htaccess`.
