from django.db import migrations


def create_groups_and_permissions(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Create groups with their permissions
    groups_data = {
        'Project Manager': [21, 22, 24, 25, 28, 32, 33, 38, 37, 34, 36, 39, 40, 41, 42, 48],
        'Team Member': [21, 22, 24, 25, 28, 32, 36, 42, 48, 50],
        'Staff Admin': [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 38, 37, 34, 35, 36, 39, 40, 41, 42, 43, 44, 46, 48, 50],
        'Super Admin': [21, 22, 23, 24, 1, 2, 3, 4, 9, 10, 11, 12, 5, 6, 7, 8, 13, 14, 15, 16, 71, 72, 73, 74, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 25, 26, 27, 28, 29, 30, 31, 32, 33, 38, 37, 34, 35, 36, 39, 40, 41, 42, 17, 18, 19, 20, 43, 44, 45, 46, 47, 48, 49, 50, 75, 76, 77, 78, 79, 80, 81, 82],
        'Viewer': [24, 28, 32, 36, 42]
    }

    for group_name, permission_ids in groups_data.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        permissions = Permission.objects.filter(id__in=permission_ids)
        group.permissions.set(permissions)


def reverse_func(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Project Manager', 'Team Member', 'Staff Admin', 'Super Admin', 'Viewer']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0008_userprofile_telephone'),
    ]

    operations = [
        migrations.RunPython(create_groups_and_permissions, reverse_func),
    ]