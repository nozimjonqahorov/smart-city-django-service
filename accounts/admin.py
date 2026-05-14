from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "role", "region", "city", "phone", "is_staff")
    list_filter = UserAdmin.list_filter + ("role", "region")
    fieldsets = UserAdmin.fieldsets + (
        ("Smart City ma'lumotlari", {"fields": ("role", "phone", "region", "city", "category", "avatar", "telegram_id")}),
    )
