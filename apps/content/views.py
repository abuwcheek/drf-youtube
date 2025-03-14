from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import  Category, Content, View, Like, Comment
from .serializers import ContentSerializers
from .paginations import MyPageNumberPagination
from .permissions import IsHasChanel
from apps.chanel.models import Chanel
from apps.chanel.serializers import GetChanelDataSerializers



class CreateContentAPIView(APIView):
     permission_classes = [IsAuthenticated, IsHasChanel]
     serializer_class = ContentSerializers

     def post(self, request):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid(raise_exception=True)
          content = serializer.save()
          chanel = request.user.chanel
          content.author = chanel
          content.save()

          data = {
               'status': True,
               'message': "Video qo'shdingiz",
               'data': self.serializer_class(instance=content, context={'request': request}).data
          }

          return Response(data=data)