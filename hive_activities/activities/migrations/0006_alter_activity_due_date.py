# Generated by Django 5.1.3 on 2024-12-07 13:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_alter_activity_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 7, 13, 4, 3, 797791, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]