from django.urls import path
from .views import ChanelCreateAPIView, GetChanelDataAPIView, DeleteChanelAPIView





urlpatterns = [
     path('create-chanel', ChanelCreateAPIView.as_view(), name='chanel-create'),
     path('get-chanel-data', GetChanelDataAPIView.as_view(), name='chanel-data'),
     path('delete-chanel/<int:pk>', DeleteChanelAPIView.as_view(), name='chanel-delete')
     ]
