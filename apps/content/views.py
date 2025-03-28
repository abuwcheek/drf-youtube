from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.generics import (CreateAPIView, UpdateAPIView,
                                      DestroyAPIView, RetrieveAPIView, 
                                      ListAPIView)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import  Category, CommentLike, CommentReply, Content, View, Like, Comment
from .serializers import (ContentSerializers, UpdateCommentReplyToContentSerializers, 
                          UpdateContentSerializers, 
                          CommentToContenSerializers, UpdateCommentToContentSerializers, 
                          CommentReplyToContentSerializers, CommentListToContentSerializers)
from .paginations import MyPageNumberPagination
from .permissions import IsHasChanel, IsOwner, IsAuthor
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
               'message': "video qo'shdingiz",
               'data': self.serializer_class(instance=content, context={'request': request}).data
          }

          return Response(data=data)



class UpdateContentAPIView(UpdateAPIView):
     permission_classes = [IsAuthenticated, IsOwner]
     serializer_class = UpdateContentSerializers
     queryset = Content.objects.filter(is_active=True)

     def update(self, request, *args, **kwargs):
          super().update(request, *args, **kwargs)
          data = {
               'status': True,
               'message': 'videoni o`zgartirdingiz'
          }
          return Response(data=data)



class DeleteContentAPIView(DestroyAPIView):
     permission_classes = [IsAuthenticated, IsOwner]
     serializer_class = UpdateContentSerializers
     queryset = Content.objects.filter(is_active=True)

     def destroy(self, request, *args, **kwargs):
          super().destroy(request, *args, **kwargs)

          data = {
               'status': True,
               'message': "videoni o'chirib tashladingiz"
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



class UpdateCommentToContentAPIView(UpdateAPIView):
     permission_classes = [IsAuthenticated, IsAuthor]
     serializer_class = UpdateCommentToContentSerializers
     queryset = Comment.objects.filter(is_active=True)


     def update(self, request, *args, **kwargs):
          instance = self.get_object()
          if instance.user != request.user:
               data = {
                    'status': False,
                    'message': "bu comment sizga tegishli emas"
               }
               return Response(data=data)
          
          super().update(request, *args, **kwargs)
          data = {
               'status': True,
               'message': "comment o'zgartirildi"
          }
          return Response(data=data)



class DeleteCommentToContentAPIView(DestroyAPIView):
     permission_classes = [IsAuthenticated, IsAuthor]
     serializer_class = CommentToContenSerializers
     queryset = Comment.objects.filter(is_active=True)


     def destroy(self, request, *args, **kwargs):
          instance = self.get_object()
          if instance.user != request.user:
               data = {
                    'status': False,
                    'message': "bu comment sizga tegishli emas"
               }
               return Response(data=data)

          super().destroy(request, *args, **kwargs)
          data = {
               'status': True,
               'message': "comment o'chirildi"
          }
          return Response(data=data)



class LikeCommentToContentAPIView(APIView):
     permission_classes = [IsAuthenticated]

     def post(self, request):
          comment = get_object_or_404(Comment, id=request.data['comment'])
          like = CommentLike.objects.filter(comment=comment, user=request.user).first()
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
               CommentLike.objects.create(comment=comment, user=request.user, dislike=dislike)
               data = {
                    'status': True,
                    'message': "like bosildi"
               }
          
          return Response(data=data)



class CommentReplyToContentAPIView(CreateAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = CommentReplyToContentSerializers
     queryset = CommentReply.objects.all()



class UpdateCommentReplyToContentAPIView(UpdateAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = UpdateCommentReplyToContentSerializers
     queryset = CommentReply.objects.filter(is_active=True)

     def update(self, request, *args, **kwargs):
          super().update(request, *args, **kwargs)
          data = {
               'status': True,
               'message': "comment reply o'zgartirildi"
          }
          return Response(data=data)



class DestroyCommentReplyToContentAPIView(DestroyAPIView):
     permission_classes = [IsAuthenticated, IsAuthor]
     serializer_class = UpdateCommentReplyToContentSerializers
     queryset = CommentReply.objects.filter(is_active=True)


     def delete(self, request, *args, **kwargs):
          super().delete(request, *args, **kwargs)
          data = {
               'status': True,
               'message': "comment replay o'chirib tashlandi"
          }
          return Response(data=data)



class CommentListToContentAPIView(ListAPIView):
     permission_classes = [AllowAny]
     serializer_class = CommentListToContentSerializers
     queryset = Comment.objects.filter(is_avtive=True)

     def get_queryset(self):
          id = self.kwargs.get('pk')
          content = get_object_or_404(Comment, id=id)
          comments = content.content_comments.filter(is_active=True)
          return comments