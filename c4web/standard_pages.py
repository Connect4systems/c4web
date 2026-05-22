from pathlib import Path
import re

import frappe
from frappe.utils.file_manager import save_file


APP_ROOT = Path(__file__).resolve().parent.parent
SITE_ASSET_DIR = APP_ROOT / "assets" / "images" / "site"
CSS_PATH = APP_ROOT / "assets" / "css" / "style.css"
JS_PATH = APP_ROOT / "assets" / "js" / "app.js"

HTML_TITLE_RE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)
META_DESCRIPTION_RE = re.compile(
    r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']',
    re.IGNORECASE,
)
HEAD_RE = re.compile(r"<head[^>]*>(.*?)</head>", re.IGNORECASE | re.DOTALL)
BODY_RE = re.compile(r"<body[^>]*>(.*?)</body>", re.IGNORECASE | re.DOTALL)
SCRIPT_LINK_RE = re.compile(
    r'\s*<link\s+rel=["\']stylesheet["\']\s+href=["\']/assets/css/style\.css["\']\s*/?>'
    r'|\s*<script\s+defer\s+src=["\']/assets/js/app\.js["\']></script>',
    re.IGNORECASE,
)


def _clean_text(value):
    return re.sub(r"\s+", " ", value or "").strip()


def _page_route(path):
    return "index" if path.name == "index.html" else path.stem


def _field_exists(meta, fieldname):
    return bool(meta.get_field(fieldname))


def _extract_title(html, fallback):
    match = HTML_TITLE_RE.search(html)
    return _clean_text(match.group(1)) if match else fallback


def _extract_meta_description(html):
    match = META_DESCRIPTION_RE.search(html)
    return _clean_text(match.group(1)) if match else ""


def _extract_head_extras(html):
    match = HEAD_RE.search(html)
    if not match:
        return ""

    head = SCRIPT_LINK_RE.sub("", match.group(1))
    # Keep SEO, schema, canonical, and tracking tags with the Web Page content.
    return _clean_text(head)


def _extract_body(html):
    match = BODY_RE.search(html)
    return match.group(1).strip() if match else html.strip()


def _ensure_public_file(source_path):
    file_name = f"c4web-site-{source_path.name}"

    existing = frappe.db.exists("File", {"file_name": file_name, "is_private": 0})
    if existing:
        return frappe.db.get_value("File", existing, "file_url")

    content = source_path.read_bytes()
    file_doc = save_file(file_name, content, None, None, is_private=0)
    return file_doc.file_url


def _asset_url_map():
    url_map = {}
    if not SITE_ASSET_DIR.exists():
        return url_map

    for asset in SITE_ASSET_DIR.iterdir():
        if asset.is_file():
            url_map[f"/assets/images/site/{asset.name}"] = _ensure_public_file(asset)

    return url_map


def _rewrite_asset_urls(html, url_map):
    for old, new in url_map.items():
        html = html.replace(old, new)
    return html


def _rewrite_internal_links(html):
    for page_path in sorted(APP_ROOT.glob("*.html")):
        route = _page_route(page_path)
        href = "/" if route == "index" else f"/{route}"
        html = html.replace(f'href="{page_path.name}"', f'href="{href}"')
        html = html.replace(f"href='{page_path.name}'", f"href='{href}'")
    return html


def _build_page_content(html, url_map):
    head_extras = _rewrite_asset_urls(_extract_head_extras(html), url_map)
    body = _rewrite_asset_urls(_extract_body(html), url_map)
    css = CSS_PATH.read_text(encoding="utf-8", errors="ignore") if CSS_PATH.exists() else ""
    js = JS_PATH.read_text(encoding="utf-8", errors="ignore") if JS_PATH.exists() else ""
    css = _rewrite_asset_urls(css, url_map)
    js = _rewrite_asset_urls(js, url_map)
    head_extras = _rewrite_internal_links(head_extras)
    body = _rewrite_internal_links(body)
    js = _rewrite_internal_links(js)

    blocks = []
    if head_extras:
        blocks.append(head_extras)
    if css:
        blocks.append(f"<style>\n{css}\n</style>")
    blocks.append(body)
    if js:
        blocks.append(f"<script>\n{js}\n</script>")
    return "\n".join(blocks)


def _find_existing_web_page(route):
    if frappe.db.exists("Web Page", {"route": route}):
        return frappe.get_doc("Web Page", {"route": route})
    return None


def _set_home_page(route):
    if route != "index" or not frappe.db.exists("Website Settings", "Website Settings"):
        return

    settings = frappe.get_doc("Website Settings", "Website Settings")
    if hasattr(settings, "home_page"):
        settings.home_page = "index"
        settings.save(ignore_permissions=True)


def _set_if_field(doc, meta, fieldname, value):
    if _field_exists(meta, fieldname):
        doc.set(fieldname, value)


@frappe.whitelist()
def install_standard_web_pages():
    """Create/update editable Website > Web Page records from the static site files."""
    meta = frappe.get_meta("Web Page")
    url_map = _asset_url_map()
    installed = []

    for html_path in sorted(APP_ROOT.glob("*.html")):
        html = html_path.read_text(encoding="utf-8", errors="ignore")
        route = _page_route(html_path)
        title = _extract_title(html, html_path.stem.replace("-", " ").title())
        content = _build_page_content(html, url_map)

        doc = _find_existing_web_page(route)
        if doc is None:
            doc = frappe.new_doc("Web Page")
            _set_if_field(doc, meta, "route", route)

        _set_if_field(doc, meta, "title", title)
        _set_if_field(doc, meta, "published", 1)
        _set_if_field(doc, meta, "content_type", "HTML")
        _set_if_field(doc, meta, "main_section", content)
        _set_if_field(doc, meta, "main_section_html", content)
        _set_if_field(doc, meta, "html", content)
        _set_if_field(doc, meta, "meta_title", title)

        description = _extract_meta_description(html)
        if description:
            _set_if_field(doc, meta, "meta_description", description)

        doc.flags.ignore_permissions = True
        doc.save(ignore_permissions=True)
        _set_home_page(route)
        installed.append("/" if route == "index" else route)

    frappe.db.commit()
    return {"ok": True, "count": len(installed), "routes": installed}
