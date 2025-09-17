# tracker/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, MiniProject

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("username", "email", "password", "role")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "role", "password1", "password2", "is_staff", "is_active"),
        }),
    )
    search_fields = ("username", "email", "role")
    ordering = ("username",)


class MiniProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "trainee", "trainer", "progress", "created_at")
    list_filter = ("trainer", "trainee")
    search_fields = ("title", "description", "trainee__username", "trainer__username")
    ordering = ("-created_at",)


admin.site.register(User, CustomUserAdmin)
admin.site.register(MiniProject, MiniProjectAdmin)
