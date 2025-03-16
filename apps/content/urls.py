from django.urls import path
from .views import CreateContentAPIView, UpdateContentAPIView, DeleteContentAPIView




urlpatterns = [
     path('create-content', CreateContentAPIView.as_view()),
     path('update-content/<int:pk>', UpdateContentAPIView.as_view()),
     path('delete-content/<int:pk>', DeleteContentAPIView.as_view()),

]