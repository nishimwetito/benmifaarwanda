from django.db import migrations, models


DEFAULT_PILLARS = [
    {
        "name": "The Body",
        "description": "Nurturing health through sustainable nutrition, clean water access, and preventive wellness systems.",
        "accent": "#2e7d32",
    },
    {
        "name": "The Mind",
        "description": "Advancing through digital literacy, career pathfinding, and innovative leadership development.",
        "accent": "#1565c0",
    },
    {
        "name": "The Spirit",
        "description": "Building strong foundations through family counseling, mentorship, and faith-based guidance.",
        "accent": "#7b1fa2",
    },
    {
        "name": "Environment & Technology",
        "description": "Integrating home productivity, waste management, and social media literacy into daily life.",
        "accent": "#00acc1",
    },
    {
        "name": "The Economy",
        "description": "Empowering families through KWIGIRA savings, strategic planning & budgeting, business planning, monitoring evaluation and scaling, and business scaling.",
        "accent": "#B5662D",
    },
]


def seed_default_pillars(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    obj, _ = SiteSettings.objects.get_or_create(pk=1)
    if not obj.home_pillars:
        obj.home_pillars = DEFAULT_PILLARS
    if not obj.home_pillars_label:
        obj.home_pillars_label = "Our Framework"
    if not obj.home_pillars_title:
        obj.home_pillars_title = "The Five Foundations of Holistic Living"
    obj.save()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0016_seed_support_catalog_services"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="home_pillars_label",
            field=models.CharField(default="Our Framework", max_length=60),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="home_pillars_title",
            field=models.CharField(default="The Five Foundations of Holistic Living", max_length=120),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="home_pillars",
            field=models.JSONField(
                default=list,
                help_text='List of pillars as JSON objects: [{"name": "...", "description": "...", "accent": "#RRGGBB"}]',
            ),
        ),
        migrations.RunPython(seed_default_pillars, reverse_code=migrations.RunPython.noop),
    ]

