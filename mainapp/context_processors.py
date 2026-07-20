from urllib.parse import quote

from django.conf import settings


def contact_info(request):
    """
    Site contact numbers for every template.

    Primary:
      contact_phone_display / contact_phone_tel / contact_whatsapp_url
    Alternate:
      contact_phone_alt_display / contact_phone_alt_tel / contact_whatsapp_alt_url
    Both (for loops):
      contact_numbers — list of dicts with display, tel, whatsapp_url, label
    """
    whatsapp_message = quote(settings.CONTACT_WHATSAPP_DEFAULT_MESSAGE)
    primary = {
        "display": settings.CONTACT_PHONE_DISPLAY,
        "tel": settings.CONTACT_PHONE_TEL,
        "whatsapp_url": (
            f"https://wa.me/{settings.CONTACT_WHATSAPP_NUMBER}?text={whatsapp_message}"
        ),
        "label": "Primary",
    }
    alternate = {
        "display": settings.CONTACT_PHONE_ALT_DISPLAY,
        "tel": settings.CONTACT_PHONE_ALT_TEL,
        "whatsapp_url": (
            f"https://wa.me/{settings.CONTACT_WHATSAPP_ALT_NUMBER}?text={whatsapp_message}"
        ),
        "label": "Alternate",
    }
    return {
        "contact_phone_display": primary["display"],
        "contact_phone_tel": primary["tel"],
        "contact_whatsapp_url": primary["whatsapp_url"],
        "contact_phone_alt_display": alternate["display"],
        "contact_phone_alt_tel": alternate["tel"],
        "contact_whatsapp_alt_url": alternate["whatsapp_url"],
        "contact_numbers": [primary, alternate],
    }
