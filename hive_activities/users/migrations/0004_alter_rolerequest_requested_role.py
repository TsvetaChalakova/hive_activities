# Generated by Django 5.1.3 on 2024-12-01 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_appuser_options_alter_appuser_user_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rolerequest',
            name='requested_role',
            field=models.CharField(choices=[('PROJECT_MANAGER', 'Project Manager')], max_length=20),
        ),
    ]