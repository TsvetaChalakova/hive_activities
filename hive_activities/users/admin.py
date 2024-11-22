# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import AppUser, UserProfile
#
#
# @admin.register(AppUser)
# class CustomUserAdmin(UserAdmin):
#     model = AppUser
#     list_display = ('email', 'is_active', 'is_staff', 'user_type')
#     list_filter = ('is_active', 'is_staff', 'user_type')
#     ordering = ('email',)
#     search_fields = ('email',)
#
#
# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'first_name', 'last_name', 'created_at', 'updated_at')
#     readonly_fields = ('created_at', 'updated_at')
