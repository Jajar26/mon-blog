# Generated by Django 5.1.3 on 2024-11-22 00:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_athlete_age_athlete_email_athlete_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipment',
            name='last_maintenance',
        ),
    ]
