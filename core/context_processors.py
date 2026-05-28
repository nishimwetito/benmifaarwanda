from urllib.parse import quote

DEFAULT_WHATSAPP = '250783558316'
DEFAULT_MESSAGE = 'Hello BE2SAHOBE LTD, I would like to get in touch.'


def _normalize_whatsapp(raw):
    if not raw:
        return ''
    return ''.join(c for c in str(raw).strip() if c.isdigit())


def _format_whatsapp_display(digits):
    if not digits:
        return ''
    if digits.startswith('250') and len(digits) >= 12:
        return f"+{digits[:3]} {digits[3:5]} {digits[5:8]} {digits[8:]}"
    return f"+{digits}"


def site_settings(request):
    """Site-wide editable content (singleton)."""
    try:
        from .models import SiteSettings
        site = SiteSettings.load()
    except Exception:
        site = None
    return {'site': site}


def site_contact(request):
    """WhatsApp and contact links — driven by Site Settings in the dashboard."""
    digits = DEFAULT_WHATSAPP
    contact_phone = ''
    try:
        from .models import SiteSettings
        site = SiteSettings.load()
        if site:
            if site.whatsapp_number:
                digits = _normalize_whatsapp(site.whatsapp_number) or digits
            contact_phone = (site.contact_phone or '').strip()
    except Exception:
        pass

    display = _format_whatsapp_display(digits)
    base_url = f'https://wa.me/{digits}' if digits else ''
    phone_tel = ''.join(c for c in contact_phone if c.isdigit() or c == '+')
    if phone_tel and not phone_tel.startswith('+'):
        phone_tel = f'+{phone_tel.lstrip("0")}'

    return {
        'whatsapp_number': digits,
        'whatsapp_display': display,
        'whatsapp_url': base_url,
        'whatsapp_url_default': f'{base_url}?text={quote(DEFAULT_MESSAGE)}' if base_url else '',
        'contact_phone_tel': phone_tel or f'+{digits}',
    }
