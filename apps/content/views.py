from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.generics import (CreateAPIView, UpdateAPIView,
                                      DestroyAPIView, RetrieveAPIView, 
                                      ListAPIView)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import  Category, Content, View, Like, Comment
from .serializers import ContentSerializers, UpdateContentSerializers, CommentToContenSerializers
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



class UpdateContentAPIView(UpdateAPIView):
     permission_classes = [IsAuthenticated, IsHasChanel]
     serializer_class = UpdateContentSerializers
     queryset = Content.objects.filter(is_active=True)

     def update(self, request, *args, **kwargs):
          super().update(request, *args, **kwargs)
          data = {
               'status': True,
               'message': 'Videoni o`zgartirdingiz'
          }
          return Response(data=data)



class DeleteContentAPIView(DestroyAPIView):
     permission_classes = [IsAuthenticated, IsHasChanel]
     serializer_class = UpdateContentSerializers
     queryset = Content.objects.filter(is_active=True)

     def destroy(self, request, *args, **kwargs):
          super().destroy(request, *args, **kwargs)

          data = {
               'status': True,
               'message': "Videoni o'chirib tashladingiz"
          }

          return Response(data=data)



class RetrieveContentAPIView(RetrieveAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = ContentSerializers
     queryset = Content.objects.all()

     def retrieve(self, request, *args, **kwargs):
          if request.user.is_authenticated:
               content = self.get_object()
               user = request.user
               view = View.objects.get_or_create(user=user, content=content)

          return super().retrieve(request, *args, **kwargs)



class ListContentAPIView(ListAPIView):
     permission_classes = [AllowAny]
     serializer_class = ContentSerializers
     queryset = Content.objects.filter(is_active=True)
     pagination_class = MyPageNumberPagination



class LikeToContentAPIView(APIView):
     permission_classes = [IsAuthenticated]

     def post(self, request):
          video_id = request.data.get("video")

          video = get_object_or_404(Content, id=video_id)
          like = Like.objects.filter(video_id=video.id, user=request.user).first()
          dislike = request.data.get('dislike') == 'true'
          if like:
               if like.dislike == dislike:
                    like.delete()
                    data = {
                         'status': True,
                         'message': "like o'chirildi"
                    }
               else:
                    like.dislike = dislike
                    like.save()
                    data = {
                         'status': True,
                         'message': "like o'zgartirildi"
                    }
          else:
               Like.objects.create(video_id=video.id, user=request.user, dislike=dislike)
               data = { 
                    'status': True,
                    "message": "like bosildi"
               }
     
          return Response(data=data)
     


class CommetToContentAPIView(CreateAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = CommentToContenSerializers
     queryset = Comment.objects.all()

     def get_serializer_context(self):
          context = super().get_serializer_context()
          context['user'] = self.request.user
          return context 