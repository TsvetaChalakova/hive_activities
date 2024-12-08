# Generated by Django 5.1.3 on 2024-12-08 15:11

import hive_activities.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_alter_projectmembership_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-created_at'], 'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(help_text='Enter a unique project title', max_length=200, unique=True, validators=[hive_activities.core.validators.validate_no_special_characters]),
        ),
    ]
