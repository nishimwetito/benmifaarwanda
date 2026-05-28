from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_feature_existing_homepage_videos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='course',
        ),
        migrations.RemoveField(
            model_name='pdfguide',
            name='course',
        ),
        migrations.RemoveField(
            model_name='slide',
            name='course',
        ),
        migrations.DeleteModel(
            name='Course',
        ),
    ]
