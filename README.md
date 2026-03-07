# c4web

Arabic RTL redesign starter for `connect4systems.com`.

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

## Planning Docs

- `docs/redesign-backlog-ar-rtl.md`: Full rollout backlog and template mapping
- `docs/sitemap-links.txt`: Export of all current sitemap links (`128` URLs)
- `docs/redirect-seed.csv`: Initial redirect map for legacy/malformed URLs

## Quick Preview

1. Open `prototype/index.html` in VS Code and run with Live Server or open directly in browser.
2. Navigate to the other prototype pages through the top menu.
3. Review typography, RTL layout behavior, and interaction patterns on mobile + desktop widths.

## Next Implementation Step

Map each live URL to one of the six templates, then port these templates into the active Frappe website theme layer while applying redirects from `docs/redirect-seed.csv`.