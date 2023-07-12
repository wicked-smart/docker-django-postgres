# Generated by Django 4.2.2 on 2023-07-07 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barfoo', '0003_rename_booking_refid_flightbook_booking_ref'),
    ]

    operations = [
        migrations.AddField(
            model_name='flightbook',
            name='passenger',
            field=models.ManyToManyField(blank=True, null=True, related_name='bookings', to='barfoo.passenger'),
        ),
    ]
