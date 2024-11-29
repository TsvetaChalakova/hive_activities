# Generated by Django 5.1.3 on 2024-11-29 13:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_alter_note_activity_alter_note_created_by'),
        ('notifications', '0003_alter_notification_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='note',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.note'),
        ),
    ]
