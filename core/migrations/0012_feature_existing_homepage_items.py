from django.db import migrations


def feature_existing(apps, schema_editor):
    Course = apps.get_model('core', 'Course')
    Service = apps.get_model('core', 'ProfessionalSupportService')

    for i, course in enumerate(Course.objects.order_by('-created_at')[:6]):
        course.show_on_homepage = True
        course.homepage_order = i
        course.save(update_fields=['show_on_homepage', 'homepage_order'])

    for i, service in enumerate(Service.objects.order_by('order', '-created_at')[:6]):
        service.show_on_homepage = True
        service.homepage_order = i
        service.save(update_fields=['show_on_homepage', 'homepage_order'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_homepage_featured_fields'),
    ]

    operations = [
        migrations.RunPython(feature_existing, migrations.RunPython.noop),
    ]
