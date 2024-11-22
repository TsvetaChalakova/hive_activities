# Generated by Django 5.1.3 on 2024-11-22 17:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('TASK_ASSIGNED', 'Task Assigned'), ('TASK_COMPLETED', 'Task Completed'), ('COMMENT_ADDED', 'New Comment'), ('DUE_DATE', 'Due Date Approaching'), ('PROJECT_UPDATE', 'Project Update')], max_length=20)),
                ('title', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('read', models.BooleanField(default=False)),
                ('object_id', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
