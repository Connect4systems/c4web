import frappe
from frappe import _


def _clean_text(value, max_len=0):
    text = (value or "").strip()
    if max_len and len(text) > max_len:
        return text[:max_len]
    return text


@frappe.whitelist(allow_guest=True)
def create_website_lead():
    """Create a Lead from the public website contact form."""
    request_json = {}
    if hasattr(frappe.request, "get_json"):
        request_json = frappe.request.get_json(silent=True) or {}

    form_dict = frappe.local.form_dict or {}
    data = frappe._dict({**request_json, **form_dict})

    full_name = _clean_text(data.get("name"), 140)
    company = _clean_text(data.get("company"), 140)
    phone = _clean_text(data.get("phone"), 80)
    email = _clean_text(data.get("email"), 140)
    sector = _clean_text(data.get("sector"), 140)
    scope = _clean_text(data.get("scope"), 140)
    message = _clean_text(data.get("message"), 2000)
    source_page = _clean_text(data.get("source_page"), 255) or _clean_text(getattr(frappe.request, "path", ""), 255)

    if not full_name:
        frappe.throw(_("يرجى إدخال الاسم الكامل"), frappe.ValidationError)
    if not email:
        frappe.throw(_("يرجى إدخال البريد الإلكتروني"), frappe.ValidationError)
    if not phone:
        frappe.throw(_("يرجى إدخال رقم الجوال"), frappe.ValidationError)

    if not frappe.utils.validate_email_address(email, throw=False):
        frappe.throw(_("البريد الإلكتروني غير صالح"), frappe.ValidationError)

    extra_notes = []
    if sector and "اختر" not in sector:
        extra_notes.append(f"Sector: {sector}")
    if scope and "اختر" not in scope:
        extra_notes.append(f"Need: {scope}")
    if source_page:
        extra_notes.append(f"Source Page: {source_page}")
    if message:
        extra_notes.append(f"Message: {message}")

    lead_data = {
        "doctype": "Lead",
        "lead_name": full_name,
        "company_name": company or None,
        "email_id": email,
        "mobile_no": phone,
        "source": "Website",
        "status": "Lead",
    }

    notes_text = "\n".join(extra_notes)
    lead_meta = frappe.get_meta("Lead")
    if notes_text:
        if lead_meta.has_field("notes"):
            lead_data["notes"] = notes_text
        elif lead_meta.has_field("description"):
            lead_data["description"] = notes_text

    lead = frappe.get_doc(lead_data)
    lead.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "ok": True,
        "lead_name": lead.name,
        "message": _("تم استلام طلبك بنجاح، وسنتواصل معك قريبا"),
    }
