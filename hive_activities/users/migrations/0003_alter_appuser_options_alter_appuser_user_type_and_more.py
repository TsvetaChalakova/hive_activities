# Generated by Django 5.1.3 on 2024-12-01 13:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appuser',
            options={'ordering': ['pk'], 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterField(
            model_name='appuser',
            name='user_type',
            field=models.CharField(choices=[('TEAM_MEMBER', 'Team Member'), ('PROJECT_MANAGER', 'Project Manager'), ('VIEWER', 'Viewer'), ('STAFF_ADMIN', 'Staff Admin'), ('SUPER_ADMIN', 'Super Admin')], default='TEAM_MEMBER', max_length=20),
        ),
        migrations.CreateModel(
            name='RoleRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_role', models.CharField(choices=[('PROJECT_MANAGER', 'Project Manager'), ('VIEWER', 'Viewer')], max_length=20)),
                ('approved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='role_request', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
