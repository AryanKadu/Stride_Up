from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "username", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "username", "password", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "role", "is_active", "is_staff"),
        }),
    )
    search_fields = ("email", "username")
    ordering = ("email",)

admin.site.register(CustomUser, CustomUserAdmin)
