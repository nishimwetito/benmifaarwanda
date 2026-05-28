from django.db import migrations


SUPPORT_SERVICES = [
    {
        'title': 'IT Consultancy & Technical Support',
        'description': 'Expert advice on IT infrastructure, hardware/software troubleshooting, and digital systems management.',
        'image_url': 'https://images.pexels.com/photos/1181244/pexels-photo-1181244.jpeg?auto=compress&cs=tinysrgb&w=800',
        'image_alt': 'IT Consultancy',
        'tag_label': 'Technical',
        'icon_class': 'bi-laptop',
        'order': 10,
        'homepage_order': 0,
    },
    {
        'title': 'Digital Literacy Training',
        'description': 'Empowering individuals with essential computer skills, internet safety, and software proficiency.',
        'image_url': 'https://images.pexels.com/photos/3182773/pexels-photo-3182773.jpeg?auto=compress&cs=tinysrgb&w=800',
        'image_alt': 'Digital Literacy',
        'tag_label': 'Training',
        'icon_class': 'bi-mortarboard-fill',
        'order': 11,
        'homepage_order': 1,
    },
    {
        'title': 'Social Media Strategy',
        'description': 'Strategic usage of social platforms for branding, community engagement, and digital marketing.',
        'image_url': 'https://images.pexels.com/photos/607812/pexels-photo-607812.jpeg?auto=compress&cs=tinysrgb&w=800',
        'image_alt': 'Social Media',
        'tag_label': 'Marketing',
        'icon_class': 'bi-share-fill',
        'order': 12,
        'homepage_order': 2,
    },
]


def seed_support_catalog(apps, schema_editor):
    Service = apps.get_model('core', 'ProfessionalSupportService')
    for data in SUPPORT_SERVICES:
        Service.objects.update_or_create(
            title=data['title'],
            defaults={
                **data,
                'show_on_homepage': True,
                'email': 'info@be2sahobe.rw',
            },
        )


def unseed_support_catalog(apps, schema_editor):
    Service = apps.get_model('core', 'ProfessionalSupportService')
    Service.objects.filter(title__in=[s['title'] for s in SUPPORT_SERVICES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_remove_course_model'),
    ]

    operations = [
        migrations.RunPython(seed_support_catalog, unseed_support_catalog),
    ]
