from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_sitesettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='homepage_order',
            field=models.PositiveIntegerField(default=0, help_text='Lower numbers appear first on the homepage.'),
        ),
        migrations.AddField(
            model_name='course',
            name='show_on_homepage',
            field=models.BooleanField(default=False, help_text='Display this resource on the landing page.'),
        ),
        migrations.AddField(
            model_name='professionalsupportservice',
            name='homepage_order',
            field=models.PositiveIntegerField(default=0, help_text='Lower numbers appear first on the homepage (among featured items).'),
        ),
        migrations.AddField(
            model_name='professionalsupportservice',
            name='show_on_homepage',
            field=models.BooleanField(default=False, help_text='Display this service on the landing page.'),
        ),
    ]
