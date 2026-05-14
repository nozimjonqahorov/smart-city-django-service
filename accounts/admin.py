from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Viloyat, Tuman

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "role", "region", "city", "phone", "is_staff")
    list_filter = UserAdmin.list_filter + ("role", "region")
    fieldsets = UserAdmin.fieldsets + (
        ("Smart City ma'lumotlari", {"fields": ("role", "phone", "region", "city", "category", "avatar", "telegram_id")}),
    )


@admin.register(Viloyat)
class ViloyatAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Tuman)
class TumanAdmin(admin.ModelAdmin):
    list_display = ("name", "viloyat", "created_at")
    list_filter = ("viloyat",)
    search_fields = ("name", "viloyat__name")
    ordering = ("viloyat", "name")
