from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_booking_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Booking',
        ),
    ]
