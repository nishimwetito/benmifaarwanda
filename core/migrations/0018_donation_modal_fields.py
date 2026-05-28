from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0017_home_pillars_settings"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="donation_modal_title",
            field=models.CharField(default="Support our mission", max_length=120),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="donation_modal_subtitle",
            field=models.TextField(
                default="Your contribution helps families grow through holistic education and community support.",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="momo_merchant_code",
            field=models.CharField(blank=True, default="123456", max_length=40),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="momo_account_name",
            field=models.CharField(blank=True, default="BE2SAHOBE LTD", max_length=120),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="bank_name",
            field=models.CharField(blank=True, default="Equity Bank Rwanda", max_length=120),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="bank_account_name",
            field=models.CharField(blank=True, default="BE2SAHOBE LIMITED", max_length=120),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="bank_account_number",
            field=models.CharField(blank=True, default="4000 1234 5678 9", max_length=120),
        ),
    ]

