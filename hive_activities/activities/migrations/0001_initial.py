# Generated by Django 5.1.3 on 2024-11-22 17:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('activity_type', models.CharField(choices=[('PARENT', 'Parent Activity'), ('CHILD', 'Child Activity')], default='PARENT', max_length=20)),
                ('status', models.CharField(choices=[('OPEN', 'Open'), ('ASSIGNED', 'Assigned'), ('IN_PROGRESS', 'In Progress'), ('PENDING', 'Pending'), ('IN_REVIEW', 'In Review'), ('CLOSED', 'Closed')], default='OPEN', max_length=20)),
                ('priority', models.CharField(choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('URGENT', 'Urgent')], default='LOW', max_length=20)),
                ('due_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='assigned_activities', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_activities', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='activities.activity')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='projects.project')),
            ],
            options={
                'verbose_name_plural': 'Activities',
                'ordering': ['-priority', 'due_date'],
            },
        ),
    ]