from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_professionalsupportservice'),
    ]

    operations = [
        migrations.AddField(
            model_name='professionalsupportservice',
            name='tag_label',
            field=models.CharField(blank=True, help_text='e.g. Data-Driven, Professional Branding', max_length=80),
        ),
        migrations.AddField(
            model_name='professionalsupportservice',
            name='icon_class',
            field=models.CharField(
                default='bi-briefcase-fill',
                help_text='Bootstrap icon class, e.g. bi-diagram-3-fill',
                max_length=80,
            ),
        ),
    ]
