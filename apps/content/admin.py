from django.contrib import admin
from .models import Category, Content, View, Like, Comment, PlayList


admin.site.register(Category)
admin.site.register(View)
admin.site.register(Like)
admin.site.register(Comment)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
     list_display = ('id', 'title', 'description', 'author', 'created_at')
     list_display_links = ('id', 'title')
     search_fields = ('title', 'description')
     list_filter = ('category',)
     ordering = ('-created_at',)

     

@admin.register(PlayList)
class PlayListAdmin(admin.ModelAdmin):
     list_display = ('id', 'title', 'user', 'created_at')
     list_display_links = ('id', 'title')