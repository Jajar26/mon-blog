# Generated by Django 5.1.3 on 2024-11-24 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_alter_athlete_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athlete',
            name='gender',
            field=models.CharField(choices=[('M', 'Homme'), ('F', 'Femme'), ('O', 'Autre')], max_length=1),
        ),
    ]
