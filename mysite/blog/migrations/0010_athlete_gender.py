# Generated by Django 5.1.3 on 2024-11-23 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_athlete_current_equipment'),
    ]

    operations = [
        migrations.AddField(
            model_name='athlete',
            name='gender',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
