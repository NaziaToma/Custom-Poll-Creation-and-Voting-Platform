# Generated by Django 5.1 on 2024-08-13 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_choice_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='phone_number',
        ),
    ]
