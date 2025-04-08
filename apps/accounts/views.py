from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import CustomRegisterUserSerializer, CustomUpdateUserSerializer, CustomRetrieveUserSerializer
from .models import CustomUser
from apps.chanel.serializers import GetChanelDataSerializers
from apps.chanel.models import Chanel


class CustomRegisterUserView(APIView):
     permission_classes = [AllowAny]

     def post(self, request):
          try:
               email = request.user.email
               username = request.user.username
               if CustomUser.objects.filter(username=username).exists():
                    data = {
                         'status': False,
                         'message': "Bu username orqali siz allaqachon ro'yxatdan o'tgansiz"
                    }
                    return Response(data=data)
               if CustomUser.objects.filter(email=email).exists():
                    data = {
                         'status': False,
                         'message': "Bu email orqali siz allaqachon ro'yxatdan o'tgansiz"
                    }
                    return Response(data=data)
          except Exception as e:
               pass

          serializer = CustomRegisterUserSerializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()

          data = {
               'status': True,
               'message': "Muvaffaqiyatli ro'yxatdan o'tdingiz",
               'data': serializer.data
          }
          return Response(data=data)



class CustomUpdateUserView(APIView):
     permission_classes = [IsAuthenticated]

     def patch(self, request):
          user = get_object_or_404(CustomUser, email=request.user.email)
          serializer = CustomUpdateUserSerializer(user, data=request.data, partial=True)
          if serializer.is_valid(raise_exception=True):
               serializer.save()

               data = {
                    'status': True,
                    'message': "Muvaffaqiyatli yangiladingiz",
                    'data': serializer.data
               }
               return Response(data=data)
          
          data = {
               'status': False,
               'message': "Xatolik yuz berdi",
               'data': serializer.errors
          }
          return Response(data=data)



class CustomRetrieveUserView(APIView):
     permission_classes = [IsAuthenticated]

     def get(self, request):
          user = get_object_or_404(CustomUser, email=request.user.email)
          serializer = CustomRetrieveUserSerializer(user)

          data = {
               'status': True,
               'data': serializer.data
          }
          return Response(data=data)



class CustomDeleteUserView(APIView):
     permission_classes = [IsAuthenticated]
     
     def delete(self, request):
          user = get_object_or_404(CustomUser, email=request.user.email)
          user.delete()

          data = {
               'status': True,
               'message': "Muvaffaqiyatli o'chirdingiz"
          }
          return Response(data=data)



class FollowUnfollowToChanelAPIView(APIView):
     permission_classes = [IsAuthenticated]
     
     def post(self, request):
          user = request.user
          chanel = get_object_or_404(Chanel, id=request.data['chanel'])

          if user in chanel.subscribers.all():
               chanel.subscribers.remove(user)
               data = {
                    'status': True,
                    'message': "obuna bekor qilindi"
               }
               return Response(data=data)
          else:
               chanel.subscribers.add(user)
               data = {
                    'status': True,
                    'message': "obuna bo'ldingiz"
               }
               return Response(data=data)



class FollowChanelsListView(ListAPIView):
     permission_classes = [IsAuthenticated]
     serializers_class = GetChanelDataSerializers

     def get(self, request, *args, **kwargs):
          user = request.user
          chanel = user.chanel_subscribed.all()
          serializer = GetChanelDataSerializers(chanel, many=True)
          data = {
               'status': True,
               'data': serializer.data
          }
          return Response(data=data)
     
     def get_serializer_context(self):
          context = super().get_serializer_context()
          context['request'] = self.request  # bu MUHIM!
          return context