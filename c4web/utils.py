import frappe


def update_website_context(context):
    """Inject shared website context values used by static templates."""
    website_logo = frappe.get_cached_value("Website Settings", "Website Settings", "app_logo")

    # Use Website Settings logo first, then fall back to known public assets.
    context.c4_logo_url = website_logo or "/files/logo.png"
    context.c4_logo_fallback_url = "/files/logo-02.png"
