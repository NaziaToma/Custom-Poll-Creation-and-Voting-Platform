# Generated by Django 5.1 on 2024-08-12 16:33

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_alter_profile_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.CharField(default='BD', max_length=2),
        ),
        migrations.AddField(
            model_name='profile',
            name='district',
            field=models.CharField(default='Dhaka', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]
