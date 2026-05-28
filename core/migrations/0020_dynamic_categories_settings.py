from django.db import migrations, models


def seed_categories(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    obj, _ = SiteSettings.objects.get_or_create(pk=1)
    if not obj.video_categories:
        obj.video_categories = ["Training", "Economy", "Farming", "Wellness"]
    if not obj.pdf_categories:
        obj.pdf_categories = ["Manual", "Tracker", "Technical", "Guide"]
    if not obj.slide_categories:
        obj.slide_categories = ["Workshop", "Finance", "Farming", "Health", "Community"]
    if not obj.gallery_categories:
        obj.gallery_categories = ["Impact", "Training", "Farming", "Wellness"]
    obj.save(update_fields=["video_categories", "pdf_categories", "slide_categories", "gallery_categories"])


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0019_donation_methods_list"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="video_categories",
            field=models.JSONField(default=list, help_text="Video categories list"),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="pdf_categories",
            field=models.JSONField(default=list, help_text="PDF guide categories list"),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="slide_categories",
            field=models.JSONField(default=list, help_text="Slides categories list"),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="gallery_categories",
            field=models.JSONField(default=list, help_text="Gallery categories list"),
        ),
        migrations.RunPython(seed_categories, reverse_code=migrations.RunPython.noop),
    ]

