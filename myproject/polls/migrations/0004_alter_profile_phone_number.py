# Generated by Django 5.1 on 2024-08-12 12:35

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_profile_phone_number_alter_profile_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+1234567890', max_length=128, region=None),
        ),
    ]
