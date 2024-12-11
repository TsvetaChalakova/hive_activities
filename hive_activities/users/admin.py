from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import PermissionDenied
from hive_activities.users.models import AppUser, UserProfile, RoleRequest


@admin.register(AppUser)
class CustomUserAdmin(UserAdmin):
    model = AppUser

    list_display = ("email", "is_active", "is_staff", "user_type")

    list_filter = ("is_active", "is_staff", "user_type")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("user_type",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_superuser", "user_type"),
        }),
    )

    search_fields = ("email",)

    ordering = ("pk",)

    def save_model(self, request, obj, form, change):

        if 'Staff Admin' in [group.name for group in obj.groups.all()]:
            if not request.user.is_superuser:
                raise PermissionDenied("Only superusers can add users to the Staff Admin group.")

        super().save_model(request, obj, form, change)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = ('user', 'first_name', 'last_name', 'created_at', 'updated_at')

    readonly_fields = ('created_at', 'updated_at')


@admin.register(RoleRequest)
class RoleRequestAdmin(admin.ModelAdmin):

    list_display = ('user', 'requested_role', 'approved', 'created_at')
