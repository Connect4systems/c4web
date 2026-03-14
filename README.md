# c4web

Full Arabic RTL redesign for `connect4systems.com` as an installable Frappe app.

This repository now contains the **Phase 2 full version**:
- Professional interactive frontend
- Rewritten Arabic content
- Sector pages for trade, retail, CRM, factory, and HR
- AI-first brand positioning (`80%` AI-enabled team workflow)
- Legacy URL route mapping for key old pages

## App Structure

- `c4web/public/css/style.css`: Shared design system (RTL, responsive, interactive)
- `c4web/public/js/app.js`: Shared behavior (menu, reveal, counters, tabs, filters, accordion)
- `c4web/www/index.html`: New homepage
- `c4web/www/solution-template.html`: Solutions hub
- `c4web/www/trade.html`: Trade sector page
- `c4web/www/retail-system.html`: Retail sector page
- `c4web/www/crm.html`: CRM sector page
- `c4web/www/factory.html`: Factory sector page
- `c4web/www/hr.html`: HR sector page
- `c4web/www/catalog.html`: Packages + full verified media gallery
- `c4web/www/blog-list.html`: Blog listing with filters
- `c4web/www/blog-post.html`: Featured article page
- `c4web/www/about.html`: Company profile page
- `c4web/www/contact.html`: Conversion-focused contact page
- `c4web/hooks.py`: App metadata + route rules from legacy URLs to new pages

## Planning And Inventory Docs

- `docs/redesign-backlog-ar-rtl.md`: rollout backlog
- `docs/sitemap-links.txt`: sitemap export
- `docs/redirect-seed.csv`: redirect seed map
- `docs/image-inventory-verified.txt`: verified image URLs used in the redesign

## Bench Install (first time)

```bash
cd ~/frappe-bench

# If needed, remove old app clone first
rm -rf apps/c4web

bench get-app https://github.com/Connect4systems/c4web
bench --site <your-site-name> install-app c4web
bench --site <your-site-name> migrate
bench build
bench clear-cache
bench --site <your-site-name> clear-website-cache
bench restart
```

## Updating the Site (pulling latest changes)

### Normal update (app was cloned with `bench get-app`)

```bash
cd ~/frappe-bench/apps/c4web
git pull origin main

cd ~/frappe-bench
bench --site <your-site-name> clear-cache
bench --site <your-site-name> clear-website-cache
bench build --app c4web
bench restart
```

### Fix: `fatal: 'origin' does not appear to be a git repository`

This error means the remote URL was never configured (or the app was copied manually instead of cloned). Run the following to add the remote and then pull:

```bash
cd ~/frappe-bench/apps/c4web

# Check current remotes (may be empty)
git remote -v

# Add the GitHub remote
git remote add origin https://github.com/Connect4systems/c4web.git

# Fetch and pull the latest code
git fetch origin
git pull origin main

# Back to bench root – clear cache and restart
cd ~/frappe-bench
bench --site <your-site-name> clear-cache
bench --site <your-site-name> clear-website-cache
bench build --app c4web
bench restart
```

### Fix: directory is not a git repository at all

If `apps/c4web` was extracted from a zip or copied manually it has no `.git` folder. The safest fix is a clean re-install:

```bash
cd ~/frappe-bench

# Remove the manually-copied directory
rm -rf apps/c4web

# Re-clone via bench (this is the `bench get-app` command you may remember)
bench get-app https://github.com/Connect4systems/c4web.git

# No need to re-run install-app if the site already has c4web installed
bench --site <your-site-name> clear-cache
bench --site <your-site-name> clear-website-cache
bench build --app c4web
bench restart
```

## Development Notes

- All pages are authored with `lang="ar" dir="rtl"`.
- Legacy links like `/home`, `/all-products`, `/retais-erp`, `/hr2`, and key `/blog/*` category routes are mapped in `c4web/hooks.py`.
- The catalog page includes the full verified image set to satisfy the full-asset usage requirement.
