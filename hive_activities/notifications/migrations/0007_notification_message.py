# Generated by Django 5.1.3 on 2024-12-08 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0006_remove_notification_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='message',
            field=models.TextField(default='trust'),
            preserve_default=False,
        ),
    ]
