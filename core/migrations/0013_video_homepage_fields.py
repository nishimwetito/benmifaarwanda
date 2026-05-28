from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_feature_existing_homepage_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='homepage_order',
            field=models.PositiveIntegerField(
                default=0,
                help_text='Lower numbers appear first on the homepage.',
            ),
        ),
        migrations.AddField(
            model_name='video',
            name='show_on_homepage',
            field=models.BooleanField(
                default=False,
                help_text='Display this video in the homepage learning section.',
            ),
        ),
    ]
