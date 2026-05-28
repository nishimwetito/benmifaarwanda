from django.db import migrations


def seed_services(apps, schema_editor):
    Service = apps.get_model('core', 'ProfessionalSupportService')
    if Service.objects.exists():
        return
    Service.objects.bulk_create([
        Service(
            title='Project Design & M&E',
            description='Professional framework design, monitoring, and evaluation for community development and social impact projects.',
            image_url='https://images.pexels.com/photos/3182812/pexels-photo-3182812.jpeg?auto=compress&cs=tinysrgb&w=800',
            image_alt='Project Design & M&E',
            tag_label='Data-Driven',
            icon_class='bi-diagram-3-fill',
            order=1,
        ),
        Service(
            title='Business Document Design',
            description='High-impact design for company profiles, annual reports, funding proposals, and corporate presentations.',
            image_url='https://images.pexels.com/photos/3183153/pexels-photo-3183153.jpeg?auto=compress&cs=tinysrgb&w=800',
            image_alt='Business Document Design',
            tag_label='Professional Branding',
            icon_class='bi-file-earmark-richtext-fill',
            order=2,
        ),
        Service(
            title='Business Planning',
            description='Strategic business modeling, market analysis, and financial forecasting to launch or scale your venture.',
            image_url='https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg?auto=compress&cs=tinysrgb&w=800',
            image_alt='Business Planning',
            tag_label='Strategic Growth',
            icon_class='bi-rocket-takeoff-fill',
            order=3,
        ),
    ])


def unseed_services(apps, schema_editor):
    Service = apps.get_model('core', 'ProfessionalSupportService')
    Service.objects.filter(
        title__in=[
            'Project Design & M&E',
            'Business Document Design',
            'Business Planning',
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_professionalsupportservice_tag_icon'),
    ]

    operations = [
        migrations.RunPython(seed_services, unseed_services),
    ]
