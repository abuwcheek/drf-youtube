from django.urls import path
from .views import CreateContentAPIView




urlpatterns = [
     path('create-content', CreateContentAPIView.as_view())

]