# Generated by Django 4.2.20 on 2025-03-21 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0018_rentavehicle'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rentavehicle',
            old_name='phone',
            new_name='phone_number',
        ),
    ]
