# Standard Web Page Migration

Use this before uninstalling the `c4web` app from the live Frappe site.

The migration creates editable **Website > Web Page** records from the root HTML files and uploads the local image assets as public `/files/...` records. The generated pages include the same CSS and JavaScript behavior inline, so the routes do not depend on `c4web/public` after the app is removed.

Run from the bench folder:

```bash
bench --site connect4systems.com execute c4web.standard_pages.install_standard_web_pages
bench --site connect4systems.com clear-cache
```

Expected result:

```python
{
    "ok": True,
    "count": 26,
    "routes": ["/", "about", "catalog", "..."]
}
```

After the command succeeds, open the site pages from **Website > Web Page** and confirm the routes are published before uninstalling the app.

