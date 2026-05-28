from django.db import migrations, models


def seed_donation_methods(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    obj, _ = SiteSettings.objects.get_or_create(pk=1)
    if obj.donation_methods:
        return
    obj.donation_methods = [
        {
            "title": "Mobile Money (MTN / Airtel)",
            "icon": "bi-phone-fill",
            "rows": [
                {"label": "Merchant code", "value": obj.momo_merchant_code or "123456"},
                {"label": "Phone", "value": obj.contact_phone or ""},
                {"label": "Name", "value": obj.momo_account_name or "BE2SAHOBE LTD"},
            ],
        },
        {
            "title": "Bank transfer",
            "icon": "bi-bank2",
            "rows": [
                {"label": "Bank", "value": obj.bank_name or "Equity Bank Rwanda"},
                {"label": "Account name", "value": obj.bank_account_name or "BE2SAHOBE LIMITED"},
                {"label": "Account number", "value": obj.bank_account_number or "4000 1234 5678 9"},
            ],
        },
    ]
    obj.save(update_fields=["donation_methods"])


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0018_donation_modal_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="donation_methods",
            field=models.JSONField(
                default=list,
                help_text='Donation methods list. Each item: {"title": "...", "icon": "bi-phone-fill", "rows": [{"label":"...","value":"..."}]}',
            ),
        ),
        migrations.RunPython(seed_donation_methods, reverse_code=migrations.RunPython.noop),
    ]

