from django.urls import path
from .views import (CreateContentAPIView, UpdateContentAPIView, 
                    DeleteContentAPIView, RetrieveContentAPIView, 
                    ListContentAPIView)




urlpatterns = [
     path('create-content', CreateContentAPIView.as_view()),
     path('update-content/<int:pk>', UpdateContentAPIView.as_view()),
     path('delete-content/<int:pk>', DeleteContentAPIView.as_view()),
     path('retrieve-content/<int:pk>', RetrieveContentAPIView.as_view()),
     path('list-content', ListContentAPIView.as_view()),
]