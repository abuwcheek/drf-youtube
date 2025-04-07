from django.contrib import admin
from .models import Chanel


@admin.register(Chanel)
class ChanelAdmin(admin.ModelAdmin):
     list_display = ('id', 'name', 'user', 'get_username', 'get_subscribers', 'created_at', 'updated_at', 'is_active')
     list_display_links = ('id', 'name', 'user')
     list_filter = ('user', 'subscribers')
     search_fields = ('name', 'user__username')
     ordering = ('-created_at',)
     list_editable = ('is_active',)
     readonly_fields = ('id', 'subscribers', 'created_at', 'updated_at')
     list_per_page = 20

     def get_username(self, obj):
          return obj.user.username if obj.user else "Username"
     
     def get_subscribers(self, obj):
          return obj.subscribers.count() if obj.subscribers else 0