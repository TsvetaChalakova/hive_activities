# Generated by Django 5.1.3 on 2024-11-24 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter a unique project title', max_length=200, unique=True)),
                ('description', models.TextField(blank=True, help_text='Describe the project goals and scope', null=True)),
                ('status', models.CharField(choices=[('IN_PROGRESS', 'In Progress'), ('ON_HOLD', 'On Hold'), ('COMPLETED', 'Completed')], default='IN_PROGRESS', max_length=20)),
                ('start_date', models.DateField(help_text='Project start date')),
                ('due_date', models.DateField(help_text='Project deadline')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
                'ordering': ['-created_at'],
                'permissions': [('can_change_project_status', 'Can change project status'), ('can_assign_team_members', 'Can assign team members')],
            },
        ),
        migrations.CreateModel(
            name='ProjectMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('MEMBER', 'Team Member'), ('MANAGER', 'Project Manager')], max_length=20)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Project Membership',
                'verbose_name_plural': 'Project Memberships',
            },
        ),
    ]
