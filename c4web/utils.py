import re

import frappe


_SRC_RE = re.compile(r"src=['\"]([^'\"]+)['\"]", re.IGNORECASE)


def _extract_logo_from_brand_html(brand_html):
    if not brand_html:
        return ""
    match = _SRC_RE.search(brand_html)
    return match.group(1).strip() if match else ""


def update_website_context(context):
    """Inject shared website context values used by static templates."""
    settings = frappe.get_cached_doc("Website Settings", "Website Settings")

    website_logo = (
        (settings.get("brand_image") or "").strip()
        or (settings.get("app_logo") or "").strip()
        or _extract_logo_from_brand_html(settings.get("brand_html"))
    )

    # Use Website Settings logo first, then fall back to known public assets.
    context.c4_logo_url = website_logo or "/files/logo-erp.png"
    context.c4_logo_fallback_url = "/files/logo.png"
