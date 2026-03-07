# c4web

Arabic RTL redesign starter for `connect4systems.com`.

This repository now includes a valid **Frappe app scaffold** so it can be installed via `bench get-app`.

## What Is Included

- `prototype/index.html`: Modern interactive homepage (Template A)
- `prototype/solution-template.html`: Reusable solution page (Template B)
- `prototype/catalog.html`: Products/shop page (Template C)
- `prototype/about.html`: About/company page (Template D)
- `prototype/contact.html`: Contact/conversion page (Template D)
- `prototype/blog-list.html`: Blog category page (Template E)
- `prototype/blog-post.html`: Blog detail page (Template F)
- `prototype/assets/css/style.css`: Shared Arabic RTL design system
- `prototype/assets/js/app.js`: Shared interactions (menu, reveal, counters, tabs, accordion)
- `setup.py`, `MANIFEST.in`, `requirements.txt`: Bench/Python packaging files
- `c4web/hooks.py`, `c4web/modules.txt`, `c4web/config/desktop.py`: Frappe app core files
- `c4web/public/css/style.css`, `c4web/public/js/app.js`: App assets served under `/assets/c4web/...`
- `c4web/www/*.html`: Website pages served by Frappe routes

## Planning Docs

- `docs/redesign-backlog-ar-rtl.md`: Full rollout backlog and template mapping
- `docs/sitemap-links.txt`: Export of all current sitemap links (`128` URLs)
- `docs/redirect-seed.csv`: Initial redirect map for legacy/malformed URLs

## Quick Preview

1. Open `prototype/index.html` in VS Code and run with Live Server or open directly in browser.
2. Navigate to the other prototype pages through the top menu.
3. Review typography, RTL layout behavior, and interaction patterns on mobile + desktop widths.

## Bench Install

Use these commands on your Frappe server:

```bash
cd ~/frappe-bench

# If a failed clone already exists, remove it first
rm -rf apps/c4web

bench get-app https://github.com/Connect4systems/c4web
bench --site <your-site-name> install-app c4web
bench build
bench clear-cache
bench restart
```

If your bench version is old, update it first (recommended):

```bash
pip install --upgrade frappe-bench
```

## Next Implementation Step

Map each live URL to one of the six templates, then port these templates into the active Frappe website theme layer while applying redirects from `docs/redirect-seed.csv`.