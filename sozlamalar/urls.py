from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('content/', include('apps.content.urls')),
    path('chanel/', include('apps.chanel.urls')),
]
