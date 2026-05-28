from django.db import migrations


def feature_existing_videos(apps, schema_editor):
    Video = apps.get_model('core', 'Video')
    if Video.objects.filter(show_on_homepage=True).exists():
        return
    for i, video in enumerate(Video.objects.order_by('-created_at')[:6]):
        video.show_on_homepage = True
        video.homepage_order = i
        video.save(update_fields=['show_on_homepage', 'homepage_order'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_video_homepage_fields'),
    ]

    operations = [
        migrations.RunPython(feature_existing_videos, migrations.RunPython.noop),
    ]
