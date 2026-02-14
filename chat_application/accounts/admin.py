from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": ("profile_picture", "is_online", "last_seen"),
        }),
    )

    list_display = (
        "username",
        "email",
        "is_online",
        "is_staff",
    )
