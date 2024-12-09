from django.db.models.signals import post_migrate


def create_groups_and_permissions(sender, **kwargs):

    apps = kwargs['apps']
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    groups_data = {
        'Project Manager': [21, 22, 24, 25, 28, 32, 33, 38, 37, 34, 36, 39, 40, 41, 42, 48],
        'Team Member': [21, 22, 24, 25, 28, 32, 36, 42, 48, 50],
        'Staff Admin': [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 38, 37, 34, 35, 36, 39, 40, 41, 42, 43, 44, 46, 48, 50],
        'Super Admin': [21, 22, 23, 24, 1, 2, 3, 4, 9, 10, 11, 12, 5, 6, 7, 8, 13, 14, 15, 16, 71, 72, 73, 74, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 25, 26, 27, 28, 29, 30, 31, 32, 33, 38, 37, 34, 35, 36, 39, 40, 41, 42, 17, 18, 19, 20, 43, 44, 45, 46, 47, 48, 49, 50],
        'Viewer': [24, 28, 32, 36, 42],
    }

    for group_name, permission_ids in groups_data.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        permissions = Permission.objects.filter(id__in=permission_ids)
        group.permissions.set(permissions)




