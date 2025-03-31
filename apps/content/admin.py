from django.contrib import admin
from .models import Category, Content, View, Like, Comment, PlayList


admin.site.register(Category)
admin.site.register(Content)
admin.site.register(View)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(PlayList)