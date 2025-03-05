from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active',]
    list_display_links = ['id', 'username', 'email']
    list_filter = ['is_active', 'is_staff']
    list_editable = ['is_active']