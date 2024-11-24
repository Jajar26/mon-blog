# Generated by Django 5.1.3 on 2024-11-22 19:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_rename_reservation_date_equipment_reservation_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athlete',
            name='current_equipment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='blog.equipment'),
        ),
    ]